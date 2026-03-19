#!/usr/bin/env python3
"""
VOC processor used by the qfd-analysis pipeline.

This module accepts raw VOC inputs (CSV/TXT/JSON) and also structured
requirement-like records, then normalizes them into the requirement contract
consumed by qfd_pipeline.py.
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


TEXT_FIELD_HINTS = [
    "comment",
    "feedback",
    "review",
    "voice",
    "voc",
    "text",
    "content",
    "remark",
    "\u9700\u6c42",
    "\u8bc4\u8bba",
    "\u53cd\u9988",
    "\u610f\u89c1",
]
REQUIREMENT_FIELD_HINTS = [
    "requirement",
    "description",
    "need",
    "label",
    "title",
    "customer_need",
    "customer_requirement",
    "\u9700\u6c42",
    "\u63cf\u8ff0",
]
CATEGORY_FIELD_HINTS = ["category", "cluster", "theme", "topic", "\u7c7b\u578b", "\u7c7b\u522b"]
IMPORTANCE_FIELD_HINTS = ["importance", "priority", "weight", "score", "\u91cd\u8981", "\u6743\u91cd"]
QUOTE_FIELD_HINTS = ["quote", "sample", "example", "evidence", "\u5f15\u7528", "\u6837\u672c", "\u793a\u4f8b"]

GENERIC_ENGLISH = {
    "good",
    "great",
    "better",
    "best",
    "issue",
    "problem",
    "thing",
    "stuff",
    "feature",
    "device",
    "product",
}
GENERIC_CHINESE = {
    "\u5f88\u597d",
    "\u4e0d\u597d",
    "\u95ee\u9898",
    "\u529f\u80fd",
    "\u4ea7\u54c1",
    "\u8bbe\u5907",
    "\u5176\u4ed6",
}
OTHER_CATEGORY = "Other"
OTHER_CATEGORY_ALIASES = {OTHER_CATEGORY, "\u5176\u4ed6"}
EN_STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "that",
    "this",
    "from",
    "have",
    "has",
    "had",
    "very",
    "more",
    "less",
    "make",
    "made",
    "need",
    "needs",
    "want",
    "wants",
    "should",
    "would",
    "could",
    "into",
    "onto",
    "when",
    "while",
    "during",
    "about",
    "because",
    "after",
    "before",
}

PHRASE_PATTERNS = [
    re.compile(r"(?:need|needs|want|wants|should|must|would like)\s+(?:to\s+)?([a-z][a-z0-9 \-/]{3,80})", re.I),
    re.compile(r"(?:too|very|quite)\s+([a-z][a-z0-9 \-/]{3,40})", re.I),
    re.compile(r"(?:not enough|lacks?|missing)\s+([a-z][a-z0-9 \-/]{3,50})", re.I),
    re.compile("(?:\u5e0c\u671b|\u9700\u8981|\u6700\u597d|\u5efa\u8bae|\u5e94\u8be5)(.{2,24})"),
    re.compile("(?:\u592a|\u4e0d\u591f)(.{1,16})"),
]


def _pick_field(headers: Iterable[str], hints: Iterable[str]) -> Optional[str]:
    normalized = [(header, str(header).strip().lower()) for header in headers if str(header).strip()]
    for header, header_lower in normalized:
        if any(hint in header_lower for hint in hints):
            return header
    return None


def _normalize_field_name(field_name: Any) -> str:
    return re.sub(r"[\s\-]+", "_", str(field_name).strip().lower())


def _field_matches(field_name: Any, hints: Iterable[str]) -> bool:
    normalized = _normalize_field_name(field_name)
    return any(hint in normalized for hint in hints)


def _append_text_values(target: List[str], value: Any) -> None:
    if isinstance(value, list):
        target.extend(clean_text(str(item)) for item in value if clean_text(str(item)))
        return
    if value is not None and clean_text(str(value)):
        target.append(clean_text(str(value)))


def clean_text(text: str) -> str:
    text = text.replace("\ufeff", " ")
    text = text.replace("\uFF0C", ", ").replace("\u3002", ". ").replace("\uFF1B", "; ")
    text = re.sub(r"[\t\r\n]+", " ", text)
    text = re.sub(r"^[\-\*\d\.\)\(]+", "", text.strip())
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"[^\w\s\u4e00-\u9fff,.;:!?/%+\-()'\"#&]", "", text)
    return text.strip(" -;:,")


def _safe_float(value: Any) -> Optional[float]:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _is_cjk(ch: str) -> bool:
    return "\u4e00" <= ch <= "\u9fff"


def _normalize_token(token: str) -> str:
    token = token.strip().lower()
    if not token:
        return ""
    if token.endswith("ies") and len(token) > 4:
        token = token[:-3] + "y"
    elif token.endswith("s") and len(token) > 3 and not token.endswith("ss"):
        token = token[:-1]
    return token


def _tokenize_text(text: str) -> List[str]:
    tokens = [_normalize_token(token) for token in re.findall(r"[a-z0-9]+", text.lower())]
    tokens = [token for token in tokens if token and token not in EN_STOPWORDS]
    cjk_chars = [ch for ch in text if _is_cjk(ch)]
    for idx in range(max(0, len(cjk_chars) - 1)):
        tokens.append("".join(cjk_chars[idx : idx + 2]))
    return tokens


def _candidate_from_quote(text: str) -> List[str]:
    cleaned = clean_text(text)
    if not cleaned:
        return []

    candidates: List[str] = []
    for pattern in PHRASE_PATTERNS:
        for match in pattern.findall(cleaned):
            phrase = clean_text(match if isinstance(match, str) else " ".join(match))
            if phrase:
                candidates.append(phrase)

    english_chunks = re.findall(r"[a-zA-Z][a-zA-Z0-9/\- ]{4,60}", cleaned)
    candidates.extend(clean_text(chunk) for chunk in english_chunks)
    chinese_chunks = re.findall(r"[\u4e00-\u9fff]{2,18}", cleaned)
    candidates.extend(clean_text(chunk) for chunk in chinese_chunks)
    return [candidate for candidate in candidates if candidate]


def _description_score(candidate: str, category: str, frequency: int = 1) -> float:
    text = clean_text(candidate)
    if not text:
        return -1.0

    lower = text.lower()
    words = [token for token in re.findall(r"[a-z0-9]+", lower) if token not in EN_STOPWORDS]
    cjk_count = sum(1 for ch in text if _is_cjk(ch))
    score = 0.0

    if 6 <= len(text) <= 48:
        score += 1.2
    elif 4 <= len(text) <= 64:
        score += 0.6

    if len(words) >= 2:
        score += 1.4
    elif cjk_count >= 3:
        score += 1.2

    if lower in GENERIC_ENGLISH or text in GENERIC_CHINESE:
        score -= 2.0

    if category and category not in OTHER_CATEGORY_ALIASES and category.lower() in lower:
        score += 0.4

    score += min(float(frequency), 4.0) * 0.2
    score -= abs(len(words) - 4) * 0.08
    return score


def is_low_signal_description(text: str) -> bool:
    cleaned = clean_text(text)
    if not cleaned:
        return True
    if cleaned in GENERIC_CHINESE:
        return True

    lower = cleaned.lower()
    if lower in GENERIC_ENGLISH:
        return True

    words = [token for token in re.findall(r"[a-zA-Z0-9]+", lower) if token not in EN_STOPWORDS]
    cjk_count = sum(1 for ch in cleaned if _is_cjk(ch))
    if cjk_count > 0:
        return cjk_count < 2
    return len(words) < 2


def categorize_requirement(text: str) -> str:
    categories = {
        "Power / Runtime": [
            "\u7535\u6c60",
            "\u7eed\u822a",
            "\u5145\u7535",
            "\u7535\u91cf",
            "\u5f85\u673a",
            "runtime",
            "battery",
            "charge",
            "power",
        ],
        "Portability": [
            "\u91cd\u91cf",
            "\u8f7b",
            "\u4fbf\u643a",
            "\u643a\u5e26",
            "\u5927\u5c0f",
            "\u5c3a\u5bf8",
            "\u4f53\u79ef",
            "portable",
            "travel",
        ],
        "Performance": [
            "\u901f\u5ea6",
            "\u5feb",
            "\u6162",
            "\u5361\u987f",
            "\u6d41\u7545",
            "\u6027\u80fd",
            "\u8fd0\u884c",
            "performance",
            "latency",
            "response",
        ],
        "Durability": [
            "\u8010\u7528",
            "\u7ed3\u5b9e",
            "\u575a\u56fa",
            "\u6454",
            "\u9632\u62a4",
            "\u5bff\u547d",
            "\u8d28\u91cf",
            "durable",
            "reliable",
        ],
        "Protection": [
            "\u9632\u6c34",
            "\u9632\u5c18",
            "ip",
            "\u5bc6\u5c01",
            "\u9632\u6454",
            "waterproof",
            "dust",
        ],
        "Display": [
            "\u5c4f\u5e55",
            "\u663e\u793a",
            "\u4eae\u5ea6",
            "\u6e05\u6670",
            "\u5206\u8fa8\u7387",
            "display",
            "screen",
            "brightness",
        ],
        "Controls": [
            "\u64cd\u4f5c",
            "\u6309\u952e",
            "\u89e6\u6478",
            "\u754c\u9762",
            "\u6613\u7528",
            "setup",
            "control",
            "usability",
        ],
        "Connectivity": [
            "\u8fde\u63a5",
            "\u84dd\u7259",
            "wifi",
            "\u7f51\u7edc",
            "\u4fe1\u53f7",
            "connect",
            "wireless",
            "bluetooth",
        ],
        "Storage": [
            "\u5b58\u50a8",
            "\u5185\u5b58",
            "\u7a7a\u95f4",
            "\u5bb9\u91cf",
            "storage",
            "memory",
        ],
        "Appearance": [
            "\u5916\u89c2",
            "\u989c\u8272",
            "\u8bbe\u8ba1",
            "\u7f8e\u89c2",
            "\u597d\u770b",
            "design",
            "look",
        ],
        "Price": [
            "\u4ef7\u683c",
            "\u8d35",
            "\u4fbf\u5b9c",
            "\u6027\u4ef7\u6bd4",
            "\u6210\u672c",
            "price",
            "cost",
        ],
        "Service": [
            "\u670d\u52a1",
            "\u552e\u540e",
            "\u4fdd\u4fee",
            "\u5ba2\u670d",
            "\u652f\u6301",
            "service",
            "support",
            "warranty",
        ],
        "Noise / Comfort": [
            "\u566a\u97f3",
            "noise",
            "quiet",
            "fan",
            "\u9707\u52a8",
            "comfort",
        ],
    }

    text_lower = text.lower()
    for category, keywords in categories.items():
        if any(keyword in text_lower for keyword in keywords):
            return category
    return OTHER_CATEGORY


def _normalize_requirement_record(record: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    description = ""
    category = ""
    importance = None
    frequency = 1
    sample_quotes: List[str] = []

    for key in REQUIREMENT_FIELD_HINTS:
        if key in record and str(record[key]).strip():
            description = clean_text(str(record[key]))
            break
    if not description and "name" in record and str(record["name"]).strip():
        description = clean_text(str(record["name"]))
    if not description:
        return None

    for key in CATEGORY_FIELD_HINTS:
        if key in record and str(record[key]).strip():
            category = clean_text(str(record[key]))
            break
    if not category:
        category = categorize_requirement(description)

    for key in IMPORTANCE_FIELD_HINTS:
        if key in record:
            importance = _safe_float(record[key])
            if importance is not None:
                break

    raw_frequency = record.get("frequency") or record.get("count") or record.get("mentions")
    try:
        if raw_frequency is not None:
            frequency = max(1, int(raw_frequency))
    except (TypeError, ValueError):
        frequency = 1

    for key, value in record.items():
        if _field_matches(key, QUOTE_FIELD_HINTS):
            _append_text_values(sample_quotes, value)

    if not sample_quotes:
        for key in QUOTE_FIELD_HINTS + TEXT_FIELD_HINTS:
            _append_text_values(sample_quotes, record.get(key))

    if not sample_quotes:
        sample_quotes = [description]

    return {
        "description": description,
        "importance": importance,
        "frequency_in_voc": frequency,
        "category": category,
        "sample_quotes": list(dict.fromkeys(sample_quotes))[:3],
        "user_confirmed": importance is not None,
    }


def _looks_like_requirement_record(record: Dict[str, Any]) -> bool:
    keys = {str(key).strip().lower() for key in record.keys()}
    return any(hint in keys for hint in REQUIREMENT_FIELD_HINTS) or "requirements" in keys


def _extract_text_record(record: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    text_value = ""
    category = ""
    for key in TEXT_FIELD_HINTS + REQUIREMENT_FIELD_HINTS + ["summary", "body", "message"]:
        if key in record and str(record[key]).strip():
            text_value = clean_text(str(record[key]))
            break
    if not text_value:
        return None

    for key in CATEGORY_FIELD_HINTS:
        if key in record and str(record[key]).strip():
            category = clean_text(str(record[key]))
            break
    return {
        "original": text_value,
        "cleaned": text_value,
        "category_hint": category,
    }


def load_voc_file(file_path: str) -> Dict[str, Any]:
    path = Path(file_path)
    suffix = path.suffix.lower()
    raw_entries: List[Dict[str, Any]] = []
    structured_requirements: List[Dict[str, Any]] = []
    detected_fields: Dict[str, Any] = {"source_format": suffix.lstrip(".")}

    if suffix == ".csv":
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = reader.fieldnames or []
            detected_fields["headers"] = fieldnames
            text_field = _pick_field(fieldnames, TEXT_FIELD_HINTS)
            req_field = _pick_field(fieldnames, REQUIREMENT_FIELD_HINTS)
            category_field = _pick_field(fieldnames, CATEGORY_FIELD_HINTS)
            detected_fields["text_field"] = text_field
            detected_fields["requirement_field"] = req_field
            for row in reader:
                if not isinstance(row, dict):
                    continue
                if req_field and row.get(req_field):
                    normalized = _normalize_requirement_record(row)
                    if normalized:
                        structured_requirements.append(normalized)
                        continue
                text_key = text_field or req_field
                if text_key and row.get(text_key):
                    raw_entries.append(
                        {
                            "original": clean_text(str(row[text_key])),
                            "cleaned": clean_text(str(row[text_key])),
                            "category_hint": clean_text(str(row.get(category_field, ""))) if category_field else "",
                        }
                    )

    elif suffix == ".txt":
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                cleaned = clean_text(line)
                if cleaned and not cleaned.startswith("#"):
                    raw_entries.append({"original": cleaned, "cleaned": cleaned, "category_hint": ""})

    elif suffix == ".json":
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)

        records: List[Any]
        if isinstance(payload, dict):
            if isinstance(payload.get("requirements"), list):
                records = payload["requirements"]
                detected_fields["json_mode"] = "requirements"
            elif isinstance(payload.get("voc"), list):
                records = payload["voc"]
                detected_fields["json_mode"] = "voc"
            elif isinstance(payload.get("entries"), list):
                records = payload["entries"]
                detected_fields["json_mode"] = "entries"
            elif isinstance(payload.get("records"), list):
                records = payload["records"]
                detected_fields["json_mode"] = "records"
            else:
                records = [payload]
                detected_fields["json_mode"] = "object"
        elif isinstance(payload, list):
            records = payload
            detected_fields["json_mode"] = "list"
        else:
            records = []

        for item in records:
            if isinstance(item, str):
                cleaned = clean_text(item)
                if cleaned:
                    raw_entries.append({"original": cleaned, "cleaned": cleaned, "category_hint": ""})
                continue
            if not isinstance(item, dict):
                continue
            if _looks_like_requirement_record(item):
                normalized = _normalize_requirement_record(item)
                if normalized:
                    structured_requirements.append(normalized)
                    continue
            extracted = _extract_text_record(item)
            if extracted:
                raw_entries.append(extracted)

    else:
        return {
            "success": False,
            "error": f"Unsupported VOC file format: {path.suffix}",
        }

    deduped_entries: List[Dict[str, Any]] = []
    seen_raw: set[str] = set()
    for entry in raw_entries:
        cleaned = clean_text(str(entry.get("cleaned", "")))
        if not cleaned or cleaned in seen_raw:
            continue
        seen_raw.add(cleaned)
        deduped_entries.append(
            {
                "original": str(entry.get("original", cleaned)),
                "cleaned": cleaned,
                "category_hint": str(entry.get("category_hint", "")),
            }
        )

    deduped_requirements: List[Dict[str, Any]] = []
    seen_descriptions: set[str] = set()
    for requirement in structured_requirements:
        description = clean_text(str(requirement.get("description", "")))
        if not description or description.lower() in seen_descriptions:
            continue
        seen_descriptions.add(description.lower())
        requirement["description"] = description
        deduped_requirements.append(requirement)

    input_mode = "structured_requirements" if deduped_requirements else "raw_voc"
    return {
        "success": bool(deduped_entries or deduped_requirements),
        "input_mode": input_mode,
        "detected_fields": detected_fields,
        "entries": deduped_entries,
        "structured_requirements": deduped_requirements,
        "total_raw_entries": len(raw_entries),
        "total_unique_entries": len(deduped_entries),
    }


def extract_keywords(text: str) -> List[str]:
    candidates = _candidate_from_quote(text)
    if candidates:
        return candidates[:6]

    tokens = [token for token in _tokenize_text(text) if len(token) > 1]
    if not tokens:
        return []
    counts = Counter(tokens)
    return [token for token, _ in counts.most_common(6)]


def cluster_voc_entries(entries: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    clustered: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for entry in entries:
        cleaned = clean_text(str(entry.get("cleaned", "")))
        if len(cleaned) < 4:
            continue
        category = str(entry.get("category_hint") or categorize_requirement(cleaned))
        clustered[category].append(
            {
                "original": str(entry.get("original", cleaned)),
                "cleaned": cleaned,
                "keywords": extract_keywords(cleaned),
            }
        )
    return dict(clustered)


def _select_requirement_description(entries: List[Dict[str, Any]], category: str) -> str:
    candidate_counts: Counter[str] = Counter()
    for entry in entries:
        candidate_counts[clean_text(entry.get("cleaned", ""))] += 1
        for keyword in entry.get("keywords", []):
            candidate_counts[clean_text(keyword)] += 1
        for quote_candidate in _candidate_from_quote(str(entry.get("original", ""))):
            candidate_counts[clean_text(quote_candidate)] += 1

    best_candidate = ""
    best_score = -999.0
    for candidate, frequency in candidate_counts.items():
        if not candidate:
            continue
        score = _description_score(candidate, category, frequency)
        if score > best_score:
            best_score = score
            best_candidate = candidate

    if best_candidate and not is_low_signal_description(best_candidate):
        return best_candidate

    if category and category not in OTHER_CATEGORY_ALIASES:
        return category

    descriptions = [clean_text(entry.get("cleaned", "")) for entry in entries if clean_text(entry.get("cleaned", ""))]
    return min(descriptions, key=len) if descriptions else "Unspecified customer need"


def _normalize_structured_requirements(requirements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for item in requirements:
        description = clean_text(str(item.get("description", "")))
        if not description:
            continue
        normalized.append(
            {
                "description": description,
                "importance": item.get("importance"),
                "frequency_in_voc": max(1, int(item.get("frequency_in_voc", 1) or 1)),
                "category": clean_text(str(item.get("category", ""))) or categorize_requirement(description),
                "sample_quotes": list(dict.fromkeys(item.get("sample_quotes", [description])))[:3],
                "user_confirmed": bool(item.get("user_confirmed", item.get("importance") is not None)),
            }
        )
    normalized.sort(key=lambda item: item["frequency_in_voc"], reverse=True)
    for idx, req in enumerate(normalized, start=1):
        req["id"] = f"REQ-{idx:03d}"
    return normalized


def generate_requirements(
    clustered: Dict[str, List[Dict[str, Any]]],
    min_frequency: int = 2,
) -> List[Dict[str, Any]]:
    requirements: List[Dict[str, Any]] = []
    for category, entries in clustered.items():
        if len(entries) < min_frequency:
            continue
        description = _select_requirement_description(entries, category)
        sample_quotes = [str(entry.get("original", ""))[:120] for entry in entries[:3]]
        requirements.append(
            {
                "description": description,
                "importance": None,
                "frequency_in_voc": len(entries),
                "category": category,
                "sample_quotes": sample_quotes,
                "user_confirmed": False,
            }
        )

    requirements.sort(key=lambda item: item["frequency_in_voc"], reverse=True)
    for idx, requirement in enumerate(requirements, start=1):
        requirement["id"] = f"REQ-{idx:03d}"
    return requirements


def process_voc_file(file_path: str, min_frequency: int = 2) -> Dict[str, Any]:
    loaded = load_voc_file(file_path)
    if not loaded.get("success"):
        return {
            "success": False,
            "error": loaded.get("error", "Could not extract valid VOC entries from the file"),
        }

    structured_input = loaded.get("input_mode") == "structured_requirements"
    if structured_input:
        requirements = _normalize_structured_requirements(list(loaded.get("structured_requirements", [])))
        categories_found = sorted({item.get("category", OTHER_CATEGORY) for item in requirements})
        return {
            "success": bool(requirements),
            "input_mode": "structured_requirements",
            "structured_input": True,
            "detected_fields": loaded.get("detected_fields", {}),
            "total_voc_entries": len(requirements),
            "raw_voc_entries": loaded.get("total_raw_entries", 0),
            "deduplicated_voc_entries": len(requirements),
            "categories_found": categories_found,
            "requirements_generated": len(requirements),
            "requirements": requirements,
        }

    entries = list(loaded.get("entries", []))
    if not entries:
        return {
            "success": False,
            "error": "Could not extract valid VOC entries from the file",
        }

    clustered = cluster_voc_entries(entries)
    requirements = generate_requirements(clustered, min_frequency)
    if not requirements:
        fallback_clustered = cluster_voc_entries(entries)
        requirements = generate_requirements(fallback_clustered, min_frequency=1)

    return {
        "success": bool(requirements),
        "input_mode": "raw_voc",
        "structured_input": False,
        "detected_fields": loaded.get("detected_fields", {}),
        "total_voc_entries": loaded.get("total_raw_entries", len(entries)),
        "raw_voc_entries": loaded.get("total_raw_entries", len(entries)),
        "deduplicated_voc_entries": loaded.get("total_unique_entries", len(entries)),
        "categories_found": list(clustered.keys()),
        "requirements_generated": len(requirements),
        "requirements": requirements,
    }


def format_requirements_table(requirements: List[Dict[str, Any]]) -> str:
    lines = [
        "| ID | Requirement | Frequency | Category | Importance |",
        "|----|-------------|-----------|----------|------------|",
    ]
    for req in requirements:
        importance = req.get("importance") or "___"
        lines.append(
            f"| {req['id']} | {req['description']} | {req['frequency_in_voc']} | {req['category']} | {importance} |"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python voc_processor.py <voc_file> [min_frequency]")
        sys.exit(1)

    file_path = sys.argv[1]
    min_freq = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    result = process_voc_file(file_path, min_freq)
    if result["success"]:
        print("VOC processing completed")
        print(f"Input mode: {result['input_mode']}")
        print(f"Entries: {result['total_voc_entries']}")
        print(f"Requirements: {result['requirements_generated']}")
        print(format_requirements_table(result["requirements"]))
    else:
        print(f"Processing failed: {result['error']}")

#!/usr/bin/env python3
"""Unified DOE pipeline CLI with subcommands.

Subcommands:
- evidence: build evidence catalog from discovery + fetch manifest
- factor: extract factor hypotheses from evidence catalog
- design: build DOE design and run sheet
- report: render markdown plan report
- run-all: execute all steps in order
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import re
import sys
from pathlib import Path
from statistics import mean
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np

try:
    # Optional dependency. Fallbacks are used if unavailable.
    import pyDOE3  # type: ignore

    HAS_PYDOE3 = True
except Exception:
    pyDOE3 = None
    HAS_PYDOE3 = False


SENTENCE_SPLIT = re.compile(r"(?<=[\.;!?])\s+|\n+")
RANGE_PATTERN = re.compile(
    r"(?P<low>\d+(?:\.\d+)?)\s*(?:to|-|~|–|—)\s*(?P<high>\d+(?:\.\d+)?)\s*(?P<unit>[a-zA-Z%°/_-]+)?"
)
BETWEEN_RANGE_PATTERN = re.compile(
    r"(?:between|from)\s+(?P<low>\d+(?:\.\d+)?)\s*(?:and|to)\s*(?P<high>\d+(?:\.\d+)?)\s*(?P<unit>[a-zA-Z%°/_-]+)?",
    re.IGNORECASE,
)
P_VALUE_PATTERN = re.compile(r"p\s*[<=>]\s*0\.0?5", re.IGNORECASE)
SIGNIFICANCE_PATTERN = re.compile(r"\bsignificant\b|\bstatistically\b", re.IGNORECASE)
SINGLE_VALUE_PATTERN = re.compile(
    r"(?P<value>\d+(?:\.\d+)?)\s*(?P<unit>[a-zA-Z%°/_-]+)"
)


FACTOR_LIBRARY: Dict[str, Dict[str, Any]] = {
    "temperature": {
        "patterns": [
            r"\btemperature\b",
            r"\btemp\b",
            r"\btemp(?:erature)?\s+setpoint\b",
            r"\bdegc\b",
            r"\bcelsius\b",
            r"°c",
            r"\bfahrenheit\b",
        ],
        "default_range": {"low": 28.0, "high": 37.0, "unit": "degC"},
        "unit_alias": {"c": "degC", "degc": "degC", "celsius": "degC", "°c": "degC"},
        "mechanism": "Temperature modulates enzyme kinetics and cell stress response.",
        "risk": "Out-of-range values may reduce viability or product quality.",
        "type": "range",
    },
    "pH": {
        "patterns": [r"\bph\b", r"\bp\s*h\b", r"\bacidity\b", r"\balkalinity\b"],
        "default_range": {"low": 5.5, "high": 7.5, "unit": "pH"},
        "unit_alias": {},
        "mechanism": "pH controls transport and enzyme activity in the bioreactor.",
        "risk": "Rapid pH drift can destabilize growth and quality attributes.",
        "type": "range",
    },
    "dissolved_oxygen": {
        "patterns": [
            r"\bdissolved\s+oxygen\b",
            r"\boxygen\s+setpoint\b",
            r"\bdo\s+setpoint\b",
            r"\bdo\s+level\b",
            r"\boxygen\s+level\b",
            r"\b%\s*do\b",
        ],
        "default_range": {"low": 20.0, "high": 60.0, "unit": "%"},
        "unit_alias": {"percent": "%", "%": "%"},
        "mechanism": "DO setpoint constrains respiratory flux and energy balance.",
        "risk": "Low DO risks oxygen limitation; high DO may increase oxidative stress.",
        "type": "range",
    },
    "agitation_speed": {
        "patterns": [r"\bagitation\b", r"\bagitation\s+speed\b", r"\brpm\b", r"\bstir(ring)?\b", r"\bimpeller\b"],
        "default_range": {"low": 200.0, "high": 900.0, "unit": "rpm"},
        "unit_alias": {"rpm": "rpm", "rps": "rpm"},
        "mechanism": "Agitation drives mixing, kLa, and shear profile.",
        "risk": "Excess agitation may increase shear damage.",
        "type": "range",
    },
    "aeration_rate": {
        "patterns": [r"\baeration\b", r"\bairflow\b", r"\bvvm\b", r"\bgas\s+flow\b", r"\bsparging\b"],
        "default_range": {"low": 0.3, "high": 1.2, "unit": "vvm"},
        "unit_alias": {"vvm": "vvm"},
        "mechanism": "Aeration modulates oxygen transfer and strip-out behavior.",
        "risk": "High aeration can cause foaming and process instability.",
        "type": "range",
    },
    "feed_rate": {
        "patterns": [
            r"\bfeed\s+rate\b",
            r"\bfeeding\b",
            r"\bfeeding\s+rate\b",
            r"\bsubstrate\s+feed\b",
            r"\bglucose\s+feed\b",
            r"\bfed-batch\b",
        ],
        "default_range": {"low": 0.5, "high": 6.0, "unit": "mL_per_h"},
        "unit_alias": {"ml_per_h": "mL_per_h", "ml/h": "mL_per_h", "mlhr": "mL_per_h"},
        "mechanism": "Feed rate controls carbon availability and overflow metabolism.",
        "risk": "Overfeeding may cause byproduct accumulation.",
        "type": "range",
    },
    "induction_timing": {
        "patterns": [r"\binduction\s+timing\b", r"\binduce\b", r"\biptg\s+time\b", r"\bpost-induction\b"],
        "default_range": {"low": 4.0, "high": 16.0, "unit": "h"},
        "unit_alias": {"h": "h", "hr": "h", "hours": "h", "hour": "h", "min": "h"},
        "mechanism": "Induction timing sets burden and expression balance.",
        "risk": "Poor timing can reduce expression efficiency.",
        "type": "range",
    },
}


class DoePipelineError(Exception):
    def __init__(self, code: str, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details or {}


def _emit_doe_error(code: str, message: str, details: Optional[Dict[str, Any]] = None) -> int:
    payload = {
        "error_code": code,
        "message": message,
        "details": details or {},
    }
    print(json.dumps(payload, ensure_ascii=False), file=sys.stderr)
    return 2

def _load_json(path: Path) -> Dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise DoePipelineError(
            "DOE_INPUT_NOT_FOUND",
            f"input file not found: {path}",
            {"path": str(path), "type": type(exc).__name__},
        ) from exc
    except json.JSONDecodeError as exc:
        raise DoePipelineError(
            "DOE_INVALID_JSON",
            f"input file contains invalid JSON: {path}",
            {
                "path": str(path),
                "line": exc.lineno,
                "column": exc.colno,
                "message": exc.msg,
            },
        ) from exc
    if isinstance(data, dict):
        return data
    raise DoePipelineError(
        "DOE_INVALID_JSON",
        f"expected JSON object: {path}",
        {"path": str(path), "actual_type": type(data).__name__},
    )


def _write_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _safe_year(value: Any) -> int:
    try:
        year = int(value)
        if 1900 <= year <= 2100:
            return year
    except (TypeError, ValueError):
        pass
    return 0


def _safe_score(value: Any) -> float:
    try:
        score = float(value)
    except (TypeError, ValueError):
        score = 0.5
    return max(0.0, min(1.0, score))


def _source_prefix(source_type: str) -> str:
    if source_type == "patent":
        return "PAT"
    if source_type == "paper":
        return "PAP"
    return "WEB"


def _make_source_id(source_type: str, raw_key: str) -> str:
    prefix = _source_prefix(source_type)
    digest = hashlib.sha1(f"{source_type}|{raw_key}".encode("utf-8")).hexdigest()[:12]
    return f"{prefix}-{digest}"


def _normalize_source(item: Dict[str, Any], default_type: str) -> Dict[str, Any]:
    source_type = str(item.get("source_type") or default_type).lower()
    if source_type not in {"patent", "paper", "web"}:
        source_type = default_type

    raw_key = str(
        item.get("id")
        or item.get("url_or_id")
        or item.get("url")
        or item.get("title")
        or "unknown"
    )
    return {
        "source_type": source_type,
        "source_id": _make_source_id(source_type, raw_key),
        "raw_key": raw_key,
        "title": str(item.get("title") or f"Untitled {source_type}"),
        "year": _safe_year(item.get("year")),
        "url_or_id": str(item.get("url_or_id") or item.get("url") or item.get("id") or ""),
        "relevance_score": _safe_score(item.get("relevance_score")),
    }


def _load_discovery(path: Path) -> Dict[str, Any]:
    raw = _load_json(path)

    objective = str(raw.get("objective") or "")
    responses = raw.get("responses") or []
    constraints = raw.get("constraints") or []

    rows: List[Dict[str, Any]] = []
    for item in raw.get("patents", []):
        if isinstance(item, dict):
            rows.append(_normalize_source(item, "patent"))
    for item in raw.get("papers", []):
        if isinstance(item, dict):
            rows.append(_normalize_source(item, "paper"))
    for item in raw.get("web", []):
        if isinstance(item, dict):
            rows.append(_normalize_source(item, "web"))

    for item in raw.get("candidates", []):
        if isinstance(item, dict):
            default_type = str(item.get("source_type") or "paper").lower()
            if default_type not in {"patent", "paper", "web"}:
                default_type = "paper"
            rows.append(_normalize_source(item, default_type))

    normalized_responses = responses if isinstance(responses, list) else [responses]
    normalized_responses = [str(item).strip() for item in normalized_responses if str(item).strip()]

    if not objective.strip():
        raise DoePipelineError(
            "DOE_DISCOVERY_INVALID",
            "search_input.json requires a non-empty objective",
            {"path": str(path), "required_field": "objective"},
        )
    if not normalized_responses:
        raise DoePipelineError(
            "DOE_DISCOVERY_INVALID",
            "search_input.json requires at least one response metric",
            {"path": str(path), "required_field": "responses"},
        )
    if not rows:
        raise DoePipelineError(
            "DOE_DISCOVERY_INVALID",
            "search_input.json requires at least one candidate evidence source",
            {"path": str(path), "required_fields": ["patents", "papers", "web", "candidates"]},
        )

    rows.sort(key=lambda r: (r["relevance_score"], r["year"]), reverse=True)

    return {
        "objective": objective,
        "responses": normalized_responses,
        "constraints": constraints if isinstance(constraints, list) else [constraints],
        "sources": rows,
    }


def _load_fetch_manifest(path: Path) -> Dict[str, Dict[str, Any]]:
    raw = _load_json(path)
    items = raw.get("items", [])
    if not isinstance(items, list):
        raise DoePipelineError(
            "DOE_FETCH_MANIFEST_INVALID",
            "fetch manifest requires items[]",
            {"path": str(path), "required_field": "items"},
        )
    if not items:
        raise DoePipelineError(
            "DOE_FETCH_MANIFEST_INVALID",
            "fetch manifest requires at least one item",
            {"path": str(path), "required_field": "items"},
        )

    out: Dict[str, Dict[str, Any]] = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        key = str(item.get("source_key") or item.get("id") or item.get("url_or_id") or item.get("url") or "")
        if not key:
            continue
        status = str(item.get("status") or "failed")
        fetch_path = str(item.get("path") or "")
        if status == "success":
            if not fetch_path:
                raise DoePipelineError(
                    "DOE_FETCH_MANIFEST_INVALID",
                    "successful fetch items must include a local path",
                    {"path": str(path), "source_key": key},
                )
            resolved_path = Path(fetch_path)
            if not resolved_path.is_absolute():
                resolved_path = (path.parent / resolved_path).resolve()
            if not resolved_path.exists() or not resolved_path.is_file():
                raise DoePipelineError(
                    "DOE_FETCH_PATH_INVALID",
                    "fetch manifest points to a missing local evidence file",
                    {"path": str(path), "source_key": key, "fetch_path": fetch_path},
                )
            fetch_path = str(resolved_path)
        out[key] = {
            "status": status,
            "attempts": int(item.get("attempts") or 1),
            "path": fetch_path,
            "error": str(item.get("error") or ""),
        }
    if not out:
        raise DoePipelineError(
            "DOE_FETCH_MANIFEST_INVALID",
            "fetch manifest did not contain any usable source keys",
            {"path": str(path)},
        )
    return out


def _extract_sentence_bucket(text: str) -> Dict[str, str]:
    method: List[str] = []
    condition: List[str] = []
    result: List[str] = []
    boundary: List[str] = []

    for sentence in SENTENCE_SPLIT.split(text):
        line = sentence.strip()
        if not line:
            continue
        low = line.lower()
        if any(k in low for k in ["method", "protocol", "fermentation", "cultivation", "assay"]):
            method.append(line)
        if any(k in low for k in ["temperature", "ph", "dissolved oxygen", "agitation", "rpm", "vvm", "feed"]):
            condition.append(line)
        if any(k in low for k in ["increase", "decrease", "improve", "yield", "titer", "result", "productivity"]):
            result.append(line)
        if any(k in low for k in ["limit", "boundary", "constraint", "not significant", "tradeoff", "unstable"]):
            boundary.append(line)

    def _best(lines: List[str]) -> str:
        return lines[0][:360] if lines else ""

    return {
        "method": _best(method),
        "condition": _best(condition),
        "result": _best(result),
        "boundary": _best(boundary),
    }


def _read_text(path: str) -> str:
    p = Path(path)
    if not p.exists() or not p.is_file():
        return ""
    return p.read_text(encoding="utf-8", errors="ignore")


def build_evidence_catalog(search_input: Path, fetch_manifest: Path, top_k: int) -> Dict[str, Any]:
    discovery = _load_discovery(search_input)
    manifest = _load_fetch_manifest(fetch_manifest)

    selected = discovery["sources"][: max(1, top_k)]
    sources: List[Dict[str, Any]] = []

    for source in selected:
        fetch = manifest.get(source["raw_key"], {"status": "failed", "attempts": 1, "path": "", "error": "missing manifest entry"})
        text = _read_text(fetch.get("path", "")) if fetch.get("status") == "success" else ""

        read_status = "failed"
        read_payload = {
            "status": "failed",
            "method": "",
            "condition": "",
            "result": "",
            "boundary": "",
            "significance": "low",
            "excerpt": "",
        }

        if text:
            bucket = _extract_sentence_bucket(text)
            significance = "high" if (P_VALUE_PATTERN.search(text) or SIGNIFICANCE_PATTERN.search(text)) else "medium"
            if bucket["condition"] or bucket["result"]:
                read_status = "success"
            elif bucket["method"] or bucket["boundary"]:
                read_status = "partial"
            else:
                read_status = "failed"

            read_payload = {
                "status": read_status,
                "method": bucket["method"],
                "condition": bucket["condition"],
                "result": bucket["result"],
                "boundary": bucket["boundary"],
                "significance": significance,
                "excerpt": text[:800],
            }

        sources.append(
            {
                "source_id": source["source_id"],
                "source_type": source["source_type"],
                "title": source["title"],
                "year": source["year"],
                "url_or_id": source["url_or_id"],
                "relevance_score": source["relevance_score"],
                "fetch": {
                    "status": str(fetch.get("status") or "failed"),
                    "attempts": int(fetch.get("attempts") or 1),
                    "path": str(fetch.get("path") or ""),
                    "error": str(fetch.get("error") or ""),
                },
                "read": read_payload,
            }
        )

    coverage: Dict[str, Dict[str, int]] = {
        "patent": {"total": 0, "fetched": 0, "read": 0},
        "paper": {"total": 0, "fetched": 0, "read": 0},
        "web": {"total": 0, "fetched": 0, "read": 0},
    }

    for row in sources:
        source_type = row["source_type"]
        if source_type not in coverage:
            continue
        coverage[source_type]["total"] += 1
        if row["fetch"]["status"] == "success":
            coverage[source_type]["fetched"] += 1
        if row["read"]["status"] in {"success", "partial"}:
            coverage[source_type]["read"] += 1

    payload = {
        "objective": discovery["objective"],
        "responses": discovery["responses"],
        "constraints": discovery["constraints"],
        "sources": sources,
        "coverage": coverage,
    }
    payload["gates"] = _evaluate_evidence_gates(payload)
    return payload


def _clean_unit_token(unit: str) -> str:
    clean = unit.strip().lower()
    clean = clean.replace("°", "")
    clean = clean.replace("per", "/")
    clean = clean.replace(" ", "")
    return clean


def _normalize_unit(unit: str, factor_name: str) -> str:
    clean = _clean_unit_token(unit)
    aliases = FACTOR_LIBRARY[factor_name].get("unit_alias", {})
    if clean in aliases:
        return aliases[clean]
    if factor_name == "pH":
        return "pH"
    if not clean:
        return FACTOR_LIBRARY[factor_name]["default_range"].get("unit", "")
    return unit


def _convert_numeric_range(
    factor_name: str,
    low: float,
    high: float,
    unit: str,
) -> Optional[Tuple[float, float, str]]:
    clean = _clean_unit_token(unit)
    canonical = _normalize_unit(unit, factor_name)

    if factor_name == "temperature":
        if clean in {"f", "degf", "fahrenheit"}:
            low = (low - 32.0) * 5.0 / 9.0
            high = (high - 32.0) * 5.0 / 9.0
            canonical = "degC"
        elif canonical != "degC":
            return None
    elif factor_name == "feed_rate":
        if clean in {"ml/min", "mlmin"}:
            low *= 60.0
            high *= 60.0
            canonical = "mL_per_h"
        elif canonical != "mL_per_h":
            return None
    elif factor_name == "induction_timing":
        if clean in {"min", "mins", "minute", "minutes"}:
            low /= 60.0
            high /= 60.0
            canonical = "h"
        elif canonical != "h":
            return None
    elif factor_name == "agitation_speed":
        if clean == "rps":
            low *= 60.0
            high *= 60.0
            canonical = "rpm"
        elif canonical != "rpm":
            return None
    elif factor_name == "aeration_rate":
        if canonical != "vvm":
            return None
    elif factor_name == "dissolved_oxygen":
        if canonical != "%":
            return None
    elif factor_name == "pH":
        canonical = "pH"

    return round(min(low, high), 4), round(max(low, high), 4), canonical


def _factor_occurrences(text: str, factor_name: str) -> List[Tuple[int, int]]:
    spans: List[Tuple[int, int]] = []
    for pattern in FACTOR_LIBRARY[factor_name]["patterns"]:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            left = text[max(0, match.start() - 24) : match.start()].strip()
            if re.search(r"(?:^|\b)(?:no|not|without)\s*$", left):
                continue
            spans.append((match.start(), match.end()))
    spans.sort(key=lambda item: item[0])
    return spans


def _extract_local_ranges(text: str, span: Tuple[int, int], window: int = 120) -> List[Dict[str, Any]]:
    start, end = span
    left = max(0, start - window)
    right = min(len(text), end + window)
    region = text[left:right]

    ranges: List[Dict[str, Any]] = []
    for pattern in (RANGE_PATTERN, BETWEEN_RANGE_PATTERN):
        for match in pattern.finditer(region):
            low = float(match.group("low"))
            high = float(match.group("high"))
            unit = str(match.group("unit") or "")
            ranges.append(
                {
                    "low": min(low, high),
                    "high": max(low, high),
                    "unit": unit,
                    "span_text": region[max(0, match.start() - 30) : min(len(region), match.end() + 30)].strip(),
                    "distance": abs((left + match.start() + left + match.end()) / 2.0 - (start + end) / 2.0),
                }
            )
    return ranges


def _extract_local_single_values(text: str, span: Tuple[int, int], window: int = 80) -> List[Dict[str, Any]]:
    start, end = span
    left = max(0, start - window)
    right = min(len(text), end + window)
    region = text[left:right]

    values: List[Dict[str, Any]] = []
    for match in SINGLE_VALUE_PATTERN.finditer(region):
        raw_unit = str(match.group("unit") or "")
        if not raw_unit:
            continue
        try:
            value = float(match.group("value"))
        except (TypeError, ValueError):
            continue
        values.append(
            {
                "low": value,
                "high": value,
                "unit": raw_unit,
                "span_text": region[max(0, match.start() - 24) : min(len(region), match.end() + 24)].strip(),
                "distance": abs((left + match.start() + left + match.end()) / 2.0 - (start + end) / 2.0),
            }
        )
    return values


def _range_candidate_score(candidate: Dict[str, Any], source_type: str) -> float:
    score = 1.0 / (1.0 + float(candidate.get("distance", 999.0)))
    if float(candidate.get("high", 0.0)) > float(candidate.get("low", 0.0)):
        score += 0.35
    if source_type in {"patent", "paper"}:
        score += 0.15
    return score


def _score_evidence_link(
    source: Dict[str, Any],
    read: Dict[str, Any],
    chosen_range: Optional[Dict[str, Any]],
    support_role: str,
) -> float:
    base = float(source.get("relevance_score", 0.5))
    if str(read.get("significance", "")).lower() == "high":
        base += 0.12
    elif str(read.get("significance", "")).lower() == "medium":
        base += 0.05
    if str(read.get("status", "")) == "success":
        base += 0.08
    if not read.get("condition"):
        base -= 0.1
    if not read.get("result"):
        base -= 0.08
    if chosen_range is not None:
        base += 0.08
    if support_role == "supplemental":
        base -= 0.12
    return round(max(0.0, min(1.0, base)), 3)


def _link_quality_bucket(confidence: float) -> str:
    if confidence >= 0.75:
        return "high"
    if confidence >= 0.5:
        return "medium"
    return "low"


def _select_best_range(factor: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    candidates = list(factor.get("range_candidates") or [])
    if not candidates:
        return None
    candidates.sort(
        key=lambda item: (
            int(item.get("support_role") == "core"),
            float(item.get("source_confidence", 0.0)),
            float(item.get("score", 0.0)),
        ),
        reverse=True,
    )
    best = candidates[0]
    return {
        "low": best["low"],
        "high": best["high"],
        "unit": best["unit"],
        "source_id": best.get("source_id", ""),
        "support_role": best.get("support_role", ""),
        "score": round(float(best.get("score", 0.0)), 4),
    }


def _evaluate_evidence_gates(catalog: Dict[str, Any]) -> Dict[str, Any]:
    coverage = catalog.get("coverage", {})
    sources = list(catalog.get("sources", []))
    patent_read = int(coverage.get("patent", {}).get("read", 0) or 0)
    paper_read = int(coverage.get("paper", {}).get("read", 0) or 0)
    web_read = int(coverage.get("web", {}).get("read", 0) or 0)
    readable_total = patent_read + paper_read + web_read
    condition_result_sources = sum(
        1
        for row in sources
        if str(row.get("read", {}).get("status") or "") == "success"
        and row.get("read", {}).get("condition")
        and row.get("read", {}).get("result")
    )
    blocking_issues: List[str] = []

    if readable_total < 2:
        blocking_issues.append("Need at least two readable sources before factor extraction.")
    if patent_read == 0:
        blocking_issues.append("Need at least one readable patent source.")
    if paper_read == 0:
        blocking_issues.append("Need at least one readable paper source.")
    if condition_result_sources == 0:
        blocking_issues.append("Need at least one source with both condition and result excerpts.")

    return {
        "status": "ready" if not blocking_issues else "blocked",
        "readable_source_count": readable_total,
        "readable_patents": patent_read,
        "readable_papers": paper_read,
        "readable_web_sources": web_read,
        "condition_result_sources": condition_result_sources,
        "blocking_issues": blocking_issues,
    }


def extract_factor_hypotheses(catalog_path: Path, max_factors: int) -> Dict[str, Any]:
    catalog = _load_json(catalog_path)
    sources = list(catalog.get("sources", []))
    gates = _evaluate_evidence_gates(catalog)
    if gates["status"] != "ready":
        return {
            "factors": [],
            "summary": {
                "status": "blocked",
                "total_factors": 0,
                "high_priority_total": 0,
                "high_priority_covered": 0,
                "high_priority_coverage_rate": 0.0,
                "design_ready_factors": 0,
                "blocking_issues": list(gates["blocking_issues"]),
                "evidence_gate": gates,
            },
        }

    factor_map: Dict[str, Dict[str, Any]] = {}

    for source in sources:
        read = source.get("read", {})
        if read.get("status") not in {"success", "partial"}:
            continue

        text = " ".join(
            [
                str(read.get("method", "")),
                str(read.get("condition", "")),
                str(read.get("result", "")),
                str(read.get("boundary", "")),
                str(read.get("excerpt", "")),
            ]
        )
        text_low = text.lower()
        if not text_low.strip():
            continue

        for factor_name, meta in FACTOR_LIBRARY.items():
            occurrences = _factor_occurrences(text_low, factor_name)
            if not occurrences:
                continue

            factor = factor_map.setdefault(
                factor_name,
                {
                    "name": factor_name,
                    "type": meta["type"],
                    "unit": meta["default_range"]["unit"],
                    "suggested_range": dict(meta["default_range"]),
                    "mechanism_hypothesis": meta["mechanism"],
                    "risk_note": meta["risk"],
                    "confidence": 0.0,
                    "evidence_links": [],
                    "coverage": {"has_patent": False, "has_paper": False, "has_web": False},
                    "range_candidates": [],
                    "high_priority": False,
                },
            )

            for span in occurrences:
                local_ranges = _extract_local_ranges(text, span)
                chosen_range = None
                if not local_ranges:
                    local_ranges = _extract_local_single_values(text, span)
                if local_ranges:
                    source_type = str(source.get("source_type") or "")
                    normalized_candidates: List[Dict[str, Any]] = []
                    for candidate in local_ranges:
                        converted = _convert_numeric_range(
                            factor_name,
                            float(candidate["low"]),
                            float(candidate["high"]),
                            str(candidate.get("unit") or ""),
                        )
                        if converted is None:
                            continue
                        low, high, unit = converted
                        normalized_candidates.append(
                            {
                                "low": low,
                                "high": high,
                                "unit": unit,
                                "span_text": candidate.get("span_text", ""),
                                "distance": candidate.get("distance", 999.0),
                                "score": _range_candidate_score(candidate, source_type),
                            }
                        )
                    if normalized_candidates:
                        chosen_range = max(
                            normalized_candidates,
                            key=lambda item: (float(item.get("score", 0.0)), -float(item.get("distance", 999.0))),
                        )

                support_role = "core" if str(source.get("source_type") or "") in {"patent", "paper"} else "supplemental"
                confidence = _score_evidence_link(source, read, chosen_range, support_role)
                link = {
                    "source_id": source.get("source_id", ""),
                    "quote_or_paraphrase": (
                        str(read.get("condition") or "") + " | " + str(read.get("result") or "")
                    ).strip(" |")[:420],
                    "condition": str(read.get("condition") or ""),
                    "result": str(read.get("result") or ""),
                    "confidence": confidence,
                    "evidence_quality": _link_quality_bucket(confidence),
                    "support_role": support_role,
                    "fact_or_inference": "fact"
                    if (
                        support_role == "core"
                        and read.get("condition")
                        and read.get("result")
                    )
                    else "inference",
                }
                if chosen_range:
                    link["range_hint"] = {
                        "low": chosen_range["low"],
                        "high": chosen_range["high"],
                        "unit": chosen_range["unit"],
                    }
                    factor["range_candidates"].append(
                        {
                            **chosen_range,
                            "source_id": source.get("source_id", ""),
                            "support_role": support_role,
                            "source_confidence": confidence,
                        }
                    )
                factor["evidence_links"].append(link)

                source_type = str(source.get("source_type") or "")
                if source_type == "patent":
                    factor["coverage"]["has_patent"] = True
                elif source_type == "paper":
                    factor["coverage"]["has_paper"] = True
                elif source_type == "web":
                    factor["coverage"]["has_web"] = True

    if not factor_map:
        return {
            "factors": [],
            "summary": {
                "status": "blocked",
                "total_factors": 0,
                "high_priority_total": 0,
                "high_priority_covered": 0,
                "high_priority_coverage_rate": 0.0,
                "design_ready_factors": 0,
                "blocking_issues": [
                    "Readable evidence did not yield any supported factor hypotheses from the canonical library."
                ],
                "evidence_gate": gates,
            },
        }

    factors: List[Dict[str, Any]] = []
    for factor in factor_map.values():
        links = factor["evidence_links"]
        best_range = _select_best_range(factor)
        if best_range:
            factor["unit"] = best_range["unit"]
            factor["suggested_range"] = {
                "low": best_range["low"],
                "high": best_range["high"],
                "unit": best_range["unit"],
            }
            factor["range_support"] = {
                "source_id": best_range["source_id"],
                "support_role": best_range["support_role"],
                "score": best_range["score"],
            }

        conf = mean(float(item["confidence"]) for item in links) if links else 0.2
        if factor["coverage"]["has_patent"] and factor["coverage"]["has_paper"]:
            conf += 0.08
        if not any(link.get("range_hint") for link in links):
            conf -= 0.06
        factor["confidence"] = round(max(0.0, min(1.0, conf)), 3)

        has_full_core = factor["coverage"]["has_patent"] and factor["coverage"]["has_paper"]
        if not has_full_core:
            factor["risk_note"] = (
                factor["risk_note"]
                + " Evidence gap: lacks patent+paper dual support for this factor."
            )

        numeric_range = _numeric_range(factor.get("suggested_range"))
        core_links = [link for link in links if link.get("support_role") == "core"]
        factor["evidence_strength"] = {
            "core_link_count": len(core_links),
            "supplemental_link_count": len([link for link in links if link.get("support_role") == "supplemental"]),
            "high_quality_links": len([link for link in links if link.get("evidence_quality") == "high"]),
        }
        factor["design_ready"] = (
            bool(links)
            and numeric_range is not None
            and factor["confidence"] >= 0.45
            and len(core_links) >= 2
            and has_full_core
        )
        factor["fact_or_inference"] = "fact" if has_full_core else "inference"
        factor.pop("range_candidates", None)
        factors.append(factor)

    factors.sort(key=lambda item: item["confidence"], reverse=True)
    factors = factors[: max(1, max_factors)]

    high_priority_count = max(1, min(3, len(factors)))
    for idx, factor in enumerate(factors, start=1):
        factor["factor_id"] = f"FACTOR-{idx:03d}"
        factor["high_priority"] = idx <= high_priority_count

    high_priority_total = sum(1 for f in factors if f["high_priority"])
    high_priority_covered = sum(
        1
        for f in factors
        if f["high_priority"] and f["coverage"]["has_patent"] and f["coverage"]["has_paper"]
    )
    design_ready_factors = sum(1 for f in factors if f.get("design_ready"))
    blocking_issues = []
    if design_ready_factors == 0:
        blocking_issues.append("No factors have both usable ranges and sufficient evidence quality for DOE design.")
    if high_priority_total and high_priority_covered < high_priority_total:
        blocking_issues.append("At least one high-priority factor still lacks patent+paper dual support.")

    return {
        "factors": factors,
        "summary": {
            "status": "ready" if not blocking_issues else "blocked",
            "total_factors": len(factors),
            "high_priority_total": high_priority_total,
            "high_priority_covered": high_priority_covered,
            "high_priority_coverage_rate": round(
                high_priority_covered / high_priority_total, 3
            )
            if high_priority_total
            else 0.0,
            "design_ready_factors": design_ready_factors,
            "design_ready_factor_ids": [f["factor_id"] for f in factors if f.get("design_ready")],
            "strong_factor_count": sum(1 for f in factors if float(f.get("confidence", 0.0)) >= 0.65),
            "blocking_issues": blocking_issues,
            "evidence_gate": gates,
        },
    }


def _numeric_range(suggested_range: Any) -> Optional[Tuple[float, float, str]]:
    if not isinstance(suggested_range, dict):
        return None
    try:
        low = float(suggested_range.get("low"))
        high = float(suggested_range.get("high"))
        unit = str(suggested_range.get("unit") or "")
    except (TypeError, ValueError):
        return None
    return min(low, high), max(low, high), unit


def _coded_to_actual(code: float, suggested_range: Any) -> Any:
    numeric = _numeric_range(suggested_range)
    if not numeric:
        if code <= -0.99:
            return "LOW"
        if code >= 0.99:
            return "HIGH"
        if abs(code) < 0.01:
            return "CENTER"
        return f"AXIAL({code:.2f})"

    low, high, unit = numeric
    center = (low + high) / 2.0
    half = (high - low) / 2.0
    actual = round(center + code * half, 4)
    return f"{actual} {unit}".strip()


def _full_factorial(k: int) -> np.ndarray:
    rows = []
    for i in range(2**k):
        row = []
        for j in range(k):
            row.append(1.0 if ((i >> j) & 1) else -1.0)
        rows.append(row)
    return np.array(rows, dtype=float)


def _pb_matrix(k: int) -> np.ndarray:
    if HAS_PYDOE3:
        matrix = np.array(pyDOE3.pbdesign(k), dtype=float)
        return matrix[:, :k]

    # Hadamard fallback for screening designs.
    n = 1
    while n < k + 1:
        n *= 2
    h = np.array([[1.0]])
    while h.shape[0] < n:
        h = np.block([[h, h], [h, -h]])
    mat = h[1:, 1 : k + 1]
    return mat


def _ffd_matrix(k: int) -> np.ndarray:
    if HAS_PYDOE3:
        # Build a half-fraction generator string.
        if k <= 1:
            return _full_factorial(k)
        base_letters = "abcdefghijklmnopqrstuvwxyz"
        base = min(4, k - 1)
        generators = [base_letters[i] for i in range(base)]
        while len(generators) < k:
            generators.append("".join(generators[:2]))
        expr = " ".join(generators[:k])
        return np.array(pyDOE3.fracfact(expr), dtype=float)

    ff = _full_factorial(k)
    parity = np.sum(ff > 0, axis=1) % 2
    return ff[parity == 0]


def _bbd_matrix(k: int, center_points: int) -> np.ndarray:
    if HAS_PYDOE3 and k >= 3:
        return np.array(pyDOE3.bbdesign(k, center=center_points), dtype=float)

    if k < 3:
        return _full_factorial(k)

    rows: List[List[float]] = []
    for i in range(k):
        for j in range(i + 1, k):
            for a, b in [(-1.0, -1.0), (-1.0, 1.0), (1.0, -1.0), (1.0, 1.0)]:
                row = [0.0] * k
                row[i] = a
                row[j] = b
                rows.append(row)
    for _ in range(max(1, center_points)):
        rows.append([0.0] * k)
    return np.array(rows, dtype=float)


def _ccd_matrix(k: int, center_points: int) -> np.ndarray:
    if HAS_PYDOE3:
        center = (center_points, center_points)
        return np.array(pyDOE3.ccdesign(k, center=center, alpha="o", face="ccc"), dtype=float)

    alpha = math.sqrt(k) if k > 1 else 1.0
    rows = _full_factorial(k).tolist()
    for i in range(k):
        plus = [0.0] * k
        minus = [0.0] * k
        plus[i] = alpha
        minus[i] = -alpha
        rows.append(plus)
        rows.append(minus)
    for _ in range(max(1, center_points)):
        rows.append([0.0] * k)
    return np.array(rows, dtype=float)


def _design_diag(matrix: np.ndarray) -> Dict[str, Any]:
    if matrix.size == 0 or matrix.shape[1] <= 1:
        return {"max_abs_column_corr": 0.0, "orthogonality": "n/a"}

    cols = matrix - np.mean(matrix, axis=0)
    std = np.std(cols, axis=0)
    valid_cols = std > 1e-8
    if np.sum(valid_cols) <= 1:
        return {"max_abs_column_corr": 0.0, "orthogonality": "low-information"}
    corr = np.corrcoef(cols[:, valid_cols], rowvar=False)
    max_abs = float(np.max(np.abs(corr - np.eye(corr.shape[0]))))
    quality = "good" if max_abs < 0.1 else "moderate" if max_abs < 0.3 else "weak"
    return {
        "max_abs_column_corr": round(max_abs, 4),
        "orthogonality": quality,
    }


def _analysis_plan(design_type: str) -> List[str]:
    if design_type in {"pb", "ffd"}:
        return [
            "Fit main-effects model and screen significant factors.",
            "Check residual patterns and effect sparsity assumptions.",
            "Carry top factors into response-surface optimization.",
        ]
    return [
        "Fit quadratic response-surface model.",
        "Run ANOVA, lack-of-fit, and residual diagnostics.",
        "Estimate optimum region and verify with confirmation runs.",
    ]


def _next_round_rules() -> List[str]:
    return [
        "Continue when primary response improves >= 10% without violating constraints.",
        "Stop or redesign if safety, operability, or quality limits are breached.",
        "Expand factor ranges only for inconclusive high-priority factors.",
    ]


def _pick_auto_design(phase: str, factor_count: int, resource_budget: int) -> Tuple[str, str]:
    if phase == "screening":
        if factor_count >= 7:
            return "pb", "Screening phase with many factors favors Plackett-Burman efficiency."
        if factor_count >= 4:
            return "ffd", "Screening phase with medium factor count favors fractional factorial."
        return "ffd", "Screening with few factors still uses FFD to estimate main effects efficiently."

    # optimization
    if factor_count <= 5:
        if resource_budget and resource_budget < 30:
            return "bbd", "Optimization with tight run budget favors Box-Behnken."
        return "ccd", "Optimization with sufficient budget favors Central Composite for curvature."
    return "ffd", "Too many factors for response-surface directly; use FFD for reduction first."


def build_design(
    factors_json: Path,
    design_type: str,
    phase: str,
    resource_budget: int,
    replicates: int,
    center_points: int,
    seed: int,
    responses: Sequence[str],
    max_factors: int,
) -> Dict[str, Any]:
    payload = _load_json(factors_json)
    summary = payload.get("summary", {})
    if str(summary.get("status") or "ready") != "ready":
        raise DoePipelineError(
            "DOE_FACTORS_BLOCKED",
            "factor hypotheses are not ready for DOE design",
            {
                "path": str(factors_json),
                "blocking_issues": list(summary.get("blocking_issues") or []),
            },
        )
    factors = list(payload.get("factors", []))
    if not factors:
        raise DoePipelineError(
            "DOE_FACTORS_BLOCKED",
            "no factors found in factor_hypotheses.json",
            {"path": str(factors_json)},
        )

    designable = [
        factor
        for factor in factors
        if factor.get("design_ready") and _numeric_range(factor.get("suggested_range")) is not None
    ]
    if not designable:
        raise DoePipelineError(
            "DOE_FACTORS_BLOCKED",
            "no factors have usable ranges and evidence quality for DOE design",
            {
                "path": str(factors_json),
                "available_factors": len(factors),
                "blocking_issues": list(summary.get("blocking_issues") or []),
            },
        )
    if not list(responses):
        raise DoePipelineError(
            "DOE_DESIGN_INVALID",
            "at least one response metric is required for DOE design",
            {"path": str(factors_json), "required_field": "responses"},
        )

    designable.sort(key=lambda f: (bool(f.get("high_priority")), float(f.get("confidence", 0.0))), reverse=True)
    factors = designable
    selected = factors[: max(1, max_factors)]
    k = len(selected)

    rationale = ""
    if design_type == "auto":
        selected_type, rationale = _pick_auto_design(phase, k, resource_budget)
    else:
        selected_type = design_type
        rationale = f"Explicit design selection: {design_type}."

    if selected_type == "pb":
        matrix = _pb_matrix(k)
    elif selected_type == "ffd":
        matrix = _ffd_matrix(k)
    elif selected_type == "bbd":
        matrix = _bbd_matrix(k, center_points)
    elif selected_type == "ccd":
        matrix = _ccd_matrix(k, center_points)
    else:
        raise ValueError(f"Unsupported design type: {selected_type}")

    if resource_budget > 0 and matrix.shape[0] > resource_budget:
        # Downsample deterministically by seed to satisfy budget.
        rng = random.Random(seed)
        indices = list(range(matrix.shape[0]))
        rng.shuffle(indices)
        keep = sorted(indices[:resource_budget])
        matrix = matrix[keep, :]
        rationale += f" Run budget capped to {resource_budget}; matrix was downsampled."

    runs: List[Dict[str, Any]] = []
    run_id = 1
    for row in matrix.tolist():
        for rep in range(max(1, replicates)):
            coded_levels: Dict[str, float] = {}
            actual_levels: Dict[str, Any] = {}
            for idx, factor in enumerate(selected):
                code = float(row[idx])
                factor_id = str(factor["factor_id"])
                coded_levels[factor_id] = code
                actual_levels[factor_id] = _coded_to_actual(code, factor.get("suggested_range"))
            runs.append(
                {
                    "run_id": run_id,
                    "replicate": rep + 1,
                    "levels_coded": coded_levels,
                    "levels_actual": actual_levels,
                }
            )
            run_id += 1

    randomized = list(runs)
    rng = random.Random(seed)
    rng.shuffle(randomized)
    for order, row in enumerate(randomized, start=1):
        row["run_order"] = order

    diag = _design_diag(matrix)
    diag.update(
        {
            "run_count": len(randomized),
            "center_points": max(1, center_points),
            "alias_risk": "high" if selected_type in {"pb", "ffd"} else "low",
            "randomization_seed": seed,
            "engine": "pyDOE3" if HAS_PYDOE3 else "builtin",
        }
    )

    return {
        "design_type": selected_type,
        "selection_rationale": {
            "phase": phase,
            "factor_count": k,
            "resource_budget": resource_budget,
            "why_this_design": rationale,
        },
        "response_metrics": [str(item) for item in responses],
        "selected_factors": [
            {
                "factor_id": f.get("factor_id"),
                "name": f.get("name"),
                "type": f.get("type"),
                "unit": f.get("unit"),
                "suggested_range": f.get("suggested_range"),
                "confidence": f.get("confidence", 0.0),
                "high_priority": f.get("high_priority", False),
                "fact_or_inference": f.get("fact_or_inference", "inference"),
                "evidence_strength": f.get("evidence_strength", {}),
            }
            for f in selected
        ],
        "runs": randomized,
        "analysis_plan": _analysis_plan(selected_type),
        "next_round_rules": _next_round_rules(),
        "diagnostics": diag,
    }


def write_run_sheet(design: Dict[str, Any], csv_path: Path) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    factor_ids = [f["factor_id"] for f in design.get("selected_factors", [])]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        header = ["run_order", "run_id", "replicate"] + [f"{fid}_actual" for fid in factor_ids] + [
            f"{fid}_coded" for fid in factor_ids
        ]
        writer.writerow(header)
        for row in design.get("runs", []):
            values = [row.get("run_order"), row.get("run_id"), row.get("replicate")]
            values += [row.get("levels_actual", {}).get(fid, "") for fid in factor_ids]
            values += [row.get("levels_coded", {}).get(fid, "") for fid in factor_ids]
            writer.writerow(values)


def _source_type_map(catalog: Dict[str, Any]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for row in catalog.get("sources", []):
        sid = str(row.get("source_id") or "")
        if sid:
            out[sid] = str(row.get("source_type") or "")
    return out


def _coverage_rows(factors: Sequence[Dict[str, Any]], source_type_map: Dict[str, str]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for factor in factors:
        patents: List[str] = []
        papers: List[str] = []
        webs: List[str] = []

        for link in factor.get("evidence_links", []):
            sid = str(link.get("source_id") or "")
            stype = source_type_map.get(sid, "")
            if stype == "patent" and sid not in patents:
                patents.append(sid)
            elif stype == "paper" and sid not in papers:
                papers.append(sid)
            elif stype == "web" and sid not in webs:
                webs.append(sid)

        status = "ok" if patents and papers else "gap"
        rows.append(
            {
                "factor_id": factor.get("factor_id", ""),
                "name": factor.get("name", ""),
                "patents": patents,
                "papers": papers,
                "web": webs,
                "status": status,
                "high_priority": bool(factor.get("high_priority", False)),
                "label": factor.get("fact_or_inference", "inference"),
            }
        )
    return rows


def _acceptance(rows: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(rows)
    covered = sum(1 for row in rows if row["status"] == "ok")

    high_rows = [row for row in rows if row["high_priority"]]
    high_total = len(high_rows)
    high_covered = sum(1 for row in high_rows if row["status"] == "ok")

    checks = {
        "factor_coverage_ge_80": (covered / total >= 0.8) if total else False,
        "high_priority_coverage_eq_100": (high_covered == high_total) if high_total else False,
    }
    return {
        "metrics": {
            "factor_coverage_rate": round(covered / total, 3) if total else 0.0,
            "high_priority_coverage_rate": round(high_covered / high_total, 3) if high_total else 0.0,
            "covered_factors": covered,
            "total_factors": total,
            "covered_high_priority": high_covered,
            "total_high_priority": high_total,
        },
        "checks": checks,
        "overall_pass": all(checks.values()),
    }


def render_report(
    context: Dict[str, Any],
    catalog: Dict[str, Any],
    factors_payload: Dict[str, Any],
    design: Dict[str, Any],
) -> str:
    factors = list(factors_payload.get("factors", []))
    source_map = _source_type_map(catalog)
    rows = _coverage_rows(factors, source_map)

    objective = context.get("objective") or catalog.get("objective") or "Not provided"
    responses = context.get("responses") or catalog.get("responses") or design.get("response_metrics") or []
    constraints = context.get("constraints") or catalog.get("constraints") or []

    if isinstance(responses, list):
        responses_text = ", ".join(str(item) for item in responses)
    else:
        responses_text = str(responses)

    if isinstance(constraints, list):
        constraints_text = ", ".join(str(item) for item in constraints)
    else:
        constraints_text = str(constraints)

    lines: List[str] = []
    lines.append("# DOE Plan")
    lines.append("")

    lines.append("## 1. Objective and Constraints")
    lines.append(f"- Objective: {objective}")
    lines.append(f"- Responses: {responses_text}")
    lines.append(f"- Constraints: {constraints_text if constraints_text else 'None provided'}")
    lines.append("")

    lines.append("## 2. Selected DOE Method and Rationale")
    lines.append(f"- Design Type: {str(design.get('design_type', 'unknown')).upper()}")
    rationale = design.get("selection_rationale", {})
    lines.append(f"- Phase: {rationale.get('phase', 'unknown')}")
    lines.append(f"- Factor Count: {rationale.get('factor_count', 0)}")
    lines.append(f"- Resource Budget: {rationale.get('resource_budget', 0)}")
    lines.append(f"- Rationale: {rationale.get('why_this_design', '')}")
    lines.append("")

    lines.append("## 3. Run Sheet Summary")
    diag = design.get("diagnostics", {})
    lines.append(f"- Total Runs: {len(design.get('runs', []))}")
    lines.append(f"- Engine: {diag.get('engine', 'unknown')}")
    lines.append(f"- Max column correlation: {diag.get('max_abs_column_corr', 0.0)}")
    lines.append(f"- Alias risk: {diag.get('alias_risk', 'unknown')}")
    lines.append("")

    lines.append("## 4. Evidence Coverage Matrix")
    lines.append("| Factor | Name | Patent Sources | Paper Sources | Web Sources | Status | Label |")
    lines.append("|---|---|---|---|---|---|---|")
    for row in rows:
        lines.append(
            "| {fid} | {name} | {pat} | {pap} | {web} | {status} | {label} |".format(
                fid=row["factor_id"],
                name=row["name"],
                pat=", ".join(row["patents"]) if row["patents"] else "-",
                pap=", ".join(row["papers"]) if row["papers"] else "-",
                web=", ".join(row["web"]) if row["web"] else "-",
                status=row["status"],
                label=row["label"],
            )
        )
    lines.append("")

    lines.append("## 5. Facts vs Inference vs Unknowns")
    facts = [row for row in rows if row["status"] == "ok"]
    inference = [row for row in rows if row["status"] == "gap" and (row["patents"] or row["papers"] or row["web"])]
    unknowns = [row for row in rows if row["status"] == "gap" and not (row["patents"] or row["papers"] or row["web"])]

    lines.append("### Facts")
    lines.extend([f"- {row['factor_id']} {row['name']}" for row in facts] or ["- none"])
    lines.append("### Inference")
    lines.extend([f"- {row['factor_id']} {row['name']}" for row in inference] or ["- none"])
    lines.append("### Unknowns")
    lines.extend([f"- {row['factor_id']} {row['name']}" for row in unknowns] or ["- none"])
    lines.append("")

    lines.append("## 6. Next-round Criteria")
    for rule in design.get("next_round_rules", []):
        lines.append(f"- {rule}")
    lines.append("")

    return "\n".join(lines) + "\n"


def cmd_evidence(args: argparse.Namespace) -> int:
    try:
        result = build_evidence_catalog(
            search_input=Path(args.search_input),
            fetch_manifest=Path(args.fetch_manifest),
            top_k=args.top_k,
        )
        output = Path(args.output)
        _write_json(output, result)
        print(f"wrote: {output}")
        return 0
    except DoePipelineError as exc:
        return _emit_doe_error(exc.code, exc.message, exc.details)


def cmd_factor(args: argparse.Namespace) -> int:
    try:
        result = extract_factor_hypotheses(
            catalog_path=Path(args.evidence_catalog),
            max_factors=args.max_factors,
        )
        output = Path(args.output)
        _write_json(output, result)
        print(f"wrote: {output}")
        print(f"factors: {result['summary']['total_factors']}")
        if str(result.get("summary", {}).get("status") or "ready") != "ready":
            return _emit_doe_error(
                "DOE_EVIDENCE_INSUFFICIENT",
                "factor extraction blocked by insufficient evidence quality",
                {
                    "path": str(output),
                    "blocking_issues": list(result.get("summary", {}).get("blocking_issues") or []),
                    "evidence_gate": result.get("summary", {}).get("evidence_gate", {}),
                },
            )
        return 0
    except DoePipelineError as exc:
        return _emit_doe_error(exc.code, exc.message, exc.details)


def cmd_design(args: argparse.Namespace) -> int:
    try:
        responses = [item.strip() for item in args.responses.split(",") if item.strip()]
        result = build_design(
            factors_json=Path(args.factors_json),
            design_type=args.design_type,
            phase=args.phase,
            resource_budget=args.resource_budget,
            replicates=args.replicates,
            center_points=args.center_points,
            seed=args.seed,
            responses=responses,
            max_factors=args.max_factors,
        )
        output_json = Path(args.output_json)
        output_csv = Path(args.output_csv)
        _write_json(output_json, result)
        write_run_sheet(result, output_csv)
        print(f"wrote: {output_json}")
        print(f"wrote: {output_csv}")
        print(f"runs: {len(result['runs'])}")
        return 0
    except DoePipelineError as exc:
        return _emit_doe_error(exc.code, exc.message, exc.details)


def cmd_report(args: argparse.Namespace) -> int:
    try:
        context = _load_json(Path(args.context_json)) if args.context_json else {}
        catalog = _load_json(Path(args.evidence_catalog))
        factors = _load_json(Path(args.factors_json))
        design = _load_json(Path(args.design_json))
        markdown = render_report(context, catalog, factors, design)
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(markdown, encoding="utf-8")
        print(f"wrote: {output}")
        return 0
    except DoePipelineError as exc:
        return _emit_doe_error(exc.code, exc.message, exc.details)


def cmd_run_all(args: argparse.Namespace) -> int:
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    evidence_path = out_dir / "evidence_catalog.json"
    factors_path = out_dir / "factor_hypotheses.json"
    design_path = out_dir / "doe_design.json"
    run_sheet_path = out_dir / "run_sheet.csv"
    report_path = out_dir / "doe_plan.md"

    evidence_args = argparse.Namespace(
        search_input=args.search_input,
        fetch_manifest=args.fetch_manifest,
        top_k=args.top_k,
        output=str(evidence_path),
    )
    rc = cmd_evidence(evidence_args)
    if rc != 0:
        return rc

    factor_args = argparse.Namespace(
        evidence_catalog=str(evidence_path),
        max_factors=args.max_factors,
        output=str(factors_path),
    )
    rc = cmd_factor(factor_args)
    if rc != 0:
        return rc

    design_args = argparse.Namespace(
        factors_json=str(factors_path),
        design_type=args.design_type,
        phase=args.phase,
        resource_budget=args.resource_budget,
        replicates=args.replicates,
        center_points=args.center_points,
        seed=args.seed,
        responses=args.responses,
        max_factors=args.max_factors,
        output_json=str(design_path),
        output_csv=str(run_sheet_path),
    )
    rc = cmd_design(design_args)
    if rc != 0:
        return rc

    report_args = argparse.Namespace(
        context_json=args.context_json,
        evidence_catalog=str(evidence_path),
        factors_json=str(factors_path),
        design_json=str(design_path),
        output=str(report_path),
    )
    return cmd_report(report_args)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Unified DOE planning pipeline")
    sub = parser.add_subparsers(dest="command", required=True)

    p_evidence = sub.add_parser("evidence", help="Build evidence catalog")
    p_evidence.add_argument("--search-input", required=True)
    p_evidence.add_argument("--fetch-manifest", required=True)
    p_evidence.add_argument("--top-k", type=int, default=12)
    p_evidence.add_argument("--output", required=True)
    p_evidence.set_defaults(func=cmd_evidence)

    p_factor = sub.add_parser("factor", help="Extract factor hypotheses")
    p_factor.add_argument("--evidence-catalog", required=True)
    p_factor.add_argument("--max-factors", type=int, default=8)
    p_factor.add_argument("--output", required=True)
    p_factor.set_defaults(func=cmd_factor)

    p_design = sub.add_parser("design", help="Build DOE design and run sheet")
    p_design.add_argument("--factors-json", required=True)
    p_design.add_argument("--design-type", default="auto", choices=["auto", "pb", "ffd", "bbd", "ccd"])
    p_design.add_argument("--phase", default="screening", choices=["screening", "optimization"])
    p_design.add_argument("--resource-budget", type=int, default=0)
    p_design.add_argument("--replicates", type=int, default=1)
    p_design.add_argument("--center-points", type=int, default=3)
    p_design.add_argument("--seed", type=int, default=42)
    p_design.add_argument("--responses", default="yield,titer")
    p_design.add_argument("--max-factors", type=int, default=6)
    p_design.add_argument("--output-json", required=True)
    p_design.add_argument("--output-csv", required=True)
    p_design.set_defaults(func=cmd_design)

    p_report = sub.add_parser("report", help="Render DOE markdown report")
    p_report.add_argument("--context-json")
    p_report.add_argument("--evidence-catalog", required=True)
    p_report.add_argument("--factors-json", required=True)
    p_report.add_argument("--design-json", required=True)
    p_report.add_argument("--output", required=True)
    p_report.set_defaults(func=cmd_report)

    p_all = sub.add_parser("run-all", help="Run full DOE pipeline")
    p_all.add_argument("--search-input", required=True)
    p_all.add_argument("--fetch-manifest", required=True)
    p_all.add_argument("--context-json")
    p_all.add_argument("--output-dir", required=True)
    p_all.add_argument("--top-k", type=int, default=12)
    p_all.add_argument("--max-factors", type=int, default=8)
    p_all.add_argument("--design-type", default="auto", choices=["auto", "pb", "ffd", "bbd", "ccd"])
    p_all.add_argument("--phase", default="screening", choices=["screening", "optimization"])
    p_all.add_argument("--resource-budget", type=int, default=0)
    p_all.add_argument("--replicates", type=int, default=1)
    p_all.add_argument("--center-points", type=int, default=3)
    p_all.add_argument("--seed", type=int, default=42)
    p_all.add_argument("--responses", default="yield,titer")
    p_all.set_defaults(func=cmd_run_all)

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())

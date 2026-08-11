#!/usr/bin/env python3
"""Stage 4: calculate the documented 30/30/20/20 screening score."""

from __future__ import annotations

import argparse
import bisect
import math
import re
from collections import Counter
from typing import Any

from hv_common import checkpoint_meta, file_sha256, jdump, jload, require_checkpoint


INVENTOR_SEPARATOR = re.compile(r"[|;\uFF1B\n\r]+")


def split_inventors(value: Any) -> list[str]:
    """Preserve commas inside Western names and remove within-patent duplicates."""
    if not value:
        return []
    names = [" ".join(item.split()) for item in INVENTOR_SEPARATOR.split(str(value)) if item.strip()]
    return list(dict.fromkeys(names))


def core_inventors(candidates: list[dict[str, Any]], override: list[str] | None = None) -> tuple[list[str], list[dict[str, Any]], str]:
    if override:
        names = list(dict.fromkeys(" ".join(name.split()) for name in override if name.strip()))
        return names[:5], [{"name": name, "candidate_patent_count": None} for name in names[:5]], "user_override"
    counts: Counter[str] = Counter()
    for candidate in candidates:
        counts.update(split_inventors(candidate.get("inventor")))
    ranking = sorted(counts.items(), key=lambda item: (-item[1], item[0].casefold(), item[0]))
    top = [name for name, _ in ranking[:5]]
    return top, [{"name": name, "candidate_patent_count": count} for name, count in ranking], "candidate_set_exact_name"


def available_vector(records: dict[str, dict[str, Any]], field: str, state_field: str) -> list[int]:
    output = []
    for record in records.values():
        if record.get(state_field) == "available" and isinstance(record.get(field), int):
            output.append(int(record[field]))
    return sorted(output)


def percentile(values: list[int], value: int) -> float:
    return bisect.bisect_right(values, value) / len(values) if values else 0.0


def numeric_score(values: list[int], value: int | None, state: str, candidate_count: int) -> tuple[float, float | None, str]:
    if state != "available" or value is None:
        return 0.0, None, "missing_policy_zero"
    pct = percentile(values, value)
    if candidate_count >= 10:
        return round(pct * 30, 2), round(pct * 100, 2), "candidate_set_percentile"
    nonzero = [item for item in values if item > 0]
    if not nonzero or value == 0:
        return 0.0, round(pct * 100, 2), "small_set_all_zero_or_record_zero"
    if len(set(nonzero)) == 1:
        return 15.0, round(pct * 100, 2), "small_set_equal_nonzero_fallback"
    return round(pct * 30, 2), round(pct * 100, 2), "small_set_unstable_percentile"


def application_date_key(value: Any) -> int:
    digits = re.sub(r"\D", "", str(value or ""))[:8]
    return int(digits) if len(digits) == 8 else 99999999


def score_rows(candidates: list[dict[str, Any]], numeric: dict[str, dict[str, Any]], legal: dict[str, dict[str, Any]], top_names: list[str]) -> list[dict[str, Any]]:
    citation_values = available_vector(numeric, "cited_by_simple_family", "citation_state")
    family_values = available_vector(numeric, "simple_family_count", "simple_family_state")
    core_set = set(top_names)
    rows = []
    for candidate in candidates:
        patent_id = str(candidate.get("patent_id") or "")
        num = numeric.get(patent_id, {})
        law = legal.get(patent_id, {})
        citation_value = num.get("cited_by_simple_family")
        family_value = num.get("simple_family_count")
        citation_score, citation_percentile, citation_method = numeric_score(citation_values, citation_value, str(num.get("citation_state", "missing")), len(candidates))
        family_score, family_percentile, family_method = numeric_score(family_values, family_value, str(num.get("simple_family_state", "missing")), len(candidates))
        inventors = split_inventors(candidate.get("inventor"))
        matched = [name for name in inventors if name in core_set]
        inventor_score = 20 if matched else 0
        event_hit = bool(law.get("any_verified_event"))
        event_score = 20 if event_hit else 0
        event_categories = [name for name, detail in (law.get("categories") or {}).items() if detail.get("state") == "available" and int(detail.get("count") or 0) > 0]
        gaps = []
        if num.get("citation_state") != "available":
            gaps.append(f"Forward-citation evidence: {num.get('citation_state', 'missing')}.")
        if num.get("simple_family_state") != "available":
            gaps.append(f"Simple-family evidence: {num.get('simple_family_state', 'missing')}.")
        if not law.get("all_categories_successfully_checked"):
            gaps.append("One or more legal-event categories were not successfully checked.")
        total = round(citation_score + family_score + inventor_score + event_score, 2)
        rows.append({
            "patent_id": patent_id,
            "pn": candidate.get("pn"),
            "title": candidate.get("title"),
            "current_assignee": candidate.get("current_assignee") or candidate.get("original_assignee"),
            "inventor": candidate.get("inventor"),
            "apdt": candidate.get("apdt"),
            "pbdt": candidate.get("pbdt"),
            "authority": candidate.get("authority"),
            "cited_by_simple_family": citation_value,
            "citation_state": num.get("citation_state", "missing"),
            "citation_percentile": citation_percentile,
            "simple_family_count": family_value,
            "simple_family_state": num.get("simple_family_state", "missing"),
            "family_percentile": family_percentile,
            "core_inventor": bool(matched),
            "matched_inventors": matched,
            "legal_event_hit": event_hit,
            "legal_event_categories": event_categories,
            "legal_event_evidence": law.get("categories", {}),
            "s_cited": citation_score,
            "s_fam": family_score,
            "s_inv": inventor_score,
            "s_legal": event_score,
            "citation_scoring_method": citation_method,
            "family_scoring_method": family_method,
            "score": total,
            "gaps": gaps,
        })
    rows.sort(key=lambda row: (
        -row["score"],
        -(row["cited_by_simple_family"] if isinstance(row["cited_by_simple_family"], int) else -1),
        -(row["simple_family_count"] if isinstance(row["simple_family_count"], int) else -1),
        0 if row["legal_event_hit"] else 1,
        0 if row["core_inventor"] else 1,
        -len(row["legal_event_categories"]),
        application_date_key(row["apdt"]),
        str(row.get("pn") or ""),
        row["patent_id"],
    ))
    for index, row in enumerate(rows, start=1):
        row["rank"] = index
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Score and rank the high-value patent screening universe.")
    parser.add_argument("--candidates", default="cand_raw.json")
    parser.add_argument("--numeric", default="enrich_num.json")
    parser.add_argument("--legal", default="enrich_legal.json")
    parser.add_argument("--output", default="scored.json")
    parser.add_argument("--core-inventor", action="append", default=[], help="Reviewed exact-name override; repeat up to five times")
    parser.add_argument("--selection-ratio", type=float, default=0.10)
    args = parser.parse_args()
    if not 0.10 <= args.selection_ratio <= 0.15:
        parser.error("--selection-ratio must be between 0.10 and 0.15")
    source = require_checkpoint(jload(args.candidates), keys=("candidates", "run_id"), filename=args.candidates)
    numeric_source = require_checkpoint(jload(args.numeric), keys=("records", "run_id"), filename=args.numeric)
    legal_source = require_checkpoint(jload(args.legal), keys=("records", "run_id"), filename=args.legal)
    if len({source["run_id"], numeric_source["run_id"], legal_source["run_id"]}) != 1:
        raise ValueError("Checkpoint run IDs do not match.")
    candidates = [item for item in source["candidates"] if isinstance(item, dict)]
    names, inventor_ranking, inventor_method = core_inventors(candidates, args.core_inventor)
    rows = score_rows(candidates, numeric_source["records"], legal_source["records"], names)
    count = len(rows)
    selected_count = min(count, math.ceil(count * args.selection_ratio)) if count else 0
    maximum_count = math.ceil(count * 0.15) if count else 0
    payload = {
        **checkpoint_meta(stage="screening_score", run_id=source["run_id"], upstream_sha256=file_sha256(args.candidates)),
        "model": {"version": "2.0", "weights": {"forward_citations": 30, "family_size": 30, "core_inventor": 20, "legal_event_activity": 20}},
        "candidate_count": count,
        "top5_inventors": inventor_ranking[:5],
        "all_inventor_ranking": inventor_ranking,
        "inventor_method": inventor_method,
        "selected_count": selected_count,
        "sel_max_15pct": maximum_count,
        "ratio": round(selected_count / count * 100, 2) if count else 0.0,
        "rows": rows,
        "errors": numeric_source.get("errors", []) + legal_source.get("errors", []),
    }
    jdump(payload, args.output)
    print(f"Scored {count} candidates; selected {selected_count} ({payload['ratio']}%).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

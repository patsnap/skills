#!/usr/bin/env python3
"""Summarize search-track overlap for monoclonal-antibody FTO screening.

This script preserves the source package's three-track operational record while
correcting its statistical interpretation. Keyword, semantic, and sequence
searches are deliberately related and are not random, independent captures.
Their overlap therefore cannot establish recall or the size of an unseen patent
universe. The script reports observed coverage diagnostics only. It never
certifies search completeness or legal freedom to operate.

Usage:
    python scripts/mab_fto_recall_estimator.py --input-json round.json

Input (legacy fields remain accepted):
    {
      "round": 2,
      "keyword_ids": ["P1", "P2"],
      "semantic_ids": ["P2", "P3"],
      "sequence_ids": ["P4"],
      "seen_ids": ["P0"],
      "delta_n_min": 5,
      "required_modules": ["M1", "M1.5", "M2"],
      "completed_modules": ["M1", "M2"],
      "required_jurisdictions": ["US", "EP"],
      "covered_jurisdictions": ["US"],
      "known_gaps": ["EP register status not verified"]
    }

Legacy `recall_target`, `overlap_correction_threshold`, and
`correction_factor` values are accepted and reported as ignored. This avoids
breaking historical input files without preserving an unsupported calculation.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Report observed overlap and coverage gaps for mAb FTO searches."
    )
    parser.add_argument("--input-json", required=True, help="Path to a UTF-8 JSON input file.")
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Print compact JSON and omit the human-readable summary.",
    )
    return parser.parse_args()


def fail(message: str, exit_code: int = 2) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(exit_code)


def load_input(path_value: str) -> dict[str, Any]:
    path = Path(path_value)
    if not path.is_file():
        fail(f"Input file does not exist: {path}")
    try:
        # utf-8-sig also accepts ordinary UTF-8 and tolerates BOMs emitted by
        # common Windows/PowerShell workflows.
        with path.open(encoding="utf-8-sig") as handle:
            value = json.load(handle)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"Unable to read valid UTF-8 JSON: {exc}")
    if not isinstance(value, dict):
        fail("The JSON root must be an object.")
    return value


def normalize_ids(data: dict[str, Any], field: str) -> set[str]:
    value = data.get(field, [])
    if value is None:
        return set()
    if not isinstance(value, list):
        fail(f"{field} must be an array of identifiers.")
    normalized: set[str] = set()
    for index, item in enumerate(value):
        if not isinstance(item, (str, int)):
            fail(f"{field}[{index}] must be a string or integer identifier.")
        identifier = str(item).strip()
        if not identifier:
            fail(f"{field}[{index}] is blank.")
        normalized.add(identifier)
    return normalized


def normalize_labels(data: dict[str, Any], field: str) -> set[str]:
    value = data.get(field, [])
    if value is None:
        return set()
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        fail(f"{field} must be an array of strings.")
    return {item.strip() for item in value if item.strip()}


def normalize_nonnegative_int(data: dict[str, Any], field: str, default: int) -> int:
    value = data.get(field, default)
    if isinstance(value, bool):
        fail(f"{field} must be an integer.")
    try:
        normalized = int(value)
    except (TypeError, ValueError):
        fail(f"{field} must be an integer.")
    if normalized < 0:
        fail(f"{field} cannot be negative.")
    return normalized


def summarize(data: dict[str, Any]) -> dict[str, Any]:
    round_number = normalize_nonnegative_int(data, "round", 1)
    if round_number < 1:
        fail("round must be at least 1.")

    keyword = normalize_ids(data, "keyword_ids")
    semantic = normalize_ids(data, "semantic_ids")
    sequence = normalize_ids(data, "sequence_ids")
    seen = normalize_ids(data, "seen_ids")
    delta_min = normalize_nonnegative_int(data, "delta_n_min", 5)

    required_modules = normalize_labels(data, "required_modules")
    completed_modules = normalize_labels(data, "completed_modules")
    required_jurisdictions = normalize_labels(data, "required_jurisdictions")
    covered_jurisdictions = normalize_labels(data, "covered_jurisdictions")
    known_gaps_value = data.get("known_gaps", [])
    if not isinstance(known_gaps_value, list) or any(
        not isinstance(item, str) for item in known_gaps_value
    ):
        fail("known_gaps must be an array of strings.")
    known_gaps = [item.strip() for item in known_gaps_value if item.strip()]

    current = keyword | semantic | sequence
    cumulative = seen | current
    new_ids = current - seen

    missing_modules = sorted(required_modules - completed_modules)
    missing_jurisdictions = sorted(required_jurisdictions - covered_jurisdictions)

    warnings: list[str] = []
    ignored_legacy_fields = [
        field
        for field in (
            "recall_target",
            "overlap_correction_threshold",
            "correction_factor",
        )
        if field in data
    ]
    if ignored_legacy_fields:
        warnings.append(
            "Unsupported recall-estimation settings were ignored: "
            + ", ".join(ignored_legacy_fields)
        )
    if not current:
        warnings.append("All three search tracks are empty in this round.")
    if sum(bool(track) for track in (keyword, semantic, sequence)) < 2:
        warnings.append("Fewer than two search tracks returned results.")
    if len(new_ids) < delta_min:
        warnings.append(
            f"Observed incremental yield is below the configured review threshold "
            f"({len(new_ids)} < {delta_min}); this is not proof of completeness."
        )
    if missing_modules:
        warnings.append("Required search modules remain incomplete.")
    if missing_jurisdictions:
        warnings.append("Required jurisdictions remain uncovered.")
    warnings.extend(f"Known gap: {gap}" for gap in known_gaps)

    review_ready = bool(current) and not missing_modules and not missing_jurisdictions
    if known_gaps:
        review_ready = False

    if not current:
        decision = "expand_or_repair_search"
    elif missing_modules or missing_jurisdictions:
        decision = "complete_required_coverage"
    elif known_gaps:
        decision = "resolve_known_gaps"
    elif len(new_ids) < delta_min:
        decision = "manual_stop_review"
    else:
        decision = "continue_search"

    return {
        "schema_version": "2.0",
        "round": round_number,
        "observed_counts": {
            "keyword": len(keyword),
            "semantic": len(semantic),
            "sequence": len(sequence),
            "keyword_semantic_overlap": len(keyword & semantic),
            "keyword_sequence_overlap": len(keyword & sequence),
            "semantic_sequence_overlap": len(semantic & sequence),
            "all_three_overlap": len(keyword & semantic & sequence),
            "current_union": len(current),
            "new_this_round": len(new_ids),
            "cumulative_union": len(cumulative),
        },
        "coverage": {
            "required_modules": sorted(required_modules),
            "completed_modules": sorted(completed_modules),
            "missing_modules": missing_modules,
            "required_jurisdictions": sorted(required_jurisdictions),
            "covered_jurisdictions": sorted(covered_jurisdictions),
            "missing_jurisdictions": missing_jurisdictions,
            "known_gaps": known_gaps,
        },
        "diagnostic_only": True,
        "recall_estimate": None,
        "review_ready": review_ready,
        "decision": decision,
        "warnings": warnings,
        "interpretation": (
            "Observed overlap and incremental yield are search-process diagnostics. "
            "They do not estimate total patent coverage, legal risk, or freedom to operate."
        ),
    }


def print_human(result: dict[str, Any]) -> None:
    counts = result["observed_counts"]
    coverage = result["coverage"]
    print("\nObserved search coverage")
    print("=" * 60)
    print(f"Round: {result['round']}")
    print(
        "Tracks: "
        f"keyword={counts['keyword']}, semantic={counts['semantic']}, "
        f"sequence={counts['sequence']}"
    )
    print(
        "Overlap: "
        f"K∩S={counts['keyword_semantic_overlap']}, "
        f"K∩Q={counts['keyword_sequence_overlap']}, "
        f"S∩Q={counts['semantic_sequence_overlap']}, "
        f"all={counts['all_three_overlap']}"
    )
    print(
        f"Cumulative records: {counts['cumulative_union']}; "
        f"new this round: {counts['new_this_round']}"
    )
    print(f"Missing modules: {', '.join(coverage['missing_modules']) or 'none declared'}")
    print(
        "Missing jurisdictions: "
        f"{', '.join(coverage['missing_jurisdictions']) or 'none declared'}"
    )
    print(f"Decision: {result['decision']}")
    print(f"Manual review ready: {str(result['review_ready']).lower()}")
    if result["warnings"]:
        print("Warnings:")
        for warning in result["warnings"]:
            print(f"- {warning}")
    print("=" * 60)


def main() -> None:
    args = parse_args()
    data = load_input(args.input_json)
    result = summarize(data)
    print(json.dumps(result, ensure_ascii=True, indent=None if args.compact else 2))
    if not args.compact:
        print_human(result)


if __name__ == "__main__":
    main()

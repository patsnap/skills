#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


class InputError(ValueError):
    pass


def load_payload(path: Path) -> dict[str, Any]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise InputError(f"Input file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise InputError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(raw, dict):
        raise InputError("Input payload must be a JSON object.")
    return raw


def normalize_identifier_list(payload: dict[str, Any], key: str) -> set[str]:
    value = payload.get(key)
    if not isinstance(value, list):
        raise InputError(f"'{key}' must be a JSON array.")

    normalized: set[str] = set()
    for item in value:
        text = str(item).strip()
        if text:
            normalized.add(text)
    return normalized


def normalize_probability(value: Any, *, field_name: str) -> float:
    try:
        numeric = float(value)
    except (TypeError, ValueError) as exc:
        raise InputError(f"'{field_name}' must be numeric.") from exc

    if numeric <= 0:
        raise InputError(f"'{field_name}' must be greater than 0.")
    if numeric <= 1:
        return numeric
    if numeric <= 100:
        return numeric / 100.0
    raise InputError(f"'{field_name}' must be in (0, 1] or (0, 100].")


def normalize_non_negative_int(value: Any, *, field_name: str, allow_zero: bool = True) -> int:
    try:
        numeric = int(value)
    except (TypeError, ValueError) as exc:
        raise InputError(f"'{field_name}' must be an integer.") from exc
    if allow_zero and numeric < 0:
        raise InputError(f"'{field_name}' must be >= 0.")
    if not allow_zero and numeric <= 0:
        raise InputError(f"'{field_name}' must be > 0.")
    return numeric


def round_float(value: float | None) -> float | None:
    if value is None:
        return None
    return round(value, 6)


def compute_recall_metrics(payload: dict[str, Any]) -> dict[str, Any]:
    round_no = normalize_non_negative_int(payload.get("round"), field_name="round", allow_zero=False)
    keyword_ids = normalize_identifier_list(payload, "keyword_ids")
    semantic_ids = normalize_identifier_list(payload, "semantic_ids")
    seen_ids = normalize_identifier_list(payload, "seen_ids")
    recall_target = normalize_probability(payload.get("recall_target"), field_name="recall_target")
    delta_n_min = normalize_non_negative_int(payload.get("delta_n_min"), field_name="delta_n_min")
    overlap_threshold = normalize_probability(
        payload.get("overlap_correction_threshold", 0.5),
        field_name="overlap_correction_threshold",
    )
    correction_factor = normalize_probability(
        payload.get("correction_factor", 0.9),
        field_name="correction_factor",
    )

    del round_no  # validated for completeness; not returned by contract.

    n_k = len(keyword_ids)
    n_s = len(semantic_ids)
    overlap_ids = keyword_ids & semantic_ids
    n_ks = len(overlap_ids)
    round_union = keyword_ids | semantic_ids
    n_pool = len(seen_ids | round_union)
    delta_n = len(round_union - seen_ids)

    warnings: list[str] = []

    if n_k == 0 and n_s == 0:
        warnings.append("empty_dual_result")
        return {
            "n_k": 0,
            "n_s": 0,
            "n_ks": 0,
            "n_pool": len(seen_ids),
            "delta_n": 0,
            "universe_estimate_raw": None,
            "universe_estimate_adjusted": None,
            "recall_estimate": None,
            "correction_applied": False,
            "decision": "expand_search",
            "warnings": warnings,
        }

    universe_raw = (((n_k + 1) * (n_s + 1)) / (n_ks + 1)) - 1
    universe_adjusted = universe_raw
    correction_applied = False

    min_channel = min(n_k, n_s)
    if min_channel > 0 and n_ks > overlap_threshold * min_channel:
        universe_adjusted *= correction_factor
        correction_applied = True
        warnings.append("overlap_dependence_detected")

    if universe_adjusted < n_pool:
        universe_adjusted = float(n_pool)
        warnings.append("universe_floor_applied")

    recall_estimate = n_pool / universe_adjusted if universe_adjusted > 0 else None
    if recall_estimate is not None:
        recall_estimate = min(recall_estimate, 1.0)

    if recall_estimate is not None and recall_estimate >= recall_target:
        decision = "target_met"
    elif delta_n < delta_n_min:
        decision = "diminishing_returns"
    else:
        decision = "continue_search"

    return {
        "n_k": n_k,
        "n_s": n_s,
        "n_ks": n_ks,
        "n_pool": n_pool,
        "delta_n": delta_n,
        "universe_estimate_raw": round_float(universe_raw),
        "universe_estimate_adjusted": round_float(universe_adjusted),
        "recall_estimate": round_float(recall_estimate),
        "correction_applied": correction_applied,
        "decision": decision,
        "warnings": warnings,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Estimate FTO search recall and stopping decisions from one search round."
    )
    parser.add_argument("--input-json", required=True, help="Path to the round input JSON file.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        payload = load_payload(Path(args.input_json))
        result = compute_recall_metrics(payload)
    except InputError as exc:
        print(json.dumps({"success": False, "message": str(exc)}, ensure_ascii=False))
        return 1

    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

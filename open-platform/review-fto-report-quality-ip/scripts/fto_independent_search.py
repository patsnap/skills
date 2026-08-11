"""
Independent-search comparison helper for an FTO report-quality review.

The module does not call a network service. An authorized agent performs live
search through current PatSnap MCP tools and passes normalized results to
build_verification_result.

Routes one through four form the independent comparison pool: semantic,
keyword/nested-query, assignee-focused, and IPC/CPC-focused retrieval. A fifth
recent-pending route is reported separately as a watchlist because a pending
application does not yet contain an enforceable granted claim.

Observed overlap and omissions are the primary outputs. A Chapman
capture-recapture calculation is available only as an explicitly qualified
heuristic. Correlated search routes, ranking, family duplication, and unknown
inclusion probabilities normally violate its assumptions. The default is
therefore not_estimated, never a fabricated recall percentage.

CLI:
    python fto_independent_search.py <input.json> <output.json>

The CLI emits a truthful local skeleton. It never claims a live search ran.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


TRACK_LABELS = {
    "semantic": "Semantic route",
    "keyword": "Keyword or nested-query route",
    "assignee": "Assignee-focused route",
    "classification": "IPC/CPC-focused route",
    "temporal": "Recent pending-application watchlist",
}


def normalize_patent_number(value: Any) -> str:
    """Normalize a publication/application identifier for deterministic joins."""
    return re.sub(r"[^A-Z0-9]", "", str(value or "").strip().upper())


def patent_number(record: dict[str, Any]) -> str:
    """Read and normalize the first supported patent-number field."""
    for key in (
        "patent_number", "patent_no", "publication_number", "public_no", "no"
    ):
        value = normalize_patent_number(record.get(key))
        if value:
            return value
    return ""


def family_key(record: dict[str, Any]) -> str:
    """Return a supplied family ID, otherwise a disclosed publication fallback."""
    for key in ("simple_family_id", "family_id", "docdb_family_id"):
        value = str(record.get(key) or "").strip()
        if value:
            return f"FAMILY:{value}"
    number = patent_number(record)
    return f"PUBLICATION:{number}" if number else ""


def qualify_chapman_estimate(
    n_a: int,
    n_b: int,
    n_c: int,
    *,
    assumptions_supported: bool = False,
    assumption_note: str = "",
) -> dict[str, Any]:
    """
    Return a qualified two-pool Chapman estimate.

    assumptions_supported is allowed only where evidence supports a common
    target population, comparable counting units, meaningful independence,
    stable inclusion rules, and verified deduplication.
    """
    if min(n_a, n_b, n_c) < 0:
        raise ValueError("Pool counts cannot be negative.")
    if n_c > min(n_a, n_b):
        raise ValueError("Overlap cannot exceed either pool.")
    counts = {"original_pool": n_a, "independent_pool": n_b, "overlap": n_c}
    if not assumptions_supported:
        return {
            "status": "not_estimated",
            "method": "Chapman two-pool capture-recapture",
            "estimated_total": None,
            "estimated_original_coverage_percent": None,
            "estimated_independent_coverage_percent": None,
            "counts": counts,
            "assumptions_supported": False,
            "note": assumption_note or (
                "No recall estimate was calculated. Search routes are commonly "
                "correlated and their inclusion probabilities are unknown."
            ),
        }
    if n_a == 0 or n_b == 0 or n_c == 0:
        return {
            "status": "not_estimated",
            "method": "Chapman two-pool capture-recapture",
            "estimated_total": None,
            "estimated_original_coverage_percent": None,
            "estimated_independent_coverage_percent": None,
            "counts": counts,
            "assumptions_supported": True,
            "note": "The estimate is not identified with a zero pool or overlap.",
        }
    estimate = max(
        ((n_a + 1) * (n_b + 1)) / (n_c + 1) - 1,
        float(max(n_a, n_b)),
    )
    return {
        "status": "heuristic_estimate",
        "method": "Chapman two-pool capture-recapture",
        "estimated_total": round(estimate, 1),
        "estimated_original_coverage_percent": round(100 * n_a / estimate, 1),
        "estimated_independent_coverage_percent": round(100 * n_b / estimate, 1),
        "counts": counts,
        "assumptions_supported": True,
        "note": (
            "Heuristic only; this is not proof of recall or no omissions. "
            + (assumption_note or "Reviewer documented the stated assumptions.")
        ),
    }


def chapman_estimate(n_a: int, n_b: int, n_c: int) -> dict[str, Any]:
    """Backward-compatible name that safely defaults to not_estimated."""
    return qualify_chapman_estimate(n_a, n_b, n_c)


def empirical_coverage(
    original_numbers: set[str], independent_numbers: set[str]
) -> dict[str, Any]:
    """Return observed overlap metrics without asserting population recall."""
    overlap = original_numbers & independent_numbers
    union = original_numbers | independent_numbers
    return {
        "original_pool_count": len(original_numbers),
        "independent_pool_count": len(independent_numbers),
        "overlap_count": len(overlap),
        "union_count": len(union),
        "original_share_of_observed_union_percent": (
            round(100 * len(original_numbers) / len(union), 1) if union else None
        ),
        "independent_share_of_observed_union_percent": (
            round(100 * len(independent_numbers) / len(union), 1)
            if union else None
        ),
        "jaccard_overlap_percent": (
            round(100 * len(overlap) / len(union), 1) if union else None
        ),
        "interpretation": (
            "Observed-pool metrics only; they do not measure true search recall."
        ),
    }


def _copy_with_track(record: dict[str, Any], track: str) -> dict[str, Any]:
    copied = dict(record)
    copied["_source_track"] = TRACK_LABELS[track]
    copied["_source_tracks"] = [TRACK_LABELS[track]]
    copied["_normalized_patent_number"] = patent_number(record)
    copied["_family_key"] = family_key(record)
    return copied


def merge_routes(
    routes: Iterable[tuple[str, list[dict[str, Any]]]]
) -> list[dict[str, Any]]:
    """Merge routes by publication number while preserving route provenance."""
    merged: dict[str, dict[str, Any]] = {}
    for track, records in routes:
        if track not in TRACK_LABELS:
            raise ValueError(f"Unsupported search route: {track}")
        for record in records:
            number = patent_number(record)
            if not number:
                continue
            if number not in merged:
                merged[number] = _copy_with_track(record, track)
            elif TRACK_LABELS[track] not in merged[number]["_source_tracks"]:
                merged[number]["_source_tracks"].append(TRACK_LABELS[track])
    return list(merged.values())


def find_omissions(
    original_nos: set[str], independent_results: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """
    Return candidates absent from the report pool.

    A retrieval omission is not automatically a material FTO miss. Claim scope,
    territory, status, family, relevant acts, and product mapping require review.
    """
    original = {normalize_patent_number(value) for value in original_nos}
    omissions: list[dict[str, Any]] = []
    for record in independent_results:
        number = patent_number(record)
        if not number or number in original:
            continue
        omissions.append({
            "patent_no": number,
            "title": record.get("title") or "Not supplied",
            "assignee": record.get("assignee") or "Not supplied",
            "status": record.get("legal_status") or "Not verified",
            "status_as_of": record.get("status_as_of") or "",
            "jurisdiction": record.get("jurisdiction") or "",
            "family_key": family_key(record),
            "source": record.get("_source_track") or "Independent retrieval",
            "source_tracks": record.get("_source_tracks") or [],
            "url": record.get("url") or "",
            "review_status": "candidate_requires_verification",
            "materiality": "not_assessed",
        })
    return omissions


def extract_top_ipcs(
    results: list[dict[str, Any]], top_n: int = 5
) -> list[str]:
    """Aggregate frequent four-character IPC/CPC sections."""
    if top_n < 1:
        raise ValueError("top_n must be positive.")
    counter: Counter[str] = Counter()
    for record in results:
        codes = record.get("ipc") or record.get("cpc") or []
        if isinstance(codes, str):
            codes = re.split(r"[,;|]", codes)
        for raw in codes:
            code = re.sub(r"\s+", "", str(raw).upper())[:4]
            if len(code) == 4:
                counter[code] += 1
    return [code for code, _ in counter.most_common(top_n)]


def extract_top_assignees(
    results: list[dict[str, Any]], top_n: int = 5
) -> list[str]:
    """Aggregate assignees for search-strategy diagnostics."""
    if top_n < 1:
        raise ValueError("top_n must be positive.")
    counter: Counter[str] = Counter()
    for record in results:
        value = record.get("assignee") or record.get("current_assignee") or ""
        names = value if isinstance(value, list) else re.split(r"[;|]", str(value))
        for name in names:
            normalized = str(name).strip()
            if normalized and normalized.lower() not in {
                "unknown", "not supplied", "-"
            }:
                counter[normalized] += 1
    return [name for name, _ in counter.most_common(top_n)]


def route_overlap_matrix(
    route_records: dict[str, list[dict[str, Any]]]
) -> list[dict[str, Any]]:
    """Return pairwise route overlap for redundancy review."""
    sets = {
        route: {patent_number(r) for r in records if patent_number(r)}
        for route, records in route_records.items()
    }
    matrix: list[dict[str, Any]] = []
    names = list(sets)
    for index, left in enumerate(names):
        for right in names[index + 1:]:
            union = sets[left] | sets[right]
            overlap = sets[left] & sets[right]
            matrix.append({
                "route_a": TRACK_LABELS.get(left, left),
                "route_b": TRACK_LABELS.get(right, right),
                "overlap_count": len(overlap),
                "union_count": len(union),
                "jaccard_percent": (
                    round(100 * len(overlap) / len(union), 1) if union else None
                ),
            })
    return matrix


def build_verification_result(
    product_description: str,
    original_patents: list[dict[str, Any]],
    semantic_results: list[dict[str, Any]],
    keyword_results: list[dict[str, Any]],
    assignee_results: list[dict[str, Any]] | None = None,
    ipc_results: list[dict[str, Any]] | None = None,
    temporal_results: list[dict[str, Any]] | None = None,
    mode: str = "standard",
    *,
    estimate_assumptions_supported: bool = False,
    estimate_assumption_note: str = "",
    counting_unit: str = "publication",
) -> dict[str, Any]:
    """Build the verification payload consumed by the HTML generator."""
    if counting_unit not in {"publication", "simple_family"}:
        raise ValueError("counting_unit must be publication or simple_family")
    route_records = {
        "semantic": semantic_results,
        "keyword": keyword_results,
        "assignee": assignee_results or [],
        "classification": ipc_results or [],
    }
    independent_pool = merge_routes(route_records.items())
    pending_watchlist = merge_routes([("temporal", temporal_results or [])])
    original_numbers = {
        patent_number(record) for record in original_patents if patent_number(record)
    }
    independent_numbers = {
        patent_number(record) for record in independent_pool if patent_number(record)
    }
    observed = empirical_coverage(original_numbers, independent_numbers)
    estimate = qualify_chapman_estimate(
        observed["original_pool_count"],
        observed["independent_pool_count"],
        observed["overlap_count"],
        assumptions_supported=estimate_assumptions_supported,
        assumption_note=estimate_assumption_note,
    )
    route_counts = {
        TRACK_LABELS[name]: len(records) for name, records in route_records.items()
    }
    route_counts[TRACK_LABELS["temporal"]] = len(temporal_results or [])
    return {
        "status": "comparison_completed",
        "live_search_executed": any(route_counts.values()),
        "mode": mode,
        "product_description": product_description or "Not supplied",
        "counting_unit": counting_unit,
        "route_counts": route_counts,
        "observed_coverage": observed,
        "estimate": estimate,
        "tool_status": " | ".join(
            f"{key}: {value}" for key, value in route_counts.items()
        ),
        "original_pool_count": observed["original_pool_count"],
        "independent_pool_count": observed["independent_pool_count"],
        "overlap_count": observed["overlap_count"],
        "estimated_total": estimate["estimated_total"],
        "recall_rate": (
            f"{estimate['estimated_original_coverage_percent']}%"
            if estimate["status"] == "heuristic_estimate" else "Not estimated"
        ),
        "recall_rating": (
            "Heuristic only"
            if estimate["status"] == "heuristic_estimate" else "Not estimated"
        ),
        "top_ipcs": extract_top_ipcs(independent_pool),
        "top_assignees": extract_top_assignees(independent_pool),
        "route_overlap_matrix": route_overlap_matrix(route_records),
        "omissions": find_omissions(original_numbers, independent_pool),
        "pending_application_watchlist": pending_watchlist,
        "validity_checks": [],
        "note": estimate["note"],
        "independent_pool_sample": independent_pool[:20],
    }


def empty_verification(params: dict[str, Any]) -> dict[str, Any]:
    """Create a truthful skeleton when no live search results were supplied."""
    verification = build_verification_result(
        product_description=params.get("product_description", ""),
        original_patents=params.get("original_patents", []),
        semantic_results=[],
        keyword_results=[],
        assignee_results=[],
        ipc_results=[],
        temporal_results=[],
        mode=str(params.get("mode") or "standard"),
        counting_unit=str(params.get("counting_unit") or "publication"),
    )
    verification.update({
        "status": "not_executed",
        "live_search_executed": False,
        "mcp_enrichment_status": "not_executed",
        "note": (
            "No live MCP results were supplied. This local skeleton makes no "
            "omission, status, claim-scope, materiality, or recall assertion."
        ),
    })
    return verification


def main() -> int:
    if len(sys.argv) != 3:
        print(
            "Usage: python fto_independent_search.py <input.json> <output.json>",
            file=sys.stderr,
        )
        return 2
    input_path, output_path = Path(sys.argv[1]), Path(sys.argv[2])
    if not input_path.is_file():
        print(f"Input file does not exist: {input_path}", file=sys.stderr)
        return 2
    try:
        params = json.loads(input_path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Unable to read input JSON: {exc}", file=sys.stderr)
        return 2
    if not isinstance(params, dict):
        print("Input JSON must contain an object.", file=sys.stderr)
        return 2
    result = {"input_params": params, "verification": empty_verification(params)}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Wrote local verification skeleton: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

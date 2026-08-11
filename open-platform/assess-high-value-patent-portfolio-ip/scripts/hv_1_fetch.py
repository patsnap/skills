#!/usr/bin/env python3
"""Stage 1: retrieve, normalize, and deduplicate the P002 candidate universe."""

from __future__ import annotations

import argparse
import os
from typing import Any

from hv_common import api_post_with_evidence, checkpoint_meta, jdump, load_query, new_run_id


P002_PATH = "/search/patent/query-search-patent/v2"
DEFAULT_PAGE_SIZE = 100
DEFAULT_MAX_RECORDS = 5000


def clean(value: Any) -> str:
    return " ".join(str(value or "").split())


def normalize_candidate(record: dict[str, Any]) -> dict[str, Any]:
    patent_id = clean(record.get("patent_id"))
    publication_number = clean(record.get("pn") or record.get("publication_number"))
    return {
        "patent_id": patent_id,
        "pn": publication_number,
        "title": clean(record.get("title")),
        "current_assignee": clean(record.get("current_assignee") or record.get("current_patentee")),
        "original_assignee": clean(record.get("original_assignee") or record.get("applicant")),
        "inventor": clean(record.get("inventor")),
        "apdt": clean(record.get("apdt") or record.get("application_date")),
        "pbdt": clean(record.get("pbdt") or record.get("publication_date")),
        "authority": clean(record.get("authority") or record.get("country")),
        "source_record": record,
    }


def candidate_key(record: dict[str, Any]) -> str:
    return clean(record.get("patent_id") or record.get("pn")).upper()


def fetch_all(query: str, *, page_size: int, max_records: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if not query.strip():
        raise ValueError("The reviewed P002 query must not be empty.")
    page_size = max(1, min(int(page_size), 500))
    maximum = max(1, int(max_records))
    output: list[dict[str, Any]] = []
    requests_evidence: list[dict[str, Any]] = []
    page_signatures: set[tuple[str, ...]] = set()
    offset = 0
    reported_total: int | None = None
    truncated = False
    while len(output) < maximum:
        limit = min(page_size, maximum - len(output))
        payload = {
            "sort": [{"field": "SCORE", "order": "DESC"}],
            "limit": limit,
            "offset": offset,
            "query_text": query,
        }
        data, evidence = api_post_with_evidence(P002_PATH, payload)
        if not isinstance(data, dict):
            raise ValueError("P002 data must be an object.")
        results = data.get("results") or []
        if not isinstance(results, list):
            raise ValueError("P002 data.results must be an array.")
        total_value = data.get("total_search_result_count", data.get("total"))
        if total_value is not None:
            try:
                reported_total = int(total_value)
            except (TypeError, ValueError):
                pass
        normalized = [normalize_candidate(item) for item in results if isinstance(item, dict)]
        signature = tuple(candidate_key(item) for item in normalized)
        if signature and signature in page_signatures:
            raise RuntimeError(f"P002 repeated a prior page at offset {offset}; pagination stopped to prevent a loop.")
        if signature:
            page_signatures.add(signature)
        requests_evidence.append({**evidence, "offset": offset, "limit": limit, "returned": len(normalized)})
        output.extend(normalized)
        offset += len(results)
        print(f"P002 retrieved {len(output)} candidates" + (f" of {reported_total}" if reported_total is not None else ""))
        if not results or len(results) < limit:
            break
        if reported_total is not None and offset >= reported_total:
            break
    if reported_total is not None and len(output) < reported_total and len(output) >= maximum:
        truncated = True
    return output, {
        "reported_total": reported_total,
        "retrieved_count": len(output),
        "page_count": len(requests_evidence),
        "max_records": maximum,
        "truncated": truncated,
        "requests": requests_evidence,
    }


def deduplicate(records: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    unique: dict[str, dict[str, Any]] = {}
    duplicates: list[dict[str, Any]] = []
    for position, record in enumerate(records, start=1):
        key = candidate_key(record)
        if not key:
            key = f"MISSING-ID-{position:08d}"
            record.setdefault("data_gaps", []).append("P002 returned neither patent_id nor publication number.")
        if key in unique:
            duplicates.append({"key": key, "kept_patent_id": unique[key].get("patent_id"), "dropped_patent_id": record.get("patent_id")})
            continue
        unique[key] = record
    return list(unique.values()), duplicates


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Retrieve and deduplicate the PatSnap P002 candidate universe.")
    parser.add_argument("--page-size", type=int, default=int(os.getenv("HVP_PAGE_SIZE", DEFAULT_PAGE_SIZE)))
    parser.add_argument("--max-records", type=int, default=int(os.getenv("HVP_MAX_RECORDS", DEFAULT_MAX_RECORDS)))
    parser.add_argument("--output", default="cand_raw.json")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    query = load_query()
    rows, retrieval = fetch_all(query, page_size=args.page_size, max_records=args.max_records)
    candidates, duplicates = deduplicate(rows)
    run_id = os.getenv("HVP_RUN_ID") or new_run_id()
    payload = {
        **checkpoint_meta(stage="candidate_retrieval", run_id=run_id, query=query),
        "query_text": query,
        "total_search_result_count": retrieval["reported_total"],
        "retrieval": retrieval,
        "deduplicated_count": len(candidates),
        "duplicate_count": len(duplicates),
        "duplicates": duplicates,
        "candidates": candidates,
        "errors": [],
    }
    jdump(payload, args.output)
    print(f"Wrote {len(candidates)} unique candidates to {args.output}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

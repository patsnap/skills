#!/usr/bin/env python3
"""Stage 2: enrich every candidate with P014 family and P015 citation evidence."""

from __future__ import annotations

import argparse
from typing import Any

from hv_common import (
    PatSnapRequestError,
    api_get_with_evidence,
    checkpoint_meta,
    chunks,
    file_sha256,
    jdump,
    jload,
    require_checkpoint,
)


P014_PATH = "/basic-patent-data/patent-family"
P015_PATH = "/basic-patent-data/forward-citation/v3"


def integer_or_none(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    try:
        return int(value) if value is not None and str(value).strip() != "" else None
    except (TypeError, ValueError):
        return None


def initialize(candidates: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {
        str(item.get("patent_id")): {
            "patent_id": item.get("patent_id"),
            "pn": item.get("pn"),
            "simple_family_count": None,
            "simple_family_state": "not_run",
            "cited_by_simple_family": None,
            "citation_state": "not_run",
            "citation_detail": {},
            "request_evidence": [],
            "errors": [],
        }
        for item in candidates
        if item.get("patent_id")
    }


def request_batch(path: str, batch: list[dict[str, Any]]) -> tuple[Any, dict[str, Any]]:
    ids = ",".join(str(item.get("patent_id")) for item in batch if item.get("patent_id"))
    numbers = ",".join(str(item.get("pn")) for item in batch if item.get("pn"))
    return api_get_with_evidence(path, {"patent_id": ids, "patent_number": numbers})


def apply_family(data: Any, records: dict[str, dict[str, Any]], evidence: dict[str, Any]) -> None:
    if not isinstance(data, list):
        raise ValueError("P014 data must be an array.")
    returned: set[str] = set()
    for item in data:
        if not isinstance(item, dict):
            continue
        patent_id = str(item.get("patent_id") or "")
        if patent_id not in records:
            continue
        returned.add(patent_id)
        family = item.get("patent_family")
        simple = family.get("simple_family") if isinstance(family, dict) else None
        if isinstance(simple, list):
            records[patent_id]["simple_family_count"] = len(simple)
            records[patent_id]["simple_family_state"] = "available"
        elif simple is None:
            records[patent_id]["simple_family_state"] = "missing"
        else:
            records[patent_id]["simple_family_state"] = "error"
            records[patent_id]["errors"].append("P014 simple_family was not an array.")
        records[patent_id]["request_evidence"].append(evidence)
    for patent_id in records:
        if records[patent_id]["simple_family_state"] == "not_run" and patent_id not in returned:
            records[patent_id]["simple_family_state"] = "empty"


def apply_citations(data: Any, records: dict[str, dict[str, Any]], evidence: dict[str, Any]) -> None:
    if not isinstance(data, list):
        raise ValueError("P015 data must be an array.")
    returned: set[str] = set()
    for item in data:
        if not isinstance(item, dict):
            continue
        patent_id = str(item.get("patent_id") or "")
        if patent_id not in records:
            continue
        returned.add(patent_id)
        cited = item.get("patent_cited") or {}
        raw = cited.get("cited_by_simple_family") if isinstance(cited, dict) else None
        value = integer_or_none(raw)
        records[patent_id]["cited_by_simple_family"] = value
        records[patent_id]["citation_state"] = "available" if value is not None else "missing"
        if isinstance(cited, dict):
            records[patent_id]["citation_detail"] = {
                key: cited.get(key)
                for key in ("cited_by_simple_family", "cited_by_inpadoc_family", "cited_by_patsnap_family", "cited_by_3y", "cited_by_5y")
            }
        records[patent_id]["request_evidence"].append(evidence)
    for patent_id in records:
        if records[patent_id]["citation_state"] == "not_run" and patent_id not in returned:
            records[patent_id]["citation_state"] = "empty"


def mark_batch_error(records: dict[str, dict[str, Any]], batch: list[dict[str, Any]], field: str, message: str) -> None:
    for item in batch:
        patent_id = str(item.get("patent_id") or "")
        if patent_id in records:
            records[patent_id][field] = "error"
            records[patent_id]["errors"].append(message)


def run(input_path: str, output_path: str, batch_size: int) -> None:
    source = require_checkpoint(jload(input_path), keys=("candidates", "run_id"), filename=input_path)
    candidates = [item for item in source["candidates"] if isinstance(item, dict)]
    records = initialize(candidates)
    global_errors: list[dict[str, Any]] = []
    for batch_number, batch in enumerate(chunks(candidates, batch_size), start=1):
        try:
            data, evidence = request_batch(P014_PATH, batch)
            apply_family(data, records, evidence)
        except (PatSnapRequestError, ValueError) as exc:
            mark_batch_error(records, batch, "simple_family_state", str(exc))
            global_errors.append({"batch": batch_number, "endpoint": "P014", "message": str(exc)})
        try:
            data, evidence = request_batch(P015_PATH, batch)
            apply_citations(data, records, evidence)
        except (PatSnapRequestError, ValueError) as exc:
            mark_batch_error(records, batch, "citation_state", str(exc))
            global_errors.append({"batch": batch_number, "endpoint": "P015", "message": str(exc)})
        print(f"Numeric enrichment batch {batch_number} completed ({min(batch_number * batch_size, len(candidates))}/{len(candidates)}).")
    payload = {
        **checkpoint_meta(stage="numeric_enrichment", run_id=source["run_id"], upstream_sha256=file_sha256(input_path)),
        "candidate_count": len(candidates),
        "records": records,
        "errors": global_errors,
    }
    jdump(payload, output_path)
    print(f"Wrote numeric evidence for {len(records)} candidates to {output_path}.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Retrieve P014 and P015 numeric screening evidence.")
    parser.add_argument("--input", default="cand_raw.json")
    parser.add_argument("--output", default="enrich_num.json")
    parser.add_argument("--batch-size", type=int, default=20)
    args = parser.parse_args()
    if args.batch_size < 1:
        parser.error("--batch-size must be positive")
    run(args.input, args.output, args.batch_size)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

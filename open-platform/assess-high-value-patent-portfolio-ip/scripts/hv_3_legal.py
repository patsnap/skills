#!/usr/bin/env python3
"""Stage 3: retrieve event-level legal activity for every candidate."""

from __future__ import annotations

import argparse
from typing import Any

from hv_common import PatSnapRequestError, api_get_with_evidence, checkpoint_meta, chunks, file_sha256, jdump, jload, require_checkpoint


ENDPOINTS = {
    "Litigation": ("/high-value-data/litigation", "patent_litigation_data"),
    "Reexamination or invalidation": ("/advanced-patent-data/re-examination-and-invalidation", "patent_reexam_invalid_data"),
    "License": ("/advanced-patent-data/license-data", "patent_license_data"),
    "Transfer": ("/advanced-patent-data/transfer-data", "patent_transfer_data"),
}


def initialize(candidates: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {
        str(candidate["patent_id"]): {
            "patent_id": candidate["patent_id"],
            "pn": candidate.get("pn"),
            "categories": {
                category: {"state": "not_run", "count": None, "events": [], "request_evidence": None, "error": None}
                for category in ENDPOINTS
            },
            "any_verified_event": False,
            "all_categories_successfully_checked": False,
        }
        for candidate in candidates
        if candidate.get("patent_id")
    }


def batch_params(batch: list[dict[str, Any]]) -> dict[str, str]:
    return {
        "patent_id": ",".join(str(item.get("patent_id")) for item in batch if item.get("patent_id")),
        "patent_number": ",".join(str(item.get("pn")) for item in batch if item.get("pn")),
    }


def apply_response(category: str, field: str, data: Any, evidence: dict[str, Any], records: dict[str, dict[str, Any]], batch: list[dict[str, Any]]) -> None:
    if not isinstance(data, list):
        raise ValueError(f"{category} endpoint data must be an array.")
    returned: set[str] = set()
    for item in data:
        if not isinstance(item, dict):
            continue
        patent_id = str(item.get("patent_id") or "")
        if patent_id not in records:
            continue
        returned.add(patent_id)
        events = item.get(field)
        target = records[patent_id]["categories"][category]
        target["request_evidence"] = evidence
        if isinstance(events, list):
            target["events"] = events
            target["count"] = len(events)
            target["state"] = "available" if events else "empty"
        elif events is None:
            target["state"] = "missing"
        else:
            target["state"] = "error"
            target["error"] = f"{field} was not an array."
    for candidate in batch:
        patent_id = str(candidate.get("patent_id") or "")
        if patent_id in records and patent_id not in returned:
            target = records[patent_id]["categories"][category]
            target["state"] = "empty"
            target["count"] = 0
            target["request_evidence"] = evidence


def run(input_path: str, output_path: str, batch_size: int) -> None:
    source = require_checkpoint(jload(input_path), keys=("candidates", "run_id"), filename=input_path)
    candidates = [item for item in source["candidates"] if isinstance(item, dict)]
    records = initialize(candidates)
    errors: list[dict[str, Any]] = []
    for category, (path, field) in ENDPOINTS.items():
        for batch_number, batch in enumerate(chunks(candidates, batch_size), start=1):
            try:
                data, evidence = api_get_with_evidence(path, batch_params(batch))
                apply_response(category, field, data, evidence, records, batch)
            except (PatSnapRequestError, ValueError) as exc:
                errors.append({"category": category, "batch": batch_number, "message": str(exc)})
                for candidate in batch:
                    patent_id = str(candidate.get("patent_id") or "")
                    if patent_id in records:
                        target = records[patent_id]["categories"][category]
                        target["state"] = "error"
                        target["error"] = str(exc)
        print(f"{category}: completed {len(candidates)} candidate checks.")
    for record in records.values():
        categories = list(record["categories"].values())
        record["any_verified_event"] = any(item["state"] == "available" and int(item["count"] or 0) > 0 for item in categories)
        record["all_categories_successfully_checked"] = all(item["state"] in {"available", "empty"} for item in categories)
    payload = {
        **checkpoint_meta(stage="legal_event_enrichment", run_id=source["run_id"], upstream_sha256=file_sha256(input_path)),
        "candidate_count": len(candidates),
        "endpoint_categories": ENDPOINTS,
        "records": records,
        "errors": errors,
        "interpretation": "Event presence is an activity signal, not a positive-value or enforceability conclusion.",
    }
    jdump(payload, output_path)
    print(f"Wrote legal-event evidence for {len(records)} candidates to {output_path}.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Retrieve event-level legal activity for the candidate universe.")
    parser.add_argument("--input", default="cand_raw.json")
    parser.add_argument("--output", default="enrich_legal.json")
    parser.add_argument("--batch-size", type=int, default=20)
    args = parser.parse_args()
    if args.batch_size < 1:
        parser.error("--batch-size must be positive")
    run(args.input, args.output, args.batch_size)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Stage 5: retrieve selected-record display evidence from P021, P025, and P041."""

from __future__ import annotations

import argparse
from typing import Any, Callable

from hv_common import PatSnapRequestError, api_get_with_evidence, checkpoint_meta, chunks, file_sha256, jdump, jload, require_checkpoint


ENDPOINTS = {
    "abstract_drawing": ("/basic-patent-data/abstract-image", "P021"),
    "technical_summary": ("/high-value-data/tech-problem-and-benefit-summary", "P025"),
    "simple_legal_status": ("/basic-patent-data/simple-legal-status", "P041"),
}


def initialize(selected: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {
        str(row["patent_id"]): {
            "patent_id": row["patent_id"],
            "pn": row.get("pn"),
            "drawing": None,
            "drawing_state": "not_run",
            "patsnap_title": None,
            "tech_problem": None,
            "tech_approach": None,
            "benefit": None,
            "technical_summary_state": "not_run",
            "legal_status": None,
            "legal_status_state": "not_run",
            "request_evidence": [],
            "gaps": [],
        }
        for row in selected
        if row.get("patent_id")
    }


def params(batch: list[dict[str, Any]], *, language: bool = False) -> dict[str, str]:
    output = {
        "patent_id": ",".join(str(row.get("patent_id")) for row in batch if row.get("patent_id")),
        "patent_number": ",".join(str(row.get("pn")) for row in batch if row.get("pn")),
    }
    if language:
        output["lang"] = "en"
    return output


def flatten_paragraphs(value: Any) -> str | None:
    if isinstance(value, str):
        text = " ".join(value.split())
        return text or None
    if isinstance(value, list):
        text = " ".join(" ".join(str(item).split()) for item in value if item)
        return text or None
    if isinstance(value, dict):
        for key in ("benefit_para", "tech_problem_para", "technical_approach_para", "text", "summary"):
            text = flatten_paragraphs(value.get(key))
            if text:
                return text
    return None


def apply_drawing(item: dict[str, Any], target: dict[str, Any]) -> None:
    drawing = item.get("abstract_drawing")
    path = drawing.get("path") if isinstance(drawing, dict) else None
    target["drawing"] = str(path).strip() if path else None
    target["drawing_state"] = "available" if path else "empty"


def apply_summary(item: dict[str, Any], target: dict[str, Any]) -> None:
    target["patsnap_title"] = flatten_paragraphs(item.get("patsnap_title"))
    target["tech_problem"] = flatten_paragraphs(item.get("tech_problem_summary"))
    target["tech_approach"] = flatten_paragraphs(item.get("technical_approach_summary"))
    target["benefit"] = flatten_paragraphs(item.get("benefit_summary"))
    fields = (target["patsnap_title"], target["tech_problem"], target["tech_approach"], target["benefit"])
    target["technical_summary_state"] = "available" if any(fields) else "empty"


def apply_status(item: dict[str, Any], target: dict[str, Any]) -> None:
    status = item.get("simple_legal_status")
    if isinstance(status, list):
        target["legal_status"] = "; ".join(str(value) for value in status if value) or None
    elif status:
        target["legal_status"] = str(status)
    target["legal_status_state"] = "available" if target["legal_status"] else "empty"


def retrieve(
    *,
    selected: list[dict[str, Any]],
    records: dict[str, dict[str, Any]],
    path: str,
    label: str,
    state_field: str,
    apply: Callable[[dict[str, Any], dict[str, Any]], None],
    batch_size: int,
    language: bool = False,
) -> list[dict[str, Any]]:
    errors = []
    for batch_number, batch in enumerate(chunks(selected, batch_size), start=1):
        try:
            data, evidence = api_get_with_evidence(path, params(batch, language=language))
            if not isinstance(data, list):
                raise ValueError(f"{label} data must be an array.")
            returned: set[str] = set()
            for item in data:
                if not isinstance(item, dict):
                    continue
                patent_id = str(item.get("patent_id") or "")
                if patent_id not in records:
                    continue
                returned.add(patent_id)
                apply(item, records[patent_id])
                records[patent_id]["request_evidence"].append({"endpoint": label, **evidence})
            for row in batch:
                patent_id = str(row.get("patent_id") or "")
                if patent_id in records and patent_id not in returned:
                    records[patent_id][state_field] = "empty"
                    records[patent_id]["request_evidence"].append({"endpoint": label, **evidence})
        except (PatSnapRequestError, ValueError) as exc:
            errors.append({"endpoint": label, "batch": batch_number, "message": str(exc)})
            for row in batch:
                patent_id = str(row.get("patent_id") or "")
                if patent_id in records:
                    records[patent_id][state_field] = "error"
                    records[patent_id]["gaps"].append(f"{label} retrieval failed: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Retrieve selected-record display evidence.")
    parser.add_argument("--input", default="scored.json")
    parser.add_argument("--output", default="enrich_display.json")
    parser.add_argument("--batch-size", type=int, default=15)
    args = parser.parse_args()
    if args.batch_size < 1:
        parser.error("--batch-size must be positive")
    source = require_checkpoint(jload(args.input), keys=("rows", "selected_count", "run_id"), filename=args.input)
    selected = [row for row in source["rows"][: int(source["selected_count"])] if isinstance(row, dict)]
    records = initialize(selected)
    errors = []
    errors.extend(retrieve(selected=selected, records=records, path=ENDPOINTS["abstract_drawing"][0], label="P021", state_field="drawing_state", apply=apply_drawing, batch_size=args.batch_size))
    errors.extend(retrieve(selected=selected, records=records, path=ENDPOINTS["technical_summary"][0], label="P025", state_field="technical_summary_state", apply=apply_summary, batch_size=args.batch_size, language=True))
    errors.extend(retrieve(selected=selected, records=records, path=ENDPOINTS["simple_legal_status"][0], label="P041", state_field="legal_status_state", apply=apply_status, batch_size=1))
    for record in records.values():
        for label, field in (("Abstract drawing", "drawing_state"), ("English technical summary", "technical_summary_state"), ("Simple legal status", "legal_status_state")):
            if record[field] != "available":
                record["gaps"].append(f"{label}: {record[field]}.")
    payload = {
        **checkpoint_meta(stage="display_enrichment", run_id=source["run_id"], upstream_sha256=file_sha256(args.input)),
        "selected_count": len(selected),
        "records": records,
        "errors": errors,
        "image_note": "P021 URLs may expire. Reports must validate HTTP(S), download only on request, and retain text alternatives.",
    }
    jdump(payload, args.output)
    print(f"Wrote selected-record display evidence for {len(records)} patents to {args.output}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

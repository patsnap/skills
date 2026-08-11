#!/usr/bin/env python3
"""Stage 6: assemble selected records and a complete candidate-level trace."""

from __future__ import annotations

import argparse
from typing import Any

from hv_common import checkpoint_meta, file_sha256, jdump, jload, require_checkpoint


def evidence_phrase(label: str, value: Any, percentile: Any, state: str) -> str:
    if state != "available" or value is None:
        return f"{label}: {state}; zero points under the documented missing-data policy"
    pct = f"candidate-set P{round(float(percentile))}" if percentile is not None else "percentile unavailable"
    return f"{label}: {value} ({pct}; available)"


def rationale(row: dict[str, Any]) -> str:
    parts = [
        evidence_phrase("Simple-family forward citations", row.get("cited_by_simple_family"), row.get("citation_percentile"), str(row.get("citation_state"))),
        evidence_phrase("Simple-family size", row.get("simple_family_count"), row.get("family_percentile"), str(row.get("simple_family_state"))),
    ]
    if row.get("core_inventor"):
        parts.append("Core-inventor match: " + ", ".join(row.get("matched_inventors") or []))
    else:
        parts.append("No exact-name core-inventor match")
    categories = row.get("legal_event_categories") or []
    if categories:
        parts.append("Event activity detected: " + ", ".join(categories))
    elif any("legal-event" in str(gap).lower() for gap in row.get("gaps") or []):
        parts.append("Legal-event absence cannot be concluded because checks are incomplete")
    else:
        parts.append("All checked legal-event categories returned no event records")
    parts.append("Selected under the documented 30/30/20/20 screening model; no monetary-value conclusion")
    return ". ".join(part.rstrip(".") for part in parts) + "."


def display_value(display: dict[str, Any], field: str) -> Any:
    value = display.get(field)
    return value if value not in (None, "") else None


def assemble(row: dict[str, Any], display: dict[str, Any]) -> dict[str, Any]:
    gaps = list(dict.fromkeys(list(row.get("gaps") or []) + list(display.get("gaps") or [])))
    return {
        "rank": row.get("rank"),
        "score": row.get("score"),
        "score_components": {
            "forward_citations": row.get("s_cited"),
            "family_size": row.get("s_fam"),
            "core_inventor": row.get("s_inv"),
            "legal_event_activity": row.get("s_legal"),
        },
        "rationale": rationale(row),
        "pn": row.get("pn"),
        "title": row.get("title"),
        "patent_id": row.get("patent_id"),
        "record_url": None,
        "record_url_state": "not_configured",
        "drawing": display_value(display, "drawing"),
        "drawing_state": display.get("drawing_state", "not_run"),
        "current_assignee": row.get("current_assignee"),
        "legal_status": display_value(display, "legal_status"),
        "legal_status_state": display.get("legal_status_state", "not_run"),
        "patsnap_title": display_value(display, "patsnap_title"),
        "tech_problem": display_value(display, "tech_problem"),
        "tech_approach": display_value(display, "tech_approach"),
        "benefit": display_value(display, "benefit"),
        "technical_summary_state": display.get("technical_summary_state", "not_run"),
        "cited_by_simple_family": row.get("cited_by_simple_family"),
        "citation_state": row.get("citation_state"),
        "citation_percentile": row.get("citation_percentile"),
        "simple_family_count": row.get("simple_family_count"),
        "simple_family_state": row.get("simple_family_state"),
        "family_percentile": row.get("family_percentile"),
        "core_inventor": row.get("core_inventor"),
        "matched_inventors": row.get("matched_inventors") or [],
        "legal_event_hit": row.get("legal_event_hit"),
        "legal_event_categories": row.get("legal_event_categories") or [],
        "legal_event_evidence": row.get("legal_event_evidence") or {},
        "inventor": row.get("inventor"),
        "authority": row.get("authority"),
        "application_date": row.get("apdt"),
        "publication_date": row.get("pbdt"),
        "gaps": gaps,
        "display_request_evidence": display.get("request_evidence") or [],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Assemble final high-value screening records and full trace JSON.")
    parser.add_argument("--scored", default="scored.json")
    parser.add_argument("--display", default="enrich_display.json")
    parser.add_argument("--candidates", default="cand_raw.json")
    parser.add_argument("--output", default="final_records.json")
    parser.add_argument("--trace", default="high_value_patent_screening_data.json")
    args = parser.parse_args()
    scored = require_checkpoint(jload(args.scored), keys=("rows", "selected_count", "run_id"), filename=args.scored)
    display = require_checkpoint(jload(args.display), keys=("records", "run_id"), filename=args.display)
    candidates = require_checkpoint(jload(args.candidates), keys=("candidates", "run_id"), filename=args.candidates)
    if len({scored["run_id"], display["run_id"], candidates["run_id"]}) != 1:
        raise ValueError("Checkpoint run IDs do not match.")
    selected_rows = scored["rows"][: int(scored["selected_count"])]
    selected = [assemble(row, display["records"].get(str(row.get("patent_id")), {})) for row in selected_rows]
    meta = {
        "run_id": scored["run_id"],
        "candidate_count": scored["candidate_count"],
        "p002_reported_total": candidates.get("total_search_result_count"),
        "retrieved_count": candidates.get("retrieval", {}).get("retrieved_count"),
        "deduplicated_count": candidates.get("deduplicated_count"),
        "selected_count": scored["selected_count"],
        "sel_max_15pct": scored["sel_max_15pct"],
        "ratio": scored["ratio"],
        "top5_inventors": scored["top5_inventors"],
        "model": scored["model"],
        "query_text": candidates.get("query_text"),
        "query_sha256": candidates.get("query_sha256"),
        "source_mode": candidates.get("source_mode"),
        "limitations": [
            "Scores are relative to this candidate universe and are not monetary valuations.",
            "Citation and family metrics are affected by age, field, authority, family rule, and database coverage.",
            "Legal-event presence is an activity signal, not a positive-value, validity, or enforceability conclusion.",
            "Publication identifiers remain plain text unless a verified stable global record URL is supplied.",
        ],
    }
    checkpoint = checkpoint_meta(stage="record_assembly", run_id=scored["run_id"], upstream_sha256=file_sha256(args.scored))
    final_payload = {**checkpoint, "meta": meta, "selected": selected, "errors": scored.get("errors", []) + display.get("errors", [])}
    trace_payload = {**checkpoint, "meta": meta, "all_candidates_scored": scored["rows"], "selected": selected, "errors": final_payload["errors"]}
    jdump(final_payload, args.output)
    jdump(trace_payload, args.trace)
    print(f"Assembled {len(selected)} selected records; wrote {args.output} and {args.trace}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

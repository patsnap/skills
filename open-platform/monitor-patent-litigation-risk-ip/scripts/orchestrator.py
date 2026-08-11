"""Create and validate the structured litigation-monitoring evidence record.

This module does not retrieve data and never creates case or patent facts. The
agent populates the schema only from verified connectors and cited primary
sources. The renderer consumes the resulting JSON as an optional export path.
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from config import (
    DEFAULT_FAMILY_SCOPE,
    DEFAULT_INVENTOR_LOOKBACK_YEARS,
    DEFAULT_MAX_LITIGATED_PER_ASSIGNEE,
    DEFAULT_REPORT_LANG,
    DEFAULT_TOP_INVENTORS,
    EVIDENCE_STATES,
    RISK_STATES,
    TARGET_ROLES,
)

PATENT_RECORD_TEMPLATE = {
    "publication_number": "",
    "application_number": "",
    "patent_url": "",
    "title": "",
    "filing_date": "",
    "publication_date": "",
    "priority_date": "",
    "legal_status": "",
    "legal_status_as_of": "",
    "target_role": "other",
    "risk_state": "not_assessable",
    "evidence_state": "unverified",
    "case_ids": [],
    "asserted_claims": [],
    "abstract_image_b64": "",
    "abstract_image_url": "",
    "technology_problem": "",
    "technology_means": "",
    "technology_effect": "",
    "open_questions": [],
    "claims": "",
    "claim_source_language": "",
    "family_members": [],
    "sources": [],
}

CASE_RECORD_TEMPLATE = {
    "case_id": "",
    "case_name": "",
    "case_number": "",
    "tribunal": "",
    "jurisdiction": "",
    "filed_date": "",
    "verified_as_of": "",
    "plaintiffs": [],
    "defendants": [],
    "target_role": "other",
    "asserted_patents": [],
    "asserted_claims": [],
    "allegations": [],
    "defenses": [],
    "procedural_posture": "",
    "disposition": "",
    "appeal": "",
    "timeline": [],
    "sources": [],
    "evidence_state": "unverified",
}

REPORT_DATA_TEMPLATE = {
    "schema_version": "3.0",
    "generated_at": "",
    "cutoff_date": "",
    "report_language": DEFAULT_REPORT_LANG,
    "target": {"name": "", "aliases": [], "role_basis": "first named target"},
    "comparison_parties": [],
    "scope": {
        "jurisdictions": [],
        "family_scope": DEFAULT_FAMILY_SCOPE,
        "inventor_lookback_years": DEFAULT_INVENTOR_LOOKBACK_YEARS,
        "max_litigated_per_party": DEFAULT_MAX_LITIGATED_PER_ASSIGNEE,
        "top_inventors": DEFAULT_TOP_INVENTORS,
        "searches": [],
        "limitations": [],
    },
    "overview": {
        "party_count": 0,
        "candidate_patent_count": 0,
        "verified_asserted_patent_count": 0,
        "family_member_count": 0,
        "verified_case_count": 0,
        "party_patent_map": [],
    },
    "family_analysis": {
        "geography": [],
        "classifications": [],
        "legal_detail": [],
        "geographic_analysis": "",
        "claim_comparison": [],
        "counting_rule": "INPADOC family unless otherwise stated",
    },
    "litigated_patents": [],
    "litigation_timeline": [],
    "cases": [],
    "inventors": [],
    "conclusions": {
        "geographic_exposure": [],
        "litigation_alert": "",
        "technology_trend": "",
        "actions": [],
    },
    "sources": [],
    "assumptions": [],
    "limitations": [],
}


def _safe_url(value: str) -> bool:
    if not value:
        return True
    parsed = urlparse(value)
    return parsed.scheme in {"https", "http"} and bool(parsed.netloc)


def build_skeleton(parties: list[str], **options) -> dict:
    """Create an empty target-centric record without inventing facts."""
    clean = [item.strip() for item in parties if item and item.strip()]
    if not clean:
        raise ValueError("At least one target party is required.")
    if len(clean) > 5:
        raise ValueError("The source workflow supports one to five named parties.")
    data = copy.deepcopy(REPORT_DATA_TEMPLATE)
    data["generated_at"] = datetime.now(timezone.utc).isoformat()
    data["cutoff_date"] = options.get("cutoff_date", "")
    data["report_language"] = options.get("report_language", DEFAULT_REPORT_LANG)
    data["target"]["name"] = clean[0]
    data["comparison_parties"] = clean[1:]
    data["overview"]["party_count"] = len(clean)
    data["scope"]["family_scope"] = options.get("family_scope", DEFAULT_FAMILY_SCOPE)
    data["scope"]["inventor_lookback_years"] = options.get(
        "inventor_lookback_years", DEFAULT_INVENTOR_LOOKBACK_YEARS
    )
    data["scope"]["max_litigated_per_party"] = options.get(
        "max_litigated", DEFAULT_MAX_LITIGATED_PER_ASSIGNEE
    )
    data["scope"]["top_inventors"] = options.get("top_inventors", DEFAULT_TOP_INVENTORS)
    return data


def make_patent_record(**values) -> dict:
    record = copy.deepcopy(PATENT_RECORD_TEMPLATE)
    record.update(values)
    return record


def make_case_record(**values) -> dict:
    record = copy.deepcopy(CASE_RECORD_TEMPLATE)
    record.update(values)
    return record


def validate_record(data: dict) -> list[str]:
    """Return deterministic cross-field and safety errors."""
    errors: list[str] = []
    if data.get("schema_version") != "3.0":
        errors.append("schema_version must be 3.0")
    target = data.get("target", {}).get("name", "").strip()
    if not target:
        errors.append("target.name is required")
    if not data.get("cutoff_date"):
        errors.append("cutoff_date is required before final delivery")
    case_ids: set[str] = set()
    for index, case in enumerate(data.get("cases", []), start=1):
        prefix = f"cases[{index}]"
        case_id = case.get("case_id", "").strip()
        if not case_id:
            errors.append(f"{prefix}.case_id is required")
        elif case_id in case_ids:
            errors.append(f"{prefix}.case_id is duplicated: {case_id}")
        case_ids.add(case_id)
        if case.get("target_role") not in TARGET_ROLES:
            errors.append(f"{prefix}.target_role is invalid")
        if case.get("evidence_state") not in EVIDENCE_STATES:
            errors.append(f"{prefix}.evidence_state is invalid")
        if not case.get("verified_as_of"):
            errors.append(f"{prefix}.verified_as_of is required")
        if not case.get("sources"):
            errors.append(f"{prefix}.sources requires a primary-source locator")
    for index, patent in enumerate(data.get("litigated_patents", []), start=1):
        prefix = f"litigated_patents[{index}]"
        if not patent.get("publication_number"):
            errors.append(f"{prefix}.publication_number is required")
        if patent.get("target_role") not in TARGET_ROLES:
            errors.append(f"{prefix}.target_role is invalid")
        if patent.get("risk_state") not in RISK_STATES:
            errors.append(f"{prefix}.risk_state is invalid")
        if patent.get("evidence_state") not in EVIDENCE_STATES:
            errors.append(f"{prefix}.evidence_state is invalid")
        for key in ("patent_url", "abstract_image_url"):
            if not _safe_url(str(patent.get(key, ""))):
                errors.append(f"{prefix}.{key} must be an http(s) URL")
        unknown = sorted(set(patent.get("case_ids", [])) - case_ids)
        if unknown:
            errors.append(f"{prefix}.case_ids contains unknown IDs: {', '.join(unknown)}")
        if not patent.get("sources"):
            errors.append(f"{prefix}.sources is required")
    return errors


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Create an empty litigation evidence record.")
    parser.add_argument("--parties", required=True, help="Comma-separated target first, then comparison parties")
    parser.add_argument("--out", required=True, help="Output JSON path")
    parser.add_argument("--cutoff-date", default="")
    parser.add_argument("--family-scope", default=DEFAULT_FAMILY_SCOPE)
    parser.add_argument("--inventor-lookback-years", type=int, default=DEFAULT_INVENTOR_LOOKBACK_YEARS)
    parser.add_argument("--max-litigated", type=int, default=DEFAULT_MAX_LITIGATED_PER_ASSIGNEE)
    parser.add_argument("--top-inventors", type=int, default=DEFAULT_TOP_INVENTORS)
    args = parser.parse_args(argv)

    parties = [value.strip() for value in args.parties.split(",") if value.strip()]
    try:
        data = build_skeleton(
            parties,
            cutoff_date=args.cutoff_date,
            family_scope=args.family_scope,
            inventor_lookback_years=args.inventor_lookback_years,
            max_litigated=args.max_litigated,
            top_inventors=args.top_inventors,
        )
    except ValueError as exc:
        print(f"[orchestrator] {exc}", file=sys.stderr)
        return 2

    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[orchestrator] Empty evidence record written: {output}")
    print("[orchestrator] Populate it only with cited PatSnap and primary-source evidence.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

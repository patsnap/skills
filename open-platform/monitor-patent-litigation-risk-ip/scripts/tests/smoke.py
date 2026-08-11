"""Offline smoke and safety tests for the localized litigation report."""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS))

from orchestrator import validate_record  # noqa: E402
from render_report import render  # noqa: E402

FIXTURE = {
    "schema_version": "3.0",
    "generated_at": "2026-08-07T00:00:00+00:00",
    "cutoff_date": "2026-08-07",
    "report_language": "en",
    "target": {"name": "Northstar Devices", "aliases": [], "role_basis": "first named target"},
    "comparison_parties": ["Meridian Systems"],
    "scope": {
        "jurisdictions": ["US"],
        "family_scope": "inpadoc",
        "inventor_lookback_years": 3,
        "max_litigated_per_party": 30,
        "top_inventors": 10,
        "searches": [],
        "limitations": ["Fixture uses synthetic facts for offline rendering tests only."],
    },
    "overview": {
        "party_count": 2,
        "candidate_patent_count": 1,
        "verified_asserted_patent_count": 1,
        "family_member_count": 2,
        "verified_case_count": 1,
        "party_patent_map": [],
    },
    "family_analysis": {
        "geography": [{"jurisdiction": "US", "family_count": 2, "active_count": 1, "pending_count": 1, "risk_state": "not_assessable", "reason": "A filing count alone does not establish risk."}],
        "classifications": [],
        "legal_detail": [],
        "geographic_analysis": "",
        "claim_comparison": [],
        "counting_rule": "INPADOC family",
    },
    "litigated_patents": [{
        "publication_number": "US1234567B2",
        "application_number": "US00/000000",
        "patent_url": "https://example.com/patent/US1234567B2",
        "title": "Example wireless control system <script>alert(1)</script>",
        "filing_date": "2020-01-01",
        "publication_date": "2022-01-01",
        "priority_date": "2019-01-01",
        "legal_status": "Active in fixture",
        "legal_status_as_of": "2026-08-07",
        "target_role": "defendant",
        "risk_state": "not_assessable",
        "evidence_state": "verified",
        "case_ids": ["CASE-001"],
        "asserted_claims": [1],
        "abstract_image_b64": "",
        "abstract_image_url": "javascript:alert(1)",
        "technology_problem": "Fixture only",
        "technology_means": "Fixture only",
        "technology_effect": "Fixture only",
        "open_questions": [],
        "claims": "Fixture claim text",
        "claim_source_language": "en",
        "family_members": [{"publication_number": "EP0000000A1", "jurisdiction": "EP", "legal_status": "Pending", "filing_date": "2020-01-01"}],
        "sources": [{"id": "S2", "label": "Patent fixture", "ref": "https://example.com/patent"}],
    }],
    "litigation_timeline": [{"date": "2025-01-10", "event": "Complaint filed (fixture)", "case_id": "CASE-001", "source": "S1"}],
    "cases": [{
        "case_id": "CASE-001",
        "case_name": "Meridian Systems v. Northstar Devices",
        "case_number": "1:25-cv-00001",
        "tribunal": "Example Court",
        "jurisdiction": "US",
        "filed_date": "2025-01-10",
        "verified_as_of": "2026-08-07",
        "plaintiffs": ["Meridian Systems"],
        "defendants": ["Northstar Devices"],
        "target_role": "defendant",
        "asserted_patents": ["US1234567B2"],
        "asserted_claims": [1],
        "allegations": ["Infringement alleged; fixture only."],
        "defenses": ["No merits conclusion; fixture only."],
        "procedural_posture": "Pending in fixture",
        "disposition": "No final disposition in fixture",
        "appeal": "",
        "timeline": [{"date": "2025-01-10", "event": "Complaint filed", "source": "S1"}],
        "sources": [{"id": "S1", "label": "Primary docket fixture", "ref": "https://example.com/docket"}],
        "evidence_state": "verified",
    }],
    "inventors": [{"name": "Alex Morgan", "recent_count": 4, "top_classifications": ["H04W"], "technology_focus": ["wireless control"], "note": "Descriptive only."}],
    "conclusions": {
        "geographic_exposure": ["Not assessable from fixture counts alone."],
        "litigation_alert": "Track the verified procedural record; do not predict outcome.",
        "technology_trend": "Recent activity is descriptive and not a litigation predictor.",
        "actions": [{"priority": "High", "action": "Verify the current docket", "owner": "Legal", "trigger": "New filing", "evidence": "S1"}],
    },
    "sources": [{"id": "S1", "type": "primary docket", "label": "Primary docket fixture", "ref": "https://example.com/docket", "accessed_at": "2026-08-07", "coverage": "Fixture"}],
    "assumptions": ["All facts are synthetic test data."],
    "limitations": ["Not for substantive use."],
}


def main() -> int:
    errors = validate_record(FIXTURE)
    assert errors == ["litigated_patents[1].abstract_image_url must be an http(s) URL"], errors
    safe_fixture = dict(FIXTURE)
    safe_fixture["litigated_patents"] = [dict(FIXTURE["litigated_patents"][0], abstract_image_url="")]
    assert validate_record(safe_fixture) == []
    document = render(safe_fixture)
    assert "<!doctype html>" in document
    assert "Northstar Devices" in document
    assert "CASE-001" in document
    assert "US1234567B2" in document
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in document
    assert "<script>alert(1)</script>" not in document
    assert "javascript:" not in document
    assert "cdn.jsdelivr" not in document
    assert "\u8bc9\u8bbc" not in document
    print(f"[smoke] OK, html_chars={len(document):,}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

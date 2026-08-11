"""Global defaults and field semantics for patent-litigation monitoring."""
from __future__ import annotations

# Input defaults. Override them for the jurisdiction, business question, and
# evidence availability; never present a default as a legal threshold.
DEFAULT_INVENTOR_LOOKBACK_YEARS = 3
DEFAULT_FAMILY_SCOPE = "inpadoc"
DEFAULT_REPORT_LANG = "en"
DEFAULT_MAX_LITIGATED_PER_ASSIGNEE = 30
DEFAULT_TOP_INVENTORS = 10

# English discovery signals for patent records and public case sources. Add
# jurisdiction-language equivalents at runtime and document the translation.
# A keyword match is a lead, not proof that a patent was asserted in litigation.
LITIGATION_KEYWORDS = [
    "litigation",
    "lawsuit",
    "patent infringement",
    "complaint",
    "counterclaim",
    "injunction",
    "appeal",
    "invalidity",
    "inter partes review",
    "post-grant review",
    "opposition",
    "ITC investigation",
    "FRAND",
    "SEP",
    "licensing dispute",
]

# Stable report order. The active SKILL.md defines the authoritative content.
REPORT_SECTIONS = [
    "executive_summary",
    "scope_and_method",
    "target_overview",
    "litigation_timeline",
    "asserted_patents",
    "case_deep_dive",
    "inventor_activity",
    "three_dimension_conclusions",
    "action_register",
    "sources_and_limitations",
]

CONCLUSION_DIMENSIONS = [
    "geographic_exposure",
    "litigation_alert",
    "technology_trend",
]

TARGET_ROLES = {"plaintiff", "defendant", "counterclaimant", "co_party", "other"}
EVIDENCE_STATES = {"verified", "partially_verified", "unverified", "conflicting"}
RISK_STATES = {"elevated", "moderate", "lower_on_reviewed_evidence", "not_assessable"}

FIELD_NOTES = {
    "matched_total": "Total matches reported by the named source for the recorded query and cutoff.",
    "returned_count": "Records actually returned and reviewed in the current page or sample.",
    "family_scope": "Patent-family definition used for counts; default is INPADOC.",
    "litigation_signal": "Discovery lead from PatSnap legal data or a public source; requires primary-source verification.",
    "case_status": "Procedural posture as of the stated verification date, not a prediction.",
    "target_role": "The monitored target's verified role in the specific proceeding.",
    "risk_state": "Evidence-qualified screening state, not legal advice or an outcome forecast.",
}

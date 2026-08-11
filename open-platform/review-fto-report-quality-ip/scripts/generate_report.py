"""
Generate the formal English FTO report-quality assessment.

The generator preserves the source package's sixteen-section report contract,
four-dimension scorecard, three-layer review, independent-search comparison,
risk lists, issues, remediation actions, and fixed CSS dependency.

Security and evidence controls:

- every dynamic text value is HTML-escaped;
- links are restricted to http and https;
- no inline style attributes are generated;
- a fixed local CSS file is embedded verbatim;
- missing evidence remains visibly missing;
- no live search, legal-status check, claim review, or recall estimate is
  inferred from the presence of an empty data structure;
- pending applications are shown as a watchlist, not enforceable claims;
- fatal factual defects remain separate from the numerical quality score.

CLI:
    python generate_report.py [assessment.json] <output.html>
"""

from __future__ import annotations

import datetime as dt
import html
import json
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


SCRIPT_DIR = Path(__file__).resolve().parent
CSS_SOURCE = SCRIPT_DIR.parent / "assets" / "fto_report.css"

MANDATORY_MODULES = [
    "Executive summary",
    "Three-layer review overview",
    "Search-topic fit",
    "Search-scope coverage",
    "Independent-search comparison",
    "Claim-comparison rigor",
    "Higher-risk patent list",
    "Moderate-risk patent list",
    "Lower-risk patent list",
    "Response-measure quality",
    "Risk-mitigation recommendations",
    "Four-dimension scorecard and issue register",
    "Conclusion and remediation plan",
]

METHODOLOGY_LAYERS = [
    "Evidence and reproducibility",
    "Legal reasoning",
    "Decision usability",
]

DIMENSION_DEFAULTS = [
    {"name": "Search strategy quality", "score": None, "max": 25},
    {"name": "Patent analysis depth", "score": None, "max": 30},
    {"name": "Legal reasoning quality", "score": None, "max": 25},
    {"name": "Documentation and traceability", "score": None, "max": 20},
]

GRADE_CLASSES = {
    "Excellent": "grade-excellent",
    "Good": "grade-good",
    "Pass": "grade-pass",
    "Needs improvement": "grade-warning",
    "Fail": "grade-fail",
    "Fatal": "grade-fail",
    "Not scored": "grade-none",
}


def escape(value: Any) -> str:
    """Escape a dynamic value for element text."""
    return html.escape("" if value is None else str(value), quote=True)


def safe_url(value: Any) -> str:
    """Allow only absolute HTTP(S) links in generated evidence tables."""
    raw = str(value or "").strip()
    if not raw:
        return ""
    parsed = urlparse(raw)
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc:
        return ""
    return escape(raw)


def grade_class(grade: str) -> str:
    return GRADE_CLASSES.get(str(grade), "grade-none")


def coverage_class(rating: str) -> str:
    normalized = str(rating or "").lower()
    if "heuristic" in normalized:
        return "recall-low"
    if "not estimated" in normalized or "not executed" in normalized:
        return "recall-none"
    return "recall-none"


def percentage_class(value: Any) -> str:
    try:
        numeric = max(0.0, min(100.0, float(value)))
    except (TypeError, ValueError):
        numeric = 0.0
    bucket = int(round(numeric / 10.0) * 10)
    return f"pct-{bucket}"


def score_text(value: Any, maximum: Any = None) -> str:
    if value in (None, ""):
        return "Not scored"
    return f"{value}/{maximum}" if maximum not in (None, "") else str(value)


def score_percentage(score: Any, maximum: Any) -> float | None:
    try:
        denominator = float(maximum)
        if denominator <= 0:
            return None
        return max(0.0, min(100.0, 100.0 * float(score) / denominator))
    except (TypeError, ValueError):
        return None


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Merge a user payload into defaults without dropping nested defaults."""
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            deep_merge(base[key], value)
        else:
            base[key] = value
    return base


def empty_data() -> dict[str, Any]:
    """Return a truthful, visibly incomplete assessment skeleton."""
    layers = {
        name: {
            "status": "Not assessed",
            "confidence": "Not assessed",
            "findings": "Evidence not supplied.",
        }
        for name in METHODOLOGY_LAYERS
    }
    dimensions = [
        {
            **dimension,
            "comment": "Evidence not supplied.",
        }
        for dimension in DIMENSION_DEFAULTS
    ]
    return {
        "report_title": "FTO report quality assessment",
        "subject_report": "Not supplied",
        "submitter": "Not supplied",
        "product_description": "Not supplied",
        "target_market": "Not supplied",
        "relevant_acts": "Not supplied",
        "scenario": "Not determined",
        "exhibition_applicable": False,
        "industry_profile": "Not determined",
        "maturity": "Not assessed",
        "audit_date": dt.date.today().isoformat(),
        "data_cutoff": "Not supplied",
        "status_checked_as_of": "Not supplied",
        "claim_text_version": "Not supplied",
        "translation_source": "Not supplied",
        "counting_unit": "Not supplied",
        "family_method": "Not supplied",
        "auditor": "review-fto-report-quality-ip",
        "confidentiality": "Internal",
        "total_score": None,
        "grade": "Not scored",
        "fatal_status": "Not assessed",
        "fatal_defects": [],
        "conclusion": "No conclusion formed.",
        "methodology_layers": layers,
        "verification": {
            "status": "not_executed",
            "live_search_executed": False,
            "tool_status": "No live results supplied.",
            "counting_unit": "publication",
            "original_pool_count": None,
            "independent_pool_count": None,
            "overlap_count": None,
            "estimated_total": None,
            "recall_rate": "Not estimated",
            "recall_rating": "Not estimated",
            "observed_coverage": {
                "union_count": None,
                "original_share_of_observed_union_percent": None,
                "independent_share_of_observed_union_percent": None,
                "jaccard_overlap_percent": None,
            },
            "estimate": {
                "status": "not_estimated",
                "method": "Not applied",
                "assumptions_supported": False,
                "note": "No qualifying estimate was supplied.",
            },
            "route_counts": {},
            "route_overlap_matrix": [],
            "top_ipcs": [],
            "top_assignees": [],
            "omissions": [],
            "pending_application_watchlist": [],
            "validity_checks": [],
            "note": (
                "No live independent search was supplied. No omission or "
                "population-recall conclusion is available."
            ),
        },
        "dimensions": dimensions,
        "modules": {
            name: "Evidence not supplied." for name in MANDATORY_MODULES
        },
        "risk_lists": {"high": [], "medium": [], "low": []},
        "countermeasures": [],
        "issues": {"critical": [], "important": [], "suggestions": []},
        "mandatory_actions": [],
        "sources": [],
        "limitations": [],
    }


def load_data(json_path: str | None) -> dict[str, Any]:
    """Load and merge an assessment JSON object."""
    data = empty_data()
    if not json_path:
        print("No JSON input supplied; generating an incomplete review skeleton.")
        return data
    source = Path(json_path)
    try:
        loaded = json.loads(source.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Unable to load assessment JSON: {exc}") from exc
    if not isinstance(loaded, dict):
        raise ValueError("Assessment JSON must contain an object.")
    return deep_merge(data, loaded)


def load_fixed_css() -> str:
    """Read the sole style source and fail closed if it is missing."""
    if not CSS_SOURCE.is_file():
        raise FileNotFoundError(f"Fixed CSS source not found: {CSS_SOURCE}")
    return CSS_SOURCE.read_text(encoding="utf-8")


def table_empty(columns: int, message: str) -> str:
    return f"<tr><td colspan='{columns}'>{escape(message)}</td></tr>"


def issue_rows(items: list[dict[str, Any]], empty_message: str) -> str:
    if not items:
        return table_empty(3, empty_message)
    rows: list[str] = []
    for item in items:
        rows.append(
            "<tr>"
            f"<td>{escape(item.get('id') or '-')}</td>"
            f"<td>{escape(item.get('desc') or item.get('description') or '')}</td>"
            f"<td>{escape(item.get('impact') or item.get('suggestion') or '-')}</td>"
            "</tr>"
        )
    return "".join(rows)


def patent_rows(items: list[dict[str, Any]], empty_message: str) -> str:
    if not items:
        return table_empty(7, empty_message)
    rows: list[str] = []
    for item in items:
        rows.append(
            "<tr>"
            f"<td>{escape(item.get('patent_no') or item.get('no') or '-')}</td>"
            f"<td>{escape(item.get('title') or '-')}</td>"
            f"<td>{escape(item.get('assignee') or '-')}</td>"
            f"<td>{escape(item.get('jurisdiction') or '-')}</td>"
            f"<td>{escape(item.get('status') or 'Not verified')}</td>"
            f"<td>{escape(item.get('status_as_of') or '-')}</td>"
            f"<td>{escape(item.get('basis') or item.get('risk_basis') or '-')}</td>"
            "</tr>"
        )
    return "".join(rows)


def omission_rows(items: list[dict[str, Any]]) -> str:
    if not items:
        return table_empty(8, "No independent-pool candidate omissions supplied.")
    rows: list[str] = []
    for item in items:
        risk = str(item.get("risk_level") or "").lower()
        row_class = (
            "risk-high" if "high" in risk
            else "risk-medium" if "medium" in risk
            else "risk-normal"
        )
        number = escape(item.get("patent_no") or "-")
        url = safe_url(item.get("url"))
        number_cell = (
            f"<a href='{url}' target='_blank' rel='noopener noreferrer'>{number}</a>"
            if url else number
        )
        rows.append(
            f"<tr class='{row_class}'>"
            f"<td>{number_cell}</td>"
            f"<td>{escape(item.get('title') or '-')}</td>"
            f"<td>{escape(item.get('assignee') or '-')}</td>"
            f"<td>{escape(item.get('jurisdiction') or '-')}</td>"
            f"<td>{escape(item.get('status') or 'Not verified')}</td>"
            f"<td>{escape(item.get('status_as_of') or '-')}</td>"
            f"<td>{escape(item.get('source') or 'Independent retrieval')}</td>"
            f"<td>{escape(item.get('materiality') or 'Not assessed')}</td>"
            "</tr>"
        )
    return "".join(rows)


def pending_rows(items: list[dict[str, Any]]) -> str:
    if not items:
        return table_empty(6, "No pending-application watch items supplied.")
    rows: list[str] = []
    for item in items:
        rows.append(
            "<tr>"
            f"<td>{escape(item.get('patent_no') or item.get('patent_number') or '-')}</td>"
            f"<td>{escape(item.get('title') or '-')}</td>"
            f"<td>{escape(item.get('assignee') or '-')}</td>"
            f"<td>{escape(item.get('jurisdiction') or '-')}</td>"
            f"<td>{escape(item.get('status') or 'Pending; verify')}</td>"
            "<td>Watch item only; assess the current claim set and prosecution.</td>"
            "</tr>"
        )
    return "".join(rows)


def action_rows(items: list[dict[str, Any]]) -> str:
    if not items:
        return table_empty(8, "No remediation recommendation supplied.")
    rows: list[str] = []
    for item in items:
        rows.append(
            "<tr>"
            f"<td>{escape(item.get('id') or '-')}</td>"
            f"<td>{escape(item.get('patent_no') or '-')}</td>"
            f"<td>{escape(item.get('path_type') or item.get('type') or '-')}</td>"
            f"<td>{escape(item.get('action') or item.get('description') or '-')}</td>"
            f"<td>{escape(item.get('owner') or 'Unassigned')}</td>"
            f"<td>{escape(item.get('due_date') or '-')}</td>"
            f"<td>{escape(item.get('priority') or '-')}</td>"
            f"<td>{escape(item.get('evidence_gate') or 'Counsel review required')}</td>"
            "</tr>"
        )
    return "".join(rows)


def source_rows(items: list[dict[str, Any]]) -> str:
    if not items:
        return table_empty(5, "No source register supplied.")
    rows: list[str] = []
    for item in items:
        raw_url = safe_url(item.get("url"))
        source_name = escape(item.get("source") or item.get("name") or "-")
        source_cell = (
            f"<a href='{raw_url}' target='_blank' rel='noopener noreferrer'>"
            f"{source_name}</a>" if raw_url else source_name
        )
        rows.append(
            "<tr>"
            f"<td>{source_cell}</td>"
            f"<td>{escape(item.get('record_or_query') or '-')}</td>"
            f"<td>{escape(item.get('accessed') or '-')}</td>"
            f"<td>{escape(item.get('purpose') or '-')}</td>"
            f"<td>{escape(item.get('limitations') or '-')}</td>"
            "</tr>"
        )
    return "".join(rows)


def dimensions_html(dimensions: list[dict[str, Any]]) -> str:
    blocks: list[str] = []
    for dimension in dimensions:
        maximum = dimension.get("max")
        numeric = score_percentage(dimension.get("score"), maximum)
        blocks.append(
            "<div class='dim'>"
            f"<span>{escape(dimension.get('name') or 'Unnamed dimension')}</span>"
            "<div class='bar' aria-hidden='true'>"
            f"<i class='bar-fill {percentage_class(numeric)} grade-good'></i></div>"
            f"<b>{escape(score_text(dimension.get('score'), maximum))}</b>"
            f"<small>{escape(dimension.get('comment') or '')}</small>"
            "</div>"
        )
    return "".join(blocks)


def layers_html(data: dict[str, Any]) -> str:
    rows: list[str] = []
    layers = data.get("methodology_layers") or {}
    for name in METHODOLOGY_LAYERS:
        value = layers.get(name) or {}
        rows.append(
            "<tr>"
            f"<td>{escape(name)}</td>"
            f"<td>{escape(value.get('status') or 'Not assessed')}</td>"
            f"<td>{escape(value.get('confidence') or 'Not assessed')}</td>"
            f"<td>{escape(value.get('findings') or 'Evidence not supplied.')}</td>"
            "</tr>"
        )
    return "".join(rows)


def coverage_indicator(verification: dict[str, Any]) -> str:
    estimate = verification.get("estimate") or {}
    rating = str(verification.get("recall_rating") or "Not estimated")
    estimate_value = estimate.get("estimated_original_coverage_percent")
    if estimate.get("status") != "heuristic_estimate":
        display = "Not estimated"
        width = None
    else:
        display = f"{estimate_value}% heuristic"
        width = estimate_value
    return (
        f"<div class='gauge-wrap {coverage_class(rating)}'>"
        "<div class='gauge-label'>Qualified population-coverage estimate</div>"
        "<div class='gauge-bar' aria-hidden='true'>"
        f"<div class='gauge-fill {percentage_class(width)}'></div></div>"
        f"<div class='gauge-value'>{escape(display)} — {escape(rating)}</div>"
        "<p class='data-note'>Observed-pool coverage is not true recall. "
        "Use an estimate only when its assumptions are documented.</p></div>"
    )


def module(data: dict[str, Any], name: str) -> str:
    return escape((data.get("modules") or {}).get(name) or "Evidence not supplied.")


def list_items(values: list[Any], empty_message: str) -> str:
    if not values:
        return f"<li>{escape(empty_message)}</li>"
    return "".join(f"<li>{escape(value)}</li>" for value in values)


def ranked_values(values: list[Any]) -> str:
    """Format ranked strings or ``{value, count}`` records safely."""

    rendered: list[str] = []
    for item in values:
        if isinstance(item, dict):
            value = item.get("value") or item.get("name") or item.get("code") or "-"
            count = item.get("count")
            rendered.append(f"{value} ({count})" if count is not None else str(value))
        else:
            rendered.append(str(item))
    return ", ".join(rendered) if rendered else "Not supplied"


def generate_html(data: dict[str, Any], output_path: Path) -> Path:
    """Generate one self-contained, print-safe HTML assessment."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    css = load_fixed_css()
    grade = str(data.get("grade") or "Not scored")
    fatal_status = str(data.get("fatal_status") or "Not assessed")
    verification = data.get("verification") or {}
    observed = verification.get("observed_coverage") or {}
    estimate = verification.get("estimate") or {}
    risks = data.get("risk_lists") or {}
    issues = data.get("issues") or {}
    actions = data.get("countermeasures") or []
    fatal_defects = data.get("fatal_defects") or []
    fatal_banner = ""
    if grade.lower() == "fatal" or fatal_defects:
        fatal_banner = (
            "<aside class='fatal-banner' role='alert'>"
            "Fatal defect — do not use the reviewed report for the stated "
            "decision until the listed defect is cured.</aside>"
        )

    document = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <title>{escape(data.get("report_title"))}</title>
  <style id="fto-fixed-style">
{css}
  </style>
</head>
<body>
<header class="hero">
  <h1>{escape(data.get("report_title"))}</h1>
  <p class="subtitle">Evidence-based quality review of an existing freedom-to-operate report</p>
  <div class="meta">
    <div><span>Report reviewed</span>{escape(data.get("subject_report"))}</div>
    <div><span>Target market</span>{escape(data.get("target_market"))}</div>
    <div><span>Scenario</span>{escape(data.get("scenario"))}</div>
    <div><span>Review date</span>{escape(data.get("audit_date"))}</div>
  </div>
  <div class="scene-badge">Scenario: {escape(data.get("scenario"))}</div>
</header>
<main class="wrap">
  {fatal_banner}
  <section class="card">
    <h2><span class="chapter-no">1.</span>Report identity and scope</h2>
    <table>
      <caption>Scope and evidence controls</caption>
      <tr><th>Field</th><th>Recorded value</th></tr>
      <tr><td>Report reviewed</td><td>{escape(data.get("subject_report"))}</td></tr>
      <tr><td>Submitting party</td><td>{escape(data.get("submitter"))}</td></tr>
      <tr><td>Product or technology</td><td>{escape(data.get("product_description"))}</td></tr>
      <tr><td>Target market</td><td>{escape(data.get("target_market"))}</td></tr>
      <tr><td>Relevant acts</td><td>{escape(data.get("relevant_acts"))}</td></tr>
      <tr><td>Data cutoff</td><td>{escape(data.get("data_cutoff"))}</td></tr>
      <tr><td>Status checked as of</td><td>{escape(data.get("status_checked_as_of"))}</td></tr>
      <tr><td>Claim text version</td><td>{escape(data.get("claim_text_version"))}</td></tr>
      <tr><td>Translation source</td><td>{escape(data.get("translation_source"))}</td></tr>
      <tr><td>Counting unit</td><td>{escape(data.get("counting_unit"))}</td></tr>
      <tr><td>Family method</td><td>{escape(data.get("family_method"))}</td></tr>
      <tr><td>Confidentiality</td><td>{escape(data.get("confidentiality"))}</td></tr>
    </table>
  </section>

  <section class="card">
    <h2><span class="chapter-no">2.</span>Executive summary</h2>
    <div class="score {grade_class(grade)}">{escape(score_text(data.get("total_score"), 100))}</div>
    <p class="grade-label">Quality grade: {escape(grade)}</p>
    <p><b>Fatal-defect status:</b> {escape(fatal_status)}</p>
    <p><b>Conclusion:</b> {escape(data.get("conclusion"))}</p>
    <p><b>Report maturity:</b> {escape(data.get("maturity"))}</p>
    <div class="disclosure">{module(data, "Executive summary")}</div>
    <h3>Fatal factual defects</h3>
    <ul>{list_items(fatal_defects, "No fatal-defect finding supplied.")}</ul>
  </section>

  <section class="card">
    <h2><span class="chapter-no">3.</span>Three-layer review overview</h2>
    <table>
      <tr><th>Layer</th><th>Status</th><th>Confidence</th><th>Key finding</th></tr>
      {layers_html(data)}
    </table>
  </section>

  <section class="card">
    <h2><span class="chapter-no">4.</span>Four-dimension scorecard</h2>
    {dimensions_html(data.get("dimensions") or [])}
    <p class="data-note">Scores measure report quality, not infringement probability or legal clearance.</p>
  </section>

  <section class="card verify">
    <h2><span class="chapter-no">5.</span>Independent-search comparison and omissions</h2>
    {coverage_indicator(verification)}
    <table>
      <caption>Observed pools and qualified estimate</caption>
      <tr><th>Metric</th><th>Result</th></tr>
      <tr><td>Verification status</td><td>{escape(verification.get("status"))}</td></tr>
      <tr><td>Live search executed</td><td>{escape(verification.get("live_search_executed"))}</td></tr>
      <tr><td>Route counts</td><td>{escape(json.dumps(verification.get("route_counts") or {}, ensure_ascii=False))}</td></tr>
      <tr><td>Original report pool</td><td>{escape(verification.get("original_pool_count"))}</td></tr>
      <tr><td>Independent pool</td><td>{escape(verification.get("independent_pool_count"))}</td></tr>
      <tr><td>Observed overlap</td><td>{escape(verification.get("overlap_count"))}</td></tr>
      <tr><td>Observed union</td><td>{escape(observed.get("union_count"))}</td></tr>
      <tr><td>Jaccard overlap</td><td>{escape(observed.get("jaccard_overlap_percent"))}%</td></tr>
      <tr><td>Estimate status</td><td>{escape(estimate.get("status"))}</td></tr>
      <tr><td>Estimate method</td><td>{escape(estimate.get("method"))}</td></tr>
      <tr><td>Assumptions supported</td><td>{escape(estimate.get("assumptions_supported"))}</td></tr>
      <tr><td>Estimate note</td><td>{escape(estimate.get("note") or verification.get("note"))}</td></tr>
    <tr><td>Top IPC/CPC sections</td><td>{escape(ranked_values(verification.get("top_ipcs") or []))}</td></tr>
    <tr><td>Top assignees</td><td>{escape(ranked_values(verification.get("top_assignees") or []))}</td></tr>
    </table>
    <h3>Candidate omissions</h3>
    <table>
      <tr><th>Patent</th><th>Title</th><th>Assignee</th><th>Jurisdiction</th><th>Status</th><th>Status date</th><th>Route</th><th>Materiality</th></tr>
      {omission_rows(verification.get("omissions") or [])}
    </table>
    <h3>Recent pending-application watchlist</h3>
    <table>
      <tr><th>Application</th><th>Title</th><th>Applicant</th><th>Jurisdiction</th><th>Status</th><th>Interpretation</th></tr>
      {pending_rows(verification.get("pending_application_watchlist") or [])}
    </table>
  </section>

  <section class="card">
    <h2><span class="chapter-no">6.</span>Search-topic fit</h2>
    <p>{module(data, "Search-topic fit")}</p>
  </section>

  <section class="card">
    <h2><span class="chapter-no">7.</span>Search-scope coverage</h2>
    <p>{module(data, "Search-scope coverage")}</p>
  </section>

  <section class="card">
    <h2><span class="chapter-no">8.</span>Claim-comparison rigor</h2>
    <p>{module(data, "Claim-comparison rigor")}</p>
  </section>

  <section class="card">
    <h2><span class="chapter-no">9.</span>Higher-risk patent list</h2>
    <p>{module(data, "Higher-risk patent list")}</p>
    <table>
      <tr><th>Patent</th><th>Title</th><th>Right holder</th><th>Jurisdiction</th><th>Status</th><th>Status date</th><th>Evidence basis</th></tr>
      {patent_rows(risks.get("high") or [], "No higher-risk patent finding supplied.")}
    </table>
  </section>

  <section class="card">
    <h2><span class="chapter-no">10.</span>Moderate-risk patent list</h2>
    <p>{module(data, "Moderate-risk patent list")}</p>
    <table>
      <tr><th>Patent</th><th>Title</th><th>Right holder</th><th>Jurisdiction</th><th>Status</th><th>Status date</th><th>Evidence basis</th></tr>
      {patent_rows(risks.get("medium") or [], "No moderate-risk patent finding supplied.")}
    </table>
  </section>

  <section class="card">
    <h2><span class="chapter-no">11.</span>Lower-risk patent list</h2>
    <p>{module(data, "Lower-risk patent list")}</p>
    <table>
      <tr><th>Patent</th><th>Title</th><th>Right holder</th><th>Jurisdiction</th><th>Status</th><th>Status date</th><th>Evidence basis</th></tr>
      {patent_rows(risks.get("low") or [], "No lower-risk patent finding supplied.")}
    </table>
  </section>

  <section class="card">
    <h2><span class="chapter-no">12.</span>Response-measure quality</h2>
    <p>{module(data, "Response-measure quality")}</p>
  </section>

  <section class="card mitigation">
    <h2><span class="chapter-no">13.</span>Risk-mitigation recommendations</h2>
    <p>{module(data, "Risk-mitigation recommendations")}</p>
    <table>
      <tr><th>ID</th><th>Patent</th><th>Path</th><th>Action</th><th>Owner</th><th>Due date</th><th>Priority</th><th>Evidence gate</th></tr>
      {action_rows(actions)}
    </table>
  </section>

  <section class="card">
    <h2><span class="chapter-no">14.</span>Consolidated issue register</h2>
    <h3>Critical issues</h3>
    <table><tr><th>ID</th><th>Issue</th><th>Impact or recommendation</th></tr>
      {issue_rows(issues.get("critical") or [], "No critical issue supplied.")}
    </table>
    <h3>Important issues</h3>
    <table><tr><th>ID</th><th>Issue</th><th>Impact or recommendation</th></tr>
      {issue_rows(issues.get("important") or [], "No important issue supplied.")}
    </table>
    <h3>Suggested improvements</h3>
    <table><tr><th>ID</th><th>Suggestion</th><th>Explanation</th></tr>
      {issue_rows(issues.get("suggestions") or [], "No suggested improvement supplied.")}
    </table>
  </section>

  <section class="card">
    <h2><span class="chapter-no">15.</span>Conclusion and remediation plan</h2>
    <p><b>Conclusion:</b> {escape(data.get("conclusion"))}</p>
    <ol>{list_items(data.get("mandatory_actions") or [], "No mandatory action supplied.")}</ol>
    <h3>Source register</h3>
    <table>
      <tr><th>Source</th><th>Record or query</th><th>Accessed</th><th>Purpose</th><th>Limitations</th></tr>
      {source_rows(data.get("sources") or [])}
    </table>
  </section>

  <section class="card">
    <h2><span class="chapter-no">16.</span>Review boundary and disclaimer</h2>
    <div class="disclosure">
      This is an automated quality review of an existing FTO report and is not
      a legal opinion, clearance opinion, validity opinion, or guarantee of
      non-infringement. Patent scope, infringement, equivalents, indirect
      infringement, enforceability, remedies, and procedure are
      jurisdiction-specific. Simple legal-status data is not a dispositive
      validity determination. Verify material records in official registers
      and obtain advice from qualified counsel in each relevant jurisdiction.
      Patent FTO does not by itself cover trademarks, copyright, trade secrets,
      contracts, standards licenses, regulatory compliance, product safety,
      export controls, or other non-patent obligations.
    </div>
    <h3>Recorded limitations</h3>
    <ul>{list_items(data.get("limitations") or [], "No additional limitation supplied.")}</ul>
  </section>
</main>
</body>
</html>
"""
    output_path.write_text(document, encoding="utf-8")
    return output_path


def main() -> int:
    if len(sys.argv) == 2:
        json_path = None
        output_path = Path(sys.argv[1])
    elif len(sys.argv) == 3:
        json_path = sys.argv[1]
        output_path = Path(sys.argv[2])
    else:
        print(
            "Usage: python generate_report.py [assessment.json] <output.html>",
            file=sys.stderr,
        )
        return 2
    if output_path.suffix.lower() != ".html":
        print("Output path must use the .html extension.", file=sys.stderr)
        return 2
    try:
        data = load_data(json_path)
        generated = generate_html(data, output_path)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f"Unable to generate report: {exc}", file=sys.stderr)
        return 1
    print(f"Generated HTML assessment: {generated}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

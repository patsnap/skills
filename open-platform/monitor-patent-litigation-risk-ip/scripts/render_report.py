"""Render a safe, offline, target-centric patent-litigation monitoring report.

The active SKILL.md defaults to direct evidence-backed HTML authoring. This
renderer is retained from the source package as an optional deterministic export
path and for regression testing. It does not retrieve or infer facts.
"""

# Renderer data contract
#
# This comment intentionally documents every source capability consumed by the
# renderer. It keeps the retained script independently maintainable without
# duplicating legal or research instructions from SKILL.md.
#
# Root metadata
# - schema_version: orchestrator schema version.
# - generated_at: UTC artifact-generation timestamp.
# - cutoff_date: last substantive verification date.
# - report_language: requested report language.
# - target: canonical monitored organization.
# - comparison_parties: other named organizations.
# - scope: search coverage, caps, family rule, and limitations.
# - overview: reconciled descriptive counts.
# - family_analysis: geography, classifications, status, and claims.
# - litigated_patents: qualified patent records.
# - litigation_timeline: cross-case chronological events.
# - cases: proceeding records.
# - inventors: descriptive inventor activity.
# - conclusions: geographic exposure, alert, trend, and actions.
# - sources: evidence register.
# - assumptions: explicit analyst assumptions.
# - limitations: report-level coverage limits.
#
# Target metadata
# - target.name is required before substantive output.
# - target.aliases contains only sourced aliases.
# - target.role_basis explains why the first party is primary.
# - comparison parties never replace the target as report subject.
#
# Scope metadata
# - jurisdictions lists included forums and authorities.
# - family_scope states the family definition.
# - inventor_lookback_years controls descriptive recent activity.
# - max_litigated_per_party discloses the review cap.
# - top_inventors discloses the presentation cap.
# - searches holds reproducible retrieval logs.
# - limitations states access, language, and coverage restrictions.
#
# Overview counts
# - party_count counts named organizations.
# - candidate_patent_count counts de-duplicated leads.
# - verified_asserted_patent_count counts sufficiently linked patents.
# - family_member_count counts publications under one family rule.
# - verified_case_count counts sufficiently verified proceedings.
# - party_patent_map stores explicit relationship edges.
#
# Patent identity
# - publication_number is the display and reconciliation key.
# - application_number remains separate from publication number.
# - patent_url must use HTTP or HTTPS.
# - title is escaped before rendering.
# - filing_date is distinct from publication_date.
# - priority_date is not presented as entitlement analysis.
#
# Patent legal context
# - legal_status is a source label, not an enforceability opinion.
# - legal_status_as_of is required for current-status wording.
# - target_role comes from the proceeding record.
# - risk_state is evidence-qualified, not predictive.
# - evidence_state reports verification completeness.
# - case_ids must resolve to existing case records.
# - asserted_claims contains only publicly verified claim numbers.
#
# Patent image handling
# - abstract_image_b64 accepts a bounded raw PNG base64 payload.
# - abstract_image_url accepts an absolute HTTP(S) fallback.
# - active data formats are rejected.
# - invalid base64 is rejected.
# - missing images do not block substantive rendering.
# - alt text identifies the associated publication.
#
# Patent technical context
# - technology_problem summarizes the disclosed problem.
# - technology_means summarizes the disclosed solution mechanism.
# - technology_effect summarizes the disclosed result or benefit.
# - open_questions preserves unresolved evidence issues.
# - claims preserves exact or provenance-labeled translated text.
# - claim_source_language identifies authoritative language.
# - family_members preserves member-specific facts.
# - sources links patent facts to evidence.
#
# Family member fields
# - publication_number identifies the family publication.
# - application_number remains separate when supplied.
# - jurisdiction is the filing authority.
# - relationship_type records continuation, divisional, or national stage.
# - filing_date is not substituted for priority date.
# - publication_date is not substituted for grant date.
# - grant_date is optional and source-verified.
# - priority_date is qualified where entitlement is not reviewed.
# - legal_status is member-specific.
# - legal_status_as_of makes status wording temporal.
# - representative_reason explains claim selection.
# - translation_provenance identifies working translations.
# - source provides the member locator.
#
# Family analysis
# - geography stores jurisdiction-level descriptive records.
# - classifications stores classification counts and rules.
# - legal_detail stores dated member-specific events.
# - geographic_analysis stores qualified prose.
# - claim_comparison stores representative-claim differences.
# - counting_rule controls family aggregation.
#
# Geographic row fields
# - jurisdiction names the relevant authority.
# - family_count follows the stated family definition.
# - active_count follows a named status source and date.
# - pending_count follows a named status source and date.
# - risk_state is not inferred from counts alone.
# - reason explains evidence and uncertainty.
#
# Case identity
# - case_id is stable within all artifacts.
# - case_name is the verified caption.
# - case_number is the official proceeding identifier.
# - tribunal identifies the court, board, or agency.
# - jurisdiction identifies the territorial forum.
# - filed_date is labeled according to the source event.
# - verified_as_of states currentness.
#
# Case parties and role
# - plaintiffs contains verified plaintiffs or complainants.
# - defendants contains verified defendants or respondents.
# - target_role describes this target in this proceeding.
# - counterclaimants may be represented through target_role and allegations.
# - party names are escaped and never used as raw HTML.
#
# Case patent links
# - asserted_patents contains verified identifiers.
# - asserted_claims contains public claim-level information.
# - patent links do not propagate to unrelated family members.
# - missing asserted claims are shown as unverified, not inferred.
#
# Case substance
# - allegations remains clearly labeled as party content.
# - defenses remains clearly labeled as party content.
# - procedural_posture states current stage.
# - disposition distinguishes final and non-final outcomes.
# - appeal records current verified appeal information.
# - timeline holds case-specific events.
# - sources prioritizes primary records.
# - evidence_state reports verification completeness.
#
# Timeline fields
# - date uses ISO format when a complete date is known.
# - case_id resolves to a case record.
# - event uses neutral procedural language.
# - event_type distinguishes filing, order, judgment, and appeal.
# - patents lists only patents relevant to the event.
# - claims lists only claims relevant to the event.
# - target_role is event-consistent.
# - source points to a stable source ID or locator.
# - evidence_state discloses verification.
# - uncertainty preserves partial or conflicting dates.
#
# Inventor fields
# - name is the disambiguated display name.
# - name_variants preserves source forms.
# - identity_confidence states ambiguity.
# - recent_count follows a stated counting method.
# - yearly_stats supports time distribution.
# - top_classifications uses source classifications.
# - technology_focus uses evidence-backed themes.
# - representative_publications provides examples.
# - note states descriptive limits.
# - source and cutoff establish currentness.
#
# Conclusion fields
# - geographic_exposure is a list of jurisdiction records or statements.
# - litigation_alert summarizes verified posture and monitoring needs.
# - technology_trend distinguishes observations from hypotheses.
# - actions provides priority, owner, trigger, evidence, and completion rule.
# - no conclusion is calculated from color or a hidden score.
# - no conclusion predicts a legal outcome as fact.
#
# Source fields
# - id is stable and unique.
# - type distinguishes primary, patent, and secondary sources.
# - label is human-readable.
# - issuing_body identifies the authority when known.
# - ref or url supplies the locator.
# - accessed_at supplies retrieval date.
# - coverage explains what the source establishes.
# - limitation explains what it does not establish.
# - language and translation provenance remain visible.
#
# Safety contract
# - esc() handles every external text insertion.
# - safe_url() allows only absolute HTTP(S) links.
# - safe_image_data() validates bounded base64.
# - no remote JavaScript is emitted.
# - no remote font is required.
# - no analytics or tracker is emitted.
# - no local absolute path is embedded.
# - no secret or API key is embedded.
# - no source HTML is trusted.
# - links receive noopener and noreferrer.
# - missing values receive neutral text.
#
# Accessibility contract
# - one h1 describes the report.
# - heading order remains hierarchical.
# - navigation labels are descriptive.
# - tables use captions and column headers.
# - states include visible text.
# - images include descriptive alt text.
# - contrast is sufficient on paper and screen.
# - narrow screens retain horizontal table access.
# - print output hides sticky navigation.
# - printed tables repeat headers where supported.
#
# Rendering contract
# - render() is deterministic for identical input and generation metadata.
# - render() does not retrieve, enrich, or infer evidence.
# - render() tolerates absent optional arrays.
# - render() preserves zero counts.
# - render() reconciles displayed records with input arrays.
# - render() outputs a complete HTML document.
# - output uses UTF-8.
# - report language defaults to English.
# - generated output stays outside the skill package.
#
# Test contract
# - the smoke fixture is explicitly synthetic.
# - schema validation catches unsafe URLs.
# - schema validation catches unknown case references.
# - schema validation catches invalid roles and states.
# - renderer escapes an injected script element.
# - renderer removes a JavaScript URL.
# - renderer contains the target, case, and patent.
# - renderer contains no remote CDN reference.
# - renderer contains no unintended CJK text.
# - tests run with bytecode writing disabled where possible.
from __future__ import annotations

import argparse
import base64
import html
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


STYLE = """
:root {
  --ink: #172033;
  --muted: #5d6878;
  --navy: #173b67;
  --blue: #2d648f;
  --line: #d8dee8;
  --panel: #f6f8fb;
  --paper: #ffffff;
  --elevated: #9e3d38;
  --moderate: #8b6418;
  --lower: #28664d;
  --unknown: #667085;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  color: var(--ink);
  background: #edf1f6;
  font: 15px/1.55 Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
}
main { max-width: 1180px; margin: 0 auto; background: var(--paper); min-height: 100vh; }
header { padding: 40px 48px 30px; color: white; background: var(--navy); }
.eyebrow { margin: 0 0 8px; color: #c9d8ea; font-size: 12px; letter-spacing: .12em; text-transform: uppercase; }
h1 { margin: 0; max-width: 900px; font-size: clamp(28px, 4vw, 44px); line-height: 1.12; }
.subtitle { margin: 14px 0 0; max-width: 880px; color: #e4edf7; }
.meta { display: flex; flex-wrap: wrap; gap: 10px 22px; margin-top: 22px; font-size: 13px; }
nav { position: sticky; top: 0; z-index: 3; padding: 10px 48px; background: #f9fbfd; border-bottom: 1px solid var(--line); }
nav a { display: inline-block; margin: 4px 18px 4px 0; color: var(--navy); font-size: 13px; font-weight: 650; text-decoration: none; }
.content { padding: 24px 48px 64px; }
section { scroll-margin-top: 60px; padding: 24px 0; border-bottom: 1px solid var(--line); }
h2 { margin: 0 0 14px; color: var(--navy); font-size: 22px; }
h3 { margin: 20px 0 10px; font-size: 16px; }
p { max-width: 90ch; }
.grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; }
.stat, .card { border: 1px solid var(--line); border-radius: 8px; background: var(--paper); }
.stat { padding: 16px; }
.stat b { display: block; margin-top: 4px; font-size: 26px; color: var(--navy); }
.label { color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: .05em; }
.card { margin: 12px 0; padding: 18px; }
.card-head { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 10px; }
.badge { display: inline-block; border: 1px solid currentColor; border-radius: 999px; padding: 2px 8px; font-size: 12px; font-weight: 650; }
.elevated { color: var(--elevated); }
.moderate { color: var(--moderate); }
.lower_on_reviewed_evidence { color: var(--lower); }
.not_assessable, .unverified, .conflicting { color: var(--unknown); }
.table-wrap { width: 100%; overflow-x: auto; border: 1px solid var(--line); border-radius: 7px; }
table { width: 100%; border-collapse: collapse; font-size: 13px; }
caption { padding: 10px 12px; text-align: left; color: var(--muted); font-weight: 650; }
th, td { padding: 9px 11px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }
th { color: var(--navy); background: var(--panel); font-weight: 700; }
tr:last-child td { border-bottom: 0; }
.timeline { margin: 0; padding: 0; list-style: none; }
.timeline li { position: relative; margin-left: 8px; padding: 0 0 18px 22px; border-left: 2px solid #b7c7da; }
.timeline li::before { content: ""; position: absolute; left: -6px; top: 5px; width: 10px; height: 10px; border-radius: 50%; background: var(--blue); }
.source { color: var(--muted); font-size: 12px; overflow-wrap: anywhere; }
.callout { padding: 14px 16px; border-left: 4px solid var(--blue); background: var(--panel); }
.patent-image { display: block; max-width: 100%; max-height: 260px; margin: 12px auto; object-fit: contain; }
a { color: #155e91; overflow-wrap: anywhere; }
footer { padding: 24px 48px 40px; color: var(--muted); font-size: 12px; }
@media (max-width: 850px) {
  header, .content, footer { padding-left: 22px; padding-right: 22px; }
  nav { padding-left: 22px; padding-right: 22px; }
  .grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (max-width: 500px) { .grid { grid-template-columns: 1fr; } }
@media print {
  body, main { background: white; }
  nav { display: none; }
  header { background: white; color: var(--ink); border-bottom: 2px solid var(--navy); }
  header .subtitle, header .eyebrow { color: var(--muted); }
  section, .card { break-inside: avoid; }
  thead { display: table-header-group; }
  a { color: inherit; text-decoration: none; }
}
"""


def esc(value) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def safe_url(value: str) -> str:
    """Return only an absolute HTTP(S) URL."""
    value = str(value or "").strip()
    parsed = urlparse(value)
    return value if parsed.scheme in {"http", "https"} and parsed.netloc else ""


def safe_image_data(value: str) -> str:
    """Accept a bounded base64 payload, not an arbitrary data URL."""
    value = str(value or "").strip()
    if not value or len(value) > 8_000_000:
        return ""
    try:
        base64.b64decode(value, validate=True)
    except Exception:
        return ""
    return f"data:image/png;base64,{value}"


def link(label: str, url: str) -> str:
    checked = safe_url(url)
    return f'<a href="{esc(checked)}" rel="noopener noreferrer">{esc(label)}</a>' if checked else esc(label)


def text_list(values) -> str:
    items = values if isinstance(values, list) else []
    if not items:
        return '<p class="source">Not reported.</p>'
    return "<ul>" + "".join(f"<li>{esc(item)}</li>" for item in items) + "</ul>"


def source_list(values) -> str:
    items = values if isinstance(values, list) else []
    if not items:
        return '<p class="source">No source locator supplied.</p>'
    rows = []
    for item in items:
        if isinstance(item, dict):
            label = item.get("label") or item.get("id") or "Source"
            locator = item.get("url") or item.get("ref") or ""
            rows.append(f"<li>{link(label, locator) if safe_url(locator) else esc(label)} — {esc(locator)}</li>")
        else:
            rows.append(f"<li>{esc(item)}</li>")
    return '<ul class="source">' + "".join(rows) + "</ul>"


def table(caption: str, headers: list[str], rows: list[list[object]]) -> str:
    head = "".join(f"<th scope=\"col\">{esc(value)}</th>" for value in headers)
    body = "".join("<tr>" + "".join(f"<td>{esc(value)}</td>" for value in row) + "</tr>" for row in rows)
    if not rows:
        body = f'<tr><td colspan="{len(headers)}">No verified records.</td></tr>'
    return f'<div class="table-wrap"><table><caption>{esc(caption)}</caption><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def render_patents(patents: list[dict]) -> str:
    if not patents:
        return '<p class="callout">No patent has been verified as asserted in the reviewed proceedings.</p>'
    blocks = []
    for patent in patents:
        number = patent.get("publication_number") or "Publication number unavailable"
        risk = patent.get("risk_state") or "not_assessable"
        image = safe_image_data(patent.get("abstract_image_b64", ""))
        image_url = safe_url(patent.get("abstract_image_url", ""))
        image_html = ""
        if image:
            image_html = f'<img class="patent-image" src="{image}" alt="First drawing for {esc(number)}">'
        elif image_url:
            image_html = f'<img class="patent-image" src="{esc(image_url)}" alt="First drawing for {esc(number)}">'
        family_rows = [
            [member.get("publication_number") or member.get("pn", ""), member.get("jurisdiction", ""), member.get("legal_status", ""), member.get("filing_date") or member.get("apply_date", "")]
            for member in patent.get("family_members", [])
        ]
        blocks.append(f"""
        <article class="card">
          <div class="card-head"><h3>{link(number, patent.get('patent_url', ''))}</h3><span class="badge {esc(risk)}">{esc(risk.replace('_', ' ').title())}</span></div>
          <p><strong>{esc(patent.get('title', 'Title unavailable'))}</strong></p>
          <p class="source">Target role: {esc(patent.get('target_role', 'other'))} · Evidence: {esc(patent.get('evidence_state', 'unverified'))} · Status as of: {esc(patent.get('legal_status_as_of', 'not supplied'))}</p>
          {image_html}
          <p><strong>Technical problem:</strong> {esc(patent.get('technology_problem', ''))}</p>
          <p><strong>Technical means:</strong> {esc(patent.get('technology_means', ''))}</p>
          <p><strong>Technical effect:</strong> {esc(patent.get('technology_effect', ''))}</p>
          <p><strong>Asserted claims:</strong> {esc(', '.join(map(str, patent.get('asserted_claims', []))) or 'Not verified')}</p>
          {table('Family members', ['Publication', 'Jurisdiction', 'Status', 'Filing date'], family_rows)}
          <h3>Patent evidence</h3>{source_list(patent.get('sources', []))}
        </article>
        """)
    return "".join(blocks)


def render_cases(cases: list[dict]) -> str:
    if not cases:
        return '<p class="callout">No proceeding has been verified against a primary source.</p>'
    blocks = []
    for case in cases:
        timeline_rows = [
            [event.get("date", ""), event.get("event", ""), event.get("source", "")]
            for event in case.get("timeline", []) if isinstance(event, dict)
        ]
        blocks.append(f"""
        <article class="card">
          <div class="card-head"><h3>{esc(case.get('case_name') or case.get('case_id', 'Case'))}</h3><span class="badge {esc(case.get('evidence_state', 'unverified'))}">{esc(case.get('evidence_state', 'unverified').replace('_', ' ').title())}</span></div>
          <p class="source">{esc(case.get('tribunal', ''))} · {esc(case.get('case_number', ''))} · Verified as of {esc(case.get('verified_as_of', 'not supplied'))}</p>
          <p><strong>Plaintiff(s):</strong> {esc(', '.join(case.get('plaintiffs', [])))}</p>
          <p><strong>Defendant(s):</strong> {esc(', '.join(case.get('defendants', [])))}</p>
          <p><strong>Target role:</strong> {esc(case.get('target_role', 'other'))}</p>
          <p><strong>Procedural posture:</strong> {esc(case.get('procedural_posture', ''))}</p>
          <p><strong>Disposition:</strong> {esc(case.get('disposition', 'Not finally determined or not reported'))}</p>
          <h3>Allegations</h3>{text_list(case.get('allegations', []))}
          <h3>Defenses</h3>{text_list(case.get('defenses', []))}
          {table('Case timeline', ['Date', 'Verified event', 'Source'], timeline_rows)}
          <h3>Primary sources</h3>{source_list(case.get('sources', []))}
        </article>
        """)
    return "".join(blocks)


def render(data: dict, lang: str = "en") -> str:
    """Render a complete HTML document while escaping all external text."""
    target = data.get("target", {}).get("name") or "Target not supplied"
    overview = data.get("overview", {})
    generated = data.get("generated_at") or datetime.now(timezone.utc).isoformat()
    cutoff = data.get("cutoff_date") or "Not supplied"
    cases = data.get("cases", [])
    patents = data.get("litigated_patents", [])
    timeline = data.get("litigation_timeline", [])
    timeline_html = "<ul class=\"timeline\">" + "".join(
        f"<li><strong>{esc(item.get('date', ''))}</strong><br>{esc(item.get('event') or item.get('title', ''))}<br><span class=\"source\">{esc(item.get('case_id', ''))} · {esc(item.get('source', ''))}</span></li>"
        for item in timeline if isinstance(item, dict)
    ) + "</ul>"
    if not timeline:
        timeline_html = '<p class="callout">No verified timeline events.</p>'
    geo_rows = [
        [row.get("jurisdiction", ""), row.get("family_count", row.get("count", "")), row.get("active_count", ""), row.get("pending_count", ""), row.get("risk_state", ""), row.get("reason", "")]
        for row in data.get("family_analysis", {}).get("geography", [])
    ]
    inventor_rows = [
        [row.get("name", ""), row.get("recent_count", ""), ", ".join(row.get("top_classifications", row.get("top_ipc", []))), ", ".join(row.get("technology_focus", [])), row.get("note", "")]
        for row in data.get("inventors", [])
    ]
    action_rows = [
        [row.get("priority", ""), row.get("action", ""), row.get("owner", ""), row.get("trigger", ""), row.get("evidence", "")]
        for row in data.get("conclusions", {}).get("actions", [])
    ]
    source_rows = [
        [row.get("id", ""), row.get("type", ""), row.get("label", ""), row.get("ref") or row.get("url", ""), row.get("accessed_at", ""), row.get("coverage", "")]
        for row in data.get("sources", []) if isinstance(row, dict)
    ]
    stats = [
        ("Named parties", overview.get("party_count", 0)),
        ("Verified cases", overview.get("verified_case_count", len(cases))),
        ("Verified asserted patents", overview.get("verified_asserted_patent_count", len(patents))),
        ("Family members", overview.get("family_member_count", 0)),
    ]
    stat_html = "".join(f'<div class="stat"><span class="label">{esc(label)}</span><b>{esc(value)}</b></div>' for label, value in stats)
    conclusions = data.get("conclusions", {})
    return f"""<!doctype html>
<html lang="{esc(lang)}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(target)} — Patent Litigation Risk Monitoring</title><style>{STYLE}</style></head>
<body><main>
<header><p class="eyebrow">Evidence-backed monitoring report</p><h1>{esc(target)} — Patent Litigation Risk Monitoring</h1><p class="subtitle">Target-centric review of verified proceedings, asserted patents, family coverage, legal events, inventor activity, and evidence-qualified actions.</p><div class="meta"><span>Cutoff: {esc(cutoff)}</span><span>Generated: {esc(generated)}</span><span>Schema: {esc(data.get('schema_version', ''))}</span></div></header>
<nav><a href="#summary">Summary</a><a href="#scope">Scope</a><a href="#timeline">Timeline</a><a href="#patents">Patents</a><a href="#cases">Cases</a><a href="#inventors">Inventors</a><a href="#conclusions">Conclusions</a><a href="#sources">Sources</a></nav>
<div class="content">
<section id="summary"><h2>Executive summary</h2><div class="grid">{stat_html}</div><p class="callout">Patent-database litigation signals are discovery leads. Case facts and current posture require verification against primary tribunal or official-register sources.</p></section>
<section id="scope"><h2>Scope and method</h2><p><strong>Primary target:</strong> {esc(target)}</p><p><strong>Comparison parties:</strong> {esc(', '.join(data.get('comparison_parties', [])) or 'None')}</p><p><strong>Family scope:</strong> {esc(data.get('scope', {}).get('family_scope', ''))}</p><h3>Limitations</h3>{text_list(data.get('scope', {}).get('limitations', []) + data.get('limitations', []))}</section>
<section id="overview"><h2>Target and family overview</h2>{table('Geographic family and exposure review', ['Jurisdiction', 'Family count', 'Active', 'Pending', 'Evidence-qualified state', 'Reason'], geo_rows)}</section>
<section id="timeline"><h2>Litigation timeline</h2>{timeline_html}</section>
<section id="patents"><h2>Verified asserted patents and families</h2>{render_patents(patents)}</section>
<section id="cases"><h2>Proceeding deep dives</h2>{render_cases(cases)}</section>
<section id="inventors"><h2>Core inventor activity</h2>{table('Recent activity; descriptive, not a litigation predictor', ['Inventor', 'Recent filings', 'Top classifications', 'Technology focus', 'Evidence note'], inventor_rows)}</section>
<section id="conclusions"><h2>Three-dimensional conclusions and actions</h2><h3>Geographic exposure</h3>{text_list(conclusions.get('geographic_exposure', []))}<h3>Litigation alert</h3><p>{esc(conclusions.get('litigation_alert', 'Not assessable.'))}</p><h3>Technology trend</h3><p>{esc(conclusions.get('technology_trend', 'Not assessable.'))}</p>{table('Action register', ['Priority', 'Action', 'Owner', 'Trigger', 'Evidence'], action_rows)}</section>
<section id="sources"><h2>Sources, assumptions, and limitations</h2>{table('Evidence register', ['ID', 'Type', 'Source', 'Locator', 'Accessed', 'Coverage'], source_rows)}<h3>Assumptions</h3>{text_list(data.get('assumptions', []))}</section>
</div><footer>This report is an evidence-backed monitoring aid, not legal advice or a prediction of litigation outcome. Verify material decisions with qualified counsel in each relevant jurisdiction.</footer>
</main></body></html>"""


def validate_document(document: str, data: dict) -> list[str]:
    """Return deterministic completeness and portability errors.

    This is deliberately conservative. It verifies that identifiers from the
    structured record reached the rendered artifact and that prohibited active
    content or local-path forms were not introduced.
    """
    errors: list[str] = []
    lowered = document.lower()
    required_fragments = [
        "<!doctype html>",
        "<html",
        "<head>",
        "<body>",
        "executive summary",
        "scope and method",
        "litigation timeline",
        "verified asserted patents",
        "proceeding deep dives",
        "core inventor activity",
        "three-dimensional conclusions",
        "sources, assumptions, and limitations",
    ]
    for fragment in required_fragments:
        if fragment not in lowered:
            errors.append(f"Missing required document fragment: {fragment}")

    prohibited_fragments = [
        "javascript:",
        "file://",
        "cdn.jsdelivr",
        "<script src=",
        "google-analytics",
        "googletagmanager",
        "your" + "apikey",
        "{{",
        "}}",
    ]
    for fragment in prohibited_fragments:
        if fragment in lowered:
            errors.append(f"Prohibited document fragment: {fragment}")

    target = str(data.get("target", {}).get("name", "")).strip()
    if target and esc(target) not in document:
        errors.append("Target name is missing from the document")

    for case in data.get("cases", []):
        case_id = str(case.get("case_id", "")).strip()
        if case_id and esc(case_id) not in document:
            errors.append(f"Case identifier is missing: {case_id}")
        case_number = str(case.get("case_number", "")).strip()
        if case_number and esc(case_number) not in document:
            errors.append(f"Case number is missing: {case_number}")

    for patent in data.get("litigated_patents", []):
        number = str(patent.get("publication_number", "")).strip()
        if number and esc(number) not in document:
            errors.append(f"Patent identifier is missing: {number}")

    for source in data.get("sources", []):
        if not isinstance(source, dict):
            continue
        source_id = str(source.get("id", "")).strip()
        if source_id and esc(source_id) not in document:
            errors.append(f"Source identifier is missing: {source_id}")

    expected_stats = data.get("overview", {})
    for key in (
        "party_count",
        "verified_case_count",
        "verified_asserted_patent_count",
        "family_member_count",
    ):
        value = expected_stats.get(key)
        if value is not None and esc(value) not in document:
            errors.append(f"Overview value is missing: {key}={value}")

    return errors


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Render a safe offline litigation report.")
    parser.add_argument("--data", required=True, help="Populated report JSON")
    parser.add_argument("--out", required=True, help="Output HTML path")
    parser.add_argument("--lang", default="en")
    args = parser.parse_args(argv)
    data = json.loads(Path(args.data).read_text(encoding="utf-8"))
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    document = render(data, lang=args.lang)
    errors = validate_document(document, data)
    if errors:
        for error in errors:
            print(f"[render_report] {error}", file=sys.stderr)
        return 2
    output.write_text(document, encoding="utf-8")
    print(f"[render_report] wrote {output} ({len(document):,} characters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

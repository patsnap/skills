#!/usr/bin/env python3
"""Render a normalized patent-family evidence package as a safe offline HTML report.

Usage:
    python analyze_family.py DATA_JSON [--out REPORT_HTML]

This source-authorized renderer does not search patents, call an MCP server, or perform
AI analysis. The upstream workflow defined in ../SKILL.md creates normalized JSON from
authorized evidence. This program validates that package, escapes untrusted text, and
renders the eight-section scientific report.

Security and integrity rules:
    * No network access.
    * No remote CSS, JavaScript, fonts, or analytics.
    * No unescaped user or database text in HTML.
    * Only HTTP(S) links are emitted.
    * Embedded relationship JSON is protected against closing-tag injection.
    * Invalid top-level input fails before the requested output is written.
    * Missing optional evidence is rendered as Unavailable, never invented.
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence
from urllib.parse import urlparse


SCHEMA_VERSION = "1.0"
DEFAULT_OUTPUT = "patent_family_report.html"
ALLOWED_SCHEMES = {"http", "https"}
REQUIRED_TOP_LEVEL = (
    "seed",
    "scope",
    "members",
    "relationships",
    "analyses",
    "comparisons",
    "themes",
    "matrix",
    "chronology",
    "conclusions",
    "evidence",
    "limitations",
)


class InputError(ValueError):
    """Raised when the normalized input cannot support a valid report."""


def as_mapping(value: Any) -> Mapping[str, Any]:
    """Return a mapping or an empty mapping for optional nested objects."""
    return value if isinstance(value, Mapping) else {}


def as_list(value: Any) -> list[Any]:
    """Return a list for JSON arrays and an empty list for missing optional arrays."""
    return list(value) if isinstance(value, list) else []


def text(value: Any, default: str = "Unavailable") -> str:
    """Normalize a scalar for display without treating false numeric values as missing."""
    if value is None:
        return default
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, (int, float)):
        return str(value)
    rendered = str(value).strip()
    return rendered if rendered else default


def esc(value: Any, default: str = "Unavailable") -> str:
    """Normalize and HTML-escape untrusted display content."""
    return html.escape(text(value, default), quote=True)


def safe_url(value: Any) -> str | None:
    """Allow absolute HTTP(S) URLs only."""
    if value is None:
        return None
    candidate = str(value).strip()
    if not candidate:
        return None
    parsed = urlparse(candidate)
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        return None
    if not parsed.netloc:
        return None
    return candidate


def link(value: Any, label: Any) -> str:
    """Render a safe external link or escaped text when the URL is not allowed."""
    label_html = esc(label)
    url = safe_url(value)
    if not url:
        return label_html
    return (
        f'<a href="{html.escape(url, quote=True)}" '
        f'target="_blank" rel="noopener noreferrer">{label_html}</a>'
    )


def join_text(values: Any, separator: str = ", ") -> str:
    """Join a JSON list as escaped readable text."""
    items = [esc(item) for item in as_list(values) if text(item, "")]
    return separator.join(items) if items else "Unavailable"


def identifier(value: Any, fallback: str) -> str:
    """Return a stable display identifier without emitting blank values."""
    candidate = text(value, "")
    return candidate if candidate else fallback


def validate_input(data: Any) -> dict[str, Any]:
    """Validate the report package before any output file is written."""
    if not isinstance(data, dict):
        raise InputError("The JSON root must be an object.")
    missing = [name for name in REQUIRED_TOP_LEVEL if name not in data]
    if missing:
        raise InputError("Missing required top-level fields: " + ", ".join(missing))
    if not isinstance(data.get("seed"), dict):
        raise InputError("seed must be an object.")
    if not isinstance(data.get("scope"), dict):
        raise InputError("scope must be an object.")
    for name in (
        "members",
        "relationships",
        "analyses",
        "comparisons",
        "themes",
        "chronology",
        "evidence",
        "limitations",
    ):
        if not isinstance(data.get(name), list):
            raise InputError(f"{name} must be an array.")
    if not isinstance(data.get("matrix"), dict):
        raise InputError("matrix must be an object.")
    if not isinstance(data.get("conclusions"), dict):
        raise InputError("conclusions must be an object.")
    member_ids: set[str] = set()
    for index, member in enumerate(data["members"], start=1):
        if not isinstance(member, dict):
            raise InputError(f"members[{index - 1}] must be an object.")
        member_id = identifier(member.get("member_id"), "")
        if not member_id:
            raise InputError(f"members[{index - 1}] is missing member_id.")
        if member_id in member_ids:
            raise InputError(f"Duplicate member_id: {member_id}")
        member_ids.add(member_id)
    for index, relationship in enumerate(data["relationships"], start=1):
        if not isinstance(relationship, dict):
            raise InputError(f"relationships[{index - 1}] must be an object.")
        source_id = text(relationship.get("source_member_id"), "")
        target_id = text(relationship.get("target_member_id"), "")
        if source_id and source_id not in member_ids:
            raise InputError(f"Relationship source member is unknown: {source_id}")
        if target_id and target_id not in member_ids:
            raise InputError(f"Relationship target member is unknown: {target_id}")
    return data


def load_json(path: Path) -> dict[str, Any]:
    """Load and validate UTF-8 JSON."""
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise InputError(f"Cannot read input JSON: {exc}") from exc
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise InputError(
            f"Invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc
    return validate_input(parsed)


def member_index(data: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    """Index normalized members by stable member ID."""
    return {
        text(member.get("member_id"), ""): member
        for member in as_list(data.get("members"))
        if isinstance(member, Mapping)
    }


def evidence_index(data: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    """Index evidence records by stable evidence ID."""
    result: dict[str, Mapping[str, Any]] = {}
    for item in as_list(data.get("evidence")):
        if not isinstance(item, Mapping):
            continue
        evidence_id = text(item.get("evidence_id"), "")
        if evidence_id:
            result[evidence_id] = item
    return result


def count_authorities(members: Sequence[Any]) -> int:
    """Count non-empty patent authorities."""
    values = {
        text(member.get("authority"), "")
        for member in members
        if isinstance(member, Mapping) and text(member.get("authority"), "")
    }
    return len(values)


def status_counts(members: Sequence[Any]) -> dict[str, int]:
    """Return normalized status counts without interpreting legal effect."""
    counts: dict[str, int] = {}
    for member in members:
        if not isinstance(member, Mapping):
            continue
        state = text(member.get("normalized_status"), "Unavailable")
        counts[state] = counts.get(state, 0) + 1
    return counts


def render_status_summary(counts: Mapping[str, int]) -> str:
    """Render status counts as text-labelled items."""
    if not counts:
        return '<p class="unavailable">Legal-status summary unavailable.</p>'
    items = "".join(
        f"<li><strong>{esc(state)}</strong><span>{count}</span></li>"
        for state, count in sorted(counts.items(), key=lambda item: item[0].lower())
    )
    return f'<ul class="status-list">{items}</ul>'


def render_scope(data: Mapping[str, Any]) -> str:
    """Render report scope, metrics, and evidence boundaries."""
    seed = as_mapping(data.get("seed"))
    scope = as_mapping(data.get("scope"))
    metadata = as_mapping(data.get("metadata"))
    members = as_list(data.get("members"))
    analyses = as_list(data.get("analyses"))
    retrieved = metadata.get("retrieved_member_count", len(members))
    analyzed = metadata.get("analyzed_member_count", len(analyses))
    status_html = render_status_summary(status_counts(members))
    return f"""
    <section id="scope" class="report-section">
      <div class="section-kicker">01 · Scope and evidence</div>
      <h2>Family definition, cutoff, and coverage</h2>
      <div class="metric-grid">
        <article class="metric"><span>Retrieved members</span><strong>{esc(retrieved)}</strong></article>
        <article class="metric"><span>Deeply analyzed</span><strong>{esc(analyzed)}</strong></article>
        <article class="metric"><span>Authorities</span><strong>{count_authorities(members)}</strong></article>
        <article class="metric"><span>Family definition</span><strong>{esc(scope.get('family_definition'))}</strong></article>
      </div>
      <div class="two-column">
        <article class="panel">
          <h3>Seed record</h3>
          <dl class="definition-list">
            <dt>Publication</dt><dd>{link(seed.get('source_locator'), seed.get('normalized_publication_number'))}</dd>
            <dt>Application</dt><dd>{esc(seed.get('application_number'))}</dd>
            <dt>Grant</dt><dd>{esc(seed.get('grant_number'))}</dd>
            <dt>Authority</dt><dd>{esc(seed.get('authority'))}</dd>
            <dt>Title</dt><dd>{esc(seed.get('title'))}</dd>
          </dl>
        </article>
        <article class="panel">
          <h3>Analytical scope</h3>
          <dl class="definition-list">
            <dt>Included relationships</dt><dd>{join_text(scope.get('included_relationships'))}</dd>
            <dt>Excluded relationships</dt><dd>{join_text(scope.get('excluded_relationships'))}</dd>
            <dt>Status cutoff</dt><dd>{esc(scope.get('status_cutoff'))}</dd>
            <dt>Retrieval cutoff</dt><dd>{esc(scope.get('retrieval_cutoff'))}</dd>
            <dt>Selection rule</dt><dd>{esc(scope.get('selection_rule'))}</dd>
          </dl>
        </article>
      </div>
      <article class="panel">
        <h3>Status observations as of the stated cutoff</h3>
        {status_html}
        <p class="note">Status is member-, jurisdiction-, record-, and date-specific. It is not a validity or enforceability conclusion.</p>
      </article>
    </section>
    """


def render_member_rows(members: Sequence[Any]) -> str:
    """Render the complete member list."""
    rows: list[str] = []
    for position, member in enumerate(members, start=1):
        if not isinstance(member, Mapping):
            continue
        publication = member.get("publication_number")
        rows.append(
            "<tr>"
            f"<td>{position}</td>"
            f"<td><code>{esc(member.get('member_id'))}</code></td>"
            f"<td>{link(member.get('source_url'), publication)}</td>"
            f"<td>{esc(member.get('authority'))}</td>"
            f"<td>{esc(member.get('relationship_type'))}</td>"
            f"<td>{esc(member.get('earliest_priority_date'))}</td>"
            f"<td>{esc(member.get('filing_date'))}</td>"
            f"<td>{esc(member.get('publication_date'))}</td>"
            f"<td>{esc(member.get('normalized_status'))}<br><small>{esc(member.get('status_as_of'))}</small></td>"
            f"<td>{esc(member.get('title'))}</td>"
            "</tr>"
        )
    if not rows:
        return '<tr><td colspan="10" class="unavailable">No family members were supplied.</td></tr>'
    return "".join(rows)


def render_members(data: Mapping[str, Any]) -> str:
    """Render all retrieved family members, not only the analysis subset."""
    rows = render_member_rows(as_list(data.get("members")))
    return f"""
    <section id="members" class="report-section">
      <div class="section-kicker">02 · Complete member register</div>
      <h2>Retrieved patent-family members</h2>
      <p class="section-intro">This table shows the complete retrieved set under the stated family definition. Procedural publications and jurisdictional equivalents are not counted as separate inventions.</p>
      <div class="table-wrap">
        <table>
          <caption>Complete normalized member list</caption>
          <thead><tr><th>No.</th><th>Member ID</th><th>Publication</th><th>Authority</th><th>Relationship</th><th>Earliest priority</th><th>Filed</th><th>Published</th><th>Status/as of</th><th>Title</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
    </section>
    """


def graph_payload(data: Mapping[str, Any]) -> str:
    """Return JSON safe for embedding in a non-executable application/json element."""
    members = []
    for member in as_list(data.get("members")):
        if not isinstance(member, Mapping):
            continue
        members.append(
            {
                "id": text(member.get("member_id"), ""),
                "label": text(member.get("publication_number"), "Unavailable"),
                "authority": text(member.get("authority"), ""),
                "date": text(member.get("earliest_priority_date"), ""),
                "relationship": text(member.get("relationship_type"), "Unavailable"),
            }
        )
    relationships = []
    for edge in as_list(data.get("relationships")):
        if not isinstance(edge, Mapping):
            continue
        relationships.append(
            {
                "id": text(edge.get("relationship_id"), ""),
                "source": text(edge.get("source_member_id"), ""),
                "target": text(edge.get("target_member_id"), ""),
                "type": text(edge.get("relationship_type"), "Unavailable"),
                "confidence": text(edge.get("confidence"), "Unavailable"),
            }
        )
    encoded = json.dumps(
        {"nodes": members, "edges": relationships},
        ensure_ascii=False,
        separators=(",", ":"),
    )
    return encoded.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def render_relationship_rows(data: Mapping[str, Any]) -> str:
    """Render the accessible relationship-table equivalent for the SVG graph."""
    members = member_index(data)
    rows: list[str] = []
    for relationship in as_list(data.get("relationships")):
        if not isinstance(relationship, Mapping):
            continue
        source_id = text(relationship.get("source_member_id"), "")
        target_id = text(relationship.get("target_member_id"), "")
        source = as_mapping(members.get(source_id))
        target = as_mapping(members.get(target_id))
        rows.append(
            "<tr>"
            f"<td><code>{esc(relationship.get('relationship_id'))}</code></td>"
            f"<td>{esc(source.get('publication_number', source_id))}</td>"
            f"<td>{esc(relationship.get('relationship_type'))}</td>"
            f"<td>{esc(target.get('publication_number', target_id))}</td>"
            f"<td>{join_text(relationship.get('evidence_ids'))}</td>"
            f"<td>{esc(relationship.get('confidence'))}</td>"
            "</tr>"
        )
    return "".join(rows) or '<tr><td colspan="6" class="unavailable">No verified family edges were supplied.</td></tr>'


def render_graph(data: Mapping[str, Any]) -> str:
    """Render graph host, safe JSON payload, legend, and accessible table."""
    payload = graph_payload(data)
    rows = render_relationship_rows(data)
    return f"""
    <section id="relationships" class="report-section">
      <div class="section-kicker">03 · Family relationships</div>
      <h2>Priority and procedural relationship graph</h2>
      <p class="section-intro">Edges appear only when supported by relationship evidence. Vertical position is a readable layout, not an assertion of technical progression.</p>
      <div class="graph-panel">
        <svg id="familyGraph" viewBox="0 0 1100 520" role="img" aria-labelledby="graphTitle graphDesc">
          <title id="graphTitle">Patent-family relationship graph</title>
          <desc id="graphDesc">A directed graph of verified priority and procedural relationships. The table below contains the same edge information.</desc>
        </svg>
        <div class="legend"><span><i class="legend-line"></i> Verified relationship</span><span>Node labels show publication and authority</span></div>
      </div>
      <script id="familyGraphData" type="application/json">{payload}</script>
      <div class="table-wrap">
        <table>
          <caption>Accessible family relationship register</caption>
          <thead><tr><th>Relationship ID</th><th>Source</th><th>Type</th><th>Target</th><th>Evidence IDs</th><th>Confidence</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
    </section>
    """


def render_analysis_cards(data: Mapping[str, Any]) -> str:
    """Render deeply analyzed family-member cards."""
    members = member_index(data)
    cards: list[str] = []
    for analysis in as_list(data.get("analyses")):
        if not isinstance(analysis, Mapping):
            continue
        member_id = text(analysis.get("member_id"), "")
        member = as_mapping(members.get(member_id))
        claim_focus = analysis.get("independent_claim_focus")
        if isinstance(claim_focus, list):
            claim_html = "<ul>" + "".join(f"<li>{esc(item)}</li>" for item in claim_focus) + "</ul>"
        else:
            claim_html = f"<p>{esc(claim_focus)}</p>"
        cards.append(
            f"""
            <article class="analysis-card">
              <header><div><code>{esc(member_id)}</code><h3>{esc(member.get('publication_number'))} · {esc(member.get('title'))}</h3></div><span class="state">{esc(analysis.get('evidence_basis'))}</span></header>
              <p class="selection"><strong>Selection reason:</strong> {esc(analysis.get('selection_reason'))}</p>
              <div class="analysis-grid">
                <section><h4>Technical problem</h4><p>{esc(analysis.get('technical_problem'))}</p></section>
                <section><h4>Technical means</h4><p>{esc(analysis.get('technical_means'))}</p></section>
                <section><h4>Technical effect</h4><p>{esc(analysis.get('technical_effect'))}</p></section>
                <section><h4>Independent-claim focus</h4>{claim_html}</section>
              </div>
              <footer><strong>Sources:</strong> {join_text(analysis.get('source_ids'))} · <strong>Limitations:</strong> {esc(analysis.get('limitations'))}</footer>
            </article>
            """
        )
    if not cards:
        cards.append('<p class="unavailable">No members were selected for deep analysis.</p>')
    return f"""
    <section id="analyses" class="report-section">
      <div class="section-kicker">04 · Selected-member analysis</div>
      <h2>Technical disclosure and independent-claim focus</h2>
      <p class="section-intro">This is a disclosed subset of up to twenty members, not the complete family register.</p>
      {''.join(cards)}
    </section>
    """


def render_comparisons(data: Mapping[str, Any]) -> str:
    """Render technical, claim, and procedural comparisons separately."""
    members = member_index(data)
    rows: list[str] = []
    for comparison in as_list(data.get("comparisons")):
        if not isinstance(comparison, Mapping):
            continue
        a_id = text(comparison.get("member_a"), "")
        b_id = text(comparison.get("member_b"), "")
        a = as_mapping(members.get(a_id))
        b = as_mapping(members.get(b_id))
        rows.append(
            "<tr>"
            f"<td><code>{esc(comparison.get('comparison_id'))}</code></td>"
            f"<td>{esc(a.get('publication_number', a_id))}<br>↔<br>{esc(b.get('publication_number', b_id))}</td>"
            f"<td>{esc(comparison.get('relationship_basis'))}</td>"
            f"<td>{esc(comparison.get('shared_disclosure'))}</td>"
            f"<td>{esc(comparison.get('technical_difference'))}</td>"
            f"<td>{esc(comparison.get('claim_focus_difference'))}</td>"
            f"<td>{esc(comparison.get('procedural_difference'))}</td>"
            f"<td>{join_text(comparison.get('evidence_ids'))}</td>"
            f"<td>{esc(comparison.get('confidence'))}<br><small>{esc(comparison.get('limitations'))}</small></td>"
            "</tr>"
        )
    body = "".join(rows) or '<tr><td colspan="9" class="unavailable">No evidence-backed comparisons were supplied.</td></tr>'
    return f"""
    <section id="comparisons" class="report-section">
      <div class="section-kicker">05 · Relationship analysis</div>
      <h2>Technical, claim, and procedural differences</h2>
      <div class="table-wrap">
        <table>
          <caption>Pairwise comparison register</caption>
          <thead><tr><th>ID</th><th>Members</th><th>Relationship basis</th><th>Shared disclosure</th><th>Technical difference</th><th>Claim-focus difference</th><th>Procedural difference</th><th>Evidence</th><th>Confidence/limits</th></tr></thead>
          <tbody>{body}</tbody>
        </table>
      </div>
    </section>
    """


def theme_index(data: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    """Index theme definitions by stable ID."""
    result: dict[str, Mapping[str, Any]] = {}
    for theme in as_list(data.get("themes")):
        if not isinstance(theme, Mapping):
            continue
        theme_id = text(theme.get("theme_id"), "")
        if theme_id:
            result[theme_id] = theme
    return result


def matrix_cell(matrix: Mapping[str, Any], member_id: str, theme_id: str) -> tuple[str, str]:
    """Return a text state and evidence IDs for one matrix cell."""
    cells = as_mapping(matrix.get("cells"))
    member_cells = as_mapping(cells.get(member_id))
    raw = member_cells.get(theme_id)
    if isinstance(raw, Mapping):
        state = text(raw.get("state"), "Unavailable")
        evidence = join_text(raw.get("evidence_ids"))
        return state, evidence
    if raw is None:
        return "Unavailable", "Unavailable"
    return text(raw), "Unavailable"


def render_matrix(data: Mapping[str, Any]) -> str:
    """Render the theme matrix with text states and evidence tooltips."""
    matrix = as_mapping(data.get("matrix"))
    members = member_index(data)
    themes = theme_index(data)
    member_ids = [text(value, "") for value in as_list(matrix.get("member_ids"))]
    theme_ids = [text(value, "") for value in as_list(matrix.get("theme_ids"))]
    header = "".join(f"<th>{esc(themes.get(theme_id, {}).get('label', theme_id))}</th>" for theme_id in theme_ids)
    rows: list[str] = []
    for member_id in member_ids:
        member = as_mapping(members.get(member_id))
        cells: list[str] = []
        for theme_id in theme_ids:
            state, evidence = matrix_cell(matrix, member_id, theme_id)
            state_class = "matrix-" + state.lower().replace(" ", "-").replace("/", "-")
            cells.append(f'<td class="{html.escape(state_class, quote=True)}"><strong>{esc(state)}</strong><small>{esc(evidence)}</small></td>')
        rows.append(f"<tr><th>{esc(member.get('publication_number', member_id))}</th>{''.join(cells)}</tr>")
    if not rows:
        rows.append('<tr><td class="unavailable">Theme matrix unavailable.</td></tr>')
    definitions = "".join(
        f"<li><code>{esc(theme_id)}</code><strong>{esc(theme.get('label'))}</strong><span>{esc(theme.get('definition'))}</span><small>Evidence: {join_text(theme.get('evidence_ids'))} · Confidence: {esc(theme.get('confidence'))}</small></li>"
        for theme_id, theme in themes.items()
    ) or '<li class="unavailable">No theme definitions were supplied.</li>'
    return f"""
    <section id="matrix" class="report-section">
      <div class="section-kicker">06 · Technical-theme matrix</div>
      <h2>Evidence-labelled theme coverage</h2>
      <ul class="theme-definitions">{definitions}</ul>
      <div class="table-wrap">
        <table class="matrix-table">
          <caption>Covered, Partially covered, Not evidenced, or Unavailable; classification alone does not establish claim coverage</caption>
          <thead><tr><th>Member</th>{header}</tr></thead>
          <tbody>{''.join(rows)}</tbody>
        </table>
      </div>
    </section>
    """


def render_chronology(data: Mapping[str, Any]) -> str:
    """Render dated events without implying unsupported technical progression."""
    members = member_index(data)
    events = sorted(
        [item for item in as_list(data.get("chronology")) if isinstance(item, Mapping)],
        key=lambda item: text(item.get("date"), "9999-99-99"),
    )
    items: list[str] = []
    for event in events:
        member_id = text(event.get("member_id"), "")
        member = as_mapping(members.get(member_id))
        items.append(
            f"""
            <li>
              <time>{esc(event.get('date'))}</time>
              <div><span class="state">{esc(event.get('date_type'))}</span><h3>{esc(member.get('publication_number', member_id))} · {esc(event.get('document_event'))}</h3><p>{esc(event.get('technical_or_claim_change'))}</p><small>Relationship: {esc(event.get('relationship_type'))} · Evidence: {join_text(event.get('evidence_ids'))} · Confidence: {esc(event.get('confidence'))}</small></div>
            </li>
            """
        )
    if not items:
        items.append('<li class="unavailable">No chronology events were supplied.</li>')
    return f"""
    <section id="chronology" class="report-section">
      <div class="section-kicker">07 · Chronology</div>
      <h2>Priority, procedural, technical, and claim events</h2>
      <p class="section-intro">Chronology does not establish technical evolution unless the cited record demonstrates a technical or claim change.</p>
      <ol class="timeline">{''.join(items)}</ol>
    </section>
    """


def render_evidence(data: Mapping[str, Any]) -> str:
    """Render the evidence source register."""
    rows: list[str] = []
    for item in as_list(data.get("evidence")):
        if not isinstance(item, Mapping):
            continue
        rows.append(
            "<tr>"
            f"<td><code>{esc(item.get('evidence_id'))}</code></td>"
            f"<td>{esc(item.get('source_type'))}</td>"
            f"<td>{esc(item.get('publisher_or_connector'))}</td>"
            f"<td>{link(item.get('url'), item.get('title_or_record'))}</td>"
            f"<td>{esc(item.get('date'))}</td>"
            f"<td>{esc(item.get('retrieved_at'))}</td>"
            f"<td>{esc(item.get('scope'))}</td>"
            "</tr>"
        )
    return "".join(rows) or '<tr><td colspan="7" class="unavailable">Evidence register unavailable.</td></tr>'


def conclusion_block(label: str, value: Any) -> str:
    """Render one bounded conclusion block."""
    return f"<section><h3>{esc(label)}</h3><p>{esc(value)}</p></section>"


def render_conclusions(data: Mapping[str, Any]) -> str:
    """Render bounded conclusions, limitations, evidence, and next actions."""
    conclusions = as_mapping(data.get("conclusions"))
    blocks = "".join(
        (
            conclusion_block("Technical position", conclusions.get("technical_position")),
            conclusion_block("Jurisdictional filing footprint", conclusions.get("filing_footprint")),
            conclusion_block("Claim-structure assessment", conclusions.get("claim_structure_assessment")),
            conclusion_block("Technical or claim branches", conclusions.get("technical_or_claim_branches")),
            conclusion_block("Gaps and risks", conclusions.get("gaps_and_risks")),
            conclusion_block("Recommended follow-up", conclusions.get("recommended_follow_up")),
        )
    )
    limitations = "".join(
        f"<li>{esc(item)}</li>" for item in as_list(data.get("limitations"))
    ) or "<li>None supplied; review required.</li>"
    evidence_rows = render_evidence(data)
    return f"""
    <section id="conclusions" class="report-section">
      <div class="section-kicker">08 · Conclusions and sources</div>
      <h2>Bounded assessment and follow-up</h2>
      <div class="conclusion-grid">{blocks}</div>
      <article class="callout"><h3>Interpretation limits</h3><p>Filing footprint is not proof of market presence or strategy. Family size is not protection strength. Status is not validity or enforceability. Theme gaps are not necessarily technical white space. This report is not an infringement or FTO opinion.</p></article>
      <article class="panel"><h3>Report limitations</h3><ul>{limitations}</ul></article>
      <div class="table-wrap">
        <table>
          <caption>Evidence source register</caption>
          <thead><tr><th>ID</th><th>Type</th><th>Publisher/connector</th><th>Record</th><th>Date</th><th>Retrieved</th><th>Evidence scope</th></tr></thead>
          <tbody>{evidence_rows}</tbody>
        </table>
      </div>
    </section>
    """


CSS = r"""
    :root {
      --paper: #ffffff;
      --canvas: #eef2f6;
      --ink: #172033;
      --muted: #5d6877;
      --navy: #173b67;
      --teal: #176f6a;
      --line: #d5dde7;
      --panel: #f6f8fb;
      --warn: #815f19;
      --danger: #8a3f3b;
      --radius: 8px;
      --sans: ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
      --mono: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body { margin: 0; color: var(--ink); background: var(--canvas); font: 15px/1.55 var(--sans); }
    a { color: var(--navy); text-underline-offset: 2px; }
    a:focus-visible, button:focus-visible { outline: 3px solid #5b9bd5; outline-offset: 2px; }
    code { font-family: var(--mono); font-size: .9em; }
    .shell { width: min(1480px, 100%); min-height: 100vh; margin: 0 auto; background: var(--paper); }
    .topbar { position: sticky; top: 0; z-index: 10; display: flex; flex-wrap: wrap; justify-content: space-between; gap: 10px; padding: 12px 28px; border-bottom: 1px solid var(--line); background: rgba(255,255,255,.98); }
    .brand { color: var(--navy); font-weight: 760; }
    .topbar nav { display: flex; flex-wrap: wrap; gap: 12px; }
    .topbar nav a { font-size: 12px; text-decoration: none; }
    .report-header { padding: 42px 36px 30px; border-bottom: 1px solid var(--line); }
    .eyebrow, .section-kicker { color: var(--teal); font-size: 11px; font-weight: 800; letter-spacing: .11em; text-transform: uppercase; }
    h1 { max-width: 960px; margin: 7px 0 10px; color: var(--navy); font-size: clamp(29px, 4vw, 46px); line-height: 1.12; }
    h2 { margin: 6px 0 14px; color: var(--navy); font-size: 24px; line-height: 1.25; }
    h3 { color: var(--navy); }
    .header-meta { display: flex; flex-wrap: wrap; gap: 8px 18px; color: var(--muted); font-size: 13px; }
    main { padding: 0 36px 60px; }
    .report-section { padding: 34px 0; border-bottom: 1px solid var(--line); scroll-margin-top: 55px; }
    .section-intro, .note { max-width: 980px; color: var(--muted); }
    .metric-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin: 18px 0; }
    .metric { padding: 15px; border: 1px solid var(--line); border-radius: var(--radius); background: var(--panel); }
    .metric span { display: block; color: var(--muted); font-size: 12px; }
    .metric strong { display: block; margin-top: 4px; color: var(--navy); font-size: 20px; }
    .two-column { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
    .panel { margin: 14px 0; padding: 18px; border: 1px solid var(--line); border-radius: var(--radius); }
    .panel h3 { margin-top: 0; }
    .definition-list { display: grid; grid-template-columns: minmax(130px, .35fr) 1fr; gap: 7px 14px; margin: 0; }
    .definition-list dt { color: var(--muted); font-weight: 700; }
    .definition-list dd { margin: 0; }
    .status-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 8px; padding: 0; list-style: none; }
    .status-list li { display: flex; justify-content: space-between; padding: 8px 10px; background: var(--panel); }
    .table-wrap { margin: 16px 0; overflow-x: auto; border: 1px solid var(--line); border-radius: var(--radius); }
    table { width: 100%; border-collapse: collapse; font-size: 12px; }
    caption { padding: 10px 12px; color: var(--muted); text-align: left; font-weight: 700; }
    th, td { min-width: 90px; padding: 9px 10px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }
    th { color: var(--navy); background: var(--panel); }
    tbody tr:last-child td { border-bottom: 0; }
    small { display: block; color: var(--muted); }
    .graph-panel { padding: 14px; border: 1px solid var(--line); border-radius: var(--radius); overflow-x: auto; }
    #familyGraph { min-width: 760px; height: auto; background: var(--paper); }
    .legend { display: flex; flex-wrap: wrap; gap: 16px; color: var(--muted); font-size: 12px; }
    .legend-line { display: inline-block; width: 24px; margin-right: 5px; border-top: 2px solid var(--teal); vertical-align: middle; }
    .analysis-card { margin: 16px 0; padding: 20px; border: 1px solid var(--line); border-left: 4px solid var(--teal); border-radius: var(--radius); }
    .analysis-card header { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 12px; }
    .analysis-card h3 { margin: 4px 0; }
    .analysis-card footer { margin-top: 12px; padding-top: 10px; color: var(--muted); border-top: 1px solid var(--line); font-size: 12px; }
    .state { display: inline-block; color: var(--navy); font-size: 11px; font-weight: 800; letter-spacing: .04em; text-transform: uppercase; }
    .selection { padding: 9px 11px; background: var(--panel); }
    .analysis-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
    .analysis-grid section { padding: 12px; border: 1px solid var(--line); }
    .analysis-grid h4 { margin: 0 0 6px; color: var(--navy); }
    .theme-definitions { display: grid; gap: 7px; padding: 0; list-style: none; }
    .theme-definitions li { display: grid; grid-template-columns: 90px 160px 1fr; gap: 8px; padding: 9px; background: var(--panel); }
    .matrix-table td strong { display: block; }
    .matrix-covered { border-left: 3px solid var(--teal); }
    .matrix-partially-covered { border-left: 3px solid var(--warn); }
    .matrix-not-evidenced { border-left: 3px solid var(--danger); }
    .matrix-unavailable { border-left: 3px solid var(--muted); }
    .timeline { position: relative; padding-left: 28px; list-style: none; }
    .timeline::before { content: ""; position: absolute; left: 8px; top: 8px; bottom: 8px; border-left: 2px solid var(--line); }
    .timeline li { position: relative; display: grid; grid-template-columns: 120px 1fr; gap: 12px; margin: 0 0 18px; }
    .timeline li::before { content: ""; position: absolute; left: -25px; top: 7px; width: 10px; height: 10px; border: 2px solid var(--teal); border-radius: 50%; background: var(--paper); }
    .timeline time { color: var(--muted); font-family: var(--mono); font-size: 12px; }
    .timeline h3 { margin: 3px 0; font-size: 16px; }
    .timeline p { margin: 4px 0; }
    .conclusion-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
    .conclusion-grid section { padding: 16px; border: 1px solid var(--line); }
    .conclusion-grid h3 { margin-top: 0; }
    .callout { margin: 18px 0; padding: 16px 18px; border-left: 4px solid var(--warn); background: #fbf8ef; }
    .callout h3 { margin-top: 0; }
    .unavailable { color: var(--muted); font-style: italic; }
    .report-footer { padding: 24px 36px; color: var(--muted); border-top: 1px solid var(--line); font-size: 12px; }
    @media (max-width: 900px) {
      .metric-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .two-column, .analysis-grid, .conclusion-grid { grid-template-columns: 1fr; }
      .theme-definitions li { grid-template-columns: 1fr; }
    }
    @media (max-width: 620px) {
      .topbar, .report-header, main, .report-footer { padding-left: 18px; padding-right: 18px; }
      .topbar { position: static; }
      .metric-grid { grid-template-columns: 1fr; }
      .definition-list { grid-template-columns: 1fr; }
      .timeline li { grid-template-columns: 1fr; }
    }
    @media print {
      body, .shell { background: white; }
      .topbar { position: static; }
      .topbar nav { display: none; }
      .report-section, .analysis-card, .panel, .graph-panel { break-inside: avoid; }
      .table-wrap { overflow: visible; }
      a { color: inherit; text-decoration: none; }
      thead { display: table-header-group; }
    }
"""


GRAPH_SCRIPT = r"""
    (() => {
      "use strict";
      const svg = document.getElementById("familyGraph");
      const payloadNode = document.getElementById("familyGraphData");
      if (!svg || !payloadNode) return;
      let graph;
      try {
        graph = JSON.parse(payloadNode.textContent || "{}");
      } catch (_error) {
        return;
      }
      const nodes = Array.isArray(graph.nodes) ? graph.nodes : [];
      const edges = Array.isArray(graph.edges) ? graph.edges : [];
      const NS = "http://www.w3.org/2000/svg";
      const make = (name, attrs = {}) => {
        const element = document.createElementNS(NS, name);
        for (const [key, value] of Object.entries(attrs)) element.setAttribute(key, String(value));
        return element;
      };
      const appendText = (parent, value, attrs = {}) => {
        const element = make("text", attrs);
        element.textContent = String(value ?? "");
        parent.appendChild(element);
      };
      const width = 1100;
      const nodeWidth = 180;
      const nodeHeight = 62;
      const columns = Math.max(1, Math.min(5, Math.ceil(Math.sqrt(nodes.length || 1))));
      const rows = Math.max(1, Math.ceil(nodes.length / columns));
      const xGap = (width - 80 - nodeWidth) / Math.max(1, columns - 1);
      const yGap = Math.max(95, (480 - nodeHeight) / Math.max(1, rows - 1));
      const positions = new Map();
      nodes.forEach((node, index) => {
        const column = index % columns;
        const row = Math.floor(index / columns);
        positions.set(node.id, {x: 40 + column * xGap, y: 25 + row * yGap});
      });
      const fragment = document.createDocumentFragment();
      const marker = make("marker", {id: "arrow", viewBox: "0 0 10 10", refX: 8, refY: 5, markerWidth: 6, markerHeight: 6, orient: "auto-start-reverse"});
      marker.appendChild(make("path", {d: "M 0 0 L 10 5 L 0 10 z", fill: "#176f6a"}));
      const defs = make("defs");
      defs.appendChild(marker);
      fragment.appendChild(defs);
      edges.forEach((edge) => {
        const source = positions.get(edge.source);
        const target = positions.get(edge.target);
        if (!source || !target) return;
        const x1 = source.x + nodeWidth / 2;
        const y1 = source.y + nodeHeight / 2;
        const x2 = target.x + nodeWidth / 2;
        const y2 = target.y + nodeHeight / 2;
        const line = make("line", {x1, y1, x2, y2, stroke: "#176f6a", "stroke-width": 1.7, "marker-end": "url(#arrow)"});
        const title = make("title");
        title.textContent = `${edge.type} (${edge.confidence})`;
        line.appendChild(title);
        fragment.appendChild(line);
      });
      nodes.forEach((node) => {
        const position = positions.get(node.id);
        if (!position) return;
        const group = make("g", {transform: `translate(${position.x},${position.y})`});
        group.appendChild(make("rect", {width: nodeWidth, height: nodeHeight, rx: 6, fill: "#ffffff", stroke: "#173b67", "stroke-width": 1.4}));
        appendText(group, node.label, {x: 10, y: 20, fill: "#173b67", "font-size": 12, "font-weight": 700});
        appendText(group, node.authority || "Authority unavailable", {x: 10, y: 38, fill: "#5d6877", "font-size": 10});
        appendText(group, node.date || "Date unavailable", {x: 10, y: 52, fill: "#5d6877", "font-size": 9});
        const title = make("title");
        title.textContent = `${node.label}; ${node.relationship}`;
        group.appendChild(title);
        fragment.appendChild(group);
      });
      svg.replaceChildren(fragment);
    })();
"""


def build_html(data: Mapping[str, Any]) -> str:
    """Assemble the complete offline report."""
    seed = as_mapping(data.get("seed"))
    metadata = as_mapping(data.get("metadata"))
    report_title = text(data.get("report_title"), "Patent Family Analysis")
    generated_at = text(
        metadata.get("generated_at"),
        datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    )
    seed_number = text(seed.get("normalized_publication_number"), "Unresolved seed")
    sections = "".join(
        (
            render_scope(data),
            render_members(data),
            render_graph(data),
            render_analysis_cards(data),
            render_comparisons(data),
            render_matrix(data),
            render_chronology(data),
            render_conclusions(data),
        )
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="generator" content="PatSnap localized patent-family renderer {SCHEMA_VERSION}">
  <title>{esc(report_title)} · {esc(seed_number)}</title>
  <style>{CSS}</style>
</head>
<body>
<div class="shell">
  <header class="topbar">
    <div class="brand">Patent Family Analysis</div>
    <nav aria-label="Report sections">
      <a href="#scope">Scope</a>
      <a href="#members">Members</a>
      <a href="#relationships">Relationships</a>
      <a href="#analyses">Analysis</a>
      <a href="#comparisons">Comparisons</a>
      <a href="#matrix">Themes</a>
      <a href="#chronology">Chronology</a>
      <a href="#conclusions">Conclusions</a>
    </nav>
  </header>
  <section class="report-header">
    <div class="eyebrow">Evidence-bound family intelligence</div>
    <h1>{esc(report_title)}</h1>
    <div class="header-meta"><span>Seed {esc(seed_number)}</span><span>Generated {esc(generated_at)}</span><span>Schema {esc(data.get('schema_version', SCHEMA_VERSION))}</span></div>
  </section>
  <main>{sections}</main>
  <footer class="report-footer">Generated from normalized evidence JSON. PatSnap connector output and legal-status data remain subject to the stated sources and cutoffs. This report is not legal advice, an FTO opinion, or proof of market strategy.</footer>
</div>
<script>{GRAPH_SCRIPT}</script>
</body>
</html>
"""


def write_report(output_path: Path, report_html: str) -> None:
    """Write the requested HTML after successful validation and rendering."""
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report_html, encoding="utf-8", newline="\n")
    except OSError as exc:
        raise InputError(f"Cannot write output HTML: {exc}") from exc


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line interface."""
    parser = argparse.ArgumentParser(
        description="Render normalized patent-family evidence JSON as safe offline HTML."
    )
    parser.add_argument(
        "data_json",
        type=Path,
        help="Path to the normalized family-analysis JSON input.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(DEFAULT_OUTPUT),
        help=f"Output HTML path (default: {DEFAULT_OUTPUT}).",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point with structured errors and nonzero failure status."""
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        data = load_json(args.data_json)
        report_html = build_html(data)
        write_report(args.out, report_html)
    except InputError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"Report generated: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Self-contained technology-transfer matching report generator.

The renderer preserves the source report's technology, advancement, patent
value, recipient, risk, and pathway modules while replacing external ECharts,
unsafe interpolation, decorative gradients, and China-only presentation.

Input values are escaped. Links permit absolute HTTP(S) only. Charts use
accessible native HTML/SVG and repeat their values in text or tables. The
function returns HTML; it does not write files, open a browser, or start a
server. Use ``report_generator_patch.py`` for approved output paths.
"""

from __future__ import annotations

import html
import json
from datetime import date
from typing import Any, Iterable, Mapping, Sequence
from urllib.parse import urlparse


REPORT_SECTIONS = (
    ("summary", "Decision summary"),
    ("scope", "Scope and evidence quality"),
    ("technology", "Technology and transfer package"),
    ("advancement", "Advancement and readiness"),
    ("patent-value", "Patent and commercialization value"),
    ("portfolio", "Patent portfolio evidence"),
    ("recipients", "Potential recipients"),
    ("risk", "Transfer risk"),
    ("pathway", "Transfer pathway"),
    ("sources", "Sources and limitations"),
)


class ReportDataError(ValueError):
    """Raised when a report would violate a hard evidence or safety gate."""


def e(value: Any) -> str:
    if value is None:
        return ""
    return html.escape(str(value), quote=True)


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple, set)):
        return ", ".join(clean_text(item) for item in value if clean_text(item))
    return " ".join(str(value).split())


def items(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, (tuple, set)):
        return list(value)
    return [value]


def obj(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def safe_url(value: Any) -> str:
    candidate = clean_text(value)
    parsed = urlparse(candidate)
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc:
        return ""
    return candidate


def link(label: Any, url: Any) -> str:
    accepted = safe_url(url)
    if not accepted:
        return e(label)
    return f'<a href="{e(accepted)}" target="_blank" rel="noopener noreferrer">{e(label)}</a>'


def numeric(value: Any, *, minimum: float = 0.0, maximum: float = 100.0) -> float | None:
    if value is None or value == "":
        return None
    if not isinstance(value, (int, float)):
        raise ReportDataError(f"Expected numeric value, received {value!r}")
    number = float(value)
    if not minimum <= number <= maximum:
        raise ReportDataError(f"Numeric value {number} outside {minimum}..{maximum}")
    return number


def status(value: Any) -> str:
    raw = clean_text(value).lower().replace(" ", "_").replace("-", "_")
    allowed = {"executed", "partial", "not_scored", "not_assessed", "not_executed", "unavailable", "error"}
    return raw if raw in allowed else "unavailable"


def badge(value: Any) -> str:
    normalized = status(value)
    label = normalized.replace("_", " ").title()
    return f'<span class="status status-{e(normalized.replace("_", "-"))}">{e(label)}</span>'


def render_list(values: Iterable[Any], css_class: str = "") -> str:
    normalized = [clean_text(value) for value in values if clean_text(value)]
    if not normalized:
        return '<p class="empty">Not available.</p>'
    class_attr = f' class="{e(css_class)}"' if css_class else ""
    return f'<ul{class_attr}>' + "".join(f"<li>{e(value)}</li>" for value in normalized) + "</ul>"


def field(label: str, value: Any) -> str:
    rendered = clean_text(value) or "Not available"
    return f'<div class="field"><div class="field-label">{e(label)}</div><div>{e(rendered)}</div></div>'


def evidence_refs(value: Any) -> str:
    refs = [clean_text(item) for item in items(value) if clean_text(item)]
    return ", ".join(refs) if refs else "No evidence ID supplied"


def percent(value: Any) -> str:
    number = numeric(value, minimum=0.0, maximum=1.0)
    return "Not available" if number is None else f"{number:.0%}"


def score_text(value: Any, maximum: float = 100.0) -> str:
    number = numeric(value, minimum=0.0, maximum=maximum)
    return "Not scored" if number is None else f"{number:.1f}/{maximum:.0f}"


def validate_report_data(data: Mapping[str, Any]) -> list[str]:
    """Return hard-gate errors; the caller must stop when nonempty."""
    errors: list[str] = []
    if not isinstance(data, Mapping):
        return ["Report input must be a mapping"]
    metadata = obj(data.get("metadata"))
    if not clean_text(metadata.get("title")):
        errors.append("metadata.title is required")
    cutoff = clean_text(metadata.get("evidence_cutoff"))
    try:
        if not cutoff:
            raise ValueError
        date.fromisoformat(cutoff)
    except ValueError:
        errors.append("metadata.evidence_cutoff must use YYYY-MM-DD")
    if not clean_text(metadata.get("output_language")):
        errors.append("metadata.output_language is required")

    technology = obj(data.get("technology"))
    if not clean_text(technology.get("topic")):
        errors.append("technology.topic is required")
    if not clean_text(technology.get("source")):
        errors.append("technology.source is required")

    evidence_ids = set()
    for index, evidence in enumerate(items(data.get("evidence")), 1):
        if not isinstance(evidence, Mapping):
            errors.append(f"evidence[{index}] must be an object")
            continue
        identifier = clean_text(evidence.get("evidence_id"))
        if not identifier:
            errors.append(f"evidence[{index}] requires evidence_id")
        elif identifier in evidence_ids:
            errors.append(f"Duplicate evidence ID: {identifier}")
        else:
            evidence_ids.add(identifier)
        url = evidence.get("url_or_locator")
        if clean_text(url).startswith(("http:", "https:")) and not safe_url(url):
            errors.append(f"evidence[{index}] has an unsafe URL")

    def check_refs(owner: str, refs: Any) -> None:
        for ref in items(refs):
            normalized = clean_text(ref)
            if normalized and normalized not in evidence_ids:
                errors.append(f"{owner} references missing evidence ID {normalized}")

    for index, finding in enumerate(items(data.get("findings")), 1):
        if isinstance(finding, Mapping):
            check_refs(f"findings[{index}]", finding.get("evidence_ids"))
    for index, metric in enumerate(items(technology.get("kpis")), 1):
        if isinstance(metric, Mapping):
            check_refs(f"technology.kpis[{index}]", metric.get("evidence_ids"))
    for index, candidate in enumerate(items(data.get("recipients")), 1):
        if not isinstance(candidate, Mapping):
            errors.append(f"recipients[{index}] must be an object")
            continue
        if not clean_text(candidate.get("company_name")):
            errors.append(f"recipients[{index}] requires company_name")
        check_refs(f"recipients[{index}]", candidate.get("evidence_ids"))
        coverage = candidate.get("evidence_coverage")
        if coverage is not None:
            try:
                numeric(coverage, minimum=0.0, maximum=1.0)
            except ReportDataError as exc:
                errors.append(f"recipients[{index}].evidence_coverage: {exc}")
        if candidate.get("rankable") and not candidate.get("eligible"):
            errors.append(f"recipients[{index}] cannot be rankable when ineligible")

    valuation = obj(data.get("patent_value")).get("valuation", {})
    if isinstance(valuation, Mapping) and status(valuation.get("status")) == "executed":
        for required in ("method", "currency", "valuation_date", "low", "base", "high", "assumptions"):
            if valuation.get(required) in (None, "", []):
                errors.append(f"Executed valuation requires {required}")

    return errors


def render_navigation() -> str:
    entries = "".join(f'<li><a href="#{section_id}">{e(label)}</a></li>' for section_id, label in REPORT_SECTIONS)
    return f'<nav class="toc" aria-label="Report sections"><ul>{entries}</ul></nav>'


def render_header(data: Mapping[str, Any]) -> str:
    metadata = obj(data.get("metadata"))
    technology = obj(data.get("technology"))
    title = metadata.get("title") or f'Technology transfer match: {technology.get("topic", "")}'
    return (
        '<header class="report-header">'
        '<div class="report-kicker">Technology transfer opportunity assessment</div>'
        f'<h1>{e(title)}</h1>'
        '<div class="header-meta">'
        f'<span>Technology: {e(technology.get("topic", "Not available"))}</span>'
        f'<span>Source: {e(technology.get("source", "Not available"))}</span>'
        f'<span>Evidence cutoff: {e(metadata.get("evidence_cutoff", "Not available"))}</span>'
        f'<span>Report status: {e(metadata.get("status", "Draft"))}</span>'
        '</div></header>'
    )


def render_summary(data: Mapping[str, Any]) -> str:
    findings = []
    for item in items(data.get("findings")):
        if not isinstance(item, Mapping):
            continue
        findings.append(
            '<article class="finding">'
            f'<h3>{e(item.get("finding", "Finding"))}</h3>'
            f'<p>{e(item.get("interpretation", ""))}</p>'
            f'<p class="source-note">Evidence: {e(evidence_refs(item.get("evidence_ids")))}; '
            f'confidence: {e(item.get("confidence", "Not assessed"))}.</p>'
            f'<p class="limitation">{e(item.get("limitation", "No limitation supplied."))}</p>'
            '</article>'
        )
    body = "".join(findings) or '<p class="empty">No decision findings supplied.</p>'
    return f'<section id="summary"><h2>Decision summary</h2><div class="finding-grid">{body}</div></section>'


def render_scope(data: Mapping[str, Any]) -> str:
    scope = obj(data.get("scope"))
    cards = "".join((
        field("Transfer objective", scope.get("transfer_objective")),
        field("Target applications", scope.get("target_applications")),
        field("Target markets", scope.get("target_markets")),
        field("Jurisdictions", scope.get("jurisdictions")),
        field("Recipient types", scope.get("recipient_types")),
        field("Excluded recipients", scope.get("excluded_recipients")),
        field("Currency / valuation date", scope.get("currency_and_valuation_date")),
        field("Minimum evidence coverage", scope.get("minimum_evidence_coverage")),
    ))
    statuses = obj(data.get("section_status"))
    status_rows = "".join(
        f'<tr><th scope="row">{e(name.replace("_", " ").title())}</th><td>{badge(value)}</td></tr>'
        for name, value in statuses.items()
    )
    status_table = (
        '<div class="table-wrap"><table><caption>Execution status by evidence area</caption><tbody>'
        f'{status_rows}</tbody></table></div>' if status_rows else '<p class="empty">No section status supplied.</p>'
    )
    return f'<section id="scope"><h2>Scope and evidence quality</h2><div class="field-grid">{cards}</div>{status_table}</section>'


def render_kpis(kpis: Sequence[Any]) -> str:
    rows = []
    for metric in kpis:
        if not isinstance(metric, Mapping):
            continue
        rows.append(
            '<tr>'
            f'<th scope="row">{e(metric.get("name", "Unnamed metric"))}</th>'
            f'<td>{e(metric.get("value", ""))}</td><td>{e(metric.get("unit", ""))}</td>'
            f'<td>{e(metric.get("method", ""))}</td><td>{e(metric.get("conditions", ""))}</td>'
            f'<td>{e(evidence_refs(metric.get("evidence_ids")))}</td>'
            f'<td>{e(metric.get("uncertainty", ""))}</td></tr>'
        )
    if not rows:
        return '<p class="empty">No verified KPI supplied.</p>'
    return (
        '<div class="table-wrap"><table><caption>Verified performance indicators</caption>'
        '<thead><tr><th>Metric</th><th>Value</th><th>Unit</th><th>Method</th><th>Conditions</th><th>Evidence</th><th>Uncertainty</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div>'
    )


def render_alternatives(alternatives: Sequence[Any]) -> str:
    rows = []
    for alternative in alternatives:
        if not isinstance(alternative, Mapping):
            continue
        rows.append(
            '<tr>'
            f'<th scope="row">{e(alternative.get("name", "Unnamed alternative"))}</th>'
            f'<td>{e(alternative.get("mechanism", ""))}</td>'
            f'<td>{e(alternative.get("performance", ""))}</td>'
            f'<td>{e(alternative.get("cost_status", ""))}</td>'
            f'<td>{e(alternative.get("readiness_scale", ""))}</td>'
            f'<td>{e(alternative.get("integration", ""))}</td>'
            f'<td>{e(evidence_refs(alternative.get("evidence_ids")))}</td>'
            f'<td>{e(alternative.get("limitations", ""))}</td></tr>'
        )
    if not rows:
        return '<p class="empty">No comparable alternative evidence supplied.</p>'
    return (
        '<div class="table-wrap"><table><caption>Alternative and incumbent comparison</caption>'
        '<thead><tr><th>Alternative</th><th>Mechanism</th><th>Performance</th><th>Cost status</th><th>Scale/readiness</th><th>Integration</th><th>Evidence</th><th>Limitations</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div>'
    )


def render_technology(data: Mapping[str, Any]) -> str:
    tech = obj(data.get("technology"))
    basic = "".join((
        field("Provider", tech.get("source")),
        field("Topic", tech.get("topic")),
        field("Claimed readiness", tech.get("claimed_readiness")),
        field("Supported readiness", tech.get("supported_readiness")),
        field("IP / ownership status", tech.get("ip_status")),
        field("Core team", tech.get("core_team")),
    ))
    return (
        '<section id="technology"><h2>Technology and transfer package</h2>'
        f'<div class="field-grid">{basic}</div>'
        f'<h3>Technical background and problem</h3><p>{e(tech.get("background", "Not available"))}</p>'
        f'<h3>Mechanism and method</h3><p>{e(tech.get("summary", "Not available"))}</p>'
        f'<h3>Supported innovation points</h3>{render_list(items(tech.get("innovations")))}'
        f'<h3>Performance evidence</h3>{render_kpis(items(tech.get("kpis")))}'
        f'<h3>Alternatives</h3>{render_alternatives(items(tech.get("alternatives")))}'
        '<div class="two-column">'
        f'<div><h3>Application scenarios</h3>{render_list(items(tech.get("scenarios")))}</div>'
        f'<div><h3>Transfer advantages</h3>{render_list(items(tech.get("transfer_advantages")))}</div>'
        '</div>'
        f'<h3>Transfer-package gaps</h3>{render_list(items(tech.get("transfer_gaps")))}'
        '</section>'
    )


def score_bar(label: str, value: Any, maximum: float, note: Any = "") -> str:
    number = numeric(value, minimum=0.0, maximum=maximum)
    if number is None:
        return f'<div class="score-row"><div><strong>{e(label)}</strong><div class="source-note">Not scored</div></div></div>'
    width = 0.0 if maximum <= 0 else number / maximum * 100.0
    return (
        '<div class="score-row">'
        f'<div><strong>{e(label)}</strong><div class="source-note">{e(note)}</div></div>'
        f'<div class="bar" role="img" aria-label="{e(label)}: {number:.1f} of {maximum:.1f}">'
        f'<span style="width:{width:.2f}%"></span></div><div class="numeric">{number:.1f}/{maximum:.0f}</div></div>'
    )


def render_advancement(data: Mapping[str, Any]) -> str:
    advancement = obj(data.get("advancement"))
    factors = []
    for factor in items(advancement.get("factors")):
        if not isinstance(factor, Mapping):
            continue
        factors.append(
            '<article class="score-card">'
            f'<h3>{e(factor.get("name", "Factor"))}</h3>'
            f'{score_bar("Weighted contribution", factor.get("weighted_score"), factor.get("weight", 100), factor.get("rationale", ""))}'
            f'<p>{e(factor.get("rationale", "No rationale supplied."))}</p>'
            f'<p class="source-note">Raw score: {e(factor.get("raw_score", "Not scored"))}; '
            f'weight: {e(factor.get("weight", "Not specified"))}; evidence: {e(evidence_refs(factor.get("evidence_ids")))}; '
            f'confidence: {e(factor.get("confidence", "Not assessed"))}.</p>'
            f'<p class="limitation">Missing evidence: {e(factor.get("missing_evidence", "None recorded"))}; '
            f'sensitivity: {e(factor.get("sensitivity", "Not assessed"))}.</p></article>'
        )
    total = advancement.get("total")
    return (
        '<section id="advancement"><h2>Advancement and readiness</h2>'
        f'<div class="total-score"><span>{e(score_text(total))}</span><strong>{e(advancement.get("grade_label", "Not assessed"))}</strong></div>'
        f'<p class="method-note">Rubric: {e(advancement.get("rubric", "Not specified"))}. '
        f'Weight approval: {e(advancement.get("weight_approval", "Not recorded"))}.</p>'
        f'<div class="score-grid">{"".join(factors) or "<p class=\"empty\">No advancement factors supplied.</p>"}</div>'
        '</section>'
    )


def render_value_dimension(name: str, dimension: Any) -> str:
    item = obj(dimension)
    return (
        '<article class="value-panel">'
        f'<h3>{e(name)}</h3>{badge(item.get("status", "not_assessed"))}'
        f'<p>{e(item.get("assessment", "No assessment supplied."))}</p>'
        f'{render_list(items(item.get("factors")))}'
        f'<p class="source-note">Evidence: {e(evidence_refs(item.get("evidence_ids")))}; '
        f'limitations: {e(item.get("limitations", "Not specified"))}.</p></article>'
    )


def render_valuation(value: Any) -> str:
    valuation = obj(value)
    state = status(valuation.get("status", "not_assessed"))
    if state != "executed":
        return (
            '<div class="valuation limitation"><h3>Valuation</h3>'
            f'{badge(state)}<p>{e(valuation.get("reason", "Valuation was not assessed."))}</p>'
            f'{render_list(items(valuation.get("required_inputs")))}</div>'
        )
    currency = clean_text(valuation.get("currency"))
    low = clean_text(valuation.get("low"))
    base = clean_text(valuation.get("base"))
    high = clean_text(valuation.get("high"))
    return (
        '<div class="valuation"><h3>Valuation scenarios</h3>'
        f'<p class="valuation-range">Low {e(currency)} {e(low)} · Base {e(currency)} {e(base)} · High {e(currency)} {e(high)}</p>'
        f'<p>Method: {e(valuation.get("method"))}; valuation date: {e(valuation.get("valuation_date"))}.</p>'
        f'<h4>Assumptions</h4>{render_list(items(valuation.get("assumptions")))}'
        f'<h4>Sensitivity</h4>{render_list(items(valuation.get("sensitivity")))}'
        f'<p class="limitation">{e(valuation.get("limitations", "No limitation supplied."))}</p></div>'
    )


def render_patent_value(data: Mapping[str, Any]) -> str:
    value = obj(data.get("patent_value"))
    panels = "".join((
        render_value_dimension("Technical value", value.get("technical")),
        render_value_dimension("Market value evidence", value.get("market")),
        render_value_dimension("Legal value evidence", value.get("legal")),
        render_value_dimension("Strategic value", value.get("strategic")),
    ))
    return f'<section id="patent-value"><h2>Patent and commercialization value</h2><div class="value-grid">{panels}</div>{render_valuation(value.get("valuation"))}</section>'


def render_portfolio_metrics(portfolio: Mapping[str, Any]) -> str:
    metrics = (
        ("Population", portfolio.get("population_count"), portfolio.get("counting_unit")),
        ("Displayed patents", portfolio.get("displayed_count"), "selected records"),
        ("Granted members", portfolio.get("granted_count"), portfolio.get("counting_unit")),
        ("Jurisdictions", len(items(portfolio.get("jurisdictions"))), "authorities"),
    )
    cards = []
    for label, value, unit in metrics:
        cards.append(
            '<div class="metric"><div class="metric-label">'
            f'{e(label)}</div><div class="metric-value">{e(value if value not in (None, "") else "N/A")}</div>'
            f'<div class="source-note">{e(unit or "Unit not specified")}</div></div>'
        )
    return '<div class="metric-grid">' + "".join(cards) + "</div>"


def render_classifications(values: Sequence[Any]) -> str:
    rows = []
    for item in values:
        if not isinstance(item, Mapping):
            continue
        rows.append(
            f'<tr><th scope="row">{e(item.get("code", ""))}</th><td>{e(item.get("description", ""))}</td>'
            f'<td class="numeric">{e(item.get("count", ""))}</td><td>{e(item.get("counting_unit", ""))}</td>'
            f'<td>{e(item.get("method", ""))}</td></tr>'
        )
    if not rows:
        return '<p class="empty">No classification distribution supplied.</p>'
    return (
        '<div class="table-wrap"><table><caption>Patent classification distribution</caption>'
        '<thead><tr><th>Code</th><th>Description</th><th>Count</th><th>Unit</th><th>Method</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div>'
    )


def render_patent(item: Mapping[str, Any]) -> str:
    identifier = item.get("publication_number") or item.get("application_number") or "Unidentified record"
    return (
        '<article class="patent-record">'
        f'<div class="record-label">{e(item.get("role", "Selected patent"))}</div>'
        f'<h3>{link(item.get("title", identifier), item.get("url"))}</h3>'
        '<div class="record-meta">'
        f'<span>{e(identifier)}</span><span>Filed: {e(item.get("filing_date", "N/A"))}</span>'
        f'<span>Published: {e(item.get("publication_date", "N/A"))}</span>'
        f'<span>Status: {e(item.get("status", "N/A"))} as of {e(item.get("status_as_of", "N/A"))}</span>'
        '</div>'
        f'<p>{e(item.get("summary", "No evidence-bounded summary supplied."))}</p>'
        f'<p class="source-note">Classification: {e(clean_text(item.get("classifications")))}; '
        f'citation context: {e(item.get("citation_context", "Not assessed"))}; '
        f'evidence: {e(evidence_refs(item.get("evidence_ids")))}.</p>'
        f'<p class="limitation">{e(item.get("limitations", "No limitation supplied."))}</p></article>'
    )


def render_portfolio(data: Mapping[str, Any]) -> str:
    portfolio = obj(data.get("portfolio"))
    records = "".join(render_patent(item) for item in items(portfolio.get("patents")) if isinstance(item, Mapping))
    return (
        '<section id="portfolio"><h2>Patent portfolio evidence</h2>'
        f'<p class="method-note">Search scope: {e(portfolio.get("search_scope", "Not specified"))}; '
        f'family rule: {e(portfolio.get("family_rule", "Not specified"))}; '
        f'selection method: {e(portfolio.get("selection_method", "Not specified"))}.</p>'
        f'{render_portfolio_metrics(portfolio)}'
        f'<h3>Classification distribution</h3>{render_classifications(items(portfolio.get("classifications")))}'
        f'<h3>Selected patent records</h3>{records or "<p class=\"empty\">No selected patent records supplied.</p>"}'
        f'<h3>Portfolio strategy observations</h3>{render_list(items(portfolio.get("strategy_observations")))}'
        '</section>'
    )


def recipient_dimension_rows(candidate: Mapping[str, Any]) -> str:
    rows = []
    for name, dimension in obj(candidate.get("dimensions")).items():
        item = obj(dimension)
        maximum = item.get("maximum", 0)
        rows.append(
            '<tr>'
            f'<th scope="row">{e(name.replace("_", " ").title())}</th>'
            f'<td>{e(score_text(item.get("raw_score"), maximum or 100))}</td>'
            f'<td>{e(percent(item.get("evidence_coverage")))}</td>'
            f'<td>{badge(item.get("status", "not_scored"))}</td>'
            f'<td>{e(evidence_refs(item.get("evidence_ids")))}</td></tr>'
        )
    return "".join(rows)


def render_recipient(candidate: Mapping[str, Any], rank: int | None) -> str:
    rank_text = f"Rank {rank}" if rank is not None else "Unranked"
    total = score_text(candidate.get("raw_total"))
    coverage = percent(candidate.get("evidence_coverage"))
    return (
        '<article class="recipient">'
        '<header class="recipient-header"><div>'
        f'<div class="record-label">{e(rank_text)} · {e(candidate.get("grade_label", "Not assessed"))}</div>'
        f'<h3>{e(candidate.get("company_name", "Unnamed candidate"))}</h3>'
        f'<p>{e(candidate.get("recipient_type", "Recipient type not specified"))} · '
        f'{e(candidate.get("relevant_business_unit", "Business unit not specified"))}</p></div>'
        f'<div class="recipient-total"><strong>{e(total)}</strong><span>Coverage {e(coverage)}</span></div></header>'
        '<div class="table-wrap"><table><caption>Evidence-dimension score</caption>'
        '<thead><tr><th>Dimension</th><th>Raw score</th><th>Coverage</th><th>Status</th><th>Evidence</th></tr></thead>'
        f'<tbody>{recipient_dimension_rows(candidate)}</tbody></table></div>'
        '<div class="three-column">'
        f'<div><h4>Supported reasons</h4>{render_list(items(candidate.get("reasons")))}</div>'
        f'<div><h4>Evidence gaps</h4>{render_list(items(candidate.get("evidence_gaps")))}</div>'
        f'<div><h4>Next validation actions</h4>{render_list(items(candidate.get("next_actions")))}</div>'
        '</div>'
        f'<p class="source-note">Eligibility: {e(candidate.get("eligible", False))}; rankable: {e(candidate.get("rankable", False))}; '
        f'sensitivity: {e(candidate.get("sensitivity_low", "N/A"))}–{e(candidate.get("sensitivity_high", "N/A"))}; '
        f'model: {e(candidate.get("model_version", "Not specified"))}; evidence: {e(evidence_refs(candidate.get("evidence_ids")))}.</p>'
        '</article>'
    )


def render_recipients(data: Mapping[str, Any]) -> str:
    method = obj(data.get("matching_method"))
    rank_counter = 0
    cards = []
    for candidate in items(data.get("recipients")):
        if not isinstance(candidate, Mapping):
            continue
        rank = None
        if candidate.get("rankable"):
            rank_counter += 1
            rank = rank_counter
        cards.append(render_recipient(candidate, rank))
    return (
        '<section id="recipients"><h2>Potential recipients</h2>'
        f'<p class="method-note">Model: {e(method.get("model_version", "Not specified"))}; '
        f'top-level weights: {e(clean_text(method.get("weights")))}; '
        f'minimum coverage: {e(method.get("minimum_coverage", "Not specified"))}; '
        f'missing-data rule: {e(method.get("missing_data_rule", "Not specified"))}.</p>'
        f'<h3>Discovery and entity-resolution method</h3><p>{e(method.get("discovery_method", "Not specified"))}</p>'
        f'<h3>Sensitivity summary</h3><p>{e(method.get("sensitivity_summary", "Not assessed"))}</p>'
        f'{"".join(cards) or "<p class=\"empty\">No candidate recipients supplied.</p>"}</section>'
    )


def render_risk_dimension(item: Mapping[str, Any]) -> str:
    name = clean_text(item.get("name")) or "Risk dimension"
    score = item.get("score")
    return (
        '<article class="risk-card">'
        f'<h3>{e(name)}</h3>{score_bar("Risk", score, 100, item.get("rationale", ""))}'
        f'<p>{e(item.get("rationale", "No rationale supplied."))}</p>'
        f'<h4>Mitigations</h4>{render_list(items(item.get("mitigations")))}'
        f'<p class="source-note">Evidence: {e(evidence_refs(item.get("evidence_ids")))}; '
        f'uncertainty: {e(item.get("uncertainty", "Not assessed"))}; '
        f'owner: {e(item.get("owner", "Not assigned"))}.</p></article>'
    )


def render_risk_profile(profile: Mapping[str, Any]) -> str:
    return (
        '<article class="risk-profile">'
        f'<div class="record-label">{e(profile.get("risk_label", "Risk not assessed"))}</div>'
        f'<h3>{e(profile.get("company_name", "Unnamed candidate"))}</h3>'
        f'<h4>Candidate-specific concerns</h4>{render_list(items(profile.get("concerns")))}'
        f'<h4>Mitigations and gates</h4>{render_list(items(profile.get("mitigations")))}'
        f'<p class="source-note">Evidence: {e(evidence_refs(profile.get("evidence_ids")))}.</p></article>'
    )


def render_risk(data: Mapping[str, Any]) -> str:
    risk = obj(data.get("risk"))
    dimensions = "".join(
        render_risk_dimension(item) for item in items(risk.get("dimensions")) if isinstance(item, Mapping)
    )
    profiles = "".join(
        render_risk_profile(item) for item in items(risk.get("recipient_profiles")) if isinstance(item, Mapping)
    )
    return (
        '<section id="risk"><h2>Transfer risk</h2>'
        f'<div class="risk-summary"><strong>Overall risk: {e(score_text(risk.get("overall_score")))}</strong>'
        f'<span>{e(risk.get("overall_label", "Not assessed"))}</span>'
        f'<p>{e(risk.get("method", "Risk method not specified."))}</p></div>'
        f'<div class="risk-grid">{dimensions or "<p class=\"empty\">No risk dimensions supplied.</p>"}</div>'
        f'<h3>Top-recipient risk profiles</h3><div class="profile-grid">{profiles or "<p class=\"empty\">No recipient-specific risk profiles supplied.</p>"}</div>'
        '</section>'
    )


def render_timeline(phases: Sequence[Any]) -> str:
    cards = []
    for index, phase in enumerate(phases, 1):
        if not isinstance(phase, Mapping):
            continue
        cards.append(
            '<article class="timeline-phase">'
            f'<div class="phase-index">{index}</div><div><h3>{e(phase.get("name", "Phase"))}</h3>'
            f'<p class="source-note">Indicative timing: {e(phase.get("timing", "Not specified"))}; '
            f'gate owner: {e(phase.get("owner", "Not assigned"))}.</p>'
            f'{render_list(items(phase.get("actions")))}'
            f'<p class="limitation">Exit gate: {e(phase.get("exit_gate", "Not specified"))}.</p></div></article>'
        )
    return '<div class="timeline">' + ("".join(cards) or '<p class="empty">No transfer phases supplied.</p>') + "</div>"


def render_routes(routes: Sequence[Any]) -> str:
    cards = []
    for route in routes:
        if not isinstance(route, Mapping):
            continue
        cards.append(
            '<article class="route">'
            f'<h3>{e(route.get("name", "Transfer route"))}</h3><p>{e(route.get("fit", "Fit not assessed"))}</p>'
            f'<h4>Advantages</h4>{render_list(items(route.get("advantages")))}'
            f'<h4>Trade-offs</h4>{render_list(items(route.get("tradeoffs")))}'
            f'<h4>Key terms and gates</h4>{render_list(items(route.get("terms_and_gates")))}'
            f'<p class="source-note">Evidence: {e(evidence_refs(route.get("evidence_ids")))}.</p></article>'
        )
    return '<div class="route-grid">' + ("".join(cards) or '<p class="empty">No route comparison supplied.</p>') + "</div>"


def render_pathway(data: Mapping[str, Any]) -> str:
    pathway = obj(data.get("pathway"))
    return (
        '<section id="pathway"><h2>Transfer pathway</h2>'
        f'<p>{e(pathway.get("strategy", "No pathway strategy supplied."))}</p>'
        f'<h3>Gated timeline</h3>{render_timeline(items(pathway.get("phases")))}'
        f'<h3>Transfer-route comparison</h3>{render_routes(items(pathway.get("routes")))}'
        '</section>'
    )


def render_source_register(values: Sequence[Any]) -> str:
    rows = []
    for source in values:
        if not isinstance(source, Mapping):
            continue
        title = source.get("title") or source.get("evidence_id") or "Source"
        rows.append(
            '<tr>'
            f'<th scope="row">{e(source.get("evidence_id", ""))}</th>'
            f'<td>{e(source.get("source_type", ""))}</td>'
            f'<td>{link(title, source.get("url_or_locator"))}</td>'
            f'<td>{e(source.get("publisher_or_owner", ""))}</td>'
            f'<td>{e(source.get("publication_or_event_date", ""))}</td>'
            f'<td>{e(source.get("retrieved_at", ""))}</td>'
            f'<td>{e(source.get("quality", ""))}</td>'
            f'<td>{e(source.get("limitations", ""))}</td></tr>'
        )
    if not rows:
        return '<p class="empty">No source register supplied.</p>'
    return (
        '<div class="table-wrap"><table><caption>Evidence and source register</caption>'
        '<thead><tr><th>ID</th><th>Type</th><th>Source</th><th>Publisher/owner</th><th>Published/event</th><th>Retrieved</th><th>Quality</th><th>Limitations</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div>'
    )


def render_sources(data: Mapping[str, Any]) -> str:
    limitations = items(data.get("limitations"))
    return (
        '<section id="sources"><h2>Sources and limitations</h2>'
        f'{render_source_register(items(data.get("evidence")))}'
        f'<h3>Overall limitations</h3>{render_list(limitations)}'
        '<div class="legal-note"><strong>Decision boundary.</strong> This report supports prioritization and diligence planning. '
        'It does not establish ownership, validity, infringement clearance, standards essentiality, transaction value, market demand, financial capacity, compliance, or willingness to transact.</div>'
        '</section>'
    )


CSS = r"""
:root {
  --ink: #17212b;
  --muted: #536475;
  --line: #c9d4de;
  --line-strong: #8293a4;
  --paper: #ffffff;
  --wash: #f3f6f8;
  --accent: #155b8a;
  --accent-dark: #0d4267;
  --accent-soft: #e8f1f7;
  --success: #21633b;
  --success-bg: #edf7f1;
  --warning: #7a4e00;
  --warning-bg: #fff7df;
  --danger: #8b2c2c;
  --danger-bg: #fff0f0;
  --radius: 4px;
  --measure: 86rem;
}

* { box-sizing: border-box; }
html { color-scheme: light; scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont,
    "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  font-size: 16px;
  line-height: 1.55;
}
a {
  color: var(--accent-dark);
  text-decoration-thickness: .08em;
  text-underline-offset: .14em;
  overflow-wrap: anywhere;
}
a:hover { color: var(--accent); }
a:focus-visible, summary:focus-visible {
  outline: 3px solid #f2b84b;
  outline-offset: 3px;
}
.skip-link {
  position: absolute;
  top: -5rem;
  left: 1rem;
  z-index: 50;
  background: var(--ink);
  color: var(--paper);
  padding: .65rem .85rem;
}
.skip-link:focus { top: 1rem; }
.report-header {
  border-bottom: 1px solid var(--line-strong);
  padding: 3rem max(1.25rem, calc((100vw - var(--measure)) / 2));
}
.report-kicker {
  color: var(--accent-dark);
  font-size: .78rem;
  font-weight: 750;
  letter-spacing: .1em;
  text-transform: uppercase;
}
.report-header h1 {
  max-width: 62rem;
  margin: .4rem 0 .9rem;
  font-family: Georgia, "Times New Roman", serif;
  font-size: clamp(2rem, 4.8vw, 3.6rem);
  font-weight: 600;
  letter-spacing: -.025em;
  line-height: 1.08;
}
.header-meta {
  display: flex;
  flex-wrap: wrap;
  gap: .45rem 1.35rem;
  color: var(--muted);
  font-size: .9rem;
}
.toc {
  position: sticky;
  top: 0;
  z-index: 20;
  border-bottom: 1px solid var(--line);
  background: rgba(255, 255, 255, .97);
}
.toc ul {
  max-width: var(--measure);
  margin: 0 auto;
  padding: .65rem 1.25rem;
  display: flex;
  gap: .35rem 1rem;
  overflow-x: auto;
  list-style: none;
}
.toc a { white-space: nowrap; text-decoration: none; font-size: .86rem; font-weight: 700; }
main { max-width: var(--measure); margin: 0 auto; padding: 2rem 1.25rem 5rem; }
section { padding: 2.2rem 0; border-bottom: 1px solid var(--line); }
h2, h3, h4 { scroll-margin-top: 5rem; }
h2 {
  margin: 0 0 1.25rem;
  font-family: Georgia, "Times New Roman", serif;
  font-size: clamp(1.55rem, 3vw, 2.25rem);
  line-height: 1.2;
}
h3 { margin: 1.6rem 0 .65rem; font-size: 1.08rem; }
h4 { margin: 1rem 0 .4rem; font-size: .92rem; }
p { max-width: 76ch; }
.finding-grid, .field-grid, .score-grid, .value-grid, .risk-grid, .profile-grid, .route-grid,
.metric-grid, .two-column, .three-column {
  display: grid;
  gap: .9rem;
}
.finding-grid, .score-grid, .value-grid, .risk-grid { grid-template-columns: repeat(auto-fit, minmax(18rem, 1fr)); }
.field-grid, .metric-grid { grid-template-columns: repeat(auto-fit, minmax(14rem, 1fr)); }
.profile-grid, .route-grid { grid-template-columns: repeat(auto-fit, minmax(18rem, 1fr)); }
.two-column { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.three-column { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.finding, .field, .score-card, .value-panel, .patent-record, .recipient, .risk-card,
.risk-profile, .route, .timeline-phase, .metric, .valuation, .risk-summary, .legal-note {
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--paper);
  padding: 1rem;
}
.field-label, .metric-label, .record-label {
  color: var(--muted);
  font-size: .76rem;
  font-weight: 750;
  letter-spacing: .05em;
  text-transform: uppercase;
}
.metric-value {
  margin-top: .2rem;
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.8rem;
  font-variant-numeric: tabular-nums;
}
.source-note, .method-note { color: var(--muted); font-size: .84rem; }
.method-note { border-left: 4px solid var(--accent); background: var(--accent-soft); padding: .75rem 1rem; max-width: none; }
.limitation { border-left: 4px solid var(--warning); background: var(--warning-bg); padding: .75rem 1rem; }
.legal-note { border-left: 4px solid var(--line-strong); background: var(--wash); margin-top: 1rem; }
.empty { color: var(--muted); font-style: italic; }
.status {
  display: inline-block;
  border: 1px solid currentColor;
  border-radius: 999px;
  padding: .12rem .5rem;
  font-size: .75rem;
  font-weight: 750;
}
.status-executed { color: var(--success); background: var(--success-bg); }
.status-partial, .status-not-scored, .status-not-assessed, .status-not-executed,
.status-unavailable { color: var(--warning); background: var(--warning-bg); }
.status-error { color: var(--danger); background: var(--danger-bg); }
.table-wrap { overflow-x: auto; margin: .8rem 0; }
table { width: 100%; border-collapse: collapse; font-size: .88rem; }
caption { padding: 0 0 .55rem; text-align: left; color: var(--muted); font-weight: 700; }
th, td { border-bottom: 1px solid var(--line); padding: .62rem .68rem; text-align: left; vertical-align: top; }
thead th { background: var(--wash); }
.numeric { text-align: right; font-variant-numeric: tabular-nums; }
.score-row { display: grid; grid-template-columns: minmax(10rem, 1fr) minmax(8rem, 2fr) auto; gap: .7rem; align-items: center; }
.bar { height: .68rem; border: 1px solid var(--line); background: var(--wash); }
.bar span { display: block; height: 100%; background: var(--accent); }
.total-score { display: flex; flex-wrap: wrap; gap: .7rem 1.3rem; align-items: baseline; margin-bottom: 1rem; }
.total-score span { font-family: Georgia, "Times New Roman", serif; font-size: 2.4rem; }
.valuation-range { font-family: Georgia, "Times New Roman", serif; font-size: 1.5rem; max-width: none; }
.record-meta { display: flex; flex-wrap: wrap; gap: .25rem 1rem; color: var(--muted); font-size: .84rem; }
.recipient { margin: 1rem 0; }
.recipient-header { display: flex; justify-content: space-between; gap: 1rem; align-items: flex-start; }
.recipient-header h3 { margin: .2rem 0; }
.recipient-total { display: flex; flex-direction: column; align-items: flex-end; min-width: 8rem; }
.recipient-total strong { font-family: Georgia, "Times New Roman", serif; font-size: 1.65rem; }
.recipient-total span { color: var(--muted); font-size: .8rem; }
.risk-summary { margin-bottom: 1rem; border-left: 4px solid var(--warning); }
.risk-summary strong { display: block; font-family: Georgia, "Times New Roman", serif; font-size: 1.4rem; }
.timeline { border-left: 2px solid var(--line-strong); margin-left: 1.1rem; }
.timeline-phase { display: grid; grid-template-columns: 2.2rem 1fr; margin: 0 0 1rem 1.1rem; position: relative; }
.phase-index { width: 2rem; height: 2rem; margin-left: -3.25rem; border: 2px solid var(--accent); border-radius: 50%; background: var(--paper); display: grid; place-items: center; font-weight: 750; }
.timeline-phase h3 { margin-top: 0; }
footer { max-width: var(--measure); margin: 0 auto; padding: 1.5rem 1.25rem 3rem; color: var(--muted); font-size: .84rem; }

@media (max-width: 56rem) {
  .two-column, .three-column { grid-template-columns: 1fr; }
  .recipient-header { flex-direction: column; }
  .recipient-total { align-items: flex-start; }
}
@media (max-width: 38rem) {
  .score-row { grid-template-columns: 1fr auto; }
  .bar { grid-column: 1 / -1; }
}
@media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }
@media print {
  :root { --ink: #000; --muted: #333; --line: #999; --paper: #fff; --wash: #f3f3f3; }
  @page { size: A4; margin: 14mm; }
  body { font-size: 9.5pt; }
  .skip-link, .toc { display: none; }
  .report-header, main, footer { max-width: none; padding-left: 0; padding-right: 0; }
  section { break-before: auto; }
  .finding, .field, .score-card, .value-panel, .patent-record, .recipient, .risk-card,
  .risk-profile, .route, .timeline-phase, .metric, table { break-inside: avoid; }
  a { color: #000; text-decoration: underline; }
  a[href^="http"]::after { content: " (" attr(href) ")"; font-size: 7.5pt; overflow-wrap: anywhere; }
}
"""


def generate_html_report(data: Mapping[str, Any]) -> str:
    """Validate and render the full localized report."""
    errors = validate_report_data(data)
    if errors:
        raise ReportDataError("Report validation failed:\n- " + "\n- ".join(errors))
    metadata = obj(data.get("metadata"))
    title = metadata.get("title") or "Technology transfer opportunity assessment"
    body = "".join((
        render_summary(data),
        render_scope(data),
        render_technology(data),
        render_advancement(data),
        render_patent_value(data),
        render_portfolio(data),
        render_recipients(data),
        render_risk(data),
        render_pathway(data),
        render_sources(data),
    ))
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<title>{e(title)}</title><style>{CSS}</style></head>
<body><a class="skip-link" href="#main">Skip to report content</a>
{render_header(data)}{render_navigation()}<main id="main">{body}</main>
<footer>Evidence-backed technology-transfer decision support. Verify material legal, technical, commercial, financial, regulatory and compliance decisions with qualified professionals and current primary sources.</footer>
</body></html>'''


def data_contract() -> dict[str, Any]:
    """Return a compact non-factual schema fixture for integration tests."""
    return {
        "metadata": {
            "title": "Technology transfer opportunity assessment — synthetic fixture",
            "evidence_cutoff": "2026-08-07",
            "output_language": "en",
            "status": "Synthetic fixture",
        },
        "scope": {
            "transfer_objective": "Joint development",
            "target_applications": ["Synthetic application"],
            "target_markets": ["Synthetic market"],
            "jurisdictions": ["US"],
            "recipient_types": ["Operating company"],
            "excluded_recipients": [],
            "currency_and_valuation_date": "USD; valuation not assessed",
            "minimum_evidence_coverage": "70%",
        },
        "section_status": {
            "patents": "partial",
            "company_signals": "partial",
            "procurement": "not_scored",
            "valuation": "not_assessed",
        },
        "findings": [{
            "finding": "Synthetic finding",
            "interpretation": "Used only to test report rendering.",
            "evidence_ids": ["E-001"],
            "confidence": "Synthetic",
            "limitation": "Not a real conclusion.",
        }],
        "technology": {
            "source": "Example Research Organization",
            "topic": "Synthetic technology",
            "claimed_readiness": "TRL 5 (claim)",
            "supported_readiness": "Not independently verified",
            "ip_status": "Synthetic fixture",
            "core_team": ["Example Researcher"],
            "background": "Synthetic problem statement.",
            "summary": "Synthetic mechanism and method.",
            "innovations": ["Synthetic innovation point."],
            "kpis": [{
                "name": "Synthetic performance",
                "value": "10",
                "unit": "arbitrary units",
                "method": "Synthetic fixture",
                "conditions": "Not real",
                "evidence_ids": ["E-001"],
                "uncertainty": "Not characterized",
            }],
            "alternatives": [],
            "scenarios": ["Synthetic application"],
            "transfer_advantages": ["Synthetic advantage"],
            "transfer_gaps": ["Replace fixture evidence"],
        },
        "advancement": {
            "rubric": "Synthetic configurable eight-factor baseline",
            "weight_approval": "Fixture only",
            "total": 60,
            "grade_label": "Synthetic",
            "factors": [],
        },
        "patent_value": {
            "technical": {"status": "partial", "assessment": "Synthetic", "evidence_ids": ["E-001"]},
            "market": {"status": "not_assessed"},
            "legal": {"status": "not_assessed"},
            "strategic": {"status": "not_assessed"},
            "valuation": {"status": "not_assessed", "reason": "Synthetic fixture"},
        },
        "portfolio": {
            "search_scope": "Synthetic fixture",
            "family_rule": "Simple-family fixture",
            "selection_method": "Synthetic",
            "population_count": 1,
            "displayed_count": 1,
            "granted_count": 0,
            "counting_unit": "simple family",
            "jurisdictions": ["US"],
            "classifications": [],
            "patents": [],
            "strategy_observations": [],
        },
        "matching_method": {
            "model_version": "global-transfer-match-1.0:fixture",
            "weights": {"patent": 40, "public_signal": 30, "procurement": 30},
            "minimum_coverage": "70%",
            "missing_data_rule": "Missing is not zero and is not silently redistributed.",
            "discovery_method": "Synthetic fixture",
            "sensitivity_summary": "Not assessed",
        },
        "recipients": [],
        "risk": {
            "overall_score": None,
            "overall_label": "Not assessed",
            "method": "Four-dimension baseline; fixture only",
            "dimensions": [],
            "recipient_profiles": [],
        },
        "pathway": {
            "strategy": "Synthetic gated pathway.",
            "phases": [],
            "routes": [],
        },
        "evidence": [{
            "evidence_id": "E-001",
            "source_type": "synthetic_fixture",
            "title": "Synthetic source",
            "publisher_or_owner": "Example",
            "publication_or_event_date": "2026-08-07",
            "retrieved_at": "2026-08-07",
            "url_or_locator": "https://example.com/source",
            "quality": "unverified",
            "limitations": "Not real evidence.",
        }],
        "limitations": ["All data in this fixture is synthetic."],
    }


if __name__ == "__main__":
    rendered = generate_html_report(data_contract())
    print(json.dumps({"status": "ok", "characters": len(rendered), "sections": len(REPORT_SECTIONS)}))

"""Build a safe, static technology-intelligence briefing from ``v2_data``.

Run this script from a working directory containing a reviewed ``v2_data.py``.
It writes one HTML file and never opens a browser. All evidence is escaped and
only HTTP(S) links are emitted.
"""

from __future__ import annotations

import html
import importlib.util
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse

import v2_css


SCRIPT_DIR = Path(__file__).resolve().parent
SECTION_IDS = ("scope", "findings", "trends", "patents", "literature", "news", "methods")


def e(value: Any) -> str:
    """Escape evidence as display text."""
    if value is None:
        return ""
    return html.escape(str(value), quote=True)


def text(value: Any) -> str:
    """Normalize a scalar for display."""
    if value is None:
        return ""
    if isinstance(value, (list, tuple, set)):
        return ", ".join(str(item) for item in value)
    return str(value)


def safe_url(value: Any) -> str:
    """Allow absolute HTTP(S) links only."""
    if not isinstance(value, str):
        return ""
    candidate = value.strip()
    parsed = urlparse(candidate)
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc:
        return ""
    return candidate


def link(label: Any, url: Any) -> str:
    """Render a safe external link or plain text."""
    label_html = e(label)
    accepted = safe_url(url)
    if not accepted:
        return label_html
    return f'<a href="{e(accepted)}" target="_blank" rel="noopener noreferrer">{label_html}</a>'


def sequence(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, (tuple, set)):
        return list(value)
    return [value]


def mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def load_data(path: Path | None = None) -> Any:
    """Load v2_data.py from the working directory or an explicit path."""
    source = path or (Path.cwd() / "v2_data.py")
    if not source.is_file():
        raise FileNotFoundError(f"Data module not found: {source}")
    spec = importlib.util.spec_from_file_location("briefing_v2_data", source)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load data module: {source}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get(data: Any, name: str, default: Any) -> Any:
    return getattr(data, name, default)


def status_badge(value: Any) -> str:
    raw = text(value).strip() or "not_executed"
    normalized = raw.lower().replace(" ", "_").replace("-", "_")
    allowed = {"executed", "not_executed", "unavailable", "error"}
    css_name = normalized if normalized in allowed else "unavailable"
    label = raw.replace("_", " ").strip().capitalize()
    return f'<span class="status status-{e(css_name.replace("_", "-"))}">{e(label)}</span>'


def render_list(items: Iterable[Any], css_class: str = "") -> str:
    values = [item for item in items if text(item).strip()]
    if not values:
        return '<p class="empty">Not available.</p>'
    class_attr = f' class="{e(css_class)}"' if css_class else ""
    return f'<ul{class_attr}>' + "".join(f"<li>{e(text(item))}</li>" for item in values) + "</ul>"


def render_nav() -> str:
    labels = {
        "scope": "Scope",
        "findings": "Key findings",
        "trends": "Trends and topics",
        "patents": "Patent evidence",
        "literature": "Scientific literature",
        "news": "Current developments",
        "methods": "Methods and limitations",
    }
    links = "".join(f'<li><a href="#{name}">{labels[name]}</a></li>' for name in SECTION_IDS)
    return f'<nav class="toc" aria-label="Report sections"><ul>{links}</ul></nav>'


def render_scope(data: Any) -> str:
    scope = mapping(get(data, "SCOPE", {}))
    rows = []
    labels = {
        "research_question": "Research question",
        "technology": "Technology",
        "companies": "Companies/legal entities",
        "jurisdictions": "Patent jurisdictions",
        "date_field": "Patent date field",
        "counting_unit": "Population counting unit",
        "family_rule": "Family/deduplication rule",
        "display_selection": "Displayed-record selection",
    }
    for key, label_value in labels.items():
        value = text(scope.get(key))
        if value:
            rows.append(f'<div class="panel"><div class="field-label">{e(label_value)}</div><div>{e(value)}</div></div>')
    content = "".join(rows) or '<p class="empty">Scope metadata was not supplied.</p>'
    return f'<section id="scope"><h2>Scope</h2><div class="scope-grid">{content}</div></section>'


def render_findings(data: Any) -> str:
    items = sequence(get(data, "SUMMARY", []))
    cards = []
    for item in items:
        if isinstance(item, dict):
            finding = item.get("finding", "")
            evidence = text(item.get("evidence_ids"))
            confidence = item.get("confidence", "")
            limitation = item.get("limitation", "")
            cards.append(
                '<article class="finding">'
                f'<h3>{e(finding or "Finding")}</h3>'
                f'<p><span class="field-label">Evidence</span><br>{e(evidence or "Not specified")}</p>'
                f'<p><span class="field-label">Confidence</span><br>{e(confidence or "Not specified")}</p>'
                f'<p class="limitation"><span class="field-label">Limitation</span><br>{e(limitation or "Not specified")}</p>'
                '</article>'
            )
        else:
            cards.append(f'<article class="finding"><p>{e(item)}</p></article>')
    body = "".join(cards) or '<p class="empty">No findings were supplied.</p>'
    return f'<section id="findings"><h2>Key findings</h2><div class="finding-grid">{body}</div></section>'


def render_company_metrics(data: Any) -> str:
    totals = mapping(get(data, "PATENT_TOTAL_BY_COMPANY", {}))
    cards = []
    for company, raw in totals.items():
        item = mapping(raw)
        population = item.get("population_count", "Unavailable")
        displayed = item.get("displayed_count", "Unavailable")
        unit = item.get("counting_unit", "Unspecified")
        count_status = item.get("count_status", "unavailable")
        cards.append(
            '<article class="metric">'
            f'<div class="metric-label">{e(company)}</div>'
            f'<div class="metric-value">{e(population)}</div>'
            f'<div>Population ({e(unit)})</div>'
            f'<div class="source-note">Count status: {e(count_status)}; displayed: {e(displayed)}</div>'
            '</article>'
        )
    return '<div class="metric-grid">' + ("".join(cards) or '<p class="empty">No population metrics.</p>') + "</div>"


def render_trends(data: Any) -> str:
    series = mapping(get(data, "TREND_SERIES", {}))
    meta = mapping(get(data, "TREND_META", {}))
    blocks = []
    for company, points_raw in series.items():
        points = mapping(points_raw)
        numeric_values = [value for value in points.values() if isinstance(value, (int, float))]
        maximum = max(numeric_values, default=0)
        rows = []
        for period, value in points.items():
            number = value if isinstance(value, (int, float)) else 0
            width = 0 if maximum <= 0 else max(0, min(100, number / maximum * 100))
            rows.append(
                '<div class="bar-row">'
                f'<span>{e(period)}</span><div class="bar-track" aria-hidden="true">'
                f'<div class="bar-fill" style="width:{width:.2f}%"></div></div>'
                f'<span class="numeric">{e(value)}</span></div>'
            )
        blocks.append(f'<div class="panel"><h3>{e(company)}</h3>{"".join(rows)}</div>')
    topic_items = []
    for raw in sequence(get(data, "WORD_CLOUD", [])):
        if isinstance(raw, dict):
            topic_items.append(f'{text(raw.get("term"))} ({text(raw.get("count"))})')
        else:
            topic_items.append(text(raw))
    note = (
        f'Date field: {text(meta.get("date_field")) or "not specified"}; '
        f'counting unit: {text(meta.get("counting_unit")) or "not specified"}.'
    )
    body = "".join(blocks) or '<p class="empty">No trend series supplied.</p>'
    return (
        '<section id="trends"><h2>Trends and topics</h2>'
        f'<p class="source-note">{e(note)}</p>{body}<h3>Frequent technical terms</h3>'
        f'{render_list(topic_items, "term-list")}</section>'
    )


def patent_index(data: Any) -> dict[str, dict[str, Any]]:
    output = {}
    for raw in sequence(get(data, "PATENTS", [])):
        if isinstance(raw, dict):
            key = text(raw.get("id") or raw.get("publication_number")).strip()
            if key and key not in output:
                output[key] = raw
    return output


def render_patent_card(item: dict[str, Any]) -> str:
    identifier = item.get("publication_number") or item.get("id") or "Unidentified record"
    title_html = link(item.get("title") or identifier, item.get("url"))
    meta = [
        item.get("assignee"),
        item.get("publication_date"),
        item.get("jurisdiction"),
        item.get("status"),
    ]
    fields = (
        ("Technical problem", item.get("technical_problem")),
        ("Technical means", item.get("technical_means")),
        ("Reported effect", item.get("reported_effect")),
        ("Evidence locator", item.get("evidence_locator")),
        ("Limitations", item.get("limitations")),
    )
    details = "".join(
        f'<p><span class="field-label">{e(label_value)}</span><br>{e(value)}</p>'
        for label_value, value in fields if text(value).strip()
    )
    return (
        '<article class="patent-card">'
        f'<h3>{title_html}</h3><div class="record-meta"><span>{e(identifier)}</span>'
        + "".join(f'<span>{e(value)}</span>' for value in meta if text(value).strip())
        + f'</div><p>{e(item.get("summary", ""))}</p>{details}</article>'
    )


def render_patents(data: Any) -> str:
    status = mapping(get(data, "SECTION_STATUS", {})).get("patents", "not_executed")
    index = patent_index(data)
    company_groups = mapping(get(data, "PATENTS_BY_COMPANY", {}))
    groups = []
    referenced: set[str] = set()
    for company, identifiers in company_groups.items():
        cards = []
        for identifier in sequence(identifiers):
            key = text(identifier)
            if key in index:
                referenced.add(key)
                cards.append(render_patent_card(index[key]))
        groups.append(
            f'<details open><summary>{e(company)} — {len(cards)} displayed records</summary>'
            f'<div class="details-body">{"".join(cards) or "<p class=\"empty\">No resolved records.</p>"}</div></details>'
        )
    ungrouped = [render_patent_card(item) for key, item in index.items() if key not in referenced]
    if ungrouped:
        groups.append(
            f'<details><summary>Other selected records — {len(ungrouped)}</summary>'
            f'<div class="details-body">{"".join(ungrouped)}</div></details>'
        )
    body = "".join(groups) or '<p class="empty">No patent records supplied.</p>'
    return f'<section id="patents"><h2>Patent evidence</h2>{status_badge(status)}{render_company_metrics(data)}{body}</section>'


def render_literature(data: Any) -> str:
    status = mapping(get(data, "SECTION_STATUS", {})).get("literature", "not_executed")
    cards = []
    for item in sequence(get(data, "LITERATURE", [])):
        if not isinstance(item, dict):
            continue
        url = item.get("url")
        doi = text(item.get("doi")).strip()
        if not safe_url(url) and doi:
            url = f"https://doi.org/{doi}"
        citation = " · ".join(filter(None, [text(item.get("authors")), text(item.get("journal")), text(item.get("year"))]))
        cards.append(
            '<article class="literature-item">'
            f'<h3>{link(item.get("title") or "Untitled record", url)}</h3>'
            f'<div class="record-meta"><span>{e(citation)}</span><span>{e(doi)}</span></div>'
            f'<p>{e(item.get("summary", ""))}</p>'
            f'<p class="source-note">Reason included: {e(item.get("reason_included", "Not specified"))}. '
            f'Source: {e(item.get("source", "Not specified"))}; retrieved {e(item.get("retrieved_at", "not specified"))}.</p>'
            f'<p class="limitation">{e(item.get("limitations", "No limitation supplied."))}</p></article>'
        )
    body = "".join(cards) or '<p class="empty">No literature records supplied.</p>'
    return f'<section id="literature"><h2>Scientific literature</h2>{status_badge(status)}{body}</section>'


def render_news(data: Any) -> str:
    status = mapping(get(data, "SECTION_STATUS", {})).get("news", "not_executed")
    cards = []
    for item in sequence(get(data, "NEWS", [])):
        if not isinstance(item, dict):
            continue
        dates = f'Published {text(item.get("publication_date")) or "date unavailable"}'
        if item.get("event_date"):
            dates += f'; event {text(item.get("event_date"))}'
        cards.append(
            '<article class="news-item">'
            f'<h3>{link(item.get("title") or "Untitled item", item.get("url"))}</h3>'
            f'<div class="record-meta"><span>{e(item.get("source", "Source unavailable"))}</span><span>{e(dates)}</span></div>'
            f'<p>{e(item.get("summary", ""))}</p>'
            f'<p class="source-note">Relevance: {e(item.get("relevance", "Not specified"))}. '
            f'Source quality: {e(item.get("source_quality", "Not specified"))}. '
            f'Retrieved: {e(item.get("retrieved_at", "not specified"))}.</p></article>'
        )
    body = "".join(cards) or '<p class="empty">No current-development records supplied.</p>'
    return f'<section id="news"><h2>Current developments</h2>{status_badge(status)}{body}</section>'


def render_methods(data: Any) -> str:
    limitations = sequence(get(data, "LIMITATIONS", []))
    sources = sequence(get(data, "SOURCES", []))
    source_rows = []
    for item in sources:
        if not isinstance(item, dict):
            continue
        source_rows.append(
            '<tr>'
            f'<td>{e(item.get("id", ""))}</td><td>{e(item.get("type", ""))}</td>'
            f'<td>{link(item.get("title", "Source"), item.get("url"))}</td>'
            f'<td>{e(item.get("retrieved_at", ""))}</td></tr>'
        )
    table = (
        '<div class="table-wrap"><table><caption>Source register</caption>'
        '<thead><tr><th>ID</th><th>Type</th><th>Source</th><th>Retrieved</th></tr></thead>'
        f'<tbody>{"".join(source_rows)}</tbody></table></div>' if source_rows else '<p class="empty">No source register supplied.</p>'
    )
    return (
        '<section id="methods"><h2>Methods and limitations</h2>'
        '<p>Counts, selected records, summaries, and interpretations must be read within the declared scope and evidence cutoff.</p>'
        f'<h3>Limitations</h3>{render_list(limitations)}<h3>Sources</h3>{table}</section>'
    )


def validate(data: Any) -> list[str]:
    errors = []
    index = patent_index(data)
    for company, identifiers in mapping(get(data, "PATENTS_BY_COMPANY", {})).items():
        for identifier in sequence(identifiers):
            if text(identifier) not in index:
                errors.append(f"PATENTS_BY_COMPANY[{company!r}] references missing patent {identifier!r}")
    for subtech in sequence(get(data, "SUB_TECHS", [])):
        if isinstance(subtech, dict):
            for identifier in sequence(subtech.get("patents")):
                if text(identifier) not in index:
                    errors.append(f"SUB_TECHS references missing patent {identifier!r}")
    for company, value in mapping(get(data, "PATENT_TOTAL_BY_COMPANY", {})).items():
        item = mapping(value)
        population = item.get("population_count")
        displayed = item.get("displayed_count")
        if isinstance(population, (int, float)) and population < 0:
            errors.append(f"Negative population count for {company}")
        if isinstance(displayed, (int, float)) and displayed < 0:
            errors.append(f"Negative displayed count for {company}")
    return errors


def build(data: Any) -> str:
    errors = validate(data)
    if errors:
        raise ValueError("Data validation failed:\n- " + "\n- ".join(errors))
    title = text(get(data, "TITLE", "Technology intelligence briefing"))
    time_range = text(get(data, "TIME_RANGE", "Not specified"))
    cutoff = text(get(data, "EVIDENCE_CUTOFF", "Not specified"))
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    sections = "".join((
        render_scope(data), render_findings(data), render_trends(data), render_patents(data),
        render_literature(data), render_news(data), render_methods(data),
    ))
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title><style>{v2_css.CSS}</style></head>
<body><a class="skip-link" href="#main">Skip to report content</a>
<header class="report-header"><div class="report-kicker">Technology intelligence briefing</div>
<h1 class="report-title">{e(title)}</h1><div class="report-meta">
<span>Research period: {e(time_range)}</span><span>Evidence cutoff: {e(cutoff)}</span>
<span>Generated: {e(generated)}</span></div></header>{render_nav()}
<main id="main">{sections}</main>
<footer>Evidence-backed research support. Verify material decisions against the cited primary sources and current authoritative records.</footer>
</body></html>'''


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    output = Path(args[0]).expanduser() if args else Path.cwd() / "technology-intelligence-briefing.html"
    data_path = Path(args[1]).expanduser() if len(args) > 1 else None
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        rendered = build(load_data(data_path))
        output.write_text(rendered, encoding="utf-8")
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"report generation failed: {exc}", file=sys.stderr)
        return 2
    print(os.fspath(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

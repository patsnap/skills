#!/usr/bin/env python3
"""Render a localized competitor patent landscape as HTML or PDF.

Usage:
    python generate_report.py --data-path analysis.json --output-path report.pdf

The input JSON contract is documented in references/workflow_guide.md.
All JSON-derived values are HTML-escaped before rendering.
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate a competitor patent landscape report from JSON."
    )
    parser.add_argument(
        "--data-path",
        required=True,
        help="Path to the analysis JSON file.",
    )
    parser.add_argument(
        "--output-path",
        required=True,
        help="Requested .pdf or .html output path.",
    )
    return parser.parse_args()


def text(value: Any, default: str = "") -> str:
    """Return an escaped text representation for HTML content."""
    if value is None:
        value = default
    return html.escape(str(value), quote=True)


def integer(value: Any, default: int = 0) -> int:
    """Convert a value to an integer without propagating bad input."""
    if isinstance(value, bool):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def safe_url(value: Any) -> str | None:
    """Allow only absolute HTTP(S) links in report anchors."""
    if not isinstance(value, str):
        return None
    parsed = urlparse(value.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return None
    return html.escape(value.strip(), quote=True)


def list_value(data: dict[str, Any], key: str) -> list[Any]:
    """Return a list field or an empty list."""
    value = data.get(key, [])
    return value if isinstance(value, list) else []


def dict_value(data: dict[str, Any], key: str) -> dict[str, Any]:
    """Return a dictionary field or an empty dictionary."""
    value = data.get(key, {})
    return value if isinstance(value, dict) else {}


STYLE = """
<style>
  :root {
    --ink: #1f2933;
    --muted: #52606d;
    --accent: #245b8a;
    --line: #cbd2d9;
    --surface: #f7f9fb;
    --high: #7f1d1d;
    --moderate: #7c4a03;
    --low: #24543a;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    color: var(--ink);
    background: #fff;
    font-family: Inter, ui-sans-serif, system-ui, -apple-system,
      BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
    font-size: 14px;
    line-height: 1.55;
  }
  header, main, footer {
    width: min(1120px, calc(100% - 40px));
    margin-inline: auto;
  }
  header { padding: 36px 0 18px; border-bottom: 2px solid var(--accent); }
  main { padding: 8px 0 40px; }
  footer { padding: 16px 0 32px; border-top: 1px solid var(--line); color: var(--muted); }
  h1 { margin: 0 0 12px; font-size: 28px; line-height: 1.2; }
  h2 { margin: 34px 0 12px; font-size: 21px; color: var(--accent); }
  h3 { margin: 22px 0 8px; font-size: 16px; }
  p { margin: 8px 0; }
  .metadata { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px 18px; }
  .metadata div { border-top: 1px solid var(--line); padding-top: 6px; }
  .label { display: block; color: var(--muted); font-size: 12px; }
  .summary, .warning {
    margin: 16px 0;
    padding: 14px 16px;
    border-left: 4px solid var(--accent);
    background: var(--surface);
  }
  .warning { border-left-color: var(--moderate); }
  .table-wrap { overflow-x: auto; margin: 12px 0; }
  table { width: 100%; border-collapse: collapse; }
  caption { padding: 0 0 8px; text-align: left; color: var(--muted); }
  th, td { border: 1px solid var(--line); padding: 8px 10px; text-align: left; vertical-align: top; }
  th { background: #eaf0f5; font-weight: 650; }
  .density-high { border-left: 4px solid var(--high); }
  .density-moderate { border-left: 4px solid var(--moderate); }
  .density-low { border-left: 4px solid var(--low); }
  .status { font-weight: 650; }
  a { color: #174f7a; text-decoration-thickness: 1px; text-underline-offset: 2px; }
  code { overflow-wrap: anywhere; }
  @media (max-width: 720px) {
    header, main, footer { width: min(100% - 24px, 1120px); }
    .metadata { grid-template-columns: 1fr; }
    th, td { min-width: 130px; }
  }
  @media print {
    body { font-size: 10pt; }
    header, main, footer { width: 100%; }
    a { color: inherit; }
    tr { break-inside: avoid; }
    h2, h3 { break-after: avoid; }
  }
</style>
"""


def density(count: int, maximum: int) -> tuple[str, str]:
    """Return a text-plus-style density classification."""
    if maximum <= 0:
        return "No observed records", "density-low"
    ratio = count / maximum
    if ratio >= 0.60:
        return "High observed density", "density-high"
    if ratio >= 0.30:
        return "Moderate observed density", "density-moderate"
    return "Low observed density", "density-low"


def render_source(source: Any) -> str:
    """Render one source entry from a string or object."""
    if isinstance(source, dict):
        label = text(source.get("label"), "Source")
        accessed = text(source.get("accessed"), "date not supplied")
        url = safe_url(source.get("url"))
        label_html = f'<a href="{url}">{label}</a>' if url else label
        return f"<li>{label_html}; accessed {accessed}</li>"
    return f"<li>{text(source)}</li>"


def render_html(data: dict[str, Any]) -> str:
    """Render one complete, self-contained HTML report."""
    competitor = text(data.get("competitor"), "Competitor not supplied")
    technology = text(data.get("technology"), "Technology not supplied")
    market_scope = ", ".join(text(item) for item in list_value(data, "market_scope")) or "Not supplied"
    total_patents = integer(data.get("total_patents"))
    counting_unit = text(data.get("counting_unit"), "Not supplied")
    date_basis = text(data.get("date_basis"), "Not supplied")
    date_from = text(data.get("date_from"), "Not supplied")
    date_to = text(data.get("date_to"), "Not supplied")
    retrieved_at = text(data.get("retrieved_at"), datetime.now(timezone.utc).isoformat())
    query = text(data.get("search_query"), "Not supplied")
    sample_limit = text(data.get("sample_limit"), "Not supplied")

    framework_rows = []
    for index, item in enumerate(list_value(data, "tech_framework"), start=1):
        record = item if isinstance(item, dict) else {}
        framework_rows.append(
            "<tr>"
            f"<td>{index}</td>"
            f"<td>{text(record.get('name'))}</td>"
            f"<td>{text(record.get('description'))}</td>"
            "</tr>"
        )

    market_rows = []
    market_distribution = dict_value(data, "market_distribution")
    sorted_markets = sorted(
        market_distribution.items(),
        key=lambda pair: integer(pair[1]),
        reverse=True,
    )
    for market, count in sorted_markets:
        market_rows.append(
            f"<tr><td>{text(market)}</td><td>{integer(count)}</td></tr>"
        )

    patent_rows = []
    top_patents = list_value(data, "top_patents")
    for item in top_patents:
        patent = item if isinstance(item, dict) else {}
        publication_number = text(patent.get("publication_number"), "Not supplied")
        patent_url = safe_url(patent.get("patent_url"))
        number_html = (
            f'<a href="{patent_url}">{publication_number}</a>'
            if patent_url
            else publication_number
        )
        patent_rows.append(
            "<tr>"
            f"<td>{text(patent.get('title'))}</td>"
            f"<td>{number_html}</td>"
            f"<td>{integer(patent.get('family_size'))}</td>"
            f"<td>{text(patent.get('legal_status'), 'Unverified')}</td>"
            f"<td>{text(patent.get('status_date'), 'Not supplied')}</td>"
            f"<td>{text(patent.get('tech_sub_area'))}</td>"
            f"<td>{text(patent.get('layout_type'), 'Unclassified')}</td>"
            f"<td>{text(patent.get('claim_summary'))}</td>"
            f"<td>{text(patent.get('selection_reason'))}</td>"
            "</tr>"
        )

    subareas = [item for item in list_value(data, "sub_area_heatmap") if isinstance(item, dict)]
    maximum = max((integer(item.get("count")) for item in subareas), default=0)
    heat_rows = []
    for item in subareas:
        count = integer(item.get("count"))
        label, css_class = density(count, maximum)
        heat_rows.append(
            "<tr>"
            f"<td>{text(item.get('name'))}</td>"
            f'<td class="{css_class}"><span class="status">{label}</span>: {count}</td>'
            f"<td>{integer(item.get('core_count'))}</td>"
            f"<td>{integer(item.get('periph_count'))}</td>"
            "</tr>"
        )

    suggestions = "".join(f"<li>{text(item)}</li>" for item in list_value(data, "suggestions"))
    limitations = "".join(f"<li>{text(item)}</li>" for item in list_value(data, "limitations"))
    sources = "".join(render_source(item) for item in list_value(data, "sources"))
    product_map = dict_value(data, "product_map")

    low_data_warning = ""
    if total_patents < 10:
        low_data_warning = (
            '<div class="warning"><strong>Coverage warning:</strong> '
            "Fewer than ten records were retrieved. Review entity coverage, query scope, "
            "classifications, languages, jurisdictions, and the result cap before drawing conclusions."
            "</div>"
        )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{competitor} — {technology} patent landscape</title>
  {STYLE}
</head>
<body>
<header>
  <h1>Competitor patent landscape</h1>
  <p>{competitor} — {technology}</p>
  <div class="metadata">
    <div><span class="label">Jurisdictions</span>{market_scope}</div>
    <div><span class="label">Observed records</span>{total_patents} ({counting_unit})</div>
    <div><span class="label">Date basis</span>{date_basis}</div>
    <div><span class="label">Period</span>{date_from} to {date_to}</div>
    <div><span class="label">Retrieved</span>{retrieved_at}</div>
    <div><span class="label">Sample limit</span>{sample_limit}</div>
  </div>
</header>
<main>
  {low_data_warning}
  <section aria-labelledby="summary-heading">
    <h2 id="summary-heading">1. Executive summary</h2>
    <div class="summary">{text(data.get('exec_summary'), 'No executive summary supplied.')}</div>
  </section>
  <section aria-labelledby="framework-heading">
    <h2 id="framework-heading">2. Technical framework</h2>
    <div class="table-wrap"><table>
      <caption>Technical subareas used to classify the retrieved portfolio.</caption>
      <thead><tr><th>#</th><th>Subarea</th><th>Definition</th></tr></thead>
      <tbody>{''.join(framework_rows)}</tbody>
    </table></div>
  </section>
  <section aria-labelledby="market-heading">
    <h2 id="market-heading">3. Filing-jurisdiction distribution</h2>
    <div class="table-wrap"><table>
      <caption>Observed distribution; interpret under the stated counting unit and date basis.</caption>
      <thead><tr><th>Office or jurisdiction</th><th>Count</th></tr></thead>
      <tbody>{''.join(market_rows)}</tbody>
    </table></div>
  </section>
  <section aria-labelledby="patents-heading">
    <h2 id="patents-heading">4. Representative patents</h2>
    <div class="table-wrap"><table>
      <caption>Selected through a multi-factor review; family size is not a standalone importance score.</caption>
      <thead><tr><th>Title</th><th>Publication</th><th>Simple family</th><th>Status</th><th>Status date</th><th>Subarea</th><th>Portfolio role</th><th>Claim focus</th><th>Selection reason</th></tr></thead>
      <tbody>{''.join(patent_rows)}</tbody>
    </table></div>
  </section>
  <section aria-labelledby="architecture-heading">
    <h2 id="architecture-heading">5. Core and peripheral hypotheses</h2>
    <h3>Core architecture</h3>
    <p>{text(data.get('core_analysis'), 'Not analyzed.')}</p>
    <h3>Peripheral architecture</h3>
    <p>{text(data.get('periph_analysis'), 'Not analyzed.')}</p>
  </section>
  <section aria-labelledby="density-heading">
    <h2 id="density-heading">6. Technical-subarea activity</h2>
    <div class="table-wrap"><table>
      <caption>Relative observed density within this dataset; low density does not establish white space.</caption>
      <thead><tr><th>Subarea</th><th>Observed density and count</th><th>Core hypotheses</th><th>Peripheral hypotheses</th></tr></thead>
      <tbody>{''.join(heat_rows)}</tbody>
    </table></div>
  </section>
  <section aria-labelledby="product-heading">
    <h2 id="product-heading">7. Product-feature mapping</h2>
    <p><strong>Provenance:</strong> {text(product_map.get('provenance'), 'No product map supplied.')}</p>
    <p>{text(product_map.get('description'), 'No accessible description supplied.')}</p>
  </section>
  <section aria-labelledby="actions-heading">
    <h2 id="actions-heading">8. R&amp;D and IP actions</h2>
    <ul>{suggestions}</ul>
  </section>
  <section aria-labelledby="method-heading">
    <h2 id="method-heading">9. Evidence and methodology</h2>
    <p><strong>Recorded query:</strong> <code>{query}</code></p>
    <h3>Sources</h3><ul>{sources}</ul>
    <h3>Limitations</h3><ul>{limitations}</ul>
  </section>
</main>
<footer>
  Generated from user-supplied and retrieved analysis data. This report supports research and strategy;
  it is not a legal opinion or freedom-to-operate conclusion.
</footer>
</body>
</html>"""


def write_report(html_content: str, output_path: Path) -> Path:
    """Write HTML directly or attempt PDF with an explicit HTML fallback."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix.lower() == ".html":
        output_path.write_text(html_content, encoding="utf-8")
        return output_path

    requested_pdf = output_path.with_suffix(".pdf")
    try:
        from weasyprint import HTML

        HTML(string=html_content).write_pdf(str(requested_pdf))
        return requested_pdf
    except Exception as exc:  # Conversion can fail for native-library reasons.
        fallback = output_path.with_suffix(".html")
        fallback.write_text(html_content, encoding="utf-8")
        print(
            f"[WARNING] PDF conversion failed ({type(exc).__name__}); wrote HTML fallback.",
            file=sys.stderr,
        )
        return fallback


def load_data(path: Path) -> dict[str, Any]:
    """Load and minimally validate the analysis JSON object."""
    if not path.is_file():
        raise FileNotFoundError(f"Data file does not exist: {path}")
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("The analysis JSON root must be an object.")
    return data


def main() -> int:
    """Run the command-line renderer."""
    args = parse_args()
    try:
        data = load_data(Path(args.data_path))
        html_content = render_html(data)
        actual_path = write_report(html_content, Path(args.output_path))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1
    print(f"[OK] Report generated: {actual_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Stage 7: render safe, static, responsive English HTML from final_records.json."""

from __future__ import annotations

import argparse
import datetime as dt
import html
import pathlib
from collections import Counter
from typing import Any
from urllib.parse import urlparse

from hv_common import jload, require_checkpoint


def esc(value: Any) -> str:
    if value is None or value == "":
        return "Not available"
    return html.escape(str(value), quote=True)


def safe_url(value: Any) -> str | None:
    text = str(value or "").strip()
    parsed = urlparse(text)
    return text if parsed.scheme.lower() in {"http", "https"} and parsed.netloc else None


def link(label: Any, url: Any, *, title: str = "Open source record") -> str:
    href = safe_url(url)
    if not href:
        return esc(label)
    return f'<a href="{html.escape(href, quote=True)}" target="_blank" rel="noopener noreferrer" title="{html.escape(title, quote=True)}">{esc(label)}</a>'


def state_value(value: Any, state: Any) -> str:
    label = str(state or "not_run").replace("_", " ").title()
    return f"{esc(value)} <span class=\"state\">{esc(label)}</span>"


def event_summary(record: dict[str, Any]) -> str:
    categories = record.get("legal_event_categories") or []
    if not categories:
        checked = record.get("legal_event_evidence") or {}
        complete = checked and all((detail or {}).get("state") in {"available", "empty"} for detail in checked.values())
        return "No event records returned in all checked categories" if complete else "Incomplete event evidence"
    pieces = []
    evidence = record.get("legal_event_evidence") or {}
    for category in categories:
        detail = evidence.get(category) or {}
        pieces.append(f"{category} ({int(detail.get('count') or 0)})")
    return "; ".join(pieces)


def image_cell(record: dict[str, Any]) -> str:
    url = safe_url(record.get("drawing"))
    if not url:
        return f'<span class="state">{esc(str(record.get("drawing_state") or "not_run").replace("_", " ").title())}</span>'
    alt = f"Abstract drawing for {record.get('pn') or 'selected patent'}"
    return f'<a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener noreferrer"><img src="{html.escape(url, quote=True)}" alt="{html.escape(alt, quote=True)}" loading="lazy" referrerpolicy="no-referrer"></a>'


def score_components(record: dict[str, Any]) -> str:
    component = record.get("score_components") or {}
    return (
        f"Citations {esc(component.get('forward_citations'))}/30 · "
        f"Family {esc(component.get('family_size'))}/30 · "
        f"Inventor {esc(component.get('core_inventor'))}/20 · "
        f"Events {esc(component.get('legal_event_activity'))}/20"
    )


def row(record: dict[str, Any]) -> str:
    patent_label = record.get("pn") or record.get("patent_id") or "Identifier unavailable"
    gaps = record.get("gaps") or []
    matched = record.get("matched_inventors") or []
    inventor = "Yes — " + ", ".join(str(item) for item in matched) if record.get("core_inventor") else "No"
    return f"""
<tr>
  <td>{esc(record.get('rank'))}</td>
  <td><strong>{esc(record.get('score'))}</strong><span class="secondary">{score_components(record)}</span></td>
  <td class="wide">{esc(record.get('rationale'))}</td>
  <td>{link(patent_label, record.get('record_url'), title='Open verified global patent record')}</td>
  <td class="wide"><strong>{esc(record.get('title'))}</strong><span class="secondary">{esc(record.get('authority'))}</span></td>
  <td>{image_cell(record)}</td>
  <td>{esc(record.get('current_assignee'))}</td>
  <td>{state_value(record.get('legal_status'), record.get('legal_status_state'))}</td>
  <td>{esc(record.get('patsnap_title'))}</td>
  <td class="wide">{esc(record.get('tech_problem'))}</td>
  <td class="wide">{esc(record.get('tech_approach'))}</td>
  <td class="wide">{esc(record.get('benefit'))}</td>
  <td>{state_value(record.get('cited_by_simple_family'), record.get('citation_state'))}<span class="secondary">P{esc(record.get('citation_percentile'))}</span></td>
  <td>{state_value(record.get('simple_family_count'), record.get('simple_family_state'))}<span class="secondary">P{esc(record.get('family_percentile'))}</span></td>
  <td>{esc(inventor)}</td>
  <td>{esc(event_summary(record))}</td>
  <td class="wide">{esc('; '.join(str(item) for item in gaps) if gaps else 'None recorded')}</td>
</tr>"""


def list_items(values: list[Any], fallback: str) -> str:
    if not values:
        return f"<li>{esc(fallback)}</li>"
    return "".join(f"<li>{esc(value)}</li>" for value in values)


def render(data: dict[str, Any], output: pathlib.Path) -> None:
    meta = data.get("meta") if isinstance(data.get("meta"), dict) else {}
    selected = [item for item in data.get("selected", []) if isinstance(item, dict)]
    errors = data.get("errors") or []
    inventors = meta.get("top5_inventors") or []
    limitations = meta.get("limitations") or []
    gap_counter: Counter[str] = Counter()
    event_counter: Counter[str] = Counter()
    for record in selected:
        gap_counter.update(str(item) for item in record.get("gaps") or [])
        event_counter.update(str(item) for item in record.get("legal_event_categories") or [])
    generated = data.get("generated_at") or dt.datetime.now(dt.timezone.utc).isoformat()
    inventor_rows = "".join(
        f"<tr><td>{index}</td><td>{esc(item.get('name'))}</td><td>{esc(item.get('candidate_patent_count'))}</td></tr>"
        for index, item in enumerate(inventors, start=1)
        if isinstance(item, dict)
    ) or '<tr><td colspan="3">No inventor ranking available.</td></tr>'
    selected_rows = "".join(row(record) for record in selected) or '<tr><td colspan="17">No patents were selected because the candidate universe was empty.</td></tr>'
    error_items = [str(item.get("message") or item) if isinstance(item, dict) else str(item) for item in errors]
    gap_items = [f"{label} ({count} selected records)" for label, count in gap_counter.most_common()]
    event_items = [f"{label}: {count} selected records" for label, count in event_counter.most_common()]
    query_text = meta.get("query_text") or "Not retained in this checkpoint"
    markup = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>High-Value Patent Portfolio Screening</title>
<style>
:root{{--navy:#17324d;--teal:#246b84;--ink:#273746;--muted:#5d6c78;--line:#cbd5dc;--wash:#eef3f5;--paper:#fff;--bg:#f4f6f7}}
*{{box-sizing:border-box}} html{{scroll-behavior:smooth}} body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 Arial,Helvetica,sans-serif}}
a{{color:#185d78;text-decoration-thickness:.08em;text-underline-offset:.16em}} a:focus-visible{{outline:3px solid #c57a19;outline-offset:2px}}
header{{background:var(--navy);color:#fff;border-bottom:5px solid var(--teal)}} .hero{{max-width:1440px;margin:auto;padding:44px 32px 36px}}
.eyebrow{{font-size:.76rem;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#c9dce5}} h1{{font-size:clamp(2rem,4vw,3.45rem);line-height:1.05;margin:.4rem 0 1rem;max-width:980px}}
.subtitle{{max-width:950px;color:#e5edf1;font-size:1.03rem}} main{{max-width:1440px;margin:auto;padding:28px 32px 60px}}
nav{{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 24px}} nav a{{background:#fff;border:1px solid var(--line);padding:7px 10px;border-radius:3px;text-decoration:none;font-size:.85rem}}
section{{background:var(--paper);border:1px solid var(--line);border-left:4px solid var(--teal);padding:24px;margin:0 0 20px;box-shadow:0 2px 10px rgba(23,50,77,.05)}}
h2{{color:var(--navy);font-size:1.35rem;margin:0 0 15px}} h3{{font-size:1rem;color:var(--teal);margin:20px 0 8px}} p{{margin:.45rem 0 1rem}}
.metrics{{display:grid;grid-template-columns:repeat(5,minmax(140px,1fr));gap:10px}} .metric{{background:var(--wash);border-top:3px solid var(--teal);padding:14px}}
.metric span{{display:block;font-size:.76rem;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}} .metric strong{{font-size:1.35rem;color:var(--navy)}}
.notice{{background:#f7f4ed;border:1px solid #d8c59d;border-left:4px solid #9b6a16;padding:14px 16px;margin:14px 0}}
.table-wrap{{overflow-x:auto;border:1px solid var(--line)}} table{{border-collapse:collapse;width:100%;min-width:2450px}} .compact{{min-width:520px}}
caption{{text-align:left;font-weight:700;padding:10px;background:var(--wash);color:var(--navy)}} th{{background:var(--navy);color:#fff;text-align:left;vertical-align:bottom;font-size:.78rem;padding:9px;border:1px solid #40576d}}
td{{vertical-align:top;padding:9px;border:1px solid var(--line);font-size:.78rem;max-width:260px;overflow-wrap:anywhere}} tbody tr:nth-child(even){{background:#f7f9fa}} td.wide{{min-width:230px}}
td img{{display:block;width:120px;height:90px;object-fit:contain;background:#fff;border:1px solid var(--line)}} .state{{display:inline-block;margin-top:4px;padding:2px 5px;border:1px solid #9aabb5;background:#fff;font-size:.68rem;text-transform:uppercase;letter-spacing:.03em}}
.secondary{{display:block;color:var(--muted);font-size:.7rem;margin-top:4px}} code{{white-space:pre-wrap;overflow-wrap:anywhere;background:var(--wash);padding:.15em .3em}}
footer{{max-width:1440px;margin:auto;padding:0 32px 40px;color:var(--muted);font-size:.78rem}}
@media(max-width:900px){{.hero,main,footer{{padding-left:18px;padding-right:18px}}.metrics{{grid-template-columns:repeat(2,1fr)}}section{{padding:18px}}}}
@media(max-width:480px){{.metrics{{grid-template-columns:1fr}}h1{{font-size:2rem}}}}
@page{{size:Letter landscape;margin:.45in}} @media print{{body{{background:#fff;font-size:9pt}}header{{background:#fff;color:#000;border-bottom:2px solid #000}}.hero,main,footer{{max-width:none;padding-left:0;padding-right:0}}.subtitle,.eyebrow{{color:#333}}nav{{display:none}}section{{box-shadow:none;border:1px solid #777;break-inside:avoid}}.table-wrap{{overflow:visible}}table{{min-width:0;font-size:6.2pt}}th{{background:#e7ecef;color:#000}}td{{font-size:6.2pt;padding:4px}}a{{color:#000;text-decoration:none}}}}
@media(prefers-reduced-motion:reduce){{*{{scroll-behavior:auto!important}}}}
</style>
</head>
<body>
<header><div class="hero"><div class="eyebrow">Patent portfolio screening · evidence trace</div><h1>High-Value Patent Portfolio Screening</h1><p class="subtitle">A transparent ranking of one documented PatSnap candidate universe. Scores are screening signals—not monetary values, legal opinions, or conclusions on validity or enforceability.</p></div></header>
<main>
<nav aria-label="Report sections"><a href="#summary">Summary</a><a href="#method">Method</a><a href="#inventors">Inventors</a><a href="#portfolio">Selected portfolio</a><a href="#quality">Evidence quality</a><a href="#provenance">Provenance</a></nav>
<section id="summary"><h2>1. Screening summary</h2><div class="metrics">
<div class="metric"><span>P002 reported</span><strong>{esc(meta.get('p002_reported_total'))}</strong></div><div class="metric"><span>Retrieved</span><strong>{esc(meta.get('retrieved_count'))}</strong></div><div class="metric"><span>Deduplicated</span><strong>{esc(meta.get('deduplicated_count'))}</strong></div><div class="metric"><span>Selected</span><strong>{esc(meta.get('selected_count'))}</strong></div><div class="metric"><span>Selection ratio</span><strong>{esc(meta.get('ratio'))}%</strong></div>
</div><div class="notice"><strong>Interpretation boundary.</strong> This report ranks patents only within the stated query result. Citation, family, inventor, and legal-event signals require contextual review. A legal-event hit can be favorable, adverse, neutral, historical, or irrelevant.</div></section>
<section id="method"><h2>2. Query and method</h2><h3>Reviewed query</h3><code>{esc(query_text)}</code><p class="secondary">Query SHA-256: {esc(meta.get('query_sha256'))} · Source mode: {esc(meta.get('source_mode'))} · Run ID: {esc(meta.get('run_id'))}</p>
<div class="table-wrap"><table class="compact"><caption>100-point screening model</caption><thead><tr><th>Indicator</th><th>Weight</th><th>Interpretation</th></tr></thead><tbody><tr><td>Simple-family forward-citation position</td><td>30</td><td>Candidate-set relative and age/field/office dependent.</td></tr><tr><td>Simple-family size position</td><td>30</td><td>Family breadth, not market coverage or enforceability.</td></tr><tr><td>Core-inventor membership</td><td>20</td><td>Exact-name concentration within this candidate universe.</td></tr><tr><td>Verified legal-event activity</td><td>20</td><td>Activity presence, not positive value.</td></tr></tbody></table></div></section>
<section id="inventors"><h2>3. Core-inventor calculation</h2><div class="table-wrap"><table class="compact"><caption>Top exact-returned inventor names</caption><thead><tr><th>Rank</th><th>Inventor</th><th>Candidate patents</th></tr></thead><tbody>{inventor_rows}</tbody></table></div><p class="secondary">Western commas remain inside one inventor name. Transliteration variants and homonyms are not merged automatically.</p></section>
<section id="portfolio"><h2>4. Selected patent portfolio ({len(selected)} records)</h2><p>Publication identifiers remain plain text when no verified stable PatSnap global record URL is configured. This avoids publishing a guessed or China-only product deep link.</p><div class="table-wrap"><table><caption>Selected records and evidence</caption><thead><tr><th>Rank</th><th>Score</th><th>Selection rationale</th><th>Publication</th><th>Original title</th><th>Abstract drawing</th><th>Current assignee</th><th>Simple legal status</th><th>PatSnap title</th><th>Technical problem</th><th>Technical approach</th><th>Benefit/effect</th><th>Forward citations</th><th>Family size</th><th>Core inventor</th><th>Event activity</th><th>Data gaps</th></tr></thead><tbody>{selected_rows}</tbody></table></div></section>
<section id="quality"><h2>5. Evidence quality and unresolved gaps</h2><h3>Selected-record gaps</h3><ul>{list_items(gap_items, 'No selected-record gap was recorded; reviewer confirmation remains required.')}</ul><h3>Selected-record event categories</h3><ul>{list_items(event_items, 'No verified event activity was recorded in selected records.')}</ul><h3>Pipeline errors</h3><ul>{list_items(error_items, 'No pipeline error was recorded.')}</ul></section>
<section id="provenance"><h2>6. Provenance, limitations, and review</h2><p>Generated: {esc(generated)} · Schema: {esc(data.get('schema_version'))}</p><ul>{list_items(limitations, 'No limitation text supplied.')}</ul><div class="notice"><strong>Required review.</strong> Confirm query scope, entity normalization, family convention, metric coverage, missing values, event meaning, selected-record narratives, and any commercial or legal use before distribution.</div></section>
</main><footer>PatSnap-assisted research screening · static HTML · no embedded scripts · report data must be retained with its JSON trace.</footer>
</body></html>"""
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markup, encoding="utf-8")
    print(f"Wrote HTML report to {output}.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the required high-value patent screening HTML report.")
    parser.add_argument("--input", default="final_records.json")
    parser.add_argument("--output", default="high_value_patent_portfolio_screening.html")
    args = parser.parse_args()
    data = require_checkpoint(jload(args.input), keys=("meta", "selected"), filename=args.input)
    render(data, pathlib.Path(args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

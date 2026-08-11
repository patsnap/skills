#!/usr/bin/env python3
"""Build research instructions or render reviewed inventor-mobility signal data.

This script does not search patents itself and does not infer resignation or
employment. ``prompt`` creates a scoped research protocol. ``report`` validates
reviewed JSON and produces an escaped, self-contained HTML briefing.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from collections import Counter
from datetime import date, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


LEVELS = ("priority_review", "review", "watch", "insufficient_evidence")
LEVEL_LABELS = {
    "priority_review": "Priority review",
    "review": "Review",
    "watch": "Watch",
    "insufficient_evidence": "Insufficient evidence",
}
LEVEL_COLORS = {
    "priority_review": "#B42318",
    "review": "#B54708",
    "watch": "#175CD3",
    "insufficient_evidence": "#475467",
}
IDENTITY_LEVELS = ("resolved", "probable", "ambiguous", "unresolved")


def parse_iso_date(value: Any, field: str, errors: list[str]) -> date | None:
    if not isinstance(value, str):
        errors.append(f"{field} must be an ISO date string")
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        errors.append(f"{field} must use YYYY-MM-DD")
        return None


def nonempty(value: Any, field: str, errors: list[str]) -> str:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{field} must be a non-empty string")
        return ""
    return value.strip()


def validate_url(value: Any, field: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{field} must be a non-empty URL")
        return
    parsed = urlparse(value)
    if parsed.scheme not in {"https", "http"} or not parsed.netloc:
        errors.append(f"{field} must be an absolute HTTP(S) URL")


def validate_patent(record: Any, field: str, errors: list[str]) -> None:
    if not isinstance(record, dict):
        errors.append(f"{field} must be an object")
        return
    for key in ("publication_number", "title", "applicant", "relevant_date", "technical_relevance"):
        nonempty(record.get(key), f"{field}.{key}", errors)
    validate_url(record.get("url"), f"{field}.url", errors)


def validate_report_data(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    nonempty(data.get("company"), "company", errors)
    report_date = parse_iso_date(data.get("report_date"), "report_date", errors)
    monitor_start = parse_iso_date(data.get("monitor_start"), "monitor_start", errors)
    monitor_end = parse_iso_date(data.get("monitor_end"), "monitor_end", errors)
    if monitor_start and monitor_end and monitor_start > monitor_end:
        errors.append("monitor_start must not be after monitor_end")
    if report_date and monitor_end and report_date < monitor_end:
        errors.append("report_date must not be before monitor_end")

    methodology = data.get("methodology")
    if not isinstance(methodology, dict):
        errors.append("methodology must be an object")
    else:
        parse_iso_date(methodology.get("cutoff_date"), "methodology.cutoff_date", errors)
        for key in ("counting_unit", "coverage", "identity_policy", "rating_policy"):
            nonempty(methodology.get(key), f"methodology.{key}", errors)
        limitations = methodology.get("limitations", [])
        if not isinstance(limitations, list) or any(not isinstance(item, str) for item in limitations):
            errors.append("methodology.limitations must be an array of strings")

    inventors = data.get("inventors")
    if not isinstance(inventors, list):
        errors.append("inventors must be an array")
        inventors = []
    for index, inventor in enumerate(inventors):
        prefix = f"inventors[{index}]"
        if not isinstance(inventor, dict):
            errors.append(f"{prefix} must be an object")
            continue
        nonempty(inventor.get("display_name"), f"{prefix}.display_name", errors)
        identity = inventor.get("identity_status")
        if identity not in IDENTITY_LEVELS:
            errors.append(f"{prefix}.identity_status must be one of {IDENTITY_LEVELS}")
        level = inventor.get("signal_level")
        if level not in LEVELS:
            errors.append(f"{prefix}.signal_level must be one of {LEVELS}")
        if identity in {"ambiguous", "unresolved"} and level in {"priority_review", "review"}:
            errors.append(
                f"{prefix} cannot receive {level!r} while identity_status is {identity!r}"
            )
        nonempty(inventor.get("rationale"), f"{prefix}.rationale", errors)
        for key in ("source_org_patents", "later_patents"):
            records = inventor.get(key)
            if not isinstance(records, list):
                errors.append(f"{prefix}.{key} must be an array")
                continue
            for record_index, record in enumerate(records):
                validate_patent(record, f"{prefix}.{key}[{record_index}]", errors)

    supplied_summary = data.get("summary")
    if not isinstance(supplied_summary, dict):
        errors.append("summary must be an object")
    else:
        computed = Counter(
            inventor.get("signal_level")
            for inventor in inventors
            if isinstance(inventor, dict) and inventor.get("signal_level") in LEVELS
        )
        for level in LEVELS:
            value = supplied_summary.get(level)
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                errors.append(f"summary.{level} must be a non-negative integer")
            elif value != computed[level]:
                errors.append(
                    f"summary.{level}={value} does not match inventor records ({computed[level]})"
                )
    return errors


def escape(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        value = "; ".join(str(item) for item in value)
    return html.escape(str(value), quote=True)


def safe_link(url: Any, label: Any) -> str:
    raw = str(url or "")
    parsed = urlparse(raw)
    escaped_label = escape(label)
    if parsed.scheme not in {"https", "http"} or not parsed.netloc:
        return escaped_label
    return f'<a href="{escape(raw)}" target="_blank" rel="noopener noreferrer">{escaped_label}</a>'


def patent_table(records: list[dict[str, Any]], caption: str) -> str:
    if not records:
        return f'<p class="empty">No reviewed public records in this section.</p>'
    rows = []
    for record in records:
        rows.append(
            "<tr>"
            f"<td>{safe_link(record.get('url'), record.get('publication_number'))}</td>"
            f"<td>{escape(record.get('title'))}</td>"
            f"<td>{escape(record.get('applicant'))}</td>"
            f"<td>{escape(record.get('relevant_date'))}</td>"
            f"<td>{escape(record.get('technical_relevance'))}</td>"
            "</tr>"
        )
    return (
        f'<table><caption>{escape(caption)}</caption><thead><tr>'
        "<th>Publication</th><th>Title</th><th>Applicant</th><th>Relevant date</th>"
        "<th>Technical relevance and limits</th></tr></thead><tbody>"
        + "".join(rows)
        + "</tbody></table>"
    )


def inventor_section(inventor: dict[str, Any]) -> str:
    level = inventor["signal_level"]
    observed = inventor.get("observed_organizations", [])
    organizations = escape(observed) if observed else "Not reported"
    return f"""
    <article class="person-card" aria-labelledby="person-{escape(inventor['display_name'])}">
      <header class="person-header">
        <div>
          <h3 id="person-{escape(inventor['display_name'])}">{escape(inventor['display_name'])}</h3>
          <p>Identity status: <strong>{escape(inventor['identity_status'])}</strong></p>
        </div>
        <span class="badge" style="--badge:{LEVEL_COLORS[level]}">{LEVEL_LABELS[level]}</span>
      </header>
      <dl>
        <dt>Organizations observed in reviewed patent records</dt><dd>{organizations}</dd>
        <dt>Rationale</dt><dd>{escape(inventor['rationale'])}</dd>
        <dt>Counterevidence / uncertainty</dt><dd>{escape(inventor.get('counterevidence')) or 'Not reported'}</dd>
        <dt>Recommended qualified review</dt><dd>{escape(inventor.get('recommended_review')) or 'Not reported'}</dd>
      </dl>
      {patent_table(inventor.get('source_org_patents', []), 'Reviewed focal-organization records')}
      {patent_table(inventor.get('later_patents', []), 'Reviewed later public records')}
    </article>
    """


def generate_html_report(data: dict[str, Any], output_path: str | Path) -> Path:
    output = Path(output_path)
    summary = Counter(inventor["signal_level"] for inventor in data["inventors"])
    cards = "".join(
        f"""<section class="metric"><strong>{summary[level]}</strong><span>{LEVEL_LABELS[level]}</span></section>"""
        for level in LEVELS
    )
    people = "".join(inventor_section(inventor) for inventor in data["inventors"])
    if not people:
        people = '<p class="empty">No inventor records were supplied for review.</p>'
    method = data["methodology"]
    limitations = "".join(f"<li>{escape(item)}</li>" for item in method.get("limitations", []))

    document = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Inventor mobility signals — {escape(data['company'])}</title>
  <style>
    :root{{--ink:#101828;--muted:#475467;--line:#D0D5DD;--paper:#FFFFFF;--wash:#F8FAFC;--accent:#175CD3}}
    *{{box-sizing:border-box}} body{{margin:0;background:var(--wash);color:var(--ink);font:15px/1.55 Arial,Helvetica,sans-serif}}
    main{{max-width:1180px;margin:auto;padding:42px 24px 72px}} a{{color:#175CD3}} h1{{font-size:34px;line-height:1.15;margin:0 0 10px}}
    h2{{margin-top:38px;border-bottom:1px solid var(--line);padding-bottom:8px}} h3{{margin:0;font-size:21px}}
    .eyebrow{{color:var(--accent);font-weight:700;text-transform:uppercase;letter-spacing:.08em;font-size:12px}}
    .scope{{color:var(--muted);max-width:900px}} .notice{{border-left:5px solid #B42318;background:#FEF3F2;padding:18px 20px;margin:24px 0}}
    .metrics{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:24px 0}}
    .metric{{background:var(--paper);border:1px solid var(--line);padding:18px;display:grid;gap:4px}}
    .metric strong{{font-size:28px}} .metric span{{color:var(--muted)}} .person-card{{background:var(--paper);border:1px solid var(--line);padding:24px;margin:18px 0}}
    .person-header{{display:flex;justify-content:space-between;gap:18px;align-items:flex-start}} .person-header p{{margin:4px 0;color:var(--muted)}}
    .badge{{background:var(--badge);color:#fff;padding:6px 10px;font-weight:700;font-size:12px}} dl{{display:grid;grid-template-columns:230px 1fr;gap:7px 18px}}
    dt{{font-weight:700}} dd{{margin:0}} table{{width:100%;border-collapse:collapse;margin:18px 0;font-size:13px}} caption{{text-align:left;font-weight:700;margin-bottom:6px}}
    th,td{{text-align:left;vertical-align:top;border:1px solid var(--line);padding:8px}} th{{background:#EAECF0}} .empty{{color:var(--muted);font-style:italic}}
    .method{{background:#F2F4F7;padding:20px}} footer{{margin-top:44px;color:var(--muted);font-size:12px}}
    @media(max-width:760px){{.metrics{{grid-template-columns:1fr 1fr}}dl{{grid-template-columns:1fr}}.person-header{{display:block}}table{{display:block;overflow-x:auto}}}}
    @media print{{body{{background:#fff}}main{{max-width:none;padding:0}}.person-card{{break-inside:avoid}}a{{color:inherit;text-decoration:none}}}}
  </style>
</head>
<body><main>
  <p class="eyebrow">Public patent evidence · human review required</p>
  <h1>Inventor mobility signals</h1>
  <p class="scope"><strong>Focal organization:</strong> {escape(data['company'])} · <strong>Window:</strong> {escape(data['monitor_start'])} to {escape(data['monitor_end'])} · <strong>Report date:</strong> {escape(data['report_date'])} · <strong>Technology:</strong> {escape(data.get('tech_domain')) or 'Not specified'}</p>
  <aside class="notice"><strong>Important boundary.</strong> Patent records do not establish employment, resignation, organizational movement, misconduct, confidentiality breach, ownership or legal risk. Labels below prioritize qualified review only. Recent applications may not yet be public, and same-name inventors may be different people.</aside>
  <section class="metrics" aria-label="Review priority counts">{cards}</section>
  <h2>Reviewed inventor signals</h2>{people}
  <h2>Method and limitations</h2>
  <section class="method">
    <p><strong>Cutoff:</strong> {escape(method['cutoff_date'])}</p>
    <p><strong>Counting:</strong> {escape(method['counting_unit'])}</p>
    <p><strong>Coverage:</strong> {escape(method['coverage'])}</p>
    <p><strong>Identity policy:</strong> {escape(method['identity_policy'])}</p>
    <p><strong>Rating policy:</strong> {escape(method['rating_policy'])}</p>
    <ul>{limitations or '<li>No additional limitations supplied; reviewer must confirm completeness.</li>'}</ul>
  </section>
  <footer>Generated from reviewed structured data. Restrict access and retention according to the documented purpose and applicable law.</footer>
</main></body></html>"""
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding="utf-8")
    return output


def build_monitor_prompt(
    company: str | None,
    tech_keywords: list[str],
    inventors: list[str] | None,
    inactive_years: int,
    monitor_years: int,
    as_of: date,
) -> str:
    monitor_start = as_of - timedelta(days=round(365.2425 * monitor_years))
    target = f"Focal organization: {company}" if company else "Named inventors: " + ", ".join(inventors or [])
    domain = ", ".join(tech_keywords) if tech_keywords else "Define function/mechanism scope before searching"
    return f"""# Inventor mobility signal research protocol

Execution date: {as_of.isoformat()}
Monitoring window: {monitor_start.isoformat()} to {as_of.isoformat()}
{target}
Technology seeds: {domain}
Inactivity screening lookback: {inactive_years} years (screening only; never infer departure)

## Required controls
1. Confirm legitimate purpose, authorized users, jurisdictions, access and retention.
2. Normalize organization names, family/counting unit, date fields, languages and cutoff.
3. Retrieve and paginate the focal corpus; preserve exact queries, response counts and URLs.
4. Treat filing inactivity only as a public-record signal and document publication lag.
5. Resolve identity using name variants, co-inventors, organizations, geography, technology and chronology.
6. Search later public records without assuming a different applicant is an employer.
7. Compare claim-relevant functions/mechanisms; IPC and keywords are screening features only.
8. Assign review priority, preserve counterevidence and route material questions to qualified reviewers.
9. Produce JSON conforming to references/data_schema.json; do not include unnecessary personal data.
"""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    prompt = subparsers.add_parser("prompt", help="Create an evidence-collection protocol")
    target = prompt.add_mutually_exclusive_group(required=True)
    target.add_argument("--company")
    target.add_argument("--inventors", nargs="+")
    prompt.add_argument("--tech", nargs="+", default=[])
    prompt.add_argument("--inactive-years", type=int, default=5)
    prompt.add_argument("--monitor-years", type=int, default=2)
    prompt.add_argument("--as-of", type=date.fromisoformat, default=date.today())

    report = subparsers.add_parser("report", help="Generate HTML from reviewed JSON")
    report.add_argument("--data", required=True, type=Path)
    report.add_argument("--output", required=True, type=Path)
    report.add_argument("--force", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.command == "prompt":
            if not 1 <= args.inactive_years <= 50 or not 1 <= args.monitor_years <= 50:
                raise ValueError("Year windows must be between 1 and 50")
            print(build_monitor_prompt(args.company, args.tech, args.inventors, args.inactive_years, args.monitor_years, args.as_of))
            return 0

        if args.output.suffix.lower() not in {".html", ".htm"}:
            raise ValueError("Output path must use .html or .htm")
        if args.output.exists() and not args.force:
            raise ValueError(f"Refusing to replace existing output without --force: {args.output}")
        data = json.loads(args.data.read_text(encoding="utf-8-sig"))
        if not isinstance(data, dict):
            raise ValueError("Top-level JSON value must be an object")
        errors = validate_report_data(data)
        if errors:
            raise ValueError("Input validation failed:\n- " + "\n- ".join(errors))
        generate_html_report(data, args.output)
        print(f"Generated reviewed mobility-signal briefing: {args.output}")
        return 0
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

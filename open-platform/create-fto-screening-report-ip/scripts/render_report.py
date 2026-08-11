#!/usr/bin/env python3
"""Render structured FTO-screening evidence as safe, static English HTML.

The public function preserves the source renderer contract:

    render_html_report(
        fto_result, patent_list, features, queries, title, output_path,
        claim_chart_results=None, candidates=None
    )

It also accepts a single normalized ``fto_structured_data.json`` through the
CLI. All dynamic values are escaped, evidence links are restricted to HTTP(S),
and the report uses no script or inline style attributes.

The rendered result is an FTO screening, not a legal opinion or clearance.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse


RISK_ORDER = {
    "higher": 0,
    "high": 0,
    "moderate": 1,
    "medium": 1,
    "lower": 2,
    "low": 2,
    "pending_watchlist": 3,
    "pending": 3,
    "not_assessed": 4,
    "unknown": 4,
}

RISK_LABELS = {
    "higher": "Higher screening concern",
    "high": "Higher screening concern",
    "moderate": "Moderate screening concern",
    "medium": "Moderate screening concern",
    "lower": "Lower screening concern",
    "low": "Lower screening concern",
    "pending_watchlist": "Pending watchlist",
    "pending": "Pending watchlist",
    "not_assessed": "Not assessed",
    "unknown": "Not assessed",
}


def _safe_str(value: Any, default: str = "") -> str:
    """Convert arbitrary JSON-compatible values without raising."""

    if value is None:
        return default
    if isinstance(value, (dict, list, tuple)):
        try:
            return json.dumps(value, ensure_ascii=False, sort_keys=True)
        except (TypeError, ValueError):
            return str(value)
    return str(value)


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _esc(value: Any) -> str:
    return html.escape(_safe_str(value), quote=True)


def _safe_url(value: Any) -> str:
    raw = _safe_str(value).strip()
    if not raw:
        return ""
    parsed = urlparse(raw)
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc:
        return ""
    return raw


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _first(record: dict[str, Any], *keys: str, default: Any = "") -> Any:
    for key in keys:
        value = record.get(key)
        if value is not None and value != "":
            return value
    return default


def _risk_key(record: dict[str, Any]) -> str:
    conclusion = _as_dict(record.get("conclusion"))
    raw = _first(
        conclusion,
        "screening_concern",
        default=_first(record, "screening_concern", "risk_level", "risk", default="not_assessed"),
    )
    key = re.sub(r"[^a-z]+", "_", _safe_str(raw).strip().lower()).strip("_")
    return key if key in RISK_ORDER else "not_assessed"


def _risk_label(record: dict[str, Any]) -> str:
    conclusion = _as_dict(record.get("conclusion"))
    explicit = _safe_str(conclusion.get("label")).strip()
    return explicit or RISK_LABELS[_risk_key(record)]


def _risk_badge(record: dict[str, Any]) -> str:
    key = _risk_key(record)
    return f'<span class="risk-badge risk-{_esc(key)}">{_esc(_risk_label(record))}</span>'


def _empty_row(columns: int, text: str) -> str:
    return f'<tr><td colspan="{int(columns)}" class="empty">{_esc(text)}</td></tr>'


def _list_html(values: Iterable[Any], empty_text: str) -> str:
    items = list(values)
    if not items:
        return f"<li>{_esc(empty_text)}</li>"
    rendered: list[str] = []
    for item in items:
        if isinstance(item, dict):
            text = _first(item, "text", "finding", "message", "action", "note", default=_safe_str(item))
        else:
            text = item
        rendered.append(f"<li>{_esc(text)}</li>")
    return "".join(rendered)


def _query_items(queries: Any) -> list[dict[str, Any]]:
    if isinstance(queries, dict):
        if isinstance(queries.get("queries"), list):
            return [item for item in queries["queries"] if isinstance(item, dict)]
        return [
            {"query_id": str(key), "expression": value}
            for key, value in queries.items()
            if not str(key).startswith("_")
        ]
    if isinstance(queries, list):
        return [item if isinstance(item, dict) else {"expression": item} for item in queries]
    return []


def _query_rows(queries: Any) -> str:
    rows: list[str] = []
    for index, item in enumerate(_query_items(queries), 1):
        rows.append(
            "<tr>"
            f"<td>{_esc(_first(item, 'query_id', 'id', default=f'Q-{index:03d}'))}</td>"
            f"<td><code>{_esc(_first(item, 'expression', 'query', 'query_text'))}</code></td>"
            f"<td>{_esc(_first(item, 'origin', 'source', default='Not supplied'))}</td>"
            f"<td>{_esc(_first(item, 'approval_status', 'status', default='Not supplied'))}</td>"
            f"<td>{_esc(_first(item, 'result_count', 'count', default='Not supplied'))}</td>"
            "</tr>"
        )
    return "".join(rows) or _empty_row(5, "No reviewed search expression supplied.")


def _feature_rows(features: list[dict[str, Any]]) -> str:
    rows: list[str] = []
    for index, item in enumerate(features, 1):
        evidence = _as_dict(item.get("product_evidence"))
        evidence_text = " · ".join(
            part
            for part in [
                _safe_str(_first(evidence, "reference", "source")),
                _safe_str(evidence.get("version")),
                _safe_str(evidence.get("date")),
            ]
            if part
        )
        rows.append(
            "<tr>"
            f"<td>{_esc(_first(item, 'feature_id', 'id', default=f'F-{index:03d}'))}</td>"
            f"<td>{_esc(_first(item, 'feature_group', 'group', 'category', default='Not supplied'))}</td>"
            f"<td>{_esc(_first(item, 'feature', 'text', 'description', 'technical_feature'))}</td>"
            f"<td>{_esc(_first(item, 'importance', 'essentiality', default='Not classified'))}</td>"
            f"<td>{_esc(evidence_text or _first(item, 'evidence', default='Not supplied'))}</td>"
            "</tr>"
        )
    return "".join(rows) or _empty_row(5, "No product/process feature evidence supplied.")


def _patent_identity(record: dict[str, Any]) -> str:
    return _safe_str(
        _first(
            record,
            "publication_number",
            "pn",
            "patent_number",
            "grant_number",
            "application_number",
            "patent_id",
            default="Unidentified record",
        )
    )


def _status_text(record: dict[str, Any]) -> str:
    value = record.get("legal_status")
    if isinstance(value, dict):
        status = _first(value, "normalized_status", "raw_status", "status", default="Not supplied")
        date = _first(value, "status_as_of", "date", default="")
        source = _first(value, "source", default="")
        return " · ".join(_safe_str(item) for item in (status, date, source) if item not in {None, ""})
    return _safe_str(_first(record, "status", "simple_legal_status", default="Not supplied"))


def _candidate_rows(records: list[dict[str, Any]]) -> str:
    rows: list[str] = []
    for item in sorted(records, key=lambda value: (RISK_ORDER[_risk_key(value)], _patent_identity(value))):
        url = _safe_url(_first(item, "source_url", "url", "patent_url"))
        identity = _patent_identity(item)
        identity_html = f'<a href="{_esc(url)}" rel="noopener noreferrer">{_esc(identity)}</a>' if url else _esc(identity)
        conclusion = _as_dict(item.get("conclusion"))
        basis = _first(conclusion, "basis", default=_first(item, "finding", "analysis", "conclusion", default="Not assessed"))
        confidence = _first(conclusion, "confidence", default=_first(item, "confidence", default="Not supplied"))
        rows.append(
            "<tr>"
            f"<td>{identity_html}</td>"
            f"<td>{_esc(_first(item, 'title', default='Not supplied'))}</td>"
            f"<td>{_esc(_first(item, 'authority', 'jurisdiction', default='Not supplied'))}</td>"
            f"<td>{_esc(_status_text(item))}</td>"
            f"<td>{_risk_badge(item)}</td>"
            f"<td>{_esc(basis)}</td>"
            f"<td>{_esc(confidence)}</td>"
            "</tr>"
        )
    return "".join(rows) or _empty_row(7, "No candidate records supplied.")


def _limitation_rows(comparisons: list[dict[str, Any]]) -> str:
    rows: list[str] = []
    for comparison in comparisons:
        patent = _patent_identity(comparison)
        for item in _as_list(comparison.get("features_comparison")):
            if not isinstance(item, dict):
                continue
            evidence = _as_dict(item.get("product_evidence"))
            evidence_text = " · ".join(
                _safe_str(value)
                for value in (
                    _first(evidence, "reference", "source"),
                    evidence.get("version"),
                    evidence.get("date"),
                )
                if value not in {None, ""}
            )
            rows.append(
                "<tr>"
                f"<td>{_esc(patent)}</td>"
                f"<td>{_esc(_first(item, 'claim_number', default='Not supplied'))}</td>"
                f"<td>{_esc(_first(item, 'limitation_id', default='Not supplied'))}</td>"
                f"<td>{_esc(_first(item, 'claim_limitation', 'claim_text'))}</td>"
                f"<td>{_esc(_first(item, 'product_feature', default='Not identified'))}<small>{_esc(evidence_text)}</small></td>"
                f"<td>{_esc(_first(item, 'literal_mapping', default='Not assessed'))}<small>{_esc(_first(item, 'literal_rationale'))}</small></td>"
                f"<td>{_esc(_first(item, 'equivalents_assessment', default='Not assessed'))}<small>{_esc(_first(item, 'equivalents_rationale'))}</small></td>"
                f"<td>{_esc(_first(item, 'confidence', default='Not supplied'))}</td>"
                "</tr>"
            )
    return "".join(rows) or _empty_row(8, "No limitation-level comparison supplied.")


def _pending_rows(items: list[dict[str, Any]]) -> str:
    rows: list[str] = []
    for item in items:
        rows.append(
            "<tr>"
            f"<td>{_esc(_patent_identity(item))}</td>"
            f"<td>{_esc(_first(item, 'authority', 'jurisdiction', default='Not supplied'))}</td>"
            f"<td>{_esc(_first(item, 'procedural_status', 'status', default='Pending'))}</td>"
            f"<td>{_esc(_first(item, 'status_as_of', default='Not supplied'))}</td>"
            f"<td>{_esc(_first(item, 'claims_or_features_to_monitor', 'monitor', default='Not supplied'))}</td>"
            f"<td>{_esc(_first(item, 'trigger', default='Not supplied'))}</td>"
            f"<td>{_esc(_first(item, 'owner', default='Not supplied'))} · {_esc(_first(item, 'cadence', default='Not supplied'))}</td>"
            "</tr>"
        )
    return "".join(rows) or _empty_row(7, "No pending-application watch item supplied.")


def _action_rows(items: list[dict[str, Any]]) -> str:
    rows: list[str] = []
    for index, item in enumerate(items, 1):
        rows.append(
            "<tr>"
            f"<td>{_esc(_first(item, 'action_id', 'id', default=f'A-{index:03d}'))}</td>"
            f"<td>{_esc(_first(item, 'priority', default='Not ranked'))}</td>"
            f"<td>{_esc(_first(item, 'finding', 'issue', default='Not supplied'))}</td>"
            f"<td>{_esc(_first(item, 'action', 'recommendation', default='Not supplied'))}</td>"
            f"<td>{_esc(_first(item, 'owner', default='Not assigned'))}</td>"
            f"<td>{_esc(_first(item, 'timing', 'due', 'trigger', default='Not supplied'))}</td>"
            f"<td>{_esc(_first(item, 'residual_risk', 'residual', default='Not supplied'))}</td>"
            "</tr>"
        )
    return "".join(rows) or _empty_row(7, "No remediation action supplied.")


def _source_rows(items: list[dict[str, Any]]) -> str:
    rows: list[str] = []
    for index, item in enumerate(items, 1):
        url = _safe_url(_first(item, "url", "source_url"))
        ref = _first(item, "reference", "record", "endpoint", "tool", default="Not supplied")
        ref_html = f'<a href="{_esc(url)}" rel="noopener noreferrer">{_esc(ref)}</a>' if url else _esc(ref)
        rows.append(
            "<tr>"
            f"<td>{_esc(_first(item, 'source_id', 'id', default=f'SRC-{index:03d}'))}</td>"
            f"<td>{_esc(_first(item, 'provider', 'source', 'name', default='Not supplied'))}</td>"
            f"<td>{_esc(_first(item, 'proposition', 'purpose', default='Not supplied'))}</td>"
            f"<td>{ref_html}</td>"
            f"<td>{_esc(_first(item, 'date', 'retrieved_at', 'accessed_at', default='Not supplied'))}</td>"
            f"<td>{_esc(_first(item, 'limitations', 'limitation', default='None stated'))}</td>"
            "</tr>"
        )
    return "".join(rows) or _empty_row(6, "No source register supplied.")


def _merge_records(
    fto_result: dict[str, Any],
    patent_list: list[dict[str, Any]],
    claim_chart_results: list[dict[str, Any]] | None,
    candidates: list[dict[str, Any]] | None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    comparisons = claim_chart_results
    if comparisons is None:
        comparisons = _as_list(
            fto_result.get("comparisons")
            or fto_result.get("claim_chart_results")
            or fto_result.get("analyzed_patents")
            or fto_result.get("final_result")
        )
    normalized_comparisons = [item for item in comparisons if isinstance(item, dict)]
    candidate_values = candidates if candidates is not None else patent_list
    normalized_candidates = [item for item in _as_list(candidate_values) if isinstance(item, dict)]
    if not normalized_candidates:
        normalized_candidates = normalized_comparisons
    return normalized_comparisons, normalized_candidates


def _report_css() -> str:
    """Return the fixed, print-safe scientific/legal stylesheet."""

    percentage_classes = "\n".join(f".pct-{i}{{width:{i}%}}" for i in range(0, 101))
    return f"""
:root {{
  color-scheme: light;
  --navy: #163e5c;
  --navy-2: #245877;
  --ink: #1f2937;
  --muted: #5f6b76;
  --line: #d8dee5;
  --paper: #ffffff;
  --page: #f4f6f8;
  --higher: #8f1d2c;
  --moderate: #875d10;
  --lower: #216344;
  --pending: #45546a;
}}
* {{ box-sizing: border-box; }}
html {{ background: var(--page); }}
body {{
  margin: 0;
  background: var(--page);
  color: var(--ink);
  font: 14px/1.62 Inter, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
}}
a {{ color: #145b86; text-decoration-thickness: 1px; text-underline-offset: 2px; }}
a:focus-visible {{ outline: 3px solid #8cc5e5; outline-offset: 2px; }}
.hero {{ background: var(--navy); color: white; padding: 34px 40px; }}
.hero-inner {{ max-width: 1180px; margin: 0 auto; }}
.eyebrow {{ margin: 0 0 8px; color: #c7deeb; font-size: 12px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }}
h1 {{ margin: 0; max-width: 920px; font-size: clamp(26px, 4vw, 40px); line-height: 1.16; }}
.subtitle {{ margin: 10px 0 0; max-width: 840px; color: #d7e5ed; }}
.meta-grid {{ display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 10px; margin-top: 22px; }}
.meta-item {{ padding: 10px 12px; border: 1px solid rgba(255,255,255,.25); border-radius: 5px; background: rgba(255,255,255,.07); }}
.meta-item span {{ display: block; margin-bottom: 2px; color: #c7deeb; font-size: 11px; }}
.wrap {{ max-width: 1180px; margin: 0 auto; padding: 26px 20px 48px; }}
.card {{ margin: 0 0 16px; padding: 20px 22px; background: var(--paper); border: 1px solid var(--line); border-radius: 7px; box-shadow: 0 1px 3px rgba(15,23,42,.05); }}
.card h2 {{ margin: 0 0 14px; padding-bottom: 8px; border-bottom: 2px solid #e5eaef; color: var(--navy); font-size: 18px; }}
.card h3 {{ margin: 18px 0 8px; color: var(--navy-2); font-size: 15px; }}
.chapter {{ display: inline-block; min-width: 32px; color: #73808b; font-weight: 500; }}
.scope-grid {{ display: grid; grid-template-columns: repeat(3,minmax(0,1fr)); gap: 10px; }}
.scope-item {{ padding: 10px 12px; border-left: 3px solid #7aa8c2; background: #f7fafc; }}
.scope-item dt {{ color: var(--muted); font-size: 11px; font-weight: 700; text-transform: uppercase; }}
.scope-item dd {{ margin: 3px 0 0; }}
.callout {{ padding: 14px 16px; border-left: 4px solid var(--navy-2); background: #f4f8fb; }}
.callout strong {{ display: block; color: var(--navy); }}
.disclaimer {{ border-left-color: #7b8793; background: #f7f8fa; }}
.table-wrap {{ max-width: 100%; overflow-x: auto; overscroll-behavior-inline: contain; -webkit-overflow-scrolling: touch; }}
table {{ width: 100%; min-width: 700px; border-collapse: collapse; font-size: 12.5px; }}
caption {{ padding: 0 0 8px; color: var(--muted); font-weight: 650; text-align: left; }}
th, td {{ padding: 8px 9px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }}
th {{ background: var(--navy); color: white; font-weight: 650; }}
tbody tr:nth-child(even) td {{ background: #fafbfc; }}
td small {{ display: block; margin-top: 4px; color: var(--muted); }}
td code {{ white-space: pre-wrap; word-break: break-word; }}
.empty {{ color: var(--muted); font-style: italic; }}
.risk-badge {{ display: inline-block; padding: 2px 7px; border: 1px solid currentColor; border-radius: 999px; font-size: 11px; font-weight: 750; white-space: nowrap; }}
.risk-higher, .risk-high {{ color: var(--higher); background: #fff5f6; }}
.risk-moderate, .risk-medium {{ color: var(--moderate); background: #fffbef; }}
.risk-lower, .risk-low {{ color: var(--lower); background: #f2fbf6; }}
.risk-pending_watchlist, .risk-pending {{ color: var(--pending); background: #f5f7fa; }}
.risk-not_assessed, .risk-unknown {{ color: #59636e; background: #f5f6f7; }}
.stat-grid {{ display: grid; grid-template-columns: repeat(5,minmax(0,1fr)); gap: 10px; }}
.stat {{ padding: 12px; border: 1px solid var(--line); border-radius: 5px; background: #fbfcfd; }}
.stat b {{ display: block; color: var(--navy); font-size: 22px; }}
.stat span {{ color: var(--muted); font-size: 11px; }}
ul {{ padding-left: 20px; }}
li {{ margin: 4px 0; }}
footer {{ max-width: 1180px; margin: 0 auto; padding: 0 20px 32px; color: var(--muted); font-size: 12px; }}
{percentage_classes}
@media (max-width: 820px) {{
  .hero {{ padding: 24px 18px; }}
  .wrap {{ padding: 16px 10px 34px; }}
  .card {{ padding: 16px 14px; }}
  .meta-grid {{ grid-template-columns: 1fr 1fr; }}
  .scope-grid {{ grid-template-columns: 1fr 1fr; }}
  .stat-grid {{ grid-template-columns: 1fr 1fr; }}
}}
@media (max-width: 480px) {{
  .meta-grid, .scope-grid, .stat-grid {{ grid-template-columns: 1fr; }}
}}
@media print {{
  @page {{ size: Letter; margin: 14mm; }}
  html, body {{ background: white; color: black; font-size: 10pt; }}
  .hero {{ padding: 0 0 12pt; background: white; color: black; border-bottom: 2pt solid #333; }}
  .hero-inner, .wrap, footer {{ max-width: none; padding-left: 0; padding-right: 0; }}
  .subtitle, .eyebrow, .meta-item span {{ color: #333; }}
  .meta-item, .card {{ box-shadow: none; break-inside: avoid; }}
  .meta-item {{ border-color: #777; background: white; }}
  .table-wrap {{ overflow: visible; }}
  table {{ min-width: 0; font-size: 8.5pt; }}
  th {{ background: #e8edf1; color: black; }}
  a {{ color: black; text-decoration: none; }}
}}
@media (prefers-reduced-motion: reduce) {{ * {{ scroll-behavior: auto !important; }} }}
"""


def render_html_report(
    fto_result: dict,
    patent_list: list[dict],
    features: list[dict],
    queries: dict[str, str] | list[dict],
    title: str,
    output_path: str | Path,
    claim_chart_results: list[dict] | None = None,
    candidates: list[dict] | None = None,
) -> None:
    """Generate the complete static HTML report and write it atomically enough for CLI use."""

    data = _as_dict(fto_result)
    project = _as_dict(data.get("project"))
    scope = _as_dict(data.get("scope"))
    provenance = _as_dict(data.get("run_provenance") or data.get("provenance"))
    comparisons, candidate_records = _merge_records(data, patent_list, claim_chart_results, candidates)
    pending = [item for item in _as_list(data.get("pending_application_watchlist")) if isinstance(item, dict)]
    actions = [item for item in _as_list(data.get("recommendations") or data.get("actions") or data.get("mandatory_actions")) if isinstance(item, dict)]
    sources = [item for item in _as_list(data.get("sources") or data.get("source_register")) if isinstance(item, dict)]
    limitations = _as_list(data.get("limitations"))
    errors = _as_list(data.get("errors"))
    conclusions = _as_dict(data.get("conclusion"))

    concern_counts = {key: 0 for key in ("higher", "moderate", "lower", "pending", "not_assessed")}
    for record in candidate_records:
        key = _risk_key(record)
        bucket = "higher" if key == "high" else "moderate" if key == "medium" else "lower" if key == "low" else "pending" if key == "pending_watchlist" else key
        concern_counts[bucket] = concern_counts.get(bucket, 0) + 1

    report_title = _safe_str(title or data.get("report_title") or "FTO screening report")
    generated = _safe_str(data.get("generated_at") or dt.datetime.now(dt.timezone.utc).isoformat())
    mode = _first(provenance, "mode", default="Not supplied")
    run_status = _first(provenance, "status", default=_first(data, "status", "run_status", default="Not supplied"))
    subject = _first(project, "product_name", "target_subject", default=_first(scope, "product_name", "product_description", default="Not supplied"))
    version = _first(project, "product_version", default=_first(scope, "product_version", "technical_version", default="Not supplied"))
    jurisdictions = _first(project, "target_jurisdictions", default=_first(scope, "target_jurisdictions", "target_market", default="Not supplied"))
    acts = _first(project, "relevant_acts", default=_first(scope, "relevant_acts", default="Not supplied"))
    search_cutoff = _first(project, "search_cutoff", default=_first(scope, "search_cutoff", "data_cutoff", default="Not supplied"))
    status_cutoff = _first(project, "status_cutoff", default=_first(scope, "status_cutoff", "status_checked_as_of", default="Not supplied"))
    family_rule = _first(project, "family_counting_convention", default=_first(scope, "family_counting_convention", "family_method", default="Not supplied"))
    decision = _first(project, "decision_context", default=_first(scope, "decision_context", "purpose", default="Not supplied"))

    executive = _first(
        conclusions,
        "summary",
        "basis",
        default=_first(data, "executive_summary", "screening_summary", default="No screening conclusion supplied."),
    )
    overall_status = _first(conclusions, "screening_status", "label", default=_first(data, "screening_status", default="Not assessed"))

    document = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<title>{_esc(report_title)}</title>
<style>
{_report_css()}
</style>
</head>
<body>
<header class="hero">
  <div class="hero-inner">
    <p class="eyebrow">PatSnap evidence workflow · invention-patent screening</p>
    <h1>{_esc(report_title)}</h1>
    <p class="subtitle">Traceable search, claim-data review, limitation mapping, uncertainty, and action planning. Screening output only.</p>
    <div class="meta-grid">
      <div class="meta-item"><span>Target subject</span>{_esc(subject)}</div>
      <div class="meta-item"><span>Controlled version</span>{_esc(version)}</div>
      <div class="meta-item"><span>Target jurisdiction(s)</span>{_esc(jurisdictions)}</div>
      <div class="meta-item"><span>Run status</span>{_esc(run_status)}</div>
    </div>
  </div>
</header>
<main class="wrap">
  <section class="card" aria-labelledby="section-1">
    <h2 id="section-1"><span class="chapter">1.</span>Executive screening summary</h2>
    <div class="callout"><strong>{_esc(overall_status)}</strong>{_esc(executive)}</div>
    <div class="stat-grid">
      <div class="stat"><b>{concern_counts['higher']}</b><span>Higher concern</span></div>
      <div class="stat"><b>{concern_counts['moderate']}</b><span>Moderate concern</span></div>
      <div class="stat"><b>{concern_counts['lower']}</b><span>Lower concern</span></div>
      <div class="stat"><b>{len(pending)}</b><span>Pending watchlist</span></div>
      <div class="stat"><b>{len(errors)}</b><span>Recorded errors</span></div>
    </div>
  </section>

  <section class="card" aria-labelledby="section-2">
    <h2 id="section-2"><span class="chapter">2.</span>Purpose, subject, and decision context</h2>
    <dl class="scope-grid">
      <div class="scope-item"><dt>Subject</dt><dd>{_esc(subject)}</dd></div>
      <div class="scope-item"><dt>Version</dt><dd>{_esc(version)}</dd></div>
      <div class="scope-item"><dt>Jurisdictions</dt><dd>{_esc(jurisdictions)}</dd></div>
      <div class="scope-item"><dt>Relevant acts</dt><dd>{_esc(acts)}</dd></div>
      <div class="scope-item"><dt>Decision</dt><dd>{_esc(decision)}</dd></div>
      <div class="scope-item"><dt>Generated</dt><dd>{_esc(generated)}</dd></div>
    </dl>
  </section>

  <section class="card" aria-labelledby="section-3">
    <h2 id="section-3"><span class="chapter">3.</span>Scope, cutoffs, assumptions, and exclusions</h2>
    <dl class="scope-grid">
      <div class="scope-item"><dt>Search cutoff</dt><dd>{_esc(search_cutoff)}</dd></div>
      <div class="scope-item"><dt>Status cutoff</dt><dd>{_esc(status_cutoff)}</dd></div>
      <div class="scope-item"><dt>Family/counting convention</dt><dd>{_esc(family_rule)}</dd></div>
    </dl>
    <h3>Assumptions</h3><ul>{_list_html(_as_list(data.get('assumptions')), 'No assumption register supplied.')}</ul>
    <h3>Exclusions</h3><ul>{_list_html(_as_list(data.get('exclusions')), 'No exclusion register supplied.')}</ul>
  </section>

  <section class="card" aria-labelledby="section-4">
    <h2 id="section-4"><span class="chapter">4.</span>Technical-feature and product-evidence inventory</h2>
    <div class="table-wrap"><table><caption>Features retained for claim comparison</caption>
      <thead><tr><th>ID</th><th>Group</th><th>Technical feature</th><th>Importance</th><th>Product evidence</th></tr></thead>
      <tbody>{_feature_rows([item for item in features if isinstance(item, dict)])}</tbody>
    </table></div>
  </section>

  <section class="card" aria-labelledby="section-5">
    <h2 id="section-5"><span class="chapter">5.</span>Data-access mode and search methodology</h2>
    <p><strong>Mode:</strong> {_esc(mode)} · <strong>Provider:</strong> {_esc(_first(provenance, 'provider', default='Not supplied'))}</p>
    <p>{_esc(_first(provenance, 'notes', default='No additional provenance note supplied.'))}</p>
    <div class="table-wrap"><table><caption>Reviewed PatSnap search expressions</caption>
      <thead><tr><th>Query ID</th><th>Expression</th><th>Origin</th><th>Approval/run status</th><th>Results</th></tr></thead>
      <tbody>{_query_rows(queries)}</tbody>
    </table></div>
  </section>

  <section class="card" aria-labelledby="section-6">
    <h2 id="section-6"><span class="chapter">6.</span>Candidate and family overview</h2>
    <p>{len(candidate_records)} candidate record(s) are displayed under the supplied family/counting convention. A candidate is not an infringement finding.</p>
    <div class="table-wrap"><table><caption>Candidate screening register</caption>
      <thead><tr><th>Patent / publication</th><th>Title</th><th>Authority</th><th>Status evidence</th><th>Concern</th><th>Basis</th><th>Confidence</th></tr></thead>
      <tbody>{_candidate_rows(candidate_records)}</tbody>
    </table></div>
  </section>

  <section class="card" aria-labelledby="section-7">
    <h2 id="section-7"><span class="chapter">7.</span>Higher and moderate screening concerns</h2>
    <div class="table-wrap"><table><caption>Records requiring priority review</caption>
      <thead><tr><th>Patent / publication</th><th>Title</th><th>Authority</th><th>Status evidence</th><th>Concern</th><th>Basis</th><th>Confidence</th></tr></thead>
      <tbody>{_candidate_rows([item for item in candidate_records if _risk_key(item) in {'higher','high','moderate','medium'}])}</tbody>
    </table></div>
  </section>

  <section class="card" aria-labelledby="section-8">
    <h2 id="section-8"><span class="chapter">8.</span>Lower concern and not-assessed records</h2>
    <div class="table-wrap"><table><caption>Lower concern and incomplete comparisons</caption>
      <thead><tr><th>Patent / publication</th><th>Title</th><th>Authority</th><th>Status evidence</th><th>Concern</th><th>Basis</th><th>Confidence</th></tr></thead>
      <tbody>{_candidate_rows([item for item in candidate_records if _risk_key(item) in {'lower','low','not_assessed','unknown'}])}</tbody>
    </table></div>
  </section>

  <section class="card" aria-labelledby="section-9">
    <h2 id="section-9"><span class="chapter">9.</span>Claim-limitation comparison</h2>
    <div class="table-wrap"><table><caption>Literal mapping and jurisdiction-qualified equivalents review</caption>
      <thead><tr><th>Patent</th><th>Claim</th><th>Limitation</th><th>Claim text</th><th>Product evidence</th><th>Literal mapping</th><th>Equivalents</th><th>Confidence</th></tr></thead>
      <tbody>{_limitation_rows(comparisons)}</tbody>
    </table></div>
  </section>

  <section class="card" aria-labelledby="section-10">
    <h2 id="section-10"><span class="chapter">10.</span>Pending-application watchlist</h2>
    <p>Pending claims may change and are not presented as currently enforceable patent claims.</p>
    <div class="table-wrap"><table><caption>Applications and prosecution events to monitor</caption>
      <thead><tr><th>Application/publication</th><th>Authority</th><th>Status</th><th>Status date</th><th>Claim/feature</th><th>Trigger</th><th>Owner/cadence</th></tr></thead>
      <tbody>{_pending_rows(pending)}</tbody>
    </table></div>
  </section>

  <section class="card" aria-labelledby="section-11">
    <h2 id="section-11"><span class="chapter">11.</span>Status, family, claim-version, and translation controls</h2>
    <ul>{_list_html(_as_list(data.get('evidence_controls')), 'No consolidated evidence-control note supplied; inspect each comparison record.')}</ul>
    <p>A PatSnap status/filter value is screening evidence and may require confirmation in the authoritative register. Family members may have different claims and status.</p>
  </section>

  <section class="card" aria-labelledby="section-12">
    <h2 id="section-12"><span class="chapter">12.</span>Errors, unresolved evidence, and limitations</h2>
    <h3>Recorded errors</h3><ul>{_list_html(errors, 'No run error recorded.')}</ul>
    <h3>Limitations</h3><ul>{_list_html(limitations, 'No limitation register supplied; this is itself a documentation gap.')}</ul>
  </section>

  <section class="card" aria-labelledby="section-13">
    <h2 id="section-13"><span class="chapter">13.</span>Recommendations and re-review triggers</h2>
    <div class="table-wrap"><table><caption>Decision-ready remediation plan</caption>
      <thead><tr><th>ID</th><th>Priority</th><th>Finding</th><th>Action</th><th>Owner</th><th>Timing/trigger</th><th>Residual risk</th></tr></thead>
      <tbody>{_action_rows(actions)}</tbody>
    </table></div>
    <h3>Re-review triggers</h3><ul>{_list_html(_as_list(data.get('re_review_triggers')), 'Define product, jurisdiction, prosecution, status, publication, and decision-gate triggers.')}</ul>
  </section>

  <section class="card" aria-labelledby="section-14">
    <h2 id="section-14"><span class="chapter">14.</span>Source and provenance register</h2>
    <div class="table-wrap"><table><caption>Evidence sources and limitations</caption>
      <thead><tr><th>ID</th><th>Provider/source</th><th>Proposition</th><th>Record/tool</th><th>Date</th><th>Limitation</th></tr></thead>
      <tbody>{_source_rows(sources)}</tbody>
    </table></div>
  </section>

  <section class="card" aria-labelledby="section-15">
    <h2 id="section-15"><span class="chapter">15.</span>Screening boundary and disclaimer</h2>
    <div class="callout disclaimer">
      <strong>FTO screening — not legal clearance</strong>
      This report is limited to the defined subject, controlled version, commercial acts, jurisdictions, search and status cutoffs, claims, product evidence, provider coverage, and family/counting convention. Patent applications may remain unpublished; claims, ownership, status, products, and law may change. The report does not establish complete recall, infringement, validity, enforceability, or freedom to operate. Qualified local counsel should review any material legal or commercial decision.
    </div>
  </section>
</main>
<footer>Generated as a static evidence-based screening report. Data source and execution mode are identified above; no credential is embedded.</footer>
</body>
</html>
"""

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding="utf-8")
    print(f"FTO screening HTML written: {output.resolve()}")


def render_from_structured_data(data: dict[str, Any], output_path: str | Path) -> None:
    """Map one normalized data object into the backward-compatible renderer."""

    project = _as_dict(data.get("project"))
    title = _safe_str(data.get("report_title") or f"{project.get('product_name') or 'Product'} FTO screening report")
    patent_list = [item for item in _as_list(data.get("patent_list") or data.get("candidates")) if isinstance(item, dict)]
    features = [item for item in _as_list(data.get("features") or data.get("technical_features")) if isinstance(item, dict)]
    queries = data.get("queries") or {}
    comparisons = [item for item in _as_list(data.get("comparisons") or data.get("claim_chart_results")) if isinstance(item, dict)]
    render_html_report(
        data,
        patent_list,
        features,
        queries,
        title,
        output_path,
        claim_chart_results=comparisons,
        candidates=patent_list,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render normalized FTO screening JSON as safe static English HTML.")
    parser.add_argument("input", type=Path, help="fto_structured_data.json")
    parser.add_argument("output", type=Path, help="Output HTML path")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        loaded = json.loads(args.input.read_text(encoding="utf-8-sig"))
        if not isinstance(loaded, dict):
            raise ValueError("Input JSON must contain an object.")
        render_from_structured_data(loaded, args.output)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        print(f"Unable to render FTO screening report: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

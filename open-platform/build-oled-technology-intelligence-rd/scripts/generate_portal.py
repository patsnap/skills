#!/usr/bin/env python3
"""Generate a reviewed, self-contained technology-intelligence HTML portal."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse


SAFE_ID = re.compile(r"^[a-z0-9][a-z0-9-]{0,79}$")
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
REQUIRED_ARRAYS = (
    "executive_findings",
    "companies",
    "technologies",
    "records",
    "events",
    "publications",
    "patents",
    "search_log",
    "rejections",
)
REQUIRED_PORTAL_FIELDS = (
    "title",
    "technology_domain",
    "scope",
    "decision_context",
    "geographies",
    "languages",
    "period_start",
    "period_end",
    "evidence_cutoff",
    "generated_on",
    "analyst",
    "confidentiality",
    "methodology",
    "limitations",
    "patent_count_unit",
)
RESERVED_SLUGS = {"index", "patents", "assets", "con", "prn", "aux", "nul"}


class PortalError(ValueError):
    """Raised when input or output would make the portal unreliable or unsafe."""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render reviewed technology-intelligence JSON as a multi-page HTML portal."
    )
    parser.add_argument("--data", required=True, type=Path, help="UTF-8 reviewed portal JSON")
    parser.add_argument("--output", required=True, type=Path, help="Output portal directory")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace only portal pages that this run is expected to generate",
    )
    return parser.parse_args(argv)


def fail(message: str) -> None:
    raise PortalError(message)


def require_object(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{path} must be an object")
    return value


def require_list(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        fail(f"{path} must be an array")
    return value


def require_text(value: Any, path: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str):
        fail(f"{path} must be a string")
    cleaned = value.strip()
    if not allow_empty and not cleaned:
        fail(f"{path} must not be empty")
    return cleaned


def optional_text(value: Any, path: str) -> str:
    if value is None:
        return ""
    return require_text(value, path, allow_empty=True)


def require_text_list(value: Any, path: str) -> list[str]:
    items = require_list(value, path)
    return [require_text(item, f"{path}[{index}]") for index, item in enumerate(items)]


def require_date(value: Any, path: str) -> str:
    date = require_text(value, path)
    if not ISO_DATE.fullmatch(date):
        fail(f"{path} must use YYYY-MM-DD")
    return date


def require_id(value: Any, path: str) -> str:
    identifier = require_text(value, path)
    if not SAFE_ID.fullmatch(identifier):
        fail(f"{path} must contain lowercase ASCII letters, digits, and hyphens")
    if identifier in RESERVED_SLUGS or identifier.startswith(".") or ".." in identifier:
        fail(f"{path} uses a reserved or unsafe identifier")
    return identifier


def safe_external_url(value: Any, path: str) -> str:
    url = optional_text(value, path)
    if not url:
        return ""
    parsed = urlparse(url)
    if parsed.scheme not in {"https", "http"} or not parsed.netloc:
        fail(f"{path} must be an absolute HTTP(S) URL or an empty string")
    if parsed.username or parsed.password:
        fail(f"{path} must not contain embedded credentials")
    return url


def escape(value: Any) -> str:
    return html.escape(str(value), quote=True)


def text_or(value: Any, fallback: str = "Not established from reviewed evidence") -> str:
    if value is None:
        return fallback
    if isinstance(value, str):
        cleaned = value.strip()
        return cleaned if cleaned else fallback
    return str(value)


def join_text(values: Iterable[Any], fallback: str = "Not specified") -> str:
    rendered = [str(value).strip() for value in values if str(value).strip()]
    return ", ".join(rendered) if rendered else fallback


def read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        fail(f"Input file does not exist: {path}")
    try:
        raw = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        fail(f"Unable to read UTF-8 input: {exc}")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        fail(f"Invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}")
    return require_object(data, "root")


def unique_id_map(items: list[Any], path: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(items):
        obj = require_object(item, f"{path}[{index}]")
        identifier = require_id(obj.get("id"), f"{path}[{index}].id")
        if identifier in result:
            fail(f"Duplicate identifier {identifier!r} in {path}")
        result[identifier] = obj
    return result


def check_references(
    values: Any,
    path: str,
    allowed: set[str],
) -> list[str]:
    references = require_text_list(values or [], path)
    unknown = [value for value in references if value not in allowed]
    if unknown:
        fail(f"{path} contains unknown IDs: {', '.join(unknown)}")
    return references


def validate_portal_metadata(portal: dict[str, Any]) -> None:
    for field in REQUIRED_PORTAL_FIELDS:
        if field not in portal:
            fail(f"portal.{field} is required")
    for field in (
        "title",
        "technology_domain",
        "scope",
        "decision_context",
        "analyst",
        "confidentiality",
        "methodology",
        "limitations",
        "patent_count_unit",
    ):
        require_text(portal[field], f"portal.{field}")
    require_text_list(portal["geographies"], "portal.geographies")
    require_text_list(portal["languages"], "portal.languages")
    start = require_date(portal["period_start"], "portal.period_start")
    end = require_date(portal["period_end"], "portal.period_end")
    cutoff = require_date(portal["evidence_cutoff"], "portal.evidence_cutoff")
    require_date(portal["generated_on"], "portal.generated_on")
    if start > end:
        fail("portal.period_start must not be after portal.period_end")
    if end > cutoff:
        fail("portal.period_end must not be after portal.evidence_cutoff")


def validate_company(
    company: dict[str, Any],
    path: str,
    evidence_ids: set[str],
    technology_ids: set[str],
    patent_ids: set[str],
) -> None:
    require_text(company.get("display_name"), f"{path}.display_name")
    optional_text(company.get("legal_name"), f"{path}.legal_name")
    require_text_list(company.get("aliases", []), f"{path}.aliases")
    require_text(company.get("entity_type"), f"{path}.entity_type")
    require_text_list(company.get("value_chain_roles", []), f"{path}.value_chain_roles")
    require_text_list(company.get("geographies", []), f"{path}.geographies")
    require_text(company.get("inclusion_rationale"), f"{path}.inclusion_rationale")
    check_references(company.get("evidence_ids", []), f"{path}.evidence_ids", evidence_ids)
    check_references(company.get("technology_ids", []), f"{path}.technology_ids", technology_ids)
    check_references(company.get("patent_ids", []), f"{path}.patent_ids", patent_ids)
    require_date(company.get("first_evidence_date"), f"{path}.first_evidence_date")
    require_date(company.get("last_evidence_date"), f"{path}.last_evidence_date")
    require_text(company.get("review_status"), f"{path}.review_status")
    require_text(company.get("confidence"), f"{path}.confidence")
    optional_text(company.get("relationship_notes"), f"{path}.relationship_notes")
    optional_text(company.get("summary"), f"{path}.summary")


def validate_technology(
    technology: dict[str, Any],
    path: str,
    evidence_ids: set[str],
) -> None:
    require_text(technology.get("name"), f"{path}.name")
    require_text(technology.get("definition"), f"{path}.definition")
    require_text(technology.get("inclusion_criteria"), f"{path}.inclusion_criteria")
    require_text(technology.get("exclusion_criteria"), f"{path}.exclusion_criteria")
    require_text_list(technology.get("synonyms", []), f"{path}.synonyms")
    require_text_list(technology.get("disambiguation_terms", []), f"{path}.disambiguation_terms")
    require_text_list(technology.get("parent_ids", []), f"{path}.parent_ids")
    require_text_list(technology.get("related_ids", []), f"{path}.related_ids")
    check_references(technology.get("evidence_ids", []), f"{path}.evidence_ids", evidence_ids)
    require_date(technology.get("review_date"), f"{path}.review_date")
    require_text(technology.get("review_status"), f"{path}.review_status")
    require_text(technology.get("confidence"), f"{path}.confidence")
    optional_text(technology.get("maturity_note"), f"{path}.maturity_note")


def validate_record(
    record: dict[str, Any],
    path: str,
    company_ids: set[str],
    technology_ids: set[str],
) -> None:
    require_text(record.get("title"), f"{path}.title")
    require_text(record.get("record_type"), f"{path}.record_type")
    require_text(record.get("source_name"), f"{path}.source_name")
    safe_external_url(record.get("source_url", ""), f"{path}.source_url")
    require_date(record.get("published_date"), f"{path}.published_date")
    optional_event_date = record.get("event_date")
    if optional_event_date:
        require_date(optional_event_date, f"{path}.event_date")
    require_date(record.get("accessed_date"), f"{path}.accessed_date")
    require_text(record.get("language"), f"{path}.language")
    require_text(record.get("summary"), f"{path}.summary")
    check_references(record.get("company_ids", []), f"{path}.company_ids", company_ids)
    check_references(record.get("technology_ids", []), f"{path}.technology_ids", technology_ids)
    require_text(record.get("evidence_type"), f"{path}.evidence_type")
    require_text(record.get("review_status"), f"{path}.review_status")
    require_text(record.get("confidence"), f"{path}.confidence")
    optional_text(record.get("analyst_note"), f"{path}.analyst_note")


def validate_patent(
    patent: dict[str, Any],
    path: str,
    company_ids: set[str],
    technology_ids: set[str],
) -> None:
    require_text(patent.get("publication_number"), f"{path}.publication_number")
    require_text(patent.get("title"), f"{path}.title")
    require_text(patent.get("jurisdiction"), f"{path}.jurisdiction")
    require_text_list(patent.get("applicants", []), f"{path}.applicants")
    require_text_list(patent.get("assignees", []), f"{path}.assignees")
    priority = patent.get("earliest_priority_date")
    if priority:
        require_date(priority, f"{path}.earliest_priority_date")
    require_date(patent.get("publication_date"), f"{path}.publication_date")
    optional_text(patent.get("simple_family_id"), f"{path}.simple_family_id")
    optional_text(patent.get("extended_family_id"), f"{path}.extended_family_id")
    optional_text(patent.get("legal_status"), f"{path}.legal_status")
    status_date = patent.get("legal_status_as_of")
    if status_date:
        require_date(status_date, f"{path}.legal_status_as_of")
    require_text(patent.get("abstract_summary"), f"{path}.abstract_summary")
    require_text(patent.get("relevance_note"), f"{path}.relevance_note")
    check_references(patent.get("company_ids", []), f"{path}.company_ids", company_ids)
    check_references(patent.get("technology_ids", []), f"{path}.technology_ids", technology_ids)
    safe_external_url(patent.get("source_url", ""), f"{path}.source_url")
    require_text(patent.get("review_depth"), f"{path}.review_depth")
    require_text(patent.get("review_status"), f"{path}.review_status")
    require_text(patent.get("confidence"), f"{path}.confidence")


def validate_data(data: dict[str, Any]) -> dict[str, dict[str, dict[str, Any]]]:
    if data.get("review_status") != "reviewed":
        fail("review_status must be 'reviewed'")
    portal = require_object(data.get("portal"), "portal")
    validate_portal_metadata(portal)
    for name in REQUIRED_ARRAYS:
        require_list(data.get(name), name)

    maps = {
        "companies": unique_id_map(data["companies"], "companies"),
        "technologies": unique_id_map(data["technologies"], "technologies"),
        "records": unique_id_map(data["records"], "records"),
        "events": unique_id_map(data["events"], "events"),
        "publications": unique_id_map(data["publications"], "publications"),
        "patents": unique_id_map(data["patents"], "patents"),
        "search_log": unique_id_map(data["search_log"], "search_log"),
    }
    company_ids = set(maps["companies"])
    technology_ids = set(maps["technologies"])
    record_ids = set(maps["records"])
    publication_ids = set(maps["publications"])
    patent_ids = set(maps["patents"])
    evidence_ids = record_ids | publication_ids | patent_ids

    for identifier, company in maps["companies"].items():
        validate_company(
            company,
            f"companies[{identifier}]",
            evidence_ids,
            technology_ids,
            patent_ids,
        )
    for identifier, technology in maps["technologies"].items():
        validate_technology(technology, f"technologies[{identifier}]", evidence_ids)
    for identifier, record in maps["records"].items():
        validate_record(
            record,
            f"records[{identifier}]",
            company_ids,
            technology_ids,
        )
    for identifier, patent in maps["patents"].items():
        validate_patent(
            patent,
            f"patents[{identifier}]",
            company_ids,
            technology_ids,
        )

    for identifier, technology in maps["technologies"].items():
        for field in ("parent_ids", "related_ids"):
            check_references(
                technology.get(field, []),
                f"technologies[{identifier}].{field}",
                technology_ids,
            )

    for identifier, event in maps["events"].items():
        require_text(event.get("title"), f"events[{identifier}].title")
        require_date(event.get("event_date"), f"events[{identifier}].event_date")
        check_references(event.get("source_ids", []), f"events[{identifier}].source_ids", evidence_ids)
        check_references(event.get("company_ids", []), f"events[{identifier}].company_ids", company_ids)
        check_references(event.get("technology_ids", []), f"events[{identifier}].technology_ids", technology_ids)
        require_text(event.get("observed_fact"), f"events[{identifier}].observed_fact")
        optional_text(event.get("analyst_inference"), f"events[{identifier}].analyst_inference")
        require_text(event.get("decision_relevance"), f"events[{identifier}].decision_relevance")
        require_text(event.get("confidence"), f"events[{identifier}].confidence")
        require_text(event.get("review_status"), f"events[{identifier}].review_status")

    for identifier, publication in maps["publications"].items():
        require_text(publication.get("title"), f"publications[{identifier}].title")
        require_text_list(publication.get("authors", []), f"publications[{identifier}].authors")
        require_text(publication.get("venue"), f"publications[{identifier}].venue")
        optional_text(publication.get("doi"), f"publications[{identifier}].doi")
        safe_external_url(publication.get("source_url", ""), f"publications[{identifier}].source_url")
        require_date(publication.get("published_date"), f"publications[{identifier}].published_date")
        require_text(publication.get("abstract_summary"), f"publications[{identifier}].abstract_summary")
        check_references(publication.get("company_ids", []), f"publications[{identifier}].company_ids", company_ids)
        check_references(publication.get("technology_ids", []), f"publications[{identifier}].technology_ids", technology_ids)
        require_text(publication.get("review_status"), f"publications[{identifier}].review_status")
        require_text(publication.get("confidence"), f"publications[{identifier}].confidence")

    for identifier, search in maps["search_log"].items():
        require_text(search.get("source_or_tool"), f"search_log[{identifier}].source_or_tool")
        require_text(search.get("searched_at"), f"search_log[{identifier}].searched_at")
        require_text(search.get("query"), f"search_log[{identifier}].query")
        require_object(search.get("filters", {}), f"search_log[{identifier}].filters")
        require_text_list(search.get("languages", []), f"search_log[{identifier}].languages")
        for count_field in ("requested_limit", "returned_count"):
            count = search.get(count_field)
            if not isinstance(count, int) or isinstance(count, bool) or count < 0:
                fail(f"search_log[{identifier}].{count_field} must be a non-negative integer")
        check_references(
            search.get("reviewed_ids", []),
            f"search_log[{identifier}].reviewed_ids",
            evidence_ids,
        )
        require_text(
            search.get("pagination_or_truncation"),
            f"search_log[{identifier}].pagination_or_truncation",
        )
        require_text(search.get("deduplication"), f"search_log[{identifier}].deduplication")
        require_text(search.get("limitations"), f"search_log[{identifier}].limitations")

    for index, finding in enumerate(data["executive_findings"]):
        obj = require_object(finding, f"executive_findings[{index}]")
        require_text(obj.get("finding"), f"executive_findings[{index}].finding")
        require_text(obj.get("basis"), f"executive_findings[{index}].basis")
        check_references(obj.get("evidence_ids", []), f"executive_findings[{index}].evidence_ids", evidence_ids)
        require_text(obj.get("confidence"), f"executive_findings[{index}].confidence")

    return maps


SHARED_CSS = """
:root{--ink:#172033;--muted:#5a667a;--line:#d8dee8;--paper:#fff;--wash:#f5f7fa;--accent:#145da0;--accent-soft:#eaf2f9;--positive:#287a55;--warning:#9a6318;--critical:#a13d3d;--radius:8px;--measure:1200px}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--wash);color:var(--ink);font-family:Inter,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;font-size:15px;line-height:1.55}
a{color:var(--accent);text-underline-offset:2px}a:focus-visible{outline:3px solid #79aede;outline-offset:2px}.skip-link{position:absolute;left:-9999px;top:8px}.skip-link:focus{left:8px;z-index:100;background:#fff;padding:8px}
.masthead{background:var(--paper);border-bottom:1px solid var(--line)}.masthead-inner{max-width:var(--measure);margin:0 auto;padding:34px 28px 28px}.eyebrow{color:var(--accent);font-size:12px;font-weight:750;letter-spacing:.08em;text-transform:uppercase}
h1{max-width:920px;margin:8px 0 12px;font:600 clamp(32px,5vw,54px)/1.08 Georgia,"Times New Roman",serif}h2{margin:0 0 6px;font:600 28px/1.2 Georgia,"Times New Roman",serif}h3{margin:18px 0 7px;font-size:16px}.deck{max-width:900px;color:var(--muted);font-size:17px}
.meta-grid{display:grid;grid-template-columns:repeat(4,minmax(150px,1fr));gap:1px;margin-top:24px;border:1px solid var(--line);background:var(--line)}.meta{min-height:76px;padding:12px 14px;background:var(--paper)}.meta-label{color:var(--muted);font-size:10px;font-weight:750;letter-spacing:.05em;text-transform:uppercase}.meta-value{margin-top:5px;font-weight:650}
.topnav{position:sticky;top:0;z-index:20;border-bottom:1px solid var(--line);background:rgba(255,255,255,.97)}.topnav-inner{display:flex;gap:6px;max-width:var(--measure);margin:0 auto;padding:8px 28px;overflow-x:auto}.topnav a{padding:7px 10px;color:var(--muted);font-size:13px;text-decoration:none;white-space:nowrap}.topnav a:hover,.topnav a:focus{color:var(--accent);background:var(--accent-soft)}
main{max-width:var(--measure);margin:22px auto 60px;padding:0 28px}section{margin-bottom:22px;padding:24px;border:1px solid var(--line);border-radius:var(--radius);background:var(--paper)}.section-deck{margin:0 0 18px;color:var(--muted)}
.stats{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:1px;border:1px solid var(--line);background:var(--line)}.stat{padding:14px;background:var(--paper)}.stat-value{font:600 26px Georgia,serif;font-variant-numeric:tabular-nums}.stat-label{color:var(--muted);font-size:11px}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}.card{display:block;border:1px solid var(--line);border-top:3px solid var(--accent);padding:15px;color:inherit;text-decoration:none}.card:hover{border-color:#9ebbd4;background:#fbfdff}.card-title{font-weight:700}.card-meta{margin-top:5px;color:var(--muted);font-size:12px}
.tag{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:2px 8px;font-size:11px;font-weight:700}.tag.checked{color:var(--positive);background:#eff8f3}.tag.gap{color:var(--critical);background:#fff3f3}.tag.inference{color:var(--warning);background:#fff9ef}
.finding{display:grid;grid-template-columns:42px minmax(0,1fr);gap:12px;padding:13px 0;border-bottom:1px solid var(--line)}.finding-index{color:var(--accent);font:24px Georgia,serif}.timeline{border-left:2px solid var(--line);margin-left:6px;padding-left:18px}.event{position:relative;padding:0 0 18px}.event:before{content:"";position:absolute;left:-24px;top:6px;width:8px;height:8px;border:2px solid var(--accent);border-radius:50%;background:#fff}.event-date{color:var(--muted);font-size:11px;font-variant-numeric:tabular-nums}.event-title{font-weight:700}
.table-wrap{overflow-x:auto}table{width:100%;border-collapse:collapse;font-size:13px;font-variant-numeric:tabular-nums}caption{padding-bottom:8px;color:var(--muted);text-align:left}th,td{padding:10px 9px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}th{background:var(--wash);color:var(--muted);font-size:10px;letter-spacing:.04em;text-transform:uppercase}
.notice{border-left:4px solid var(--warning);padding:11px 14px;background:#fff9ef;color:#6c481a}.empty{color:var(--muted);font-style:italic}.source-list{padding-left:20px}.source-list li{margin:5px 0}.detail-header{display:flex;justify-content:space-between;gap:18px;align-items:flex-start}.back-link{display:inline-block;margin-bottom:16px}.two-col{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.panel{border:1px solid var(--line);padding:14px}footer{border-top:1px solid var(--line);padding:24px 28px;color:var(--muted);font-size:12px}
@media(max-width:900px){.stats{grid-template-columns:repeat(3,1fr)}.grid{grid-template-columns:repeat(2,1fr)}.meta-grid{grid-template-columns:repeat(2,1fr)}}@media(max-width:620px){.stats,.grid,.meta-grid,.two-col{grid-template-columns:1fr}main,.masthead-inner{padding-left:15px;padding-right:15px}section{padding:17px}}@media print{body{background:#fff;font-size:10pt}.topnav,.skip-link,.no-print{display:none}main{max-width:none;margin:0;padding:0}section,.card{break-inside:avoid}a{color:inherit;text-decoration:none}}
"""


def meta_cell(label: str, value: str) -> str:
    return (
        '<div class="meta"><div class="meta-label">'
        + escape(label)
        + '</div><div class="meta-value">'
        + escape(value)
        + "</div></div>"
    )


def local_link(label: str, href: str) -> str:
    return f'<a href="{escape(href)}">{escape(label)}</a>'


def source_link(label: str, url: str) -> str:
    if not url:
        return f"{escape(label)} — Source link not supplied"
    return (
        f'<a href="{escape(url)}" target="_blank" rel="noopener noreferrer">'
        f"{escape(label)}</a>"
    )


def shell(
    *,
    title: str,
    eyebrow: str,
    deck: str,
    metadata: list[tuple[str, str]],
    navigation: list[tuple[str, str]],
    body: str,
    footer: str,
) -> str:
    meta_html = "".join(meta_cell(label, value) for label, value in metadata)
    nav_html = "".join(local_link(label, href) for label, href in navigation)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <style>{SHARED_CSS}</style>
</head>
<body>
  <a class="skip-link" href="#main">Skip to main content</a>
  <header class="masthead">
    <div class="masthead-inner">
      <div class="eyebrow">{escape(eyebrow)}</div>
      <h1>{escape(title)}</h1>
      <p class="deck">{escape(deck)}</p>
      <div class="meta-grid" aria-label="Portal metadata">{meta_html}</div>
    </div>
  </header>
  <nav class="topnav" aria-label="Portal navigation"><div class="topnav-inner">{nav_html}</div></nav>
  <main id="main">{body}</main>
  <footer>{escape(footer)}</footer>
</body>
</html>
"""


def evidence_ids_html(ids: list[str]) -> str:
    if not ids:
        return '<span class="empty">No evidence ID supplied</span>'
    return ", ".join(f'<code id="evidence-{escape(value)}">{escape(value)}</code>' for value in ids)


def render_empty(message: str) -> str:
    return f'<p class="empty">{escape(message)}</p>'


def calculated_patent_count(patents: list[dict[str, Any]], unit: str) -> int:
    normalized = unit.lower()
    if "simple" in normalized and "family" in normalized:
        keys = {text_or(item.get("simple_family_id"), item["id"]) for item in patents}
        return len(keys)
    if "extended" in normalized and "family" in normalized:
        keys = {text_or(item.get("extended_family_id"), item["id"]) for item in patents}
        return len(keys)
    return len(patents)


def records_for(
    records: list[dict[str, Any]],
    field: str,
    identifier: str,
) -> list[dict[str, Any]]:
    return [record for record in records if identifier in record.get(field, [])]


def patent_rows(
    patents: list[dict[str, Any]],
    technologies: dict[str, dict[str, Any]],
) -> str:
    if not patents:
        return '<tr><td colspan="8" class="empty">No reviewed patent records were supplied.</td></tr>'
    rows: list[str] = []
    for patent in sorted(patents, key=lambda item: item["publication_date"], reverse=True):
        publication = source_link(patent["publication_number"], patent.get("source_url", ""))
        names = [technologies[value]["name"] for value in patent.get("technology_ids", [])]
        rows.append(
            "<tr>"
            f"<td>{publication}</td>"
            f"<td>{escape(patent['title'])}</td>"
            f"<td>{escape(join_text(patent.get('applicants', [])))}</td>"
            f"<td>{escape(text_or(patent.get('earliest_priority_date')))}<br>{escape(patent['publication_date'])}</td>"
            f"<td>{escape(text_or(patent.get('simple_family_id')))}</td>"
            f"<td>{escape(join_text(names))}</td>"
            f"<td>{escape(patent['relevance_note'])}</td>"
            f"<td>{escape(patent['review_depth'])}<br>{escape(patent['review_status'])}</td>"
            "</tr>"
        )
    return "".join(rows)


def render_index(
    data: dict[str, Any],
    maps: dict[str, dict[str, dict[str, Any]]],
) -> str:
    portal = data["portal"]
    companies = list(maps["companies"].values())
    technologies = list(maps["technologies"].values())
    records = list(maps["records"].values())
    events = list(maps["events"].values())
    publications = list(maps["publications"].values())
    patents = list(maps["patents"].values())
    patent_count = calculated_patent_count(patents, portal["patent_count_unit"])
    stats = [
        ("Current-awareness records", len(records)),
        ("Material events", len(events)),
        ("Scientific publications", len(publications)),
        (f"Patents · {portal['patent_count_unit']}", patent_count),
        ("Monitored organizations", len(companies)),
        ("Technology routes", len(technologies)),
    ]
    stats_html = "".join(
        f'<div class="stat"><div class="stat-value">{value}</div><div class="stat-label">{escape(label)}</div></div>'
        for label, value in stats
    )

    findings: list[str] = []
    for index, finding in enumerate(data["executive_findings"], start=1):
        findings.append(
            '<article class="finding">'
            f'<div class="finding-index">{index:02d}</div>'
            f"<div><strong>{escape(finding['finding'])}</strong>"
            f"<p>{escape(finding['basis'])}</p>"
            f'<div class="card-meta">Evidence: {evidence_ids_html(finding.get("evidence_ids", []))} · '
            f"Confidence: {escape(finding['confidence'])}</div></div></article>"
        )
    findings_html = "".join(findings) or render_empty("No reviewed executive findings were supplied.")

    company_cards: list[str] = []
    for company in sorted(companies, key=lambda item: item["display_name"].casefold()):
        company_cards.append(
            f'<a class="card" href="company-{escape(company["id"])}.html">'
            f'<div class="card-title">{escape(company["display_name"])}</div>'
            f'<div class="card-meta">{escape(join_text(company.get("value_chain_roles", [])))}</div>'
            f"<p>{escape(company['inclusion_rationale'])}</p>"
            f'<span class="tag checked">{escape(company["review_status"])}</span> '
            f'<span class="card-meta">Evidence through {escape(company["last_evidence_date"])}</span></a>'
        )
    company_html = "".join(company_cards) or render_empty("No reviewed organizations were supplied.")

    technology_cards: list[str] = []
    for technology in sorted(technologies, key=lambda item: item["name"].casefold()):
        count = len(records_for(records, "technology_ids", technology["id"]))
        technology_cards.append(
            f'<a class="card" href="tech-{escape(technology["id"])}.html">'
            f'<div class="card-title">{escape(technology["name"])}</div>'
            f"<p>{escape(technology['definition'])}</p>"
            f'<span class="tag checked">{escape(technology["review_status"])}</span> '
            f'<span class="card-meta">{count} reviewed records</span></a>'
        )
    technology_html = "".join(technology_cards) or render_empty("No reviewed technology routes were supplied.")

    event_items: list[str] = []
    for event in sorted(events, key=lambda item: item["event_date"], reverse=True):
        inference = optional_text(event.get("analyst_inference"), "event.analyst_inference")
        inference_html = (
            f'<p><span class="tag inference">Analyst inference</span> {escape(inference)}</p>'
            if inference
            else ""
        )
        event_items.append(
            '<article class="event">'
            f'<div class="event-date">{escape(event["event_date"])}</div>'
            f'<div class="event-title">{escape(event["title"])}</div>'
            f"<p>{escape(event['observed_fact'])}</p>{inference_html}"
            f'<div class="card-meta">Sources: {evidence_ids_html(event.get("source_ids", []))} · '
            f"Confidence: {escape(event['confidence'])}</div></article>"
        )
    events_html = "".join(event_items) or render_empty("No reviewed material events were supplied.")

    pub_rows: list[str] = []
    for publication in sorted(publications, key=lambda item: item["published_date"], reverse=True):
        pub_rows.append(
            "<tr>"
            f"<td>{source_link(publication['title'], publication.get('source_url', ''))}</td>"
            f"<td>{escape(join_text(publication.get('authors', [])))}</td>"
            f"<td>{escape(publication['venue'])}</td>"
            f"<td>{escape(publication['published_date'])}</td>"
            f"<td>{escape(publication['abstract_summary'])}</td>"
            f"<td>{escape(publication['review_status'])}</td>"
            "</tr>"
        )
    publications_html = "".join(pub_rows) or '<tr><td colspan="6" class="empty">No reviewed scientific publications were supplied.</td></tr>'

    body = f"""
<section id="coverage">
  <h2>Coverage and calculated statistics</h2>
  <p class="section-deck">Counts are calculated from accepted reviewed arrays; patent count unit: {escape(portal['patent_count_unit'])}.</p>
  <div class="stats">{stats_html}</div>
</section>
<section id="findings"><h2>Executive findings</h2><p class="section-deck">Each finding must cite reviewed record IDs and expose confidence.</p>{findings_html}</section>
<section id="companies"><h2>Monitored organizations</h2><p class="section-deck">Inclusion is evidence-based and does not by itself imply competitive tier or market activity.</p><div class="grid">{company_html}</div></section>
<section id="technologies"><h2>Technology routes</h2><p class="section-deck">Definitions and criteria are reviewed; overlapping tags are permitted when explained.</p><div class="grid">{technology_html}</div></section>
<section id="events"><h2>Material event timeline</h2><p class="section-deck">Observed facts remain separate from analyst inference.</p><div class="timeline">{events_html}</div></section>
<section id="publications"><h2>Scientific and technical publications</h2><div class="table-wrap"><table><caption>Reviewed literature evidence.</caption><thead><tr><th>Publication</th><th>Authors</th><th>Venue</th><th>Date</th><th>Technical summary</th><th>Review</th></tr></thead><tbody>{publications_html}</tbody></table></div></section>
<section id="patents"><h2>Patent evidence preview</h2><p class="section-deck">Patent documents do not establish infringement, validity, freedom to operate, product use, or technical leadership.</p><div class="table-wrap"><table><caption>Latest reviewed patent records; full evidence appears on the patent page.</caption><thead><tr><th>Publication</th><th>Title</th><th>Applicant</th><th>Priority / publication</th><th>Family</th><th>Routes</th><th>Relevance</th><th>Review</th></tr></thead><tbody>{patent_rows(patents[:8], maps['technologies'])}</tbody></table></div><p>{local_link('Open the complete patent evidence page', 'patents.html')}</p></section>
<section id="method"><h2>Method, refresh, and limitations</h2><h3>Scope</h3><p>{escape(portal['scope'])}</p><h3>Methodology</h3><p>{escape(portal['methodology'])}</p><h3>Limitations</h3><p>{escape(portal['limitations'])}</p><p>Rejected records: {len(data['rejections'])}. Search-log entries: {len(data['search_log'])}.</p><div class="notice">Public evidence may omit non-public activity. This portal is not legal, investment, or commercial advice.</div></section>
"""
    metadata = [
        ("Technology domain", portal["technology_domain"]),
        ("Period", f"{portal['period_start']} to {portal['period_end']}"),
        ("Evidence cutoff", portal["evidence_cutoff"]),
        ("Geography / language", f"{join_text(portal['geographies'])} · {join_text(portal['languages'])}"),
    ]
    navigation = [
        ("Coverage", "#coverage"),
        ("Findings", "#findings"),
        ("Organizations", "#companies"),
        ("Technology routes", "#technologies"),
        ("Events", "#events"),
        ("Publications", "#publications"),
        ("Patents", "#patents"),
        ("Method", "#method"),
    ]
    return shell(
        title=portal["title"],
        eyebrow="Technology intelligence · reviewed evidence",
        deck=portal["decision_context"],
        metadata=metadata,
        navigation=navigation,
        body=body,
        footer=f"{portal['title']} · {portal['analyst']} · Evidence cutoff {portal['evidence_cutoff']}",
    )


def record_list(records: list[dict[str, Any]]) -> str:
    if not records:
        return render_empty("No reviewed current-awareness records were supplied for this page.")
    items: list[str] = []
    for record in sorted(records, key=lambda item: item["published_date"], reverse=True):
        title = source_link(record["title"], record.get("source_url", ""))
        items.append(
            '<article class="event">'
            f'<div class="event-date">{escape(record["published_date"])}</div>'
            f'<div class="event-title">{title}</div>'
            f"<p>{escape(record['summary'])}</p>"
            f'<div class="card-meta">{escape(record["source_name"])} · {escape(record["record_type"])} · '
            f"{escape(record['review_status'])} · confidence {escape(record['confidence'])}</div></article>"
        )
    return '<div class="timeline">' + "".join(items) + "</div>"


def render_company_page(
    company: dict[str, Any],
    data: dict[str, Any],
    maps: dict[str, dict[str, dict[str, Any]]],
) -> str:
    portal = data["portal"]
    records = records_for(list(maps["records"].values()), "company_ids", company["id"])
    patents = [
        patent
        for patent in maps["patents"].values()
        if company["id"] in patent.get("company_ids", [])
    ]
    route_names = [
        maps["technologies"][identifier]["name"]
        for identifier in company.get("technology_ids", [])
    ]
    body = f"""
<section>
  <a class="back-link" href="index.html">Back to portal</a>
  <div class="detail-header"><div><h2>{escape(company['display_name'])}</h2><p class="section-deck">{escape(join_text(company.get('value_chain_roles', [])))}</p></div><span class="tag checked">{escape(company['review_status'])}</span></div>
  <div class="two-col"><div class="panel"><h3>Identity and inclusion</h3><p><strong>Legal name:</strong> {escape(text_or(company.get('legal_name')))}</p><p><strong>Aliases:</strong> {escape(join_text(company.get('aliases', [])))}</p><p><strong>Entity type:</strong> {escape(company['entity_type'])}</p><p><strong>Geographies:</strong> {escape(join_text(company.get('geographies', [])))}</p><p>{escape(company['inclusion_rationale'])}</p></div><div class="panel"><h3>Coverage and caveats</h3><p><strong>Evidence:</strong> {evidence_ids_html(company.get('evidence_ids', []))}</p><p><strong>Coverage:</strong> {escape(company['first_evidence_date'])} to {escape(company['last_evidence_date'])}</p><p><strong>Confidence:</strong> {escape(company['confidence'])}</p><p><strong>Relationships:</strong> {escape(text_or(company.get('relationship_notes')))}</p><p><strong>Routes:</strong> {escape(join_text(route_names))}</p></div></div>
</section>
<section><h2>Dated evidence</h2>{record_list(records)}</section>
<section><h2>Associated patent evidence</h2><div class="table-wrap"><table><caption>Records associated under the reviewed mapping; count unit is disclosed on the patent page.</caption><thead><tr><th>Publication</th><th>Title</th><th>Applicant</th><th>Priority / publication</th><th>Family</th><th>Routes</th><th>Relevance</th><th>Review</th></tr></thead><tbody>{patent_rows(patents, maps['technologies'])}</tbody></table></div></section>
<section><h2>Interpretation boundary</h2><p>{escape(text_or(company.get('summary')))}</p><div class="notice">Entity inclusion and patent association do not establish market position, product use, ownership of every record, or competitive tier.</div></section>
"""
    return shell(
        title=f"{company['display_name']} · {portal['technology_domain']}",
        eyebrow="Organization evidence profile",
        deck=company["inclusion_rationale"],
        metadata=[
            ("Evidence cutoff", portal["evidence_cutoff"]),
            ("Review status", company["review_status"]),
            ("Confidence", company["confidence"]),
            ("Current-awareness records", str(len(records))),
        ],
        navigation=[("Portal home", "index.html"), ("Patents", "patents.html")],
        body=body,
        footer=f"{portal['title']} · Organization profile · Evidence cutoff {portal['evidence_cutoff']}",
    )


def render_technology_page(
    technology: dict[str, Any],
    data: dict[str, Any],
    maps: dict[str, dict[str, dict[str, Any]]],
) -> str:
    portal = data["portal"]
    records = records_for(list(maps["records"].values()), "technology_ids", technology["id"])
    patents = [
        patent
        for patent in maps["patents"].values()
        if technology["id"] in patent.get("technology_ids", [])
    ]
    organizations = [
        company
        for company in maps["companies"].values()
        if technology["id"] in company.get("technology_ids", [])
    ]
    org_links = (
        ", ".join(
            local_link(company["display_name"], f"company-{company['id']}.html")
            for company in organizations
        )
        or '<span class="empty">No reviewed organization association supplied.</span>'
    )
    body = f"""
<section><a class="back-link" href="index.html">Back to portal</a><div class="detail-header"><div><h2>{escape(technology['name'])}</h2><p class="section-deck">{escape(technology['definition'])}</p></div><span class="tag checked">{escape(technology['review_status'])}</span></div><div class="two-col"><div class="panel"><h3>Taxonomy boundary</h3><p><strong>Include:</strong> {escape(technology['inclusion_criteria'])}</p><p><strong>Exclude:</strong> {escape(technology['exclusion_criteria'])}</p><p><strong>Synonyms:</strong> {escape(join_text(technology.get('synonyms', [])))}</p><p><strong>Disambiguation:</strong> {escape(join_text(technology.get('disambiguation_terms', [])))}</p></div><div class="panel"><h3>Review context</h3><p><strong>Evidence:</strong> {evidence_ids_html(technology.get('evidence_ids', []))}</p><p><strong>Review date:</strong> {escape(technology['review_date'])}</p><p><strong>Confidence:</strong> {escape(technology['confidence'])}</p><p><strong>Maturity note:</strong> {escape(text_or(technology.get('maturity_note')))}</p><p><strong>Associated organizations:</strong> {org_links}</p></div></div></section>
<section><h2>Dated evidence</h2>{record_list(records)}</section>
<section><h2>Associated patent evidence</h2><div class="table-wrap"><table><caption>Reviewed records tagged to this route.</caption><thead><tr><th>Publication</th><th>Title</th><th>Applicant</th><th>Priority / publication</th><th>Family</th><th>Routes</th><th>Relevance</th><th>Review</th></tr></thead><tbody>{patent_rows(patents, maps['technologies'])}</tbody></table></div></section>
<section><h2>Interpretation boundary</h2><div class="notice">Record volume does not establish technical maturity, route superiority, market adoption, or commercial readiness. Use the stated evidence and framework.</div></section>
"""
    return shell(
        title=f"{technology['name']} · {portal['technology_domain']}",
        eyebrow="Technology-route evidence profile",
        deck=technology["definition"],
        metadata=[
            ("Evidence cutoff", portal["evidence_cutoff"]),
            ("Review status", technology["review_status"]),
            ("Confidence", technology["confidence"]),
            ("Current-awareness records", str(len(records))),
        ],
        navigation=[("Portal home", "index.html"), ("Patents", "patents.html")],
        body=body,
        footer=f"{portal['title']} · Technology route · Evidence cutoff {portal['evidence_cutoff']}",
    )


def render_patents_page(
    data: dict[str, Any],
    maps: dict[str, dict[str, dict[str, Any]]],
) -> str:
    portal = data["portal"]
    patents = list(maps["patents"].values())
    count = calculated_patent_count(patents, portal["patent_count_unit"])
    search_rows: list[str] = []
    for search in maps["search_log"].values():
        search_rows.append(
            "<tr>"
            f"<td>{escape(search['id'])}</td>"
            f"<td>{escape(text_or(search.get('source_or_tool')))}</td>"
            f"<td>{escape(text_or(search.get('searched_at')))}</td>"
            f"<td>{escape(text_or(search.get('query')))}</td>"
            f"<td>{escape(text_or(search.get('deduplication')))}</td>"
            f"<td>{escape(text_or(search.get('limitations')))}</td>"
            "</tr>"
        )
    search_html = "".join(search_rows) or '<tr><td colspan="6" class="empty">No search-log entries were supplied.</td></tr>'
    body = f"""
<section><a class="back-link" href="index.html">Back to portal</a><h2>Patent evidence coverage</h2><p class="section-deck">{count} records under the declared unit: {escape(portal['patent_count_unit'])}.</p><div class="notice">Patent evidence is a technical and bibliographic source. It does not establish infringement, validity, freedom to operate, commercial use, or technical leadership.</div></section>
<section><h2>Search and normalization log</h2><div class="table-wrap"><table><thead><tr><th>ID</th><th>Source/tool</th><th>Searched at</th><th>Query</th><th>Deduplication</th><th>Limits</th></tr></thead><tbody>{search_html}</tbody></table></div></section>
<section><h2>Reviewed patent records</h2><div class="table-wrap"><table><caption>Publication records; aggregate count uses {escape(portal['patent_count_unit'])}.</caption><thead><tr><th>Publication</th><th>Title</th><th>Applicant</th><th>Priority / publication</th><th>Family</th><th>Routes</th><th>Relevance</th><th>Review</th></tr></thead><tbody>{patent_rows(patents, maps['technologies'])}</tbody></table></div></section>
<section><h2>Limitations</h2><p>{escape(portal['limitations'])}</p></section>
"""
    return shell(
        title=f"Patent evidence · {portal['technology_domain']}",
        eyebrow="Patent evidence register",
        deck="Reviewed patent records, documented count unit, search coverage, and interpretation limits.",
        metadata=[
            ("Evidence cutoff", portal["evidence_cutoff"]),
            ("Patent count unit", portal["patent_count_unit"]),
            ("Calculated count", str(count)),
            ("Search-log entries", str(len(maps["search_log"]))),
        ],
        navigation=[("Portal home", "index.html")],
        body=body,
        footer=f"{portal['title']} · Patent evidence · Cutoff {portal['evidence_cutoff']}",
    )


def prepare_output(path: Path, pages: set[str], overwrite: bool) -> Path:
    output = path.expanduser().resolve()
    if output.parent == output:
        fail("Refusing to use a filesystem root as the output directory")
    if output.exists() and output.is_symlink():
        fail("Output directory must not be a symbolic link")
    if output.exists() and not output.is_dir():
        fail("Output path exists and is not a directory")
    if output.exists():
        contents = list(output.iterdir())
        if contents and not overwrite:
            fail("Output directory is not empty; use --overwrite to replace expected portal pages")
        for name in pages:
            candidate = output / name
            if candidate.exists() and (candidate.is_symlink() or not candidate.is_file()):
                fail(f"Expected page path is not a regular file: {candidate}")
    else:
        output.mkdir(parents=True)
    return output


def write_pages(output: Path, pages: dict[str, str]) -> None:
    for name, content in pages.items():
        if Path(name).name != name or not name.endswith(".html"):
            fail(f"Unsafe generated filename: {name}")
        destination = output / name
        destination.write_text(content, encoding="utf-8")


def build_pages(
    data: dict[str, Any],
    maps: dict[str, dict[str, dict[str, Any]]],
) -> dict[str, str]:
    pages = {
        "index.html": render_index(data, maps),
        "patents.html": render_patents_page(data, maps),
    }
    for identifier, company in maps["companies"].items():
        pages[f"company-{identifier}.html"] = render_company_page(company, data, maps)
    for identifier, technology in maps["technologies"].items():
        pages[f"tech-{identifier}.html"] = render_technology_page(technology, data, maps)
    return pages


def verify_local_links(pages: dict[str, str]) -> None:
    known = set(pages)
    href_pattern = re.compile(r'href="([^"]+)"')
    for page_name, content in pages.items():
        for href in href_pattern.findall(content):
            if href.startswith(("https://", "http://", "#")):
                continue
            target = href.split("#", 1)[0]
            if target and target not in known:
                fail(f"{page_name} links to an ungenerated local page: {target}")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        data = read_json(args.data)
        maps = validate_data(data)
        pages = build_pages(data, maps)
        verify_local_links(pages)
        output = prepare_output(args.output, set(pages), args.overwrite)
        write_pages(output, pages)
    except (PortalError, OSError, UnicodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    summary = {
        "success": True,
        "output_dir": str(output),
        "index_html": str(output / "index.html"),
        "generated_files": len(pages),
        "companies": len(maps["companies"]),
        "technologies": len(maps["technologies"]),
        "records": len(maps["records"]),
        "events": len(maps["events"]),
        "publications": len(maps["publications"]),
        "patent_publications": len(maps["patents"]),
        "evidence_cutoff": data["portal"]["evidence_cutoff"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

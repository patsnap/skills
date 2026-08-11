#!/usr/bin/env python3
"""Validate a localized technology-insight HTML report before review release."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


REQUIRED_SECTIONS = [f"s{index}" for index in range(10)]
VERSION = re.compile(r"\bV(\d+\.\d+(?:\.\d+)?)\b")
ISO_DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
PLACEHOLDER = re.compile(
    r"\[\s*(?:FILL|TODO|TBD|PLACEHOLDER|INSERT)[^\]]*\]|"
    r"<!--\s*(?:FILL|TODO|TBD)[\s\S]*?-->|"
    r"\b(?:XXXX|TBD|TO BE COMPLETED)\b|"
    r"\bEDITORIAL INSTRUCTION\b",
    re.IGNORECASE,
)
LEGACY_OR_UNSAFE = re.compile(
    r"open\.zhihuiya\.com|www\.zhihuiya\.com|"
    r"file:///|" + r"C:" + r"\\Users\\" + r"|/" + r"Users/[^/]+/|/" + r"home/[^/]+/|"
    r"linear-gradient|radial-gradient|conic-gradient|"
    r"innerHTML|outerHTML|insertAdjacentHTML|document\.write",
    re.IGNORECASE,
)
OVERCLAIMS = (
    "no infringement risk",
    "will not infringe",
    "non-infringing",
    "completely safe",
    "freedom to operate confirmed",
    "global white space confirmed",
    "no patents exist",
)


@dataclass
class ParsedReport:
    ids: list[str] = field(default_factory=list)
    section_ids: list[str] = field(default_factory=list)
    links: list[str] = field(default_factory=list)
    scripts: list[dict[str, str]] = field(default_factory=list)
    stylesheets: list[str] = field(default_factory=list)
    tables: list[tuple[int, list[int]]] = field(default_factory=list)
    footer_text: str = ""
    title_text: str = ""
    meta: dict[str, str] = field(default_factory=dict)


class ReportParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.report = ParsedReport()
        self._in_footer = False
        self._in_title = False
        self._table_depth = 0
        self._header_cells = 0
        self._current_cells = 0
        self._row_cells: list[int] = []
        self._in_head_row = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        identifier = values.get("id")
        if identifier:
            self.report.ids.append(identifier)
            if tag == "section":
                self.report.section_ids.append(identifier)
        if tag == "a" and "href" in values:
            self.report.links.append(values["href"])
        if tag == "script":
            self.report.scripts.append(values)
        if tag == "link" and values.get("rel", "").casefold() == "stylesheet":
            self.report.stylesheets.append(values.get("href", ""))
        if tag == "meta" and values.get("name"):
            self.report.meta[values["name"].casefold()] = values.get("content", "")
        if tag == "footer":
            self._in_footer = True
        if tag == "title":
            self._in_title = True
        if tag == "table":
            self._table_depth += 1
            if self._table_depth == 1:
                self._header_cells = 0
                self._row_cells = []
        if self._table_depth == 1 and tag == "thead":
            self._in_head_row = True
        if self._table_depth == 1 and tag == "tr":
            self._current_cells = 0
        if self._table_depth == 1 and tag in {"th", "td"}:
            self._current_cells += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "footer":
            self._in_footer = False
        if tag == "title":
            self._in_title = False
        if self._table_depth == 1 and tag == "tr" and self._current_cells:
            if self._in_head_row:
                self._header_cells = max(self._header_cells, self._current_cells)
            else:
                self._row_cells.append(self._current_cells)
        if self._table_depth == 1 and tag == "thead":
            self._in_head_row = False
        if tag == "table" and self._table_depth:
            if self._table_depth == 1:
                self.report.tables.append((self._header_cells, list(self._row_cells)))
            self._table_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._in_footer:
            self.report.footer_text += " " + data
        if self._in_title:
            self.report.title_text += data


@dataclass
class Check:
    name: str
    passed: bool
    detail: str


def parse_report(content: str) -> ParsedReport:
    parser = ReportParser()
    try:
        parser.feed(content)
        parser.close()
    except Exception as error:
        raise ValueError(f"HTML parser failed: {error}") from error
    return parser.report


def check_structure(report: ParsedReport) -> Check:
    duplicates = {key: count for key, count in Counter(report.ids).items() if count > 1}
    missing = [identifier for identifier in REQUIRED_SECTIONS if identifier not in report.section_ids]
    order = [identifier for identifier in report.section_ids if identifier in REQUIRED_SECTIONS]
    errors = []
    if duplicates:
        errors.append(f"duplicate IDs: {duplicates}")
    if missing:
        errors.append("missing sections: " + ", ".join(missing))
    if order != REQUIRED_SECTIONS:
        errors.append(f"section order is {order}, expected {REQUIRED_SECTIONS}")
    return Check("HTML structure", not errors, "; ".join(errors) or "s0–s9 present in order; IDs unique")


def check_versions_and_dates(content: str, report: ParsedReport) -> Check:
    versions = VERSION.findall(content)
    unique = sorted(set(versions))
    dates = ISO_DATE.findall(content)
    errors = []
    if len(unique) != 1:
        errors.append(f"expected one version value, found {unique}")
    elif len(versions) < 3:
        errors.append(f"version V{unique[0]} appears {len(versions)} times; expected title, metadata, and footer")
    if not dates:
        errors.append("no ISO date found")
    if not VERSION.search(report.footer_text):
        errors.append("footer has no version")
    if not ISO_DATE.search(report.footer_text):
        errors.append("footer has no ISO evidence-cutoff/report date")
    metadata_version = report.meta.get("report-version", "")
    if unique and metadata_version != f"V{unique[0]}":
        errors.append(f"metadata version {metadata_version!r} does not match V{unique[0]}")
    if unique and not VERSION.search(report.title_text):
        errors.append("title has no report version")
    report_date = report.meta.get("report-date", "")
    cutoff = report.meta.get("evidence-cutoff", "")
    for label, value in (("report-date", report_date), ("evidence-cutoff", cutoff)):
        try:
            date.fromisoformat(value)
        except ValueError:
            errors.append(f"{label} is not a valid ISO date: {value!r}")
    if report_date and report_date not in report.footer_text:
        errors.append("metadata report-date does not match footer")
    if cutoff and cutoff not in report.footer_text:
        errors.append("metadata evidence-cutoff does not match footer")
    return Check("Version and date consistency", not errors, "; ".join(errors) or "one version and ISO-dated footer found")


def check_tables(report: ParsedReport) -> Check:
    errors = []
    for index, (headers, rows) in enumerate(report.tables, start=1):
        if headers == 0:
            errors.append(f"table {index} has no header cells")
        mismatches = [row for row in rows if row != headers]
        if mismatches:
            errors.append(f"table {index} has row widths {mismatches}, expected {headers}")
    return Check("Table integrity", not errors, "; ".join(errors) or f"{len(report.tables)} tables have consistent row widths")


def check_links_and_runtime(report: ParsedReport) -> Check:
    errors = []
    for href in report.links:
        if href.startswith("#"):
            if href[1:] and href[1:] not in report.ids:
                errors.append(f"unresolved local anchor: {href}")
            continue
        parsed = urlparse(href)
        if parsed.scheme not in {"http", "https", "mailto"}:
            errors.append(f"unsafe or nonportable link: {href}")
    for script in report.scripts:
        if script.get("src"):
            errors.append(f"external script: {script['src']}")
        else:
            errors.append("inline script is not allowed in the localized static report")
    if report.stylesheets:
        errors.extend(f"external stylesheet: {href}" for href in report.stylesheets)
    return Check("Links and runtime", not errors, "; ".join(errors) or "links are portable; no script or external stylesheet")


def check_placeholders_and_legacy(content: str) -> Check:
    errors = []
    placeholder = PLACEHOLDER.search(content)
    if placeholder:
        line = content[: placeholder.start()].count("\n") + 1
        errors.append(f"placeholder at line {line}: {placeholder.group(0)[:70]!r}")
    legacy = LEGACY_OR_UNSAFE.search(content)
    if legacy:
        line = content[: legacy.start()].count("\n") + 1
        errors.append(f"legacy/unsafe content at line {line}: {legacy.group(0)!r}")
    return Check("Release cleanliness", not errors, "; ".join(errors) or "no placeholders, legacy domains, local paths, gradients, or unsafe DOM markers")


def check_legal_language(content: str) -> Check:
    lowered = re.sub(r"<[^>]+>", " ", content).casefold()
    hits = [phrase for phrase in OVERCLAIMS if phrase in lowered]
    disclaimer = "not legal advice" in lowered and "patent professional" in lowered
    errors = []
    if hits:
        errors.append("unsupported legal overclaims: " + ", ".join(hits))
    if not disclaimer:
        errors.append("missing not-legal-advice and patent-professional boundary")
    return Check("Legal-language boundary", not errors, "; ".join(errors) or "no listed overclaim; legal boundary present")


def check_metadata(report: ParsedReport) -> Check:
    required = {"report-version", "report-date", "evidence-cutoff", "review-status"}
    missing = sorted(required - set(report.meta))
    return Check("Machine-readable metadata", not missing, "missing: " + ", ".join(missing) if missing else "required metadata present")


def run_checks(content: str) -> list[Check]:
    report = parse_report(content)
    return [
        check_structure(report),
        check_versions_and_dates(content, report),
        check_tables(report),
        check_links_and_runtime(report),
        check_placeholders_and_legacy(content),
        check_legal_language(content),
        check_metadata(report),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a technology-insight HTML report")
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    try:
        content = args.report.read_text(encoding="utf-8")
        checks = run_checks(content)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    print(f"Technology Insight Report QA: {args.report}")
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"[{status}] {check.name}: {check.detail}")
    passed = sum(check.passed for check in checks)
    print(f"Result: {passed}/{len(checks)} checks passed")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())

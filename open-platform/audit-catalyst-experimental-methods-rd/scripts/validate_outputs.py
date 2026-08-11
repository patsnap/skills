#!/usr/bin/env python3
"""Validate catalyst-method audit outputs with the Python standard library."""
from __future__ import annotations

import json
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

HTML_NAME = "Catalyst Preparation and Evaluation Method Audit Report.html"
DOCX_NAME = "Catalyst Preparation and Evaluation Method Audit Report.docx"
REQUIRED_SECTIONS = [
    "Material and classification",
    "Overall audit conclusion",
    "Priority issues",
    "Dimension-level findings",
    "Preparation-step register",
    "Sample and variable register",
    "Required additions",
]


def read_docx_text(path: Path) -> str:
    """Extract paragraph text from a valid DOCX package."""
    namespace = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    with zipfile.ZipFile(path) as archive:
        xml_data = archive.read("word/document.xml")
    root = ET.fromstring(xml_data)
    chunks: list[str] = []
    for paragraph in root.findall(".//w:p", namespace):
        text = "".join((node.text or "") for node in paragraph.findall(".//w:t", namespace)).strip()
        if text:
            chunks.append(text)
    return "\n".join(chunks)


def require_regular_file(path: Path) -> None:
    if not path.exists() or not path.is_file() or path.is_symlink():
        raise SystemExit(f"Missing or unsafe output file: {path}")
    if path.stat().st_size == 0:
        raise SystemExit(f"Output file is empty: {path}")


def main() -> int:
    output_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("outputs")
    html_path = output_dir / HTML_NAME
    docx_path = output_dir / DOCX_NAME
    context_path = output_dir / "report_context.json"
    for path in (html_path, docx_path, context_path):
        require_regular_file(path)

    context = json.loads(context_path.read_text(encoding="utf-8"))
    html_text = html_path.read_text(encoding="utf-8", errors="strict")
    docx_text = read_docx_text(docx_path)

    for section in REQUIRED_SECTIONS:
        if section not in html_text:
            raise SystemExit(f"HTML is missing section: {section}")
        if section not in docx_text:
            raise SystemExit(f"Word report is missing section: {section}")

    summary = context["computed_summary"]
    html_total = f"Critical issues: {summary['high_count']}"
    word_total = (
        f"Critical issues: {summary['high_count']}; "
        f"material issues: {summary['medium_count']}; "
        f"documentation issues: {summary['low_count']}"
    )
    if html_total not in html_text:
        raise SystemExit("HTML issue totals do not match report_context.json")
    if word_total not in docx_text:
        raise SystemExit("Word issue totals do not match report_context.json")

    for malformed in ("{'", "priority':", "None", "Not specified\nAudit mode: Not specified"):
        if malformed in html_text or malformed in docx_text:
            raise SystemExit(f"Report contains unrendered content: {malformed}")

    print("Output validation passed: HTML, Word, and context are present and internally consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

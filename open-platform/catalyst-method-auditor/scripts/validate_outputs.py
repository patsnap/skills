#!/usr/bin/env python3
"""Validate catalyst-method-auditor outputs without third-party dependencies."""
from __future__ import annotations

import json
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

HTML_NAME = "催化剂制备与评价方案审核报告.html"
DOCX_NAME = "催化剂制备与评价方案审核报告.docx"
REQUIRED_SECTIONS = ["审核对象与材料性质", "总体审核意见", "重点问题清单", "分项审核结果", "制备步骤核对表", "样品与变量关系核对表", "修改建议"]


def read_docx_text(path: Path) -> str:
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    with zipfile.ZipFile(path) as zf:
        xml_data = zf.read("word/document.xml")
    root = ET.fromstring(xml_data)
    chunks = []
    for para in root.findall(".//w:p", ns):
        text = "".join((n.text or "") for n in para.findall(".//w:t", ns)).strip()
        if text:
            chunks.append(text)
    return "\n".join(chunks)


def main() -> int:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("outputs")
    html_path = out / HTML_NAME
    docx_path = out / DOCX_NAME
    context_path = out / "report_context.json"
    missing = [str(p) for p in [html_path, docx_path, context_path] if not p.exists()]
    if missing:
        raise SystemExit(f"缺少输出文件：{missing}")
    context = json.loads(context_path.read_text(encoding="utf-8"))
    html_text = html_path.read_text(encoding="utf-8", errors="ignore")
    docx_text = read_docx_text(docx_path)
    for sec in REQUIRED_SECTIONS:
        if sec not in html_text:
            raise SystemExit(f"HTML 缺少章节：{sec}")
        if sec not in docx_text:
            raise SystemExit(f"Word 缺少章节：{sec}")
    summary = context["computed_summary"]
    if f"关键问题：{summary['high_count']} 项" not in html_text:
        raise SystemExit("HTML 问题统计与 context 不一致")
    expected_docx = f"关键问题 {summary['high_count']} 项，重要问题 {summary['medium_count']} 项，一般问题 {summary['low_count']} 项"
    if expected_docx not in docx_text:
        raise SystemExit("Word 问题统计与 context 不一致")
    for bad in ["{'", "priority':", "None"]:
        if bad in html_text or bad in docx_text:
            raise SystemExit(f"报告中出现异常未渲染内容：{bad}")
    print("输出校验通过：HTML、Word、context 文件齐全，章节和统计一致。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

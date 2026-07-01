#!/usr/bin/env python3
"""Validate fto-review HTML reports.

This is the built-in optional harness module for the fto-review skill. It is
not called automatically by scripts/generate_report.py.

Outputs:
  - fto_review_harness_result.json
  - fto_review_harness_report.html

Only Python standard library is used.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


EXPECTED_SECTIONS = [
    "报告头部与基本信息",
    "执行摘要",
    "三层审核总览",
    "四维度评分",
    "独立检索验证与漏检核查",
    "检索主题符合性评价",
    "检索范围全面性评价",
    "技术比对分析严谨性评价",
    "高风险专利数量及清单",
    "中风险专利数量及清单",
    "低风险专利数量及清单",
    "应对措施明确具体可靠性评价",
    "风险规避建议清单",
    "综合问题清单",
    "审核结论与整改行动",
    "审核边界与免责声明",
]

REQUIRED_CSS_TOKENS = [
    ".card",
    ".card.verify",
    ".card.mitigation",
    ".chapter-no",
    ".grade-excellent",
    ".grade-good",
    ".grade-pass",
    ".grade-warning",
    ".grade-fail",
    ".grade-none",
    ".recall-ok",
    ".recall-low",
    ".recall-bad",
    ".recall-none",
    ".risk-high",
    ".risk-medium",
    ".risk-normal",
    ".pct-0",
    ".pct-100",
]

DIMENSION_NAMES = ["搜索策略质量", "专利分析深度", "法律意见专业性", "文档记录完整性"]
LAYER_NAMES = ["事实层", "法律判断层", "决策可用层"]

GRADE_RANGES = {
    "优秀": (90, 100),
    "良好": (80, 89.999),
    "合格": (70, 79.999),
    "需改进": (60, 69.999),
    "不合格": (0, 59.999),
}

FORBIDDEN_PATTERNS = [
    ("FORBID-ABSOLUTE-SAFE", r"绝对安全|无任何风险|完全无风险|保证不侵权", "不得出现绝对安全或保证不侵权表述"),
    (
        "FORBID-IP-OVERREACH",
        r"(已|已全部|已经|全面|完全)(覆盖|排除).{0,20}(商标|版权|商业秘密|监管合规|产品安全).{0,20}(风险|问题)",
        "不得把专利FTO扩大为所有非专利风险全覆盖",
    ),
]


@dataclass
class Check:
    id: str
    group: str
    name: str
    status: str
    severity: str
    evidence: str = ""
    suggestion: str = ""


def strip_tags(fragment: str) -> str:
    text = re.sub(r"<[^>]+>", " ", fragment)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def extract_style(html_text: str) -> tuple[str, str]:
    m = re.search(
        r"<style\b(?P<attrs>[^>]*)id=[\"']fto-fixed-css[\"'](?P<attrs2>[^>]*)>(?P<css>.*?)</style>",
        html_text,
        flags=re.I | re.S,
    )
    if not m:
        return "", ""
    attrs = (m.group("attrs") or "") + " " + (m.group("attrs2") or "")
    return attrs, m.group("css") or ""


def extract_h2_titles(html_text: str) -> list[str]:
    titles = []
    for body in re.findall(r"<h2[^>]*>(.*?)</h2>", html_text, flags=re.I | re.S):
        text = strip_tags(body)
        text = re.sub(r"^\d+\.\s*", "", text)
        titles.append(text)
    return titles


def find_section_body(html_text: str, title: str) -> str:
    pattern = (
        r"<section\b[^>]*>\s*<h2[^>]*>.*?"
        + re.escape(title)
        + r".*?</h2>(?P<body>.*?)</section>"
    )
    m = re.search(pattern, html_text, flags=re.I | re.S)
    return m.group("body") if m else ""


def add(checks: list[Check], id_: str, group: str, name: str, ok: bool, fail_severity: str,
        evidence: str = "", suggestion: str = "") -> None:
    checks.append(
        Check(
            id=id_,
            group=group,
            name=name,
            status="pass" if ok else fail_severity,
            severity="info" if ok else fail_severity,
            evidence=evidence,
            suggestion=suggestion,
        )
    )


def extract_score(text: str) -> float | None:
    m = re.search(r"(\d+(?:\.\d+)?)\s*/\s*100", text)
    if m:
        return float(m.group(1))
    return None


def extract_grade(text: str) -> str | None:
    m = re.search(r"质量等级[:：]\s*(优秀|良好|合格|需改进|不合格|未评分)", text)
    return m.group(1) if m else None


def grade_matches(score: float | None, grade: str | None) -> bool:
    if score is None or not grade or grade == "未评分":
        return True
    lo, hi = GRADE_RANGES.get(grade, (-1, -1))
    return lo <= score <= hi


def parse_count_near(text: str, label: str) -> int | None:
    m = re.search(re.escape(label) + r".{0,20}?(\d+)", text)
    return int(m.group(1)) if m else None


def validate(html_path: Path, expected_css_sha256: str | None = None) -> dict:
    html_text = html_path.read_text(encoding="utf-8", errors="replace")
    plain_text = strip_tags(html_text)
    checks: list[Check] = []

    # STRUCTURE
    add(checks, "STRUCT-001", "STRUCTURE", "HTML doctype exists", "<!doctype html" in html_text.lower(), "fail")
    titles = extract_h2_titles(html_text)
    add(
        checks,
        "STRUCT-002",
        "STRUCTURE",
        "Fixed 16-section order",
        titles[: len(EXPECTED_SECTIONS)] == EXPECTED_SECTIONS and len(titles) == len(EXPECTED_SECTIONS),
        "fail",
        evidence=f"found={titles}",
        suggestion="Regenerate report with the fixed fto-review HTML template.",
    )
    for idx, title in enumerate(EXPECTED_SECTIONS, 1):
        add(
            checks,
            f"STRUCT-{idx+10:03d}",
            "STRUCTURE",
            f"Section {idx}: {title}",
            title in titles,
            "fail",
        )
    add(checks, "STRUCT-040", "STRUCTURE", "At least five tables exist", len(re.findall(r"<table\b", html_text, re.I)) >= 5, "warn")

    # STYLE
    style_attrs, css = extract_style(html_text)
    add(checks, "STYLE-001", "STYLE", "Embedded fixed CSS style block", bool(css), "fail")
    add(checks, "STYLE-002", "STYLE", "CSS version marker v7.1-fixed", "v7.1-fixed" in style_attrs, "fail", evidence=style_attrs)
    add(checks, "STYLE-003", "STYLE", "No inline style attributes", not re.search(r"\sstyle\s*=", html_text, re.I), "fail")
    add(checks, "STYLE-004", "STYLE", "No external stylesheet link", not re.search(r"<link\b[^>]+stylesheet", html_text, re.I), "fail")
    missing_tokens = [token for token in REQUIRED_CSS_TOKENS if token not in css]
    add(
        checks,
        "STYLE-005",
        "STYLE",
        "Required fixed CSS class families",
        not missing_tokens,
        "fail",
        evidence=", ".join(missing_tokens),
    )
    css_hash = hashlib.sha256(css.encode("utf-8")).hexdigest() if css else ""
    if expected_css_sha256:
        add(
            checks,
            "STYLE-006",
            "STYLE",
            "CSS SHA-256 matches expected baseline",
            css_hash == expected_css_sha256,
            "fail",
            evidence=f"actual={css_hash}",
        )
    else:
        checks.append(Check("STYLE-006", "STYLE", "CSS SHA-256 recorded", "pass", "info", evidence=css_hash))

    # CONTENT
    for label in ["被审核报告", "目标市场", "审核场景", "审核日期"]:
        add(checks, f"CONTENT-META-{label}", "CONTENT", f"Metadata present: {label}", label in plain_text, "fail")
    missing_dims = [name for name in DIMENSION_NAMES if name not in plain_text]
    add(checks, "CONTENT-001", "CONTENT", "All four scoring dimensions present", not missing_dims, "fail", evidence=", ".join(missing_dims))
    score = extract_score(plain_text)
    grade = extract_grade(plain_text)
    add(checks, "CONTENT-002", "CONTENT", "Score and grade are consistent", grade_matches(score, grade), "fail", evidence=f"score={score}, grade={grade}")
    if score is None:
        add(checks, "CONTENT-003", "CONTENT", "Total score populated", False, "warn", "No numeric /100 total score found")
    else:
        add(checks, "CONTENT-003", "CONTENT", "Total score populated", True, "warn", str(score))

    high_section = strip_tags(find_section_body(html_text, "高风险专利数量及清单"))
    mitigation_section = strip_tags(find_section_body(html_text, "风险规避建议清单"))
    high_count = parse_count_near(high_section, "高风险")
    has_high_patent = bool(re.search(r"(CN|US|EP|JP|WO|DE)\w{3,}", high_section))
    if (high_count and high_count > 0) or has_high_patent:
        add(
            checks,
            "CONTENT-004",
            "CONTENT",
            "High-risk patents have mitigation discussion",
            "待填写" not in mitigation_section and "原报告未提供" not in mitigation_section,
            "fail",
            suggestion="Provide concrete mitigation paths for every high-risk patent.",
        )
    else:
        add(checks, "CONTENT-004", "CONTENT", "High-risk mitigation consistency", True, "fail")

    # METHODOLOGY
    missing_layers = [layer for layer in LAYER_NAMES if layer not in plain_text]
    add(checks, "METH-001", "METHODOLOGY", "Three-layer methodology present", not missing_layers, "fail", evidence=", ".join(missing_layers))
    method_terms = ["目标市场", "法律状态", "专利族", "权利要求", "置信度", "风险边界"]
    missing_terms = [term for term in method_terms if term not in plain_text]
    add(checks, "METH-002", "METHODOLOGY", "Key methodology terms covered", not missing_terms, "warn", evidence=", ".join(missing_terms))

    # VERIFICATION LOGIC
    verification_section = strip_tags(find_section_body(html_text, "独立检索验证与漏检核查"))
    says_not_done = "未完成独立检索验证" in verification_section or "未验证" in verification_section
    has_numeric_recall = bool(re.search(r"原报告召回率.{0,30}\d+(?:\.\d+)?%", verification_section))
    if says_not_done:
        add(checks, "VERIFY-001", "CONTENT", "No numeric recall when verification not completed", not has_numeric_recall, "fail")
    else:
        add(checks, "VERIFY-001", "CONTENT", "Verification status/recall consistency", True, "fail")
    if "已完成独立检索验证" in verification_section:
        required_evidence = ["原报告专利池", "独立检索专利池", "重叠数量", "Chapman"]
        missing_evidence = [x for x in required_evidence if x not in verification_section]
        add(checks, "VERIFY-002", "CONTENT", "Completed verification has required evidence", not missing_evidence, "fail", evidence=", ".join(missing_evidence))
    else:
        add(checks, "VERIFY-002", "CONTENT", "Completed verification evidence not required", True, "fail")

    # FORBIDDEN
    for id_, pattern, name in FORBIDDEN_PATTERNS:
        match = re.search(pattern, plain_text)
        if id_ == "FORBID-IP-OVERREACH" and match:
            context = plain_text[max(0, match.start() - 20): match.end() + 20]
            if any(marker in context for marker in ["不应推定", "不覆盖", "未覆盖", "不等于", "除非报告另有分析"]):
                match = None
        add(checks, id_, "FORBIDDEN", name, not match, "fail", evidence=match.group(0) if match else "")
    if "直接通过" in plain_text and any(term in plain_text for term in ["目标市场</td><td>未填写", "目标市场 未填写"]):
        add(checks, "FORBID-PASS-NO-MARKET", "FORBIDDEN", "No direct pass when target market is missing", False, "fail")
    else:
        add(checks, "FORBID-PASS-NO-MARKET", "FORBIDDEN", "No direct pass when target market is missing", True, "fail")

    counts = {"pass": 0, "warn": 0, "fail": 0}
    for c in checks:
        counts[c.status] = counts.get(c.status, 0) + 1
    overall = "fail" if counts["fail"] else "warn" if counts["warn"] else "pass"
    total = len(checks)
    score_value = round((counts["pass"] + 0.5 * counts["warn"]) / total * 100, 1) if total else 0

    return {
        "status": overall,
        "score": score_value,
        "summary": counts,
        "input": str(html_path),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "css_sha256": css_hash,
        "checks": [asdict(c) for c in checks],
    }


def render_html(result: dict) -> str:
    css_path = Path(__file__).parent.parent / "assets" / "harness_report.css"
    css = css_path.read_text(encoding="utf-8") if css_path.exists() else ""
    rows = []
    for c in result["checks"]:
        rows.append(
            f"<tr class='{html.escape(c['status'])}'>"
            f"<td><code>{html.escape(c['id'])}</code></td>"
            f"<td>{html.escape(c['group'])}</td>"
            f"<td class='status-{html.escape(c['status'])}'>{html.escape(c['status'])}</td>"
            f"<td>{html.escape(c['name'])}</td>"
            f"<td>{html.escape(c.get('evidence') or '')}</td>"
            f"<td>{html.escape(c.get('suggestion') or '')}</td>"
            "</tr>"
        )
    status = result["status"]
    summary = result["summary"]
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>FTO Review Harness Report</title>
<style>{css}</style>
</head>
<body>
<header class="hero">
  <h1>FTO Review Harness Report</h1>
  <div>Input: {html.escape(result['input'])}</div>
</header>
<main class="wrap">
  <section class="summary">
    <div class="tile"><span>Status</span><strong class="status-{html.escape(status)}">{html.escape(status)}</strong></div>
    <div class="tile"><span>Score</span><strong>{result['score']}</strong></div>
    <div class="tile"><span>Pass</span><strong class="status-pass">{summary.get('pass', 0)}</strong></div>
    <div class="tile"><span>Warn / Fail</span><strong><span class="status-warn">{summary.get('warn', 0)}</span> / <span class="status-fail">{summary.get('fail', 0)}</span></strong></div>
  </section>
  <section class="card">
    <h2>Run Metadata</h2>
    <table>
      <tr><th>Field</th><th>Value</th></tr>
      <tr><td>Generated at</td><td>{html.escape(result['generated_at'])}</td></tr>
      <tr><td>CSS SHA-256</td><td><code>{html.escape(result.get('css_sha256') or '')}</code></td></tr>
    </table>
  </section>
  <section class="card">
    <h2>Checks</h2>
    <table>
      <tr><th>ID</th><th>Group</th><th>Status</th><th>Name</th><th>Evidence</th><th>Suggestion</th></tr>
      {''.join(rows)}
    </table>
  </section>
</main>
</body>
</html>"""


def write_outputs(result: dict, out_dir: Path) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "fto_review_harness_result.json"
    html_path = out_dir / "fto_review_harness_report.html"
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    html_path.write_text(render_html(result), encoding="utf-8")
    return json_path, html_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate fto-review HTML report.")
    parser.add_argument("html_report", help="Path to fto-review HTML report")
    parser.add_argument("--out-dir", default=None, help="Output directory for harness reports")
    parser.add_argument("--expected-css-sha256", default=None, help="Expected SHA-256 of embedded fixed CSS")
    args = parser.parse_args()

    html_path = Path(args.html_report).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve() if args.out_dir else html_path.parent / "harness_output"

    result = validate(html_path, args.expected_css_sha256)
    json_path, report_path = write_outputs(result, out_dir)

    print(f"status={result['status']} score={result['score']}")
    print(f"json={json_path}")
    print(f"html={report_path}")
    return 1 if result["status"] == "fail" else 0


if __name__ == "__main__":
    raise SystemExit(main())

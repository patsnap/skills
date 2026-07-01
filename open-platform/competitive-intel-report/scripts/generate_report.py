#!/usr/bin/env python3
"""
competitive-intel-report — V12 报告生成脚本
将 template_v12.html 中的占位公司名替换为用户指定内容，输出新报告。
"""
import os
import sys
import re
from pathlib import Path
from datetime import datetime

# ── 参数读取 ──────────────────────────────────────────────
our_company      = os.environ.get("OUR_COMPANY",       "海程新材料有限公司")
our_short        = os.environ.get("OUR_COMPANY_SHORT",  "海程")
our_products     = os.environ.get("OUR_PRODUCTS",       "Baffle / SNS")
competitor_a1    = os.environ.get("COMPETITOR_A1",      "Zephyros / L&L Products")
competitor_a2    = os.environ.get("COMPETITOR_A2",      "Sika AG")
competitor_a3    = os.environ.get("COMPETITOR_A3",      "Henkel AG")
competitors_b    = os.environ.get("COMPETITORS_B",      "BASF / Dow / LANXESS / Sonderhoff")
industry         = os.environ.get("INDUSTRY",           "汽车声学密封与结构增强")
report_period    = os.environ.get("REPORT_PERIOD",      datetime.now().strftime("%YQ%q" if hasattr(datetime,'quarter') else "%Y"))
output_path      = os.environ.get("OUTPUT_PATH",        "")

# ── 模板路径 ──────────────────────────────────────────────
script_dir = Path(__file__).parent
template_path = script_dir.parent / "references" / "template_v12.html"

if not template_path.exists():
    print(f"❌ 模板文件不存在: {template_path}", file=sys.stderr)
    sys.exit(1)

html = template_path.read_text(encoding="utf-8")

# ── 替换占位符 ─────────────────────────────────────────────
replacements = {
    "海程新材料有限公司": our_company,
    "海程新材料":         our_company,
    "海程":               our_short,
    "Baffle / SNS":       our_products,
    "Zephyros / L&L Products": competitor_a1,
    "Zephyros/L&L":       competitor_a1,
    "Sika AG":            competitor_a2,
    "Henkel AG":          competitor_a3,
    "BASF / Dow / LANXESS / Sonderhoff": competitors_b,
    "汽车声学密封与结构增强": industry,
    "2026Q2":             report_period,
}

for old, new in replacements.items():
    if new and new != old:
        html = html.replace(old, new)

# ── 写出报告 ───────────────────────────────────────────────
if not output_path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path(os.environ.get("EUREKA_PYTHON_OUTPUT_DIR", "."))
    output_path = str(out_dir / f"competitive_intel_{our_short}_{ts}.html")

out = Path(output_path)
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(html, encoding="utf-8")

print(f"✅ 报告已生成: {out}")
print(f"   公司: {our_company} ({our_short})")
print(f"   产品: {our_products}")
print(f"   A级竞品: {competitor_a1} / {competitor_a2} / {competitor_a3}")
print(f"   B级竞品: {competitors_b}")
print(f"   行业: {industry} | 报告期: {report_period}")

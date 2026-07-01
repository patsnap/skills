#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_report.py
竞争对手专利布局策略报告生成器
将分析结论数据渲染为 HTML，再通过 weasyprint 转换为 PDF。
用法:
    python generate_report.py --data-path <analysis.json> --output-path <report.pdf>
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(description="生成竞争对手专利布局 PDF 报告")
    parser.add_argument("--data-path", required=True, help="分析数据 JSON 文件路径")
    parser.add_argument("--output-path", required=True, help="输出 PDF 文件路径")
    return parser.parse_args()


# ---------------------------------------------------------------------------
# HTML 模板渲染
# ---------------------------------------------------------------------------

STYLE = """
<style>
  body { font-family: 'Noto Sans CJK SC', 'Source Han Sans CN', Arial, sans-serif;
         margin: 40px; color: #222; font-size: 14px; line-height: 1.7; }
  h1   { font-size: 22px; color: #1a3a6b; border-bottom: 2px solid #1a3a6b;
         padding-bottom: 6px; margin-top: 32px; }
  h2   { font-size: 17px; color: #2055a4; margin-top: 24px; }
  h3   { font-size: 14px; color: #333; margin-top: 16px; }
  table{ border-collapse: collapse; width: 100%; margin: 12px 0; }
  th   { background: #2055a4; color: #fff; padding: 6px 10px; text-align: left; }
  td   { border: 1px solid #ccc; padding: 5px 10px; vertical-align: top; }
  tr:nth-child(even) td { background: #f4f7fb; }
  .badge-core  { background:#e8f4e8; color:#1a6b1a; border-radius:4px;
                 padding:1px 6px; font-size:12px; }
  .badge-periph{ background:#fff4e0; color:#8a5200; border-radius:4px;
                 padding:1px 6px; font-size:12px; }
  .summary-box { background:#f0f4ff; border-left:4px solid #2055a4;
                 padding:12px 16px; margin:16px 0; border-radius:4px; }
  .warn        { background:#fff8e1; border-left:4px solid #f9a825;
                 padding:10px 14px; margin:12px 0; border-radius:4px; }
  .heat-high   { background:#d32f2f; color:#fff; }
  .heat-mid    { background:#f57c00; color:#fff; }
  .heat-low    { background:#388e3c; color:#fff; }
  footer       { font-size:11px; color:#888; margin-top:40px;
                 border-top:1px solid #ddd; padding-top:8px; }
</style>
"""


def heat_class(count: int, max_count: int) -> str:
    if max_count == 0:
        return ""
    ratio = count / max_count
    if ratio >= 0.6:
        return "heat-high"
    if ratio >= 0.3:
        return "heat-mid"
    return "heat-low"


def render_html(data: dict) -> str:
    competitor   = data.get("competitor", "未知公司")
    technology   = data.get("technology", "未知技术")
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    total_patents= data.get("total_patents", 0)
    market_scope = ", ".join(data.get("market_scope", ["全球"]))

    # --- 执行摘要 ---
    exec_summary = data.get("exec_summary", "")

    # --- 技术框架 ---
    tech_framework = data.get("tech_framework", [])
    tf_rows = "".join(
        f"<tr><td>{i+1}</td><td>{t.get('name','')}</td><td>{t.get('description','')}</td></tr>"
        for i, t in enumerate(tech_framework)
    )

    # --- 专利总览：市场分布 ---
    market_dist = data.get("market_distribution", {})
    market_rows = "".join(
        f"<tr><td>{mkt}</td><td>{cnt}</td></tr>"
        for mkt, cnt in sorted(market_dist.items(), key=lambda x: -x[1])
    )

    # --- 重点专利清单 ---
    top_patents = data.get("top_patents", [])
    patent_rows = ""
    for p in top_patents:
        layout_type = p.get("layout_type", "外围")
        badge_cls   = "badge-core" if layout_type == "核心" else "badge-periph"
        patent_rows += (
            f"<tr>"
            f"<td>{p.get('title', '')}</td>"
            f"<td>{p.get('publication_number', '')}</td>"
            f"<td>{p.get('family_size', '-')}</td>"
            f"<td>{p.get('tech_sub_area', '-')}</td>"
            f"<td><span class='{badge_cls}'>{layout_type}</span></td>"
            f"<td style='font-size:12px'>{p.get('claim_summary', '')[:120]}…</td>"
            f"</tr>"
        )

    # --- 热力表 ---
    sub_areas  = data.get("sub_area_heatmap", [])
    max_count  = max((s.get("count", 0) for s in sub_areas), default=1)
    heat_rows  = "".join(
        f"<tr><td>{s.get('name','')}</td>"
        f"<td class='{heat_class(s.get('count',0), max_count)}'>{s.get('count',0)}</td>"
        f"<td>{s.get('core_count',0)}</td><td>{s.get('periph_count',0)}</td></tr>"
        for s in sub_areas
    )

    # --- 核心 vs 外围分析 ---
    core_analysis   = data.get("core_analysis", "")
    periph_analysis = data.get("periph_analysis", "")

    # --- 研发建议 ---
    suggestions = data.get("suggestions", [])
    sug_items   = "".join(f"<li>{s}</li>" for s in suggestions)

    # --- 数据来源 ---
    sources = data.get("sources", [])
    src_items = "".join(f"<li>{s}</li>" for s in sources)

    # --- 数据不足提示 ---
    low_data_warn = ""
    if total_patents < 10:
        low_data_warn = (
            "<div class='warn'>⚠️ 当前检索结果不足 10 条，数据覆盖可能有限，"
            "建议调整检索式或扩大技术关键词范围后重新运行。</div>"
        )

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>{competitor} · {technology} 专利布局策略分析</title>
  {STYLE}
</head>
<body>

<h1>竞争对手专利布局策略分析报告</h1>
<p style="color:#555">
  <strong>竞争对手：</strong>{competitor} &nbsp;｜&nbsp;
  <strong>技术领域：</strong>{technology} &nbsp;｜&nbsp;
  <strong>市场范围：</strong>{market_scope} &nbsp;｜&nbsp;
  <strong>检索专利总数：</strong>{total_patents} 件 &nbsp;｜&nbsp;
  <strong>生成时间：</strong>{generated_at}
</p>
{low_data_warn}

<!-- ① 执行摘要 -->
<h1>① 执行摘要</h1>
<div class="summary-box">{exec_summary}</div>

<!-- ② 技术框架 -->
<h1>② 技术框架</h1>
<table>
  <tr><th>#</th><th>技术子方向</th><th>说明</th></tr>
  {tf_rows}
</table>

<!-- ③ 专利布局总览 -->
<h1>③ 专利布局总览</h1>
<h2>市场分布</h2>
<table>
  <tr><th>专利局/市场</th><th>专利数量</th></tr>
  {market_rows}
</table>

<!-- ④ 重点专利清单 -->
<h1>④ 重点专利清单（Top {len(top_patents)}）</h1>
<table>
  <tr>
    <th>专利标题</th><th>公开号</th><th>家族数</th>
    <th>技术子方向</th><th>布局类型</th><th>核心权利要求摘要</th>
  </tr>
  {patent_rows}
</table>

<!-- ⑤ 核心 vs 外围布局分析 -->
<h1>⑤ 核心 vs 外围布局分析</h1>
<h2>核心布局</h2>
<p>{core_analysis}</p>
<h2>外围布局</h2>
<p>{periph_analysis}</p>

<!-- ⑥ 技术子方向热力表 -->
<h1>⑥ 技术子方向专利热力表</h1>
<table>
  <tr><th>技术子方向</th><th>专利总数</th><th>核心专利</th><th>外围专利</th></tr>
  {heat_rows}
</table>
<p style="font-size:12px;color:#555">
  🔴 高密度（≥60%）&nbsp; 🟠 中密度（30-60%）&nbsp; 🟢 低密度（&lt;30%）
</p>

<!-- ⑦ 研发建议 -->
<h1>⑦ 研发建议</h1>
<ul>{sug_items}</ul>

<!-- ⑧ 证据与数据来源 -->
<h1>⑧ 证据与数据来源</h1>
<ul>{src_items}</ul>

<footer>
  本报告由 Eureka · PatSnap 智慧芽自动生成，专利数据来源于智慧芽专利数据库。
  结论仅供参考，关键决策请结合专业 IP 顾问意见。
</footer>

</body>
</html>"""
    return html


# ---------------------------------------------------------------------------
# PDF 转换
# ---------------------------------------------------------------------------

def html_to_pdf(html_content: str, output_path: str):
    """尝试用 weasyprint 转 PDF；若不可用则保存为 HTML。"""
    try:
        from weasyprint import HTML
        HTML(string=html_content).write_pdf(output_path)
        print(f"[OK] PDF 已生成：{output_path}")
    except ImportError:
        # Fallback: 保存为 HTML
        html_path = output_path.replace(".pdf", ".html")
        Path(html_path).write_text(html_content, encoding="utf-8")
        print(f"[WARN] weasyprint 未安装，已保存为 HTML：{html_path}")
        print("[HINT] 安装方式：pip install weasyprint")


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def main():
    args = parse_args()

    data_path   = args.data_path
    output_path = args.output_path

    if not os.path.exists(data_path):
        print(f"[ERROR] 数据文件不存在：{data_path}", file=sys.stderr)
        sys.exit(1)

    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)

    html_content = render_html(data)
    html_to_pdf(html_content, output_path)


if __name__ == "__main__":
    main()

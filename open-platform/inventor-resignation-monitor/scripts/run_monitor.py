#!/usr/bin/env python3
"""
发明人离职监控简报生成脚本
用法:
  python run_monitor.py --company 浙江孚邦 --tech 外骨骼 康复机器人 --monitor-years 2
  python run_monitor.py --inventors 陈伟海 王业伟 --tech 外骨骼 --monitor-years 2
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# ── 输出目录 ──────────────────────────────────────────────
OUTPUT_DIR = os.environ.get("EUREKA_PYTHON_OUTPUT_DIR", ".")


def parse_args():
    parser = argparse.ArgumentParser(description="发明人离职监控简报")
    parser.add_argument("--company", type=str, default=None, help="目标公司名称")
    parser.add_argument("--tech", nargs="+", default=[], help="技术领域关键词列表")
    parser.add_argument("--inventors", nargs="+", default=None, help="直接指定发明人姓名列表")
    parser.add_argument("--inactive-years", type=int, default=5, help="认定离职的无申请年限（默认5）")
    parser.add_argument("--monitor-years", type=int, default=2, help="监控窗口年数（默认2）")
    parser.add_argument("--output", type=str, default=None, help="输出HTML路径")
    return parser.parse_args()


def build_monitor_prompt(company, tech_keywords, inventors, inactive_years, monitor_years):
    """构建给Eureka AI的分析指令（供交互模式使用）"""
    today = datetime.now()
    monitor_start = today - timedelta(days=365 * monitor_years)
    inactive_cutoff = today.year - inactive_years

    lines = [
        f"# 发明人离职监控分析任务",
        f"执行日期：{today.strftime('%Y-%m-%d')}",
        f"监控窗口：{monitor_start.strftime('%Y-%m-%d')} 至 {today.strftime('%Y-%m-%d')}",
        "",
    ]

    if company:
        lines += [
            f"## 目标公司：{company}",
            f"疑似离职判定标准：{inactive_cutoff}年之后未在该公司申请专利",
        ]
    if inventors:
        lines += [f"## 直接监控发明人：{', '.join(inventors)}"]
    if tech_keywords:
        lines += [f"## 技术领域关键词：{', '.join(tech_keywords)}"]

    lines += [
        "",
        "## 分析步骤",
        "### Step 1：识别疑似离职发明人",
    ]
    if company:
        lines.append(f"检索 {company} 全部专利发明人，找出最后申请年 < {inactive_cutoff} 的人员")
    else:
        lines.append(f"直接使用指定发明人列表进行监控")

    lines += [
        "",
        "### Step 2：他处专利检索",
        f"对每位疑似离职发明人，检索其在 {monitor_start.strftime('%Y%m%d')} 之后在其他机构申请的专利",
        f"关键词：{', '.join(tech_keywords) if tech_keywords else '（使用原公司技术领域）'}",
        "",
        "### Step 3：风险评估",
        "按技术相似度分为：🔴高风险 / 🟠中风险 / 🟡持续关注 / 🟢低风险",
        "",
        "### Step 4：生成HTML简报",
        f"输出路径：{OUTPUT_DIR}/inventor_monitor_report.html",
    ]

    return "\n".join(lines)


def generate_html_report(data: dict, output_path: str):
    """根据分析数据生成HTML简报"""
    company = data.get("company", "未指定")
    report_date = data.get("report_date", datetime.now().strftime("%Y-%m-%d"))
    monitor_start = data.get("monitor_start", "")
    monitor_end = data.get("monitor_end", report_date)
    inventors = data.get("inventors", [])
    summary = data.get("summary", {})

    risk_colors = {
        "high": "#dc3545",
        "medium": "#fd7e14",
        "watch": "#ffc107",
        "low": "#28a745",
    }
    risk_labels = {
        "high": "🔴 高风险",
        "medium": "🟠 中风险",
        "watch": "🟡 持续关注",
        "low": "🟢 低风险",
    }

    # 生成发明人卡片HTML
    inventor_cards = ""
    for inv in inventors:
        name = inv.get("name", "")
        risk = inv.get("risk", "low")
        org_patents = inv.get("org_patents", [])
        new_patents = inv.get("new_patents", [])
        new_org = inv.get("new_org", "未知")
        notes = inv.get("notes", "")
        color = risk_colors.get(risk, "#6c757d")
        label = risk_labels.get(risk, "未知")

        org_rows = "".join(
            f"<tr><td>{p.get('pn','')}</td><td>{p.get('title','')}</td><td>{p.get('year','')}</td></tr>"
            for p in org_patents
        )
        new_rows = "".join(
            f"<tr><td>{p.get('pn','')}</td><td>{p.get('title','')}</td><td>{p.get('org','')}</td><td>{p.get('date','')}</td></tr>"
            for p in new_patents
        )

        inventor_cards += f"""
        <div class="inventor-card" style="border-left: 5px solid {color};">
          <div class="inv-header">
            <span class="inv-name">{name}</span>
            <span class="risk-badge" style="background:{color};">{label}</span>
          </div>
          <div class="inv-body">
            <p><strong>新就职单位：</strong>{new_org}</p>
            {'<p class="notes">' + notes + '</p>' if notes else ''}
            {'<h4>在原公司核心专利（节选）</h4><table><thead><tr><th>公开号</th><th>标题</th><th>年份</th></tr></thead><tbody>' + org_rows + '</tbody></table>' if org_rows else ''}
            {'<h4>监控期内新申请专利</h4><table class="new-table"><thead><tr><th>公开号</th><th>标题</th><th>申请机构</th><th>申请日</th></tr></thead><tbody>' + new_rows + '</tbody></table>' if new_rows else '<p class="no-result">监控期内未检出相关专利</p>'}
          </div>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>发明人离职监控简报 — {company}</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif; background: #f5f7fa; color: #333; }}
    .container {{ max-width: 1100px; margin: 0 auto; padding: 32px 20px; }}
    .header {{ background: linear-gradient(135deg, #1a237e 0%, #283593 100%); color: #fff; border-radius: 12px; padding: 32px 36px; margin-bottom: 28px; }}
    .header h1 {{ font-size: 26px; margin-bottom: 8px; }}
    .header .meta {{ font-size: 14px; opacity: 0.85; }}
    .summary-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 28px; }}
    .summary-card {{ background: #fff; border-radius: 10px; padding: 20px 16px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.07); }}
    .summary-card .num {{ font-size: 36px; font-weight: 700; }}
    .summary-card .lbl {{ font-size: 13px; color: #666; margin-top: 6px; }}
    .section-title {{ font-size: 18px; font-weight: 700; margin: 28px 0 16px; padding-left: 12px; border-left: 4px solid #1a237e; }}
    .inventor-card {{ background: #fff; border-radius: 10px; padding: 24px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.07); }}
    .inv-header {{ display: flex; align-items: center; gap: 16px; margin-bottom: 16px; }}
    .inv-name {{ font-size: 20px; font-weight: 700; }}
    .risk-badge {{ color: #fff; padding: 4px 14px; border-radius: 20px; font-size: 13px; font-weight: 600; }}
    .inv-body p {{ margin-bottom: 10px; font-size: 14px; }}
    .inv-body h4 {{ font-size: 14px; color: #555; margin: 14px 0 8px; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    th {{ background: #f0f2f5; padding: 8px 10px; text-align: left; }}
    td {{ padding: 7px 10px; border-bottom: 1px solid #eee; }}
    .new-table td {{ background: #fffde7; }}
    .no-result {{ color: #888; font-style: italic; font-size: 13px; }}
    .notes {{ background: #fff3e0; border-radius: 6px; padding: 10px 14px; font-size: 13px; color: #e65100; }}
    .disclaimer {{ background: #fff8e1; border: 1px solid #ffe082; border-radius: 8px; padding: 14px 18px; font-size: 13px; color: #7b5800; margin-top: 32px; }}
    .footer {{ text-align: center; font-size: 12px; color: #aaa; margin-top: 24px; }}
  </style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>📋 发明人离职监控简报</h1>
    <div class="meta">
      监控对象：{company}&nbsp;&nbsp;|&nbsp;&nbsp;
      监控窗口：{monitor_start} 至 {monitor_end}&nbsp;&nbsp;|&nbsp;&nbsp;
      生成日期：{report_date}
    </div>
  </div>

  <div class="summary-grid">
    <div class="summary-card">
      <div class="num" style="color:#dc3545;">{summary.get('high', 0)}</div>
      <div class="lbl">🔴 高风险</div>
    </div>
    <div class="summary-card">
      <div class="num" style="color:#fd7e14;">{summary.get('medium', 0)}</div>
      <div class="lbl">🟠 中风险</div>
    </div>
    <div class="summary-card">
      <div class="num" style="color:#ffc107;">{summary.get('watch', 0)}</div>
      <div class="lbl">🟡 持续关注</div>
    </div>
    <div class="summary-card">
      <div class="num" style="color:#28a745;">{summary.get('low', 0)}</div>
      <div class="lbl">🟢 低风险</div>
    </div>
  </div>

  <div class="section-title">发明人详情</div>
  {inventor_cards}

  <div class="disclaimer">
    ⚠️ <strong>重要说明：</strong>专利有约18个月公开时滞，监控窗口末尾18个月内申请的专利可能尚未公开，实际风险可能被低估。建议每季度执行滚动监控。同名发明人存在误报可能，建议结合IPC分类和技术词二次确认。
  </div>
  <div class="footer">Powered by Eureka · PatSnap &nbsp;|&nbsp; {report_date}</div>
</div>
</body>
</html>"""

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] 报告已生成：{output_path}")
    return output_path


def main():
    args = parse_args()

    if not args.company and not args.inventors:
        print("错误：请至少提供 --company 或 --inventors 参数", file=sys.stderr)
        sys.exit(1)

    # 打印分析指令（供Eureka AI步骤使用）
    prompt = build_monitor_prompt(
        company=args.company,
        tech_keywords=args.tech,
        inventors=args.inventors,
        inactive_years=args.inactive_years,
        monitor_years=args.monitor_years,
    )
    print(prompt)

    # 如果传入了JSON数据文件，直接生成报告
    data_file = os.environ.get("MONITOR_DATA_JSON")
    if data_file and Path(data_file).exists():
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        out = args.output or os.path.join(OUTPUT_DIR, "inventor_monitor_report.html")
        generate_html_report(data, out)
    else:
        print("\n[提示] 未检测到 MONITOR_DATA_JSON 环境变量，已输出分析指令。")
        print("[提示] 请由 Eureka AI 执行专利检索后，将结果写入 JSON 并设置 MONITOR_DATA_JSON 路径再次运行。")


if __name__ == "__main__":
    main()

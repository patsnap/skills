#!/usr/bin/env python3
"""
xiong-an-due-diligence — 主执行脚本
雄安国创中心企业及技术专项尽调报告生成器
用法：python run_due_diligence.py --company "企业全称" --credit-code "统一社会信用代码" --tech-keywords "关键词1,关键词2" [--scenario "招商落地"] [--competitors "竞品A,竞品B"] [--output-dir "/path/to/output"]
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ─── 参数解析 ────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="雄安国创中心企业及技术专项尽调报告生成器"
    )
    parser.add_argument("--company", required=True, help="目标企业全称")
    parser.add_argument("--credit-code", default="", help="统一社会信用代码（建议填写）")
    parser.add_argument(
        "--tech-keywords", required=True,
        help="核心技术关键词，英文逗号分隔，例如：激光雷达,LIDAR,自动驾驶"
    )
    parser.add_argument(
        "--scenario", default="招商落地",
        choices=["招商落地", "投资合作", "技术引进"],
        help="尽调场景（默认：招商落地）"
    )
    parser.add_argument(
        "--competitors", default="",
        help="指定竞品企业名单，英文逗号分隔；不填则由 AI 自动识别"
    )
    parser.add_argument(
        "--output-dir", default=os.environ.get("EUREKA_PYTHON_OUTPUT_DIR", "."),
        help="报告输出目录"
    )
    return parser.parse_args()

# ─── 工作流控制器 ─────────────────────────────────────────────────────────────

class DueDiligenceWorkflow:
    def __init__(self, args):
        self.company       = args.company
        self.credit_code   = args.credit_code
        self.tech_keywords = [k.strip() for k in args.tech_keywords.split(",") if k.strip()]
        self.scenario      = args.scenario
        self.competitors   = [c.strip() for c in args.competitors.split(",") if c.strip()]
        self.output_dir    = Path(args.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.report_date   = datetime.now().strftime("%Y%m%d_%H%M")
        self.context       = {}   # 跨步骤共享数据容器

    # ── Step 1 ───────────────────────────────────────────────────────────────
    def step1_scope(self):
        """自动立项 & 尽调范围界定"""
        print("\n[Step 1] 自动立项 & 尽调范围界定...")
        self.context["scope"] = {
            "company":      self.company,
            "credit_code":  self.credit_code,
            "tech_keywords": self.tech_keywords,
            "scenario":     self.scenario,
            "due_date":     datetime.now().strftime("%Y-%m-%d %H:%M"),
            "boundaries": [
                "企业基本面（工商、股权、高管）",
                "技术真实性与成熟度（TRL）",
                "专利IP权属与法律状态",
                "研发实力与团队稳定性",
                "FTO侵权风险排查",
                "法律合规（涉诉、行政处罚）",
                "竞品技术对标",
                "综合风险分级"
            ]
        }
        print(f"  ✓ 尽调范围锁定：{len(self.context['scope']['boundaries'])} 项")

    # ── Step 2 ───────────────────────────────────────────────────────────────
    def step2_framework(self):
        """搭建报告框架"""
        print("\n[Step 2] 搭建报告目录框架...")
        self.context["toc"] = [
            "1. 执行摘要（一页式）",
            "2. 企业概况",
            "3. 核心技术解析",
            "4. 知识产权尽调",
            "5. 研发能力评估",
            "6. 竞品技术对标",
            "7. 法律合规风险",
            "8. 风险等级汇总",
            "9. 尽调结论与落地建议",
        ]
        print(f"  ✓ 报告框架共 {len(self.context['toc'])} 章")

    # ── Step 3 ───────────────────────────────────────────────────────────────
    def step3_external_data(self):
        """
        外部数据检索占位符。
        在 Eureka 运行时中，此步骤由 AI 调用以下工具完成：
          - mcp_patent-search__patsnap_search  → 专利检索
          - mcp_patent-search__patsnap_fetch   → 专利详情
          - mcp_web-search__web_search         → 工商/舆情/涉诉
          - web_fetch                          → 抓取具体页面
        此脚本将调用结果写入 self.context["external"]。
        """
        print("\n[Step 3] 外部数据检索 & 清洗分析（由 Eureka AI 工具链执行）...")
        # 运行时由 AI 填充；此处为结构占位，保证后续步骤不报错
        self.context["external"] = {
            "patents":      [],   # [{pn, title, status, assignee, ipc, filing_date, abstract}]
            "papers":       [],   # [{title, authors, journal, year, abstract}]
            "company_info": {},   # {name, credit_code, reg_date, legal_rep, capital, scope, ...}
            "shareholders": [],
            "executives":   [],
            "litigations":  [],
            "penalties":    [],
            "news_negative": [],
            "financing":    [],
        }
        print("  ✓ 外部数据容器已初始化（运行时由工具链填充）")

    # ── Step 4 ───────────────────────────────────────────────────────────────
    def step4_internal_rules(self):
        """内部规则融合 — 风险打分"""
        print("\n[Step 4] 内部规则融合 & 风险打分...")
        # 内置风险评级规则（v1.0）
        self.context["risk_rules"] = {
            "version": "国创中心风险评级规则 v1.0",
            "levels": {
                "致命风险": {"icon": "🔴", "desc": "直接影响落地可行性，需立即决策"},
                "重大风险": {"icon": "🟠", "desc": "可能影响合作条款或投资估值"},
                "一般风险": {"icon": "🟡", "desc": "可管控，需在协议中约定处置方式"},
            },
            "triggers": {
                "致命风险": [
                    "核心专利权属存在争议或已被无效",
                    "企业被列入失信被执行人名单",
                    "实控人/法定代表人涉及刑事案件",
                    "核心技术落入他人有效专利保护范围（FTO红灯）",
                ],
                "重大风险": [
                    "核心专利临近到期或已质押未解除",
                    "存在重大未决诉讼（标的超过500万）",
                    "核心技术团队近1年内大量离职",
                    "技术TRL成熟度低于4级",
                    "竞品已形成明显专利包围圈",
                ],
                "一般风险": [
                    "专利布局覆盖度不足（核心技术点存在空白）",
                    "存在行政处罚记录（非重大）",
                    "研发投入占营收比低于行业基准",
                    "FTO存在黄灯专利（可规避但需关注）",
                ],
            }
        }
        print(f"  ✓ 风险打分规则加载完成（版本：{self.context['risk_rules']['version']}）")

    # ── Step 5 ───────────────────────────────────────────────────────────────
    def step5_tech_analysis(self):
        """技术深度分析"""
        print("\n[Step 5] 技术深度分析（TRL评估 + FTO排查）...")
        self.context["tech_analysis"] = {
            "trl_framework": {
                "levels": {
                    1: "基础原理研究",
                    2: "技术概念形成",
                    3: "概念验证/实验室验证",
                    4: "实验室环境测试",
                    5: "相关环境验证",
                    6: "原型演示验证",
                    7: "系统原型演示（真实环境）",
                    8: "系统完成并验证（量产准备）",
                    9: "经实际应用验证（成熟商业化）",
                }
            },
            "fto_traffic_light": {
                "green":  "技术实施路径无明显侵权风险",
                "yellow": "存在需关注专利，建议设计规避方案",
                "red":    "存在高侵权风险，建议暂停或获取许可",
            },
            "result": {}   # 运行时由 AI 填充分析结论
        }
        print("  ✓ 技术分析框架初始化完成")

    # ── Step 6 ───────────────────────────────────────────────────────────────
    def step6_integrate(self):
        """整合所有数据，准备报告内容"""
        print("\n[Step 6] 数据整合 & 报告内容融合...")
        self.context["report_ready"] = True
        print("  ✓ 数据整合完成，准备渲染 HTML 报告")

    # ── Step 7 ───────────────────────────────────────────────────────────────
    def step7_render_html(self) -> Path:
        """渲染 HTML 报告"""
        print("\n[Step 7] 渲染 HTML 报告...")
        html = build_html_report(self.context)
        output_file = self.output_dir / f"尽调报告_{self.company}_{self.report_date}.html"
        output_file.write_text(html, encoding="utf-8")
        print(f"  ✓ 报告已生成：{output_file}")
        return output_file

    # ── 主入口 ────────────────────────────────────────────────────────────────
    def run(self) -> Path:
        print(f"\n{'='*60}")
        print(f"  雄安国创中心企业及技术专项尽调报告生成器")
        print(f"  目标企业：{self.company}")
        print(f"  技术方向：{', '.join(self.tech_keywords)}")
        print(f"  尽调场景：{self.scenario}")
        print(f"{'='*60}")
        self.step1_scope()
        self.step2_framework()
        self.step3_external_data()
        self.step4_internal_rules()
        self.step5_tech_analysis()
        self.step6_integrate()
        return self.step7_render_html()


# ─── HTML 报告渲染器 ──────────────────────────────────────────────────────────

def build_html_report(ctx: dict) -> str:
    """
    基于 context 字典构建完整 HTML 报告。
    实际数据由 AI 工具链写入 ctx 后调用此函数渲染。
    """
    scope        = ctx.get("scope", {})
    toc          = ctx.get("toc", [])
    risk_rules   = ctx.get("risk_rules", {})
    tech_analysis = ctx.get("tech_analysis", {})
    company      = scope.get("company", "—")
    scenario     = scope.get("scenario", "—")
    due_date     = scope.get("due_date", "—")
    keywords     = "、".join(scope.get("tech_keywords", []))

    # 目录 HTML
    toc_html = "".join(f'<li><a href="#sec{i+1}">{item}</a></li>' for i, item in enumerate(toc))

    # 风险规则说明
    risk_levels_html = ""
    for level, info in risk_rules.get("levels", {}).items():
        risk_levels_html += (
            f'<span class="risk-badge risk-{level[:2]}">'
            f'{info["icon"]} {level}</span> {info["desc"]}<br>'
        )

    # TRL 框架表格
    trl_html = ""
    for lvl, desc in tech_analysis.get("trl_framework", {}).get("levels", {}).items():
        trl_html += f"<tr><td><b>TRL {lvl}</b></td><td>{desc}</td></tr>"

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>【尽调报告】{company} — 雄安国创中心</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
<style>
  :root {{
    --bg: #0d1117; --surface: #161b22; --border: #30363d;
    --accent: #58a6ff; --accent2: #3fb950; --text: #c9d1d9;
    --text-dim: #8b949e; --red: #f85149; --orange: #d29922; --yellow: #e3b341;
    --card-bg: #1f2937;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: var(--bg); color: var(--text); font-family: "PingFang SC","Segoe UI",sans-serif; font-size: 14px; }}
  header {{ background: linear-gradient(135deg,#1a2a4a,#0d1117); padding: 40px 60px; border-bottom: 1px solid var(--border); }}
  header h1 {{ font-size: 24px; color: #fff; margin-bottom: 8px; }}
  header p {{ color: var(--text-dim); font-size: 13px; }}
  .meta-row {{ display: flex; gap: 32px; margin-top: 16px; flex-wrap: wrap; }}
  .meta-item {{ display: flex; flex-direction: column; gap: 4px; }}
  .meta-label {{ font-size: 11px; color: var(--text-dim); text-transform: uppercase; letter-spacing: .05em; }}
  .meta-value {{ font-size: 13px; color: var(--accent); font-weight: 600; }}
  .container {{ max-width: 1200px; margin: 0 auto; padding: 32px 60px; }}
  .toc {{ background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 24px; margin-bottom: 32px; }}
  .toc h2 {{ font-size: 14px; color: var(--text-dim); margin-bottom: 12px; text-transform: uppercase; letter-spacing: .05em; }}
  .toc ol {{ padding-left: 20px; }}
  .toc li {{ margin: 6px 0; }}
  .toc a {{ color: var(--accent); text-decoration: none; font-size: 13px; }}
  .toc a:hover {{ text-decoration: underline; }}
  section {{ margin-bottom: 48px; }}
  section h2 {{ font-size: 18px; color: #fff; border-bottom: 2px solid var(--accent); padding-bottom: 8px; margin-bottom: 20px; }}
  section h3 {{ font-size: 14px; color: var(--accent2); margin: 16px 0 8px; }}
  .card {{ background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin-bottom: 16px; }}
  .summary-grid {{ display: grid; grid-template-columns: repeat(auto-fill,minmax(220px,1fr)); gap: 16px; margin-bottom: 24px; }}
  .summary-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 16px; }}
  .summary-card .label {{ font-size: 11px; color: var(--text-dim); margin-bottom: 4px; }}
  .summary-card .value {{ font-size: 20px; font-weight: 700; color: var(--accent); }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  th {{ background: var(--surface); color: var(--text-dim); padding: 10px 14px; text-align: left; border: 1px solid var(--border); font-weight: 600; }}
  td {{ padding: 10px 14px; border: 1px solid var(--border); color: var(--text); }}
  tr:hover td {{ background: rgba(88,166,255,.04); }}
  .risk-fatal   {{ background: rgba(248,81,73,.15); border-left: 3px solid var(--red); padding: 12px 16px; border-radius: 4px; margin: 8px 0; }}
  .risk-major   {{ background: rgba(210,153,34,.15); border-left: 3px solid var(--orange); padding: 12px 16px; border-radius: 4px; margin: 8px 0; }}
  .risk-general {{ background: rgba(227,179,65,.12); border-left: 3px solid var(--yellow); padding: 12px 16px; border-radius: 4px; margin: 8px 0; }}
  .risk-badge {{ display: inline-block; border-radius: 4px; padding: 2px 8px; font-size: 12px; font-weight: 600; margin-right: 6px; }}
  .risk-致命 {{ background: rgba(248,81,73,.2); color: var(--red); }}
  .risk-重大 {{ background: rgba(210,153,34,.2); color: var(--orange); }}
  .risk-一般 {{ background: rgba(227,179,65,.15); color: var(--yellow); }}
  .trl-bar {{ display: flex; align-items: center; gap: 8px; margin: 4px 0; }}
  .trl-track {{ flex: 1; height: 8px; background: var(--border); border-radius: 4px; overflow: hidden; }}
  .trl-fill {{ height: 100%; border-radius: 4px; background: linear-gradient(90deg,#1f6feb,#3fb950); }}
  .fto-green  {{ color: #3fb950; font-weight: 600; }}
  .fto-yellow {{ color: var(--yellow); font-weight: 600; }}
  .fto-red    {{ color: var(--red); font-weight: 600; }}
  .chart-container {{ width: 100%; height: 320px; margin: 16px 0; }}
  .placeholder {{ color: var(--text-dim); font-style: italic; font-size: 13px; padding: 16px; background: var(--surface); border-radius: 6px; border: 1px dashed var(--border); }}
  .source-tag {{ display: inline-block; font-size: 10px; color: var(--text-dim); background: var(--surface); border: 1px solid var(--border); border-radius: 3px; padding: 1px 6px; margin-left: 6px; }}
  footer {{ text-align: center; padding: 32px; color: var(--text-dim); font-size: 12px; border-top: 1px solid var(--border); margin-top: 48px; }}
  @media print {{
    body {{ background: #fff; color: #000; }}
    header {{ background: #1a2a4a; -webkit-print-color-adjust: exact; }}
    .chart-container {{ page-break-inside: avoid; }}
    section {{ page-break-inside: avoid; }}
  }}
</style>
</head>
<body>

<header>
  <h1>🏢 企业及技术专项尽调报告</h1>
  <p>雄安国创中心 · 标准尽调报告 · 仅供内部决策参考</p>
  <div class="meta-row">
    <div class="meta-item"><span class="meta-label">目标企业</span><span class="meta-value">{company}</span></div>
    <div class="meta-item"><span class="meta-label">核心技术方向</span><span class="meta-value">{keywords}</span></div>
    <div class="meta-item"><span class="meta-label">尽调场景</span><span class="meta-value">{scenario}</span></div>
    <div class="meta-item"><span class="meta-label">生成时间</span><span class="meta-value">{due_date}</span></div>
    <div class="meta-item"><span class="meta-label">数据来源</span><span class="meta-value">智慧芽 · 工商数据 · 公开网络</span></div>
  </div>
</header>

<div class="container">

  <!-- 目录 -->
  <div class="toc">
    <h2>📋 报告目录</h2>
    <ol>{toc_html}</ol>
  </div>

  <!-- 第1章：执行摘要 -->
  <section id="sec1">
    <h2>1. 执行摘要（一页式）</h2>
    <div class="summary-grid">
      <div class="summary-card"><div class="label">专利总量</div><div class="value" id="v-patent-total">—</div></div>
      <div class="summary-card"><div class="label">有效专利</div><div class="value" id="v-patent-active">—</div></div>
      <div class="summary-card"><div class="label">FTO风险等级</div><div class="value" id="v-fto-level">—</div></div>
      <div class="summary-card"><div class="label">综合风险评级</div><div class="value" id="v-risk-level">—</div></div>
      <div class="summary-card"><div class="label">技术TRL等级</div><div class="value" id="v-trl-level">—</div></div>
      <div class="summary-card"><div class="label">落地可行性</div><div class="value" id="v-feasibility">—</div></div>
    </div>
    <div class="card">
      <h3>🎯 关键结论</h3>
      <div class="placeholder" id="summary-conclusion">
        【由 AI 工具链在完成数据检索后自动填充——核心优势、主要风险、落地建议三段式摘要】
      </div>
    </div>
    <div class="card">
      <h3>⚠️ 重大风险高亮</h3>
      <div id="summary-risks">
        <div class="risk-fatal">🔴 <b>致命风险（待核查）</b>：数据检索完成后自动填充</div>
        <div class="risk-major">🟠 <b>重大风险（待核查）</b>：数据检索完成后自动填充</div>
      </div>
    </div>
  </section>

  <!-- 第2章：企业概况 -->
  <section id="sec2">
    <h2>2. 企业概况</h2>
    <div class="card">
      <h3>📄 工商基本信息 <span class="source-tag">来源：工商公开数据</span></h3>
      <table>
        <tr><th>企业名称</th><td id="ci-name">{company}</td><th>统一社会信用代码</th><td id="ci-code">{scope.get('credit_code','—')}</td></tr>
        <tr><th>法定代表人</th><td id="ci-legal-rep">—</td><th>注册资本</th><td id="ci-capital">—</td></tr>
        <tr><th>成立日期</th><td id="ci-reg-date">—</td><th>注册地</th><td id="ci-location">—</td></tr>
        <tr><th>经营状态</th><td id="ci-status">—</td><th>所属行业</th><td id="ci-industry">—</td></tr>
        <tr><th>经营范围</th><td id="ci-scope" colspan="3">—</td></tr>
      </table>
    </div>
    <div class="card">
      <h3>🌳 股权穿透 <span class="source-tag">来源：工商公开数据</span></h3>
      <div class="placeholder">股权架构图（由 AI 工具链检索工商数据后自动填充）</div>
    </div>
    <div class="card">
      <h3>💰 融资历史 <span class="source-tag">来源：公开融资数据库</span></h3>
      <table id="financing-table">
        <thead><tr><th>轮次</th><th>金额</th><th>投资方</th><th>时间</th></tr></thead>
        <tbody><tr><td colspan="4" class="placeholder">数据检索后自动填充</td></tr></tbody>
      </table>
    </div>
  </section>

  <!-- 第3章：核心技术解析 -->
  <section id="sec3">
    <h2>3. 核心技术解析</h2>
    <div class="card">
      <h3>🔬 技术原理与壁垒</h3>
      <div class="placeholder" id="tech-principle">
        核心技术原理解析（由 AI 结合专利摘要+论文检索结果自动生成）
      </div>
    </div>
    <div class="card">
      <h3>📊 技术成熟度（TRL）评估</h3>
      <div class="trl-bar">
        <span style="width:60px;font-size:12px;">当前TRL</span>
        <div class="trl-track"><div class="trl-fill" id="trl-fill-bar" style="width:0%"></div></div>
        <span id="trl-score" style="font-weight:700;color:var(--accent2);">—</span>
      </div>
      <table style="margin-top:12px;">
        <thead><tr><th>级别</th><th>定义</th></tr></thead>
        <tbody>{trl_html}</tbody>
      </table>
    </div>
  </section>

  <!-- 第4章：知识产权尽调 -->
  <section id="sec4">
    <h2>4. 知识产权尽调</h2>
    <div class="card">
      <h3>📑 专利布局总览 <span class="source-tag">来源：智慧芽专利数据库</span></h3>
      <div class="chart-container" id="patent-chart"></div>
    </div>
    <div class="card">
      <h3>📋 核心专利清单</h3>
      <table id="patent-table">
        <thead>
          <tr>
            <th>专利号</th><th>名称</th><th>申请日</th><th>法律状态</th>
            <th>权属归属</th><th>IPC分类</th><th>风险标注</th>
          </tr>
        </thead>
        <tbody>
          <tr><td colspan="7" class="placeholder">专利检索完成后自动填充（来源：智慧芽）</td></tr>
        </tbody>
      </table>
    </div>
    <div class="card">
      <h3>🔒 质押/许可/无效纠纷情况 <span class="source-tag">来源：智慧芽法律状态数据</span></h3>
      <div class="placeholder" id="ip-legal-status">数据检索后自动填充</div>
    </div>
  </section>

  <!-- 第5章：研发能力评估 -->
  <section id="sec5">
    <h2>5. 研发能力评估</h2>
    <div class="card">
      <h3>👥 核心研发团队</h3>
      <table id="rd-team-table">
        <thead><tr><th>姓名</th><th>职位</th><th>背景</th><th>主要专利贡献</th><th>稳定性评估</th></tr></thead>
        <tbody><tr><td colspan="5" class="placeholder">数据检索后自动填充</td></tr></tbody>
      </table>
    </div>
    <div class="card">
      <h3>💹 研发投入趋势 <span class="source-tag">来源：公开财务/年报数据</span></h3>
      <div class="chart-container" id="rd-invest-chart"></div>
    </div>
    <div class="card">
      <h3>🔮 技术迭代 & 管线储备</h3>
      <div class="placeholder" id="tech-pipeline">数据检索后自动填充</div>
    </div>
  </section>

  <!-- 第6章：竞品技术对标 -->
  <section id="sec6">
    <h2>6. 竞品技术对标</h2>
    <div class="card">
      <h3>🏆 竞品雷达图 <span class="source-tag">来源：智慧芽专利数据 + 公开资料</span></h3>
      <div class="chart-container" id="competitor-radar"></div>
    </div>
    <div class="card">
      <h3>📊 技术路线 × 专利布局对比</h3>
      <table id="competitor-table">
        <thead>
          <tr>
            <th>维度</th><th>{company}</th>
            <th>竞品A</th><th>竞品B</th><th>竞品C</th>
          </tr>
        </thead>
        <tbody>
          <tr><td>专利总量</td><td>—</td><td>—</td><td>—</td><td>—</td></tr>
          <tr><td>核心技术覆盖度</td><td>—</td><td>—</td><td>—</td><td>—</td></tr>
          <tr><td>TRL成熟度</td><td>—</td><td>—</td><td>—</td><td>—</td></tr>
          <tr><td>海外布局</td><td>—</td><td>—</td><td>—</td><td>—</td></tr>
          <tr><td>近3年专利增速</td><td>—</td><td>—</td><td>—</td><td>—</td></tr>
        </tbody>
      </table>
    </div>
  </section>

  <!-- 第7章：法律合规风险 -->
  <section id="sec7">
    <h2>7. 法律合规风险</h2>
    <div class="card">
      <h3>⚖️ 涉诉仲裁记录 <span class="source-tag">来源：裁判文书网/公开司法数据</span></h3>
      <table id="litigation-table">
        <thead><tr><th>案件类型</th><th>案件状态</th><th>标的金额</th><th>时间</th><th>结果</th><th>风险级别</th></tr></thead>
        <tbody><tr><td colspan="6" class="placeholder">数据检索后自动填充</td></tr></tbody>
      </table>
    </div>
    <div class="card">
      <h3>🚨 行政处罚 & 经营异常 <span class="source-tag">来源：市监局公示数据</span></h3>
      <div class="placeholder" id="penalty-info">数据检索后自动填充</div>
    </div>
    <div class="card">
      <h3>🔍 FTO 自由实施风险排查</h3>
      <div class="placeholder" id="fto-result">
        <p>FTO排查结论（由 AI 基于专利检索结果自动生成）：</p>
        <p>🟢 <span class="fto-green">绿灯：</span>无明显侵权风险路径 — 待填充</p>
        <p>🟡 <span class="fto-yellow">黄灯：</span>需关注专利 — 待填充</p>
        <p>🔴 <span class="fto-red">红灯：</span>高风险专利 — 待填充</p>
      </div>
    </div>
  </section>

  <!-- 第8章：风险等级汇总 -->
  <section id="sec8">
    <h2>8. 风险等级汇总</h2>
    <div class="card">
      <div style="margin-bottom:12px;">{risk_levels_html}</div>
      <table id="risk-summary-table">
        <thead>
          <tr><th>风险编号</th><th>风险描述</th><th>等级</th><th>影响说明</th><th>处置建议</th></tr>
        </thead>
        <tbody>
          <tr><td colspan="5" class="placeholder">数据检索与分析完成后自动填充（来源：综合分析结论）</td></tr>
        </tbody>
      </table>
    </div>
    <div class="chart-container" id="risk-pie-chart" style="height:260px;"></div>
  </section>

  <!-- 第9章：尽调结论与落地建议 -->
  <section id="sec9">
    <h2>9. 尽调结论与落地建议</h2>
    <div class="card">
      <h3>✅ 综合结论</h3>
      <div class="placeholder" id="final-conclusion">
        综合结论（由 AI 在完成所有分析步骤后自动填充——
        包含：是否建议推进、落地可行性评级、核心关切事项）
      </div>
    </div>
    <div class="card">
      <h3>📌 落地建议（行动清单）</h3>
      <table id="action-table">
        <thead><tr><th>#</th><th>建议事项</th><th>优先级</th><th>责任方</th><th>完成时限</th></tr></thead>
        <tbody><tr><td colspan="5" class="placeholder">数据分析完成后自动填充</td></tr></tbody>
      </table>
    </div>
  </section>

</div><!-- /container -->

<footer>
  <p>本报告由 Eureka · 智慧芽 AI 系统自动生成 | 雄安国创中心专用 | 数据来源：智慧芽专利数据库、工商公开数据、公开网络</p>
  <p>生成时间：{due_date} | 仅供内部决策参考，不构成法律意见</p>
</footer>

<script>
// ECharts 初始化（数据由 AI 写入 window.__reportData 后渲染）
document.addEventListener('DOMContentLoaded', function() {{
  // 专利分布图（示意）
  var patentChart = echarts.init(document.getElementById('patent-chart'));
  patentChart.setOption({{
    backgroundColor: 'transparent',
    title: {{ text: '专利技术分类分布', textStyle: {{ color: '#c9d1d9', fontSize: 13 }} }},
    tooltip: {{ trigger: 'item' }},
    series: [{{
      type: 'pie', radius: ['40%','70%'],
      data: (window.__reportData && window.__reportData.patentDist) || [
        {{value: 0, name: '发明专利'}},
        {{value: 0, name: '实用新型'}},
        {{value: 0, name: '外观设计'}},
      ],
      label: {{ color: '#c9d1d9' }}
    }}]
  }});

  // 风险饼图
  var riskPie = echarts.init(document.getElementById('risk-pie-chart'));
  riskPie.setOption({{
    backgroundColor: 'transparent',
    title: {{ text: '风险等级分布', textStyle: {{ color: '#c9d1d9', fontSize: 13 }} }},
    tooltip: {{ trigger: 'item' }},
    series: [{{
      type: 'pie', radius: '60%',
      data: (window.__reportData && window.__reportData.riskDist) || [
        {{value: 0, name: '致命风险', itemStyle: {{color:'#f85149'}}}},
        {{value: 0, name: '重大风险', itemStyle: {{color:'#d29922'}}}},
        {{value: 0, name: '一般风险', itemStyle: {{color:'#e3b341'}}}},
      ],
      label: {{ color: '#c9d1d9' }}
    }}]
  }});

  // 竞品雷达图
  var radar = echarts.init(document.getElementById('competitor-radar'));
  radar.setOption({{
    backgroundColor: 'transparent',
    title: {{ text: '竞品能力雷达图', textStyle: {{ color: '#c9d1d9', fontSize: 13 }} }},
    tooltip: {{}},
    radar: {{
      indicator: [
        {{name:'专利规模'}}, {{name:'技术覆盖'}}, {{name:'研发投入'}},
        {{name:'海外布局'}}, {{name:'TRL成熟度'}}, {{name:'团队稳定性'}}
      ],
      axisName: {{ color: '#8b949e' }}
    }},
    series: [{{
      type: 'radar',
      data: (window.__reportData && window.__reportData.radarData) || []
    }}]
  }});

  // 研发投入趋势
  var rdChart = echarts.init(document.getElementById('rd-invest-chart'));
  rdChart.setOption({{
    backgroundColor: 'transparent',
    title: {{ text: '研发投入趋势', textStyle: {{ color: '#c9d1d9', fontSize: 13 }} }},
    xAxis: {{ type: 'category', data: (window.__reportData && window.__reportData.rdYears) || ['2021','2022','2023','2024'] }},
    yAxis: {{ type: 'value', axisLabel: {{ color: '#8b949e' }} }},
    series: [{{
      type: 'bar',
      data: (window.__reportData && window.__reportData.rdValues) || [],
      itemStyle: {{ color: '#58a6ff' }}
    }}]
  }});

  window.addEventListener('resize', function() {{
    patentChart.resize(); riskPie.resize(); radar.resize(); rdChart.resize();
  }});
}});
</script>
</body>
</html>"""
    return html


# ─── 入口 ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    args = parse_args()
    workflow = DueDiligenceWorkflow(args)
    output_path = workflow.run()
    print(f"\n✅ 尽调报告已生成：{output_path}")
    print("   在浏览器中打开即可查看，Ctrl+P 可导出为 PDF。")

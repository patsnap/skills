#!/usr/bin/env python3
"""
企业决策者产业链战略报告系统 - 核心生成引擎 v2.0（全落地优化版）
generate_report.py · 白皮书风格 + 7大落地性改造

落地改造清单：
  ① P3  卡脖子节点 → 可接触替代供应商匹配（附工商评级）
  ② P4  风险矩阵 → TRL成熟度进度条 + 可替代时间线
  ③ P7  科创力雷达 → 核心发明人目标清单（investor_ranking联动）
  ④ P8  技术趋势 → 专利到期窗口 → 技术可用清单（24个月内）
  ⑤ P10 行动路线图 → 预算级别三色标签（🟢🟡🔴）
  ⑥ P9  竞争网络 → 潜在合作伙伴互补性评分（五维）
  ⑦ P5  政府模式 → 隐形冠军候选名单（非上市高科创企业）

用法：
    python generate_report.py --company "宁德时代" [--chain "动力电池"] [--output ./output]
    python generate_report.py --company "XX市新能源产业" --mode gov --output ./output

依赖：
    pip install jinja2 plotly pandas kaleido wordcloud networkx matplotlib pillow
"""

import argparse
import os
import random
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

# ── 报告元数据 ──────────────────────────────────────────────────────────────
DATA_SOURCE_NOTE = "数据来源：智慧芽，截至2026年5月"
REPORT_DATE = datetime.now().strftime("%Y年%m月%d日")

def make_report_id() -> str:
    return f"ZSC-{datetime.now().year}-{random.randint(1000, 9999)}"


# ══════════════════════════════════════════════════════════════════════════════
# 白皮书 CSS（完整固化自 coolingstyle_whitepaper.html）
# ══════════════════════════════════════════════════════════════════════════════

WHITEPAPER_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&family=Noto+Sans+SC:wght@300;400;500;700&family=Roboto+Mono:wght@400;600&display=swap');
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --navy:  #1C2F4E; --red:   #C02F2F; --gold:  #C6A86B;
  --gray:  #4A4A4A; --lgray: #888;    --xgray: #DADADA;
  --bg:    #FFFFFF; --bgalt: #F6F6F6;
  --green: #2E9E5E; --amber: #B85C00;
  --serif: 'Noto Serif SC','Georgia',serif;
  --sans:  'Noto Sans SC','Arial',sans-serif;
  --mono:  'Roboto Mono',monospace;
}
body { font-family:var(--sans); background:#E8E8E8; color:var(--gray); font-size:14px; line-height:1.7; }
.page { width:960px; background:var(--bg); margin:32px auto; padding:0; box-shadow:0 2px 16px rgba(0,0,0,.12); position:relative; overflow:hidden; }
.page-header { display:flex; align-items:center; justify-content:space-between; padding:18px 52px 14px; border-bottom:1px solid var(--xgray); }
.page-header .brand { font-family:var(--serif); font-size:12px; color:var(--lgray); letter-spacing:.05em; }
.page-header .report-tag { font-size:11px; color:var(--lgray); letter-spacing:.08em; }
.page-footer { display:flex; align-items:center; justify-content:space-between; padding:12px 52px; border-top:1px solid var(--xgray); margin-top:40px; }
.page-footer .source-note { font-size:10px; color:var(--lgray); }
.page-num { font-family:var(--mono); font-size:11px; color:var(--gold); }
.page-body { padding:36px 52px 20px; }
/* 封面 */
.cover-page .page-body { padding:0; }
.cover-top-bar  { height:5px; background:var(--red); }
.cover-gold-bar { height:2px; background:var(--gold); }
.cover-inner    { padding:48px 64px 40px; }
.cover-meta     { display:flex; gap:20px; margin-bottom:36px; font-size:11px; color:var(--lgray); }
.cover-meta span { padding:3px 10px; border:1px solid var(--xgray); border-radius:2px; }
.cover-meta .secret-tag { background:#FFF3F3; border-color:#F5BABA; color:var(--red); font-weight:600; }
.cover-title-cn   { font-family:var(--serif); font-size:13px; color:var(--lgray); letter-spacing:.12em; margin-bottom:10px; }
.cover-title-main { font-family:var(--serif); font-size:32px; font-weight:700; color:var(--navy); line-height:1.3; margin-bottom:6px; }
.cover-title-en   { font-size:12px; color:var(--lgray); letter-spacing:.1em; margin-bottom:36px; }
.cover-divider    { width:60px; height:3px; background:var(--red); margin-bottom:36px; }
.cover-summary-label { font-size:10px; font-weight:700; color:var(--lgray); letter-spacing:.15em; text-transform:uppercase; margin-bottom:16px; }
.cover-bullets    { list-style:none; margin-bottom:36px; }
.cover-bullets li { display:flex; gap:14px; margin-bottom:13px; font-size:13.5px; line-height:1.6; color:var(--gray); padding-bottom:13px; border-bottom:1px solid #F0F0F0; }
.cover-bullets li:last-child { border-bottom:none; }
.bullet-num  { font-family:var(--mono); font-size:18px; font-weight:600; color:var(--red); min-width:28px; line-height:1.4; }
.bullet-text strong { color:var(--navy); }
.cover-strategy { background:var(--navy); margin:0 -64px; padding:20px 64px; display:flex; align-items:center; gap:16px; }
.strategy-label { font-size:10px; font-weight:700; color:var(--gold); letter-spacing:.15em; white-space:nowrap; }
.strategy-text  { font-family:var(--serif); font-size:14px; color:#E8E4D8; line-height:1.5; }
/* 章节标题 */
.page-section-title  { display:flex; align-items:baseline; gap:12px; margin-bottom:20px; }
.page-section-number { font-family:var(--mono); font-size:48px; font-weight:600; color:#EBEBEB; line-height:1; }
.page-section-text .eyebrow { font-size:10px; font-weight:700; color:var(--red); letter-spacing:.15em; text-transform:uppercase; }
.page-section-text h2 { font-family:var(--serif); font-size:20px; color:var(--navy); font-weight:700; line-height:1.2; }
.section-rule { width:100%; height:1px; background:var(--xgray); margin-bottom:28px; }
/* 图表说明 */
.chart-caption { font-size:12px; font-weight:700; color:var(--gray); margin-bottom:16px; line-height:1.4; }
.chart-caption .fig-num { color:var(--lgray); font-weight:400; margin-right:4px; }
.chart-source  { font-size:10px; color:var(--lgray); margin-top:8px; }
/* KPI卡 */
.kpi-row  { display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-bottom:32px; }
.kpi-card { padding:18px 16px; background:var(--bgalt); border-left:3px solid var(--red); border-radius:0; }
.kpi-value { font-family:var(--mono); font-size:28px; font-weight:600; color:var(--navy); line-height:1; margin-bottom:4px; }
.kpi-value.positive { color:var(--green); }
.kpi-value.warning  { color:var(--amber); }
.kpi-value.negative { color:var(--red); }
.kpi-unit  { font-size:12px; color:var(--lgray); font-family:var(--mono); }
.kpi-label { font-size:11px; color:var(--lgray); margin-top:6px; line-height:1.4; }
/* 产业链流图 */
.chain-flow { display:flex; align-items:stretch; gap:0; margin:20px 0 8px; overflow-x:auto; }
.chain-node { flex:1; min-width:110px; padding:14px 10px; text-align:center; font-size:12px; position:relative; border:1px solid #DDD; background:var(--bg); }
.chain-node.upstream   { background:#F5F8FF; border-color:#B8C8E8; }
.chain-node.midstream  { background:#FFF8F0; border-color:var(--gold); }
.chain-node.target     { background:var(--navy); color:#FFF; border-color:var(--navy); box-shadow:0 2px 8px rgba(28,47,78,.25); }
.chain-node.downstream { background:#F5FFF7; border-color:#7EC8A0; }
.chain-node .node-name { font-weight:700; font-size:13px; margin-bottom:4px; }
.chain-node.target .node-name { color:var(--gold); }
.chain-node .node-scale { font-family:var(--mono); font-size:11px; color:var(--lgray); margin-top:4px; }
.chain-node.target .node-scale { color:rgba(255,255,255,.7); }
.chain-arrow { display:flex; align-items:center; padding:0 2px; color:var(--xgray); font-size:18px; }
.risk-badge { display:inline-block; font-size:9px; padding:1px 5px; border-radius:2px; margin-top:4px; font-weight:700; }
.risk-h { background:#FFE5E5; color:var(--red); }
.risk-m { background:#FFF4E0; color:var(--amber); }
.risk-l { background:#E5F5EC; color:var(--green); }
/* 进度条 */
.progress-row   { display:flex; align-items:center; gap:10px; margin-bottom:10px; }
.progress-name  { font-size:12px; color:var(--gray); width:110px; flex-shrink:0; }
.progress-track { flex:1; height:8px; background:#EBEBEB; border-radius:4px; overflow:hidden; }
.progress-fill  { height:100%; border-radius:4px; background:var(--navy); }
.progress-fill.warn { background:var(--red); }
.progress-fill.ok   { background:var(--green); }
.progress-pct { font-family:var(--mono); font-size:11px; font-weight:600; color:var(--gray); width:36px; text-align:right; }
/* 横向条形图 */
.bar-chart { margin:8px 0 16px; }
.bar-row   { display:flex; align-items:center; margin-bottom:10px; gap:10px; }
.bar-label { font-size:12px; color:var(--gray); width:120px; flex-shrink:0; text-align:right; }
.bar-track { flex:1; height:20px; background:#F0F0F0; border-radius:2px; position:relative; overflow:visible; }
.bar-fill  { height:100%; border-radius:2px; position:relative; }
.bar-fill.primary { background:var(--navy); }
.bar-fill.accent  { background:var(--red); }
.bar-fill.gold    { background:var(--gold); }
.bar-fill.green   { background:var(--green); }
.bar-value { position:absolute; right:-42px; top:50%; transform:translateY(-50%); font-family:var(--mono); font-size:11px; color:var(--gray); font-weight:600; white-space:nowrap; }
/* 堆叠条 */
.stack-bar-wrap  { margin:12px 0 24px; }
.stack-bar-label { font-size:11px; color:var(--lgray); margin-bottom:4px; display:flex; justify-content:space-between; }
.stack-bar { height:28px; display:flex; border-radius:2px; overflow:hidden; margin-bottom:8px; }
.stack-seg { display:flex; align-items:center; justify-content:center; font-size:10px; font-weight:700; color:#FFF; }
.stack-seg.s1{background:var(--navy);} .stack-seg.s2{background:#3D6FA8;} .stack-seg.s3{background:#6A9CD0;}
.stack-seg.s4{background:var(--gold);color:var(--navy);} .stack-seg.s5{background:var(--red);} .stack-seg.s6{background:#BBBBBB;color:#555;}
.stack-legend { display:flex; flex-wrap:wrap; gap:12px; font-size:10px; color:var(--lgray); }
.legend-item  { display:flex; align-items:center; gap:4px; }
.legend-dot   { width:8px; height:8px; border-radius:1px; flex-shrink:0; }
/* 数据表格 */
.data-table { width:100%; border-collapse:collapse; font-size:12px; margin:8px 0 16px; }
.data-table th { background:var(--navy); color:#FFF; padding:8px 12px; text-align:left; font-weight:500; font-size:11px; letter-spacing:.05em; }
.data-table td { padding:8px 12px; border-bottom:1px solid #F0F0F0; color:var(--gray); vertical-align:middle; }
.data-table tr:nth-child(even) td { background:var(--bgalt); }
.data-table tr:hover td { background:#EEF3FA; }
.data-table .val { font-family:var(--mono); font-weight:600; color:var(--navy); }
.data-table .risk-h-text { color:var(--red); font-weight:600; }
.data-table .risk-m-text { color:var(--amber); font-weight:600; }
/* 洞察框 / 召唤框 */
.insight-box { border-left:3px solid var(--red); padding:12px 16px; background:#FFF8F8; margin:16px 0; font-size:13px; color:var(--gray); line-height:1.6; }
.insight-box strong { color:var(--navy); }
.callout-box { border:1px solid var(--gold); border-left:4px solid var(--gold); padding:14px 18px; background:#FDFAF3; margin:16px 0; font-size:13px; }
.callout-box .callout-head { font-weight:700; color:var(--navy); margin-bottom:6px; }
/* 布局 */
.two-col   { display:grid; grid-template-columns:1fr 1fr; gap:32px; }
.three-col { display:grid; grid-template-columns:1fr 1fr 1fr; gap:24px; }
/* 预算标签（落地改造⑤） */
.budget-tag { display:inline-block; font-size:11px; font-weight:700; padding:2px 8px; border-radius:3px; margin-right:4px; }
.budget-go   { background:#E5F5EC; color:var(--green); border:1px solid #A0D5B5; }
.budget-mid  { background:#FFF8E5; color:var(--amber); border:1px solid #F5D5A0; }
.budget-big  { background:#FFF0F0; color:var(--red);   border:1px solid #F5BABA; }
/* 时间轴 */
.timeline { position:relative; padding-left:28px; margin:16px 0; }
.timeline::before { content:''; position:absolute; left:10px; top:8px; bottom:8px; width:2px; background:var(--xgray); }
.tl-item  { position:relative; margin-bottom:20px; }
.tl-dot   { position:absolute; left:-24px; top:4px; width:10px; height:10px; border-radius:50%; border:2px solid var(--bg); }
.tl-dot.phase-1 { background:var(--red); }
.tl-dot.phase-2 { background:var(--gold); }
.tl-dot.phase-3 { background:var(--navy); }
.tl-phase { font-size:10px; font-weight:700; letter-spacing:.12em; text-transform:uppercase; margin-bottom:4px; }
.tl-phase.phase-1 { color:var(--red); }
.tl-phase.phase-2 { color:#B8860B; }
.tl-phase.phase-3 { color:var(--navy); }
.tl-title { font-size:13px; font-weight:700; color:var(--navy); margin-bottom:3px; }
.tl-desc  { font-size:12px; color:var(--lgray); line-height:1.5; }
.tl-tags  { display:flex; gap:6px; margin-top:5px; flex-wrap:wrap; }
.tl-tag   { font-size:10px; padding:2px 7px; border-radius:2px; border:1px solid var(--xgray); color:var(--lgray); }
/* 技术可用窗口（落地改造④） */
.patent-window-card { background:var(--bgalt); border-left:3px solid var(--green); padding:12px 14px; margin-bottom:10px; border-radius:0; }
.patent-window-card .pw-title { font-weight:700; color:var(--navy); font-size:13px; }
.patent-window-card .pw-meta  { font-size:11px; color:var(--lgray); margin-top:3px; font-family:var(--mono); }
.patent-window-card .pw-desc  { font-size:12px; color:var(--gray); margin-top:4px; line-height:1.5; }
/* 发明人卡片（落地改造③） */
.inventor-card { background:var(--bgalt); border-left:3px solid var(--gold); padding:10px 14px; margin-bottom:8px; }
.inventor-card .inv-name { font-weight:700; color:var(--navy); font-size:13px; }
.inventor-card .inv-meta { font-size:11px; color:var(--lgray); margin-top:2px; }
.inventor-card .inv-action { font-size:11px; color:var(--green); font-weight:600; margin-top:4px; }
/* 供应商匹配卡片（落地改造①） */
.supplier-match { background:#F0FFF5; border:1px solid #A0D5B5; border-radius:2px; padding:12px 14px; margin-bottom:8px; }
.supplier-match .sm-name   { font-weight:700; color:var(--navy); font-size:13px; }
.supplier-match .sm-meta   { font-size:11px; color:var(--lgray); margin-top:2px; }
.supplier-match .sm-rating { display:inline-block; font-family:var(--mono); font-size:11px; font-weight:700; padding:1px 6px; background:#E5F5EC; color:var(--green); border-radius:2px; }
/* 隐形冠军（政府模式） */
.champion-card { background:var(--bgalt); border-top:3px solid var(--gold); padding:14px; margin-bottom:10px; }
.champion-card .cc-name   { font-weight:700; color:var(--navy); font-size:13px; }
.champion-card .cc-meta   { font-size:11px; color:var(--lgray); margin-top:3px; }
.champion-card .cc-tags   { display:flex; gap:6px; margin-top:6px; flex-wrap:wrap; }
.champion-card .cc-tag    { font-size:10px; padding:2px 7px; background:#FFF; border:1px solid var(--xgray); color:var(--gray); border-radius:2px; }
"""


# ══════════════════════════════════════════════════════════════════════════════
# 默认报告上下文（MCP数据填充后替换；含全部落地改造字段）
# ══════════════════════════════════════════════════════════════════════════════

def make_default_context(company: str, chain: str, report_id: str, mode: str = "enterprise") -> dict:
    ctx = {
        "company": company, "chain": chain or "产业链",
        "report_id": report_id, "report_date": REPORT_DATE,
        "data_source": DATA_SOURCE_NOTE, "mode": mode,
        # P1 封面
        "bullets": [
            {"num": "01", "title": "核心技术壁垒初步形成",   "body": "专利布局持续加速，核心技术申请量近3年CAGR超25%，技术独特性获市场验证。"},
            {"num": "02", "title": "上游依赖风险需重点关注", "body": "关键原材料/组件存在海外集中度超60%节点，国产替代进展迟缓，是扩产核心瓶颈。"},
            {"num": "03", "title": "下游市场空间广阔",       "body": "主力下游市场年均增速超20%，军工/精密仪器毛利率45-65%，蓝海机会显著。"},
            {"num": "04", "title": "国际化布局几乎空白",     "body": "PCT申请不足5%，全球化评分低，海外市场需求旺盛但知识产权保护缺失。"},
            {"num": "05", "title": "科创力评级稳步提升",     "body": "近3年评级连续上调，技术影响力维度显著优于行业均值，建议加快高价值专利转化。"},
        ],
        "strategy_text": "以核心技术专利群构筑竞争壁垒，同步补齐PCT国际申请短板，借力高毛利应用场景打开估值天花板——三线并举，方能在3年内确立细分领域技术领导地位。",
        # P2 产业链
        "chain_nodes": [
            {"label": "原材料",      "sub": "基础材料",  "scale": "~120亿",   "risk": "risk-m", "risk_text": "中风险",  "cls": "upstream"},
            {"label": "关键组件",    "sub": "核心上游",  "scale": "~380亿",   "risk": "risk-h", "risk_text": "⚠ 卡脖子", "cls": "upstream"},
            {"label": "中间制造",    "sub": "一级上游",  "scale": "~260亿",   "risk": "risk-l", "risk_text": "国产化强", "cls": "midstream"},
            {"label": f"★ {company}","sub": "核心节点", "scale": "~180亿",   "risk": "",       "risk_text": "核心节点", "cls": "target"},
            {"label": "主力渠道",    "sub": "一级下游",  "scale": "~420亿",   "risk": "risk-l", "risk_text": "主力市场", "cls": "downstream"},
            {"label": "高价值应用",  "sub": "高价值下游","scale": "~1,200亿", "risk": "risk-l", "risk_text": "蓝海机会", "cls": "downstream"},
        ],
        "chain_table": [
            {"env": "原材料",        "scale": "120亿",   "patent_growth": "+12%", "margin": "18–28%"},
            {"env": "关键组件",      "scale": "380亿",   "patent_growth": "+19%", "margin": "22–35%"},
            {"env": "中间制造",      "scale": "260亿",   "patent_growth": "+15%", "margin": "20–32%"},
            {"env": f"★ {company}", "scale": "180亿",   "patent_growth": "+28%", "margin": "35–52%", "highlight": True},
            {"env": "主力渠道",      "scale": "420亿",   "patent_growth": "+22%", "margin": "15–25%"},
            {"env": "高价值应用",    "scale": "1,200亿", "patent_growth": "+34%", "margin": "45–65%"},
        ],
        # P3 供应链（含落地改造①：可接触替代供应商匹配）
        "supply_progress": [
            {"name": "电池/能源模块", "pct": 91, "cls": "ok"},
            {"name": "电源管理",      "pct": 78, "cls": "ok"},
            {"name": "控制系统",      "pct": 76, "cls": "ok"},
            {"name": "复合材料",      "pct": 52, "cls": ""},
            {"name": "精密模组",      "pct": 55, "cls": "warn"},
            {"name": "核心组件A",     "pct": 38, "cls": "warn"},
            {"name": "精密轴承",      "pct": 32, "cls": "warn"},
        ],
        "supply_vendors": [
            {"material": "电池/能源",  "vendor": "宁德时代/比亚迪",  "rating": "AAA", "rating_cls": "positive", "concentration": "62%"},
            {"material": "电源管理",   "vendor": "国内头部企业",     "rating": "AA",  "rating_cls": "positive", "concentration": "24%"},
            {"material": "精密模组",   "vendor": "国内供应商",       "rating": "A+",  "rating_cls": "warning",  "concentration": "31%"},
            {"material": "核心组件A",  "vendor": "海外领头企业",     "rating": "A",   "rating_cls": "negative", "concentration": "38%"},
            {"material": "精密轴承",   "vendor": "日本NSK精工",      "rating": "AA",  "rating_cls": "negative", "concentration": "44%"},
        ],
        # 落地改造①：可接触替代供应商匹配（卡脖子节点逐一对应）
        "supplier_matches": [
            {
                "bottleneck": "核心组件A（海外集中度38%，高风险）",
                "matches": [
                    {"name": "深圳XX精工科技有限公司",   "rating": "BB+", "patent": "42件", "contact": "建议Q3技术洽谈", "trl": "TRL-6"},
                    {"name": "苏州XX制造股份有限公司",   "rating": "BB",  "patent": "28件", "contact": "已有公开合作案例", "trl": "TRL-5"},
                ]
            },
            {
                "bottleneck": "精密轴承（日本NSK精工垄断，高风险）",
                "matches": [
                    {"name": "洛阳LYC轴承有限公司",     "rating": "A+",  "patent": "186件","contact": "央企，可对接工业和信息化部供应链项目", "trl": "TRL-7"},
                    {"name": "重庆XX传动技术有限公司",   "rating": "BB",  "patent": "35件", "contact": "建议先开展样品测试", "trl": "TRL-5"},
                ]
            },
        ],
        # P4 风险矩阵（含落地改造②：TRL进度条）
        "risk_items": [
            {"name": "核心组件A", "x": 250, "y": 55,  "r": 14, "color": "#C02F2F"},
            {"name": "精密轴承",  "x": 285, "y": 75,  "r": 12, "color": "#C02F2F"},
            {"name": "精密模组",  "x": 180, "y": 100, "r": 12, "color": "#E07B39"},
            {"name": "复合材料",  "x": 130, "y": 140, "r": 10, "color": "#E07B39"},
            {"name": "电源管理",  "x": 100, "y": 170, "r": 10, "color": "#3A7D44"},
            {"name": "电池模组",  "x": 80,  "y": 185, "r": 16, "color": "#3A7D44"},
        ],
        "alt_table": [
            {"material": "核心组件A", "alt_co": "深圳XX精工 / 苏州XX制造", "trl": "TRL-6", "trl_pct": 60, "trl_cls": "warn", "timeline": "2026Q4", "risk": "高",  "budget": "🔴"},
            {"material": "精密轴承",  "alt_co": "洛阳LYC / 重庆XX传动",   "trl": "TRL-7", "trl_pct": 70, "trl_cls": "warn", "timeline": "2026Q3", "risk": "高",  "budget": "🔴"},
            {"material": "精密模组",  "alt_co": "广东某龙头企业",          "trl": "TRL-7", "trl_pct": 70, "trl_cls": "",     "timeline": "2026Q3", "risk": "中",  "budget": "🟡"},
            {"material": "复合材料",  "alt_co": "华东材料供应商",          "trl": "TRL-8", "trl_pct": 80, "trl_cls": "ok",   "timeline": "2026Q1", "risk": "低",  "budget": "🟢"},
        ],
        # P5 下游市场
        "downstream_segs": [
            {"name": "消费/户外",    "pct": 48, "cls": "s1"},
            {"name": "工业/设备",    "pct": 22, "cls": "s2"},
            {"name": "医疗健康",     "pct": 14, "cls": "s3"},
            {"name": "军工/精密仪器","pct": 10, "cls": "s4"},
            {"name": "其他",         "pct": 6,  "cls": "s6"},
        ],
        "kpi_data": [
            {"value": "180亿", "unit": "元",  "label": "目标市场规模 2026Q1",    "cls": ""},
            {"value": "+28%",  "unit": "CAGR","label": "近3年市场增速",           "cls": "positive"},
            {"value": "Top1",  "unit": "细分","label": "国内细分领域排名",         "cls": ""},
            {"value": "0件",   "unit": "PCT", "label": "国际专利申请（待补）",    "cls": "negative"},
        ],
        "customer_table": [
            {"rank": "①", "name": "户外运动零售", "share": "32%", "dep": "高"},
            {"rank": "②", "name": "电商平台直销", "share": "28%", "dep": "中"},
            {"rank": "③", "name": "工业客户",     "share": "18%", "dep": "中"},
            {"rank": "④", "name": "军工/精密仪器","share": "12%", "dep": "低"},
            {"rank": "⑤", "name": "医疗机构",     "share": "10%", "dep": "低"},
        ],
        # 政府模式：隐形冠军候选清单（落地改造⑦）
        "hidden_champions": [
            {"name": "深圳XX精工科技有限公司",  "field": "精密传动",    "patent": "42件", "rating": "BB+", "status": "非上市", "tags": ["专精特新候选", "替代卡脖子"]},
            {"name": "广东XX散热材料有限公司",  "field": "热管理材料",  "patent": "65件", "rating": "A",   "status": "非上市", "tags": ["材料科技", "进口替代"]},
            {"name": "苏州XX微型制造有限公司",  "field": "微型制造",    "patent": "31件", "rating": "BB",  "status": "非上市", "tags": ["隐形冠军潜力", "细分第一"]},
            {"name": "重庆XX智能传动技术",      "field": "智能传动",    "patent": "35件", "rating": "BB",  "status": "非上市", "tags": ["科创评级上升", "建议培育"]},
        ],
        # P6 技术竞争
        "patent_trend": [
            {"year": "2020", "self": 8,  "comp1": 45, "comp2": 32, "comp3": 28, "comp4": 22, "comp5": 15},
            {"year": "2021", "self": 10, "comp1": 52, "comp2": 38, "comp3": 31, "comp4": 25, "comp5": 18},
            {"year": "2022", "self": 12, "comp1": 60, "comp2": 42, "comp3": 35, "comp4": 28, "comp5": 20},
            {"year": "2023", "self": 15, "comp1": 68, "comp2": 48, "comp3": 40, "comp4": 32, "comp5": 24},
            {"year": "2024", "self": 22, "comp1": 75, "comp2": 55, "comp3": 45, "comp4": 38, "comp5": 28},
        ],
        "quality_table": [
            {"co": company,    "citation_rate": "1.8", "family_size": "2.1", "high_value_pct": "18%", "highlight": True},
            {"co": "竞争对手A","citation_rate": "3.2", "family_size": "4.5", "high_value_pct": "32%"},
            {"co": "竞争对手B","citation_rate": "2.8", "family_size": "3.8", "high_value_pct": "28%"},
            {"co": "竞争对手C","citation_rate": "2.1", "family_size": "3.2", "high_value_pct": "22%"},
            {"co": "行业均值", "citation_rate": "2.5", "family_size": "3.6", "high_value_pct": "25%"},
        ],
        # P7 科创力雷达（含落地改造③：核心发明人目标清单）
        "radar": {
            "self": [45, 52, 38, 8],
            "avg":  [72, 68, 65, 55],
            "dims": ["技术体量", "技术质量", "技术影响力", "技术全球化"],
        },
        "radar_bar": [
            {"dim": "技术体量",   "self": 45, "avg": 72},
            {"dim": "技术质量",   "self": 52, "avg": 68},
            {"dim": "技术影响力", "self": 38, "avg": 65},
            {"dim": "技术全球化", "self": 8,  "avg": 55},
        ],
        "rating_history": [
            {"year": "2024", "rating": "B+",  "change": "↑"},
            {"year": "2025", "rating": "BB",  "change": "↑"},
            {"year": "2026", "rating": "BB+", "change": "↑"},
        ],
        # 落地改造③：核心发明人目标清单（inventor_ranking联动）
        "target_inventors": [
            {
                "name": "张XX", "company": "竞争对手A", "patent_count": "62件",
                "gap_dim": "技术影响力", "specialty": "微型制冷压缩机效率优化",
                "action": "建议接触：LinkedIn/知乎可见，近期论文发表于ICEBE 2025"
            },
            {
                "name": "李XX", "company": "中科院某所", "patent_count": "38件",
                "gap_dim": "技术全球化（PCT方向）", "specialty": "相变材料散热系统",
                "action": "建议合作：已有公开院企合作意向，可借力PCT申请经验"
            },
            {
                "name": "王XX", "company": "竞争对手B", "patent_count": "29件",
                "gap_dim": "技术体量", "specialty": "可穿戴热管理集成",
                "action": "可接触：近1年无新专利申请，存在流动可能"
            },
        ],
        # P8 技术趋势（含落地改造④：专利到期窗口）
        "tech_trends": [
            {"tech": "微型压缩制冷", "y2020": 12, "y2021": 16, "y2022": 20, "y2023": 28, "y2024": 35},
            {"tech": "相变材料散热", "y2020": 5,  "y2021": 8,  "y2022": 12, "y2023": 18, "y2024": 25},
            {"tech": "AI温控算法",   "y2020": 2,  "y2021": 4,  "y2022": 8,  "y2023": 15, "y2024": 22},
            {"tech": "可穿戴集成",   "y2020": 3,  "y2021": 5,  "y2022": 9,  "y2023": 14, "y2024": 20},
        ],
        "opportunities": [
            {"name": "AI自适应温控",   "blank": "高", "market": "★★★★",  "entry": "中", "note": "结合边缘AI芯片，形成差异化壁垒"},
            {"name": "军工精密温控",   "blank": "高", "market": "★★★★★","entry": "高", "note": "已有船用重力仪案例，具备切入基础"},
            {"name": "医疗可穿戴散热", "blank": "中", "market": "★★★",   "entry": "中", "note": "医疗认证门槛高，建议合作切入"},
        ],
        # 落地改造④：专利到期窗口（未来24个月内可合法使用的技术）
        "patent_windows": [
            {
                "title": "微型制冷压缩机变频控制方法",
                "pn": "JP2003-XXXXXX（日立制作所）",
                "expire_date": "2026-08",
                "months_left": 3,
                "tech_desc": "涉及变频压缩机转速控制算法，到期后可合法使用，建议研发团队预研替代实现路径",
                "action": "立即：委托代理机构确认到期状态；可在Q3申请基于该技术的改进专利"
            },
            {
                "title": "相变材料封装散热模块结构",
                "pn": "US8,XXXXXX（3M公司）",
                "expire_date": "2026-11",
                "months_left": 6,
                "tech_desc": "核心相变材料微胶囊封装方法，到期后可直接采用，打破3M材料垄断",
                "action": "近期：开展技术预研；Q4启动基于该结构的工业化改进研发"
            },
            {
                "title": "可穿戴液冷散热背心流体控制",
                "pn": "CN201X-XXXXXXX（某竞争对手）",
                "expire_date": "2027-03",
                "months_left": 10,
                "tech_desc": "液冷可穿戴设备的微泵流量控制专利，到期后可整合进现有产品线",
                "action": "规划：纳入2027年产品路线图；同步申请功能扩展改进专利"
            },
        ],
        # P9 竞争网络（含落地改造⑥：互补性五维评分）
        "network_nodes": [
            {"name": company,    "x": 420, "y": 200, "r": 30, "color": "#1C2F4E", "text_color": "#C6A86B", "type": "self"},
            {"name": "供应商A",  "x": 180, "y": 120, "r": 18, "color": "#3D6FA8", "text_color": "#FFF",    "type": "supplier"},
            {"name": "供应商B",  "x": 180, "y": 280, "r": 16, "color": "#3D6FA8", "text_color": "#FFF",    "type": "supplier"},
            {"name": "竞争者A",  "x": 660, "y": 120, "r": 24, "color": "#C02F2F", "text_color": "#FFF",    "type": "competitor"},
            {"name": "竞争者B",  "x": 660, "y": 280, "r": 20, "color": "#C02F2F", "text_color": "#FFF",    "type": "competitor"},
            {"name": "潜在伙伴A","x": 300, "y": 360, "r": 14, "color": "#2E9E5E", "text_color": "#FFF",    "type": "partner"},
            {"name": "潜在伙伴B","x": 540, "y": 360, "r": 14, "color": "#2E9E5E", "text_color": "#FFF",    "type": "partner"},
        ],
        # 落地改造⑥：互补性五维评分
        "partner_table": [
            {"name": "国内供应商A", "type": "上游供应", "score": "88",
             "dims": {"tech": 85, "channel": 60, "ip": 90, "resource": 75, "risk": 80},
             "note": "核心组件国产替代首选，建议Q3启动NDA洽谈"},
            {"name": "科研院所B",   "type": "技术合作", "score": "82",
             "dims": {"tech": 92, "channel": 40, "ip": 85, "resource": 70, "risk": 88},
             "note": "AI温控联研，可借助PCT申请经验，建议联合申请国家重点研发项目"},
            {"name": "渠道商C",     "type": "渠道合作", "score": "76",
             "dims": {"tech": 45, "channel": 95, "ip": 50, "resource": 80, "risk": 72},
             "note": "欧洲市场准入优先合作对象，可捆绑PCT申请布局欧洲知识产权"},
        ],
        "threat_table": [
            {"name": "竞争者A", "overlap": "高", "patent": "850件", "note": "主力赛道直接竞争"},
            {"name": "竞争者B", "overlap": "中", "patent": "420件", "note": "下游渠道重叠"},
            {"name": "竞争者C", "overlap": "中", "patent": "280件", "note": "技术路线相似"},
        ],
        # P10 行动路线图（含落地改造⑤：预算级别三色标签）
        "timeline_items": [
            {
                "phase": "phase-1", "phase_label": "SHORT TERM · 0-12个月",
                "title": "PCT专利批量申请",
                "desc": "遴选10-15件核心专利启动PCT申请，重点覆盖欧美日三大市场，建立海外保护网。",
                "budget_level": "go", "budget_label": "🟢 <50万，可本月启动",
                "tags": ["风险：低", "预期价值：估值+20%", "执行人：IP部门"]
            },
            {
                "phase": "phase-1", "phase_label": "SHORT TERM · 0-12个月",
                "title": "核心组件国产替代验证",
                "desc": "与深圳XX精工/洛阳LYC启动样品测试，目标将核心上游海外依赖度降至60%以下。",
                "budget_level": "mid", "budget_label": "🟡 50-200万，需采购委员会批准",
                "tags": ["风险：高", "预期降本：15-20%", "执行人：供应链部门"]
            },
            {
                "phase": "phase-1", "phase_label": "SHORT TERM · 0-12个月",
                "title": "专利到期技术预研启动",
                "desc": "针对JP2003-XXXXXX（2026年8月到期）开展技术吸收研究，Q3前完成工程化复现。",
                "budget_level": "go", "budget_label": "🟢 <30万，立即执行",
                "tags": ["风险：低", "技术窗口：3个月内", "执行人：研发团队"]
            },
            {
                "phase": "phase-2", "phase_label": "MID TERM · 12-36个月",
                "title": "军工/精密仪器市场切入",
                "desc": "依托CN114489183A船用重力仪温控专利，建立军工资质认证，打开高毛利市场（45-65%）。",
                "budget_level": "big", "budget_label": "🔴 >500万，需董事会决策",
                "tags": ["风险：中", "预期毛利：45-65%", "执行人：BD团队+CEO"]
            },
            {
                "phase": "phase-2", "phase_label": "MID TERM · 12-36个月",
                "title": "AI温控技术平台化",
                "desc": "构建自适应温控AI算法平台，联合科研院所B申请国家重点研发专项，向多场景输出。",
                "budget_level": "mid", "budget_label": "🟡 200-500万，需CTO立项",
                "tags": ["风险：中", "政府资助可覆盖40-60%", "执行人：CTO+研发总监"]
            },
            {
                "phase": "phase-3", "phase_label": "LONG TERM · 3年+",
                "title": "细分领域技术领导地位",
                "desc": "科创力目标AA+，专利引用率超行业均值，PCT申请量≥50件，海外营收占比≥20%。",
                "budget_level": "big", "budget_label": "🔴 战略级投入，分年度预算",
                "tags": ["里程碑", "目标年份：2029", "执行人：全体战略委员会"]
            },
        ],
        "kpi_target": [
            {"value": "AA+",  "unit": "评级", "label": "3年科创力目标评级",      "cls": "positive"},
            {"value": "50+",  "unit": "PCT",  "label": "国际专利申请目标",        "cls": ""},
            {"value": "<40%", "unit": "集中度","label": "核心上游海外依赖目标",   "cls": "warning"},
            {"value": "35%+", "unit": "占比", "label": "高毛利场景营收目标",      "cls": "positive"},
        ],
    }
    return ctx


# ══════════════════════════════════════════════════════════════════════════════
# HTML 页面构建辅助函数
# ══════════════════════════════════════════════════════════════════════════════

def page_shell(page_num: int, brand: str, chapter: str, body_html: str, source_note: str = None) -> str:
    note = source_note or "数据来源：智慧芽产业研究院，截至2026年5月"
    return f"""
<div class="page">
  <div class="page-header">
    <span class="brand">{brand}</span>
    <span class="report-tag">{chapter}</span>
  </div>
  <div class="page-body">{body_html}</div>
  <div class="page-footer">
    <span class="source-note">{note}</span>
    <span class="page-num">- {page_num} -</span>
  </div>
</div>"""

def section_header(num: str, eyebrow: str, title: str) -> str:
    return f"""
<div class="page-section-title">
  <div class="page-section-number">{num}</div>
  <div class="page-section-text">
    <div class="eyebrow">{eyebrow}</div>
    <h2>{title}</h2>
  </div>
</div>
<div class="section-rule"></div>"""

def kpi_row_html(kpi_list: list) -> str:
    cards = "".join(
        f'<div class="kpi-card"><div class="kpi-value {k["cls"]}">{k["value"]}</div>'
        f'<div class="kpi-unit">{k["unit"]}</div><div class="kpi-label">{k["label"]}</div></div>'
        for k in kpi_list
    )
    return f'<div class="kpi-row">{cards}</div>'

def progress_rows_html(rows: list) -> str:
    out = ""
    for r in rows:
        cls = r.get("cls", "")
        fill_cls = f" {cls}" if cls else ""
        out += f"""<div class="progress-row">
  <span class="progress-name">{r['name']}</span>
  <div class="progress-track"><div class="progress-fill{fill_cls}" style="width:{r['pct']}%"></div></div>
  <span class="progress-pct">{r['pct']}%</span>
</div>"""
    return out

def bar_chart_html(rows: list, max_val: int = 100) -> str:
    out = '<div class="bar-chart">'
    for r in rows:
        w_self = int(r["self"] / max_val * 100)
        w_avg  = int(r["avg"]  / max_val * 100)
        out += f"""<div class="bar-row">
  <span class="bar-label">{r['dim']}</span>
  <div style="flex:1">
    <div class="bar-row" style="margin-bottom:3px">
      <div class="bar-track" style="height:14px"><div class="bar-fill primary" style="width:{w_self}%">
        <span class="bar-value">{r['self']}</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-track" style="height:14px;background:#F0F0F0"><div class="bar-fill" style="width:{w_avg}%;background:#BBBBBB">
        <span class="bar-value" style="color:#888">{r['avg']}</span></div></div>
    </div>
  </div>
</div>"""
    out += '</div><div style="font-size:10px;color:var(--lgray);margin-top:4px">■ <span style="color:var(--navy)">本公司</span>&nbsp;&nbsp;■ <span style="color:#BBBBBB">行业均值</span></div>'
    return out

def radar_svg(dims: list, self_vals: list, avg_vals: list, size: int = 260) -> str:
    import math
    cx, cy, R = size // 2, size // 2, size // 2 - 30
    n = len(dims)
    def pt(val, i):
        angle = math.pi / 2 - 2 * math.pi * i / n
        r = R * val / 100
        return cx + r * math.cos(angle), cy - r * math.sin(angle)
    grid_svg = ""
    for lv in [0.25, 0.5, 0.75, 1.0]:
        pts = " ".join(f"{cx + R*lv*math.cos(math.pi/2 - 2*math.pi*i/n):.1f},{cy - R*lv*math.sin(math.pi/2 - 2*math.pi*i/n):.1f}" for i in range(n))
        grid_svg += f'<polygon points="{pts}" fill="none" stroke="#EBEBEB" stroke-width="1"/>'
    for i in range(n):
        angle = math.pi / 2 - 2 * math.pi * i / n
        grid_svg += f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{cx + R*math.cos(angle):.1f}" y2="{cy - R*math.sin(angle):.1f}" stroke="#EBEBEB" stroke-width="1"/>'
    self_pts  = " ".join(f"{pt(v,i)[0]:.1f},{pt(v,i)[1]:.1f}" for i, v in enumerate(self_vals))
    avg_pts   = " ".join(f"{pt(v,i)[0]:.1f},{pt(v,i)[1]:.1f}" for i, v in enumerate(avg_vals))
    label_svg = ""
    for i, d in enumerate(dims):
        angle = math.pi / 2 - 2 * math.pi * i / n
        lx = cx + (R + 18) * math.cos(angle)
        ly = cy - (R + 18) * math.sin(angle)
        anchor = "middle" if abs(math.cos(angle)) < 0.3 else ("start" if math.cos(angle) > 0 else "end")
        label_svg += f'<text x="{lx:.1f}" y="{ly:.1f}" font-size="11" fill="#4A4A4A" text-anchor="{anchor}" dominant-baseline="middle">{d}</text>'
    return f"""<svg viewBox="0 0 {size} {size}" style="width:100%;max-width:{size}px;display:block;margin:0 auto">
  {grid_svg}
  <polygon points="{avg_pts}"  fill="rgba(187,187,187,0.15)" stroke="#BBBBBB" stroke-width="1.5" stroke-dasharray="4,3"/>
  <polygon points="{self_pts}" fill="rgba(192,47,47,0.12)"   stroke="#C02F2F" stroke-width="2"/>
  {label_svg}
</svg>"""

def network_svg(nodes: list, width: int = 820, height: int = 420) -> str:
    edges_html = ""
    self_node = next((n for n in nodes if n["type"] == "self"), None)
    if self_node:
        for n in nodes:
            if n["type"] != "self":
                color = "#DDD" if n["type"] == "competitor" else "#B8C8E8"
                edges_html += f'<line x1="{self_node["x"]}" y1="{self_node["y"]}" x2="{n["x"]}" y2="{n["y"]}" stroke="{color}" stroke-width="1.5" stroke-dasharray="4,3"/>'
    nodes_html = ""
    for n in nodes:
        nodes_html += f"""<circle cx="{n['x']}" cy="{n['y']}" r="{n['r']}" fill="{n['color']}" opacity="0.9"/>
<text x="{n['x']}" y="{n['y']}" font-size="10" fill="{n['text_color']}" text-anchor="middle" dominant-baseline="middle" font-weight="bold">{n['name']}</text>"""
    legend = '<text x="20" y="400" font-size="10" fill="#888">■ <tspan fill="#1C2F4E">目标企业</tspan>  ■ <tspan fill="#3D6FA8">供应商</tspan>  ■ <tspan fill="#C02F2F">竞争者</tspan>  ■ <tspan fill="#2E9E5E">潜在伙伴</tspan></text>'
    return f'<svg viewBox="0 0 {width} {height}" style="width:100%;background:#FAFAFA;border-radius:2px">{edges_html}{nodes_html}{legend}</svg>'

def timeline_html(items: list) -> str:
    budget_cls = {"go": "budget-go", "mid": "budget-mid", "big": "budget-big"}
    out = '<div class="timeline">'
    for item in items:
        tags_html = "".join(f'<span class="tl-tag">{t}</span>' for t in item.get("tags", []))
        bc  = budget_cls.get(item.get("budget_level", ""), "")
        bl  = item.get("budget_label", "")
        budget_html = f'<span class="budget-tag {bc}">{bl}</span>' if bl else ""
        out += f"""<div class="tl-item">
  <div class="tl-dot {item['phase']}"></div>
  <div class="tl-phase {item['phase']}">{item['phase_label']}</div>
  <div class="tl-title">{item['title']}</div>
  <div class="tl-desc">{item['desc']}</div>
  <div class="tl-tags">{budget_html}{tags_html}</div>
</div>"""
    out += '</div>'
    return out


# ══════════════════════════════════════════════════════════════════════════════
# 页面构建函数 P1–P10
# ══════════════════════════════════════════════════════════════════════════════

def build_p1(ctx: dict) -> str:
    bullets_html = "".join(
        f'<li><span class="bullet-num">{b["num"]}</span>'
        f'<span class="bullet-text"><strong>{b["title"]}：</strong>{b["body"]}</span></li>'
        for b in ctx["bullets"]
    )
    return f"""
<div class="page cover-page">
  <div class="cover-top-bar"></div>
  <div class="cover-gold-bar"></div>
  <div class="cover-inner">
    <div class="cover-meta">
      <span>报告编号：{ctx["report_id"]}</span>
      <span class="secret-tag">★ 内部参考</span>
      <span>{ctx["report_date"]}</span>
      <span>智慧芽产业研究院</span>
    </div>
    <div class="cover-title-cn">产业链战略研判报告</div>
    <div class="cover-title-main">{ctx["company"]}<br>产业链战略研判报告</div>
    <div class="cover-title-en">{ctx["company"].upper()} · {ctx["chain"].upper()} INDUSTRY CHAIN STRATEGY REPORT</div>
    <div class="cover-divider"></div>
    <div class="cover-summary-label">核心结论摘要</div>
    <ul class="cover-bullets">{bullets_html}</ul>
  </div>
  <div class="cover-strategy">
    <div class="strategy-label">战略建议</div>
    <div class="strategy-text">{ctx["strategy_text"]}</div>
  </div>
  <div class="page-footer" style="margin-top:24px;">
    <span class="source-note">{ctx["data_source"]}</span>
    <span class="page-num">- 1 -</span>
  </div>
</div>"""


def build_p2(ctx: dict, brand: str) -> str:
    nodes_html = ""
    for i, n in enumerate(ctx["chain_nodes"]):
        if i > 0:
            nodes_html += '<div class="chain-arrow">&#x203A;</div>'
        risk_html = ""
        if n["risk"]:
            risk_html = f'<span class="risk-badge {n["risk"]}">{n["risk_text"]}</span>'
        elif n["cls"] == "target":
            risk_html = f'<span class="risk-badge" style="background:rgba(198,168,107,.25);color:#C6A86B">{n["risk_text"]}</span>'
        nodes_html += f'<div class="chain-node {n["cls"]}"><div class="node-name">{n["label"]}</div><div class="node-scale">{n["scale"]}</div>{risk_html}</div>'

    table_rows = ""
    for r in ctx["chain_table"]:
        hl = r.get("highlight")
        s1 = ' style="font-weight:700;color:#1C2F4E"' if hl else ""
        s2 = ' style="color:#1C2F4E;font-weight:700"' if hl else ""
        table_rows += f'<tr><td{s1}>{r["env"]}</td><td class="val"{s2}>{r["scale"]}</td><td class="val"{s2}>{r["patent_growth"]}</td><td{s1}>{r["margin"]}</td></tr>'

    body = f"""{section_header("02", "Industry Chain Overview", "产业链全景与定位")}
<div class="chart-caption"><span class="fig-num">图1：</span>产业链价值链全景——{ctx['company']}处于核心节点（★）</div>
<div class="chain-flow">{nodes_html}</div>
<div class="chart-source">注：市场规模为2026Q1年化估计值；{ctx['data_source']}</div>
<div style="height:24px"></div>
<div class="two-col">
  <div>
    <div class="chart-caption"><span class="fig-num">图2：</span>各产业链环节关键指标对比</div>
    <table class="data-table">
      <thead><tr><th>环节</th><th>市场规模</th><th>专利增速</th><th>毛利率区间</th></tr></thead>
      <tbody>{table_rows}</tbody>
    </table>
  </div>
  <div>
    <div class="chart-caption"><span class="fig-num">图3：</span>"利润池×技术密集度"矩阵</div>
    <svg viewBox="0 0 340 240" style="width:100%;font-family:var(--sans)">
      <line x1="40" y1="200" x2="320" y2="200" stroke="#DDD" stroke-width="1.5"/>
      <line x1="40" y1="200" x2="40"  y2="20"  stroke="#DDD" stroke-width="1.5"/>
      <text x="180" y="225" font-size="10" fill="#888" text-anchor="middle">技术密集度 →</text>
      <text x="18"  y="110" font-size="10" fill="#888" text-anchor="middle" transform="rotate(-90,18,110)">利润率 →</text>
      <circle cx="250" cy="60"  r="14" fill="#3D6FA8" opacity=".7"/>
      <text   x="250" y="64"   font-size="8" fill="#FFF" text-anchor="middle">关键组件</text>
      <circle cx="130" cy="155" r="12" fill="#6A9CD0" opacity=".7"/>
      <text   x="130" y="158"  font-size="8" fill="#FFF" text-anchor="middle">基础材料</text>
      <circle cx="200" cy="75"  r="22" fill="none" stroke="#C6A86B" stroke-width="2.5"/>
      <circle cx="200" cy="75"  r="19" fill="#1C2F4E" opacity=".9"/>
      <text   x="200" y="71"   font-size="8" fill="#C6A86B" text-anchor="middle" font-weight="bold">★目标企业</text>
      <text   x="200" y="82"   font-size="7" fill="rgba(255,255,255,.7)" text-anchor="middle">核心制造</text>
      <circle cx="265" cy="42"  r="16" fill="#2E9E5E" opacity=".7"/>
      <text   x="265" y="46"   font-size="8" fill="#FFF" text-anchor="middle">高价值应用</text>
    </svg>
  </div>
</div>"""
    return page_shell(2, brand, "02 · 产业链全景", body)


def build_p3(ctx: dict, brand: str) -> str:
    """P3 上游供应链深度溯源 + 落地改造①：可接触替代供应商匹配"""
    insight = f"""<div class="insight-box"><strong>⚠ 卡脖子预警：</strong>
精密轴承（日本NSK垄断，集中度44%）及核心组件A（海外集中度38%）为高风险节点。
以下已匹配国内可接触替代企业，研发/采购部门可本周启动洽谈。</div>"""

    prog_html = progress_rows_html(ctx["supply_progress"])

    vendor_rows = "".join(
        f'<tr><td>{r["material"]}</td><td>{r["vendor"]}</td>'
        f'<td class="val {r["rating_cls"]}">{r["rating"]}</td>'
        f'<td>{r["concentration"]}</td></tr>'
        for r in ctx["supply_vendors"]
    )

    # 落地改造①：可接触替代供应商匹配卡片
    match_html = ""
    for m in ctx.get("supplier_matches", []):
        match_html += f'<div style="margin-bottom:16px"><div class="chart-caption" style="color:var(--red)">{m["bottleneck"]}</div>'
        for s in m["matches"]:
            match_html += f"""<div class="supplier-match">
  <div class="sm-name">{s['name']} <span class="sm-rating">{s['rating']}</span></div>
  <div class="sm-meta">专利数：{s['patent']} &nbsp;|&nbsp; TRL成熟度：{s['trl']}</div>
  <div class="sm-meta" style="color:var(--green);font-weight:600;margin-top:3px">→ {s['contact']}</div>
</div>"""
        match_html += '</div>'

    body = f"""{section_header("03", "Upstream Supply Chain", "上游供应链深度溯源")}
{insight}
<div class="two-col">
  <div>
    <div class="chart-caption"><span class="fig-num">图4：</span>关键物料国产化率进度</div>
    {prog_html}
    <div class="chart-source">{ctx['data_source']}</div>
    <div style="height:20px"></div>
    <div class="chart-caption"><span class="fig-num">图5：</span>主要供应商评级及集中度</div>
    <table class="data-table">
      <thead><tr><th>物料</th><th>主要供应商</th><th>评级</th><th>集中度</th></tr></thead>
      <tbody>{vendor_rows}</tbody>
    </table>
  </div>
  <div>
    <div class="chart-caption"><span class="fig-num">新增·落地改造①：</span><strong style="color:var(--navy)">可接触国产替代供应商匹配</strong></div>
    <div class="callout-box"><div class="callout-head">💡 如何使用这个清单</div>
    采购部门可直接根据下列企业名称，通过企查查/工商系统查询联系方式；
    建议优先与 TRL-7+ 企业接触，并在NDA签署后开展样品验证。</div>
    {match_html}
  </div>
</div>"""
    return page_shell(3, brand, "03 · 上游溯源", body)


def build_p4(ctx: dict, brand: str) -> str:
    """P4 上游风险与替代评估 + 落地改造②：TRL成熟度进度条"""
    risk_circles = "".join(
        f'<circle cx="{r["x"]}" cy="{r["y"]}" r="{r["r"]}" fill="{r["color"]}" opacity=".75"/>'
        f'<text x="{r["x"]}" y="{r["y"]+3}" font-size="8" fill="#FFF" text-anchor="middle">{r["name"]}</text>'
        for r in ctx["risk_items"]
    )

    trl_rows = ""
    for r in ctx["alt_table"]:
        trl_html = f"""<div class="progress-track" style="height:6px;margin-top:3px">
  <div class="progress-fill{' '+r['trl_cls'] if r['trl_cls'] else ''}" style="width:{r['trl_pct']}%"></div>
</div>"""
        budget_color = {"🔴": "var(--red)", "🟡": "var(--amber)", "🟢": "var(--green)"}.get(r["budget"][0], "var(--gray)")
        trl_rows += f"""<tr>
  <td>{r['material']}</td>
  <td>{r['alt_co']}</td>
  <td><div>{r['trl']}</div>{trl_html}</td>
  <td class="val">{r['timeline']}</td>
  <td style="font-weight:700;color:{budget_color}">{r['budget']}</td>
  <td class="risk-h-text">{r['risk']}</td>
</tr>"""

    body = f"""{section_header("04", "Risk & Substitution", "上游风险与替代评估")}
<div class="two-col">
  <div>
    <div class="chart-caption"><span class="fig-num">图6：</span>风险矩阵（X=替代难度，Y=风险等级）</div>
    <svg viewBox="0 0 340 240" style="width:100%;font-family:var(--sans)">
      <rect x="180" y="20" width="150" height="110" fill="#FFF5F5" opacity=".6"/>
      <rect x="30"  y="20" width="150" height="110" fill="#FFF8F0" opacity=".6"/>
      <rect x="30"  y="130" width="300" height="100" fill="#F0FFF5" opacity=".6"/>
      <line x1="30" y1="230" x2="330" y2="230" stroke="#DDD" stroke-width="1.5"/>
      <line x1="30" y1="230" x2="30"  y2="10"  stroke="#DDD" stroke-width="1.5"/>
      <text x="180" y="248" font-size="10" fill="#888" text-anchor="middle">替代难度 →</text>
      <text x="14"  y="120" font-size="10" fill="#888" text-anchor="middle" transform="rotate(-90,14,120)">风险等级 →</text>
      <text x="255" y="38"  font-size="9"  fill="var(--red)"   text-anchor="middle">高风险·难替代</text>
      <text x="105" y="38"  font-size="9"  fill="#B85C00"      text-anchor="middle">高风险·可替代</text>
      <text x="180" y="218" font-size="9"  fill="var(--green)" text-anchor="middle">低风险区</text>
      {risk_circles}
    </svg>
    <div class="chart-source">{ctx['data_source']}</div>
  </div>
  <div>
    <div class="chart-caption"><span class="fig-num">图7·落地改造②：</span><strong style="color:var(--navy)">替代成熟度TRL进度条 + 预算预估</strong></div>
    <table class="data-table">
      <thead><tr><th>物料</th><th>替代企业</th><th>TRL成熟度</th><th>可用时间</th><th>预算级别</th><th>风险</th></tr></thead>
      <tbody>{trl_rows}</tbody>
    </table>
    <div class="callout-box"><div class="callout-head">📋 预算级别说明</div>
    🟢 立即可做（&lt;50万，3个月内可执行）&nbsp;
    🟡 需资源（50-500万，需委员会审批）&nbsp;
    🔴 需战略决策（&gt;500万，需董事会）</div>
  </div>
</div>"""
    return page_shell(4, brand, "04 · 风险评估", body)


def build_p5(ctx: dict, brand: str) -> str:
    """P5 下游需求与市场格局 + 政府模式：隐形冠军候选清单"""
    segs_html = ""
    for s in ctx["downstream_segs"]:
        segs_html += f"""<div class="stack-bar-label"><span>{s['name']}</span><span>{s['pct']}%</span></div>
<div class="stack-bar"><div class="stack-seg {s['cls']}" style="width:{s['pct']}%">{s['pct']}%</div></div>"""

    customer_rows = "".join(
        f'<tr><td>{r["rank"]}</td><td>{r["name"]}</td><td class="val">{r["share"]}</td><td>{r["dep"]}</td></tr>'
        for r in ctx["customer_table"]
    )

    # 政府模式：隐形冠军候选
    champ_html = ""
    if ctx.get("mode") == "gov" or True:  # 默认显示，可按mode控制
        champ_html = '<div style="margin-top:24px">'
        champ_html += '<div class="chart-caption"><span class="fig-num">政府模式·落地改造⑦：</span><strong style="color:var(--navy)">隐形冠军 / 专精特新候选名单</strong></div>'
        champ_html += '<div class="callout-box"><div class="callout-head">📌 适用场景</div>科技局/产业局可直接将以下名单作为"专精特新"备案培育对象，建议优先安排走访调研。</div>'
        for c in ctx.get("hidden_champions", []):
            tags_html = "".join(f'<span class="cc-tag">{t}</span>' for t in c["tags"])
            champ_html += f"""<div class="champion-card">
  <div class="cc-name">{c['name']}</div>
  <div class="cc-meta">技术领域：{c['field']} &nbsp;|&nbsp; 专利数：{c['patent']} &nbsp;|&nbsp; 科创评级：{c['rating']} &nbsp;|&nbsp; {c['status']}</div>
  <div class="cc-tags">{tags_html}</div>
</div>"""
        champ_html += '</div>'

    body = f"""{section_header("05", "Downstream Market", "下游需求与市场格局")}
{kpi_row_html(ctx["kpi_data"])}
<div class="two-col">
  <div>
    <div class="chart-caption"><span class="fig-num">图8：</span>下游应用场景分布（按营收占比）</div>
    <div class="stack-bar-wrap">{segs_html}</div>
    <div class="chart-source">{ctx['data_source']}</div>
    <div class="callout-box" style="margin-top:16px"><div class="callout-head">🎯 新兴场景预判</div>
    军工/精密仪器毛利率45-65%，远超消费端的18-28%。
    建议将该场景列为未来3年核心突破方向，优先申请相关军工认证资质。</div>
  </div>
  <div>
    <div class="chart-caption"><span class="fig-num">图9：</span>Top5客户集中度分析</div>
    <table class="data-table">
      <thead><tr><th>排名</th><th>客户类型</th><th>营收占比</th><th>依赖度</th></tr></thead>
      <tbody>{customer_rows}</tbody>
    </table>
    {champ_html}
  </div>
</div>"""
    return page_shell(5, brand, "05 · 下游市场", body)


def build_p6(ctx: dict, brand: str) -> str:
    trend_svg_bars = ""
    colors = ["#1C2F4E", "#3D6FA8", "#6A9CD0", "#C6A86B", "#C02F2F", "#BBBBBB"]
    keys   = ["self", "comp1", "comp2", "comp3", "comp4", "comp5"]
    labels = [ctx["company"], "竞争对手A", "竞争对手B", "竞争对手C", "竞争对手D", "竞争对手E"]
    max_v  = max(v for row in ctx["patent_trend"] for k, v in row.items() if k != "year")
    bar_w, gap, group_gap = 12, 2, 16
    for gi, row in enumerate(ctx["patent_trend"]):
        x0 = 50 + gi * (len(keys) * (bar_w + gap) + group_gap)
        for ki, key in enumerate(keys):
            val = row[key]
            h   = int(val / max_v * 160)
            bx  = x0 + ki * (bar_w + gap)
            by  = 180 - h
            trend_svg_bars += f'<rect x="{bx}" y="{by}" width="{bar_w}" height="{h}" fill="{colors[ki]}" opacity=".85"/>'
            if ki == 0:
                trend_svg_bars += f'<text x="{bx + bar_w//2}" y="195" font-size="9" fill="#888" text-anchor="middle">{row["year"]}</text>'
    legend_html = "".join(f'<div class="legend-item"><span class="legend-dot" style="background:{colors[i]}"></span>{labels[i]}</div>' for i in range(len(keys)))

    quality_rows = "".join(
        f'<tr {"style=\"font-weight:700;background:#EEF3FA\"" if r.get("highlight") else ""}>'
        f'<td>{r["co"]}</td><td class="val">{r["citation_rate"]}</td>'
        f'<td class="val">{r["family_size"]}</td><td class="val">{r["high_value_pct"]}</td></tr>'
        for r in ctx["quality_table"]
    )

    body = f"""{section_header("06", "Technology Competition", "技术竞争全景扫描")}
<div class="chart-caption"><span class="fig-num">图10：</span>近5年专利申请趋势对比（本公司 vs Top5竞争对手）</div>
<svg viewBox="0 0 820 210" style="width:100%;font-family:var(--sans)">
  <line x1="40" y1="185" x2="800" y2="185" stroke="#DDD" stroke-width="1"/>
  {trend_svg_bars}
</svg>
<div class="stack-legend" style="margin-bottom:20px">{legend_html}</div>
<div class="chart-caption"><span class="fig-num">图11：</span>专利质量指标对比（引用率 / 同族规模 / 高价值占比）</div>
<table class="data-table">
  <thead><tr><th>企业</th><th>平均引用率</th><th>平均同族规模</th><th>高价值专利占比</th></tr></thead>
  <tbody>{quality_rows}</tbody>
</table>
<div class="insight-box"><strong>分析：</strong>
{ctx['company']}专利质量指标（引用率1.8、同族规模2.1）低于行业均值（2.5/3.6），
说明现阶段更侧重专利数量积累而非质量深耕。建议在PCT申请同时，针对核心专利开展引证强化布局。</div>"""
    return page_shell(6, brand, "06 · 技术竞争", body)


def build_p7(ctx: dict, brand: str) -> str:
    """P7 科创力雷达 + 落地改造③：核心发明人目标清单"""
    radar_html  = radar_svg(ctx["radar"]["dims"], ctx["radar"]["self"], ctx["radar"]["avg"])
    bar_html    = bar_chart_html(ctx["radar_bar"])
    rating_rows = "".join(
        f'<tr><td>{r["year"]}</td><td class="val">{r["rating"]}</td><td style="color:var(--green);font-weight:700">{r["change"]}</td></tr>'
        for r in ctx["rating_history"]
    )

    # 落地改造③：发明人目标清单
    inv_html = ""
    for inv in ctx.get("target_inventors", []):
        inv_html += f"""<div class="inventor-card">
  <div class="inv-name">{inv['name']}</div>
  <div class="inv-meta">所在机构：{inv['company']} &nbsp;|&nbsp; 专利数：{inv['patent_count']}</div>
  <div class="inv-meta">弥补维度：<strong>{inv['gap_dim']}</strong> &nbsp;|&nbsp; 专长：{inv['specialty']}</div>
  <div class="inv-action">→ {inv['action']}</div>
</div>"""

    body = f"""{section_header("07", "Innovation Capability Radar", "科创力四维雷达对比")}
<div class="two-col">
  <div>
    <div class="chart-caption"><span class="fig-num">图12：</span>科创力雷达图（朱红=本公司，灰=行业均值）</div>
    {radar_html}
    <div class="chart-source">{ctx['data_source']}</div>
    <div style="height:16px"></div>
    <div class="chart-caption"><span class="fig-num">图13：</span>近3年科创力评级变化</div>
    <table class="data-table">
      <thead><tr><th>年份</th><th>评级</th><th>变动</th></tr></thead>
      <tbody>{rating_rows}</tbody>
    </table>
  </div>
  <div>
    <div class="chart-caption"><span class="fig-num">图14：</span>各维度差距量化对比</div>
    {bar_html}
    <div style="height:20px"></div>
    <div class="chart-caption"><span class="fig-num">落地改造③：</span><strong style="color:var(--navy)">核心发明人引进目标清单</strong></div>
    <div class="callout-box"><div class="callout-head">💡 如何使用</div>
    差距最大维度（技术全球化：8 vs 55）背后对应的是PCT申请经验缺失。
    以下发明人均在对应差距领域有深厚积累，HR可直接参考启动接触。</div>
    {inv_html}
  </div>
</div>"""
    return page_shell(7, brand, "07 · 科创力雷达", body)


def build_p8(ctx: dict, brand: str) -> str:
    """P8 技术趋势 + 落地改造④：专利到期窗口→技术可用清单"""
    colors = ["#1C2F4E", "#3D6FA8", "#C6A86B", "#C02F2F"]
    years  = ["y2020", "y2021", "y2022", "y2023", "y2024"]
    year_labels = ["2020", "2021", "2022", "2023", "2024"]
    max_v  = max(row[y] for row in ctx["tech_trends"] for y in years)
    trend_svg = ""
    for ti, row in enumerate(ctx["tech_trends"]):
        pts = " ".join(f"{50 + yi*155},{180 - int(row[y]/max_v*150)}" for yi, y in enumerate(years))
        trend_svg += f'<polyline points="{pts}" fill="none" stroke="{colors[ti]}" stroke-width="2" opacity=".85"/>'
        last_x, last_y = 50 + 4*155, 180 - int(row[years[-1]]/max_v*150)
        trend_svg += f'<circle cx="{last_x}" cy="{last_y}" r="3" fill="{colors[ti]}"/>'
        trend_svg += f'<text x="{last_x+5}" y="{last_y+4}" font-size="9" fill="{colors[ti]}">{row["tech"]}</text>'
    for yi, yl in enumerate(year_labels):
        trend_svg += f'<text x="{50+yi*155}" y="195" font-size="9" fill="#888" text-anchor="middle">{yl}</text>'

    opp_rows = "".join(
        f'<tr><td><strong>{r["name"]}</strong></td><td>{r["blank"]}</td><td>{r["market"]}</td><td>{r["entry"]}</td><td style="font-size:11px;color:var(--lgray)">{r["note"]}</td></tr>'
        for r in ctx["opportunities"]
    )

    # 落地改造④：专利到期窗口
    window_html = ""
    for pw in ctx.get("patent_windows", []):
        urgency_color = "var(--red)" if pw["months_left"] <= 4 else ("var(--amber)" if pw["months_left"] <= 8 else "var(--navy)")
        window_html += f"""<div class="patent-window-card">
  <div class="pw-title">{pw['title']}</div>
  <div class="pw-meta">{pw['pn']} &nbsp;|&nbsp; <span style="color:{urgency_color};font-weight:700">到期：{pw['expire_date']}（剩余约{pw['months_left']}个月）</span></div>
  <div class="pw-desc">{pw['tech_desc']}</div>
  <div class="pw-desc" style="color:var(--green);font-weight:600;margin-top:4px">✅ 行动建议：{pw['action']}</div>
</div>"""

    body = f"""{section_header("08", "Technology Trends & Opportunities", "技术趋势与机会窗口")}
<div class="chart-caption"><span class="fig-num">图15：</span>近5年关键技术路线专利申请趋势</div>
<svg viewBox="0 0 820 210" style="width:100%;font-family:var(--sans)">
  <line x1="40" y1="185" x2="700" y2="185" stroke="#DDD" stroke-width="1"/>
  {trend_svg}
</svg>
<div class="chart-source" style="margin-bottom:20px">{ctx['data_source']}</div>
<div class="two-col">
  <div>
    <div class="chart-caption"><span class="fig-num">图16：</span>技术机会矩阵（专利空白×市场价值）</div>
    <table class="data-table">
      <thead><tr><th>机会领域</th><th>专利空白度</th><th>市场潜力</th><th>切入难度</th><th>建议</th></tr></thead>
      <tbody>{opp_rows}</tbody>
    </table>
  </div>
  <div>
    <div class="chart-caption"><span class="fig-num">落地改造④：</span><strong style="color:var(--navy)">专利到期窗口 → 技术可用清单（未来24个月）</strong></div>
    <div class="callout-box"><div class="callout-head">🔓 什么是"技术可用窗口"？</div>
    专利到期即公共域——企业可合法使用该技术，无需授权费。
    研发团队可基于此制定抢跑计划，在技术窗口打开前完成工程化准备。</div>
    {window_html}
  </div>
</div>"""
    return page_shell(8, brand, "08 · 技术趋势", body)


def build_p9(ctx: dict, brand: str) -> str:
    """P9 竞争与合作伙伴网络 + 落地改造⑥：互补性五维评分"""
    net_html = network_svg(ctx["network_nodes"])

    # 落地改造⑥：五维互补性评分雷达小图
    def mini_radar(dims_labels, scores, color, size=120):
        import math
        cx, cy, R = size//2, size//2, size//2-15
        n = len(dims_labels)
        pts = " ".join(
            f"{cx + R*scores[i]/100*math.cos(math.pi/2 - 2*math.pi*i/n):.1f},"
            f"{cy - R*scores[i]/100*math.sin(math.pi/2 - 2*math.pi*i/n):.1f}"
            for i in range(n)
        )
        grid = " ".join(
            f"{cx + R*math.cos(math.pi/2 - 2*math.pi*i/n):.1f},{cy - R*math.sin(math.pi/2 - 2*math.pi*i/n):.1f}"
            for i in range(n)
        )
        labels_svg = ""
        for i, lab in enumerate(dims_labels):
            angle = math.pi/2 - 2*math.pi*i/n
            lx, ly = cx + (R+14)*math.cos(angle), cy - (R+14)*math.sin(angle)
            labels_svg += f'<text x="{lx:.1f}" y="{ly:.1f}" font-size="8" fill="#888" text-anchor="middle" dominant-baseline="middle">{lab}</text>'
        return f'<svg viewBox="0 0 {size} {size}" style="width:{size}px;height:{size}px;flex-shrink:0"><polygon points="{grid}" fill="none" stroke="#EBEBEB" stroke-width="1"/><polygon points="{pts}" fill="{color}" opacity=".3" stroke="{color}" stroke-width="1.5"/>{labels_svg}</svg>'

    dim_labels = ["技术", "渠道", "IP", "资源", "风险"]
    partner_cards = ""
    for p in ctx.get("partner_table", []):
        dims = p.get("dims", {})
        scores = [dims.get("tech",0), dims.get("channel",0), dims.get("ip",0), dims.get("resource",0), dims.get("risk",0)]
        radar_mini = mini_radar(dim_labels, scores, "#2E9E5E")
        partner_cards += f"""<div style="display:flex;gap:12px;align-items:flex-start;background:var(--bgalt);padding:12px;margin-bottom:8px;border-left:3px solid var(--green)">
  {radar_mini}
  <div>
    <div style="font-weight:700;color:var(--navy)">{p['name']} <span style="font-size:11px;color:var(--lgray)">({p['type']})</span>
      <span class="risk-badge risk-l" style="margin-left:6px">互补评分 {p['score']}</span></div>
    <div style="font-size:12px;color:var(--lgray);margin-top:4px">{p['note']}</div>
  </div>
</div>"""

    threat_rows = "".join(
        f'<tr><td>{r["name"]}</td><td><span class="risk-badge {"risk-h" if r["overlap"]=="高" else "risk-m"}">{r["overlap"]}</span></td>'
        f'<td class="val">{r["patent"]}</td><td style="font-size:11px">{r["note"]}</td></tr>'
        for r in ctx["threat_table"]
    )

    body = f"""{section_header("09", "Competition & Partnership Network", "竞争与合作伙伴网络")}
<div class="chart-caption"><span class="fig-num">图17：</span>产业关系网络图（节点大小=专利规模）</div>
{net_html}
<div class="chart-source" style="margin-bottom:20px">{ctx['data_source']}</div>
<div class="two-col">
  <div>
    <div class="chart-caption"><span class="fig-num">落地改造⑥：</span><strong style="color:var(--navy)">潜在合作伙伴互补性五维评分</strong></div>
    <div class="callout-box"><div class="callout-head">💡 五维评分说明</div>
    技术互补度 / 渠道互补度 / IP协同度 / 资源互补度 / 风险互补度（0-100）。
    总分越高代表战略协同价值越大，建议优先联系总分≥80的伙伴。</div>
    {partner_cards}
  </div>
  <div>
    <div class="chart-caption"><span class="fig-num">图18：</span>主要竞争威胁企业分析</div>
    <table class="data-table">
      <thead><tr><th>威胁企业</th><th>技术重叠</th><th>专利规模</th><th>风险说明</th></tr></thead>
      <tbody>{threat_rows}</tbody>
    </table>
    <div class="insight-box"><strong>建议：</strong>
    对竞争者A（高重叠，850件专利），建议开展专利白地分析，
    识别其未覆盖的技术方向，作为下一阶段专利布局的主攻区域。</div>
  </div>
</div>"""
    return page_shell(9, brand, "09 · 竞争网络", body)


def build_p10(ctx: dict, brand: str) -> str:
    """P10 战略建议与行动路线图 + 落地改造⑤：预算级别三色标签"""
    tl_html     = timeline_html(ctx["timeline_items"])
    kpi_tgt_html= kpi_row_html(ctx["kpi_target"])
    body = f"""{section_header("10", "Strategic Roadmap", "战略建议与行动路线图")}
<div class="callout-box"><div class="callout-head">📌 预算级别说明</div>
<span class="budget-tag budget-go">🟢 立即可做</span>投入&lt;50万，3个月内可执行，无需特别审批&emsp;
<span class="budget-tag budget-mid">🟡 需资源</span>投入50-500万，需委员会/CTO审批&emsp;
<span class="budget-tag budget-big">🔴 需战略决策</span>投入&gt;500万，需董事会决策</div>
<div class="two-col" style="margin-top:20px">
  <div>
    <div class="chart-caption"><span class="fig-num">图19：</span>三阶段行动路线图（含预算级别标签）</div>
    {tl_html}
  </div>
  <div>
    <div class="chart-caption"><span class="fig-num">图20：</span>3年目标KPI</div>
    {kpi_tgt_html}
    <div class="insight-box" style="margin-top:16px"><strong>优先级建议：</strong>
    本月可立即启动的🟢绿色行动项（PCT申请+专利到期技术预研），
    无需重大资源投入即可显著提升科创力评级，建议CEO本周签发启动令。</div>
    <div class="callout-box" style="margin-top:20px"><div class="callout-head">⚖️ 免责声明</div>
    本报告基于公开专利数据及智慧芽分析模型生成，不构成投资建议。
    供应商名称、专利到期日期仅供参考，请以官方数据库核实为准。
    报告内容须经相关负责人审核后方可对外引用。</div>
  </div>
</div>"""
    return page_shell(10, brand, "10 · 战略路线图", body)


# ══════════════════════════════════════════════════════════════════════════════
# 主渲染入口 & CLI
# ══════════════════════════════════════════════════════════════════════════════

def render_html(ctx: dict, output_path: str = None) -> str:
    brand = f"{ctx['company']} 产业链战略报告 · {ctx['report_id']}"
    pages = [
        build_p1(ctx),
        build_p2(ctx, brand),
        build_p3(ctx, brand),
        build_p4(ctx, brand),
        build_p5(ctx, brand),
        build_p6(ctx, brand),
        build_p7(ctx, brand),
        build_p8(ctx, brand),
        build_p9(ctx, brand),
        build_p10(ctx, brand),
    ]
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{ctx['company']} 产业链战略报告 · {ctx['report_id']}</title>
<style>{WHITEPAPER_CSS}</style>
</head>
<body>
{''.join(pages)}
<div style="height:40px"></div>
</body>
</html>"""
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ 报告已生成：{output_path}")
    return html


def main():
    parser = argparse.ArgumentParser(description="企业决策者产业链战略报告系统 v2.0")
    parser.add_argument("--company", required=True,    help="目标企业名称")
    parser.add_argument("--chain",   default="",       help="产业链名称（可选）")
    parser.add_argument("--mode",    default="enterprise", choices=["enterprise", "gov"], help="报告模式")
    parser.add_argument("--output",  default="./output",   help="输出目录")
    args = parser.parse_args()

    report_id = make_report_id()
    ctx = make_default_context(args.company, args.chain, report_id, args.mode)

    safe_name  = args.company.replace(" ", "_").replace("/", "_")[:30]
    out_file   = Path(args.output) / f"{safe_name}_report.html"
    render_html(ctx, str(out_file))


if __name__ == "__main__":
    main()

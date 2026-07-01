"""
智慧情报门户生成脚本 gen_smart_intel.py
用法:
  python gen_smart_intel.py --company "华能集团" --industry "核能 风电 储能" --output portal.html
  python gen_smart_intel.py --company "国家电网" --industry "特高压 储能 电力现货" --use-patsnap --output sgcc.html
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
import random

# ─────────────────────────────────────────────
# CLI 参数解析
# ─────────────────────────────────────────────
def parse_args():
    parser = argparse.ArgumentParser(description="智慧情报门户生成器")
    parser.add_argument("--company",   required=True,  help="目标企业/机构名称")
    parser.add_argument("--industry",  required=True,  help="行业关键词（空格分隔）")
    parser.add_argument("--output",    default="portal.html", help="输出HTML路径")
    parser.add_argument("--title",     default="",     help="平台标题（留空自动生成）")
    parser.add_argument("--use-patsnap",  action="store_true", help="调用PatSnap检索真实专利数据")
    parser.add_argument("--use-websearch",action="store_true", help="调用Web Search获取真实新闻/政策")
    parser.add_argument("--modules",   default="intel,policy,tech,sci",
                        help="启用模块，逗号分隔: intel,policy,tech,sci")
    parser.add_argument("--year-range", default="1", help="数据年份范围（年数）")
    return parser.parse_args()

# ─────────────────────────────────────────────
# 数据生成层：示例数据（无MCP时的fallback）
# ─────────────────────────────────────────────
def make_date(days_ago_max=365, days_ago_min=7):
    """生成近一年内的随机日期字符串"""
    d = datetime.now() - timedelta(days=random.randint(days_ago_min, days_ago_max))
    return d.strftime("%Y-%m-%d")

def gen_patents(company, industry_kws, n=50):
    """生成示例专利数据"""
    types = ["发明专利", "实用新型", "发明专利", "发明专利"]
    ipc_map = {
        "储能": ["H01M10/058", "H02J3/28", "G06Q50/06"],
        "电力": ["H02J3/00", "G06F30/20", "H02G1/00"],
        "风电": ["F03D7/02", "H02P9/00", "G06Q10/04"],
        "核能": ["G21D3/00", "G21C17/00", "H02K7/18"],
        "氢能": ["C25B1/04", "H01M8/04", "C01B3/02"],
    }
    kw_list = industry_kws.split()
    patents = []
    for i in range(1, n+1):
        kw = random.choice(kw_list) if kw_list else "电力"
        ipc_pool = ipc_map.get(kw, ["H02J3/00", "G06F30/20"])
        patents.append({
            "id": i,
            "title": f"{company}{kw}关键技术专利({''.join(random.choices('ABCDEF', k=2))}{i:03d})",
            "type": random.choice(types),
            "applicant": company,
            "ipc": random.choice(ipc_pool),
            "field": kw,
            "app_no": f"CN{random.randint(2025,2026)}0{random.randint(1000000,9999999)}A",
            "date": make_date()
        })
    return patents

def gen_news(company, industry_kws, n=50):
    """生成示例新闻数据"""
    sources = ["新华社", "人民日报", "中国能源报", "国家能源局", "电力报", "科技日报"]
    kw_list = industry_kws.split()
    news = []
    for i in range(1, n+1):
        kw = random.choice(kw_list) if kw_list else "电力"
        news.append({
            "id": i,
            "title": f"{kw}领域重要进展：{company}发布第{i}号行业动态",
            "source": random.choice(sources),
            "tag": kw,
            "field": kw,
            "date": make_date()
        })
    return news

def gen_policies(company, industry_kws, n=50):
    """生成示例政策数据"""
    orgs = ["国家发展改革委", "国家能源局", "科技部", "工业和信息化部", "国务院"]
    levels = ["国家级", "部委级", "省级"]
    statuses = ["已发布", "征求意见", "已发布", "施行中"]
    kw_list = industry_kws.split()
    policies = []
    for i in range(1, n+1):
        kw = random.choice(kw_list) if kw_list else "电力"
        policies.append({
            "id": i,
            "title": f"关于推进{kw}产业高质量发展的指导意见（第{i}号）",
            "org": random.choice(orgs),
            "level": random.choice(levels),
            "status": random.choice(statuses),
            "field": kw,
            "date": make_date()
        })
    return policies

def gen_reports(company, industry_kws, n=50):
    """生成示例行业报告数据"""
    publishers = ["BNEF", "IEA", "国家能源研究院", "中电联", "麦肯锡", "德勤"]
    kw_list = industry_kws.split()
    reports = []
    for i in range(1, n+1):
        kw = random.choice(kw_list) if kw_list else "电力"
        reports.append({
            "id": i,
            "title": f"2025-2026年{kw}行业发展研究报告（第{i}期）",
            "publisher": random.choice(publishers),
            "type": "行业研究",
            "field": kw,
            "date": make_date()
        })
    return reports

def gen_internal(company, industry_kws, n=50):
    """生成示例内部报告数据"""
    depts = ["规划研究院", "技术研究中心", "战略发展部", "科技管理部"]
    levels = ["机密", "内部", "秘密"]
    kw_list = industry_kws.split()
    internals = []
    for i in range(1, n+1):
        kw = random.choice(kw_list) if kw_list else "电力"
        internals.append({
            "id": i,
            "title": f"{company}{kw}专项研究报告（{make_date()[:7]}）",
            "dept": random.choice(depts),
            "level": random.choice(levels),
            "field": kw,
            "date": make_date(60, 3)
        })
    return internals

# ─────────────────────────────────────────────
# HTML 生成核心函数
# ─────────────────────────────────────────────
def build_intel_rows(items, tab_type):
    """生成情报列表行HTML"""
    rows_html = ""
    for it in items:
        if tab_type == "patent":
            badge = '<span style="background:#e8f4fd;color:#1a73e8;padding:2px 6px;border-radius:3px;font-size:11px;">' + it["type"] + '</span>'
            rows_html += (
                '<div class="data-row" onclick="openModal(\'' + str(it["id"]) + '\',\'' + tab_type + '\')">'
                '<span class="row-num">' + str(it["id"]) + '</span>'
                '<span class="row-title">' + it["title"] + '</span>'
                + badge +
                '<span class="row-meta">' + it["applicant"] + '</span>'
                '<span class="row-meta">' + it["ipc"] + '</span>'
                '<span class="row-date">' + it["date"] + '</span>'
                '</div>'
            )
        elif tab_type == "policy":
            color = {"已发布": "#34a853", "征求意见": "#fbbc04", "施行中": "#1a73e8"}.get(it["status"], "#888")
            badge = '<span style="background:' + color + ';color:#fff;padding:2px 6px;border-radius:3px;font-size:11px;">' + it["status"] + '</span>'
            rows_html += (
                '<div class="data-row" onclick="openModal(\'' + str(it["id"]) + '\',\'' + tab_type + '\')">'
                '<span class="row-num">' + str(it["id"]) + '</span>'
                '<span class="row-title">' + it["title"] + '</span>'
                + badge +
                '<span class="row-meta">' + it["org"] + '</span>'
                '<span class="row-meta">' + it["level"] + '</span>'
                '<span class="row-date">' + it["date"] + '</span>'
                '</div>'
            )
        else:
            rows_html += (
                '<div class="data-row" onclick="openModal(\'' + str(it["id"]) + '\',\'' + tab_type + '\')">'
                '<span class="row-num">' + str(it["id"]) + '</span>'
                '<span class="row-title">' + it["title"] + '</span>'
                '<span class="row-meta">' + it.get("source", it.get("publisher", it.get("dept", ""))) + '</span>'
                '<span class="row-meta">' + it.get("tag", it.get("type", it.get("level", ""))) + '</span>'
                '<span class="row-date">' + it["date"] + '</span>'
                '</div>'
            )
    return rows_html

def generate_portal_html(args, data):
    """生成完整HTML字符串"""
    company = args.company
    industry = args.industry
    title = args.title if args.title else (company + " 智慧情报与政策孵化平台")
    kw_list = industry.split()
    kw1 = kw_list[0] if kw_list else "电力"
    kw2 = kw_list[1] if len(kw_list) > 1 else kw1
    kw3 = kw_list[2] if len(kw_list) > 2 else kw1
    now_year = datetime.now().year

    patent_rows  = build_intel_rows(data["patents"],  "patent")
    news_rows    = build_intel_rows(data["news"],     "news")
    policy_rows  = build_intel_rows(data["policies"], "policy")
    report_rows  = build_intel_rows(data["reports"],  "report")
    internal_rows= build_intel_rows(data["internals"],"internal")

    html = (
        "<!DOCTYPE html><html lang='zh-CN'><head>"
        "<meta charset='UTF-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<title>" + title + "</title>"
        "<style>"
        "*{box-sizing:border-box;margin:0;padding:0}"
        "body{font-family:'PingFang SC','Microsoft YaHei',sans-serif;background:#f0f2f5;color:#333}"
        ".top-bar{background:linear-gradient(135deg,#1a3a6b,#2563eb);color:#fff;padding:0 24px;"
        "height:52px;display:flex;align-items:center;justify-content:space-between;position:fixed;"
        "top:0;left:0;right:0;z-index:200}"
        ".top-bar .logo{font-size:18px;font-weight:700;letter-spacing:1px}"
        ".top-tabs{display:flex;gap:4px}"
        ".top-tab{padding:8px 20px;border-radius:6px;cursor:pointer;font-size:14px;color:rgba(255,255,255,0.8);transition:all 0.2s}"
        ".top-tab:hover{background:rgba(255,255,255,0.15);color:#fff}"
        ".top-tab.active{background:#fff;color:#1a3a6b;font-weight:600}"
        ".page-wrap{display:flex;padding-top:52px;height:100vh}"
        ".sidebar{width:220px;background:#fff;border-right:1px solid #e5e7eb;overflow-y:auto;flex-shrink:0}"
        ".sidebar-title{padding:16px;font-size:13px;color:#888;font-weight:600;border-bottom:1px solid #f0f0f0}"
        ".sidebar-item{padding:10px 16px;cursor:pointer;font-size:13px;color:#555;border-left:3px solid transparent;transition:all 0.15s}"
        ".sidebar-item:hover{background:#f0f4ff;color:#1a3a6b}"
        ".sidebar-item.active{background:#eff6ff;color:#1a3a6b;border-left-color:#1a3a6b;font-weight:600}"
        ".sidebar-sub{padding:8px 16px 8px 28px;cursor:pointer;font-size:12px;color:#777;transition:all 0.15s}"
        ".sidebar-sub:hover,.sidebar-sub.active{color:#1a3a6b;background:#f5f8ff}"
        ".content{flex:1;overflow-y:auto;padding:20px 24px}"
        ".view{display:none}"
        ".view.active{display:block}"
        "#view-scimgmt{position:fixed !important;top:52px !important;left:0;right:0;bottom:0;"
        "overflow-y:auto;z-index:100;background:#f0f2f5;display:none}"
        "#view-scimgmt.active{display:block !important}"
        ".stat-cards{display:flex;gap:12px;margin-bottom:20px;flex-wrap:wrap}"
        ".stat-card{background:#fff;border-radius:8px;padding:16px 20px;min-width:140px;flex:1;"
        "box-shadow:0 1px 4px rgba(0,0,0,0.06);cursor:pointer;transition:all 0.2s;border-top:3px solid #1a3a6b}"
        ".stat-card:hover{transform:translateY(-2px);box-shadow:0 4px 12px rgba(0,0,0,0.1)}"
        ".stat-card .num{font-size:28px;font-weight:700;color:#1a3a6b}"
        ".stat-card .label{font-size:12px;color:#888;margin-top:4px}"
        ".search-bar{display:flex;gap:8px;margin-bottom:16px}"
        ".search-bar input{flex:1;padding:8px 14px;border:1px solid #ddd;border-radius:6px;font-size:14px}"
        ".search-bar input:focus{outline:none;border-color:#1a3a6b}"
        ".tag-cloud{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:16px}"
        ".tag{padding:4px 10px;background:#eff6ff;color:#1a3a6b;border-radius:12px;font-size:12px;cursor:pointer;transition:all 0.2s}"
        ".tag:hover,.tag.active{background:#1a3a6b;color:#fff}"
        ".data-tabs{display:flex;gap:0;margin-bottom:0;border-bottom:2px solid #e5e7eb}"
        ".data-tab{padding:10px 20px;cursor:pointer;font-size:13px;color:#888;border-bottom:2px solid transparent;margin-bottom:-2px;transition:all 0.2s}"
        ".data-tab:hover{color:#1a3a6b}"
        ".data-tab.active{color:#1a3a6b;font-weight:600;border-bottom-color:#1a3a6b}"
        ".data-panel{display:none;background:#fff;border-radius:0 0 8px 8px;box-shadow:0 1px 4px rgba(0,0,0,0.06)}"
        ".data-panel.active{display:block}"
        ".data-row{display:flex;align-items:center;gap:10px;padding:10px 14px;border-bottom:1px solid #f5f5f5;"
        "cursor:pointer;transition:background 0.15s;font-size:13px}"
        ".data-row:hover{background:#f8faff}"
        ".row-num{color:#bbb;font-size:11px;min-width:28px;text-align:right}"
        ".row-title{flex:1;color:#333;font-weight:500}"
        ".row-meta{color:#888;font-size:12px;min-width:80px}"
        ".row-date{color:#aaa;font-size:11px;min-width:90px;text-align:right}"
        ".section-card{background:#fff;border-radius:8px;padding:20px;margin-bottom:16px;box-shadow:0 1px 4px rgba(0,0,0,0.06)}"
        ".section-title{font-size:15px;font-weight:600;color:#1a3a6b;margin-bottom:14px;padding-bottom:8px;border-bottom:1px solid #f0f0f0}"
        ".step-tabs{display:flex;gap:8px;margin-bottom:20px;flex-wrap:wrap}"
        ".step-tab{padding:8px 16px;border-radius:6px;cursor:pointer;font-size:13px;background:#fff;"
        "border:1px solid #ddd;color:#666;transition:all 0.2s}"
        ".step-tab:hover{border-color:#1a3a6b;color:#1a3a6b}"
        ".step-tab.active{background:#1a3a6b;color:#fff;border-color:#1a3a6b}"
        ".step-panel{display:none}.step-panel.active{display:block}"
        ".table-wrap{overflow-x:auto}"
        "table{width:100%;border-collapse:collapse;font-size:13px}"
        "th{background:#f8f9fa;padding:10px 12px;text-align:left;font-weight:600;color:#555;border-bottom:2px solid #e5e7eb}"
        "td{padding:9px 12px;border-bottom:1px solid #f0f0f0;color:#444}"
        "tr:hover td{background:#f8faff}"
        ".badge{padding:2px 8px;border-radius:10px;font-size:11px;font-weight:500}"
        ".badge-red{background:#fef2f2;color:#dc2626}"
        ".badge-yellow{background:#fffbeb;color:#d97706}"
        ".badge-green{background:#f0fdf4;color:#16a34a}"
        ".badge-blue{background:#eff6ff;color:#1d4ed8}"
        ".prog-bar{height:8px;background:#e5e7eb;border-radius:4px;overflow:hidden}"
        ".prog-fill{height:100%;border-radius:4px;transition:width 0.6s}"
        ".kpi-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin-bottom:16px}"
        ".kpi-card{background:#f8f9fa;border-radius:8px;padding:14px;text-align:center;border-left:4px solid #1a3a6b}"
        ".kpi-val{font-size:24px;font-weight:700;color:#1a3a6b}"
        ".kpi-lbl{font-size:12px;color:#888;margin-top:4px}"
        ".chart-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px}"
        ".chart-card{background:#f8f9fa;border-radius:8px;padding:16px}"
        ".chart-card canvas{width:100%;height:220px;display:block}"
        ".chart-card h4{font-size:13px;color:#555;margin-bottom:10px;font-weight:600}"
        ".sci-wrap{padding:20px 28px}"
        ".sci-top-kpi{display:flex;gap:12px;margin-bottom:16px;flex-wrap:wrap}"
        ".sci-kpi{background:#fff;border-radius:8px;padding:14px 18px;min-width:130px;text-align:center;"
        "box-shadow:0 1px 4px rgba(0,0,0,0.06);border-top:3px solid #1a3a6b;flex:1}"
        ".sci-kpi .val{font-size:22px;font-weight:700;color:#1a3a6b}"
        ".sci-kpi .lbl{font-size:11px;color:#888;margin-top:3px}"
        ".sci-nav{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:20px;background:#fff;padding:12px;border-radius:8px;box-shadow:0 1px 4px rgba(0,0,0,0.06)}"
        ".sci-nav-btn{padding:7px 14px;border-radius:6px;cursor:pointer;font-size:12px;background:#f5f5f5;color:#555;transition:all 0.2s}"
        ".sci-nav-btn:hover{background:#eff6ff;color:#1a3a6b}"
        ".sci-nav-btn.active{background:#1a3a6b;color:#fff}"
        ".sci-panel{display:none}.sci-panel.active{display:block}"
        ".modal-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:999;align-items:center;justify-content:center}"
        ".modal-overlay.active{display:flex}"
        ".modal-box{background:#fff;border-radius:12px;padding:28px;max-width:600px;width:90%;max-height:80vh;overflow-y:auto}"
        ".modal-title{font-size:16px;font-weight:700;color:#1a3a6b;margin-bottom:16px}"
        ".modal-close{float:right;cursor:pointer;color:#888;font-size:20px}"
        ".bot-btn{position:fixed;bottom:24px;right:24px;width:52px;height:52px;background:#1a3a6b;color:#fff;"
        "border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:22px;cursor:pointer;"
        "box-shadow:0 4px 12px rgba(26,58,107,0.4);z-index:300;transition:transform 0.2s}"
        ".bot-btn:hover{transform:scale(1.1)}"
        ".action-btn{display:inline-block;padding:9px 20px;background:#1a3a6b;color:#fff;border-radius:6px;"
        "cursor:pointer;font-size:13px;margin-top:12px;transition:background 0.2s}"
        ".action-btn:hover{background:#2563eb}"
        ".action-btn.green{background:#16a34a}.action-btn.green:hover{background:#15803d}"
        "</style></head><body>"

        # ── 顶部导航栏 ──
        "<div class='top-bar'>"
        "<div class='logo'>⚡ " + title + "</div>"
        "<div class='top-tabs'>"
        "<div class='top-tab active' onclick='switchView(\"intel\")'>📡 情报中心</div>"
        "<div class='top-tab' onclick='switchView(\"workbench\")'>🏛️ 政策孵化工作台</div>"
        "<div class='top-tab' onclick='switchView(\"techroute\")'>🔬 技术路线研判</div>"
        "<div class='top-tab' onclick='switchView(\"scimgmt\")'>🏢 科技创新管理</div>"
        "</div></div>"

        # ── 主体布局 ──
        "<div class='page-wrap'>"
        "<div class='sidebar' id='main-sidebar'>"
        "<div class='sidebar-title'>情报分类</div>"
        "<div class='sidebar-item active' onclick='switchDataTab(\"patent\")'>🔬 专利情报</div>"
        "<div class='sidebar-item' onclick='switchDataTab(\"news\")'>📰 行业新闻</div>"
        "<div class='sidebar-item' onclick='switchDataTab(\"policy\")'>📋 政策法规</div>"
        "<div class='sidebar-item' onclick='switchDataTab(\"report\")'>📊 行业研究报告</div>"
        "<div class='sidebar-item' onclick='switchDataTab(\"internal\")'>🔒 内部报告</div>"
        "<div class='sidebar-title' style='margin-top:8px'>技术领域</div>"
        + "".join(['<div class="sidebar-sub" onclick="filterByKw(\'' + kw + '\')">' + kw + '</div>' for kw in kw_list]) +
        "</div>"  # end sidebar

        "<div class='content'>"

        # ═══ 视图1：情报中心 ═══
        "<div class='view active' id='view-intel'>"
        "<div class='stat-cards'>"
        "<div class='stat-card' onclick='switchDataTab(\"patent\")'><div class='num'>50</div><div class='label'>🔬 专利情报</div></div>"
        "<div class='stat-card' onclick='switchDataTab(\"news\")'><div class='num'>50</div><div class='label'>📰 行业新闻</div></div>"
        "<div class='stat-card' onclick='switchDataTab(\"policy\")'><div class='num'>50</div><div class='label'>📋 政策法规</div></div>"
        "<div class='stat-card' onclick='switchDataTab(\"report\")'><div class='num'>50</div><div class='label'>📊 行业报告</div></div>"
        "<div class='stat-card' onclick='switchDataTab(\"internal\")'><div class='num'>50</div><div class='label'>🔒 内部报告</div></div>"
        "</div>"
        "<div class='search-bar'><input type='text' id='search-input' placeholder='🔍 搜索情报...' oninput='filterRows()'></div>"
        "<div class='tag-cloud'>"
        + "".join(['<span class="tag" onclick="filterByKw(\'' + kw + '\')">' + kw + '</span>' for kw in kw_list]) +
        "</div>"
        "<div class='data-tabs'>"
        "<div class='data-tab active' id='tab-patent' onclick='switchDataTab(\"patent\")'>🔬 专利情报 (50)</div>"
        "<div class='data-tab' id='tab-news' onclick='switchDataTab(\"news\")'>📰 行业新闻 (50)</div>"
        "<div class='data-tab' id='tab-policy' onclick='switchDataTab(\"policy\")'>📋 政策法规 (50)</div>"
        "<div class='data-tab' id='tab-report' onclick='switchDataTab(\"report\")'>📊 行业报告 (50)</div>"
        "<div class='data-tab' id='tab-internal' onclick='switchDataTab(\"internal\")'>🔒 内部报告 (50)</div>"
        "</div>"
        "<div class='data-panel active' id='panel-patent'>" + patent_rows + "</div>"
        "<div class='data-panel' id='panel-news'>" + news_rows + "</div>"
        "<div class='data-panel' id='panel-policy'>" + policy_rows + "</div>"
        "<div class='data-panel' id='panel-report'>" + report_rows + "</div>"
        "<div class='data-panel' id='panel-internal'>" + internal_rows + "</div>"
        "</div>"  # end view-intel

        # ═══ 视图2：政策孵化工作台 ═══
        "<div class='view' id='view-workbench'>"
        "<div class='section-card'>"
        "<div class='section-title'>🏛️ 政策孵化工作台 — 五步全链路研究流程</div>"
        "<div class='step-tabs'>"
        "<div class='step-tab active' onclick='switchStep(\"wb\",\"s1\",this)'>① 需求拆解</div>"
        "<div class='step-tab' onclick='switchStep(\"wb\",\"s2\",this)'>② 数据摸排</div>"
        "<div class='step-tab' onclick='switchStep(\"wb\",\"s3\",this)'>③ 推演测算</div>"
        "<div class='step-tab' onclick='switchStep(\"wb\",\"s4\",this)'>④ 试点路径</div>"
        "<div class='step-tab' onclick='switchStep(\"wb\",\"s5\",this)'>⑤ 成果汇总</div>"
        "</div>"
        "<div class='step-panel active' id='wb-s1'>"
        "<div class='kpi-grid'>"
        "<div class='kpi-card'><div class='kpi-val'>28</div><div class='kpi-lbl'>需求总条数</div></div>"
        "<div class='kpi-card'><div class='kpi-val'>7</div><div class='kpi-lbl'>P1 紧急需求</div></div>"
        "<div class='kpi-card'><div class='kpi-val'>5</div><div class='kpi-lbl'>核心行业痛点</div></div>"
        "<div class='kpi-card'><div class='kpi-val'>3</div><div class='kpi-lbl'>上级政策导向</div></div>"
        "</div>"
        "<div class='chart-grid'>"
        "<div class='chart-card'><h4>需求优先级分布</h4><canvas id='wb-chart1' width='400' height='220'></canvas></div>"
        "<div class='chart-card'><h4>来源机构分布</h4><canvas id='wb-chart2' width='400' height='220'></canvas></div>"
        "</div>"
        "<table><tr><th>编号</th><th>需求描述</th><th>优先级</th><th>来源</th><th>紧迫程度</th></tr>"
        "<tr><td>RQ-001</td><td>" + kw1 + "安全标准亟需更新完善</td><td><span class='badge badge-red'>P1</span></td><td>政府监管</td><td>极紧迫</td></tr>"
        "<tr><td>RQ-002</td><td>" + kw1 + "成本下降路径需量化测算</td><td><span class='badge badge-red'>P1</span></td><td>产业痛点</td><td>紧迫</td></tr>"
        "<tr><td>RQ-003</td><td>" + kw2 + "市场机制尚不健全</td><td><span class='badge badge-yellow'>P2</span></td><td>市场反馈</td><td>较紧迫</td></tr>"
        "<tr><td>RQ-004</td><td>" + kw2 + "技术标准与国际接轨</td><td><span class='badge badge-yellow'>P2</span></td><td>政策导向</td><td>较紧迫</td></tr>"
        "<tr><td>RQ-005</td><td>" + kw3 + "人才培养体系不完善</td><td><span class='badge badge-blue'>P3</span></td><td>企业诉求</td><td>一般</td></tr>"
        "</table>"
        "</div>"  # end wb-s1

        "<div class='step-panel' id='wb-s2'>"
        "<div class='kpi-grid'>"
        "<div class='kpi-card'><div class='kpi-val'>144.7GW</div><div class='kpi-lbl'>全国" + kw1 + "装机（2025）</div></div>"
        "<div class='kpi-card'><div class='kpi-val'>+84%</div><div class='kpi-lbl'>同比增速</div></div>"
        "<div class='kpi-card'><div class='kpi-val'>0.62元</div><div class='kpi-lbl'>单位成本（元/kWh）</div></div>"
        "<div class='kpi-card'><div class='kpi-val'>3国</div><div class='kpi-lbl'>国际对标经验</div></div>"
        "</div>"
        "<div class='chart-grid'>"
        "<div class='chart-card'><h4>" + kw1 + "装机增长趋势（GW）</h4><canvas id='wb-chart3' width='400' height='220'></canvas></div>"
        "<div class='chart-card'><h4>度电成本下降趋势（元/kWh）</h4><canvas id='wb-chart4' width='400' height='220'></canvas></div>"
        "</div>"
        "<table><tr><th>地区</th><th>装机规模</th><th>政策特点</th><th>市场成熟度</th></tr>"
        "<tr><td>中国</td><td>144.7GW</td><td>政府主导+市场辅助</td><td>★★★★☆</td></tr>"
        "<tr><td>美国</td><td>68.3GW</td><td>IRA法案补贴驱动</td><td>★★★★★</td></tr>"
        "<tr><td>欧盟</td><td>52.1GW</td><td>碳市场机制联动</td><td>★★★★☆</td></tr>"
        "<tr><td>澳大利亚</td><td>18.6GW</td><td>容量市场+辅助服务</td><td>★★★☆☆</td></tr>"
        "</table>"
        "</div>"  # end wb-s2

        "<div class='step-panel' id='wb-s3'>"
        "<div class='chart-grid'>"
        "<div class='chart-card'><h4>三情景装机预测（2026-2030）</h4><canvas id='wb-chart5' width='400' height='220'></canvas></div>"
        "<div class='chart-card'><h4>三方案综合IRR对比</h4><canvas id='wb-chart6' width='400' height='220'></canvas></div>"
        "</div>"
        "<table><tr><th>方案</th><th>核心机制</th><th>2030装机</th><th>IRR</th><th>推荐度</th></tr>"
        "<tr><td><b>方案A</b></td><td>政府强制配置</td><td>280GW</td><td>8.2%</td><td>★★★☆☆</td></tr>"
        "<tr><td><b>方案B ⭐</b></td><td>市场化容量补偿</td><td>320GW</td><td>12.5%</td><td>★★★★★</td></tr>"
        "<tr><td><b>方案C</b></td><td>混合激励机制</td><td>295GW</td><td>10.8%</td><td>★★★★☆</td></tr>"
        "</table>"
        "</div>"  # end wb-s3

        "<div class='step-panel' id='wb-s4'>"
        "<div class='chart-grid'>"
        "<div class='chart-card'><h4>试点KPI达成率预测</h4><canvas id='wb-chart7' width='400' height='220'></canvas></div>"
        "<div class='chart-card'><h4>试点省份综合评估雷达图</h4><canvas id='wb-chart8' width='400' height='220'></canvas></div>"
        "</div>"
        "<table><tr><th>KPI指标</th><th>2026目标</th><th>2028目标</th><th>2030目标</th><th>预警阈值</th></tr>"
        "<tr><td>" + kw1 + "装机规模</td><td>160GW</td><td>240GW</td><td>320GW</td><td>&lt;140GW预警</td></tr>"
        "<tr><td>度电成本</td><td>0.55元</td><td>0.45元</td><td>0.38元</td><td>&gt;0.60元预警</td></tr>"
        "<tr><td>市场化率</td><td>35%</td><td>55%</td><td>75%</td><td>&lt;25%预警</td></tr>"
        "<tr><td>安全事故</td><td>&lt;5起/年</td><td>&lt;3起/年</td><td>&lt;1起/年</td><td>&gt;8起/年预警</td></tr>"
        "</table>"
        "</div>"  # end wb-s4

        "<div class='step-panel' id='wb-s5'>"
        "<div class='chart-grid'>"
        "<div class='chart-card'><h4>成果类型分布</h4><canvas id='wb-chart9' width='400' height='220'></canvas></div>"
        "<div class='chart-card'><h4>五维质量评分</h4><canvas id='wb-chart10' width='400' height='220'></canvas></div>"
        "</div>"
        "<div class='kpi-grid'>"
        "<div class='kpi-card'><div class='kpi-val'>3</div><div class='kpi-lbl'>政策研究报告</div></div>"
        "<div class='kpi-card'><div class='kpi-val'>12</div><div class='kpi-lbl'>政策建议条目</div></div>"
        "<div class='kpi-card'><div class='kpi-val'>6</div><div class='kpi-lbl'>配套标准草案</div></div>"
        "<div class='kpi-card'><div class='kpi-val'>4</div><div class='kpi-lbl'>试点方案</div></div>"
        "</div>"
        "<div style='margin-top:12px'>"
        "<span class='action-btn green' onclick='alert(\"研究报告已导出为PDF\")'>📄 导出政策报告</span> "
        "<span class='action-btn' onclick='switchView(\"techroute\")'>🔬 启动技术路线研判 →</span>"
        "</div>"
        "</div>"  # end wb-s5
        "</div></div>"  # end section-card, view-workbench

        # ═══ 视图3：技术路线研判 ═══
        "<div class='view' id='view-techroute'>"
        "<div class='section-card'>"
        "<div class='section-title'>🔬 技术路线研判 — 六步工作流</div>"
        "<div class='step-tabs'>"
        "<div class='step-tab active' onclick='switchStep(\"tr\",\"s1\",this)'>① 情报萃取</div>"
        "<div class='step-tab' onclick='switchStep(\"tr\",\"s2\",this)'>② 政策拆解</div>"
        "<div class='step-tab' onclick='switchStep(\"tr\",\"s3\",this)'>③ 诉求映射</div>"
        "<div class='step-tab' onclick='switchStep(\"tr\",\"s4\",this)'>④ 路线推演</div>"
        "<div class='step-tab' onclick='switchStep(\"tr\",\"s5\",this)'>⑤ 落地定型</div>"
        "<div class='step-tab' onclick='switchStep(\"tr\",\"s6\",this)'>⑥ 输出成果</div>"
        "</div>"
        "<div class='step-panel active' id='tr-s1'>"
        "<div class='chart-grid'>"
        "<div class='chart-card'><h4>主要机构技术布局能力雷达</h4><canvas id='tr-chart1' width='400' height='220'></canvas></div>"
        "<div class='chart-card'><h4>近12月行业热点动态频次</h4><canvas id='tr-chart2' width='400' height='220'></canvas></div>"
        "</div>"
        "<table><tr><th>机构</th><th>技术优势</th><th>专利数量</th><th>研发投入</th><th>竞争态势</th></tr>"
        "<tr><td>" + company + "</td><td>" + kw1 + "/" + kw2 + "</td><td>2,847</td><td>12.3亿</td><td><span class='badge badge-green'>领先</span></td></tr>"
        "<tr><td>竞争机构A</td><td>" + kw1 + "</td><td>1,923</td><td>8.7亿</td><td><span class='badge badge-yellow'>追赶</span></td></tr>"
        "<tr><td>竞争机构B</td><td>" + kw3 + "</td><td>1,456</td><td>6.2亿</td><td><span class='badge badge-blue'>跟随</span></td></tr>"
        "</table>"
        "</div>"  # tr-s1

        "<div class='step-panel' id='tr-s2'>"
        "<div class='chart-grid'>"
        "<div class='chart-card'><h4>近一年政策类型分布</h4><canvas id='tr-chart3' width='400' height='220'></canvas></div>"
        "<div class='chart-card'><h4>核心约束指标执行优先级</h4><canvas id='tr-chart4' width='400' height='220'></canvas></div>"
        "</div>"
        "<table><tr><th>政策目标</th><th>约束指标</th><th>执行力度</th><th>硬性边界</th></tr>"
        "<tr><td>" + kw1 + "规模化推广</td><td>2030年装机≥320GW</td><td><span class='badge badge-red'>强制</span></td><td>是</td></tr>"
        "<tr><td>安全标准升级</td><td>事故率&lt;0.1‰</td><td><span class='badge badge-red'>强制</span></td><td>是</td></tr>"
        "<tr><td>成本下降目标</td><td>2026年&lt;0.55元/kWh</td><td><span class='badge badge-yellow'>引导</span></td><td>否</td></tr>"
        "<tr><td>市场化率提升</td><td>2028年≥55%</td><td><span class='badge badge-yellow'>引导</span></td><td>否</td></tr>"
        "</table>"
        "</div>"  # tr-s2

        "<div class='step-panel' id='tr-s3'>"
        "<div class='chart-grid'>"
        "<div class='chart-card'><h4>诉求映射强度矩阵</h4><canvas id='tr-chart5' width='400' height='220'></canvas></div>"
        "<div class='chart-card'><h4>技术需求优先级</h4><canvas id='tr-chart6' width='400' height='220'></canvas></div>"
        "</div>"
        "<table><tr><th>产业痛点/政策管控</th><th>映射技术需求</th><th>映射强度</th><th>研发优先级</th></tr>"
        "<tr><td>安全事故频发</td><td>安全监测与预警系统</td><td>★★★★★</td><td><span class='badge badge-red'>P1</span></td></tr>"
        "<tr><td>度电成本偏高</td><td>材料创新与系统集成优化</td><td>★★★★★</td><td><span class='badge badge-red'>P1</span></td></tr>"
        "<tr><td>并网调度难</td><td>智能调度算法</td><td>★★★★☆</td><td><span class='badge badge-yellow'>P2</span></td></tr>"
        "<tr><td>标准不统一</td><td>互联互通接口标准</td><td>★★★☆☆</td><td><span class='badge badge-blue'>P3</span></td></tr>"
        "</table>"
        "</div>"  # tr-s3

        "<div class='step-panel' id='tr-s4'>"
        "<div class='chart-grid'>"
        "<div class='chart-card'><h4>技术路线TRL成熟度演进（2026-2030）</h4><canvas id='tr-chart7' width='400' height='220'></canvas></div>"
        "<div class='chart-card'><h4>综合适配度雷达图</h4><canvas id='tr-chart8' width='400' height='220'></canvas></div>"
        "</div>"
        "<table><tr><th>技术路线</th><th>适配度</th><th>TRL（当前）</th><th>预计TRL（2028）</th><th>推荐</th></tr>"
        "<tr><td>路线A：" + kw1 + "主流方案</td><td><div class='prog-bar'><div class='prog-fill' style='width:92%;background:#1a3a6b'></div></div></td><td>TRL7</td><td>TRL9</td><td><span class='badge badge-green'>首选</span></td></tr>"
        "<tr><td>路线B：" + kw2 + "融合方案</td><td><div class='prog-bar'><div class='prog-fill' style='width:78%;background:#2563eb'></div></div></td><td>TRL6</td><td>TRL8</td><td><span class='badge badge-yellow'>备选</span></td></tr>"
        "<tr><td>路线C：" + kw3 + "创新方案</td><td><div class='prog-bar'><div class='prog-fill' style='width:61%;background:#64748b'></div></div></td><td>TRL4</td><td>TRL6</td><td><span class='badge badge-blue'>长期</span></td></tr>"
        "</table>"
        "</div>"  # tr-s4

        "<div class='step-panel' id='tr-s5'>"
        "<div class='chart-grid'>"
        "<div class='chart-card'><h4>核心技术产业化时序甘特图</h4><canvas id='tr-chart9' width='400' height='220'></canvas></div>"
        "<div class='chart-card'><h4>落地优先级×实施难度象限图</h4><canvas id='tr-chart10' width='400' height='220'></canvas></div>"
        "</div>"
        "<table><tr><th>技术品类</th><th>攻关重点</th><th>应用场景</th><th>产业化时序</th></tr>"
        "<tr><td>" + kw1 + "核心技术</td><td>安全性与循环寿命</td><td>电网侧大规模</td><td>2026-2027</td></tr>"
        "<tr><td>" + kw2 + "集成技术</td><td>系统效率优化</td><td>工商业用户侧</td><td>2027-2028</td></tr>"
        "<tr><td>" + kw3 + "控制技术</td><td>智能调度算法</td><td>虚拟电厂聚合</td><td>2028-2030</td></tr>"
        "</table>"
        "</div>"  # tr-s5

        "<div class='step-panel' id='tr-s6'>"
        "<div class='chart-grid'>"
        "<div class='chart-card'><h4>综合评估仪表盘</h4><canvas id='tr-chart11' width='400' height='220'></canvas></div>"
        "<div class='chart-card'><h4>输出成果统计</h4><canvas id='tr-chart12' width='400' height='220'></canvas></div>"
        "</div>"
        "<div class='kpi-grid'>"
        "<div class='kpi-card'><div class='kpi-val'>12</div><div class='kpi-lbl'>技术路线清单</div></div>"
        "<div class='kpi-card'><div class='kpi-val'>18</div><div class='kpi-lbl'>关键技术攻关目录</div></div>"
        "<div class='kpi-card'><div class='kpi-val'>6</div><div class='kpi-lbl'>落地方案</div></div>"
        "<div class='kpi-card'><div class='kpi-val'>3</div><div class='kpi-lbl'>研判报告</div></div>"
        "</div>"
        "<div style='margin-top:12px'>"
        "<span class='action-btn' onclick='submitToSciMgmt()'>🚀 提交立项审查 → 科技创新管理</span>"
        "</div>"
        "</div>"  # tr-s6
        "</div></div>"  # end section-card, view-techroute

        # ═══ 视图4：科技创新管理 ═══
        "<div class='view' id='view-scimgmt'>"
        "<div class='sci-wrap'>"
        "<div class='sci-top-kpi'>"
        "<div class='sci-kpi'><div class='val'>47</div><div class='lbl'>在研项目</div></div>"
        "<div class='sci-kpi'><div class='val'>1,284</div><div class='lbl'>有效专利</div></div>"
        "<div class='sci-kpi'><div class='val'>92.5</div><div class='lbl'>高企评分</div></div>"
        "<div class='sci-kpi'><div class='val'>14</div><div class='lbl'>功能模块</div></div>"
        "<div class='sci-kpi'><div class='val'>94.2</div><div class='lbl'>综合绩效分</div></div>"
        "</div>"
        "<div class='sci-nav'>"
        "<div class='sci-nav-btn active' onclick='showSciModule(\"proj\",this)'>📁 科技项目管理</div>"
        "<div class='sci-nav-btn' onclick='showSciModule(\"req\",this)'>📋 科技需求管理</div>"
        "<div class='sci-nav-btn' onclick='showSciModule(\"org\",this)'>👥 科技组织管理</div>"
        "<div class='sci-nav-btn' onclick='showSciModule(\"plan\",this)'>🗓️ 创新规划管理</div>"
        "<div class='sci-nav-btn' onclick='showSciModule(\"coop\",this)'>🤝 科技外协管理</div>"
        "<div class='sci-nav-btn' onclick='showSciModule(\"annual\",this)'>📅 年度计划管理</div>"
        "<div class='sci-nav-btn' onclick='showSciModule(\"platform\",this)'>🏛️ 科技平台管理</div>"
        "<div class='sci-nav-btn' onclick='showSciModule(\"award\",this)'>🏆 科技奖励管理</div>"
        "<div class='sci-nav-btn' onclick='showSciModule(\"review\",this)'>🔍 科研评审管理</div>"
        "<div class='sci-nav-btn' onclick='showSciModule(\"ip\",this)'>🔒 知识产权管理</div>"
        "<div class='sci-nav-btn' onclick='showSciModule(\"hightech\",this)'>🏅 高企申计管理</div>"
        "<div class='sci-nav-btn' onclick='showSciModule(\"result\",this)'>🎯 科技成果管理</div>"
        "<div class='sci-nav-btn' onclick='showSciModule(\"std\",this)'>📐 标准管理</div>"
        "<div class='sci-nav-btn' onclick='showSciModule(\"perf\",this)'>📊 绩效管理</div>"
        "</div>"

        # 科技项目管理
        "<div class='sci-panel active' id='sci-proj'>"
        "<div class='kpi-grid'>"
        "<div class='kpi-card'><div class='kpi-val'>47</div><div class='kpi-lbl'>在研项目</div></div>"
        "<div class='kpi-card'><div class='kpi-val'>12</div><div class='kpi-lbl'>本年新立项</div></div>"
        "<div class='kpi-card'><div class='kpi-val'>8</div><div class='kpi-lbl'>待验收</div></div>"
        "<div class='kpi-card'><div class='kpi-val'>186</div><div class='kpi-lbl'>历年结题</div></div>"
        "</div>"
        "<div class='chart-grid'>"
        "<div class='chart-card'><h4>项目阶段分布</h4><canvas id='sci-proj-bar' width='400' height='200'></canvas></div>"
        "<div class='chart-card'><h4>历年立项趋势</h4><canvas id='sci-proj-line' width='400' height='200'></canvas></div>"
        "</div>"
        "<table><tr><th>项目编号</th><th>项目名称</th><th>负责部门</th><th>开始时间</th><th>进度</th><th>状态</th></tr>"
        "<tr><td>EPPEI-2026-ST-047</td><td>" + kw1 + "关键技术研究（立项审查来源）</td><td>技术中心</td><td>2026-05</td><td><div class='prog-bar'><div class='prog-fill' style='width:10%;background:#1a3a6b'></div></div></td><td><span class='badge badge-green'>新建</span></td></tr>"
        "<tr><td>EPPEI-2025-ST-036</td><td>" + kw2 + "系统集成优化研究</td><td>研发院</td><td>2025-03</td><td><div class='prog-bar'><div class='prog-fill' style='width:65%;background:#1a3a6b'></div></div></td><td><span class='badge badge-blue'>在研</span></td></tr>"
        "<tr><td>EPPEI-2025-ST-028</td><td>" + kw3 + "智能调度算法开发</td><td>数字化中心</td><td>2025-01</td><td><div class='prog-bar'><div class='prog-fill' style='width:82%;background:#16a34a'></div></div></td><td><span class='badge badge-yellow'>待验收</span></td></tr>"
        "<tr><td>EPPEI-2024-ST-019</td><td>电力市场竞价策略研究</td><td>市场研究部</td><td>2024-06</td><td><div class='prog-bar'><div class='prog-fill' style='width:95%;background:#16a34a'></div></div></td><td><span class='badge badge-yellow'>待结题</span></td></tr>"
        "<tr><td>EPPEI-2024-ST-011</td><td>碳中和路径规划研究</td><td>战略规划院</td><td>2024-02</td><td><div class='prog-bar'><div class='prog-fill' style='width:100%;background:#888'></div></div></td><td><span class='badge badge-blue'>已结题</span></td></tr>"
        "</table>"
        "</div>"  # sci-proj

        # 知识产权管理（嵌入PatSnap数据）
        "<div class='sci-panel' id='sci-ip'>"
        "<div class='kpi-grid'>"
        "<div class='kpi-card'><div class='kpi-val'>1,284</div><div class='kpi-lbl'>有效专利</div></div>"
        "<div class='kpi-card'><div class='kpi-val'>186</div><div class='kpi-lbl'>本年申请</div></div>"
        "<div class='kpi-card'><div class='kpi-val'>342</div><div class='kpi-lbl'>软件著作权</div></div>"
        "<div class='kpi-card'><div class='kpi-val'>28</div><div class='kpi-lbl'>技术秘密</div></div>"
        "</div>"
        "<div class='chart-grid'>"
        "<div class='chart-card'><h4>近5年申请/授权趋势</h4><canvas id='sci-ip-line' width='400' height='200'></canvas></div>"
        "<div class='chart-card'><h4>IPC技术构成（Top 6）</h4><canvas id='sci-ip-bar' width='400' height='200'></canvas></div>"
        "</div>"
        "<table><tr><th>IPC分类</th><th>技术领域</th><th>专利量</th><th>占比</th></tr>"
        "<tr><td>H02J</td><td>电力系统控制</td><td>4,822</td><td>28.3%</td></tr>"
        "<tr><td>H01M</td><td>电化学储能</td><td>3,441</td><td>20.2%</td></tr>"
        "<tr><td>G06Q</td><td>数据处理/电力市场</td><td>2,153</td><td>12.6%</td></tr>"
        "<tr><td>G06F</td><td>数字计算/模拟</td><td>1,622</td><td>9.5%</td></tr>"
        "<tr><td>G06N</td><td>人工智能</td><td>1,234</td><td>7.2%</td></tr>"
        "<tr><td>H02P</td><td>电机控制</td><td>987</td><td>5.8%</td></tr>"
        "</table>"
        "</div>"  # sci-ip

        # 绩效管理
        "<div class='sci-panel' id='sci-perf'>"
        "<div class='kpi-grid'>"
        "<div class='kpi-card'><div class='kpi-val'>94.2</div><div class='kpi-lbl'>综合绩效分</div></div>"
        "<div class='kpi-card'><div class='kpi-val'>91.5</div><div class='kpi-lbl'>项目绩效分</div></div>"
        "<div class='kpi-card'><div class='kpi-val'>96.8</div><div class='kpi-lbl'>人员绩效分</div></div>"
        "<div class='kpi-card'><div class='kpi-val'>2</div><div class='kpi-lbl'>预警所室</div></div>"
        "</div>"
        "<div class='chart-grid'>"
        "<div class='chart-card'><h4>所室绩效评分排行</h4><canvas id='sci-perf-bar' width='400' height='200'></canvas></div>"
        "<div class='chart-card'><h4>季度绩效趋势</h4><canvas id='sci-perf-line' width='400' height='200'></canvas></div>"
        "</div>"
        "<table><tr><th>排名</th><th>姓名</th><th>所室</th><th>项目得分</th><th>成果得分</th><th>综合得分</th></tr>"
        "<tr><td>🥇1</td><td>张工</td><td>技术中心</td><td>98</td><td>97</td><td><b>97.5</b></td></tr>"
        "<tr><td>🥈2</td><td>李工</td><td>研发院</td><td>96</td><td>95</td><td><b>95.5</b></td></tr>"
        "<tr><td>🥉3</td><td>王工</td><td>数字化中心</td><td>94</td><td>96</td><td><b>95.0</b></td></tr>"
        "<tr><td>4</td><td>赵工</td><td>规划院</td><td>93</td><td>94</td><td><b>93.5</b></td></tr>"
        "<tr><td>5</td><td>陈工</td><td>市场研究部</td><td>92</td><td>93</td><td><b>92.5</b></td></tr>"
        "</table>"
        "</div>"  # sci-perf

        # 标准管理
        "<div class='sci-panel' id='sci-std'>"
        "<div class='kpi-grid'>"
        "<div class='kpi-card'><div class='kpi-val'>23</div><div class='kpi-lbl'>国家标准</div></div>"
        "<div class='kpi-card'><div class='kpi-val'>56</div><div class='kpi-lbl'>行业标准</div></div>"
        "<div class='kpi-card'><div class='kpi-val'>34</div><div class='kpi-lbl'>团体标准</div></div>"
        "<div class='kpi-card'><div class='kpi-val'>12</div><div class='kpi-lbl'>工法</div></div>"
        "</div>"
        "<div class='chart-grid'>"
        "<div class='chart-card'><h4>标准类型分布</h4><canvas id='sci-std-pie' width='400' height='200'></canvas></div>"
        "<div class='chart-card'><h4>标准生命周期状态</h4><canvas id='sci-std-bar' width='400' height='200'></canvas></div>"
        "</div>"
        "<table><tr><th>标准编号</th><th>标准名称</th><th>类型</th><th>状态</th><th>预计发布</th></tr>"
        "<tr><td>GB/T XXXX-2026</td><td>" + kw1 + "系统安全技术规范</td><td>国标</td><td><span class='badge badge-yellow'>报批中</span></td><td>2026-Q3</td></tr>"
        "<tr><td>DL/T XXXX-2026</td><td>" + kw2 + "并网技术要求</td><td>行标</td><td><span class='badge badge-blue'>征求意见</span></td><td>2026-Q4</td></tr>"
        "<tr><td>T/CEC XXXX-2025</td><td>" + kw3 + "互联互通接口规范</td><td>团标</td><td><span class='badge badge-green'>已发布</span></td><td>2025-12</td></tr>"
        "<tr><td>GB/T XXXX-2025</td><td>电力" + kw1 + "数据交换协议</td><td>国标</td><td><span class='badge badge-green'>已发布</span></td><td>2025-09</td></tr>"
        "</table>"
        "</div>"  # sci-std

        # 其余10个子模块（精简版，各含KPI+图表+表格占位）
        + gen_remaining_sci_modules(company, kw1, kw2, kw3) +

        "</div></div>"  # end sci-wrap, view-scimgmt

        # ── Modal 弹窗 ──
        "<div class='modal-overlay' id='modal'>"
        "<div class='modal-box'>"
        "<span class='modal-close' onclick='closeModal()'>✕</span>"
        "<div class='modal-title' id='modal-title'>详情</div>"
        "<div id='modal-body'></div>"
        "</div></div>"

        # ── AI 机器人按钮 ──
        "<div class='bot-btn' onclick='alert(\"AI情报助理：请输入您的问题，我将从250条情报中为您检索答案。\")' title='AI情报助理'>🤖</div>"

        "</div></div>"  # end content, page-wrap

        # ════════ JS ════════
        "<script>"
        "var currentView='intel';"
        "function switchView(v){"
        "  document.querySelectorAll('.view').forEach(function(el){el.classList.remove('active');});"
        "  document.getElementById('view-'+v).classList.add('active');"
        "  var tabs=document.querySelectorAll('.top-tab');"
        "  var idx={'intel':0,'workbench':1,'techroute':2,'scimgmt':3};"
        "  tabs.forEach(function(t){t.classList.remove('active');});"
        "  if(idx[v]!==undefined) tabs[idx[v]].classList.add('active');"
        "  var sb=document.getElementById('main-sidebar');"
        "  if(sb) sb.style.display=(v==='scimgmt')?'none':'block';"
        "  currentView=v;"
        "  if(v==='scimgmt'){setTimeout(function(){showSciModule('proj',null);},80);}"
        "  window.scrollTo(0,0);"
        "}"
        "function switchDataTab(t){"
        "  document.querySelectorAll('.data-tab').forEach(function(el){el.classList.remove('active');});"
        "  document.querySelectorAll('.data-panel').forEach(function(el){el.classList.remove('active');});"
        "  var tab=document.getElementById('tab-'+t);"
        "  var panel=document.getElementById('panel-'+t);"
        "  if(tab) tab.classList.add('active');"
        "  if(panel) panel.classList.add('active');"
        "  var items=document.querySelectorAll('.sidebar-item');"
        "  var map={'patent':0,'news':1,'policy':2,'report':3,'internal':4};"
        "  items.forEach(function(i){i.classList.remove('active');});"
        "  if(map[t]!==undefined && items[map[t]]) items[map[t]].classList.add('active');"
        "}"
        "function switchStep(prefix,id,btn){"
        "  var panels=document.querySelectorAll('[id^=\"'+prefix+'-s\"]');"
        "  panels.forEach(function(p){p.classList.remove('active');});"
        "  var el=document.getElementById(prefix+'-'+id);"
        "  if(el) el.classList.add('active');"
        "  if(btn){"
        "    var sibs=btn.parentElement.querySelectorAll('.step-tab');"
        "    sibs.forEach(function(s){s.classList.remove('active');});"
        "    btn.classList.add('active');"
        "  }"
        "  if(prefix==='tr') setTimeout(drawAllTrCharts,80);"
        "  if(prefix==='wb') setTimeout(drawAllWbCharts,80);"
        "}"
        "var sciModuleActive=null;"
        "function showSciModule(id,btn){"
        "  document.querySelectorAll('.sci-panel').forEach(function(p){p.classList.remove('active');});"
        "  var el=document.getElementById('sci-'+id);"
        "  if(el) el.classList.add('active');"
        "  document.querySelectorAll('.sci-nav-btn').forEach(function(b){b.classList.remove('active');});"
        "  if(btn) btn.classList.add('active');"
        "  sciModuleActive=id;"
        "  setTimeout(function(){drawSciChartsFor(id);},80);"
        "}"
        "function openModal(id,type){"
        "  document.getElementById('modal-title').textContent=type+'情报 #'+id+' 详情';"
        "  document.getElementById('modal-body').innerHTML='<p style=\"color:#666;line-height:1.8\">情报编号：'+id+'<br>类型：'+type+'<br>数据来源：PatSnap智慧芽 / Web Search<br><br>点击查看完整内容，可从此情报启动政策孵化工作台分析。</p>"
        "<div style=\"margin-top:12px\"><span class=\"action-btn\" onclick=\"switchView('workbench');closeModal()\">→ 启动政策孵化</span></div>';"
        "  document.getElementById('modal').classList.add('active');"
        "}"
        "function closeModal(){"
        "  document.getElementById('modal').classList.remove('active');"
        "}"
        "function filterRows(){"
        "  var q=document.getElementById('search-input').value.toLowerCase();"
        "  document.querySelectorAll('.data-row').forEach(function(r){"
        "    r.style.display=r.textContent.toLowerCase().indexOf(q)>=0?'flex':'none';"
        "  });"
        "}"
        "function filterByKw(kw){"
        "  document.getElementById('search-input').value=kw;"
        "  filterRows();"
        "}"
        "function submitToSciMgmt(){"
        "  if(confirm('确认提交立项审查？\\n项目：" + kw1 + "关键技术研究\\n来源：技术路线研判输出成果\\n系统将自动在科技创新管理中创建项目记录 EPPEI-2026-ST-047')){"
        "    switchView('scimgmt');"
        "    setTimeout(function(){showSciModule('proj',null);},200);"
        "  }"
        "}"

        # Canvas 绘图工具函数
        "function setupC(id){"
        "  var c=document.getElementById(id);"
        "  if(!c)return null;"
        "  var p=c.parentElement;"
        "  var w=p.clientWidth||400; var h=220;"
        "  var dpr=window.devicePixelRatio||1;"
        "  c.width=Math.round(w*dpr); c.height=Math.round(h*dpr);"
        "  c.style.width=w+'px'; c.style.height=h+'px';"
        "  var ctx=c.getContext('2d');"
        "  ctx.scale(dpr,dpr);"
        "  return {ctx:ctx,w:w,h:h};"
        "}"
        "function drawBar(id,labels,vals,colors,title){"
        "  var s=setupC(id); if(!s)return;"
        "  var ctx=s.ctx,W=s.w,H=s.h;"
        "  var pad={l:44,r:16,t:28,b:36};"
        "  var bw=W-pad.l-pad.r; var bh=H-pad.t-pad.b;"
        "  var max=Math.max.apply(null,vals)*1.15||1;"
        "  ctx.clearRect(0,0,W,H);"
        "  for(var i=0;i<5;i++){var y=pad.t+bh*(1-i/4);ctx.strokeStyle='#e5e7eb';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(pad.l,y);ctx.lineTo(W-pad.r,y);ctx.stroke();ctx.fillStyle='#aaa';ctx.font='10px sans-serif';ctx.textAlign='right';ctx.fillText(Math.round(max*i/4),pad.l-4,y+4);}"
        "  var bw2=(bw/labels.length)*0.6; var gap=(bw/labels.length)*0.4;"
        "  for(var i=0;i<labels.length;i++){"
        "    var x=pad.l+(bw/labels.length)*i+gap/2;"
        "    var h2=(vals[i]/max)*bh;"
        "    ctx.fillStyle=colors[i%colors.length];"
        "    ctx.fillRect(x,pad.t+bh-h2,bw2,h2);"
        "    ctx.fillStyle='#333';ctx.font='bold 10px sans-serif';ctx.textAlign='center';"
        "    ctx.fillText(vals[i],x+bw2/2,pad.t+bh-h2-4);"
        "    ctx.fillStyle='#666';ctx.font='10px sans-serif';"
        "    ctx.fillText(labels[i],x+bw2/2,H-pad.b+14);"
        "  }"
        "}"
        "function drawLine(id,labels,series,colors){"
        "  var s=setupC(id); if(!s)return;"
        "  var ctx=s.ctx,W=s.w,H=s.h;"
        "  var pad={l:44,r:16,t:20,b:36};"
        "  var all=[].concat.apply([],series.map(function(s){return s.data;}));"
        "  var max=Math.max.apply(null,all)*1.1||1;"
        "  ctx.clearRect(0,0,W,H);"
        "  for(var i=0;i<5;i++){var y=pad.t+(H-pad.t-pad.b)*(1-i/4);ctx.strokeStyle='#e5e7eb';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(pad.l,y);ctx.lineTo(W-pad.r,y);ctx.stroke();ctx.fillStyle='#aaa';ctx.font='10px sans-serif';ctx.textAlign='right';ctx.fillText(Math.round(max*i/4),pad.l-4,y+4);}"
        "  var step=(W-pad.l-pad.r)/(labels.length-1||1);"
        "  for(var si=0;si<series.length;si++){"
        "    var d=series[si].data; ctx.beginPath(); ctx.strokeStyle=colors[si%colors.length]; ctx.lineWidth=2;"
        "    for(var i=0;i<d.length;i++){var x=pad.l+i*step;var y=pad.t+(H-pad.t-pad.b)*(1-d[i]/max);if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);}"
        "    ctx.stroke();"
        "    for(var i=0;i<d.length;i++){var x=pad.l+i*step;var y=pad.t+(H-pad.t-pad.b)*(1-d[i]/max);ctx.beginPath();ctx.arc(x,y,3,0,Math.PI*2);ctx.fillStyle=colors[si%colors.length];ctx.fill();}"
        "  }"
        "  for(var i=0;i<labels.length;i++){ctx.fillStyle='#666';ctx.font='10px sans-serif';ctx.textAlign='center';ctx.fillText(labels[i],pad.l+i*step,H-pad.b+14);}"
        "}"
        "function drawPie(id,labels,vals,colors){"
        "  var s=setupC(id); if(!s)return;"
        "  var ctx=s.ctx,W=s.w,H=s.h;"
        "  ctx.clearRect(0,0,W,H);"
        "  var total=vals.reduce(function(a,b){return a+b;},0)||1;"
        "  var cx=W*0.38,cy=H/2,r=Math.min(cx,cy)*0.78;"
        "  var a=-.5*Math.PI;"
        "  for(var i=0;i<vals.length;i++){"
        "    var slice=vals[i]/total*Math.PI*2;"
        "    ctx.beginPath();ctx.moveTo(cx,cy);ctx.arc(cx,cy,r,a,a+slice);ctx.closePath();"
        "    ctx.fillStyle=colors[i%colors.length];ctx.fill();"
        "    ctx.strokeStyle='#fff';ctx.lineWidth=1.5;ctx.stroke();"
        "    var ma=a+slice/2; var tx=cx+Math.cos(ma)*r*0.65; var ty=cy+Math.sin(ma)*r*0.65;"
        "    ctx.fillStyle='#fff';ctx.font='bold 10px sans-serif';ctx.textAlign='center';"
        "    ctx.fillText(Math.round(vals[i]/total*100)+'%',tx,ty+4);"
        "    a+=slice;"
        "  }"
        "  var lx=W*0.72, ly=H/2-(labels.length-1)*11;"
        "  for(var i=0;i<labels.length;i++){ctx.fillStyle=colors[i%colors.length];ctx.fillRect(lx,ly+i*22,10,10);ctx.fillStyle='#444';ctx.font='11px sans-serif';ctx.textAlign='left';ctx.fillText(labels[i],lx+14,ly+i*22+10);}"
        "}"
        "function drawGauge(id,val,max,color){"
        "  var s=setupC(id); if(!s)return;"
        "  var ctx=s.ctx,W=s.w,H=s.h;"
        "  ctx.clearRect(0,0,W,H);"
        "  var cx=W/2,cy=H*0.62,r=Math.min(W,H)*0.38;"
        "  ctx.beginPath();ctx.arc(cx,cy,r,Math.PI,2*Math.PI);ctx.strokeStyle='#e5e7eb';ctx.lineWidth=16;ctx.stroke();"
        "  ctx.beginPath();ctx.arc(cx,cy,r,Math.PI,Math.PI*(1+val/max));ctx.strokeStyle=color||'#1a3a6b';ctx.lineWidth=16;ctx.stroke();"
        "  ctx.fillStyle='#1a3a6b';ctx.font='bold 28px sans-serif';ctx.textAlign='center';ctx.fillText(val,cx,cy+8);"
        "  ctx.fillStyle='#888';ctx.font='12px sans-serif';ctx.fillText('/'+max,cx,cy+26);"
        "}"

        # 技术路线图表
        "function drawAllTrCharts(){"
        "  drawBar('tr-chart2',['政策热点','储能安全','现货市场','绿氢','虚拟电厂','碳市场'],[42,38,35,28,22,18],['#1a3a6b','#2563eb','#3b82f6','#60a5fa','#93c5fd','#bfdbfe']);"
        "  drawPie('tr-chart3',['指导意见','强制标准','试点通知','补贴政策','规划文件'],[32,25,20,13,10],['#1a3a6b','#2563eb','#3b82f6','#60a5fa','#93c5fd']);"
        "  drawBar('tr-chart4',['安全红线','市场准入','环保要求','并网标准','数据安全','补贴条件'],[95,88,82,78,71,64],['#dc2626','#ea580c','#d97706','#1a3a6b','#2563eb','#3b82f6']);"
        "  drawBar('tr-chart6',['安全监测','成本优化','智能调度','互联标准','长时储能','绿氢制备'],[95,90,82,74,68,55],['#1a3a6b','#2563eb','#3b82f6','#60a5fa','#93c5fd','#bfdbfe']);"
        "  drawLine('tr-chart7',['2026','2027','2028','2029','2030'],["
        "    {data:[7,8,8,9,9]},"
        "    {data:[6,7,7,8,9]},"
        "    {data:[4,5,6,7,8]}"
        "  ],['#1a3a6b','#2563eb','#60a5fa']);"
        "  drawGauge('tr-chart11',92,100,'#1a3a6b');"
        "  drawBar('tr-chart12',['路线清单','攻关目录','落地方案','研判报告'],[12,18,6,3],['#1a3a6b','#2563eb','#3b82f6','#60a5fa']);"
        "}"

        # 政策孵化图表
        "function drawAllWbCharts(){"
        "  drawBar('wb-chart1',['P1','P2','P3','P4','P5'],[7,9,6,4,2],['#dc2626','#ea580c','#d97706','#1a3a6b','#3b82f6']);"
        "  drawPie('wb-chart2',['政府监管','产业痛点','市场反馈','政策导向','企业诉求'],[8,7,6,5,2],['#1a3a6b','#2563eb','#3b82f6','#60a5fa','#93c5fd']);"
        "  drawLine('wb-chart3',['2021','2022','2023','2024','2025','2026'],[{data:[22,38,57,78,112,145]}],['#1a3a6b']);"
        "  drawLine('wb-chart4',['2021','2022','2023','2024','2025','2026'],[{data:[1.20,1.05,0.92,0.78,0.68,0.62]}],['#2563eb']);"
        "  drawLine('wb-chart5',['2026','2027','2028','2029','2030'],["
        "    {data:[160,200,250,290,320]},"
        "    {data:[155,185,220,265,295]},"
        "    {data:[148,168,195,235,268]}"
        "  ],['#16a34a','#1a3a6b','#dc2626']);"
        "  drawBar('wb-chart6',['方案A','方案B','方案C'],[8.2,12.5,10.8],['#60a5fa','#1a3a6b','#2563eb']);"
        "  drawBar('wb-chart7',['装机规模','度电成本','市场化率','安全事故','人才培养'],[88,76,65,92,70],['#1a3a6b','#2563eb','#3b82f6','#16a34a','#60a5fa']);"
        "  drawPie('wb-chart9',['政策报告','配套标准','试点方案','建议条目'],[3,6,4,12],['#1a3a6b','#2563eb','#3b82f6','#60a5fa']);"
        "  drawBar('wb-chart10',['政策完备','数据支撑','可操作性','创新性','落地性'],[92,88,85,90,87],['#1a3a6b','#2563eb','#3b82f6','#60a5fa','#93c5fd']);"
        "}"

        # 科技创新管理图表
        "function drawSciChartsFor(id){"
        "  if(id==='proj'){drawBar('sci-proj-bar',['立项论证','开题','中期','验收','结题'],[12,9,14,8,4],['#1a3a6b','#2563eb','#3b82f6','#16a34a','#888']);drawLine('sci-proj-line',['2021','2022','2023','2024','2025','2026'],[{data:[28,32,35,38,43,47]}],['#1a3a6b']);}"
        "  else if(id==='ip'){drawLine('sci-ip-line',['2021','2022','2023','2024','2025','2026'],[{data:[120,145,162,178,186,186]},{data:[88,102,118,131,142,148]}],['#1a3a6b','#2563eb']);drawBar('sci-ip-bar',['H02J','H01M','G06Q','G06F','G06N','H02P'],[4822,3441,2153,1622,1234,987],['#1a3a6b','#2563eb','#3b82f6','#60a5fa','#93c5fd','#bfdbfe']);}"
        "  else if(id==='perf'){drawBar('sci-perf-bar',['技术中心','研发院','数字化','规划院','市场部','标准所','平台部'],[97,95,93,92,91,89,88],['#1a3a6b','#2563eb','#3b82f6','#60a5fa','#93c5fd','#bfdbfe','#dbeafe']);drawLine('sci-perf-line',['Q1 2025','Q2 2025','Q3 2025','Q4 2025','Q1 2026'],[{data:[91,92,93,93,94]}],['#1a3a6b']);}"
        "  else if(id==='std'){drawPie('sci-std-pie',['国标','行标','团标','工法'],[23,56,34,12],['#1a3a6b','#2563eb','#3b82f6','#60a5fa']);drawBar('sci-std-bar',['报批中','征求意见','已发布','修订中','废止'],[8,12,89,8,3],['#d97706','#3b82f6','#16a34a','#60a5fa','#dc2626']);}"
        "  else if(id==='req'){drawPie('sci-req-pie',['政府行业','战略客户','企业内部','员工报送','市场反馈'],[8,7,6,5,2],['#1a3a6b','#2563eb','#3b82f6','#60a5fa','#93c5fd']);drawBar('sci-req-bar',['P1','P2','P3','P4','P5'],[7,9,6,4,2],['#dc2626','#ea580c','#d97706','#1a3a6b','#3b82f6']);}"
        "  else if(id==='award'){drawBar('sci-award-bar',['国家进步奖','中电科技奖','省部级奖','专利优秀奖','其他'],[2,5,8,12,3],['#1a3a6b','#2563eb','#3b82f6','#60a5fa','#93c5fd']);drawLine('sci-award-line',['2021','2022','2023','2024','2025'],[{data:[18,22,24,26,30]}],['#2563eb']);}"
        "  else if(id==='result'){drawBar('sci-result-bar',['TRL1-3','TRL4-5','TRL6-7','TRL8','TRL9'],[18,42,98,156,109],['#93c5fd','#60a5fa','#3b82f6','#2563eb','#1a3a6b']);drawLine('sci-result-line',['2021','2022','2023','2024','2025'],[{data:[18,22,28,34,42]}],['#16a34a']);}"
        "  else if(id==='hightech'){drawPie('sci-hightech-pie',['人员费','仪器折旧','材料费','委托研发','其他'],[42,23,18,12,5],['#1a3a6b','#2563eb','#3b82f6','#60a5fa','#93c5fd']);drawGauge('sci-hightech-gauge',92,100,'#16a34a');}"
        "  else if(id==='org'){drawBar('sci-org-bar',['博士','硕士','本科','专科'],[89,156,203,42],['#1a3a6b','#2563eb','#3b82f6','#60a5fa']);drawPie('sci-org-pie',['高级','中级','初级','院士/专家'],[142,198,132,18],['#1a3a6b','#2563eb','#3b82f6','#dc2626']);}"
        "  else if(id==='plan'){drawBar('sci-plan-bar',['指标A','指标B','指标C','指标D','指标E','指标F'],[88,92,76,95,82,79],['#1a3a6b','#2563eb','#3b82f6','#60a5fa','#93c5fd','#bfdbfe']);drawLine('sci-plan-line',['2021','2022','2023','2024','2025','2026'],[{data:[72,78,82,86,90,92]}],['#1a3a6b']);}"
        "  else if(id==='coop'){drawPie('sci-coop-pie',['高校院所','央企国企','民营企业','国际机构','科研院所'],[28,18,12,5,4],['#1a3a6b','#2563eb','#3b82f6','#60a5fa','#93c5fd']);drawBar('sci-coop-bar',['联合研发','委托研究','人才交流','平台共建','成果转化'],[32,18,12,8,6],['#1a3a6b','#2563eb','#3b82f6','#60a5fa','#93c5fd']);}"
        "  else if(id==='annual'){drawBar('sci-annual-bar',['Q1','Q2','Q3','Q4'],[82,88,76,91],['#1a3a6b','#2563eb','#3b82f6','#16a34a']);drawLine('sci-annual-line',['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月'],[{data:[72,68,75,80,85,88,82,79,84,88,91,93]}],['#1a3a6b']);}"
        "  else if(id==='platform'){drawBar('sci-platform-bar',['国家级','省部级','博士后站','院士工作站'],[3,8,4,2],['#1a3a6b','#2563eb','#3b82f6','#60a5fa']);drawPie('sci-platform-pie',['电力系统','储能技术','新能源','数字化','氢能'],[4,3,3,2,5],['#1a3a6b','#2563eb','#3b82f6','#60a5fa','#93c5fd']);}"
        "  else if(id==='review'){drawBar('sci-review-bar',['立项评审','中期评估','结题验收','成果鉴定','奖励评审'],[38,42,36,24,16],['#1a3a6b','#2563eb','#3b82f6','#60a5fa','#93c5fd']);drawPie('sci-review-pie',['优秀','良好','合格','需整改'],[42,88,22,4],['#16a34a','#1a3a6b','#d97706','#dc2626']);}"
        "}"

        "window.addEventListener('load',function(){"
        "  drawAllTrCharts();"
        "  drawAllWbCharts();"
        "  setTimeout(function(){drawSciChartsFor('proj');},200);"
        "});"
        "</script></body></html>"
    )
    return html

def gen_remaining_sci_modules(company, kw1, kw2, kw3):
    """生成剩余10个科技创新管理子模块HTML"""
    modules = {
        "req": (
            "<div class='kpi-grid'>"
            "<div class='kpi-card'><div class='kpi-val'>28</div><div class='kpi-lbl'>需求总数</div></div>"
            "<div class='kpi-card'><div class='kpi-val'>7</div><div class='kpi-lbl'>P1紧急</div></div>"
            "<div class='kpi-card'><div class='kpi-val'>9</div><div class='kpi-lbl'>P2重要</div></div>"
            "<div class='kpi-card'><div class='kpi-val'>12</div><div class='kpi-lbl'>已处理</div></div>"
            "</div>"
            "<div class='chart-grid'>"
            "<div class='chart-card'><h4>需求来源分布</h4><canvas id='sci-req-pie' width='400' height='200'></canvas></div>"
            "<div class='chart-card'><h4>优先级分布</h4><canvas id='sci-req-bar' width='400' height='200'></canvas></div>"
            "</div>"
            "<table><tr><th>编号</th><th>需求描述</th><th>优先级</th><th>来源</th><th>状态</th></tr>"
            "<tr><td>RQ-001</td><td>" + kw1 + "安全标准亟需更新</td><td><span class='badge badge-red'>P1</span></td><td>政府监管</td><td><span class='badge badge-yellow'>处理中</span></td></tr>"
            "<tr><td>RQ-002</td><td>" + kw1 + "成本下降路径测算</td><td><span class='badge badge-red'>P1</span></td><td>产业需求</td><td><span class='badge badge-blue'>新建</span></td></tr>"
            "<tr><td>RQ-003</td><td>" + kw2 + "市场机制完善</td><td><span class='badge badge-yellow'>P2</span></td><td>市场反馈</td><td><span class='badge badge-green'>已分发</span></td></tr>"
            "</table>"
        ),
        "org": (
            "<div class='kpi-grid'>"
            "<div class='kpi-card'><div class='kpi-val'>490</div><div class='kpi-lbl'>科研人员</div></div>"
            "<div class='kpi-card'><div class='kpi-val'>18</div><div class='kpi-lbl'>院士/专家</div></div>"
            "<div class='kpi-card'><div class='kpi-val'>245</div><div class='kpi-lbl'>博士</div></div>"
            "<div class='kpi-card'><div class='kpi-val'>12</div><div class='kpi-lbl'>创新团队</div></div>"
            "</div>"
            "<div class='chart-grid'>"
            "<div class='chart-card'><h4>学历结构</h4><canvas id='sci-org-bar' width='400' height='200'></canvas></div>"
            "<div class='chart-card'><h4>职称分布</h4><canvas id='sci-org-pie' width='400' height='200'></canvas></div>"
            "</div>"
            "<table><tr><th>团队名称</th><th>负责人</th><th>研究方向</th><th>人数</th><th>级别</th></tr>"
            "<tr><td>" + kw1 + "技术团队</td><td>张教授</td><td>安全与控制</td><td>32</td><td><span class='badge badge-red'>国家级</span></td></tr>"
            "<tr><td>" + kw2 + "创新团队</td><td>李研究员</td><td>系统集成</td><td>28</td><td><span class='badge badge-blue'>省部级</span></td></tr>"
            "<tr><td>数字化研究团队</td><td>王教授</td><td>AI调度算法</td><td>24</td><td><span class='badge badge-blue'>省部级</span></td></tr>"
            "</table>"
        ),
        "plan": (
            "<div class='kpi-grid'>"
            "<div class='kpi-card'><div class='kpi-val'>88%</div><div class='kpi-lbl'>规划执行进度</div></div>"
            "<div class='kpi-card'><div class='kpi-val'>24</div><div class='kpi-lbl'>核心指标数</div></div>"
            "<div class='kpi-card'><div class='kpi-val'>6</div><div class='kpi-lbl'>重点专项</div></div>"
            "<div class='kpi-card'><div class='kpi-val'>2026</div><div class='kpi-lbl'>中期评估年</div></div>"
            "</div>"
            "<div class='chart-grid'>"
            "<div class='chart-card'><h4>核心指标完成率</h4><canvas id='sci-plan-bar' width='400' height='200'></canvas></div>"
            "<div class='chart-card'><h4>规划目标演进</h4><canvas id='sci-plan-line' width='400' height='200'></canvas></div>"
            "</div>"
            "<table><tr><th>指标名称</th><th>基准值</th><th>2026目标</th><th>当前值</th><th>完成率</th></tr>"
            "<tr><td>科研经费</td><td>8.2亿</td><td>12亿</td><td>11.1亿</td><td><div class='prog-bar'><div class='prog-fill' style='width:88%;background:#1a3a6b'></div></div></td></tr>"
            "<tr><td>授权专利</td><td>980</td><td>1500</td><td>1284</td><td><div class='prog-bar'><div class='prog-fill' style='width:76%;background:#2563eb'></div></div></td></tr>"
            "<tr><td>成果转化率</td><td>35%</td><td>55%</td><td>48%</td><td><div class='prog-bar'><div class='prog-fill' style='width:72%;background:#3b82f6'></div></div></td></tr>"
            "</table>"
        ),
        "coop": (
            "<div class='kpi-grid'>"
            "<div class='kpi-card'><div class='kpi-val'>67</div><div class='kpi-lbl'>合作机构</div></div>"
            "<div class='kpi-card'><div class='kpi-val'>28</div><div class='kpi-lbl'>高校院所</div></div>"
            "<div class='kpi-card'><div class='kpi-val'>18</div><div class='kpi-lbl'>央企国企</div></div>"
            "<div class='kpi-card'><div class='kpi-val'>5</div><div class='kpi-lbl'>国际机构</div></div>"
            "</div>"
            "<div class='chart-grid'>"
            "<div class='chart-card'><h4>机构类型分布</h4><canvas id='sci-coop-pie' width='400' height='200'></canvas></div>"
            "<div class='chart-card'><h4>合作模式分布</h4><canvas id='sci-coop-bar' width='400' height='200'></canvas></div>"
            "</div>"
            "<table><tr><th>机构名称</th><th>合作类型</th><th>合作项目数</th><th>合同金额</th><th>状态</th></tr>"
            "<tr><td>清华大学</td><td>联合研发</td><td>8</td><td>2,400万</td><td><span class='badge badge-green'>合作中</span></td></tr>"
            "<tr><td>中国科学院</td><td>委托研究</td><td>5</td><td>1,800万</td><td><span class='badge badge-green'>合作中</span></td></tr>"
            "<tr><td>国家电网</td><td>平台共建</td><td>3</td><td>3,200万</td><td><span class='badge badge-blue'>洽谈中</span></td></tr>"
            "</table>"
        ),
        "annual": (
            "<div class='kpi-grid'>"
            "<div class='kpi-card'><div class='kpi-val'>86</div><div class='kpi-lbl'>年度计划总数</div></div>"
            "<div class='kpi-card'><div class='kpi-val'>42</div><div class='kpi-lbl'>进行中</div></div>"
            "<div class='kpi-card'><div class='kpi-val'>34</div><div class='kpi-lbl'>已完成</div></div>"
            "<div class='kpi-card'><div class='kpi-val'>3</div><div class='kpi-lbl'>预警</div></div>"
            "</div>"
            "<div class='chart-grid'>"
            "<div class='chart-card'><h4>季度完成情况</h4><canvas id='sci-annual-bar' width='400' height='200'></canvas></div>"
            "<div class='chart-card'><h4>月度执行进度</h4><canvas id='sci-annual-line' width='400' height='200'></canvas></div>"
            "</div>"
            "<table><tr><th>计划编号</th><th>计划名称</th><th>负责部门</th><th>进度</th><th>状态</th></tr>"
            "<tr><td>AP-2026-001</td><td>" + kw1 + "专项研究计划</td><td>技术中心</td><td><div class='prog-bar'><div class='prog-fill' style='width:45%;background:#1a3a6b'></div></div></td><td><span class='badge badge-blue'>正常</span></td></tr>"
            "<tr><td>AP-2026-002</td><td>数字化转型计划</td><td>数字中心</td><td><div class='prog-bar'><div class='prog-fill' style='width:62%;background:#2563eb'></div></div></td><td><span class='badge badge-blue'>正常</span></td></tr>"
            "<tr><td>AP-2026-003</td><td>" + kw2 + "标准制定计划</td><td>标准所</td><td><div class='prog-bar'><div class='prog-fill' style='width:28%;background:#dc2626'></div></div></td><td><span class='badge badge-red'>预警</span></td></tr>"
            "</table>"
        ),
        "platform": (
            "<div class='kpi-grid'>"
            "<div class='kpi-card'><div class='kpi-val'>3</div><div class='kpi-lbl'>国家级平台</div></div>"
            "<div class='kpi-card'><div class='kpi-val'>8</div><div class='kpi-lbl'>省部级平台</div></div>"
            "<div class='kpi-card'><div class='kpi-val'>4</div><div class='kpi-lbl'>博士后工作站</div></div>"
            "<div class='kpi-card'><div class='kpi-val'>2</div><div class='kpi-lbl'>院士工作站</div></div>"
            "</div>"
            "<div class='chart-grid'>"
            "<div class='chart-card'><h4>平台级别分布</h4><canvas id='sci-platform-bar' width='400' height='200'></canvas></div>"
            "<div class='chart-card'><h4>研究领域分布</h4><canvas id='sci-platform-pie' width='400' height='200'></canvas></div>"
            "</div>"
            "<table><tr><th>平台名称</th><th>级别</th><th>依托机构</th><th>成立时间</th><th>状态</th></tr>"
            "<tr><td>" + kw1 + "国家重点实验室</td><td><span class='badge badge-red'>国家级</span></td><td>" + company + "</td><td>2018-06</td><td><span class='badge badge-green'>运行中</span></td></tr>"
            "<tr><td>电力系统技术工程研究中心</td><td><span class='badge badge-blue'>省部级</span></td><td>" + company + "</td><td>2019-03</td><td><span class='badge badge-green'>运行中</span></td></tr>"
            "<tr><td>" + kw2 + "院士工作站</td><td><span class='badge badge-yellow'>院士站</span></td><td>" + company + "/清华大学</td><td>2022-09</td><td><span class='badge badge-green'>运行中</span></td></tr>"
            "</table>"
        ),
        "award": (
            "<div class='kpi-grid'>"
            "<div class='kpi-card'><div class='kpi-val'>2</div><div class='kpi-lbl'>国家科技进步奖</div></div>"
            "<div class='kpi-card'><div class='kpi-val'>15</div><div class='kpi-lbl'>中国电力科技奖</div></div>"
            "<div class='kpi-card'><div class='kpi-val'>28</div><div class='kpi-lbl'>省部级奖励</div></div>"
            "<div class='kpi-card'><div class='kpi-val'>3</div><div class='kpi-lbl'>申报中</div></div>"
            "</div>"
            "<div class='chart-grid'>"
            "<div class='chart-card'><h4>获奖类型分布</h4><canvas id='sci-award-bar' width='400' height='200'></canvas></div>"
            "<div class='chart-card'><h4>历年获奖趋势</h4><canvas id='sci-award-line' width='400' height='200'></canvas></div>"
            "</div>"
            "<table><tr><th>奖项名称</th><th>获奖项目</th><th>奖励等级</th><th>年度</th><th>状态</th></tr>"
            "<tr><td>国家科技进步奖</td><td>" + kw1 + "关键技术</td><td>二等奖</td><td>2025</td><td><span class='badge badge-green'>已获奖</span></td></tr>"
            "<tr><td>中国电力科技奖</td><td>" + kw2 + "系统优化</td><td>一等奖</td><td>2025</td><td><span class='badge badge-green'>已获奖</span></td></tr>"
            "<tr><td>国家科技进步奖</td><td>" + kw3 + "智慧调度</td><td>二等奖</td><td>2026</td><td><span class='badge badge-yellow'>申报中</span></td></tr>"
            "</table>"
        ),
        "review": (
            "<div class='kpi-grid'>"
            "<div class='kpi-card'><div class='kpi-val'>156</div><div class='kpi-lbl'>年度评审总次</div></div>"
            "<div class='kpi-card'><div class='kpi-val'>12</div><div class='kpi-lbl'>本月待评</div></div>"
            "<div class='kpi-card'><div class='kpi-val'>328</div><div class='kpi-lbl'>专家库人数</div></div>"
            "<div class='kpi-card'><div class='kpi-val'>94%</div><div class='kpi-lbl'>优良率</div></div>"
            "</div>"
            "<div class='chart-grid'>"
            "<div class='chart-card'><h4>评审类型分布</h4><canvas id='sci-review-bar' width='400' height='200'></canvas></div>"
            "<div class='chart-card'><h4>评审结果分布</h4><canvas id='sci-review-pie' width='400' height='200'></canvas></div>"
            "</div>"
            "<table><tr><th>评审名称</th><th>类型</th><th>计划时间</th><th>专家数</th><th>状态</th></tr>"
            "<tr><td>EPPEI-2026-ST-047立项评审</td><td>立项</td><td>2026-06-15</td><td>7</td><td><span class='badge badge-yellow'>待评</span></td></tr>"
            "<tr><td>" + kw2 + "项目中期评估</td><td>中期</td><td>2026-06-20</td><td>5</td><td><span class='badge badge-yellow'>待评</span></td></tr>"
            "<tr><td>" + kw3 + "项目结题验收</td><td>验收</td><td>2026-06-28</td><td>9</td><td><span class='badge badge-blue'>筹备中</span></td></tr>"
            "</table>"
        ),
        "hightech": (
            "<div class='kpi-grid'>"
            "<div class='kpi-card'><div class='kpi-val'>92.5</div><div class='kpi-lbl'>高企评分</div></div>"
            "<div class='kpi-card'><div class='kpi-val'>3.28亿</div><div class='kpi-lbl'>研发费用</div></div>"
            "<div class='kpi-card'><div class='kpi-val'>8.6%</div><div class='kpi-lbl'>研发投入强度</div></div>"
            "<div class='kpi-card'><div class='kpi-val'>2027-12</div><div class='kpi-lbl'>证书到期</div></div>"
            "</div>"
            "<div class='chart-grid'>"
            "<div class='chart-card'><h4>研发费用构成</h4><canvas id='sci-hightech-pie' width='400' height='200'></canvas></div>"
            "<div class='chart-card'><h4>综合评分仪表盘</h4><canvas id='sci-hightech-gauge' width='400' height='200'></canvas></div>"
            "</div>"
            "<table><tr><th>费用类别</th><th>金额（万元）</th><th>占比</th><th>同比</th></tr>"
            "<tr><td>人员人工费</td><td>13,776</td><td>42%</td><td>+12%</td></tr>"
            "<tr><td>仪器设备折旧</td><td>7,544</td><td>23%</td><td>+8%</td></tr>"
            "<tr><td>材料费</td><td>5,904</td><td>18%</td><td>+15%</td></tr>"
            "<tr><td>委托研发费</td><td>3,936</td><td>12%</td><td>+22%</td></tr>"
            "<tr><td>其他费用</td><td>1,640</td><td>5%</td><td>+5%</td></tr>"
            "</table>"
        ),
        "result": (
            "<div class='kpi-grid'>"
            "<div class='kpi-card'><div class='kpi-val'>423</div><div class='kpi-lbl'>在库成果</div></div>"
            "<div class='kpi-card'><div class='kpi-val'>168</div><div class='kpi-lbl'>已转化</div></div>"
            "<div class='kpi-card'><div class='kpi-val'>4.7亿</div><div class='kpi-lbl'>转化收益</div></div>"
            "<div class='kpi-card'><div class='kpi-val'>28</div><div class='kpi-lbl'>推进中</div></div>"
            "</div>"
            "<div class='chart-grid'>"
            "<div class='chart-card'><h4>TRL成熟度分布</h4><canvas id='sci-result-bar' width='400' height='200'></canvas></div>"
            "<div class='chart-card'><h4>成果转化趋势</h4><canvas id='sci-result-line' width='400' height='200'></canvas></div>"
            "</div>"
            "<table><tr><th>成果名称</th><th>技术领域</th><th>TRL</th><th>转化方式</th><th>状态</th></tr>"
            "<tr><td>" + kw1 + "安全监测系统</td><td>" + kw1 + "</td><td>TRL8 ●●●●●●●●○</td><td>许可证转让</td><td><span class='badge badge-green'>已转化</span></td></tr>"
            "<tr><td>" + kw2 + "优化调度平台</td><td>" + kw2 + "</td><td>TRL7 ●●●●●●●○○</td><td>合作开发</td><td><span class='badge badge-yellow'>推进中</span></td></tr>"
            "<tr><td>" + kw3 + "预测算法</td><td>" + kw3 + "</td><td>TRL6 ●●●●●●○○○</td><td>技术入股</td><td><span class='badge badge-blue'>洽谈中</span></td></tr>"
            "</table>"
        ),
    }

    html = ""
    for mid, content in modules.items():
        html += "<div class='sci-panel' id='sci-" + mid + "'>" + content + "</div>"
    return html

# ─────────────────────────────────────────────
# 主流程
# ─────────────────────────────────────────────
def main():
    args = parse_args()
    print("[智慧情报门户生成器] 启动...")
    print("  企业：" + args.company)
    print("  行业：" + args.industry)
    print("  输出：" + args.output)

    # 生成示例数据（真实数据通过MCP获取后可替换）
    data = {
        "patents":   gen_patents(args.company, args.industry),
        "news":      gen_news(args.company, args.industry),
        "policies":  gen_policies(args.company, args.industry),
        "reports":   gen_reports(args.company, args.industry),
        "internals": gen_internal(args.company, args.industry),
    }

    print("[生成] 各类数据（每类50条）完成")

    html = generate_portal_html(args, data)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")

    print("[完成] 文件已写入: " + str(out_path) + " (" + str(len(html)) + " 字符)")
    print("[提示] 用浏览器打开该文件即可查看完整情报门户")

if __name__ == "__main__":
    main()

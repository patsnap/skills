#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pharma-intelligence-brief · generate_report.py  v2.4.0
修复记录：
  v2.4.0  根本修复：补全全部缺失渲染函数及 main() 入口（v2.1.0/v2.2.0/v2.3.0 文件截断遗留）
          - 新增 render_papers_section()
          - 新增 render_trials_section()
          - 新增 render_deals_section()
          - 新增 render_news_section()
          - 新增 render_actions_section()
          - 新增 render_sources_section()
          - 新增 build_html() 完整页面组装
          - 新增 main() 命令行入口
  v2.3.0  根本修复：申请人回填逻辑 + 渲染层警示样式
  v2.2.0  重写完整脚本：补全 HTML 渲染函数和 main() 入口（v2.1.0 文件截断导致 Python 失败）
  v2.1.0  patent_link() 新增 patent_id 参数

用法：
  python generate_report.py <data_json_path> [output_html_path]
  若未指定输出路径，则写入 EUREKA_PYTHON_OUTPUT_DIR/pharma_intel_brief_YYYYMMDD.html
"""

import json
import os
import sys
import html as html_module
from datetime import datetime

# ── RDKit 可选 ─────────────────────────────────────────────────
try:
    from rdkit import Chem
    from rdkit.Chem import Draw
    import base64, io
    RDKIT_AVAILABLE = True
except ImportError:
    RDKIT_AVAILABLE = False


# ════════════════════════════════════════════════════════════════
# 工具函数
# ════════════════════════════════════════════════════════════════

def esc(text) -> str:
    """HTML 转义，防止 XSS。"""
    if text is None:
        return ""
    return html_module.escape(str(text), quote=True)


def smiles_to_svg(smiles: str):
    if not RDKIT_AVAILABLE or not smiles:
        return None
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        from rdkit.Chem.Draw import rdMolDraw2D
        import base64
        drawer = rdMolDraw2D.MolDraw2DSVG(300, 200)
        drawer.DrawMolecule(mol)
        drawer.FinishDrawing()
        svg = drawer.GetDrawingText()
        b64 = base64.b64encode(svg.encode()).decode()
        return f'data:image/svg+xml;base64,{b64}'
    except Exception:
        return None


def patent_link(pn: str, url: str = "", patent_id: str = "") -> str:
    """将专利号渲染为可点击链接。"""
    if not pn:
        return pn or ""
    if url:
        href = url
    elif patent_id:
        href = f"https://eureka.zhihuiya.com/view/#/fullText?patentId={patent_id}"
    else:
        import urllib.parse
        href = f"https://eureka.zhihuiya.com/patent-search/search?q={urllib.parse.quote(pn)}"
    return (
        f'<a href="{href}" target="_blank" rel="noopener noreferrer" '
        f'style="color:#1a6fbc;text-decoration:underline;font-weight:600;">{esc(pn)}</a>'
    )


def render_assignee(assignee: str) -> str:
    """渲染申请人字段，空值或占位符显示橙色警示。"""
    placeholder_values = {"", "[待补充]", "[待查]", "[待查询]"}
    if (assignee or "").strip() in placeholder_values:
        return ('<span style="color:#e67e22;font-weight:600;" '
                'title="申请人信息未能从搜索结果获取，请点击专利号链接查看原始著录项">'
                '⚠ 申请人待查（点击专利号查看原文）</span>')
    return esc(assignee)


def tag_class(type_tag: str) -> str:
    mapping = {
        "化合物": "compound", "compound": "compound",
        "序列": "sequence", "sequence": "sequence",
        "晶型": "crystal", "crystal form": "crystal",
        "医药用途": "use", "new use": "use",
        "组合物": "combo", "combination": "combo",
        "制剂": "formulation", "formulation": "formulation",
        "制备方法": "process", "合成工艺": "process", "process": "process",
    }
    key = (type_tag or "").strip().lower()
    cls = mapping.get(key, "other")
    return f"tag tag-{cls}"


def priority_color(priority: str) -> str:
    mapping = {"高": "#e74c3c", "中": "#e67e22", "低": "#27ae60",
               "high": "#e74c3c", "medium": "#e67e22", "low": "#27ae60"}
    return mapping.get((priority or "").strip(), "#95a5a6")


def evaluation_badge(ev: str) -> str:
    ev_map = {
        "阳性": ("#27ae60", "✓ 阳性"), "POSITIVE": ("#27ae60", "✓ 阳性"),
        "阴性": ("#e74c3c", "✗ 阴性"), "NEGATIVE": ("#e74c3c", "✗ 阴性"),
        "中性": ("#95a5a6", "— 中性"), "SIMILAR": ("#95a5a6", "— 中性"),
    }
    color, label = ev_map.get((ev or "").upper(), ("#95a5a6", ev or "—"))
    return f'<span style="color:{color};font-weight:600;">{esc(label)}</span>'


# ════════════════════════════════════════════════════════════════
# CSS
# ════════════════════════════════════════════════════════════════

def get_css() -> str:
    return """
<style>
  :root {
    --hero-bg: linear-gradient(135deg, #0f2b5e 0%, #1a4a8a 60%, #1e6091 100%);
    --accent: #1a6fbc;
    --accent-light: #e8f1fb;
    --border: #dde4f0;
    --text: #1a1a2e;
    --text-muted: #6b7280;
    --bg: #f7f9fc;
    --white: #ffffff;
    --red: #e74c3c;
    --orange: #e67e22;
    --green: #27ae60;
    --yellow: #f39c12;
    --section-radius: 10px;
    --shadow: 0 2px 12px rgba(0,0,0,0.07);
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', sans-serif;
    background: var(--bg); color: var(--text); line-height: 1.6;
  }
  .hero {
    background: var(--hero-bg); position: sticky; top: 0; z-index: 1000;
    box-shadow: 0 2px 16px rgba(0,0,0,0.18);
  }
  .hero-top {
    display: flex; align-items: flex-start; justify-content: space-between;
    padding: 14px 24px 8px 24px; flex-wrap: wrap; gap: 8px;
  }
  .hero-title { color: #fff; font-size: 20px; font-weight: 700; letter-spacing: 0.5px; line-height: 1.3; }
  .hero-meta { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 6px; }
  .hero-meta-item {
    color: rgba(255,255,255,0.88); font-size: 12px;
    background: rgba(255,255,255,0.12); border-radius: 12px;
    padding: 2px 10px; border: 1px solid rgba(255,255,255,0.18);
  }
  .hero-badge {
    background: linear-gradient(135deg, #f39c12, #e67e22); color: white;
    font-size: 12px; font-weight: 700; padding: 4px 14px; border-radius: 16px;
    white-space: nowrap; align-self: flex-start; margin-top: 2px;
  }
  .hero-nav {
    background: rgba(0,0,0,0.18); border-top: 1px solid rgba(255,255,255,0.1);
    padding: 0 24px; display: flex; gap: 0; overflow-x: auto; scrollbar-width: none;
  }
  .hero-nav::-webkit-scrollbar { display: none; }
  .hero-nav a {
    color: rgba(255,255,255,0.78); text-decoration: none; font-size: 13px;
    padding: 8px 14px; white-space: nowrap; border-bottom: 2px solid transparent; transition: all 0.2s;
  }
  .hero-nav a:hover, .hero-nav a.active {
    color: #fff; border-bottom: 2px solid #f39c12; background: rgba(255,255,255,0.08);
  }
  .main { max-width: 1100px; margin: 24px auto; padding: 0 20px 60px 20px; }
  .section {
    background: var(--white); border-radius: var(--section-radius);
    box-shadow: var(--shadow); margin-bottom: 20px; overflow: hidden; scroll-margin-top: 110px;
  }
  .section summary {
    display: flex; align-items: center; justify-content: space-between;
    padding: 14px 20px; cursor: pointer; background: var(--white);
    border-bottom: 1px solid var(--border); font-size: 15px; font-weight: 700;
    color: var(--text); user-select: none; list-style: none;
  }
  .section summary::-webkit-details-marker { display: none; }
  .section summary:hover { background: var(--accent-light); }
  .section summary .toggle-icon { font-size: 12px; color: var(--text-muted); }
  .section-body { padding: 16px 20px; }
  .patent-card {
    border: 1px solid var(--border); border-radius: 8px;
    padding: 14px 16px; margin-bottom: 12px; background: #fafcff;
  }
  .patent-card:hover { border-color: var(--accent); }
  .patent-header { display: flex; align-items: flex-start; gap: 10px; flex-wrap: wrap; margin-bottom: 8px; }
  .patent-pn { font-weight: 700; font-size: 14px; }
  .tag { display: inline-block; padding: 1px 8px; border-radius: 10px; font-size: 11px; font-weight: 600; white-space: nowrap; }
  .tag-compound  { background: #e8f5e9; color: #2e7d32; }
  .tag-sequence  { background: #e3f2fd; color: #1565c0; }
  .tag-crystal   { background: #fce4ec; color: #880e4f; }
  .tag-use       { background: #fff3e0; color: #e65100; }
  .tag-combo     { background: #f3e5f5; color: #6a1b9a; }
  .tag-process   { background: #e0f2f1; color: #00695c; }
  .tag-formulation { background: #fafafa; color: #424242; }
  .tag-other     { background: #f5f5f5; color: #616161; }
  .legal-active   { color: #27ae60; font-weight: 600; }
  .legal-inactive { color: #e74c3c; }
  .legal-pending  { color: #e67e22; }
  .patent-summary {
    font-size: 13px; color: #444; line-height: 1.7; margin-top: 6px;
    border-left: 3px solid var(--accent-light); padding-left: 10px;
  }
  .patent-meta { font-size: 12px; color: var(--text-muted); margin-top: 8px; display: flex; flex-wrap: wrap; gap: 12px; }
  .data-table { width: 100%; border-collapse: collapse; font-size: 13px; margin-top: 8px; }
  .data-table th {
    background: var(--accent-light); color: var(--accent); padding: 8px 12px;
    text-align: left; font-weight: 600; border-bottom: 2px solid var(--border);
  }
  .data-table td { padding: 8px 12px; border-bottom: 1px solid var(--border); vertical-align: top; }
  .data-table tr:hover td { background: #f7f9ff; }
  .summary-stat {
    display: inline-block; background: var(--accent-light); color: var(--accent);
    border-radius: 8px; padding: 8px 16px; margin: 4px; font-size: 14px; font-weight: 600;
  }
  .summary-stat span { font-size: 22px; display: block; }
  .top-finding {
    border-left: 4px solid var(--accent); padding: 8px 14px; margin: 8px 0;
    background: var(--accent-light); border-radius: 0 6px 6px 0; font-size: 13px;
  }
  .insight-card { border: 1px solid #b8daff; border-radius: 8px; padding: 12px 16px; margin: 8px 0; background: #f0f7ff; }
  .action-item { border-left: 4px solid; padding: 10px 14px; margin: 8px 0; border-radius: 0 6px 6px 0; }
  .empty-tip { text-align: center; color: var(--text-muted); padding: 28px 0; font-size: 14px; }
  .source-footer { background: #f0f4fa; border-radius: 8px; padding: 12px 16px; font-size: 12px; color: var(--text-muted); margin-top: 8px; }
  .pill {
    display: inline-block; padding: 2px 10px; border-radius: 12px;
    font-size: 11px; font-weight: 600; background: #e8f1fb; color: #1a6fbc; margin: 2px;
  }
  @media (max-width: 768px) {
    .main { padding: 0 10px 40px 10px; }
    .hero-top { padding: 10px 12px 6px 12px; }
  }
</style>
"""


# ════════════════════════════════════════════════════════════════
# 各模块 HTML 渲染函数
# ════════════════════════════════════════════════════════════════

def render_summary_section(data: dict) -> str:
    summary = data.get("summary", {})
    stats = summary.get("stats", {})
    findings = summary.get("top_findings", [])
    meta = data.get("meta", {})

    stat_html = ""
    for label, val in stats.items():
        stat_html += f'<div class="summary-stat"><span>{esc(str(val))}</span>{esc(label)}</div>\n'

    finding_html = ""
    for f in findings:
        priority = f.get("priority", "中")
        color = priority_color(priority)
        finding_html += (
            f'<div class="top-finding" style="border-left-color:{color};">'
            f'<b style="color:{color};">[{esc(priority)}]</b> {esc(f.get("text", ""))}</div>\n'
        )

    if not finding_html:
        finding_html = '<div class="empty-tip">暂无关键发现</div>'

    report_type = esc(meta.get("report_type", "情报简报"))
    gen_time = datetime.now().strftime("%Y-%m-%d %H:%M")

    return f"""
<details class="section" id="summary" open>
  <summary>📊 执行摘要 <span class="toggle-icon">▾</span></summary>
  <div class="section-body">
    <div style="margin-bottom:12px;">{stat_html}</div>
    <div style="margin-bottom:8px;font-weight:600;font-size:14px;color:var(--text);">🔍 本期关键发现</div>
    {finding_html}
    <div class="source-footer" style="margin-top:14px;">
      报告类型：{report_type} &nbsp;|&nbsp; 生成时间：{gen_time}
    </div>
  </div>
</details>
"""


def render_patents_section(data: dict) -> str:
    patents = data.get("patents", [])
    total = data.get("patents_total", len(patents))
    date_range = data.get("patent_date_range", "")

    if not patents:
        body = '<div class="empty-tip">⚠️ 暂无专利数据</div>'
    else:
        cards = ""
        for p in patents:
            pn = p.get("pn", "")
            url = p.get("url", "")
            patent_id = p.get("patent_id", "")
            pn_link = patent_link(pn, url, patent_id)
            type_tag = p.get("type_tag", "其他")
            legal = p.get("legal_status", "")
            legal_cls = ("legal-active" if ("有效" in legal or "active" in legal.lower())
                         else "legal-inactive" if ("无效" in legal or "失效" in legal or "inactive" in legal.lower())
                         else "legal-pending")
            assignee_html = render_assignee(p.get("assignee", ""))
            pub_date = esc(p.get("pub_date", ""))
            summary_text = esc(p.get("summary", ""))
            title = esc(p.get("title", ""))

            mol_html = ""
            for mol in p.get("molecules", []):
                smiles = mol.get("smiles", "")
                svg_uri = smiles_to_svg(smiles)
                if svg_uri:
                    mol_html += f'<img src="{svg_uri}" style="max-width:200px;margin-top:6px;" alt="结构式">'

            cards += f"""
<div class="patent-card">
  <div class="patent-header">
    <span class="patent-pn">{pn_link}</span>
    <span class="{tag_class(type_tag)}">{esc(type_tag)}</span>
    <span class="{legal_cls}">{esc(legal)}</span>
  </div>
  <div style="font-size:13px;font-weight:600;margin-bottom:4px;">{title}</div>
  <div class="patent-summary">{summary_text}</div>
  <div class="patent-meta">
    <span>📅 公开日：{pub_date}</span>
    <span>🏢 申请人：{assignee_html}</span>
  </div>
  {mol_html}
</div>
"""
        body = cards

    header_extra = f"（{esc(date_range)}，共 {total} 篇）" if date_range else f"（共 {total} 篇）"
    return f"""
<details class="section" id="patents" open>
  <summary>🔬 专利动态 {header_extra} <span class="toggle-icon">▾</span></summary>
  <div class="section-body">{body}</div>
</details>
"""


def render_papers_section(data: dict) -> str:
    papers = data.get("papers", [])
    total = data.get("papers_total", len(papers))
    date_range = data.get("paper_date_range", "")

    if not papers:
        body = '<div class="empty-tip">⚠️ 暂无文献数据</div>'
    else:
        rows = ""
        for p in papers:
            title = esc(p.get("title", ""))
            url = p.get("url", "")
            journal = esc(p.get("journal", ""))
            pub_date = esc(p.get("pub_date", ""))
            authors = esc(p.get("authors", ""))
            summary_text = esc(p.get("summary", ""))
            ev = p.get("evaluation", "")
            ev_html = evaluation_badge(ev) if ev else ""

            title_link = (
                f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer" '
                f'style="color:#1a6fbc;text-decoration:underline;font-weight:600;">{title}</a>'
                if url else f'<b>{title}</b>'
            )
            rows += f"""
<div class="patent-card">
  <div style="font-size:14px;margin-bottom:4px;">{title_link} {ev_html}</div>
  <div class="patent-summary">{summary_text}</div>
  <div class="patent-meta">
    <span>📅 {pub_date}</span>
    <span>📖 {journal}</span>
    <span>✍️ {authors}</span>
  </div>
</div>
"""
        body = rows

    header_extra = f"（{esc(date_range)}，共 {total} 篇）" if date_range else f"（共 {total} 篇）"
    return f"""
<details class="section" id="papers" open>
  <summary>📄 文献动态 {header_extra} <span class="toggle-icon">▾</span></summary>
  <div class="section-body">{body}</div>
</details>
"""


def render_trials_section(data: dict) -> str:
    trials = data.get("trials", [])
    total = data.get("trials_total", len(trials))
    date_range = data.get("trial_date_range", "")

    if not trials:
        body = '<div class="empty-tip">⚠️ 暂无临床试验数据</div>'
    else:
        rows = ""
        for t in trials:
            nct = esc(t.get("register_number") or t.get("nct_id", ""))
            title = esc(t.get("title", ""))
            url = t.get("url", "")
            phase = esc(t.get("phase", ""))
            status = esc(t.get("status", ""))
            sponsor = esc(t.get("sponsor", ""))
            disease = esc(t.get("disease", ""))
            drug = esc(t.get("drug", ""))
            summary_text = esc(t.get("summary", ""))

            nct_link = (
                f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer" '
                f'style="color:#1a6fbc;font-weight:700;">{nct}</a>'
                if url else f'<b>{nct}</b>'
            )
            rows += f"""
<div class="patent-card">
  <div class="patent-header">
    <span class="patent-pn">{nct_link}</span>
    <span class="pill">{phase}</span>
    <span class="pill">{status}</span>
  </div>
  <div style="font-size:13px;font-weight:600;margin-bottom:4px;">{title}</div>
  <div class="patent-summary">{summary_text}</div>
  <div class="patent-meta">
    <span>🏢 {sponsor}</span>
    <span>🎯 适应症：{disease}</span>
    <span>💊 药物：{drug}</span>
  </div>
</div>
"""
        body = rows

    header_extra = f"（{esc(date_range)}，共 {total} 条）" if date_range else f"（共 {total} 条）"
    return f"""
<details class="section" id="trials" open>
  <summary>🧪 临床试验 {header_extra} <span class="toggle-icon">▾</span></summary>
  <div class="section-body">{body}</div>
</details>
"""


def render_deals_section(data: dict) -> str:
    deals = data.get("deals", [])
    total = data.get("deals_total", len(deals))
    date_range = data.get("deal_date_range", "")

    if not deals:
        body = '<div class="empty-tip">⚠️ 暂无 BD 交易数据</div>'
    else:
        rows = ""
        for d in deals:
            title = esc(d.get("title", ""))
            url = d.get("url", "")
            deal_date = esc(d.get("deal_date", ""))
            deal_type = esc(d.get("deal_type", ""))
            licensor = esc(d.get("licensor", ""))
            licensee = esc(d.get("licensee", ""))
            value = esc(d.get("amount") or d.get("value", ""))
            summary_text = esc(d.get("summary", ""))

            title_link = (
                f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer" '
                f'style="color:#1a6fbc;font-weight:600;">{title}</a>'
                if url else f'<b>{title}</b>'
            )
            rows += f"""
<div class="patent-card">
  <div style="font-size:14px;margin-bottom:4px;">{title_link}</div>
  <div class="patent-summary">{summary_text}</div>
  <div class="patent-meta">
    <span>📅 {deal_date}</span>
    <span class="pill">{deal_type}</span>
    <span>🏢 授权方：{licensor}</span>
    <span>🏢 受让方：{licensee}</span>
    {f'<span>💰 {value}</span>' if value else ''}
  </div>
</div>
"""
        body = rows

    header_extra = f"（{esc(date_range)}，共 {total} 条）" if date_range else f"（共 {total} 条）"
    return f"""
<details class="section" id="deals" open>
  <summary>🤝 BD 交易 {header_extra} <span class="toggle-icon">▾</span></summary>
  <div class="section-body">{body}</div>
</details>
"""


def render_news_section(data: dict) -> str:
    news_list = data.get("news", [])
    total = data.get("news_total", len(news_list))
    date_range = data.get("news_date_range", "")

    if not news_list:
        body = '<div class="empty-tip">⚠️ 暂无新闻动态</div>'
    else:
        rows = ""
        for n in news_list:
            title = esc(n.get("title", ""))
            url = n.get("url", "")
            pub_date = esc(n.get("pub_date", ""))
            source = esc(n.get("source", ""))
            summary_text = esc(n.get("summary", ""))

            title_link = (
                f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer" '
                f'style="color:#1a6fbc;font-weight:600;">{title}</a>'
                if url else f'<b>{title}</b>'
            )
            rows += f"""
<div class="patent-card">
  <div style="font-size:14px;margin-bottom:4px;">{title_link}</div>
  <div class="patent-summary">{summary_text}</div>
  <div class="patent-meta">
    <span>📅 {pub_date}</span>
    <span>📰 {source}</span>
  </div>
</div>
"""
        body = rows

    header_extra = f"（{esc(date_range)}，共 {total} 条）" if date_range else f"（共 {total} 条）"
    return f"""
<details class="section" id="news" open>
  <summary>📰 新闻动态 {header_extra} <span class="toggle-icon">▾</span></summary>
  <div class="section-body">{body}</div>
</details>
"""


def render_actions_section(data: dict) -> str:
    actions = data.get("action_checklist") or data.get("actions", [])

    if not actions:
        body = '<div class="empty-tip">暂无行动建议</div>'
    else:
        items = ""
        for a in actions:
            priority = a.get("priority", "中")
            color = priority_color(priority)
            text = esc(a.get("action") or a.get("text", ""))
            deadline = esc(a.get("deadline", ""))
            reason = esc(a.get("reason", ""))
            dimension = esc(a.get("dimension", ""))
            items += f"""
<div class="action-item" style="border-left-color:{color};background:{color}11;">
  <span style="color:{color};font-weight:700;">[{esc(priority)}]</span>
  {text}
  {f'<div style="color:var(--text-muted);font-size:12px;margin-top:4px;">{dimension} · {reason}</div>' if (dimension or reason) else ''}
  {f'<span style="float:right;color:var(--text-muted);font-size:12px;">⏰ {deadline}</span>' if deadline else ''}
</div>
"""
        body = items

    return f"""
<details class="section" id="actions" open>
  <summary>⚡ 行动建议 <span class="toggle-icon">▾</span></summary>
  <div class="section-body">{body}</div>
</details>
"""


def render_sources_section(data: dict) -> str:
    sources = data.get("sources", [])

    if not sources:
        return ""

    rows = ""
    for i, s in enumerate(sources, 1):
        if isinstance(s, str):
            s = {"label": f"S{i}", "type": "source", "title": s}
        label = esc(s.get("label", f"S{i}"))
        source_type = esc(s.get("type", ""))
        title = esc(s.get("title", ""))
        url = s.get("url", "")
        retrieved_at = esc(s.get("retrieved_at", ""))

        title_link = (
            f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer" '
            f'style="color:#1a6fbc;">{title}</a>'
            if url else title
        )
        rows += f"""
<tr>
  <td style="font-weight:700;white-space:nowrap;">[{label}]</td>
  <td><span class="pill">{source_type}</span></td>
  <td>{title_link}</td>
  <td style="white-space:nowrap;">{retrieved_at}</td>
</tr>
"""

    return f"""
<details class="section" id="sources">
  <summary>📚 来源列表 <span class="toggle-icon">▾</span></summary>
  <div class="section-body">
    <table class="data-table">
      <thead><tr><th>编号</th><th>类型</th><th>标题</th><th>检索时间</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
    <div class="source-footer" style="margin-top:10px;">
      ⚠️ 未显式标注来源标记的结论应视为 <code>Unverified</code>。
    </div>
  </div>
</details>
"""


# ════════════════════════════════════════════════════════════════
# 完整页面组装
# ════════════════════════════════════════════════════════════════

def build_html(data: dict) -> str:
    meta = data.get("meta", {})
    title_text = meta.get("title", "情报简报")
    subtitle = meta.get("subtitle", "")
    date_range = meta.get("time_window") or meta.get("date_range", "")
    targets = meta.get("targets", [])
    target = ", ".join(targets) if isinstance(targets, list) else (targets or meta.get("target", ""))
    company = meta.get("user_company") or meta.get("company", "")

    meta_items = ""
    for label, val in [("靶点/主题", target), ("报告周期", date_range), ("研究机构", company)]:
        if val:
            meta_items += f'<span class="hero-meta-item">{esc(label)}：{esc(val)}</span>'

    nav_links = ""
    nav_map = [
        ("summary", "📊 执行摘要"),
        ("patents", "🔬 专利"),
        ("papers", "📄 文献"),
        ("trials", "🧪 临床"),
        ("deals", "🤝 BD 交易"),
        ("news", "📰 新闻"),
        ("actions", "⚡ 行动建议"),
        ("sources", "📚 来源"),
    ]
    for anchor, label in nav_map:
        nav_links += f'<a href="#{anchor}">{label}</a>'

    sections_html = (
        render_summary_section(data)
        + render_patents_section(data)
        + render_papers_section(data)
        + render_trials_section(data)
        + render_deals_section(data)
        + render_news_section(data)
        + render_actions_section(data)
        + render_sources_section(data)
    )

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title_text)}</title>
  {get_css()}
</head>
<body>
<div class="hero">
  <div class="hero-top">
    <div>
      <div class="hero-title">{esc(title_text)}</div>
      {f'<div style="color:rgba(255,255,255,0.75);font-size:13px;margin-top:4px;">{esc(subtitle)}</div>' if subtitle else ''}
      <div class="hero-meta">{meta_items}</div>
    </div>
    <div class="hero-badge">Pharma Intel Brief</div>
  </div>
  <nav class="hero-nav">{nav_links}</nav>
</div>
<div class="main">{sections_html}</div>
<script>
  // 导航栏高亮
  const navLinks = document.querySelectorAll('.hero-nav a');
  const observer = new IntersectionObserver((entries) => {{
    entries.forEach(e => {{
      if (e.isIntersecting) {{
        navLinks.forEach(a => a.classList.remove('active'));
        const active = document.querySelector('.hero-nav a[href="#' + e.target.id + '"]');
        if (active) active.classList.add('active');
      }}
    }});
  }}, {{ rootMargin: '-110px 0px -60% 0px' }});
  document.querySelectorAll('.section[id]').forEach(s => observer.observe(s));
</script>
</body>
</html>"""


# ════════════════════════════════════════════════════════════════
# main() 命令行入口
# ════════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("用法：python generate_report.py <data_json_path> [output_html_path]", file=sys.stderr)
        sys.exit(1)

    data_path = sys.argv[1]
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    html_content = build_html(data)

    if len(sys.argv) >= 3:
        out_path = sys.argv[2]
    else:
        out_dir = os.environ.get("EUREKA_PYTHON_OUTPUT_DIR", ".")
        today = datetime.now().strftime("%Y%m%d")
        out_path = os.path.join(out_dir, f"pharma_intel_brief_{today}.html")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[OK] 报告已生成：{out_path}")
    return out_path


if __name__ == "__main__":
    main()

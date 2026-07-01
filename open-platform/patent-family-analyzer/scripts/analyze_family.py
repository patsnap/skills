#!/usr/bin/env python3
"""
Patent Family Analyzer — 同族专利深度分析脚本

用法:
    python analyze_family.py <patent_number> [--out <output_html_path>]

说明:
    1. 通过 Eureka MCP (patsnap_fetch) 获取同族专利数据
    2. 逐件获取各同族专利全文
    3. 调用 AI 分析技术要素并生成 HTML 报告

    本脚本为技能的参考实现，实际执行由 Eureka Agent 逐步完成。
    脚本主要负责 HTML 报告的结构与渲染逻辑。
"""

import json
import sys
import os
import argparse
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# HTML 报告模板生成
# ---------------------------------------------------------------------------

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>同族专利分析报告 — {root_pn}</title>
<style>
  :root {{
    --primary: #1a73e8;
    --secondary: #34a853;
    --accent: #fbbc04;
    --danger: #ea4335;
    --bg: #f8f9fa;
    --card-bg: #ffffff;
    --border: #e0e0e0;
    --text: #202124;
    --muted: #5f6368;
    --sidebar-w: 260px;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: "Segoe UI", "PingFang SC", sans-serif; background: var(--bg); color: var(--text); display: flex; min-height: 100vh; }}
  
  /* ---- Sidebar ---- */
  #sidebar {{
    width: var(--sidebar-w); min-width: var(--sidebar-w);
    background: #fff; border-right: 1px solid var(--border);
    position: fixed; top: 0; left: 0; height: 100vh; overflow-y: auto;
    z-index: 100; padding: 24px 0;
  }}
  #sidebar .logo {{ padding: 0 20px 20px; border-bottom: 1px solid var(--border); }}
  #sidebar .logo h2 {{ font-size: 15px; color: var(--primary); font-weight: 700; }}
  #sidebar .logo p {{ font-size: 12px; color: var(--muted); margin-top: 4px; }}
  #sidebar nav {{ padding: 12px 0; }}
  #sidebar nav a {{
    display: flex; align-items: center; gap: 8px;
    padding: 10px 20px; font-size: 14px; color: var(--muted);
    text-decoration: none; transition: all .2s;
    border-left: 3px solid transparent;
  }}
  #sidebar nav a:hover, #sidebar nav a.active {{
    background: #e8f0fe; color: var(--primary);
    border-left-color: var(--primary);
  }}
  #sidebar nav a .icon {{ font-size: 16px; width: 20px; text-align: center; }}
  
  /* ---- Main ---- */
  #main {{ margin-left: var(--sidebar-w); flex: 1; padding: 32px 40px; max-width: 1200px; }}
  
  /* ---- Header ---- */
  .report-header {{
    background: linear-gradient(135deg, var(--primary), #0d47a1);
    color: white; border-radius: 12px; padding: 32px;
    margin-bottom: 32px;
  }}
  .report-header h1 {{ font-size: 24px; font-weight: 700; }}
  .report-header p {{ opacity: .85; margin-top: 8px; font-size: 14px; }}
  .meta-chips {{ display: flex; gap: 12px; margin-top: 16px; flex-wrap: wrap; }}
  .chip {{
    background: rgba(255,255,255,.2); border-radius: 20px;
    padding: 4px 14px; font-size: 12px;
  }}
  
  /* ---- Section ---- */
  .section {{ margin-bottom: 40px; scroll-margin-top: 24px; }}
  .section-title {{
    font-size: 20px; font-weight: 700; color: var(--text);
    border-left: 4px solid var(--primary); padding-left: 12px;
    margin-bottom: 20px;
  }}
  
  /* ---- Cards ---- */
  .card {{
    background: var(--card-bg); border: 1px solid var(--border);
    border-radius: 10px; padding: 20px; margin-bottom: 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,.06);
  }}
  .card-header {{
    display: flex; justify-content: space-between; align-items: flex-start;
    margin-bottom: 14px;
  }}
  .card-header h3 {{ font-size: 15px; font-weight: 600; color: var(--primary); }}
  .badge {{
    display: inline-block; border-radius: 4px; padding: 2px 8px;
    font-size: 11px; font-weight: 600; white-space: nowrap;
  }}
  .badge-active {{ background: #e6f4ea; color: #137333; }}
  .badge-inactive {{ background: #fce8e6; color: #c5221f; }}
  .badge-pending {{ background: #fef7e0; color: #b06000; }}
  .badge-country {{ background: #e8f0fe; color: var(--primary); }}
  
  .field-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px 20px; }}
  .field {{ font-size: 13px; }}
  .field .label {{ color: var(--muted); font-size: 11px; text-transform: uppercase; letter-spacing: .5px; margin-bottom: 3px; }}
  .field .value {{ color: var(--text); font-weight: 500; }}
  
  .tech-section {{ margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--border); }}
  .tech-item {{ margin-bottom: 12px; }}
  .tech-item .tech-label {{
    font-size: 12px; font-weight: 700; color: var(--primary);
    text-transform: uppercase; letter-spacing: .5px; margin-bottom: 4px;
  }}
  .tech-item p {{ font-size: 13px; color: var(--text); line-height: 1.6; }}
  
  /* ---- Tree Chart ---- */
  #family-tree {{ overflow-x: auto; }}
  #tree-svg {{ min-height: 300px; width: 100%; }}
  
  /* ---- Table ---- */
  .matrix-table {{ width: 100%; border-collapse: collapse; font-size: 12px; overflow-x: auto; display: block; }}
  .matrix-table th {{
    background: var(--primary); color: white;
    padding: 8px 12px; text-align: center;
    position: sticky; top: 0;
  }}
  .matrix-table td {{ padding: 8px 12px; border: 1px solid var(--border); text-align: center; }}
  .matrix-table tr:nth-child(even) td {{ background: #f8f9fa; }}
  .cell-yes {{ background: #e6f4ea !important; color: #137333; font-weight: 700; }}
  .cell-partial {{ background: #fef7e0 !important; color: #b06000; font-weight: 700; }}
  
  /* ---- Timeline ---- */
  .timeline {{ position: relative; padding-left: 32px; }}
  .timeline::before {{
    content: ""; position: absolute; left: 12px; top: 0; bottom: 0;
    width: 2px; background: var(--border);
  }}
  .tl-item {{ position: relative; margin-bottom: 24px; }}
  .tl-dot {{
    position: absolute; left: -27px; top: 4px;
    width: 14px; height: 14px; border-radius: 50%;
    background: var(--primary); border: 3px solid #fff;
    box-shadow: 0 0 0 2px var(--primary);
  }}
  .tl-date {{ font-size: 11px; color: var(--muted); margin-bottom: 4px; }}
  .tl-content {{ font-size: 13px; line-height: 1.6; }}
  .tl-tag {{
    display: inline-block; background: #e8f0fe; color: var(--primary);
    border-radius: 3px; padding: 1px 6px; font-size: 11px; margin: 2px;
  }}
  
  /* ---- Summary ---- */
  .summary-grid {{ display: grid; grid-template-columns: repeat(3,1fr); gap: 16px; margin-bottom: 24px; }}
  .stat-card {{
    text-align: center; background: var(--card-bg);
    border: 1px solid var(--border); border-radius: 10px; padding: 20px;
  }}
  .stat-card .num {{ font-size: 36px; font-weight: 700; color: var(--primary); }}
  .stat-card .label {{ font-size: 12px; color: var(--muted); margin-top: 4px; }}
  
  @media (max-width: 900px) {{
    #sidebar {{ display: none; }}
    #main {{ margin-left: 0; padding: 20px; }}
    .summary-grid {{ grid-template-columns: 1fr 1fr; }}
  }}
</style>
</head>
<body>
<nav id="sidebar">
  <div class="logo">
    <h2>📋 同族专利分析</h2>
    <p>{root_pn}</p>
  </div>
  <nav>
    <a href="#overview" class="active"><span class="icon">🏠</span> 概览</a>
    <a href="#family-list"><span class="icon">📑</span> 同族清单</a>
    <a href="#family-tree"><span class="icon">🌳</span> 同族树状图</a>
    <a href="#tech-analysis"><span class="icon">🔬</span> 技术分析</a>
    <a href="#tech-relation"><span class="icon">🔗</span> 技术关联性</a>
    <a href="#cross-matrix"><span class="icon">📊</span> 主题交叉矩阵</a>
    <a href="#evolution"><span class="icon">📈</span> 技术演进路线</a>
    <a href="#conclusion"><span class="icon">📝</span> 分析总结</a>
  </nav>
</nav>

<main id="main">
  <div class="report-header">
    <h1>同族专利深度分析报告</h1>
    <p>基于专利 {root_pn} 的全球同族专利技术分析</p>
    <div class="meta-chips">
      <span class="chip">🗓 生成时间：{gen_time}</span>
      <span class="chip">📦 同族数量：{family_count} 件</span>
      <span class="chip">🌍 覆盖国家/地区：{country_count}</span>
    </div>
  </div>

  <!-- ① 概览统计 -->
  <section class="section" id="overview">
    <h2 class="section-title">① 概览统计</h2>
    <div class="summary-grid">
      {stat_cards}
    </div>
  </section>

  <!-- ② 同族专利清单 -->
  <section class="section" id="family-list">
    <h2 class="section-title">② 同族专利清单</h2>
    {family_list_html}
  </section>

  <!-- ③ 同族树状图 -->
  <section class="section" id="family-tree">
    <h2 class="section-title">③ 同族专利树状图</h2>
    <div id="family-tree">
      <svg id="tree-svg"></svg>
    </div>
  </section>

  <!-- ④ 技术分析 -->
  <section class="section" id="tech-analysis">
    <h2 class="section-title">④ 逐件技术要素分析</h2>
    {tech_analysis_html}
  </section>

  <!-- ⑤ 技术关联性 -->
  <section class="section" id="tech-relation">
    <h2 class="section-title">⑤ 技术关联性分析</h2>
    {tech_relation_html}
  </section>

  <!-- ⑥ 主题交叉矩阵 -->
  <section class="section" id="cross-matrix">
    <h2 class="section-title">⑥ 技术主题交叉分析矩阵</h2>
    <div style="overflow-x:auto">
      {cross_matrix_html}
    </div>
  </section>

  <!-- ⑦ 技术演进路线 -->
  <section class="section" id="evolution">
    <h2 class="section-title">⑦ 技术演进路线</h2>
    <div class="timeline">
      {timeline_html}
    </div>
  </section>

  <!-- ⑧ 分析总结 -->
  <section class="section" id="conclusion">
    <h2 class="section-title">⑧ 分析总结</h2>
    <div class="card">
      {conclusion_html}
    </div>
  </section>

  <div style="text-align:center;color:var(--muted);font-size:12px;padding:40px 0 20px">
    本报告由 Eureka × PatSnap 智慧芽 同族专利分析技能生成 · {gen_time}
  </div>
</main>

<script>
// ---- 侧边栏高亮 ----
const sections = document.querySelectorAll(".section");
const navLinks = document.querySelectorAll("#sidebar nav a");
const observer = new IntersectionObserver(entries => {{
  entries.forEach(e => {{
    if(e.isIntersecting) {{
      navLinks.forEach(a => a.classList.remove("active"));
      const link = document.querySelector(`#sidebar nav a[href="#${{e.target.id}}"]`);
      if(link) link.classList.add("active");
    }}
  }});
}}, {{threshold: 0.3}});
sections.forEach(s => observer.observe(s));

// ---- 树状图 D3-lite (纯 SVG，无需外部依赖) ----
const treeData = {tree_data_json};
(function renderTree() {{
  const svg = document.getElementById("tree-svg");
  if(!treeData || !treeData.nodes) return;
  const W = svg.parentElement.clientWidth || 900;
  const NODE_H = 48, NODE_W = 180, H_GAP = 60, V_GAP = 80;
  
  // 按层次分组
  const levels = {{}};
  treeData.nodes.forEach(n => {{
    if(!levels[n.depth]) levels[n.depth] = [];
    levels[n.depth].push(n);
  }});
  const maxDepth = Math.max(...Object.keys(levels).map(Number));
  const svgH = (maxDepth + 1) * (NODE_H + V_GAP) + 40;
  svg.setAttribute("viewBox", `0 0 ${{W}} ${{svgH}}`);
  svg.setAttribute("height", svgH);
  
  // 计算位置
  Object.entries(levels).forEach(([depth, nodes]) => {{
    const totalW = nodes.length * NODE_W + (nodes.length - 1) * H_GAP;
    const startX = (W - totalW) / 2;
    nodes.forEach((n, i) => {{
      n.x = startX + i * (NODE_W + H_GAP);
      n.y = Number(depth) * (NODE_H + V_GAP) + 20;
    }});
  }});
  
  const nodeMap = {{}};
  treeData.nodes.forEach(n => nodeMap[n.id] = n);
  
  let svgContent = "";
  // 画连线
  treeData.edges.forEach(e => {{
    const s = nodeMap[e.source], t = nodeMap[e.target];
    if(!s || !t) return;
    const sx = s.x + NODE_W/2, sy = s.y + NODE_H;
    const tx = t.x + NODE_W/2, ty = t.y;
    const my = (sy + ty) / 2;
    svgContent += `<path d="M${{sx}},${{sy}} C${{sx}},${{my}} ${{tx}},${{my}} ${{tx}},${{ty}}" fill="none" stroke="#bbb" stroke-width="1.5"/>`;
  }});
  // 画节点
  treeData.nodes.forEach(n => {{
    const fill = n.depth === 0 ? "#1a73e8" : (n.depth === 1 ? "#34a853" : "#fbbc04");
    const textColor = n.depth <= 1 ? "white" : "#202124";
    svgContent += `
      <g transform="translate(${{n.x}},${{n.y}})" style="cursor:pointer" onclick="window.open('${{n.url || ""}}','_blank')">
        <rect width="${{NODE_W}}" height="${{NODE_H}}" rx="8" fill="${{fill}}" opacity=".92"/>
        <text x="${{NODE_W/2}}" y="16" text-anchor="middle" fill="${{textColor}}" font-size="11" font-weight="700">${{n.label}}</text>
        <text x="${{NODE_W/2}}" y="30" text-anchor="middle" fill="${{textColor}}" font-size="10" opacity=".85">${{n.country || ""}}</text>
        <text x="${{NODE_W/2}}" y="42" text-anchor="middle" fill="${{textColor}}" font-size="9" opacity=".75">${{n.date || ""}}</text>
      </g>`;
  }});
  svg.innerHTML = svgContent;
}})();
</script>
</body>
</html>
'''


def make_stat_cards(stats: list) -> str:
    """生成统计卡片 HTML"""
    cards = []
    for s in stats:
        cards.append(f'<div class="stat-card"><div class="num">{s["num"]}</div><div class="label">{s["label"]}</div></div>')
    return "\n".join(cards)


def make_family_list(patents: list) -> str:
    """生成同族专利清单 HTML"""
    items = []
    for p in patents:
        status_badge = f'<span class="badge badge-{p.get("legal_status","pending")}">{p.get("legal_status_label","未知")}</span>'
        items.append(f'''
<div class="card">
  <div class="card-header">
    <h3><a href="{p.get("url","#")}" target="_blank" style="color:inherit;text-decoration:none">🔗 {p.get("pn","")}</a></h3>
    <div style="display:flex;gap:6px;flex-wrap:wrap">
      <span class="badge badge-country">{p.get("country","")}</span>
      {status_badge}
    </div>
  </div>
  <div class="field-grid">
    <div class="field"><div class="label">标题</div><div class="value">{p.get("title","—")}</div></div>
    <div class="field"><div class="label">申请人</div><div class="value">{p.get("assignee","—")}</div></div>
    <div class="field"><div class="label">申请日</div><div class="value">{p.get("app_date","—")}</div></div>
    <div class="field"><div class="label">公开日</div><div class="value">{p.get("pub_date","—")}</div></div>
    <div class="field"><div class="label">IPC分类</div><div class="value">{p.get("ipc","—")}</div></div>
    <div class="field"><div class="label">优先权日</div><div class="value">{p.get("priority_date","—")}</div></div>
  </div>
</div>''')
    return "\n".join(items)


def make_tech_analysis(analyses: list) -> str:
    """生成技术要素分析 HTML"""
    items = []
    for a in analyses:
        note = '<span style="font-size:11px;color:#b06000;margin-left:6px">⚠ 基于摘要分析</span>' if a.get("abstract_only") else ""
        items.append(f'''
<div class="card">
  <div class="card-header">
    <h3>🔬 {a.get("pn","")} — {a.get("title","")}{note}</h3>
    <span class="badge badge-country">{a.get("country","")}</span>
  </div>
  <div class="tech-section">
    <div class="tech-item">
      <div class="tech-label">🎯 技术问题</div>
      <p>{a.get("tech_problem","—")}</p>
    </div>
    <div class="tech-item">
      <div class="tech-label">⚙️ 技术手段</div>
      <p>{a.get("tech_means","—")}</p>
    </div>
    <div class="tech-item">
      <div class="tech-label">✅ 技术效果</div>
      <p>{a.get("tech_effect","—")}</p>
    </div>
    <div class="tech-item">
      <div class="tech-label">📋 权利要求结构要点</div>
      <p>{a.get("claim_structure","—")}</p>
    </div>
  </div>
</div>''')    
    return "\n".join(items)


def make_tech_relation(relations: list) -> str:
    """生成技术关联性分析 HTML"""
    items = []
    for r in relations:
        items.append(f'''
<div class="card">
  <div class="card-header">
    <h3>🔗 {r.get("pn","")} 相对关联同族</h3>
  </div>
  <div class="tech-section">
    <div class="tech-item">
      <div class="tech-label">📈 改进点</div>
      <p>{r.get("improvement","—")}</p>
    </div>
    <div class="tech-item">
      <div class="tech-label">💡 创新点</div>
      <p>{r.get("innovation","—")}</p>
    </div>
    <div class="tech-item">
      <div class="tech-label">↔️ 并行扩展</div>
      <p>{r.get("extension","—")}</p>
    </div>
  </div>
</div>''')
    return "\n".join(items)


def make_cross_matrix(matrix: dict) -> str:
    """生成技术主题交叉矩阵 HTML"""
    patents = matrix.get("patents", [])
    themes = matrix.get("themes", [])
    cells = matrix.get("cells", {})
    
    th_row = "".join([f'<th>专利号</th>'] + [f'<th>{t}</th>' for t in themes])
    rows = []
    for p in patents:
        tds = f'<td style="text-align:left;font-weight:600;color:var(--primary)">{p}</td>'
        for t in themes:
            val = cells.get(p, {}).get(t, "")
            cls = "cell-yes" if val == "●" else ("cell-partial" if val == "◑" else "")
            tds += f'<td class="{cls}">{val}</td>'
        rows.append(f'<tr>{tds}</tr>')
    
    legend = '<div style="font-size:12px;color:var(--muted);margin-top:12px">● 完全覆盖 &nbsp; ◑ 部分覆盖 &nbsp; — 不涉及</div>'
    return f'<table class="matrix-table"><thead><tr>{th_row}</tr></thead><tbody>{chr(10).join(rows)}</tbody></table>{legend}'


def make_timeline(events: list) -> str:
    """生成时间轴 HTML"""
    items = []
    for e in events:
        tags = "".join([f'<span class="tl-tag">{t}</span>' for t in e.get("tags", [])])
        items.append(f'''
<div class="tl-item">
  <div class="tl-dot"></div>
  <div class="tl-date">{e.get("date","")} · {e.get("pn","")}</div>
  <div class="tl-content">
    <strong>{e.get("title","")}</strong><br>
    {e.get("desc","")}
    <div style="margin-top:6px">{tags}</div>
  </div>
</div>''')
    return "\n".join(items)


def make_conclusion(conclusion: dict) -> str:
    """生成总结 HTML"""
    return f'''
<div style="line-height:1.8">
  <p style="margin-bottom:12px"><strong>📌 技术定位：</strong>{conclusion.get("positioning","—")}</p>
  <p style="margin-bottom:12px"><strong>🌍 市场覆盖策略：</strong>{conclusion.get("market_coverage","—")}</p>
  <p style="margin-bottom:12px"><strong>🛡 核心技术保护强度：</strong>{conclusion.get("protection_strength","—")}</p>
  <p style="margin-bottom:12px"><strong>⚠️ 技术空白与风险提示：</strong>{conclusion.get("risk","—")}</p>
</div>'''


def build_html(data: dict) -> str:
    """组装完整 HTML 报告"""
    patents = data.get("patents", [])
    root_pn = data.get("root_pn", "未知")
    countries = list(set(p.get("country", "") for p in patents))
    
    stats = [
        {"num": len(patents), "label": "同族专利总数"},
        {"num": len(countries), "label": "覆盖国家/地区"},
        {"num": len([p for p in patents if p.get("legal_status") == "active"]), "label": "有效专利"},
    ]
    
    html = HTML_TEMPLATE.format(
        root_pn=root_pn,
        gen_time=datetime.now().strftime("%Y-%m-%d %H:%M"),
        family_count=len(patents),
        country_count=len(countries),
        stat_cards=make_stat_cards(stats),
        family_list_html=make_family_list(patents),
        tech_analysis_html=make_tech_analysis(data.get("analyses", [])),
        tech_relation_html=make_tech_relation(data.get("relations", [])),
        cross_matrix_html=make_cross_matrix(data.get("matrix", {})),
        timeline_html=make_timeline(data.get("timeline", [])),
        conclusion_html=make_conclusion(data.get("conclusion", {})),
        tree_data_json=json.dumps(data.get("tree", {"nodes": [], "edges": []})),
    )
    return html


def main():
    parser = argparse.ArgumentParser(description="同族专利分析 HTML 报告生成器")
    parser.add_argument("data_json", help="包含分析结果的 JSON 数据文件路径")
    parser.add_argument("--out", default="patent_family_report.html", help="输出 HTML 文件路径")
    args = parser.parse_args()
    
    with open(args.data_json, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    html = build_html(data)
    
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ 报告已生成: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

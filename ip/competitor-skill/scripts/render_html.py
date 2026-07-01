#!/usr/bin/env python3
"""将竞对专利报告 Markdown 转换为 Google Material Design 风格的 HTML 页面。"""
import sys
import re
import urllib.parse
from pathlib import Path
from datetime import datetime


# ── 样式 ──────────────────────────────────────────────────────────────────────
STYLE = """
:root{--bg:#f0f2f5;--white:#fff;--border:#e4e8ef;--accent:#2563eb;--accent2:#1d4ed8;
  --text:#1a1a2e;--sub:#64748b;--success:#16a34a;--warn:#d97706;--danger:#dc2626;
  --nav-w:270px;--radius:12px;}

*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:-apple-system,"PingFang SC","Helvetica Neue",sans-serif;
  background:var(--bg);color:var(--text);display:flex;min-height:100vh;}
#sidebar{width:var(--nav-w);min-width:var(--nav-w);background:var(--white);
  border-right:1px solid var(--border);position:fixed;top:0;left:0;
  height:100vh;overflow-y:auto;z-index:200;display:flex;flex-direction:column;}
#sidebar-logo{padding:20px 18px 12px;border-bottom:1px solid var(--border);}
#sidebar-logo h2{font-size:14px;font-weight:700;color:var(--accent);}
#sidebar-logo p{font-size:11px;color:var(--sub);margin-top:3px;}
#sidebar nav{padding:10px 0 40px;}
.nav-part{display:flex;align-items:center;gap:8px;padding:9px 18px;
  font-size:12px;font-weight:700;color:var(--sub);text-transform:uppercase;
  letter-spacing:.06em;cursor:pointer;text-decoration:none;
  border-left:3px solid transparent;transition:all .15s;}
.nav-part:hover,.nav-part.active{color:var(--accent);background:#eff6ff;border-left-color:var(--accent);}
.nav-sub{padding:4px 18px 4px 36px;}
.nav-sub a{display:block;font-size:12px;color:var(--sub);text-decoration:none;
  padding:4px 8px;border-radius:6px;transition:all .15s;white-space:nowrap;
  overflow:hidden;text-overflow:ellipsis;}
.nav-sub a:hover{background:#eff6ff;color:var(--accent);}
.nav-sub a.active{background:#dbeafe;color:var(--accent2);font-weight:600;}
.nav-assignee{padding:2px 18px 2px 52px;}
.nav-assignee a{display:block;font-size:11px;color:#94a3b8;text-decoration:none;
  padding:3px 6px;border-radius:4px;transition:all .15s;white-space:nowrap;
  overflow:hidden;text-overflow:ellipsis;}
.nav-assignee a:hover{color:var(--accent);background:#f0f9ff;}
#main{margin-left:var(--nav-w);flex:1;padding:32px 36px 80px;max-width:1100px;}
.hero{background:linear-gradient(135deg,#1e3a5f 0%,#1d4ed8 60%,#0ea5e9 100%);
  border-radius:var(--radius);padding:36px 40px;margin-bottom:28px;color:#fff;position:relative;overflow:hidden;}
.hero::before{content:'';position:absolute;inset:0;
  background:radial-gradient(ellipse at 80% 50%,rgba(255,255,255,.08) 0%,transparent 60%);}
.hero-dots{position:absolute;inset:0;pointer-events:none;
  background-image:radial-gradient(circle,rgba(255,255,255,.07) 1px,transparent 1px);
  background-size:28px 28px;}
.hero-inner{position:relative;z-index:1;}
.hero-badge{display:inline-block;background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.3);
  font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;
  padding:4px 12px;border-radius:20px;margin-bottom:14px;}
.hero h1{font-size:clamp(20px,2.5vw,32px);font-weight:800;letter-spacing:-.02em;margin-bottom:8px;}
.hero-meta{font-size:12px;opacity:.7;}
.hero-stats{display:flex;gap:16px;margin-top:20px;flex-wrap:wrap;}
.hero-stat{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);
  border-radius:10px;padding:12px 20px;text-align:center;min-width:90px;}
.hero-stat-num{font-size:26px;font-weight:800;line-height:1;}
.hero-stat-label{font-size:11px;opacity:.8;margin-top:4px;}
.section{background:var(--white);border:1px solid var(--border);border-radius:var(--radius);
  margin-bottom:24px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.04);}
.section-hd{display:flex;align-items:center;gap:10px;padding:18px 24px 14px;
  border-bottom:1px solid var(--border);}
.section-icon{width:32px;height:32px;border-radius:8px;display:flex;align-items:center;
  justify-content:center;font-size:16px;flex-shrink:0;}
.section-title{font-size:16px;font-weight:700;}
.section-bd{padding:20px 24px;}
.part-label{display:inline-block;font-size:10px;font-weight:700;text-transform:uppercase;
  letter-spacing:.08em;color:var(--accent);background:#dbeafe;padding:2px 8px;
  border-radius:4px;margin-bottom:16px;}
.meta-card{background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:14px 18px;margin-bottom:16px;}
.query-label{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--sub);margin-bottom:6px;}
.query-text{font-family:'SF Mono',monospace;font-size:12px;color:var(--accent2);word-break:break-all;line-height:1.7;}
.company-bars{display:flex;flex-direction:column;gap:12px;margin-bottom:20px;}
.cbar{display:flex;align-items:center;gap:10px;}
.cbar-name{font-size:13px;font-weight:600;min-width:120px;color:var(--text);}
.cbar-track{flex:1;height:8px;background:var(--border);border-radius:4px;overflow:hidden;}
.cbar-fill{height:100%;border-radius:4px;background:linear-gradient(90deg,var(--accent),#38bdf8);}
.cbar-cnt{font-size:12px;color:var(--sub);min-width:36px;text-align:right;font-weight:600;}
.summary-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px;}
.summary-card{background:var(--bg);border:1px solid var(--border);border-radius:10px;padding:16px 18px;}
.summary-card-hd{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;}
.summary-name{font-size:14px;font-weight:700;}
.summary-cnt{background:var(--accent);color:#fff;font-size:11px;font-weight:700;padding:2px 8px;border-radius:10px;}
.direction-chips{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px;}
.direction-chip{background:var(--white);color:var(--sub);font-size:11px;padding:3px 10px;
  border-radius:999px;border:1px solid var(--border);}
.rep-tech{list-style:none;display:flex;flex-direction:column;gap:4px;}
.rep-tech li{font-size:12px;color:var(--text);padding-left:12px;position:relative;line-height:1.5;}
.rep-tech li::before{content:'';position:absolute;left:0;top:7px;width:5px;height:5px;
  border-radius:50%;background:var(--accent);}

.company-section{margin-bottom:32px;}
.company-section-title{font-size:15px;font-weight:700;color:var(--text);
  margin-bottom:16px;display:flex;align-items:center;gap:8px;
  padding:10px 0 12px;border-bottom:2px solid var(--accent);}
.company-dot{width:10px;height:10px;border-radius:50%;flex-shrink:0;}
.company-cnt-badge{background:var(--accent);color:#fff;font-size:11px;font-weight:700;padding:2px 8px;border-radius:10px;}
.branch-group{margin-bottom:20px;}
.branch-label{font-size:12px;font-weight:600;color:var(--sub);text-transform:uppercase;
  letter-spacing:.06em;margin-bottom:10px;display:flex;align-items:center;gap:8px;}
.branch-label::after{content:'';flex:1;height:1px;background:var(--border);}
.patent-card{background:var(--white);border:1px solid var(--border);border-radius:10px;
  overflow:hidden;margin-bottom:12px;box-shadow:0 1px 3px rgba(0,0,0,.04);}
.patent-card-hd{display:flex;align-items:center;gap:10px;padding:10px 16px;
  background:#f0f5ff;border-bottom:1px solid #dbeafe;flex-wrap:wrap;}
.pn-badge{display:inline-flex;align-items:center;gap:4px;background:#dbeafe;color:#1e3a8a;
  font-size:11px;font-weight:700;padding:3px 10px;border-radius:6px;
  font-family:'SF Mono',monospace;text-decoration:none;border:1px solid #93c5fd;}
.pn-badge:hover{background:#bfdbfe;}
.status{display:inline-flex;align-items:center;gap:4px;font-size:10px;font-weight:700;padding:2px 8px;border-radius:12px;}
.status.granted{background:rgba(22,163,74,.12);color:#15803d;}
.status.pending{background:rgba(217,119,6,.12);color:#b45309;}
.status.expired{background:rgba(220,38,38,.12);color:#b91c1c;}
.status.other{background:rgba(100,116,139,.1);color:#475569;}
.patent-tag{font-size:11px;padding:2px 10px;border-radius:999px;border:1px solid var(--border);
  color:var(--sub);background:var(--bg);}
.patent-tag.assignee{border-color:#9334e6;color:#7b1fa2;background:#f3e8fd;}
.patent-tag.apdt{border-color:var(--accent);color:#1557b0;background:#e8f0fe;}
.patent-tag.pbdt{border-color:#00897b;color:#00695c;background:#e0f2f1;}
.patent-card-body{display:flex;gap:0;}
.patent-fields{flex:1;min-width:0;padding:14px 18px;display:flex;flex-direction:column;gap:10px;}
.p-title{font-size:13px;font-weight:600;color:var(--text);line-height:1.5;}
.p-meta{display:flex;flex-wrap:wrap;gap:12px;font-size:12px;color:var(--sub);}
.p-meta span b{color:var(--text);}
.field{display:flex;flex-direction:column;gap:3px;}
.field-lbl{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;
  color:#fff;padding:1px 7px;border-radius:3px;display:inline-block;width:fit-content;}
.lbl-problem{background:#dc2626;}.lbl-approach{background:#16a34a;}.lbl-benefit{background:#d97706;}
.field-val{font-size:12.5px;color:var(--text);line-height:1.7;}
.patent-fig{flex-shrink:0;width:180px;background:linear-gradient(160deg,#f0f4ff,#e0eaff);
  border-left:1px solid var(--border);padding:14px;display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:6px;}
.patent-fig img{width:100%;height:auto;border-radius:6px;box-shadow:0 2px 6px rgba(0,0,0,.1);}
.fig-cap{font-size:10px;font-weight:600;color:var(--accent);text-transform:uppercase;letter-spacing:.04em;}

.lit-card{background:var(--white);border:1px solid var(--border);border-radius:10px;
  margin-bottom:16px;box-shadow:0 1px 3px rgba(0,0,0,.04);overflow:hidden;padding:20px 24px;}
.lit-card:hover{box-shadow:0 2px 8px rgba(0,0,0,.08);}
.lit-idx{font-size:11px;font-weight:700;color:var(--sub);margin-bottom:6px;letter-spacing:.04em;}
.lit-title{font-size:14px;font-weight:700;color:var(--text);line-height:1.55;margin-bottom:8px;}
.lit-title a{color:var(--accent2);text-decoration:none;}
.lit-title a:hover{text-decoration:underline;}
.lit-authors{font-size:12px;color:var(--sub);margin-bottom:4px;line-height:1.5;}
.lit-journal{font-size:12px;color:var(--sub);font-style:italic;margin-bottom:12px;}
.lit-journal b{font-style:normal;font-weight:600;color:var(--text);}
.lit-abstract{font-size:12.5px;color:#374151;line-height:1.8;margin-bottom:14px;
  padding:12px 14px;background:var(--bg);border-radius:6px;border-left:3px solid var(--border);}
.lit-abstract-toggle{font-size:11px;color:var(--accent);cursor:pointer;margin-left:6px;
  background:none;border:none;padding:0;text-decoration:underline;}
.lit-abstract-full{display:none;}
.lit-abstract-full.open{display:inline;}
.lit-meta{display:flex;flex-wrap:wrap;gap:8px;align-items:center;padding-top:12px;
  border-top:1px solid var(--border);}
.lit-doi{font-size:11px;color:var(--accent);text-decoration:none;
  display:inline-flex;align-items:center;gap:4px;}
.lit-doi:hover{text-decoration:underline;}
.lit-cite{font-size:11px;padding:2px 10px;border-radius:999px;
  border:1px solid #fcd34d;color:#92400e;background:#fffbeb;}
.lit-ai-box{margin-top:24px;background:linear-gradient(135deg,#eff6ff 0%,#f0fdf4 100%);
  border:1px solid #bfdbfe;border-radius:10px;padding:20px 24px;}
.lit-ai-box h4{font-size:13px;font-weight:700;color:var(--accent2);margin:0 0 12px;
  display:flex;align-items:center;gap:6px;}
.lit-ai-content{font-size:13px;color:#1e293b;line-height:1.85;}
.lit-ai-content strong,.lit-ai-content b{color:var(--accent2);}
.lit-ai-content h3,.lit-ai-content h4{font-size:13px;font-weight:700;color:var(--text);
  margin:14px 0 6px;}
.lit-ai-ref{color:var(--accent);font-weight:700;text-decoration:none;
  background:#dbeafe;border-radius:4px;padding:0 4px;}
.lit-ai-ref:hover{background:#bfdbfe;}
.footer{text-align:center;padding:32px;color:var(--sub);font-size:12px;
  border-top:1px solid var(--border);margin-top:20px;}
@media(max-width:768px){
  #sidebar{transform:translateX(-100%);transition:transform .3s;}
  #sidebar.open{transform:translateX(0);}
  #main{margin-left:0;padding:20px 16px 60px;}
  .patent-card-body{flex-direction:column;}
  .patent-fig{width:100%;border-left:none;border-top:1px solid var(--border);}
}
"""

JS = """
function toggleAbs(idx) {
  const el = document.getElementById('abs-' + idx);
  const btn = el.nextElementSibling;
  if (el.classList.contains('open')) {
    el.classList.remove('open');
    btn.textContent = '展开';
  } else {
    el.classList.add('open');
    btn.textContent = '收起';
  }
}
const links = document.querySelectorAll('#sidebar a');
const observer = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if(e.isIntersecting){
      links.forEach(l=>l.classList.remove('active'));
      const a = document.querySelector('#sidebar a[href="#'+e.target.id+'"]');
      if(a) a.classList.add('active');
    }
  });
}, {threshold:0.3});
document.querySelectorAll('[id]').forEach(el=>observer.observe(el));
"""


def legal_tag(status):
    s = status or ""
    if "授权" in s or "Granted" in s.lower():
        return f'<span class="patent-tag granted">{s}</span>'
    if "审查" in s or "Pending" in s.lower() or "公布" in s:
        return f'<span class="patent-tag pending">{s}</span>'
    if "PCT" in s:
        return f'<span class="patent-tag pct">{s}</span>'
    return f'<span class="patent-tag">{s}</span>'


def parse_md(md_text):
    """单遍状态机解析报告 Markdown。"""
    lines = md_text.splitlines()

    title = ""
    gen_time = ""
    query = ""
    total = 0
    company_counts = {}
    summaries = {}       # {company: {directions, rep_techs}}
    details = {}         # {company: {branch: [patent_dict]}}
    literature = []      # [{title, authors, publication, doi, citation, abstract}]
    lit_query = ""
    lit_total = 0
    lit_ai_summary = []  # lines of AI summary block

    # 状态：None / "summary" / "detail" / "literature" / "lit_ai"
    section = None
    cur_company = None
    cur_branch = None
    cur_patent = None
    cur_lit = None

    def flush_patent():
        if cur_patent and cur_company and cur_branch is not None:
            details.setdefault(cur_company, {}).setdefault(cur_branch, []).append(cur_patent)

    def flush_lit():
        if cur_lit:
            literature.append(cur_lit)

    for line in lines:
        # ── 顶级标题 ──
        if re.match(r'^# ', line) and not title:
            title = line[2:].strip()
            continue

        # ── 生成时间 ──
        m = re.match(r'>\s*生成时间[：:]\s*(.+)', line)
        if m:
            gen_time = m.group(1).strip()
            continue

        # ── Section 切换 ──
        if re.match(r'^## [一二三四五]', line):
            if '一' in line[:6]:
                section = "overview"
            elif '二' in line[:6]:
                section = "summary"
            elif '三' in line[:6]:
                section = "detail"
            elif '四' in line[:6]:
                flush_patent(); cur_patent = None
                section = "literature"
            cur_company = cur_branch = cur_patent = None
            continue

        # ── 概况 section ──
        if section == "overview":
            m = re.match(r'-\s*\*\*检索式\*\*[：:]\s*`(.+)`', line)
            if m: query = m.group(1).strip(); continue
            m = re.match(r'-\s*\*\*专利总数\*\*[：:]\s*(\d+)', line)
            if m: total = int(m.group(1)); continue
            m = re.match(r'\|\s*(.+?)\s*\|\s*(\d+)\s*\|', line)
            if m and m.group(1).strip() not in ("公司", "---", ":---"):
                company_counts[m.group(1).strip()] = int(m.group(2))
            continue

        # ── 技术总结 section ──
        if section == "summary":
            m = re.match(r'^### (.+?)（\d+\s*件）', line)
            if m:
                cur_company = m.group(1).strip()
                summaries[cur_company] = {"directions": [], "rep_techs": []}
                continue
            if cur_company:
                m = re.match(r'-\s*\*\*主要技术方向\*\*[：:]\s*(.+)', line)
                if m:
                    for part in re.split(r'[、，,]', m.group(1)):
                        part = part.strip()
                        nm = re.match(r'(.+?)（(\d+)件）', part)
                        if nm:
                            summaries[cur_company]["directions"].append({"name": nm.group(1), "count": nm.group(2)})
                        elif part:
                            summaries[cur_company]["directions"].append({"name": part, "count": ""})
                    continue
                m = re.match(r'-\s*\*\*代表性技术\*\*[：:]\s*(.+)', line)
                if m:
                    summaries[cur_company]["rep_techs"].append(m.group(1).strip())
                    continue
            continue

        # ── 专利详情 section ──
        if section == "detail":
            # 公司标题 ### (exactly 3 #)
            m = re.match(r'^### (.+?)（\d+\s*件）', line)
            if m and not line.startswith('####'):
                flush_patent(); cur_patent = None
                cur_company = m.group(1).strip()
                cur_branch = None
                details.setdefault(cur_company, {})
                continue

            # 技术分支 #### (exactly 4 #)
            m = re.match(r'^#### (.+?)（\d+\s*件）', line)
            if m and not line.startswith('#####') and cur_company:
                flush_patent(); cur_patent = None
                cur_branch = m.group(1).strip()
                details[cur_company].setdefault(cur_branch, [])
                continue

            # 专利条目 ##### (exactly 5 #)
            m = re.match(r'^##### \[(.+?)\]\((.+?)\)', line)
            if m and cur_company and cur_branch is not None:
                flush_patent()
                cur_patent = {"pn": m.group(1), "url": m.group(2),
                              "title": "", "legal": "", "assignee": "",
                              "apdt": "", "pbdt": "",
                              "problem": "", "approach": "", "benefit": "", "fig": ""}
                continue

            if cur_patent:
                for key, label in [("title","标题"),("legal","法律状态"),("assignee","申请人"),
                                    ("apdt","申请日"),("pbdt","公开日"),("problem","技术问题"),
                                    ("approach","技术手段"),("benefit","技术功效")]:
                    m = re.match(rf'-\s*\*\*{label}\*\*[：:]\s*(.+)', line)
                    if m: cur_patent[key] = m.group(1).strip(); break
                fm = re.match(r'-\s*\*\*摘要附图\*\*[：:].*!\[.+?\]\((.+)\)', line)
                if fm: cur_patent["fig"] = fm.group(1)

        # ── 期刊文献 section ──
        if section == "literature":
            m = re.match(r'-\s*\*\*文献检索式\*\*[：:]\s*`(.+)`', line)
            if m: lit_query = m.group(1).strip(); continue
            m = re.match(r'-\s*\*\*命中文献数\*\*[：:]\s*(\d+)', line)
            if m: lit_total = int(m.group(1)); continue
            # AI 总结子节
            if re.match(r'^### AI 文献总结', line):
                flush_lit(); cur_lit = None
                section = "lit_ai"
                continue
            m = re.match(r'^### \d+\.\s+(.+)', line)
            if m:
                flush_lit()
                cur_lit = {"title": m.group(1).strip(), "authors": "", "publication": "", "doi": "", "doi_url": "", "citation": "", "abstract": ""}
                continue
            if cur_lit:
                m = re.match(r'-\s*\*\*作者\*\*[：:]\s*(.+)', line)
                if m: cur_lit["authors"] = m.group(1).strip(); continue
                m = re.match(r'-\s*\*\*期刊\*\*[：:]\s*(.+)', line)
                if m: cur_lit["publication"] = m.group(1).strip(); continue
                m = re.match(r'-\s*\*\*DOI\*\*[：:]\s*\[(.+?)\]\((.+?)\)', line)
                if m: cur_lit["doi"] = m.group(1).strip(); cur_lit["doi_url"] = m.group(2).strip(); continue
                m = re.match(r'-\s*\*\*DOI\*\*[：:]\s*(.+)', line)
                if m: cur_lit["doi"] = m.group(1).strip(); continue
                m = re.match(r'-\s*\*\*引用次数\*\*[：:]\s*(.+)', line)
                if m: cur_lit["citation"] = m.group(1).strip(); continue
                m = re.match(r'-\s*\*\*摘要\*\*[：:]\s*(.+)', line)
                if m: cur_lit["abstract"] = m.group(1).strip(); continue

        # ── AI 文献总结 section ──
        if section == "lit_ai":
            lit_ai_summary.append(line)

    flush_patent()
    flush_lit()

    return {
        "title": title, "gen_time": gen_time, "query": query,
        "total": total, "company_counts": company_counts,
        "summaries": summaries, "details": details,
        "literature": literature, "lit_query": lit_query, "lit_total": lit_total,
        "lit_ai_summary": "\n".join(lit_ai_summary).strip(),
    }


def company_color(name):
    if "宁德" in name or "CATL" in name or "CONTEMPORARY" in name:
        return "#1A73E8", "catl"
    if "比亚迪" in name or "BYD" in name:
        return "#34A853", "byd"
    return "#9AA0A6", "other"


def render_html(data):
    title = data["title"] or "专利分析报告"
    gen_time = data["gen_time"]
    query = data["query"]
    total = data["total"]
    company_counts = data["company_counts"]
    summaries = data["summaries"]
    details = data["details"]
    literature = data.get("literature", [])
    lit_query = data.get("lit_query", "")
    lit_total = data.get("lit_total", 0)
    lit_ai_summary = data.get("lit_ai_summary", "")

    # 只保留有名字的公司（排除"其他"），专利总数用 details 实际数量
    named_companies = {k: v for k, v in company_counts.items() if k != "其他"}
    real_total = sum(named_companies.values())

    # ── 侧边栏 ──
    sidebar_company_links = ""
    for ci, (cname, branches) in enumerate(details.items()):
        sidebar_company_links += f'<div class="nav-sub"><a href="#company-{ci}">{cname}</a></div>\n'
        for bi, branch in enumerate(branches.keys()):
            sidebar_company_links += f'<div class="nav-assignee"><a href="#branch-{ci}-{bi}">{branch}</a></div>\n'

    lit_nav = ""
    if literature:
        lit_ai_nav = '<div class="nav-sub"><a href="#lit-ai-box">🤖 AI 文献总结</a></div>' if lit_ai_summary else ""
        lit_nav = f'<a href="#sec4" class="nav-part">📄 相关期刊文献</a>{lit_ai_nav}<div class="nav-sub"><a href="#lit-detail">📑 文献详情</a></div>'

    sidebar = f"""
<div id="sidebar">
  <div id="sidebar-logo"><h2>技术情报报告</h2><p>{title}</p></div>
  <nav>
    <a href="#sec1" class="nav-part">📊 新公开专利概况</a>
    <a href="#sec2" class="nav-part">🏢 专利技术总结</a>
    <a href="#sec3" class="nav-part">📋 专利详情</a>
    {sidebar_company_links}
    {lit_nav}
  </nav>
</div>"""

    # ── Hero header ──
    num_companies = len(named_companies)
    num_branches = sum(len(b) for b in details.values())

    hero = f"""
<div class="hero">
  <div class="hero-dots"></div>
  <div class="hero-inner">
    <div class="hero-badge">技术情报报告</div>
    <h1>{title}</h1>
    <div class="hero-meta">生成时间：{gen_time}</div>
    <div class="hero-stats">
      <div class="hero-stat"><div class="hero-stat-num">{real_total}</div><div class="hero-stat-label">专利总数</div></div>
      <div class="hero-stat"><div class="hero-stat-num">{num_companies}</div><div class="hero-stat-label">分析公司</div></div>
      <div class="hero-stat"><div class="hero-stat-num">{num_branches}</div><div class="hero-stat-label">技术方向</div></div>
    </div>
  </div>
</div>"""

    # ── 一、概况 ──
    max_cnt = max(named_companies.values()) if named_companies else 1
    cbar_rows = ""
    for cname, cnt in named_companies.items():
        pct = int(cnt / max_cnt * 100)
        cbar_rows += f"""<div class="cbar"><div class="cbar-name">{cname}</div><div class="cbar-track"><div class="cbar-fill" style="width:{pct}%"></div></div><div class="cbar-cnt">{cnt}</div></div>"""

    section1 = f"""
<div class="section" id="sec1">
  <div class="section-hd">
    <div class="section-icon">📊</div>
    <div class="section-title">新公开专利概况</div>
  </div>
  <div class="section-bd">
    <div class="company-bars">{cbar_rows}</div>
  </div>
</div>"""

    # ── 二、技术总结 ──
    summary_cards = ""
    for cname, info in summaries.items():
        color, _ = company_color(cname)
        chips = "".join(
            f'<span class="direction-chip">{d["name"]}{"（" + d["count"] + "件）" if d["count"] else ""}</span>'
            for d in info["directions"]
        )
        techs = "".join(f"<li>{t}</li>" for t in info["rep_techs"])
        cnt = sum(int(d["count"]) for d in info["directions"] if d["count"])
        summary_cards += f"""
<div class="summary-card">
  <div class="summary-card-hd">
    <div class="summary-name" style="color:{color}">{cname}</div>
    <span class="summary-cnt">{cnt} 件</span>
  </div>
  <div class="direction-chips">{chips}</div>
  <ul class="rep-tech">{techs}</ul>
</div>"""

    section2 = f"""
<div class="section" id="sec2">
  <div class="section-hd">
    <div class="section-icon">🏢</div>
    <div class="section-title">专利技术总结</div>
  </div>
  <div class="section-bd">
    <div class="summary-grid">{summary_cards}</div>
  </div>
</div>"""

    # ── 三、专利详情 ──
    detail_html = ""
    for ci, (cname, branches) in enumerate(details.items()):
        color, _ = company_color(cname)
        total_c = sum(len(v) for v in branches.values())
        branch_html = ""
        for bi, (branch, patents) in enumerate(branches.items()):
            cards = ""
            for p in patents:
                assignee_clean = p["assignee"].replace("|", " · ")

                # status badge
                legal = p.get("legal", "")
                if "授权" in legal or "Granted" in legal.lower():
                    status_cls = "granted"
                elif "审查" in legal or "Pending" in legal.lower() or "公布" in legal:
                    status_cls = "pending"
                else:
                    status_cls = "other"

                # fields
                fields_html = ""
                for key, label, lbl_cls in [("problem","技术问题","lbl-problem"),("approach","技术手段","lbl-approach"),("benefit","技术功效","lbl-benefit")]:
                    if p.get(key):
                        fields_html += f'<div class="field"><div class="field-lbl {lbl_cls}">{label}</div><div class="field-val">{p[key]}</div></div>'

                fig_html = ""
                if p.get("fig"):
                    fig_html = f'<div class="patent-fig"><img src="{p["fig"]}" alt="{p["pn"]}" loading="lazy"/><div class="fig-cap">摘要附图</div></div>'

                cards += f"""<div class="patent-card">
  <div class="patent-card-hd">
    <a class="pn-badge" href="{p['url']}" target="_blank">{p['pn']}</a>
    <span class="status {status_cls}">{legal}</span>
    <span class="patent-tag assignee">{assignee_clean}</span>
    <span class="patent-tag apdt">申请 {p['apdt']}</span>
    <span class="patent-tag pbdt">公开 {p['pbdt']}</span>
  </div>
  <div class="patent-card-body">
    <div class="patent-fields">
      <div class="p-title">{p['title']}</div>
      {fields_html}
    </div>
    {fig_html}
  </div>
</div>"""

            branch_html += f"""
<div class="branch-group">
  <div class="branch-label" id="branch-{ci}-{bi}">{branch}（{len(patents)} 件）</div>
  {cards}
</div>"""

        detail_html += f"""
<div class="company-section">
  <div class="company-section-title" id="company-{ci}">
    <span class="company-dot" style="background:{color}"></span>
    {cname}
    <span class="company-cnt-badge">{total_c} 件</span>
  </div>
  {branch_html}
</div>"""

    section3 = f"""
<div class="section" id="sec3">
  <div class="section-hd">
    <div class="section-icon">📋</div>
    <div class="section-title">专利详情</div>
  </div>
  <div class="section-bd">
    {detail_html}
  </div>
</div>"""

    # ── 四、期刊文献 ──
    section4 = ""
    if literature:
        lit_cards = ""
        for idx, lit in enumerate(literature, 1):
            if lit.get("doi_url"):
                title_html = f'<a href="{lit["doi_url"]}" target="_blank">{lit["title"]}</a>'
            else:
                search_url = "https://scholar.google.com/scholar?q=" + urllib.parse.quote(lit["title"])
                title_html = f'<a href="{search_url}" target="_blank">{lit["title"]}</a>'

            authors_html = f'<div class="lit-authors">{lit["authors"]}</div>' if lit.get("authors") else ""
            journal_html = f'<div class="lit-journal"><b>{lit["publication"]}</b></div>' if lit.get("publication") else ""
            abstract = lit.get("abstract", "")
            if abstract:
                if len(abstract) <= 300:
                    abstract_html = f'<div class="lit-abstract">{abstract}</div>'
                else:
                    preview = abstract[:300]
                    rest = abstract[300:]
                    abstract_html = f'<div class="lit-abstract">{preview}<span class="lit-abstract-full" id="abs-{idx}">{rest}</span><button class="lit-abstract-toggle" onclick="toggleAbs({idx})">展开</button></div>'
            else:
                abstract_html = ""

            meta_items = ""
            if lit.get("doi_url"):
                meta_items += f'<a class="lit-doi" href="{lit["doi_url"]}" target="_blank">🔗 DOI: {lit["doi"]}</a>'
            elif lit.get("doi"):
                meta_items += f'<span class="lit-doi">DOI: {lit["doi"]}</span>'
            if lit.get("citation"):
                for part in lit["citation"].split("、"):
                    meta_items += f'<span class="lit-cite">{part.strip()}</span>'

            lit_cards += f"""
<div class="lit-card" id="lit-{idx}">
  <div class="lit-idx">{idx}</div>
  <div class="lit-title">{title_html}</div>
  {authors_html}
  {journal_html}
  {abstract_html}
  <div class="lit-meta">{meta_items}</div>
</div>"""

        # AI 总结块
        ai_box_html = ""
        if lit_ai_summary:
            # 将 Markdown 粗体/标题简单转为 HTML，**[N]** 转为锚点链接
            ai_html_lines = []
            for ln in lit_ai_summary.splitlines():
                # **[N]** → 带锚点的链接，必须在通用粗体替换之前处理
                ln_h = re.sub(r'\*\*\[(\d+)\]\*\*', lambda m: f'<a class="lit-ai-ref" href="#lit-{m.group(1)}">[{m.group(1)}]</a>', ln)
                ln_h = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', ln_h)
                if re.match(r'^### ', ln_h):
                    ln_h = f'<h3>{ln_h[4:].strip()}</h3>'
                elif re.match(r'^## ', ln_h):
                    ln_h = f'<h3>{ln_h[3:].strip()}</h3>'
                else:
                    ln_h = ln_h + '<br>'
                ai_html_lines.append(ln_h)
            ai_box_html = f"""<div class="lit-ai-box" id="lit-ai-box">
  <h4>🤖 AI 文献总结</h4>
  <div class="lit-ai-content">{"".join(ai_html_lines)}</div>
</div>"""

        section4 = f"""
<div class="section" id="sec4">
  <div class="section-hd">
    <div class="section-icon">📄</div>
    <div class="section-title">相关期刊文献（{lit_total} 条命中，展示前 {len(literature)} 条）</div>
  </div>
  <div class="section-bd">
    {ai_box_html}
    <div id="lit-detail">{lit_cards}</div>
  </div>
</div>"""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>{STYLE}</style>
</head>
<body>
{sidebar}
<div id="main">
{hero}
{section1}
{section2}
{section3}
{section4}
<div class="footer">技术情报报告 · {gen_time}</div>
</div>
<script>{JS}</script>
</body>
</html>"""


def main():
    if len(sys.argv) < 2:
        print("用法: render_html.py <report.md>", file=sys.stderr)
        sys.exit(1)
    md_path = Path(sys.argv[1])
    if not md_path.exists():
        print(f"文件不存在: {md_path}", file=sys.stderr)
        sys.exit(1)
    md_text = md_path.read_text(encoding="utf-8")
    data = parse_md(md_text)
    html = render_html(data)
    out_path = md_path.with_suffix(".html")
    out_path.write_text(html, encoding="utf-8")
    print(str(out_path))


if __name__ == "__main__":
    main()

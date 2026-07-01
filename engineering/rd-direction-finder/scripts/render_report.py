#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Html报告渲染脚本
输入：一个 payload JSON 文件，结构见 references/report_payload.md
输出：一份自包含 HTML 报告。

# 路径定义见 [assets/paths.md](assets/paths.md),$MD_PATH,$PAYLOAD_PATH 为输入路径，$HTML_PATH 为输出路径。

Usage:
    python3 scripts/render_report.py --payload "$PAYLOAD_PATH" --output "$HTML_PATH"

关键约定：
- ../SKILL.md  Step 4 / Step 5
- ../assets/report-template.md
"""

import argparse
import html as _html
import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

import mistune


def esc(s: Any) -> str:
    if s is None:
        return ""
    return _html.escape(str(s), quote=True)


def _cite_label(sid: Any) -> str:
    if sid is None:
        return ""
    return str(sid).strip().strip("[]").strip()


def cite_tag(sid: Any) -> str:
    label = _cite_label(sid)
    if not label:
        return ""
    return f'<span class="cite-tag">{esc(label)}</span>'


def render_cites(cites: Optional[Iterable[Any]]) -> str:
    if not cites:
        return ""
    if isinstance(cites, (str, int)):
        cites = [cites]
    parts = [cite_tag(c) for c in cites if c]
    parts = [p for p in parts if p]
    return (" " + " ".join(parts)) if parts else ""


def status_span(s: Any) -> str:
    if not s:
        return ""
    t = str(s).strip()
    if t == "有效":
        return f'<span class="status-active">{esc(t)}</span>'
    if t in ("已失效", "失效"):
        return f'<span class="status-inactive">{esc(t)}</span>'
    if t in ("申请中", "实质审查"):
        return f'<span class="status-pending">{esc(t)}</span>'
    return esc(t)


def link(title: Any, url: Any) -> str:
    t = esc(title) if title else (esc(url) if url else "")
    if not url:
        return t
    return f'<a href="{esc(url)}" target="_blank" rel="noopener">{t}</a>'


def _get(d: Any, *path: str, default: Any = "") -> Any:
    cur = d
    for k in path:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(k)
        if cur is None:
            return default
    return cur if cur is not None else default


def _list(d: Any, *path: str) -> List[Any]:
    v = _get(d, *path, default=None)
    if isinstance(v, list):
        return v
    return []


def first_value(*values: Any) -> Any:
    for value in values:
        if value is None:
            continue
        if isinstance(value, (int, float)):
            return value
        if isinstance(value, str):
            if value.strip():
                return value.strip()
            continue
        if value:
            return value
    return ""


def parse_labeled_text(text: Any, labels: Sequence[str]) -> Dict[str, str]:
    raw = md_text(text)
    if not raw:
        return {}
    normalized = re.sub(r"(?i)<br\s*/?>", "\n", raw)
    label_alt = "|".join(re.escape(label) for label in labels)
    pattern = re.compile(rf"(?P<label>{label_alt})\s*[：:]\s*", re.M)
    matches = list(pattern.finditer(normalized))
    if not matches:
        return {}
    parsed: Dict[str, str] = {}
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(normalized)
        parsed[match.group("label")] = normalized[start:end].strip(" \n;；")
    return parsed


def legacy_analysis_rows(payload: Dict[str, Any]) -> Dict[str, str]:
    rows = first_value(
        _get(payload, "step0_analysis", default=None),
        _get(payload, "analysis_rows", default=None),
        _get(payload, "dimensions", default=None),
    )
    found = {"demand": "", "bottleneck": "", "solution": ""}
    if not isinstance(rows, list):
        return found
    for row in rows:
        dim = md_text(first_value(_get(row, "dim"), _get(row, "dimension"), _get(row, "title")))
        content = md_text(first_value(_get(row, "content"), _get(row, "text"), _get(row, "value")))
        if "需求牵引" in dim:
            found["demand"] = content
        elif "瓶颈分析" in dim:
            found["bottleneck"] = content
        elif "解决思路" in dim:
            found["solution"] = content
    return found


def normalize_analysis(payload: Dict[str, Any]) -> Dict[str, Any]:
    current = _get(payload, "analysis") or {}
    legacy = _get(payload, "requirement_analysis") or {}
    rows = legacy_analysis_rows(payload)

    demand_row = parse_labeled_text(rows["demand"], ["场景", "痛点", "当前应对"])
    bottleneck_row = parse_labeled_text(rows["bottleneck"], ["瓶颈", "现有措施局限", "现有措施局限性", "原理局限"])
    solution_row = parse_labeled_text(rows["solution"], ["技术路径", "系统方案", "工程兼容性", "锁定目标"])

    demand = _get(current, "demand") or {}
    old_demand = _get(legacy, "need_traction") or {}
    bottleneck = _get(current, "bottleneck") or {}
    old_bottleneck = _get(legacy, "bottleneck") or {}
    solution = _get(current, "solution") or {}
    old_solution = _get(legacy, "solution") or {}

    return {
        "demand": {
            "scene": first_value(_get(demand, "scene"), _get(old_demand, "scene"), demand_row.get("场景")),
            "pain": first_value(_get(demand, "pain"), _get(old_demand, "pain_point"), _get(old_demand, "pain"), demand_row.get("痛点")),
            "current": first_value(_get(demand, "current"), _get(old_demand, "current_response"), _get(old_demand, "current"), demand_row.get("当前应对")),
        },
        "bottleneck": {
            "limit": first_value(_get(bottleneck, "limit"), _get(old_bottleneck, "bottleneck"), _get(old_bottleneck, "limit"), bottleneck_row.get("瓶颈")),
            "cost": first_value(_get(bottleneck, "cost"), _get(old_bottleneck, "current_limit"), _get(old_bottleneck, "cost"), bottleneck_row.get("现有措施局限"), bottleneck_row.get("现有措施局限性")),
            "principle": first_value(_get(bottleneck, "principle"), _get(old_bottleneck, "principle_limit"), _get(old_bottleneck, "principle"), bottleneck_row.get("原理局限")),
        },
        "solution": {
            "path": first_value(_get(solution, "path"), _get(old_solution, "tech_path"), _get(old_solution, "path"), solution_row.get("技术路径")),
            "system": first_value(_get(solution, "system"), _get(old_solution, "system_plan"), _get(old_solution, "system"), solution_row.get("系统方案")),
            "compat": first_value(_get(solution, "compat"), _get(old_solution, "compatibility"), _get(old_solution, "compat"), solution_row.get("工程兼容性")),
            "target": first_value(_get(solution, "target"), _get(old_solution, "lock_target"), _get(old_solution, "target"), solution_row.get("锁定目标")),
        },
    }


def normalize_evidence_item(item: Dict[str, Any], kind: str, direction: str = "", sid: str = "") -> Dict[str, Any]:
    if kind == "case":
        return {
            "no": first_value(_get(item, "no")),
            "src": first_value(_get(item, "src"), _get(item, "source")),
            "year": first_value(_get(item, "year")),
            "publisher": first_value(_get(item, "publisher"), _get(item, "org")),
            "title": first_value(_get(item, "title")),
            "url": first_value(_get(item, "url")),
            "summary": first_value(_get(item, "summary"), _get(item, "content"), _get(item, "note")),
            "grade": first_value(_get(item, "grade"), _get(item, "level")),
            "sid": first_value(_get(item, "sid"), sid),
            "direction": direction,
        }
    if kind == "paper":
        return {
            "src": first_value(_get(item, "src"), _get(item, "source")),
            "year": first_value(_get(item, "year")),
            "affiliation": first_value(_get(item, "affiliation"), _get(item, "author")),
            "title": first_value(_get(item, "title")),
            "url": first_value(_get(item, "url")),
            "cited_by": first_value(_get(item, "cited_by"), _get(item, "citations"), _get(item, "cited")),
            "doi": first_value(_get(item, "doi")),
            "sid": first_value(_get(item, "sid"), sid),
            "direction": direction,
        }
    if kind == "patent":
        return {
            "src": first_value(_get(item, "src"), _get(item, "source")),
            "pub_no": first_value(_get(item, "pub_no"), _get(item, "pn")),
            "title": first_value(_get(item, "title")),
            "url": first_value(_get(item, "url")),
            "applicant": first_value(_get(item, "applicant"), _get(item, "assignee")),
            "pub_year": first_value(_get(item, "pub_year"), _get(item, "year")),
            "status": first_value(_get(item, "status")),
            "cited_by": first_value(_get(item, "cited_by"), _get(item, "citations"), _get(item, "cited")),
            "sid": first_value(_get(item, "sid"), sid),
            "direction": direction,
        }
    return {
        "site": first_value(_get(item, "site"), _get(item, "src"), _get(item, "source")),
        "title": first_value(_get(item, "title")),
        "url": first_value(_get(item, "url")),
        "summary": first_value(_get(item, "summary"), _get(item, "note"), _get(item, "content")),
        "sid": first_value(_get(item, "sid"), sid),
        "category": first_value(_get(item, "category"), _get(item, "type")),
    }


def normalize_issue(item: Dict[str, Any], idx: int) -> Dict[str, Any]:
    return {
        "no": first_value(_get(item, "no"), _get(item, "id"), _get(item, "code"), f"T{idx + 1}"),
        "name": first_value(_get(item, "name"), _get(item, "title")),
        "desc": first_value(
            _get(item, "desc"),
            _get(item, "description"),
            _get(item, "text"),
            _get(item, "content"),
        ),
    }


def normalize_covers(value: Any, fallback: Any = "") -> Any:
    selected = first_value(value, fallback)
    if isinstance(selected, list):
        return [str(x).strip() for x in selected if str(x).strip()]
    if isinstance(selected, tuple):
        return [str(x).strip() for x in selected if str(x).strip()]
    text = md_text(selected)
    if not text:
        return ""
    parts = [p.strip() for p in re.split(r"[+、,，/\s]+", text) if p.strip()]
    if parts and all(re.fullmatch(r"T\d+", p) for p in parts):
        return parts
    return text


def normalize_direction(item: Dict[str, Any], idx: int, issues: Sequence[Any]) -> Dict[str, Any]:
    fallback_cover = ""
    if idx < len(issues):
        fallback_cover = _get(issues[idx], "no") or f"T{idx + 1}"
    return {
        **item,
        "name": first_value(_get(item, "name"), _get(item, "title"), _get(item, "label")),
        "covers": normalize_covers(
            first_value(
                _get(item, "covers"),
                _get(item, "coverage"),
                _get(item, "challenge_ids"),
                _get(item, "issue_ids"),
                _get(item, "problem_codes"),
                _get(item, "challenges"),
            ),
            fallback_cover,
        ),
        "problem": first_value(_get(item, "problem"), _get(item, "core_problem")),
    }


def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Accept both the current payload schema and earlier rd-direction-finder payloads."""
    out = dict(payload)
    meta = dict(_get(out, "meta") or {})
    meta["project_name"] = first_value(_get(meta, "project_name"), _get(out, "project_name"))
    meta["project_short"] = first_value(_get(meta, "project_short"), _get(out, "project_short"), meta["project_name"])
    meta["applicant"] = first_value(_get(meta, "applicant"), _get(out, "applicant"))
    meta["today_iso"] = first_value(_get(meta, "today_iso"), _get(out, "search_date"))
    meta["scope"] = first_value(_get(meta, "scope"), "专利+论文+网络学术文献补充")
    out["meta"] = meta
    out["requirement_text"] = first_value(_get(out, "requirement_text"), _get(out, "raw_requirement"), _get(meta, "raw_requirement"))
    out["analysis"] = normalize_analysis(out)

    source_issues = _list(out, "issues") or _list(out, "challenges") or _list(out, "step1_problems")
    if source_issues:
        out["issues"] = [normalize_issue(x, i) for i, x in enumerate(source_issues)]

    routes = _list(out, "routes")
    directions = [
        normalize_direction(x, i, _list(out, "issues"))
        for i, x in enumerate(_list(out, "directions") or _list(out, "step1_directions"))
    ]
    if routes:
        normalized_dirs = []
        for idx, route in enumerate(routes):
            base = directions[idx] if idx < len(directions) and isinstance(directions[idx], dict) else {}
            name = first_value(_get(route, "name"), _get(base, "name"))
            evidence = _get(route, "evidence") or {}
            cases = [normalize_evidence_item(x, "case", name) for x in _list(evidence, "cases") or _list(evidence, "engineering_cases")]
            papers = [normalize_evidence_item(x, "paper", name) for x in _list(evidence, "papers")]
            patents = [normalize_evidence_item(x, "patent", name) for x in _list(evidence, "patents")]
            webs = [normalize_evidence_item(x, "web", name) for x in _list(evidence, "webs") or _list(evidence, "web_supplement")]
            normalized_dirs.append({
                "name": name,
                "covers": normalize_covers(first_value(_get(route, "covers"), _get(base, "covers")), _get(base, "covers")),
                "problem": first_value(_get(route, "problem"), _get(route, "core_problem")),
                "contents": _get(route, "contents") or _get(route, "rd_items") or [],
                "target": first_value(_get(route, "target"), _get(route, "tech_target"), _get(route, "goal")),
                "counts": {
                    "case": len(cases),
                    "paper": len(papers),
                    "patent": len(patents),
                    "web": len(webs),
                },
                "hit_extra": _get(route, "hit_extra"),
                "evidence": {"cases": cases, "papers": papers, "patents": patents, "webs": webs},
                "summary_focus": _get(route, "summary_focus"),
                "summary_output": _get(route, "summary_output"),
                "summary_sids": _get(route, "summary_sids") or [],
            })
        out["directions"] = normalized_dirs
    elif directions:
        # Normalize evidence items even when only directions (no routes) are provided
        normalized_dirs = []
        for idx, d in enumerate(directions):
            ev = _get(d, "evidence") or {}
            dir_name = _get(d, "name") or ""
            cases = [normalize_evidence_item(x, "case", dir_name) for x in _list(ev, "cases") or _list(ev, "engineering_cases")]
            papers = [normalize_evidence_item(x, "paper", dir_name) for x in _list(ev, "papers")]
            patents = [normalize_evidence_item(x, "patent", dir_name) for x in _list(ev, "patents")]
            webs = [normalize_evidence_item(x, "web", dir_name) for x in _list(ev, "webs") or _list(ev, "web_supplement")]
            d["evidence"] = {"cases": cases, "papers": papers, "patents": patents, "webs": webs}
            # Normalize contents: handle both dict and string items
            raw_contents = _get(d, "contents") or _get(d, "rd_items") or []
            normalized_contents = []
            for c in raw_contents:
                if isinstance(c, dict):
                    normalized_contents.append({
                        "text": first_value(_get(c, "text"), _get(c, "content")),
                        "cites": _get(c, "cites") or ([_get(c, "sid")] if _get(c, "sid") else []),
                    })
                elif isinstance(c, str):
                    normalized_contents.append(c)
                else:
                    normalized_contents.append(str(c))
            d["contents"] = normalized_contents
            # Ensure counts reflect actual evidence size
            d["counts"] = first_value(
                _get(d, "counts"),
                {"case": len(cases), "paper": len(papers), "patent": len(patents), "web": len(webs)}
            )
            normalized_dirs.append(d)
        out["directions"] = normalized_dirs

    if not _list(out, "units") and _list(out, "orgs"):
        out["units"] = [
            {
                "name": first_value(_get(x, "name"), _get(x, "unit")),
                "covers": first_value(_get(x, "covers"), _get(x, "routes"), _get(x, "covered_routes")),
                "focus": _get(x, "focus"),
                "achievements": "、".join(str(y) for y in _get(x, "achievements")) if isinstance(_get(x, "achievements"), list) else _get(x, "achievements"),
                "cites": _get(x, "cites") or [],
            }
            for x in _list(out, "orgs")
        ]

    app = dict(_get(out, "appendix") or {})
    if not _list(app, "a1") and _list(out, "directions"):
        app["a1"] = []
        app["a2"] = []
        app["a3"] = []
        app["a4"] = []
        case_no = 1
        for direction in _list(out, "directions"):
            ev = _get(direction, "evidence") or {}
            dir_name = _get(direction, "name")
            for item in _list(ev, "cases"):
                row = dict(item)
                row["no"] = first_value(_get(row, "no"), f"C{case_no}")
                row["direction"] = first_value(_get(row, "direction"), dir_name)
                app["a1"].append(row)
                case_no += 1
            for key, target in (("papers", "a2"), ("patents", "a3")):
                for item in _list(ev, key):
                    row = dict(item)
                    row["direction"] = first_value(_get(row, "direction"), dir_name)
                    app[target].append(row)
            for item in _list(ev, "webs"):
                row = dict(item)
                row["category"] = first_value(_get(row, "category"), "期刊论文")
                app["a4"].append(row)
    out["appendix"] = app

    summary = dict(_get(out, "summary") or {})
    summary["cnt_case"] = first_value(_get(summary, "cnt_case"), len(_list(app, "a1")))
    summary["cnt_paper"] = first_value(_get(summary, "cnt_paper"), len(_list(app, "a2")))
    summary["cnt_patent"] = first_value(_get(summary, "cnt_patent"), len(_list(app, "a3")))
    summary["cnt_web"] = first_value(_get(summary, "cnt_web"), len(_list(app, "a4")))
    units = _list(out, "units")
    summary["cnt_org_total"] = first_value(_get(summary, "cnt_org_total"), len({md_text(_get(u, "name")) for u in units if md_text(_get(u, "name"))}))
    summary["cnt_org_top5"] = first_value(_get(summary, "cnt_org_top5"), min(5, len(units)))
    summary["top_orgs"] = first_value(_get(summary, "top_orgs"), "、".join(md_text(_get(u, "name")) for u in units[:3] if md_text(_get(u, "name"))))
    out["summary"] = summary

    return out


CSS = r"""
:root{--primary:#1a5fa8;--primary-light:#e8f0fb;--accent:#e07b39;--success:#2e7d32;--warning:#f57c00;--danger:#c62828;--gray-50:#f9fafb;--gray-100:#f3f4f6;--gray-200:#e5e7eb;--gray-400:#9ca3af;--gray-600:#4b5563;--gray-800:#1f2937;--border-radius:8px;--shadow:0 2px 8px rgba(0,0,0,.08);--shadow-md:0 4px 16px rgba(0,0,0,.12);}
*{box-sizing:border-box;}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;color:#223047;background:#f6f8fb;margin:0;font-size:16px;line-height:1.72;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;}
.container{max-width:1240px;margin:0 auto;padding:0 1.35rem 2.6rem;}
html{scroll-behavior:smooth;}
.report-header{background:linear-gradient(135deg,#1a3a6e 0%,#2563eb 60%,#3b82f6 100%);color:#fff;padding:2.5rem 2rem 2rem;border-radius:0 0 1rem 1rem;}
.report-header h1{margin:0 0 .5rem;font-size:1.75rem;}
.report-header .meta{font-size:.9rem;opacity:.92;}
.report-header .meta span{margin-right:1.5rem;}
.toc{background:#fff;border:1px solid var(--gray-200);border-radius:var(--border-radius);padding:1rem 1.5rem;margin:1.5rem 0;box-shadow:var(--shadow);}
.toc ul{list-style:none;padding:0;margin:0;display:flex;flex-wrap:wrap;gap:.5rem 1.5rem;}
.toc a{color:var(--primary);text-decoration:none;font-weight:500;}
.toc a:hover{text-decoration:underline;}
.demand-block{background:var(--primary-light);border-left:4px solid var(--primary);border-radius:0 var(--border-radius) var(--border-radius) 0;padding:1rem 1.25rem;margin:1.5rem 0;color:var(--gray-800);}
.demand-block .demand-title{font-weight:600;color:var(--primary);margin-bottom:.4rem;}
.section-card{background:#fff;border-radius:var(--border-radius);box-shadow:var(--shadow);margin:1.5rem 0;overflow:hidden;}
.section-header{background:var(--primary);color:#fff;padding:.85rem 1.25rem;font-size:1.15rem;font-weight:600;}
.section-body{padding:1.25rem 1.5rem;}
"""
CSS_PART2 = r"""
.route-card{border:1px solid var(--gray-200);border-radius:var(--border-radius);margin:1rem 0;background:#fff;overflow:hidden;}
.route-header{display:flex;align-items:center;gap:.75rem;padding:.85rem 1.25rem;cursor:pointer;user-select:none;background:var(--gray-50);border-bottom:1px solid var(--gray-200);}
.route-header:hover{background:var(--gray-100);}
.route-header h3{margin:0;font-size:1.05rem;flex:1;color:var(--gray-800);}
.route-header::after{content:"\25BE";color:var(--gray-400);transition:transform .2s;}
.route-card:not(.open) .route-header::after{transform:rotate(-90deg);}
.route-body{padding:1rem 1.25rem;display:none;}
.route-card.open .route-body{display:block;}
.route-badge{display:inline-block;min-width:1.6rem;padding:.15rem .5rem;border-radius:.4rem;color:#fff;font-size:.78rem;font-weight:600;text-align:center;}
.route-badge.r1{background:#2563eb;}
.route-badge.r2{background:#7c3aed;}
.route-badge.r3{background:#16a34a;}
.route-badge.r4{background:#ea580c;}
.route-badge.r5{background:#0891b2;}
.route-badge.r6{background:#dc2626;}
.route-badge.r7{background:#ca8a04;}
.route-badge.r8{background:#4b5563;}
.route-badge.r9{background:#db2777;}
.route-badge.r10{background:#92400e;}
.route-badge.summary{background:#475569;}
.cite-tag{display:inline-block;background:#2563eb;color:#fff;border-radius:.3rem;padding:.05rem .4rem;font-size:.75rem;font-weight:600;margin:0 .1rem;vertical-align:middle;}
.status-active{color:var(--success);font-weight:600;}
.status-inactive{color:var(--danger);font-weight:600;}
.status-pending{color:var(--warning);font-weight:600;}
.src-footer{background:#f8fafc;padding:1.5rem 2rem;margin-top:2rem;border-top:2px solid var(--gray-200);}
.src-footer h2{margin:0 0 .5rem;font-size:1.1rem;color:var(--gray-800);}
.src-grid{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:.75rem;}
.src-chip{display:inline-flex;align-items:center;gap:.3rem;background:#eff6ff;border:1px solid #bfdbfe;border-radius:.5rem;padding:.3rem .75rem;font-size:.8rem;color:#1d4ed8;text-decoration:none;}
.src-chip:hover{background:#dbeafe;}
.src-chip .sid{font-weight:700;}
.unit-row{display:grid;grid-template-columns:1.4fr 1fr 1.6fr 1.6fr;gap:.75rem;padding:.75rem 1rem;border-bottom:1px solid var(--gray-200);align-items:start;}
.unit-row:nth-child(even){background:var(--gray-50);}
.unit-row .unit-name{font-weight:600;color:var(--primary);}
.unit-row.unit-head{background:var(--gray-100);font-weight:600;color:var(--gray-600);}
.tbl-wrap{overflow-x:auto;margin:.75rem 0;border-radius:var(--border-radius);}
table{width:100%;border-collapse:collapse;font-size:.9rem;background:#fff;}
th{background:#1a3a6e;color:#fff;padding:.6rem .75rem;text-align:left;white-space:nowrap;}
td{padding:.5rem .75rem;border-bottom:1px solid var(--gray-200);vertical-align:top;}
tr:nth-child(even) td{background:#f8fafc;}
td a{color:var(--primary);text-decoration:none;}
td a:hover{text-decoration:underline;}
.footer{text-align:center;padding:1.5rem 1rem 2rem;color:var(--gray-400);font-size:.8rem;}
h4.evi-title{margin:1.1rem 0 .4rem;font-size:.98rem;color:var(--gray-600);}
h4.app-title{margin:1.1rem 0 .4rem;font-size:1rem;color:var(--primary);}
p.tight{margin:.4rem 0;}
ul.tight{margin:.4rem 0 .8rem;padding-left:1.4rem;}
ul.tight li{margin:.2rem 0;}
.empty{color:var(--gray-400);font-style:italic;}
@media (max-width:768px){.section-card .section-body{padding:1rem;}.route-card .route-body{padding:1rem;}.unit-row{grid-template-columns:1fr;gap:.25rem;}table{font-size:.85rem;}th,td{padding:.4rem .5rem;}.toc ul{flex-direction:column;gap:.4rem;}}
"""
REPORT_CSS = r"""
.hero-header{background:linear-gradient(120deg,#104da4 0%,#1977cf 100%);color:#fff;padding:2.7rem 0 2.25rem;box-shadow:0 10px 28px rgba(17,83,164,.22);}
.hero-header h1{font-size:2.18rem;line-height:1.18;margin:0 0 1rem;font-weight:800;letter-spacing:0;}
.hero-subtitle{font-size:1.08rem;line-height:1.58;margin:0 0 1.45rem;opacity:.94;max-width:980px;}
.hero-meta{display:flex;flex-wrap:wrap;gap:.7rem 1rem;align-items:center;}
.hero-chip{display:inline-flex;align-items:center;gap:.4rem;background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.18);border-radius:999px;padding:.42rem .85rem;font-size:.92rem;font-weight:700;white-space:nowrap;backdrop-filter:blur(8px);}
.hero-chip span{opacity:.9;}
.report-toc{background:#eaf6ff;border:1px solid #add4f5;border-radius:12px;box-shadow:0 3px 14px rgba(28,86,145,.08);margin:1.65rem 0 1.35rem;padding:1.55rem 1.85rem;}
.report-toc-title{color:#155fa8;font-size:1.24rem;font-weight:800;margin:0 0 1.08rem;line-height:1.3;}
.report-toc-list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.78rem 2.7rem;list-style:none;margin:0;padding:0;}
.report-toc-list li{margin:0;}
.report-toc-list a{display:inline-flex;align-items:center;gap:.45rem;color:#1d63ad;font-size:1.02rem;font-weight:700;text-decoration:none;line-height:1.45;}
.report-toc-list a::before{content:"›";color:#1d63ad;font-size:1.25rem;line-height:1;font-weight:900;}
.report-toc-list a:hover{text-decoration:underline;}
.markdown-report{background:#fff;border:1px solid #e1e8f0;border-radius:12px;box-shadow:0 8px 28px rgba(25,52,86,.08);margin:1.35rem 0 2.4rem;padding:2.25rem 2.5rem;}
.markdown-report h2{font-size:1.42rem;line-height:1.35;color:#163e70;border-bottom:2px solid #dfe8f2;padding-bottom:.55rem;margin:2.05rem 0 1.1rem;scroll-margin-top:1.25rem;}
.markdown-report h2:first-child{margin-top:0;}
.markdown-report > h2:first-child,.markdown-report > h2:first-child + blockquote{display:none;}
.markdown-report h3{font-size:1.12rem;line-height:1.42;color:#1a5fa8;margin:1.5rem 0 .8rem;scroll-margin-top:1.25rem;}
.markdown-report p{margin:.58rem 0;}
.markdown-report blockquote{background:#f0f4ff;border-left:4px solid #2563eb;margin:1rem 0;padding:.8rem 1rem;border-radius:0 8px 8px 0;color:var(--gray-800);}
.markdown-report blockquote p{margin:.35rem 0;}
.markdown-report .requirement-shell{background:#fff;border:1px solid #cfe0ef;border-radius:12px;box-shadow:0 3px 14px rgba(28,86,145,.08);margin:1.25rem 0 1.9rem;padding:1.5rem 1.6rem;}
.markdown-report .requirement-block{background:#f2f7ff;border-left:5px solid #1d63ad;border-radius:8px;margin:0;padding:1.3rem 1.7rem 1.42rem;color:#24344d;}
.markdown-report .requirement-block .requirement-title{font-size:1.1rem;font-weight:800;margin:0 0 .6rem;color:#263a59;}
.markdown-report .requirement-block .requirement-text{font-size:1.03rem;line-height:1.92;font-weight:400;letter-spacing:0;margin:0;white-space:pre-line;color:#203451;}
.markdown-report .summary-card{border:1px solid #bfd7ee;border-radius:10px;background:#fff;box-shadow:0 3px 14px rgba(28,86,145,.09);margin:1.25rem 0 1.75rem;overflow:hidden;}
.markdown-report .summary-card-title{background:#2674c9;color:#fff;font-size:1.05rem;font-weight:800;margin:0;padding:.82rem 1.1rem;border:0;}
.markdown-report .summary-card-body{padding:1.2rem 1.35rem 1.35rem;}
.markdown-report .summary-card-body p{font-size:1rem;line-height:1.84;margin:.35rem 0 .8rem;}
.markdown-report .summary-card-body blockquote{background:#eef7ff;border-left:4px solid #8bc5f3;margin:1rem 0 0;padding:.78rem 1rem;border-radius:0 6px 6px 0;}
.markdown-report .summary-card-body blockquote p{margin:0;color:#334155;}
.markdown-report .route-section-card{border:1px solid #bfd7ee;border-radius:10px;background:#fff;box-shadow:0 3px 14px rgba(28,86,145,.09);margin:1.25rem 0 1.8rem;overflow:hidden;}
.markdown-report .route-section-title{background:#2674c9;color:#fff;font-size:1.05rem;font-weight:800;margin:0;padding:.82rem 1.1rem;border:0;}
.markdown-report .route-section-body{padding:1.2rem 1.35rem 1.35rem;}
.markdown-report .route-section-body p{font-size:1rem;line-height:1.84;margin:.35rem 0 .8rem;}
.markdown-report .route-section-body ul{margin:.45rem 0 1.1rem;}
.markdown-report .route-section-body > table:first-child{margin-top:.35rem;}
.markdown-report table{border-collapse:separate;border-spacing:0;margin:1rem 0 1.55rem;width:100%;background:#fff;border:1px solid #cfe0ef;border-radius:12px;box-shadow:0 3px 12px rgba(15,45,80,.07);overflow:hidden;font-size:.96rem;line-height:1.72;}
.markdown-report thead th{background:#2d7fca;color:#fff;font-size:.98rem;font-weight:700;padding:.95rem 1.05rem;text-align:left;border:0;white-space:nowrap;}
.markdown-report thead th:first-child{border-top-left-radius:11px;}
.markdown-report thead th:last-child{border-top-right-radius:11px;}
.markdown-report tbody td{padding:.95rem 1.05rem;border:0;border-top:1px solid #d7e4f0;color:#1f2937;vertical-align:top;background:#fff;}
.markdown-report tbody tr:nth-child(even) td{background:#f2f7fd;}
.markdown-report tbody tr:first-child td{border-top:0;}
.markdown-report tbody tr:last-child td:first-child{border-bottom-left-radius:11px;}
.markdown-report tbody tr:last-child td:last-child{border-bottom-right-radius:11px;}
.markdown-report tbody td:first-child{width:18%;min-width:8rem;color:#1f67aa;font-weight:700;}
.markdown-report tbody td:first-child strong{display:block;color:#1f67aa;font-size:1.04rem;margin-bottom:.1rem;}
.markdown-report tbody td:first-child strong + br{display:none;}
.markdown-report tbody td:nth-child(2){font-size:1rem;}
.markdown-report tbody td:nth-child(2) strong{color:#111827;font-weight:800;}
.markdown-report .evidence-title{color:#165fa7;font-size:1.12rem;font-weight:800;margin:1.55rem 0 .6rem;}
.markdown-report .evidence-title strong{color:#165fa7;font-weight:800;}
.markdown-report table.evidence-table{border-collapse:collapse;border-spacing:0;border:0;border-radius:0;box-shadow:none;margin:.45rem 0 1.55rem;background:#fff;font-size:.96rem;line-height:1.56;overflow:visible;}
.markdown-report table.evidence-table thead th{background:#e4f4ff;color:#1267b7;border:0;border-bottom:2px solid #88c8f5;padding:.82rem .9rem;font-size:.98rem;font-weight:800;text-align:left;white-space:nowrap;}
.markdown-report table.evidence-table thead th:first-child,.markdown-report table.evidence-table thead th:last-child{border-radius:0;}
.markdown-report table.evidence-table tbody td{background:#fff;border:0;border-bottom:1px solid #d9e4ee;color:#1f2937;padding:.78rem .9rem;font-size:.96rem;font-weight:400;vertical-align:middle;}
.markdown-report table.evidence-table tbody tr:nth-child(even) td{background:#fff;}
.markdown-report table.evidence-table tbody td:first-child{width:auto;min-width:0;color:#1f2937;font-weight:400;}
.markdown-report table.evidence-table tbody td:nth-child(2){font-size:.96rem;}
.markdown-report table.evidence-table a{color:#1d63ad;font-weight:700;text-decoration:none;}
.markdown-report table.evidence-table a:hover{text-decoration:underline;}
.markdown-report table.evidence-table .status-badge{display:inline-block;border-radius:999px;padding:.18rem .55rem;font-size:.84rem;font-weight:800;line-height:1.35;}
.markdown-report table.evidence-table .status-active{background:#e6f7e8;color:#268238;}
.markdown-report table.evidence-table .status-inactive{background:#fff4d8;color:#f08a00;}
.markdown-report table.evidence-table .status-pending{background:#e1f4ff;color:#1164d8;}
.markdown-report .appendix-title{color:#165fa7;font-size:1.12rem;font-weight:800;margin:1.55rem 0 .7rem;}
.markdown-report .appendix-group-title{color:#1f4f83;background:#eef7ff;border-left:4px solid #2d7fca;border-radius:0 6px 6px 0;font-size:.98rem;font-weight:800;margin:1.1rem 0 .5rem;padding:.42rem .72rem;}
.markdown-report ul{margin:.45rem 0 1rem;padding-left:1.4rem;}
.markdown-report li{margin:.25rem 0;}
.markdown-report a{color:#1d4ed8;text-decoration:none;}
.markdown-report a:hover{text-decoration:underline;}
.markdown-report code{background:#f3f4f6;border-radius:4px;padding:.1rem .3rem;}
@media (max-width:768px){.container{padding:0 1rem 2rem;}.hero-header{padding:1.7rem 0 1.55rem;}.hero-header h1{font-size:1.55rem;}.hero-subtitle{font-size:.95rem;}.hero-meta{gap:.5rem;}.hero-chip{font-size:.82rem;white-space:normal;}.report-toc{padding:1.1rem 1.2rem;}.report-toc-list{grid-template-columns:1fr;gap:.55rem;}.report-toc-list a{font-size:.95rem;}.markdown-report{padding:1rem;margin:1rem 0;}.markdown-report h2{font-size:1.18rem;}.markdown-report h3{font-size:1rem;}.markdown-report table{display:block;overflow-x:auto;border-radius:10px;font-size:.88rem;}.markdown-report thead th,.markdown-report tbody td{padding:.75rem .85rem;}.markdown-report tbody td:first-child{min-width:7rem;}}
@media print{body{background:#fff;}.hero-header{box-shadow:none;}.report-toc,.markdown-report{box-shadow:none;}.container{max-width:none;padding-left:.6in;padding-right:.6in;}}
"""
JS = r"""
document.addEventListener("click",function(e){var h=e.target.closest(".route-header");if(!h)return;h.parentElement.classList.toggle("open");});
"""


def render_table(headers: Sequence[str], rows: Sequence[Sequence[str]], empty_msg: str = "未检索到相关条目") -> str:
    if not rows:
        return f'<p class="empty">{esc(empty_msg)}</p>'
    th = "".join(f"<th>{esc(h)}</th>" for h in headers)
    body = []
    for r in rows:
        cells = "".join(f"<td>{c}</td>" for c in r)
        body.append(f"<tr>{cells}</tr>")
    return (
        '<div class="tbl-wrap"><table><thead><tr>'
        + th
        + "</tr></thead><tbody>"
        + "".join(body)
        + "</tbody></table></div>"
    )


# 工程案例 / 标准 行
def row_case(item: Dict[str, Any]) -> List[str]:
    sid = _get(item, "sid")
    return [
        esc(_get(item, "src")),
        esc(_get(item, "year")),
        esc(_get(item, "publisher")),
        link(_get(item, "title"), _get(item, "url")),
        esc(_get(item, "summary")) + render_cites([sid] if sid else None),
        esc(_get(item, "grade")),
    ]


# 论文行
def row_paper(item: Dict[str, Any]) -> List[str]:
    sid = _get(item, "sid")
    cited = _get(item, "cited_by", default="")
    return [
        esc(_get(item, "src")),
        esc(_get(item, "year")),
        esc(_get(item, "affiliation")),
        link(_get(item, "title"), _get(item, "url")),
        f"被引 {esc(cited)}" if cited != "" else "",
        esc(_get(item, "doi")) + render_cites([sid] if sid else None),
    ]


# 专利行
def row_patent(item: Dict[str, Any]) -> List[str]:
    sid = _get(item, "sid")
    cited = _get(item, "cited_by", default="")
    return [
        esc(_get(item, "src")),
        esc(_get(item, "pub_no")),
        link(_get(item, "title"), _get(item, "url")),
        esc(_get(item, "applicant")),
        esc(_get(item, "pub_year")),
        status_span(_get(item, "status")),
        (f"被引 {esc(cited)}" if cited != "" else "") + render_cites([sid] if sid else None),
    ]


# Web 学术行
def row_web(item: Dict[str, Any]) -> List[str]:
    sid = _get(item, "sid")
    return [
        esc(_get(item, "site")),
        link(_get(item, "title"), _get(item, "url")),
        esc(_get(item, "summary")) + render_cites([sid] if sid else None),
    ]


HEADERS_CASE = ["源", "年", "发布机构", "标题", "核心内容", "鉴定等级"]
HEADERS_PAPER = ["源", "年", "作者机构", "标题", "被引", "DOI"]
HEADERS_PATENT = ["源", "公开号", "标题", "申请人", "公开年", "状态", "被引"]
HEADERS_WEB = ["源站点", "标题", "简述"]
def render_header(payload: Dict[str, Any]) -> str:
    project_name = _get(payload, "meta", "project_name")
    applicant = _get(payload, "meta", "applicant")
    today_iso = _get(payload, "meta", "today_iso")
    scope = _get(payload, "meta", "scope") or "专利+论文+网络学术文献补充"

    meta_lines: List[str] = []
    if project_name:
        meta_lines.append(f'<span><strong>项目名称：</strong>{esc(project_name)}</span>')
    if applicant:
        meta_lines.append(f'<span><strong>申报单位：</strong>{esc(applicant)}</span>')
    meta_lines.append(f'<span><strong>检索日期：</strong>{esc(today_iso)}</span>')
    meta_lines.append(f'<span><strong>检索范围：</strong>{esc(scope)}</span>')

    return (
        '<div class="report-header">'
        '<div class="container">'
        '<h1>科研需求检索报告</h1>'
        '<div class="meta">' + "".join(meta_lines) + '</div>'
        '</div></div>'
    )


def render_toc() -> str:
    return (
        '<nav class="toc"><ul>'
        '<li><a href="#s1">一、项目需求解析</a></li>'
        '<li><a href="#s2">二、技术难题拆解</a></li>'
        '<li><a href="#s3">三、主要研究内容和措施</a></li>'
        '<li><a href="#s4">四、主要科研单位分析</a></li>'
        '<li><a href="#s5">五、附录</a></li>'
        '<li><a href="#src">来源清单</a></li>'
        '</ul></nav>'
    )


def render_demand(payload: Dict[str, Any]) -> str:
    text = _get(payload, "requirement_text") or "未提及"
    text_html = esc(text).replace("\n", "<br>")
    return (
        '<section class="demand-block">'
        '<div class="demand-title">需求输入原文</div>'
        f'<div>{text_html}</div>'
        '</section>'
    )


def _val(v: Any) -> str:
    s = "" if v is None else str(v).strip()
    return esc(s) if s else "未提及"


def render_s1(payload: Dict[str, Any]) -> str:
    a = _get(payload, "analysis")
    rows = [
        ["<strong>需求牵引：问题从哪来</strong>",
         f"<strong>场景</strong>：{_val(_get(a,'demand','scene'))}<br>"
         f"<strong>痛点</strong>：{_val(_get(a,'demand','pain'))}<br>"
         f"<strong>当前应对</strong>：{_val(_get(a,'demand','current'))}"],
        ["<strong>瓶颈分析：现有方案为何不行</strong>",
         f"<strong>瓶颈</strong>：{_val(_get(a,'bottleneck','limit'))}<br>"
         f"<strong>现有措施局限</strong>：{_val(_get(a,'bottleneck','cost'))}<br>"
         f"<strong>原理局限</strong>：{_val(_get(a,'bottleneck','principle'))}"],
        ["<strong>解决思路：本课题如何突破</strong>",
         f"<strong>技术路径</strong>：{_val(_get(a,'solution','path'))}<br>"
         f"<strong>系统方案</strong>：{_val(_get(a,'solution','system'))}<br>"
         f"<strong>工程兼容性</strong>：{_val(_get(a,'solution','compat'))}<br>"
         f"<strong>锁定目标</strong>：{_val(_get(a,'solution','target'))}"],
    ]
    body = render_table(["维度", "关键内容"], rows)
    return (
        '<section class="section-card" id="s1">'
        '<div class="section-header">一、项目需求解析</div>'
        f'<div class="section-body">{body}</div>'
        '</section>'
    )


CIRCLED = ["①","②","③","④","⑤","⑥","⑦","⑧","⑨","⑩","⑪","⑫","⑬","⑭","⑮"]


def render_s2(payload: Dict[str, Any]) -> str:
    issues = _list(payload, "issues")
    rows = []
    for it in issues:
        no = esc(_get(it, "no") or f"T{len(rows)+1}")
        name = _get(it, "name") or ""
        desc = _get(it, "desc") or ""
        rows.append([no, f"<strong>[{esc(name)}]</strong>：{esc(desc)}"])
    table_html = render_table(["序号", "技术难题描述"], rows, empty_msg="原文未提炼出技术难题")

    directions = _list(payload, "directions")
    n = len(issues)
    k = len(directions)
    items = []
    for i, d in enumerate(directions):
        mark = CIRCLED[i] if i < len(CIRCLED) else f"({i+1})"
        covers = _get(d, "covers") or []
        if isinstance(covers, list):
            covers_str = "+".join(str(c) for c in covers)
        else:
            covers_str = str(covers)
        items.append(
            f'<li><strong>方向{mark}</strong> {esc(_get(d,"name"))}'
            + (f"（覆盖 {esc(covers_str)}）" if covers_str else "")
            + "</li>"
        )
    tip = (
        '<section class="demand-block">'
        f'<div class="demand-title">基于以上 {n} 个技术难题，识别 {k} 个核心技术攻关方向</div>'
        f'<ul class="tight">{"".join(items) or "<li class=\"empty\">未识别攻关方向</li>"}</ul>'
        '</section>'
    )
    return (
        '<section class="section-card" id="s2">'
        '<div class="section-header">二、技术难题拆解</div>'
        f'<div class="section-body">{table_html}{tip}</div>'
        '</section>'
    )
def render_summary(payload: Dict[str, Any]) -> str:
    s = _get(payload, "summary") or {}
    cnt_case = _get(s, "cnt_case", default=0)
    cnt_paper = _get(s, "cnt_paper", default=0)
    cnt_patent = _get(s, "cnt_patent", default=0)
    cnt_web = _get(s, "cnt_web", default=0)
    cnt_org_total = _get(s, "cnt_org_total", default=0)
    cnt_org_top5 = _get(s, "cnt_org_top5", default=0)
    top_orgs = _get(s, "top_orgs") or "暂未识别明确研究单位"

    sentence = (
        f"本次技术经检索后发现 {esc(cnt_case)} 条工程案例/标准、"
        f"{esc(cnt_paper)} 篇相似技术论文，"
        f"{esc(cnt_patent)} 篇相似技术专利，"
        f"{esc(cnt_web)} 条网络学术补充条目，"
        f"业内主要研究该技术单位 {esc(cnt_org_total)} 家，"
        f"其中代表性单位为 {esc(top_orgs)}。"
    )
    block = (
        '<section class="demand-block">'
        '<div class="demand-title">检索成果汇总</div>'
        f'<div>{sentence}</div>'
        '</section>'
    )
    rows = [
        ["工程案例/标准", esc(cnt_case)],
        ["相似技术论文", esc(cnt_paper)],
        ["相似技术专利", esc(cnt_patent)],
        ["网络学术补充", esc(cnt_web)],
        ["主要科研单位（去重）", esc(cnt_org_total)],
        ["代表性单位（展示家数）", esc(cnt_org_top5)],
    ]
    table_html = render_table(["类别", "数量"], rows)
    return block + table_html


def render_route_card(idx: int, d: Dict[str, Any]) -> str:
    mark = CIRCLED[idx] if idx < len(CIRCLED) else f"({idx+1})"
    rid = f"r{idx+1}"
    badge_cls = f"r{idx+1}" if idx + 1 <= 10 else "r10"
    name = _get(d, "name")
    no_label = ["一","二","三","四","五","六","七","八","九","十"]
    label = no_label[idx] if idx < len(no_label) else str(idx+1)

    cnt = _get(d, "counts") or {}
    hit = (
        f"本路线命中 {esc(_get(cnt,'case',default=0))} 条工程案例/标准、"
        f"{esc(_get(cnt,'paper',default=0))} 篇论文、"
        f"{esc(_get(cnt,'patent',default=0))} 篇专利、"
        f"{esc(_get(cnt,'web',default=0))} 条网络补充"
    )
    extra = _get(d, "hit_extra")
    if extra:
        hit += "；" + esc(extra)
    if all(int(_get(cnt, k, default=0) or 0) == 0 for k in ("case", "paper", "patent", "web")):
        hit = "未检索到直接相关技术"

    contents = _list(d, "contents")
    li = []
    for c in contents:
        if isinstance(c, dict):
            text = esc(_get(c, "text"))
            cites = _get(c, "cites") or ([_get(c, "sid")] if _get(c, "sid") else [])
            li.append(f"<li>{text}{render_cites(cites)}</li>")
        else:
            li.append(f"<li>{esc(c)}</li>")
    contents_html = (
        f'<ul class="tight">{"".join(li)}</ul>' if li else '<p class="empty">未给出研发内容</p>'
    )

    cases = _list(d, "evidence", "cases")
    papers = _list(d, "evidence", "papers")
    patents = _list(d, "evidence", "patents")
    webs = _list(d, "evidence", "webs")

    body = (
        f'<p class="tight"><strong>检索结果</strong>：{hit}</p>'
        f'<p class="tight"><strong>核心问题</strong>：{esc(_get(d, "problem")) or "未提及"}</p>'
        f'<p class="tight"><strong>研发内容</strong>：</p>{contents_html}'
        f'<p class="tight"><strong>技术目标</strong>：{esc(_get(d, "target")) or "未提及"}</p>'
        '<h4 class="evi-title">代表参考证据（工程案例/标准）</h4>'
        + render_table(HEADERS_CASE, [row_case(x) for x in cases])
        + '<h4 class="evi-title">代表参考证据（论文）</h4>'
        + render_table(HEADERS_PAPER, [row_paper(x) for x in papers])
        + '<h4 class="evi-title">代表参考证据（专利）</h4>'
        + render_table(HEADERS_PATENT, [row_patent(x) for x in patents])
        + '<h4 class="evi-title">代表参考证据(Web 学术补充)</h4>'
        + render_table(HEADERS_WEB, [row_web(x) for x in webs])
    )
    return (
        f'<div class="route-card open" id="{rid}">'
        '<div class="route-header">'
        f'<span class="route-badge {badge_cls}">{mark}</span>'
        f'<h3>研发路线{label}：{esc(name)}</h3>'
        '</div>'
        f'<div class="route-body">{body}</div>'
        '</div>'
    )


def render_route_summary(payload: Dict[str, Any]) -> str:
    directions = _list(payload, "directions")
    k = len(directions)
    rid = f"r{k+1}"
    rows = []
    for i, d in enumerate(directions):
        mark = CIRCLED[i] if i < len(CIRCLED) else f"({i+1})"
        covers = _get(d, "covers") or []
        if isinstance(covers, list):
            covers_str = "+".join(str(c) for c in covers)
        else:
            covers_str = str(covers)
        sids = _get(d, "summary_sids") or []
        rows.append([
            f"方向{mark} {esc(_get(d,'name'))}",
            esc(covers_str),
            esc(_get(d, "summary_focus")),
            esc(_get(d, "summary_output")),
            render_cites(sids).strip() or "",
        ])
    table_html = render_table(
        ["路线", "对应难题", "核心攻关", "输出成果", "代表参考证据"],
        rows,
    )
    return (
        f'<div class="route-card open" id="{rid}">'
        '<div class="route-header">'
        '<span class="route-badge summary">Σ</span>'
        '<h3>研发路线总结</h3>'
        '</div>'
        f'<div class="route-body">{table_html}</div>'
        '</div>'
    )


def render_s3(payload: Dict[str, Any]) -> str:
    cards = "".join(
        render_route_card(i, d) for i, d in enumerate(_list(payload, "directions"))
    )
    return (
        '<section class="section-card" id="s3">'
        '<div class="section-header">三、主要研究内容和措施</div>'
        '<div class="section-body">'
        + render_summary(payload)
        + cards
        + render_route_summary(payload)
        + '</div></section>'
    )
def render_s4(payload: Dict[str, Any]) -> str:
    units = _list(payload, "units")
    head = (
        '<div class="unit-row unit-head">'
        '<div>单位</div><div>覆盖路线</div><div>技术重点</div><div>代表成果</div>'
        '</div>'
    )
    rows = []
    for u in units:
        cites = _get(u, "cites") or ([_get(u, "sid")] if _get(u, "sid") else [])
        achievements = esc(_get(u, "achievements")) + render_cites(cites)
        covers = _get(u, "covers") or []
        if isinstance(covers, list):
            covers_str = "、".join(str(c) for c in covers)
        else:
            covers_str = str(covers)
        rows.append(
            '<div class="unit-row">'
            f'<div class="unit-name">{esc(_get(u,"name"))}</div>'
            f'<div>{esc(covers_str)}</div>'
            f'<div>{esc(_get(u,"focus"))}</div>'
            f'<div>{achievements}</div>'
            '</div>'
        )
    body = head + ("".join(rows) if rows else '<p class="empty">暂未识别明确研究单位</p>')
    return (
        '<section class="section-card" id="s4">'
        '<div class="section-header">四、主要科研单位分析</div>'
        f'<div class="section-body">{body}</div>'
        '</section>'
    )


def _group_by_dir(items: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    groups: Dict[str, List[Dict[str, Any]]] = {}
    for it in items:
        key = str(_get(it, "direction") or _get(it, "dir") or "未分组")
        groups.setdefault(key, []).append(it)
    return groups


def _appendix_block(title: str, headers: Sequence[str], rows: List[List[str]]) -> str:
    return f'<h4 class="app-title">{esc(title)}</h4>' + render_table(headers, rows)


def render_appendix(payload: Dict[str, Any]) -> str:
    app = _get(payload, "appendix") or {}
    parts: List[str] = []

    # A1
    parts.append('<h3>A1 工程案例 / 标准清单</h3>')
    a1 = _list(app, "a1")
    if a1:
        for dir_name, items in _group_by_dir(a1).items():
            parts.append(
                _appendix_block(
                    f"{dir_name} · 工程案例/标准",
                    ["编号", "源", "年", "发布机构", "标题", "核心内容", "鉴定等级"],
                    [
                        [
                            esc(_get(x, "no")),
                            esc(_get(x, "src")),
                            esc(_get(x, "year")),
                            esc(_get(x, "publisher")),
                            link(_get(x, "title"), _get(x, "url")),
                            esc(_get(x, "summary")) + render_cites([_get(x, "sid")] if _get(x, "sid") else None),
                            esc(_get(x, "grade")),
                        ]
                        for x in items
                    ],
                )
            )
    else:
        parts.append('<p class="empty">未收录工程案例/标准</p>')

    # A2
    parts.append('<h3>A2 论文清单</h3>')
    a2 = _list(app, "a2")
    if a2:
        for dir_name, items in _group_by_dir(a2).items():
            parts.append(
                _appendix_block(
                    f"{dir_name} · 论文",
                    HEADERS_PAPER,
                    [row_paper(x) for x in items],
                )
            )
    else:
        parts.append('<p class="empty">未收录论文</p>')

    # A3
    parts.append('<h3>A3 专利清单</h3>')
    a3 = _list(app, "a3")
    if a3:
        for dir_name, items in _group_by_dir(a3).items():
            parts.append(
                _appendix_block(
                    f"{dir_name} · 专利",
                    HEADERS_PATENT,
                    [row_patent(x) for x in items],
                )
            )
    else:
        parts.append('<p class="empty">未收录专利</p>')

    # A4
    parts.append('<h3>A4 网络学术清单</h3>')
    a4 = _list(app, "a4")
    if a4:
        cat_order = ["期刊论文", "工程案例", "技术标准"]
        groups: Dict[str, List[Dict[str, Any]]] = {}
        for it in a4:
            cat = str(_get(it, "category") or "其他")
            groups.setdefault(cat, []).append(it)
        ordered_keys = [k for k in cat_order if k in groups] + [
            k for k in groups if k not in cat_order
        ]
        for cat in ordered_keys:
            parts.append(
                _appendix_block(
                    f"{cat}",
                    HEADERS_WEB,
                    [row_web(x) for x in groups[cat]],
                )
            )
    else:
        parts.append('<p class="empty">未收录网络学术补充</p>')

    return (
        '<section class="section-card" id="s5">'
        '<div class="section-header">五、附录</div>'
        f'<div class="section-body">{"".join(parts)}</div>'
        '</section>'
    )
def _sid_sort_key(sid: str) -> tuple:
    s = sid.strip()
    prefix = s[0] if s and not s[0].isdigit() else ""
    digits = "".join(ch for ch in s if ch.isdigit())
    try:
        n = int(digits) if digits else 0
    except ValueError:
        n = 0
    return (prefix, n, s)


def _walk_collect_sources(payload: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
    """Collect {sid: {title, url}} from directions evidence + appendix A1/A2/A3/A4."""
    bag: Dict[str, Dict[str, str]] = {}

    def add(item: Dict[str, Any]) -> None:
        sid = _cite_label(_get(item, "sid"))
        if not sid:
            return
        title = str(_get(item, "title") or _get(item, "summary") or "")
        url = str(_get(item, "url") or "")
        if sid not in bag or (not bag[sid].get("url") and url):
            bag[sid] = {"title": title, "url": url}

    for d in _list(payload, "directions"):
        for key in ("cases", "papers", "patents", "webs"):
            for it in _list(d, "evidence", key):
                if isinstance(it, dict):
                    add(it)
    app = _get(payload, "appendix") or {}
    for key in ("a1", "a2", "a3", "a4"):
        for it in _list(app, key):
            if isinstance(it, dict):
                add(it)
    return bag


def render_sources(payload: Dict[str, Any]) -> str:
    bag = _walk_collect_sources(payload)
    if not bag:
        return (
            '<footer class="src-footer" id="src">'
            '<h2>来源清单</h2>'
            '<p class="empty">暂无引用条目</p>'
            '</footer>'
        )
    chips = []
    for sid in sorted(bag.keys(), key=_sid_sort_key):
        info = bag[sid]
        title = info.get("title") or sid
        url = info.get("url")
        sid_label = f'<span class="sid">[{esc(sid)}]</span>'
        if url:
            chips.append(
                f'<a class="src-chip" href="{esc(url)}" target="_blank" rel="noopener">'
                f'{sid_label}{esc(title)}</a>'
            )
        else:
            chips.append(f'<span class="src-chip">{sid_label}{esc(title)}</span>')
    return (
        '<footer class="src-footer" id="src">'
        '<div class="container">'
        '<h2>来源清单</h2>'
        f'<div class="src-grid">{"".join(chips)}</div>'
        '</div></footer>'
    )


def render_footer(payload: Dict[str, Any]) -> str:
    today = _get(payload, "meta", "today_iso") or ""
    return (
        '<div class="footer">'
        f'本报告由 rd-direction-finder 自动生成 · 生成日期 {esc(today)}'
        '</div>'
    )


def md_text(s: Any) -> str:
    if s is None:
        return ""
    return str(s).replace("\r\n", "\n").replace("\r", "\n").strip()


def md_cell(s: Any) -> str:
    text = md_text(s)
    if not text:
        return "未提及"
    return text.replace("|", "\\|").replace("\n", " <br> ")


def md_link(title: Any, url: Any) -> str:
    title_text = md_text(title) or md_text(url)
    url_text = md_text(url)
    title_text = title_text.replace("[", "\\[").replace("]", "\\]")
    if not url_text:
        return title_text or "未提及"
    url_text = url_text.replace(")", "%29").replace(" ", "%20")
    return f"[{title_text}]({url_text})"


def cite_text(cites: Optional[Iterable[Any]]) -> str:
    if not cites:
        return ""
    if isinstance(cites, (str, int)):
        cites = [cites]
    labels = [_cite_label(c) for c in cites if c]
    labels = [f"[{label}]" for label in labels if label]
    return (" " + " ".join(labels)) if labels else ""


def covers_text(covers: Any) -> str:
    if isinstance(covers, list):
        return "+".join(str(c) for c in covers)
    return md_text(covers)


def md_table(headers: Sequence[str], rows: Sequence[Sequence[Any]]) -> str:
    header = "| " + " | ".join(headers) + " |"
    align = "| " + " | ".join(":--" for _ in headers) + " |"
    body = [
        "| " + " | ".join(md_cell(cell) for cell in row) + " |"
        for row in rows
    ]
    if not body:
        body = ["| " + " | ".join("未提及" for _ in headers) + " |"]
    return "\n".join([header, align] + body)


def extract_cite_labels(text: str) -> List[str]:
    return [f"S{m}" for m in re.findall(r"(?<![\w/-])\[S(\d+)\]", text or "")]


def route_sid_index(markdown_text: str) -> tuple[Dict[str, str], List[str]]:
    """Map evidence citation ids back to the 3.2+ route section where they appear."""
    headings = list(re.finditer(r"^### (?P<title>3\.\d+ [^\n]+)$", markdown_text, flags=re.M))
    sid_to_route: Dict[str, str] = {}
    route_order: List[str] = []
    for i, match in enumerate(headings):
        title = match.group("title").strip()
        if "检索成果汇总" in title or "研发路线总结" in title:
            continue
        end = headings[i + 1].start() if i + 1 < len(headings) else len(markdown_text)
        body = markdown_text[match.end():end]
        route_order.append(title)
        for sid in extract_cite_labels(body):
            sid_to_route.setdefault(sid, title)
    return sid_to_route, route_order


def split_markdown_table(block: str) -> tuple[str, str, str]:
    """Return text before the first table, that table, and text after it."""
    lines = block.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip().startswith("|") and line.strip().endswith("|"):
            start = i
            break
    if start is None:
        return block, "", ""
    end = start
    while end < len(lines) and lines[end].strip().startswith("|") and lines[end].strip().endswith("|"):
        end += 1
    before = "\n".join(lines[:start]).strip()
    table = "\n".join(lines[start:end]).strip()
    after = "\n".join(lines[end:]).strip()
    return before, table, after


def group_markdown_table_by_route(
    table_text: str,
    sid_to_route: Dict[str, str],
    route_order: Sequence[str],
) -> str:
    lines = [line for line in table_text.splitlines() if line.strip()]
    if len(lines) < 3:
        return table_text
    header = lines[:2]
    rows = lines[2:]
    grouped: Dict[str, List[str]] = {}
    order = list(route_order)
    fallback = "未归类技术方向"

    for row in rows:
        route = fallback
        for sid in extract_cite_labels(row):
            if sid in sid_to_route:
                route = sid_to_route[sid]
                break
        if route not in order and route != fallback:
            order.append(route)
        grouped.setdefault(route, []).append(row)

    ordered_keys = [key for key in order if key in grouped]
    if fallback in grouped:
        ordered_keys.append(fallback)
    if len(ordered_keys) <= 1 and ordered_keys == [fallback]:
        return table_text

    chunks: List[str] = []
    for route in ordered_keys:
        chunks.extend([f"#### {route}", "", "\n".join(header + grouped[route]), ""])
    return "\n".join(chunks).strip()


def group_appendices_by_route(markdown_text: str) -> str:
    """Make A1/A2/A3 comply with Step 4's route-grouped appendix requirement."""
    sid_to_route, route_order = route_sid_index(markdown_text)
    if not sid_to_route:
        return markdown_text

    def repl(match: re.Match[str]) -> str:
        title = match.group("title")
        body = match.group("body")
        if re.search(r"^####\s+", body, flags=re.M):
            return match.group(0)
        before, table, after = split_markdown_table(body)
        if not table:
            return match.group(0)
        grouped = group_markdown_table_by_route(table, sid_to_route, route_order)
        body_parts = [part for part in [before, grouped, after] if part]
        return f"### {title}\n\n" + "\n\n".join(body_parts).rstrip() + "\n"

    return re.sub(
        r"^### (?P<title>A[1-3] [^\n]+)\n\n(?P<body>.*?)(?=^### A[2-4] |\Z)",
        repl,
        markdown_text,
        flags=re.M | re.S,
    )


def direction_title(idx: int) -> str:
    labels = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
    return labels[idx] if idx < len(labels) else str(idx + 1)


def md_case_row(item: Dict[str, Any], include_no: bool = False) -> List[str]:
    sid = _get(item, "sid")
    row = [
        _get(item, "src"),
        _get(item, "year"),
        _get(item, "publisher"),
        md_link(_get(item, "title"), _get(item, "url")),
        md_text(_get(item, "summary")) + cite_text([sid] if sid else None),
        _get(item, "grade"),
    ]
    if include_no:
        return [_get(item, "no")] + row
    return row


def md_paper_row(item: Dict[str, Any]) -> List[str]:
    sid = _get(item, "sid")
    cited = _get(item, "cited_by", default="")
    return [
        _get(item, "src"),
        _get(item, "year"),
        _get(item, "affiliation"),
        md_link(_get(item, "title"), _get(item, "url")),
        f"被引 {md_text(cited)}" if cited != "" else "",
        md_text(_get(item, "doi")) + cite_text([sid] if sid else None),
    ]


def md_patent_row(item: Dict[str, Any]) -> List[str]:
    sid = _get(item, "sid")
    cited = _get(item, "cited_by", default="")
    return [
        _get(item, "src"),
        _get(item, "pub_no"),
        md_link(_get(item, "title"), _get(item, "url")),
        _get(item, "applicant"),
        _get(item, "pub_year"),
        _get(item, "status"),
        (f"被引 {md_text(cited)}" if cited != "" else "") + cite_text([sid] if sid else None),
    ]


def md_web_row(item: Dict[str, Any], include_category: bool = False) -> List[str]:
    sid = _get(item, "sid")
    row = [
        _get(item, "site"),
        md_link(_get(item, "title"), _get(item, "url")),
        md_text(_get(item, "summary")) + cite_text([sid] if sid else None),
    ]
    if include_category:
        return [_get(item, "category") or "其他"] + row
    return row


def build_markdown_report(payload: Dict[str, Any]) -> str:
    """Build the exact Step 4 report body defined by SKILL.md/report-template.md."""
    meta = _get(payload, "meta") or {}
    project_name = md_text(_get(meta, "project_name"))
    applicant = md_text(_get(meta, "applicant"))
    today_iso = md_text(_get(meta, "today_iso"))
    scope = md_text(_get(meta, "scope")) or "专利+论文+网络学术文献补充"
    requirement = md_text(_get(payload, "requirement_text")) or "未提及"
    analysis = _get(payload, "analysis") or {}
    summary = _get(payload, "summary") or {}
    issues = _list(payload, "issues")
    directions = _list(payload, "directions")
    units = _list(payload, "units")
    app = _get(payload, "appendix") or {}

    parts: List[str] = ["## 科研需求检索报告", ""]
    parts.append("> **科研需求检索报告**")
    if project_name:
        parts.append(f"> **项目名称：** {project_name}")
    meta_line = []
    if applicant:
        meta_line.append(f"**申报单位：** {applicant}")
    meta_line.append(f"**检索日期：** {today_iso}")
    meta_line.append(f"**检索范围：** {scope}")
    parts.extend([">", "> " + " &nbsp;&nbsp;".join(meta_line), ""])
    parts.extend(["> **需求输入原文：**", ">", *["> " + line for line in requirement.split("\n")], ""])

    parts.extend([
        "## 一、项目需求解析",
        "",
        md_table(
            ["维度", "关键内容"],
            [
                [
                    "**需求牵引：问题从哪来**",
                    f"**场景**：{md_text(_get(analysis, 'demand', 'scene')) or '未提及'} <br> "
                    f"**痛点**：{md_text(_get(analysis, 'demand', 'pain')) or '未提及'} <br> "
                    f"**当前应对**：{md_text(_get(analysis, 'demand', 'current')) or '未提及'}",
                ],
                [
                    "**瓶颈分析：现有方案为何不行**",
                    f"**瓶颈**：{md_text(_get(analysis, 'bottleneck', 'limit')) or '未提及'} <br> "
                    f"**现有措施局限**：{md_text(_get(analysis, 'bottleneck', 'cost')) or '未提及'} <br> "
                    f"**原理局限**：{md_text(_get(analysis, 'bottleneck', 'principle')) or '未提及'}",
                ],
                [
                    "**解决思路：本课题如何突破**",
                    f"**技术路径**：{md_text(_get(analysis, 'solution', 'path')) or '未提及'} <br> "
                    f"**系统方案**：{md_text(_get(analysis, 'solution', 'system')) or '未提及'} <br> "
                    f"**工程兼容性**：{md_text(_get(analysis, 'solution', 'compat')) or '未提及'} <br> "
                    f"**锁定目标**：{md_text(_get(analysis, 'solution', 'target')) or '未提及'}",
                ],
            ],
        ),
        "",
        "## 二、技术难题拆解",
        "",
        md_table(
            ["序号", "技术难题描述"],
            [
                [
                    _get(it, "no") or f"T{i + 1}",
                    f"**[{md_text(_get(it, 'name'))}]**：{md_text(_get(it, 'desc'))}",
                ]
                for i, it in enumerate(issues)
            ],
        ),
        "",
        f"> 基于以上 {len(issues)} 个技术难题，识别 {len(directions)} 个核心技术攻关方向（k = min(N, max_directions)，可合并同类项），驱动 Step 2a、Step 2b 检索：",
        ">",
    ])
    for i, d in enumerate(directions):
        mark = CIRCLED[i] if i < len(CIRCLED) else f"({i + 1})"
        parts.append(f"> - **方向{mark}** {md_text(_get(d, 'name'))}（覆盖 {covers_text(_get(d, 'covers'))}）")

    cnt_case = _get(summary, "cnt_case", default=0)
    cnt_paper = _get(summary, "cnt_paper", default=0)
    cnt_patent = _get(summary, "cnt_patent", default=0)
    cnt_web = _get(summary, "cnt_web", default=0)
    cnt_org_total = _get(summary, "cnt_org_total", default=0)
    top_orgs = md_text(_get(summary, "top_orgs")) or "暂未识别明确研究单位"
    parts.extend([
        "",
        "## 三、主要研究内容和措施",
        "",
        "### 3.1 检索成果汇总",
        "",
        f"**检索成果汇总**：结论前置，一句话总结检索成果。本次技术经检索后发现 {cnt_case} 条工程案例/标准、{cnt_paper} 篇相似技术论文，{cnt_patent} 篇相似技术专利，{cnt_web} 条网络学术补充条目，业内主要研究该技术单位 {cnt_org_total} 家，其中代表性单位为 {top_orgs}。",
        "",
        "> 总数为各路线去重合并后的全量计数，必须来自工具返回的真实数字；各路线明细在 3.2 起逐条展开，完整清单见附录 A1/A2/A3/A4，主要科研单位见第四节。",
        "",
    ])

    for i, d in enumerate(directions):
        section_no = f"3.{i + 2}"
        counts = _get(d, "counts") or {}
        cnts = {
            key: _get(counts, key, default=0)
            for key in ("case", "paper", "patent", "web")
        }
        hit = (
            f"本路线命中 {cnts['case']} 条工程案例/标准、{cnts['paper']} 篇论文、"
            f"{cnts['patent']} 篇专利、{cnts['web']} 条网络补充"
        )
        if md_text(_get(d, "hit_extra")):
            hit += "、" + md_text(_get(d, "hit_extra"))
        if all(int(cnts[k] or 0) == 0 for k in cnts):
            hit = "未检索到直接相关技术"

        parts.extend([
            f"### {section_no} 研发路线{direction_title(i)}：{md_text(_get(d, 'name'))}",
            "",
            f"**检索结果**：{hit}",
            "",
            f"**核心问题**：{md_text(_get(d, 'problem')) or '未提及'}",
            "",
            "**研发内容**（每条至少绑定 1 个 [S#] 证据）：",
            "",
        ])
        for c in _list(d, "contents"):
            if isinstance(c, dict):
                parts.append(f"- {md_text(_get(c, 'text'))}{cite_text(_get(c, 'cites') or ([_get(c, 'sid')] if _get(c, 'sid') else []))}")
            else:
                parts.append(f"- {md_text(c)}")
        if not _list(d, "contents"):
            parts.append("- 未提及")

        ev = _get(d, "evidence") or {}
        parts.extend([
            "",
            f"**技术目标**：{md_text(_get(d, 'target')) or '未提及'}",
            "",
            "**代表参考证据（工程案例/标准）**：",
            "",
            md_table(HEADERS_CASE, [md_case_row(x) for x in _list(ev, "cases")]),
            "",
            "**代表参考证据（论文）**：",
            "",
            md_table(HEADERS_PAPER, [md_paper_row(x) for x in _list(ev, "papers")]),
            "",
            "**代表参考证据（专利）**：",
            "",
            md_table(HEADERS_PATENT, [md_patent_row(x) for x in _list(ev, "patents")]),
            "",
            "**代表参考证据（Web 学术补充）**：",
            "",
            md_table(HEADERS_WEB, [md_web_row(x) for x in _list(ev, "webs")]),
            "",
        ])

    parts.extend([
        f"### 3.{len(directions) + 2} 研发路线总结",
        "",
        md_table(
            ["路线", "对应难题", "核心攻关", "输出成果", "代表参考证据"],
            [
                [
                    f"方向{CIRCLED[i] if i < len(CIRCLED) else f'({i + 1})'} {md_text(_get(d, 'name'))}",
                    covers_text(_get(d, "covers")),
                    _get(d, "summary_focus"),
                    _get(d, "summary_output"),
                    cite_text(_get(d, "summary_sids")).strip(),
                ]
                for i, d in enumerate(directions)
            ],
        ),
        "",
        "## 四、主要科研单位分析",
        "",
        md_table(
            ["单位", "覆盖路线", "技术重点", "代表成果"],
            [
                [
                    _get(u, "name"),
                    "、".join(str(x) for x in _get(u, "covers")) if isinstance(_get(u, "covers"), list) else _get(u, "covers"),
                    _get(u, "focus"),
                    md_text(_get(u, "achievements")) + cite_text(_get(u, "cites") or ([_get(u, "sid")] if _get(u, "sid") else [])),
                ]
                for u in units
            ],
        ),
        "",
        "## 五、附录",
        "",
        "### A1 工程案例 / 标准清单",
        "",
    ])
    a1 = _list(app, "a1")
    if a1:
        for dir_name, items in _group_by_dir(a1).items():
            parts.extend([
                f"#### {md_text(dir_name)}",
                "",
                md_table(["编号", "源", "年", "发布机构", "标题", "核心内容", "鉴定等级"], [md_case_row(x, include_no=True) for x in items]),
                "",
            ])
    else:
        parts.append("未收录工程案例/标准。")

    parts.extend(["", "### A2 论文清单", ""])
    a2 = _list(app, "a2")
    if a2:
        for dir_name, items in _group_by_dir(a2).items():
            parts.extend([
                f"#### {md_text(dir_name)}",
                "",
                md_table(HEADERS_PAPER, [md_paper_row(x) for x in items]),
                "",
            ])
    else:
        parts.append("未收录论文。")

    parts.extend(["", "### A3 专利清单", ""])
    a3 = _list(app, "a3")
    if a3:
        for dir_name, items in _group_by_dir(a3).items():
            parts.extend([
                f"#### {md_text(dir_name)}",
                "",
                md_table(HEADERS_PATENT, [md_patent_row(x) for x in items]),
                "",
            ])
    else:
        parts.append("未收录专利。")

    parts.extend(["", "### A4 网络学术清单", ""])
    a4 = _list(app, "a4")
    if a4:
        parts.append(md_table(["类别", *HEADERS_WEB], [md_web_row(x, include_category=True) for x in a4]))
    else:
        parts.append("未收录网络学术补充。")

    return "\n".join(parts).strip() + "\n"


def render_markdown_report(markdown_text: str) -> str:
    markdown_text = group_appendices_by_route(markdown_text)
    renderer = mistune.create_markdown(escape=False, plugins=["table"])
    html_text = renderer(markdown_text)
    html_text = re.sub(
        r"(?<![\w/-])\[S(\d+)\]",
        r'<span class="cite-tag">S\1</span>',
        html_text,
    )
    html_text = re.sub(
        r"<blockquote>\n<p><strong>需求输入原文：</strong></p>\n<p>(?P<text>.*?)</p>\n</blockquote>",
        lambda m: (
            '<section class="requirement-shell">'
            '<div class="requirement-block">'
            '<div class="requirement-title">需求输入原文：</div>'
            f'<p class="requirement-text">{m.group("text")}</p>'
            '</div>'
            '</section>'
        ),
        html_text,
        count=1,
        flags=re.S,
    )
    html_text = re.sub(
        r"<p><strong>(代表参考证据（([^）]+)）)</strong>：</p>\n<table>",
        lambda m: (
            f'<p class="evidence-title"><strong>{m.group(1)}</strong></p>\n'
            f'<table class="evidence-table evidence-{evidence_kind_class(m.group(2))}">'
        ),
        html_text,
    )
    html_text = re.sub(
        r"<h3>(A[1-4] [^<]+)</h3>\n<table>",
        lambda m: (
            f'<h3 class="appendix-title">{m.group(1)}</h3>\n'
            f'<table class="evidence-table appendix-table appendix-{appendix_kind_class(m.group(1))}">'
        ),
        html_text,
    )
    html_text = re.sub(
        r"<h3>(A[1-4] [^<]+)</h3>",
        r'<h3 class="appendix-title">\1</h3>',
        html_text,
    )
    html_text = re.sub(
        r"<h4>([^<]+)</h4>\n<table>",
        r'<h4 class="appendix-group-title">\1</h4>\n<table class="evidence-table appendix-table">',
        html_text,
    )
    html_text = re.sub(
        r"<h3>3\.1 检索成果汇总</h3>\n(?P<body>.*?)(?=\n<h3>3\.2 )",
        lambda m: (
            '<section class="summary-card">'
            '<h3 class="summary-card-title">3.1 检索成果汇总</h3>'
            f'<div class="summary-card-body">{m.group("body").strip()}</div>'
            '</section>'
        ),
        html_text,
        count=1,
        flags=re.S,
    )
    html_text = re.sub(
        r"<h3>(3\.(?!1\b)\d+ [^<]+)</h3>\n(?P<body>.*?)(?=\n<h3>3\.\d+ |\n<h2>四、)",
        lambda m: (
            '<section class="route-section-card">'
            f'<h3 class="route-section-title">{m.group(1)}</h3>'
            f'<div class="route-section-body">{format_route_section_body(m.group(1), m.group("body").strip())}</div>'
            '</section>'
        ),
        html_text,
        flags=re.S,
    )
    html_text = html_text.replace(
        '<td style="text-align:left">有效</td>',
        '<td style="text-align:left"><span class="status-badge status-active">有效</span></td>',
    )
    html_text = html_text.replace(
        '<td style="text-align:left">失效</td>',
        '<td style="text-align:left"><span class="status-badge status-inactive">失效</span></td>',
    )
    html_text = html_text.replace(
        '<td style="text-align:left">已失效</td>',
        '<td style="text-align:left"><span class="status-badge status-inactive">已失效</span></td>',
    )
    html_text = html_text.replace(
        '<td style="text-align:left">申请中</td>',
        '<td style="text-align:left"><span class="status-badge status-pending">申请中</span></td>',
    )
    html_text = html_text.replace(
        '<td style="text-align:left">审中</td>',
        '<td style="text-align:left"><span class="status-badge status-pending">审中</span></td>',
    )
    return html_text


def evidence_kind_class(kind: str) -> str:
    mapping = {
        "工程案例/标准": "case",
        "论文": "paper",
        "专利": "patent",
        "Web 学术补充": "web",
    }
    return mapping.get(kind.strip(), "generic")


def appendix_kind_class(title: str) -> str:
    if title.startswith("A1"):
        return "case"
    if title.startswith("A2"):
        return "paper"
    if title.startswith("A3"):
        return "patent"
    if title.startswith("A4"):
        return "web"
    return "generic"


def format_route_section_body(title: str, body: str) -> str:
    if "研发路线总结" not in title:
        return body
    return body.replace(
        "<table>",
        '<table class="evidence-table route-summary-table">',
        1,
    )


def validate_step4_html(html_text: str) -> None:
    required = [
        "科研需求检索报告",
        "需求输入原文",
        "一、项目需求解析",
        "二、技术难题拆解",
        "三、主要研究内容和措施",
        "3.1 检索成果汇总",
        "研发路线总结",
        "四、主要科研单位分析",
        "五、附录",
        "A1 工程案例 / 标准清单",
        "A2 论文清单",
        "A3 专利清单",
        "A4 网络学术清单",
    ]
    missing = [item for item in required if item not in html_text]
    if missing:
        raise ValueError("HTML report missing Step 4 sections: " + ", ".join(missing))


def strip_html_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s).strip()


def add_toc_ids(html_text: str) -> tuple[str, List[Dict[str, str]]]:
    toc_items: List[Dict[str, str]] = []
    seq = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal seq
        level = match.group("level")
        attrs = match.group("attrs") or ""
        inner = match.group("inner")
        label = strip_html_tags(inner)
        include = label != "科研需求检索报告" and (
            level == "2" or label.startswith("3.")
        )
        if label.startswith("A"):
            include = False
        if not include:
            return match.group(0)

        seq += 1
        anchor = f"toc-{seq}"
        toc_items.append({"id": anchor, "label": label, "level": level})
        if re.search(r'\sid="[^"]*"', attrs):
            return match.group(0)
        return f'<h{level} id="{anchor}"{attrs}>{inner}</h{level}>'

    html_text = re.sub(
        r"<h(?P<level>[23])(?P<attrs>[^>]*)>(?P<inner>.*?)</h(?P=level)>",
        repl,
        html_text,
        flags=re.S,
    )
    return html_text, toc_items


def render_report_toc(toc_items: List[Dict[str, str]]) -> str:
    if not toc_items:
        return ""
    items = "".join(
        f'<li class="toc-level-{esc(item["level"])}"><a href="#{esc(item["id"])}">{esc(item["label"])}</a></li>'
        for item in toc_items
    )
    return (
        '<section class="report-toc">'
        '<h2 class="report-toc-title">📋 报告目录</h2>'
        f'<ul class="report-toc-list">{items}</ul>'
        '</section>'
    )


def render_page_header(payload: Dict[str, Any]) -> str:
    meta = _get(payload, "meta") or {}
    project_name = md_text(_get(meta, "project_name"))
    project_short = (
        md_text(_get(meta, "project_short"))
        or project_name
        or "科研需求项目"
    )
    applicant = md_text(_get(meta, "applicant"))
    today_iso = md_text(_get(meta, "today_iso"))
    scope = md_text(_get(meta, "scope")) or "专利+论文+网络学术文献补充"

    chips = []
    chips.append(("🏢", "申请单位：", applicant or "未提及"))
    if today_iso:
        chips.append(("📅", "检索日期：", today_iso))
    chips.append(("🔍", "检索范围：", scope))
    chip_html = "".join(
        f'<div class="hero-chip"><span>{esc(icon)}</span>{esc(label)}{esc(value)}</div>'
        for icon, label, value in chips
    )

    return (
        '<header class="hero-header">'
        '<div class="container">'
        '<h1>科研需求检索报告</h1>'
        f'<p class="hero-subtitle">{esc(project_name or project_short)}</p>'
        f'<div class="hero-meta">{chip_html}</div>'
        '</div>'
        '</header>'
    )


def build_html(payload: Dict[str, Any]) -> str:
    payload = normalize_payload(payload)
    project_short = (
        _get(payload, "meta", "project_short")
        or _get(payload, "meta", "project_name")
        or "科研需求"
    )
    title = "科研需求检索报告"
    markdown_text = build_report_markdown(payload)
    report_html = render_markdown_report(markdown_text)
    validate_step4_html(report_html)
    report_html, toc_items = add_toc_ids(report_html)
    head = (
        '<!DOCTYPE html>'
        '<html lang="zh-CN"><head>'
        '<meta charset="UTF-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
        f'<title>{esc(title)}</title>'
        f'<style>{CSS}{CSS_PART2}{REPORT_CSS}</style>'
        '</head><body>'
    )
    body = (
        render_page_header(payload)
        + '<main class="container">'
        + render_report_toc(toc_items)
        + f'<article class="markdown-report" data-project="{esc(project_short)}">'
        + report_html
        + '</article>'
        + '</main>'
        + render_footer(payload)
    )
    tail = "</body></html>"
    return head + body + tail


def build_report_markdown(payload: Dict[str, Any]) -> str:
    payload = normalize_payload(payload)
    return md_text(_get(payload, "markdown_report")) or build_markdown_report(payload)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render rd-direction-finder payload JSON into HTML and optional Markdown reports."
    )
    parser.add_argument("--payload", required=True, help="Path to payload JSON")
    parser.add_argument("--output", required=True, help="Path to output HTML")
    parser.add_argument("--markdown-output", help="Optional path to output Markdown report")
    args = parser.parse_args()

    payload_path = Path(args.payload)
    output_path = Path(args.output)
    markdown_output_path = Path(args.markdown_output) if args.markdown_output else None

    if not payload_path.is_file():
        print(f"[err] payload not found: {payload_path}")
        return 2

    try:
        payload = json.loads(payload_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"[err] payload is not valid JSON: {e}")
        return 2

    if not isinstance(payload, dict):
        print("[err] payload root must be a JSON object")
        return 2

    markdown_text = build_report_markdown(payload)
    html_text = build_html(payload)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_text, encoding="utf-8")
    size = output_path.stat().st_size
    if size <= 0:
        print(f"[err] output is empty: {output_path}")
        return 1
    print(f"[ok] report written -> {output_path}")
    if markdown_output_path:
        markdown_output_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_output_path.write_text(markdown_text, encoding="utf-8")
        markdown_size = markdown_output_path.stat().st_size
        if markdown_size <= 0:
            print(f"[err] markdown output is empty: {markdown_output_path}")
            return 1
        print(f"[ok] markdown written -> {markdown_output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

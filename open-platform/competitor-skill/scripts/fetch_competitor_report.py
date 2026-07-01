#!/usr/bin/env python3
"""竞争对手专利报告：给定 PatSnap 检索式，检索并输出 Markdown 报告。"""
import sys
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent))
import config as _cfg
from fetch_literature import fetch_literature_for_query, render_literature_section, ai_summarize_literature
import requests


def _auth_headers():
    return {"Authorization": f"Bearer {_cfg.PATSNAP_API_KEY}"}


def _batched(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def extract_companies_from_query(query):
    """从检索式中提取 TREE@"..." 的公司全称列表。无则返回 ['全部']。"""
    if not query:
        return ["全部"]
    names = re.findall(r'TREE@"([^"]+)"', query)
    if names:
        return names
    # 尝试提取 ALL_AN:("...") 中的名称
    names = re.findall(r'ALL_AN:\("([^"]+)"', query)
    return names if names else ["全部"]


def match_company(assignee, companies):
    """将 original_assignee 匹配到公司列表中最接近的一项。"""
    if companies == ["全部"]:
        return "全部"
    assignee = assignee or ""
    for c in companies:
        if c in assignee or assignee in c:
            return c
    return "其他"


def search(query, limit=200):
    url = f"{_cfg.PATSNAP_BASE_URL}/search/patent/query-search-patent"
    payload = {
        "sort": [{"field": "PBDT_YEARMONTHDAY", "order": "DESC"}],
        "limit": limit,
        "offset": 0,
        "query_text": query,
        "collapse_by": "PBD",
        "collapse_type": "DOCDB",
        "collapse_order": "LATEST",
    }
    resp = requests.post(url, json=payload, headers=_auth_headers(), timeout=30)
    resp.raise_for_status()
    return resp.json().get("data", {}).get("results", [])


def get_legal(patent_ids):
    if not patent_ids:
        return {}
    url = f"{_cfg.PATSNAP_BASE_URL}/basic-patent-data/legal-status"
    mapping = {}
    for batch in _batched(patent_ids, 30):
        resp = requests.get(url, params={"patent_id": ",".join(batch)},
                            headers=_auth_headers(), timeout=20)
        resp.raise_for_status()
        for item in resp.json().get("data", []):
            legal = item.get("patent_legal", {})
            raw = legal.get("legal_status", [])
            mapping[item.get("patent_id")] = raw[-1] if raw else "Unknown"
    return mapping


def _extract_text_field(field):
    """从 [{lang, text}] 列表中优先取中文，否则取第一条。"""
    if not field:
        return ""
    if isinstance(field, str):
        return field
    cn = next((x.get("text", "") for x in field if x.get("lang") == "CN"), "")
    return cn or field[0].get("text", "")


def get_patent_detail(patent_ids):
    """并发获取专利标题、申请人、申请日、公开日，返回 {patent_id: dict}。"""
    if not patent_ids:
        return {}
    from concurrent.futures import ThreadPoolExecutor, as_completed
    url = f"{_cfg.PATSNAP_BASE_URL}/basic-patent-data/patent-detail"

    def fetch_one(pid):
        try:
            resp = requests.get(url, params={"patent_id": pid, "lang": "cn"},
                                headers=_auth_headers(), timeout=20)
            resp.raise_for_status()
            item = resp.json().get("data") or {}
            if not item or not item.get("patent_id"):
                return pid, None
            bib = item.get("bibliographic_data", {})
            applicants = bib.get("applicants") or bib.get("assignees") or []
            assignee = "、".join(a.get("name", "") for a in applicants if a.get("name"))
            apdt = str(bib.get("application_reference", {}).get("date", ""))
            pbdt = str(bib.get("publication_reference", {}).get("date", ""))
            return pid, {
                "title": _extract_text_field(item.get("title", "")),
                "original_assignee": assignee,
                "apdt": apdt,
                "pbdt": pbdt,
            }
        except Exception as e:
            print(f"[警告] patent-detail 失败 ({pid}): {e}", file=sys.stderr)
            return pid, None

    mapping = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(fetch_one, pid): pid for pid in patent_ids}
        for future in as_completed(futures):
            pid, detail = future.result()
            if detail:
                mapping[pid] = detail
    return mapping


def get_ai_summary(patent_ids):
    if not patent_ids:
        return {}
    url = f"{_cfg.PATSNAP_BASE_URL}/high-value-data/tech-problem-and-benefit-summary"
    mapping = {}
    for batch in _batched(patent_ids, 30):
        resp = requests.get(url, params={"patent_id": ",".join(batch), "lang": "cn"},
                            headers=_auth_headers(), timeout=20)
        resp.raise_for_status()
        for item in resp.json().get("data", []):
            pid = item.get("patent_id")
            mapping[pid] = {
                "patsnap_title": item.get("patsnap_title"),
                "benefit_summary": "".join(
                    item.get("benefit_summary", {}).get("benefit_para", [])),
                "tech_problem_summary": "".join(
                    item.get("tech_problem_summary", {}).get("tech_problem_para", [])),
                "technical_approach_summary": "".join(
                    item.get("technical_approach_summary", {}).get("technical_approach_para", [])),
            }
    return mapping


def get_abstract_figures(patent_ids, images_dir=None):
    if not patent_ids:
        return {}
    url = f"{_cfg.PATSNAP_BASE_URL}/basic-patent-data/abstract-image"
    mapping = {}
    for batch in _batched(patent_ids, 30):
        try:
            resp = requests.get(url, params={"patent_id": ",".join(batch)},
                                headers=_auth_headers(), timeout=15)
            resp.raise_for_status()
            for item in resp.json().get("data", []):
                pid = item.get("patent_id")
                fig_url = item.get("abstract_drawing", {}).get("path")
                if pid and fig_url:
                    if images_dir:
                        # 下载图片到本地
                        try:
                            img_resp = requests.get(fig_url, timeout=15)
                            img_resp.raise_for_status()
                            ext = fig_url.split("?")[0].rsplit(".", 1)[-1] or "jpg"
                            local_path = images_dir / f"{pid}.{ext}"
                            local_path.write_bytes(img_resp.content)
                            mapping[pid] = str(local_path)
                        except Exception as e:
                            print(f"[警告] 图片下载失败 {pid}: {e}", file=sys.stderr)
                            mapping[pid] = fig_url
                    else:
                        mapping[pid] = fig_url
        except Exception:
            pass
    return mapping


def get_technology_topics(patent_ids):
    """批量获取专利技术主题标签（中文），返回 {patent_id: first_topic_str}。"""
    if not patent_ids:
        return {}
    url = f"{_cfg.PATSNAP_BASE_URL}/high-value-data/technology-topic"
    mapping = {}
    for batch in _batched(patent_ids, 30):
        try:
            resp = requests.get(url, params={"patent_id": ",".join(batch), "lang": "cn"},
                                headers=_auth_headers(), timeout=20)
            resp.raise_for_status()
            for item in resp.json().get("data", []):
                pid = item.get("patent_id")
                topics = item.get("technology_topic_data", [])
                if pid and topics:
                    mapping[pid] = topics[0]
        except Exception as e:
            print(f"[警告] technology-topic API 失败: {e}", file=sys.stderr)
    return mapping


def classify_patents(items):
    """用 technology-topic API 获取每篇专利的技术主题，取第一个标签作为分支。无标签时归入'其他'。"""
    ids = [r.get("patent_id") for r in items if r.get("patent_id")]
    topic_map = get_technology_topics(ids)
    for item in items:
        pid = item.get("patent_id")
        item["_branch"] = topic_map.get(pid) or "其他"


def render_report(companies, report_title, raw_query, all_results):
    """生成标准 Markdown 格式报告。"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [f"# {report_title}", "", f"> 生成时间：{now}", ""]

    # === 一、新公开专利概况 ===
    lines += ["## 一、新公开专利概况", ""]
    lines.append(f"- **检索式**：`{raw_query[:200]}{'...' if len(raw_query) > 200 else ''}`")
    lines.append(f"- **专利总数**：{len(all_results)}")
    lines.append("")

    company_counts = defaultdict(int)
    for r in all_results:
        company_counts[r.get("_company", "N/A")] += 1

    lines.append("| 公司 | 专利数 |")
    lines.append("|------|--------|")
    for company in companies:
        cnt = company_counts.get(company, 0)
        lines.append(f"| {company} | {cnt} |")
    if "其他" in company_counts:
        lines.append(f"| 其他 | {company_counts['其他']} |")
    lines.append("")

    # === 二、专利技术总结 ===
    lines += ["## 二、专利技术总结", ""]
    for company in companies:
        company_patents = [r for r in all_results if r.get("_company") == company]
        if not company_patents:
            continue
        lines.append(f"### {company}（{len(company_patents)} 件）")
        branch_counts = defaultdict(int)
        for r in company_patents:
            branch_counts[r.get("_branch", "其他")] += 1
        top_branches = sorted(branch_counts.items(), key=lambda x: -x[1])[:4]
        lines.append(f"- **主要技术方向**：{'、'.join(f'{b}（{n}件）' for b, n in top_branches)}")
        for r in company_patents[:3]:
            summary = (r.get("technical_approach_summary") or r.get("tech_problem_summary") or r.get("title") or "")
            if summary:
                lines.append(f"- **代表性技术**：{summary[:120]}")
        lines.append("")

    # === 三、专利详情 ===
    lines += ["## 三、专利详情", ""]
    for company in companies:
        company_patents = [r for r in all_results if r.get("_company") == company]
        if not company_patents:
            continue
        lines.append(f"### {company}（{len(company_patents)} 件）")
        by_branch = defaultdict(list)
        for r in company_patents:
            by_branch[r.get("_branch", "其他")].append(r)
        for branch, patents in sorted(by_branch.items(), key=lambda kv: (kv[0] == "其他", -len(kv[1]))):
            lines.append(f"#### {branch}（{len(patents)} 件）")
            for r in patents:
                pn = r.get("pn", "N/A")
                pid = r.get("patent_id", "")
                url = f"https://analytics.zhihuiya.com/patent-view/abst?_type=query&source_type=search_result&rows=20&patentId={pid}" if pid else ""
                pn_display = f"[{pn}]({url})" if url else pn
                lines.append(f"##### {pn_display}")
                lines.append(f"- **标题**：{r.get('title', 'N/A')}")
                lines.append(f"- **法律状态**：{r.get('legal_status', 'N/A')}")
                lines.append(f"- **申请人**：{r.get('original_assignee', 'N/A')}")
                lines.append(f"- **申请日**：{r.get('apdt', 'N/A')}")
                lines.append(f"- **公开日**：{r.get('pbdt', 'N/A')}")
                if r.get("tech_problem_summary"):
                    lines.append(f"- **技术问题**：{r['tech_problem_summary']}")
                if r.get("technical_approach_summary"):
                    lines.append(f"- **技术手段**：{r['technical_approach_summary']}")
                if r.get("benefit_summary"):
                    lines.append(f"- **技术功效**：{r['benefit_summary']}")
                if r.get("fig_url"):
                    lines.append(f'- **摘要附图**：![{pn}]({r["fig_url"]})')
                lines.append("")
        lines.append("")

    return "\n".join(lines)



def main():
    args = sys.argv[1:]
    if len(args) < 1:
        print("用法: fetch_competitor_report.py <检索式> [报告标题] [数量]", file=sys.stderr)
        sys.exit(1)

    # 检测 API Key 是否已配置
    if not _cfg.PATSNAP_API_KEY:
        env_path = Path(__file__).parent / ".env"
        print("[配置] 未检测到智慧芽 API Key。", file=sys.stderr)
        print("[配置] 请前往 https://connect.zhihuiya.com 获取 API Key（格式：sk-xxx）", file=sys.stderr)
        print(f"[配置] 然后将以下内容写入 {env_path}：", file=sys.stderr)
        print(f"[配置]   PATSNAP_API_KEY=sk-你的APIKey", file=sys.stderr)
        sys.exit(1)

    raw_query = args[0]
    report_title = args[1] if len(args) > 1 else "专利检索报告"
    limit = int(args[2]) if len(args) > 2 and args[2].isdigit() else 200

    companies = extract_companies_from_query(raw_query)
    print(f"[检索] 识别公司: {companies}", file=sys.stderr)
    print(f"[检索] 检索式: {raw_query[:120]}...", file=sys.stderr)

    results = search(raw_query, limit)

    if not results:
        md_content = f"# {report_title}\n\n## 检索结果\n\n- 未命中任何专利，请检查检索式。\n"
        print(md_content)
        return

    # 过滤外观设计专利
    DESIGN_PREFIXES = ("CN3", "USD", "KRD")
    results = [r for r in results if not any(
        (r.get("pn", "") or "").startswith(p) for p in DESIGN_PREFIXES
    )]

    ids = [r.get("patent_id") for r in results if r.get("patent_id")]
    print(f"[检索] 获取著录项目...", file=sys.stderr)
    detail_map = get_patent_detail(ids)
    legal_map = get_legal(ids)
    ai_map = get_ai_summary(ids)

    # 匹配公司（用 detail_map 里的 original_assignee）
    for r in results:
        pid = r.get("patent_id")
        assignee = detail_map.get(pid, {}).get("original_assignee", "") or r.get("original_assignee", "") or ""
        r["_company"] = match_company(assignee, companies)

    merged = []
    for r in results:
        pid = r.get("patent_id")
        ai = ai_map.get(pid, {})
        detail = detail_map.get(pid, {})
        merged.append({**r,
            "title": detail.get("title") or r.get("title") or ai.get("patsnap_title") or "N/A",
            "original_assignee": detail.get("original_assignee") or r.get("original_assignee", "N/A"),
            "apdt": detail.get("apdt") or r.get("apdt", "N/A"),
            "pbdt": detail.get("pbdt") or r.get("pbdt", "N/A"),
            "legal_status": legal_map.get(pid, "N/A"),
            "tech_problem_summary": ai.get("tech_problem_summary", ""),
            "technical_approach_summary": ai.get("technical_approach_summary", ""),
            "benefit_summary": ai.get("benefit_summary", ""),
        })

    if not merged:
        print(f"# {report_title}\n\n## 检索结果\n\n- 未命中任何专利，请检查检索式。\n")
        return

    # 输出到 reports/ 目录
    reports_dir = Path(__file__).parent.parent / "reports"
    reports_dir.mkdir(exist_ok=True)
    images_dir = reports_dir / "images"
    images_dir.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 摘要附图：下载到 images/ 目录
    print(f"[附图] 正在下载摘要附图...", file=sys.stderr)
    fig_map = get_abstract_figures(
        list(set(r.get("patent_id") for r in merged if r.get("patent_id"))),
        images_dir=images_dir,
    )
    for r in merged:
        pid = r.get("patent_id")
        if pid and pid in fig_map:
            local_path = fig_map[pid]
            # HTML 用相对路径 images/xxx.jpg
            r["fig_url"] = f"images/{Path(local_path).name}"

    classify_patents(merged)

    md_content = render_report(companies, report_title, raw_query, merged)

    # 追加期刊文献部分
    print(f"[文献] 正在检索相关期刊文献...", file=sys.stderr)
    lit_results, lit_total, lit_query = fetch_literature_for_query(raw_query, limit=20)
    print(f"[文献] 正在生成 AI 总结...", file=sys.stderr)
    ai_summary = ai_summarize_literature(lit_results) if lit_results else ""
    lit_section = render_literature_section(lit_results, lit_total, lit_query, ai_summary)
    md_content = md_content.rstrip() + "\n\n" + lit_section

    md_path = reports_dir / f"report_{ts}.md"
    html_path = reports_dir / f"report_{ts}.html"

    md_path.write_text(md_content, encoding="utf-8")
    print(f"[输出] MD  → {md_path}", file=sys.stderr)

    # 生成 HTML
    sys.path.insert(0, str(Path(__file__).parent))
    from render_html import parse_md, render_html as _render_html
    html_content = _render_html(parse_md(md_content))
    html_path.write_text(html_content, encoding="utf-8")
    print(f"[输出] HTML → {html_path}", file=sys.stderr)

    print(md_content)


if __name__ == "__main__":
    main()

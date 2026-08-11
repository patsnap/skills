#!/usr/bin/env python3
"""Retrieve a PatSnap query and render a competitor patent report."""
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
    _, api_key = _cfg.patent_api_settings()
    return {"Authorization": f"Bearer {api_key}"}


def _base_url():
    """Return the explicitly configured, verified PatSnap REST base URL."""
    base_url, _ = _cfg.patent_api_settings()
    return base_url.rstrip("/")


def _batched(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def extract_companies_from_query(query):
    """Extract company names from TREE@ or ALL_AN expressions."""
    if not query:
        return ["All applicants"]
    names = re.findall(r'TREE@"([^"]+)"', query)
    if names:
        return names
    # Fall back to quoted names inside ALL_AN:(...).
    names = re.findall(r'ALL_AN:\("([^"]+)"', query)
    return names if names else ["All applicants"]


def match_company(assignee, companies):
    """Map an original-assignee string to a requested company label."""
    if companies == ["All applicants"]:
        return "All applicants"
    assignee = assignee or ""
    for c in companies:
        if c in assignee or assignee in c:
            return c
    return "Other"


def search(query, limit=200):
    """Run the verified v2 query-search endpoint."""
    url = f"{_base_url()}/search/patent/query-search-patent/v2"
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
    url = f"{_base_url()}/basic-patent-data/simple-legal-status"
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
    """Prefer English text in a list of language/text objects."""
    if not field:
        return ""
    if isinstance(field, str):
        return field
    english = next(
        (x.get("text", "") for x in field if str(x.get("lang", "")).upper() in {"EN", "ENG"}),
        "",
    )
    return english or field[0].get("text", "")


def get_patent_detail(patent_ids):
    """Fetch bibliography concurrently and return a patent-ID mapping."""
    if not patent_ids:
        return {}
    from concurrent.futures import ThreadPoolExecutor, as_completed
    url = f"{_base_url()}/basic-patent-data/bibliography"

    def fetch_one(pid):
        try:
            resp = requests.get(url, params={"patent_id": pid, "lang": "en"},
                                headers=_auth_headers(), timeout=20)
            resp.raise_for_status()
            item = resp.json().get("data") or {}
            if not item or not item.get("patent_id"):
                return pid, None
            bib = item.get("bibliographic_data", {})
            applicants = bib.get("applicants") or bib.get("assignees") or []
            assignee = "; ".join(a.get("name", "") for a in applicants if a.get("name"))
            apdt = str(bib.get("application_reference", {}).get("date", ""))
            pbdt = str(bib.get("publication_reference", {}).get("date", ""))
            return pid, {
                "title": _extract_text_field(item.get("title", "")),
                "original_assignee": assignee,
                "apdt": apdt,
                "pbdt": pbdt,
            }
        except Exception as e:
            print(f"[WARNING] Bibliography retrieval failed ({pid}): {e}", file=sys.stderr)
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
    url = f"{_base_url()}/high-value-data/tech-problem-and-benefit-summary"
    mapping = {}
    for batch in _batched(patent_ids, 30):
        resp = requests.get(url, params={"patent_id": ",".join(batch), "lang": "en"},
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
    url = f"{_base_url()}/search/patent/intelligent-attached-image"
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
                        # Download a retrieved patent image into the report fixture directory.
                        try:
                            img_resp = requests.get(fig_url, timeout=15)
                            img_resp.raise_for_status()
                            ext = fig_url.split("?")[0].rsplit(".", 1)[-1] or "jpg"
                            local_path = images_dir / f"{pid}.{ext}"
                            local_path.write_bytes(img_resp.content)
                            mapping[pid] = str(local_path)
                        except Exception as e:
                            print(f"[WARNING] Image download failed ({pid}): {e}", file=sys.stderr)
                            mapping[pid] = fig_url
                    else:
                        mapping[pid] = fig_url
        except Exception:
            pass
    return mapping


def get_technology_topics(patent_ids):
    """Fetch the first available English technology-topic label."""
    if not patent_ids:
        return {}
    url = f"{_base_url()}/high-value-data/technology-topic"
    mapping = {}
    for batch in _batched(patent_ids, 30):
        try:
            resp = requests.get(url, params={"patent_id": ",".join(batch), "lang": "en"},
                                headers=_auth_headers(), timeout=20)
            resp.raise_for_status()
            for item in resp.json().get("data", []):
                pid = item.get("patent_id")
                topics = item.get("technology_topic_data", [])
                if pid and topics:
                    mapping[pid] = topics[0]
        except Exception as e:
            print(f"[WARNING] Technology-topic retrieval failed: {e}", file=sys.stderr)
    return mapping


def classify_patents(items):
    """Assign the first retrieved topic, or Other when no topic is available."""
    ids = [r.get("patent_id") for r in items if r.get("patent_id")]
    topic_map = get_technology_topics(ids)
    for item in items:
        pid = item.get("patent_id")
        item["_branch"] = topic_map.get(pid) or "Other"


def render_report(companies, report_title, raw_query, all_results):
    """Render the normalized records as a three-part Markdown report."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [f"# {report_title}", "", f"> Generated: {now}", ""]

    # Part 1: recently published patent overview.
    lines += ["## Part 1: Recently published patent overview", ""]
    lines.append(f"- **Query:** `{raw_query[:200]}{'...' if len(raw_query) > 200 else ''}`")
    lines.append(f"- **Returned records:** {len(all_results)}")
    lines.append("")

    company_counts = defaultdict(int)
    for r in all_results:
        company_counts[r.get("_company", "Not available")] += 1

    lines.append("| Company or applicant group | Record count |")
    lines.append("|---|---:|")
    for company in companies:
        cnt = company_counts.get(company, 0)
        lines.append(f"| {company} | {cnt} |")
    if "Other" in company_counts:
        lines.append(f"| Other | {company_counts['Other']} |")
    lines.append("")

    # Part 2: company technology summaries.
    lines += ["## Part 2: Company technology summaries", ""]
    for company in companies:
        company_patents = [r for r in all_results if r.get("_company") == company]
        if not company_patents:
            continue
        lines.append(f"### {company} ({len(company_patents)} records)")
        branch_counts = defaultdict(int)
        for r in company_patents:
            branch_counts[r.get("_branch", "Other")] += 1
        top_branches = sorted(branch_counts.items(), key=lambda x: -x[1])[:4]
        lines.append(f"- **Leading observed topics:** {'; '.join(f'{b} ({n})' for b, n in top_branches)}")
        for r in company_patents[:3]:
            summary = (r.get("technical_approach_summary") or r.get("tech_problem_summary") or r.get("title") or "")
            if summary:
                lines.append(f"- **Representative technical approach:** {summary[:120]}")
        lines.append("")

    # Part 3: detailed patent records.
    lines += ["## Part 3: Patent details", ""]
    for company in companies:
        company_patents = [r for r in all_results if r.get("_company") == company]
        if not company_patents:
            continue
        lines.append(f"### {company} ({len(company_patents)} records)")
        by_branch = defaultdict(list)
        for r in company_patents:
            by_branch[r.get("_branch", "Other")].append(r)
        for branch, patents in sorted(by_branch.items(), key=lambda kv: (kv[0] == "Other", -len(kv[1]))):
            lines.append(f"#### {branch} ({len(patents)} records)")
            for r in patents:
                pn = r.get("pn", "N/A")
                pid = r.get("patent_id", "")
                url = f"https://analytics.patsnap.com/patent-view/abst?patentId={pid}" if pid else ""
                pn_display = f"[{pn}]({url})" if url else pn
                lines.append(f"##### {pn_display}")
                lines.append(f"- **Title:** {r.get('title', 'Not available')}")
                lines.append(f"- **Legal status:** {r.get('legal_status', 'Unverified')}")
                lines.append(f"- **Original applicant:** {r.get('original_assignee', 'Not available')}")
                lines.append(f"- **Application date:** {r.get('apdt', 'Not available')}")
                lines.append(f"- **Publication date:** {r.get('pbdt', 'Not available')}")
                if r.get("tech_problem_summary"):
                    lines.append(f"- **Technical problem:** {r['tech_problem_summary']}")
                if r.get("technical_approach_summary"):
                    lines.append(f"- **Technical approach:** {r['technical_approach_summary']}")
                if r.get("benefit_summary"):
                    lines.append(f"- **Technical benefit:** {r['benefit_summary']}")
                if r.get("fig_url"):
                    lines.append(f'- **Abstract drawing:** ![{pn} patent drawing]({r["fig_url"]})')
                lines.append("")
        lines.append("")

    return "\n".join(lines)



def main():
    args = sys.argv[1:]
    if len(args) < 1:
        print("Usage: fetch_competitor_report.py <query> [report-title] [limit]", file=sys.stderr)
        sys.exit(1)

    # Fail closed unless an explicitly verified REST endpoint and key are supplied.
    try:
        _cfg.patent_api_settings()
    except RuntimeError as exc:
        print(f"[CONFIGURATION] {exc}", file=sys.stderr)
        print("[CONFIGURATION] Preferred fallback: use the Advanced Patent Search MCP server.", file=sys.stderr)
        sys.exit(1)

    raw_query = args[0]
    report_title = args[1] if len(args) > 1 else "Patent search report"
    limit = int(args[2]) if len(args) > 2 and args[2].isdigit() else 200

    companies = extract_companies_from_query(raw_query)
    print(f"[SEARCH] Identified company labels: {companies}", file=sys.stderr)
    print(f"[SEARCH] Query: {raw_query[:120]}...", file=sys.stderr)

    results = search(raw_query, limit)

    if not results:
        md_content = f"# {report_title}\n\n## Search result\n\n- No patent records matched. Review the query and scope.\n"
        print(md_content)
        return

    # Preserve the source workflow's explicit design-publication exclusion.
    DESIGN_PREFIXES = ("CN3", "USD", "KRD")
    results = [r for r in results if not any(
        (r.get("pn", "") or "").startswith(p) for p in DESIGN_PREFIXES
    )]

    ids = [r.get("patent_id") for r in results if r.get("patent_id")]
    print("[SEARCH] Retrieving bibliography and enrichment fields...", file=sys.stderr)
    detail_map = get_patent_detail(ids)
    legal_map = get_legal(ids)
    ai_map = get_ai_summary(ids)

    # Match companies using the original-applicant field.
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
            "title": detail.get("title") or r.get("title") or ai.get("patsnap_title") or "Not available",
            "original_assignee": detail.get("original_assignee") or r.get("original_assignee", "Not available"),
            "apdt": detail.get("apdt") or r.get("apdt", "Not available"),
            "pbdt": detail.get("pbdt") or r.get("pbdt", "Not available"),
            "legal_status": legal_map.get(pid, "Unverified"),
            "tech_problem_summary": ai.get("tech_problem_summary", ""),
            "technical_approach_summary": ai.get("technical_approach_summary", ""),
            "benefit_summary": ai.get("benefit_summary", ""),
        })

    if not merged:
        print(f"# {report_title}\n\n## Search result\n\n- No patent records matched. Review the query and scope.\n")
        return

    # Write report artifacts under reports/.
    reports_dir = Path(__file__).parent.parent / "reports"
    reports_dir.mkdir(exist_ok=True)
    images_dir = reports_dir / "images"
    images_dir.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Download available abstract drawings into reports/images/.
    print("[IMAGES] Downloading available patent drawings...", file=sys.stderr)
    fig_map = get_abstract_figures(
        list(set(r.get("patent_id") for r in merged if r.get("patent_id"))),
        images_dir=images_dir,
    )
    for r in merged:
        pid = r.get("patent_id")
        if pid and pid in fig_map:
            local_path = fig_map[pid]
            # HTML consumes a relative images/<file> path.
            r["fig_url"] = f"images/{Path(local_path).name}"

    classify_patents(merged)

    md_content = render_report(companies, report_title, raw_query, merged)

    # Append an optional, separately labeled literature section.
    print("[LITERATURE] Retrieving related literature when configured...", file=sys.stderr)
    lit_results, lit_total, lit_query = fetch_literature_for_query(raw_query, limit=20)
    print("[LITERATURE] Generating a summary only when an approved provider is configured...", file=sys.stderr)
    ai_summary = ai_summarize_literature(lit_results) if lit_results else ""
    lit_section = render_literature_section(lit_results, lit_total, lit_query, ai_summary)
    md_content = md_content.rstrip() + "\n\n" + lit_section

    md_path = reports_dir / f"report_{ts}.md"
    html_path = reports_dir / f"report_{ts}.html"

    md_path.write_text(md_content, encoding="utf-8")
    print(f"[OUTPUT] Markdown: {md_path}", file=sys.stderr)

    # Render the corresponding HTML report.
    sys.path.insert(0, str(Path(__file__).parent))
    from render_html import parse_md, render_html as _render_html
    html_content = _render_html(parse_md(md_content))
    html_path.write_text(html_content, encoding="utf-8")
    print(f"[OUTPUT] HTML: {html_path}", file=sys.stderr)

    print(md_content)


if __name__ == "__main__":
    main()

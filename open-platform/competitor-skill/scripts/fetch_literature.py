#!/usr/bin/env python3
"""从 PatSnap 检索式提取关键词和时间，检索期刊文献，返回结构化结果列表。"""
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import config as _cfg
import requests


def _patsnap_date_to_ts(date_str):
    """将 PatSnap 日期字符串（如 20251201）转为毫秒时间戳。"""
    try:
        dt = datetime.strptime(date_str.strip(), "%Y%m%d").replace(tzinfo=timezone.utc)
        return int(dt.timestamp() * 1000)
    except ValueError:
        return None


def extract_keywords_from_query(query):
    """从 PatSnap 检索式中提取关键词，用于文献检索的 query_text。

    策略：
    1. 提取 TAC_all:(...)、TAC:(...)、MAINF:(...)、TTL:(...)、ABST:(...) 括号内的词
    2. 去掉字段名、布尔运算符、引号，保留实质关键词
    3. 拼成 title:(...) 形式
    """
    if not query:
        return ""

    # 提取各文本字段括号内的内容
    field_pattern = re.compile(
        r'(?:TAC_all|TAC|TACD|MAINF|TTL|ABST|CLMS|DESC|TA)\s*:\s*\(([^)]+)\)',
        re.IGNORECASE,
    )
    matches = field_pattern.findall(query)

    if not matches:
        # 没有括号字段，尝试直接提取引号内词
        matches = re.findall(r'"([^"]+)"', query)

    # 合并所有匹配内容，提取引号内的词或裸词
    keywords = []
    for m in matches:
        # 提取引号内的词
        quoted = re.findall(r'"([^"]+)"', m)
        if quoted:
            keywords.extend(quoted)
        else:
            # 去掉布尔运算符，保留词
            words = re.sub(r'\b(AND|OR|NOT)\b', ' ', m, flags=re.IGNORECASE)
            words = re.sub(r'["\(\)]', ' ', words).split()
            keywords.extend(w for w in words if len(w) > 1)

    if not keywords:
        return ""

    # 去重保序
    seen = set()
    unique = []
    for k in keywords:
        if k not in seen:
            seen.add(k)
            unique.append(k)

    # 构造 title:(kw1 OR kw2 ...) 形式
    kw_str = " OR ".join(f'"{k}"' if " " in k else k for k in unique[:6])
    return f"title:({kw_str})"


def extract_date_range_from_query(query):
    """从 PatSnap 检索式中提取 PBD 或 APD 日期范围，返回 (start_ts_ms, end_ts_ms) 或 (None, None)。"""
    if not query:
        return None, None

    pattern = re.compile(r'(?:PBD|APD)\s*:\s*\[(\d{8})\s+TO\s+(\d{8})\]', re.IGNORECASE)
    m = pattern.search(query)
    if not m:
        return None, None

    start_ts = _patsnap_date_to_ts(m.group(1))
    end_ts = _patsnap_date_to_ts(m.group(2))
    return start_ts, end_ts


def search_literature(query_text, date_time_str=None, limit=10):
    """调用期刊文献检索 API，返回结果列表。"""
    if not _cfg.LITERATURE_API_KEY:
        print("[配置] 未检测到文献检索 API Key，已跳过期刊文献检索。", file=sys.stderr)
        return [], 0

    url = f"{_cfg.PATSNAP_BASE_URL}/search/literature/query-search"
    payload = {
        "query_text": query_text,
        "limit": limit,
        "offset": 0,
    }
    if date_time_str:
        payload["date_time"] = date_time_str

    resp = requests.post(url, headers=_lit_headers(), json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data.get("data", {}).get("results", []), data.get("data", {}).get("total_search_result_count", 0)


def _lit_headers():
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {_cfg.LITERATURE_API_KEY}",
    }


def get_bibliography(doi_or_id, use_paper_id=False):
    """根据 DOI 或 paper_id 获取文献详情（摘要、期刊名、发表年份等）。"""
    url = f"{_cfg.PATSNAP_BASE_URL}/literature/bibliography"
    key = "paper_id" if use_paper_id else "doi"
    try:
        resp = requests.post(url, headers=_lit_headers(), json={key: doi_or_id}, timeout=20)
        resp.raise_for_status()
        data = resp.json().get("data", [])
        return data[0] if data else {}
    except Exception as e:
        print(f"[警告] bibliography API 失败 ({key}={doi_or_id}): {e}", file=sys.stderr)
        return {}


def get_citation(doi_or_id, use_paper_id=False):
    """根据 DOI 或 paper_id 获取文献引用次数，返回 (reference_no, np_citation_no)。"""
    url = f"{_cfg.PATSNAP_BASE_URL}/literature/citation"
    key = "paper_id" if use_paper_id else "doi"
    try:
        resp = requests.post(url, headers=_lit_headers(), json={key: doi_or_id}, timeout=20)
        resp.raise_for_status()
        data = resp.json().get("data", [])
        if data:
            return data[0].get("reference_no", 0), data[0].get("np_citation_no", 0)
    except Exception as e:
        print(f"[警告] citation API 失败 ({key}={doi_or_id}): {e}", file=sys.stderr)
    return 0, 0


def fetch_literature_for_query(patent_query, limit=20):
    """给定专利检索式，自动提取关键词和时间，检索期刊文献并补充详情，返回 (results, total, query_text)。"""
    query_text = extract_keywords_from_query(patent_query)
    if not query_text:
        return [], 0, ""

    start_ts, end_ts = extract_date_range_from_query(patent_query)
    date_time_str = None
    if start_ts and end_ts:
        date_time_str = f"[{start_ts} TO {end_ts}]"

    try:
        results, total = search_literature(query_text, date_time_str, limit)
    except Exception as e:
        print(f"[警告] 期刊文献检索失败: {e}", file=sys.stderr)
        return [], 0, query_text

    if not results:
        return [], 0, query_text

    # 对有 DOI 或 paper_id 的文献补充详情和引用次数
    enriched = []
    for item in results:
        doi = item.get("doi", "")
        paper_id = item.get("paper_id", "")
        if doi:
            detail = get_bibliography(doi, use_paper_id=False)
            if detail:
                # 只用 detail 里非空的字段覆盖，避免空值抹掉 search 结果里的摘要等
                item = {**item, **{k: v for k, v in detail.items() if v}}
            ref_no, np_no = get_citation(doi, use_paper_id=False)
        elif paper_id:
            detail = get_bibliography(paper_id, use_paper_id=True)
            if detail:
                item = {**item, **{k: v for k, v in detail.items() if v}}
            ref_no, np_no = get_citation(paper_id, use_paper_id=True)
        else:
            ref_no, np_no = 0, 0
        item["_reference_no"] = ref_no
        item["_np_citation_no"] = np_no
        enriched.append(item)

    return enriched, total, query_text


def ai_summarize_literature(results):
    """调用 ARK API 对文献列表进行 AI 总结，返回 Markdown 格式的总结文本。"""
    if not results:
        return ""
    if not _cfg.ARK_API_KEY:
        print("[配置] 未检测到 ARK_API_KEY，已跳过 AI 文献总结。", file=sys.stderr)
        return ""

    # 构建每篇文献的摘要文本
    papers = []
    for i, item in enumerate(results, 1):
        title = _extract_text(item.get("title", "")) or "N/A"
        abstract = _extract_text(item.get("abstract", ""))
        papers.append(f"[{i}] 标题：{title}\n摘要：{abstract if abstract else '（无摘要）'}")

    papers_text = "\n\n".join(papers)
    prompt = f"""以下是一批学术文献的标题和摘要，请：
1. 逐一总结每篇文献的核心技术要点（1-2句话）
2. 在最后提供一个综合性总结，归纳这批文献共同关注的技术方向和研究趋势

文献列表：
{papers_text}

请按以下格式输出：
### 综合总结
综合分析...

### 逐篇总结
**[1]** 文献标题（简短）：核心要点...
**[2]** ...
"""

    try:
        resp = requests.post(
            f"{_cfg.ARK_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {_cfg.ARK_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": _cfg.ARK_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 2000,
            },
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[警告] AI 文献总结失败: {e}", file=sys.stderr)
        return ""


def _extract_text(field):
    """从 title/abstract 字段提取文本，兼容字符串列表和 [{lang, text}] 两种格式。"""
    if not field:
        return ""
    if isinstance(field, str):
        return field
    if isinstance(field, list):
        if not field:
            return ""
        first = field[0]
        if isinstance(first, dict):
            return first.get("text", "")
        return str(first)
    return str(field)


def render_literature_section(results, total, query_text, ai_summary=""):
    """将文献结果渲染为 Markdown 章节，每篇文献展示详细信息，末尾附 AI 总结。"""
    lines = ["## 四、相关期刊文献", ""]

    if not results:
        lines.append("- 未检索到相关期刊文献。")
        lines.append("")
        return "\n".join(lines)

    lines.append(f"- **命中文献数**：{total}（展示前 {len(results)} 条）")
    lines.append("")

    for i, item in enumerate(results, 1):
        title = _extract_text(item.get("title", "")) or "N/A"
        authors = item.get("author", [])
        author_str = "、".join(authors[:5])
        if len(authors) > 5:
            author_str += " 等"
        doi = item.get("doi", "")
        doi_display = f"[{doi}](https://doi.org/{doi})" if doi else "—"
        publication = item.get("publication", "")
        pub_year = item.get("publication_year", "")
        volume = item.get("volume", "")
        issue = item.get("issue", "")
        pagination = item.get("pagination", "")
        abstract = _extract_text(item.get("abstract", ""))

        ref_no = item.get("_reference_no", 0)
        np_no = item.get("_np_citation_no", 0)

        lines.append(f"### {i}. {title}")
        if author_str:
            lines.append(f"- **作者**：{author_str}")
        if publication:
            pub_info = publication
            if pub_year:
                pub_info += f"，{pub_year}"
            if volume:
                pub_info += f"，Vol.{volume}"
            if issue:
                pub_info += f"({issue})"
            if pagination:
                pub_info += f"，pp.{pagination}"
            lines.append(f"- **期刊**：{pub_info}")
        if doi:
            lines.append(f"- **DOI**：{doi_display}")
        if ref_no or np_no:
            citation_parts = []
            if ref_no:
                citation_parts.append(f"文献引用 {ref_no} 次")
            if np_no:
                citation_parts.append(f"专利引用 {np_no} 次")
            lines.append(f"- **引用次数**：{'、'.join(citation_parts)}")
        if abstract:
            lines.append(f"- **摘要**：{abstract}")
        lines.append("")

    # AI 总结部分
    if ai_summary:
        lines.append("### AI 文献总结")
        lines.append("")
        lines.append(ai_summary)
        lines.append("")

    return "\n".join(lines)

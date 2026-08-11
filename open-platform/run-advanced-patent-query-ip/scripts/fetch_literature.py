#!/usr/bin/env python3
"""Derive a literature query from a PatSnap query and return structured results."""
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import config as _cfg
import requests


def _patsnap_date_to_ts(date_str):
    """Convert a YYYYMMDD PatSnap date to a UTC millisecond timestamp."""
    try:
        dt = datetime.strptime(date_str.strip(), "%Y%m%d").replace(tzinfo=timezone.utc)
        return int(dt.timestamp() * 1000)
    except ValueError:
        return None


def extract_keywords_from_query(query):
    """Extract terms from selected PatSnap text fields for literature search.

    Strategy:
    1. Extract terms inside TAC_ALL, TAC, MAINF, TTL, ABST, and related fields.
    2. Remove field labels, Boolean operators, and syntactic quoting.
    3. Return a title:(...) expression for the configured literature service.
    """
    if not query:
        return ""

    # Extract content from supported parenthesized text fields.
    field_pattern = re.compile(
        r'(?:TAC_all|TAC|TACD|MAINF|TTL|ABST|CLMS|DESC|TA)\s*:\s*\(([^)]+)\)',
        re.IGNORECASE,
    )
    matches = field_pattern.findall(query)

    if not matches:
        # Fall back to quoted terms when no supported field is present.
        matches = re.findall(r'"([^"]+)"', query)

    # Merge quoted phrases or non-Boolean bare terms.
    keywords = []
    for m in matches:
        # Preserve quoted phrases.
        quoted = re.findall(r'"([^"]+)"', m)
        if quoted:
            keywords.extend(quoted)
        else:
            # Remove Boolean operators while retaining substantive terms.
            words = re.sub(r'\b(AND|OR|NOT)\b', ' ', m, flags=re.IGNORECASE)
            words = re.sub(r'["\(\)]', ' ', words).split()
            keywords.extend(w for w in words if len(w) > 1)

    if not keywords:
        return ""

    # Deduplicate while preserving first-seen order.
    seen = set()
    unique = []
    for k in keywords:
        if k not in seen:
            seen.add(k)
            unique.append(k)

    # Construct the title:(term OR term) form expected by the source workflow.
    kw_str = " OR ".join(f'"{k}"' if " " in k else k for k in unique[:6])
    return f"title:({kw_str})"


def extract_date_range_from_query(query):
    """Extract a PBD or APD range as UTC millisecond timestamps."""
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
    """Call an explicitly configured, verified literature-search endpoint."""
    try:
        base_url, _ = _cfg.literature_api_settings()
    except RuntimeError as exc:
        print(f"[CONFIGURATION] Literature retrieval skipped: {exc}", file=sys.stderr)
        return [], 0

    url = f"{base_url.rstrip('/')}/search/literature/query-search"
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
    _, api_key = _cfg.literature_api_settings()
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }


def get_bibliography(doi_or_id, use_paper_id=False):
    """Retrieve bibliography by DOI or paper ID from the configured service."""
    base_url, _ = _cfg.literature_api_settings()
    url = f"{base_url.rstrip('/')}/literature/bibliography"
    key = "paper_id" if use_paper_id else "doi"
    try:
        resp = requests.post(url, headers=_lit_headers(), json={key: doi_or_id}, timeout=20)
        resp.raise_for_status()
        data = resp.json().get("data", [])
        return data[0] if data else {}
    except Exception as e:
        print(f"[WARNING] Literature bibliography failed ({key}={doi_or_id}): {e}", file=sys.stderr)
        return {}


def get_citation(doi_or_id, use_paper_id=False):
    """Retrieve literature and patent citation counts by DOI or paper ID."""
    base_url, _ = _cfg.literature_api_settings()
    url = f"{base_url.rstrip('/')}/literature/citation"
    key = "paper_id" if use_paper_id else "doi"
    try:
        resp = requests.post(url, headers=_lit_headers(), json={key: doi_or_id}, timeout=20)
        resp.raise_for_status()
        data = resp.json().get("data", [])
        if data:
            return data[0].get("reference_no", 0), data[0].get("np_citation_no", 0)
    except Exception as e:
        print(f"[WARNING] Literature citation lookup failed ({key}={doi_or_id}): {e}", file=sys.stderr)
    return 0, 0


def fetch_literature_for_query(patent_query, limit=20):
    """Retrieve and enrich literature for a patent query."""
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
        print(f"[WARNING] Literature search failed: {e}", file=sys.stderr)
        return [], 0, query_text

    if not results:
        return [], 0, query_text

    results, validation_warnings = validate_literature_results(results)
    for warning in validation_warnings:
        print(f"[WARNING] {warning}", file=sys.stderr)

    # Enrich records that expose a DOI or paper ID.
    enriched = []
    for item in results:
        doi = item.get("doi", "")
        paper_id = item.get("paper_id", "")
        if doi:
            detail = get_bibliography(doi, use_paper_id=False)
            if detail:
                # Merge non-empty detail fields without erasing search data.
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
    """Preserve the optional-summary hook without using an undisclosed provider.

    The source hard-coded a China-region ARK/Doubao service. The localized
    package does not send literature content to that provider. A caller may
    summarize retrieved evidence through an approved agent workflow and pass
    the resulting text to render_literature_section explicitly.
    """
    if results:
        print(
            "[LITERATURE] Automated summary skipped; no approved provider is configured.",
            file=sys.stderr,
        )
    return ""


def _extract_text(field):
    """Extract text from string, list, or language/text object fields."""
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


def validate_literature_results(results):
    """Return normalized records and warnings for malformed service data.

    This validation is intentionally conservative. It preserves source fields
    while preventing a malformed response from being treated as complete
    literature evidence. The caller may include the warnings in methodology
    and limitations sections.
    """
    normalized = []
    warnings = []
    if not isinstance(results, list):
        return [], ["The literature result payload was not a list."]
    for index, item in enumerate(results, 1):
        if not isinstance(item, dict):
            warnings.append(f"Literature result {index} was not an object and was skipped.")
            continue
        record = dict(item)
        title = _extract_text(record.get("title", "")).strip()
        doi = str(record.get("doi", "") or "").strip()
        paper_id = str(record.get("paper_id", "") or "").strip()
        if not title:
            warnings.append(f"Literature result {index} has no title.")
            record["title"] = "Title not available"
        if not doi and not paper_id:
            warnings.append(
                f"Literature result {index} has neither a DOI nor a paper ID; "
                "bibliographic enrichment could not be verified."
            )
        authors = record.get("author", [])
        if authors and not isinstance(authors, list):
            warnings.append(f"Literature result {index} has a non-list author field.")
            record["author"] = [str(authors)]
        normalized.append(record)
    return normalized, warnings


def render_literature_section(results, total, query_text, ai_summary=""):
    """Render detailed literature records and an optional approved summary."""
    lines = ["## Part 4: Related literature", ""]
    if query_text:
        lines.append(f"- **Derived literature query:** `{query_text}`")

    if not results:
        lines.append("- No related literature was retrieved, or the literature service was not configured.")
        lines.append("")
        return "\n".join(lines)

    lines.append(f"- **Matching literature records:** {total}; showing {len(results)}")
    lines.append("")

    for i, item in enumerate(results, 1):
        title = _extract_text(item.get("title", "")) or "Not available"
        authors = item.get("author", [])
        author_str = "; ".join(authors[:5])
        if len(authors) > 5:
            author_str += "; et al."
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
            lines.append(f"- **Authors:** {author_str}")
        if publication:
            pub_info = publication
            if pub_year:
                pub_info += f", {pub_year}"
            if volume:
                pub_info += f", vol. {volume}"
            if issue:
                pub_info += f"({issue})"
            if pagination:
                pub_info += f", pp. {pagination}"
            lines.append(f"- **Publication:** {pub_info}")
        if doi:
            lines.append(f"- **DOI:** {doi_display}")
        if ref_no or np_no:
            citation_parts = []
            if ref_no:
                citation_parts.append(f"cited by {ref_no} literature records")
            if np_no:
                citation_parts.append(f"cited by {np_no} patent records")
            lines.append(f"- **Citation context:** {'; '.join(citation_parts)}")
        if abstract:
            lines.append(f"- **Abstract:** {abstract}")
        lines.append("")

    # Append only a summary supplied by an approved caller.
    if ai_summary:
        lines.append("### AI-assisted literature synthesis")
        lines.append("")
        lines.append(ai_summary)
        lines.append("")

    return "\n".join(lines)

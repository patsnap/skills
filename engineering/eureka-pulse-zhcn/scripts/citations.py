import re
from collections import Counter
from urllib.parse import unquote, urlsplit
from uuid import UUID

from bs4 import BeautifulSoup, NavigableString

from common import require


UUID_TEXT = r"[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}"
INTERNAL_ID = re.compile(r"(?<![A-Za-z0-9_-])(?:" + UUID_TEXT + r"|[0-9a-f]{8})(?![A-Za-z0-9_-])", re.I)
ID_GROUP = re.compile(r"（[^（）()]*）|\([^（）()]*\)")


def reference_from_url(href: str) -> str:
    parsed = urlsplit(href)
    reference = unquote(parsed.netloc + parsed.path)
    prefix, separator, identity = reference.partition("-")
    if identity.startswith("{") and identity.endswith("}"):
        identity = identity[1:-1]
    return prefix + separator + identity


def identity_index(record_keys) -> dict[str, set[str]]:
    index = {}
    for key in record_keys:
        identity = key.partition(":")[2]
        if re.fullmatch(UUID_TEXT, identity, re.I):
            canonical = str(UUID(identity))
            for alias in (canonical, canonical[:8]):
                index.setdefault(alias, set()).add(key)
    return index


def citation_node(soup, reference: str, label: str, anchor: str | None):
    citation = soup.new_tag("sup", attrs={"class": "citation", "data-citation-ref": reference})
    if anchor:
        link = soup.new_tag("a", attrs={
            "href": "#" + anchor, "class": "citation-link", "data-record-target": anchor,
            "role": "button", "aria-haspopup": "dialog", "aria-controls": "record-drawer",
            "aria-expanded": "false", "aria-label": "查看引用资料 " + label})
        link.string = "[" + label + "]"
        citation.append(link)
    else:
        citation["class"].append("citation-unavailable")
        citation["title"] = "引用资料暂不可定位"
        citation.string = "[" + label + "]"
    return citation


def internal_text_nodes(soup):
    return [node for node in soup.find_all(string=True)
            if not node.find_parent(["a", "sup", "script", "style"])]


def internal_matches(text: str, index: dict):
    return [match for match in INTERNAL_ID.finditer(text)
            if match.group().lower() in index or len(match.group()) == 36]


def resolve_identity(identity: str, index: dict) -> str:
    candidates = index.get(identity.lower(), set())
    require(bool(candidates), "概述内部 ID 没有对应资料：" + identity)
    require(len(candidates) == 1, "概述内部 ID 对应多条资料：" + identity)
    return next(iter(candidates))


def convert_summary_ids(soup, index: dict, targets: dict):
    labels = {}
    next_number = 1
    for link in soup.select("a.citation-link"):
        label = link.get_text(strip=True)[1:-1]
        labels.setdefault(link["data-record-target"], label)
        if label.isdecimal():
            next_number = max(next_number, int(label) + 1)
    for node in internal_text_nodes(soup):
        text = str(node)
        matches = internal_matches(text, index)
        if not matches:
            continue
        spans, grouped = [], set()
        for group in ID_GROUP.finditer(text):
            members = [match for match in matches if group.start() < match.start() and match.end() < group.end()]
            remainder = group.group()[1:-1]
            for match in reversed(members):
                start, end = match.start() - group.start() - 1, match.end() - group.start() - 1
                remainder = remainder[:start] + remainder[end:]
            if members and not remainder.strip(" \t\r\n、,，;；"):
                spans.append((group.start(), group.end(), members))
                grouped.update(match.start() for match in members)
        spans += [(match.start(), match.end(), [match]) for match in matches if match.start() not in grouped]
        cursor = 0
        for start, end, members in sorted(spans):
            if cursor < start:
                node.insert_before(soup.new_string(text[cursor:start]))
            for match in members:
                identity = match.group()
                key = resolve_identity(identity, index)
                require(key in targets, "概述内部 ID 缺少对应资料抽屉：" + identity)
                anchor = targets[key]
                if anchor not in labels:
                    labels[anchor] = str(next_number)
                    next_number += 1
                citation = citation_node(soup, "detail-" + key.partition(":")[2], labels[anchor], anchor)
                citation["data-internal-id"] = identity
                citation["data-record-key"] = key
                node.insert_before(citation)
            cursor = end
        if cursor < len(text):
            node.insert_before(soup.new_string(text[cursor:]))
        node.extract()
    return soup


def group_summary_citations(soup):
    for first in list(soup.select("sup.citation:not(.citation-unavailable)")):
        if first.find_parent("sup", class_="citation-group"):
            continue
        members, nodes, separators = [first], [first], []
        cursor = first.next_sibling
        while cursor is not None:
            if isinstance(cursor, NavigableString) and not str(cursor).strip(" \t\r\n、,，"):
                separators.append(cursor)
            elif cursor.name == "sup" and "citation" in cursor.get("class", []) and cursor.select_one("a.citation-link"):
                nodes.extend(separators)
                nodes.append(cursor)
                members.append(cursor)
                separators = []
            else:
                break
            cursor = cursor.next_sibling
        targets = list(dict.fromkeys(member.select_one("a.citation-link")["data-record-target"] for member in members))
        group = soup.new_tag("sup", attrs={"class": "citation citation-group"})
        link = soup.new_tag("a", attrs={
            "class": "citation-group-link", "href": "#" + targets[0],
            "data-record-targets": " ".join(targets), "data-citation-count": str(len(targets)),
            "role": "button", "aria-haspopup": "dialog", "aria-controls": "record-drawer",
            "aria-expanded": "false", "aria-label": f"查看{len(targets)}条技术资料"})
        link.string = f"[{len(targets)}]"
        group.append(link)
        originals = soup.new_tag("span", attrs={"class": "citation-members", "hidden": ""})
        group.append(originals)
        first.insert_before(group)
        for node in nodes:
            originals.append(node.extract())
    return soup


def check_summary_citation_groups(page: str, original_markup: str) -> dict:
    original = BeautifulSoup(original_markup, "html.parser")
    expected = Counter((reference_from_url(link["href"]), link.get_text(" ", strip=True))
                       for link in original.select('a[href^="page://"]'))
    soup = BeautifulSoup(page, "html.parser")
    summary = soup.find(id="summary")
    if summary is None:
        require(not expected, "概述引用缺少概述章节")
        return {"summary_citation_groups": 0, "summary_citation_members": 0}
    actual = Counter((node["data-citation-ref"], node.get_text(strip=True)[1:-1])
                     for node in summary.select("sup[data-citation-ref]:not([data-internal-id])"))
    require(actual == expected, "概述原始引用身份、编号或数量不一致")
    cards = {node["id"]: node for node in soup.select("article.record")}
    groups = summary.select("sup.citation-group")
    total = 0
    for group in groups:
        link = group.find("a", class_="citation-group-link", recursive=False)
        originals = group.find("span", class_="citation-members", recursive=False)
        require(link is not None and originals is not None and originals.has_attr("hidden"), "概述引用组缺少入口或原始引用")
        members = originals.select("sup.citation > a.citation-link")
        targets = list(dict.fromkeys(member["data-record-target"] for member in members))
        require(bool(targets) and all(target in cards for target in targets), "概述引用组包含无对应资料的成员")
        require(link.get("data-record-targets", "").split() == targets and
                link.get("data-citation-count") == str(len(targets)) and link.get_text() == f"[{len(targets)}]" and
                link.get("href") == "#" + targets[0] and link.get("aria-controls") == "record-drawer" and
                link.get("aria-haspopup") == "dialog", "概述引用数量或列表目标与真实资料不一致")
        following = group.next_sibling
        while isinstance(following, NavigableString) and not str(following).strip(" \t\r\n、,，"):
            following = following.next_sibling
        require(not (getattr(following, "name", None) == "sup" and "citation-group" in following.get("class", [])),
                "同一位置的概述引用仍分为多个入口")
        total += len(members)
    require(all(node.find_parent("span", class_="citation-members") is not None
                for node in summary.select("a.citation-link")), "概述仍包含没有使用数量入口的引用")
    return {"summary_citation_groups": len(groups), "summary_citation_members": total}


def check_summary_ids(page: str, original_markup: str, index: dict) -> dict:
    original = BeautifulSoup(original_markup, "html.parser")
    expected = Counter(match.group() for node in internal_text_nodes(original)
                       for match in internal_matches(str(node), index))
    soup = BeautifulSoup(page, "html.parser")
    summary = soup.find(id="summary")
    require(summary is not None or not expected, "概述内部 ID 引用缺少概述章节")
    converted = summary.select("sup[data-internal-id]") if summary else []
    require(Counter(node["data-internal-id"] for node in converted) == expected,
            "概述内部 ID 转换数量或原始身份不一致")
    targets = {node["id"]: node["data-record-key"] for node in soup.select("article.record")}
    existing = summary.select("a.citation-link") if summary else []
    for citation in converted:
        identity = citation["data-internal-id"]
        key = resolve_identity(identity, index)
        link = citation.select_one("a.citation-link")
        require(link is not None and targets.get(link.get("data-record-target")) == key and
                citation.get("data-record-key") == key, "概述内部 ID 引用指向了其他资料：" + identity)
        labels = {node.get_text(strip=True) for node in existing
                  if node.get("data-record-target") == link["data-record-target"] and
                  not node.parent.has_attr("data-internal-id")}
        require(not labels or link.get_text(strip=True) in labels, "概述内部 ID 未沿用已有引用编号：" + identity)
    remaining = [match.group() for node in internal_text_nodes(summary) for match in internal_matches(str(node), index)] if summary else []
    require(not remaining, "概述正文仍包含内部 ID：" + ", ".join(remaining))
    return {"summary_internal_ids_checked": sum(expected.values()),
            "summary_internal_id_records": len({resolve_identity(identity, index) for identity in expected}),
            "unconverted_summary_internal_ids": remaining}

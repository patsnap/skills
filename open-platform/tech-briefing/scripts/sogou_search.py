#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""搜狗搜索新闻脚本。

用法:
    python sogou_search.py "查询词" [max_results]

输出:
    JSON 数组，每条含 title、url、desc。抓取失败时输出空数组并在 stderr 提示。
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from html import unescape

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)


def fetch(url, timeout=15):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": UA, "Accept-Language": "zh-CN,zh;q=0.9"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def strip_tags(s):
    return unescape(re.sub(r"<[^>]+>", "", s)).strip()


def parse(html):
    """提取搜狗 web 结果页条目。失败返回空列表。"""
    items = []
    block_pat = re.compile(
        r'<div[^>]+class="(?:vrwrap|result)[^"]*"[^>]*>(.*?)'
        r'(?=<div[^>]+class="(?:vrwrap|result)[^"]*"|<div[^>]+id="pagebar)',
        re.DOTALL,
    )
    title_pat = re.compile(
        r'<h3[^>]*>.*?<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
        re.DOTALL,
    )
    desc_pat = re.compile(
        r'<div[^>]*class="[^"]*(?:text-layout|ft|space-txt|fz-mid|star-wiki)[^"]*"[^>]*>'
        r'(.*?)</div>',
        re.DOTALL,
    )
    for block in block_pat.findall(html):
        m = title_pat.search(block)
        if not m:
            continue
        href, title_html = m.group(1), m.group(2)
        title = strip_tags(title_html)
        if not title:
            continue
        if href.startswith("/link?"):
            href = "https://www.sogou.com" + href
        elif not href.startswith("http"):
            continue
        dm = desc_pat.search(block)
        desc = strip_tags(dm.group(1)) if dm else ""
        items.append({"title": title, "url": href, "desc": desc[:300]})
    return items


def search(query, max_results=8):
    queries = [query, f"{query} 最新消息", f"{query} 新闻"]
    seen_urls, seen_titles, out = set(), set(), []
    for q in queries:
        if len(out) >= max_results:
            break
        try:
            html = fetch("https://www.sogou.com/web?query=" + urllib.parse.quote(q))
        except Exception as exc:
            print(f"[sogou_search] fetch failed for {q!r}: {exc}", file=sys.stderr)
            continue
        for item in parse(html):
            if item["url"] in seen_urls or item["title"] in seen_titles:
                continue
            seen_urls.add(item["url"])
            seen_titles.add(item["title"])
            out.append(item)
            if len(out) >= max_results:
                break
        time.sleep(0.4)
    return out


def main():
    if len(sys.argv) < 2:
        print('Usage: python sogou_search.py "query" [max_results]', file=sys.stderr)
        sys.exit(1)
    q = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    print(json.dumps(search(q, n), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

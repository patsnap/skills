from __future__ import annotations

import argparse
import html
import json
from datetime import timedelta
from pathlib import Path
from string import Template
from urllib.parse import urlsplit

from bs4 import BeautifulSoup
from markdown_it import MarkdownIt

from report_themes import resolve_theme, theme_css, theme_info

from citations import (check_summary_citation_groups, check_summary_ids, citation_node, convert_summary_ids,
                       group_summary_citations, identity_index, reference_from_url)
from common import (ai_field_index, check_source, digest, display_config, distinct_output, encode_week,
                    filter_operator, load_json, parse_date, period_data, report_assets, report_config, require, resolve_ai_fields,
                    source_ref, utc_now, write_json)


ROOT = Path(__file__).resolve().parent.parent
MARKDOWN = MarkdownIt("commonmark", {"html": False, "linkify": False}).enable("table")
LABELS = {"title": "标题", "company": "公司", "pn": "专利号", "patent_type": "专利类型",
          "PBD": "公开日期", "pbd": "公开日期", "link": "来源链接", "score": "相关度",
          "analysis": "情报研判", "abstract": "摘要", "doi": "DOI", "record_id": "资料 ID"}
LABELS.update({"llm_tech_problem": "技术问题", "llm_innovation_list": "方案要点", "llm_benefit": "预期效果",
               "technical_title": "AI 核心要求", "ai_summary": "资料摘要"})
PATENT_TYPES = {"A": "invention_application", "B": "invention_grant", "U": "utility_model",
                "D": "design", "S": "design"}
TYPE_NAMES = {"patent": "专利", "paper": "论文", "news": "新闻"}
RECORD_PREVIEW_COUNT = 2
RECORD_BATCH_SIZE = 5


def present(value) -> bool:
    return value is not None and value != "" and value != [] and value != {}


def safe_url(value) -> str | None:
    if not isinstance(value, str) or any(ord(char) < 32 for char in value):
        return None
    parsed = urlsplit(value)
    return value if parsed.scheme.lower() in {"https", "http"} and parsed.hostname else None


def markdown(value, aliases: dict[str, str]) -> str:
    require(isinstance(value, str), "文字内容必须为字符串")
    soup = BeautifulSoup(MARKDOWN.render(value), "html.parser")
    for link in soup.find_all("a"):
        href = link.get("href", "")
        if href.startswith("page://"):
            reference = reference_from_url(href)
            anchor = aliases.get(reference)
            label = link.get_text(" ", strip=True)
            link.replace_with(citation_node(soup, reference, label, anchor))
        elif safe_url(href):
            link["rel"] = "noopener noreferrer"
            link["target"] = "_blank"
        else:
            link.unwrap()
    for image in soup.find_all("img"):
        if not safe_url(image.get("src")):
            image.replace_with(image.get("alt", "图片地址不可用"))
        else:
            image["loading"] = "lazy"
            image["referrerpolicy"] = "no-referrer"
    for table in soup.find_all("table"):
        wrapper = soup.new_tag("div", attrs={"class": "table-scroll", "tabindex": "0", "role": "region", "aria-label": "数据表格"})
        table.wrap(wrapper)
    return str(soup)


def render_value(value, aliases: dict) -> str:
    if isinstance(value, dict):
        return "<dl>" + "".join(f"<dt>{html.escape(str(key))}</dt><dd>{render_value(item, aliases)}</dd>"
                               for key, item in value.items() if present(item)) + "</dl>"
    if isinstance(value, list):
        return "<ul>" + "".join(f"<li>{render_value(item, aliases)}</li>" for item in value) + "</ul>"
    return markdown(str(value), aliases)


def records(value, name: str) -> list[dict]:
    if value is None:
        return []
    if isinstance(value, dict) and "records" in value:
        require(not value.get("has_next"), f"{name} 尚有后续页")
        require(not value.get("has_previous") and value.get("page", 1) == 1, f"{name} 缺少前面的分页")
        rows = value["records"]
        require(value.get("total", len(rows)) == len(rows), f"{name} 返回数量不完整")
    elif isinstance(value, dict):
        rows = list(value.values())
    else:
        rows = value
    require(isinstance(rows, list) and all(isinstance(row, dict) for row in rows), f"{name} 必须为记录对象集合")
    return rows


def normalize(row: dict, kind: str | None = None) -> dict:
    info = row.get("item_info", row)
    require(isinstance(info, dict), "item_info 必须为对象")
    kind = kind or row.get("item_type") or info.get("data_type")
    require(kind in {"patent", "paper", "news"}, "记录缺少支持的 item_type")
    identity = row.get("item_id") or row.get("news_id") or info.get(kind + "_id")
    require(isinstance(identity, str) and identity.strip(), "记录缺少稳定 ID")
    score = row.get("score", info.get("relevance", {}).get("score"))
    require(score is None or isinstance(score, (float, int)), "相关度必须为数值或缺失")
    return {"id": identity, "key": kind + ":" + identity, "kind": kind, "row": row, "info": info,
            "fields": row.get("extracted_fields", {}), "score": score}


def high_record_keys(data: dict) -> set[str]:
    rows = list(records(data.get("tech_items"), "tech_items"))
    rows += [item["record_info"] for item in records(data.get("typical_tech_interpret"), "typical_tech_interpret")
             if isinstance(item.get("record_info"), dict)]
    normalized = [normalize(row) for row in rows]
    return {record["key"] for record in normalized if record["kind"] != "news" and
            record["score"] is not None and record["score"] >= 4}


def summary_text(data: dict) -> str:
    overview = data.get("overview", {})
    summary = overview.get("overall_judgement") if isinstance(overview, dict) else overview
    if not present(summary):
        summary = data.get("summary")
    return summary if isinstance(summary, str) else ""


def summary_identity_index(data: dict) -> dict:
    rows = [(row, None) for row in records(data.get("tech_items"), "tech_items")]
    rows += [(row, "news") for row in records(data.get("hot_news"), "hot_news")]
    rows += [(item["record_info"], None)
             for item in records(data.get("typical_tech_interpret"), "typical_tech_interpret")
             if isinstance(item.get("record_info"), dict)]
    return identity_index(normalize(row, kind)["key"] for row, kind in rows)


def standard(record: dict, key: str, company_group: bool = False):
    row, info = record["row"], record["info"]
    if key == "company":
        value = row.get("company") or info.get("company")
        if not present(value):
            names = info.get("ancs", {})
            value = names.get("full_ans_name") or names.get("ans_name") if isinstance(names, dict) else None
        values = value if isinstance(value, list) else [value] if present(value) else []
        return list(dict.fromkeys(values + (row.get("sub_field_name", []) if company_group else [])))
    if key in row and key not in {"extracted_fields", "item_info"}:
        return row[key]
    if key in info:
        return info[key]
    if key == "PBD":
        return info.get("pbd")
    if key == "abstract":
        value = info.get("abst")
        return BeautifulSoup(value, "html.parser").get_text("\n", strip=True) if isinstance(value, str) else value
    if key == "title" and record["kind"] == "paper":
        return info.get("paper_title")
    return None


def field(record: dict, key: str, ai_keys: set[str], company_group: bool = False):
    return record["fields"].get(key) if key in ai_keys else standard(record, key, company_group)


def citation_summary(record: dict, ai_keys: set[str]):
    for key in ("technical_title", "abstract"):
        value = field(record, key, ai_keys)
        if present(value) and (not isinstance(value, str) or value.strip()):
            return key, value
    return None, None


def reading_title(record: dict, result: dict | None = None, selection: dict | None = None):
    return ((selection or {}).get("display_title") or (result or {}).get("ai_title") or standard(record, "title") or
            standard(record, "technical_title") or standard(record, "pn") or standard(record, "doi") or record["id"])


def in_scope(record: dict, scope: list) -> bool:
    require(isinstance(scope, list), "data_scope 必须为数组")
    types = {record["kind"]}
    if record["kind"] == "patent":
        subtype = record["info"].get("patent_type")
        if subtype in PATENT_TYPES:
            types.add(PATENT_TYPES[subtype])
        if subtype in PATENT_TYPES.values():
            types.add(subtype)
        if record["info"].get("legal_event"):
            types.add("legal_event")
    return bool(types.intersection(scope))


def matches(record: dict, module: dict, ai_keys: set[str]) -> bool:
    if not in_scope(record, module["data_scope"]):
        return False
    for condition in module.get("filter", []):
        key = condition["filter_key"]
        actual = field(record, key, ai_keys, module.get("classification_type") == "company")
        operator = filter_operator(condition)
        require(operator in {"eq", "ne", "in", "not_in", "contains", "contains_any", "contains_all",
                             "gt", "gte", "lt", "lte", "exists"}, f"未知过滤操作符：{operator}")
        expected = condition.get("value")
        if operator == "exists":
            ok = present(actual) == (True if expected is None else bool(expected))
        elif not present(actual):
            ok = False
        else:
            values = actual if isinstance(actual, list) else [actual]
            candidates = expected if isinstance(expected, list) else [expected]
            overlap = any(value == candidate for value in values for candidate in candidates)
            if operator in {"eq", "in", "contains_any"}:
                ok = overlap
            elif operator in {"ne", "not_in"}:
                ok = not overlap
            elif operator == "contains_all":
                ok = all(candidate in values for candidate in candidates)
            elif operator == "contains":
                ok = any(str(candidate) in actual for candidate in candidates) if isinstance(actual, str) else overlap
            else:
                require(len(candidates) == 1 and isinstance(actual, (int, float)) and isinstance(candidates[0], (int, float)),
                        "数值过滤需要单个数值")
                expected = candidates[0]
                ok = {"gt": actual > expected, "gte": actual >= expected,
                      "lt": actual < expected, "lte": actual <= expected}[operator]
        if not ok:
            return False
    return True


def figure_url(value) -> str | None:
    if isinstance(value, dict):
        return next((value[key] for key in ["url", "image_url", "storage_path", "fulltext_image240_url", "content"]
                     if safe_url(value.get(key))), None)
    return safe_url(value)


def selected_figures(record: dict, result: dict | None) -> list[dict]:
    selected = next((source["important_figures"] for source in [result or {}, record["row"], record["info"]]
                     if source.get("important_figures")), [])
    require(isinstance(selected, list), "important_figures 必须为数组")
    images = record["info"].get("pdf_images", [])
    require(isinstance(images, list), "pdf_images 必须为数组")
    figures = []
    for index, item in enumerate(selected[:3]):
        number = item.get("figure_no") if isinstance(item, dict) else None
        url = figure_url(item)
        if not url and present(number):
            matches = [image for image in images if isinstance(image, dict) and str(number).strip().casefold() in
                       {str(label).strip().casefold() for label in [image.get("fig_title_code"), *image.get("labels", [])]
                        if present(label)}]
            urls = {figure_url(image) for image in matches if figure_url(image)}
            require(len(urls) <= 1, "已选图号对应多个不同图片地址：" + str(number))
            url = next(iter(urls), None)
        figures.append({"url": url, "number": str(number) if present(number) else str(index + 1),
                        "description": item.get("content", "") if isinstance(item, dict) else "",
                        "evidence_source": item.get("evidence_source", "") if isinstance(item, dict) else ""})
    return figures


def image_url(record: dict, result: dict | None) -> str | None:
    candidates = []
    for source in [result or {}, record["row"], record["info"]]:
        figures = source.get("important_figures", [])
        if isinstance(figures, list):
            candidates.extend(figures)
    candidates.append(record["info"].get("patent_image"))
    pdf_images = record["info"].get("pdf_images", [])
    if pdf_images:
        candidates.append(pdf_images[0])
    for item in candidates:
        if figure_url(item):
            return figure_url(item)
    return None


def validate_inputs(config: dict, data: dict, target: dict) -> None:
    require(config.get("pulse_id") == target["pulse_id"] == data.get("basic_info", {}).get("pulse_id"),
            "配置、结果和目标的 pulse_id 不一致")
    require(target["period_type"] in {"week", "month"}, "目标周期类型无效")
    require(len(target["period"]) == 6 and target["period"].isdigit(), "目标周期编码无效")
    start, end = parse_date(target["start_date"]), parse_date(target["end_date"])
    require(parse_date(data["report_start_date"]) == start and parse_date(data["report_end_date"]) == end,
            "服务返回日期与目标周期不一致")
    if target["period_type"] == "week":
        require(start.weekday() == 6 and (end - start).days == 6, "目标必须为周日至周六")
        require(encode_week(start, target["week_rule"]) == target["period"], "周编码与目标日期不一致")
    else:
        require(start.day == 1 and start.strftime("%Y%m") == target["period"], "月报目标日期无效")
        require(end.year == start.year and end.month == start.month and
                (end + timedelta(days=1)).day == 1, "月报必须覆盖完整自然月")
    if target.get("reference_date"):
        require(end < parse_date(target["reference_date"]), "目标周期尚未结束")
    require(data.get("run_status", "FINISHED") == "FINISHED", "目标期尚未完成")
    require(data.get("complete", True) is True, "目标期数据不完整")
    require("tech_items" in data or "hot_news" in data, "周期结果缺少记录集合")
    template = data.get("basic_info", {}).get("template_custom", {})
    for key in ["detail_module", "typical_filters", "card_fields"]:
        if key in template:
            require(display_config(template[key]) == display_config(config.get(key)),
                    f"目标期显示配置与当前配置不一致：{key}；请核实配置来源及版本")
    for key in ["config_version", "config_updated_at"]:
        actual = data.get(key, data.get("basic_info", {}).get(key))
        expected = config.get(key, config.get("updated_at") if key == "config_updated_at" else None)
        if actual is not None and expected is not None:
            require(actual == expected, f"配置版本不一致：{key}")


def build_groups(config: dict, data: dict, focus: dict | None = None, review: dict | None = None) -> tuple[list, list, list]:
    ai_keys = set(ai_field_index(config))
    pool = {}
    source_rows = [(row, None) for row in records(data.get("tech_items"), "tech_items")]
    source_rows += [(row, "news") for row in records(data.get("hot_news"), "hot_news")]
    for row, kind in source_rows:
        record = normalize(row, kind)
        if record["key"] in pool:
            require(pool[record["key"]]["row"] == row, "同一稳定 ID 对应不同记录")
        pool[record["key"]] = record
    definitions = config.get("typical_filters", [])
    require(len({x["name"] for x in definitions}) == len(definitions), "重点分组名称重复")
    for definition in definitions:
        resolve_ai_fields(config, definition)
    definition_by_name = {item["name"]: item for item in definitions}
    interpreted = records(data.get("typical_tech_interpret"), "typical_tech_interpret")
    for item in interpreted:
        if isinstance(item.get("record_info"), dict):
            record = normalize(item["record_info"])
            if record["key"] in pool:
                require(pool[record["key"]]["info"] == record["info"], "重点结果与普通记录身份内容冲突")
            else:
                pool[record["key"]] = record
    interpreted_records = []
    for item in interpreted:
        result = item.get("typical_result", {})
        definition = definition_by_name.get(result.get("typical_name"))
        if definition is None or not any(present(result.get(k)) for k in ["display_summary", "extracted_content"]):
            continue
        require(isinstance(item.get("record_info"), dict), "重点结果缺少完整 record_info")
        record = normalize(item["record_info"])
        record["fields"] = {**record["fields"], **item.get("extracted_fields", {}),
                            **record["row"].get("typical_extracted_fields", {})}
        if in_scope(record, definition["data_scope"]):
            interpreted_records.append((item, record))
    high = any(record["kind"] != "news" and record["score"] is not None and record["score"] >= 4
               for record in list(pool.values()) + [record for _, record in interpreted_records])
    eligible = lambda r: r["kind"] == "news" or r["score"] is not None and (r["score"] >= 4 or not high)
    typicals, chosen = [], set()
    definition_keys = [x.get("key") or "typical-" + digest(x["name"])[:20] for x in definitions]
    require(len(set(definition_keys)) == len(definitions), "重点分组 key 重复")
    require(all(isinstance(key, str) and key and not any(char.isspace() for char in key) for key in definition_keys),
            "重点分组 key 必须为非空且不含空白的字符串")
    for definition, definition_key in zip(definitions, definition_keys):
        cards, seen = [], set()
        for item, record in interpreted_records:
            result = item.get("typical_result", {})
            if result.get("typical_name") != definition["name"] or not any(present(result.get(k)) for k in ["display_summary", "extracted_content"]):
                continue
            require(record["key"] not in pool or pool[record["key"]]["info"] == record["info"], "重点结果与普通记录身份内容冲突")
            if not in_scope(record, definition["data_scope"]) or not eligible(record) or record["key"] in seen:
                continue
            cards.append((record, result, definition))
            chosen.add(record["key"])
            seen.add(record["key"])
        if cards:
            typicals.append({"id": definition_key, "name": definition["name"], "cards": cards})
    require((focus is None) == (review is None), "本期重点审核需要同时提供规则和审核结果")
    if review is not None:
        from focus import review_groups
        require(review.get("data_sha256") == digest(data), "重点审核对应的周期内容不一致")
        for group in review_groups(focus, review, pool, config["pulse_id"]):
            definition = group["definition"]
            resolve_ai_fields(config, definition)
            selected = [(record, selection) for record, selection in group["selections"] if record["key"] not in chosen]
            require(all(in_scope(record, definition["data_scope"]) for record, _ in selected), "重点资料类型与规则不一致")
            if selected:
                typicals.append({"id": group["id"], "name": group["name"], "local_review": True,
                                 "review_notes": {record["key"]: selection for record, selection in selected},
                                 "cards": [(record, None, definition) for record, _ in selected]})
                chosen.update(record["key"] for record, _ in selected)
    detail = config["detail_module"]
    mode = detail.get("mode")
    if detail.get("visible") is not False:
        require(mode in {"none", "merged", "split"}, "detail_module.mode 无效")
    ordinary = [record for record in pool.values() if record["key"] not in chosen and eligible(record)]
    groups = []
    if mode == "split" or detail.get("visible") is not False and mode != "none":
        modules = detail.get("sub_modules", []) if mode == "split" else [{"name": "全部技术动态"}]
        for index, module in enumerate(modules):
            selected = [r for r in ordinary if matches(r, module, ai_keys)] if mode == "split" else ordinary
            groups.append({"id": "detail-group-" + str(index), "name": module["name"], "configured_module": mode == "split",
                           "cards": [(r, None, config["card_fields"]) for r in selected]})
        displayed = {record["key"] for group in groups for record, _, _ in group["cards"]}
        unmatched = [record for record in ordinary if record["key"] not in displayed and
                     (any(in_scope(record, module["data_scope"]) for module in modules) or
                      record["kind"] != "news" and record["score"] is not None and record["score"] >= 4)] if mode == "split" else []
        if unmatched:
            groups.append({"id": "unclassified-records", "name": "其他",
                           "unclassified": True, "cards": [(r, None, config["card_fields"]) for r in unmatched]})
    displayed = {record["key"] for group in groups for record, _, _ in group["cards"]}
    remaining_high = [record for record in ordinary if record["kind"] != "news" and
                      record["score"] is not None and record["score"] >= 4 and record["key"] not in displayed]
    if remaining_high:
        groups.append({"id": "high-relevance-records", "name": "高相关技术资料", "coverage_group": True,
                       "cards": [(record, None, config["card_fields"]) for record in remaining_high]})
    supplements = [record for record in pool.values() if high and record["kind"] == "patent" and
                   record["score"] is not None and record["score"] < 4 and record["key"] not in chosen]
    patent_index = {}
    for record in supplements:
        patent_index.setdefault(record["info"].get("patent_id", record["id"]), record)
    return typicals, groups, list(patent_index.values())


def news_records(data: dict) -> dict:
    rows = [(row, "news") for row in records(data.get("hot_news"), "hot_news")]
    rows += [(row, None) for row in records(data.get("tech_items"), "tech_items")]
    rows += [(item["record_info"], None) for item in records(data.get("typical_tech_interpret"), "typical_tech_interpret")
             if isinstance(item.get("record_info"), dict)]
    result = {}
    for row, kind in rows:
        record = normalize(row, kind)
        if record["kind"] == "news":
            require(record["key"] not in result or result[record["key"]]["info"] == record["info"],
                    "新闻资料身份内容冲突")
            result.setdefault(record["key"], record)
    return result


def report_groups(config: dict, data: dict, focus=None, review=None) -> tuple[list, list, list, list]:
    typicals, groups, supplements = build_groups(config, data, focus, review)
    news = {key: (record, None, config["card_fields"]) for key, record in news_records(data).items()}
    news_notes = {}
    for group in typicals + groups:
        for record, result, definition in group["cards"]:
            if record["kind"] == "news" and (news[record["key"]][1] is None or result):
                news[record["key"]] = record, result, definition
                if record["key"] in group.get("review_notes", {}):
                    news_notes[record["key"]] = group["review_notes"][record["key"]]
        group["cards"] = [item for item in group["cards"] if item[0]["kind"] != "news"]
    typicals = [group for group in typicals if group["cards"]]
    news_groups = [{"id": "news-records", "name": "新闻动态", "cards": list(news.values()), "review_notes": news_notes}] if news else []
    return news_groups, typicals, groups, supplements


def build_page(config: dict, data: dict, target: dict, tokens: str, focus: dict | None = None,
               review: dict | None = None, history_charts: dict | None = None,
               theme: str | None = None) -> tuple[str, dict]:
    news_groups, typicals, groups, supplements = report_groups(config, data, focus, review)
    global_fields = ai_field_index(config)
    ai_keys = set(global_fields)
    labels = {**LABELS, **{key: item.get("display_name", key) for key, item in global_fields.items()}}
    aliases, ambiguous, card_ids, summary_targets = {}, set(), {}, {}
    all_groups = news_groups + typicals + groups
    if supplements:
        all_groups += [{"id": "supplementary", "name": "补充专利线索", "cards": [(r, None, config["card_fields"]) for r in supplements]}]
    for index, group in enumerate(all_groups):
        for record, _, _ in group["cards"]:
            anchor = "record-" + digest([group["id"], record["key"]])[:24]
            card_ids[(index, record["key"])] = anchor
            summary_targets.setdefault(record["key"], anchor)
            ids = [record["id"], record["info"].get("pn")]
            for identity in filter(None, ids):
                for prefix in ["detail-", "typical-"]:
                    key = prefix + identity
                    if key in aliases and aliases[key][0] != record["key"]:
                        ambiguous.add(key)
                    else:
                        aliases.setdefault(key, (record["key"], anchor))
    aliases = {key: value[1] for key, value in aliases.items() if key not in ambiguous}

    def card(record, result, fields, anchor, supplementary=False, featured=False, selection=None, initially_hidden=False):
        kind = record["kind"]
        local_ai_keys, local_labels = ai_keys, labels
        extra_fields = []
        if isinstance(fields, dict) and "card_fields" in fields:
            extra_fields = resolve_ai_fields(config, fields)
            local_ai_keys = ai_keys | {item["field_key"] for item in extra_fields}
            local_labels = {**labels, **{item["field_key"]: item.get("display_name", item["field_key"]) for item in extra_fields}}
            fields = fields.get("card_fields", {})
        if isinstance(fields, dict):
            fields = fields.get(kind, [])
        require(isinstance(fields, list), "卡片字段必须为数组或按资料类型分组的对象")
        title = reading_title(record, result, selection)
        source_title = standard(record, "title")
        content, fields_html, metadata, configured_html = "", "", "", ""
        enum_html = ""
        formats = {key: item.get("data_format") for key, item in global_fields.items()}
        formats.update({item["field_key"]: item.get("data_format") for item in extra_fields})
        lead_key, lead_value = None, None
        if not featured and kind in {"patent", "paper"} and not supplementary:
            lead_key = "technical_title" if present(field(record, "technical_title", local_ai_keys)) else "abstract"
            lead_value = field(record, lead_key, local_ai_keys)
        elif not featured:
            lead_key = next((key for key in fields if formats.get(key) != "enum" and
                             key not in {"title", "pn", "doi", "company", "PBD", "score", "link", "analysis"} and
                             isinstance(field(record, key, local_ai_keys), str) and present(field(record, key, local_ai_keys))), None)
            lead_value = field(record, lead_key, local_ai_keys) if lead_key else standard(record, "abstract")
        identity_keys = ["pn"] if kind == "patent" else ["doi"] if kind == "paper" else []
        identity_keys += ["company", "PBD"]
        for key in identity_keys:
            value = standard(record, key)
            if present(value):
                value_class = ' source-id' if key in {"pn", "doi"} else ""
                metadata += f'<div class="field meta-item{value_class}"><dt>{html.escape(LABELS[key])}</dt><dd>{render_value(value, aliases)}</dd></div>'
        if not metadata:
            metadata = f'<div class="field meta-item source-id"><dt>资料 ID</dt><dd>{html.escape(record["id"])}</dd></div>'
        if record["score"] is not None:
            metadata += f'<div class="meta-item meta-score"><dt>相关度</dt><dd>{record["score"]:g}</dd></div>'
        source = safe_url(standard(record, "link"))
        if source:
            metadata += f'<a class="source-link" href="{html.escape(source, quote=True)}" target="_blank" rel="noopener noreferrer">阅读原文 ↗</a>'
        for key in fields:
            value = field(record, key, local_ai_keys)
            if not present(value) or key in identity_keys + ["title", "score", "link", "analysis", lead_key]:
                continue
            if formats.get(key) == "enum":
                values = value if isinstance(value, list) else [value]
                value_html = '<div class="record-tags">' + ''.join(f'<span class="record-tag" title="{html.escape(local_labels.get(key, key), quote=True)}">{html.escape(str(item))}</span>' for item in values) + '</div>'
            else:
                value_html = render_value(value, aliases)
            field_class = "field field-enum" if formats.get(key) == "enum" else "field"
            field_html = f'<div class="{field_class}" data-field-key="{html.escape(key, quote=True)}"><dt>{html.escape(local_labels.get(key, key))}</dt><dd>{value_html}</dd></div>'
            if formats.get(key) == "enum":
                enum_html += field_html
            else:
                configured_html += field_html
        configured_html = '<dl class="record-configured">' + configured_html + '</dl>' if configured_html else ""
        enum_html = '<dl class="record-configured record-enums">' + enum_html + '</dl>' if enum_html else ""
        if featured:
            for key, label_key, default_label in [("display_summary", "display_summary_field_name", "重点摘要"),
                                                   ("extracted_content", "extract_content_field_name", "专项解读")]:
                value = (result or {}).get(key)
                if present(value):
                    label = (result or {}).get(label_key) or default_label
                    content += f'<div class="record-special rich-text" data-field-key="{key}"><p class="field-label">{html.escape(str(label))}</p>{render_value(value, aliases)}</div>'
        elif present(lead_value):
            label = LABELS["technical_title"] if lead_key == "technical_title" else local_labels.get(lead_key, "摘要")
            content = f'<div class="record-lead rich-text" data-field-key="{lead_key or "abstract"}"><p class="field-label">{html.escape(label)}</p>{render_value(lead_value, aliases)}</div>'
        analysis = standard(record, "analysis")
        analysis_html = ""
        if present(analysis):
            analysis_html = ('<div class="record-analysis rich-text" data-field-key="analysis"><p class="field-label">'
                             + LABELS["analysis"] + '</p>' + render_value(analysis, aliases) + '</div>')
        if selection:
            evidence_html = ''.join('<li>' + html.escape(item["quote"]) + '</li>' for item in selection["evidence"])
            fields_html += '<div class="field"><dt>入选证据摘录</dt><dd><ul>' + evidence_html + '</ul></dd></div>'
            content = '<div class="record-takeaway"><p>' + html.escape(selection["reason"]) + '</p></div>' + content
        if present(source_title):
            fields_html = '<div class="field"><dt>原始标题</dt><dd>' + html.escape(str(source_title)) + '</dd></div>' + fields_html
        abstract = standard(record, "abstract")
        if present(abstract) and lead_key != "abstract" and "abstract" not in fields:
            fields_html += '<div class="field"><dt>原始摘要</dt><dd class="rich-text">' + render_value(abstract, aliases) + '</dd></div>'
        details = (f'<details class="record-details"><summary>查看详情</summary><div class="details-content"><dl>{fields_html}</dl></div></details>'
                   if fields_html or len(str(lead_value or "")) > 240 else "")
        picture = image_url(record, result)
        image = (f'<figure><a href="{html.escape(picture, quote=True)}" target="_blank" rel="noopener noreferrer" aria-label="打开原始附图">'
                 f'<img src="{html.escape(picture, quote=True)}" alt="{html.escape(str(title), quote=True)} 对应资料图片" '
                 'loading="lazy" referrerpolicy="no-referrer"></a><figcaption hidden>图片暂时无法加载</figcaption></figure>') if picture else ""
        if featured:
            figures = [figure for figure in selected_figures(record, result) if figure["url"]]
            if figures:
                image = '<div class="selected-figures" aria-label="已选重点附图">'
                for figure in figures:
                    number = html.escape(figure["number"], quote=True)
                    image += f'<figure data-figure-no="{number}">'
                    if figure["url"]:
                        url = html.escape(figure["url"], quote=True)
                        image += f'<a href="{url}" target="_blank" rel="noopener noreferrer" aria-label="打开已选附图 {number}"><img src="{url}" alt="{html.escape(str(title), quote=True)} 附图 {number}" loading="lazy" referrerpolicy="no-referrer"></a><p class="image-error" hidden>图片暂时无法加载</p>'
                    image += f'<figcaption><span class="figure-number">附图 {number}</span>'
                    if present(figure["description"]) and not safe_url(figure["description"]):
                        image += render_value(figure["description"], aliases)
                    if present(figure["evidence_source"]):
                        image += '<p class="figure-source">' + html.escape(str(figure["evidence_source"])) + '</p>'
                    image += '</figcaption></figure>'
                image += '</div>'
        badge = TYPE_NAMES[kind]
        style = " record-featured" if result or featured else " record-supplement" if supplementary else ""
        if kind == "news":
            style += " record-news"
        heading = '<div class="record-heading" aria-hidden="true"></div>' if result or featured else ""
        detail_attribute = f' data-detail-target="{anchor}-details"'
        detail_images = f'<div class="detail-figures" aria-label="资料附图">{image}</div>' if image else ""
        detail_source = (f'<div class="record-detail-source" id="{anchor}-details">'
                         f'<dl class="record-meta">{metadata}</dl>{enum_html}{detail_images}{content}{configured_html}'
                         f'<dl class="record-fields">{fields_html}</dl>{analysis_html}</div>')
        title_html = (f'<span class="record-kind" data-record-kind="{kind}">{badge}</span>'
                      f'<span class="record-title">{html.escape(str(title))}</span>')
        citation_source = ""
        if kind == "patent":
            style += " record-patent"
            details = ""
            summary_key, summary_value = citation_summary(record, local_ai_keys)
            if summary_key is not None:
                citation_source = (f'<template class="citation-summary-source" data-field-key="{summary_key}">'
                                   f'{render_value(summary_value, aliases)}</template>')
            title_html = (f'<button class="record-open" type="button" aria-haspopup="dialog" aria-controls="record-drawer" '
                          f'aria-expanded="false" aria-label="查看专利详细资料：{html.escape(str(title), quote=True)}">{title_html}</button>')
        hidden_attribute = " hidden" if initially_hidden else ""
        return (f'<article class="record{style}" id="{anchor}" data-record-key="{html.escape(record["key"], quote=True)}"{detail_attribute}{hidden_attribute}>'
                f'{heading}<h4>{title_html}</h4>'
                f'<dl class="record-meta">{metadata}</dl>{enum_html}'
                f'<div class="record-layout{" with-image" if image else ""}"><div>{content}{configured_html}{details}</div>{image}</div>{analysis_html}{detail_source}{citation_source}</article>')

    sections, navigation = [], []

    def add_section(identity, title, body, extra_nav="", count=None):
        number = f'{len(sections) + 1:02d}'
        sections.append(f'<section class="report-panel" id="{identity}" aria-labelledby="{identity}-title"><div class="section-heading"><span class="section-number" aria-hidden="true">{number}</span><h2 id="{identity}-title">{html.escape(title)}</h2></div>{body}</section>')
        label = {"summary": "本期概览", "news-updates": "新闻动态", "key-updates": "重点解读", "latest-updates": "高相关技术", "supplementary": "补充线索"}.get(identity, title)
        count_html = f'<span class="chapter-count">{count}</span>' if count is not None else ""
        menu = f'<details class="nav-details"><summary aria-label="展开{html.escape(title, quote=True)}目录">⌄</summary><div class="nav-menu">{extra_nav}</div></details>' if extra_nav else ""
        navigation.append(f'<div class="nav-chapter"><a class="chapter-link" href="#{identity}">{html.escape(label)}{count_html}</a>{menu}</div>')

    overview = data.get("overview", {})
    summary = summary_text(data)
    if summary.strip():
        summary_body = BeautifulSoup(markdown(summary, aliases), "html.parser")
        convert_summary_ids(summary_body, summary_identity_index(data), summary_targets)
        group_summary_citations(summary_body)
        first = summary_body.find(True, recursive=False)
        if first and first.name == "p":
            intro = str(first.extract())
            rest = str(summary_body).strip()
            summary_html = '<div class="summary-intro rich-text">' + intro + '</div>'
            if rest:
                summary_html += '<div class="summary-detail rich-text">' + rest + '</div>'
        else:
            summary_html = '<div class="summary-intro rich-text">' + str(summary_body) + '</div>'
        add_section("summary", "本期概述", summary_html)
    if history_charts is not None:
        from charts import section_title
        add_section("recent-changes", section_title(history_charts), history_charts["html"])
    insight_data = data.get("insights", [])
    insight_data = insight_data.get("items", []) if isinstance(insight_data, dict) else insight_data
    require(isinstance(insight_data, list), "insights 结果必须为数组或 items 对象")
    configured = config.get("insights", {}).get("items", [])
    order = {item.get("key", item.get("id")): i for i, item in enumerate(configured)}
    for index, insight in enumerate(sorted(insight_data, key=lambda item: order.get(item.get("key", item.get("id")), len(order)))):
        text = insight.get("content", insight.get("text"))
        if isinstance(text, str) and text.strip():
            add_section("insight-" + str(index), insight.get("title", insight.get("name", "Insight")), markdown(text, aliases))
    actions = data.get("recommendations", data.get("actions", overview.get("recommendations") if isinstance(overview, dict) else None))
    if present(actions):
        add_section("actions", "建议行动", render_value(actions, aliases))
    offset = 0
    for section_id, title, selected in [("news-updates", "新闻动态", news_groups),
                                      ("key-updates", "重点技术动态", typicals), ("latest-updates", "高相关技术", groups),
                                      ("supplementary", "补充专利线索", all_groups[len(news_groups) + len(typicals) + len(groups):])]:
        if not selected:
            if section_id == "key-updates" and review is not None and present(review.get("no_selection_reason")):
                add_section("key-updates", "重点技术动态", '<p class="notice">' + html.escape(review["no_selection_reason"]) + '</p>')
            continue
        body, subnav = "", ""
        if section_id == "supplementary":
            body = '<p class="section-intro">以下为本期检索中的低相关专利，供延伸查阅。阅读时请核实其与当前研究问题的直接联系。</p>'
        if section_id == "latest-updates":
            total = len({record["key"] for group in selected for record, _, _ in group["cards"]})
            filters = f'<button class="record-filter" type="button" data-filter-group="all" aria-pressed="true">全部 <span>{total}</span></button>'
            for group in selected:
                disabled = " disabled" if not group["cards"] else ""
                filters += (f'<button class="record-filter" type="button" data-filter-group="{html.escape(group["id"], quote=True)}" '
                            f'aria-pressed="false"{disabled}>{html.escape(group["name"])} <span>{len(group["cards"])}</span></button>')
            body += (f'<div class="record-browser" data-record-browser><div class="record-filter-list" role="group" aria-label="按目录筛选">{filters}</div>'
                     f'<p class="record-filter-status" role="status" aria-live="polite" data-filter-status>全部 {total} 条，当前匹配 {total} 条</p></div>'
                     '<p class="empty" data-filter-empty hidden>没有符合当前条件的资料。</p>')
            has_high = any(r["kind"] != "news" and r["score"] is not None and r["score"] >= 4 for g in selected for r, _, _ in g["cards"])
            has_low = any(r["kind"] != "news" and r["score"] is not None and r["score"] < 4 for g in selected for r, _, _ in g["cards"])
            if has_low and not has_high:
                body += '<p class="notice">本期未发现高相关技术，以下内容相关度较低，仅供参考。</p>'
        for group in selected:
            group_id = group["id"] if section_id == "key-updates" else "group-" + digest([section_id, group["id"]])[:20]
            escaped_group_id = html.escape(group_id, quote=True)
            body += (f'<div class="report-group" data-report-group="{html.escape(group["id"], quote=True)}" '
                     f'data-group-name="{html.escape(group["name"], quote=True)}">')
            show_heading = section_id == "key-updates" or section_id == "latest-updates" and (config["detail_module"].get("mode") == "split" or group.get("coverage_group"))
            if show_heading:
                label = html.escape(group["name"]) + f' <span class="count">{len(group["cards"])}</span>'
                if group["cards"]:
                    subnav += f'<a class="subnav" href="#{escaped_group_id}">{label}</a>'
                    body += (f'<header class="group-heading"><h3 id="{escaped_group_id}">'
                             f'{html.escape(group["name"])}<span class="group-count">{len(group["cards"])}条</span></h3>')
                    if group.get("local_review"):
                        body += '<p class="group-description">本期重点根据监控问题及已取得资料中的技术问题、方案和效果证据复核入选，保留入选依据与原文摘录。</p>'
                    body += '</header>'
                else:
                    subnav += f'<span class="subnav disabled" aria-disabled="true">{label}</span>'
            paginated = section_id in {"key-updates", "latest-updates", "supplementary"}
            list_id = escaped_group_id + "-records"
            list_class = "feature-grid" if section_id == "key-updates" else "record-list"
            pagination = (f' id="{list_id}" data-record-group data-initial-visible="{RECORD_PREVIEW_COUNT}" '
                          f'data-load-step="{RECORD_BATCH_SIZE}"') if paginated else ""
            body += f'<div class="{list_class}"{pagination}>'
            for index, (record, result, fields) in enumerate(group["cards"]):
                body += card(record, result, fields, card_ids[(offset, record["key"])], section_id == "supplementary",
                             section_id == "key-updates" or bool(result), group.get("review_notes", {}).get(record["key"]),
                             initially_hidden=paginated and index >= RECORD_PREVIEW_COUNT)
            body += '</div>'
            if paginated and len(group["cards"]) > RECORD_PREVIEW_COUNT:
                body += (f'<button class="record-more" type="button" data-record-more aria-controls="{list_id}" '
                         f'aria-label="查看更多{html.escape(group["name"], quote=True)}，每次最多{RECORD_BATCH_SIZE}条">查看更多</button>')
            body += '</div>'
            offset += 1
        if not any(g["cards"] for g in selected):
            body += '<p class="empty">本期暂无符合当前目录条件的记录。</p>'
        section_count = len({record["key"] for group in selected for record, _, _ in group["cards"]})
        add_section(section_id, title, body, subnav, section_count)
    if not sections:
        sections.append('<p class="empty">本期暂无可显示内容。</p>')
    assets = ROOT / "assets"
    title = config.get("pulse_name") or data["basic_info"].get("title") or "情报监控简报"
    scope = config.get("core_subject")
    scope_line = f'<p class="cover-scope">关注范围 · {html.escape(scope)}</p>' if isinstance(scope, str) and scope.strip() else ""
    focus_keys = sorted({record["key"] for group in typicals for record, _, _ in group["cards"]})
    high_keys = sorted(high_record_keys(data))
    from overview_metrics import build_overview_metrics
    selection = history_charts["model"].get("dimension_selection") if history_charts else None
    news_keys = sorted({record["key"] for group in news_groups for record, _, _ in group["cards"]})
    metrics, skipped_metrics = build_overview_metrics(config, data, focus_keys, high_keys, news_keys, selection)
    metric_cards = ""
    for metric in metrics:
        encoded_keys = html.escape(json.dumps(metric["keys"], ensure_ascii=False), quote=True)
        payload = html.escape(json.dumps(metric, ensure_ascii=False), quote=True)
        label = html.escape(metric["label"])
        detail = target["start_date"] + " 至 " + target["end_date"]
        if metric["coverage"]:
            coverage = metric["coverage"]
            detail += f' · 有信息 {coverage["classified"]}／{coverage["eligible"]} 条{coverage["population"]}'
        else:
            detail += " · 按资料去重计数"
        unit = "项" if metric["kind"] == "groups" else "条资料"
        metric_cards += (f'<button type="button" class="visual-metric" data-summary-metric="{html.escape(metric["key"], quote=True)}" '
                         f'data-metric-kind="{metric["kind"]}" data-value="{metric["value"]}" '
                         f'data-record-keys="{encoded_keys}" data-metric="{payload}" '
                         f'aria-label="{label}，{metric["value"]} {unit}，查看来源" title="{html.escape(detail, quote=True)}">'
                         f'<strong>{metric["value"]}</strong><span class="visual-metric-name">{label}</span></button>')
    from charts import javascript as chart_javascript
    page = Template((assets / "report.html").read_text(encoding="utf-8")).substitute(
        title=html.escape(title), period=html.escape(target["period"]),
        report_kind="每周情报报告" if target["period_type"] == "week" else "每月情报报告",
        year=target["period"][:4], edition=("W" if target["period_type"] == "week" else "M") + target["period"][4:], scope_line=scope_line,
        start_date=html.escape(target["start_date"], quote=True), end_date=html.escape(target["end_date"], quote=True),
        metric_cards=metric_cards, metric_overview_hidden="",
        dates=html.escape(target["start_date"] + " 至 " + target["end_date"]),
        css=tokens + "\n" + theme_css(theme) + "\n" + (assets / "report.css").read_text(encoding="utf-8"),
        javascript=(assets / "report.js").read_text(encoding="utf-8") + "\n" + (assets / "record-filter.js").read_text(encoding="utf-8") + ("\n" + chart_javascript() if history_charts else ""),
        navigation="".join(navigation), sections="".join(sections))
    expected = high_record_keys(data)
    visible = {r["key"] for group in all_groups for r, _, _ in group["cards"]}
    require(expected <= visible, "高相关记录未完整显示")
    checks = {"groups": [{"name": group["name"], "count": len(group["cards"])} for group in all_groups],
              "visible_unique_records": len({r["key"] for group in all_groups for r, _, _ in group["cards"]}),
              "expected_high_record_keys": sorted(expected), "visible_record_keys": sorted(visible),
              "high_record_coverage_required": True, "high_record_count": len(expected),
              "visible_high_record_count": len(expected.intersection(visible)), "missing_high_record_keys": sorted(expected - visible),
              "service_typical_records": sum(len(group["cards"]) for group in typicals if not group.get("local_review")),
              "reviewed_focus_records": sum(len(group["cards"]) for group in typicals if group.get("local_review")),
              "overview_metrics": {"focus": len(focus_keys), "high-relevance": len(high_keys)},
              "overview_metric_details": metrics, "overview_metric_skipped_fields": skipped_metrics,
              "news_records": len({record["key"] for group in news_groups for record, _, _ in group["cards"]}),
              "detail_submenus": [{"name": group["name"], "count": len(group["cards"])}
                                  for group in groups if group.get("configured_module")],
              "unclassified_records": sum(len(g["cards"]) for g in groups if g.get("unclassified")),
              "config_updated_at": config.get("updated_at"),
              "period_config_version": data.get("config_version", data.get("basic_info", {}).get("config_version"))}
    if history_charts is not None:
        checks["history"] = {"presentation_engine": "browser", **history_charts["checks"]}
    checks["theme"] = theme_info(theme)
    return page, checks


def build_history_report(config: dict, target: dict, tokens: str, bundle: dict,
                         theme: str | None = None) -> tuple[str, dict]:
    from charts import javascript as chart_javascript, section_title
    assets = ROOT / "assets"
    title = config.get("pulse_name") or "情报监控简报"
    heading = html.escape(section_title(bundle))
    page = Template((assets / "report.html").read_text()).substitute(
        title=html.escape(title), period=target["period"], report_kind="历史情报比较报告",
        year=target["period"][:4], edition=("M" if target["period_type"] == "month" else "W") + target["period"][4:], scope_line="",
        start_date=html.escape(target["start_date"], quote=True), end_date=html.escape(target["end_date"], quote=True),
        metric_cards="", metric_overview_hidden=" hidden",
        dates=html.escape(target["start_date"] + " 至 " + target["end_date"]),
        css=tokens + "\n" + theme_css(theme) + "\n" + (assets / "report.css").read_text(), javascript=(assets / "report.js").read_text() + "\n" + chart_javascript(),
        navigation='<div class="nav-chapter"><a class="chapter-link" href="#recent-changes">' + heading + '</a></div>',
        sections='<section class="report-panel" id="recent-changes" aria-labelledby="recent-changes-title"><div class="section-heading">'
                 '<span class="section-number" aria-hidden="true">01</span><h2 id="recent-changes-title">' + heading + '</h2></div>'
                 '<p class="section-intro">目标期没有可用于本期明细的完整结果，以下展示已经取得的历史资料。</p>'
                 + bundle["html"] + '</section>')
    return page, {"report_scope": "history_only", "target_data_available": False, "visible_record_keys": [], "theme": theme_info(theme),
                  "history": {"presentation_engine": "browser", **bundle["checks"]}}


def check_html(page: str) -> dict:
    soup = BeautifulSoup(page, "html.parser")
    require(all(len(soup.find_all(name)) == 1 for name in ["html", "head", "body", "title"]),
            "HTML 文档结构不完整或包含重复根节点")
    require(bool(soup.title.get_text(strip=True)), "HTML 缺少报告标题")
    for key, name in {"content": "main", "record-drawer": "dialog", "drawer-close": "button",
                      "record-drawer-body": "div", "record-citation-list": "div",
                      "metric-source-dialog": "dialog", "metric-source-body": "div",
                      "print-button": "button"}.items():
        require(soup.find(name, id=key) is not None, "HTML 缺少页面功能节点：" + key)
    ids = [node["id"] for node in soup.select("[id]")]
    require(len(ids) == len(set(ids)), "HTML 锚点重复")
    for link in soup.select('a[href^="#"]'):
        require(link["href"][1:] in ids, "HTML 内部引用无法定位")
    for link in soup.select("a[href]"):
        require(link["href"].startswith("#") or safe_url(link["href"]), "HTML 包含不安全链接")
    for image in soup.select("img"):
        require(safe_url(image.get("src")), "HTML 包含不安全图片")
    require(not soup.select("script[src], link[rel=stylesheet], iframe, object, embed, [onclick], [onerror]"),
            "HTML 包含外部脚本、外部样式或不允许的元素")
    cards = soup.select("article.record")
    paginated = soup.select("[data-record-group]")
    for group in paginated:
        rows = group.find_all("article", class_="record", recursive=False)
        require(group.get("data-initial-visible") == str(RECORD_PREVIEW_COUNT) and
                group.get("data-load-step") == str(RECORD_BATCH_SIZE), "子目录展示数量设置无效")
        require([row.has_attr("hidden") for row in rows] ==
                [index >= RECORD_PREVIEW_COUNT for index in range(len(rows))], "子目录初始展示数量不一致")
        button = soup.find("button", attrs={"data-record-more": True, "aria-controls": group["id"]})
        require((button is not None) == (len(rows) > RECORD_PREVIEW_COUNT), "子目录查看更多入口不一致")
    card_index = {card["id"]: card for card in cards}
    for card in cards:
        title = card.select_one(":scope > h4 .record-title")
        tag = card.select_one(":scope > h4 .record-kind")
        kind = card.get("data-record-key", "").partition(":")[0]
        require(card.get("data-record-key") and title and title.get_text(strip=True) not in
                {"", "专利资料", "论文资料", "新闻资料"}, "卡片缺少可识别的标题或资料身份")
        require(tag and tag.get("data-record-kind") == kind and tag.get_text() == TYPE_NAMES.get(kind),
                "资料类型标签与原始类型不一致")
        require(any(node.get_text(strip=True) for node in card.select(".field dd, .rich-text")),
                "卡片缺少有效文字内容")
        source = soup.find(id=card.get("data-detail-target"))
        require(source is not None and "record-detail-source" in source.get("class", []) and source.parent == card,
                "资料抽屉缺少对应内容：" + card["data-record-key"])
    citations = soup.select("a.citation-link")
    for citation in citations:
        target = citation.get("data-record-target")
        require(target in card_index and citation.get("href") == "#" + target and
                citation.get("aria-controls") == "record-drawer" and citation.get("aria-haspopup") == "dialog",
                "引用与资料抽屉的对应关系无效")
        require(citation.parent.name == "sup" and "citation" in citation.parent.get("class", []) and
                citation.get_text().startswith("[") and citation.get_text().endswith("]"), "引用缺少独立上标样式")
    browsers = soup.select('[data-record-browser]')
    for browser in browsers:
        section = browser.find_parent("section")
        require(browser.select_one('[data-filter-group="all"][aria-pressed="true"]') is not None and
                browser.select_one('[data-filter-status]') is not None, "技术资料筛选缺少全部入口或数量")
        for group in section.select('[data-record-group]'):
            require(group.find_parent(attrs={"data-report-group": True}) is not None, "技术目录缺少筛选分组")
    return {"page_structure_checked": True, "anchors": len(ids), "cards": len(cards), "type_tags_checked": len(cards),
            "empty_cards": 0, "internal_links_valid": True, "citation_links_checked": len(citations),
            "record_drawer_sources_checked": len(cards),
            "record_group_previews_checked": len(paginated), "record_preview_count": RECORD_PREVIEW_COUNT,
            "record_load_step": RECORD_BATCH_SIZE,
            "record_browsers_checked": len(browsers),
            "initially_visible_record_count": sum(not card.has_attr("hidden") for card in cards),
            "unresolved_citations": [node.get("data-citation-ref") for node in soup.select(".citation-unavailable")]}


def check_coverage(page: str, data: dict) -> dict:
    expected = high_record_keys(data)
    soup = BeautifulSoup(page, "html.parser")
    actual = {node.get("data-record-key") for node in soup.select("article.record")}
    missing = sorted(expected - actual)
    require(not missing, "HTML 缺少高相关记录：" + ", ".join(missing))
    expected_news = set(news_records(data))
    news_cards = soup.select('#news-updates article.record')
    require({node.get("data-record-key") for node in news_cards} == expected_news and len(news_cards) == len(expected_news),
            "新闻章节缺少资料或包含重复记录")
    require(not any(node.get("data-record-key", "").startswith("news:") for node in soup.select('section:not(#news-updates) article.record')),
            "新闻资料重复进入技术章节")
    return {"news_coverage_checked": len(expected_news), "high_record_coverage_required": True, "high_record_count": len(expected),
            "visible_high_record_count": len(expected.intersection(actual)), "missing_high_record_keys": missing}


def check_presentation(page: str, config: dict, data: dict, focus: dict | None = None, review: dict | None = None) -> dict:
    soup = BeautifulSoup(page, "html.parser")
    news_groups, typicals, groups, supplements = report_groups(config, data, focus, review)
    global_fields = ai_field_index(config)
    labels = {**LABELS, **{key: item.get("display_name", key) for key, item in global_fields.items()}}
    configured_count, special_count, figure_count, primary_count, enum_count, label_count = 0, 0, 0, 0, 0, 0
    citation_summary_count = 0
    unresolved = []
    sections = [("news-updates", news_groups), ("key-updates", typicals), ("latest-updates", groups),
                ("supplementary", [{"cards": [(record, None, config["card_fields"]) for record in supplements]}])]
    for section_id, selected in sections:
        section = soup.find(id=section_id)
        for group in selected:
            for record, result, definition in group["cards"]:
                card = section.find("article", attrs={"data-record-key": record["key"]}) if section else None
                require(card is not None, "字段检查未找到记录：" + record["key"])
                layout = card.select_one(":scope > .record-layout")
                local_fields = resolve_ai_fields(config, definition) if "card_fields" in definition else []
                ai_keys = set(global_fields) | {item["field_key"] for item in local_fields}
                if record["kind"] == "patent":
                    key, value = citation_summary(record, ai_keys)
                    template = card.select_one(":scope > template.citation-summary-source")
                    require((template is not None) == (key is not None), "引用列表正文来源缺失或多余：" + record["key"])
                    if key is not None:
                        require(template.get("data-field-key") == key, "引用列表正文使用了其他字段：" + record["key"])
                        expected_text = BeautifulSoup(render_value(value, {}), "html.parser").get_text(" ", strip=True)
                        actual_text = BeautifulSoup(template.decode_contents(), "html.parser").get_text(" ", strip=True)
                        require(actual_text == expected_text, "引用列表正文与原始资料不一致：" + record["key"])
                        citation_summary_count += 1
                fields = definition.get("card_fields", definition).get(record["kind"], [])
                lead = layout.select_one(".record-lead")
                skip = {"pn" if record["kind"] == "patent" else "doi" if record["kind"] == "paper" else None,
                        "company", "PBD", "title", "score", "link", "analysis", lead.get("data-field-key") if lead else None}
                expected = [key for key in fields if key not in skip and present(field(record, key, ai_keys))]
                formats = {key: item.get("data_format") for key, item in global_fields.items()}
                formats.update({item["field_key"]: item.get("data_format") for item in local_fields})
                expected = [key for key in expected if formats.get(key) == "enum"] + [key for key in expected if formats.get(key) != "enum"]
                nodes = card.select(":scope > .record-configured > .field, :scope > .record-layout .record-configured > .field")
                actual = [node["data-field-key"] for node in nodes]
                require(actual == expected, "配置字段显示不完整或顺序不一致：" + record["key"])
                for key, node in zip(expected, nodes):
                    label = labels.get(key, key)
                    require(node.dt is not None and node.dt.get_text() == label,
                            "配置字段名称与全局定义不一致：" + record["key"] + ":" + key)
                    label_count += key in global_fields
                    value = field(record, key, ai_keys)
                    if global_fields.get(key, {}).get("data_format") == "enum":
                        values = value if isinstance(value, list) else [value]
                        tags = node.dd.select(".record-tags > .record-tag")
                        require([tag.get_text() for tag in tags] == [str(item) for item in values] and
                                all(tag.get("title") == label for tag in tags),
                                "枚举字段显示与全局定义不一致：" + record["key"] + ":" + key)
                        enum_count += 1
                    else:
                        require(not node.dd.select(".record-tags"),
                                "枚举字段显示与全局定义不一致：" + record["key"] + ":" + key)
                        source_text = BeautifulSoup(render_value(value, {}), "html.parser").get_text(" ", strip=True)
                        require(source_text == node.dd.get_text(" ", strip=True), "配置字段内容不一致：" + record["key"] + ":" + key)
                configured_count += len(expected)
                if section_id == "latest-updates" and record["kind"] in {"patent", "paper"}:
                    primary = "technical_title" if present(field(record, "technical_title", ai_keys)) else "abstract"
                    if present(field(record, primary, ai_keys)):
                        require(lead is not None and lead.get("data-field-key") == primary, "默认技术标题或摘要未显示：" + record["key"])
                        source_text = BeautifulSoup(render_value(field(record, primary, ai_keys), {}), "html.parser").get_text(" ", strip=True)
                        require(source_text in lead.get_text(" ", strip=True), "默认正文内容不一致：" + record["key"])
                        primary_count += 1
                if section_id != "key-updates" and not (section_id == "news-updates" and result):
                    continue
                for key, label_key, default in [("display_summary", "display_summary_field_name", "重点摘要"),
                                                ("extracted_content", "extract_content_field_name", "专项解读")]:
                    if present((result or {}).get(key)):
                        node = layout.select_one('.record-special[data-field-key="' + key + '"]')
                        require(node is not None and node.select_one(".field-label").get_text() == str(result.get(label_key) or default),
                                "重点特殊字段或名称未显示：" + record["key"] + ":" + key)
                        source_text = BeautifulSoup(render_value(result[key], {}), "html.parser").get_text(" ", strip=True)
                        require(source_text in node.get_text(" ", strip=True), "重点特殊字段内容不一致：" + record["key"] + ":" + key)
                        special_count += 1
                expected_figures = selected_figures(record, result)
                unresolved.extend({"record_key": record["key"], "figure_no": figure["number"]}
                                  for figure in expected_figures if not figure["url"])
                expected_figures = [figure for figure in expected_figures if figure["url"]]
                figures = layout.select(".selected-figures figure")
                require(len(figures) == len(expected_figures), "已选图片显示数量不一致：" + record["key"])
                for node, expected_figure in zip(figures, expected_figures):
                    require(node.get("data-figure-no") == expected_figure["number"], "已选图片图号不一致")
                    if expected_figure["url"]:
                        require(node.img is not None and node.img.get("src") == expected_figure["url"], "已选图片地址不一致")
                        figure_count += 1
    return {"configured_fields_checked": configured_count, "typical_special_fields_checked": special_count,
            "global_ai_field_labels_checked": label_count, "enum_fields_checked": enum_count,
            "selected_figures_checked": figure_count, "unresolved_selected_figures": unresolved,
            "citation_patent_summaries_checked": citation_summary_count,
            "default_technical_body_checked": primary_count}


def report_filename(config: dict, target: dict, topic: str | None = None,
                    history_charts: dict | None = None, history_only: bool = False) -> str:
    title = topic or config.get("pulse_name") or config.get("core_subject")
    require(isinstance(title, str) and title.strip(), "请通过 --report-name 提供报告主题")
    invalid = '<>:"/\\|?*'
    title = " ".join("".join("_" if character in invalid or ord(character) < 32 else character
                            for character in title).split()).strip(" ._")
    while len(title.encode("utf-8")) > 160:
        title = title[:-1]
    require(bool(title), "报告主题需要包含有效文件名文字")
    start, end = target["start_date"], target["end_date"]
    kind = "情报周报" if target["period_type"] == "week" else "情报月报"
    if history_only:
        require(history_charts is not None, "历史报告缺少日期范围")
        periods = history_charts["model"]["periods"]
        start, end = periods[0]["target"]["start_date"], periods[-1]["target"]["end_date"]
        kind = "历史情报比较报告"
    return f"{title}_{parse_date(start).isoformat()}至{parse_date(end).isoformat()}_{kind}.html"


def main() -> None:
    parser = argparse.ArgumentParser(description="自动生成情报监控 HTML 简报")
    for key in ["config", "data", "target", "inputs", "charts"]:
        parser.add_argument("--" + key, type=Path)
    output = parser.add_mutually_exclusive_group(required=True)
    output.add_argument("--output-dir", type=Path)
    output.add_argument("--output", type=Path)
    parser.add_argument("--report-name")
    parser.add_argument("--theme", help="报告色系的英文标识或中文名称")
    args = parser.parse_args()
    theme = resolve_theme(args.theme)
    require(args.output is None or args.output.name.lower() != "report.html", "请使用包含主题和周期的文件名，或通过 --output-dir 自动命名")
    require(not args.report_name or args.output_dir is not None, "--report-name 需要配合 --output-dir 使用")
    base_path = report_assets() / "report-base.css"
    base_styles = source_ref(base_path)
    tokens = base_path.read_text(encoding="utf-8")
    if args.inputs:
        require(not any([args.config, args.data, args.target, args.charts]), "inputs 与独立输入参数只能选择一种")
        references = load_json(args.inputs)
        paths = {key: check_source(reference) for key, reference in references.items()}
        require(all(key in paths for key in ["config", "target"]) and ("data" in paths or "charts" in paths),
                "输入清单需要配置、目标及本期结果或历史图表")
    else:
        require(args.config and args.target and (args.data or args.charts), "必须提供 config、target 及 data 或 charts")
        paths = {key: getattr(args, key) for key in ["config", "data", "target", "charts"] if getattr(args, key)}
        references = {key: source_ref(path) for key, path in paths.items()}
    inputs = list(paths.values()) + ([args.inputs] if args.inputs else []) + [base_path]
    chart_sources = []
    history_charts = None
    if "charts" in paths:
        from charts import bundle_sources, load_charts
        history_charts = load_charts(paths["charts"], references["config"], references["target"])
        chart_sources = bundle_sources(history_charts)
        inputs += [check_source(reference) for reference in chart_sources]
    elif "data" in paths:
        from charts import bundle_sources, make_current_bundle
        history_charts = make_current_bundle(paths["config"], paths["data"], paths["target"])
        chart_sources = bundle_sources(history_charts)
        inputs += [check_source(reference) for reference in chart_sources]
    config, target = report_config(load_json(paths["config"])), load_json(paths["target"])
    data = period_data(load_json(paths["data"])) if "data" in paths else None
    if args.output_dir:
        name = report_filename(config, target, args.report_name, history_charts, data is None)
        if args.theme is not None:
            name = Path(name).stem + "_" + theme_info(theme)["name"] + ".html"
        args.output = args.output_dir / name
    distinct_output(args.output, inputs)
    distinct_output(args.output.with_suffix(".checks.json"), inputs)
    if data is not None:
        validate_inputs(config, data, target)
    else:
        require(history_charts is not None, "历史报告缺少图表输入")
        require(history_charts["model"]["periods"][-1]["status"] != "available", "目标期已有资料，请提供完整本期结果")
    require(("focus" in paths) == ("review" in paths), "本期重点审核需要同时提供 focus 与 review")
    focus = load_json(paths["focus"]) if "focus" in paths else None
    review = load_json(paths["review"]) if "review" in paths else None
    if review:
        require(data is not None, "本期资料审核需要目标期资料")
        require(review.get("data_source") == references["data"], "重点审核引用了其他周期响应")
        require(review.get("period") == target["period"], "重点审核的 period 不一致")
    if data is not None:
        page, checks = build_page(config, data, target, tokens, focus, review, history_charts, theme)
        checks.update(check_coverage(page, data))
        checks.update(check_presentation(page, config, data, focus, review))
        checks.update(check_summary_ids(page, MARKDOWN.render(summary_text(data)), summary_identity_index(data)))
        checks.update(check_summary_citation_groups(page, MARKDOWN.render(summary_text(data))))
    else:
        page, checks = build_history_report(config, target, tokens, history_charts, theme)
    checks.update(check_html(page))
    actual = {node["data-record-key"] for node in BeautifulSoup(page, "html.parser").select("article.record")}
    require(actual == set(checks["visible_record_keys"]), "HTML 与记录索引不一致")
    for reference in list(references.values()) + chart_sources + [base_styles]:
        check_source(reference)
    args.output = args.output.resolve()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(page, encoding="utf-8")
    for reference in list(references.values()) + chart_sources + [base_styles]:
        check_source(reference)
    checks.update({"passed": True, "created_at": utc_now(), "target": target,
                   "config_sha256": digest(config), "data_sha256": digest(data),
                   "sources": references, "raw_sources_unchanged": True,
                   "base_styles": base_styles, "browser_checked": False})
    receipt = write_json(args.output.with_suffix(".checks.json"), checks)
    print(json.dumps({"html": str(args.output), "checks": str(receipt), "cards": checks["cards"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()

from common import ai_field_index, require
from history import categorical_values, company_dimensions, record_pool


def record_metric(key: str, label: str, keys: list[str]) -> dict:
    members = sorted(set(keys))
    return {"key": key, "label": label, "kind": "records", "value": len(members),
            "keys": members, "groups": [], "coverage": None}


def group_metric(key: str, label: str, members: dict, eligible: list[str], population: str) -> dict | None:
    groups = [{"label": name, "keys": sorted(set(keys))} for name, keys in members.items() if keys]
    if not groups:
        return None
    groups.sort(key=lambda item: (-len(item["keys"]), item["label"]))
    keys = sorted({key for group in groups for key in group["keys"]})
    coverage = {"classified": len(keys), "eligible": len(set(eligible)), "population": population}
    require(set(keys) <= set(eligible), "顶部卡片的分类资料超出适用范围")
    return {"key": key, "label": label, "kind": "groups", "value": len(groups),
            "keys": keys, "groups": groups, "coverage": coverage}


def build_overview_metrics(config: dict, data: dict, focus_keys: list[str], high_keys: list[str],
                           news_keys: list[str], selection: dict | None = None) -> tuple[list[dict], list[dict]]:
    from render_report import in_scope

    pool = record_pool(data)
    selected = selection or {}
    high = {key: pool[key] for key in high_keys}
    metrics = [record_metric("focus", "重点解读", focus_keys), record_metric("high-relevance", "高相关技术", high_keys)]
    company_pool = {**high, **{key: pool[key] for key in news_keys}}
    companies = {item["id"]: item for item in company_dimensions(company_pool)}
    company_order = [selected.get("company_trend_dimension"), "company:patent", "company:paper", "company:news"]
    for key in dict.fromkeys(company_order):
        if key not in companies:
            continue
        company = companies[key]
        metric = group_metric(key, company["name"], company["members"], company["eligible_members"],
                              "已展示新闻" if key == "company:news" else "高相关技术资料")
        if metric:
            metrics.append(metric)
            break
    fields = ai_field_index(config)
    main = selected.get("category_trend_dimension", "")
    main = main.removeprefix("field:") if main else None
    priority = [main, selected.get("company_route_field"), *selected.get("priority_order", []), *fields]
    skipped = []
    for key in dict.fromkeys(priority):
        if key not in fields or fields[key].get("data_format") != "enum":
            continue
        definition = fields[key]
        eligible = [record for record in company_pool.values() if in_scope(record, definition["data_scope"])]
        members = {}
        for record in eligible:
            for name in categorical_values(record["fields"].get(key)):
                members.setdefault(name, []).append(record["key"])
        population = "高相关技术与已展示新闻" if any(record["kind"] == "news" for record in eligible) else "高相关技术资料"
        metric = group_metric("field:" + key, definition.get("display_name", key), members,
                              [record["key"] for record in eligible], population)
        if metric is None:
            skipped.append({"field_key": key, "reason": "没有实际分类值", "eligible": len(eligible)})
            continue
        if len(metrics) < 5:
            metrics.append(metric)
    if len(metrics) < 4:
        for kind, label, keys in [("patent", "高相关专利", [key for key in high if pool[key]["kind"] == "patent"]),
                                 ("paper", "高相关论文", [key for key in high if pool[key]["kind"] == "paper"]),
                                 ("news", "相关新闻", news_keys)]:
            metric = record_metric("type:" + kind, label, keys)
            if keys and not any(item["kind"] == "records" and item["keys"] == metric["keys"] for item in metrics):
                metrics.append(metric)
            if len(metrics) >= 5:
                break
    require(len(metrics) <= 5 and len({item["key"] for item in metrics}) == len(metrics), "顶部卡片数量或字段唯一性无效")
    require(all(set(item["keys"]) <= set(pool) for item in metrics), "顶部卡片引用了不存在的资料")
    return metrics, skipped

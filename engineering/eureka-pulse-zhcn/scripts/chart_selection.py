import math

from common import check_source, load_json, report_config, require


ROLES = ("technology_route", "product_line", "technical_field")
COMPANY_DIMENSIONS = ("company:patent", "company:paper", "company:news")


def select_dimensions(statistics: dict, selection: dict) -> dict:
    require(selection.get("schema_version") == 1, "图表维度选择文件版本无效")
    config = report_config(load_json(check_source(statistics["config"])))
    fields = {item["field_key"]: item for item in config.get("ai_fields", [])}
    roles = selection.get("fields", [])
    require(isinstance(roles, list) and all(isinstance(item, dict) for item in roles), "分类字段角色必须为对象数组")
    require(len({item.get("field_key") for item in roles}) == len(roles), "图表字段角色不能重复")
    require(all(item.get("field_key") in fields and item.get("role") in ROLES for item in roles),
            "图表字段角色必须引用配置中的真实字段及支持的角色")
    require(all(fields[item["field_key"]].get("data_format") == "enum" for item in roles),
            "图表分类维度必须使用枚举字段")
    priority = selection.get("priority_order", [])
    reason = selection.get("priority_reason")
    require(isinstance(priority, list) and len(set(priority)) == len(priority) and
            set(priority) == {item["field_key"] for item in roles}, "AI 优先顺序必须完整引用已登记的分类字段")
    require(isinstance(reason, str) and bool(reason.strip()), "图表维度选择需要说明业务依据")
    available = [period for period in statistics["periods"] if period["status"] == "available"]
    candidates = []
    for item in roles:
        key = item["field_key"]
        dimensions = [(period, dimension) for period in available for dimension in period["dimensions"]
                      if dimension["id"] == "field:" + key and any(dimension["members"].values())]
        if not dimensions:
            continue
        level = fields[key].get("level")
        require(level is None or (type(level) in (int, float) and math.isfinite(level)),
                "图表字段 level 必须为实际返回的有限数值或缺失")
        cross_periods = []
        for period, dimension in dimensions:
            component = dimension.get("components", {}).get("patent", {})
            company = next((value for value in period["dimensions"] if value["id"] == "company:patent"), None)
            if not component.get("complete") or company is None:
                continue
            company_keys = {key for keys in company["members"].values() for key in keys}
            if any(company_keys.intersection(keys) for keys in component["members"].values()):
                cross_periods.append(period["target"]["period"])
        candidates.append({"field_key": key, "dimension_id": "field:" + key, "role": item["role"],
                           "level": level, "periods": [period["target"]["period"] for period, _ in dimensions],
                           "cross_periods": cross_periods})
    company = next((key for key in COMPANY_DIMENSIONS if any(dimension["id"] == key and any(dimension["members"].values())
                   for period in available for dimension in period["dimensions"])), None)
    trend_candidates = [item for item in candidates if len(item["periods"]) >= 2] or candidates
    ranked = [item for item in trend_candidates if item["level"] is not None]
    if ranked:
        highest = max(item["level"] for item in ranked)
        ranked = [item for item in ranked if item["level"] == highest]
    else:
        ranked = trend_candidates
    trend = min(ranked, key=lambda item: priority.index(item["field_key"])) if ranked else None
    cross_candidates = [item for item in candidates if item["cross_periods"]]
    cross = min(cross_candidates, key=lambda item: (ROLES.index(item["role"]),
                priority.index(item["field_key"]))) if cross_candidates else None
    return {"schema_version": 1, "company_trend_dimension": company,
            "category_trend_dimension": trend["dimension_id"] if trend else None,
            "category_trend_basis": "field_level" if trend and trend["level"] is not None else "ai_analysis",
            "category_trend_level": trend["level"] if trend else None,
            "company_route_field": cross["field_key"] if cross else None,
            "company_route_role": cross["role"] if cross else None,
            "priority_reason": reason, "priority_order": priority, "candidates": candidates,
            "layout": "two_trends_then_company_cross"}

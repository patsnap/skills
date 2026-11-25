from __future__ import annotations

from common import check_source, digest, require


def definitions(value: dict | list) -> list[dict]:
    if isinstance(value, dict):
        require(isinstance(value.get("monitoring_objective"), str) and bool(value["monitoring_objective"].strip()),
                "重点规则需要明确监控目标")
    items = value.get("typical_filters") if isinstance(value, dict) else value
    require(isinstance(items, list) and bool(items), "需要根据监控需求配置非空 typical_filters")
    keys, names = set(), set()
    for item in items:
        require(isinstance(item, dict), "重点规则必须为对象")
        for key in ["name", "judgement", "focus_guidance", "output_guidance"]:
            require(isinstance(item.get(key), str) and bool(item[key].strip()), f"重点规则缺少 {key}")
        require(isinstance(item.get("data_scope"), list) and bool(item["data_scope"]), "重点规则缺少资料类型")
        require(all(isinstance(scope, str) and bool(scope) for scope in item["data_scope"]), "重点资料类型必须为非空字符串")
        require(isinstance(item.get("card_fields"), dict), "重点规则缺少展示字段")
        kinds = {scope if scope in {"paper", "news"} else "patent" for scope in item["data_scope"]}
        for kind in kinds:
            fields = item["card_fields"].get(kind)
            require(isinstance(fields, list) and bool(fields) and all(isinstance(field, str) and bool(field) for field in fields),
                    f"重点规则缺少 {kind} 展示字段")
        identity = item.get("key") or "typical-" + digest(item["name"])[:20]
        require(isinstance(identity, str) and identity and not any(char.isspace() for char in identity), "重点规则 key 无效")
        require(identity not in keys and item["name"] not in names, "重点规则 key 或名称重复")
        keys.add(identity)
        names.add(item["name"])
    return items


def review_groups(plan: dict, review: dict, pool: dict, pulse_id: str) -> list[dict]:
    criteria = definitions(plan)
    require(review.get("source") == "local_evidence_review", "重点筛选必须声明实际来源")
    require(review.get("pulse_id") == pulse_id, "重点筛选的 pulse_id 不一致")
    raw = check_source(review["data_source"])
    require(raw.is_file(), "重点筛选缺少原始周期响应")
    require(review.get("focus_sha256") == digest(plan), "重点筛选对应的规则已变化")
    expected = {key for key, record in pool.items() if record["kind"] != "news" and
                record["score"] is not None and record["score"] >= 4}
    assessed = review.get("assessed_record_keys", [])
    require(isinstance(assessed, list) and all(isinstance(key, str) for key in assessed), "重点审核范围必须为记录键数组")
    require(len(assessed) == len(set(assessed)) and set(assessed) == expected, "重点审核未覆盖全部高相关技术记录")
    grouped = {item.get("key") or "typical-" + digest(item["name"])[:20]: [] for item in criteria}
    seen = set()
    require(isinstance(review.get("selections"), list), "重点筛选缺少 selections")
    if not review["selections"]:
        require(isinstance(review.get("no_selection_reason"), str) and bool(review["no_selection_reason"].strip()),
                "无重点入选时需要说明实际原因")
    for selection in review["selections"]:
        key, identity = selection["focus_key"], selection["record_key"]
        require(key in grouped and identity in pool, "重点筛选引用了不存在的规则或资料")
        require((key, identity) not in seen, "同一重点分组中资料重复")
        seen.add((key, identity))
        record = pool[identity]
        require(record["kind"] == "news" or record["score"] is not None and record["score"] >= 4,
                "技术重点必须来自真实高相关记录")
        require(isinstance(selection.get("reason"), str) and bool(selection["reason"].strip()), "重点筛选缺少入选依据")
        if "display_title" in selection:
            require(isinstance(selection["display_title"], str) and bool(selection["display_title"].strip()),
                    "重点阅读标题必须为非空文字")
        require(isinstance(selection.get("evidence"), list) and len(selection["evidence"]) >= 2,
                "每项重点至少需要两项原始字段证据")
        paths = set()
        for evidence in selection["evidence"]:
            path = evidence.get("path")
            require(isinstance(path, list) and bool(path), "证据必须明确原始字段位置")
            value = record["row"]
            for part in path:
                require(isinstance(part, (str, int)) and not isinstance(part, bool), "证据字段位置无效")
                value = value[part]
            quote = evidence.get("quote")
            require(isinstance(quote, str) and bool(quote.strip()) and isinstance(value, str) and quote in value,
                    "重点依据无法在原始字段中核实")
            paths.add(tuple(path))
        require(len(paths) >= 2, "重点依据必须来自不同原始字段")
        grouped[key].append((record, selection))
    result = []
    for definition in criteria:
        key = definition.get("key") or "typical-" + digest(definition["name"])[:20]
        selected = grouped[key]
        if selected:
            result.append({"id": "reviewed-" + key, "name": definition["name"], "local_review": True,
                           "definition": definition, "selections": selected})
    return result

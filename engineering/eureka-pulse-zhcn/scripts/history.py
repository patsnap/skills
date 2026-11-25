from __future__ import annotations

import argparse
import json
from datetime import timedelta
from pathlib import Path

from bs4 import BeautifulSoup

from common import (check_source, digest, distinct_output, encode_week, load_json, make_target,
                    parse_date, report_config, require, source_ref, unwrap, write_json)


STATISTICS_VERSION = 3


def window_key(target: dict) -> str:
    require(target["period_type"] in {"week", "month"}, "历史目标必须为自然周或自然月")
    return "months" if target["period_type"] == "month" else "weeks"


def history_targets(target: dict, count: int) -> list[dict]:
    period_type = target["period_type"]
    key = window_key(target)
    limit = 60 if key == "months" else 52
    require(type(count) is int and 1 <= count <= limit, f"历史窗口期数必须在 1 至 {limit} 之间")
    start = parse_date(target["start_date"])
    reference = parse_date(target["reference_date"])
    expected_current = make_target(target["pulse_id"], period_type, reference, target["period"], target["week_rule"])
    require(all(target[name] == expected_current[name] for name in expected_current), "历史目标日期与周期编码不一致")
    targets = []
    for offset in reversed(range(count)):
        if period_type == "month":
            year, month = divmod(start.year * 12 + start.month - 1 - offset, 12)
            period = f"{year:04d}{month + 1:02d}"
        else:
            period = encode_week(start - timedelta(weeks=offset), target["week_rule"])
        targets.append(make_target(target["pulse_id"], period_type, reference, period, target["week_rule"]))
    return targets


def plan_history(config_path: Path, target_path: Path, output: Path,
                 weeks: int | None = None, months: int | None = None) -> dict:
    require(not output.exists(), "历史清单已存在，请继续已有清单")
    config, target = report_config(load_json(config_path)), load_json(target_path)
    require(config["pulse_id"] == target["pulse_id"], "历史目标与配置身份不一致")
    key = window_key(target)
    require(months is None if key == "weeks" else weeks is None, "历史窗口参数必须与目标周期一致")
    count = (months if months is not None else 12) if key == "months" else (weeks if weeks is not None else 8)
    targets = history_targets(target, count)
    slots = []
    for expected in targets:
        period = expected["period"]
        arguments = {"pulse-id": target["pulse_id"], "period_type": target["period_type"], "period": period}
        path = output.parent / "periods" / period / "arguments.json"
        distinct_output(path, [config_path, target_path, output])
        slots.append({"target": expected, "arguments": str(write_json(path, arguments)), "status": "pending"})
    value = {"schema_version": 1, "config": source_ref(config_path), "target": source_ref(target_path),
             key: count, "periods": slots}
    distinct_output(output, [config_path, target_path])
    write_json(output, value)
    return value


def inspect_response(path: Path, target: dict) -> tuple[str, dict | None, str]:
    body = unwrap(load_json(path), allow_empty=True)
    if body is None or body == {} or body == []:
        return "missing", None, "服务明确返回该期无数据"
    require(isinstance(body, dict), "历史周期响应类型无效")
    if body.get("status") == "NOT_FOUND" or body.get("run_status") == "NOT_FOUND":
        return "missing", None, "服务明确返回 NOT_FOUND"
    if "run_id" in body and "sub_tasks" in body:
        if body.get("status") == "NOT_FOUND":
            return "missing", None, "服务明确返回 NOT_FOUND"
        require(body.get("status") == "FINISHED", "历史任务尚未成功完成")
        body = body["data"]
        require(isinstance(body, dict), "历史任务缺少周期内容")
    require(body.get("run_status", "FINISHED") == "FINISHED", "历史周期尚未成功完成")
    require(body.get("complete", True) is True, "历史周期返回不完整")
    identity = body.get("basic_info", {}).get("pulse_id")
    require(identity == target["pulse_id"], "历史周期返回了其他简报")
    if "report_start_date" not in body or "report_end_date" not in body:
        return "unavailable", None, "返回内容没有完整起止日期，无法确认该期统计范围"
    require(parse_date(body["report_start_date"]) == parse_date(target["start_date"]) and
            parse_date(body["report_end_date"]) == parse_date(target["end_date"]), "历史响应日期与请求周期不一致")
    if not any(isinstance(body.get(key), (list, dict)) for key in ("tech_items", "hot_news")):
        return "unavailable", None, "返回内容没有可用于统计的记录集合"
    record_pool(body)
    return "available", body, ""


def attach_response(plan_path: Path, period: str, response: Path) -> dict:
    plan = load_json(plan_path)
    check_source(plan["config"])
    check_source(plan["target"])
    matches = [slot for slot in plan["periods"] if slot["target"]["period"] == period]
    require(len(matches) == 1, "响应期次不在历史窗口中")
    slot = matches[0]
    reference = source_ref(response)
    require(slot["status"] == "pending" or slot.get("source") == reference,
            "该期已经登记其他响应，请保留已有来源并核实结果版本")
    status, _, reason = inspect_response(response, slot["target"])
    slot.update({"status": status, "source": reference, "reason": reason})
    distinct_output(plan_path, [response, Path(plan["config"]["path"]), Path(plan["target"]["path"])])
    write_json(plan_path, plan)
    return {"period": period, "status": status, "reason": reason, "source": reference}


def record_pool(data: dict) -> dict:
    from render_report import normalize, records

    pool = {}
    rows = [(row, None, {}) for row in records(data.get("tech_items"), "tech_items")]
    rows += [(row, "news", {}) for row in records(data.get("hot_news"), "hot_news")]
    rows += [(item["record_info"], None, item.get("extracted_fields", {})) for item in records(data.get("typical_tech_interpret"), "typical_tech_interpret")
             if isinstance(item.get("record_info"), dict)]
    for row, kind, extracted in rows:
        record = normalize(row, kind)
        additions = {**extracted, **row.get("typical_extracted_fields", {})}
        for key, value in additions.items():
            require(key not in record["fields"] or record["fields"][key] == value, "重点资料提取字段内容冲突")
        record["fields"] = {**record["fields"], **additions}
        previous = pool.get(record["key"])
        if previous:
            require(previous["info"] == record["info"], "历史统计中同一记录身份内容冲突")
            require(previous["score"] is None or record["score"] is None or previous["score"] == record["score"],
                    "历史统计中同一记录相关度冲突")
            for key, value in record["fields"].items():
                require(key not in previous["fields"] or previous["fields"][key] == value,
                        "历史统计中同一记录提取字段冲突")
            previous["fields"] = {**previous["fields"], **record["fields"]}
            if previous["score"] is None:
                previous["score"] = record["score"]
        else:
            pool[record["key"]] = record
    return pool


def dimension_definitions(snapshot: dict, requested: list[str]) -> list[dict]:
    fields = snapshot.get("ai_fields", [])
    selected = [item for item in fields if item.get("field_key") in requested]
    if not requested:
        module_keys = {condition["filter_key"] for module in snapshot.get("detail_module", {}).get("sub_modules", [])
                       for condition in module.get("filter", []) if condition.get("filter_key")}
        displayed = {key for values in snapshot.get("card_fields", {}).values() if isinstance(values, list)
                     for key in values if isinstance(key, str)}
        selected = [item for item in fields if item.get("field_key") in module_keys.union(displayed)
                    and item.get("enum_options")]
    return selected


def categorical_values(value) -> list[str]:
    values = value if isinstance(value, list) else [value] if value is not None else []
    require(all(isinstance(item, str) for item in values), "统计维度必须返回字符串或字符串数组")
    return list(dict.fromkeys(item.strip() for item in values if item.strip()))


def definition_signature(definition: dict) -> str:
    basis = {key: value for key, value in definition.items() if key not in {"display_name", "level"}}
    for key in ("data_scope", "data_fields", "enum_options"):
        if isinstance(basis.get(key), list):
            basis[key] = sorted(basis[key], key=digest)
    return digest(basis)


def field_dimension(pool: dict, definition: dict, known: dict) -> dict:
    from render_report import PATENT_TYPES, in_scope

    key = definition["field_key"]
    components = {}
    for kind in ("patent", "paper"):
        types = {kind, *PATENT_TYPES.values(), "legal_event"} if kind == "patent" else {kind}
        if not types.intersection(definition["data_scope"]):
            continue
        applicable = [record for record in pool.values() if record["kind"] == kind and
                      in_scope(record, definition["data_scope"])]
        missing_scores = sum(record["score"] is None for record in applicable)
        eligible = [record for record in applicable if record["score"] is not None and record["score"] >= 4]
        members, classified = {}, []
        for record in eligible:
            labels = categorical_values(record["fields"].get(key))
            if labels:
                classified.append(record["key"])
            for label in labels:
                members.setdefault(label, []).append(record["key"])
        components[kind] = {"complete": known[kind] and missing_scores == 0,
                            "unknown_score_count": missing_scores, "members": members,
                            "eligible_members": [record["key"] for record in eligible],
                            "classified_count": len(classified), "eligible_count": len(eligible)}
    complete = [component for component in components.values() if component["complete"]]
    values = {}
    for component in complete:
        for label, keys in component["members"].items():
            values.setdefault(label, []).extend(keys)
    return {"id": "field:" + key, "field_key": key, "name": definition.get("display_name", key),
            "definition": definition, "signature": definition_signature(definition), "members": values,
            "population": "评分完整资料类型中的高相关技术资料", "components": components,
            "eligible_members": [key for item in complete for key in item["eligible_members"]],
            "classified_count": sum(item["classified_count"] for item in complete),
            "eligible_count": sum(item["eligible_count"] for item in complete),
            "unknown_score_count": sum(item["unknown_score_count"] for item in components.values())}


def company_dimensions(pool: dict) -> list[dict]:
    from render_report import standard

    dimensions = []
    for kind, name in (("patent", "专利申请人"), ("paper", "论文机构"), ("news", "新闻涉及公司")):
        eligible = [record for record in pool.values() if record["kind"] == kind]
        members = {}
        classified = set()
        for record in eligible:
            value = standard(record, "company")
            if not value and kind == "paper":
                value = record["info"].get("organizations")
            if isinstance(value, list) and any(isinstance(item, dict) for item in value):
                require(all(isinstance(item, dict) for item in value), "机构字段类型不一致")
                value = [item.get("standard_name") or item.get("name") for item in value]
                value = [item for item in value if item]
            for label in categorical_values(value):
                members.setdefault(label, []).append(record["key"])
                classified.add(record["key"])
        if members:
            definition = {"field_key": "company", "kind": kind, "role": name, "population": "returned_records"}
            dimensions.append({"id": "company:" + kind, "field_key": "company", "name": name,
                               "definition": definition, "signature": digest(definition), "members": members,
                               "population": "本期收录资料", "classified_count": len(classified),
                               "eligible_members": [record["key"] for record in eligible],
                               "eligible_count": len(eligible)})
    return dimensions


def summarize_period(data: dict, target: dict, requested: list[str]) -> dict:
    from render_report import reading_title, safe_url, standard

    pool = record_pool(data)
    counts, high, members, high_members, known_types = {}, {}, {}, {}, {}
    for kind in ("patent", "paper", "news"):
        known = isinstance(data.get("hot_news" if kind == "news" else "tech_items"), (list, dict))
        known_types[kind] = known
        keys = sorted(key for key, record in pool.items() if record["kind"] == kind)
        members[kind] = keys if known else None
        counts[kind] = len(keys) if known else None
        if kind != "news":
            scores_known = known and all(pool[key]["score"] is not None for key in keys)
            high_members[kind] = [key for key in keys if pool[key]["score"] is not None and pool[key]["score"] >= 4] if scores_known else None
            high[kind] = len(high_members[kind]) if scores_known else None
    snapshot = data["basic_info"].get("template_custom", {})
    require(isinstance(snapshot, dict), "历史配置快照类型无效")
    version = data.get("config_version", data["basic_info"].get("config_version"))
    comparison_basis = {"config_version": version} if version is not None else {}
    dimensions = [dimension for dimension in company_dimensions(pool)
                  if counts[dimension["definition"]["kind"]] is not None]
    for definition in dimension_definitions(snapshot, requested):
        dimensions.append(field_dimension(pool, definition, known_types))
    catalogue = {}
    for key, record in pool.items():
        preview = {}
        for field in ("technical_title", "abstract"):
            value = standard(record, field)
            require(value is None or isinstance(value, str), "统计来源的文字字段类型无效：" + field)
            preview[field] = (BeautifulSoup(value, "html.parser").get_text("\n", strip=True)
                              if field == "abstract" else value.strip()) if value else None
        catalogue[key] = {"title": str(reading_title(record)), "link": safe_url(standard(record, "link")),
                          "kind": record["kind"], **preview}
    return {"target": target, "counts": counts, "high": high, "members": members, "high_members": high_members,
            "comparison_basis": comparison_basis,
            "dimensions": dimensions, "records": catalogue}


def current_statistics(config_path: Path, data_path: Path, target_path: Path, requested: list[str]) -> dict:
    from common import period_data
    from render_report import validate_inputs

    config = report_config(load_json(config_path))
    target = load_json(target_path)
    data = period_data(load_json(data_path))
    validate_inputs(config, data, target)
    require(set(requested) <= {item["field_key"] for item in config.get("ai_fields", [])},
            "指定统计维度不属于当前监控配置")
    period = {**summarize_period(data, target, requested), "status": "available", "reason": "", "source": source_ref(data_path)}
    return {"schema_version": STATISTICS_VERSION, "mode": "current", "config": source_ref(config_path), "target": source_ref(target_path),
            "data": source_ref(data_path), "dimension_fields": requested, window_key(target): 1, "periods": [period],
            "checks": {"source_count": 1, "available_periods": 1, "missing_periods": [], "unavailable_periods": [],
                       "raw_sources_unchanged": True, "historical_runs_started": 0}}


def build_statistics(plan_path: Path, requested: list[str]) -> dict:
    plan = load_json(plan_path)
    require(plan.get("schema_version") == 1, "历史清单版本无效")
    current = report_config(load_json(check_source(plan["config"])))
    target = load_json(check_source(plan["target"]))
    require(current["pulse_id"] == target["pulse_id"], "历史配置身份不一致")
    require(set(requested) <= {item["field_key"] for item in current.get("ai_fields", [])},
            "指定历史分类字段不属于当前监控配置")
    key = window_key(target)
    expected_targets = history_targets(target, plan[key])
    require([slot["target"] for slot in plan["periods"]] == expected_targets,
            "历史窗口必须按日期连续排列并包含目标期，起止日期和周期类型须一致")
    periods, responses = [], []
    for slot in plan["periods"]:
        require(slot["status"] != "pending", "历史窗口仍有未查询期次，不能生成统计")
        require(slot["target"]["pulse_id"] == target["pulse_id"], "历史清单中混入其他简报")
        expected_arguments = {"pulse-id": target["pulse_id"], "period_type": target["period_type"], "period": slot["target"]["period"]}
        require(load_json(Path(slot["arguments"])) == expected_arguments, "历史查询参数与计划不一致")
        path = check_source(slot["source"])
        status, data, reason = inspect_response(path, slot["target"])
        require(status == slot["status"], "历史期次状态与原始响应不一致")
        item = {"target": slot["target"], "status": status, "reason": reason, "source": slot["source"]}
        periods.append(item)
        responses.append(data)
    selected = requested or sorted({definition["field_key"] for snapshot in
        [current, *[data["basic_info"].get("template_custom", {}) for data in responses if data is not None]]
        for definition in dimension_definitions(snapshot, [])})
    for item, data in zip(periods, responses):
        if data is not None:
            item.update(summarize_period(data, item["target"], selected))
    require(len(periods) == plan[key] and len({p["target"]["period"] for p in periods}) == plan[key],
            "历史窗口期次数量或唯一性无效")
    return {"schema_version": STATISTICS_VERSION, "mode": "history", "plan": source_ref(plan_path), "config": plan["config"], "target": plan["target"],
            "dimension_fields": requested, key: plan[key], "periods": periods,
            "checks": {"source_count": len(periods), "available_periods": sum(p["status"] == "available" for p in periods),
                       "missing_periods": [p["target"]["period"] for p in periods if p["status"] == "missing"],
                       "unavailable_periods": [p["target"]["period"] for p in periods if p["status"] == "unavailable"],
                       "raw_sources_unchanged": True, "historical_runs_started": 0}}


def validate_statistics(path: Path) -> dict:
    value = load_json(path)
    require(value.get("schema_version") == STATISTICS_VERSION, "历史统计版本无效，请从原始响应重新生成")
    plan = check_source(value["plan"])
    require(value == build_statistics(plan, value["dimension_fields"]), "历史统计与原始响应不一致")
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description="读取已有自然月或自然周响应并生成有来源的历史统计")
    commands = parser.add_subparsers(dest="command", required=True)
    plan = commands.add_parser("plan")
    plan.add_argument("--config", type=Path, required=True)
    plan.add_argument("--target", type=Path, required=True)
    plan.add_argument("--output", type=Path, required=True)
    plan.add_argument("--weeks", type=int)
    plan.add_argument("--months", type=int)
    attach = commands.add_parser("attach")
    attach.add_argument("--plan", type=Path, required=True)
    attach.add_argument("--period", required=True)
    attach.add_argument("--response", type=Path, required=True)
    build = commands.add_parser("build")
    build.add_argument("--plan", type=Path, required=True)
    build.add_argument("--output", type=Path, required=True)
    build.add_argument("--dimension-field", action="append", default=[])
    args = parser.parse_args()
    if args.command == "plan":
        result = plan_history(args.config, args.target, args.output, args.weeks, args.months)
        print(json.dumps({"plan": str(args.output.resolve()), "queries": [slot["arguments"] for slot in result["periods"]]}, ensure_ascii=False))
    elif args.command == "attach":
        print(json.dumps(attach_response(args.plan, args.period, args.response), ensure_ascii=False))
    else:
        result = build_statistics(args.plan, args.dimension_field)
        sources = [args.plan, Path(result["config"]["path"]), Path(result["target"]["path"])]
        sources += [Path(item["source"]["path"]) for item in result["periods"]]
        distinct_output(args.output, sources)
        write_json(args.output, result)
        print(json.dumps({"statistics": str(args.output.resolve()), **result["checks"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()

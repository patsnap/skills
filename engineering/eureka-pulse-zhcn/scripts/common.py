from __future__ import annotations

import hashlib
import json
import shutil
from copy import deepcopy
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4


TOOLS = {"generate_mcp_brief_params_from_intent", "create_personal_mcp_brief",
         "list_mcp_briefs", "get_mcp_brief_info", "update_personal_mcp_brief",
         "run_mcp_personal_brief", "run_mcp_week_brief", "run_mcp_month_brief",
         "get_mcp_brief_run_status", "get_mcp_brief_data", "delete_mcp_brief"}
MCP_LANGUAGE = "CN"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def desktop_connection(path: Path, server: str = "eureka-pulse") -> dict:
    connection = load_json(path)["servers"][server]
    require(connection.get("enabled") is True, "目标 MCP 连接尚未启用")
    transport = connection["transport"]
    require(transport.get("kind") == "streamable_http", "请检查实际提供 HTTP 传输的 MCP 连接")
    headers = transport.get("headers", {})
    require(isinstance(headers, dict), "MCP 连接 headers 必须为对象")
    values = [value for name, value in headers.items() if name.lower() == "x-site-lang"]
    require(values == [MCP_LANGUAGE], "Desktop MCP 连接必须配置唯一的 X-Site-Lang: CN，并重新加载连接")
    require(all(name.lower() != "x-language" for name in headers), "Desktop MCP 连接包含不适用的语言 Header")
    return {"server": server, "config": str(path.resolve()), "site_language": MCP_LANGUAGE,
            "verification": "saved_connection", "wire_verified": False, "checked_at": utc_now()}


def write_json(path: Path, value: Any) -> Path:
    path = path.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def source_ref(path: Path) -> dict:
    path = path.resolve()
    reference = {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    receipt = path.with_name("response.ref.json")
    if path.name == "response.json" and receipt.is_file():
        require(load_json(receipt) == reference, f"原始响应校验失败：{path}")
    return reference


def check_source(reference: dict) -> Path:
    path = Path(reference["path"])
    require(source_ref(path) == reference, f"输入文件已变化：{path}")
    return path


def distinct_output(path: Path, sources: list[Path]) -> None:
    path = path.resolve()
    require(all(path != source.resolve() and (not path.exists() or not path.samefile(source))
                for source in sources), "输出路径不能覆盖输入文件")


def prepare_call(workspace: Path, tool: str, arguments: Path) -> dict:
    validate_call(tool, load_json(arguments))
    require(workspace.is_dir(), "执行目录不存在")
    call_dir = workspace.resolve() / "calls" / uuid4().hex
    call_dir.mkdir(parents=True)
    shutil.copyfile(arguments, call_dir / "arguments.json")
    write_json(call_dir / "request.json", {"tool": tool, "created_at": utc_now(), "status": "submitting"})
    event(workspace, tool, "submitting", {"call_dir": str(call_dir)})
    return {"call_dir": str(call_dir), "arguments": str(call_dir / "arguments.json"),
            "response": str(call_dir / "response.json")}


def finish_call(workspace: Path, call_dir: Path) -> dict:
    request = load_json(call_dir / "request.json")
    path = call_dir / "response.json"
    reference = source_ref(path)
    write_json(call_dir / "response.ref.json", reference)
    event(workspace, request["tool"], "response", {"call_dir": str(call_dir), "source": reference})
    unwrap(load_json(path), allow_empty=request["tool"] == "get_mcp_brief_data")
    result = {"status": "response_saved", "call_dir": str(call_dir), "response": str(path.resolve()),
              "source": reference}
    write_json(call_dir / "result.json", result)
    return result


def report_assets() -> Path:
    assets = Path(__file__).resolve().parent.parent / "assets"
    for name in ["report-base.css", "report.css", "report.html", "report.js", "record-filter.js"]:
        require((assets / name).is_file(), f"报告缺少内置资源：{name}")
    return assets


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def require(condition: Any, message: str) -> None:
    if not condition:
        raise ValueError(message)


def unwrap(value: Any, allow_empty: bool = False) -> Any:
    require(isinstance(value, dict), "响应必须为 JSON 对象")
    if value.get("isError"):
        messages = [item.get("text", "") for item in value.get("content", []) if item.get("type") == "text"]
        raise ValueError("MCP 返回错误：" + "\n".join(messages)[:2000])
    require(value.get("ok") is not False and value.get("success") is not False,
            "调用失败，请检查原始响应")
    if "payload" in value and isinstance(value["payload"], dict):
        return unwrap(value["payload"], allow_empty)
    if value.get("structuredContent") is not None:
        return unwrap(value["structuredContent"], allow_empty)
    if "content" in value and isinstance(value["content"], list):
        texts = [x["text"] for x in value["content"] if x.get("type") == "text"]
        require(len(texts) == 1, "MCP 必须返回唯一 JSON 文字对象或 structuredContent")
        return unwrap(json.loads(texts[0]), allow_empty)
    if (allow_empty and value.get("error_code") == 90112044 and
            isinstance(value.get("data"), dict) and value["data"].get("error_code") == "Data not existing"):
        return None
    if value.get("status") is False or value.get("error_code", 0) != 0:
        details = {key: value[key] for key in ["status", "error_code", "message", "error", "msg", "error_msg"] if key in value}
        if isinstance(value.get("data"), dict):
            for key in ["tracking_id", "error_message", "originating_service"]:
                if key in value["data"]:
                    details[key] = value["data"][key]
            if "error_code" in value["data"]:
                details["service_error_code"] = value["data"]["error_code"]
        raise ValueError("业务请求失败：" + json.dumps(details, ensure_ascii=False)[:2000])
    if "data" in value and ("status" in value or "error_code" in value):
        if allow_empty and value["data"] is None:
            return None
        require(isinstance(value["data"], (dict, list)), "业务数据缺失或类型无效")
        return value["data"]
    return value


def validate_call(tool: str, parameters: dict) -> None:
    require(tool in TOOLS, "该 Tool 不在个人情报监控调用范围内")
    require(isinstance(parameters, dict), "参数必须为完整 JSON 对象")
    require(parameters.get("pulse_type", "PERSONAL_MCP") == "PERSONAL_MCP", "pulse_type 必须为 PERSONAL_MCP")
    if tool in {"create_personal_mcp_brief", "update_personal_mcp_brief"}:
        require(parameters.get("period_type", "week") == "week", "监控计划的 period_type 必须为 week")
    if tool in {"get_mcp_brief_info", "get_mcp_brief_data", "run_mcp_personal_brief",
                "run_mcp_week_brief", "run_mcp_month_brief", "delete_mcp_brief"}:
        require(isinstance(parameters.get("pulse-id"), str) and bool(parameters["pulse-id"].strip()),
                "该 Tool 必须提供 pulse-id")
    if tool == "get_mcp_brief_run_status":
        require(isinstance(parameters.get("run-id"), str) and bool(parameters["run-id"].strip()),
                "状态查询必须提供真实 run-id")
    if tool in {"get_mcp_brief_data", "run_mcp_personal_brief", "run_mcp_week_brief", "run_mcp_month_brief"}:
        if tool in {"get_mcp_brief_data", "run_mcp_personal_brief"}:
            period_type = parameters.get("period_type")
            require(period_type in {"week", "month"}, "该 Tool 必须显式提供 period_type=week 或 month")
        else:
            require("period_type" not in parameters, "周期专用运行 Tool 仅提交 pulse-id 和 period")
            period_type = "month" if tool == "run_mcp_month_brief" else "week"
        period = parameters.get("period")
        require(isinstance(period, str) and len(period) == 6 and period.isdigit(), "period 必须为六位数字字符串")
        require(1 <= int(period[:4]) <= 9999, "周期年份必须有效")
        limit = 12 if period_type == "month" else 53
        require(1 <= int(period[4:]) <= limit,
                "月份必须在 01 至 12 之间" if period_type == "month" else "周次必须在 01 至 53 之间")
    if tool == "create_personal_mcp_brief":
        validate_creation(parameters)


def validate_creation(parameters: dict) -> None:
    from focus import definitions
    detail = parameters.get("detail_module", {})
    require(detail.get("visible") is True and detail.get("mode") in {"merged", "split"},
            "监控配置必须开启技术明细，显示高相关资料")
    criteria = definitions(parameters.get("typical_filters"))
    scope = parameters.get("data_scope")
    require(isinstance(scope, list) and bool(scope), "创建参数缺少资料范围")
    for criterion in criteria:
        require(set(criterion["data_scope"]) <= set(scope), "重点规则超出本次资料范围")
        resolve_ai_fields(parameters, criterion)


def ai_field_index(config: dict) -> dict[str, dict]:
    definitions = config.get("ai_fields", [])
    require(isinstance(definitions, list), "全局 ai_fields 必须为字段定义数组")
    index = {}
    for position, definition in enumerate(definitions):
        location = f"ai_fields[{position}]"
        require(isinstance(definition, dict), f"{location} 必须为字段定义对象")
        key = definition.get("field_key")
        require(isinstance(key, str) and bool(key.strip()), f"{location} 缺少有效 field_key")
        require(key not in index, f"全局 ai_fields 存在重复 field_key：{key}")
        index[key] = definition
    return index


def resolve_ai_fields(config: dict, module: dict) -> list[dict]:
    index = ai_field_index(config)
    location = f"重点规则 {module.get('name', '<未命名>')} 的 ai_fields"
    keys = module.get("ai_fields", [])
    require(isinstance(keys, list), f"{location} 必须为字段名数组")
    seen, definitions = set(), []
    for position, key in enumerate(keys):
        require(isinstance(key, str) and bool(key.strip()), f"{location}[{position}] 必须为非空字段名")
        require(key not in seen, f"{location} 重复引用字段：{key}")
        require(key in index, f"{location} 引用了全局 ai_fields 中不存在的字段：{key}")
        seen.add(key)
        definitions.append(index[key])
    return definitions


def report_config(value: dict) -> dict:
    body = unwrap(value)
    require(isinstance(body, dict), "配置响应必须包含对象")
    template = body.get("template_custom")
    config = {**deepcopy(template or {}), **deepcopy(body)}
    config.pop("template_custom", None)
    require(isinstance(config.get("pulse_id"), str) and bool(config["pulse_id"].strip()),
            "完整配置缺少 pulse_id，请读取 get_mcp_brief_info 原始响应")
    require(isinstance(config.get("detail_module"), dict) and isinstance(config.get("card_fields"), dict),
            "配置响应缺少完整显示配置，请读取 get_mcp_brief_info")
    return config


def period_data(value: dict) -> dict:
    body = unwrap(value)
    require(isinstance(body, dict), "周期响应必须包含对象")
    if "run_id" in body and "sub_tasks" in body:
        require(body.get("status") == "FINISHED", "原始任务响应尚未完成")
        body = body.get("data")
        require(isinstance(body, dict), "已完成任务缺少完整周期内容")
    require("basic_info" in body, "响应缺少周期 basic_info，请取得完整目标期结果")
    return body


def filter_operator(condition: dict) -> str:
    operator = condition.get("operator")
    if operator is None:
        require("filter_key" in condition and "value" in condition, "成员过滤必须提供 filter_key 和 value")
        return "in"
    return operator


def display_config(value: Any) -> Any:
    if isinstance(value, list):
        return [display_config(item) for item in value]
    if isinstance(value, dict):
        result = {key: display_config(item) for key, item in value.items()}
        if "filter_key" in result and "value" in result:
            result["operator"] = filter_operator(result)
        return result
    return value


def configure(value: dict, scheduled_run_enabled: bool, focus: dict | None = None) -> dict:
    from focus import definitions
    parameters = deepcopy(unwrap(value))
    scope = parameters.get("data_scope")
    require(isinstance(scope, list) and bool(scope) and all(isinstance(item, str) for item in scope),
            "参数生成工具尚未返回有效默认资料范围")
    parameters.update({"pulse_type": "PERSONAL_MCP", "period_type": "week",
                       "scheduled_run_enabled": scheduled_run_enabled})
    detail = parameters.setdefault("detail_module", {})
    require(isinstance(detail, dict), "detail_module 必须为对象")
    detail["visible"] = True
    if detail.get("mode") not in {"merged", "split"} or detail.get("mode") == "split" and not detail.get("sub_modules"):
        detail["mode"] = "merged"
    if focus is not None:
        require(isinstance(focus.get("monitoring_objective"), str) and bool(focus["monitoring_objective"].strip()),
                "重点配置缺少本次监控目标")
        parameters["typical_filters"] = deepcopy(definitions(focus))
    else:
        definitions(parameters.get("typical_filters"))
    validate_call("create_personal_mcp_brief", parameters)
    return parameters


def parse_date(value: str) -> date:
    require(isinstance(value, str), "日期必须为字符串")
    return datetime.strptime(value, "%Y%m%d").date() if len(value) == 8 else date.fromisoformat(value[:10])


def week_anchor(year: int, rule: str) -> date:
    first = date(year, 1, 1)
    offset = (first.weekday() + 1) % 7
    return first - timedelta(days=offset) if rule == "jan1" else first + timedelta(days=(7 - offset) % 7)


def encode_week(start: date, rule: str) -> str:
    year = start.year
    if rule == "jan1" and start >= week_anchor(year + 1, rule):
        year += 1
    require(start >= week_anchor(year, rule), "该周属于上一年度，请明确周期编码")
    return f"{year}{(start - week_anchor(year, rule)).days // 7 + 1:02d}"


def make_target(pulse_id: str, period_type: str, today: date, period: str | None, rule: str) -> dict:
    require(bool(pulse_id), "必须提供真实 pulse_id")
    require(period_type in {"week", "month"}, "报告周期必须为 week 或 month")
    require(rule in {"jan1", "first-sunday"}, "周编码规则无效")
    if period is not None:
        require(len(period) == 6 and period.isdigit(), "period 必须为六位数字字符串")
    if period_type == "month":
        month = date(int(period[:4]), int(period[4:]), 1) if period else today.replace(day=1) - timedelta(days=1)
        start = month.replace(day=1)
        next_month = (start.replace(day=28) + timedelta(days=4)).replace(day=1)
        end = next_month - timedelta(days=1)
        period = start.strftime("%Y%m")
    else:
        if period:
            number = int(period[4:])
            require(1 <= number <= 53, "周次必须在 01 至 53 之间")
            start = week_anchor(int(period[:4]), rule) + timedelta(weeks=number - 1)
            require(encode_week(start, rule) == period, "该年度不存在此周编码")
        else:
            current_sunday = today - timedelta(days=(today.weekday() + 1) % 7)
            start = current_sunday - timedelta(days=7)
            period = encode_week(start, rule)
        end = start + timedelta(days=6)
    require(end < today, "目标必须为已经结束的完整周期")
    return {"pulse_id": pulse_id, "period_type": period_type, "period": period,
            "start_date": start.isoformat(), "end_date": end.isoformat(), "week_rule": rule,
            "reference_date": today.isoformat()}


def event(workspace: Path, step: str, operation: str, result: Any) -> None:
    workspace = workspace.resolve()
    require(workspace.is_dir(), "执行目录不存在")
    value = {"time": utc_now(), "workspace": str(workspace), "step": step,
             "operation": operation, "result": result}
    with (workspace / "events.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(value, ensure_ascii=False) + "\n")

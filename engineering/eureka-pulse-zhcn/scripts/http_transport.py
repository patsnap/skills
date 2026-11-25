from __future__ import annotations

import json
import os
import tomllib
from pathlib import Path

import httpx2 as httpx

from common import MCP_LANGUAGE, load_json, require, utc_now


DETAIL_TOOLS = {"get_mcp_brief_info", "get_mcp_brief_data"}
MAX_SSE_EVENT_SIZE = 64 * 1024 * 1024


def load_connection(args) -> dict:
    desktop_path = getattr(args, "desktop_config", None)
    if desktop_path:
        entry = load_json(desktop_path)["servers"][args.server]
        require(entry.get("enabled") is True, "Desktop MCP 连接尚未启用")
        transport = entry["transport"]
        require(transport.get("kind") == "streamable_http", "Desktop 详情读取需要 HTTP 连接")
        connection = {"url": transport["url"], "http_headers": transport.get("headers", {})}
        if args.connection:
            supplied = load_json(args.connection)
            require(supplied.get("url") == connection["url"], "认证连接地址与 Desktop 当前服务不一致")
            connection.update(supplied)
        elif transport.get("bearer_token"):
            connection["bearer_token"] = transport["bearer_token"]
        else:
            require(not transport.get("credential_provider"),
                    "Desktop 使用宿主管理的认证，请提供同一服务的 --connection HTTP 认证参数；不能通过宿主原生调用省略 Header 校验")
        return connection
    if args.codex_config:
        return tomllib.loads(args.codex_config.read_text(encoding="utf-8"))["mcp_servers"][args.server]
    return load_json(args.connection)


def request_headers(connection: dict) -> httpx.Headers:
    headers = httpx.Headers(connection.get("http_headers", {}))
    headers.update({key: os.environ[value] for key, value in connection.get("env_http_headers", {}).items()
                    if key.lower() not in {"x-language", "x-site-lang"}})
    bearer = connection.get("bearer_token")
    if connection.get("bearer_token_env_var"):
        bearer = os.environ[connection["bearer_token_env_var"]]
    if bearer:
        headers["Authorization"] = "Bearer " + bearer
    headers.pop("X-Language", None)
    headers["X-Site-Lang"] = MCP_LANGUAGE
    return headers


class HttpLanguageAudit:
    def __init__(self, url: str, path: Path):
        self.origin = httpx.URL(url).copy_with(path="/", query=None, fragment=None)
        self.path = path.resolve()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.sequence = 0

    def record(self, value: dict) -> None:
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({"at": utc_now(), **value}, ensure_ascii=False) + "\n")

    async def before_request(self, request: httpx.Request) -> None:
        require(request.url.copy_with(path="/", query=None, fragment=None) == self.origin,
                "MCP HTTP 请求地址发生跨服务变化")
        request.headers.pop("X-Language", None)
        request.headers["X-Site-Lang"] = MCP_LANGUAGE
        require(request.headers.get_list("X-Site-Lang") == [MCP_LANGUAGE], "HTTP 请求语言 Header 无效")
        self.sequence += 1
        request.extensions["pulse_language_sequence"] = self.sequence
        details = {}
        if request.method == "POST" and request.headers.get("content-type", "").startswith("application/json"):
            body = json.loads(await request.aread())
            details = {"rpc_method": body.get("method")}
            if body.get("method") == "tools/call":
                details["tool"] = body["params"]["name"]
        self.record({"stage": "send", "sequence": self.sequence, "http_method": request.method,
                     "site_language": request.headers["X-Site-Lang"], **details})

    async def after_response(self, response: httpx.Response) -> None:
        self.record({"stage": "response", "sequence": response.request.extensions["pulse_language_sequence"],
                     "status_code": response.status_code})

    def client(self, connection: dict) -> httpx.AsyncClient:
        return httpx.AsyncClient(headers=request_headers(connection), timeout=httpx.Timeout(180, read=600),
                                 event_hooks={"request": [self.before_request], "response": [self.after_response]})


def audit_result(path: Path, tool: str) -> dict:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    sends = [row for row in rows if row["stage"] == "send"]
    responses = {row["sequence"]: row for row in rows if row["stage"] == "response"}
    calls = [row for row in sends if row.get("tool") == tool]
    require(sends and calls and all(row["site_language"] == MCP_LANGUAGE for row in sends),
            "缺少详情请求实际发送前的 Header 检查记录")
    require(all(row["sequence"] in responses for row in calls), "详情请求尚未收到 HTTP 响应")
    return {"path": str(path.resolve()), "site_language": MCP_LANGUAGE,
            "verification": "httpx_request_and_response", "requests_checked": len(sends),
            "detail_requests": len(calls), "detail_status_codes": [responses[row["sequence"]]["status_code"] for row in calls]}

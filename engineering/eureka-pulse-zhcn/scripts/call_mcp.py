from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from uuid import uuid4

from jsonschema import validate
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamable_http_client

from common import digest, event, finish_call, load_json, require, utc_now, validate_call, write_json
from http_transport import MAX_SSE_EVENT_SIZE, HttpLanguageAudit, audit_result, load_connection, request_headers


async def submit(session: ClientSession, args, call_dir: Path, parameters: dict) -> dict:
    await session.initialize()
    catalog = await session.list_tools()
    matches = [tool for tool in catalog.tools if tool.name == args.tool]
    while not matches and catalog.next_cursor:
        catalog = await session.list_tools(params=types.PaginatedRequestParams(cursor=catalog.next_cursor))
        matches = [tool for tool in catalog.tools if tool.name == args.tool]
    require(len(matches) == 1, "目标 Tool 未在指定服务中唯一找到")
    validate(parameters, matches[0].input_schema)
    write_json(call_dir / "input-schema.json", matches[0].input_schema)
    event(args.workspace, args.tool, "submitting", {"call_id": call_dir.name})
    response = await session.send_request(
        types.CallToolRequest(params=types.CallToolRequestParams(name=args.tool, arguments=parameters)),
        types.CallToolResult)
    raw = response.model_dump(mode="json", by_alias=True, exclude_unset=True)
    path = call_dir / "response.json"
    with path.open("x", encoding="utf-8") as stream:
        json.dump(raw, stream, ensure_ascii=False, indent=2)
    result = {**finish_call(args.workspace, call_dir), "call_id": call_dir.name}
    await session.validate_tool_result(args.tool, response)
    return result


async def run(args) -> dict:
    parameters = load_json(args.arguments)
    validate_call(args.tool, parameters)
    require(args.workspace.is_dir(), "请先创建执行目录")
    connection = load_connection(args)
    call_dir = args.workspace.resolve() / "calls" / uuid4().hex
    call_dir.mkdir(parents=True)
    write_json(call_dir / "arguments.json", parameters)
    write_json(call_dir / "request.json", {"server": args.server, "tool": args.tool,
               "arguments_sha256": digest(parameters), "created_at": utc_now(), "status": "prepared"})
    audit_path = call_dir / "http-requests.jsonl"
    # 连接配置只在内存中读取，不写入业务日志。
    if "url" in connection:
        audit = HttpLanguageAudit(connection["url"], audit_path)
        async with audit.client(connection) as client:
            async with streamable_http_client(connection["url"], http_client=client,
                                              max_sse_event_size=MAX_SSE_EVENT_SIZE) as (reader, writer):
                async with ClientSession(reader, writer) as session:
                    result = await submit(session, args, call_dir, parameters)
    else:
        bridge = Path(__file__).with_name("stdio_bridge.py").resolve()
        arguments = connection.get("args", [])
        require(Path(connection["command"]).resolve() == Path(sys.executable).resolve() and
                bool(arguments) and Path(arguments[0]).resolve() == bridge,
                "stdio 详情读取必须使用内置 stdio_bridge.py，并明确提供上游 HTTP 连接")
        server = StdioServerParameters(command=connection["command"], args=connection.get("args", []),
                                       env={**os.environ, **connection.get("env", {}), "PULSE_MCP_HTTP_AUDIT": str(audit_path)})
        async with stdio_client(server) as (reader, writer):
            async with ClientSession(reader, writer) as session:
                result = await submit(session, args, call_dir, parameters)
    result["http_audit"] = audit_result(audit_path, args.tool)
    write_json(call_dir / "result.json", {**result, "status": "response_saved", "finished_at": utc_now()})
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="从完整参数文件直接调用 MCP 并保存响应")
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--connection", type=Path)
    source.add_argument("--codex-config", type=Path, nargs="?", const=Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "config.toml")
    parser.add_argument("--desktop-config", type=Path)
    parser.add_argument("--server", default="eureka-pulse")
    parser.add_argument("--tool", required=True)
    parser.add_argument("--arguments", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    args = parser.parse_args()
    require(args.connection is not None or args.codex_config is not None or args.desktop_config is not None,
            "请提供实际 MCP 连接配置")
    require(not (args.desktop_config and args.codex_config), "Desktop 与 Codex 连接分别使用")
    print(json.dumps(asyncio.run(run(args)), ensure_ascii=False))


if __name__ == "__main__":
    main()

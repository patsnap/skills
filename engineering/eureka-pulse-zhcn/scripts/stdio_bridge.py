from __future__ import annotations

import argparse
import asyncio
import os
from pathlib import Path

from mcp import ClientSession, types
from mcp.client.streamable_http import streamable_http_client
from mcp.server.lowlevel import Server
from mcp.server.stdio import stdio_server

from common import require, validate_call
from http_transport import MAX_SSE_EVENT_SIZE, HttpLanguageAudit, load_connection


async def run(args) -> None:
    connection = load_connection(args)
    require("url" in connection, "stdio 适配器需要明确的上游 HTTP 连接")
    audit = HttpLanguageAudit(connection["url"], args.audit)
    async with audit.client(connection) as client:
        async with streamable_http_client(connection["url"], http_client=client,
                                          max_sse_event_size=MAX_SSE_EVENT_SIZE) as (reader, writer):
            async with ClientSession(reader, writer) as session:
                await session.initialize()

                async def list_tools(context, parameters):
                    return await session.list_tools(params=parameters)

                async def call_tool(context, parameters):
                    validate_call(parameters.name, parameters.arguments or {})
                    return await session.send_request(
                        types.CallToolRequest(params=types.CallToolRequestParams(
                            name=parameters.name, arguments=parameters.arguments or {})), types.CallToolResult)

                server = Server("eureka-pulse-cn", on_list_tools=list_tools, on_call_tool=call_tool)
                async with stdio_server() as (incoming, outgoing):
                    await server.run(incoming, outgoing, server.create_initialization_options(), raise_exceptions=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="通过固定中文 HTTP 连接转发 stdio MCP 请求")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--connection", type=Path)
    source.add_argument("--codex-config", type=Path)
    parser.add_argument("--server", default="eureka-pulse")
    parser.add_argument("--audit", type=Path, default=Path(os.environ["PULSE_MCP_HTTP_AUDIT"]) if "PULSE_MCP_HTTP_AUDIT" in os.environ else None)
    args = parser.parse_args()
    require(args.audit is not None, "stdio 适配器必须提供 --audit 或 PULSE_MCP_HTTP_AUDIT")
    asyncio.run(run(args))


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

from common import desktop_connection, finish_call, load_json, prepare_call, write_json
from http_transport import DETAIL_TOOLS


def main() -> None:
    parser = argparse.ArgumentParser(description="在 Eureka Desktop 的 Python 工具中从文件调用 MCP")
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--tool", required=True)
    parser.add_argument("--arguments", type=Path, required=True)
    parser.add_argument("--desktop-config", type=Path, required=True)
    parser.add_argument("--connection", type=Path)
    args = parser.parse_args()
    if args.tool in DETAIL_TOOLS:
        from call_mcp import run
        args.server = "eureka-pulse"
        args.codex_config = None
        print(json.dumps(asyncio.run(run(args)), ensure_ascii=False))
        return
    connection = desktop_connection(args.desktop_config)
    import eureka_tools

    call = prepare_call(args.workspace, args.tool, args.arguments)
    write_json(Path(call["call_dir"]) / "connection.json", connection)
    result = eureka_tools.call("eureka-pulse", args.tool, load_json(Path(call["arguments"])))
    with Path(call["response"]).open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
    print(json.dumps(finish_call(args.workspace, Path(call["call_dir"])), ensure_ascii=False))


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

from common import (check_source, configure, desktop_connection, distinct_output, event, finish_call, load_json,
                    make_target, period_data, prepare_call, report_assets, report_config, require, source_ref, unwrap, utc_now, write_json)


def main() -> None:
    parser = argparse.ArgumentParser(description="情报监控的目录、周期和执行记录")
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init")
    init.add_argument("--root", type=Path, required=True)
    period = commands.add_parser("period")
    period.add_argument("--pulse-id", required=True)
    period.add_argument("--period-type", choices=["week", "month"], default="month")
    period.add_argument("--period")
    period.add_argument("--today", type=date.fromisoformat, required=True)
    period.add_argument("--week-rule", choices=["jan1", "first-sunday"], default="first-sunday")
    period.add_argument("--output", type=Path, required=True)
    extract = commands.add_parser("extract")
    extract.add_argument("--input", type=Path, required=True)
    extract.add_argument("--output", type=Path, required=True)
    extract.add_argument("--kind", choices=["data", "config"], default="data")
    report = commands.add_parser("prepare-report")
    report.add_argument("--config", type=Path, required=True)
    report.add_argument("--data", type=Path)
    report.add_argument("--target", type=Path, required=True)
    report.add_argument("--output", type=Path, required=True)
    report.add_argument("--focus", type=Path)
    report.add_argument("--review", type=Path)
    report.add_argument("--charts", type=Path)
    commands.add_parser("check-report-assets")
    connection = commands.add_parser("check-connection")
    connection.add_argument("--desktop-config", type=Path, required=True)
    connection.add_argument("--server", default="eureka-pulse")
    configuration = commands.add_parser("configure")
    configuration.add_argument("--input", type=Path, required=True)
    configuration.add_argument("--output", type=Path, required=True)
    configuration.add_argument("--scheduled-run-enabled", choices=["true", "false"], default="true")
    configuration.add_argument("--focus", type=Path)
    state = commands.add_parser("state")
    state.add_argument("--workspace", type=Path, required=True)
    state.add_argument("--step", required=True)
    state.add_argument("--status", choices=["running", "waiting", "failed", "complete", "cancelled"], required=True)
    state.add_argument("--pulse-id")
    state.add_argument("--run-id")
    state.add_argument("--continue-condition")
    state.add_argument("--files", type=Path)
    log = commands.add_parser("event")
    log.add_argument("--workspace", type=Path, required=True)
    log.add_argument("--step", required=True)
    log.add_argument("--operation", required=True)
    log.add_argument("--result", type=Path, required=True)
    inspect = commands.add_parser("inspect")
    inspect.add_argument("--workspace", type=Path, required=True)
    clean = commands.add_parser("clean-logs")
    clean.add_argument("--root", type=Path, required=True)
    clean.add_argument("--days", type=int, default=30)
    transfer = commands.add_parser("read-chunk")
    transfer.add_argument("--input", type=Path, required=True)
    transfer.add_argument("--offset", type=int, default=0)
    prepare = commands.add_parser("prepare-call")
    prepare.add_argument("--workspace", type=Path, required=True)
    prepare.add_argument("--tool", required=True)
    prepare.add_argument("--arguments", type=Path, required=True)
    finish = commands.add_parser("finish-call")
    finish.add_argument("--workspace", type=Path, required=True)
    finish.add_argument("--call-dir", type=Path, required=True)
    args = parser.parse_args()
    result = {}
    if args.command == "init":
        workspace = args.root.resolve() / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid4().hex[:12])
        workspace.mkdir(parents=True)
        (workspace / "calls").mkdir()
        (workspace / "fetch").mkdir()
        write_json(workspace / "state.json", {"step": "start", "status": "running", "updated_at": utc_now()})
        event(workspace, "start", "init", {"workspace": str(workspace)})
        result = {"workspace": str(workspace)}
    elif args.command == "period":
        result = make_target(args.pulse_id, args.period_type, args.today, args.period, args.week_rule)
        write_json(args.output, result)
    elif args.command == "extract":
        distinct_output(args.output, [args.input])
        value = report_config(load_json(args.input)) if args.kind == "config" else unwrap(load_json(args.input))
        result = {"output": str(write_json(args.output, value)), "source": source_ref(args.input)}
    elif args.command == "prepare-report":
        require(args.data is not None or args.charts is not None, "报告需要目标期资料或历史图表")
        sources = [args.config, args.target] + ([args.data] if args.data else [])
        require(bool(args.focus) == bool(args.review), "本期重点审核需要同时提供 focus 与 review")
        if args.focus:
            sources += [args.focus, args.review]
        distinct_output(args.output, sources)
        config = report_config(load_json(args.config))
        target = load_json(args.target)
        if args.data:
            from render_report import validate_inputs
            validate_inputs(config, period_data(load_json(args.data)), target)
        manifest = {"config": source_ref(args.config), "target": source_ref(args.target)}
        if args.data:
            manifest["data"] = source_ref(args.data)
        if args.charts:
            from charts import bundle_sources, load_charts
            bundle = load_charts(args.charts, manifest["config"], manifest["target"])
            sources += [args.charts] + [Path(item["path"]) for item in bundle_sources(bundle)]
            distinct_output(args.output, sources)
            manifest["charts"] = source_ref(args.charts)
            if not args.data:
                require(bundle["model"]["periods"][-1]["status"] != "available", "目标期已有资料，请使用完整本期报告入口")
        if args.focus:
            manifest.update({"focus": source_ref(args.focus), "review": source_ref(args.review)})
        result = {"inputs": str(write_json(args.output, manifest)), "pulse_id": config["pulse_id"],
                  "period": target["period"], "sources": manifest}
    elif args.command == "configure":
        distinct_output(args.output, [args.input] + ([args.focus] if args.focus else []))
        parameters = configure(load_json(args.input), args.scheduled_run_enabled == "true", load_json(args.focus) if args.focus else None)
        result = {"output": str(write_json(args.output, parameters)), "pulse_type": parameters["pulse_type"],
                  "period_type": parameters["period_type"], "data_scope": parameters["data_scope"],
                  "scheduled_run_enabled": parameters["scheduled_run_enabled"]}
    elif args.command == "check-report-assets":
        assets = report_assets()
        result = {"assets": str(assets), "base_styles": source_ref(assets / "report-base.css")}
    elif args.command == "check-connection":
        result = desktop_connection(args.desktop_config, args.server)
    elif args.command == "state":
        current = load_json(args.workspace / "state.json")
        current.update({"step": args.step, "status": args.status, "updated_at": utc_now()})
        for key in ["pulse_id", "run_id", "continue_condition"]:
            value = getattr(args, key)
            if value is not None:
                current[key] = value
        if args.files:
            current["files"] = load_json(args.files)
        write_json(args.workspace / "state.json", current)
        event(args.workspace, args.step, "state", current)
        result = current
    elif args.command == "event":
        event(args.workspace, args.step, args.operation, load_json(args.result))
        result = {"logged": True}
    elif args.command == "inspect":
        result = {"state": load_json(args.workspace / "state.json"),
                  "events": str((args.workspace / "events.jsonl").resolve())}
    elif args.command == "read-chunk":
        require(args.offset >= 0, "读取位置无效")
        value = args.input.read_text(encoding="utf-8")
        end = min(args.offset + 4000, len(value))
        result = {"text": value[args.offset:end], "next_offset": end, "complete": end == len(value)}
    elif args.command == "prepare-call":
        result = prepare_call(args.workspace, args.tool, args.arguments)
    elif args.command == "finish-call":
        result = finish_call(args.workspace, args.call_dir)
    elif args.command == "clean-logs":
        require(args.days >= 1, "日志保留天数必须大于零")
        cutoff = datetime.now(timezone.utc) - timedelta(days=args.days)
        removed = []
        for path in args.root.resolve().glob("*/state.json"):
            value = load_json(path)
            if value["status"] in {"complete", "cancelled"} and datetime.fromisoformat(value["updated_at"]) < cutoff:
                log_path = path.parent / "events.jsonl"
                if log_path.exists():
                    log_path.unlink()
                    removed.append(str(log_path))
        result = {"removed_logs": removed}
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Validate reviewed JSON and generate an escaped HTML mobility-signal briefing.

Usage:
    python generate_report.py --data reviewed-data.json --output report.html

The legacy ``MONITOR_DATA_JSON`` environment variable remains supported for
compatibility, but explicit ``--data`` and ``--output`` arguments are preferred.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from run_monitor import generate_html_report, validate_report_data


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, help="Reviewed UTF-8 JSON input")
    parser.add_argument("--output", type=Path, required=True, help="Output .html path")
    parser.add_argument("--force", action="store_true", help="Replace an existing report")
    return parser.parse_args(argv)


def load_data(path: Path) -> dict:
    if not path.is_file():
        raise ValueError(f"Input file does not exist: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read valid JSON from {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("Top-level JSON value must be an object")
    return data


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        legacy = os.environ.get("MONITOR_DATA_JSON")
        data_path = args.data or (Path(legacy) if legacy else None)
        if data_path is None:
            raise ValueError("Provide --data (preferred) or MONITOR_DATA_JSON")
        if args.output.suffix.lower() not in {".html", ".htm"}:
            raise ValueError("Output path must use .html or .htm")
        if args.output.exists() and not args.force:
            raise ValueError(f"Refusing to replace existing output without --force: {args.output}")

        data = load_data(data_path)
        errors = validate_report_data(data)
        if errors:
            raise ValueError("Input validation failed:\n- " + "\n- ".join(errors))
        generate_html_report(data, args.output)
        print(f"Generated reviewed mobility-signal briefing: {args.output}")
        return 0
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

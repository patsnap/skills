#!/usr/bin/env python3
"""Compatibility wrapper: report step now lives in doe_pipeline.py."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from doe_pipeline import main as pipeline_main  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate DOE markdown report")
    parser.add_argument("--context-json")
    parser.add_argument("--evidence-catalog", required=True)
    parser.add_argument("--factors-json", required=True)
    parser.add_argument("--design-json", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    cmd = [
        "report",
        "--evidence-catalog",
        args.evidence_catalog,
        "--factors-json",
        args.factors_json,
        "--design-json",
        args.design_json,
        "--output",
        args.output,
    ]
    if args.context_json:
        cmd.extend(["--context-json", args.context_json])

    return pipeline_main(cmd)


if __name__ == "__main__":
    raise SystemExit(main())

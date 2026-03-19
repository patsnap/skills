#!/usr/bin/env python3
"""Compatibility wrapper: design step now lives in doe_pipeline.py."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from doe_pipeline import main as pipeline_main  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate DOE design and run sheet")
    parser.add_argument("--factors-json", required=True)
    parser.add_argument("--design-type", default="auto", choices=["auto", "pb", "ffd", "bbd", "ccd"])
    parser.add_argument("--phase", default="screening", choices=["screening", "optimization"])
    parser.add_argument("--resource-budget", type=int, default=0)
    parser.add_argument("--replicates", type=int, default=1)
    parser.add_argument("--center-points", type=int, default=3)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--responses", default="yield,titer")
    parser.add_argument("--max-factors", type=int, default=6)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-csv", required=True)
    args = parser.parse_args()

    return pipeline_main(
        [
            "design",
            "--factors-json",
            args.factors_json,
            "--design-type",
            args.design_type,
            "--phase",
            args.phase,
            "--resource-budget",
            str(args.resource_budget),
            "--replicates",
            str(args.replicates),
            "--center-points",
            str(args.center_points),
            "--seed",
            str(args.seed),
            "--responses",
            args.responses,
            "--max-factors",
            str(args.max_factors),
            "--output-json",
            args.output_json,
            "--output-csv",
            args.output_csv,
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())

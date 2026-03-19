#!/usr/bin/env python3
"""Compatibility wrapper: factor step now lives in doe_pipeline.py."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from doe_pipeline import main as pipeline_main  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract factor hypotheses")
    parser.add_argument("--evidence-catalog", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--max-factors", type=int, default=8)
    args = parser.parse_args()

    return pipeline_main(
        [
            "factor",
            "--evidence-catalog",
            args.evidence_catalog,
            "--max-factors",
            str(args.max_factors),
            "--output",
            args.output,
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Compatibility wrapper: evidence step now lives in doe_pipeline.py."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from doe_pipeline import main as pipeline_main  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Build evidence catalog")
    parser.add_argument("--search-input", required=True)
    parser.add_argument("--fetch-manifest", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--top-k", type=int, default=12)
    args = parser.parse_args()

    return pipeline_main(
        [
            "evidence",
            "--search-input",
            args.search_input,
            "--fetch-manifest",
            args.fetch_manifest,
            "--top-k",
            str(args.top_k),
            "--output",
            args.output,
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())

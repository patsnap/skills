#!/usr/bin/env python3
"""Run all restartable high-value patent screening stages in order."""

from __future__ import annotations

import argparse
import os
import pathlib
import subprocess
import sys
import uuid


SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
STAGES = [
    ("hv_1_fetch.py", "Retrieve and deduplicate P002 candidates"),
    ("hv_2_numeric.py", "Retrieve P014/P015 numeric evidence"),
    ("hv_3_legal.py", "Retrieve P034/P027/P028/P029 event evidence"),
    ("hv_4_score.py", "Score, rank, and select under the 30/30/20/20 model"),
    ("hv_5_display.py", "Retrieve selected-record P021/P025/P041 evidence"),
    ("hv_6_assemble.py", "Assemble final records and full JSON trace"),
    ("hv_7_html_a.py", "Render the required safe static HTML report"),
]
WORD_STAGE = ("hv_8_word.py", "Render the optional DOCX report")


def run_stage(script: str, description: str, *, working_directory: pathlib.Path, environment: dict[str, str], extra: list[str] | None = None) -> None:
    command = [sys.executable, str(SCRIPT_DIR / script)] + list(extra or [])
    print(f"\n===== {script}: {description} =====", flush=True)
    subprocess.run(command, cwd=working_directory, env=environment, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the complete high-value patent portfolio screening pipeline.")
    parser.add_argument("--output-dir", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--word", action="store_true", help="Also generate the optional DOCX report")
    parser.add_argument("--images", action="store_true", help="With --word, download safe P021 images subject to type/size limits")
    parser.add_argument("--selection-ratio", type=float, default=0.10)
    args = parser.parse_args()
    if not 0.10 <= args.selection_ratio <= 0.15:
        parser.error("--selection-ratio must be between 0.10 and 0.15")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    environment = dict(os.environ)
    environment["HVP_RUN_ID"] = environment.get("HVP_RUN_ID") or str(uuid.uuid4())
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    for script, description in STAGES:
        extra = ["--selection-ratio", str(args.selection_ratio)] if script == "hv_4_score.py" else []
        run_stage(script, description, working_directory=args.output_dir, environment=environment, extra=extra)
    if args.word:
        extra = ["--images"] if args.images else []
        run_stage(WORD_STAGE[0], WORD_STAGE[1], working_directory=args.output_dir, environment=environment, extra=extra)
    artifacts = [
        "high_value_patent_portfolio_screening.html",
        "high_value_patent_screening_data.json",
        "final_records.json",
    ]
    if args.word:
        artifacts.append("high_value_patent_portfolio_screening.docx")
    print("\nDONE. Review these artifacts together:")
    for artifact in artifacts:
        print(f"- {args.output_dir / artifact}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

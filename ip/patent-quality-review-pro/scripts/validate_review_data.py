#!/usr/bin/env python3
"""Validate review evidence before using it for scores, conclusions, or Word."""

import argparse
import json
import os
import sys

from review_validation import (
    clear_validation_errors,
    validate_evidence_contract,
    write_validation_errors,
    write_validation_pass,
)


def main():
    parser = argparse.ArgumentParser(description="Validate patent-quality-review-pro evidence contract")
    parser.add_argument("--data", required=True, help="Review/evidence JSON file path")
    parser.add_argument(
        "--stage",
        default="pre_use",
        choices=["pre_use", "pre_word"],
        help="Validation stage label written to review_validation_passed.json",
    )
    parser.add_argument(
        "--output",
        help="Optional output path used only to choose where validation status files are written",
    )
    args = parser.parse_args()

    data_path = os.path.abspath(args.data)
    if not os.path.exists(data_path):
        print(f"VALIDATION_ERROR: data file not found: {data_path}")
        return 2

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    output_path = args.output or os.path.join(os.path.dirname(data_path), "_validation_placeholder.docx")
    errors, session_root, runtime_skills = validate_evidence_contract(
        data,
        data_file_path=data_path,
        output_path=output_path,
    )

    if errors:
        error_path = write_validation_errors(errors, output_path)
        print("VALIDATION_ERROR: evidence chain incomplete; data use blocked.")
        print(f"Validation details: {error_path}")
        for error in errors:
            print(f"- {error}")
        return 2

    clear_validation_errors(output_path)
    pass_path = write_validation_pass(data_path, output_path, args.stage, session_root, runtime_skills)
    print(f"OK: evidence chain validated for {args.stage}")
    print(f"MANIFEST:{pass_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

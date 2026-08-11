#!/usr/bin/env bash
# Run the reviewed patent-based R&D briefing workflow.

set -euo pipefail

usage() {
  echo "Usage: $0 <input.xlsx> <topic-key> <start-date> <end-date> [output-directory]"
  echo
  echo "Dates must use YYYY-MM-DD."
  echo "Example:"
  echo "  $0 ./patents.xlsx BIPV 2026-01-01 2026-03-31 ./output"
}

if [[ $# -lt 4 || $# -gt 5 ]]; then
  usage >&2
  exit 2
fi

INPUT_XLSX=$1
TOPIC_KEY=$2
START_DATE=$3
END_DATE=$4
OUTPUT_DIR=${5:-"$(dirname "$INPUT_XLSX")"}

if [[ ! -f "$INPUT_XLSX" ]]; then
  echo "ERROR: Input workbook does not exist: $INPUT_XLSX" >&2
  exit 1
fi

if [[ ! "$TOPIC_KEY" =~ ^[A-Za-z0-9_-]+$ ]]; then
  echo "ERROR: Topic key may contain only ASCII letters, numbers, hyphens, and underscores." >&2
  exit 1
fi

if [[ ! "$START_DATE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
  echo "ERROR: Start date must use YYYY-MM-DD." >&2
  exit 1
fi

if [[ ! "$END_DATE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
  echo "ERROR: End date must use YYYY-MM-DD." >&2
  exit 1
fi

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
SKILL_DIR=$(dirname "$SCRIPT_DIR")
if [[ "$TOPIC_KEY" == "coffee-machine" ]]; then
  KEYWORDS_CONFIG="$SKILL_DIR/config/$(printf '\345\222\226\345\225\241\346\234\272')_keywords.py"
  CONTENT_CONFIG="$SKILL_DIR/config/$(printf '\345\222\226\345\225\241\346\234\272')_content.py"
else
  KEYWORDS_CONFIG="$SKILL_DIR/config/${TOPIC_KEY}_keywords.py"
  CONTENT_CONFIG="$SKILL_DIR/config/${TOPIC_KEY}_content.py"
fi

if [[ ! -f "$KEYWORDS_CONFIG" ]]; then
  echo "ERROR: Keyword configuration does not exist: $KEYWORDS_CONFIG" >&2
  exit 1
fi

if [[ ! -f "$CONTENT_CONFIG" ]]; then
  echo "ERROR: Content configuration does not exist: $CONTENT_CONFIG" >&2
  exit 1
fi

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN=python
else
  echo "ERROR: Python 3 is required." >&2
  exit 1
fi

if ! "$PYTHON_BIN" -c "import pandas, openpyxl" >/dev/null 2>&1; then
  echo "ERROR: Required packages are missing." >&2
  echo "Review requirements.txt and install dependencies in an approved environment." >&2
  echo "This script does not install software automatically." >&2
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

INPUT_NAME=$(basename "$INPUT_XLSX")
INPUT_STEM=${INPUT_NAME%.*}
DATE_RANGE_ID="${START_DATE}_to_${END_DATE}"
TAGGED_XLSX="$OUTPUT_DIR/${INPUT_STEM}_tagged.xlsx"
OUTPUT_HTML="$OUTPUT_DIR/${TOPIC_KEY}_report_${DATE_RANGE_ID}.html"

if [[ -e "$TAGGED_XLSX" || -e "$OUTPUT_HTML" ]]; then
  echo "ERROR: An output already exists. Move it or run the Python scripts with explicit overwrite review." >&2
  echo "Tagged workbook: $TAGGED_XLSX" >&2
  echo "HTML report: $OUTPUT_HTML" >&2
  exit 1
fi

echo "Patent-Based R&D Briefing"
echo "=========================="
echo "Input workbook: $INPUT_XLSX"
echo "Topic key: $TOPIC_KEY"
echo "Evidence window: $START_DATE to $END_DATE"
echo "Output directory: $OUTPUT_DIR"
echo

echo "[1/3] Adding discovery signals"
"$PYTHON_BIN" -B "$SCRIPT_DIR/tag_relevant.py" \
  "$INPUT_XLSX" \
  "$TAGGED_XLSX" \
  "$TOPIC_KEY"

echo
echo "[2/3] Human review required"
echo "Open the tagged workbook and set Review status, Reviewer, Review date,"
echo "and Discovery disposition for every record used in the briefing."
echo
echo "The report generator will withhold unreviewed candidate records."
echo "Continue only after the workbook review is complete."

if [[ "${PATENT_BRIEFING_NONINTERACTIVE:-0}" != "1" ]]; then
  read -r -p "Type REVIEWED to continue: " confirmation
  if [[ "$confirmation" != "REVIEWED" ]]; then
    echo "Stopped before report generation. Tagged workbook is retained."
    exit 3
  fi
fi

echo
echo "[3/3] Generating the static briefing"
"$PYTHON_BIN" -B "$SCRIPT_DIR/generate_report.py" \
  "$TAGGED_XLSX" \
  "$OUTPUT_HTML" \
  "$TOPIC_KEY" \
  "$START_DATE" \
  "$END_DATE"

echo
echo "Completed"
echo "========="
echo "Tagged workbook: $TAGGED_XLSX"
echo "HTML report: $OUTPUT_HTML"
echo
echo "The report remains a technical-intelligence briefing, not legal advice."
echo "Review evidence coverage, patent-family treatment, legal status, and the"
echo "specialist-review boundary before distribution."

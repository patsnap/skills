#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
SKILL_DIR="$(dirname -- "$SCRIPT_DIR")"
cd "$SKILL_DIR"

if [ "$#" -lt 1 ]; then
  echo "Usage: bash scripts/run.sh <query> [report-title] [limit]" >&2
  exit 2
fi

QUERY="$1"
TITLE="${2:-Patent search report}"
LIMIT="${3:-200}"

case "$LIMIT" in
  ''|*[!0-9]*)
    echo "Error: limit must be a positive integer." >&2
    exit 2
    ;;
esac

if [ "$LIMIT" -lt 1 ]; then
  echo "Error: limit must be at least 1." >&2
  exit 2
fi

PYTHON_BIN="${PYTHON_BIN:-}"
if [ -z "$PYTHON_BIN" ]; then
  PYTHON_BIN="$(command -v python3 || command -v python || true)"
fi
if [ -z "$PYTHON_BIN" ]; then
  echo "Error: Python 3 is required." >&2
  exit 1
fi

if ! "$PYTHON_BIN" -c 'import requests' >/dev/null 2>&1; then
  echo "Error: the requests package is required; install dependencies explicitly before running." >&2
  exit 1
fi

SAFE_NAME="$($PYTHON_BIN -c 'import re,sys; value=sys.argv[1]; value=re.sub(r"[,/\\ ]+", "_", value); value=re.sub(r"[^A-Za-z0-9_.-]", "", value); print((value or "patent_report")[:60])' "$TITLE")"
TIMESTAMP="$(date -u +'%Y%m%dT%H%M%SZ')"
OUTPUT_FILE="reports/${SAFE_NAME}_${TIMESTAMP}.md"
mkdir -p reports

"$PYTHON_BIN" scripts/fetch_competitor_report.py "$QUERY" "$TITLE" "$LIMIT" | tee "$OUTPUT_FILE"

echo "" >&2
echo "[OK] Markdown report saved: $OUTPUT_FILE" >&2

HTML_FILE="${OUTPUT_FILE%.md}.html"
if "$PYTHON_BIN" scripts/render_html.py "$OUTPUT_FILE"; then
  echo "[OK] HTML report saved: $HTML_FILE" >&2
else
  echo "[WARNING] HTML rendering failed; the Markdown report remains available." >&2
  exit 1
fi

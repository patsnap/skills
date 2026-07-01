#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."

if [ -z "$1" ]; then
  echo "用法: bash scripts/run.sh <检索式> [报告标题] [数量]" >&2
  exit 1
fi

QUERY="$1"
TITLE="${2:-专利检索报告}"
LIMIT="${3:-200}"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
SAFE_NAME=$(python3 -c "
import re, sys
s = '${TITLE}'
s = re.sub(r'[，,、/ ]+', '_', s)
s = re.sub(r'[^\w\u4e00-\u9fff\-]', '', s)
print(s[:60])
")
OUTPUT_FILE="reports/${SAFE_NAME}_${TIMESTAMP}.md"
mkdir -p reports

CLEAN_ENV=(env -u PYTHONHOME -u PYTHONPATH -u VIRTUAL_ENV -u CONDA_PREFIX)

if command -v uv &>/dev/null; then
  "${CLEAN_ENV[@]}" uv run --with requests --with python-dotenv python scripts/fetch_competitor_report.py "$QUERY" "$TITLE" "$LIMIT" | tee "$OUTPUT_FILE"
else
  PYTHON=$("${CLEAN_ENV[@]}" sh -c 'command -v python3 || command -v python || echo /opt/homebrew/bin/python3')
  "${CLEAN_ENV[@]}" "$PYTHON" -c "import requests, dotenv, oss2" 2>/dev/null || \
    "${CLEAN_ENV[@]}" "$PYTHON" -m pip install --quiet requests python-dotenv oss2
  "${CLEAN_ENV[@]}" "$PYTHON" scripts/fetch_competitor_report.py "$QUERY" "$TITLE" "$LIMIT" | tee "$OUTPUT_FILE"
fi

echo "" >&2
echo "[报告已保存] $OUTPUT_FILE" >&2

# 生成 HTML
HTML_FILE="${OUTPUT_FILE%.md}.html"
PYTHON_BIN=$(command -v python3 || command -v python || echo /opt/homebrew/bin/python3)
"$PYTHON_BIN" scripts/render_html.py "$OUTPUT_FILE" >/dev/null 2>&1 && \
  echo "[HTML已生成] $HTML_FILE" >&2 || \
  echo "[警告] HTML 生成失败" >&2

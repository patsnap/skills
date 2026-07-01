#!/usr/bin/env bash
# save_latest.sh - Copy HTML to a timestamped latest file
# Usage: bash scripts/save_latest.sh <source-html> <label>
set -e
SRC="$1"
LABEL="${2:-SmartLink}"
DATE=$(date +%Y%m%d)
DEST_DIR="$(dirname "$SRC")"
DEST="${DEST_DIR}/${LABEL}_最新版_${DATE}.html"
cp "$SRC" "$DEST"
BACKUP_DIR="/Users/tangmingying/Downloads/智慧芽HTML自动备份"
mkdir -p "$BACKUP_DIR"
cp "$SRC" "${BACKUP_DIR}/${LABEL}_${DATE}_$(date +%H%M%S).html"
echo "Saved: $DEST"
echo "Backup: ${BACKUP_DIR}"

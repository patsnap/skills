#!/usr/bin/env bash
# Install the localized skill into an explicit user-selected directory.

set -euo pipefail

usage() {
  echo "Usage: $0 --target <absolute-or-relative-directory> [--install-dependencies]"
  echo
  echo "The installer never deletes an existing installation."
  echo "If the target exists, it is moved to a timestamped sibling backup."
  echo "Dependency installation is opt-in and should be reviewed first."
}

TARGET_DIR=""
INSTALL_DEPS=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)
      if [[ $# -lt 2 ]]; then
        echo "ERROR: --target requires a path." >&2
        exit 2
      fi
      TARGET_DIR=$2
      shift 2
      ;;
    --install-dependencies)
      INSTALL_DEPS=1
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "ERROR: Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -z "$TARGET_DIR" ]]; then
  echo "ERROR: An explicit --target directory is required." >&2
  usage >&2
  exit 2
fi

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

if command -v realpath >/dev/null 2>&1; then
  SOURCE_RESOLVED=$(realpath "$SCRIPT_DIR")
  mkdir -p "$(dirname "$TARGET_DIR")"
  TARGET_PARENT=$(cd "$(dirname "$TARGET_DIR")" && pwd)
  TARGET_RESOLVED="$TARGET_PARENT/$(basename "$TARGET_DIR")"
else
  SOURCE_RESOLVED="$SCRIPT_DIR"
  mkdir -p "$(dirname "$TARGET_DIR")"
  TARGET_PARENT=$(cd "$(dirname "$TARGET_DIR")" && pwd)
  TARGET_RESOLVED="$TARGET_PARENT/$(basename "$TARGET_DIR")"
fi

if [[ "$TARGET_RESOLVED" == "/" || -z "$TARGET_RESOLVED" ]]; then
  echo "ERROR: Refusing to install into a broad or unresolved target." >&2
  exit 1
fi

echo "Patent-Based R&D Briefing Skill Installer"
echo "=========================================="
echo "Version: v1.1.0-localized"
echo "Source: $SOURCE_RESOLVED"
echo "Target: $TARGET_RESOLVED"
echo

if [[ "$SOURCE_RESOLVED" == "$TARGET_RESOLVED" ]]; then
  echo "Package is already at the selected target; file copy is not required."
else
  if [[ -e "$TARGET_RESOLVED" ]]; then
    BACKUP_PATH="${TARGET_RESOLVED}.backup.$(date +%Y%m%d%H%M%S)"
    echo "Existing target detected."
    echo "Backup destination: $BACKUP_PATH"
    read -r -p "Type BACKUP to move the existing target and continue: " answer
    if [[ "$answer" != "BACKUP" ]]; then
      echo "Installation cancelled without changing the target."
      exit 3
    fi
    mv -- "$TARGET_RESOLVED" "$BACKUP_PATH"
  fi
  mkdir -p "$TARGET_RESOLVED"
  cp -R "$SOURCE_RESOLVED"/. "$TARGET_RESOLVED"/
  echo "Package files copied."
fi

chmod +x "$TARGET_RESOLVED/install.sh"
chmod +x "$TARGET_RESOLVED/scripts/run.sh"
chmod +x "$TARGET_RESOLVED/scripts/tag_relevant.py"
chmod +x "$TARGET_RESOLVED/scripts/generate_report.py"

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN=python
else
  echo "ERROR: Python 3 was not found. Package files remain installed." >&2
  exit 1
fi

echo "Python runtime: $($PYTHON_BIN --version 2>&1)"

if [[ $INSTALL_DEPS -eq 1 ]]; then
  echo "Installing declared Python dependencies after explicit opt-in."
  "$PYTHON_BIN" -m pip install -r "$TARGET_RESOLVED/requirements.txt"
else
  if "$PYTHON_BIN" -c "import pandas, openpyxl" >/dev/null 2>&1; then
    echo "Required Python packages are already available."
  else
    echo "Required packages are not currently importable."
    echo "Review requirements.txt, then rerun with --install-dependencies or install them in an approved environment."
  fi
fi

echo
echo "Installation completed"
echo "======================"
echo "Location: $TARGET_RESOLVED"
echo
echo "Next steps:"
echo "1. Read SKILL.md and examples/SAMPLE_DATA.md."
echo "2. Prepare an authorized workbook using English/global column names."
echo "3. Run scripts/run.sh with a configured topic key and ISO dates."
echo "4. Review candidate signals before generating the HTML briefing."
echo
echo "No source-absent README was added. The frozen source refers to one that"
echo "does not exist; SKILL.md is the authoritative operating guide."

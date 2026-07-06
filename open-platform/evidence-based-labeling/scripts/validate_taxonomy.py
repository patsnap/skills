#!/usr/bin/env python3
import argparse
import csv
import json
from collections import Counter
from pathlib import Path

REQUIRED_COLUMNS = ["label_id", "dimension", "label_name", "label_path", "parent_label_id", "definition", "include_when", "exclude_when", "status", "taxonomy_version"]
FORMAL_REQUIRED = ["label_id", "dimension", "label_name", "label_path", "definition", "include_when", "exclude_when", "taxonomy_version"]
VALID_STATUS = {"candidate", "formal", "deprecated"}

def main():
    parser = argparse.ArgumentParser(description="Validate a labeling taxonomy CSV")
    parser.add_argument("taxonomy", type=Path)
    args = parser.parse_args()
    with args.taxonomy.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        fields = reader.fieldnames or []
    errors, warnings = [], []
    missing_columns = [c for c in REQUIRED_COLUMNS if c not in fields]
    if missing_columns:
        errors.append(f"missing columns: {missing_columns}")
    ids = [r.get("label_id", "").strip() for r in rows]
    paths = [r.get("label_path", "").strip() for r in rows if r.get("status", "").strip() == "formal"]
    duplicates = [k for k, v in Counter(ids).items() if k and v > 1]
    duplicate_paths = [k for k, v in Counter(paths).items() if k and v > 1]
    if duplicates: errors.append(f"duplicate label_id: {duplicates}")
    if duplicate_paths: errors.append(f"duplicate formal label_path: {duplicate_paths}")
    id_set = {i for i in ids if i}
    parent_map = {}
    for line, row in enumerate(rows, 2):
        status = row.get("status", "").strip()
        if status not in VALID_STATUS:
            errors.append(f"row {line}: invalid status {status!r}")
        parent = row.get("parent_label_id", "").strip()
        label_id = row.get("label_id", "").strip()
        if parent and parent not in id_set:
            errors.append(f"row {line}: unknown parent_label_id {parent!r}")
        parent_map[label_id] = parent
        if status == "formal":
            for col in FORMAL_REQUIRED:
                if not row.get(col, "").strip():
                    errors.append(f"row {line}: formal label missing {col}")
        if not row.get("positive_example", "").strip():
            warnings.append(f"row {line}: no positive example")
    for label_id in id_set:
        seen, current = set(), label_id
        while current:
            if current in seen:
                errors.append(f"parent cycle involving {label_id}")
                break
            seen.add(current)
            current = parent_map.get(current, "")
    report = {"valid": not errors, "rows": len(rows), "errors": sorted(set(errors)), "warnings": warnings}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not errors else 1)

if __name__ == "__main__":
    main()

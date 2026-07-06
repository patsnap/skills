#!/usr/bin/env python3
"""Create a small RNA patent landscape project scaffold."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def slugify(value: str) -> str:
    chars = []
    last_dash = False
    for ch in value.lower():
        if ch.isalnum():
            chars.append(ch)
            last_dash = False
        elif not last_dash:
            chars.append("-")
            last_dash = True
    return "".join(chars).strip("-") or "company"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("company", help="Company name for the landscape")
    parser.add_argument("--root", default=".", help="Project root directory")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    slug = slugify(args.company)
    paths = {
        "root": root,
        "patent_markdowns": root / "patent_markdowns",
        "outputs": root / "outputs" / "patent_analysis",
        "intermediate": root / "outputs" / "intermediate",
    }
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)

    config = {
        "company": args.company,
        "company_slug": slug,
        "patent_input_file": "patent_numbers.txt",
        "markdown_dir": "patent_markdowns",
        "output_dir": "outputs/patent_analysis",
        "xlsx_output": f"outputs/patent_analysis/{slug}_patent_landscape.xlsx",
        "html_output": f"outputs/patent_analysis/{slug}_multidimensional_tag_timeline.html",
        "suffix_retry_order": ["", "A", "A1", "A2", "B", "B1", "B2"],
    }
    (root / "landscape_config.json").write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    (root / "patent_numbers.txt").touch(exist_ok=True)
    print(json.dumps(config, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

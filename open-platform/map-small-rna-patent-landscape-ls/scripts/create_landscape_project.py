#!/usr/bin/env python3
"""Create a version-safe small-RNA patent-landscape project scaffold."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def slugify(value: str) -> str:
    """Return a conservative ASCII project slug."""
    normalized = value.strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    return normalized.strip("-") or "company"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("company", help="Company or portfolio name")
    parser.add_argument("--root", default=".", help="Existing parent directory")
    parser.add_argument(
        "--project-dir",
        help="Project directory name; defaults to <company-slug>-small-rna-landscape",
    )
    parser.add_argument(
        "--force-empty",
        action="store_true",
        help="Allow use of an existing but empty project directory",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the planned configuration without creating files",
    )
    return parser.parse_args()


def fail(message: str) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(2)


def ensure_within(parent: Path, child: Path) -> None:
    try:
        child.relative_to(parent)
    except ValueError:
        fail(f"Project path escapes the selected root: {child}")


def ensure_empty_or_new(project: Path, force_empty: bool) -> None:
    if not project.exists():
        return
    if not project.is_dir():
        fail(f"Project path exists and is not a directory: {project}")
    entries = list(project.iterdir())
    if entries:
        fail(
            "Refusing to modify a non-empty project directory. "
            "Choose a new --project-dir."
        )
    if not force_empty:
        fail(
            "Project directory already exists. Use --force-empty only after "
            "confirming that it is empty."
        )


def build_config(company: str, project: Path) -> dict[str, object]:
    slug = slugify(company)
    return {
        "schema_version": "2.0",
        "company": company.strip(),
        "company_slug": slug,
        "project_root": str(project),
        "patent_input_file": "patent_numbers.txt",
        "markdown_dir": "patent_markdowns",
        "output_dir": "outputs/patent_analysis",
        "intermediate_dir": "outputs/intermediate",
        "fetch_summary_csv": "outputs/intermediate/fetch_summary.csv",
        "fetch_summary_json": "outputs/intermediate/fetch_summary.json",
        "analysis_rows_json": "outputs/intermediate/patent_analysis_rows.json",
        "xlsx_output": f"outputs/patent_analysis/{slug}_patent_landscape.xlsx",
        "html_output": (
            f"outputs/patent_analysis/{slug}_multidimensional_patent_timeline.html"
        ),
        "identifier_resolution": {
            "preserve_user_input": True,
            "resolve_by_exact_number_service": True,
            "kind_code_guessing": False,
            "note": (
                "Use a verified patent-number resolver. Do not blindly append kind "
                "codes across jurisdictions."
            ),
        },
        "language": "en",
        "status": "scaffold_only",
    }


def main() -> None:
    args = parse_args()
    company = args.company.strip()
    if not company:
        fail("Company name cannot be blank.")

    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        fail(f"--root must be an existing directory: {root}")

    project_name = args.project_dir or f"{slugify(company)}-small-rna-landscape"
    if Path(project_name).is_absolute():
        fail("--project-dir must be a relative directory name.")
    project = (root / project_name).resolve()
    ensure_within(root, project)
    ensure_empty_or_new(project, args.force_empty)

    config = build_config(company, project)
    if args.dry_run:
        print(json.dumps(config, ensure_ascii=True, indent=2))
        return

    directories = [
        project,
        project / "patent_markdowns",
        project / "outputs" / "patent_analysis",
        project / "outputs" / "intermediate",
    ]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

    config_path = project / "landscape_config.json"
    input_path = project / "patent_numbers.txt"
    if config_path.exists() or input_path.exists():
        fail("Refusing to overwrite an existing scaffold file.")

    config_path.write_text(
        json.dumps(config, ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
    )
    input_path.write_text("", encoding="utf-8")
    print(json.dumps(config, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Validate and render a portable five-level system-decomposition map.

The input contract is demonstrated by ``example_mindmap_data_plc.json``.
All values are plain text. The source renderer allowed inline HTML in JSON;
this localized renderer escapes every value and creates markup itself.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from typing import Any


class RenderError(ValueError):
    """Raised when reviewed input is incomplete or unsafe."""


IDENTIFIER = re.compile(r"^[A-Za-z][A-Za-z0-9._-]{0,39}$")


def fail(message: str) -> None:
    raise RenderError(message)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a reviewed five-level system decomposition as self-contained HTML."
    )
    parser.add_argument("--data", required=True, type=Path, help="Reviewed JSON data")
    parser.add_argument("--out", required=True, type=Path, help="Destination HTML file")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace the exact named destination if it exists",
    )
    return parser.parse_args()


def require_object(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{path} must be an object")
    return value


def require_list(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        fail(f"{path} must be an array")
    return value


def require_text(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{path} must be a non-empty string")
    return value.strip()


def optional_text(value: Any, path: str) -> str:
    if value is None:
        return ""
    if not isinstance(value, str):
        fail(f"{path} must be a string")
    return value.strip()


def require_id(value: Any, path: str) -> str:
    identifier = require_text(value, path)
    if not IDENTIFIER.fullmatch(identifier):
        fail(f"{path} contains an invalid identifier")
    return identifier


def require_bool(value: Any, path: str) -> bool:
    if not isinstance(value, bool):
        fail(f"{path} must be a boolean")
    return value


def validate_named_records(value: Any, path: str, allowed: set[str]) -> list[dict[str, Any]]:
    records = require_list(value, path)
    seen: set[str] = set()
    for index, raw in enumerate(records):
        record = require_object(raw, f"{path}[{index}]")
        unknown = set(record) - allowed
        if unknown:
            fail(f"{path}[{index}] contains unsupported keys: {', '.join(sorted(unknown))}")
        identifier = require_id(record.get("id"), f"{path}[{index}].id")
        if identifier in seen:
            fail(f"Duplicate identifier in {path}: {identifier}")
        seen.add(identifier)
        require_text(record.get("name"), f"{path}[{index}].name")
        optional_text(record.get("tag"), f"{path}[{index}].tag")
        for key in allowed & {
            "merged_with_critical_part",
            "priority",
            "reference_only",
        }:
            if key in record:
                require_bool(record[key], f"{path}[{index}].{key}")
    return records


def validate_payload(payload: dict[str, Any]) -> None:
    required = {
        "schema_version",
        "review_status",
        "title",
        "subtitle",
        "product",
        "systems",
        "subsystems",
        "components",
        "critical_parts",
        "notes",
    }
    missing = required - set(payload)
    unknown = set(payload) - required
    if missing:
        fail("Missing top-level fields: " + ", ".join(sorted(missing)))
    if unknown:
        fail("Unsupported top-level fields: " + ", ".join(sorted(unknown)))
    if payload["schema_version"] != "2.0":
        fail("schema_version must be '2.0'")
    if payload["review_status"] != "reviewed-example" and payload["review_status"] != "reviewed":
        fail("review_status must be 'reviewed' or 'reviewed-example'")
    require_text(payload["title"], "title")
    require_text(payload["subtitle"], "subtitle")
    product = require_object(payload["product"], "product")
    if set(product) != {"name", "description"}:
        fail("product must contain exactly name and description")
    require_text(product["name"], "product.name")
    require_text(product["description"], "product.description")
    systems = validate_named_records(
        payload["systems"],
        "systems",
        {"id", "name", "tag", "accent"},
    )
    for index, system in enumerate(systems):
        accent = optional_text(system.get("accent"), f"systems[{index}].accent")
        if accent not in {"", "secondary"}:
            fail(f"systems[{index}].accent must be empty or 'secondary'")
    validate_named_records(
        payload["components"],
        "components",
        {"id", "name", "tag", "merged_with_critical_part"},
    )
    validate_named_records(
        payload["critical_parts"],
        "critical_parts",
        {"id", "name", "tag", "priority", "reference_only"},
    )
    for index, subsystem in enumerate(require_list(payload["subsystems"], "subsystems")):
        require_text(subsystem, f"subsystems[{index}]")
    for index, note in enumerate(require_list(payload["notes"], "notes")):
        require_text(note, f"notes[{index}]")


def e(value: Any) -> str:
    return html.escape(str(value), quote=True)


def node(css_class: str, identifier: str, name: str, tag: str = "") -> str:
    tag_html = f'<p class="tag">{e(tag)}</p>' if tag else ""
    return (
        f'<article class="node {e(css_class)}">'
        f'<p class="id">{e(identifier)}</p>'
        f'<p class="name">{e(name)}</p>'
        f'{tag_html}</article>'
    )


def render(payload: dict[str, Any]) -> str:
    product = payload["product"]
    product_html = (
        '<article class="node product">'
        f'<p class="name">{e(product["name"])}</p>'
        f'<p class="tag">{e(product["description"])}</p>'
        '</article>'
    )
    systems_html = "".join(
        node(
            "system secondary" if record.get("accent") == "secondary" else "system",
            record["id"],
            record["name"],
            record.get("tag", ""),
        )
        for record in payload["systems"]
    )
    subsystems_html = "".join(
        node("subsystem", f"SS{index}", name)
        for index, name in enumerate(payload["subsystems"], start=1)
    )
    components_html = "".join(
        node(
            "component merged" if record.get("merged_with_critical_part") else "component",
            record["id"],
            record["name"],
            record.get("tag", ""),
        )
        for record in payload["components"]
    )
    parts_html = "".join(
        node(
            "critical reference" if record.get("reference_only") else "critical",
            record["id"] + (" PRIORITY" if record.get("priority") else ""),
            record["name"],
            record.get("tag", ""),
        )
        for record in payload["critical_parts"]
    )
    notes_html = "".join(f"<li>{e(note)}</li>" for note in payload["notes"])
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(payload['title'])}</title>
<style>
:root {{
  --canvas: #eef2f5;
  --paper: #ffffff;
  --ink: #17202a;
  --muted: #5f6b76;
  --line: #cbd5dc;
  --navy: #123247;
  --blue: #0b6b9a;
  --teal: #0f766e;
  --amber: #a16207;
  --shadow: 0 6px 18px rgba(18, 50, 71, .08);
}}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--canvas); color: var(--ink); font: 14px/1.5 Inter, Arial, sans-serif; }}
header {{ background: var(--navy); color: #fff; border-bottom: 5px solid #38bdf8; padding: 34px max(24px, calc((100vw - 1450px)/2)); }}
h1 {{ margin: 0; font: 700 2.1rem/1.15 Georgia, serif; }}
header p {{ max-width: 950px; margin: 9px 0 0; color: #d7e5ec; }}
main {{ max-width: 1450px; margin: auto; padding: 24px; }}
.legend {{ display: flex; flex-wrap: wrap; gap: 10px 24px; padding: 14px 18px; background: #fff; border: 1px solid var(--line); }}
.legend span {{ font-weight: 700; }}
.grid {{ display: grid; grid-template-columns: 150px 210px 220px 250px minmax(300px, 1fr); gap: 14px; align-items: start; margin-top: 18px; }}
.column-title {{ border-bottom: 3px solid var(--navy); padding: 7px 4px; color: var(--navy); font-size: .75rem; font-weight: 800; letter-spacing: .09em; text-transform: uppercase; }}
.node {{ margin: 0 0 9px; padding: 10px 12px; background: var(--paper); border: 1px solid var(--line); border-left: 4px solid var(--blue); box-shadow: var(--shadow); }}
.node p {{ margin: 0; }}
.node .id {{ color: var(--blue); font: 700 .7rem/1.4 Consolas, monospace; letter-spacing: .04em; }}
.node .name {{ font-weight: 750; }}
.node .tag {{ margin-top: 3px; color: var(--muted); font-size: .76rem; }}
.product {{ background: var(--navy); color: #fff; border-color: var(--navy); text-align: center; padding: 24px 10px; }}
.product .tag {{ color: #d7e5ec; }}
.system.secondary {{ border-left-color: var(--teal); }}
.merged {{ border-left-style: dashed; border-left-color: var(--muted); }}
.critical {{ border-left-color: var(--amber); }}
.critical.reference {{ border-left-style: dashed; border-left-color: var(--muted); background: #f8fafc; }}
.notes {{ margin-top: 24px; padding: 18px 22px; background: #fff; border: 1px solid var(--line); }}
.notes h2 {{ margin: 0 0 8px; font: 700 1.1rem Georgia, serif; }}
.notes li {{ margin: 4px 0; }}
@media (max-width: 950px) {{
  .grid {{ grid-template-columns: 1fr; }}
  .column-title {{ margin-top: 16px; }}
}}
@media print {{
  body {{ background: #fff; font-size: 9pt; }}
  header {{ background: #fff; color: var(--ink); border-bottom-color: var(--navy); padding: 16px 0; }}
  header p {{ color: var(--muted); }}
  main {{ max-width: none; padding: 0; }}
  .node {{ box-shadow: none; break-inside: avoid; }}
}}
</style>
</head>
<body>
<header><h1>{e(payload['title'])}</h1><p>{e(payload['subtitle'])}</p></header>
<main>
<aside class="legend" aria-label="Legend"><span>Blue: system or component</span><span>Amber: critical review unit</span><span>Dashed: merged or reference-only unit</span></aside>
<section class="grid" aria-label="Five-level system decomposition">
<h2 class="column-title">Product</h2><h2 class="column-title">Major systems</h2><h2 class="column-title">Subsystems</h2><h2 class="column-title">Components</h2><h2 class="column-title">Critical parts or modules</h2>
<div>{product_html}</div><div>{systems_html}</div><div>{subsystems_html}</div><div>{components_html}</div><div>{parts_html}</div>
</section>
<section class="notes"><h2>Scope and review notes</h2><ul>{notes_html}</ul></section>
</main>
</body>
</html>"""


def write_output(path: Path, content: str, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        fail(f"Refusing to overwrite existing file without --overwrite: {path}")
    if path.exists() and path.is_dir():
        fail(f"Output path is a directory: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(content, encoding="utf-8", newline="\n")
    temporary.replace(path)


def main() -> int:
    args = parse_args()
    try:
        payload = require_object(json.loads(args.data.read_text(encoding="utf-8")), "root")
    except (OSError, json.JSONDecodeError) as error:
        fail(f"Cannot read reviewed JSON: {error}")
    validate_payload(payload)
    document = render(payload)
    if "<script" in document.casefold():
        fail("Internal safety check rejected a script element")
    write_output(args.out, document, args.overwrite)
    print(
        "Rendered decomposition: "
        f"systems={len(payload['systems'])}, "
        f"subsystems={len(payload['subsystems'])}, "
        f"components={len(payload['components'])}, "
        f"critical_parts={len(payload['critical_parts'])}"
    )
    print(f"Output: {args.out}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RenderError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)

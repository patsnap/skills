#!/usr/bin/env python3
"""Validate reviewed route labels and render a self-contained evolution forest."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import triz_forest_common as common


class ForestError(ValueError):
    """Raised when forest input or output is invalid."""


UNIT_ID = re.compile(r"^[A-Za-z][A-Za-z0-9._-]{0,39}$")


def fail(message: str) -> None:
    raise ForestError(message)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render reviewed evidence on the compact evolution-route skeleton."
    )
    parser.add_argument("--records", required=True, type=Path, help="Reviewed JSON record file")
    parser.add_argument("--out", required=True, type=Path, help="Destination HTML")
    parser.add_argument("--title", default="Technology Evolution Forest")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def require_object(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{path} must be an object")
    return value


def require_array(value: Any, path: str) -> list[Any]:
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


def require_route(value: Any, path: str) -> int:
    if isinstance(value, bool):
        fail(f"{path} must be an integer route number")
    try:
        route = int(value)
    except (TypeError, ValueError):
        fail(f"{path} must be an integer route number")
    if route not in common.ROUTES:
        fail(f"{path} references unknown route {route}")
    return route


def validate_payload(payload: dict[str, Any]) -> list[dict[str, Any]]:
    required = {"schema_version", "review_status", "taxonomy_id", "part_names", "records"}
    missing = required - set(payload)
    unknown = set(payload) - required
    if missing:
        fail("Missing top-level fields: " + ", ".join(sorted(missing)))
    if unknown:
        fail("Unsupported top-level fields: " + ", ".join(sorted(unknown)))
    if payload["schema_version"] != "2.0":
        fail("schema_version must be '2.0'")
    if payload["review_status"] != "reviewed":
        fail("review_status must be 'reviewed'")
    if payload["taxonomy_id"] != common.TAXONOMY_ID:
        fail(f"taxonomy_id must be {common.TAXONOMY_ID!r}")
    part_names = require_object(payload["part_names"], "part_names")
    for identifier, name in part_names.items():
        if not isinstance(identifier, str) or not UNIT_ID.fullmatch(identifier):
            fail(f"Invalid part_names identifier: {identifier!r}")
        require_text(name, f"part_names.{identifier}")

    records = require_array(payload["records"], "records")
    seen: set[str] = set()
    allowed = {"id", "publication_id", "unit_id", "core", "labels", "dependent_routes"}
    for index, raw in enumerate(records):
        record = require_object(raw, f"records[{index}]")
        unknown_record = set(record) - allowed
        if unknown_record:
            fail(f"records[{index}] contains unsupported keys: {', '.join(sorted(unknown_record))}")
        identifier = require_text(record.get("id"), f"records[{index}].id")
        if identifier in seen:
            fail(f"Duplicate record id: {identifier}")
        seen.add(identifier)
        optional_text(record.get("publication_id"), f"records[{index}].publication_id")
        unit_id = require_text(record.get("unit_id"), f"records[{index}].unit_id")
        if not UNIT_ID.fullmatch(unit_id):
            fail(f"records[{index}].unit_id is invalid")
        if unit_id not in part_names:
            fail(f"records[{index}].unit_id is not declared in part_names")
        require_text(record.get("core"), f"records[{index}].core")
        labels = require_object(record.get("labels"), f"records[{index}].labels")
        if not labels:
            fail(f"records[{index}].labels must not be empty")
        for raw_route, raw_label in labels.items():
            route = require_route(raw_route, f"records[{index}].labels route")
            label = require_object(raw_label, f"records[{index}].labels.{route}")
            if set(label) != {"node", "action"}:
                fail(f"records[{index}].labels.{route} must contain node and action")
            node = require_text(label["node"], f"records[{index}].labels.{route}.node")
            valid_nodes = {position for position, _ in common.ROUTES[route]}
            if node not in valid_nodes:
                fail(f"records[{index}].labels.{route}.node is not in the compact taxonomy")
            require_text(label["action"], f"records[{index}].labels.{route}.action")
        for edge_index, raw_edge in enumerate(require_array(record.get("dependent_routes", []), f"records[{index}].dependent_routes")):
            edge = require_object(raw_edge, f"records[{index}].dependent_routes[{edge_index}]")
            if set(edge) != {"from_route", "from_node", "to_route", "rationale", "evidence"}:
                fail(f"records[{index}].dependent_routes[{edge_index}] has an invalid shape")
            from_route = require_route(edge["from_route"], f"records[{index}].dependent_routes[{edge_index}].from_route")
            to_route = require_route(edge["to_route"], f"records[{index}].dependent_routes[{edge_index}].to_route")
            from_node = require_text(edge["from_node"], f"records[{index}].dependent_routes[{edge_index}].from_node")
            if from_node not in {position for position, _ in common.ROUTES[from_route]}:
                fail(f"records[{index}].dependent_routes[{edge_index}].from_node is invalid")
            if from_route == to_route:
                fail(f"records[{index}].dependent_routes[{edge_index}] must link different routes")
            require_text(edge["rationale"], f"records[{index}].dependent_routes[{edge_index}].rationale")
            require_text(edge["evidence"], f"records[{index}].dependent_routes[{edge_index}].evidence")
    return records


def build_units(payload: dict[str, Any], records: list[dict[str, Any]]) -> dict[str, Any]:
    units: dict[str, Any] = defaultdict(
        lambda: {
            "routes": defaultdict(lambda: {"hits": defaultdict(int), "representative": {}}),
            "record_ids": set(),
            "edges": [],
        }
    )
    for record in records:
        unit = units[record["unit_id"]]
        unit["record_ids"].add(record["id"])
        for raw_route, label in record["labels"].items():
            route = int(raw_route)
            position = label["node"]
            route_data = unit["routes"][route]
            route_data["hits"][position] += 1
            if position not in route_data["representative"]:
                route_data["representative"][position] = {
                    "action": label["action"],
                    "record_id": record["publication_id"] or record["id"],
                }
        for edge in record["dependent_routes"]:
            unit["edges"].append({**edge, "record_id": record["id"]})
    return units


def render_document(payload: dict[str, Any], records: list[dict[str, Any]], title: str) -> str:
    units = build_units(payload, records)
    body: list[str] = []
    for unit_id in sorted(units):
        unit = units[unit_id]
        routes = sorted(unit["routes"])
        sections = [
            '<article class="unit">',
            '<header class="unit-header">',
            f'<h2>{common.escape(payload["part_names"][unit_id])}</h2>',
            f'<p>{common.escape(unit_id)}; {len(routes)} active routes; {len(unit["record_ids"])} accepted records</p>',
            '</header>',
            '<div class="unit-body">',
        ]
        for route in routes:
            route_data = unit["routes"][route]
            sections.append(
                common.render_route(
                    route,
                    dict(route_data["hits"]),
                    route_data["representative"],
                )
            )
        if unit["edges"]:
            annotations = []
            for edge in unit["edges"]:
                annotations.append(
                    '<span class="annotation"><strong>Evidence-supported dependent route:</strong> '
                    f'route {common.escape(edge["from_route"])} node {common.escape(edge["from_node"])} '
                    f'→ route {common.escape(edge["to_route"])}; '
                    f'{common.escape(edge["rationale"])}; '
                    f'evidence {common.escape(edge["record_id"])}: {common.escape(edge["evidence"])}</span>'
                )
            sections.append('<div class="annotations">' + "".join(annotations) + '</div>')
        sections.extend(['</div>', '</article>'])
        body.append("".join(sections))

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{common.escape(title)}</title>
<style>{common.CSS}</style>
</head>
<body>
<header>
<h1>{common.escape(title)}</h1>
<p>Taxonomy: {common.escape(common.TAXONOMY_ID)}. A zero-hit node means only that no accepted record was observed in this reviewed dataset. It does not establish global white space, novelty, or freedom to operate.</p>
</header>
{common.LEGEND}
<main>{''.join(body)}</main>
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
        payload = require_object(json.loads(args.records.read_text(encoding="utf-8")), "root")
    except (OSError, json.JSONDecodeError) as error:
        fail(f"Cannot read reviewed JSON: {error}")
    records = validate_payload(payload)
    document = render_document(payload, records, args.title)
    if "<script" in document.casefold():
        fail("Internal safety check rejected a script element")
    write_output(args.out, document, args.overwrite)
    print(f"Rendered forest: units={len(build_units(payload, records))}, records={len(records)}")
    print(f"Output: {args.out}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ForestError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)

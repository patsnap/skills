#!/usr/bin/env python3
"""Render a reviewed competitive-intelligence data set into a bundled HTML template."""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path
from typing import Any


TOKEN = re.compile(r"\{\{([A-Z][A-Z0-9_]*)\}\}")
REQUIRED_FIELDS = (
    "report_title",
    "focal_organization",
    "technology_scope",
    "geography",
    "report_period",
    "evidence_cutoff",
    "analyst",
)
TEMPLATES = {"v8": "template_v8.html", "v11": "template_v11.html", "v12": "template_v12.html"}


class InputError(ValueError):
    """Raised when the reviewed data contract is incomplete or unsafe."""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render an evidence-led technology competitive-intelligence HTML report."
    )
    parser.add_argument("--data", required=True, type=Path, help="UTF-8 JSON input reviewed by an analyst")
    parser.add_argument("--output", required=True, type=Path, help="Destination .html file")
    parser.add_argument("--template", choices=sorted(TEMPLATES), default="v12", help="Bundled report generation")
    return parser.parse_args(argv)


def read_data(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise InputError(f"Input file does not exist: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise InputError(f"Input must be valid UTF-8 JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise InputError("The JSON root must be an object.")
    return value


def validate_data(data: dict[str, Any]) -> None:
    if data.get("review_status") != "reviewed":
        raise InputError("review_status must be 'reviewed' before publication.")
    missing = [name for name in REQUIRED_FIELDS if not str(data.get(name, "")).strip()]
    if missing:
        raise InputError("Missing required fields: " + ", ".join(missing))
    for name in REQUIRED_FIELDS:
        if not isinstance(data[name], str):
            raise InputError(f"{name} must be a string.")
    if len(data["report_title"]) > 240:
        raise InputError("report_title exceeds 240 characters.")
    sections = data.get("sections", {})
    if sections is not None and not isinstance(sections, dict):
        raise InputError("sections must be an object when supplied.")


def plain_text(value: Any, fallback: str = "Not established from reviewed evidence") -> str:
    if value is None or value == "":
        return fallback
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, indent=2)
    return str(value)


def build_tokens(data: dict[str, Any]) -> dict[str, str]:
    sections = data.get("sections") or {}
    values: dict[str, Any] = {
        "REPORT_TITLE": data["report_title"],
        "FOCAL_ORGANIZATION": data["focal_organization"],
        "TECHNOLOGY_SCOPE": data["technology_scope"],
        "GEOGRAPHY": data["geography"],
        "REPORT_PERIOD": data["report_period"],
        "EVIDENCE_CUTOFF": data["evidence_cutoff"],
        "ANALYST": data["analyst"],
        "DECISION_CONTEXT": data.get("decision_context"),
        "EXECUTIVE_SUMMARY": sections.get("executive_summary"),
        "SCOPE_METHOD": sections.get("scope_method"),
        "MARKET_LANDSCAPE": sections.get("market_landscape"),
        "FOCAL_POSITION": sections.get("focal_position"),
        "TIER_A": sections.get("tier_a"),
        "TIER_B": sections.get("tier_b"),
        "CUSTOMER_MATRIX": sections.get("customer_matrix"),
        "EVENTS": sections.get("events"),
        "THREATS_OPPORTUNITIES": sections.get("threats_opportunities"),
        "ACTIONS": sections.get("actions"),
        "SOURCES": sections.get("sources"),
        "LIMITATIONS": data.get("limitations"),
    }
    return {key: html.escape(plain_text(value), quote=True) for key, value in values.items()}


def render(template: str, tokens: dict[str, str]) -> str:
    unknown = sorted(set(TOKEN.findall(template)) - set(tokens))
    if unknown:
        raise InputError("Template contains unsupported tokens: " + ", ".join(unknown))
    rendered = TOKEN.sub(lambda match: tokens[match.group(1)], template)
    remaining = sorted(set(TOKEN.findall(rendered)))
    if remaining:
        raise InputError("Unresolved template tokens: " + ", ".join(remaining))
    return rendered


def safe_output(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    if resolved.suffix.lower() != ".html":
        raise InputError("Output must use the .html extension.")
    if resolved.parent == resolved:
        raise InputError("Refusing to write to a filesystem root.")
    return resolved


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        data = read_data(args.data)
        validate_data(data)
        template_path = Path(__file__).resolve().parent.parent / "references" / TEMPLATES[args.template]
        template = template_path.read_text(encoding="utf-8")
        output = safe_output(args.output)
        result = render(template, build_tokens(data))
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(result, encoding="utf-8")
    except (InputError, OSError, UnicodeError) as exc:
        print(f"error: {exc}")
        return 2
    print(f"Rendered reviewed report: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

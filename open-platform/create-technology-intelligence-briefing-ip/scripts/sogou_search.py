"""Normalize already retrieved news records for the briefing.

The filename is retained solely to preserve the source package topology. The
localized implementation does not scrape Sogou or any search-result page.
Use an authorized web-research tool first, save its records as JSON, and pass
that JSON to this script for deterministic validation and normalization.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


REQUIRED_FIELDS = ("title", "source", "publication_date", "url")


def safe_http_url(value: Any) -> str:
    """Return a normalized HTTP(S) URL or an empty string."""
    if not isinstance(value, str):
        return ""
    candidate = value.strip()
    parsed = urlparse(candidate)
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc:
        return ""
    return candidate


def iso_date(value: Any, field: str) -> str:
    """Validate an ISO 8601 calendar date."""
    if not isinstance(value, str) or not value.strip():
        return ""
    candidate = value.strip()
    try:
        date.fromisoformat(candidate)
    except ValueError as exc:
        raise ValueError(f"{field} must use YYYY-MM-DD: {candidate!r}") from exc
    return candidate


def clean_text(value: Any) -> str:
    """Collapse whitespace without interpreting markup."""
    if value is None:
        return ""
    return " ".join(str(value).split())


def normalize_record(raw: Any, index: int) -> dict[str, Any]:
    """Validate one record and return the renderer's stable schema."""
    if not isinstance(raw, dict):
        raise ValueError(f"Record {index} must be a JSON object")

    missing = [field for field in REQUIRED_FIELDS if not clean_text(raw.get(field))]
    if missing:
        raise ValueError(f"Record {index} is missing: {', '.join(missing)}")

    url = safe_http_url(raw.get("url"))
    if not url:
        raise ValueError(f"Record {index} has an unsafe or invalid URL")

    publication_date = iso_date(raw.get("publication_date"), "publication_date")
    event_date = iso_date(raw.get("event_date"), "event_date")
    retrieved_at = iso_date(raw.get("retrieved_at"), "retrieved_at")
    if not retrieved_at:
        raise ValueError(f"Record {index} requires retrieved_at")

    return {
        "id": clean_text(raw.get("id")) or f"NEWS-{index:04d}",
        "title": clean_text(raw.get("title")),
        "source": clean_text(raw.get("source")),
        "publication_date": publication_date,
        "event_date": event_date,
        "url": url,
        "summary": clean_text(raw.get("summary") or raw.get("desc")),
        "relevance": clean_text(raw.get("relevance")),
        "source_quality": clean_text(raw.get("source_quality")),
        "company": clean_text(raw.get("company")),
        "technology": clean_text(raw.get("technology")),
        "retrieved_at": retrieved_at,
    }


def normalize_records(payload: Any) -> list[dict[str, Any]]:
    """Normalize a JSON list or a mapping containing ``items``."""
    items = payload.get("items") if isinstance(payload, dict) else payload
    if not isinstance(items, list):
        raise ValueError("Input must be a JSON list or an object with an items list")

    normalized = [normalize_record(item, i) for i, item in enumerate(items, 1)]
    seen: set[str] = set()
    output: list[dict[str, Any]] = []
    for item in normalized:
        key = item["url"].casefold()
        if key not in seen:
            seen.add(key)
            output.append(item)
    return output


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path | None, value: Any) -> None:
    rendered = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    if path is None:
        sys.stdout.write(rendered)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(rendered, encoding="utf-8")


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(
        description="Normalize authorized news-research records; no web scraping is performed."
    )
    command.add_argument("input", type=Path, help="UTF-8 JSON input")
    command.add_argument("--output", type=Path, help="Optional UTF-8 JSON output")
    return command


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        result = normalize_records(read_json(args.input))
        write_json(args.output, result)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"news normalization failed: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

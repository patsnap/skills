#!/usr/bin/env python3
"""Validate and render an evidence-backed R&D direction report."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable, Sequence
from urllib.parse import urlparse


SCHEMA_VERSION = "2.0"
ISSUE_ID = re.compile(r"^T[1-9][0-9]*$")
DIRECTION_ID = re.compile(r"^D[1-9][0-9]*$")
TASK_ID = re.compile(r"^D[1-9][0-9]*-R[1-9][0-9]*$")
EVIDENCE_ID = re.compile(r"^E[1-9][0-9]*$")
ORGANIZATION_ID = re.compile(r"^O[1-9][0-9]*$")
SEARCH_ID = re.compile(r"^S[1-9][0-9]*$")
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ALLOWED_EVIDENCE_TYPES = {
    "patent",
    "paper",
    "standard",
    "engineering_case",
    "authoritative_web",
}
ALLOWED_CONFIDENCE = {"high", "medium", "low"}
ALLOWED_REVIEW_STATUS = {
    "unreviewed",
    "checked",
    "corroborated",
    "specialist reviewed",
}
MISSING_SOURCE_VALUE = "Not provided in the source requirement"
REQUIRED_TOP_LEVEL = (
    "schema_version",
    "review_status",
    "meta",
    "requirement_text",
    "analysis",
    "issues",
    "directions",
    "evidence",
    "organizations",
    "search_log",
    "limitations",
    "review",
)
REQUIRED_META = (
    "project_name",
    "project_short_name",
    "applicant_or_team",
    "report_date",
    "evidence_cutoff",
    "decision_context",
    "scope",
    "geographies",
    "languages",
    "patent_count_unit",
    "time_zone",
)


class ReportError(ValueError):
    """Raised when a report cannot be validated or rendered safely."""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate an identify-rd-directions-rd v2 payload and render "
            "synchronized self-contained HTML and Markdown reports."
        )
    )
    parser.add_argument("--payload", required=True, type=Path, help="Reviewed v2 JSON payload")
    parser.add_argument("--output", required=True, type=Path, help="Destination HTML report")
    parser.add_argument(
        "--markdown-output",
        required=True,
        type=Path,
        help="Destination Markdown report",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace the exact named HTML and Markdown files if they already exist",
    )
    return parser.parse_args(argv)


def fail(message: str) -> None:
    raise ReportError(message)


def require_object(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{path} must be an object")
    return value


def require_array(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        fail(f"{path} must be an array")
    return value


def require_string(value: Any, path: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str):
        fail(f"{path} must be a string")
    cleaned = value.strip()
    if not allow_empty and not cleaned:
        fail(f"{path} must not be empty")
    return cleaned


def optional_string(value: Any, path: str) -> str:
    if value is None:
        return ""
    return require_string(value, path, allow_empty=True)


def require_string_array(value: Any, path: str) -> list[str]:
    values = require_array(value, path)
    return [require_string(item, f"{path}[{index}]") for index, item in enumerate(values)]


def require_date(value: Any, path: str) -> str:
    date = require_string(value, path)
    if not ISO_DATE.fullmatch(date):
        fail(f"{path} must use YYYY-MM-DD")
    return date


def require_non_negative_int(value: Any, path: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        fail(f"{path} must be a non-negative integer")
    return value


def optional_non_negative_int(value: Any, path: str) -> int | None:
    if value is None:
        return None
    return require_non_negative_int(value, path)


def require_identifier(value: Any, path: str, pattern: re.Pattern[str]) -> str:
    identifier = require_string(value, path)
    if not pattern.fullmatch(identifier):
        fail(f"{path} has an invalid identifier: {identifier!r}")
    return identifier


def require_enum(value: Any, path: str, allowed: set[str]) -> str:
    selected = require_string(value, path)
    if selected not in allowed:
        fail(f"{path} must be one of: {', '.join(sorted(allowed))}")
    return selected


def safe_url(value: Any, path: str) -> str:
    url = optional_string(value, path)
    if not url:
        return ""
    parsed = urlparse(url)
    if parsed.scheme not in {"https", "http"} or not parsed.netloc:
        fail(f"{path} must be an absolute HTTP(S) URL or empty")
    if parsed.username or parsed.password:
        fail(f"{path} must not contain embedded credentials")
    return url


def unique_map(
    values: Any,
    path: str,
    pattern: re.Pattern[str],
) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for index, raw in enumerate(require_array(values, path)):
        item = require_object(raw, f"{path}[{index}]")
        identifier = require_identifier(item.get("id"), f"{path}[{index}].id", pattern)
        if identifier in result:
            fail(f"Duplicate identifier {identifier!r} in {path}")
        result[identifier] = item
    return result


def resolve_references(
    values: Any,
    path: str,
    allowed: set[str],
) -> list[str]:
    references = require_string_array(values, path)
    duplicates = [key for key, count in _counts(references).items() if count > 1]
    if duplicates:
        fail(f"{path} contains duplicate references: {', '.join(duplicates)}")
    unknown = [reference for reference in references if reference not in allowed]
    if unknown:
        fail(f"{path} contains unresolved references: {', '.join(unknown)}")
    return references


def _counts(values: Iterable[str]) -> dict[str, int]:
    result: dict[str, int] = {}
    for value in values:
        result[value] = result.get(value, 0) + 1
    return result


def load_payload(path: Path) -> dict[str, Any]:
    if not path.is_file():
        fail(f"Payload does not exist: {path}")
    if path.is_symlink():
        fail("Payload must not be a symbolic link")
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        fail(f"Unable to read UTF-8 payload: {exc}")
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        fail(f"Invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}")
    return require_object(payload, "root")


def validate_meta(meta: dict[str, Any]) -> None:
    for key in REQUIRED_META:
        if key not in meta:
            fail(f"meta.{key} is required")
    for key in ("project_name", "project_short_name", "applicant_or_team"):
        require_string(meta[key], f"meta.{key}", allow_empty=True)
    for key in ("decision_context", "scope", "patent_count_unit", "time_zone"):
        require_string(meta[key], f"meta.{key}")
    require_string_array(meta["geographies"], "meta.geographies")
    require_string_array(meta["languages"], "meta.languages")
    report_date = require_date(meta["report_date"], "meta.report_date")
    evidence_cutoff = require_date(meta["evidence_cutoff"], "meta.evidence_cutoff")
    if evidence_cutoff > report_date:
        fail("meta.evidence_cutoff must not be after meta.report_date")


def validate_analysis(analysis: dict[str, Any]) -> None:
    groups = {
        "demand": (
            "operating_context",
            "stakeholder_need",
            "technical_consequence",
            "current_response",
        ),
        "bottleneck": (
            "performance_limit",
            "evidence",
            "tradeoffs",
            "mechanistic_limit",
        ),
        "solution_hypothesis": (
            "technical_path",
            "system_concept",
            "compatibility",
            "target_outcome",
        ),
    }
    for group, keys in groups.items():
        obj = require_object(analysis.get(group), f"analysis.{group}")
        for key in keys:
            require_string(obj.get(key), f"analysis.{group}.{key}")


def validate_issue(item: dict[str, Any], path: str, issue_ids: set[str]) -> None:
    require_string(item.get("name"), f"{path}.name")
    require_string(item.get("description"), f"{path}.description")
    locations = require_string_array(item.get("source_locations"), f"{path}.source_locations")
    if not locations:
        fail(f"{path}.source_locations must contain at least one source location")
    resolve_references(item.get("dependencies", []), f"{path}.dependencies", issue_ids)
    require_enum(item.get("confidence"), f"{path}.confidence", ALLOWED_CONFIDENCE)


def validate_task(
    task: dict[str, Any],
    path: str,
    direction_id: str,
    evidence_ids: set[str],
) -> None:
    task_id = require_identifier(task.get("id"), f"{path}.id", TASK_ID)
    if not task_id.startswith(direction_id + "-R"):
        fail(f"{path}.id must use its parent direction prefix {direction_id}-R")
    require_string(task.get("text"), f"{path}.text")
    require_string(task.get("validation_method"), f"{path}.validation_method")
    require_string(task.get("success_metric"), f"{path}.success_metric")
    references = resolve_references(
        task.get("evidence_ids", []),
        f"{path}.evidence_ids",
        evidence_ids,
    )
    uncertainty = require_string(task.get("uncertainty"), f"{path}.uncertainty")
    if not references and "hypothesis" not in uncertainty.casefold():
        fail(f"{path} has no evidence and must explicitly label an analyst hypothesis")


def validate_direction(
    item: dict[str, Any],
    path: str,
    issue_ids: set[str],
    evidence_ids: set[str],
) -> None:
    direction_id = require_identifier(item.get("id"), f"{path}.id", DIRECTION_ID)
    require_string(item.get("name"), f"{path}.name")
    issues = resolve_references(item.get("issue_ids"), f"{path}.issue_ids", issue_ids)
    if not issues:
        fail(f"{path}.issue_ids must contain at least one issue")
    for key in (
        "rationale",
        "core_question",
        "target",
        "evidence_gap",
        "priority_basis",
    ):
        require_string(item.get(key), f"{path}.{key}")
    require_enum(item.get("confidence"), f"{path}.confidence", ALLOWED_CONFIDENCE)
    deliverables = require_string_array(item.get("deliverables"), f"{path}.deliverables")
    if not deliverables:
        fail(f"{path}.deliverables must contain at least one deliverable")
    resolve_references(item.get("evidence_ids", []), f"{path}.evidence_ids", evidence_ids)
    task_ids: set[str] = set()
    tasks = require_array(item.get("research_tasks"), f"{path}.research_tasks")
    if not tasks:
        fail(f"{path}.research_tasks must contain at least one task")
    for index, raw_task in enumerate(tasks):
        task = require_object(raw_task, f"{path}.research_tasks[{index}]")
        task_id = require_identifier(
            task.get("id"),
            f"{path}.research_tasks[{index}].id",
            TASK_ID,
        )
        if task_id in task_ids:
            fail(f"Duplicate task ID {task_id!r} in {path}")
        task_ids.add(task_id)
        validate_task(
            task,
            f"{path}.research_tasks[{index}]",
            direction_id,
            evidence_ids,
        )


def validate_patent_subtype(value: Any, path: str) -> None:
    obj = require_object(value, path)
    require_string(obj.get("publication_number"), f"{path}.publication_number")
    require_string(obj.get("jurisdiction"), f"{path}.jurisdiction")
    require_string_array(obj.get("applicants"), f"{path}.applicants")
    require_string_array(obj.get("assignees"), f"{path}.assignees")
    priority = optional_string(obj.get("earliest_priority_date"), f"{path}.earliest_priority_date")
    if priority:
        require_date(priority, f"{path}.earliest_priority_date")
    require_date(obj.get("publication_date"), f"{path}.publication_date")
    optional_string(obj.get("simple_family_id"), f"{path}.simple_family_id")
    optional_string(obj.get("legal_status"), f"{path}.legal_status")
    status_date = optional_string(obj.get("legal_status_as_of"), f"{path}.legal_status_as_of")
    if status_date:
        require_date(status_date, f"{path}.legal_status_as_of")
    optional_non_negative_int(obj.get("cited_by"), f"{path}.cited_by")


def validate_paper_subtype(value: Any, path: str) -> None:
    obj = require_object(value, path)
    require_string_array(obj.get("authors"), f"{path}.authors")
    require_string_array(obj.get("affiliations"), f"{path}.affiliations")
    require_string(obj.get("venue"), f"{path}.venue")
    optional_string(obj.get("doi"), f"{path}.doi")
    require_string(obj.get("publication_type"), f"{path}.publication_type")
    require_string(obj.get("peer_review_status"), f"{path}.peer_review_status")
    optional_non_negative_int(obj.get("cited_by"), f"{path}.cited_by")


def validate_case_subtype(value: Any, path: str) -> None:
    obj = require_object(value, path)
    require_string(obj.get("publisher"), f"{path}.publisher")
    optional_string(obj.get("document_number"), f"{path}.document_number")
    require_string(obj.get("status_or_stage"), f"{path}.status_or_stage")
    require_string(obj.get("location_or_system"), f"{path}.location_or_system")


def validate_web_subtype(value: Any, path: str) -> None:
    obj = require_object(value, path)
    require_string(obj.get("publisher_type"), f"{path}.publisher_type")
    require_string(obj.get("content_category"), f"{path}.content_category")


def validate_evidence(
    item: dict[str, Any],
    path: str,
    direction_ids: set[str],
    organization_ids: set[str],
    cutoff: str,
) -> None:
    evidence_type = require_enum(
        item.get("evidence_type"),
        f"{path}.evidence_type",
        ALLOWED_EVIDENCE_TYPES,
    )
    for key in ("title", "source_name", "language", "summary", "relevance", "review_depth"):
        require_string(item.get(key), f"{path}.{key}")
    safe_url(item.get("source_url", ""), f"{path}.source_url")
    published = require_date(item.get("published_date"), f"{path}.published_date")
    accessed = require_date(item.get("accessed_date"), f"{path}.accessed_date")
    if published > cutoff:
        fail(f"{path}.published_date exceeds the evidence cutoff")
    if accessed > cutoff:
        fail(f"{path}.accessed_date exceeds the evidence cutoff")
    year = require_non_negative_int(item.get("year"), f"{path}.year")
    if year != int(published[:4]):
        fail(f"{path}.year must equal the published_date year")
    resolve_references(
        item.get("organization_ids", []),
        f"{path}.organization_ids",
        organization_ids,
    )
    direction_refs = resolve_references(
        item.get("direction_ids"),
        f"{path}.direction_ids",
        direction_ids,
    )
    if not direction_refs:
        fail(f"{path}.direction_ids must contain at least one direction")
    require_enum(item.get("review_status"), f"{path}.review_status", ALLOWED_REVIEW_STATUS)
    require_enum(item.get("confidence"), f"{path}.confidence", ALLOWED_CONFIDENCE)
    subtypes = {
        "patent": require_object(item.get("patent"), f"{path}.patent"),
        "paper": require_object(item.get("paper"), f"{path}.paper"),
        "standard_or_case": require_object(
            item.get("standard_or_case"),
            f"{path}.standard_or_case",
        ),
        "web": require_object(item.get("web"), f"{path}.web"),
    }
    expected_key = {
        "patent": "patent",
        "paper": "paper",
        "standard": "standard_or_case",
        "engineering_case": "standard_or_case",
        "authoritative_web": "web",
    }[evidence_type]
    for key, subtype in subtypes.items():
        if key == expected_key and not subtype:
            fail(f"{path}.{key} must be populated for evidence_type {evidence_type}")
        if key != expected_key and subtype:
            fail(f"{path}.{key} must be empty for evidence_type {evidence_type}")
    if evidence_type == "patent":
        validate_patent_subtype(subtypes["patent"], f"{path}.patent")
    elif evidence_type == "paper":
        validate_paper_subtype(subtypes["paper"], f"{path}.paper")
    elif evidence_type in {"standard", "engineering_case"}:
        validate_case_subtype(subtypes["standard_or_case"], f"{path}.standard_or_case")
    else:
        validate_web_subtype(subtypes["web"], f"{path}.web")


def validate_organization(
    item: dict[str, Any],
    path: str,
    direction_ids: set[str],
    evidence_ids: set[str],
) -> None:
    require_string(item.get("name"), f"{path}.name")
    require_string_array(item.get("aliases"), f"{path}.aliases")
    require_string(item.get("organization_type"), f"{path}.organization_type")
    resolve_references(item.get("direction_ids"), f"{path}.direction_ids", direction_ids)
    require_string(item.get("focus"), f"{path}.focus")
    evidence = resolve_references(
        item.get("evidence_ids"),
        f"{path}.evidence_ids",
        evidence_ids,
    )
    if not evidence:
        fail(f"{path}.evidence_ids must contain at least one record")
    require_string(item.get("representative_outputs"), f"{path}.representative_outputs")
    require_enum(item.get("confidence"), f"{path}.confidence", ALLOWED_CONFIDENCE)


def validate_search(
    item: dict[str, Any],
    path: str,
    direction_ids: set[str],
    evidence_ids: set[str],
) -> None:
    resolve_references(
        [item.get("direction_id")],
        f"{path}.direction_id",
        direction_ids,
    )
    require_enum(
        item.get("evidence_type"),
        f"{path}.evidence_type",
        ALLOWED_EVIDENCE_TYPES,
    )
    for key in (
        "source_or_tool",
        "searched_at",
        "query",
        "deduplication",
        "pagination_or_truncation",
        "limitations",
    ):
        require_string(item.get(key), f"{path}.{key}")
    require_object(item.get("filters"), f"{path}.filters")
    require_string_array(item.get("languages"), f"{path}.languages")
    require_non_negative_int(item.get("requested_limit"), f"{path}.requested_limit")
    require_non_negative_int(item.get("returned_count"), f"{path}.returned_count")
    resolve_references(
        item.get("reviewed_evidence_ids", []),
        f"{path}.reviewed_evidence_ids",
        evidence_ids,
    )


def validate_review(review: dict[str, Any]) -> None:
    for key in ("analyst", "reviewer", "quality_status", "legal_boundary"):
        require_string(review.get(key), f"review.{key}")
    require_date(review.get("reviewed_on"), "review.reviewed_on")


def validate_payload(payload: dict[str, Any]) -> dict[str, dict[str, dict[str, Any]]]:
    missing = [key for key in REQUIRED_TOP_LEVEL if key not in payload]
    if missing:
        fail("Missing top-level fields: " + ", ".join(missing))
    if payload.get("schema_version") != SCHEMA_VERSION:
        fail(f"schema_version must be {SCHEMA_VERSION!r}")
    if payload.get("review_status") != "reviewed":
        fail("review_status must be 'reviewed'")

    meta = require_object(payload["meta"], "meta")
    validate_meta(meta)
    require_string(payload["requirement_text"], "requirement_text")
    validate_analysis(require_object(payload["analysis"], "analysis"))
    limitations = require_string_array(payload["limitations"], "limitations")
    if not limitations:
        fail("limitations must contain at least one limitation")
    validate_review(require_object(payload["review"], "review"))

    maps = {
        "issues": unique_map(payload["issues"], "issues", ISSUE_ID),
        "directions": unique_map(payload["directions"], "directions", DIRECTION_ID),
        "evidence": unique_map(payload["evidence"], "evidence", EVIDENCE_ID),
        "organizations": unique_map(
            payload["organizations"],
            "organizations",
            ORGANIZATION_ID,
        ),
        "search_log": unique_map(payload["search_log"], "search_log", SEARCH_ID),
    }
    issue_ids = set(maps["issues"])
    direction_ids = set(maps["directions"])
    evidence_ids = set(maps["evidence"])
    organization_ids = set(maps["organizations"])
    cutoff = meta["evidence_cutoff"]

    if not issue_ids:
        fail("issues must contain at least one technical issue")
    if not direction_ids:
        fail("directions must contain at least one R&D direction")

    for identifier, issue in maps["issues"].items():
        validate_issue(issue, f"issues[{identifier}]", issue_ids)
    for identifier, evidence in maps["evidence"].items():
        validate_evidence(
            evidence,
            f"evidence[{identifier}]",
            direction_ids,
            organization_ids,
            cutoff,
        )
    for identifier, direction in maps["directions"].items():
        validate_direction(
            direction,
            f"directions[{identifier}]",
            issue_ids,
            evidence_ids,
        )
    for identifier, organization in maps["organizations"].items():
        validate_organization(
            organization,
            f"organizations[{identifier}]",
            direction_ids,
            evidence_ids,
        )
    for identifier, search in maps["search_log"].items():
        validate_search(
            search,
            f"search_log[{identifier}]",
            direction_ids,
            evidence_ids,
        )

    covered = {
        issue_id
        for direction in maps["directions"].values()
        for issue_id in direction["issue_ids"]
    }
    uncovered = sorted(issue_ids - covered, key=id_number)
    if uncovered:
        combined_limits = " ".join(limitations)
        missing_disclosure = [issue for issue in uncovered if issue not in combined_limits]
        if missing_disclosure:
            fail(
                "Uncovered issues must be named in limitations: "
                + ", ".join(missing_disclosure)
            )

    for evidence_id, evidence in maps["evidence"].items():
        for organization_id in evidence["organization_ids"]:
            organization = maps["organizations"][organization_id]
            if evidence_id not in organization["evidence_ids"]:
                fail(
                    f"evidence[{evidence_id}] references {organization_id}, but the "
                    "organization does not reference the evidence"
                )
        for direction_id in evidence["direction_ids"]:
            direction = maps["directions"][direction_id]
            cited = set(direction["evidence_ids"])
            for task in direction["research_tasks"]:
                cited.update(task["evidence_ids"])
            if evidence_id not in cited:
                fail(
                    f"evidence[{evidence_id}] references {direction_id}, but the "
                    "direction or its tasks do not reference the evidence"
                )

    return maps


def id_number(identifier: str) -> int:
    match = re.search(r"\d+", identifier)
    return int(match.group(0)) if match else 0


def text(value: Any, fallback: str = "Not provided") -> str:
    if value is None:
        return fallback
    rendered = str(value).strip()
    return rendered if rendered else fallback


def join_values(values: Iterable[Any], fallback: str = "None") -> str:
    rendered = [str(value).strip() for value in values if str(value).strip()]
    return ", ".join(rendered) if rendered else fallback


def markdown_escape(value: Any) -> str:
    rendered = str(value) if value is not None else ""
    return rendered.replace("\\", "\\\\").replace("|", "\\|")


def markdown_link(label: Any, url: str) -> str:
    safe_label = str(label).replace("[", "\\[").replace("]", "\\]")
    if not url:
        return safe_label + " — Source link not supplied"
    safe_target = url.replace(" ", "%20").replace(")", "%29")
    return f"[{safe_label}]({safe_target})"


def markdown_table(headers: Sequence[str], rows: Sequence[Sequence[Any]]) -> str:
    header = "| " + " | ".join(markdown_escape(value) for value in headers) + " |"
    separator = "| " + " | ".join("---" for _ in headers) + " |"
    if not rows:
        empty = ["No reviewed records"] + [""] * (len(headers) - 1)
        rows = [empty]
    body = [
        "| " + " | ".join(markdown_escape(value) for value in row) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def evidence_reference(ids: Iterable[str]) -> str:
    values = list(ids)
    return " ".join(f"[{identifier}]" for identifier in values) if values else "No evidence cited"


def partition_evidence(
    evidence: dict[str, dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    result = {
        "a1": [],
        "a2": [],
        "a3": [],
        "a4": [],
    }
    for item in evidence.values():
        kind = item["evidence_type"]
        if kind in {"standard", "engineering_case"}:
            result["a1"].append(item)
        elif kind == "paper":
            result["a2"].append(item)
        elif kind == "patent":
            result["a3"].append(item)
        else:
            result["a4"].append(item)
    for values in result.values():
        values.sort(key=lambda item: id_number(item["id"]))
    return result


def patent_aggregate_count(
    patents: list[dict[str, Any]],
    count_unit: str,
) -> int:
    normalized = count_unit.casefold()
    if "simple" in normalized and "family" in normalized:
        keys = {
            text(item["patent"].get("simple_family_id"), item["id"])
            for item in patents
        }
        return len(keys)
    return len(patents)


def derived_counts(
    payload: dict[str, Any],
    maps: dict[str, dict[str, dict[str, Any]]],
) -> dict[str, int]:
    appendix = partition_evidence(maps["evidence"])
    return {
        "standards_and_cases": len(appendix["a1"]),
        "papers": len(appendix["a2"]),
        "patent_records": len(appendix["a3"]),
        "patent_aggregate": patent_aggregate_count(
            appendix["a3"],
            payload["meta"]["patent_count_unit"],
        ),
        "authoritative_web": len(appendix["a4"]),
        "organizations_total": len(maps["organizations"]),
        "organizations_displayed": len(maps["organizations"]),
        "searches": len(maps["search_log"]),
    }


def build_markdown(
    payload: dict[str, Any],
    maps: dict[str, dict[str, dict[str, Any]]],
) -> str:
    meta = payload["meta"]
    analysis = payload["analysis"]
    counts = derived_counts(payload, maps)
    appendix = partition_evidence(maps["evidence"])
    lines: list[str] = ["# R&D Direction Evidence Report", ""]
    if meta["project_name"].strip():
        lines.append(f"> **Project:** {meta['project_name']}")
    if meta["applicant_or_team"].strip():
        lines.append(f"> **Applicant or team:** {meta['applicant_or_team']}")
    lines.extend(
        [
            f"> **Report date:** {meta['report_date']}",
            f"> **Evidence cutoff:** {meta['evidence_cutoff']}",
            f"> **Scope:** {meta['scope']}",
            f"> **Geographies:** {join_values(meta['geographies'])}",
            f"> **Languages:** {join_values(meta['languages'])}",
            f"> **Patent count unit:** {meta['patent_count_unit']}",
            "",
            "## Source Requirement",
            "",
            *["> " + line for line in payload["requirement_text"].splitlines()],
            "",
            "## 1. Requirement Analysis",
            "",
        ]
    )
    analysis_rows = [
        [
            "Demand and operating need",
            "**Operating context:** "
            + analysis["demand"]["operating_context"]
            + " <br> **Stakeholder need:** "
            + analysis["demand"]["stakeholder_need"]
            + " <br> **Technical consequence:** "
            + analysis["demand"]["technical_consequence"]
            + " <br> **Current response:** "
            + analysis["demand"]["current_response"],
        ],
        [
            "Bottleneck",
            "**Performance limit:** "
            + analysis["bottleneck"]["performance_limit"]
            + " <br> **Evidence:** "
            + analysis["bottleneck"]["evidence"]
            + " <br> **Tradeoffs:** "
            + analysis["bottleneck"]["tradeoffs"]
            + " <br> **Mechanistic limit:** "
            + analysis["bottleneck"]["mechanistic_limit"],
        ],
        [
            "Solution hypothesis",
            "**Technical path:** "
            + analysis["solution_hypothesis"]["technical_path"]
            + " <br> **System concept:** "
            + analysis["solution_hypothesis"]["system_concept"]
            + " <br> **Compatibility:** "
            + analysis["solution_hypothesis"]["compatibility"]
            + " <br> **Target outcome:** "
            + analysis["solution_hypothesis"]["target_outcome"],
        ],
    ]
    lines.extend(
        [
            markdown_table(["Dimension", "Source-grounded analysis"], analysis_rows),
            "",
            "## 2. Technical Issue Decomposition",
            "",
        ]
    )
    issue_rows = []
    for issue in sorted(maps["issues"].values(), key=lambda item: id_number(item["id"])):
        issue_rows.append(
            [
                issue["id"],
                f"**{issue['name']}** — {issue['description']}",
                join_values(issue["source_locations"]),
                join_values(issue["dependencies"]),
                issue["confidence"],
            ]
        )
    lines.extend(
        [
            markdown_table(
                ["ID", "Technical issue", "Source locations", "Dependencies", "Confidence"],
                issue_rows,
            ),
            "",
            "### Issue-to-direction coverage",
            "",
        ]
    )
    for direction in sorted(
        maps["directions"].values(),
        key=lambda item: id_number(item["id"]),
    ):
        lines.append(
            f"- **{direction['id']} — {direction['name']}** covers "
            + join_values(direction["issue_ids"])
        )
    lines.extend(
        [
            "",
            "## 3. Proposed R&D Directions",
            "",
            "### 3.1 Evidence Summary",
            "",
            f"- Standards and engineering cases: **{counts['standards_and_cases']}**",
            f"- Papers: **{counts['papers']}**",
            f"- Patent publication records: **{counts['patent_records']}**",
            f"- Patent aggregate under `{meta['patent_count_unit']}`: **{counts['patent_aggregate']}**",
            f"- Authoritative web records: **{counts['authoritative_web']}**",
            f"- Unique normalized organizations: **{counts['organizations_total']}**",
            f"- Organizations displayed: **{counts['organizations_displayed']}**",
            f"- Search log entries: **{counts['searches']}**",
            "",
        ]
    )
    sorted_directions = sorted(
        maps["directions"].values(),
        key=lambda item: id_number(item["id"]),
    )
    for index, direction in enumerate(sorted_directions, start=2):
        lines.extend(
            [
                f"### 3.{index} {direction['id']} — {direction['name']}",
                "",
                f"**Issues addressed:** {join_values(direction['issue_ids'])}",
                "",
                f"**Rationale:** {direction['rationale']}",
                "",
                f"**Core research question:** {direction['core_question']}",
                "",
                f"**Technical target:** {direction['target']}",
                "",
                f"**Confidence:** {direction['confidence']}",
                "",
                f"**Priority basis:** {direction['priority_basis']}",
                "",
                "#### Research tasks",
                "",
            ]
        )
        task_rows = []
        for task in direction["research_tasks"]:
            task_rows.append(
                [
                    task["id"],
                    task["text"],
                    task["validation_method"],
                    task["success_metric"],
                    evidence_reference(task["evidence_ids"]),
                    task["uncertainty"],
                ]
            )
        lines.extend(
            [
                markdown_table(
                    [
                        "Task",
                        "Research activity",
                        "Validation method",
                        "Success metric",
                        "Evidence",
                        "Uncertainty",
                    ],
                    task_rows,
                ),
                "",
                "#### Representative evidence",
                "",
            ]
        )
        representative = [
            maps["evidence"][identifier]
            for identifier in direction["evidence_ids"]
        ]
        representative_rows = [
            [
                item["id"],
                item["evidence_type"],
                markdown_link(item["title"], item["source_url"]),
                item["published_date"],
                item["relevance"],
                item["review_depth"],
                item["confidence"],
            ]
            for item in representative
        ]
        lines.extend(
            [
                markdown_table(
                    ["Evidence", "Type", "Record", "Date", "Relevance", "Review depth", "Confidence"],
                    representative_rows,
                ),
                "",
                "#### Evidence gap",
                "",
                direction["evidence_gap"],
                "",
                "#### Expected deliverables",
                "",
                *[f"- {deliverable}" for deliverable in direction["deliverables"]],
                "",
            ]
        )
    lines.extend(
        [
            "### Direction Synthesis",
            "",
            markdown_table(
                ["Direction", "Issues", "Core question", "Target", "Deliverables", "Evidence", "Confidence"],
                [
                    [
                        f"{direction['id']} — {direction['name']}",
                        join_values(direction["issue_ids"]),
                        direction["core_question"],
                        direction["target"],
                        join_values(direction["deliverables"]),
                        evidence_reference(direction["evidence_ids"]),
                        direction["confidence"],
                    ]
                    for direction in sorted_directions
                ],
            ),
            "",
            "## 4. Research and Industry Organizations",
            "",
            f"The accepted evidence contains **{counts['organizations_total']}** unique normalized organizations; **{counts['organizations_displayed']}** are displayed below.",
            "",
        ]
    )
    organization_rows = []
    for organization in sorted(
        maps["organizations"].values(),
        key=lambda item: (item["name"].casefold(), item["id"]),
    ):
        organization_rows.append(
            [
                organization["name"],
                organization["organization_type"],
                join_values(organization["direction_ids"]),
                organization["focus"],
                organization["representative_outputs"],
                evidence_reference(organization["evidence_ids"]),
                organization["confidence"],
            ]
        )
    lines.extend(
        [
            markdown_table(
                ["Organization", "Type", "Directions", "Evidence-backed focus", "Representative outputs", "Evidence", "Confidence"],
                organization_rows,
            ),
            "",
            "## 5. Search Method and Coverage",
            "",
        ]
    )
    search_rows = []
    for search in sorted(
        maps["search_log"].values(),
        key=lambda item: id_number(item["id"]),
    ):
        search_rows.append(
            [
                search["id"],
                search["direction_id"],
                search["evidence_type"],
                search["source_or_tool"],
                search["query"],
                json.dumps(search["filters"], ensure_ascii=False, sort_keys=True),
                search["requested_limit"],
                search["returned_count"],
                len(search["reviewed_evidence_ids"]),
                search["deduplication"],
                search["limitations"],
            ]
        )
    lines.extend(
        [
            markdown_table(
                [
                    "Search ID",
                    "Direction",
                    "Evidence type",
                    "Source/tool",
                    "Query",
                    "Filters",
                    "Requested",
                    "Returned",
                    "Reviewed",
                    "Deduplication",
                    "Limits",
                ],
                search_rows,
            ),
            "",
            "## 6. Limitations and Specialist Review",
            "",
            *[f"- {limitation}" for limitation in payload["limitations"]],
            f"- **Review boundary:** {payload['review']['legal_boundary']}",
            "",
            "## 7. Appendices",
            "",
            "### A1. Standards and Engineering Cases",
            "",
            build_a1_markdown(appendix["a1"]),
            "",
            "### A2. Scientific and Technical Papers",
            "",
            build_a2_markdown(appendix["a2"]),
            "",
            "### A3. Patent Evidence",
            "",
            build_a3_markdown(appendix["a3"]),
            "",
            "### A4. Authoritative Web Evidence",
            "",
            build_a4_markdown(appendix["a4"]),
            "",
            "## Complete Source Register",
            "",
            build_source_register_markdown(maps["evidence"]),
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def build_a1_markdown(items: list[dict[str, Any]]) -> str:
    rows = []
    for item in items:
        subtype = item["standard_or_case"]
        rows.append(
            [
                item["id"],
                item["evidence_type"],
                item["published_date"],
                subtype["publisher"],
                markdown_link(item["title"], item["source_url"]),
                subtype["status_or_stage"] + "; " + subtype["location_or_system"],
                item["summary"],
                join_values(item["direction_ids"]),
                item["review_status"],
            ]
        )
    return markdown_table(
        ["Evidence", "Type", "Date", "Publisher", "Document/project", "Context/status", "Summary", "Directions", "Review"],
        rows,
    )


def build_a2_markdown(items: list[dict[str, Any]]) -> str:
    rows = []
    for item in items:
        subtype = item["paper"]
        cited = subtype["cited_by"]
        rows.append(
            [
                item["id"],
                item["published_date"],
                join_values(subtype["authors"]) + " / " + join_values(subtype["affiliations"]),
                markdown_link(item["title"], item["source_url"]),
                subtype["venue"] + ("; DOI " + subtype["doi"] if subtype["doi"] else ""),
                "Not supplied" if cited is None else str(cited),
                join_values(item["direction_ids"]),
                item["review_status"],
            ]
        )
    return markdown_table(
        ["Evidence", "Date", "Authors/affiliations", "Title", "Venue/DOI", "Citation count", "Directions", "Review"],
        rows,
    )


def build_a3_markdown(items: list[dict[str, Any]]) -> str:
    rows = []
    for item in items:
        subtype = item["patent"]
        status = subtype["legal_status"] or "Not supplied"
        if subtype["legal_status_as_of"]:
            status += " as of " + subtype["legal_status_as_of"]
        rows.append(
            [
                item["id"],
                markdown_link(subtype["publication_number"], item["source_url"]),
                item["title"],
                join_values(subtype["applicants"]) + " / " + join_values(subtype["assignees"]),
                text(subtype["earliest_priority_date"]) + " / " + subtype["publication_date"],
                text(subtype["simple_family_id"]),
                status,
                join_values(item["direction_ids"]),
                item["review_depth"],
            ]
        )
    return markdown_table(
        ["Evidence", "Publication", "Title", "Applicants/assignees", "Priority/publication", "Family", "Legal status", "Directions", "Review depth"],
        rows,
    )


def build_a4_markdown(items: list[dict[str, Any]]) -> str:
    rows = []
    for item in items:
        subtype = item["web"]
        rows.append(
            [
                item["id"],
                item["published_date"],
                item["source_name"] + "; " + subtype["publisher_type"] + "; " + subtype["content_category"],
                markdown_link(item["title"], item["source_url"]),
                item["summary"],
                join_values(item["direction_ids"]),
                item["review_status"],
            ]
        )
    return markdown_table(
        ["Evidence", "Date", "Publisher/type", "Title", "Summary", "Directions", "Review"],
        rows,
    )


def build_source_register_markdown(evidence: dict[str, dict[str, Any]]) -> str:
    rows = []
    for item in sorted(evidence.values(), key=lambda value: id_number(value["id"])):
        rows.append(
            [
                item["id"],
                item["evidence_type"],
                markdown_link(item["title"], item["source_url"]),
                item["source_name"],
                item["published_date"],
                item["review_depth"],
                item["review_status"],
                item["confidence"],
            ]
        )
    return markdown_table(
        ["Evidence", "Type", "Record", "Source", "Date", "Review depth", "Review status", "Confidence"],
        rows,
    )


def h(value: Any) -> str:
    """Escape untrusted report content for an HTML text or attribute context."""
    return html.escape(str(value) if value is not None else "", quote=True)


def html_link(label: Any, url: str) -> str:
    if not url:
        return h(label) + ' <span class="muted">(source link not supplied)</span>'
    return (
        f'<a href="{h(url)}" target="_blank" rel="noopener noreferrer">'
        f'{h(label)}</a>'
    )


def html_list(values: Iterable[Any], *, ordered: bool = False) -> str:
    items = list(values)
    if not items:
        return '<p class="empty">No reviewed records.</p>'
    tag = "ol" if ordered else "ul"
    body = "".join(f"<li>{h(value)}</li>" for value in items)
    return f"<{tag}>{body}</{tag}>"


def html_table(headers: Sequence[str], rows: Sequence[Sequence[Any]]) -> str:
    head = "".join(f'<th scope="col">{h(item)}</th>' for item in headers)
    if rows:
        body = "".join(
            "<tr>" + "".join(f"<td>{value}</td>" for value in row) + "</tr>"
            for row in rows
        )
    else:
        body = f'<tr><td colspan="{len(headers)}" class="empty">No reviewed records.</td></tr>'
    return (
        '<div class="table-wrap"><table><thead><tr>' + head
        + "</tr></thead><tbody>" + body + "</tbody></table></div>"
    )


def badge(value: Any, kind: str = "neutral") -> str:
    return f'<span class="badge badge-{h(kind)}">{h(value)}</span>'


def evidence_chips(ids: Iterable[str]) -> str:
    values = list(ids)
    if not values:
        return '<span class="muted">No evidence cited</span>'
    return " ".join(badge(identifier, "evidence") for identifier in values)


def metric_card(label: str, value: Any, note: str) -> str:
    return (
        '<article class="metric">'
        f'<p class="metric-label">{h(label)}</p>'
        f'<p class="metric-value">{h(value)}</p>'
        f'<p class="metric-note">{h(note)}</p>'
        '</article>'
    )


def render_analysis_html(analysis: dict[str, Any]) -> str:
    groups = (
        ("Demand and operating need", analysis["demand"]),
        ("Bottleneck", analysis["bottleneck"]),
        ("Solution hypothesis", analysis["solution_hypothesis"]),
    )
    cards = []
    for title, values in groups:
        rows = "".join(
            '<div class="definition-row">'
            f'<dt>{h(key.replace("_", " ").title())}</dt>'
            f'<dd>{h(value)}</dd></div>'
            for key, value in values.items()
        )
        cards.append(
            f'<article class="analysis-card"><h3>{h(title)}</h3><dl>{rows}</dl></article>'
        )
    return '<div class="analysis-grid">' + "".join(cards) + "</div>"


def render_direction_html(
    direction: dict[str, Any],
    evidence: dict[str, dict[str, Any]],
) -> str:
    tasks = html_table(
        ["Task", "Research activity", "Validation", "Success metric", "Evidence", "Uncertainty"],
        [
            [
                h(task["id"]),
                h(task["text"]),
                h(task["validation_method"]),
                h(task["success_metric"]),
                evidence_chips(task["evidence_ids"]),
                h(task["uncertainty"]),
            ]
            for task in direction["research_tasks"]
        ],
    )
    records = html_table(
        ["Evidence", "Type", "Record", "Date", "Relevance", "Review", "Confidence"],
        [
            [
                badge(item["id"], "evidence"),
                h(item["evidence_type"]),
                html_link(item["title"], item["source_url"]),
                h(item["published_date"]),
                h(item["relevance"]),
                h(item["review_depth"]),
                badge(item["confidence"], item["confidence"]),
            ]
            for item in (evidence[identifier] for identifier in direction["evidence_ids"])
        ],
    )
    return f"""
    <article class="direction-card" id="{h(direction['id'])}">
      <header class="direction-header">
        <div><p class="eyebrow">R&amp;D direction {h(direction['id'])}</p><h3>{h(direction['name'])}</h3></div>
        {badge(direction['confidence'] + ' confidence', direction['confidence'])}
      </header>
      <div class="direction-meta">
        <p><strong>Issues addressed</strong><br>{' '.join(badge(x, 'issue') for x in direction['issue_ids'])}</p>
        <p><strong>Priority basis</strong><br>{h(direction['priority_basis'])}</p>
      </div>
      <div class="callout"><strong>Core research question</strong><p>{h(direction['core_question'])}</p></div>
      <p><strong>Rationale.</strong> {h(direction['rationale'])}</p>
      <p><strong>Technical target.</strong> {h(direction['target'])}</p>
      <h4>Research tasks</h4>{tasks}
      <h4>Representative evidence</h4>{records}
      <div class="gap"><strong>Evidence gap</strong><p>{h(direction['evidence_gap'])}</p></div>
      <h4>Expected deliverables</h4>{html_list(direction['deliverables'])}
    </article>"""


def render_appendix_html(
    partitions: dict[str, list[dict[str, Any]]],
    evidence: dict[str, dict[str, Any]],
) -> str:
    a1 = html_table(
        ["Evidence", "Type", "Record", "Date", "Organization", "Status", "Directions", "Review"],
        [
            [
                badge(x["id"], "evidence"),
                h(x["evidence_type"]),
                html_link(x["title"], x["source_url"]),
                h(x["published_date"]),
                h(x["standard_or_case"]["publisher"]),
                h(
                    x["standard_or_case"]["status_or_stage"]
                    + "; "
                    + x["standard_or_case"]["location_or_system"]
                ),
                h(join_values(x["direction_ids"])),
                h(x["review_status"]),
            ]
            for x in partitions["a1"]
        ],
    )
    a2 = html_table(
        ["Evidence", "Date", "Venue", "Paper", "Publication type", "Peer review", "Directions", "Review"],
        [
            [
                badge(x["id"], "evidence"),
                h(x["published_date"]),
                h(x["paper"]["venue"]),
                html_link(x["title"], x["source_url"]),
                h(x["paper"]["publication_type"]),
                h(x["paper"]["peer_review_status"]),
                h(join_values(x["direction_ids"])),
                h(x["review_status"]),
            ]
            for x in partitions["a2"]
        ],
    )
    a3 = html_table(
        ["Evidence", "Publication", "Family", "Title", "Priority", "Applicant", "Status", "Directions", "Review"],
        [
            [
                badge(x["id"], "evidence"),
                h(x["patent"]["publication_number"]),
                h(x["patent"]["simple_family_id"]),
                html_link(x["title"], x["source_url"]),
                h(x["patent"]["earliest_priority_date"]),
                h(join_values(x["patent"]["applicants"])),
                h(x["patent"]["legal_status"]),
                h(join_values(x["direction_ids"])),
                h(x["review_status"]),
            ]
            for x in partitions["a3"]
        ],
    )
    a4 = html_table(
        ["Evidence", "Date", "Publisher/type", "Title", "Summary", "Directions", "Review"],
        [
            [
                badge(x["id"], "evidence"),
                h(x["published_date"]),
                h(
                    x["source_name"]
                    + "; "
                    + x["web"]["publisher_type"]
                    + "; "
                    + x["web"]["content_category"]
                ),
                html_link(x["title"], x["source_url"]),
                h(x["summary"]),
                h(join_values(x["direction_ids"])),
                h(x["review_status"]),
            ]
            for x in partitions["a4"]
        ],
    )
    register = html_table(
        ["Evidence", "Type", "Record", "Source", "Date", "Review depth", "Review status", "Confidence"],
        [
            [
                badge(x["id"], "evidence"),
                h(x["evidence_type"]),
                html_link(x["title"], x["source_url"]),
                h(x["source_name"]),
                h(x["published_date"]),
                h(x["review_depth"]),
                h(x["review_status"]),
                badge(x["confidence"], x["confidence"]),
            ]
            for x in sorted(
                evidence.values(),
                key=lambda item: id_number(item["id"]),
            )
        ],
    )
    return f"""
      <details open><summary>A1. Standards and engineering cases</summary>{a1}</details>
      <details open><summary>A2. Scientific and technical papers</summary>{a2}</details>
      <details open><summary>A3. Patent evidence</summary>{a3}</details>
      <details open><summary>A4. Authoritative web evidence</summary>{a4}</details>
      <h3>Complete source register</h3>{register}
    """


def build_html(
    payload: dict[str, Any],
    maps: dict[str, dict[str, dict[str, Any]]],
) -> str:
    meta = payload["meta"]
    counts = derived_counts(payload, maps)
    partitions = partition_evidence(maps["evidence"])
    issue_rows = [[badge(x["id"], "issue"), h(x["name"]), h(x["description"]), h(join_values(x["source_locations"])), h(join_values(x["dependencies"])), badge(x["confidence"], x["confidence"])] for x in sorted(maps["issues"].values(), key=lambda item: id_number(item["id"]))]
    organization_rows = [[h(x["name"]), h(x["organization_type"]), h(join_values(x["direction_ids"])), h(x["focus"]), h(x["representative_outputs"]), evidence_chips(x["evidence_ids"]), badge(x["confidence"], x["confidence"])] for x in sorted(maps["organizations"].values(), key=lambda item: (item["name"].casefold(), item["id"]))]
    search_rows = [[badge(x["id"]), h(x["direction_id"]), h(x["evidence_type"]), h(x["source_or_tool"]), f'<code>{h(x["query"])}</code>', f'<code>{h(json.dumps(x["filters"], ensure_ascii=False, sort_keys=True))}</code>', h(x["requested_limit"]), h(x["returned_count"]), h(len(x["reviewed_evidence_ids"])), h(x["deduplication"]), h(x["limitations"])] for x in sorted(maps["search_log"].values(), key=lambda item: id_number(item["id"]))]
    directions = "".join(render_direction_html(x, maps["evidence"]) for x in sorted(maps["directions"].values(), key=lambda item: id_number(item["id"])))
    metrics = "".join((
        metric_card("Directions", len(maps["directions"]), "Reviewed R&D paths"),
        metric_card("Evidence records", len(maps["evidence"]), "Accepted into the source register"),
        metric_card("Patent aggregate", counts["patent_aggregate"], meta["patent_count_unit"]),
        metric_card("Organizations", counts["organizations_total"], "Unique normalized entities"),
    ))
    project = meta["project_name"].strip() or "R&D Direction Evidence Report"
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{h(project)} | R&amp;D Direction Evidence Report</title>
<style>
:root{{--ink:#17202a;
--muted:#5d6875;
--paper:#fff;
--canvas:#edf1f4;
--line:#ccd5dc;
--accent:#075985;
--accent-soft:#e0f2fe;
--navy:#0f2d3d;
--green:#166534;
--amber:#92400e;
--red:#991b1b;
--radius:8px;
--shadow:0 8px 24px rgba(15,45,61,.08)}}

*{{box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{margin:0;
background:var(--canvas);
color:var(--ink);
font:15px/1.65 Inter,Arial,"Helvetica Neue",sans-serif}}
a{{color:var(--accent);
text-underline-offset:2px}}
a:hover{{text-decoration-thickness:2px}}
header.hero{{background:var(--navy);
color:#fff;
border-bottom:5px solid #38bdf8}}
.hero-inner{{max-width:1200px;
margin:auto;
padding:56px 28px 44px}}
.kicker,.eyebrow{{font-size:.74rem;
font-weight:800;
letter-spacing:.12em;
text-transform:uppercase}}
.kicker{{color:#7dd3fc}}
h1{{max-width:900px;
margin:.25rem 0 1rem;
font:700 clamp(2rem,4vw,3.5rem)/1.08 Georgia,"Times New Roman",serif}}
.subtitle{{max-width:850px;
color:#d8e5eb;
font-size:1.05rem}}
.meta-line{{display:flex;
flex-wrap:wrap;
gap:8px 20px;
margin-top:24px;
color:#bcd0da;
font-size:.86rem}}
main{{max-width:1200px;
margin:auto;
padding:28px}}
nav.toc{{background:#fff;
border:1px solid var(--line);
border-radius:var(--radius);
padding:14px 20px;
box-shadow:var(--shadow)}}
nav.toc a{{display:inline-block;
margin:4px 18px 4px 0;
font-weight:700;
text-decoration:none}}
section{{background:var(--paper);
margin:24px 0;
padding:28px;
border:1px solid var(--line);
border-radius:var(--radius);
box-shadow:var(--shadow)}}
h2{{margin:0 0 20px;
padding-bottom:10px;
border-bottom:2px solid var(--navy);
font:700 1.65rem/1.2 Georgia,"Times New Roman",serif}}
h3{{font:700 1.22rem/1.3 Georgia,"Times New Roman",serif}}
h4{{margin-top:25px}}
.metrics{{display:grid;
grid-template-columns:repeat(4,minmax(0,1fr));
gap:12px;
margin:20px 0}}
.metric{{border:1px solid var(--line);
border-top:4px solid var(--accent);
padding:15px;
background:#f8fafc}}
.metric p{{margin:0}}
.metric-label{{color:var(--muted);
font-weight:700;
text-transform:uppercase;
font-size:.7rem;
letter-spacing:.08em}}
.metric-value{{font:700 1.8rem/1.2 Georgia,serif}}
.metric-note{{color:var(--muted);
font-size:.78rem}}
.analysis-grid{{display:grid;
grid-template-columns:repeat(3,minmax(0,1fr));
gap:16px}}
.analysis-card{{border-left:4px solid var(--accent);
background:#f8fafc;
padding:18px}}
dl{{margin:0}}
.definition-row{{padding:8px 0;
border-top:1px solid var(--line)}}
dt{{font-weight:800;
text-transform:capitalize}}
dd{{margin:2px 0;
color:#334155}}
.table-wrap{{overflow-x:auto;
margin:14px 0 22px}}
table{{width:100%;
border-collapse:collapse;
font-size:.82rem}}
th{{background:var(--navy);
color:#fff;
text-align:left}}
th,td{{padding:10px;
border:1px solid var(--line);
vertical-align:top}}
tbody tr:nth-child(even){{background:#f5f7f9}}
.badge{{display:inline-block;
margin:1px;
padding:2px 7px;
border:1px solid #9aa7b1;
border-radius:999px;
background:#f1f5f9;
font-size:.72rem;
font-weight:800;
white-space:nowrap}}
.badge-evidence{{background:var(--accent-soft);
border-color:#7dd3fc;
color:#075985}}
.badge-issue{{background:#f3e8ff;
border-color:#c4b5fd;
color:#6b21a8}}
.badge-high{{background:#dcfce7;
border-color:#86efac;
color:var(--green)}}
.badge-medium{{background:#fef3c7;
border-color:#fcd34d;
color:var(--amber)}}
.badge-low{{background:#fee2e2;
border-color:#fca5a5;
color:var(--red)}}
.direction-card{{margin:24px 0;
padding:24px;
border:1px solid var(--line);
border-left:6px solid var(--accent);
border-radius:var(--radius)}}
.direction-header{{display:flex;
justify-content:space-between;
align-items:flex-start;
gap:20px}}
.direction-header h3{{margin:2px 0;
font-size:1.5rem}}
.eyebrow{{margin:0;
color:var(--accent)}}
.direction-meta{{display:grid;
grid-template-columns:1fr 2fr;
gap:20px}}
.callout,.gap{{margin:18px 0;
padding:16px;
border-left:4px solid #38bdf8;
background:#f0f9ff}}
.gap{{border-color:#f59e0b;
background:#fffbeb}}
.callout p,.gap p{{margin:.25rem 0}}
blockquote{{margin:0;
padding:18px 22px;
background:#f8fafc;
border-left:4px solid var(--accent);
white-space:pre-wrap}}
code{{font:12px/1.45 Consolas,"SFMono-Regular",monospace;
overflow-wrap:anywhere}}
details{{border:1px solid var(--line);
margin:14px 0;
padding:0 16px}}
summary{{cursor:pointer;
font-weight:800;
padding:14px 0}}
ul,ol{{padding-left:22px}}
.empty,.muted{{color:var(--muted);
font-style:italic}}
footer{{max-width:1200px;
margin:auto;
padding:8px 28px 40px;
color:var(--muted);
font-size:.8rem}}
@media(max-width:850px){{.metrics,.analysis-grid{{grid-template-columns:1fr 1fr}}
.direction-meta{{grid-template-columns:1fr}}
}}
@media(max-width:560px){{main,.hero-inner{{padding-left:16px;
padding-right:16px}}
section{{padding:18px}}
.metrics,.analysis-grid{{grid-template-columns:1fr}}
}}
@media print{{body{{background:#fff;
font-size:10pt}}
nav.toc{{display:none}}
section{{box-shadow:none;
break-inside:avoid;
margin:12px 0}}
a{{color:inherit;
text-decoration:none}}
}}

</style>
</head>
<body>
<header class="hero">
<div class="hero-inner">
<p class="kicker">Evidence-backed decision support</p>
<h1>{h(project)}</h1>
<p class="subtitle">Structured R&amp;D direction assessment linking source requirements, technical issues, research tasks, patents, papers, standards, engineering cases, and reviewed web evidence.</p>
<div class="meta-line">
<span>Report date: {h(meta['report_date'])}</span>
<span>Evidence cutoff: {h(meta['evidence_cutoff'])}</span>
<span>Geographies: {h(join_values(meta['geographies']))}</span>
<span>Patent unit: {h(meta['patent_count_unit'])}</span>
</div>
</div>
</header>
<main>
<nav class="toc" aria-label="Report sections">
<a href="#requirement">Requirement</a>
<a href="#analysis">Analysis</a>
<a href="#issues">Issues</a>
<a href="#directions">Directions</a>
<a href="#organizations">Organizations</a>
<a href="#method">Method</a>
<a href="#appendices">Appendices</a>
</nav>
<section id="requirement">
<h2>Source Requirement</h2>
<blockquote>{h(payload['requirement_text'])}</blockquote>
</section>
<section id="analysis">
<h2>1. Requirement Analysis</h2>{render_analysis_html(payload['analysis'])}</section>
<section id="issues">
<h2>2. Technical Issue Decomposition</h2>{html_table(['ID','Issue','Description','Source locations','Dependencies','Confidence'], issue_rows)}</section>
<section id="directions">
<h2>3. Proposed R&amp;D Directions</h2>
<div class="metrics">{metrics}</div>{directions}</section>
<section id="organizations">
<h2>4. Research and Industry Organizations</h2>
<p>The accepted evidence contains <strong>{counts['organizations_total']}</strong> unique normalized organizations; <strong>{counts['organizations_displayed']}</strong> are displayed.</p>{html_table(['Organization','Type','Directions','Evidence-backed focus','Representative outputs','Evidence','Confidence'], organization_rows)}</section>
<section id="method">
<h2>5. Search Method and Coverage</h2>{html_table(['Search ID','Direction','Evidence type','Source/tool','Query','Filters','Requested','Returned','Reviewed','Deduplication','Limits'], search_rows)}</section>
<section id="limitations">
<h2>6. Limitations and Specialist Review</h2>{html_list(payload['limitations'])}<div class="callout">
<strong>Review boundary</strong>
<p>{h(payload['review']['legal_boundary'])}</p>
<p>Analyst: {h(payload['review']['analyst'])} | Reviewer: {h(payload['review']['reviewer'])} | Reviewed: {h(payload['review']['reviewed_on'])}</p>
</div>
</section>
<section id="appendices">
<h2>7. Appendices</h2>{render_appendix_html(partitions, maps['evidence'])}</section>
</main>
<footer>Generated from strict schema version {h(payload['schema_version'])}. Counts are derived from the validated evidence registry.</footer>
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


def ensure_distinct_outputs(html_path: Path, markdown_path: Path | None) -> None:
    if markdown_path is not None and html_path.resolve() == markdown_path.resolve():
        fail("--output and --markdown-output must be different files")


def require_rendered_fragment(document: str, fragment: str, path: str) -> None:
    if fragment not in document:
        fail(f"Rendered {path} is missing required content: {fragment!r}")


def validate_rendered_markdown(
    document: str,
    payload: dict[str, Any],
    maps: dict[str, dict[str, dict[str, Any]]],
) -> None:
    """Confirm the Markdown artifact retained every accepted registry record."""
    required_sections = (
        "# R&D Direction Evidence Report",
        "## Source Requirement",
        "## 1. Requirement Analysis",
        "## 2. Technical Issue Decomposition",
        "## 3. Proposed R&D Directions",
        "## 4. Research and Industry Organizations",
        "## 5. Search Method and Coverage",
        "## 6. Limitations and Specialist Review",
        "## 7. Appendices",
        "### A1. Standards and Engineering Cases",
        "### A2. Scientific and Technical Papers",
        "### A3. Patent Evidence",
        "### A4. Authoritative Web Evidence",
        "## Complete Source Register",
    )
    for section in required_sections:
        require_rendered_fragment(document, section, "Markdown")

    require_rendered_fragment(
        document,
        payload["requirement_text"],
        "Markdown source requirement",
    )
    for issue in maps["issues"].values():
        require_rendered_fragment(document, issue["id"], "Markdown issue registry")
        require_rendered_fragment(document, issue["name"], "Markdown issue registry")
    for direction in maps["directions"].values():
        require_rendered_fragment(document, direction["id"], "Markdown direction registry")
        require_rendered_fragment(document, direction["name"], "Markdown direction registry")
        for task in direction["research_tasks"]:
            require_rendered_fragment(document, task["id"], "Markdown task registry")
    for evidence in maps["evidence"].values():
        require_rendered_fragment(document, evidence["id"], "Markdown evidence registry")
        require_rendered_fragment(document, evidence["title"], "Markdown evidence registry")
    for organization in maps["organizations"].values():
        require_rendered_fragment(
            document,
            organization["name"],
            "Markdown organization registry",
        )
    for search in maps["search_log"].values():
        require_rendered_fragment(document, search["id"], "Markdown search log")


def validate_rendered_html(
    document: str,
    payload: dict[str, Any],
    maps: dict[str, dict[str, dict[str, Any]]],
) -> None:
    """Apply deterministic safety and completeness gates to self-contained HTML."""
    lowered = document.casefold()
    forbidden_fragments = (
        "<script",
        "javascript:",
        "data:text/html",
        " onerror=",
        " onload=",
        "document.write",
        "innerhtml",
        "outerhtml",
        "insertadjacenthtml",
        "linear-gradient",
        "radial-gradient",
        "conic-gradient",
        "@import",
    )
    for fragment in forbidden_fragments:
        if fragment in lowered:
            fail(f"Rendered HTML contains forbidden fragment: {fragment!r}")

    required_landmarks = (
        '<html lang="en">',
        '<meta charset="utf-8">',
        'aria-label="Report sections"',
        'id="requirement"',
        'id="analysis"',
        'id="issues"',
        'id="directions"',
        'id="organizations"',
        'id="method"',
        'id="limitations"',
        'id="appendices"',
        "Complete source register",
    )
    for landmark in required_landmarks:
        require_rendered_fragment(document, landmark, "HTML")

    project = payload["meta"]["project_name"].strip()
    if project:
        require_rendered_fragment(document, h(project), "HTML title")
    require_rendered_fragment(
        document,
        h(payload["requirement_text"]),
        "HTML source requirement",
    )

    for direction in maps["directions"].values():
        require_rendered_fragment(
            document,
            f'id="{h(direction["id"])}"',
            "HTML direction anchor",
        )
        require_rendered_fragment(document, h(direction["name"]), "HTML direction")
        for task in direction["research_tasks"]:
            require_rendered_fragment(document, h(task["id"]), "HTML task registry")

    for evidence in maps["evidence"].values():
        require_rendered_fragment(document, h(evidence["id"]), "HTML evidence registry")
        require_rendered_fragment(document, h(evidence["title"]), "HTML evidence registry")
        if evidence["source_url"]:
            require_rendered_fragment(
                document,
                f'href="{h(evidence["source_url"])}"',
                "HTML source link",
            )

    for organization in maps["organizations"].values():
        require_rendered_fragment(
            document,
            h(organization["name"]),
            "HTML organization registry",
        )
    for search in maps["search_log"].values():
        require_rendered_fragment(document, h(search["id"]), "HTML search log")

    # The page must remain portable: every dependency is embedded, and every
    # outbound evidence link is explicit in the reviewed payload.
    external_runtime_markers = (
        'src="http://',
        'src="https://',
        'href="//',
    )
    for marker in external_runtime_markers:
        if marker in lowered:
            fail(f"Rendered HTML contains an external runtime dependency: {marker!r}")

    counts = derived_counts(payload, maps)
    for label, value in (
        ("Directions", len(maps["directions"])),
        ("Evidence records", len(maps["evidence"])),
        ("Patent aggregate", counts["patent_aggregate"]),
        ("Organizations", counts["organizations_total"]),
    ):
        require_rendered_fragment(document, h(label), "HTML metric label")
        require_rendered_fragment(document, h(value), "HTML metric value")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    ensure_distinct_outputs(args.output, args.markdown_output)
    payload = load_payload(args.payload)
    maps = validate_payload(payload)
    html_report = build_html(payload, maps)
    markdown_report = build_markdown(payload, maps)
    validate_rendered_html(html_report, payload, maps)
    validate_rendered_markdown(markdown_report, payload, maps)
    write_output(args.output, html_report, args.overwrite)
    if args.markdown_output is not None:
        write_output(args.markdown_output, markdown_report, args.overwrite)
    print(f"Rendered HTML report: {args.output}")
    if args.markdown_output is not None:
        print(f"Rendered Markdown report: {args.markdown_output}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ReportError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)

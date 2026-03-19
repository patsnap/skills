#!/usr/bin/env python3
"""
Unified QFD pipeline entrypoint for the qfd-analysis skill.

This script orchestrates:
workspace -> VOC -> weights -> HOQ -> benchmark(optional) -> report
and returns one structured JSON payload to stdout.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from benchmark_analyzer import analyze_gaps, build_benchmark_table
from hoq_builder import (
    build_correlation_matrix,
    build_relationship_matrix,
    identify_conflicts,
)
from report_generator import (
    generate_hoq_excel,
    generate_markdown_report,
    generate_priority_recommendations,
)
from voc_processor import OTHER_CATEGORY_ALIASES, is_low_signal_description, process_voc_file

WORKSPACE_SUBDIRS = [
    "01_voc",
    "02_technical",
    "02_technical/manuals",
    "03_analysis",
    "04_benchmark",
    "05_output",
]

LOW_SIGNAL_LABELS = {"fan", "ace", "for travel", "noise", "weight"}
DEFAULT_MODEL_SOURCE = "python:local"
TOKEN_ALIASES: Dict[str, Tuple[str, ...]] = {
    "battery": ("power", "runtime", "charge", "\u7eed\u822a", "\u7535\u6c60"),
    "runtime": ("battery", "power", "batterylife", "\u7eed\u822a"),
    "charge": ("battery", "runtime", "charging", "\u5145\u7535"),
    "noise": ("quiet", "fan", "sound", "\u566a\u97f3"),
    "quiet": ("noise", "silent", "sound", "\u5b89\u9759"),
    "portable": ("travel", "carry", "lightweight", "\u4fbf\u643a"),
    "travel": ("portable", "carry", "weight", "\u4fbf\u643a"),
    "weight": ("portable", "travel", "lightweight", "\u91cd\u91cf"),
    "display": ("screen", "brightness", "\u663e\u793a", "\u5c4f\u5e55"),
    "screen": ("display", "brightness", "\u5c4f\u5e55", "\u663e\u793a"),
    "connectivity": ("wireless", "signal", "bluetooth", "\u8fde\u63a5"),
    "bluetooth": ("wireless", "connectivity", "signal", "\u84dd\u7259"),
}
RUNTIME_CONTEXT: Dict[str, Any] = {
    "stage": "bootstrap",
    "workspace_path": None,
    "files_written": [],
    "warnings": [],
}
RESULT_FILE_LAYOUT: List[Tuple[str, Path]] = [
    ("project_meta_json", Path("project_meta.json")),
    ("requirements_json", Path("01_voc/requirements.json")),
    ("cluster_diagnostics_json", Path("01_voc/cluster_diagnostics.json")),
    ("llm_merge_trace_json", Path("01_voc/llm_merge_trace.json")),
    ("our_product_spec_json", Path("02_technical/our_product_spec.json")),
    ("relationship_matrix_json", Path("03_analysis/relationship_matrix.json")),
    ("correlation_matrix_json", Path("03_analysis/correlation_matrix.json")),
    ("conflicts_json", Path("03_analysis/conflicts.json")),
    ("benchmark_table_json", Path("04_benchmark/benchmark_table.json")),
    ("gap_analysis_json", Path("04_benchmark/gap_analysis.json")),
    ("priority_recommendations_json", Path("05_output/priority_recommendations.json")),
    ("qfd_report_md", Path("05_output/qfd_report.md")),
    ("hoq_matrix_xlsx", Path("05_output/hoq_matrix.xlsx")),
]


def set_runtime_stage(stage: str) -> None:
    RUNTIME_CONTEXT["stage"] = stage


def set_runtime_workspace(workspace: Path) -> None:
    RUNTIME_CONTEXT["workspace_path"] = str(workspace)


def sync_runtime_state(files_written: List[str], warnings: List[str]) -> None:
    RUNTIME_CONTEXT["files_written"] = list(dict.fromkeys(files_written))
    RUNTIME_CONTEXT["warnings"] = list(dict.fromkeys(warnings))


def current_workspace() -> Optional[Path]:
    workspace_path = RUNTIME_CONTEXT.get("workspace_path")
    if not workspace_path:
        return None
    return Path(str(workspace_path))


def build_result_files_map(workspace: Optional[Path]) -> Dict[str, str]:
    if workspace is None:
        return {}
    result_files: Dict[str, str] = {}
    for key, relative_path in RESULT_FILE_LAYOUT:
        absolute_path = workspace / relative_path
        if absolute_path.exists():
            result_files[key] = str(absolute_path)
    return result_files


def build_quick_access(result_files: Dict[str, str]) -> Dict[str, str]:
    quick_access: Dict[str, str] = {}
    for target_key, source_key in [
        ("primary_report", "qfd_report_md"),
        ("priority_recommendations", "priority_recommendations_json"),
        ("conflicts", "conflicts_json"),
    ]:
        if source_key in result_files:
            quick_access[target_key] = result_files[source_key]
    return quick_access


def build_read_guide() -> List[str]:
    return [
        "Read qfd_report_md first for the narrative summary and recommendations.",
        "Read priority_recommendations_json to verify ranking and action order.",
        "Read conflicts_json before explaining trade-offs or technical tensions.",
    ]


def default_failure_next_actions() -> List[str]:
    return [
        "Inspect error_code, message, and details before retrying.",
        "If missing_inputs is present, ask the user for those files instead of rerunning immediately.",
    ]


def missing_input(
    name: str,
    kind: str,
    reason: str,
    suggested_flag: str,
    expected_schema: Optional[str] = None,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "name": name,
        "kind": kind,
        "reason": reason,
        "suggested_flag": suggested_flag,
    }
    if expected_schema:
        payload["expected_schema"] = expected_schema
    return payload


def now_iso() -> str:
    return datetime.now().isoformat()


def abs_path(path_text: str, base: Path) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return (base / path).resolve()


def read_json(path: Path) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def read_json_input(
    path: Path,
    *,
    input_name: str,
    suggested_flag: str,
    input_kind: str = "json",
    expected_schema: Optional[str] = None,
    stage: Optional[str] = None,
    next_action: Optional[str] = None,
    next_actions: Optional[List[str]] = None,
    reason: Optional[str] = None,
    retryable: bool = True,
) -> Any:
    try:
        return read_json(path)
    except json.JSONDecodeError as exc:
        details = {
            "path": str(path),
            "line": exc.lineno,
            "column": exc.colno,
            "message": exc.msg,
        }
        if expected_schema:
            details["expected_schema"] = expected_schema
        fail(
            "QFD_VALIDATION_ERROR",
            f"{input_name} contains invalid JSON: {path}",
            details=details,
            stage=stage,
            retryable=retryable,
            next_action=next_action or f"ask_user_for_corrected_{input_name}",
            next_actions=next_actions,
            missing_inputs=[
                missing_input(
                    input_name,
                    input_kind,
                    reason or f"{input_name} must be valid JSON",
                    suggested_flag,
                    expected_schema,
                )
            ],
        )
    except OSError as exc:
        fail(
            "QFD_RUNTIME_ERROR",
            f"failed to read {input_name}: {path}",
            details={"path": str(path), "message": str(exc), "type": type(exc).__name__},
            stage=stage,
            retryable=retryable,
            next_action=next_action or f"inspect_{input_name}_path_and_retry",
            next_actions=next_actions,
        )


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def is_cjk(ch: str) -> bool:
    return ("\u4e00" <= ch <= "\u9fff") or ("\u3040" <= ch <= "\u30ff")


def is_low_signal_label(text: str) -> bool:
    trimmed = text.strip()
    if not trimmed:
        return True
    if is_low_signal_description(trimmed):
        return True
    lower = trimmed.lower()
    if lower in LOW_SIGNAL_LABELS:
        return True

    cjk_count = sum(1 for ch in trimmed if is_cjk(ch))
    if cjk_count > 0:
        return cjk_count < 2

    words = re.findall(r"[a-zA-Z0-9]+", trimmed)
    informative = sum(1 for ch in trimmed if ch.isalnum())
    if len(words) <= 1:
        return True
    return informative < 4


def normalize_relationship_token(token: str) -> str:
    token = token.strip().lower()
    if not token:
        return ""
    if token.endswith("ies") and len(token) > 4:
        token = token[:-3] + "y"
    elif token.endswith("s") and len(token) > 3 and not token.endswith("ss"):
        token = token[:-1]
    return token


def expand_relationship_tokens(tokens: List[str]) -> set[str]:
    expanded: set[str] = set()
    for token in tokens:
        normalized = normalize_relationship_token(token)
        if not normalized:
            continue
        expanded.add(normalized)
        for alias in TOKEN_ALIASES.get(normalized, ()):
            expanded.add(alias)
    return expanded


def derive_requirement_candidates(req: Dict[str, Any]) -> List[str]:
    candidates: List[str] = []
    description = str(req.get("description", "")).strip()
    if description:
        candidates.append(description)
    category = str(req.get("category", "")).strip()
    if category and category not in OTHER_CATEGORY_ALIASES:
        candidates.append(category)
    for quote in req.get("sample_quotes", []) or []:
        text = str(quote).strip()
        if not text:
            continue
        candidates.append(text)
        for pattern in [
            re.compile(r"(?:need|needs|want|wants|should|must|would like)\s+(?:to\s+)?([a-z][a-z0-9 \-/]{3,60})", re.I),
            re.compile(r"(?:not enough|too|very)\s+([a-z][a-z0-9 \-/]{3,40})", re.I),
            re.compile("(?:\u5e0c\u671b|\u9700\u8981|\u6700\u597d|\u5efa\u8bae|\u5e94\u8be5)(.{2,24})"),
            re.compile("(?:\u592a|\u4e0d\u591f)(.{1,16})"),
        ]:
            for match in pattern.findall(text):
                phrase = str(match).strip(" .,:;-/")
                if phrase:
                    candidates.append(phrase)
    return list(dict.fromkeys(candidate for candidate in candidates if candidate))


def select_requirement_label(candidates: List[str], category: str) -> str:
    best_label = ""
    best_score = -999.0
    category_lower = category.lower()
    for candidate in candidates:
        cleaned = re.sub(r"\s+", " ", candidate).strip(" .,:;-/")
        if not cleaned:
            continue
        score = 0.0
        lower_cleaned = cleaned.lower()
        words = re.findall(r"[a-zA-Z0-9]+", cleaned.lower())
        cjk_count = sum(1 for ch in cleaned if is_cjk(ch))
        if 6 <= len(cleaned) <= 42:
            score += 1.0
        elif 4 <= len(cleaned) <= 56:
            score += 0.5
        if len(words) >= 2:
            score += 1.2
        elif cjk_count >= 3:
            score += 1.0
        if len(words) >= 4:
            score += 0.4
        if category and category not in OTHER_CATEGORY_ALIASES and category_lower in cleaned.lower():
            score += 0.4
        if category and cleaned == category:
            score -= 0.8
        if is_low_signal_label(cleaned):
            score -= 1.8
        if "/" in cleaned and cleaned == category:
            score -= 0.4
        if lower_cleaned.startswith(("for ", "the ", "and ", "with ")):
            score -= 0.8
        if any(token in lower_cleaned for token in (" too ", " need ", " needs ", " quieter", " louder", " longer", " shorter")):
            score += 0.3
        if score > best_score:
            best_score = score
            best_label = cleaned
    if best_label:
        return best_label
    if category and category not in OTHER_CATEGORY_ALIASES:
        return category
    return candidates[0].strip() if candidates else ""


def repair_low_signal_requirements(
    requirements: List[Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, str]], List[str]]:
    repaired: List[Dict[str, Any]] = []
    repairs: List[Dict[str, str]] = []
    warnings: List[str] = []

    for requirement in requirements:
        current = str(requirement.get("description", "")).strip()
        if not is_low_signal_label(current):
            repaired.append(requirement)
            continue
        category = str(requirement.get("category", "")).strip()
        replacement = select_requirement_label(derive_requirement_candidates(requirement), category)
        updated = dict(requirement)
        if replacement and not is_low_signal_label(replacement):
            updated["description"] = replacement
            repairs.append(
                {
                    "requirement_id": str(requirement.get("id", "?")),
                    "from": current,
                    "to": replacement,
                }
            )
            warnings.append(
                f"Repaired low-signal requirement label {requirement.get('id', '?')} -> {replacement}"
            )
        repaired.append(updated)

    return repaired, repairs, warnings


def fail(
    error_code: str,
    message: str,
    details: Dict[str, Any] | None = None,
    *,
    stage: Optional[str] = None,
    retryable: bool = False,
    next_action: Optional[str] = None,
    next_actions: Optional[List[str]] = None,
    missing_inputs: Optional[List[Dict[str, Any]]] = None,
) -> None:
    workspace = current_workspace()
    result_files = build_result_files_map(workspace)
    payload = {
        "success": False,
        "status": "failed",
        "action": "qfd_pipeline_run",
        "error_code": error_code,
        "error": f"{error_code}: {message}",
        "message": message,
        "stage": stage or str(RUNTIME_CONTEXT.get("stage") or "bootstrap"),
        "retryable": retryable,
        "next_action": next_action or "report_failure_and_stop",
        "next_actions": next_actions or default_failure_next_actions(),
        "details": details or {},
        "warnings": list(RUNTIME_CONTEXT.get("warnings") or []),
        "exit_code": 1,
    }
    files_written = list(RUNTIME_CONTEXT.get("files_written") or [])
    if workspace is not None:
        payload["workspace_path"] = str(workspace)
    if files_written:
        payload["files_written"] = files_written
    if result_files:
        payload["result_files"] = result_files
        payload["quick_access"] = build_quick_access(result_files)
        payload["read_guide"] = build_read_guide()
    if missing_inputs:
        payload["missing_inputs"] = missing_inputs
    print(json.dumps(payload, ensure_ascii=False))
    sys.exit(1)


def init_workspace(workspace: Path, project_name: str) -> Dict[str, Any]:
    workspace.mkdir(parents=True, exist_ok=True)
    for subdir in WORKSPACE_SUBDIRS:
        (workspace / subdir).mkdir(parents=True, exist_ok=True)

    meta_path = workspace / "project_meta.json"
    now = now_iso()
    if meta_path.exists():
        meta = read_json_input(
            meta_path,
            input_name="project_meta",
            suggested_flag="--workspace",
            input_kind="state",
            expected_schema="JSON object created by the QFD workspace bootstrap step",
            stage="bootstrap",
            next_action="ask_user_to_clear_or_replace_workspace",
            next_actions=[
                "Ask the user whether to clear the broken workspace metadata or choose a new workspace path.",
                "Do not continue with partial workspace state until project_meta.json is valid again.",
            ],
            reason="workspace metadata is corrupted and must be repaired before continuing",
            retryable=False,
        )
    else:
        meta = {
            "project_id": f"qfd_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "project_name": project_name,
            "created_at": now,
            "last_updated": now,
            "status": {
                "step1_voc": "pending",
                "step2_technical": "pending",
                "step3_matrix": "pending",
                "step4_benchmark": "pending",
                "step5_priority": "pending",
            },
            "our_product": None,
            "competitors": [],
        }

    meta["project_name"] = project_name
    meta["last_updated"] = now
    write_json(meta_path, meta)
    return meta


def normalize_weights(weights_payload: Any) -> Dict[str, float]:
    out: Dict[str, float] = {}
    if isinstance(weights_payload, dict):
        for key, value in weights_payload.items():
            try:
                out[str(key)] = float(value)
            except (TypeError, ValueError):
                continue
        return out

    if isinstance(weights_payload, list):
        for item in weights_payload:
            if not isinstance(item, dict):
                continue
            req_id = item.get("requirement_id")
            importance = item.get("importance")
            if req_id is None or importance is None:
                continue
            try:
                out[str(req_id)] = float(importance)
            except (TypeError, ValueError):
                continue
    return out


def apply_importance(
    requirements: List[Dict[str, Any]],
    weights: Dict[str, float],
) -> None:
    for req in requirements:
        req_id = req.get("id")
        if req_id in weights:
            req["importance"] = weights[req_id]
            req["user_confirmed"] = True

    ranked = sorted(requirements, key=lambda r: r.get("frequency_in_voc", 0), reverse=True)
    n = len(ranked)
    for idx, req in enumerate(ranked):
        if req.get("importance") is not None:
            continue
        if n <= 1:
            req["importance"] = 3.0
        else:
            req["importance"] = float(max(1, 5 - ((idx * 4) // (n - 1))))
        req["user_confirmed"] = False


def tokenize_text(text: str) -> List[str]:
    lower = text.lower()
    base_tokens = [normalize_relationship_token(token) for token in re.findall(r"[a-z0-9]+", lower)]
    tokens = [token for token in base_tokens if token]
    for idx in range(len(tokens) - 1):
        tokens.append(f"{tokens[idx]}_{tokens[idx + 1]}")
    cjk_chars = [ch for ch in text if is_cjk(ch)]
    if len(cjk_chars) >= 2:
        for idx in range(len(cjk_chars) - 1):
            tokens.append("".join(cjk_chars[idx : idx + 2]))
    return tokens


def auto_relationships(
    requirements: List[Dict[str, Any]],
    features: List[Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], Dict[str, Any], List[str]]:
    warnings: List[str] = []
    rels: List[Dict[str, Any]] = []
    diagnostics = {
        "auto_generated": True,
        "fallback_count": 0,
        "strong_matches": 0,
        "medium_matches": 0,
        "weak_matches": 0,
    }

    feature_tokens: Dict[str, set[str]] = {}
    for feature in features:
        f_id = str(feature.get("id", "")).strip()
        name = str(feature.get("name", ""))
        desc = str(feature.get("description", ""))
        feature_tokens[f_id] = expand_relationship_tokens(tokenize_text(f"{name} {desc}"))

    for req in requirements:
        req_id = str(req.get("id", "")).strip()
        req_fragments = [str(req.get("description", "")), str(req.get("category", ""))]
        req_fragments.extend(str(item) for item in (req.get("sample_quotes") or []))
        req_tokens = expand_relationship_tokens(tokenize_text(" ".join(req_fragments)))

        scored: List[Tuple[str, float]] = []
        for feature in features:
            f_id = str(feature.get("id", "")).strip()
            overlap = req_tokens.intersection(feature_tokens.get(f_id, set()))
            score = float(len(overlap))
            if str(req.get("description", "")).lower() in str(feature.get("name", "")).lower():
                score += 1.5
            if str(req.get("category", "")).lower() in str(feature.get("description", "")).lower():
                score += 0.5
            scored.append((f_id, score))

        scored.sort(key=lambda item: item[1], reverse=True)
        for feature_id, score in scored:
            if score <= 0:
                continue
            if score >= 3:
                strength = 9
                diagnostics["strong_matches"] += 1
            elif score >= 1.5:
                strength = 3
                diagnostics["medium_matches"] += 1
            else:
                strength = 1
                diagnostics["weak_matches"] += 1
            rels.append(
                {
                    "requirement_id": req_id,
                    "feature_id": feature_id,
                    "strength": strength,
                }
            )

        if not any(rel["requirement_id"] == req_id for rel in rels) and scored:
            best_feature = scored[0][0]
            rels.append(
                {
                    "requirement_id": req_id,
                    "feature_id": best_feature,
                    "strength": 1,
                }
            )
            diagnostics["fallback_count"] += 1
            warnings.append(
                f"Auto fallback relationship injected for {req_id} -> {best_feature}"
            )

    unique = {}
    for rel in rels:
        key = (rel["requirement_id"], rel["feature_id"])
        if key not in unique or rel["strength"] > unique[key]["strength"]:
            unique[key] = rel
    diagnostics["relationship_count"] = len(unique)
    return list(unique.values()), diagnostics, warnings


def normalize_features_payload(raw: Any) -> List[Dict[str, Any]]:
    if isinstance(raw, dict):
        if isinstance(raw.get("features"), list):
            features = raw["features"]
        else:
            fail(
                "QFD_VALIDATION_ERROR",
                "features payload must contain a 'features' array",
                details={"expected_schema": "object with top-level 'features' array"},
                stage="load_feature_spec",
                retryable=True,
                next_action="ask_user_for_corrected_feature_spec_json",
                missing_inputs=[
                    missing_input(
                        "features_path",
                        "json",
                        "feature spec is required for the HOQ step",
                        "--features-path",
                        "object with top-level 'features' array",
                    )
                ],
            )
    elif isinstance(raw, list):
        features = raw
    else:
        fail(
            "QFD_VALIDATION_ERROR",
            "invalid features payload",
            details={"expected_schema": "list of feature objects or object with 'features' array"},
            stage="load_feature_spec",
            retryable=True,
            next_action="ask_user_for_corrected_feature_spec_json",
            missing_inputs=[
                missing_input(
                    "features_path",
                    "json",
                    "feature spec is required for the HOQ step",
                    "--features-path",
                    "list of feature objects or object with top-level 'features' array",
                )
            ],
        )

    normalized: List[Dict[str, Any]] = []
    for item in features:
        if not isinstance(item, dict):
            continue
        feature_id = str(item.get("id", "")).strip()
        name = str(item.get("name", "")).strip()
        if not feature_id or not name:
            continue
        normalized.append(
            {
                "id": feature_id,
                "name": name,
                "value": item.get("value", item.get("target_value", "")),
                "unit": item.get("unit", ""),
                "direction": item.get("direction", "higher_better"),
                "description": item.get("description", ""),
            }
        )
    if not normalized:
        fail(
            "QFD_VALIDATION_ERROR",
            "no valid features found in features payload",
            details={"required_fields": ["id", "name"]},
            stage="load_feature_spec",
            retryable=True,
            next_action="ask_user_for_corrected_feature_spec_json",
            missing_inputs=[
                missing_input(
                    "features_path",
                    "json",
                    "feature spec must contain at least one feature with id and name",
                    "--features-path",
                    "feature objects with non-empty 'id' and 'name'",
                )
            ],
        )
    return normalized


def load_list_payload(
    path: Path,
    key: str,
    input_name: str,
    suggested_flag: str,
) -> List[Dict[str, Any]]:
    payload = read_json_input(
        path,
        input_name=input_name,
        suggested_flag=suggested_flag,
        expected_schema=f"list of objects or object with top-level '{key}' list",
        stage=str(RUNTIME_CONTEXT.get("stage") or "unknown"),
        next_action=f"ask_user_for_corrected_{input_name}",
        reason=f"{input_name} must match the expected list schema",
    )
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict) and isinstance(payload.get(key), list):
        return [item for item in payload[key] if isinstance(item, dict)]
    fail(
        "QFD_VALIDATION_ERROR",
        f"{input_name} must be a list or object with '{key}' list",
        details={"path": str(path), "expected_key": key},
        stage=str(RUNTIME_CONTEXT.get("stage") or "unknown"),
        retryable=True,
        next_action=f"ask_user_for_corrected_{input_name}",
        missing_inputs=[
            missing_input(
                input_name,
                "json",
                f"{input_name} is malformed",
                suggested_flag,
                f"list of objects or object with top-level '{key}' list",
            )
        ],
    )
    return []


def parse_args() -> Tuple[argparse.Namespace, List[str]]:
    parser = argparse.ArgumentParser(description="Run unified QFD pipeline")
    parser.add_argument("--voc-path", required=True, help="Path to VOC input file")
    parser.add_argument("--workspace", default="qfd-analysis", help="Workspace directory")
    parser.add_argument(
        "--project-name", default="QFD Analysis Project", help="Project display name"
    )
    parser.add_argument("--features-path", help="Path to feature spec JSON")
    parser.add_argument("--relationships-path", help="Path to relationships JSON")
    parser.add_argument("--correlations-path", help="Path to correlations JSON")
    parser.add_argument("--weights-path", help="Path to weights JSON")
    parser.add_argument(
        "--competitor-specs-path",
        action="append",
        default=[],
        help="Path to competitor spec JSON (repeatable)",
    )
    parser.add_argument("--requirement-ratings-path", help="Path to requirement ratings JSON")
    parser.add_argument("--min-frequency", type=int, default=2)
    parser.add_argument("--include-xlsx", action="store_true", default=True)
    parser.add_argument("--no-xlsx", action="store_true")
    parser.add_argument("--deterministic-seed", type=int, default=42)
    args, unknown = parser.parse_known_args()
    if args.no_xlsx:
        args.include_xlsx = False
    return args, unknown


def main() -> None:
    args, unknown_args = parse_args()
    warnings: List[str] = []
    if unknown_args:
        warnings.append(f"Ignored unknown args: {' '.join(unknown_args)}")
    sync_runtime_state([], warnings)

    cwd = Path.cwd()
    set_runtime_stage("validate_inputs")
    workspace = abs_path(args.workspace, cwd)
    set_runtime_workspace(workspace)
    voc_path = abs_path(args.voc_path, cwd)
    if not voc_path.exists():
        fail(
            "QFD_VALIDATION_ERROR",
            f"voc_path not found: {voc_path}",
            details={"requested_path": str(voc_path)},
            stage="validate_inputs",
            retryable=True,
            next_action="ask_user_for_voc_file",
            missing_inputs=[
                missing_input(
                    "voc_path",
                    "file",
                    "VOC input is required to generate requirements",
                    "--voc-path",
                )
            ],
        )

    meta = init_workspace(workspace, args.project_name)
    files_written: List[str] = [str(workspace / "project_meta.json")]
    sync_runtime_state(files_written, warnings)

    # Step 1: VOC
    set_runtime_stage("voc_process")
    try:
        voc_result = process_voc_file(str(voc_path), max(1, args.min_frequency))
    except json.JSONDecodeError as exc:
        fail(
            "QFD_VALIDATION_ERROR",
            f"voc_path contains invalid JSON: {voc_path}",
            details={
                "requested_path": str(voc_path),
                "line": exc.lineno,
                "column": exc.colno,
                "message": exc.msg,
            },
            stage="voc_process",
            retryable=True,
            next_action="ask_user_for_better_voc_input",
            missing_inputs=[
                missing_input(
                    "voc_path",
                    "file",
                    "VOC JSON input is malformed and must be corrected before retrying",
                    "--voc-path",
                    "CSV, TXT, or valid JSON VOC payload",
                )
            ],
        )
    except OSError as exc:
        fail(
            "QFD_RUNTIME_ERROR",
            f"failed to read voc_path: {voc_path}",
            details={
                "requested_path": str(voc_path),
                "message": str(exc),
                "type": type(exc).__name__,
            },
            stage="voc_process",
            retryable=True,
            next_action="ask_user_for_better_voc_input",
        )
    if not voc_result.get("success"):
        fail(
            "QFD_VALIDATION_ERROR",
            str(voc_result.get("error", "VOC processing failed")),
            details={"voc_path": str(voc_path)},
            stage="voc_process",
            retryable=True,
            next_action="ask_user_for_better_voc_input",
            missing_inputs=[
                missing_input(
                    "voc_path",
                    "file",
                    "VOC file exists but did not yield usable entries",
                    "--voc-path",
                )
            ],
        )

    requirements = list(voc_result.get("requirements", []))
    voc_input_mode = str(voc_result.get("input_mode", "raw_voc"))
    voc_structured_input = bool(voc_result.get("structured_input"))
    if not requirements:
        fail(
            "QFD_VALIDATION_ERROR",
            "No requirements generated from VOC input",
            details={"voc_path": str(voc_path), "total_voc_entries": voc_result.get("total_voc_entries", 0)},
            stage="voc_process",
            retryable=True,
            next_action="ask_user_for_better_voc_input",
            missing_inputs=[
                missing_input(
                    "voc_path",
                    "file",
                    "VOC content did not produce any actionable requirements",
                    "--voc-path",
                )
            ],
        )

    weights_map: Dict[str, float] = {}
    if args.weights_path:
        weights_path = abs_path(args.weights_path, cwd)
        if not weights_path.exists():
            fail(
                "QFD_VALIDATION_ERROR",
                f"weights_path not found: {weights_path}",
                details={"requested_path": str(weights_path)},
                stage="voc_process",
                retryable=True,
                next_action="ask_user_for_weights_json_or_rerun_without_it",
                next_actions=[
                    "Ask the user to re-upload the weights JSON if custom requirement weights are required.",
                    "Otherwise rerun without --weights-path to keep auto-derived importance values.",
                ],
                missing_inputs=[
                    missing_input(
                        "weights_path",
                        "json",
                        "custom weights file was requested but is missing",
                        "--weights-path",
                    )
                ],
            )
        weights_map = normalize_weights(
            read_json_input(
                weights_path,
                input_name="weights_path",
                suggested_flag="--weights-path",
                expected_schema="JSON object {requirement_id: importance} or list of {requirement_id, importance}",
                stage="voc_process",
                next_action="ask_user_for_weights_json_or_rerun_without_it",
                next_actions=[
                    "Ask the user to re-upload a valid weights JSON if custom requirement weights are required.",
                    "Otherwise rerun without --weights-path to keep auto-derived importance values.",
                ],
                reason="custom weights must be valid JSON before they can override requirement importance",
            )
        )

    apply_importance(requirements, weights_map)
    requirements, repair_log, repair_warnings = repair_low_signal_requirements(requirements)
    warnings.extend(repair_warnings)
    sync_runtime_state(files_written, warnings)

    low_signal = [req.get("id", "?") for req in requirements if is_low_signal_label(str(req.get("description", "")))]
    if low_signal:
        fail(
            "QFD_VALIDATION_ERROR",
            f"low-signal requirement labels remain after repair for {', '.join(low_signal)}",
            details={
                "requirement_ids": low_signal,
                "repair_attempts": repair_log,
            },
            stage="voc_process",
            retryable=True,
            next_action="ask_user_for_cleaner_voc_or_manual_requirements",
            next_actions=[
                "Ask the user for cleaner VOC input or a manual requirements JSON with explicit requirement descriptions.",
                "Keep the current workspace artifacts for inspection instead of rerunning immediately.",
            ],
        )

    requirements_payload = {
        "version": "1.0",
        "last_updated": now_iso(),
        "total_voc_entries": voc_result.get("total_voc_entries", 0),
        "input_mode": voc_input_mode,
        "structured_input": voc_structured_input,
        "repairs_applied": repair_log,
        "requirements": requirements,
    }
    req_path = workspace / "01_voc" / "requirements.json"
    write_json(req_path, requirements_payload)
    files_written.append(str(req_path))
    sync_runtime_state(files_written, warnings)

    diag_path = workspace / "01_voc" / "cluster_diagnostics.json"
    trace_path = workspace / "01_voc" / "llm_merge_trace.json"
    write_json(
        diag_path,
        {
            "version": "1.0",
            "last_updated": now_iso(),
            "min_frequency": args.min_frequency,
            "total_voc_entries": voc_result.get("total_voc_entries", 0),
            "deduplicated_voc_entries": voc_result.get("deduplicated_voc_entries", voc_result.get("total_voc_entries", 0)),
            "categories_found": voc_result.get("categories_found", []),
            "input_mode": voc_input_mode,
            "structured_input": voc_structured_input,
            "repairs_applied": repair_log,
            "detected_fields": voc_result.get("detected_fields", {}),
            "model_source": DEFAULT_MODEL_SOURCE,
        },
    )
    write_json(
        trace_path,
        {
            "model_source": DEFAULT_MODEL_SOURCE,
            "llm_enabled": False,
            "note": "Python pipeline currently uses deterministic local processing only.",
        },
    )
    files_written.extend([str(diag_path), str(trace_path)])
    sync_runtime_state(files_written, warnings)

    # Step 2: feature spec
    set_runtime_stage("load_feature_spec")
    feature_path: Path
    if args.features_path:
        feature_path = abs_path(args.features_path, cwd)
    else:
        feature_path = workspace / "02_technical" / "our_product_spec.json"
    if not feature_path.exists():
        fail(
            "QFD_VALIDATION_ERROR",
            (
                "features_path is required and must point to a JSON spec "
                "with a features array"
            ),
            {"expected_path": str(feature_path)},
            stage="load_feature_spec",
            retryable=True,
            next_action="ask_user_for_feature_spec_json",
            missing_inputs=[
                missing_input(
                    "features_path",
                    "json",
                    "feature spec is required for the HOQ step",
                    "--features-path",
                    "object with top-level 'features' array",
                )
            ],
        )

    feature_payload = read_json_input(
        feature_path,
        input_name="features_path",
        suggested_flag="--features-path",
        expected_schema="list of feature objects or object with top-level 'features' array",
        stage="load_feature_spec",
        next_action="ask_user_for_corrected_feature_spec_json",
        reason="feature spec is required for the HOQ step",
    )
    features = normalize_features_payload(feature_payload)
    our_spec = {
        "version": "1.0",
        "last_updated": now_iso(),
        "product": {"id": "our_product", "name": args.project_name},
        "source": {"type": "user_input", "path": str(feature_path)},
        "features": features,
    }
    our_spec_path = workspace / "02_technical" / "our_product_spec.json"
    write_json(our_spec_path, our_spec)
    files_written.append(str(our_spec_path))
    sync_runtime_state(files_written, warnings)

    # Step 3: HOQ
    set_runtime_stage("build_matrices")
    auto_relationship_diagnostics: Dict[str, Any] = {"auto_generated": False, "fallback_count": 0}
    if args.relationships_path:
        rel_path = abs_path(args.relationships_path, cwd)
        if not rel_path.exists():
            fail(
                "QFD_VALIDATION_ERROR",
                f"relationships_path not found: {rel_path}",
                details={"requested_path": str(rel_path)},
                stage="build_matrices",
                retryable=True,
                next_action="ask_user_for_relationships_json_or_rerun_without_it",
                next_actions=[
                    "Ask the user to re-upload the relationships JSON if manual relationships are required.",
                    "Otherwise rerun without --relationships-path to allow auto-generated relationships.",
                ],
                missing_inputs=[
                    missing_input(
                        "relationships_path",
                        "json",
                        "manual relationships file was requested but is missing",
                        "--relationships-path",
                    )
                ],
            )
        relationships = load_list_payload(
            rel_path,
            "relationships",
            "relationships_path",
            "--relationships-path",
        )
    else:
        relationships, auto_relationship_diagnostics, rel_warnings = auto_relationships(requirements, features)
        warnings.extend(rel_warnings)
        sync_runtime_state(files_written, warnings)

    if args.correlations_path:
        corr_path = abs_path(args.correlations_path, cwd)
        if not corr_path.exists():
            fail(
                "QFD_VALIDATION_ERROR",
                f"correlations_path not found: {corr_path}",
                details={"requested_path": str(corr_path)},
                stage="build_matrices",
                retryable=True,
                next_action="ask_user_for_correlations_json_or_rerun_without_it",
                next_actions=[
                    "Ask the user to re-upload the correlations JSON if a roof matrix is required.",
                    "Otherwise rerun without --correlations-path to continue with an empty roof matrix.",
                ],
                missing_inputs=[
                    missing_input(
                        "correlations_path",
                        "json",
                        "manual correlations file was requested but is missing",
                        "--correlations-path",
                    )
                ],
            )
        correlations = load_list_payload(
            corr_path,
            "correlations",
            "correlations_path",
            "--correlations-path",
        )
    else:
        correlations = []
        warnings.append("No correlations provided; roof matrix is empty.")
        sync_runtime_state(files_written, warnings)

    relationship_matrix = build_relationship_matrix(requirements, features, relationships)
    relationship_matrix["generation"] = {
        "mode": "manual" if args.relationships_path else "auto",
        **auto_relationship_diagnostics,
    }
    correlation_matrix = build_correlation_matrix(features, correlations)
    rel_lookup = {
        (rel["requirement_id"], rel["feature_id"]): rel.get("strength", 0)
        for rel in relationships
    }
    conflicts = identify_conflicts(requirements, features, correlations, rel_lookup)

    relationship_path = workspace / "03_analysis" / "relationship_matrix.json"
    correlation_path = workspace / "03_analysis" / "correlation_matrix.json"
    conflicts_path = workspace / "03_analysis" / "conflicts.json"
    write_json(relationship_path, relationship_matrix)
    write_json(correlation_path, correlation_matrix)
    write_json(conflicts_path, conflicts)
    files_written.extend(
        [str(relationship_path), str(correlation_path), str(conflicts_path)]
    )
    sync_runtime_state(files_written, warnings)

    # Step 4: benchmark (optional)
    set_runtime_stage("build_benchmark")
    competitor_specs: List[Dict[str, Any]] = []
    competitor_meta: List[Dict[str, Any]] = []
    for raw_path in args.competitor_specs_path:
        spec_path = abs_path(raw_path, cwd)
        if not spec_path.exists():
            fail(
                "QFD_VALIDATION_ERROR",
                f"competitor spec not found: {spec_path}",
                details={"requested_path": str(spec_path)},
                stage="build_benchmark",
                retryable=True,
                next_action="ask_user_for_competitor_spec_json_or_rerun_without_it",
                next_actions=[
                    "Ask the user to re-upload the missing competitor spec if benchmark comparison is required.",
                    "Otherwise rerun without that --competitor-specs-path argument.",
                ],
                missing_inputs=[
                    missing_input(
                        "competitor_specs_path",
                        "json",
                        "benchmark comparison file is missing",
                        "--competitor-specs-path",
                    )
                ],
            )
        payload = read_json_input(
            spec_path,
            input_name="competitor_specs_path",
            suggested_flag="--competitor-specs-path",
            expected_schema="JSON object with product metadata and features array",
            stage="build_benchmark",
            next_action="ask_user_for_corrected_competitor_spec_json",
            reason="competitor spec must be a valid JSON object before benchmark comparison can run",
        )
        if not isinstance(payload, dict):
            fail(
                "QFD_VALIDATION_ERROR",
                f"invalid competitor spec: {spec_path}",
                details={"requested_path": str(spec_path)},
                stage="build_benchmark",
                retryable=True,
                next_action="ask_user_for_corrected_competitor_spec_json",
                missing_inputs=[
                    missing_input(
                        "competitor_specs_path",
                        "json",
                        "competitor spec must be a JSON object",
                        "--competitor-specs-path",
                    )
                ],
            )
        competitor_specs.append(payload)
        product = payload.get("product", {}) if isinstance(payload, dict) else {}
        competitor_meta.append(
            {
                "id": product.get("id"),
                "name": product.get("name"),
                "model": product.get("model"),
                "source": str(spec_path),
            }
        )

    requirement_ratings: Dict[str, Any] = {}
    if args.requirement_ratings_path:
        ratings_path = abs_path(args.requirement_ratings_path, cwd)
        if not ratings_path.exists():
            fail(
                "QFD_VALIDATION_ERROR",
                f"requirement_ratings_path not found: {ratings_path}",
                details={"requested_path": str(ratings_path)},
                stage="build_benchmark",
                retryable=True,
                next_action="ask_user_for_requirement_ratings_json_or_rerun_without_it",
                next_actions=[
                    "Ask the user to re-upload the requirement ratings JSON if benchmark scoring is required.",
                    "Otherwise rerun without --requirement-ratings-path.",
                ],
                missing_inputs=[
                    missing_input(
                        "requirement_ratings_path",
                        "json",
                        "requirement ratings file is missing",
                        "--requirement-ratings-path",
                    )
                ],
            )
        ratings_payload = read_json_input(
            ratings_path,
            input_name="requirement_ratings_path",
            suggested_flag="--requirement-ratings-path",
            expected_schema="JSON object keyed by requirement id",
            stage="build_benchmark",
            next_action="ask_user_for_corrected_requirement_ratings_json",
            reason="requirement ratings must be valid JSON before benchmark scoring can run",
        )
        if not isinstance(ratings_payload, dict):
            fail(
                "QFD_VALIDATION_ERROR",
                "requirement_ratings must be a JSON object",
                details={"requested_path": str(ratings_path)},
                stage="build_benchmark",
                retryable=True,
                next_action="ask_user_for_corrected_requirement_ratings_json",
                missing_inputs=[
                    missing_input(
                        "requirement_ratings_path",
                        "json",
                        "requirement ratings payload is malformed",
                        "--requirement-ratings-path",
                        "JSON object keyed by requirement id",
                    )
                ],
            )
        requirement_ratings = ratings_payload

    benchmark_state = "completed" if competitor_specs else "skipped"
    if benchmark_state == "skipped":
        warnings.append("Benchmark skipped because no competitor specs were provided.")
        sync_runtime_state(files_written, warnings)
    benchmark_table = build_benchmark_table(
        requirements, our_spec, competitor_specs, requirement_ratings
    )
    benchmark_table["benchmark_state"] = benchmark_state
    benchmark_table["competitor_count"] = len(competitor_specs)
    gap_analysis = analyze_gaps(benchmark_table)
    gap_analysis["benchmark_state"] = benchmark_state
    gap_analysis["competitor_count"] = len(competitor_specs)
    benchmark_path = workspace / "04_benchmark" / "benchmark_table.json"
    gap_path = workspace / "04_benchmark" / "gap_analysis.json"
    write_json(benchmark_path, benchmark_table)
    write_json(gap_path, gap_analysis)
    files_written.extend([str(benchmark_path), str(gap_path)])
    sync_runtime_state(files_written, warnings)

    # Step 5: report
    set_runtime_stage("generate_report")
    priorities = generate_priority_recommendations(
        requirements,
        relationship_matrix.get("feature_scores", []),
        conflicts.get("conflicts", []),
        gap_analysis,
    )
    priorities_payload = {
        "version": "1.0",
        "last_updated": now_iso(),
        **priorities,
    }
    priorities_path = workspace / "05_output" / "priority_recommendations.json"
    write_json(priorities_path, priorities_payload)
    files_written.append(str(priorities_path))

    report_text = generate_markdown_report(
        meta,
        requirements_payload,
        relationship_matrix,
        correlation_matrix,
        conflicts,
        benchmark_table,
        gap_analysis,
        priorities,
    )

    conflict_count = len(conflicts.get("conflicts", []))
    has_no_conflict_line = "No significant technical conflicts identified." in report_text
    if conflict_count == 0 and not has_no_conflict_line:
        fail(
            "QFD_CONSISTENCY_ERROR",
            "report text does not match conflicts.json (expected no conflicts line)",
            details={"conflict_count": conflict_count},
            stage="generate_report",
        )
    if conflict_count > 0 and has_no_conflict_line:
        fail(
            "QFD_CONSISTENCY_ERROR",
            "report text does not match conflicts.json (contains no-conflict line)",
            details={"conflict_count": conflict_count},
            stage="generate_report",
        )

    report_path = workspace / "05_output" / "qfd_report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)
    files_written.append(str(report_path))
    sync_runtime_state(files_written, warnings)

    xlsx_written = False
    xlsx_path = workspace / "05_output" / "hoq_matrix.xlsx"
    if args.include_xlsx:
        xlsx_written = generate_hoq_excel(
            requirements,
            features,
            relationship_matrix,
            correlation_matrix,
            str(xlsx_path),
        )
        if xlsx_written:
            files_written.append(str(xlsx_path))
        else:
            warnings.append("XLSX output skipped (openpyxl not installed).")
        sync_runtime_state(files_written, warnings)

    meta["status"] = {
        "step1_voc": "completed",
        "step2_technical": "completed",
        "step3_matrix": "completed",
        "step4_benchmark": benchmark_state,
        "step5_priority": "completed",
    }
    meta["our_product"] = {
        "id": "our_product",
        "name": args.project_name,
        "model": None,
        "source": str(feature_path),
    }
    meta["competitors"] = competitor_meta
    meta["last_updated"] = now_iso()
    meta_path = workspace / "project_meta.json"
    write_json(meta_path, meta)
    sync_runtime_state(files_written, warnings)
    result_files = build_result_files_map(workspace)
    quick_access = build_quick_access(result_files)
    read_guide = build_read_guide()
    run_quality = "complete"
    if benchmark_state == "skipped":
        run_quality = "benchmark_skipped"
    if repair_log or auto_relationship_diagnostics.get("fallback_count") or not args.relationships_path:
        run_quality = "partially_inferred" if benchmark_state == "completed" else "benchmark_skipped"

    payload = {
        "success": True,
        "status": "completed",
        "action": "qfd_pipeline_run",
        "message": "QFD pipeline completed successfully.",
        "workspace_path": str(workspace),
        "files_written": files_written,
        "result_files": result_files,
        "quick_access": quick_access,
        "read_guide": read_guide,
        "next_actions": [
            "Read qfd_report_md before drafting the user-facing answer.",
            "Read priority_recommendations_json to verify ranking and recommendations.",
            "Read conflicts_json before explaining trade-offs or contradictions.",
        ],
        "summary": {
            "requirements_generated": len(requirements),
            "features": len(features),
            "relationships": len(relationships),
            "correlations": len(correlations),
            "conflicts": conflict_count,
            "competitors": len(competitor_specs),
            "benchmark_state": benchmark_state,
            "benchmark_skipped": benchmark_state == "skipped",
            "run_quality": run_quality,
            "voc_input_mode": voc_input_mode,
            "structured_voc_input": voc_structured_input,
            "requirements_repaired": len(repair_log),
            "auto_relationship_fallbacks": int(auto_relationship_diagnostics.get("fallback_count", 0)),
            "include_xlsx": bool(args.include_xlsx),
            "xlsx_written": xlsx_written,
            "model_source": DEFAULT_MODEL_SOURCE,
        },
        "warnings": warnings,
        "project_meta": meta,
        "exit_code": 0,
    }
    print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except json.JSONDecodeError as exc:  # pragma: no cover
        fail(
            "QFD_VALIDATION_ERROR",
            "encountered invalid JSON while reading pipeline inputs",
            details={
                "line": exc.lineno,
                "column": exc.colno,
                "message": exc.msg,
                "type": type(exc).__name__,
            },
            next_action="ask_user_for_corrected_json_input",
            next_actions=[
                "Ask the user which JSON input was being supplied and request a corrected file.",
                "Do not continue with partial results until the malformed JSON is fixed.",
            ],
            retryable=True,
        )
    except Exception as exc:  # pragma: no cover
        fail("QFD_RUNTIME_ERROR", str(exc), {"type": type(exc).__name__})

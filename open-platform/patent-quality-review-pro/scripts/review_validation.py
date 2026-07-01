#!/usr/bin/env python3
"""Shared evidence-chain validation for patent-quality-review-pro."""

import json
import os


NOVELTY_ARTIFACTS = [
    "claim_elements.md",
    "prior_art_catalog.json",
    "element_mapping.md",
    "claim_diff_matrix.md",
    "novelty_report.md",
]

NON_OBVIOUSNESS_ARTIFACTS = [
    "jurisdiction_plan.md",
    "claim_diff_matrix.md",
    "combination_candidates.json",
    "motivation_matrix.md",
    "secondary_considerations.md",
    "inventive_step_report.md",
]

NON_OBVIOUSNESS_D2D3_ARTIFACTS = [
    "combination_candidates.json",
    "motivation_matrix.md",
    "inventive_step_report.md",
]

UNREAD_REFERENCE_MARKERS = [
    "摘要读取",
    "仅读取摘要",
    "未fetch",
    "未 fetch",
    "未read",
    "未 read",
    "未读取全文",
    "未fetch/read全文",
]


def infer_session_root(data_file_path="", output_path="", cwd=None):
    """Infer the Eureka session folder from data/output paths or cwd."""
    seeds = [data_file_path, output_path, cwd or os.getcwd()]
    for seed in seeds:
        if not seed:
            continue
        path = os.path.abspath(seed)
        if os.path.isfile(path):
            path = os.path.dirname(path)
        while True:
            if os.path.basename(path).startswith("session-"):
                return path
            if os.path.exists(os.path.join(path, "session.runtime.json")):
                return path
            parent = os.path.dirname(path)
            if parent == path:
                break
            path = parent
    return cwd or os.getcwd()


def resolve_artifact_path(raw_path, session_root, cwd=None):
    """Resolve Eureka-style @session/@skill_workspace refs and plain paths."""
    if not raw_path or not isinstance(raw_path, str):
        return ""
    raw_path = raw_path.strip()
    if raw_path.startswith("@session/"):
        return os.path.join(session_root, raw_path[len("@session/"):])
    if raw_path == "@session":
        return session_root
    if raw_path.startswith("@skill_workspace/"):
        return os.path.join(cwd or os.getcwd(), raw_path[len("@skill_workspace/"):])
    if raw_path == "@skill_workspace":
        return cwd or os.getcwd()
    if os.path.isabs(raw_path):
        return raw_path

    cwd_candidate = os.path.abspath(raw_path)
    if os.path.exists(cwd_candidate):
        return cwd_candidate
    return os.path.join(session_root, raw_path)


def artifact_candidates(data, name, category=None):
    paths = []
    artifact_paths = data.get("artifact_paths", {})
    stem = os.path.splitext(name)[0]

    def add(value):
        if isinstance(value, str):
            paths.append(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    paths.append(item)

    if isinstance(artifact_paths, dict):
        if category and isinstance(artifact_paths.get(category), dict):
            add(artifact_paths[category].get(name))
            add(artifact_paths[category].get(stem))
        add(artifact_paths.get(name))
        add(artifact_paths.get(stem))

        if name == "claim_diff_matrix.md" and category == "non_obviousness":
            novelty_paths = artifact_paths.get("novelty")
            if isinstance(novelty_paths, dict):
                add(novelty_paths.get(name))
                add(novelty_paths.get(stem))
    elif isinstance(artifact_paths, list):
        add(artifact_paths)

    for item in data.get("evidence_artifacts", []):
        if isinstance(item, str) and item.strip().endswith(name):
            add(item)

    return paths


def existing_nonempty_path(paths, session_root, cwd=None):
    for raw_path in paths:
        path = resolve_artifact_path(raw_path, session_root, cwd)
        if path and os.path.exists(path) and os.path.getsize(path) > 0:
            return path
    return ""


def reference_entries(data):
    entries = []
    raw_refs = data.get("fetched_references", [])
    if isinstance(raw_refs, list):
        for item in raw_refs:
            if isinstance(item, dict):
                entries.append(item)
    raw_paths = data.get("fetched_reference_paths", {})
    if isinstance(raw_paths, dict):
        for role, value in raw_paths.items():
            values = value if isinstance(value, list) else [value]
            for path in values:
                if isinstance(path, str):
                    entries.append({"role": role, "path": path})
    elif isinstance(raw_paths, list):
        for path in raw_paths:
            if isinstance(path, str):
                entries.append({"role": "unknown", "path": path})
    return entries


def existing_reference_paths(data, role_names, session_root, cwd=None):
    wanted = {role.upper() for role in role_names}
    paths = []
    for entry in reference_entries(data):
        role = str(entry.get("role", "")).upper()
        path = entry.get("path", "")
        if role in wanted:
            resolved = resolve_artifact_path(path, session_root, cwd)
            if resolved and os.path.exists(resolved) and os.path.getsize(resolved) > 0:
                paths.append(resolved)
    return paths


def has_existing_reference(data, role_names, session_root, cwd=None):
    return bool(existing_reference_paths(data, role_names, session_root, cwd))


def validate_d1_selection_rationale(data, session_root, cwd=None):
    errors = []
    rationale = data.get("d1_selection_rationale")
    if not isinstance(rationale, dict):
        return ["evidence_mode=full 时必须提供 d1_selection_rationale，说明 D1 选择依据。"]

    required_fields = ["selected_d1", "source", "reason", "date_check", "fetch_path"]
    for field in required_fields:
        if not str(rationale.get(field, "")).strip():
            errors.append(f"d1_selection_rationale 缺少必要字段：{field}")

    fetch_path = rationale.get("fetch_path", "")
    resolved_fetch_path = resolve_artifact_path(fetch_path, session_root, cwd)
    if fetch_path and not (resolved_fetch_path and os.path.exists(resolved_fetch_path) and os.path.getsize(resolved_fetch_path) > 0):
        errors.append("d1_selection_rationale.fetch_path 必须指向已 fetch/read 的 D1 原文文件。")

    d1_paths = existing_reference_paths(data, ["D1"], session_root, cwd)
    if resolved_fetch_path and d1_paths and resolved_fetch_path not in d1_paths:
        errors.append("d1_selection_rationale.fetch_path 必须与 fetched_references 中 D1 路径一致。")

    alternatives = rationale.get("alternatives_considered", [])
    if alternatives is not None and not isinstance(alternatives, list):
        errors.append("d1_selection_rationale.alternatives_considered 必须为列表；没有备选时写空列表。")

    limitations = rationale.get("limitations", [])
    if limitations is not None and not isinstance(limitations, list):
        errors.append("d1_selection_rationale.limitations 必须为列表；没有限制时写空列表。")

    return errors


def artifact_has_unread_reference_marker(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception:
        return False
    return any(marker in text for marker in UNREAD_REFERENCE_MARKERS)


def session_file_path(session_root, filename):
    path = os.path.join(session_root, filename)
    return path if os.path.exists(path) else ""


def actual_loaded_skills(session_root):
    """Read Eureka runtime records instead of trusting the review JSON alone."""
    skills = set()

    runtime_path = session_file_path(session_root, "session.runtime.json")
    if runtime_path:
        try:
            with open(runtime_path, "r", encoding="utf-8") as f:
                runtime = json.load(f)
            skills.update(runtime.get("loaded_skills") or [])
            active_skill = runtime.get("active_skill")
            if active_skill:
                skills.add(active_skill)
        except Exception:
            pass

    index_path = session_file_path(session_root, "turn_context_index.json")
    if index_path:
        try:
            with open(index_path, "r", encoding="utf-8") as f:
                index = json.load(f)
            for record in index.get("records", []):
                if record.get("tool_name") != "skills":
                    continue
                tool_input = record.get("input") or {}
                result = record.get("result_digest") or {}
                if tool_input.get("action") != "load":
                    continue
                if record.get("status") != "completed":
                    continue
                if result.get("success") is False:
                    continue
                skill_name = tool_input.get("name") or result.get("skill")
                if skill_name:
                    skills.add(skill_name)
        except Exception:
            pass

    return skills


def has_session_runtime_records(session_root):
    return bool(
        session_file_path(session_root, "session.runtime.json")
        or session_file_path(session_root, "turn_context_index.json")
    )


def validation_error_path(output_path):
    return os.path.join(
        os.path.dirname(os.path.abspath(output_path)),
        "review_validation_errors.json",
    )


def validation_pass_path(output_path):
    return os.path.join(
        os.path.dirname(os.path.abspath(output_path)),
        "review_validation_passed.json",
    )


def write_validation_errors(errors, output_path):
    error_path = validation_error_path(output_path)
    os.makedirs(os.path.dirname(error_path), exist_ok=True)
    with open(error_path, "w", encoding="utf-8") as f:
        json.dump({"errors": errors}, f, ensure_ascii=False, indent=2)
    return error_path


def clear_validation_errors(output_path):
    error_path = os.path.abspath(validation_error_path(output_path))
    output_dir = os.path.dirname(os.path.abspath(output_path))
    if os.path.basename(error_path) != "review_validation_errors.json":
        return
    if os.path.dirname(error_path) != output_dir:
        return
    if os.path.exists(error_path):
        os.remove(error_path)


def write_validation_pass(data_file_path, output_path, stage, session_root, runtime_skills):
    pass_path = validation_pass_path(output_path)
    os.makedirs(os.path.dirname(pass_path), exist_ok=True)
    payload = {
        "status": "passed",
        "stage": stage,
        "data_path": os.path.abspath(data_file_path) if data_file_path else "",
        "session_root": session_root,
        "runtime_loaded_skills": sorted(runtime_skills),
    }
    with open(pass_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return pass_path


def validate_evidence_contract(data, data_file_path="", output_path="", cwd=None):
    session_root = infer_session_root(data_file_path, output_path, cwd)
    errors = []
    evidence_mode = data.get("evidence_mode")
    novelty = data.get("novelty_conclusion")
    inventive = data.get("inventive_step_conclusion")
    loaded_skills = set(data.get("loaded_skills") or [])
    runtime_skills = actual_loaded_skills(session_root)
    enforce_runtime_skills = has_session_runtime_records(session_root)

    def require_loaded_skill(skill_name, message):
        if skill_name not in loaded_skills:
            errors.append(message)
        elif enforce_runtime_skills and skill_name not in runtime_skills:
            errors.append(f"{message} session.runtime.json/turn_context_index.json 中未记录实际加载 {skill_name}。")

    if not evidence_mode:
        errors.append("缺少 evidence_mode，无法判断是否完成官方技能证据链。")
    if evidence_mode == "degraded":
        errors.append("evidence_mode=degraded 不允许生成最终 Word；请补齐证据链或改为经用户确认的 document_only。")

    if evidence_mode == "document_only":
        if data.get("document_only_confirmed") is not True:
            errors.append("document_only 必须设置 document_only_confirmed=true，表示用户明确确认跳过外部检索/官方技能。")
        if novelty != "uncertain":
            errors.append("document_only 下 novelty_conclusion 只能为 uncertain。")
        if inventive != "uncertain":
            errors.append("document_only 下 inventive_step_conclusion 只能为 uncertain。")
        return errors, session_root, runtime_skills

    if evidence_mode == "full":
        require_loaded_skill("novelty-check", "evidence_mode=full 时 loaded_skills 必须包含 novelty-check。")
        if novelty not in {"novelty_rejected", "novelty_preserved", "uncertain"}:
            errors.append("novelty_conclusion 必须为 novelty_rejected/novelty_preserved/uncertain。")
        if not has_existing_reference(data, ["D1"], session_root, cwd):
            errors.append("evidence_mode=full 时 fetched_references 必须包含一个已 fetch/read 的 D1 原文路径。")
        errors.extend(validate_d1_selection_rationale(data, session_root, cwd))

        for filename in NOVELTY_ARTIFACTS:
            if not existing_nonempty_path(artifact_candidates(data, filename, "novelty"), session_root, cwd):
                errors.append(f"缺少 novelty-check 官方产物或文件为空：{filename}")

        if novelty != "novelty_rejected":
            require_loaded_skill("non-obviousness-check", "新颖性未被否定时，loaded_skills 必须包含 non-obviousness-check。")
            if inventive not in {"strong", "weak", "uncertain"}:
                errors.append("inventive_step_conclusion 必须为 strong/weak/uncertain。")
            for filename in NON_OBVIOUSNESS_ARTIFACTS:
                if not existing_nonempty_path(artifact_candidates(data, filename, "non_obviousness"), session_root, cwd):
                    errors.append(f"缺少 non-obviousness-check 官方产物或文件为空：{filename}")
            if inventive in {"strong", "weak"}:
                d2d3_paths = existing_reference_paths(data, ["D2", "D3"], session_root, cwd)
                if not d2d3_paths:
                    errors.append("inventive_step_conclusion 为 strong/weak 时，fetched_references 必须包含至少一个已 fetch/read 的 D2 或 D3 原文路径。")
                else:
                    newest_reference_mtime = max(os.path.getmtime(path) for path in d2d3_paths)
                    for filename in NON_OBVIOUSNESS_D2D3_ARTIFACTS:
                        artifact_path = existing_nonempty_path(
                            artifact_candidates(data, filename, "non_obviousness"),
                            session_root,
                            cwd,
                        )
                        if not artifact_path:
                            continue
                        if os.path.getmtime(artifact_path) + 1 < newest_reference_mtime:
                            errors.append(f"{filename} 早于 D2/D3 原文读取时间，需在 fetch/read D2/D3 后重写 non-obviousness-check 产物。")
                        if artifact_has_unread_reference_marker(artifact_path):
                            errors.append(f"{filename} 仍包含 D2/D3 未阅读全文的表述，不能支撑 strong/weak 结论。")

    return errors, session_root, runtime_skills

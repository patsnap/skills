#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

REQUIRED = ["task_id", "task_object", "business_goal", "mode", "state", "record_id_field", "dimensions"]
MODES = {"discovery", "semi_open", "closed"}
STATES = {
    "pending_validation", "diagnosing", "awaiting_scope_confirmation", "building_assets",
    "piloting", "awaiting_freeze_confirmation", "frozen",
    # Legacy states remain valid for resumability of tasks created before v1.1.
    "awaiting_mode_confirmation", "awaiting_taxonomy_confirmation", "awaiting_pilot_confirmation",
    "awaiting_full_run_authorization", "labeling", "validating", "awaiting_review", "completed"
}

def load_config(path: Path):
    text = path.read_text(encoding="utf-8-sig")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            import yaml
        except ImportError as exc:
            raise SystemExit("Config is not JSON-compatible YAML and PyYAML is unavailable") from exc
        return yaml.safe_load(text)

def main():
    parser = argparse.ArgumentParser(description="Validate an evidence-based labeling task config")
    parser.add_argument("config", type=Path)
    args = parser.parse_args()
    data = load_config(args.config)
    errors = []
    if not isinstance(data, dict):
        errors.append("config must be an object")
    else:
        for key in REQUIRED:
            if key not in data or data[key] in (None, "", []):
                errors.append(f"missing required value: {key}")
        if data.get("mode") not in MODES:
            errors.append(f"mode must be one of {sorted(MODES)}")
        if data.get("state") not in STATES:
            errors.append(f"state must be one of {sorted(STATES)}")
        if data.get("mode") == "closed" and data.get("allow_candidate_labels"):
            errors.append("closed mode cannot allow candidate labels")
        if data.get("preserve_original_columns") is False:
            errors.append("preserve_original_columns must remain true unless explicitly approved")
        gated_states = {"frozen", "awaiting_full_run_authorization", "labeling", "validating", "awaiting_review", "completed"}
        full_run_states = {"labeling", "validating", "awaiting_review", "completed"}
        confirmations = data.get("confirmations") or {}
        scope_confirmed = confirmations.get("scope_confirmed") is True or all(
            confirmations.get(key) is True for key in ("goal_unit_dimensions", "mode_confirmed")
        )
        freeze_confirmed = confirmations.get("freeze_approved") is True or all(
            confirmations.get(key) is True for key in ("taxonomy_frozen", "pilot_approved")
        )
        if data.get("state") not in {"pending_validation", "diagnosing", "awaiting_scope_confirmation", "awaiting_mode_confirmation"}:
            if not scope_confirmed:
                errors.append("scope gate confirmation is required")
        if data.get("state") in gated_states:
            if data.get("mode") != "closed":
                errors.append("frozen and downstream states require closed mode")
            if not freeze_confirmed:
                errors.append("freeze gate confirmation is required")
        if data.get("state") in full_run_states:
            if confirmations.get("full_run_authorized") is not True:
                errors.append("full_run_authorized confirmation is required")
            if str(data.get("taxonomy_version", "")).lower().startswith("draft"):
                errors.append("full run cannot use a draft taxonomy version")
    report = {"valid": not errors, "errors": errors}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not errors else 1)

if __name__ == "__main__":
    main()

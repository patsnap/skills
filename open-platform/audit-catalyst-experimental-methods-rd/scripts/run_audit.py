#!/usr/bin/env python3
"""Deterministic catalyst preparation/evaluation scheme audit.

v0.4.1 changes:
- No runtime third-party dependency for DOCX read/write/validation.
- All outputs are written only to the selected output directory, which is reset at start.
- Stable sample-name filtering to avoid gas atmosphere/solvent/equipment being treated as samples.
- More professional preparation-step operation classification.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import html
import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List

SKILL_VERSION = "0.5.0"
REPORT_TITLE = "Catalyst Preparation and Evaluation Method Audit Report"
HTML_NAME = "Catalyst Preparation and Evaluation Method Audit Report.html"
DOCX_NAME = "Catalyst Preparation and Evaluation Method Audit Report.docx"

LEVEL_LABEL = {"HIGH": "Critical issue", "MEDIUM": "Material issue", "LOW": "Documentation issue"}
JUDGMENT_LABEL = {
    "SUFFICIENT": "Sufficient",
    "PARTIAL": "Partially specified—additional detail required",
    "INSUFFICIENT": "Insufficient to support the requirement",
    "NOT_APPLICABLE": "Not applicable",
}
DIM_LABEL = {
    "preparation_executability": "Preparation executability",
    "variable_attribution": "Variable design and attribution",
    "controls_and_baselines": "Controls and baselines",
    "evaluation_reliability": "Evaluation conditions and data reliability",
    "claim_validation_linkage": "Claim-to-evidence linkage",
}

ISSUE_CATALOG: Dict[str, Dict[str, str]] = {
    "PREP_MISSING_HYDROTHERMAL_FILLING": {
        "dimension": "preparation_executability",
        "level": "LOW",
        "title": "Autoclave volume or fill fraction is not specified",
        "recommendation": "Specify vessel and liner material, rated volume, charge volume, and fill fraction.",
    },
    "PREP_MISSING_CALCINATION_RAMP": {
        "dimension": "preparation_executability",
        "level": "LOW",
        "title": "Calcination ramp is not specified",
        "recommendation": "Specify the heating rate, dwell, atmosphere, and cooling method.",
    },
    "PREP_MISSING_REDUCTION_FLOW": {
        "dimension": "preparation_executability",
        "level": "MEDIUM",
        "title": "Reduction flow or space velocity is not specified",
        "recommendation": "Specify gas composition and flow, space velocity or sample charge, and temperature program.",
    },
    "PREP_MISSING_SEPARATION_DETAIL": {
        "dimension": "preparation_executability",
        "level": "LOW",
        "title": "Separation conditions are not specified",
        "recommendation": "Specify RCF or rotor/rpm, duration, temperature, or filter-medium specification.",
    },
    "SAMPLE_NO_BASELINE": {
        "dimension": "controls_and_baselines",
        "level": "HIGH",
        "title": "Comparable baseline or control is absent",
        "recommendation": "Add a justified unmodified, conventional, commercial, or literature baseline under comparable conditions.",
    },
    "SAMPLE_NO_BLANK_SUPPORT": {
        "dimension": "controls_and_baselines",
        "level": "MEDIUM",
        "title": "Support-only or no-active-component control is absent",
        "recommendation": "Add a support-only or no-active-component sample to isolate the active-component contribution.",
    },
    "SAMPLE_NAMING_NOT_TRACEABLE": {
        "dimension": "variable_attribution",
        "level": "LOW",
        "title": "Sample naming is not traceable to design variables",
        "recommendation": "Add a sample register mapping every identifier to variables, preparation differences, and batch lineage.",
    },
    "EVAL_MISSING_REACTION_CONDITIONS": {
        "dimension": "evaluation_reliability",
        "level": "HIGH",
        "title": "Catalytic evaluation conditions are absent",
        "recommendation": "Specify reaction, reactor, catalyst charge, feed, temperature, pressure, flow or space velocity, pretreatment, and analysis.",
    },
    "EVAL_MISSING_ANALYTICAL_METHOD": {
        "dimension": "evaluation_reliability",
        "level": "MEDIUM",
        "title": "Quantitative analytical method is not specified",
        "recommendation": "Specify the quantitative method, detector, calibration, internal standard or response factor, and quality controls.",
    },
    "EVAL_MISSING_REPEAT_ERROR": {
        "dimension": "evaluation_reliability",
        "level": "MEDIUM",
        "title": "Replication and uncertainty are not specified",
        "recommendation": "Define independent replication, uncertainty representation, and outlier handling.",
    },
    "EVAL_MISSING_BALANCE": {
        "dimension": "evaluation_reliability",
        "level": "MEDIUM",
        "title": "Material or elemental balance is not specified",
        "recommendation": "Define the applicable material or elemental balance, calculation basis, and acceptance criterion.",
    },
    "CHAR_MISSING_PREPARATION_VERIFICATION": {
        "dimension": "claim_validation_linkage",
        "level": "MEDIUM",
        "title": "Catalyst formation and structure are not verified",
        "recommendation": "Select claim-relevant methods to verify composition, phase, loading, oxidation state, morphology, and surface area.",
    },
    "CLAIM_NO_METRIC": {
        "dimension": "claim_validation_linkage",
        "level": "HIGH",
        "title": "Performance claim lacks a measurable endpoint",
        "recommendation": "Map each claim to a measurable endpoint with units, basis, comparator, and acceptance criterion.",
    },
    "CLAIM_STABILITY_NO_TOS": {
        "dimension": "claim_validation_linkage",
        "level": "HIGH",
        "title": "Stability claim lacks duration or cycling design",
        "recommendation": "Add justified time-on-stream or cycling, regeneration assessment, and before/after characterization.",
    },
}

STEP_KEYWORDS = [
    "weigh", "dissolve in", "dissolve", "obtain solution", "mix", "add", "add dropwise", "stir", "transfer", "hydrothermal", "hold", "cool", "centrifuge", "wash", "dry", "grind", "calcine", "calcine", "reduce", "label", "name", "denote", "impregnate", "filter", "age", "evaporate",
    "dissolved", "mixed", "stir", "hydrothermal", "centrifug", "washed", "dried", "calcined", "reduced", "impregnated", "denoted",
]
EVAL_KEYWORDS = ["catalytic evaluation", "reaction evaluation", "fixed-bed", "reactor", "conversion", "selectivity", "yield", "space velocity", "GHSV", "WHSV", "GC", "HPLC", "TCD", "FID", "product analysis"]
CHAR_KEYWORDS = ["XRD", "XPS", "TEM", "SEM", "BET", "TPR", "TPD", "DRIFTS", "Mössbauer", "Raman", "Raman", "ICP", "XRF", "characterization"]
CLAIM_KEYWORDS = ["improve", "increase", "decrease", "enhance", "improve", "stable", "deactivation resistance", "selectivity", "activity", "yield", "conversion", "mechanism", "active site"]
CONTROL_KEYWORDS = ["control", "comparison", "baseline", "supported", "blank", "unmodified", "commercial", "reference", "control", "baseline"]

NON_SAMPLE_EXACT = {
    "H2/Ar", "H₂/Ar", "N2/Ar", "N₂/Ar", "H2/N2", "H₂/N₂", "CO/H2", "CO/H₂", "CO2/H2", "CO₂/H₂",
    "deionized water", "anhydrous ethanol", "air", "tube furnace", "muffle furnace", "solution A", "solution B",
}
NON_SAMPLE_PATTERNS = [
    r"^\d+%?\s*(H2|H₂|N2|N₂|Ar|CO|CO2|CO₂)(/|:)(H2|H₂|N2|N₂|Ar|CO|CO2|CO₂)$",
    r"^(H2|H₂|N2|N₂|Ar|CO|CO2|CO₂|air|hydrogen|nitrogen)$",
    r"^\d+(\.\d+)?\s*(mL|ml|g|mg|h|min|°C|℃)$",
]
OPERATION_CATEGORIES = [
    ("reduce", ["reduce", "reduction", "reduced", "H2", "H₂"]),
    ("calcine/calcine", ["calcine", "calcine", "calcination", "calcined", "muffle furnace", "muffle"]),
    ("Hydrothermal treatment", ["hydrothermal", "hydrothermal", "autoclave", "autoclave"]),
    ("impregnate", ["impregnate", "impregnation", "impregnated"]),
    ("evaporate/age", ["evaporate", "age", "evaporat", "aging", "aged"]),
    ("Solid-liquid separation/washing", ["centrifuge", "filter", "wash", "centrifug", "filter", "wash"]),
    ("dry", ["dry", "dried", "drying"]),
    ("grind", ["grind", "grind", "ground"]),
    ("mix/stir", ["mix", "stir", "add", "add dropwise", "mixed", "stir"]),
    ("Precursor dissolution", ["weigh", "dissolve in", "dissolve", "obtain solution", "dissolved"]),
    ("Sample naming", ["label", "name", "denote", "denoted"]),
]


def read_input(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md", ".csv", ".json"}:
        return path.read_text(encoding="utf-8", errors="ignore")
    if suffix in {".html", ".htm"}:
        raw = path.read_text(encoding="utf-8", errors="ignore")
        raw = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.I | re.S)
        return html.unescape(re.sub(r"<[^>]+>", "\n", raw))
    if suffix == ".pdf":
        try:
            import fitz  # type: ignore
            with fitz.open(path) as doc:
                return "\n".join(page.get_text("text") for page in doc)
        except Exception as exc:
            raise RuntimeError(f"Unable to read PDF text; transcribe it or export text first: {exc}") from exc
    if suffix == ".docx":
        return read_docx_text(path)
    raise RuntimeError(f"Unsupported input format: {suffix}. Convert it to txt, md, docx, or text-readable PDF.")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def read_docx_text(path: Path) -> str:
    """Read DOCX text using only Python standard library."""
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    try:
        with zipfile.ZipFile(path) as zf:
            xml_data = zf.read("word/document.xml")
    except Exception as exc:
        raise RuntimeError(f"Unable to read the Word document; confirm that it is a valid .docx file: {exc}") from exc
    root = ET.fromstring(xml_data)
    blocks: List[str] = []
    for para in root.findall(".//w:p", ns):
        texts = [node.text or "" for node in para.findall(".//w:t", ns)]
        line = "".join(texts).strip()
        if line:
            blocks.append(line)
    return "\n".join(blocks)


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("℃", " °C ").replace("ºC", " °C ")).strip()


def is_non_sample_name(name: str) -> bool:
    compact = re.sub(r"\s+", "", name)
    if compact in NON_SAMPLE_EXACT:
        return True
    for pattern in NON_SAMPLE_PATTERNS:
        if re.match(pattern, compact, flags=re.I):
            return True
    gas_tokens = {"H2", "H₂", "N2", "N₂", "Ar", "CO", "CO2", "CO₂"}
    pieces = re.split(r"[/:-]", compact)
    if len(pieces) >= 2 and all(piece in gas_tokens or re.match(r"^\d+%?$", piece) for piece in pieces):
        return True
    return False


def classify_operation(text: str) -> str:
    for label, kws in OPERATION_CATEGORIES:
        if any(re.search(re.escape(kw), text, flags=re.I) for kw in kws):
            return label
    return "Operation"


def diagnose_material(text: str) -> Dict[str, str]:
    t = normalize_text(text)
    step_hits = sum(1 for kw in STEP_KEYWORDS if kw in t)
    eval_hits = sum(1 for kw in EVAL_KEYWORDS if kw in t)
    if len(t) < 80 or step_hits < 2:
        return {
            "material_type": "Insufficient material",
            "audit_mode": "Insufficient-material notice",
            "confidence": "Medium",
            "scope_statement": "The input lacks sufficient catalyst preparation or evaluation detail; the report can only identify required additions.",
        }
    if step_hits >= 5 and eval_hits >= 3:
        return {
            "material_type": "Complete preparation and evaluation plan",
            "audit_mode": "Full audit",
            "confidence": "High",
            "scope_statement": "The material contains preparation and catalytic-evaluation information and supports a full audit of execution, controls, evaluation, and validation.",
        }
    if step_hits >= 5:
        return {
            "material_type": "Preparation-step method",
            "audit_mode": "Preparation-method audit",
            "confidence": "High",
            "scope_statement": "The material is preparation-focused; review executability, sample/control relationships, and missing evaluation conditions.",
        }
    return {
        "material_type": "R&D concept or early draft",
        "audit_mode": "Draft-level audit",
        "confidence": "Medium",
        "scope_statement": "The material expresses an R&D concept but lacks complete preparation and evaluation conditions; apply a draft-level audit.",
    }


def split_steps(text: str) -> List[Dict[str, Any]]:
    raw_parts = re.split(r"(?<=[.；;])\s*|\n+", text)
    steps: List[Dict[str, Any]] = []
    for part in raw_parts:
        p = part.strip()
        if not p:
            continue
        if any(kw in p for kw in STEP_KEYWORDS):
            conditions = {
                "temperature": bool(re.search(r"\d+\s*°C|\d+\s*℃", p)),
                "time": bool(re.search(r"\d+(\.\d+)?\s*(h|h|min|min|s|s)", p, flags=re.I)),
                "mass": bool(re.search(r"\d+(\.\d+)?\s*(mg|g|kg|mg|g)", p, flags=re.I)),
                "volume": bool(re.search(r"\d+(\.\d+)?\s*(mL|ml|L|μL|uL|mL|L)", p, flags=re.I)),
                "atmosphere": bool(re.search(r"air|H2|H₂|Ar|N2|N₂|oxygen|nitrogen|hydrogen|CO", p)),
            }
            steps.append({
                "step_id": f"S{len(steps)+1:02d}",
                "operation": classify_operation(p),
                "raw_text": p,
                "conditions": conditions,
                "missing_fields": [],
            })
    return steps


def extract_samples(text: str) -> List[Dict[str, str]]:
    samples: List[Dict[str, str]] = []
    pattern = r"[A-Za-z][A-Za-z0-9]*(?:[@/\-][A-Za-z0-9]+)+(?:\-[A-Za-z0-9]+)?"
    found: List[str] = []
    for m in re.finditer(pattern, text):
        value = m.group(0).strip()
        if len(value) < 4 or is_non_sample_name(value):
            continue
        if value not in found:
            found.append(value)
    for idx, name in enumerate(found[:20], 1):
        samples.append({"sample_id": f"C{idx:02d}", "sample_name": name, "role": infer_sample_role(name, text)})
    return samples


def infer_sample_role(name: str, text: str) -> str:
    windows: List[str] = []
    exact_pattern = r"(?<![A-Za-z0-9@/\-])" + re.escape(name) + r"(?![A-Za-z0-9@/\-])"
    for m in re.finditer(exact_pattern, text):
        pos = m.start()
        windows.append(text[max(0, pos - 100): pos + 140])
    joined = "\n".join(windows)
    if name.endswith("-C"):
        return "Post-calcination intermediate"
    # Control words must be directly attached to this exact sample name, not merely appear later in the same sentence.
    if re.search(exact_pattern + r"\s*(control|baseline|control|baseline|comparison)", joined, re.I) or re.search(r"(control|baseline|control|baseline|comparison)\s*" + exact_pattern, joined, re.I):
        return "Control or baseline"
    if re.search(rf"(obtain|obtain|label as|name as|denote)\s*{re.escape(name)}", joined):
        return "Target sample"
    return "Not specified"


def has_keyword(text: str, keywords: List[str]) -> bool:
    return any(k in text for k in keywords)


def add_issue(issues: List[Dict[str, str]], issue_id: str, basis: str) -> None:
    if any(i["issue_id"] == issue_id for i in issues):
        return
    item = ISSUE_CATALOG[issue_id]
    issues.append({
        "issue_id": issue_id,
        "dimension": item["dimension"],
        "dimension_label": DIM_LABEL[item["dimension"]],
        "level": item["level"],
        "level_label": LEVEL_LABEL[item["level"]],
        "title": item["title"],
        "basis": basis,
        "recommendation": item["recommendation"],
    })


def generate_issues(text: str, steps: List[Dict[str, Any]], samples: List[Dict[str, str]]) -> List[Dict[str, str]]:
    t = normalize_text(text)
    issues: List[Dict[str, str]] = []

    if re.search(r"hydrothermal|hydrothermal|autoclave|autoclave", t, re.I):
        if not re.search(r"fill fraction|charge volume|vessel volume|\d+\s*mL\s*(autoclave|autoclave)|autoclave volume", t, re.I):
            add_issue(issues, "PREP_MISSING_HYDROTHERMAL_FILLING", "The method includes a hydrothermal/autoclave step but does not specify vessel size, charge volume, or fill fraction.")
    if re.search(r"calcine|calcine|calcination|calcined|muffle", t, re.I):
        if not re.search(r"heating rate|ramp|°C\s*(?:/|per)?\s*min", t, re.I):
            add_issue(issues, "PREP_MISSING_CALCINATION_RAMP", "The method includes calcination but does not specify the heating rate.")
    if re.search(r"reduce|reduction|reduced|H2|H₂", t, re.I):
        if not re.search(r"mL\s*min|ml\s*min|flow|space velocity|GHSV|WHSV|sccm", t, re.I):
            add_issue(issues, "PREP_MISSING_REDUCTION_FLOW", "The method includes reduction conditions but does not specify gas flow or space velocity.")
    if re.search(r"centrifuge|centrifug", t, re.I):
        if not re.search(r"rpm|r/min|speed|\d+\s*min|min", t, re.I):
            add_issue(issues, "PREP_MISSING_SEPARATION_DETAIL", "The method includes centrifugation but does not specify RCF/rpm or duration.")

    if not has_keyword(t, CONTROL_KEYWORDS):
        add_issue(issues, "SAMPLE_NO_BASELINE", "No explicit control, baseline, unmodified sample, or commercial/literature comparator was identified.")
    else:
        if re.search(r"Pd|Pt|Ru|Co|Fe|Ni|Mo|Cu|Rh", t) and not re.search(r"blank|no\\s*(Pd|Pt|Ru|Co|Fe|Ni)|bare|support-only|support-only", t, re.I):
            add_issue(issues, "SAMPLE_NO_BLANK_SUPPORT", "An active-metal catalyst and comparator were identified, but no support-only or no-active-component control was found.")
    if samples and not any(s["role"] in {"Target sample", "Control or baseline"} for s in samples):
        add_issue(issues, "SAMPLE_NAMING_NOT_TRACEABLE", "Sample identifiers were found, but their relationship to design variables is not traceable.")

    has_eval = has_keyword(t, EVAL_KEYWORDS)
    if not has_eval:
        add_issue(issues, "EVAL_MISSING_REACTION_CONDITIONS", "The material is preparation-focused; no sufficient reaction, reactor, feed, temperature, pressure, or analytical conditions were identified.")
    else:
        if not re.search(r"GC|HPLC|MS|TCD|FID|chromatography|detector|calibration curve|internal standard", t, re.I):
            add_issue(issues, "EVAL_MISSING_ANALYTICAL_METHOD", "Catalytic evaluation is mentioned, but the quantitative product-analysis method is not specified.")
    if not re.search(r"replicate|parallel|error|standard deviation|error|standard deviation|n\s*=", t, re.I):
        add_issue(issues, "EVAL_MISSING_REPEAT_ERROR", "No independent replication, error representation, or uncertainty control was identified.")
    if has_eval and not re.search(r"carbon balance|material balance|mass balance|halogen balance|carbon balance|mass balance", t, re.I):
        add_issue(issues, "EVAL_MISSING_BALANCE", "Reaction evaluation is mentioned, but no material or elemental balance requirement is specified.")

    if re.search(r"doped|supported|single-atom|phase|oxidation state|pore|morphology|oxygen vacancy|hydrophobicity|hydroxyl|facet|active phase|active site", t, re.I):
        if not has_keyword(t, CHAR_KEYWORDS):
            add_issue(issues, "CHAR_MISSING_PREPARATION_VERIFICATION", "The material makes catalyst structure, composition, or active-site statements without a corresponding characterization plan.")
    if has_keyword(t, CLAIM_KEYWORDS):
        if not re.search(r"conversion|selectivity|yield|TOF|STY|stability|TOS|retention|activity|yield|yield|conversion|selectivity", t, re.I):
            add_issue(issues, "CLAIM_NO_METRIC", "A performance-improvement statement lacks a corresponding quantitative endpoint.")
        if re.search(r"stable|deactivation resistance|robust|stable|deactivation", t, re.I) and not re.search(r"TOS|time on stream|continuous|cycling|regeneration|\d+\s*h", t, re.I):
            add_issue(issues, "CLAIM_STABILITY_NO_TOS", "A stability or deactivation-resistance claim lacks time-on-stream, cycling, or regeneration evaluation.")

    level_rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    return sorted(issues, key=lambda x: (level_rank[x["level"]], x["dimension"], x["issue_id"]))


def summarize(issues: List[Dict[str, str]]) -> Dict[str, Any]:
    counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for issue in issues:
        counts[issue["level"]] += 1
    if counts["HIGH"]:
        overall = "The design is partially specified but contains critical issues affecting execution or support for conclusions."
        judgment = "PARTIAL"
    elif counts["MEDIUM"]:
        overall = "The main method is identifiable, but material conditions require additional specification."
        judgment = "PARTIAL"
    elif issues:
        overall = "The method is generally clear; remaining issues concern operational detail."
        judgment = "SUFFICIENT"
    else:
        overall = "No explicit omission was detected; review against the actual apparatus and institutional procedures."
        judgment = "SUFFICIENT"
    return {
        "high_count": counts["HIGH"],
        "medium_count": counts["MEDIUM"],
        "low_count": counts["LOW"],
        "total_count": len(issues),
        "overall_judgment": judgment,
        "overall_judgment_label": JUDGMENT_LABEL[judgment],
        "overall_opinion": overall,
    }


def infer_catalyst_system(text: str, samples: List[Dict[str, str]]) -> str:
    if samples:
        return ", ".join(s["sample_name"] for s in samples[:6])
    m = re.search(r"([A-Z][a-z]?[A-Za-z0-9@/\-]+\s*catalyst)", text)
    if m:
        return m.group(1)
    return "Not specified"


def extract_claims(text: str) -> List[Dict[str, str]]:
    claims = []
    parts = re.split(r"(?<=[.；;])\s*|\n+", text)
    for p in parts:
        if any(k in p for k in CLAIM_KEYWORDS) and len(p.strip()) > 8:
            claims.append({"claim_id": f"P{len(claims)+1:02d}", "text": p.strip()[:240]})
        if len(claims) >= 8:
            break
    return claims


def build_context(input_path: Path, text: str) -> Dict[str, Any]:
    material = diagnose_material(text)
    steps = split_steps(text)
    samples = extract_samples(text)
    issues = generate_issues(text, steps, samples)
    summary = summarize(issues)
    eval_detected = has_keyword(normalize_text(text), EVAL_KEYWORDS)
    context = {
        "meta": {
            "skill_version": SKILL_VERSION,
            "input_file": input_path.name,
            "input_sha256": sha256(input_path),
            "report_title": REPORT_TITLE,
            "generated_at": _dt.datetime.now().isoformat(timespec="seconds"),
        },
        "material_profile": material,
        "extracted_elements": {
            "catalyst_system": infer_catalyst_system(text, samples),
            "preparation_steps": steps,
            "sample_design": samples,
            "evaluation_plan": {"detected": eval_detected, "summary": "Catalytic-evaluation content was identified." if eval_detected else "No catalytic-evaluation conditions were identified."},
            "claims": extract_claims(text),
        },
        "audit_issues": issues,
        "computed_summary": summary,
    }
    return context


def render_dimension_sections_html(issues: List[Dict[str, str]]) -> str:
    blocks = []
    for dim, zh in DIM_LABEL.items():
        dim_issues = [i for i in issues if i["dimension"] == dim]
        if dim_issues:
            lis = "".join(f"<li>{html.escape(i['level_label'])}: {html.escape(i['title'])}</li>" for i in dim_issues)
            opinion = f"<ul>{lis}</ul>"
        else:
            opinion = "<p>No explicit omission was detected in this dimension.</p>"
        blocks.append(f"<h3>{html.escape(zh)}</h3>{opinion}")
    return "\n".join(blocks)


def render_recommendations_html(issues: List[Dict[str, str]]) -> str:
    if not issues:
        return "<p>Retain complete raw data and operation records under institutional laboratory-record requirements.</p>"
    return "<ol>" + "".join(f"<li>{html.escape(i['recommendation'])}</li>" for i in issues[:10]) + "</ol>"


def render_html(context: Dict[str, Any]) -> str:
    meta = context["meta"]
    material = context["material_profile"]
    summary = context["computed_summary"]
    issues = context["audit_issues"]
    elements = context["extracted_elements"]

    def esc(x: Any) -> str:
        return html.escape(str(x))

    issue_rows = "\n".join(
        f"<tr><td>{i+1}</td><td>{esc(it['level_label'])}</td><td>{esc(it['dimension_label'])}</td><td>{esc(it['title'])}</td><td>{esc(it['basis'])}</td><td>{esc(it['recommendation'])}</td></tr>"
        for i, it in enumerate(issues)
    ) or "<tr><td colspan='6'>No explicit issue was identified.</td></tr>"
    step_rows = "\n".join(
        f"<tr><td>{esc(s['step_id'])}</td><td>{esc(s['operation'])}</td><td>{esc(s['raw_text'])}</td></tr>"
        for s in elements["preparation_steps"]
    ) or "<tr><td colspan='3'>No preparation step was identified.</td></tr>"
    sample_rows = "\n".join(
        f"<tr><td>{esc(s['sample_id'])}</td><td>{esc(s['sample_name'])}</td><td>{esc(s['role'])}</td></tr>"
        for s in elements["sample_design"]
    ) or "<tr><td colspan='3'>No sample identifier was identified.</td></tr>"

    css = """
    body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;background:#f6f7f9;color:#111827;margin:0;}
    .page{max-width:1120px;margin:0 auto;padding:32px;}
    .card{background:white;border:1px solid #e5e7eb;border-radius:12px;padding:22px;margin:18px 0;box-shadow:0 4px 16px rgba(15,23,42,.04)}
    h1{font-size:30px;margin:0 0 10px;} h2{font-size:22px;margin-top:0;border-left:5px solid #009BA4;padding-left:10px;} h3{font-size:18px;margin-bottom:8px;}
    .meta{color:#4b5563;font-size:14px;line-height:1.8}.summary{display:flex;gap:12px;flex-wrap:wrap}.pill{padding:10px 14px;border-radius:10px;background:#eef2ff;border:1px solid #dbe3ff}.high{background:#fee2e2}.medium{background:#fef3c7}.low{background:#e0f2fe}
    table{border-collapse:collapse;width:100%;font-size:14px;}th,td{border:1px solid #e5e7eb;padding:10px;vertical-align:top;}th{background:#f3f4f6;text-align:left}.opinion{font-size:17px;line-height:1.75}.small{font-size:13px;color:#6b7280;}
    """
    return f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{esc(meta['report_title'])}</title><style>{css}</style></head><body><div class='page'>
    <div class='card'><h1>{esc(meta['report_title'])}</h1><div class='meta'>Material reviewed: {esc(meta['input_file'])}<br>Skill version: {esc(meta['skill_version'])}<br>Input fingerprint: {esc(meta['input_sha256'][:16])}...</div></div>
    <div class='card'><h2>1. Material and classification</h2><p class='opinion'>Material classification: <strong>{esc(material['material_type'])}</strong>; audit mode: <strong>{esc(material['audit_mode'])}</strong>; classification confidence: {esc(material['confidence'])}.</p><p>{esc(material['scope_statement'])}</p></div>
    <div class='card'><h2>2. Overall audit conclusion</h2><div class='summary'><div class='pill'>Overall judgment: {esc(summary['overall_judgment_label'])}</div><div class='pill high'>Critical issues: {summary['high_count']}</div><div class='pill medium'>Material issues: {summary['medium_count']}</div><div class='pill low'>Documentation issues: {summary['low_count']}</div></div><p class='opinion'>{esc(summary['overall_opinion'])}</p></div>
    <div class='card'><h2>3. Priority issues</h2><table><thead><tr><th>No.</th><th>Issue level</th><th>Audit dimension</th><th>Issue</th><th>Basis</th><th>Required addition</th></tr></thead><tbody>{issue_rows}</tbody></table></div>
    <div class='card'><h2>4. Dimension-level findings</h2>{render_dimension_sections_html(issues)}</div>
    <div class='card'><h2>5. Preparation-step register</h2><table><thead><tr><th>Step ID</th><th>Operation</th><th>Source text</th></tr></thead><tbody>{step_rows}</tbody></table></div>
    <div class='card'><h2>6. Sample and variable register</h2><table><thead><tr><th>Sample ID</th><th>Sample identifier</th><th>Role</th></tr></thead><tbody>{sample_rows}</tbody></table></div>
    <div class='card'><h2>7. Required additions</h2>{render_recommendations_html(issues)}</div>
    <div class='card'><h2>8. Audit limitations</h2><p class='small'>This report applies fixed audit dimensions and rules. For screenshots or scans, result stability depends on transcription consistency. It supports method improvement and pre-experiment review; it does not replace specialist judgment or EHS approval.</p></div>
    </div></body></html>"""


def xml_escape(text: Any) -> str:
    return html.escape(str(text), quote=False)


def w_p(text: Any = "", style: str | None = None) -> str:
    style_xml = f"<w:pPr><w:pStyle w:val=\"{style}\"/></w:pPr>" if style else ""
    return f"<w:p>{style_xml}<w:r><w:t>{xml_escape(text)}</w:t></w:r></w:p>"


def w_tbl(rows: List[List[Any]]) -> str:
    out = ["<w:tbl><w:tblPr><w:tblStyle w:val=\"TableGrid\"/><w:tblW w:w=\"0\" w:type=\"auto\"/><w:tblBorders><w:top w:val=\"single\" w:sz=\"4\"/><w:left w:val=\"single\" w:sz=\"4\"/><w:bottom w:val=\"single\" w:sz=\"4\"/><w:right w:val=\"single\" w:sz=\"4\"/><w:insideH w:val=\"single\" w:sz=\"4\"/><w:insideV w:val=\"single\" w:sz=\"4\"/></w:tblBorders></w:tblPr>"]
    for row in rows:
        out.append("<w:tr>")
        for cell in row:
            out.append(f"<w:tc><w:tcPr><w:tcW w:w=\"2400\" w:type=\"dxa\"/></w:tcPr>{w_p(cell)}</w:tc>")
        out.append("</w:tr>")
    out.append("</w:tbl>")
    return "".join(out)


def render_docx(context: Dict[str, Any], out_path: Path) -> None:
    meta = context["meta"]
    material = context["material_profile"]
    summary = context["computed_summary"]
    issues = context["audit_issues"]
    elements = context["extracted_elements"]
    body: List[str] = []
    body.append(w_p(meta["report_title"], "Title"))
    body.append(w_p(f"Material reviewed: {meta['input_file']}"))
    body.append(w_p(f"Skill version: {meta['skill_version']}"))
    body.append(w_p("1. Material and classification", "Heading1"))
    body.append(w_p(f"Material classification: {material['material_type']}; audit mode: {material['audit_mode']}; classification confidence: {material['confidence']}."))
    body.append(w_p(material["scope_statement"]))
    body.append(w_p("2. Overall audit conclusion", "Heading1"))
    body.append(w_p(f"Overall judgment: {summary['overall_judgment_label']}. Critical issues: {summary['high_count']}; material issues: {summary['medium_count']}; documentation issues: {summary['low_count']}."))
    body.append(w_p(summary["overall_opinion"]))
    body.append(w_p("3. Priority issues", "Heading1"))
    rows = [["No.", "Issue level", "Audit dimension", "Issue", "Basis", "Required addition"]]
    if not issues:
        rows.append(["-", "-", "-", "No explicit issue identified", "-", "-"])
    for idx, issue in enumerate(issues, 1):
        rows.append([idx, issue["level_label"], issue["dimension_label"], issue["title"], issue["basis"], issue["recommendation"]])
    body.append(w_tbl(rows))
    body.append(w_p("4. Dimension-level findings", "Heading1"))
    for dim, zh in DIM_LABEL.items():
        body.append(w_p(zh, "Heading2"))
        dim_issues = [i for i in issues if i["dimension"] == dim]
        if dim_issues:
            for issue in dim_issues:
                body.append(w_p(f"{issue['level_label']}: {issue['title']}. {issue['basis']} Required addition: {issue['recommendation']}"))
        else:
            body.append(w_p("No explicit omission was detected in this dimension."))
    body.append(w_p("5. Preparation-step register", "Heading1"))
    step_rows = [["Step ID", "Operation", "Source text"]]
    if not elements["preparation_steps"]:
        step_rows.append(["-", "-", "No preparation step was identified."])
    for step in elements["preparation_steps"]:
        step_rows.append([step["step_id"], step["operation"], str(step["raw_text"])[:600]])
    body.append(w_tbl(step_rows))
    body.append(w_p("6. Sample and variable register", "Heading1"))
    sample_rows = [["Sample ID", "Sample identifier", "Role"]]
    if not elements["sample_design"]:
        sample_rows.append(["-", "No sample identifier was identified", "-"])
    for sample in elements["sample_design"]:
        sample_rows.append([sample["sample_id"], sample["sample_name"], sample["role"]])
    body.append(w_tbl(sample_rows))
    body.append(w_p("7. Required additions", "Heading1"))
    if issues:
        for idx, issue in enumerate(issues[:10], 1):
            body.append(w_p(f"{idx}. {issue['recommendation']}"))
    else:
        body.append(w_p("Retain complete raw data and operation records under institutional laboratory-record requirements."))
    body.append(w_p("Appendix A — Extracted method elements", "Heading1"))
    body.append(w_p(f"Catalyst system / samples: {elements['catalyst_system']}"))
    body.append(w_p(f"Preparation steps identified: {len(elements['preparation_steps'])}"))
    body.append(w_p(f"Samples identified: {len(elements['sample_design'])}"))
    body.append(w_p(f"Evaluation plan: {elements['evaluation_plan']['summary']}"))
    body.append(w_p("Appendix B — Audit rules and judgment basis", "Heading1"))
    body.append(w_p("This report applies fixed dimensions for preparation executability, variable attribution, controls and baselines, evaluation reliability, and claim-to-evidence linkage."))
    body.append(w_p("Issue levels are Critical, Material, and Documentation. A Critical issue can prevent execution, reproduction, valid comparison, or support for a core conclusion."))
    body.append(w_p("Appendix C — Input and version", "Heading1"))
    body.append(w_p(f"Input file: {meta['input_file']}"))
    body.append(w_p(f"Input fingerprint: {meta['input_sha256']}"))
    body.append(w_p(f"Generated at: {meta['generated_at']}"))
    body.append(w_p(f"Skill version: {meta['skill_version']}"))

    document_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>{''.join(body)}<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr></w:body></w:document>'''
    styles_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:rPr><w:rFonts w:ascii="Aptos" w:eastAsia="Aptos"/><w:sz w:val="21"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:rPr><w:b/><w:sz w:val="36"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:rPr><w:b/><w:sz w:val="30"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:rPr><w:b/><w:sz w:val="26"/></w:rPr></w:style><w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/><w:tblPr><w:tblBorders><w:top w:val="single" w:sz="4"/><w:left w:val="single" w:sz="4"/><w:bottom w:val="single" w:sz="4"/><w:right w:val="single" w:sz="4"/><w:insideH w:val="single" w:sz="4"/><w:insideV w:val="single" w:sz="4"/></w:tblBorders></w:tblPr></w:style></w:styles>'''
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>'''
    rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'''
    doc_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>'''
    core = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>{xml_escape(meta['report_title'])}</dc:title><dc:creator>catalyst-method-auditor</dc:creator></cp:coreProperties>'''
    app = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>catalyst-method-auditor</Application></Properties>'''
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", rels)
        zf.writestr("docProps/core.xml", core)
        zf.writestr("docProps/app.xml", app)
        zf.writestr("word/document.xml", document_xml)
        zf.writestr("word/styles.xml", styles_xml)
        zf.writestr("word/_rels/document.xml.rels", doc_rels)


def extract_docx_text(path: Path) -> str:
    return read_docx_text(path)


def validate_outputs(out_dir: Path, context: Dict[str, Any]) -> None:
    html_path = out_dir / HTML_NAME
    docx_path = out_dir / DOCX_NAME
    context_path = out_dir / "report_context.json"
    if not html_path.exists() or not docx_path.exists() or not context_path.exists():
        raise RuntimeError("HTML, Word, or report_context.json is missing.")
    html_text = html_path.read_text(encoding="utf-8", errors="ignore")
    docx_text = extract_docx_text(docx_path)
    required = ["Material and classification", "Overall audit conclusion", "Priority issues", "Dimension-level findings", "Preparation-step register", "Sample and variable register", "Required additions"]
    for sec in required:
        if sec not in html_text:
            raise RuntimeError(f"HTML is missing section: {sec}")
        if sec not in docx_text:
            raise RuntimeError(f"Word is missing section: {sec}")
    for bad in ["{'", "priority':", "None", "Not specified\nAudit mode: Not specified"]:
        if bad in html_text or bad in docx_text:
            raise RuntimeError(f"Report contains unrendered content: {bad}")
    summary = context["computed_summary"]
    expected = f"Critical issues: {summary['high_count']}; material issues: {summary['medium_count']}; documentation issues: {summary['low_count']}"
    if expected not in docx_text:
        raise RuntimeError("Word issue totals do not match the context.")
    if f"Critical issues: {summary['high_count']}" not in html_text:
        raise RuntimeError("HTML issue totals do not match the context.")


def reset_output_dir(out_dir: Path) -> None:
    """Remove only this generator's known artifacts, never an entire directory."""
    resolved = out_dir.resolve()
    filesystem_root = Path(resolved.anchor).resolve()
    if resolved == filesystem_root or resolved == Path.cwd().resolve() or resolved == Path.home().resolve():
        raise RuntimeError("Refusing to use a filesystem, working-directory, or home root as the output directory.")
    if out_dir.exists() and out_dir.is_symlink():
        raise RuntimeError("Refusing to write through a symbolic-link output directory.")
    out_dir.mkdir(parents=True, exist_ok=True)
    for name in (HTML_NAME, DOCX_NAME, "report_context.json"):
        artifact = out_dir / name
        if artifact.is_symlink():
            raise RuntimeError(f"Refusing to replace symbolic-link output: {artifact}")
        if artifact.exists():
            if not artifact.is_file():
                raise RuntimeError(f"Expected a regular output file: {artifact}")
            artifact.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input file path: txt/md/html/pdf/docx")
    parser.add_argument("--out", default="outputs", help="Output directory")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    out_dir = Path(args.out).resolve()
    reset_output_dir(out_dir)

    text = read_input(input_path)
    if not text.strip():
        raise RuntimeError("No usable text was read. For an image or scan, complete a faithful transcription first.")
    context = build_context(input_path, text)
    context_path = out_dir / "report_context.json"
    context_path.write_text(json.dumps(context, ensure_ascii=False, indent=2), encoding="utf-8")

    html_path = out_dir / HTML_NAME
    html_path.write_text(render_html(context), encoding="utf-8")
    docx_path = out_dir / DOCX_NAME
    render_docx(context, docx_path)
    validate_outputs(out_dir, context)
    message = {
        "ok": True,
        "html": str(html_path),
        "docx": str(docx_path),
        "context": str(context_path),
        "completion_message": (
            f"Audit complete. Generated: {HTML_NAME}; {DOCX_NAME}."
            f" Overall judgment: {context['computed_summary']['overall_judgment_label']}."
            f" Critical issues: {context['computed_summary']['high_count']};"
            f" material issues: {context['computed_summary']['medium_count']};"
            f" documentation issues: {context['computed_summary']['low_count']}."
        ),
    }
    print(json.dumps(message, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

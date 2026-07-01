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
import shutil
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List

SKILL_VERSION = "0.4.1"
REPORT_TITLE = "催化剂制备与评价方案审核报告"
HTML_NAME = "催化剂制备与评价方案审核报告.html"
DOCX_NAME = "催化剂制备与评价方案审核报告.docx"

LEVEL_ZH = {"HIGH": "关键问题", "MEDIUM": "重要问题", "LOW": "一般问题"}
JUDGMENT_ZH = {
    "SUFFICIENT": "设计较充分",
    "PARTIAL": "设计基本具备，但需补充完善",
    "INSUFFICIENT": "当前设计不足以支撑要求",
    "NOT_APPLICABLE": "不属于本次审核范围",
}
DIM_ZH = {
    "preparation_executability": "制备步骤可执行性",
    "variable_attribution": "变量设计与归因关系",
    "controls_and_baselines": "对照样与基准样设置",
    "evaluation_reliability": "评价条件与数据可靠性",
    "claim_validation_linkage": "性能主张与验证项目对应关系",
}

ISSUE_CATALOG: Dict[str, Dict[str, str]] = {
    "PREP_MISSING_HYDROTHERMAL_FILLING": {
        "dimension": "preparation_executability",
        "level": "LOW",
        "title": "水热反应釜体积或填充率未说明",
        "recommendation": "补充水热釜规格、内衬体积、装液量或填充率。",
    },
    "PREP_MISSING_CALCINATION_RAMP": {
        "dimension": "preparation_executability",
        "level": "LOW",
        "title": "煅烧升温速率未说明",
        "recommendation": "补充升温速率和冷却方式，避免晶相或颗粒尺寸不可控。",
    },
    "PREP_MISSING_REDUCTION_FLOW": {
        "dimension": "preparation_executability",
        "level": "MEDIUM",
        "title": "还原气体流量或空速未说明",
        "recommendation": "补充还原气体流量、空速或管式炉装样量，并说明升温程序。",
    },
    "PREP_MISSING_SEPARATION_DETAIL": {
        "dimension": "preparation_executability",
        "level": "LOW",
        "title": "离心或过滤条件未明确",
        "recommendation": "补充离心转速、时间或过滤介质规格。",
    },
    "SAMPLE_NO_BASELINE": {
        "dimension": "controls_and_baselines",
        "level": "HIGH",
        "title": "缺少基准样或对照样",
        "recommendation": "设置未改性样、常规负载样、商业样或文献基准样，并保持关键制备和评价条件一致。",
    },
    "SAMPLE_NO_BLANK_SUPPORT": {
        "dimension": "controls_and_baselines",
        "level": "MEDIUM",
        "title": "缺少空白载体或无活性组分对照",
        "recommendation": "增加空白载体或无活性金属样品，用于判断活性组分贡献。",
    },
    "SAMPLE_NAMING_NOT_TRACEABLE": {
        "dimension": "variable_attribution",
        "level": "LOW",
        "title": "样品命名与变量关系不够清晰",
        "recommendation": "建立样品命名表，明确每个样品对应的关键变量和制备差异。",
    },
    "EVAL_MISSING_REACTION_CONDITIONS": {
        "dimension": "evaluation_reliability",
        "level": "HIGH",
        "title": "缺少催化评价条件",
        "recommendation": "补充目标反应、反应器类型、催化剂用量、原料组成、温度、压力、流量或空速、预处理和分析方法。",
    },
    "EVAL_MISSING_ANALYTICAL_METHOD": {
        "dimension": "evaluation_reliability",
        "level": "MEDIUM",
        "title": "产物分析方法未明确",
        "recommendation": "补充定量分析方法、检测器、标准曲线、内标或校正因子。",
    },
    "EVAL_MISSING_REPEAT_ERROR": {
        "dimension": "evaluation_reliability",
        "level": "MEDIUM",
        "title": "重复实验和误差控制未明确",
        "recommendation": "补充重复实验次数、误差表示方式和异常数据处理规则。",
    },
    "EVAL_MISSING_BALANCE": {
        "dimension": "evaluation_reliability",
        "level": "MEDIUM",
        "title": "物料平衡或碳平衡要求未明确",
        "recommendation": "补充碳平衡、氯平衡、质量平衡或元素平衡的计算口径和合格阈值。",
    },
    "CHAR_MISSING_PREPARATION_VERIFICATION": {
        "dimension": "claim_validation_linkage",
        "level": "MEDIUM",
        "title": "催化剂形成与结构确认项目未明确",
        "recommendation": "补充 XRD、ICP/XRF、XPS、TEM/SEM、BET 或 H2-TPR 等表征项目，用于确认样品组成、晶相、负载量、价态和形貌。",
    },
    "CLAIM_NO_METRIC": {
        "dimension": "claim_validation_linkage",
        "level": "HIGH",
        "title": "性能主张缺少对应评价指标",
        "recommendation": "将性能主张转化为可测指标，例如转化率、选择性、收率、TOF、STY、TOS 稳定性或抗毒化保持率。",
    },
    "CLAIM_STABILITY_NO_TOS": {
        "dimension": "claim_validation_linkage",
        "level": "HIGH",
        "title": "稳定性主张缺少连续评价设计",
        "recommendation": "增加连续运行、循环使用、再生前后性能或反应前后表征方案。",
    },
}

STEP_KEYWORDS = [
    "称取", "溶于", "溶解", "得到溶液", "混合", "加入", "滴加", "搅拌", "转移", "水热", "保持", "冷却", "离心", "洗涤", "干燥", "研磨", "煅烧", "焙烧", "还原", "标记", "命名", "记为", "浸渍", "过滤", "老化", "蒸发",
    "dissolved", "mixed", "stir", "hydrothermal", "centrifug", "washed", "dried", "calcined", "reduced", "impregnated", "denoted",
]
EVAL_KEYWORDS = ["催化评价", "反应评价", "固定床", "反应器", "转化率", "选择性", "收率", "空速", "GHSV", "WHSV", "GC", "HPLC", "TCD", "FID", "产物分析"]
CHAR_KEYWORDS = ["XRD", "XPS", "TEM", "SEM", "BET", "TPR", "TPD", "DRIFTS", "Mössbauer", "拉曼", "Raman", "ICP", "XRF", "表征"]
CLAIM_KEYWORDS = ["提高", "提升", "降低", "增强", "改善", "稳定", "抗失活", "选择性", "活性", "收率", "转化率", "机理", "活性位"]
CONTROL_KEYWORDS = ["对照", "对比", "基准", "负载型", "空白", "未改性", "商业", "reference", "control", "baseline"]

NON_SAMPLE_EXACT = {
    "H2/Ar", "H₂/Ar", "N2/Ar", "N₂/Ar", "H2/N2", "H₂/N₂", "CO/H2", "CO/H₂", "CO2/H2", "CO₂/H₂",
    "去离子水", "无水乙醇", "空气", "管式炉", "马弗炉", "溶液A", "溶液B",
}
NON_SAMPLE_PATTERNS = [
    r"^\d+%?\s*(H2|H₂|N2|N₂|Ar|CO|CO2|CO₂)(/|:)(H2|H₂|N2|N₂|Ar|CO|CO2|CO₂)$",
    r"^(H2|H₂|N2|N₂|Ar|CO|CO2|CO₂|空气|氢气|氮气)$",
    r"^\d+(\.\d+)?\s*(mL|ml|g|mg|h|min|°C|℃)$",
]
OPERATION_CATEGORIES = [
    ("还原", ["还原", "reduction", "reduced", "H2", "H₂"]),
    ("煅烧/焙烧", ["煅烧", "焙烧", "calcination", "calcined", "马弗炉", "muffle"]),
    ("水热处理", ["水热", "hydrothermal", "反应釜", "autoclave"]),
    ("浸渍", ["浸渍", "impregnation", "impregnated"]),
    ("蒸发/老化", ["蒸发", "老化", "evaporat", "aging", "aged"]),
    ("固液分离/洗涤", ["离心", "过滤", "洗涤", "centrifug", "filter", "wash"]),
    ("干燥", ["干燥", "dried", "drying"]),
    ("研磨", ["研磨", "grind", "ground"]),
    ("混合/搅拌", ["混合", "搅拌", "加入", "滴加", "mixed", "stir"]),
    ("前驱体溶解", ["称取", "溶于", "溶解", "得到溶液", "dissolved"]),
    ("样品命名", ["标记", "命名", "记为", "denoted"]),
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
            raise RuntimeError(f"无法读取 PDF 文本，请先转写或导出为文本：{exc}") from exc
    if suffix == ".docx":
        return read_docx_text(path)
    raise RuntimeError(f"暂不支持的输入格式：{suffix}。请转为 txt/md/docx/pdf。")


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
        raise RuntimeError(f"无法读取 Word 文档。请确认文件为有效 .docx：{exc}") from exc
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
    return "操作"


def diagnose_material(text: str) -> Dict[str, str]:
    t = normalize_text(text)
    step_hits = sum(1 for kw in STEP_KEYWORDS if kw in t)
    eval_hits = sum(1 for kw in EVAL_KEYWORDS if kw in t)
    if len(t) < 80 or step_hits < 2:
        return {
            "material_type": "材料信息不足",
            "audit_mode": "材料不足提示",
            "confidence": "中",
            "scope_statement": "当前输入缺少足够的催化剂制备或评价要素，报告仅能给出材料补充建议。",
        }
    if step_hits >= 5 and eval_hits >= 3:
        return {
            "material_type": "制备与评价完整方案",
            "audit_mode": "完整审核",
            "confidence": "高",
            "scope_statement": "材料同时包含制备步骤和催化评价信息，适合开展制备、对照、评价和验证路径的完整审核。",
        }
    if step_hits >= 5:
        return {
            "material_type": "制备步骤型方案",
            "audit_mode": "制备方案审核",
            "confidence": "高",
            "scope_statement": "材料以催化剂制备步骤为主，适合重点审核制备可执行性、样品与对照关系，并提示评价条件缺项。",
        }
    return {
        "material_type": "研发设想或方案初稿",
        "audit_mode": "草案级审核",
        "confidence": "中",
        "scope_statement": "材料包含一定研发意图，但制备和评价条件不完整，适合开展草案级审核。",
    }


def split_steps(text: str) -> List[Dict[str, Any]]:
    raw_parts = re.split(r"(?<=[。；;])\s*|\n+", text)
    steps: List[Dict[str, Any]] = []
    for part in raw_parts:
        p = part.strip()
        if not p:
            continue
        if any(kw in p for kw in STEP_KEYWORDS):
            conditions = {
                "temperature": bool(re.search(r"\d+\s*°C|\d+\s*℃", p)),
                "time": bool(re.search(r"\d+(\.\d+)?\s*(h|小时|min|分钟|s|秒)", p, flags=re.I)),
                "mass": bool(re.search(r"\d+(\.\d+)?\s*(mg|g|kg|毫克|克)", p, flags=re.I)),
                "volume": bool(re.search(r"\d+(\.\d+)?\s*(mL|ml|L|μL|uL|毫升|升)", p, flags=re.I)),
                "atmosphere": bool(re.search(r"空气|H2|H₂|Ar|N2|N₂|氧气|氮气|氢气|CO", p)),
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
        return "煅烧后中间样品"
    # Control words must be directly attached to this exact sample name, not merely appear later in the same sentence.
    if re.search(exact_pattern + r"\s*(对照|基准|control|baseline|comparison)", joined, re.I) or re.search(r"(对照|基准|control|baseline|comparison)\s*" + exact_pattern, joined, re.I):
        return "对照样或基准样"
    if re.search(rf"(最终得到|得到|标记为|命名为|记为)\s*{re.escape(name)}", joined):
        return "目标样品"
    return "未明确"


def has_keyword(text: str, keywords: List[str]) -> bool:
    return any(k in text for k in keywords)


def add_issue(issues: List[Dict[str, str]], issue_id: str, basis: str) -> None:
    if any(i["issue_id"] == issue_id for i in issues):
        return
    item = ISSUE_CATALOG[issue_id]
    issues.append({
        "issue_id": issue_id,
        "dimension": item["dimension"],
        "dimension_zh": DIM_ZH[item["dimension"]],
        "level": item["level"],
        "level_zh": LEVEL_ZH[item["level"]],
        "title": item["title"],
        "basis": basis,
        "recommendation": item["recommendation"],
    })


def generate_issues(text: str, steps: List[Dict[str, Any]], samples: List[Dict[str, str]]) -> List[Dict[str, str]]:
    t = normalize_text(text)
    issues: List[Dict[str, str]] = []

    if re.search(r"水热|hydrothermal|autoclave|反应釜", t, re.I):
        if not re.search(r"填充率|装液量|釜体积|\d+\s*mL\s*(水热釜|反应釜)|autoclave volume", t, re.I):
            add_issue(issues, "PREP_MISSING_HYDROTHERMAL_FILLING", "方案包含水热或反应釜步骤，但未明确反应釜规格、装液量或填充率。")
    if re.search(r"煅烧|焙烧|calcination|calcined|muffle", t, re.I):
        if not re.search(r"升温速率|ramp|°C\s*min|℃/min|°C/min", t, re.I):
            add_issue(issues, "PREP_MISSING_CALCINATION_RAMP", "方案包含煅烧或焙烧步骤，但未明确升温速率。")
    if re.search(r"还原|reduction|reduced|H2|H₂", t, re.I):
        if not re.search(r"mL\s*min|ml\s*min|流量|空速|GHSV|WHSV|sccm", t, re.I):
            add_issue(issues, "PREP_MISSING_REDUCTION_FLOW", "方案包含还原气氛、温度或时间，但未明确气体流量或空速。")
    if re.search(r"离心|centrifug", t, re.I):
        if not re.search(r"rpm|r/min|转速|\d+\s*min|分钟", t, re.I):
            add_issue(issues, "PREP_MISSING_SEPARATION_DETAIL", "方案包含离心分离步骤，但未明确离心转速或时间。")

    if not has_keyword(t, CONTROL_KEYWORDS):
        add_issue(issues, "SAMPLE_NO_BASELINE", "文本中未识别到明确的对照样、基准样、未改性样或商业/文献基准。")
    else:
        if re.search(r"Pd|Pt|Ru|Co|Fe|Ni|Mo|Cu|Rh", t) and not re.search(r"空白|无\s*(Pd|Pt|Ru|Co|Fe|Ni)|bare|support-only|载体样", t, re.I):
            add_issue(issues, "SAMPLE_NO_BLANK_SUPPORT", "文本中存在活性金属催化剂和对照样，但未识别到空白载体或无活性组分对照。")
    if samples and not any(s["role"] in {"目标样品", "对照样或基准样"} for s in samples):
        add_issue(issues, "SAMPLE_NAMING_NOT_TRACEABLE", "文本出现样品名称，但样品名称与关键变量的对应关系不够明确。")

    has_eval = has_keyword(t, EVAL_KEYWORDS)
    if not has_eval:
        add_issue(issues, "EVAL_MISSING_REACTION_CONDITIONS", "当前材料以制备步骤为主，未识别到催化评价反应、反应器、原料组成、温度、压力或分析方法。")
    else:
        if not re.search(r"GC|HPLC|MS|TCD|FID|色谱|检测器|标准曲线|内标", t, re.I):
            add_issue(issues, "EVAL_MISSING_ANALYTICAL_METHOD", "文本涉及催化评价，但未明确产物定量分析方法。")
    if not re.search(r"重复|平行|误差|标准差|error|standard deviation|n\s*=", t, re.I):
        add_issue(issues, "EVAL_MISSING_REPEAT_ERROR", "文本未识别到重复实验、误差范围或数据不确定性控制。")
    if has_eval and not re.search(r"碳平衡|物料平衡|质量平衡|氯平衡|carbon balance|mass balance", t, re.I):
        add_issue(issues, "EVAL_MISSING_BALANCE", "文本涉及反应评价，但未明确物料平衡或元素平衡要求。")

    if re.search(r"掺杂|负载|单原子|晶相|价态|孔|形貌|氧空位|疏水|羟基|facet|active phase|active site", t, re.I):
        if not has_keyword(t, CHAR_KEYWORDS):
            add_issue(issues, "CHAR_MISSING_PREPARATION_VERIFICATION", "文本涉及催化剂结构、组成或活性位形成，但未识别到相应表征计划。")
    if has_keyword(t, CLAIM_KEYWORDS):
        if not re.search(r"转化率|选择性|收率|TOF|STY|稳定性|TOS|保持率|活性|产率|yield|conversion|selectivity", t, re.I):
            add_issue(issues, "CLAIM_NO_METRIC", "文本存在性能提升类表述，但未识别到对应可量化指标。")
        if re.search(r"稳定|抗失活|robust|stable|deactivation", t, re.I) and not re.search(r"TOS|time on stream|连续|循环|再生|\d+\s*h", t, re.I):
            add_issue(issues, "CLAIM_STABILITY_NO_TOS", "文本存在稳定性或抗失活主张，但未识别到连续运行、循环或再生评价设计。")

    level_rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    return sorted(issues, key=lambda x: (level_rank[x["level"]], x["dimension"], x["issue_id"]))


def summarize(issues: List[Dict[str, str]]) -> Dict[str, Any]:
    counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for issue in issues:
        counts[issue["level"]] += 1
    if counts["HIGH"]:
        overall = "设计基本具备，但存在影响方案执行或结论成立的关键问题。"
        judgment = "PARTIAL"
    elif counts["MEDIUM"]:
        overall = "方案主体可识别，但若干重要条件需要补充完善。"
        judgment = "PARTIAL"
    elif issues:
        overall = "方案整体较清楚，主要需补充操作细节。"
        judgment = "SUFFICIENT"
    else:
        overall = "未发现明显缺项；仍建议结合实际装置和内部规范复核。"
        judgment = "SUFFICIENT"
    return {
        "high_count": counts["HIGH"],
        "medium_count": counts["MEDIUM"],
        "low_count": counts["LOW"],
        "total_count": len(issues),
        "overall_judgment": judgment,
        "overall_judgment_zh": JUDGMENT_ZH[judgment],
        "overall_opinion": overall,
    }


def infer_catalyst_system(text: str, samples: List[Dict[str, str]]) -> str:
    if samples:
        return "、".join(s["sample_name"] for s in samples[:6])
    m = re.search(r"([A-Z][a-z]?[A-Za-z0-9@/\-]+\s*催化剂)", text)
    if m:
        return m.group(1)
    return "未明确"


def extract_claims(text: str) -> List[Dict[str, str]]:
    claims = []
    parts = re.split(r"(?<=[。；;])\s*|\n+", text)
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
            "evaluation_plan": {"detected": eval_detected, "summary": "已识别到催化评价相关内容。" if eval_detected else "未识别到催化评价条件。"},
            "claims": extract_claims(text),
        },
        "audit_issues": issues,
        "computed_summary": summary,
    }
    return context


def render_dimension_sections_html(issues: List[Dict[str, str]]) -> str:
    blocks = []
    for dim, zh in DIM_ZH.items():
        dim_issues = [i for i in issues if i["dimension"] == dim]
        if dim_issues:
            lis = "".join(f"<li>{html.escape(i['level_zh'])}：{html.escape(i['title'])}</li>" for i in dim_issues)
            opinion = f"<ul>{lis}</ul>"
        else:
            opinion = "<p>未识别到该维度的明显缺项。</p>"
        blocks.append(f"<h3>{html.escape(zh)}</h3>{opinion}")
    return "\n".join(blocks)


def render_recommendations_html(issues: List[Dict[str, str]]) -> str:
    if not issues:
        return "<p>建议按内部实验记录规范保留完整原始数据和操作记录。</p>"
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
        f"<tr><td>{i+1}</td><td>{esc(it['level_zh'])}</td><td>{esc(it['dimension_zh'])}</td><td>{esc(it['title'])}</td><td>{esc(it['basis'])}</td><td>{esc(it['recommendation'])}</td></tr>"
        for i, it in enumerate(issues)
    ) or "<tr><td colspan='6'>未识别到明确问题。</td></tr>"
    step_rows = "\n".join(
        f"<tr><td>{esc(s['step_id'])}</td><td>{esc(s['operation'])}</td><td>{esc(s['raw_text'])}</td></tr>"
        for s in elements["preparation_steps"]
    ) or "<tr><td colspan='3'>未识别到制备步骤。</td></tr>"
    sample_rows = "\n".join(
        f"<tr><td>{esc(s['sample_id'])}</td><td>{esc(s['sample_name'])}</td><td>{esc(s['role'])}</td></tr>"
        for s in elements["sample_design"]
    ) or "<tr><td colspan='3'>未识别到样品名称。</td></tr>"

    css = """
    body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Microsoft YaHei',Arial,sans-serif;background:#f6f7f9;color:#111827;margin:0;}
    .page{max-width:1120px;margin:0 auto;padding:32px;}
    .card{background:white;border:1px solid #e5e7eb;border-radius:12px;padding:22px;margin:18px 0;box-shadow:0 4px 16px rgba(15,23,42,.04)}
    h1{font-size:30px;margin:0 0 10px;} h2{font-size:22px;margin-top:0;border-left:5px solid #009BA4;padding-left:10px;} h3{font-size:18px;margin-bottom:8px;}
    .meta{color:#4b5563;font-size:14px;line-height:1.8}.summary{display:flex;gap:12px;flex-wrap:wrap}.pill{padding:10px 14px;border-radius:10px;background:#eef2ff;border:1px solid #dbe3ff}.high{background:#fee2e2}.medium{background:#fef3c7}.low{background:#e0f2fe}
    table{border-collapse:collapse;width:100%;font-size:14px;}th,td{border:1px solid #e5e7eb;padding:10px;vertical-align:top;}th{background:#f3f4f6;text-align:left}.opinion{font-size:17px;line-height:1.75}.small{font-size:13px;color:#6b7280;}
    """
    return f"""<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'><title>{esc(meta['report_title'])}</title><style>{css}</style></head><body><div class='page'>
    <div class='card'><h1>{esc(meta['report_title'])}</h1><div class='meta'>审核对象：{esc(meta['input_file'])}<br>Skill 版本：{esc(meta['skill_version'])}<br>输入文件指纹：{esc(meta['input_sha256'][:16])}...</div></div>
    <div class='card'><h2>一、审核对象与材料性质</h2><p class='opinion'>本次输入材料识别为：<strong>{esc(material['material_type'])}</strong>；审核模式为：<strong>{esc(material['audit_mode'])}</strong>；判断置信度：{esc(material['confidence'])}。</p><p>{esc(material['scope_statement'])}</p></div>
    <div class='card'><h2>二、总体审核意见</h2><div class='summary'><div class='pill'>总体判定：{esc(summary['overall_judgment_zh'])}</div><div class='pill high'>关键问题：{summary['high_count']} 项</div><div class='pill medium'>重要问题：{summary['medium_count']} 项</div><div class='pill low'>一般问题：{summary['low_count']} 项</div></div><p class='opinion'>{esc(summary['overall_opinion'])}</p></div>
    <div class='card'><h2>三、重点问题清单</h2><table><thead><tr><th>序号</th><th>问题级别</th><th>审核维度</th><th>问题名称</th><th>判断依据</th><th>修改建议</th></tr></thead><tbody>{issue_rows}</tbody></table></div>
    <div class='card'><h2>四、分项审核结果</h2>{render_dimension_sections_html(issues)}</div>
    <div class='card'><h2>五、制备步骤核对表</h2><table><thead><tr><th>步骤编号</th><th>识别工序</th><th>原文内容</th></tr></thead><tbody>{step_rows}</tbody></table></div>
    <div class='card'><h2>六、样品与变量关系核对表</h2><table><thead><tr><th>样品编号</th><th>样品名称</th><th>识别角色</th></tr></thead><tbody>{sample_rows}</tbody></table></div>
    <div class='card'><h2>七、修改建议</h2>{render_recommendations_html(issues)}</div>
    <div class='card'><h2>八、审核说明</h2><p class='small'>本报告依据固定审核维度和规则生成。若输入为截图或扫描件，审核稳定性依赖转写文本的一致性。报告仅用于方案完善和实验前检查，不替代专家最终判断。</p></div>
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
    body.append(w_p(f"审核对象：{meta['input_file']}"))
    body.append(w_p(f"Skill 版本：{meta['skill_version']}"))
    body.append(w_p("一、审核对象与材料性质", "Heading1"))
    body.append(w_p(f"本次输入材料识别为：{material['material_type']}；审核模式为：{material['audit_mode']}；判断置信度：{material['confidence']}。"))
    body.append(w_p(material["scope_statement"]))
    body.append(w_p("二、总体审核意见", "Heading1"))
    body.append(w_p(f"总体判定：{summary['overall_judgment_zh']}。关键问题 {summary['high_count']} 项，重要问题 {summary['medium_count']} 项，一般问题 {summary['low_count']} 项。"))
    body.append(w_p(summary["overall_opinion"]))
    body.append(w_p("三、重点问题清单", "Heading1"))
    rows = [["序号", "问题级别", "审核维度", "问题名称", "判断依据", "修改建议"]]
    if not issues:
        rows.append(["-", "-", "-", "未识别到明确问题", "-", "-"])
    for idx, issue in enumerate(issues, 1):
        rows.append([idx, issue["level_zh"], issue["dimension_zh"], issue["title"], issue["basis"], issue["recommendation"]])
    body.append(w_tbl(rows))
    body.append(w_p("四、分项审核结果", "Heading1"))
    for dim, zh in DIM_ZH.items():
        body.append(w_p(zh, "Heading2"))
        dim_issues = [i for i in issues if i["dimension"] == dim]
        if dim_issues:
            for issue in dim_issues:
                body.append(w_p(f"{issue['level_zh']}：{issue['title']}。{issue['basis']} 建议：{issue['recommendation']}"))
        else:
            body.append(w_p("未识别到该维度的明显缺项。"))
    body.append(w_p("五、制备步骤核对表", "Heading1"))
    step_rows = [["步骤编号", "识别工序", "原文内容"]]
    if not elements["preparation_steps"]:
        step_rows.append(["-", "-", "未识别到制备步骤。"])
    for step in elements["preparation_steps"]:
        step_rows.append([step["step_id"], step["operation"], str(step["raw_text"])[:600]])
    body.append(w_tbl(step_rows))
    body.append(w_p("六、样品与变量关系核对表", "Heading1"))
    sample_rows = [["样品编号", "样品名称", "识别角色"]]
    if not elements["sample_design"]:
        sample_rows.append(["-", "未识别到样品名称", "-"])
    for sample in elements["sample_design"]:
        sample_rows.append([sample["sample_id"], sample["sample_name"], sample["role"]])
    body.append(w_tbl(sample_rows))
    body.append(w_p("七、修改建议", "Heading1"))
    if issues:
        for idx, issue in enumerate(issues[:10], 1):
            body.append(w_p(f"{idx}. {issue['recommendation']}"))
    else:
        body.append(w_p("建议按内部实验记录规范保留完整原始数据和操作记录。"))
    body.append(w_p("附录A：方案要素提取结果", "Heading1"))
    body.append(w_p(f"催化剂体系/样品：{elements['catalyst_system']}"))
    body.append(w_p(f"识别制备步骤数量：{len(elements['preparation_steps'])}"))
    body.append(w_p(f"识别样品数量：{len(elements['sample_design'])}"))
    body.append(w_p(f"评价计划：{elements['evaluation_plan']['summary']}"))
    body.append(w_p("附录B：审核规则与判定口径", "Heading1"))
    body.append(w_p("本报告采用固定审核维度：制备步骤可执行性、变量设计与归因关系、对照样与基准样设置、评价条件与数据可靠性、性能主张与验证项目对应关系。"))
    body.append(w_p("问题级别分为关键问题、重要问题和一般问题。关键问题指不补充将影响执行、复现、对比或核心结论成立的问题。"))
    body.append(w_p("附录C：输入文件与版本信息", "Heading1"))
    body.append(w_p(f"输入文件：{meta['input_file']}"))
    body.append(w_p(f"输入文件指纹：{meta['input_sha256']}"))
    body.append(w_p(f"生成时间：{meta['generated_at']}"))
    body.append(w_p(f"Skill 版本：{meta['skill_version']}"))

    document_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>{''.join(body)}<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr></w:body></w:document>'''
    styles_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:rPr><w:rFonts w:ascii="Microsoft YaHei" w:eastAsia="Microsoft YaHei"/><w:sz w:val="21"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:rPr><w:b/><w:sz w:val="36"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:rPr><w:b/><w:sz w:val="30"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:rPr><w:b/><w:sz w:val="26"/></w:rPr></w:style><w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/><w:tblPr><w:tblBorders><w:top w:val="single" w:sz="4"/><w:left w:val="single" w:sz="4"/><w:bottom w:val="single" w:sz="4"/><w:right w:val="single" w:sz="4"/><w:insideH w:val="single" w:sz="4"/><w:insideV w:val="single" w:sz="4"/></w:tblBorders></w:tblPr></w:style></w:styles>'''
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
        raise RuntimeError("HTML、Word 或 report_context.json 缺失。")
    html_text = html_path.read_text(encoding="utf-8", errors="ignore")
    docx_text = extract_docx_text(docx_path)
    required = ["审核对象与材料性质", "总体审核意见", "重点问题清单", "分项审核结果", "制备步骤核对表", "样品与变量关系核对表", "修改建议"]
    for sec in required:
        if sec not in html_text:
            raise RuntimeError(f"HTML 缺少章节：{sec}")
        if sec not in docx_text:
            raise RuntimeError(f"Word 缺少章节：{sec}")
    for bad in ["{'", "priority':", "None", "未明确\n审核模式：未明确"]:
        if bad in html_text or bad in docx_text:
            raise RuntimeError(f"报告中出现异常未渲染内容：{bad}")
    summary = context["computed_summary"]
    expected = f"关键问题 {summary['high_count']} 项，重要问题 {summary['medium_count']} 项，一般问题 {summary['low_count']} 项"
    if expected not in docx_text:
        raise RuntimeError("Word 问题统计与 context 不一致。")
    if f"关键问题：{summary['high_count']} 项" not in html_text:
        raise RuntimeError("HTML 问题统计与 context 不一致。")


def reset_output_dir(out_dir: Path) -> None:
    if out_dir.exists():
        if out_dir.resolve() == Path("/").resolve():
            raise RuntimeError("拒绝清空根目录。")
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)


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
        raise RuntimeError("输入文件未读取到有效文本。若为图片或扫描件，请先按提示词忠实转写。")
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
            f"审核完成，已生成：{HTML_NAME}；{DOCX_NAME}。"
            f"核心结论：{context['computed_summary']['overall_judgment_zh']}。"
            f"关键问题 {context['computed_summary']['high_count']} 项，"
            f"重要问题 {context['computed_summary']['medium_count']} 项，"
            f"一般问题 {context['computed_summary']['low_count']} 项。"
        ),
    }
    print(json.dumps(message, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Score an enterprise carbon credit rating JSON payload.

Input JSON should use canonical field names from references/extraction_dictionary.md.
The script is intentionally conservative: missing key fields produce no-rating unless
--allow-missing-key is passed after the user has explicitly accepted that outcome.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ABC_WEIGHTS = {
    "高碳排放强度、高转型压力": {"alpha": 0.35, "beta": 0.40, "gamma": 0.25},
    "中碳排放强度、中等转型压力": {"alpha": 0.45, "beta": 0.35, "gamma": 0.20},
    "污水处理行业特例": {"alpha": 0.20, "beta": 0.45, "gamma": 0.35},
    "低碳排放强度、低转型压力": {"alpha": 0.55, "beta": 0.25, "gamma": 0.20},
    "资源依赖型、生态敏感行业": {"alpha": 0.40, "beta": 0.35, "gamma": 0.25},
    "创新驱动型、绿色技术行业": {"alpha": 0.40, "beta": 0.30, "gamma": 0.30},
}

SWV_WEIGHTS = {
    "高碳排放强度、高转型压力": {"s": 0.25, "w": 0.50, "v": 0.25},
    "中碳排放强度、中等转型压力": {"s": 0.30, "w": 0.40, "v": 0.30},
    "污水处理行业特例": {"s": 0.20, "w": 0.45, "v": 0.35},
    "低碳排放强度、低转型压力": {"s": 0.25, "w": 0.35, "v": 0.40},
    "资源依赖型、生态敏感行业": {"s": 0.40, "w": 0.30, "v": 0.30},
    "创新驱动型、绿色技术行业": {"s": 0.35, "w": 0.35, "v": 0.30},
}

IDENTITY_REQUIRED = ["company_name", "unified_credit_code", "industry", "rating_period"]
VETO_REQUIRED = [
    "serious_dishonesty_flag",
    "carbon_data_fraud",
    "major_environment_penalty",
    "major_bank_bad_record",
]

CARBON_RAW_REQUIRED = [
    "verified_emission_qty",
    "enterprise_carbon_intensity",
    "industry_carbon_intensity",
    "carbon_behavior_total_count",
]


def num(data: dict[str, Any], key: str, default: float | None = None) -> float | None:
    value = data.get(key, default)
    if value in ("", None, "未采集数据"):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def truthy(value: Any) -> bool:
    return value in (True, 1, "1", "true", "True", "是", "yes", "Y", "y")


def is_missing(value: Any) -> bool:
    return value is None or value == "" or value == "未采集数据"


def pick(data: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in data and not is_missing(data.get(key)):
            return data.get(key)
    return None


def normalize_payload(data: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Accept both nested skill JSON and flat extracted JSON.

    Earlier ad-hoc runs used flat fields such as company_name and beta at the
    root. Normalize those so the deterministic scorer does not silently drop
    supplied values.
    """

    enterprise = dict(data.get("enterprise") or {})
    if not enterprise:
        for key in ["company_name", "unified_credit_code", "industry", "rating_period", "report_date", "industry_class"]:
            if key in data:
                enterprise[key] = data[key]

    metrics = dict(data.get("metrics") or {})
    scores = dict(data.get("scores") or {})
    adjustments = dict(data.get("adjustments") or {})
    weights = dict(data.get("weights") or {})
    veto_check = dict(data.get("veto_check") or {})

    for key in [
        "serious_dishonesty_flag",
        "verified_emission_qty",
        "enterprise_carbon_intensity",
        "industry_carbon_intensity",
        "carbon_behavior_total_count",
        "data_error_count",
        "carbon_data_error_count",
        "purchase_data_false_count",
        "green_certificate_delay_count",
        "carbon_trade_delay_count",
        "s_score",
        "w_score",
        "v_score",
        "carbon_price",
        "carbon_allowance_qty",
        "ccer_qty",
        "ccer_price",
        "verified_carbon_sink_qty",
        "carbon_sink_price",
        "green_certificate_qty",
        "power_emission_factor",
        "enterprise_output_value",
        "industry_carbon_account_value",
        "industry_output_value",
    ]:
        if key in data and key not in metrics:
            metrics[key] = data[key]

    if "data_error_count" not in metrics and "carbon_data_error_count" in metrics:
        metrics["data_error_count"] = metrics["carbon_data_error_count"]

    for key in ["basic_credit_score", "carbon_account_score", "transition_score"]:
        if key in data and key not in scores:
            scores[key] = data[key]

    for src, dst in [
        ("serious_dishonesty_flag", "serious_dishonesty_flag"),
        ("major_env_penalty", "major_environment_penalty"),
        ("major_environment_penalty", "major_environment_penalty"),
        ("major_bank_bad_record", "major_bank_bad_record"),
        ("carbon_data_fraud", "carbon_data_fraud"),
    ]:
        if src in data and dst not in adjustments:
            adjustments[dst] = data[src]
        if src in veto_check and dst not in adjustments:
            adjustments[dst] = veto_check[src]

    if "abc" in weights and isinstance(weights["abc"], dict):
        for key in ["alpha", "beta", "gamma"]:
            if key in weights["abc"] and key not in weights:
                weights[key] = weights["abc"][key]
    if "swv" in weights and isinstance(weights["swv"], dict):
        swv = weights["swv"]
        for src, dst in [("s", "Ws"), ("w", "Ww"), ("v", "Wv")]:
            if src in swv and dst not in weights:
                weights[dst] = swv[src]

    return enterprise, metrics, scores, adjustments, weights


def map_grade(score: float | None) -> str | None:
    if score is None:
        return None
    if score >= 90:
        return "AAA"
    if score >= 85:
        return "AA"
    if score >= 80:
        return "A"
    if score >= 75:
        return "BBB"
    if score >= 70:
        return "BB"
    if score >= 65:
        return "B"
    if score >= 60:
        return "CCC"
    if score >= 50:
        return "CC"
    return "C"


def band_score(value: float | None, bands: list[tuple[float | None, float | None, str, int]], include_zero=False):
    if value is None:
        return None
    for low, high, grade, score in bands:
        if low is None and high is not None and value <= high:
            return {"value": value, "grade": grade, "score": score}
        if high is None and low is not None and value > low:
            return {"value": value, "grade": grade, "score": score}
        if low is not None and high is not None:
            if include_zero and value == 0 and low == 0:
                return {"value": value, "grade": grade, "score": score}
            if low < value <= high:
                return {"value": value, "grade": grade, "score": score}
    return None


def calc_swv(data: dict[str, Any], industry_class: str, supplied_weights: dict[str, float] | None = None):
    s_score = data.get("s_score")
    w_score = data.get("w_score")
    v_score = data.get("v_score")
    details: dict[str, Any] = {}

    if s_score is None:
        carbon_price = num(data, "carbon_price")
        if carbon_price is not None:
            positive = 0.0
            positive += (num(data, "carbon_allowance_qty", 0) or 0) * carbon_price
            positive += (num(data, "ccer_qty", 0) or 0) * (num(data, "ccer_price", carbon_price) or carbon_price)
            positive += (num(data, "verified_carbon_sink_qty", 0) or 0) * (num(data, "carbon_sink_price", carbon_price) or carbon_price)
            positive += (num(data, "green_certificate_qty", 0) or 0) * (num(data, "power_emission_factor", 0) or 0) * carbon_price
            negative = (num(data, "verified_emission_qty", 0) or 0) * carbon_price
            enterprise_value = positive - negative
            enterprise_output = num(data, "enterprise_output_value")
            industry_value = num(data, "industry_carbon_account_value")
            industry_output = num(data, "industry_output_value")
            if enterprise_output and industry_value is not None and industry_output:
                s = (enterprise_value / enterprise_output) / (industry_value / industry_output)
                s_result = band_score(
                    s,
                    [
                        (2.00, None, "Aaa", 90),
                        (1.50, 2.00, "Aa", 80),
                        (1.00, 1.50, "A", 70),
                        (0.80, 1.00, "Bbb", 60),
                        (0.60, 0.80, "Bb", 50),
                        (0.40, 0.60, "B", 40),
                        (0.20, 0.40, "Ccc", 30),
                        (0.10, 0.20, "Cc", 20),
                        (0.00, 0.10, "C", 10),
                    ],
                )
                if s_result:
                    s_score = s_result["score"]
                    details["s"] = s_result | {"enterprise_carbon_account_value": enterprise_value}
    else:
        s_score = float(s_score)

    if w_score is None:
        intensity = num(data, "enterprise_carbon_intensity")
        baseline = num(data, "industry_carbon_intensity")
        if intensity is not None and baseline:
            w = intensity / baseline
            w_result = band_score(
                w,
                [
                    (0.01, 0.90, "Aaa", 90),
                    (0.90, 0.95, "Aa", 80),
                    (0.95, 1.00, "A", 70),
                    (1.00, 1.02, "Bbb", 60),
                    (1.02, 1.04, "Bb", 50),
                    (1.04, 1.06, "B", 40),
                    (1.06, 1.08, "Ccc", 30),
                    (1.08, 1.10, "Cc", 20),
                    (1.10, None, "C", 10),
                ],
            )
            if w_result:
                w_score = w_result["score"]
                details["w"] = w_result
    else:
        w_score = float(w_score)

    if v_score is None:
        total = num(data, "carbon_behavior_total_count")
        if total:
            numerator = sum(
                num(data, key, 0) or 0
                for key in [
                    "data_error_count",
                    "purchase_data_false_count",
                    "green_certificate_delay_count",
                    "carbon_trade_delay_count",
                ]
            )
            v = numerator / total
            v_result = band_score(
                v,
                [
                    (0.00, 0.00, "Aaa", 90),
                    (0.00, 0.01, "Aa", 80),
                    (0.01, 0.05, "A", 70),
                    (0.05, 0.06, "Bbb", 60),
                    (0.06, 0.08, "Bb", 50),
                    (0.08, 0.10, "B", 40),
                    (0.10, 0.12, "Ccc", 30),
                    (0.12, 0.15, "Cc", 20),
                    (0.15, None, "C", 10),
                ],
                include_zero=True,
            )
            if v_result:
                v_score = v_result["score"]
                details["v"] = v_result | {"abnormal_count": numerator}
    else:
        v_score = float(v_score)

    weights = supplied_weights or SWV_WEIGHTS.get(industry_class, SWV_WEIGHTS["中碳排放强度、中等转型压力"])
    if None in (s_score, w_score, v_score):
        return None, details | {"weights": weights, "component_scores": {"s": s_score, "w": w_score, "v": v_score}}
    score = s_score * weights["s"] + w_score * weights["w"] + v_score * weights["v"]
    return round(score, 2), details | {"weights": weights, "component_scores": {"s": s_score, "w": w_score, "v": v_score}}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--out", default="rating_result.json")
    parser.add_argument("--allow-missing-key", action="store_true")
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    enterprise, metrics, scores, adjustments, supplied_weights = normalize_payload(data)
    flat = {**enterprise, **metrics, **adjustments, **scores}

    industry_class = enterprise.get("industry_class") or data.get("industry_class") or "中碳排放强度、中等转型压力"
    if "污水" in str(enterprise.get("industry", "")) and industry_class not in ABC_WEIGHTS:
        industry_class = "污水处理行业特例"
    if "污水" in str(enterprise.get("industry", "")) and not enterprise.get("industry_class"):
        industry_class = "污水处理行业特例"

    identity_missing = [k for k in IDENTITY_REQUIRED if k not in flat or is_missing(flat.get(k))]
    veto_missing = [k for k in VETO_REQUIRED if k not in flat or is_missing(flat.get(k))]

    if {"alpha", "beta", "gamma"}.issubset(supplied_weights):
        abc = {
            "alpha": float(supplied_weights["alpha"]),
            "beta": float(supplied_weights["beta"]),
            "gamma": float(supplied_weights["gamma"]),
        }
    else:
        abc = ABC_WEIGHTS.get(industry_class, ABC_WEIGHTS["中碳排放强度、中等转型压力"])
    if {"Ws", "Ww", "Wv"}.issubset(supplied_weights):
        swv_weights = {
            "s": float(supplied_weights["Ws"]),
            "w": float(supplied_weights["Ww"]),
            "v": float(supplied_weights["Wv"]),
        }
    else:
        swv_weights = SWV_WEIGHTS.get(industry_class)

    basic_score_available = not is_missing(scores.get("basic_credit_score")) or bool(scores.get("basic_credit_dimension_scores"))
    transition_score_available = not is_missing(scores.get("transition_score")) or bool(scores.get("transition_dimension_scores"))
    carbon_score_available = not is_missing(scores.get("carbon_account_score"))
    if not carbon_score_available:
        swv_component_scores = data.get("swv_details", {}).get("component_scores", {})
        carbon_score_available = all(not is_missing(swv_component_scores.get(k)) for k in ("s", "w", "v"))

    score_missing = []
    if not basic_score_available:
        score_missing.append("basic_credit_score")
    if not transition_score_available:
        score_missing.append("transition_score")
    carbon_raw_missing = []
    if not carbon_score_available:
        carbon_raw_missing = [k for k in CARBON_RAW_REQUIRED if k not in flat or is_missing(flat.get(k))]

    key_missing = veto_missing + score_missing + carbon_raw_missing

    no_rating_reasons = []
    if identity_missing:
        no_rating_reasons.append({"type": "不可缺失基础字段缺失", "fields": identity_missing})
    if key_missing and not args.allow_missing_key:
        no_rating_reasons.append({"type": "关键必要指标未采集", "fields": key_missing})
    if truthy(flat.get("serious_dishonesty_flag")):
        no_rating_reasons.append({"type": "严重失信主体名单"})
    if truthy(flat.get("carbon_data_fraud")):
        no_rating_reasons.append({"type": "碳数据造假"})
    if truthy(flat.get("major_environment_penalty")):
        no_rating_reasons.append({"type": "重大环境处罚"})
    if truthy(flat.get("major_bank_bad_record")):
        no_rating_reasons.append({"type": "重大银行不良记录"})

    basic_score = scores.get("basic_credit_score")
    if basic_score is None and scores.get("basic_credit_dimension_scores"):
        weights = {"信用合规": 0.30, "财务能力": 0.25, "生产与合规管理": 0.20, "创新与品牌建设": 0.25}
        ds = scores["basic_credit_dimension_scores"]
        if all(k in ds for k in weights):
            basic_score = sum(float(ds[k]) * v for k, v in weights.items())
    basic_score = float(basic_score) if basic_score is not None else None

    carbon_score = scores.get("carbon_account_score")
    swv_details = dict(data.get("swv_details") or {})
    if carbon_score is None:
        carbon_score, swv_details = calc_swv(flat, industry_class, swv_weights)
    else:
        carbon_score = float(carbon_score)

    transition_score = scores.get("transition_score")
    if transition_score is None and scores.get("transition_dimension_scores"):
        weights = {"自愿减排项目投资与绩效": 0.40, "绿色转型实施绩效": 0.30, "技改降碳实施成效": 0.30}
        ds = scores["transition_dimension_scores"]
        if all(k in ds for k in weights):
            transition_score = sum(float(ds[k]) * v for k, v in weights.items())
    transition_score = float(transition_score) if transition_score is not None else None

    comprehensive_score = None
    if None not in (basic_score, carbon_score, transition_score):
        comprehensive_score = round(basic_score * abc["alpha"] + carbon_score * abc["beta"] + transition_score * abc["gamma"], 2)

    result = {
        "enterprise": enterprise,
        "industry_class": industry_class,
        "weights": {"abc": abc, "swv": swv_weights},
        "missing": {"identity_required": identity_missing, "key_required": key_missing},
        "no_rating": bool(no_rating_reasons),
        "no_rating_reasons": no_rating_reasons,
        "scores": {
            "basic_credit_score": basic_score,
            "carbon_account_score": carbon_score,
            "transition_score": transition_score,
            "comprehensive_score": comprehensive_score,
            "grade": None if no_rating_reasons else map_grade(comprehensive_score),
        },
        "swv_details": swv_details,
        "source_payload": data,
    }
    Path(args.out).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(args.out)


if __name__ == "__main__":
    main()

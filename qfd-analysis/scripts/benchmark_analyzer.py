#!/usr/bin/env python3
"""
Benchmark Analyzer
Competitive benchmark analysis comparing our product against competitors on each requirement.
"""

import json
from typing import List, Dict, Any, Optional
from datetime import datetime


def compare_spec_value(our_value: Any, their_value: Any, direction: str) -> str:
    """
    Compare specification values and return the gap analysis.

    Args:
        our_value: our product value
        their_value: competitor value
        direction: optimization direction (higher_better, lower_better, wider_better)

    Returns:
        gap description
    """
    try:
        our_num = float(our_value) if our_value else 0
        their_num = float(their_value) if their_value else 0
    except (ValueError, TypeError):
        return "Cannot compare"
    
    if our_num == their_num:
        return "Tie"
    
    if direction == "higher_better":
        if our_num > their_num:
            diff = (our_num - their_num) / their_num * 100 if their_num else 100
            return f"Ahead (+{diff:.0f}%)"
        else:
            diff = (their_num - our_num) / our_num * 100 if our_num else 100
            return f"Behind (-{diff:.0f}%)"
    
    elif direction == "lower_better":
        if our_num < their_num:
            diff = (their_num - our_num) / their_num * 100 if their_num else 100
            return f"Ahead (-{diff:.0f}%)"
        else:
            diff = (our_num - their_num) / our_num * 100 if our_num else 100
            return f"Behind (+{diff:.0f}%)"
    
    return "Needs manual review"


def rate_requirement_satisfaction(
    requirement: Dict[str, Any],
    product_spec: Dict[str, Any],
    feature_mapping: Dict[str, str]
) -> Dict[str, Any]:
    """
    Evaluate how well a product satisfies one requirement.

    Args:
        requirement: requirement record
        product_spec: product specification
        feature_mapping: requirement-to-feature map {requirement_id: feature_id}

    Returns:
        satisfaction result {level, score, evidence}
    """
    req_id = requirement["id"]
    
    if req_id not in feature_mapping:
        return {
            "level": "Unknown",
            "score": 0,
            "evidence": "No feature mapping"
        }
    
    feature_id = feature_mapping[req_id]
    features = product_spec.get("features", [])
    
    target_feature = None
    for f in features:
        if f["id"] == feature_id:
            target_feature = f
            break
    
    if not target_feature:
        return {
            "level": "Unknown",
            "score": 0,
            "evidence": "Feature not found in spec"
        }
    
    # Return a baseline rating. Richer scoring can be layered on top later.
    return {
        "level": "Mid",  # Conservative default; user review may override it.
        "score": 3,
        "evidence": f"{target_feature['name']}: {target_feature['value']} {target_feature.get('unit', '')}"
    }


def build_benchmark_table(
    requirements: List[Dict],
    our_spec: Dict[str, Any],
    competitor_specs: List[Dict[str, Any]],
    requirement_ratings: Dict[str, Dict[str, Dict]]
) -> Dict[str, Any]:
    """
    Build the competitor benchmark table.

    Args:
        requirements: requirement list
        our_spec: our product specification
        competitor_specs: competitor specification list
        requirement_ratings: requirement satisfaction ratings
            {requirement_id: {product_id: {level, score, evidence}}}

    Returns:
        benchmark table data structure
    """
    product_ids = ["our_product"] + [spec.get("product", {}).get("id", f"competitor_{i}") 
                                      for i, spec in enumerate(competitor_specs)]
    
    comparison_rows = []
    
    for req in requirements:
        req_id = req["id"]
        ratings = requirement_ratings.get(req_id, {})
        
        row = {
            "requirement_id": req_id,
            "requirement": req["description"],
            "importance": req.get("importance", 1),
            "ratings": {}
        }
        
        for pid in product_ids:
            rating = ratings.get(pid, {"level": "Unknown", "score": 0, "evidence": ""})
            row["ratings"][pid] = rating
        
        # Gap analysis
        our_score = ratings.get("our_product", {}).get("score", 0)
        max_competitor_score = max(
            ratings.get(pid, {}).get("score", 0) 
            for pid in product_ids if pid != "our_product"
        ) if len(product_ids) > 1 else 0
        
        if our_score > max_competitor_score:
            row["gap_analysis"] = "Ahead"
        elif our_score < max_competitor_score:
            row["gap_analysis"] = "Behind"
        else:
            row["gap_analysis"] = "Tie"
        
        comparison_rows.append(row)
    
    return {
        "products": product_ids,
        "requirement_comparison": comparison_rows
    }


def build_feature_comparison(
    our_spec: Dict[str, Any],
    competitor_specs: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Build the feature-comparison table.
    """
    all_features = {}
    
    # Collect our features
    for f in our_spec.get("features", []):
        all_features[f["id"]] = {
            "feature_id": f["id"],
            "feature": f["name"],
            "direction": f.get("direction", "higher_better"),
            "values": {
                "our_product": {
                    "value": f["value"],
                    "unit": f.get("unit", "")
                }
            }
        }
    
    # Collect competitor features
    for i, comp_spec in enumerate(competitor_specs):
        comp_id = comp_spec.get("product", {}).get("id", f"competitor_{i}")
        for f in comp_spec.get("features", []):
            if f["id"] in all_features:
                all_features[f["id"]]["values"][comp_id] = {
                    "value": f["value"],
                    "unit": f.get("unit", "")
                }
    
    return list(all_features.values())


def analyze_gaps(benchmark_table: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze competitive gaps.

    Returns:
        gap analysis result, including strengths and weaknesses
    """
    advantages = []
    disadvantages = []
    neutral = []
    
    for row in benchmark_table.get("requirement_comparison", []):
        gap = row.get("gap_analysis", "")
        item = {
            "requirement_id": row["requirement_id"],
            "requirement": row["requirement"],
            "importance": row.get("importance", 1)
        }
        
        if "Ahead" in gap:
            advantages.append(item)
        elif "Behind" in gap:
            disadvantages.append(item)
        else:
            neutral.append(item)

    # Sort by importance
    advantages.sort(key=lambda x: x["importance"], reverse=True)
    disadvantages.sort(key=lambda x: x["importance"], reverse=True)
    
    return {
        "advantages": advantages,
        "disadvantages": disadvantages,
        "neutral": neutral,
        "summary": {
            "advantage_count": len(advantages),
            "disadvantage_count": len(disadvantages),
            "neutral_count": len(neutral),
            "critical_gaps": [d for d in disadvantages if d["importance"] >= 4]
        }
    }


def format_benchmark_table_markdown(benchmark_data: Dict) -> str:
    """Format the benchmark table as Markdown."""
    products = benchmark_data.get("products", [])
    rows = benchmark_data.get("requirement_comparison", [])
    
    if not rows:
        return "No data"
    
    # Header row
    header = "| Requirement | Importance |"
    for p in products:
        display_name = "Our Product" if p == "our_product" else p
        header += f" {display_name} |"
    header += " Gap |"
    
    sep = "|-------------|------------|"
    for _ in products:
        sep += "----------|"
    sep += "------|"
    
    lines = [header, sep]
    
    for row in rows:
        line = f"| {row['requirement'][:15]} | {row['importance']} |"
        for p in products:
            rating = row["ratings"].get(p, {})
            level = rating.get("level", "?")
            line += f" {level:^8} |"
        line += f" {row.get('gap_analysis', ''):^5} |"
        lines.append(line)
    
    return "\n".join(lines)


def format_gap_analysis_markdown(gap_data: Dict) -> str:
    """Format the gap analysis as Markdown."""
    lines = ["## Gap Analysis\n"]
    
    summary = gap_data.get("summary", {})
    lines.append(f"- Advantages: {summary.get('advantage_count', 0)}")
    lines.append(f"- Disadvantages: {summary.get('disadvantage_count', 0)}")
    lines.append(f"- Neutral: {summary.get('neutral_count', 0)}")
    lines.append("")
    
    critical = summary.get("critical_gaps", [])
    if critical:
        lines.append("### Critical Gaps (High Importance)")
        for item in critical:
            lines.append(f"- {item['requirement']} (Importance: {item['importance']})")
        lines.append("")
    
    if gap_data.get("advantages"):
        lines.append("### Our Advantages")
        for item in gap_data["advantages"][:5]:
            lines.append(f"- {item['requirement']}")
        lines.append("")
    
    if gap_data.get("disadvantages"):
        lines.append("### Areas for Improvement")
        for item in gap_data["disadvantages"][:5]:
            lines.append(f"- {item['requirement']}")
    
    return "\n".join(lines)


if __name__ == "__main__":
    # Demo
    requirements = [
        {"id": "REQ-001", "description": "Long battery", "importance": 5},
        {"id": "REQ-002", "description": "Lightweight", "importance": 4},
    ]
    
    ratings = {
        "REQ-001": {
            "our_product": {"level": "Mid", "score": 3, "evidence": "8 hours"},
            "competitor_a": {"level": "High", "score": 5, "evidence": "12 hours"}
        },
        "REQ-002": {
            "our_product": {"level": "High", "score": 5, "evidence": "1.0 kg"},
            "competitor_a": {"level": "Mid", "score": 3, "evidence": "1.5 kg"}
        }
    }
    
    benchmark = build_benchmark_table(requirements, {}, [], ratings)
    print(format_benchmark_table_markdown(benchmark))
    
    gaps = analyze_gaps(benchmark)
    print("\n" + format_gap_analysis_markdown(gaps))

#!/usr/bin/env python3
"""
House of Quality Builder
Builds the HOQ matrix, including the relationship matrix, roof-correlation matrix, and conflict analysis.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime


def build_relationship_matrix(
    requirements: List[Dict[str, Any]],
    features: List[Dict[str, Any]],
    relationships: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Build the requirement-feature relationship matrix.

    Args:
        requirements: requirement list [{id, description, importance, ...}]
        features: feature list [{id, name, value, unit, ...}]
        relationships: relationship definitions [{requirement_id, feature_id, strength}]
            strength: 9 (strong), 3 (medium), 1 (weak), 0 (none)

    Returns:
        relationship matrix data structure
    """
    rel_lookup = {}
    for rel in relationships:
        key = (rel["requirement_id"], rel["feature_id"])
        rel_lookup[key] = rel.get("strength", 0)
    
    matrix = []
    for req in requirements:
        req_relations = []
        for feat in features:
            key = (req["id"], feat["id"])
            strength = rel_lookup.get(key, 0)
            
            if strength >= 9:
                symbol = "◎"
            elif strength >= 3:
                symbol = "○"
            elif strength >= 1:
                symbol = "△"
            else:
                symbol = ""
            
            if strength > 0:
                req_relations.append({
                    "feature_id": feat["id"],
                    "feature": feat["name"],
                    "strength": strength,
                    "symbol": symbol
                })
        
        matrix.append({
            "requirement_id": req["id"],
            "requirement": req["description"],
            "importance": req.get("importance", 1),
            "relations": req_relations
        })
    
    feature_scores = calculate_feature_scores(requirements, features, rel_lookup)
    
    return {
        "matrix": matrix,
        "feature_scores": feature_scores
    }


def calculate_feature_scores(
    requirements: List[Dict],
    features: List[Dict],
    rel_lookup: Dict[Tuple[str, str], int]
) -> List[Dict[str, Any]]:
    """
    Compute feature importance scores.
    Score = Sum(requirement importance x relationship strength)
    """
    scores = []
    
    for feat in features:
        total_score = 0
        for req in requirements:
            key = (req["id"], feat["id"])
            strength = rel_lookup.get(key, 0)
            importance = req.get("importance", 1) or 1
            total_score += importance * strength
        
        scores.append({
            "feature_id": feat["id"],
            "feature": feat["name"],
            "score": total_score
        })
    
    scores.sort(key=lambda x: x["score"], reverse=True)
    for i, s in enumerate(scores):
        s["rank"] = i + 1
    
    return scores


def build_correlation_matrix(
    features: List[Dict[str, Any]],
    correlations: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Build the feature-correlation roof matrix.

    Args:
        features: feature list
        correlations: correlation definitions
            [{feature_a_id, feature_b_id, correlation, description}]
            correlation: "++", "+", "", "-", "--"
    """
    formatted_correlations = []
    
    for corr in correlations:
        feat_a = next((f for f in features if f["id"] == corr["feature_a_id"]), None)
        feat_b = next((f for f in features if f["id"] == corr["feature_b_id"]), None)
        
        if feat_a and feat_b:
            formatted_correlations.append({
                "feature_a": {"id": feat_a["id"], "name": feat_a["name"]},
                "feature_b": {"id": feat_b["id"], "name": feat_b["name"]},
                "correlation": corr.get("correlation", ""),
                "description": corr.get("description", "")
            })
    
    return {"correlations": formatted_correlations}


def identify_conflicts(
    requirements: List[Dict],
    features: List[Dict],
    correlations: List[Dict],
    rel_lookup: Dict[Tuple[str, str], int]
) -> Dict[str, Any]:
    """
    Identify technical conflicts.

    A technical conflict exists when two features are negatively correlated and
    each is strongly linked to different high-priority requirements.
    """
    conflicts = []
    conflict_id = 1
    
    for corr in correlations:
        if corr.get("correlation") in ["-", "--"]:
            feat_a_id = corr["feature_a_id"]
            feat_b_id = corr["feature_b_id"]
            
            affected_reqs_a = []
            affected_reqs_b = []
            
            for req in requirements:
                key_a = (req["id"], feat_a_id)
                key_b = (req["id"], feat_b_id)
                
                strength_a = rel_lookup.get(key_a, 0)
                strength_b = rel_lookup.get(key_b, 0)
                
                if strength_a >= 3:
                    affected_reqs_a.append(req["id"])
                if strength_b >= 3:
                    affected_reqs_b.append(req["id"])
            
            if affected_reqs_a and affected_reqs_b:
                feat_a = next((f for f in features if f["id"] == feat_a_id), None)
                feat_b = next((f for f in features if f["id"] == feat_b_id), None)
                
                severity = "high" if corr.get("correlation") == "--" else "medium"
                
                conflicts.append({
                    "id": f"CONFLICT-{conflict_id:03d}",
                    "type": "feature_vs_feature",
                    "severity": severity,
                    "feature_a": {
                        "id": feat_a_id,
                        "name": feat_a["name"] if feat_a else feat_a_id
                    },
                    "feature_b": {
                        "id": feat_b_id,
                        "name": feat_b["name"] if feat_b else feat_b_id
                    },
                    "affected_requirements": list(set(affected_reqs_a + affected_reqs_b)),
                    "description": corr.get("description", "Technical conflict between features")
                })
                conflict_id += 1
    
    return {"conflicts": conflicts}


def format_matrix_as_markdown(matrix_data: Dict) -> str:
    """Format the relationship matrix as a Markdown table."""
    matrix = matrix_data.get("matrix", [])
    feature_scores = matrix_data.get("feature_scores", [])
    
    if not matrix:
        return "Matrix is empty"
    
    all_features = set()
    for row in matrix:
        for rel in row["relations"]:
            all_features.add(rel["feature"])
    features = sorted(list(all_features))
    
    lines = []
    header = "| Requirement | Weight |"
    for f in features:
        header += f" {f[:8]} |"
    lines.append(header)
    
    sep = "|-------------|--------|"
    for _ in features:
        sep += "----------|"
    lines.append(sep)
    
    for row in matrix:
        line = f"| {row['requirement'][:15]} | {row['importance']} |"
        rel_dict = {r["feature"]: r["symbol"] for r in row["relations"]}
        for f in features:
            symbol = rel_dict.get(f, "")
            line += f" {symbol:^8} |"
        lines.append(line)
    
    lines.append(sep)
    score_line = "| **Score** | - |"
    score_dict = {s["feature"]: s["score"] for s in feature_scores}
    for f in features:
        score = score_dict.get(f, 0)
        score_line += f" {score:^8} |"
    lines.append(score_line)
    
    return "\n".join(lines)


def format_conflicts_summary(conflicts_data: Dict) -> str:
    """Format the conflict summary."""
    conflicts = conflicts_data.get("conflicts", [])
    
    if not conflicts:
        return "No technical conflicts found"
    
    lines = [f"Found {len(conflicts)} technical conflicts:\n"]
    
    for conf in conflicts:
        severity_icon = "[HIGH]" if conf["severity"] == "high" else "[MED]"
        lines.append(f"{severity_icon} {conf['id']}: {conf['feature_a']['name']} vs {conf['feature_b']['name']}")
        lines.append(f"   Severity: {conf['severity']}")
        lines.append(f"   Affected: {', '.join(conf['affected_requirements'])}")
        lines.append(f"   Note: {conf['description']}")
        lines.append("")
    
    return "\n".join(lines)


class HOQBuilder:
    """House of Quality Builder"""
    
    def __init__(self):
        self.requirements = []
        self.features = []
        self.relationships = []
        self.correlations = []
    
    def set_requirements(self, requirements: List[Dict]):
        self.requirements = requirements
    
    def set_features(self, features: List[Dict]):
        self.features = features
    
    def add_relationship(self, requirement_id: str, feature_id: str, strength: int):
        """Add a requirement-feature relationship (strength: 9/3/1/0)"""
        self.relationships.append({
            "requirement_id": requirement_id,
            "feature_id": feature_id,
            "strength": strength
        })
    
    def add_correlation(self, feature_a_id: str, feature_b_id: str, 
                       correlation: str, description: str = ""):
        """Add a feature-feature correlation (++/+/-/--)"""
        self.correlations.append({
            "feature_a_id": feature_a_id,
            "feature_b_id": feature_b_id,
            "correlation": correlation,
            "description": description
        })
    
    def build(self) -> Dict[str, Any]:
        """Build the complete HOQ data structure"""
        rel_lookup = {}
        for rel in self.relationships:
            key = (rel["requirement_id"], rel["feature_id"])
            rel_lookup[key] = rel.get("strength", 0)
        
        relationship_matrix = build_relationship_matrix(
            self.requirements, self.features, self.relationships
        )
        
        correlation_matrix = build_correlation_matrix(
            self.features, self.correlations
        )
        
        conflicts = identify_conflicts(
            self.requirements, self.features, self.correlations, rel_lookup
        )
        
        return {
            "relationship_matrix": relationship_matrix,
            "correlation_matrix": correlation_matrix,
            "conflicts": conflicts
        }


if __name__ == "__main__":
    # Demo
    requirements = [
        {"id": "REQ-001", "description": "Long battery life", "importance": 5},
        {"id": "REQ-002", "description": "Lightweight", "importance": 4},
    ]
    
    features = [
        {"id": "TECH-001", "name": "Weight"},
        {"id": "TECH-002", "name": "Battery Capacity"},
    ]
    
    builder = HOQBuilder()
    builder.set_requirements(requirements)
    builder.set_features(features)
    builder.add_relationship("REQ-001", "TECH-002", 9)
    builder.add_relationship("REQ-002", "TECH-001", 9)
    builder.add_relationship("REQ-002", "TECH-002", 3)
    builder.add_correlation("TECH-001", "TECH-002", "--", "Larger battery increases weight")
    
    result = builder.build()
    print(json.dumps(result, indent=2, ensure_ascii=False))

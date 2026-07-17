#!/usr/bin/env python3
"""
experiment-dataset-costing 主执行脚本

用法:
    python scripts/run_estimator.py \
        --targets "PD-L1,4-1BB" \
        --task-type multi-target \
        --use-case academic \
        --molecule-type small_molecule \
        --output-dir ./output

依赖:
    python-docx, pandas, requests
    智慧芽 PatSnap MCP 服务（需在 Eureka 中配置）
"""

import argparse
import json
import os
import csv
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="实验数据集构建成本预测工具")
    parser.add_argument("--targets", type=str, required=True,
                        help="靶点名称列表，逗号分隔，如 'PD-L1,4-1BB'")
    parser.add_argument("--task-type", type=str, required=True,
                        choices=["regression", "classification", "generation", "multi-target"],
                        help="建模任务类型")
    parser.add_argument("--use-case", type=str, required=True,
                        choices=["academic", "commercial"],
                        help="用途：academic 或 commercial")
    parser.add_argument("--molecule-type", type=str, default="small_molecule",
                        choices=["small_molecule", "antibody", "fusion_protein", "all"],
                        help="分子类型")
    parser.add_argument("--output-dir", type=str, default="./output",
                        help="输出目录")
    parser.add_argument("--output-language", type=str, default="zh",
                        choices=["zh", "en"], help="报告语言")
    parser.add_argument("--max-patents", type=int, default=20,
                        help="最大 SAR 提取专利件数（默认20件）")
    return parser.parse_args()


def estimate_data_volume(targets: list, molecule_type: str) -> dict:
    """
    根据靶点数量和分子类型估算各来源数据量。
    实际运行时应替换为 MCP API 调用结果。
    基准参数来自 references/database_coverage.md。
    """
    BASE_CHEMBL = {"PD-L1": 8000, "4-1BB": 2000}
    DEFAULT_PER_TARGET = 3000  # 未知靶点的默认估算

    chembl_total = sum(BASE_CHEMBL.get(t, DEFAULT_PER_TARGET) for t in targets)
    bindingdb_total = int(chembl_total * 0.35)
    pubchem_total = int(chembl_total * 0.25)
    patent_sar_total = int(chembl_total * 0.50)
    negative_samples = int(chembl_total * 0.75)
    literature_total = int(chembl_total * 0.06)

    raw_total = (
        chembl_total + bindingdb_total + pubchem_total +
        patent_sar_total + negative_samples + literature_total
    )
    admet_retention = 0.65  # ADMET 过滤后留存约65%
    net_total = int(raw_total * admet_retention)

    return {
        "chembl": chembl_total,
        "bindingdb": bindingdb_total,
        "pubchem": pubchem_total,
        "patent_sar": patent_sar_total,
        "negative_samples": negative_samples,
        "literature": literature_total,
        "raw_total": raw_total,
        "admet_retention_rate": admet_retention,
        "net_total": net_total,
    }


def estimate_cost(n_compounds: int, n_patents: int, n_targets: int, use_case: str) -> dict:
    """
    根据数据量和专利件数估算工时区间（人天）。
    参数来自 references/cost_benchmarks.md。
    """
    unit = max(n_compounds / 10000, 1)
    patent_unit = max(n_patents / 20, 1)

    days = {
        "collection": {
            "low": n_targets * 1.0, "mid": n_targets * 2.0, "high": n_targets * 4.0
        },
        "cleaning": {
            "low": unit * 1.5, "mid": unit * 3.5, "high": unit * 6.0
        },
        "admet": {
            "low": (n_compounds / 1000) * 0.3,
            "mid": (n_compounds / 1000) * 0.5,
            "high": (n_compounds / 1000) * 0.8,
        },
        "patent_sar": {
            "low": patent_unit * 0.5, "mid": patent_unit * 1.0, "high": patent_unit * 2.0
        },
        "report": {"low": 0.5, "mid": 1.0, "high": 2.0},
    }
    if use_case == "commercial":
        days["compliance"] = {"low": 2.0, "mid": 4.0, "high": 8.0}

    total = {
        k: round(sum(v[k] for v in days.values()), 1)
        for k in ["low", "mid", "high"]
    }
    return {"breakdown": days, "total": total}


def build_compliance_matrix(data_sources: list, use_case: str) -> list:
    """
    生成合规评级矩阵。
    规则来自 references/compliance_rules.md。
    """
    RULES = {
        "ChEMBL":      {"license": "CC BY-SA 4.0",       "academic": "✅", "commercial": "✅",  "risk": "低"},
        "BindingDB":   {"license": "CC BY 3.0",          "academic": "✅", "commercial": "✅",  "risk": "低"},
        "PubChem":     {"license": "公有领域",             "academic": "✅", "commercial": "✅",  "risk": "极低"},
        "PDB":         {"license": "CC0",                "academic": "✅", "commercial": "✅",  "risk": "极低"},
        "Patent-SAR":  {"license": "公开披露",             "academic": "✅", "commercial": "⚠️", "risk": "中-高"},
        "PatSnap-MCP": {"license": "服务条款",             "academic": "✅", "commercial": "✅",  "risk": "低"},
        "Literature":  {"license": "数值不受版权保护",      "academic": "✅", "commercial": "✅",  "risk": "极低"},
        "ZINC":        {"license": "开放获取",             "academic": "✅", "commercial": "⚠️", "risk": "中"},
    }
    return [
        {"source": src,
         **RULES.get(src, {"license": "未知", "academic": "❓", "commercial": "❓", "risk": "未知"})}
        for src in data_sources
    ]


def generate_outputs(config: dict, volume: dict, cost: dict,
                     compliance: list, output_dir: str) -> str:
    """生成结构化输出文件（JSON + CSV）。Word 报告由 Eureka Office 工作流处理。"""
    os.makedirs(output_dir, exist_ok=True)
    task_slug = ("-".join(config["targets"])
                 .lower()
                 .replace("/", "-")
                 .replace(" ", "_"))

    # 成本摘要 JSON
    cost_path = os.path.join(output_dir, f"{task_slug}-cost-summary.json")
    with open(cost_path, "w", encoding="utf-8") as f:
        json.dump({
            "task_slug": task_slug,
            "config": config,
            "data_volume": volume,
            "cost_estimation_days": cost,
        }, f, ensure_ascii=False, indent=2)
    print(f"[OK] 成本摘要已保存: {cost_path}")

    # 合规矩阵 CSV
    compliance_path = os.path.join(output_dir, f"{task_slug}-compliance-matrix.csv")
    with open(compliance_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f, fieldnames=["source", "license", "academic", "commercial", "risk"]
        )
        writer.writeheader()
        writer.writerows(compliance)
    print(f"[OK] 合规矩阵已保存: {compliance_path}")

    # 数据量清单 CSV
    inventory_path = os.path.join(output_dir, f"{task_slug}-data-inventory.csv")
    rows = [
        {"source": "ChEMBL",        "estimated_records": volume["chembl"]},
        {"source": "BindingDB",      "estimated_records": volume["bindingdb"]},
        {"source": "PubChem",        "estimated_records": volume["pubchem"]},
        {"source": "Patent-SAR",     "estimated_records": volume["patent_sar"]},
        {"source": "Negative/ZINC",  "estimated_records": volume["negative_samples"]},
        {"source": "Literature",     "estimated_records": volume["literature"]},
        {"source": "RAW TOTAL",      "estimated_records": volume["raw_total"]},
        {"source": f"NET (ADMET {int(volume['admet_retention_rate']*100)}% retained)",
         "estimated_records": volume["net_total"]},
    ]
    with open(inventory_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "estimated_records"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"[OK] 数据量清单已保存: {inventory_path}")

    return task_slug


def main():
    args = parse_args()
    targets = [t.strip() for t in args.targets.split(",")]

    print(f"\n{'='*60}")
    print(f"  实验数据集构建成本预测")
    print(f"  靶点: {targets}")
    print(f"  任务类型: {args.task_type}")
    print(f"  用途: {args.use_case}")
    print(f"{'='*60}\n")

    print("[Step 1/4] 估算各来源数据量...")
    volume = estimate_data_volume(targets, args.molecule_type)
    print(f"  预计总量（ADMET前）: {volume['raw_total']:,} 条")
    print(f"  ADMET 过滤后净量:    {volume['net_total']:,} 条")

    print("[Step 2/4] 计算工时成本...")
    cost = estimate_cost(
        n_compounds=volume["raw_total"],
        n_patents=args.max_patents,
        n_targets=len(targets),
        use_case=args.use_case,
    )
    t = cost["total"]
    print(f"  总工时估算: {t['low']}–{t['high']} 人天（中位 {t['mid']} 人天）")

    print("[Step 3/4] 生成合规评级矩阵...")
    sources = ["ChEMBL", "BindingDB", "PubChem", "PDB",
               "Patent-SAR", "PatSnap-MCP", "Literature", "ZINC"]
    compliance = build_compliance_matrix(sources, args.use_case)

    print("[Step 4/4] 写出结构化报告文件...")
    task_slug = generate_outputs(
        config={"targets": targets, "task_type": args.task_type,
                "use_case": args.use_case, "molecule_type": args.molecule_type},
        volume=volume, cost=cost, compliance=compliance,
        output_dir=args.output_dir,
    )

    print(f"\n{'='*60}")
    print(f"  ✅ 完成！任务标识: {task_slug}")
    print(f"  输出目录: {args.output_dir}")
    print(f"  Word 报告请通过 Eureka Office 工作流生成")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()

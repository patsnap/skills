#!/usr/bin/env python3
"""
feasibility-review 导出脚本
执行后自动将审查数据写入网站 data/review.json
用法：
  python export_json.py --output-dir /path/to/feasibility-platform/data
  python export_json.py  # 默认写入 ./data/review.json
"""

import json
import os
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path


def get_output_dir():
    """解析输出目录：优先读取 --output-dir 参数，其次读取环境变量，最后默认 ./data"""
    parser = argparse.ArgumentParser(description="Export feasibility-review data to JSON")
    parser.add_argument(
        "--output-dir",
        type=str,
        default=os.environ.get("REVIEW_OUTPUT_DIR", str(Path(__file__).parent.parent / "feasibility-platform" / "data")),
        help="目标目录路径（默认：../feasibility-platform/data）"
    )
    parser.add_argument(
        "--project-id",
        type=str,
        default=os.environ.get("PROJECT_ID", "latest"),
        help="项目ID，写入 _meta.project_id"
    )
    args, _ = parser.parse_known_args()
    return Path(args.output_dir), args.project_id


def load_review_output() -> dict:
    """
    从技能运行时上下文中收集审查数据。
    实际使用时，将技能各模块的输出替换到对应字段。
    """
    data = {
        "_meta": {
            "skill": "feasibility-review",
            "version": "1.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "project_id": "latest",
            "source_report": "report.json"
        },
        # ── 一、形式审查 ──────────────────────────────────────────
        "formal_review": {
            "text_standard": {
                "passed": True,
                "items": []           # [{name, status, issues:[]}]
            },
            "structure": {
                "passed": True,
                "items": []           # [{name, status, detail}]
            },
            "completeness": {
                "status": "pass",     # pass / warning / fail
                "files": []           # [{name, status, label}]
            },
            "consistency": {
                "passed": True,
                "items": []           # [{field, guide_value, report_value, status, diff?}]
            },
            "summary": {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "warning": 0,
                "pass_rate": 0,
                "issues": []          # [{id, level, location, desc}]
            }
        },
        # ── 二、实质审查 ──────────────────────────────────────────
        "substantial_review": {
            "tech_routes": [],        # [{id, title, desc, keywords:[]}]
            "innovations": [],        # [{id, title, source, desc}]
            "tech_route_review": [],  # 每条技术路线的专利/论文分析
            "innovation_review": [],  # 每个创新点的专利/论文分析
            "policy": {
                "total": 0,
                "high_relevance": 0,
                "match_status": "",   # 好 / 一般 / 差
                "trend": {
                    "years": [],
                    "counts": [],
                    "relevance": []
                },
                "top10": []           # [{rank, title, source, date, relevance}]
            }
        },
        # ── 审查总结 ──────────────────────────────────────────────
        "summary": {
            "rating": "",             # A / B / C
            "rating_desc": "",
            "recommendation": "",
            "scores": [],             # [{label, score, color}]
            "trend_fit": {
                "overall": "",
                "points": []          # [{title, desc}]
            },
            "competitors": [],        # [{rank, applicant, patents, advantage, threat}]
            "opportunities_challenges": {
                "opportunities": [],
                "challenges": [],
                "solutions": []
            }
        }
    }
    return data


def merge_with_existing(new_data: dict, existing_path: Path) -> dict:
    """将新数据与已有 JSON 合并，保留 existing 中 new_data 未覆盖的字段"""
    if not existing_path.exists():
        return new_data
    try:
        with open(existing_path, "r", encoding="utf-8") as f:
            existing = json.load(f)
        for key, val in new_data.items():
            if key == "_meta":
                continue
            if not val and key in existing:
                new_data[key] = existing[key]
    except (json.JSONDecodeError, OSError):
        pass
    return new_data


def write_json(data: dict, output_dir: Path, project_id: str) -> Path:
    """将数据序列化写入目标文件"""
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "review.json"

    data["_meta"]["project_id"] = project_id
    data["_meta"]["generated_at"] = datetime.now(timezone.utc).isoformat()

    data = merge_with_existing(data, output_path)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return output_path


def main():
    output_dir, project_id = get_output_dir()

    print(f"[feasibility-review] 开始导出 review.json")
    print(f"  → 目标目录：{output_dir}")
    print(f"  → 项目ID  ：{project_id}")

    data = load_review_output()
    output_path = write_json(data, output_dir, project_id)

    print(f"  ✅ 已写入：{output_path}")
    print(f"  → 刷新浏览器即可看到最新数据")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
根据检索结果JSON数据直接生成HTML简报
用法：
  MONITOR_DATA_JSON=data.json python generate_report.py --output report.html

  data.json 格式：
  {
    "company": "浙江孚邦",
    "report_date": "2026-05-24",
    "monitor_start": "2024-05-24",
    "monitor_end": "2026-05-24",
    "summary": {"high": 1, "medium": 1, "watch": 2, "low": 6},
    "inventors": [
      {
        "name": "陈伟海",
        "risk": "high",
        "new_org": "北京航空航天大学",
        "notes": "新申请专利与原公司外骨骼驱动技术高度相关，建议法务介入",
        "org_patents": [
          {"pn": "CN109646246A", "title": "一种穿戴式下肢外骨骼机器人伸屈装置", "year": "2019"}
        ],
        "new_patents": [
          {"pn": "CN119326632A", "title": "关节自校准的下肢康复外骨骼装置", "org": "北京航空航天大学", "date": "2024-08"}
        ]
      }
    ]
  }
"""

import json
import os
import sys
import argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from run_monitor import generate_html_report


def main():
    parser = argparse.ArgumentParser(description="从JSON数据生成监控简报HTML")
    parser.add_argument("--data", type=str, default=None, help="输入JSON数据文件路径")
    parser.add_argument("--output", type=str, default=None, help="输出HTML路径")
    args = parser.parse_args()

    data_file = args.data or os.environ.get("MONITOR_DATA_JSON")
    if not data_file:
        print("错误：请通过 --data 或 MONITOR_DATA_JSON 环境变量指定数据文件", file=sys.stderr)
        sys.exit(1)

    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    output_dir = os.environ.get("EUREKA_PYTHON_OUTPUT_DIR", ".")
    company = data.get("company", "unknown")
    date = data.get("report_date", "report")
    out = args.output or os.path.join(output_dir, f"inventor_monitor_{company}_{date}.html")

    generate_html_report(data, out)


if __name__ == "__main__":
    main()

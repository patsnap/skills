"""
corp_innovation_pipeline.py
企业科创力评估流水线脚本（供 Eureka python.run 调用）

输入环境变量（通过 EUREKA_PYTHON_OUTPUT_BINDINGS_JSON 获取输出路径）：
  COMPANY_NAME   企业名称（必填）
  MARKET         目标司法管辖区，逗号分隔，如 CN,US（可选，默认 CN）
  TOPK_PATENTS   最大专利检索数量（可选，默认 100）

输出：
  report.md      结构化 Markdown 简报
  data.json      原始聚合数据（供调试）
"""

import os
import json
from datetime import date

# ── 读取环境变量 ──────────────────────────────────────────────────────────────
company_name = os.environ.get("COMPANY_NAME", "").strip()
market_raw   = os.environ.get("MARKET", "CN").strip()
topk         = int(os.environ.get("TOPK_PATENTS", "100"))
markets      = [m.strip().upper() for m in market_raw.split(",") if m.strip()]

output_dir = os.environ.get("EUREKA_PYTHON_OUTPUT_DIR", ".")

if not company_name:
    raise ValueError("COMPANY_NAME 环境变量不能为空")

# ── 占位符：实际调用由 Eureka Agent 在对话层完成 ─────────────────────────────
# 本脚本定义了数据结构规范，供 Agent 在组装报告时参考。
# 在 Eureka 技能执行中，以下步骤由 Agent 通过 patsnap_search / patsnap_fetch
# / web_search 工具完成，结果以 JSON 形式传入 report_data 字典。

report_data = {
    "company_name": company_name,
    "report_date": str(date.today()),
    "markets": markets,
    "patents": [],          # Step 1 结果
    "core_patents": [],     # Step 2 Top 10 高价值专利（含摘要）
    "ipc_clusters": {},     # Step 2 技术方向聚类
    "portfolio_stats": {    # Step 3
        "by_year": {},
        "legal_status": {"active": 0, "pending": 0, "inactive": 0},
        "citation": {"total": 0, "avg": 0.0, "max_patent": ""},
        "by_jurisdiction": {}
    },
    "papers": [],           # Step 4
    "company_overview": "", # Step 5
    "market_position": "",  # Step 5
    "risk_signals": "",     # Step 5
    "scores": {             # Step 6
        "patent_activity":  "Medium",
        "tech_barrier":     "Medium",
        "geo_coverage":     "Medium",
        "rd_continuity":    "Medium",
        "risk_level":       "Low"
    }
}

# ── 生成骨架报告（Agent 会在对话层填充真实内容）─────────────────────────────
report_md = f"""# 企业科创力分析简报
**企业名称：** {company_name}
**报告日期：** {report_data['report_date']}
**数据来源：** PatSnap 专利数据库 / 学术论文库 / 公开网络
**免责说明：** 本报告基于公开数据，仅供信贷参考，不构成最终信贷决策依据。

---

## 一、公司概况

暂待 Agent 填充

---

## 二、主营业务与产品矩阵

暂待 Agent 填充

---

## 三、与主营业务相关的核心专利及技术方向

暂待 Agent 填充

---

## 四、专利组合分析

暂待 Agent 填充

---

## 五、市场地位与战略合作

暂待 Agent 填充

---

## 六、信贷评审关注点与风险提示

暂待 Agent 填充

---

*本报告由 Eureka · PatSnap 智慧芽 自动生成，数据截止日期：{report_data['report_date']}。*
"""

# ── 写出文件 ──────────────────────────────────────────────────────────────────
report_path = os.path.join(output_dir, "report.md")
data_path   = os.path.join(output_dir, "data.json")

with open(report_path, "w", encoding="utf-8") as f:
    f.write(report_md)

with open(data_path, "w", encoding="utf-8") as f:
    json.dump(report_data, f, ensure_ascii=False, indent=2)

print(f"[corp_innovation_pipeline] 骨架报告已写出：{report_path}")
print(f"[corp_innovation_pipeline] 数据结构已写出：{data_path}")

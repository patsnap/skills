# README 模板

# {{TOPIC}} — 专利机会评估报告

**生成时间：** {{REPORT_DATE}}  
**数据来源：** 智慧芽（PatSnap）专利数据库  
**生成工具：** Eureka × PatSnap `opportunities` Skill  

---

## 📁 文件清单

| 文件 | 用途 | 数据类型 |
|------|------|----------|
| `index.html` | **主报告页**，包含趋势图、申请人分析、评分、专利布局建议等 | 全量统计 + 代表样本 |
| `patents.html` | 代表性专利样本详情（≥50条），含搜索和筛选功能 | evidence_sample |
| `evidence.html` | 证据链，每个结论绑定数据来源和支撑专利 | 全量统计 + 代表样本 |
| `subfields.html` | 子技术分支分析，含各分支趋势、申请人、机会评分 | 全量统计 + 代表样本 |
| `methodology.html` | 方法与限制说明，检索式、统计口径、质量核查 | 方法说明 |
| `intermediate_data.json` | 结构化中间数据，报告的完整数据基础 | 全量统计 + 代表样本 |
| `patent_list.csv` | 代表专利样本列表（CSV格式） | evidence_sample |
| `evidence_mapping.csv` | 结论-证据映射表（CSV格式） | 全量统计 + 代表样本 |
| `README.md` | 本文件，文件说明 | — |
| `quality_check.md` | 质量核查报告 | — |

> ⚠️ **注意：** 无任何 `.py` 文件。本报告完全通过 MCP 工具、文件写入和模型能力生成。

---

## 🚀 如何查看报告

1. **主报告**：直接用浏览器打开 `index.html`
2. **专利详情**：打开 `patents.html`，支持搜索和按国家/法律状态筛选
3. **证据链**：打开 `evidence.html`，查看每个结论的数据依据
4. **子技术分析**：打开 `subfields.html`，查看各子方向机会评分
5. **方法说明**：打开 `methodology.html`，查看检索式和统计口径

---

## 📊 数据说明

### 全量统计（full_scope_metrics）
用于报告中所有图表、趋势判断、排名、占比分析：
- 来源：PatSnap 专利分析 MCP 全量统计接口
- 年度趋势：2015年至{{REPORT_DATE}}年
- 申请人排名：全量 Top 20
- 地域分布：全量优先权国家统计
- 法律状态：全量统计

### 代表性专利样本（evidence_sample）
仅用于技术说明和证据链：
- 来源：PatSnap 专利检索，相关性排序 TopK
- 用途：Top 10 代表专利、patents.html、证据链、申请人案例
- **严禁将此样本用于趋势推断**

---

## ⚠️ 限制说明

{{LIMITATIONS_TEXT}}

---

## 📋 评分摘要

| 项目 | 结果 |
|------|------|
| 综合推荐指数 | {{TOTAL_SCORE}} / 100 |
| 研发进入建议 | {{REC_TEXT}} |
| 投资吸引力 | {{INVEST_ATTRACT}} |
| 竞争风险 | {{COMPETITION_RISK}} |
| 证据置信度 | {{EVIDENCE_CONF}} |

---

## 🔒 免责声明

本报告基于专利公开信息，不构成法律意见，不构成投资建议，不替代 FTO、市场调研、法规评估和技术专家判断。

# 示例输出：PD-L1 × 4-1BB 双靶点小分子结构预测模型数据集构建方案

> 本文件为 experiment-dataset-costing 技能的示例输出。
> 对应 Eureka 会话：2026-06-30
> 输入参数：targets=["PD-L1","4-1BB"], task_type="multi-target", use_case="academic"

---

## 智慧芽 MCP 检索结果摘要

| 检索维度 | 结果 |
|---|---|
| PD-L1 相关 Phase 2+ 药物 | 53 款 |
| 4-1BB 相关药物 | 245 款 |
| 双靶（PD-L1×4-1BB）药物 | 459 款 |
| 化合物专利池 | 2,025+ 件 |
| 相关文献 | 34,742 篇 |

代表性双靶药物：Acasunlimab、Opamtistomig、Sotiburafusp alfa、Cenopodlin、MAX-10181、ABSK-043

---

## 数据量估算

| 来源 | 预估条目 |
|---|---|
| ChEMBL（PD-L1） | ~8,000 |
| ChEMBL（4-1BB） | ~2,000 |
| BindingDB | ~3,000 |
| 专利 SAR（智慧芽） | ~4,000 |
| PubChem HTS | ~2,000 |
| 负样本/ZINC | ~6,000 |
| 文献补充 | ~500 |
| **合计（ADMET 前）** | **~25,500** |
| ADMET 净留存（65%） | **~16,575** |

---

## 成本估算（学术场景）

| 工项 | 工时（低-高） | 中位 |
|---|---|---|
| 数据采集（脚本化） | 3–5 人天 | 4 人天 |
| 数据清洗 & 去重 | 4–7 人天 | 5.5 人天 |
| ADMET 批量预测 | 0.5–1.5 人天 | 1 人天 |
| 专利 SAR 提取 | 3–6 人天 | 4.5 人天 |
| 报告撰写 | 1–2 人天 | 1.5 人天 |
| **合计** | **11.5–21.5 人天** | **16.5 人天** |

---

## 合规评级（学术用途）

所有数据源均为 ✅ 绿色，无合规障碍。

---

## 输出文件

- `pdl1-4-1bb-dataset-scheme.docx` — 完整方案报告（7 章 + 附录，~44 KB）
- `pdl1-4-1bb-cost-summary.json` — 结构化成本估算
- `pdl1-4-1bb-compliance-matrix.csv` — 合规矩阵
- `pdl1-4-1bb-data-inventory.csv` — 数据量清单

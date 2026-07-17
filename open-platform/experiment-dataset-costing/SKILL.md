---
name: experiment-dataset-costing
description: "估算实验和科研数据集所需资源、周期与成本。适用于：估算实验或训练数据集构建所需的人力、样本、试剂、设备、算力、采购和交付成本，用于预算规划与报价复核。"
---

# Experiment Dataset Cost Estimator

## 目标（Objective）

给定一个或多个药物靶点（或疾病领域），自动完成：

1. 公开数据库可用数据量评估（ChEMBL / BindingDB / PubChem / PDB）
2. 智慧芽专利库化学结构 SAR 提取量估算
3. 负样本与 ADMET 过滤后净数据量预测
4. 合规风险分级（学术研究 / 商业产品两个维度）
5. 数据工程工作量与成本区间估算
6. 输出完整的数据集构建方案报告（Word 格式）

## 输入参数（Inputs）

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `targets` | List[str] | ✅ | 靶点名称列表，如 `["PD-L1", "4-1BB"]` |
| `task_type` | str | ✅ | 建模任务：`regression` / `classification` / `generation` / `multi-target` |
| `use_case` | str | ✅ | 用途：`academic`（学术研究）/ `commercial`（商业产品） |
| `molecule_type` | str | ✅ | 分子类型：`small_molecule` / `antibody` / `fusion_protein` / `all` |
| `output_language` | str | ❌ | 报告语言，默认 `zh`（中文），支持 `en` |
| `max_patents` | int | ❌ | SAR 提取最大专利件数，默认 20 |

## 工作流步骤（Workflow）

### Step 1 — 实体规范化
调用 `ls_ner_nor_normalize` 对输入靶点名称进行标准化，获取靶点 ID、UniProt 号、别名等。

### Step 2 — 药物情报与靶点覆盖评估
并行调用：
- `ls_drug_search(target=[...], highest_phase=["approved","phase_3","phase_2"])` — 统计已知活性药物数量
- `ls_target_fetch(target=[...])` — 获取靶点结构域、表达、通路信息

输出：靶点热度评分、数据稀缺性预警。

### Step 3 — 专利化学结构估算
调用 `ls_patent_search(target=[...], patent_core_type=["product_compound"])` 检索化合物专利数量。
对 Top-10 代表性专利依次调用：
- `ls_patent_structure_fetch(pn=...)` — 获取专利关联化合物数
- `ls_sar_submit(pn=...)` → 轮询 `ls_sar_fetch(task_id=...)` — 提取 SAR 结构-活性对

根据样本专利平均化合物数外推全库估算量。

### Step 4 — ADMET 预筛选规模预测
对 Step 3 提取的代表性化合物 SMILES 批量调用：
- `ls_admet_predict(smiles=[...])` — 预测 AMES 阳性率、hERG 风险比例

根据实测淘汰率推算 ADMET 净留存比例，修正最终有效数据量预测。

### Step 5 — 文献数据量评估
- `ls_paper_search(target=[...], limit=1)` — 统计文献总量
- `ls_translational_medicine_search(target=[...], limit=1)` — 获取转化医学条目数

### Step 6 — 合规性矩阵生成
基于数据源类型，套用 `references/compliance_rules.md` 规则模板，
生成每类数据源的学术 / 商业合规评级与风险等级。

### Step 7 — 成本估算
读取 `references/cost_benchmarks.md` 中的工时基准参数，结合数据量预测，计算：
- 数据采集 / 清洗 / ADMET / SAR 提取 / 报告工时（人天，低/中/高区间）
- 计算资源成本（CPU/GPU 小时）

### Step 8 — 报告生成
调用 Office 工作流（`office` plan_workspace → run_builder → finalize）生成 Word 报告，
包含：方案概述、数据来源体系、字段规范、质量控制、合规评估、成本估算表、MCP 调用路线图。

## 示例（Examples）

### 示例 1 — PD-L1 × 4-1BB 双靶点小分子结构预测数据集（Eureka 会话 2026-06-30）

**输入：**
```json
{
  "targets": ["PD-L1", "4-1BB"],
  "task_type": "multi-target",
  "use_case": "academic",
  "molecule_type": "small_molecule",
  "output_language": "zh"
}
```

**智慧芽 MCP 检索结果摘要：**

| 检索维度 | 结果 |
|---|---|
| PD-L1 相关 Phase 2+ 药物 | 53 款 |
| 4-1BB 相关药物 | 245 款 |
| 双靶（PD-L1×4-1BB）药物 | 459 款 |
| 化合物专利池 | 2,025+ 件 |
| 相关文献 | 34,742 篇 |

代表性双靶药物：Acasunlimab、Opamtistomig、Sotiburafusp alfa、Cenopodlin、MAX-10181、ABSK-043

**数据量估算：**

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
| ADMET 净留存（约 65%） | **~16,575** |

**成本估算（学术场景）：**

| 工项 | 工时（低-高） | 中位 |
|---|---|---|
| 数据采集（脚本化） | 3–5 人天 | 4 人天 |
| 数据清洗 & 去重 | 4–7 人天 | 5.5 人天 |
| ADMET 批量预测 | 0.5–1.5 人天 | 1 人天 |
| 专利 SAR 提取 | 3–6 人天 | 4.5 人天 |
| 报告撰写 | 1–2 人天 | 1.5 人天 |
| **合计** | **11.5–21.5 人天** | **16.5 人天** |

**合规评级：** 学术使用 ✅ 全绿；商业使用 ⚠️ 专利 SAR 化合物需侵权评估

**输出文件：** `pdl1-4-1bb-dataset-scheme.docx`（7 章 + 附录，~44 KB）

详见 `assets/example_output_pdl1_4-1bb.md`。

## 输出物（Outputs）

| 文件 | 描述 |
|---|---|
| `{task_slug}-dataset-scheme.docx` | 完整数据集构建方案 Word 报告（7 章 + 附录） |
| `{task_slug}-cost-summary.json` | 结构化成本估算 JSON，可接入项目管理工具 |
| `{task_slug}-compliance-matrix.csv` | 各数据源合规评级矩阵 |
| `{task_slug}-data-inventory.csv` | 预估数据量清单（按来源分层） |

## 注意事项（Guardrails）

- 数据量估算为区间预测，实际值受靶点热度、专利密度、ChEMBL 收录深度影响，误差范围约 ±30%
- 专利 SAR 提取需逐件调用 `ls_sar_submit`，大批量时建议分批（每批 ≤20 件），避免任务超时
- ADMET 预测结果为 AI 模型输出，不替代实验验证
- 商业场景下的合规评估仅为初步风险提示，最终需法律团队审查
- 本技能不直接执行数据下载，数据采集脚本需在本地或云端独立运行

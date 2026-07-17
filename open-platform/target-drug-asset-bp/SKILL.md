---
name: target-drug-asset-bp
description: "支持靶点药物科研成果转化评估和资产BP编制。适用于：将高校、医院或科研机构的靶点/药物成果整理为转化成熟度、知识产权、竞争格局、合作方匹配和资产BP。"
---

# RD&BD · Asset-BP · Target & Drug & Evidence & Patent

## 用途

将高校、医院或科研机构的生物医药科研成果（靶点发现、候选药物、机制研究、专利或论文方向）包装成企业 BD、创新药公司、投资人、孵化器可快速判断的**成果转化包**。

此 skill **不输出情报简报**，而是输出可用于技术转移、企业路演、合作洽谈、项目尽调的结构化交付物。

> 与 `rd-bd-evaluate-target-drug-evidence-patent` 的区别：本 skill 面向**技术转化 BP / 路演 / 尽调材料**，输出六块转化包；彼 skill 面向**靶点立项分诊**，输出 Go/No-Go Scorecard。

---

## 命名说明（PatSnap Skill Namer）

| 维度 | 值 | 说明 |
|---|---|---|
| Audience | `RD&BD` | 转化医学/研发评估 + BD/技术转让团队 |
| Need | `asset-bp` | 为路演/BP汇聚竞争力评估、临床价值、合作方画像 |
| Data | `target&drug&evidence&patent` | ls_target_fetch / ls_drug_search / ls_translational_medicine_search / ls_patent_search |
| Modality | 省略 | 通用，不聚焦特定药物模态 |

原始描述性名称：`university-tech-transfer-packager`

---

## 触发场景

- 用户提供高校/机构科研项目描述、靶点、论文、专利号、PI 姓名或课题名称
- 用户询问某项基础研究成果的产业化可行性
- 用户需要为技术转让、BD 路演或投资人尽调准备材料
- 触发词：成果转化、技术转让、技术转移、BD 材料、项目尽调、产业化评估、高校成果包装

---

## 核心工作流（概览）

详细执行路径见 `references/workflow.md`。

1. **输入解析**：识别 target、disease、drug、mechanism、technology modality、institution、PI、patent、publication、project stage
2. **实体标准化**：如有具体实体，调用 `ls_ner_nor_normalize`；否则先做假设提取
3. **科学证据归纳**：调用 `ls_target_fetch`、`ls_translational_medicine_search`、`ls_paper_vector_search`
4. **临床路径判断**：调用 `ls_drug_search`、`ls_clinical_trial_search`、`ls_clinical_trial_result_search`
5. **指南与未满足需求**：如可用，调用 `ls_clinical_guideline_vector_search`
6. **专利与权属准备度**：调用 `ls_patent_search` / `ls_patent_fetch`（工具实际名称以当前 MCP tools/list 为准）
7. **合作方画像**：如用户提供机构名称，调用 `ls_organization_pipeline_fetch`
8. **生成转化包**：输出六块固定结构（见下）

MCP 工具完整参数映射见 `references/mcp-tool-map.md`。

---

## 默认输入假设

| 场景 | 处理方式 |
|---|---|
| 无明确 target | 从疾病/机制描述中做候选靶点假设，在输出中显式标注 |
| 无专利号 | 输出专利布局建议和需补充材料，不停止流程 |
| 无企业合作目标 | 默认面向中国创新药企业和产业孵化场景 |
| 无项目阶段 | 默认按 early research / preclinical translation 处理 |
| 关键材料缺失 | 评分标注 Insufficient Materials，列出缺失项 |

所有关键假设必须在输出中用 **【假设】** 标注。

---

## 成果转化成熟度评分

详细评分规则见 `references/assessment-rubric.md`。

| 标签 | 分数 | 含义 |
|---|---|---|
| Transfer Ready | 80–100 | 适合进入企业 BD 或路演材料 |
| Partnering Candidate | 65–79 | 适合定向找企业合作，需补充若干证据 |
| Incubation Needed | 45–64 | 适合继续孵化、补实验、补专利 |
| Research Only | < 45 | 更适合论文/基础研究，暂不建议产业化 |
| Insufficient Materials | — | 关键材料缺失，无法判断 |

---

## 固定输出结构（六块）

输出模板见 `references/output-templates.md`。

1. **Project Snapshot** — 项目基本信息与关键假设
2. **Commercial Translation Thesis** — 转化命题与商业逻辑
3. **Evidence & Differentiation Matrix** — 证据矩阵与差异化分析
4. **IP and Ownership Readiness** — 专利与权属准备度
5. **Partner / Licensee Fit** — 合作方画像与优先级
6. **Next-Step Package** — 下一步行动建议与尽调清单

---

## 重要约束

- 不做情报简报（使用 `pharma-intel-briefing` skill 代替）
- 不做靶点立项 scorecard（使用 `rd-bd-evaluate-target-drug-evidence-patent` skill 代替）
- 输出必须面向非科学家受众（BD/投资人）可读
- 所有关键数据必须标注来源（`[S#]` 格式）
- 所有假设必须显式标注

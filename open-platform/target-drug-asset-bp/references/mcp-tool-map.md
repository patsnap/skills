# MCP 工具映射表 — university-tech-transfer-packager

> **重要说明**：工具实际可用性以当前会话 `MCP tools/list` 为准。如下列工具名与当前环境不匹配，请使用最接近功能的可用工具并在输出中注明替代情况。

---

## 工具映射总表

| 工作流阶段 | 工具逻辑名 | 当前环境实际工具名 | 用途 | 必须/可选 |
|---|---|---|---|---|
| 实体标准化 | `ls_ner_nor_normalize` | `mcp_tool-collection-pharma-intelligence__ls_ner_nor_normalize` | 从原始文本中提取并标准化靶点、疾病、药物、机构实体 | 推荐 |
| 靶点确认 | `ls_target_fetch` | `mcp_tool-collection-pharma-intelligence__ls_target_fetch` | 获取靶点生物学信息、已知疾病关联、已有药物 | 必须 |
| 药物格局 | `ls_drug_search` | `mcp_tool-collection-pharma-intelligence__ls_drug_search` | 同靶点/适应症/技术路线的药物竞争格局 | 必须 |
| 里程碑历史 | `ls_drug_milestone_fetch` | `mcp_tool-collection-pharma-intelligence__ls_drug_milestone_fetch` | 核心竞品开发里程碑时间线 | 推荐 |
| 临床试验 | `ls_clinical_trial_search` | `mcp_tool-collection-pharma-intelligence__ls_clinical_trial_search` | 试验数量、阶段分布、活跃状态、失败信号 | 必须 |
| 临床结果 | `ls_clinical_trial_result_search` | `mcp_tool-collection-pharma-intelligence__ls_clinical_trial_result_search` | 已读出临床结果、关键终点、失败先例 | 必须 |
| 转化医学 | `ls_translational_medicine_search` | `mcp_tool-collection-pharma-intelligence__ls_translational_medicine_search` | 人群验证、biomarker 关联、机制支持文献 | 必须 |
| 临床指南 | `ls_clinical_guideline_vector_search` | `mcp_tool-collection-pharma-intelligence__ls_clinical_guideline_vector_search` | 当前治疗指南、未满足患者需求 | 可选 |
| 专利检索 | `ls_patent_search` | `mcp_tool-collection-pharma-intelligence__ls_patent_search` | 相关专利数量、权利人、IPC、地域覆盖 | 推荐 |
| 专利详情 | `ls_patent_fetch` | `mcp_patent-search__patsnap_fetch`（PatSnap 侧）或 `mcp_tool-collection-pharma-intelligence__ls_patent_fetch` | 权利要求范围、法律状态、到期日、同族布局 | 可选（有专利号时必须）|
| 合作方管线 | `ls_organization_pipeline_fetch` | `mcp_tool-collection-pharma-intelligence__ls_organization_pipeline_fetch` | 目标企业研发管线、方向匹配度判断 | 可选 |
| 文献支撑 | `ls_paper_search` / `ls_paper_vector_search` | `mcp_tool-collection-pharma-intelligence__ls_paper_search` / `__ls_paper_vector_search` | 机制论文、人群研究、动物模型结果 | 可选 |

---

## 工具调用优先级与顺序

```
[推荐] ls_ner_nor_normalize（有实体时）
    ↓
[必须] ls_target_fetch
    ↓
[并行] ls_drug_search + ls_translational_medicine_search
    ↓
[必须] ls_clinical_trial_search + ls_clinical_trial_result_search
    ↓
[可选] ls_clinical_guideline_vector_search
    ↓
[推荐] ls_patent_search（→ ls_patent_fetch，如有专利号）
    ↓
[可选] ls_organization_pipeline_fetch（如提供目标机构）
    ↓
生成转化包
```

---

## 关键参数说明

### ls_ner_nor_normalize
```
user_input: 用户原始完整输入（不得修改或预处理）
```

### ls_target_fetch
```
target: ["靶点名称"]  # 优先使用标准化后的名称
target_ids: ["uuid"]  # 如 ner_nor 返回了 normalized_id
```

### ls_drug_search
```
target: ["靶点名称"]
disease: ["疾病名称"]
drug_type: ["Small molecule drug"]  # 可选，按技术路线
limit: 20
```

### ls_clinical_trial_search
```
target: ["靶点名称"]
disease: ["疾病名称"]
limit: 20
# 关注 study_status: terminated / withdrawn / completed
```

### ls_patent_search（Pharma Intelligence 侧）
```
target: ["靶点名称"]
disease: ["疾病名称"]
organization: ["机构名称"]  # 可选
limit: 20
```

### mcp_patent-search__patsnap_search（PatSnap 侧）
```
search_strategy: ["keyword", "filter"]
keywords: ["靶点", "疾病", "技术关键词"]
filters:
  assignees: ["机构名称"]  # 可选
  jurisdiction: ["CN", "US"]  # 默认关注 CN/US/EP
limit: 20
```

### ls_organization_pipeline_fetch
```
organization: "企业名称"  # 输入名称，服务内部解析 ID
limit: 10
```

---

## 工具失败处理

| 工具 | 失败时处理方式 |
|---|---|
| ls_ner_nor_normalize | 跳过，使用原始文本继续，在输出标注"未标准化" |
| ls_target_fetch | 跳过，基于现有信息推断，标注【假设】 |
| ls_patent_search | 输出"专利数据待补充"，给出建议检索策略 |
| ls_clinical_guideline_vector_search | 跳过，基于 ls_clinical_trial 数据推断未满足需求 |
| ls_organization_pipeline_fetch | 跳过，基于药物格局数据推导合作方 |

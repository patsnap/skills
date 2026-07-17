# MCP Tool Map — RD&BD Evaluate Target×Drug×Evidence×Patent

本文件列出本 skill 所使用的智慧芽（Patsnap）MCP 工具映射。

> **优先级规则**：以当前会话实际 `MCP tools/list` 为准。如工具名与本文件不符，以实际注册名优先，并在输出中说明差异。

---

## 核心工具（必须调用）

### 1. `ls_ner_nor_normalize`
- **MCP Server**：`tool-collection-pharma-intelligence`
- **用途**：实体标准化——靶点、药物、疾病、机构名称规范化
- **调用时机**：Step 1，有具体实体输入时优先调用

### 2. `ls_target_fetch`
- **MCP Server**：`tool-collection-pharma-intelligence`
- **用途**：确认靶点信息，获取别名、基因符号、pathway 关联
- **调用时机**：Step 2

### 3. `ls_drug_search`
- **MCP Server**：`tool-collection-pharma-intelligence`
- **用途**：获取同靶点在研/已上市药物格局
- **调用时机**：Step 3

### 4. `ls_drug_milestone_fetch`
- **MCP Server**：`tool-collection-pharma-intelligence`
- **用途**：获取关键药物研发里程碑，识别失败/暂停/撤回事件
- **调用时机**：Step 4

### 5. `ls_clinical_trial_search`
- **MCP Server**：`tool-collection-pharma-intelligence`
- **用途**：获取临床活跃度——在研试验数量、阶段分布
- **调用时机**：Step 5

### 6. `ls_clinical_trial_result_search`
- **MCP Server**：`tool-collection-pharma-intelligence`
- **用途**：获取已发布临床结果，标记失败/阴性/安全性问题
- **调用时机**：Step 6

### 7. `ls_translational_medicine_search`
- **MCP Server**：`tool-collection-pharma-intelligence`
- **用途**：获取转化医学证据——生物标志物、动物模型、机制研究
- **调用时机**：Step 7

---

## 可选工具（按可用性调用）

### 8. `ls_clinical_guideline_vector_search`
- **MCP Server**：`tool-collection-pharma-intelligence`
- **用途**：检索临床指南中对该适应症的标准治疗路径和未满足需求
- **调用时机**：Step 8（disease 不为空时调用）

### 9. 专利工具组合

#### 9a. `ls_patent_search`
- **MCP Server**：`tool-collection-pharma-intelligence`
- **用途**：评估专利密度、申请人集中度、近年申请趋势

#### 9b. `mcp_patent-search__patsnap_search`
- **MCP Server**：`patent-search`
- **用途**：广谱专利检索，专利拥挤度全景扫描

#### 9c. `mcp_patent-search__patsnap_fetch`
- **MCP Server**：`patent-search`
- **用途**：获取特定专利全文，分析权利要求范围

---

## 工具调用顺序总览

```
Step 1  → ls_ner_nor_normalize              [必须，有实体时]
Step 2  → ls_target_fetch                   [必须]
Step 3  → ls_drug_search                    [必须]
Step 4  → ls_drug_milestone_fetch           [必须，对 Phase 2+ 药物]
Step 5  → ls_clinical_trial_search          [必须]
Step 6  → ls_clinical_trial_result_search   [必须]
Step 7  → ls_translational_medicine_search  [必须]
Step 8  → ls_clinical_guideline_vector_search [可选，disease 不为空时]
Step 9  → ls_patent_search + patsnap_search + patsnap_fetch [可选]
```

## 并行调用建议

- Step 5 + Step 6 + Step 7 可并行
- Step 8 + Step 9 可并行
- Step 4 需要 Step 3 的 `drug_id`，不可并行

---

## 工具名称映射表

| 本文件简称 | 实际调用名（Eureka MCP格式） |
|---|---|
| `ls_ner_nor_normalize` | `mcp_tool-collection-pharma-intelligence__ls_ner_nor_normalize` |
| `ls_target_fetch` | `mcp_tool-collection-pharma-intelligence__ls_target_fetch` |
| `ls_drug_search` | `mcp_tool-collection-pharma-intelligence__ls_drug_search` |
| `ls_drug_milestone_fetch` | `mcp_tool-collection-pharma-intelligence__ls_drug_milestone_fetch` |
| `ls_clinical_trial_search` | `mcp_tool-collection-pharma-intelligence__ls_clinical_trial_search` |
| `ls_clinical_trial_result_search` | `mcp_tool-collection-pharma-intelligence__ls_clinical_trial_result_search` |
| `ls_translational_medicine_search` | `mcp_tool-collection-pharma-intelligence__ls_translational_medicine_search` |
| `ls_clinical_guideline_vector_search` | `mcp_tool-collection-pharma-intelligence__ls_clinical_guideline_vector_search` |
| `ls_patent_search` | `mcp_tool-collection-pharma-intelligence__ls_patent_search` |
| `patsnap_search` | `mcp_patent-search__patsnap_search` |
| `patsnap_fetch` | `mcp_patent-search__patsnap_fetch` |

> 以上映射以当前会话 MCP tools/list 为准，如有变动请以实际注册名为准。

---
name: applicant-tech-patent-retrieval
description: 面向指定申请人并限定技术主题开展专利检索。适用于用户需要检索某公司/申请人在特定技术领域的专利、构建“申请人优先 + 技术主题约束”的智慧芽检索式、扩展申请人法律主体和名称变体、拆解技术主题为可检索要素、组合申请人表达式与主题公式、按申请和简单同族去重，并生成检索数据集及 Markdown/Word 报告的场景。不适用于没有技术主题限制的纯申请人全量检索、没有目标申请人的纯技术全景分析，或检索完成后的下游技术筛选任务。
---

# 申请人技术主题专利检索

## 目的

本 Skill 用于“以申请人为主线、同时限定技术主题”的专利检索。流程保留申请人检索所需的主体扩展、实体证据、合并去重、代表性数据集和检索报告要求，并叠加类似 `patsnap-topic-search-strategy` 的技术主题限定层。

执行检索前，请根据任务需要读取以下参考文件：

- [references/applicant-retrieval-workflow.md](references/applicant-retrieval-workflow.md)：申请人实体扩展、申请人字段确认、检索、合并、去重和报告产物要求。
- [references/topic-limitation-workflow.md](references/topic-limitation-workflow.md)：主题定义、主题拆解、术语矩阵、分层主题公式、申请人-主题组合与校验门禁。

## 不可跳过的门禁

### 0. 公式生成防火墙

- 默认流程必须分阶段推进。Skill 触发后的第一轮回答，只输出 Step 0 至 Step 7，并请用户确认门禁状态；除非用户明确要求“包含公式的完整草稿”，否则不得在同一轮输出 Step 8 的公式。
- 绝对规则：在检索前校验包完整写出之前，不得输出任何正式检索策略、申请人表达式、主题表达式、组合公式、`ANCS`、`TA_ALL`、`APPLICANT_TOPIC_FINAL` 或可执行的 PatSnap/智慧芽查询。
- 检索前校验包必须真实出现在回答中，不能只存在于内部推理。
- 如果回答中出现 `Step 3: Formal Search Strategy`、`正式检索策略`、`Applicant expression`、`Topic expression` 或 `Combined query` 等章节，但其前文没有完整检索前校验包，则该回答无效。
- 即使用户要求“直接跑”“给公式”“正式检索”或“继续”，也必须先补齐缺失的检索前校验包。
- 如果工具结果、连接器兜底或上一轮部分回答直接跳到公式生成，必须忽略该捷径，回到缺失门禁。

检索前校验包必须按以下顺序输出：

```text
Step 0：原始需求与执行模式
Step 1：申请人实体扩展表
Step 2：技术主题定义
Step 3：技术边界确认表
Step 4：技术主题分解表
Step 5：检索元素矩阵
Step 6：噪声与排除边界表
Step 7：检索前门禁状态
Step 8：检索策略与公式（仅在 Step 0-7 已通过且用户确认后输出）
```

固定步骤含义如下：

| Step | 只允许出现的内容 | 本步骤禁止出现的内容 |
|---|---|---|
| Step 0 | 原始需求、执行模式、假设条件。 | 申请人公式、主题公式、命中量。 |
| Step 1 | 申请人实体扩展表。 | `ANCS=...` 终版公式或单表达式捷径。 |
| Step 2 | 3-5 句话说明技术主题“是什么/不是什么”。 | 关键词矩阵、`TA_ALL`、检索策略、公式。 |
| Step 3 | 技术边界确认表。 | 正式检索策略、`TA_ALL`、组合公式。 |
| Step 4 | 技术主题分解表。 | 公式块或数量预测。 |
| Step 5 | 检索元素矩阵。 | 最终 `TA_ALL` 公式或组合公式。 |
| Step 6 | 噪声与排除边界表。 | 最终公式。 |
| Step 7 | 检索前门禁状态。 | 除非所有门禁为 `Pass` 或 `Pending`，否则不得执行检索或输出公式。 |
| Step 8+ | 只有 Step 0-7 通过，且默认获得用户确认后，才可以开始输出检索策略和公式。 | 不适用。 |

以下标题和结构均无效：

- `Step 2：固态电池技术主题关键词矩阵`。应改为 `Step 5：检索元素矩阵`，且必须先输出 Step 2-4。
- `Step 2：技术主题关键词扩展（固态电池）`。Step 2 只能是叙述性技术定义。
- `Step 3：IPC 分类号映射`。IPC/分类内容属于 Step 5 的分类锚点，或 Step 8 的公式支撑。
- `Step 4：正式检索式`。Step 4 只能是主题分解表；正式公式只能从 Step 8 开始。

公式前的最低通过标准如下：

| 门禁 | 输出公式前必须可见的最低内容 |
|---|---|
| 申请人实体扩展 | 候选法律实体/名称变体表，并标注 `Yes` / `No` / `Pending`。 |
| 技术主题定义 | 3-5 句话解释主题是什么、不是什么。 |
| 边界确认 | 纳入/排除/待确认表，并说明检索影响和确认状态。 |
| 主题分解 | 覆盖对象/材料、功能/效果、机制/工艺、应用、分类和噪声的维度表。 |
| 检索元素矩阵 | 中文/英文术语、字段范围、邻近/算符方案、公式角色和确认状态。 |
| 噪声边界 | 噪声来源、排除逻辑、过度排除风险和确认状态。 |
| 门禁状态 | 每个门禁均为 `Pass` 或 `Pending`；如有任何 `Fail`，停止且不得写公式。 |

无效输出示例：

```text
Step 3: Formal Search Strategy
Applicant expression: ANCS=(...)
Topic expression: TA_ALL=(...)
Combined query: ANCS=(...) AND TA_ALL=(...)
```

即使前文写了“基于以上分析”，只要没有完整可见的检索前校验包，上述输出仍然无效。

以下输出同样无效：

```text
Step 2：固态电池技术主题关键词矩阵
TA_ALL=(...)
Step 3：组合检索式（最终输出）
ANCS=(...) AND TA_ALL=(...)
```

原因是 Step 2 必须是主题定义，Step 3 必须是边界确认，公式不得早于 Step 8。

以下输出也无效：

```text
Step 2：技术主题关键词扩展（固态电池）
Step 3：IPC 分类号映射
Step 4：正式检索式（推荐两版）
```

原因是 Step 2 不是关键词扩展，Step 3 不是 IPC 映射，Step 4 不是公式。

### 1. 原始需求保留门禁

- 在解释申请人范围或技术范围之前，必须逐字保留用户原始需求。
- 用户已确认事实、Agent 推断、待确认假设必须显式分开。

### 2. 申请人字段确认门禁

- 如果用户尚未在本次执行中明确确认申请人检索字段，不得执行检索、数量校验、申请人公式定稿、合并、去重或报告完成。
- 在询问字段选择前，可以先澄清原始需求、消歧申请人身份，并在必要时草拟主题边界，以便提出合理的字段/范围问题。
- `ANCS` 只是推荐项，不能作为静默默认值。
- 字段确认前，不得进行有证据支撑的申请人扩展、数量校验、检索、合并、去重、最终主题组合或最终报告撰写。
- 可选字段包括：`ALL_AN`、`AN`、`ANC`、`ANS`、`ANS_EXACT`、`ANCS`、`ANCS_EXACT`。
- 每个 PatSnap/智慧芽表达式中，字段和值之间必须使用 `:`，例如 `ANCS:("示例公司")`，不得使用 `=`。

当字段尚未确认时，第一轮回答必须使用以下内容：

```text
请先确认本次按哪个"申请/专利权人"字段检索。推荐选择 ANCS（标准化当前申请/专利权人），但需要你明确确认后我才能开始检索。

可选字段：
- ALL_AN：全字段申请/专利权人
- AN：原始申请/专利权人
- ANC：当前申请/专利权人
- ANS：标准化原始申请/专利权人
- ANS_EXACT：精确标准化原始申请/专利权人
- ANCS：标准化当前申请/专利权人（推荐）
- ANCS_EXACT：精确标准化当前申请/专利权人

请回复要使用的字段，例如：ANCS 或 ANC。
```

### 3. 申请人歧义门禁

- 如果用户给的是品牌名、缩写、集团名或经历过更名的主体，而非完整法律实体，检索前必须先消歧。
- 列出候选法律实体、所属行业、历史关系和可能的申请人检索路径。
- 当存在多个合理法律实体时，不得静默选择其中一个。

### 4. 申请人实体扩展门禁

- 在任何规模预测、申请人全量数量、主题预检索或申请人-主题组合检索之前，必须先输出申请人实体扩展表。
- 不得把品牌/集团名当作单一申请人表达式。对于大型公司集团，至少扩展：上市/核心法律主体、相关母公司或集团实体、主要研发实体、制造子公司、历史名称、英文名称和用户提供的实体。
- 每个候选实体必须包含 `relationship_basis`、`evidence_source` 或 `evidence_needed`、`confidence`、`include_in_search`（`Yes` / `No` / `Pending`）。
- 若检索前无法获得证据，将实体标为 `Pending` 并请求确认，或标为检索前假设；不得静默省略扩展表。
- 只有当所有 `Yes` 实体都出现在 `APPLICANT_TOTAL_EXPANDED` 中，且公式中的每个实体都在表中出现时，申请人公式才可定稿。

### 5. 技术边界确认门禁

- 构建可执行申请人-主题公式之前，必须先用自然语言定义技术主题，并拆解为可检索维度。
- 除非用户明确要求先给完整草稿，否则必须请用户确认主题边界。
- 如果在未确认时起草，每个边界、分解分支、检索元素和噪声元素都要标为 `待用户确认`。
- 在输出主题定义、边界表、分解表和第一版检索元素矩阵之前，不得执行主题预检索、数量预测或申请人-主题组合检索。

### 6. 禁止以规模/预检索绕过门禁

- 规模预测不能替代申请人扩展或主题分解。
- 在申请人扩展表和主题边界/分解产物完成前，不得并行运行申请人全量数量、主题初步数量或组合数量。
- 如果检索连接器失败，不得切换到跳过门禁的浅层路径；应降级为 `formula_only_mode`，或在当前门禁暂停并说明缺失输入。

### 7. 报告顺序与模板门禁

- 第一段实质性报告内容不得是 `检索策略`、`Search Strategy`、`申请人表达式`、`技术主题关键词` 或组合公式。
- 第一段实质性报告内容必须是 `Step 0：原始需求与执行模式`。
- 每个交付物都必须先输出 **Pre-Retrieval Validation Package（检索前校验包）**，包含以下组件：
  1. `Original Request and Execution Mode`
  2. `Applicant Entity Expansion Table`
  3. `Technology Topic Definition`
  4. `Topic Boundary Confirmation Table`
  5. `Topic Decomposition Table`
  6. `Search Element Matrix`
  7. `Noise and Exclusion Boundary Table`
  8. `Gate Status Before Search`
- 简单的“维度 + 关键词”表不能满足主题门禁；如果其前面没有主题定义、边界确认、主题分解和噪声边界，则无效。
- 如有任一组件缺失，必须停在缺失组件处，不得继续到检索策略、数量预测或公式。
- 不得把公式章节标为 `Step 3`；公式只能出现在 `Step 7: Gate Status Before Search` 通过之后。
- 不得把关键词矩阵标为 `Step 2`；关键词/检索元素矩阵只能属于 `Step 5：检索元素矩阵`。
- 不得把 IPC/分类映射标为 `Step 3`；IPC/CPC 应属于 `Step 5：检索元素矩阵` 的分类锚点。
- 不得把正式公式标为 `Step 4`；正式公式只能属于 `Step 8：检索策略与公式`。
- 除非用户明确要求包含公式的完整草稿，否则在 `Step 7：检索前门禁状态` 后停止，并请用户确认是否进入 Step 8。

### 8. 申请人-主题组合门禁

- 组合前必须分别构建和审计申请人表达式与主题公式。
- 生产公式必须采用以下结构：

```text
(APPLICANT_TOTAL) AND (TOPIC_FINAL_BALANCED)
```

- 如使用噪声排除，精准公式必须采用以下结构：

```text
(APPLICANT_TOTAL) AND (TOPIC_FINAL_BALANCED) NOT (NOISE_TOTAL)
```

- 必须提供完全展开、可执行的公式；仅写 `A_TOTAL AND S1` 这类简写不满足交付要求。

### 9. 下游数据集门禁

- 先确定执行模式：
  - `formula_only_mode`：用户只需要检索策略、可执行公式、方法论，或无法/不要求 Codex 执行检索时使用。
  - `retrieval_dataset_mode`：用户要求 Codex 检索/导出数据、生成数据集、去重结果或准备下游分析输入时使用。
- 在 `formula_only_mode` 中，完成标准是：提供展开后的可执行公式、假设、待确认事项和 PatSnap 执行清单；不强制要求数据集或 Word 报告。
- 在 `retrieval_dataset_mode` 中，只有生成代表性数据集，并在报告中写明 `downstream_dataset_type`、`downstream_dataset_file` 和 `downstream_dataset_count` 后，才能标记为完成。
- 在 `retrieval_dataset_mode` 中，原始公开/公告数量和全量命中数只是来源/审计指标，不是下游代表性数量。
- 在 `retrieval_dataset_mode` 中，如有同族字段，优先使用简单同族代表；如无同族字段，必须明确降级为申请级代表。

### 10. Word 报告门禁

- 在 `retrieval_dataset_mode` 中，除非用户明确不需要，否则同时生成可编辑源报告（如 Markdown）和 Word 报告（`.docx`）。
- 在 `formula_only_mode` 中，除非用户要求 Word，一份简洁的 Markdown 方法/公式报告即可。
- 如果数据集检索交付缺少 Word 报告，且用户没有明确要求不创建，则交付不完整。

## 核心流程

1. **澄清范围**
   - 识别目标申请人/集团、技术主题、司法辖区/数据库范围、时间范围、专利类型/法律状态过滤条件，以及是否纳入子公司、关联公司、被收购实体、分支机构或精确法律实体。
   - 如果申请人名称存在歧义，先消歧目标法律实体或集团路径，再询问申请人字段。
   - 判断用户需要 `formula_only_mode` 还是 `retrieval_dataset_mode`；如不清楚，默认使用 `formula_only_mode`，直到用户要求实际检索或数据集。
   - 在任何检索、数量校验、申请人公式定稿或数据集工作前，确认申请人字段。
   - 在改写技术主题前，先保留用户原始表述。

2. **扩展并校验申请人实体**
   - 收集规范法律名称、中文/英文名称、历史名称、别名、子公司、研发/制造实体、分支、被收购实体和合资公司（视范围而定）。
   - 主查询只纳入有证据支撑的实体；不确定实体进入人工确认列表。
   - 申请人扩展表与申请人公式必须双向一致：所有 `include_in_search = Yes` 的实体都必须出现在公式中，公式中的每个实体也必须在表中标为 `Yes`。
   - 在任何规模预测或检索工具调用前，先输出申请人实体扩展表。例如，目标是宁德时代/CATL 这类集团时，不能只用 `ANCS:("宁德时代")`，必须先列出并分类可能的法律实体和名称变体。

3. **拆解并确认技术主题**
   - 用简洁的业务/技术语言解释核心概念。
   - 按对象/材料/部件、功能/效果/解决问题、机制/工艺/方法、应用场景/终端产品、排除项/噪声和可选分类锚点进行拆解。
   - 写公式前先构建术语矩阵，包含中文、英文、缩写、拼写变体、下位概念、相邻术语、商品名、代表性材料/工艺和相关分类号。
   - 在任何主题预检索或申请人-主题组合检索前，输出主题定义、边界表、分解表和第一版检索元素矩阵。例如，对“固态电池”，先区分全固态/半固态/固态电解质/电极-电解质界面/电芯制造，以及常规锂离子电池噪声边界。
   - 使用 `references/topic-limitation-workflow.md` 中的强制检索前模板，不得用简短的“技术主题关键词”表替代。

4. **分别构建公式层**
   - 申请人侧：`A0` 种子/精确申请人表达式、`A1` 已验证实体扩展、`APPLICANT_TOTAL`。
   - 主题侧：`S0` 种子主题查询、`S1` 核心主题查询、`S2` 召回扩展、`S3` 精准约束、`S4` 最终平衡主题公式，以及可选 `N_*` 噪声公式。
   - 对复合概念，应在合适时使用 `$Wn`、`$PREn`、`$SEN` 或 `$PARA` 建模邻近关系，而不是简单平铺 `AND`/`OR`。
   - 使用 `IPC_LOW`/`CPC_LOW` 覆盖父类及其下位组以提升召回；只有当用户明确需要精确分类号时，才使用精确 `IPC`/`CPC`。

5. **组合、检索并记录来源**
   - 只有申请人侧和主题侧均可独立审计后，才能组合。
   - 针对所有纳入申请人组和主题公式检索申请人-主题结果。
   - 保留申请人表达式、主题公式版本、来源数据库、检索日期、过滤条件、数量口径和校验备注。

6. **合并、去重和选择代表件**
   - 按规范申请人组和主题公式版本合并纳入批次。
   - 字段支持时，输出来源/公开号、申请级和简单同族级数量。
   - 为下游评审选择简单同族代表，优先级为 `CN`，其次 `WO`/`US`/`EP`，再到其他司法辖区，同时考虑标题、摘要、权利要求的丰富度。

7. **交付产物**
   - `formula_only_mode`：交付可编辑的方法/公式报告，通常命名为 `<applicant>_<topic>_patent_search_strategy.md`，包含展开公式和执行清单。
   - `retrieval_dataset_mode`：交付可编辑检索报告，通常命名为 `<applicant>_<topic>_patent_retrieval_report.md`，并生成 Word 检索报告 `<applicant>_<topic>_patent_retrieval_report.docx`。
   - `retrieval_dataset_mode`：交付全量命中/来源数据集、字段可用时的申请级数据集、字段可用时的简单同族代表数据集，以及查询/审计附录。

## 报告必备内容

报告必须包含：

- 用户原始需求。
- 执行模式与检索前门禁状态。
- 申请人字段确认说明及用户确认依据。
- 申请人范围和实体扩展表。
- 技术主题定义。
- 技术边界确认表。
- 技术定义和边界确认状态。
- 技术主题分解表。
- 检索元素矩阵。
- 噪声/排除元素表。
- 申请人检索表达式审计表。
- 主题策略表和分层主题公式。
- 展开的申请人-主题最终公式：
  - `APPLICANT_TOTAL_EXPANDED`
  - `TOPIC_FINAL_BALANCED_EXPANDED`
  - `APPLICANT_TOPIC_FINAL_EXPANDED`
  - 拟使用噪声时的 `NOISE_TOTAL_EXPANDED`
  - 使用噪声排除时的 `APPLICANT_TOPIC_PRECISION_EXPANDED`
- 检索批次日志。
- 合并和去重摘要。
- 下游数据集选择说明。
- 召回/精准校验建议。除非用户提供已执行结果集、抽样标注和独立召回样本，否则不得宣称召回率或精准率结论。
- 交接门禁表。
- 数据缺口、歧义实体、零命中表达式、边界风险和人工复核备注。

报告必须清楚写明：

```text
execution_mode: formula_only_mode | retrieval_dataset_mode
retrieval_mode: applicant_topic_limited_retrieval
topic_limitation: <confirmed topic or pending-confirmation draft>
source_hit_count_usage: audit_only
downstream_dataset_type: simple_family_representative
downstream_dataset_file: <file>
downstream_dataset_count: <count>
ready_for: downstream_review_or_analysis
```

对于 `formula_only_mode`，使用：

```text
execution_mode: formula_only_mode
retrieval_mode: applicant_topic_limited_formula
topic_limitation: <confirmed topic or pending-confirmation draft>
expanded_formula_status: complete
dataset_status: not_executed
ready_for: patsnap_execution
```

如果降级为申请级代表，使用：

```text
downstream_dataset_type: application_level_representative_fallback
simple_family_status: unavailable
```

## 约束规则

- 不得静默默认使用 `ANCS`。
- 不得静默推断存在歧义的申请人实体。
- 即使用户提供的是知名公司或常见缩写，也不得跳过申请人实体扩展表。
- 报告不得以检索策略、申请人表达式、技术关键词或公式章节开头。
- 不得把“技术主题关键词”表当作完整主题预检索包。
- 在可见的 `Step 0` 至 `Step 7` 检索前校验包完成前，不得输出 `ANCS`、`TA_ALL` 或组合查询。
- 不得把章节命名为 `Step 3: 正式检索策略`；Step 3 保留给 `Topic Boundary Confirmation Table`。
- 不得把章节命名为 `Step 2：技术主题关键词矩阵`；Step 2 保留给 `技术主题定义`，关键词/检索元素矩阵属于 Step 5。
- 不得把章节命名为 `Step 2：技术主题关键词扩展`；Step 2 保留给 `技术主题定义`。
- 不得把章节命名为 `Step 3：IPC 分类号映射`；分类映射属于 Step 5。
- 不得把章节命名为 `Step 4：正式检索式`；公式属于 Step 8。
- 不得用申请人名称替代主题逻辑；申请人公式和主题公式都必须明确。
- 不得只依赖用户主题的字面同义词；起草生产公式前，必须跨多个技术维度展开。
- 在申请人实体扩展表、主题边界/分解/检索元素矩阵两个检索前产物都完成前，不得运行申请人规模预测、主题预检索或申请人-主题组合检索。
- 不得只提供简写最终公式；必须提供展开的可执行公式。
- 没有已执行检索结果和标注验证样本时，不得宣称“查全”或“查准”。
- 不得在缺少证据或用户批准时纳入有歧义的关联公司。
- 不得隐藏申请人表达式、主题公式或查询字符串。
- 当申请级或同族字段可用时，不得把全量命中列表直接作为下游代表性数据集。
- 除非用户在检索后明确要求单独筛选/标引步骤，否则不得直接路由到下游筛选 Skill。

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。

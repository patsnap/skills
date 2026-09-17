---
name: fto-search
description: FTO（Freedom to Operate，专利自由实施）全流程编排，调用 fto-search-mcp MCP 工具走完 8 步（方案润色→特征提取→关键词扩展→检索式构建→检索式迭代优化→专利筛选→权利要求对比→报告生成），其中迭代优化由 AI agent 读取归因数据并改写检索式、权利要求对比按 10 篇分批。当用户给出技术方案要做专利侵权风险分析、FTO 评估、自由实施分析、专利规避调研，或提到「FTO」「专利风险」「自由实施」「这个方案能不能用」时使用，无需用户明说 MCP 或编排；若只想跑其中单独一步，直接调对应 MCP 工具即可，不必走本 skill。
---

# FTO Orchestrator (MCP 模式)

依次调用后端 FTO Pro 的 8 个 MCP tool 完成一次完整 FTO 分析。每步把上一步的输出作为下一步的输入（服务端无会话状态，数据靠入参显式传递），返回后立即按模板展示，再继续下一步。

整个流程实测耗时较长（Step 5 迭代优化、Step 6 筛选、Step 7 CC 分析各可达数分钟），属正常现象，耐心等待即可。

---

## 🔴 阶段 0：启动门禁（必须全部通过才能调第一个 tool）

四项检查逐条走完再开始。**任何一项不通过就停在这里报出缺失项**，不要「先跑起来看看」——
FTO 流程中途缺件不会报错，只会静默产出一份看着完整、实际漏掉大半证据的报告。

### ① 必需工具齐备（缺一即停）

本流程依赖 `fto-search-mcp` 这一组 tool，逐个核对是否可用：

| 用途 | tool 名 |
|------|---------|
| Step 1 | `fto_proposal_refine` |
| Step 2 | `fto_feature_extraction` |
| Step 3 | `fto_keyword_expansion` |
| Step 4 | `fto_query_generation` |
| Step 5 | `fto_sample_set_init` · `fto_estimate_recall` · `fto_diagnose_missed` · `fto_validate_and_fix_query` · `fto_fetch_missed_patent_details` |
| Step 6 | `fto_patent_screening` |
| Step 7 | `fto_cc_analysis` |
| Step 8 | `fto_report_generation` |

**缺失时的处理（强制）**：
1. **在调用任何 tool 之前**就停止，不要开始 Step 1。
2. 明确列出缺失的 tool 名与它对应的步骤，并说明「因此本次无法产出 XX」
   （如缺 `fto_cc_analysis` → 无法产出侵权风险结论与报告）。
3. 给出配置方式（见下），询问用户是配置后重跑，还是只跑能跑通的前几步。
4. 若用户选择只跑前几步：**在开头和结尾都要写明本次是残缺运行、缺哪几步、
   结论不能当作 FTO 结论使用**。绝不把残缺运行描述成一次 FTO 分析。

MCP 配置：
```json
"fto-search-mcp": {
  "type": "http",
  "url": "https://connect.zhihuiya.com/30af1e/mcp?apikey=YOUR_MCP_KEY"
}
```
YOUR_MCP_KEY 是您在 智慧芽 开放平台申请的密钥，请替换为实际的密钥。
登录 智慧芽 开放平台(https://open.zhihuiya.com/)，在 API 密钥 页面创建新的 MCP Key。Key 格式为 sk-xxxxxxxxxxxx，请妥善保存

### ② 输入聚焦：一次只分析一个方案

FTO 的每一步（特征提取、关键词、检索式、CC 对比）都假设输入是**单一技术方案**。
两个方案混在一段文本里，特征会被合并成一份四不像，检索式覆盖两个领域的交集，结论无效。

调 Step 1 之前先判断输入：

- 文本描述了**两个及以上彼此独立**的技术方案（不同产品、不同技术路线、
  或明显是「方案一 / 方案二」「另外我们还有」这类并列结构）→ **停下询问**：
  列出你识别到的各个方案（每个一句话概括），让用户选定本次分析哪一个，
  或确认要分别跑多次。**不要自行挑一个开始，也不要合并成一个跑。**
- 单一方案但含多个技术特征、多个实施例 → 正常，直接继续（这是 FTO 的常态输入）。

### ③ 语言：`input_lang` 决定全部产出语言

自动检测 `technical_proposal` 的主要语言：中文 → `cn`，其他 → `en`。

**`input_lang=en` 时的强制要求**：本 skill 下方所有展示模板的中文标题、表头、
标签、结论文案**全部改用英文输出**，不留任何中文。模板里的中文只是 `cn` 情形的样例，
不是要照抄的字面量。具体对照见文末「附录 A：英文模板对照」。

同时 `input_lang` 必须逐步传给**每一个** tool（每个 tool 都有该入参），
它同时决定后端 LLM 的产出语言与 Word 报告用哪份模板（cn/en 两份）。
漏传某一步，那一步的产出会掉回该 tool 的默认值 `cn`，报告里就混进中文段落。

### ④ 检索数据源可达

Step 4 拿到 `query_result_count=0` 时，几乎一定是检索数据源不可达，而非检索式问题。
此时停下告知用户，不要带着 0 命中继续往下跑。

---

## 输入参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `technical_proposal` | ✅ | 技术方案描述文本（单一方案，见门禁②） |
| `input_lang` | ✅ | `cn` / `en`，见门禁③。**每一步都要传** |
| `country` | 可选 | 受理局列表，如 `["CN"]`、`["CN","US"]`，默认 `["CN"]`。代码见 [references/country-codes.md](references/country-codes.md) |
| `legal_status` | 可选 | 法律状态，默认 `["1","2"]`（有效 + 审中） |
| `image_files` | 可选 | 方案图片，base64 字符串列表（支持 `data:image/png;base64,...` 或裸 base64）。未提供传 `[]` |

### 图片输入的传递要求（原始字节保真）

`image_files` 的每一项**必须是图片原始字节的 base64 编码，原样传递**：

- 从文件读到字节 → `base64.b64encode(raw_bytes)` → 直接放进列表。
- **不要**重新编码、转格式、压缩、缩放、截断或重新排版换行后再传。
  任何一次二次编码都会让后端解出的字节与原图不一致，图文联合分析的
  可追溯性失效（说不清结论对应的是哪张图）。
- data URI 与裸 base64 后端都接受，带换行的 base64 也接受（后端会去空白）。
  URL-safe 变体（`-_`）同样接受。
- 若手上只有图片 URL，直接把 URL 放进列表即可，后端会下载——
  但**不要**自己下载再编码，那等于多一次转手。
- 图片单张上限 20MB，仅支持 PNG / JPEG / GIF / WebP。

传完后在 Step 1 展示里注明「已附图 N 张」，让用户能核对张数。

---

## 字段参考（重要）

每步工具的真实返回字段与直觉差异很大（同一含义在不同步骤甚至换名，如 Step2 的
`chinese_keyword` 单数 vs Step3 的 `chinese_keywords` 复数）。下面每步的展示模板已按
**实测字段**编写。如遇返回结构与模板不符，以 [references/tool-outputs.md](references/tool-outputs.md)
为准，并优先 `print` 一次 keys 核对，不要凭记忆猜字段名。

---

## 🔴 全流程硬约束

以下四条贯穿 8 步，每步都适用：

1. **`task_id` 全程唯一且复用**：阶段 0 通过后生成 `fto-{YYYYMMDD}-{随机8位}`，
   8 步（含 Step 7 的每一批）**全部传同一个**。后端按 `task_id` 归集 CC 结果与
   报告状态，换 ID 会让报告读到别的任务的数据，复用旧 ID 会掺进历史残留。
   **一次会话里同时跑多个方案时，每个方案必须各自生成独立 task_id，绝不共用**——
   共用会让两个方案的 CC 结果落进同一条报告链路，混成一份错误报告。
2. **参数原样传递**：上一步返回的结构（`search_elements`、`aggregated_query`、
   `patent_ids` 等）原样传给下一步，不要摘要、重排、改名或「顺手清洗」。
   字段名以 references/tool-outputs.md 为准。
3. **数字不推算**：所有计数（命中数、保留数、风险数）只用工具返回的字段。
   工具不返回的（如筛除数、候选总数）就不写，绝不估算或反推。
4. **失败即停，不续跑**：任一步抛错或返回 `isError` → 停在该步，报出错误原文与
   已完成/未完成的步骤，问用户重试还是调整。**绝不跳过失败步骤继续下一步**，
   也不用已有的部分结果汇总出结论。详见「阶段 9：异常处理」。

---

## 执行流程

### 初始化

阶段 0 四项门禁通过后：生成 `task_id`，确认 `input_lang`、`country`（默认 `["CN"]`）、
`legal_status`（默认 `["1","2"]`）、`image_files`（默认 `[]`）。

把这几个值先复述给用户一行，便于当场纠正受理局或语言：

```markdown
本次分析：task_id `{task_id}` ｜ 语言 {input_lang} ｜ 受理局 {country} ｜ 法律状态 {legal_status} ｜ 附图 {len(image_files)} 张
```

### 逐步调用与展示

每步返回后**立即**按模板展示，再继续。模板里 `{字段}` 均为实测返回字段。
`input_lang=en` 时按附录 A 换成英文模板。

---

#### Step 1：方案润色

调用：`fto_proposal_refine(task_id, technical_proposal, input_lang, image_files)`

返回 `{success, refined_proposal, original_proposal}`。后续步骤统一用 `refined_proposal`。

**润色后自检（必做）**：对照原文核对 `refined_proposal` 是否丢了要素。
润色是 LLM 改写，会压缩它认为次要的内容，而**被压掉的往往正是跨领域方案里
非主线的那一维**（见 Step 2 的跨领域检查）。若发现原文里的某类要素在
`refined_proposal` 中整体消失，在展示中明确指出，并提醒用户该维度可能在
后续检索中覆盖不足。

```markdown
## 📋 Step 1 完成：技术方案润色

{已附图 N 张（image_files 非空时显示）}

{refined_proposal}

{检测到要素丢失时追加}⚠️ 原文中的 {丢失要素} 在润色结果中未保留，后续检索对该维度的覆盖可能不足。
```

---

#### Step 2：技术特征提取

调用：`fto_feature_extraction(task_id, refined_proposal, input_lang)`

`core_innovations`/`key_implementations`/`support_technologies` 是**字符串数组**；
`search_elements[]` 含 `chinese_keyword`（单数，此步常为空）。

`element_type` / `keyword_type` 返回值是英文枚举。展示时按 `input_lang` 映射：
`cn` 显示中文名（保留英文枚举做括注），`en` 直接显示英文枚举。映射表：

- `element_type`：`TECHNICAL_DOMAIN`=技术领域 · `CORE_INNOVATION`=核心创新 ·
  `KEY_IMPLEMENTATION`=关键实现 · `SUPPORTING_TECH`=支撑技术
- `keyword_type`：`APPLICATION`=应用 · `FUNCTIONAL`=功能 · `STRUCTURAL`=结构

##### 🔴 跨领域方案的特征完整性检查（必做，不可跳过）

**问题**：方案同时涉及多个技术维度时（典型如「硬件结构 + 算法 + 材料」），
特征提取会偏向它判断为「主线」的那一两维，把其余维度的特征整体漏掉。
漏掉的维度在 Step 3 没有关键词、Step 4 没有对应子句，检索式对该维度**零覆盖**，
而流程不会报错——最终报告看着完整，实际漏掉了一整类可能侵权的专利。

**做法**：把 `refined_proposal` 按技术维度过一遍，逐维核对是否在
`core_innovations` / `key_implementations` / `support_technologies` /
`search_elements` 中有对应项。至少覆盖这几类维度：

| 维度 | 典型表述 |
|------|---------|
| 结构 / 硬件 | 部件、装置、连接关系、几何构造 |
| 算法 / 控制 / 软件 | 模型、策略、判据、数据流、控制逻辑 |
| **材料 / 组分 / 配方** | 材料名、涂层、合金、活性成分、含量配比、表面处理 |
| 工艺 / 制法 | 工序、温度压力条件、加工方式 |
| 应用场景 | 用途、被作用对象、使用环境 |

**材料维度最容易被整体丢弃**，尤其当方案主线是硬件或算法时。
只要原文提到了具体材料、组分或配方，就必须在特征里有对应项。

**发现缺失时**：不要静默继续，也不要自己捏一条特征塞进 `search_elements`
（那会污染原样传递的结构）。按以下顺序处理：

1. 在 Step 2 展示中用 ⚠️ 明确列出缺失的维度及原文对应片段。
2. 询问用户：是「补充说明该维度后重跑 Step 2」，还是「接受现状继续」。
3. 用户选择继续时，在 Step 3 展示中再次标注该维度无关键词覆盖，
   并在 Step 8 的结论里写明「本次检索未覆盖 {维度}，该维度的专利风险未评估」。

```markdown
## 📋 Step 2 完成：技术特征提取

**技术领域**：{tech_field}
{cross_field 非空时显示}**交叉领域**：{cross_field}

### 🔴 核心创新特征
{遍历 core_innovations 字符串}- {该字符串}

### 🟡 基础必要特征
{遍历 key_implementations 字符串}- {该字符串}

### 🟢 扩展特征（为空显示「（无）」）
{遍历 support_technologies 字符串}- {该字符串}

### 🔍 检索要素（{len(search_elements)} 个，质量 {quality} / 置信度 {confidence}）
| 类型 | 描述 | 关键词类型 | 相关度 |
|------|------|-----------|--------|
{遍历 search_elements}| {element_type 按 input_lang 映射} | {element_description} | {keyword_type 按 input_lang 映射} | {relevance_score} |

### ✅ 维度覆盖自检
| 维度 | 原文是否提及 | 特征中是否覆盖 |
|------|:-----------:|:-------------:|
{逐维填写，仅列原文提及的维度}| {维度} | 是 | {是 / ⚠️ 否} |

{存在 ⚠️ 时追加}⚠️ **{维度} 维度缺失**：原文「{原文片段}」未进入特征列表，
该维度将在后续检索中零覆盖。请选择：补充说明后重跑 Step 2 / 接受现状继续。
```

---

#### Step 3：关键词扩展

调用：`fto_keyword_expansion(task_id, refined_proposal, search_elements, input_lang, region)`
> `search_elements` 取 Step 2 的 `search_elements`（原样传，不增删）；`region` 取 `country[0]`（如 `"CN"`）

`search_elements[]` 此步含 `chinese_keywords`/`english_keywords`（复数）与
`chinese_synonyms`/`english_synonyms`（与核心词一一对应的二维数组）、`classifications`。

```markdown
## 📋 Step 3 完成：关键词扩展

共 {total_elements} 个要素，{total_keywords} 个核心词 + {total_synonyms} 个同义词（质量 {quality_score}）

{遍历 search_elements，序号从 1}
### {序号}. {element_type} — {element_description}
| 核心词 | 中文扩展 | 英文 / 英文扩展 | 分类号 |
|--------|---------|----------------|--------|
{对每个 chinese_keywords[i]}| {chinese_keywords[i]} | {chinese_synonyms[i] 逗号连接} | {english_keywords[i]} / {english_synonyms[i] 逗号连接} | {classifications 逗号连接，仅首行显示} |

{Step 2 自检有缺失维度时追加}⚠️ {维度} 维度无对应要素，故本步也无该维度关键词。
```

> 传给 Step 4 的是本步的 `search_elements` 字段。

---

#### Step 4：检索式构建

调用：`fto_query_generation(task_id, refined_proposal, search_elements_with_keywords, input_lang, country, legal_status)`
> `search_elements_with_keywords` = Step 3 的 `search_elements`；`country` 默认 `["CN"]`；`legal_status` 默认 `["1","2"]`

`retrieval_queries[]` 字段：`sequence`/`query`/`actual_query`/`result_count`/`is_available`/`is_combination`。
`aggregated_query` 为聚合后的完整检索式原文，组合式（`is_combination=true`）的 `query`
字段是 `(S0) AND ((S1) AND ...)` 形式的逻辑结构（用子式序号引用，便于阅读），
`actual_query` 才是该子式展开后的真实检索式。

```markdown
## 📋 Step 4 完成：检索式构建

### 检索式层级
| 序号 | 类型 | 结果数 | 状态 |
|------|------|--------|------|
{遍历 retrieval_queries}| {sequence} | {is_combination ? 组合 : 单式} | {result_count} | {is_available ? 可用 : 不可用} |

### 聚合检索式逻辑结构
{取最后一条 is_combination=true 的 query（含 (S0) AND (...) 序号引用形式），代码块展示}

### 聚合检索式（完整原文）
{aggregated_query 完整原文，代码块展示}

命中 **{query_result_count}** 条
```

**`query_result_count=0` 时停止**：按门禁④处理，检索数据源不可达，不要继续往下跑。

---

#### Step 5：检索式迭代优化（AI agent 主导循环）

> 后端只提供原子数据计算能力（无 LLM），检索式的改写与决策完全由 AI agent 完成。
> 最大轮次 **5 轮**，每个 MCP tool 调用 ≤2 分钟，不会触发网关超时。

---

##### 5.0 初始化样本集（整个 Step 5 只做一次）

调用：`fto_sample_set_init(task_id, refined_proposal, country, legal_status="1,2", input_lang)`
> 注意此处 `legal_status` 是**逗号分隔字符串**（`"1,2"`），与 Step 4 的列表形态不同。

返回 `{sample_ids, sample_size, cached}`。把 `sample_ids` 保存为变量 `S`，后续全程复用，不再重新采样。

```markdown
样本集：{sample_size} 件（{cached ? "命中缓存" : "新采样"}）
```

**🔴 `sample_size < 10` 时停止**：这不是「样本偏少」而是语义检索链路异常，
此时算出的 recall 完全不可信（分母只有个位数，一两件命中就能虚高到 80%+）。
停下告知用户实际样本数与该数字为何不可用，询问是重试 5.0 还是跳过 Step 5
直接用 Step 4 的检索式进 Step 6。**绝不带着 <10 的样本集继续跑迭代**——
后续每一轮的 recall 都是噪声，据此做的收敛判断和检索式改写全是无效动作。

---

##### 5.1 初始指标（轮次 0）

调用：`fto_estimate_recall(task_id, aggregated_query=Step4_aggregated_query, sample_ids=S, input_lang)`

返回 `{result_count, reachable, hit, recall, missed_ids, breadth, breadth_comment,
partial_failure, failed_chunks}`。初始化迭代记录表，把 Step 4 的检索式记为 `current_query`：

```markdown
| 轮次 | 改动说明 | 结果数 | 样本查全率 |
|------|---------|--------|-----------|
| 0（初始） | Step 4 原始检索式 | {result_count} | {recall}% |
```

**🔴 `partial_failure=true` 时该轮 recall 不可用**：有 `failed_chunks` 个批次查询失败，
这些批次整批被跳过，`recall` 因分母缺失而偏小且不可信。此时**不要据此判停、也不要
据此改写检索式**（会把「查询失败」误读成「检索式漏了这批」，朝错方向放宽）。
处理：在迭代记录表该行标注 `⚠️ partial_failure（{failed_chunks} 批失败）`，
重试一次 `fto_estimate_recall`；仍失败则停下告知用户检索 API 不稳定，
询问是继续等待重试还是跳过 Step 5。

---

##### 5.2 收敛判断（每轮循环开始时检查）

**满足其一即停止**：
- `recall ≥ 85%` 且 `breadth != "narrow"`（patsnap-query-gen 实测阈值，比旧版 95% 更符合伪 GT 的真实校准区间；
  `breadth=narrow` 时命中数过少，伪 GT 样本覆盖率虚高，即便 recall 达标也不能收尾，需继续放宽）
- `recall` 连续两轮不再上升
- 已达最大轮次（5 轮）

判停只看 `partial_failure=false` 的轮次；被标注 partial_failure 的轮次不参与
「连续两轮不再上升」的计数。

若收敛，跳到 5.7 收尾补召回。否则继续 5.3。

---

##### 5.3 归因分析

调用：`fto_diagnose_missed(task_id, aggregated_query=current_query, missed_ids=前一步missed_ids[:10], input_lang)`

返回 `{blocking_clauses: [{clause, blocks, is_fixed_field}], total_missed}`。

解读原则：
- `is_fixed_field=true` 的子句（AUTHORITY/SIMPLE_LEGAL_STATUS/PATENT_TYPE/ANCS）→ **绝对不动**
- `blocks` 最多且非固定字段 → 真盲区，优先优化这个方向
- missed 集中在单一子句 → 该子句同义词不够或字段选错
- missed 均匀分布在多个子句 → 多属合理排除，可考虑接受现状

---

##### 5.4 AI agent 改写检索式

**改写约束（必须遵守）**：

1. **一次只改一个变量**：只改归因指向的那个子句；字段降级（ICLMS_ALL → TAC_ALL）和加同义词不同时做
2. **不动固定字段**：`AUTHORITY`、`SIMPLE_LEGAL_STATUS`、`PATENT_TYPE`、`ANCS` 子句维持原样
3. **领域词不能孤立做 AND**：技术领域词必须有分类号兜底 `(TAC_ALL:(词) OR IPC_CPC:(小类))`，不能单独作为 AND 必要条件
4. **查全优先于查准**：命中数几百到几千均可接受；`breadth=broad` 才考虑收紧
5. **产品名/商品名/活性成分名**：放进 OR 分支，绝不作为 AND 必要条件

把改写后的完整检索式输出在代码块中。

---

##### 5.5 语法校验

调用：`fto_validate_and_fix_query(task_id, new_query=改写后检索式, original_query=Step4_aggregated_query, input_lang)`

- `fixed_field_violated=true` → 警告固定字段被误改，展示 `violated_field`，AI agent 需重新改写
- `is_valid=false` → 展示错误，要求重新改写
- 通过 → 用 `fixed_query` 作为本轮 `current_query`，其 `result_count` 即本轮结果数

---

##### 5.6 本轮评估

调用：`fto_estimate_recall(task_id, aggregated_query=current_query, sample_ids=S, input_lang)`

更新迭代记录表（同样检查 `partial_failure`），回到 5.2 判断收敛。

---

##### 5.7 收尾补召回（收敛后执行）

仅当最终 `missed_ids` 非空时执行：

1. 调用：`fto_fetch_missed_patent_details(task_id, missed_ids=最终轮missed_ids[:15], input_lang)`

   返回每件专利的 title/abstract/ipc/cpc。

2. AI agent 分析这批专利的共同技术特征，判断是否存在检索式遗漏的技术表述（某类 IPC 小类、某个惯用表达）。

3. 若发现真盲区，生成补充子句，以 OR 追加：
   ```
   ({current_query}) OR ({补充子句})
   ```

4. 调用 `fto_validate_and_fix_query` + `fto_estimate_recall` 验证效果，追加到迭代记录表。

5. 最终检索式 = 通过验证后的 `fixed_query`。

---

##### 展示模板

```markdown
## 📋 Step 5 完成：检索式迭代优化（{迭代轮数} 轮）

### 迭代过程
| 轮次 | 改动说明 | 结果数 | 样本查全率 |
|------|---------|--------|-----------|
{遍历迭代记录表，partial_failure 的轮次标注 ⚠️}

样本集：{sample_size} 件
最终：样本查全率 **{recall}%**（≥85% 且非过窄 ✅ / 否则 ⚠️ 已达最大轮次），结果数 **{result_count}**（{breadth_comment}）

### 最终检索式
{final_query 完整原文，代码块展示}
```

若最终 recall < 85% 且已达最大轮次：说明归因显示剩余未命中多属合理排除（被发明点子句过滤），
询问用户在「接受现状继续 / 调整特征重跑 Step 4」中选择，等待选择后继续。

> 注：样本查全率 85% 对应实测真查全率接近 100%（旧阈值 95% 过于激进，85% 是 patsnap-query-gen 实测多个 case 的经验收敛线）。

---

#### Step 6：专利排除筛选（后端工具 `fto_patent_screening`）

调用：`fto_patent_screening(task_id, refined_proposal, aggregated_query, query_result_count, country, input_lang)`
> `aggregated_query`/`query_result_count` 取 Step 5 输出；`country` 传与前面各步相同的受理局列表

返回值就是**一个 patent_id 字符串数组**（顺序与筛选结果一致），不是对象，
也没有计数字段、标题、匹配度、首权或排除理由。

```markdown
## 📋 Step 6 完成：专利排除筛选

- **保留：{len(patent_ids)}** 条（进入 CC 分析）
```

> 候选总数与筛除数当前工具版本不返回，别写也别推算。排除理由同样不返回，勿编造。
> 该列表原样传给 Step 7，按 10 篇一批分批调用。

**🔴 列表为空时就地结束**：不要调用 Step 7 和 Step 8，
展示「没有保留专利，无需 CC 分析，未生成报告」后收尾。
硬跑报告工具会回退按 `task_id` 查库，要么报 `未找到权利要求对比分析结果`，
要么在 `task_id` 被复用时拿历史残留数据渲染出一份不属于本次的报告。

**空列表不等于「无侵权风险」**：它同样可能是筛选阈值过严或检索式跑偏。
收尾文案必须写成「本次未产出可进入 CC 分析的专利，因此未评估侵权风险」，
**绝不写成「未发现侵权风险」或「可以自由实施」**——后者是一个未做过的结论。
同时给出下一步建议（放宽 Step 5 检索式 / 调整特征重跑），让用户能判断要不要重跑。

---

#### Step 7：权利要求对比分析（CC 分析）（后端工具 `fto_cc_analysis`）

调用：`fto_cc_analysis(task_id, refined_proposal, patent_ids, input_lang)`

**🔴 单次最多 10 篇，必须分批调用**（超过 10 篇工具直接报错）：

1. 取 Step 6 返回的 `patent_ids`，按顺序切成每批 ≤10 篇。
2. 逐批调用 `fto_cc_analysis`，**每批都传同一个 `task_id`**（各批结果落到同一条报告链路）。
3. 批与批之间串行调用，不要并发。
4. 把所有批次返回的 `claim_analysis_results[]` 拼接成一个完整列表**仅用于本步展示**，
   `analysis_stats` 的六个计数（`total_patents`/`successful_analyses`/`failed_analyses`/
   `high_risk_patents`/`medium_risk_patents`/`low_risk_patents`）逐批求和，缺失键按 0 处理。
   **不要把这个拼接列表传给 Step 8** —— 它只有高风险明细，见 Step 8 说明。

##### 🔴 批次失败与业务失败的处理（两类都要停）

**第一类：工具抛错 / 返回 isError（传输或调用层失败）**
报出失败的批次序号与该批的专利 ID，停在这一步，等用户决定重试还是继续。

**第二类：工具成功返回，但业务层没分析成功（更隐蔽，必须主动查）**
每批返回后核对 `analysis_stats`：

- `failed_analyses > 0` → 该批有专利分析失败
- `successful_analyses + failed_analyses < total_patents` → 有专利既没成功也没记失败
- `successful_analyses == 0` 且 `total_patents > 0` → 该批**整批业务失败**

**出现任一条就停止，不要继续调用后续批次，也不要进 Step 8。**
工具返回 `success=True` 只代表调用通了，不代表专利被分析了；
把这种批次当成功累加进去，报告会少掉这些专利却读起来像完整结论。

处理：展示每批的 `total_patents / successful_analyses / failed_analyses` 三个数，
指出哪批哪几件没分析成功，询问用户是重试该批还是接受缺口。
若用户选择接受缺口继续，**必须在 Step 7 和 Step 8 的展示里都写明
「{N} 件专利未完成分析，本报告不覆盖这些专利」**。

**绝不把未完成的批次描述为分析完成**，也不要拿已成功的批次直接汇总出结论 ——
未分析的专利静默缺席，读起来却像一份完整的 FTO 结论，这是本流程代价最高的错误。

> 工具只返回该批中高风险（`infringement_risk_level=HIGH`）的专利，
> 因此某批返回空 `claim_analysis_results` 是正常的（这批没有高风险专利），不是失败；
> 判失败看工具是否抛错、以及 `analysis_stats` 的三个计数，不看返回列表是否为空。

返回 `analysis_stats`（风险计数直接用它）+ `claim_analysis_results[]`。
风险等级在 `risk_assessment.infringement_risk_level`（HIGH/MEDIUM/LOW），无顶层 risk_level。
`patent_resource` 是字符串（取不到 pn/title）；专利标识用 `patent_id`。
`feature_comparisons[]` = `{claim_num, claim_feature, comparison_feature, is_public, type, reason}`
（无 `is_text_similar`；`is_public` 为字符串 `"0"/"0.5"/"0.9"/"1"`，`type` 为等同类型枚举
`LITERAL_SAME`/`HYPERNYM`/`FUNCTIONAL`/`IMPLIED`/`FWR`/`QUESTIONABLE_RISK`/`DIFFERENT`）。

```markdown
## 📋 Step 7 完成：权利要求对比分析（{批次数} 批，每批 ≤10 篇）

共 **{累加 total_patents}** 件 ｜ ✅ 成功 **{累加 successful_analyses}** ｜ ❌ 失败 **{累加 failed_analyses}**
🔴 高风险 **{累加 high_risk_patents}** ｜ 🟡 中 **{累加 medium_risk_patents}** ｜ 🟢 低 **{累加 low_risk_patents}**

{failed_analyses > 0 时追加}⚠️ {N} 件专利未完成分析，本次结论不覆盖这些专利。

### 🔴 高风险专利（infringement_risk_level=HIGH）
| 专利 ID | 风险说明 | 结论摘要 |
|---------|---------|---------|
{遍历 HIGH 的 claim_analysis_results}| {patent_id} | {risk_assessment.risk_description} | {conclusion 前 60 字} |

{可选：对其中一件展开 feature_comparisons 逐特征对比表}
| 权项 | 专利特征 | 方案对应特征 | is_public | 等同类型 | 说明 |
|------|---------|------------|:---------:|:--------:|------|
{遍历 feature_comparisons}| {claim_num} | {claim_feature} | {comparison_feature} | {is_public} | {type} | {reason} |
```

---

#### Step 8：FTO 报告生成（后端工具 `fto_report_generation`）

调用：
```
fto_report_generation(
  task_id, refined_proposal, input_lang,
  feature_extraction, expanded_keywords, retrieval_queries,
  country, legal_status
)
```

**🔴 分批后必须省略 `claim_analysis_results`**，只复用同一 `task_id`：
Step 7 每批只返回高风险明细，但 CC Agent 已按 `task_id + patent_id` 把该批**全量**结果写库
（含 MEDIUM/LOW，且不删其他批次）。省略该入参时报告工具按 `task_id` 读取累计的完整结果，
报告才不会被截断成高风险明细，也才能在没有高风险专利时正常出报告。
传入拼接后的高风险列表会让 `project_info.patent_count` 和 Claim Chart 只剩那几件。

**🔴 `country` / `legal_status` 必须传**，且与前面各步用的是同一份值。
Word 报告的「检索范围」章节由这两个入参渲染（受理局名称 + 法律状态名称 + 检索日期）；
漏传该章节整段空白，报告读者无法核验本次检索的口径。

> `feature_extraction`/`expanded_keywords`/`retrieval_queries` 分别传 Step 2/3/4 的返回，
> 用于渲染 Word 的检索过程章节，可省略但省略的章节会显示为待补充。
> `retrieval_queries` 若 Step 5 有迭代，传 Step 5 最终检索式对应的那份。

返回 `overall_summary`（风险计数）、`analysis_stats`、`project_info`、`report_name`，
以及 **`report_id` / `file_name` / `sign_url` / `s3_key`** —— `sign_url` 就是 Word 报告的下载链接。
风险总结优先用 `analysis_stats`（最稳，`report_name` 可能为空）。

##### 🔴 报告产出必须可核验（不可跳过）

报告是本流程的最终交付物，**只报风险数字而不给出报告本体，用户无法核验任何一项**。
展示时必须做到：

1. **给出 `sign_url` 下载链接和 `file_name`**。这是 Word 报告附件，
   缺了它用户拿不到可核验的产物。`sign_url` 为空或缺失时明确写「报告文件未生成成功」，
   不要只展示统计数字就宣布完成。
2. **列出可核验的四项口径**，每项都用工具返回的字段，取不到就写「工具未返回」：
   - 封面专利数：`project_info.patent_count`
   - 分析专利数：`analysis_stats.total_patents`
   - 检索范围：本次的 `country` + `legal_status`（即传入的筛选条件）
   - 风险数量：`analysis_stats` 的 high/medium/low 三个计数
3. **检索次数**：工具不返回该字段。若要给，只能用 Step 4 的 `len(retrieval_queries)`
   与 Step 5 的迭代轮数，并注明这是编排侧计数、不是报告内字段；拿不到就写「工具未返回」。
   **绝不估算或反推。**

```markdown
## 📋 Step 8 完成：FTO 分析报告

### 📎 报告文件
- 文件名：{file_name}
- 下载链接：{sign_url}
- report_id：{report_id}

{sign_url 缺失时}⚠️ 报告文件未生成成功（`sign_url` 为空），以下统计数字无对应可核验附件。

### 可核验口径
| 项 | 值 | 来源 |
|----|----|------|
| 封面专利数 | {project_info.patent_count} | project_info |
| 分析专利数 | {analysis_stats.total_patents} | analysis_stats |
| 检索范围 | 受理局 {country}，法律状态 {legal_status} | 本次入参 |
| 检索式条数 | {len(retrieval_queries)}（编排侧计数） | Step 4 |
| 迭代轮数 | {Step 5 轮数}（编排侧计数） | Step 5 |
| 风险数量 | 🔴 {high_risk_patents} ／ 🟡 {medium_risk_patents} ／ 🟢 {low_risk_patents} | analysis_stats |

{Step 7 有未完成专利时}⚠️ {N} 件专利未完成 CC 分析，本报告不覆盖这些专利。
{Step 2 有缺失维度时}⚠️ 本次检索未覆盖 {维度} 维度，该维度的专利风险未评估。

### 核心结论
{基于高风险专利数与 overall_recommendations 给出 3-5 句结论}

### 关键规避建议
{overall_summary.overall_recommendations 要点}
```

---

## 阶段 9：异常处理

### 单步失败

工具抛错 / 返回 `isError` → **停在该步**，展示：
1. 错误信息原文（不要转述、不要美化）
2. 已完成的步骤与未完成的步骤
3. 按错误类型对照阶段 0 的门禁定位可能原因
4. 询问用户重试还是调整输入

**绝不跳过失败步骤继续下一步**，也不用已有的部分结果汇总出 FTO 结论。

### 业务失败（工具成功返回但结果不可用）

这类最容易被漏掉：调用通了、`success=True`，但业务上什么都没产出。
以下每种都必须停下，不能当成功继续：

| 场景 | 判据 | 处理 |
|------|------|------|
| 样本集过小 | Step 5.0 `sample_size < 10` | 停，recall 全程不可信，见 5.0 |
| 查全率批次失败 | Step 5 `partial_failure=true` | 该轮 recall 不可用，重试；见 5.1 |
| 检索零命中 | Step 4 `query_result_count=0` | 停，数据源不可达，见门禁④ |
| 初筛空列表 | Step 6 返回 `[]` | 就地结束，不得写成「无侵权风险」 |
| CC 整批失败 | Step 7 `successful_analyses=0` 且 `total_patents>0` | 停，见 Step 7 |
| CC 部分失败 | Step 7 `failed_analyses>0` | 停并询问，缺口须写进 Step 7/8 展示 |
| 报告无附件 | Step 8 `sign_url` 为空 | 明确写「报告文件未生成成功」 |

### 耗时

单步耗时长属正常（见开头说明），不要误判为卡死。
Step 5 迭代优化、Step 6 筛选、Step 7 CC 分析各可达数分钟。

---

## 附录 A：英文模板对照（`input_lang=en` 时使用）

`input_lang=en` 时，上文所有展示模板的中文一律替换为下列英文，**不留任何中文**。
这不是可选的润色，而是门禁③的硬要求：报告与展示文案混入中文即视为未本地化。

### 步骤标题

| cn | en |
|----|----|
| 📋 Step 1 完成：技术方案润色 | 📋 Step 1 Done: Proposal Refinement |
| 📋 Step 2 完成：技术特征提取 | 📋 Step 2 Done: Feature Extraction |
| 📋 Step 3 完成：关键词扩展 | 📋 Step 3 Done: Keyword Expansion |
| 📋 Step 4 完成：检索式构建 | 📋 Step 4 Done: Query Construction |
| 📋 Step 5 完成：检索式迭代优化（{n} 轮） | 📋 Step 5 Done: Query Iteration ({n} rounds) |
| 📋 Step 6 完成：专利排除筛选 | 📋 Step 6 Done: Patent Screening |
| 📋 Step 7 完成：权利要求对比分析 | 📋 Step 7 Done: Claim Chart Analysis |
| 📋 Step 8 完成：FTO 分析报告 | 📋 Step 8 Done: FTO Report |

### 表头与标签

| cn | en |
|----|----|
| 技术领域 / 交叉领域 | Technical Field / Cross Field |
| 核心创新特征 / 基础必要特征 / 扩展特征 | Core Innovations / Key Implementations / Supporting Technologies |
| 检索要素 | Search Elements |
| 类型 / 描述 / 关键词类型 / 相关度 | Type / Description / Keyword Type / Relevance |
| 维度 / 原文是否提及 / 特征中是否覆盖 | Dimension / Mentioned in Input / Covered in Features |
| 核心词 / 中文扩展 / 英文 / 英文扩展 / 分类号 | Core Term / CN Synonyms / EN Term / EN Synonyms / Classifications |
| 序号 / 组合 / 单式 / 结果数 / 状态 / 可用 / 不可用 | Seq / Combined / Single / Count / Status / Available / Unavailable |
| 聚合检索式逻辑结构 / 聚合检索式（完整原文） | Aggregated Query Structure / Aggregated Query (full) |
| 命中 {n} 条 | {n} results |
| 样本集：{n} 件（命中缓存 / 新采样） | Sample set: {n} (cached / newly sampled) |
| 轮次 / 改动说明 / 样本查全率 | Round / Change / Sample Recall |
| 迭代过程 / 最终检索式 | Iteration Log / Final Query |
| 保留 {n} 条（进入 CC 分析） | {n} retained (proceeding to Claim Chart) |
| 共 {n} 件 / 成功 / 失败 | {n} total / Succeeded / Failed |
| 高风险 / 中 / 低 | High Risk / Medium / Low |
| 高风险专利 | High-Risk Patents |
| 专利 ID / 风险说明 / 结论摘要 | Patent ID / Risk Description / Conclusion |
| 权项 / 专利特征 / 方案对应特征 / 等同类型 / 说明 | Claim / Patent Feature / Proposal Feature / Equivalence Type / Reason |
| 📎 报告文件 / 文件名 / 下载链接 | 📎 Report File / File Name / Download Link |
| 可核验口径 / 项 / 值 / 来源 | Verifiable Figures / Item / Value / Source |
| 封面专利数 / 分析专利数 / 检索范围 / 检索式条数 / 迭代轮数 / 风险数量 | Cover Patent Count / Analyzed Patents / Search Scope / Query Count / Iteration Rounds / Risk Counts |
| 受理局 {c}，法律状态 {s} | Authorities {c}, Legal Status {s} |
| 编排侧计数 | orchestration-side count |
| 核心结论 / 关键规避建议 | Key Conclusions / Design-Around Recommendations |

### 提示与警告文案

| cn | en |
|----|----|
| 已附图 N 张 | N image(s) attached |
| 原文中的 {X} 在润色结果中未保留…… | {X} from the original input was not retained in the refined proposal; coverage of this dimension may be insufficient. |
| {维度} 维度缺失…… | Dimension {X} is missing: it will have zero coverage in the search. Choose: re-run Step 2 with clarification / proceed as is. |
| {维度} 维度无对应要素，故本步也无该维度关键词。 | No search element for dimension {X}, hence no keywords for it in this step. |
| 没有保留专利，无需 CC 分析，未生成报告 | No patents retained; Claim Chart analysis not applicable and no report generated. |
| 本次未产出可进入 CC 分析的专利，因此未评估侵权风险 | No patents qualified for Claim Chart analysis, therefore infringement risk was not assessed. |
| {N} 件专利未完成分析，本次结论不覆盖这些专利。 | {N} patent(s) were not analyzed; this conclusion does not cover them. |
| 报告文件未生成成功（`sign_url` 为空） | Report file was not generated successfully (`sign_url` is empty). |
| 本次检索未覆盖 {维度} 维度，该维度的专利风险未评估。 | This search did not cover dimension {X}; patent risk for it was not assessed. |
| 工具未返回 | not returned by the tool |
| partial_failure（{n} 批失败） | partial_failure ({n} chunk(s) failed) |

### 元素枚举

`input_lang=en` 时 `element_type` / `keyword_type` **直接显示英文枚举原文**
（`TECHNICAL_DOMAIN` / `CORE_INNOVATION` / `KEY_IMPLEMENTATION` / `SUPPORTING_TECH`，
`APPLICATION` / `FUNCTIONAL` / `STRUCTURAL`），不做中文映射。

---

## 当前实现状态

8 步（Step 1-8）均已实现并实测跑通。Step 6 的细分类（不可排除/待定）与 Step 7 的
逐特征覆盖率等字段为后端规划中能力，当前工具版本未返回，模板不依赖它们。

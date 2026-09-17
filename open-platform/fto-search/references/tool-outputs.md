# FTO MCP 工具真实返回字段参考

> 本文档按 `app/fto_mcp/tools/` 的实际工具签名与返回校准，步骤编号与 SKILL.md 的
> 8 步流程一一对应。重写展示模板时以此为准——不要凭设想猜字段名，工具实际返回与直觉差异很大。
>
> ⚠️ 后端 `app/fto_mcp/tools/` 下的文件名仍是旧的 9 步编号（`step7_patent_screening.py`
> 对应本文的 Step 6，依此类推）。**工具名（`fto_*`）才是契约**，文件名不是。

## 通用约定

- 所有工具走 `/mcp/`（FastMCP，stateless HTTP），结果在 `result.structuredContent`（或 `result`）里。
- **stateless**：步骤间无服务端会话，数据靠入参显式传递（上一步输出 → 下一步入参）。
- **身份 header**：`X-User-Id` 是下游 LLM 网关与检索的计费/鉴权依据。缺失或为空串时
  `ResolveUserIdMiddleware` 会落到默认身份 `fto-mcp`（不再 403），因此调用能跑通，
  但计费与日志归属会记在这个匿名身份上。要正确归属就显式带上该 header。

---

## Step 1 `fto_proposal_refine`

返回字段：`success`、`refined_proposal`、`original_proposal`

⚠️ 没有 `technical_summary`、`innovation_points`。展示只用 `refined_proposal`。

---

## Step 2 `fto_feature_extraction`

顶层：`tech_field`、`cross_field`、`core_innovations`、`key_implementations`、
`support_technologies`、`search_elements`、`success`、`quality`、`confidence`、
`total_element_count`、`expected_element_count`

⚠️ 关键差异：
- `core_innovations` / `key_implementations` / `support_technologies` 是**纯字符串数组**，
  没有 `id`/`description` 子字段。直接当字符串列表遍历。
- `search_elements[]` 字段：`element_type`、`element_description`、`keyword_type`、
  `chinese_keyword`、`english_keyword`、`relevance_score`
  （注意是 `chinese_keyword` **单数**，此步关键词数组一般为空，真正扩展在 Step 3）
- `cross_field` 可能是空字符串 `""`，不是 null。

## Step 3 `fto_keyword_expansion`

顶层：`search_elements`、`expanded_keywords`、`expanded_keywords_data`、
`total_elements`、`total_keywords`、`total_synonyms`、`quality_score`、`success`

⚠️ 关键差异（与 Step 2 不同名！）：
- `search_elements[]` 字段：`element_type`、`element_description`、`keyword_type`、
  `chinese_keywords`、`english_keywords`、`chinese_synonyms`、`english_synonyms`、
  `classifications`、`relevance_score`
  （这里是 `chinese_keywords` **复数**；`*_synonyms` 是「与每个核心词一一对应的二维数组」）
- 没有 `atomic_items`/`core_atom`/`root`/`expansion_cn` 这些字段。
- `classifications` 是字符串数组，如 `["B62K15/00","B62K15/008"]`。
- **传给 Step 4 的是 `search_elements` 字段**（不是 expanded_keywords）。

## Step 4 `fto_query_generation`

顶层：`retrieval_queries`、`aggregated_query`、`query_result_count`、`query_sequence_counter`

⚠️ `retrieval_queries[]` 字段：`sequence`（如 "S0"）、`query`、`actual_query`、
`result_count`、`is_available`、`is_combination`
（没有 `id`/`purpose`/`type`/`status`）

- `query` 在组合式（`is_combination=true`）里是 `(S0) AND ((S1) AND ...)` 的序号引用形式；
  `actual_query` 才是展开后的真实检索式。展示逻辑结构用 `query`，要看真实式子用 `actual_query`。

- `query_result_count`：聚合检索式命中数。**若全为 0**，几乎一定是检索数据源不可达
  （见 SKILL.md 前置检查 ②），不是检索式本身问题。

## Step 5 迭代优化的五个原子工具

Step 5 由 AI agent 主导循环，后端只提供原子计算（**均无 LLM 调用**）。
工具名与 SKILL.md 的 Step 5 小节一一对应：

### `fto_sample_set_init`（5.0，整个 Step 5 只调一次）

入参：`(technical_proposal, task_id, country, legal_status, apd_start, apd_end, sample_limit, input_lang)`
- ⚠️ `legal_status` 是**逗号分隔字符串**（默认 `"1,2"`），不是列表 ——
  与 `fto_query_generation` 的 `list[str]` 形态不同，别混用。
- `sample_limit` 默认 200。

返回：`sample_ids`（专利 UUID 列表）、`sample_size`、`cached`
- ⚠️ 缓存键由技术方案 + 筛选条件计算，**不含 task_id**：同方案同条件的多次调用
  命中同一份样本（TTL 2h），这是预期行为。
- `sample_size < 10` 说明语义检索异常，此时 recall 不可信，应停止迭代。

### `fto_estimate_recall`（5.1 / 5.6，每轮调用）

入参：`(aggregated_query, sample_ids, task_id, chunk_size, input_lang)`
- `chunk_size` 默认 100。每个 ID 占一个 OR 子句且叠加检索式自身子句数，
  Solr 顶格 1024，调大有超限风险。

返回：`result_count`、`reachable`、`hit`、`recall`、`missed_ids`、
`breadth`、`breadth_comment`、`partial_failure`、`failed_chunks`
- `recall` = `hit / reachable * 100`（百分数，两位小数）；`reachable=0` 时返回 `0.0`。
- `missed_ids` 上限 30 个。
- `breadth` ∈ `zero` / `narrow` / `ok` / `broad`。
- ⚠️ **`partial_failure=true` 时 recall 不可信**：有 `failed_chunks` 个批次查询失败，
  整批被跳过（不按 0 计入），分母缺失导致 recall 偏小。**不要据此判停或改写检索式。**

### `fto_diagnose_missed`（5.3）

返回：`blocking_clauses[]` = `{clause, blocks, is_fixed_field}`、`total_missed`
- `is_fixed_field=true` 的子句（AUTHORITY / SIMPLE_LEGAL_STATUS / PATENT_TYPE / ANCS）不可改动。

### `fto_validate_and_fix_query`（5.5）

入参：`(new_query, original_query, task_id, input_lang)`
返回：`is_valid`、`fixed_query`、`result_count`、`fixed_field_violated`、`violated_field`

### `fto_fetch_missed_patent_details`（5.7）

入参：`(missed_ids, task_id, input_lang)`；返回每件专利的 title / abstract / ipc / cpc。

---

## `fto_iterative_optimization`（旧的一体式迭代工具，本 skill 不用）

后端仍注册着这个工具，但它是 Step 5 拆分为五个原子工具**之前**的一体式实现。
本 skill 的 Step 5 走上面五个原子工具，**不要调用它** —— 两条路径的收敛口径与
轮次控制不同，混用会让迭代记录表与实际执行不一致。

其返回形状（仅备查）：`aggregated_query`、`retrieval_queries`、`query_result_count`、
`iteration_count`、`metrics`（`{recall, result_count}`）、`relevant_patents`、
`iterative_process[]`（`{iteration, response, recall, result_count, handoff_agents}`）。
退出原因不在返回里，只在服务日志。

---

## Step 6 `fto_patent_screening`

返回值不是 dict，而是**一个 `list[str]`**：筛选后保留的 patent_id，顺序与筛选结果一致。
示例 `["CN101", "CN205", "CN309"]`。

⚠️ 走 MCP 协议时 fastmcp 会把非 dict 返回包一层：`structuredContent` 是
`{"result": ["CN101", ...]}`（output_schema 带 `x-fastmcp-wrap-result: true`），
`content[0].text` 则是裸 JSON 数组。脚本取值要兼容这两种形态。

⚠️ 关键差异（模板严重过度承诺）：
- 没有 `total_count`/`retained_count`/`excluded_count` —— 保留数只能取列表长度，
  候选总数与筛除数拿不到，不要推算。
- 没有 `screened_patents` 对象数组，也就没有 `is_screened`/`screened_reason`/
  `cannot_exclude`/`pending_review`/`relevance_score`/`claim1_summary`/标题。
- 不再返回 `screening_stats`（此前实测恒为空 `{}`）。
- 排除理由仍在服务端落库（`save_screen_patent_info` 写 DB 与 Redis），只是不经工具返回。
- 列表原样传入 Step 7（需按 10 篇一批切分）；空列表表示无保留专利，应终止流程。
- 入参 `query_result_count` 取 Step 5 最终检索式的 `result_count`。

## Step 7 `fto_cc_analysis`

顶层：`success`、`claim_analysis_results`、`overall_summary`、`project_info`、`analysis_stats`

- ⚠️ 入参为 `(technical_proposal, patent_ids, task_id, input_lang, mode, top_k)`。
  `patent_ids` 是**必传字符串列表**（不是 `screened_patents` 对象数组），
  Schema 带 `maxItems: 10`，超出被 Schema 拒绝或抛 `ValueError`。
  `mode`/`top_k` 兼容保留，但单批 ≤10 篇时其上限（lite 20 / pro 150）不会生效。
- ⚠️ 由调用方分批调用，每批复用同一 `task_id`；CC Agent 按 `task_id + patent_id`
  upsert 该批**全量**结果（含 MEDIUM/LOW），不删其他批次记录。
- ⚠️ `claim_analysis_results` **只含该批的高风险专利**（HIGH），
  返回空列表说明这批没有高风险专利，不是失败。`analysis_stats` 仍为该批全量计数。
- ⚠️ 因此 Step 8 必须**省略** `claim_analysis_results` 走查库路径；
  传入拼接后的 HIGH 列表会把报告截断成那几件。
- 空 `patent_ids` 直接返回 `success=True` + 全 0 的 `analysis_stats`（六个计数键齐全），
  不构造 Agent。
- `analysis_stats` = `{total_patents, successful_analyses, failed_analyses,
  high_risk_patents, medium_risk_patents, low_risk_patents}` —— **风险计数直接用这个**。
- `claim_analysis_results[]` 字段：`success`、`analysis_success`、`patent_id`、
  `feature_comparisons`、`risk_assessment`、`conclusion`、`claim_risks`、
  `include_in_report`、`patent_resource`
- ⚠️ 风险等级在 `risk_assessment.infringement_risk_level`（HIGH/MEDIUM/LOW），
  **没有顶层 `risk_level` 字段**。
- ⚠️ `patent_resource` 实测是**字符串**（不是 dict），取不到 pn/title/grant_date。
- `feature_comparisons[]` = `{claim_num, claim_feature, comparison_feature,
  is_public, type, reason}`（不是 claim_features，也没有 coverage_ratio，**没有 is_text_similar**）。
  - `is_public` 是字符串化的等同判定值 `"0"`/`"0.5"`/`"0.9"`/`"1"`。
  - `type` 是等同类型枚举：`LITERAL_SAME`/`HYPERNYM`/`FUNCTIONAL`/`IMPLIED`（对应 is_public=1）、
    `FWR`（0.9）、`QUESTIONABLE_RISK`（0.5）、`DIFFERENT`（0）。
- `conclusion` 是整段结论字符串；`claim_risks` 是 dict。

## Step 8 `fto_report_generation`

顶层：`success`、`report_name`、`claim_analysis_results`、`overall_summary`、
`project_info`、`analysis_stats`，以及 **`report_id`、`file_name`、`sign_url`、`s3_key`**

- ⚠️ `sign_url` 是 Word 报告的下载链接 —— 报告的实际交付物。只报统计数字而不给出
  这个链接，用户拿不到可核验的产物。为空说明 Word 生成或上传失败。
- ⚠️ `country` / `legal_status` 落库成 `user_input_filter`，Word 的「检索范围」章节
  （受理局 + 法律状态 + 检索日期）由它渲染；漏传该章节整段空白。

- `overall_summary` = `{total_patents_analyzed, high_risk_patents_count,
  medium_risk_patents_count, low_risk_patents_count, average_similarity_score,
  highest_risk_patent_id, highest_risk_score, overall_recommendations, analysis_timestamp}`
- `project_info` = `{task_id, technical_proposal, patent_count, generated_by, status}`
- ⚠️ 入参为 `(task_id, technical_proposal, input_lang, feature_extraction,
  expanded_keywords, retrieval_queries, country, legal_status, apd_start, apd_end)`，
  **不传 `claim_analysis_results`**。
  分析结果由 Step 7（`fto_cc_analysis`）落库，本工具按 `task_id` 查库获取 `patent_ids`
  与 `claim_analysis_results`；查不到会直接报错，故必须先成功执行 Step 7。
- ⚠️ `report_name` 实测可能为空字符串。风险总结优先用 `analysis_stats`（最稳）。

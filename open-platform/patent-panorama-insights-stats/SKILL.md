---
name: patent-panorama-insights-stats
description: 用于专利全景项目的环节2。它消费 patent-panorama-insights-search（环节1）产出的已验证 `search_config.json`、`candidate_pool.csv` 和 `core_recall.csv`，生成全景统计（趋势、申请人格局、技术构成、竞品画像）、按分支组织的核心专利索引（默认采信环节1召回排序，仅在必要时做有边界的兜底核查）和价值信号交叉挖掘文件。所有统计直接从检索式聚合，不需要逐件专利标引。
---

# patent-panorama-insights-stats — 全景统计与价值信号层（环节2）

> **我是环节 2/4 · 格局统计（patent-panorama-insights-stats）。** 我吃环节 1 的 `search_config.json` + `candidate_pool.csv` + `core_recall.csv`，产出 `panorama_stats.json` + `value_signals.json` + `patent_index.core.json/.csv` + `chart_data.json` + `panorama_stats_report.html`（数据快照报告），交给环节 3（patent-panorama-insights-tag）和环节 4（patent-panorama-insights-report）。

## 目标

专利全景流水线的环节2。本层是**基于检索式聚合**的层。由于 `/59100a` 和 `/3fd502` 统计工具可以直接从检索式聚合，环节2不需要逐件专利标引；只要环节1交付已验证检索式和候选池，就能运行。

它回答：

- 该领域规模多大、分布在哪、趋势如何？
- 主要玩家是谁、规模如何、趋势如何？
- 技术构成和竞品结构如何？
- 每个分支的核心专利有哪些——按分支组织，默认基于环节1召回信号分层，只在优先分支过薄时核查。
- **每个候选的价值信号集中在哪里**——高前向引用 × 大同族 × 有效法律状态 × 竞品集中度。

输出是给**环节3（patent-panorama-insights-tag）**和**环节4（patent-panorama-insights-report）**使用的统计 + 价值契约。

## 使用时机

- `/patent-panorama-insights-search` 已产出 `search_config.json` + `candidate_pool.csv` + `core_recall.csv` 之后。
- 单独使用：用户已有已验证检索式，希望直接获得全景统计 + 核心索引，不做标引。
- 在 `/patent-panorama-insights-tag`（taxonomy 推荐）和 `/patent-panorama-insights-report`（报告生成）之前。

## 输入契约（来自环节1 / patent-panorama-insights-search）

| File | Used for |
|---|---|
| `search_config.json` | 分支检索式（A6 四段）、恒定主题锚点、范围包络（司法辖区 / 日期口径 / 同族计数） |
| `candidate_pool.csv` | **pn 列表，仅供 pn 对照**（精简后只含 `pn, branch_rule_hits`，不含 metadata）。S1–S3 统计全部对检索式在线聚合，不读此文件。S4 enrichment 直接调 `/1458a4 bibliography`，不 join 此文件。 |
| `core_recall.csv` | 按分支组织的 `refered_rank` / `famn_rank` 召回清单（`branch_id, patent_id, pn, recall_source, raw_rank`，每分支约 top 10）——默认写入 `patent_index.core.*`；逐件核查只作为有边界的兜底 |

如果任何输入缺失，停止并要求用户先运行 `/patent-panorama-insights-search`。不要在这里重新推导检索式。

## 输出契约（给环节3 / 环节4）

| File | Content |
|---|---|
| `panorama_stats.json` | trend / applicant_rank / technology_constitute / tech_applicant_dist + 每个竞品画像 |
| `assignee_normalization.json` | 别名 / 子公司归并决策，`to_confirm` 标记 |
| `patent_index.core.json` / `.csv` | 按分支组织的核心专利——每条 23 字段（22 + `branch_id`）；默认采信环节1召回排序，仅在优先分支过薄时兜底核查 |
| `value_signals.json` | 候选级价值交叉得分；复用 S4 事实 + 分支级 portfolio_value 与 most_asserted，不重新查询 |
| `chart_data.json` | 所有聚合表，已适配图表，供环节4报告生成 |
| `panorama_stats_report.html` | **自包含统计仪表盘 HTML（数据快照报告）**——从已落盘的 `panorama_stats.json` + `chart_data.json` + `patent_index.core.*` + `value_signals.json` + `search_config.json` 渲染 S1–S5。可独立交付。不同于环节4的分析洞察报告（`report.html`） |
| `report_manifest.json` (extended) | 继承环节1 manifest；增加环节2文件索引、MCP 来源、数据截止日期 |

---

## 默认设置（继承环节1，重述）

| Dimension | Default |
|---|---|
| Technology stats counting | 简单同族层级（每族一条） |
| Market / legal stats counting | 公开文本层级（所有单件公开文本） |
| Date basis | 市场/法律用公开日（`pbdt`）；技术趋势用最早优先权日——与 `search_config.json` 声明保持一致 |
| Analysis mode | 竞品 vs. 行业（Mode C）——从 `run_config.json` 读取 |
| Core patent signal | 前向引用 × 同族广度 × 有效法律状态 |
| Excluded | 正式 FTO、侵权、SEP 必要性、有效性、新颖性、创造性意见 |

---

## 首选 MCP 栈

| Capability | Preferred MCP / tools | Fallback |
|---|---|---|
| 行业趋势 / 司法辖区 | `/59100a/mcp` `trend`, `search_patents_statistics`, `rec_office`, `get_rec_office_year` | `/3fd502/mcp` `trends` |
| 申请人格局 | `/59100a/mcp` `applicant_rank`, `applicant_trend` | `/3fd502/mcp` `applicant_ranking`, `/33072f/mcp` `search_patent_field(field=ASSIGNEE)` |
| 技术构成 | `/59100a/mcp` `technology_constitute`, `tech_applicant_dist`, `applicant_technology_analysis` | `search_config.json` 分支检索式的规则命中量 |
| 图表洞察 | `/3fd502/mcp` `trends`, `technology_effect_distribution`, `most_cited`, `portfolio_value` | 从 `chart_data.json` 本地生成图表 |
| 核心召回核查 | `/1458a4/mcp` `forward_citation`, `family`, `get_patent_legal_status`, `bibliography` | `/958a46/mcp` 单件专利简报 |
| 资产流（可选） | `/1458a4/mcp` `transfer_data`, `license_data`, `award_data` | — |

除非当前 key 的 `tools/list` 成功，否则默认不要使用 `/v1/ip/patent-landscape/mcp` 或 `/v1/ip/insights-report/mcp`。

---

## S1：行业全景统计

**回答问题：** 该领域规模多大，趋势往哪个方向，分布在哪里？

调用：
1. 对完整检索式调用 `/59100a` `trend` 或 `search_patents_statistics(field=APPLICATION_YEAR)` → 年度趋势。
2. `/59100a` `rec_office` 和 `get_rec_office_year` → 司法辖区/受理局分布及年度拆分。
3. `/3fd502` `trends` 作为图表友好的对比视图。
4. 从 `core_recall.csv` top 记录抽取 30–50 件样本调用 `/1458a4` `get_patent_legal_status`（不是从 `candidate_pool.csv`，因为池不再携带 metadata）→ 估算 active / pending / lapsed 比例。

输出到 `panorama_stats.json` + `chart_data.json`：
- 年度公开趋势（族级；最近 2 年注明公开滞后）。
- 司法辖区/受理局分布（文本级）。
- 法律状态分布估算，并注明样本量。

---

## S2：申请人格局

**回答问题：** 主要玩家是谁，相对规模如何，各自趋势如何？

调用：
1. 完整检索式 → `/59100a` `applicant_rank` → top 申请人及数量。
2. `/59100a` `applicant_trend` 获取 top 玩家趋势。
3. 兜底：`/33072f` `search_patent_field(field=ASSIGNEE, limit=30)`。
4. 对每个指定竞品：核查其是否出现；记录排名和数量。如缺失或异常偏低 → 标记为别名检查问题。

申请人归一化 → `assignee_normalization.json`：
- 关系明确时，将子公司归并到母公司。
- 不确定子公司标记为 `to_confirm`——不要静默合并。

输出：归一化 top 申请人排名（族级）、突出指定竞品、标注别名问题。

---

## S3：技术构成 + 竞品画像

**回答问题：** 该领域技术结构是什么；对每个指定竞品，规模、分支、市场、趋势和最具影响力专利如何？

### S3a — 技术构成（全领域）
1. `/59100a` `technology_constitute` → 官方 IPC / 技术类别基线。
2. `/59100a` `tech_applicant_dist` 或 `applicant_technology_analysis` → 申请人 × 技术结构。
3. 分支命中量：用 `/59100a` `search_patents_statistics` 跑每条 `search_config.json` 分支检索式。标注为**规则命中近似，重复计数**——环节3标引会产出验证后的分支标签。

### S3b — 竞品画像（仅 Mode B/C）
对每个指定竞品运行，并建立交叉矩阵。
1. 为每家公司构建/记录申请人别名检索式。
2. `/59100a` `applicant_trend` 或限定申请人的 `search_patents_statistics` → 总量 + 趋势。
3. 对申请人限定调用 `/59100a` `rec_office` → 司法辖区分布。
4. `/59100a` `applicant_technology_analysis` 或限定分支检索式 → 分支分布。
5. 限定近 3 年 → 近期焦点；与全周期组合对比。
6. 对申请人限定调用 `/59100a` `refered_rank` 或 `/3fd502` `most_cited` → 高被引专利。

交叉输出到 `panorama_stats.json` + `chart_data.json`：
- 竞品 × 分支矩阵（适配热力图）。
- 竞品 × 司法辖区矩阵。
- 每个玩家近 3 年焦点变化。
- 每个竞品 top 3–5 高被引专利（PN、标题、引用数）。

---

## S4：核心专利索引——按分支组织、数据驱动核查

**回答问题：** 每个技术分支中，哪些专利是该分支核心——已由环节1排序、分层，并只在必要时核查？

输入：`core_recall.csv`——环节1的**按分支组织**召回清单（`branch_id, patent_id, pn, recall_source, raw_rank`，每分支约 top 10）。这些是 **Patsnap 预计算的 `refered_rank` / `famn_rank` 排序**，不是需要批量核查的原始 ID。

> **设计决策（2026-05-31，精简版）：** 环节1 的 `candidate_pool.csv` 现在只含 `pn + branch_rule_hits`，不含 metadata。S4 的可展示字段 enrichment 改为直接对 core_recall 中的 pn **按需调用 `/1458a4 bibliography`**，而不是 join pool。核心专利总量通常 ≤ branch_count × 10（约 30–100 件），调用量可控，且只拉核心件不拉全池。

> **决策（2026-05-31）：默认采信环节1分支排序，按需兜底，绝不逐件全核查。** 旧做法会对每个候选串行调用 4–5 个 `/1458a4` 工具，返回值在上下文中累积，容易撑爆 200K 窗口。新做法：环节1给的就是智慧芽算好的现成排序，**默认直接采信落盘**；逐件 `/1458a4` 核查只在“分支凑不满 10 篇**且**是优先分支”时作为兜底触发，且全局封顶 **TOP-N = 50 次核查调用**。

### 默认路径（不逐件核查）

1. 读取 `core_recall.csv`，按 `branch_id` 分组。完整核心索引 = 每个分支按 `raw_rank` 取前约 10 → 总数约 **branch_count × 10**。该数量不封顶，因为采信环节1排序不消耗核查预算。
2. **通过批量 bibliography 补充可展示字段——不是 join candidate_pool。** 对 `core_recall.csv` 中的核心 pn，按分支一批调用 `/1458a4` `bibliography`。拉取 `title / abstract / assignee / ipc / publication_date / priority_date / jurisdiction`。只保留写入磁盘的字段，不在上下文累积完整响应。每批 ≤20 个 pn；每批后写盘；上下文只保留 `enriched X/N`。
3. **基于环节1召回信号 + join 结果分层，不做逐件 MCP：**
   - `recall_source = both`（高被引且大同族）→ `core_tier1`。
   - `recall_source = refered_rank` 或 `famn_rank` 单独出现且位于分支前半 → `core_tier2`。
   - 其余 → `core_tier3`。
   - 这是**信号分层**，标注为“recall-signal tier, not legal-verified”。
4. 立即写入 `patent_index.core.json` / `.csv`。对话中每分支只保留一行：`branch B3: 10 core, tier 2/5/3`。

### 兜底核查（数据驱动、有边界——TOP-N = 50 调用）

仅当**优先分支**（用户在 `run_config.json` 标记，或 S3 中 top-volume 分支）召回 **< 10** 个同族时触发。只对这些分支：

1. 对缺口候选运行 `/1458a4` `forward_citation` + `family` + `get_patent_legal_status` + `bibliography`，确认较低排名 ID 是否符合条件，并补齐 `candidate_pool.csv` 中未找到的 ID。
2. **全流程逐件核查调用总数硬上限 ≤50**（`TOP-N = 50`）。这是调用预算上限，不是输出上限；落盘核心索引可以超过 50 条（按 branch_count × 10），只限制核查调用。如果预算耗尽，在 manifest 记录 `verification_budget_exhausted`，不得静默继续调用。
3. **批量 ≤20，每批后写盘，上下文只保留 `verified X/N, tier a/b/c`。** 不要让带摘要、引用清单和同族成员的核查记录积累在对话里。
4. 对已核查记录，用法律核查规则升级分层：
   - **Tier 1：** 高引用且同族广度 ≥3 个主要司法辖区且法律状态有效。
   - **Tier 2：** 三项中任两项。**Tier 3：** 三项中任一项。
5. 如果核心索引超过约 120 条且用户要求完整重核查，在**隔离子代理**中运行 S4 兜底，避免逐件 payload 进入主上下文。

### 输出

`patent_index.core.json` / `.csv`——每个分支核心候选一条，23 字段（22 + `branch_id`）：
`record_id`, `branch_id`, `patent_id`, `publication_number`, `title`, `normalized_assignee`, `original_assignee`,
`publication_date`, `priority_date`, `jurisdiction`, `legal_status`, `family_size`, `citation_count`,
`score`, `tier`, `abstract`, `ai_summary`（由摘要机器生成）,
`technical_problem`, `technical_solution`, `technical_effect`, `recommendation_reason`（空——人工/环节3评审）,
`review_status`（`recall_signal` / `verified` / `needs_review`）, `source_run_id`。

- 默认采信路径下 `review_status = recall_signal`；兜底核查为 `verified`；摘要不可用（如部分 EP 专利）为 `needs_review`——不得编造缺失字段。
- 默认路径下 `family_size` / `citation_count` / `legal_status` 为 **null**（未核查），只对 `verified` 记录填写——不得从召回信号编造。
- 记录按 **`branch_id` 分组**，使环节3推荐包和环节4分支演进叙事直接对齐。

---

## S5：价值信号交叉挖掘（复用 S4 事实——不重新查询）

**回答问题：** 每个核心候选的价值信号集中在哪里？

范围是**候选级**，按 `branch_id` 组织。**本步骤不再次调用 `/1458a4`。** 所需逐件事实——引用、同族广度、法律状态——已在 S4 中解析并写入 `patent_index.core.*`。S5 **读取这些已落盘事实**，只添加下方低成本分支级信号。（分支级“价值热点”聚合不在这里做——环节4会从候选分数聚合护城河主题。）

| Signal | Source | Re-query? | Label as |
|---|---|---|---|
| High forward-citation | 复用 `patent_index.core.*`（S4）中的 `citation_count` | **no** | influence signal |
| Wide family | 复用 `patent_index.core.*`（S4）中的 `family_size` | **no** | global-protection proxy |
| Active legal status | 复用 `patent_index.core.*`（S4）中的 `legal_status`；默认采信路径用 `both`/`refered`/`famn` 召回信号做代理 | **no** | status signal |
| Competitor concentration | 读取 S3 的竞品 × 分支矩阵——哪个指定竞品集群拥有该候选分支 | **no**（S3 已计算） | who-owns-this-cluster signal |

分支级增强（低成本，按分支，不逐件循环）：

- `/3fd502` `portfolio_value` 对**每条分支检索式一次**（不是每件专利）→ 作为分支级组合价值信号，盖到该分支所有候选上。标注为信号，不是结论。
- `/3fd502` `most_asserted`（或 `most_cited` 兜底）对**每个分支一次** → 诉讼/主张强度信号。标注为诉讼暴露信号，不是法律结论。

> 调用量：S5 的逐件部分 **零 MCP 调用**（完全复用 S4 落盘）；只新增 `/3fd502` 的 `portfolio_value` + `most_asserted` 各按**分支数次**调用（branch-level，不逐件）。这是 S5 不再二次膨胀的关键。

评分：
- 将每项信号在候选集内归一化到 0–1，再合成为 `value_score`（记录所用权重）。
- 每个候选记录触发的信号和贡献事实。若某个逐件事实为 `null`（默认采信路径、未核查），使用召回信号做代理，并将证据标为 `recall_proxy`，而不是 `verified`。

输出：`value_signals.json`——每个核心候选一条：
`patent_id`, `pn`, `branch_id`, `citation_signal`, `family_signal`, `legal_signal`, `competitor_concentration_signal`,
`portfolio_value_signal`（分支级）, `most_asserted_signal`（分支级）, `value_score`, `signals_fired[]`, `evidence{}`（每项标 `verified` 或 `recall_proxy`）。

---

## S6：资产流信号（可选）

**回答问题：** top 候选是否存在明显转让、许可或奖项？

仅当用户要求资产情报，或 S4 发现感兴趣竞品的高层级候选时运行。

对 Tier-1 候选调用 `/1458a4` `transfer_data`, `license_data`, `award_data`。仅作为信号说明输出——不作法律结论。

---

## S7：统计仪表盘 HTML（`panorama_stats_report.html`）

**回答问题：** 分析师能否在不等待环节4的情况下，交付一个好看、直观、可离线打开的 S1–S5 快照？

这是**数据快照报告**，不同于环节4的分析洞察报告。它可视化“数到了什么、聚合了什么”，而不是“解释出了什么”。页眉必须带一句说明：**"统计快照（数据视图）；分析结论与演进/护城河解读见 环节4 洞察报告。"**

### 数据来源（不新增 MCP）
完全从已落盘文件渲染——`panorama_stats.json` + `chart_data.json` + `patent_index.core.*` + `value_signals.json` + `search_config.json`。**S7 不新增 MCP 调用。**

### 章节（依数据而定；v0.2 样例使用 8 个）
默认章节：**概览 / 检索质量 / 产业格局 / 申请人格局 / 技术分支 / 竞品矩阵 / 核心召回 / 方法边界**。运行有确认的下一步范围时，可包含 Layer 2 proposal 区块；数据缺失或有意压缩时，不强制固定章节数。

### 样式契约

单文件、自包含、无外部 CDN/D3、离线可打开。CSS 变量、字体、组件与环节4 `report.html` 保持一致，避免两套色板漂移。样式原则以 `skill/patent-panorama-insights/references/report-visual-style.md` 为准；当前视觉证明为 `examples/大模型联盟专利洞察/outputs/panorama_stats_report.html`。

- **CSS `:root` 变量（逐字照抄现有报告）：**
  `--bg:#ffffff; --bg-soft:#f7f9fc; --bg-mid:#eef2f8; --accent:#1d4ed8; --accent2:#0891b2; --accent3:#059669; --gold:#d97706; --red:#dc2626; --text-primary:#111827; --text-secondary:#374151; --text-muted:#6b7280; --border:#e5e7eb; --card-bg:#ffffff; --card-bg2:#f9fafb; --tier2-bg:rgba(29,78,216,0.05); --tier3-bg:rgba(217,119,6,0.05);`
- **字体：** `'Segoe UI', -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Microsoft YaHei', sans-serif`；`html` font-size 13px。
- **组件：** `.report-header`（双语标题 + tag-line + meta-row）、`.kpi-strip` / `.kpi-card`（4 列：候选池规模 / 申请人数 / 核心专利数 / 时间跨度）、`.section` / `.section-header`（双语 section 标题）、tier chip（tier1=accent / tier2=accent2 / tier3=gold）。
- **图表：** 优先用 HTML/CSS/SVG 静态结构渲染；如确需交互，JS 必须内联且可降级。禁止外部 D3/CDN 依赖。
- **数据注入：** 从已落盘 JSON/CSV 预聚合后写入 HTML，不读外部文件。

### 输出
`panorama_stats_report.html`——自包含统计仪表盘。落盘后在对话里只留一行 `panorama_stats_report.html written (N sections, N charts)`，不回贴 HTML 内容。

---

## 阶段性输出

S1–S5 完成后（可选 S6，随后 S7 渲染 `panorama_stats_report.html`），展示完整全景摘要 + Layer-2 范围建议。

```markdown
## 环节2 Panorama Summary

### Scope (from search_config.json)
[key parameters summarized inline]

### Industry Stats (S1)
- Total candidate pool: [N families / M publications]
- Annual trend: [growing / stable / declining since YYYY]
- Top jurisdictions: [...]
- Legal status estimate: [X% active, Y% pending, Z% lapsed] (sample N=__)

### Assignee Landscape (S2)
- Top 5 players: [...]
- Named competitors ranked: [...]
- Alias issues flagged: [...]

### Technology Constitution + Competitor Portraits (S3)
- Top branches by volume: [...] (rule-hit approximation)
- Fastest-growing branches (recent 3 yrs): [...]
- Per-competitor: [total, top branches, top markets, recent shift, top cited patent]

### Core Patent Index (S4)
- Organized by branch: [B1: N core, B2: N core, ...] (≈ branch_count × 10)
- Tier 1 (Core): [N] · Tier 2 (Strong): [N] · Tier 3 (Watch): [N]
- Verification: [採信 环节1 recall signals by default; fallback-verified X patents across Y priority branches, TOP-N budget used Z/50]
- See patent_index.core.json / .csv

### Value Signals (S5)
- Highest-value candidates: [top patents by value_score]
- Signal mix: [how many candidates fired all 4 signals]

### 环节3 Proposal
| Item | Proposal |
|---|---|
| Candidate pool for tagging | [N patents, from which branches/players] |
| Suggested tagging depth | Light (abstract) / Standard (abstract+claims) / Deep (full text) |
| Priority branches | [...] |
| Priority competitors | [...] |

Confirm 环节3 scope or adjust.
```

---

## MCP 工具参考

| Tool | MCP Server | Used In |
|---|---|---|
| `trend`, `search_patents_statistics`, `rec_office`, `get_rec_office_year` | `/59100a/mcp` | S1 |
| `applicant_rank`, `applicant_trend` | `/59100a/mcp` | S2, S3b |
| `technology_constitute`, `tech_applicant_dist`, `applicant_technology_analysis` | `/59100a/mcp` | S3 |
| `refered_rank`, `famn_rank` | `/59100a/mcp` | S3b（限定申请人）。核心召回已在 `core_recall.csv` 中——S4 默认不重新调用这些工具 |
| `trends`, `technology_effect_distribution`, `most_cited`, `portfolio_value`, `most_asserted` | `/3fd502/mcp` | S1, S3b；S5 的 `portfolio_value` + `most_asserted` 按**分支**运行（不是按专利） |
| `forward_citation`, `family`, `get_patent_legal_status`, `bibliography` | `/1458a4/mcp` | S4 **仅兜底**（优先分支 < 10 个同族；TOP-N ≤ 50 调用）。S5 复用 S4 落盘事实，不重新查询 |
| `transfer_data`, `license_data`, `award_data` | `/1458a4/mcp` | S6（可选） |
| （无——纯渲染） | — | S7 从已落盘文件渲染 `panorama_stats_report.html`，不调用 MCP |
| `search_patent_field` | `/33072f/mcp` | S1–S3 兜底 |

---

## 证据和语言规则

- 分支计数来自规则命中检索式：表述为“规则命中近似，重复计数”。
- 引用次数：表述为“前向引用信号，不是法律或质量结论”。
- 同族广度：表述为“全球保护代理指标——实际权利要求范围需要法律审查”。
- 法律状态：表述为“简单状态信号——执行决策前需法务确认”。
- `value_score`：表述为“综合信号分，不是估值——权重记录在 value_signals.json”。
- 竞品方向预测：使用“专利信号提示……”而不是“该公司将……”。
- 所有发现都要追溯到具体 MCP 调用、日期和检索式，并记录在运行日志中。

---

## 下一步 → 环节 3/4 · 标引推荐（patent-panorama-insights-tag）

环节2 统计与价值产物就绪后，路由到 `04_skill_draft/patent-panorama-insights-tag/SKILL.md`：
- Checkpoint 的环节3 Proposal 经用户确认后 → 读取 `patent-panorama-insights-tag/SKILL.md`，把 `panorama_stats.json` + `patent_index.core.*` + `value_signals.json` 作为输入交付。
- patent-panorama-insights-tag 据此推荐技术分解表 + 关键技术问题 + 推荐专利包，逐条标引交客户 SaaS 工具。
- 报告层 patent-panorama-insights-report（环节4）同时吃环节2的 `panorama_stats.json` + `value_signals.json` + `chart_data.json`。

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。

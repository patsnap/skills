---
name: patent-panorama-insights-report
description: 在专利全景项目的环节 4/4（环节4）使用本技能。它会把环节2统计/价值信号、环节3标引体系（tech_breakdown / key_questions / patent_packages）以及 SaaS 回流的 tagged_pool 转化为技术演进路线、护城河/价值交叉解读，并生成自包含 HTML 洞察报告（report.html + report_manifest.json）。
---

# patent-panorama-insights-report — 专利全景报告层（环节 4/4）

> **自报家门：** 我是环节 4/4（环节4）。上游是环节 2/4 patent-panorama-insights-stats（环节2 统计 + 价值信号）、环节 3/4 patent-panorama-insights-tag（环节3 标引体系 + 推荐包），以及环节 3.5 客户 SaaS 全量标引回流的 `tagged_pool.csv`。我是流水线的终点,产出交付给客户。

## 目的

环节4 将结构化专利分析转化为业务可读的报告。

它回答：

- 与决策相关的核心发现是什么？
- 哪些趋势、玩家、分支和专利包最重要？
- **技术随时间如何演进，哪些专利族标志着每次转向？**（技术演进路线）
- **可防御的护城河在哪里——哪些分支集中了承载价值的信号？**（护城河 / 价值交叉）
- 每个判断由什么证据支撑？
- 哪些内容仍不确定或需要专家复核？

环节4 是报告与综合层，不应替代法律审查。

## 适用场景

在以下条件满足后使用 `/patent-panorama-insights-report`：

- `/patent-panorama-insights-search` 和 `/patent-panorama-insights-stats` 已产出经验证的检索范围、统计结果、核心候选、价值信号和图表数据。
- `/patent-panorama-insights-tag` 已产出 `tech_breakdown.json`、`key_questions.json` 和 `patent_packages.csv`，或模式 A 中已有足够支撑报告的 SaaS 回流 `tagged_pool.csv`。
- 用户已确认报告目标和受众。

`tagged_pool.csv`（环节 3.5 客户 SaaS 全量标引回流）若已就位则报告完整；缺席时 环节4 降级为「仅基于推荐专利包 + 统计」的报告。

适用于：

- 单文件 HTML 报告。
- 报告大纲。
- 证据登记表。
- 推荐专利包摘要。
- 局限与下一步说明。

不要用于正式 FTO、侵权、SEP 必要性、有效性、新颖性或创造性意见。

## 输入

契约输入（ARCHITECTURE.md 第2节 环节2 / 环节3 / 环节 3.5 → 环节4）。

| File | Role |
|---|---|
| `report_manifest.json` (环节2, extended) | 范围、数据来源、计数方法、文件索引、MCP 出处、数据截止日 |
| `panorama_stats.json` (环节2) | trend / applicant_rank / technology_constitute / tech_applicant_dist + 竞品画像聚合 |
| `chart_data.json` (环节2) | 所有 chart-ready 聚合表（趋势、申请人、地域、分支） |
| `patent_index.core.json` (环节2) | 按 branch_id 分组、核查+分级后的核心专利（23 字段） |
| `value_signals.json` (环节2) | 候选级价值交叉打分；**环节4 在 §9 聚合到分支级护城河主题** |
| `tech_breakdown.json` (环节3) | 四列技术分解表，≤40 三级节点 → 技术矩阵 (§5) |
| `key_questions.json` (环节3) | ≥10 关键技术问题，按一级分支均分 → **演进路线种子 (§6，每条 ≥3 族)** |
| `patent_packages.csv` (环节3) | ≥10 细分领域 × ≥3 族，每件带 recommendation_reason |
| `tagged_pool.csv` (环节 3.5, SaaS 回流) | 客户 SaaS 全量标引回流，含每件三级技术分类 + 核心发明点。**可能上万行——只用脚本做分组/计数聚合，不逐行读入上下文。缺席时 环节4 降级为「仅基于推荐专利包 + 统计」的报告，并在报告中标注标引数据未回流** |
| `/59100a` official panorama outputs | 官方趋势、申请人、技术构成、地域、引用/同族排名信号 |
| `/3fd502` chart insight outputs | 技术功效分布、价值分布、最高被引及其他 chart-ready 信号 |
| `/7cc6ae` patent mining outputs | 已选专利的技术主题、应用领域、技术问题 / 手段 / 功效 |

### 运行模式 A vs B（标引后默认 A）

环节 3.5 客户 SaaS 标引回流 `tagged_pool.csv` 后，环节4 有两种跑法。**默认走 A**（标引池信息已足够丰富，可直接产报告，省去补造上游 环节3 推荐包的迭代）：

| 模式 | 触发 | 数据来源 | 适用 |
|---|---|---|---|
| **A · 标引池直驱（默认）** | 标引已回流，且 `tagged_pool.csv` 已带分类 + 技术手段/问题/功效字段 | `tagged_pool.csv`（标引主体，脚本聚合）+ 已有的 `panorama_stats.json` / `value_signals.json` / `patent_index.core.*` / `chart_data.json`（环节2 现成产物，**直接复用，不重跑 MCP**） | 路演 / 快速交付 / 上游 环节3 `tech_breakdown`·`key_questions`·`patent_packages` 尚未生成或无需重做时 |
| **B · 完整契约** | 需要 环节3 推荐包的人工 rubric 评审，或要严格走 ARCHITECTURE 全契约 | A 的全部 + 环节3 三件套（`tech_breakdown.json` / `key_questions.json` / `patent_packages.csv`） | 正式大交付、需可追溯到 环节3 rubric 的场景 |

**模式 A 的字段替代关系**（`tagged_pool.csv` 列 → 环节4 用途；列名随 SaaS 导出，执行前先 `head -1` 核对）：

| 环节4 需要 | tagged_pool 列（智慧芽 SaaS 导出常见名） |
|---|---|
| `pn` | 公开(公告)号 |
| 一级分类（§5 矩阵行 / §6 演进分支） | 技术分类\|Level 1 |
| 二级分类（§5 矩阵列 / §6 子分支） | 技术分类\|Level 2 |
| 三级分类（**有则下钻，无则 §5/§6 以二级为最细**） | 技术分类\|Level 3（本批无此列） |
| `technical_problem` / `solution_type` / `technical_effect`（§8 场景 / §7 功效） | 技术问题 / 技术手段 / 技术功效 |
| `normalized_assignee`（§4 竞品） | [标]当前申请(专利权)人 |
| `year`（§3 趋势 / §6 时间轴） | 公开(公告)日（族级取最早）；申请日备用 |
| `legal_status`（§9 有效占比） | 法律状态/事件 |
| `cited_by_count`（§9 被引信号 / §10 选包） | 简单同族被引用专利总数 |
| `family_country_count`（§9 同族宽度 / §10 选包） | 简单同族国家/地区数量 |
| family 国家列表（§3 地域、显示用） | 简单同族国家/地区 |
| `family_id`（族级去重键） | 简单同族编号 |

**模式 A 三条口径（已与用户确认）：**

1. **层级兼容、二级优先：** 报告方案兼容 2 层 / 3 层；本批数据只到 Level 2，**优先做好二级展示**，二级即最细分支；保留三级钩子，将来 `tagged_pool.csv` 出现 Level 3 列能自动下钻。
2. **允许多标签重复计数：** 一件专利的技术分类列可能含多个值（换行分隔，Level 1 / Level 2 同理）。§5 技术矩阵按这些标签展开计数，一件可计多次，报告**显著标注「分类计数 ≥ 专利数」**。这是正常情况，不去重为单值。
3. **族级去重用 `简单同族编号`：** 计数前先按 family_id 去重（公开号级 → 族级）。本批每件各自成族，去重后数量不变，但 schema 上仍按族级处理。

**模式 A 下 §6 / §10 的降级：**
- §6 演进路线：缺 环节3 `key_questions` 时，**用一级分类作为演进分支**。取族口径（已在大模型联盟 run 验证，避免明星专利劫持不相关分支）：① 先拆多标签——Level 1 / Level 2 单元格可能含换行多值，按 `\n` 拆开并 `strip('"')` 清残留引号；② 每个一级分支圈定其**主导 Level 2 子分支集**（对齐 §5 矩阵 Top 2–3），代表族必须 Level 1 命中该分支**且** Level 2 落在该子分支集内（用 (Level 1, Level 2) 配对，不能只看 Level 2，因 Level 2 词表跨一级共享）；③ 按公开年分早（≤2024）/ 成型（2025）/ 前沿（2026）三段，**段内取被引最高**，**三段间用全局 `used` 集禁止同族复用**，并**软轮换主导玩家**（优先选本路线尚未出现的申请人，让中小玩家在其被引占优段露出；实在没有再放开）；④ `turning_point{type,note}` 与 `phase_caption` **取自该代表族自身的「技术问题 / 技术手段」标引字段**，不脑补：首段=`关键专利出现`，玩家变更段=`玩家入场`，玩家延续段=`性能跃迁`。仍配 `evolution_overview` + `route_summary` + `phase_caption`，不虚构空段。⚠️ 软轮换会让中小玩家偏向露在其被引占优的时段，`evolution_overview` 须注明这是取样算法效果、非真实布局时点。
- §10 推荐专利包：缺 环节3 `patent_packages.csv` 时，**从 tagged_pool 自动精选**——每个二级分支取「被引最高 + 同族最宽」2–3 件，按 §10 给 `use_case` / `purpose_tag` / `answers_question` + `package_summary`；明确标注为自动精选、非人工 rubric 评审（脚注层标 L4）。
- 报告头部声明：「模式 A · 标引池直驱；§6/§10 部分为标引池字段的自动派生，非 环节3 人工评审」。

## 输出

契约输出（ARCHITECTURE.md 第2节 环节4 输出契约）。

| File | Content |
|---|---|
| `report_manifest.json` | 报告结构 + 每节数据出处映射 + 证据登记索引 + 模式/降级标注。**演进路线含 `evolution_overview` + 每条 route 的 `route_summary` / `phase_caption[]` / 结构化 `turning_point`；推荐包含 环节4 翻译出的 `use_case` / `purpose_tag` / `answers_question`，每个 sub_domain 含 `package_summary`，环节3 原始 `recommendation_reason` 保留为脚注层可追溯字段** |
| `report.html` | 单文件、自包含、离线可打开的洞察报告 |

可选输出：

- `evidence_register.json` — 关键发现背后的证据条目（也可内嵌进 `report_manifest.json`）
- `report_limitations.md` — 局限说明
- `recommended_patent_package.csv` — 推荐专利包的可读副本

> **与 环节2 `panorama_stats_report.html` 的区别：** 环节2 出的是**统计快照（数据视图）**——只可视化「数到了什么、聚合了什么」；环节4 出的 `report.html` 是**洞察报告（分析视图）**——演进路线、护城河解读、布局建议。两者共用同一套样式契约（见下），但定位不同,不可混淆。

## 报告结构（默认模块；随数据完整度调整）

默认模块可根据数据完整度和交付目的合并、改名或压缩。v0.2 样例使用 10 个章节：执行摘要 / 范围方法 / 格局 / 技术矩阵 / 演进路线 / 功效分布 / 问题场景 / 护城河 / 推荐包 / 附录边界。

| # | 节 | 主要数据源 | 证据级别主调 |
|---|---|---|---|
| 1 | 执行摘要 Executive summary | 全报告提炼 | 环节4/L4 |
| 2 | 范围与方法 Scope & methodology | `report_manifest.json`（scope/日期口径/族级口径/数据截止日/MCP 出处） | 环节1 |
| 3 | 行业格局 Industry landscape | `panorama_stats.json` trend/jurisdiction/legal_status_estimate | 环节1/环节3 |
| 4 | 竞品画像 Competitor portrait | `panorama_stats.json` competitor_portraits[] | 环节1/环节3 |
| 5 | 技术矩阵 Technology matrix | `tech_breakdown.json` + `tagged_pool.csv`（按三级分类计数聚合） | 环节1/环节3 |
| **6** | **技术演进路线 Technology evolution route** | `key_questions.json` + `patent_index.core.*` + `tagged_pool.csv` | 环节3/环节4 |
| **7** | **技术功效分布 Technology-effect distribution** | `/3fd502 technology_effect_distribution` + `chart_data.json` | 环节1/环节3 |
| 8 | 产品 / 部件 / 场景 Product/component/scenario | `tagged_pool.csv` + `panorama_stats.json` tech_applicant_dist | 环节1/环节3 |
| **9** | **护城河 / 价值交叉 Moat & value cross** | `value_signals.json`（**环节4 聚合到分支级**）+ `patent_index.core.*` | 环节4/L5 |
| 10 | 推荐专利包 Recommended patent package | `patent_packages.csv` + `value_signals.json` | 环节1/L4 |
| 11 | 风险与局限 Risks & limitations | 全报告 + `report_limitations.md` | L5 |
| 12 | 附录与数据 Appendix & data files | 全部落盘文件清单 | 环节1 |

> 节序决策（已确认）：**演进路线紧跟技术矩阵之后（§6）**——先看静态结构再看动态走向；**护城河紧接在推荐专利包之前（§9）**——先讲清价值在哪集中,再给出可落地的推荐包。

### §6 技术演进路线（新增模块）

从 `key_questions.json` 的关键技术问题出发,为每条问题织一条时间轴。**演进路线不只是把专利族排成时间轴——必须配"看了之后所以呢"的总结**,所以采用自顶向下三层总结结构:

**三层总结结构（自顶向下）：**

| 层级 | 字段 | 内容 | 数据来源 | 证据级别 |
|---|---|---|---|---|
| 全章顶部 | `evolution_overview` | 一段话跨所有分支:哪些分支在**加速**、哪些在**收敛**、哪些**刚冒头**。先鸟瞰再看分条时间轴。 | 跨分支 trend + key_questions 聚合 | 环节4 |
| 每条路线顶部 | `route_summary` | **一句话**:「本分支从【早期主线】→ 收敛到【当前主线】→ 正在向【前沿方向】演进。」 | `key_question.question` + `rationale` + 三段代表族 | 环节4 |
| 每段(早/中/前沿) | `phase_caption` | 一句话:该阶段技术特征 + 主导玩家。 | 该段代表族的 assignee + 三级节点 | 环节3/环节4 |

**取族与排序：**

- **种子：** 每个 `key_question` 的 `seed_node_ids[]` → 落到 `tech_breakdown.json` 的三级节点。
- **取族：** 在 `tagged_pool.csv`（或缺席时 `patent_index.core.*`）里按这些三级分类取代表专利族,**每条演进路线 ≥3 族**,沿公开日 / 优先权日排序成「早期 → 当前 → 前沿」三段。
- **每族标注：** publication_number、normalized_assignee、公开年、所属三级节点、**结构化转折点**(见下)。

**转折点要说清"为什么是转折"：** 每族的 `turning_point` 从一句模糊感想改为带类型枚举:

```text
turning_point:
  type: 路线分叉 | 关键专利出现 | 玩家入场 | 性能跃迁 | 场景迁移
  note: 一句话说明,点出转折转的是什么
```

- **不虚构时间点：** 没有族落在某时间段就如实留空,`route_summary` 不脑补「过渡技术」或不存在的过渡阶段。
- **可视化：** 用 HTML/CSS/SVG 或内联 JS 绘制横向时间轴，每条一级分支一行；`route_summary` 显示在该行时间轴上方，`phase_caption` 显示在三段分隔处，`evolution_overview` 显示在章节开头。禁止外部 D3/CDN 依赖。

### §7 技术功效分布（新增模块）

调用 `/3fd502 technology_effect_distribution`,出「技术手段 × 功效改进」矩阵:

- **数据源：** 对候选池检索式跑一次 `technology_effect_distribution`,结果落进 `chart_data.json`。
- **可视化：** 用 HTML/CSS/SVG 或内联 JS 绘制气泡 / 热力矩阵，横轴功效维度、纵轴技术手段、气泡大小=族数。禁止外部 D3/CDN 依赖。
- **标注：** 标 `/3fd502` 信号,非验证后结论;空白格如实标「该手段-功效组合在本数据集下无显著族」。

### §9 护城河 / 价值交叉（新增模块）

把 `value_signals.json` 的**候选级**分数聚合成**分支级护城河主题**（环节2 显式不做此聚合,留给 环节4）:

- **聚合方式：** 按 `branch_id` 汇总该分支下候选的 citation_signal / family_signal / legal_signal / competitor_concentration_signal / portfolio_value_signal / most_asserted_signal,得到分支级护城河强度。
- **解读：** 哪些分支同时高被引 + 大同族 + 高竞品集中 → 高护城河;哪些分支信号稀薄 → 蓝海或未成熟。
- **诚实标注：** 默认采信路径下 citation/family/legal 为 recall 信号代理,标 `recall_proxy`;只有 verified 记录用真实值。聚合分是**信号**,不是估值,不构成法律结论（L5）。
- **可视化：** 分支级护城河雷达 / 堆叠条形,signals_fired 透明展示。

### §10 推荐专利包（用户视角重构）

> **核心原则：推荐理由必须是「用户视角」,不是「分析师视角」。** 环节3 `patent_packages.csv` 的 `recommendation_reason` 是六项技术属性 rubric(`disruptive_technology` / `novel_function` …),回答的是「我们为什么从数据里挑中它」;客户真正要的是「我拿到它能干嘛」。**环节4 在渲染时做一层翻译,不改 环节3 schema。**

**双层呈现：** 主层用客户语言,数据信号下沉脚注(见「双层渲染规则」)。

**环节4 翻译产出的三个用户视角字段：**

| 字段 | 内容(用户视角) | 怎么来 | 证据级别 |
|---|---|---|---|
| `use_case`(主句) | 「建议用于:__」——客户拿到能干的动作 | 由 `purpose_tag` 决定句式 | L4 |
| `purpose_tag`(用途标签,枚举) | `监控竞品` / `规避设计参考` / `许可备选` / `自研借鉴` / `布局卡位` | 由 rubric + value_signals + assignee 映射推断 | L4 |
| `answers_question`(挂问题) | 「回答关键问题 Qn:__」 | 该族 `sub_domain` → 反查 `key_questions.seed_node_ids` 命中的 question_id | L4 |

**rubric + value_signal → purpose_tag 映射规则：**

| 环节3 rubric + value_signal 组合 | 推断 purpose_tag |
|---|---|
| 高竞品集中度 + 竞品 assignee | 监控竞品 |
| 大同族 + 有效法律状态 + 高被引 | 规避设计参考 / 布局卡位 |
| 高 portfolio_value + 资产流转信号 | 许可备选 |
| disruptive_technology / novel_function 且非竞品主导 | 自研借鉴 |
| novel_application_scenario / pulls_latent_user_demand | 布局卡位 |

> 映射是**启发式推断**,标 L4(recommendation),环节3 原始 rubric 保留在脚注层可追溯。映射不命中时 `purpose_tag` 留「待人工判定」,不硬塞。

**整包加「这个包是干嘛的」：** 每个 `sub_domain` 包顶部加 `package_summary`(一句话):这一包集中解决什么 + 推荐优先看哪 1–2 件。

**最终推荐卡片结构(双层)：**

```text
【主层 · 客户语言】
  ▸ use_case:         "建议用于 监控竞品 —— 覆盖 XX 技术,是 [竞品] 的核心卡位"
  ▸ purpose_tag:      [监控竞品]   ← 彩色 chip,可按标签筛选推荐包
  ▸ answers_question: "回答关键问题 Q3:如何降低端侧推理时延"

【脚注层 · 可展开 ⓘ 角标】
  ▸ rubric:           major_performance_gain（环节3 原始推荐依据）
  ▸ evidence:         同族 18 国 · 被引 42(recall_proxy) · 法律有效 · refered_rank top
  ▸ 免责:             信号仅供参考,不构成 FTO / 许可建议（L5）
```

## 证据级别

一致使用以下级别：

| Level | Meaning | Examples |
|---|---|---|
| 环节1 data fact | 直接计数事实 | 数量、排名、日期、地域 |
| 环节3 observed pattern | 跨事实可见的模式 | 增长、集中、分散、分支迁移 |
| 环节4 interpretation | 分析师解读 | 某一模式为什么可能重要 |
| L4 recommendation | 业务行动建议 | 接下来监控、标引、阅读或对比什么 |
| L5 legal/risk signal | 仅作风险线索 | 法律状态、同族宽度、转让、无效线索 |

报告中的每个重要判断都应映射到一个或多个证据条目。

## 证据登记

`evidence_register.json` 应使用如下条目：

```json
{
  "evidence_id": "E-001",
  "level": "环节1 data fact",
  "claim": "在标引池中，Agent workflow 专利是最大的标引组。",
  "source_file": "tagged_pool.csv",
  "source_field": "tech_level_2",
  "counting_method": "记录级单值标签（由脚本聚合，不逐行读入上下文）",
  "limitations": "标签是由 SaaS 工具应用的环节3分类标签，不是法律结论。"
}
```

## 推荐专利包

**用户视角优先(见 §10 设计段)。** 每件推荐专利的主层呈现 `use_case` + `purpose_tag` + `answers_question`(客户语言:能干嘛、归哪类用途、回答哪个关键问题);每个 sub_domain 包顶部有 `package_summary`。

下列筛选/排序标准是**分析师视角的选取依据**,作为脚注层的可追溯证据,不作为主文案:

- 与优先分支的相关性。
- 技术问题和解决方案的清晰度。
- 同族宽度或地域信号。
- 法律状态信号。
- 有意义时的引用信号。
- 可用时的官方 `refered_rank`、`famn_rank`、`most_cited` 或 `portfolio_value` 信号。
- 申请人的代表性。
- 是否已进行权利要求/说明书审阅。

未经专家审查，不要建议收购、许可、维权或 FTO 行动。

## HTML 报告规则

- 保持报告自包含。
- 说明数据来源、日期、地域和计数方法。
- 区分官方全景统计、本地规则命中近似值和环节3验证标签。
- 将规则命中数量标记为近似值。
- 将标引分布标记为环节3标签，而不是法律结论。
- 除非已通过底层专利记录验证，否则将 `/3fd502` 的价值、诉讼、引用和功效输出标记为信号。
- 在相关分析附近写明局限，不只放在文末。
- 在附录中链接或列出所有数据资产。

## HTML 骨架与样式契约

> **样式事实来源：** `skill/patent-panorama-insights/references/report-visual-style.md`。`report.html` 与 环节2 的 `panorama_stats_report.html` **共用同一套 CSS 变量、字体、组件与图表表达原则**，避免两套色板漂移。当前视觉证明为 `examples/大模型联盟专利洞察/outputs/report.html`。

- **自包含：** 单文件、CSS/数据全内联、无外部 CDN/D3、离线可双击打开。数据从落盘 JSON/CSV 预聚合后写入 HTML，不读外部文件、不逐行读 `tagged_pool.csv`（按脚本预聚合后只注入聚合结果）。如确需交互，JS 必须内联且可降级。
- **CSS `:root` 变量（逐字照抄现有报告）：**
  `--bg:#ffffff; --bg-soft:#f7f9fc; --bg-mid:#eef2f8; --accent:#1d4ed8; --accent2:#0891b2; --accent3:#059669; --gold:#d97706; --red:#dc2626; --text-primary:#111827; --text-secondary:#374151; --text-muted:#6b7280; --border:#e5e7eb; --card-bg:#ffffff; --card-bg2:#f9fafb; --tier2-bg:rgba(29,78,216,0.05); --tier3-bg:rgba(217,119,6,0.05);`
- **字体：** `'Segoe UI', -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Microsoft YaHei', sans-serif`；`html` font-size 13px。
- **组件：** `.report-header`（双语标题 + tag-line + meta-row,border-bottom 2px solid var(--accent)）、`.kpi-strip` / `.kpi-card`、`.section` / `.section-header`（双语 section 标题）、tier chip（tier1=accent / tier2=accent2 / tier3=gold）、证据级别 badge（环节1–L5）、**`purpose-tag` chip（5 色,对应 5 个用途标签:监控竞品 / 规避设计参考 / 许可备选 / 自研借鉴 / 布局卡位,可点击筛选推荐包）、`evidence-footnote` 折叠组件（ⓘ 角标展开,承载下沉的证据级别 + 数据信号 + 免责）**。
- **双层渲染规则（§6 / §9 / §10 必须遵守）：** 业务结论用主文案呈现(client-readable 语言:**是什么、所以呢、能干嘛**);环节1–L5 证据级别 badge、数据信号(被引数 / 同族宽度 / recall_proxy / refered_rank / rubric)、免责声明统一收进**可展开的 ⓘ 角标 / `evidence-footnote` 折叠脚注**,不在主文案行平铺。让客户先读懂结论,需要深究再点开证据,避免信号过载淹没结论。
- **图表：** 优先 HTML/CSS/SVG 静态表达，必要时用内联 JS；禁止外部 D3/CDN。覆盖趋势 + 地域、竞品卡片、技术矩阵、演进时间轴、技术功效矩阵、护城河/价值信号、推荐包表。
- **头部声明：** report-header 注明定位「洞察报告（分析视图）」+ scope/日期口径/族级口径/数据截止日/MCP 出处;若 `tagged_pool.csv` 缺席,头部显著标注「标引数据未回流,报告降级为仅基于推荐专利包 + 统计」。

### 输出

落盘后在对话里只留一行 `report.html written (N sections, N charts) + report_manifest.json`,**不回贴 HTML 内容**。

## 边界

不要输出：

- 正式 FTO 意见。
- 侵权意见。
- 有效性意见。
- SEP 必要性意见。
- 新颖性或创造性法律意见。
- 没有证据支持的业务判断。

在适当位置使用 “patent signals suggest”、“under this dataset” 和 “requires legal review” 等措辞。

## 下一步

我是环节 4/4(环节4),流水线终点。`report.html` + `report_manifest.json` 落盘后,把交付物清单交回编排层 `patent-panorama-insights`,由其向用户汇报全景分析完成。

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。

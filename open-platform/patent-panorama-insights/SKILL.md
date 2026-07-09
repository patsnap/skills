---
name: patent-panorama-insights
description: 当用户需要基于 PatSnap 或智慧芽专利 MCP/API 数据开展专利全景、专利版图、竞争专利情报、技术路线图、组合规划、产品/R&D 策略项目时使用本技能——无论用户显式调用 /patent-panorama-insights（或 @patent-panorama-insights），还是用自然语言描述这类专利分析任务。本技能编排五层流水线：环节1检索与降噪（search-planning step）、环节2全景统计与价值挖掘（statistics step）、环节3标引体系推荐（pps-tag）、客户 SaaS 工具中的人工标引交接，以及环节4有证据支撑的单文件 HTML 报告（report-generation step），并管理各层之间的检查点、人工标引交接、回滚和进度汇报。
---

# Patent Panorama Insights

## 第 0 步 · 预检：智慧芽专利 MCP（环节1前执行）

没有智慧芽（PatSnap）专利 MCP，本技能无法运行。工作流会把端点 ID（`/59100a`、`/1458a4` 等）硬编码为工具命名空间；如果这些工具没有连接，所有 MCP 调用都会因 “tool not found” 失败——这是配置缺口，不是技能缺陷。

**在做其他事情之前，先自检，然后分支处理：**

确认 5 个必需工具命名空间 — `59100a` `1458a4` `33072f` `3fd502` `7cc6ae` — 在当前 agent 运行环境中可见/可调用（出现在可用工具列表中，或一个简单的 `tools/list` 类探测成功）。3 个可选命名空间（`4eaa49` `958a46` `1fadfc`）可以缺席；主流水线仍可运行。

- **如果 5 个必需命名空间全部可解析** → 配置正常，直接进入环节1（search-planning step）。不要打断用户。
- **如果任何必需命名空间缺失 / 因 “tool not found” 失败** → 当前运行环境未连接智慧芽 MCP。引导用户完成连接（见下文），直到全部解析成功后再继续。不要为了绕过缺失 MCP 而编造专利数据。

### 连接方式（仅在上方检查显示端点缺失时使用）

在当前部署中，智慧芽 MCP 由宿主 agent 平台提供——这里没有 Eureka 桌面版的 `mcp add` / 项目审批流程。连接方式：

1. 确保平台侧有有效的智慧芽 API 凭证（Bearer token），并已开通所需端点权限。密钥在平台侧配置；本技能不包含密钥。
2. 在宿主平台的 MCP 配置中注册 / 启用 8 个端点。工具命名空间**必须等于端点 ID**——本技能硬编码了 `/59100a` 风格的 ID，因此如果服务器被重命名/别名化，工具将无法解析：

   | namespace (=id) | 用途 | 必需 |
   |---|---|---|
   | `59100a` | 技术全景统计（环节 2 主入口） | ✅ |
   | `1458a4` | 专利详情 / 事实核查 / 同族 / 引用 / 法律 | ✅ |
   | `33072f` | 高级检索辅助 + 扩词 fallback | ✅ |
   | `3fd502` | 图表型洞察（功效分布 / 价值 / 被引） | ✅ |
   | `7cc6ae` | 技术主题 / 应用领域 / 三要素预标签 | ✅ |
   | `4eaa49` | 大规模异步全景任务 | optional |
   | `958a46` | 单件专利速览简报 | optional |
   | `1fadfc` | 标准报告生成任务 | optional |

3. **验证：** 重新执行上述自检；5 个必需命名空间应可解析。如果调用返回 `401/403`/`No permission`，说明凭证无效、套餐未启用或该端点未授权——需要在平台侧修复，而不是在技能内修复。

必需端点可解析后，继续进入“目的”和环节1。

## 目的

使用本技能支持面向客户的专利全景项目，服务于产品规划、R&D 策略和专利组合规划。

本技能帮助 agent 将业务问题转化为可复现的分层分析工作流和客户可交付 HTML 报告：

```text
显式启动 -> 默认设置 + 需求采集
  -> Stage 1 search-planning step   (规则检索 + 降噪 + 候选池)
  -> [Checkpoint 1: confirm queries]
  -> Stage 2 statistics step    (全景统计 + 价值点交叉挖掘)
  -> [Checkpoint 2: confirm scope before tagging-system design]
  -> Stage 3 pps-tag      (推荐标引体系 + demo + 待标引导出)
  -> [Checkpoint 3: confirm tagging system]
  -> [Manual handoff 3.5: client tags the full pool in their SaaS tool, then returns the tagged file]
  -> Stage 4 report-generation step   (演进路线 + 护城河解读 + 单文件 HTML 报告)
  -> [Checkpoint 4: confirm report]
```

## 适用场景

只有当用户显式调用 `/patent-panorama-insights` 或 `@patent-panorama-insights` 时，才启动完整工作流。

如果用户提到专利全景但没有显式调用，简短询问是否启动本技能并索取最少输入；不要自动开始完整工作流。

适用于：

- 全景专利洞察 / patent panorama / patent landscape.
- 技术赛道、产品方向、研发方向的专利分析.
- 多家公司、竞品、重点申请人的专利布局对比.
- 重点技术路线、关键问题、解决方案、代表专利分析.
- 专利推荐包、专利标引清单、专利卡片.
- 基于 PatSnap / 智慧芽 MCP/API 的专利数据分析和 HTML 洞察报告.

不适用于：

- 不包含专利分析的一般市场研究。
- 对侵权、有效性、FTO、SEP 必要性、新颖性或创造性的正式法律意见。
- 文献/NPL 或 SEP 项目，除非所需工具明确可用且用户要求扩展到该范围。

## 环节命名与进度汇报

这条流水线有五层。每层有两个名称：内部技能名（`pps-*`，供 agent 加载/路由）和面向用户的环节名（用于每次向用户汇报，让用户始终知道现在在哪一层、这一层做什么、是否需要用户动作）。

| Layer | Internal name | Stage no. | User-facing stage name | One-line role | User action |
|---|---|---|---|---|---|
| Orchestration | `patent-panorama-insights` | — | 专利全景洞察（总控） | 串联所有层并管理检查点 | — |
| 环节1 | `search-planning step` | 环节 1 | 检索建库 | 专家检索式 + 降噪 + 候选池 | ✅ confirm queries |
| 环节2 | `statistics step` | 环节 2 | 格局统计 | 趋势 / 申请人 / 竞品 / 价值点挖掘 | review results |
| 环节3 | `pps-tag` | 环节 3 | 标引体系设计 | 推荐分解表 + 专利包 + demo | ✅ take to SaaS |
| (manual) | — | 环节 3.5 | 客户标引（线下） | 在客户 SaaS 中逐条全量标引 | ✅✅ client-led |
| 环节4 | `report-generation step` | 环节 4 | 报告生成 | 演进路线 + 护城河 + HTML 报告 | confirm report |

进度汇报规则：

- 每条环节级状态消息都以 `【环节 X/4 · 名称】` 开头。环节编号为 1–4；人工标引步骤为 `环节 3.5`。
- 进入任一层时，agent 用一行话自报位置，例如：“我现在在【环节 2/4 · 格局统计】（statistics step）。”
- 完成某一层时，汇报：产出了什么（关键文件 + 头部数字），然后说明下一环节以及是自动继续还是等待用户。
- 全程使用同一套中文环节名；除非用户询问技术名，否则不要把 `pps-*` 内部名放在面向用户消息的标题里。

状态消息格式：

```text
【环节 1/4 · 检索建库】完成 ✓
  候选池 N 族，M 个技术分支精度均 ≥80%
→ 即将进入【环节 2/4 · 格局统计】，默认继续

【环节 3/4 · 标引体系设计】完成 ✓
  已导出 to_be_tagged.csv（待标引 N 件）
⏸ 需要你动手：请在智慧芽 SaaS 完成标引，把结果放回约定路径
  完成后回复"标引已上传"，进入【环节 4/4 · 报告生成】
```

## 操作原则

- 从业务决策出发，而不是从现有图表出发。
- 尽量减少用户确认。标准全景范围使用默认设置；保留正式检查点（Checkpoint 1–3），但保持轻量，并在人工 SaaS 交接前确认标引体系。
- 开始时告诉用户默认设置，并只询问缺失的必需输入。
- 如果技术领域较宽，先围绕子技术、产品、部件和应用场景做一次拆解，再进入检索。
- 可用时使用已安装的 PatSnap / 智慧芽 MCP 工具；不要假设未安装的 REST、SEP、NPL、导出或高级全景 API 可用。
- 保持分析可复现：记录检索逻辑、日期范围、地域、申请人归一、计数方法和数据截止日。
- 每个重要结论都必须能追溯到数据、代表专利或明确陈述的假设。
- 将法律状态、诉讼、无效、转让、许可、质押、海关和获奖数据视为信号，而不是法律结论。
- 优先使用简洁、决策导向的业务语言。关键技术术语有帮助时可保留英文。

## 启动默认设置与需求采集

启动时说明这些默认设置，并向用户询问缺失的必需输入。

| Dimension | Default |
|---|---|
| Decision goals | 产品规划、R&D 策略、竞品跟踪和专利组合规划 |
| Geography | 中国、美国、欧洲 |
| Time range | 最早优先权日在 2023-01-01 及之后 |
| Counting method | 公开 / 公开文本层级 |
| Main deliverable | 单文件自包含 HTML 报告 |
| Exclusions | 不提供正式 FTO、侵权、有效性、SEP 必要性、新颖性、创造性或法律意见 |

必需用户输入：

- 技术领域或技术主题。
- 申请人/实体范围：全行业、选定申请人或竞品集合。
- 如有，关注的产品、产品部件或应用场景。

如果技术领域较宽，先做一轮拆解：

- 子技术和技术分支。
- 产品类别和产品部件。
- 应用场景。
- 需要关注的技术问题或功效。
- 排除项或已知噪声区域。

启动回复格式：

```markdown
除非你另有说明，我会使用这些默认设置：
- 决策目标：产品规划、R&D 策略、竞品跟踪、专利组合规划
- 地域：CN / US / EP
- 时间范围：最早优先权日 >= 2023-01-01
- 计数口径：公开 / 公开文本层级
- 交付物：单文件 HTML 报告
- 排除项：正式法律意见、SEP 必要性、FTO、侵权、有效性、新颖性、创造性

请提供：
1. 技术领域 / 技术主题
2. 申请人范围：全行业或选定申请人
3. 关注产品、部件或应用场景
```

启动时不要要求用户确认完整范围。正式确认点是 Checkpoint 1–3；其中有约束力的是 Checkpoint 3（确认标引体系），它位于人工 SaaS 交接（环节 3.5）之前。

## V0 能力边界

V0 可以支持：

- 专利检索。
- 著录项目详情。
- 同族和地域布局。
- 前向引用信号。
- 可用时读取权利要求和说明书。
- 简单法律状态。
- 法律事件线索。
- 可用时的复审 / 无效线索。
- 可用时的许可、转让、质押、海关和获奖线索。
- 官方全景 MCP 聚合：趋势、申请人、地域、技术构成、申请人趋势和关键专利排名。
- 可用时的图表型技术功效、价值、引用和诉讼信号视图。
- 技术主题、应用领域和技术问题 / 手段 / 功效的专利挖掘预标签。
- 作为 fallback 或服务业务专属分类体系的本地聚合。
- 客户可用 HTML 报告以及 Excel 风格的专利/专利包表。

V0 默认不应承诺：

- 完整文献/NPL 分析。
- SEP 必要性分析。
- 完整诉讼或 UPC 争议地图。
- REST API 批量导出。
- 未经当前 key 通过 `tools/list` 验证的 `/v1/ip/...` OpenAPI panorama / insights MCP 端点。
- 正式 FTO、侵权、新颖性、创造性或有效性意见。

## 参考文件导航

只加载用户当前场景所需的参考文件：

| User Need | Reference |
|---|---|
| 单文件 HTML 报告结构 | `references/report-html-blueprint.md` |
| HTML 视觉风格、仪表盘布局和组件规则 | `references/report-visual-style.md` |
| 行业格局、趋势、玩家、地域 | `references/scenario-industry-landscape.md` |
| 技术分类、路线演进、未来方向信号 | `references/scenario-technology-evolution.md` |
| 选定竞品或关键玩家画像 | `references/scenario-competitor-portrait.md` |
| 关键问题、解决方案路线、代表专利深读 | `references/scenario-solution-deep-dive.md` |
| 推荐专利包、专利卡片、标引索引 | `references/scenario-patent-package-and-index.md` |
| 高价值资产和法律/风险信号 | `references/scenario-asset-and-risk-signals.md` |

不要把机密原始材料作为参考文件加载。它们只能用于提取经过脱敏的模式和验证。

## PatSnap MCP 工具映射

可用时，将这些 MCP 工具作为专利数据层。统计优先使用较新的官方全景工具栈，同时保留 `/1458a4/mcp` 作为事实核查来源。

| Task | Preferred Tool |
|---|---|
| 检索专利 / 候选规模估算 | `/59100a` `search_patents_v3`, `search_patents_statistics`; fallback `/1458a4` `search_patents` |
| 关键词扩展 | `/33072f` `suggest_keywords` with array parameters; human filtering required |
| 趋势 / 地域 / 字段统计 | `/59100a` `trend`, `search_patents_statistics`, `rec_office`, `get_rec_office_year`; fallback `/33072f` `search_patent_field` |
| 申请人排名 / 申请人趋势 | `/59100a` `applicant_rank`, `applicant_trend`; fallback `/3fd502` `applicant_ranking` |
| 技术构成 / 申请人 x 技术 | `/59100a` `technology_constitute`, `tech_applicant_dist`, `applicant_technology_analysis` |
| 图表洞察 | `/3fd502` `trends`, `technology_effect_distribution`, `most_cited`, `portfolio_value` |
| 核心专利召回 | `/59100a` `refered_rank`, `famn_rank`; verify with `/1458a4` |
| 专利技术挖掘 | `/7cc6ae` `technology_topic`, `application_domain`, `tech_problem_benefit_summary` |
| 著录项目数据 | `/1458a4` `bibliography` |
| 同族数据 | `/1458a4` `family` |
| 前向引用 | `/1458a4` `forward_citation` |
| 权利要求 / 说明书 | `/1458a4` `claims`, `description` |
| 简单法律状态 / 法律事件 | `/1458a4` `get_patent_legal_status`, `legal_data` |
| 复审 / 无效 | `/1458a4` `reexamination_invalidation` |
| 许可 / 转让 / 质押 / 海关 / 获奖数据 | `/1458a4` `license_data`, `transfer_data`, `pledge_data`, `customs_data`, `award_data` |
| PDF / 图片 | `/1458a4` `pdf`, `abstract_image`, `fulltext_image` |

如果这些工具在当前 agent 环境中不可见，说明专利 MCP 不可用；此时只能继续做规划、模板或基于用户提供数据的工作。

## 核心工作流

流水线包含四个编号环节和一个人工交接。环节1建立干净候选池。环节2直接基于检索式产出全景统计和价值点挖掘——不要求先完成标引。环节3推荐标引体系（不是给全量池逐条标引）。全量逐条标引在线下客户 SaaS 工具中完成（人工交接 3.5）。环节4读取回流的标引数据以及环节2统计结果，综合生成 HTML 报告。

```text
Stage 0: startup defaults + required inputs
Stage 1 (环节 1) search-planning step  -> search_config.json + candidate_pool.csv + core_recall.csv
  └─ Checkpoint 1: confirm per-branch queries + precision
Stage 2 (环节 2) statistics step   -> panorama_stats.json + patent_index.core.* + value_signals.json
                                 + chart_data.json + panorama_stats_report.html
  └─ Checkpoint 2: confirm scope before tagging-system design
Stage 3 (环节 3) /pps-tag     -> tech_breakdown.json + key_questions.json + patent_packages.csv
                                 + tagging_demo_sample.csv + to_be_tagged.csv
  └─ Checkpoint 3: confirm tagging system
Handoff 3.5 (环节 3.5)        -> client tags to_be_tagged.csv in SaaS, returns tagged_pool.csv
Stage 4 (环节 4) report-generation step  -> report_manifest.json + report.html
  └─ Checkpoint 4: confirm report
```

各层职责和跨层文件 schema 的唯一事实来源是 `ARCHITECTURE.md`。在层间路由时，通过下面约定文件传递状态，而不是通过对话记忆。每层的第一个动作是读取输入文件；每层的最后一个动作是写出输出文件并汇报状态。

除非用户明确要求只要不含数据的框架，否则不要跳过执行层只草拟叙事报告。

### 子技能路由

| Stage | Sub-skill | Reads | Writes |
|---|---|---|---|
| 环节 1 | `search-planning step` | user intake | `search_config.json`, `candidate_pool.csv`, `core_recall.csv` |
| 环节 2 | `statistics step` | `search_config.json`, `candidate_pool.csv`, `core_recall.csv` | `panorama_stats.json`, `patent_index.core.*`, `value_signals.json`, `chart_data.json`, `panorama_stats_report.html` |
| 环节 3 | `/pps-tag` | `candidate_pool.csv`, `panorama_stats.json`, `value_signals.json` | `tech_breakdown.json`, `key_questions.json`, `patent_packages.csv`, `tagging_demo_sample.csv`, `to_be_tagged.csv` |
| 环节 3.5 | — (client SaaS) | `to_be_tagged.csv` | `tagged_pool.csv` (returned by client) |
| 环节 4 | `report-generation step` | all Stage 2/3 files + `tagged_pool.csv` | `report_manifest.json`, `report.html` |

快速功能验证可以使用固定 fixture，但真实项目必须先通过 Checkpoint 1–3，再进入人工标引交接。

## 检查点与人工交接协议

总控负责流程和停止点。每个检查点说明三件事：向用户展示什么、用户可以选择什么、每个选择会流向哪里。回滚 = 重新运行受影响的层；因为状态保存在文件中，未受影响的下游文件不会丢失。

### Checkpoint 1 — 环节 1（检索建库）之后

- 展示：按四段式 A6 骨架拆解的每个分支检索式 + 每个分支的抽样精度 %。
- 选择：
  - (a) 确认 → 进入环节 2。
  - (b) 编辑某个分支 → 仅为该分支重新运行 search-planning step → 重新抽样 → 回到这里。
  - (c) 重启 → 回到 Stage 0 需求采集。
- 默认：当每个分支精度 ≥ 80% 时，默认选择 (a)，用一句话确认。

### Checkpoint 2 — 环节 2（格局统计）之后

- 展示：趋势 / 申请人 / 竞品头部结论 + 价值点交叉挖掘短名单（高被引 × 大同族 × 法律有效 × 竞品集中）。
- 选择：
  - (a) 确认 → 进入环节 3。
  - (b) 调整范围（收窄分支、替换竞品、改变日期口径）→ 重新运行 statistics step（如果检索式本身变化，也重新运行 search-planning step）→ 回到这里。
- 默认：(a)。

### Checkpoint 3 — 环节 3（标引体系设计）之后

- 展示：四列分解表（≤40 个三级节点，互斥）+ ≥10 个关键技术问题 + ≥10 个专利包 + 20–30 条标引 demo。
- 选择：
  - (a) 确认 → 导出 `to_be_tagged.csv` 并进入 Handoff 3.5。
  - (b) 修改分类体系（合并/拆分节点、收紧描述、重新平衡问题）→ 重新运行 pps-tag → 回到这里。
- 默认：只有在用户审阅分解表后才能确认；不要自动确认分类体系。

### Handoff 3.5 — 人工客户标引（真人工断点）

这是一个真正的人类断点，不是 agent 步骤。Checkpoint 3 之后：

1. 确认 `to_be_tagged.csv` 已导出，并告诉用户行数和客户必须填写的列（根据已确认分解表填写 level-3 tag）。
2. 明确告诉用户：请在智慧芽 SaaS 工具完成全量标引，并将标引结果文件放到约定路径（默认 `tagged_pool.csv`）。
3. 停止。不要编造标引结果。不要基于想象数据进入环节 4。
4. 当用户说标引已完成时，环节 4 首先检查 `tagged_pool.csv` 是否存在且标签列有值。如果缺失或为空，继续停在这里并重新说明交接指引。

### Checkpoint 4 — 环节 4（报告生成）之后

- 展示：报告路径 + 章节列表 + 证据覆盖说明（每个主要发现都有数据 / 代表专利 / 明确假设支撑）。
- 选择：
  - (a) 接受 → 交付。
  - (b) 要求修改（章节、表达、深度）→ 重新运行相关 report-generation step 步骤 → 回到这里。
- 默认：提交给用户确认；不要悄悄视为项目完成。

### Stage 0. 将业务问题转化为可检索结构

在环节 1 之前，将用户请求转化为 3 到 7 个研究问题和第一版可检索结构。除非用户修改，否则使用启动默认值。

典型研究问题：

- 目标技术是在增长还是衰退？
- 哪些玩家投入最多？
- 哪些技术分支正在升温？
- 近期专利中能看到哪些产品场景或技术功效？
- 哪些专利值得人工阅读？
- 数据中呈现出哪些组合缺口或机会区域？

如果领域较宽，提出第一版拆解（子技术、产品类别、部件、应用场景、技术问题/功效、排除区域）。这是环节1的规则设计脚手架，不是最终标引分类体系——最终四列分解表由环节3（pps-tag）产出。

### 每个环节的细节位于对应子技能

总控负责排序、检查点、人工交接、回滚和进度汇报。每个环节的详细做法位于该环节自己的 SKILL.md 中，因此本文件只保留流程地图，不重复（也不偏离）各层逻辑：

| Stage | Where the detail lives |
|---|---|
| 环节 1 检索建库 | built-in search-planning guidance — 字段算符、恒定主题锚点、半自动 IPC、分层 NOT、A6 骨架、精度抽样 |
| 环节 2 格局统计 | built-in statistics guidance — 趋势/申请人/竞品聚合 + 价值点交叉挖掘 |
| 环节 3 标引体系设计 | `pps-tag/SKILL.md` — 四列分解表、关键问题、专利包、标引 demo、待标引导出 |
| 环节 4 报告生成 | built-in report-generation guidance — 演进路线、竞品画像、护城河解读、推荐包叙事、HTML 构建 |

环节 1 和环节 3 共享的方法论见 `references/query-and-taxonomy-methodology.md`。报告结构和场景表达见“参考文件导航”中列出的参考文件。

- 目标技术是在增长还是衰退？
- 哪些玩家投入最多？
- 哪些技术分支正在升温？
- 近期专利中能看到哪些产品场景或技术功效？
- 哪些专利值得人工阅读？
- 数据中呈现出哪些组合缺口或机会区域？

如果领域较宽，提出第一版拆解：

- 子技术和技术分支。
- 产品类别。
- 产品部件。
- 应用场景。
- 技术问题和技术功效。
- 排除区域。

这份第一版拆解不是最终标引。它是环节 1（search-planning step）的规则设计脚手架。

## HTML 报告结构

默认使用 HTML 作为面向客户的报告格式。在 v0 中，默认生成单个自包含 HTML 文件，内嵌 CSS、图表数据、表格和必要脚本。除非用户明确要求外部数据文件，或数据集过大导致单文件不实用，否则不要创建独立 `data/` 文件夹。

推荐 HTML 章节：

| Section | Purpose |
|---|---|
| Hero / cover | 主题、决策目标、日期、数据来源 |
| Executive summary | 3 到 7 条高层发现和建议动作 |
| Scope and method | 范围表、检索策略、计数方法、局限 |
| Landscape dashboard | 趋势、申请人、地域、法律状态、分支分布 |
| Technology map | 分类体系、分支矩阵、技术演进 |
| Deep dives | 问题-方案簇和代表专利 |
| Competitor portraits | 按玩家拆解的策略信号和证据 |
| Patent package | 推荐专利、理由和下一步动作 |
| Legal and asset signals | 法律状态/事件、转让/许可/质押/获奖作为线索 |
| Recommendations | 产品、R&D 和组合规划启示 |
| Appendix | 检索日志、分类定义、数据表、证据登记 |

HTML 要求：

- 从决策导向结论开始，而不是从方法论开始。
- v0 报告保持单文件自包含，便于分享和测试。
- 视觉设计、仪表盘布局、图表块、矩阵、专利卡片和响应式行为遵循 `references/report-visual-style.md`。
- 每个主要发现都配套图表、表格或代表专利证据。
- 使用密集、易读的仪表盘和克制样式；避免营销式布局。
- 使用由分析产物生成的内联静态 SVG/canvas 或嵌入式图表数据。
- 在图表标题或附近说明计数方法和数据截止日。
- 将检索式、字段定义和局限放在靠后位置。
- 将法律/风险内容标为“信号，不是法律意见”。
- 浏览器可用时，在交付前验证 HTML 渲染正确：无空白图表、断裂导航、不可读表格或文字重叠。

Excel 风格附录按每个代表专利/公开一行，包含归一申请人、日期、地域、法律状态、分类标签、技术问题、解决方案、功效、推荐级别和推荐理由。

## 证据规则

使用证据级别：

| Level | Meaning | Acceptable Output |
|---|---|---|
| 环节1 | 直接数据事实 | 数量、排名、趋势、分布 |
| 环节3 | 观察到的模式 | 增长、集中、分散、迁移 |
| 环节4 | 分析推断 | 可能的技术重点或战略含义 |
| L4 | 业务建议 | 建议关注、跟踪、组合或阅读动作 |
| L5 | 法律/风险信号 | 建议进一步法律复核 |

定稿前检查：

- 每个主要结论都有数据或代表专利证据。
- 已说明检索和计数方法。
- 预测写成基于证据的推断，而不是确定性断言。
- 法律/风险表述写成信号。
- 缺失能力标为不可用，而不是默默编造。

## 法律与风险措辞

不要陈述侵权、不侵权、无效、自由实施、SEP 必要性或确定性权利要求范围结论。优先使用“risk signal for further legal review”、“claim scope should be reviewed manually” 或 “input for later FTO/validity review, not a legal conclusion” 等表述。

## 最终输出清单

- 确认项目范围和使用的默认设置。
- 概述实际查询了哪些专利数据，或用户提供了哪些数据。
- 说明不可用工具或跳过的模块。
- 区分事实、推断和建议。
- 对 HTML 交付物，提供生成的 HTML 文件路径，并说明是否做过视觉检查。
- 包含局限和下一步。
- 除非用户要求完整报告，否则回复保持简洁。

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。

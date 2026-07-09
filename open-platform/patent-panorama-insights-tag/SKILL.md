---
name: patent-panorama-insights-tag
description: 用于专利全景项目的环节3。本 Skill 推荐标引体系，包括 4 列技术拆解表（≤40 个三级节点，彼此互斥）、≥10 个关键技术问题、≥10 个推荐专利包（每包≥3 个同族，六项推荐规则），并提供 20–30 条记录的标引示范和待标引导出文件。全量逐条标引在客户 SaaS 标引工具中完成，不在本 Skill 中完成。
---

# patent-panorama-insights-tag — 专利全景标引体系推荐器

> **我是环节 3/4 · 标引体系设计（patent-panorama-insights-tag）**
> 我吃 环节1 候选池 + 环节2 统计/价值信号，产出标引体系 + 小样本示范 + 待标引导出。
> 全量逐条标引不在我这里——导出后交客户 SaaS 工具（环节 3.5 真人工断点）。

## 目标

环节3 将已确认的环节1/环节2候选集转化为**推荐标引体系**和一个已完成标引的示范样本。它不会对全量池逐条标引。

它回答：

- 技术拆解表是什么？严格的 4 列层级（一级 / 二级 / 三级 / 说明），≤40 个三级原子节点，且同一父节点下互斥。
- 每个分支的关键技术问题是什么，即用于启动环节4演进叙事的开放问题？
- 哪些专利族最能代表每个优先子域，为什么推荐它们（六项推荐规则）？
- 标引人员应如何应用该体系？通过 20–30 条记录示范，而不是标完整池。
- 客户 SaaS 工具需要接收什么，才能运行全量逐条标引？

**环节3 不执行全量逐条标引。** 该工作交给客户 SaaS 标引工具。环节3 产出**方案**（拆解表 + 关键问题 + 推荐包）、**示范样本**（20–30 条记录）和**待标引导出文件**；SaaS 工具产出的全量标引索引再回流到环节4。

这不是完整法律审查，也不是代表性专利深度阅读；它是结构化标引体系推荐层。

## 使用时机

只有在以下条件全部就绪后，才使用 `/patent-panorama-insights-tag`：

1. `/patent-panorama-insights-search`（环节1）已产出 `candidate_pool.csv`、`core_recall.csv` 和 **`tech_taxonomy.txt`**。
2. 人工断点（环节 1.5）已完成：客户已按 `tech_taxonomy.txt` 在 SaaS 工具完成全量标引，并将结果回流为 **`tagged_pool.csv`**。
3. `/patent-panorama-insights-stats`（环节2）已产出 `panorama_stats.json` + `value_signals.json`（可与人工标引并行推进，不互相卡）。

> **`tagged_pool.csv` 未就位时不得启动本 skill。** 本层核心工作是在 SaaS 标引结果基础上做 taxonomy 校验、推荐包精选和 demo 示范；没有标引数据就没有实质输入。

## 输入

契约输入（ARCHITECTURE.md 第2节 环节1 → 人工断点 → 环节2 → 环节3）。前三个硬依赖是主线，缺其一无法运行：

| File | Role |
|---|---|
| `tagged_pool.csv` (环节 1.5 人工标引回流) | 【硬依赖】客户 SaaS 全量标引结果，含每件 `pn` + 三级技术分类标签。这是本层校验 taxonomy 覆盖率、精选推荐包的核心数据来源 |
| `tech_taxonomy.txt` (环节1) | 【硬依赖】环节1 产出的层级链文件，SaaS 标引时使用的分类树。环节3 以此为基础校验覆盖率、合并/拆分节点 |
| `panorama_stats.json` (环节2) | 【硬依赖】trend / applicant_rank / technology_constitute / tech_applicant_dist 聚合 → 判断分支粒度 split/merge |
| `value_signals.json` (环节2) | 【硬依赖】价值交叉打分（高被引 × 大同族 × 有效法律 × 竞品集中度）→ 决定哪些环节4子域做推荐包、包里选哪几族 |

可选增强输入（提供则更准，缺失则降级）：

| File | Role |
|---|---|
| `search_config.json` (环节1) | 每个分支的骨架检索式 → 锚定 level-1 / level-2 的 top-down 骨架 |
| `patent_index.core.json` (环节2) | 核心族种子（按 branch_id 分组），补强 `patent_packages.csv` 的召回 |

## 输出【强制产出清单】

| File | Content | 强制性 |
|---|---|---|
| `tech_breakdown.json` | 4-column table (level_1 / level_2 / level_3 / description), ≤40 level-3 nodes, mutually exclusive | 强制 |
| `key_questions.json` | ≥10 key technical questions, branch-balanced | 强制 |
| `patent_packages.csv` | ≥10 sub-domains × ≥3 families each; every family carries a `recommendation_reason` from the six-item rubric | 强制 |
| `tagging_demo_sample.csv` | 20–30 records tagged against the table — demo of how the SaaS tool should apply the taxonomy | 强制 |
| `to_be_tagged.csv` | Full candidate export (record_id + text columns + EMPTY tag columns) handed to client SaaS tool | 强制 |
| `taxonomy_proposal.md` | 人读版理由书：decomposition logic, key-question logic, package selection rule, tag dictionary, review plan | 强制 |
| **`panorama_stats_report.html`** | **格局统计 HTML 报告。写出路径：`@session/pps-output/panorama_stats_report.html`。在所有其他产出就绪后，主动询问用户是否生成 HTML（见 Workflow 末尾步骤）。** | **可选，主动询问** |

所有文件统一写入 `@session/pps-output/`。

## 输出架构

### `tech_breakdown.json`

```text
nodes[]:
  node_id            稳定 id，例如 "1.2.3"
  level_1            一级技术领域（共 4–6 个）
  level_2            子系统 / 能力
  level_3            具体技术——可标引的原子单元
  description        1–2 句：该技术做什么、为什么重要（成员归属规则）
  example_pn         可选，用于锚定该节点的种子公开号
meta:
  level_3_count      必须 ≤ 40
  mutually_exclusive true（在工作流步骤 9 验证）
```

### `key_questions.json`

```text
questions[]:
  question_id
  level_1            该问题所属分支
  question           一个开放技术问题（关键技术问题）
  rationale          为什么它仍开放 / 为什么重要
  seed_node_ids[]    该问题横跨的三级节点
meta:
  total              ≥ 10
  per_branch_balance 各一级分支大致均衡
```

### `patent_packages.csv`

```text
package_id, sub_domain (= a priority level-3 node), family_id, representative_publication,
title, normalized_assignee, recommendation_reason, value_signal, review_status
```

`recommendation_reason` 必须来自六项推荐规则（见方法 B5）：

```text
disruptive_technology | novel_application_scenario | pulls_latent_user_demand |
major_performance_gain | novel_function | novel_interaction_mode
```

此处 `review_status` 是粗粒度置信度/阅读深度标记：`abstract_based`、`claim_assisted`、`needs_review`。

### `tagging_demo_sample.csv` 和 `to_be_tagged.csv`

二者列布局相同。在 `tagging_demo_sample.csv` 中，标签列是**已填写**的示范；在 `to_be_tagged.csv` 中，标签列为**空**，由客户 SaaS 工具填写。

```text
record_id, publication_number, title, abstract, normalized_assignee,
tech_level_1, tech_level_2, tech_level_3,
technical_problem, solution_type, technical_effect,
recommendation_level, evidence_text, review_status
```

## 单值规则（SaaS 工具应遵循的规范）

- 除非用户明确要求多标签分析，否则 `tech_level_2` 和 `tech_level_3` 均为单值。
- `tech_level_3` 必须从所选 `tech_level_2` 下的选项列表中选择。
- 每个三级节点必须与同级节点互斥。
- 如果一条记录存在多个可能标签，选择主标签，并在 evidence/notes 中记录次要标签。
- 不要将环节1的规则命中标签视为最终标签。
- 证据不足时，不要编造技术问题、解决方案、效果或 IPC。

## 工作流

1. 加载 `candidate_pool.csv` + `patent_index.core.json` + `search_config.json` + 环节2 `panorama_stats.json` / `value_signals.json`。保留稳定记录顺序。
2. **自上而下（架构优先）：** 基于系统构成方式起草 level-1 / level-2 骨架，并用 `search_config` 分支锚定。
3. **自下而上（证据驱动）：** 对每个分支的校准样本（**每分支 ≤15–20 条；总 `/7cc6ae` 调用 ≤ branch_count × 20 —— 硬上限**），调用 `/7cc6ae/mcp`（`technology_topic`、`application_domain`、`tech_problem_benefit_summary`）并抽样摘要，以确认、拆分或合并三级节点。**达到上限即停止校准。**
4. 执行粒度规则（方法 B3）：三级总数 ≤40；每个三级节点必须能写成一条清晰分支检索式、能用一句话描述，并与同级节点互斥。写出 `tech_breakdown.json`。
5. 推导 ≥10 个**关键技术问题**，在一级分支间大致均衡分布（方法 B4）。写出 `key_questions.json`。
6. 构建 ≥10 个**推荐包**（每个优先三级子域一个），每包 ≥3 个同族。写出 `patent_packages.csv`。
7. 生成**示范样本**：选择覆盖主要分支的 20–30 条代表性记录并标引。写出 `tagging_demo_sample.csv`。
8. 导出 `to_be_tagged.csv`：完整候选池，填充文本列，标签列留空。**纯文件操作——只用脚本，绝不把行读入上下文。**
9. **验证：** 三级 ≤40 且互斥；推荐包覆盖 ≥10 × ≥3 个同族；关键问题 ≥10 且分支均衡；不编造 IPC / 问题 / 效果。
10. 写出 `taxonomy_proposal.md`。
11. **【主动询问 HTML】** 所有以上产出就绪后，主动向用户询问：

    > 「以上产出文件已全部就绪。是否同时生成格局统计 HTML 报告（`panorama_stats_report.html`）？该报告将整合环节2 的统计图表、竞品画像和核心专利列表，写入 `@session/pps-output/`，可直接分享给客户。」

    - 用户确认 → 生成 HTML，写出 `@session/pps-output/panorama_stats_report.html`，告知路径。
    - 用户跳过 → 记录，提示可随时输入「生成HTML」触发。

## 下一步（环节 3.5 · 真人工断点）

我的产出到 `to_be_tagged.csv` 为止。接下来不在本 skill 内自动完成：

1. **导出 `to_be_tagged.csv` 交客户 SaaS 工具**做全量逐条标引——真人工断点（环节 3.5）。
2. SaaS 标引完成后，把回流结果保存为 **`tagged_pool.csv`**。
3. 拿到 `tagged_pool.csv` 后，进入 **环节 4 · patent-panorama-insights-report**。

## 校准深度

| Depth | Evidence | Used for |
|---|---|---|
| `light` | title + abstract | demo-sample tagging and branch calibration 的默认深度 |
| `standard` | title + abstract + selected claims | 歧义节点、高价值推荐包候选 |
| `deep` | claims + description | 仅用于环节4代表性深度阅读记录 |

**硬上限：每分支校准 ≤15–20 条记录；总 `/7cc6ae` 调用 ≤ branch_count × 20。**

## 质量检查

- `tech_breakdown.json`：三级 ≤40，节点互斥，每个节点有一句话成员归属说明。
- `key_questions.json`：≥10 个问题，分支均衡，每个问题映射到种子节点。
- `patent_packages.csv`：≥10 个子域，每个子域 ≥3 个同族，每个同族都有基于推荐规则的理由 + 价值信号。
- `tagging_demo_sample.csv`：20–30 条记录，所有标签值来自固定列表，并覆盖主要分支。
- `to_be_tagged.csv`：完整候选池，文本列完整，标签列为空。
- 不编造 IPC / 问题 / 方案 / 效果。

## 方法参考

- B1 — 4 列拆解表（三级 ≤40）。
- B2 — 自上而下架构 + 自下而上证据，双轮拆解。
- B3 — 粒度控制。
- B4 — 关键技术问题（≥10，分支均衡）→ 环节4演进种子。
- B5 — 推荐专利包关联和六项推荐规则。

参见 `references/query-and-taxonomy-methodology.md` 和 `references/scenario-patent-package-and-index.md`。

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。

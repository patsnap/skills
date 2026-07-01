---
name: pps-tag
description: |
  Use this skill for 环节1 of a patent panorama project. It builds an expert-grade, field-scoped, anchored and de-noised search configuration, validates per-branch precision by sampling, and exports a clean candidate pool plus per-branch queries — the input contract for 环节2 (pps-stats). Statistics, portraits and core-patent recall live in 环节2.
---

# pps-search — Patent Panorama Search & Query-Construction Layer (环节1)

> **我是环节 1/4 · 检索建库（pps-search）。** 我负责把业务问题翻译成专家级检索式、去噪、定候选池，产出 `search_config.json` + `candidate_pool.csv` + `core_recall.csv` + **`tech_taxonomy.txt`**，交给环节 2（pps-stats）做统计与价值挖掘。

## Purpose

环节1 of the patent panorama pipeline. This skill answers only the **query-quality** questions:

- Is the search query expert-grade — field-scoped operators, a constant topic anchor, semi-automatic IPC, tiered NOT with recorded reasons?
- Which sub-technology branches structure the field, and what is the audited query for each (A6 four-part skeleton)?
- Is the candidate pool clean enough — per-branch sampled precision ≥ 80% — to feed statistics and tagging downstream?

Output is a **validated search configuration + a de-noised candidate pool + per-branch queries + a lightweight core-patent recall list + a tech taxonomy file for SaaS tagging** — the input contract for **环节2 (pps-stats)**.

> **Moved to 环节2 (pps-stats).** Industry stats, assignee landscape, competitor portraits, core-patent verification/tiering, and value-signal cross-mining have moved out of this layer. 环节1 no longer emits a panorama report.

## When To Use

- User invokes `/pps-search` or a patent panorama project begins.
- As the first step in the full pipeline before `/pps-stats` and `/pps-tag`.
- Standalone: when the user only needs an audited, reusable search configuration.

## Defaults

| Dimension | Default |
|---|---|
| Date basis | Publication date (`pbdt`) for market/legal views; earliest priority date (`E_PRIORITY_DATE`) for technology-trend views |
| Technology stats counting | Simple family level |
| Market / legal stats counting | Publication text level |
| Geography | CN, US, EP |
| Time range | `pbdt:[20200101 TO 20261231]` |
| Analysis mode | Competitor vs. Industry (Mode C) |
| Core patent signal | Forward citation × family breadth × active legal status |

---

## Step 0: Initialize

Record all inputs in `run_config.json`.

---

## Step 1: Expert Query Construction

Per Part A and Part D of `references/query-and-taxonomy-methodology.md`.

### 1-1 Keyword layering — strong / weak / short-word
### 1-2 Field-operator assignment (A1)
### 1-3 Constant topic anchor (A2)
### 1-4 Semi-automatic IPC (A4) — DO NOT FABRICATE IPC
### 1-5 Tiered NOT rules (A5) — every rule carries a recorded reason
### 1-6 Confirmation table — A6 four-part skeleton + precision spot-check

---

## Step 2: Branch Query Generation

Fill A6 canonical skeleton per branch. Save to `search_config.json`.

---

## Step 3: Candidate Pool Export

Export `candidate_pool.csv`：`pn, branch_rule_hits` only（族级去重）。

---

## Step 4: Lightweight Core-Patent Recall

Per branch: `refered_rank` + `famn_rank` top 10。Output `core_recall.csv`：`branch_id, patent_id, pn, recall_source, raw_rank`。

---

## Step 5: Tech Taxonomy Export【强制产出】

**`tech_taxonomy.txt` 是环节1的强制产出文件**，在候选池确认后、移交环节2前必须写出。供客户 SaaS 标引工具直接导入。

### 格式规范

**层级型**，每行一个叶节点：

```
>一级\二级\三级
```

规则：
- `>` 后紧跟第一级（Level-1 域名称）
- `\` 后依次为第二级、第三级
- 每行只写一条路径（一个叶节点）
- 每个单元格支持多值（SaaS 工具侧支持）
- **不得添加任何注释、序号、空行分组、标题行或其他额外内容**
- 文件只包含层级链，**纯内容，无任何其他信息**

示例（仅供格式参考）：
```
>静态电压\稳定性
>静态电压\监测方法
>静态电压\PCMLE
>动态响应\瞬态抑制
>动态响应\环路补偿\Type-III补偿
```

写出路径：`@session/pps-output/tech_taxonomy.txt`。写出后提示用户「可直接下载上传至智慧芽标引工具」。

---

## Output Files【强制产出清单】

| File | Written by | Content | 强制性 |
|---|---|---|---|
| `run_config.json` | Step 0 | User inputs, defaults, analysis mode | 强制 |
| `search_config.json` | Step 1–2 | Keyword layers, anchor, IPC, NOT rules, per-branch A6 queries, precision | 强制 |
| `candidate_pool.csv` | Step 3 | `pn, branch_rule_hits` only，族级去重 | 强制 |
| `core_recall.csv` | Step 4 | Per-branch raw recall: `branch_id, patent_id, pn, recall_source, raw_rank`，top ~10/branch | 强制 |
| **`tech_taxonomy.txt`** | **Step 5** | **层级链，每行 `>L1\L2\L3`，纯内容无注释，供 SaaS 标引工具直接导入** | **强制** |
| `report_manifest.json` (partial) | Step 3 | Run metadata，环节2 extends | 强制 |

---

### Contract handoff to 环节2

五件套：`search_config.json` + `candidate_pool.csv` + `core_recall.csv` + `tech_taxonomy.txt` + `report_manifest.json`。

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。

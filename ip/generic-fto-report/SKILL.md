---
name: generic-fto-report
description: |
  Generate general-industry patent FTO reports from a risk-point Word document and user-provided PatSnap search queries. Use when a patent risk analyst provides target product/technology features plus one or more direct search queries, and wants Codex to execute P002 patent searches, obtain claim 1 with P018, run AI07 auxiliary infringement comparison, and output a traceable FTO report.
---

# 通用行业 FTO 报告

## Overview

Use this skill to turn a risk-point Word document and explicit user-entered PatSnap search queries into a traceable FTO report for any industry. The workflow must use real Zhihuiya/PatSnap API results for patent retrieval, claim retrieval, and AI07 auxiliary comparison; do not invent patent data or infringement conclusions.

## Hard API Boundary

All Zhihuiya API calls must be made only by scripts bundled inside this skill. Do not use external MCP servers, other skills, plugins, ad hoc scripts outside this skill, or prior generated scripts to call P070, P002, P018, AI07, or any other Zhihuiya endpoint.

Use only:
- `scripts/run_generic_fto_report.py` for new general-industry reports.
- `scripts/zhihuiya_api.py` when maintaining API helper behavior.
- configuration in `references/zhihuiya_config.json`.

Read `references/api_call_policy.md` before changing any API behavior. For shared installations, `references/zhihuiya_config.json` contains a placeholder API key. Before first use, replace `PUT_YOUR_ZHIHUIYA_API_KEY_HERE` with the user's own Zhihuiya API key.

## Inputs

Preferred input:
- A Word document (`.docx`) containing risk-point description and a technical-feature table.

The technical-feature table should include columns equivalent to:
- `技术特征类型`
- `技术特征描述`
- `技术特征关键词`

Rows whose type contains `重要`, `核心`, `必要`, or `关键` are treated as important features. If the user uses another label, infer importance conservatively from the text and preserve the original label in the trace.

Optional metadata may appear in the Word document as paragraphs or two-column tables:
- `产品名称` / `标的产品`
- `项目名称`
- `行业`
- `分类号` / `IPC`
- `主分类号` / `MIPC`
- `竞争对手` / `竞争对手名称` / `排查对象` / `检索对象`
- `区域` / `国家地区` / `AUTHORITY`
- `法律状态`

The user may also provide the same metadata with command-line parameters. Command-line values override Word metadata, and Word metadata overrides `references/config.json` defaults.

Direct search input is required:
- Before running, ask the user to provide at least one complete PatSnap/P002 search query.
- Pass each user-entered query with `--query "..."`; repeat `--query` for multiple queries.
- For many queries, accept a JSON file through `--queries-json`.
- Do not build, rewrite, broaden, narrow, or append filters to the user's search queries unless the user explicitly asks for that edit.
- Ignore any `检索式` field found inside the Word document for execution unless the user separately provides it as `--query` or `--queries-json`.
- Still parse the Word technical features for report scope and claim comparison.

## Search Query Rules

The user is responsible for the retrieval logic. The skill executes the supplied query text exactly as entered for P002.

Useful filters that users may include in their own query:
- `IPC:(...)`
- `MIPC:(...)`
- `ALL_AN:(TREE@"竞争对手1" OR TREE@"竞争对手2")`
- `SIMPLE_LEGAL_STATUS:(...)`
- `AUTHORITY:(...)`

## Required Workflow

### 1. Parse The Risk-Point Word Document

Extract:
- Product/risk-point technical-solution text.
- Optional metadata fields listed above.
- Technical features with `type_label`, `description`, `keywords`, and `type`.

Recognize table columns dynamically by header text such as `类型`, `描述`, `内容`, `关键词`, and `关键字`. If a table has no usable headers but clearly looks like a feature table, fall back to the first three columns and record the fallback in `fto_structured_data.json`.

### 2. Preserve Feature Keywords For Comparison

Use the technical-feature keywords from the Word document for later claim comparison. These keywords may be expanded with P070 for comparison support unless the user passes `--skip-keyword-expansion`, but expanded keywords must not be used to construct or modify search queries.

### 3. Accept User Search Queries

Require `--query` or `--queries-json`. Store the provided queries in `queries.json` and use them without modification. If no query is provided, stop and ask the user for a PatSnap search query.

### 4. Retrieve Patents With P002

Call Zhihuiya P002 for each query. Combine all returned records into `patent_list.json`, deduplicate by publication number, patent id, application number, or raw row when necessary, and preserve which query matched each patent.

Do not continue to final report generation if all P002 calls fail. If the calls succeed but return zero patents, write a traceable no-hit report or ask whether to broaden the queries.

### 5. Obtain Claim 1 With P018

For each selected candidate patent, call Zhihuiya P018 through the internal script and extract claim 1. Use endpoint `/basic-patent-data/claim-data`; do not use `/basic-patent-data/claims`.

Store:
- `claim1`
- `claim1_source`: `p018_real`, `p018_empty`, or `missing_identifier`
- identifiers used for the request

Patents without real claim 1 may be listed in a blocked appendix, but they must not receive an infringement conclusion.

### 6. Run AI07 Infringement Comparison

For every patent with `claim1_source=p018_real`, call AI07 through the internal script only. The AI07 input must include:
- claim 1 text or a concise excerpt within prompt limits.
- target product technical-feature descriptions.
- a request for literal comparison, equivalent comparison, distinguishing features, risk level, and concise report conclusion.

Treat AI07 as an auxiliary record. The report conclusion must be grounded in P018 claim 1 comparison; if AI07 conflicts with claim-based analysis, preserve AI07 raw output in `fto_structured_data.json` and use the claim-based conclusion.

### 7. Generate The FTO Report

Use `assets/FTO报告模板.docx` as a report-structure reference. Include:
- Cover/title and report date.
- High-related patent list.
- Overall conclusion.
- Analysis purpose, scope, target product/technology, jurisdiction, legal-status assumptions, competitors, and classifications.
- Target technical solution introduction from the input Word document.
- Search strategy, search queries, and result counts.
- Patent screening table.
- Patent-by-patent claim comparison and risk conclusion.
- Blocked-patent appendix for records missing claim 1 or AI07 output.
- Disclaimer that conclusions are based on retrieved data and provided product information.

Use formal analyst-facing style and conclusion-first wording. Do not describe missing claim 1, missing legal status, or missing AI07 output as "no risk".

## Bundled Resources

- `scripts/run_generic_fto_report.py`: preferred self-contained runner for generic FTO parsing, P070, P002, P018 claim-data, AI07 auxiliary calls, HTML report, DOCX report, and trace JSON.
- `scripts/zhihuiya_api.py`: internal API helper for query-api-key/OAuth modes, P070/P002/P018/AI07.
- `scripts/render_report.py`: legacy HTML report renderer.
- `references/api_reference.md`: compact Zhihuiya API contract notes for troubleshooting.
- `references/api_call_policy.md`: hard boundary requiring all Zhihuiya calls to stay inside this skill.
- `references/zhihuiya_config.json`: skill-internal Zhihuiya API key configuration.
- `references/config.json`: generic default business constants such as classifications, target competitors, legal status, authority, paging limits, and candidate limits.
- `references/report_requirements.md`: generic report requirements and input-field guide.
- `assets/FTO报告模板.docx`: report template reference to copy or mirror when producing the final FTO report.

## Command Pattern

Required direct-query mode:

```bash
python scripts/run_generic_fto_report.py --docx "<风险点描述.docx>" --query "TAC_ALL:((...)) AND AUTHORITY:(CN)" --output-dir "<output-dir>" --api-config references/zhihuiya_config.json
```

Multiple user-entered queries:

```bash
python scripts/run_generic_fto_report.py --docx "<风险点描述.docx>" --query "TAC_ALL:((query one))" --query "MIPC:(B60R21/00) AND AUTHORITY:(CN)" --output-dir "<output-dir>"
```

JSON query input:

```bash
python scripts/run_generic_fto_report.py --docx "<风险点描述.docx>" --queries-json "<queries.json>" --output-dir "<output-dir>"
```

Dry-run query recording without calling Zhihuiya APIs:

```bash
python scripts/run_generic_fto_report.py --docx "<风险点描述.docx>" --query "TAC_ALL:((...)) AND AUTHORITY:(CN)" --dry-run-queries --output-dir "<output-dir>"
```

Before delivering the report, inspect the trace outputs and confirm:
- P002 was called for every query in `queries.json`.
- Every patent receiving an infringement conclusion has P018 claim 1 text.
- AI07 was called internally for each patent discussed where P018 claim 1 exists, and raw output is preserved in `fto_structured_data.json`.
- The final report identifies that the queries were manually supplied by the user.

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。

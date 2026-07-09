---
name: generic-fto-report
description: 根据风险点 Word 文档和用户提供的 PatSnap 检索式生成通用行业专利 FTO 报告。适用于专利风险分析师提供目标产品/技术特征及一个或多个直接检索式，并希望 Codex 执行 P002 专利检索、用 P018 获取权利要求 1、运行 AI07 辅助侵权比对，并输出可追溯 FTO 报告的场景。
---

# 通用行业 FTO 报告

## 概述

使用本 Skill 将风险点 Word 文档和用户明确输入的 PatSnap 检索式转化为适用于任意行业的可追溯 FTO 报告。工作流必须使用真实的智慧芽/PatSnap API 结果进行专利检索、权利要求获取和 AI07 辅助比对；不得编造专利数据或侵权结论。

## 严格 API 边界

所有智慧芽 API 调用只能由本 Skill 内置脚本发起。不要使用外部 MCP 服务、其他 Skill、插件、本 Skill 外的临时脚本或之前生成的脚本调用 P070、P002、P018、AI07 或任何其他智慧芽接口。

仅使用：
- `scripts/run_generic_fto_report.py` 用于新的通用行业报告。
- `scripts/zhihuiya_api.py` 用于维护 API 辅助行为。
- `references/zhihuiya_config.json` 中的配置。

修改任何 API 行为前，先读取 `references/api_call_policy.md`。对于共享安装，`references/zhihuiya_config.json` 含占位 API key。首次使用前，将 `PUT_YOUR_ZHIHUIYA_API_KEY_HERE` 替换为用户自己的智慧芽 API key。

## 输入

优先输入：
- 包含风险点描述和技术特征表的 Word 文档（`.docx`）。

技术特征表应包含等价于以下字段的列：
- `技术特征类型`
- `技术特征描述`
- `技术特征关键词`

类型中包含 `重要`、`核心`、`必要` 或 `关键` 的行视为重要特征。如果用户使用其他标签，需根据文本保守推断重要性，并在追踪记录中保留原始标签。

Word 文档中可用段落或两列表格提供可选元数据：
- `产品名称` / `标的产品`
- `项目名称`
- `行业`
- `分类号` / `IPC`
- `主分类号` / `MIPC`
- `竞争对手` / `竞争对手名称` / `排查对象` / `检索对象`
- `区域` / `国家地区` / `AUTHORITY`
- `法律状态`

用户也可以通过命令行参数提供相同元数据。命令行值覆盖 Word 元数据，Word 元数据覆盖 `references/config.json` 默认值。

必须提供直接检索输入：
- 运行前，要求用户提供至少一个完整的 PatSnap/P002 检索式。
- 用 `--query "..."` 传入每条用户输入的检索式；多条检索式可重复使用 `--query`。
- 检索式较多时，接受通过 `--queries-json` 传入 JSON 文件。
- 除非用户明确要求编辑，不要构建、重写、扩展、缩小或给用户检索式追加过滤条件。
- Word 文档内的任何 `检索式` 字段，除非用户另行通过 `--query` 或 `--queries-json` 提供，否则执行时忽略。
- 仍需解析 Word 中的技术特征，用于报告范围和权利要求比对。

## 检索式规则

用户负责检索逻辑。本 Skill 会按输入原文精确执行提供给 P002 的检索文本。

用户可自行在检索式中包含的有用过滤条件：
- `IPC:(...)`
- `MIPC:(...)`
- `ALL_AN:(TREE@"竞争对手1" OR TREE@"竞争对手2")`
- `SIMPLE_LEGAL_STATUS:(...)`
- `AUTHORITY:(...)`

## 必需工作流

### 1. 解析风险点 Word 文档

提取：
- 产品/风险点技术方案文本。
- 上文列出的可选元数据字段。
- 技术特征，包含 `type_label`、`description`、`keywords` 和 `type`。

通过 `类型`、`描述`、`内容`、`关键词`、`关键字` 等表头文本动态识别表格列。如果表格没有可用表头但明显像技术特征表，则回退使用前三列，并在 `fto_structured_data.json` 中记录该回退。

### 2. 保留用于比对的特征关键词

使用 Word 文档中的技术特征关键词进行后续权利要求比对。除非用户传入 `--skip-keyword-expansion`，这些关键词可用 P070 扩展以辅助比对，但扩展关键词不得用于构建或修改检索式。

### 3. 接收用户检索式

要求提供 `--query` 或 `--queries-json`。将提供的检索式保存到 `queries.json`，并不作修改地使用。若未提供检索式，停止并要求用户提供 PatSnap 检索式。

### 4. 用 P002 检索专利

对每条检索式调用智慧芽 P002。将所有返回记录合并到 `patent_list.json`，按公开号、专利 id、申请号或必要时按原始行去重，并保留每件专利匹配到的检索式。

如果所有 P002 调用失败，不要继续生成最终报告。如果调用成功但返回零件专利，写入可追溯的无命中报告，或询问是否扩展检索式。

### 5. 用 P018 获取权利要求 1

对每件入选候选专利，通过内部脚本调用智慧芽 P018 并提取权利要求 1。使用接口 `/basic-patent-data/claim-data`；不要使用 `/basic-patent-data/claims`。

保存：
- `claim1`
- `claim1_source`：`p018_real`、`p018_empty` 或 `missing_identifier`
- 请求所用标识符

没有真实权利要求 1 的专利可列入受阻附录，但不得给出侵权结论。

### 6. 运行 AI07 侵权比对

对每件 `claim1_source=p018_real` 的专利，仅通过内部脚本调用 AI07。AI07 输入必须包含：
- 权利要求 1 文本，或提示长度限制内的简洁摘录。
- 目标产品技术特征描述。
- 对字面比对、等同比对、区别特征、风险等级和简洁报告结论的请求。

将 AI07 视为辅助记录。报告结论必须基于 P018 权利要求 1 比对；如果 AI07 与基于权利要求的分析冲突，应在 `fto_structured_data.json` 中保留 AI07 原始输出，并采用基于权利要求的结论。

### 7. 生成 FTO 报告

以 `assets/FTO报告模板.docx` 作为报告结构参考。包含：
- 封面/标题和报告日期。
- 高相关专利清单。
- 总体结论。
- 分析目的、范围、目标产品/技术、司法辖区、法律状态假设、竞争对手和分类号。
- 来自输入 Word 文档的目标技术方案介绍。
- 检索策略、检索式和结果数量。
- 专利筛选表。
- 逐专利权利要求比对和风险结论。
- 对缺失权利要求 1 或 AI07 输出记录的受阻专利附录。
- 声明结论基于检索数据和提供的产品信息。

使用正式、面向分析师的风格，并采用结论先行表达。不要将缺失权利要求 1、缺失法律状态或缺失 AI07 输出描述为“无风险”。

## 内置资源

- `scripts/run_generic_fto_report.py`：推荐的自包含运行器，用于通用 FTO 解析、P070、P002、P018 claim-data、AI07 辅助调用、HTML 报告、DOCX 报告和追踪 JSON。
- `scripts/zhihuiya_api.py`：内部 API 辅助工具，支持 query-api-key/OAuth 模式及 P070/P002/P018/AI07。
- `scripts/render_report.py`：旧版 HTML 报告渲染器。
- `references/api_reference.md`：用于排障的精简智慧芽 API 合约说明。
- `references/api_call_policy.md`：要求所有智慧芽调用留在本 Skill 内部的严格边界。
- `references/zhihuiya_config.json`：Skill 内部智慧芽 API key 配置。
- `references/config.json`：通用默认业务常量，如分类、目标竞争对手、法律状态、区域、分页限制和候选数量限制。
- `references/report_requirements.md`：通用报告要求和输入字段指南。
- `assets/FTO报告模板.docx`：生成最终 FTO 报告时复制或仿照的报告模板参考。

## 命令模式

必需的直接检索模式：

```bash
python scripts/run_generic_fto_report.py --docx "<风险点描述.docx>" --query "TAC_ALL:((...)) AND AUTHORITY:(CN)" --output-dir "<output-dir>" --api-config references/zhihuiya_config.json
```

多条用户输入检索式：

```bash
python scripts/run_generic_fto_report.py --docx "<风险点描述.docx>" --query "TAC_ALL:((query one))" --query "MIPC:(B60R21/00) AND AUTHORITY:(CN)" --output-dir "<output-dir>"
```

JSON 检索式输入：

```bash
python scripts/run_generic_fto_report.py --docx "<风险点描述.docx>" --queries-json "<queries.json>" --output-dir "<output-dir>"
```

不调用智慧芽 API 的 dry-run 检索式记录：

```bash
python scripts/run_generic_fto_report.py --docx "<风险点描述.docx>" --query "TAC_ALL:((...)) AND AUTHORITY:(CN)" --dry-run-queries --output-dir "<output-dir>"
```

交付报告前，检查追踪输出并确认：
- `queries.json` 中每条检索式都已调用 P002。
- 每件获得侵权结论的专利都有 P018 权利要求 1 文本。
- 对每件被讨论且存在 P018 权利要求 1 的专利，AI07 已在内部调用，且原始输出保存在 `fto_structured_data.json`。
- 最终报告说明检索式由用户手动提供。

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。

---
name: patent-panorama-insights-search
description: 用于专利全景项目的环节1。它构建专家级、限定领域、带主题锚点且去噪的检索配置，通过抽样验证每个分支的精度，并导出干净候选池和各分支检索式——这些是环节2（patent-panorama-insights-stats）的输入契约。统计、画像和核心专利召回属于环节2。
---

# patent-panorama-insights-search — 专利全景检索与检索式构建层（环节1）

> **我是环节 1/4 · 检索建库（patent-panorama-insights-search）。** 我负责把业务问题翻译成专家级检索式、去噪、确定候选池，产出 `search_config.json` + `candidate_pool.csv` + `core_recall.csv` + **`tech_taxonomy.txt`**，交给环节 2（patent-panorama-insights-stats）做统计与价值挖掘。

## 目标

专利全景流水线的环节1。本 Skill 只回答**检索质量**问题：

- 检索式是否达到专家级：限定领域的字段算符、恒定主题锚点、半自动 IPC、分层 NOT 及原因记录？
- 哪些子技术分支构成该领域，每个分支的审计后检索式是什么（A6 四段骨架）？
- 候选池是否足够干净：每分支抽样精度 ≥ 80%，可以交给下游统计和标引？

输出是**已验证的检索配置 + 去噪候选池 + 分支检索式 + 轻量核心专利召回清单 + 供 SaaS 标引的技术分类文件**，作为**环节2（patent-panorama-insights-stats）**的输入契约。

> **已移至环节2（patent-panorama-insights-stats）。** 行业统计、申请人格局、竞品画像、核心专利核查/分级和价值信号交叉挖掘已从本层移出。环节1 不再输出全景报告。

## 使用时机

- 用户调用 `/patent-panorama-insights-search`，或专利全景项目启动。
- 在完整流水线中，作为 `/patent-panorama-insights-stats` 和 `/patent-panorama-insights-tag` 前的第一步。
- 单独使用：用户只需要一套经审计、可复用的检索配置。

## 默认设置

| Dimension | Default |
|---|---|
| Date basis | 市场/法律视角用公开日（`pbdt`）；技术趋势视角用最早优先权日（`E_PRIORITY_DATE`） |
| Technology stats counting | 简单同族层级 |
| Market / legal stats counting | 公开文本层级 |
| Geography | CN, US, EP |
| Time range | `pbdt:[20200101 TO 20261231]` |
| Analysis mode | 竞品 vs. 行业（Mode C） |
| Core patent signal | 前向引用 × 同族广度 × 有效法律状态 |

---

## 步骤 0：初始化

将所有输入记录到 `run_config.json`。

---

## 步骤 1：专家检索式构建

按照 `references/query-and-taxonomy-methodology.md` 的 Part A 和 Part D 执行。

### 1-1 关键词分层 —— 强词 / 弱词 / 短词
### 1-2 字段算符分配（A1）
### 1-3 恒定主题锚点（A2）
### 1-4 半自动 IPC（A4）—— 不得编造 IPC
### 1-5 分层 NOT 规则（A5）—— 每条规则都必须记录原因
### 1-6 确认表 —— A6 四段骨架 + 精度抽查

---

## 步骤 2：分支检索式生成

为每个分支填写 A6 标准骨架，并保存到 `search_config.json`。

---

## 步骤 3：候选池导出

导出 `candidate_pool.csv`：仅包含 `pn, branch_rule_hits`（族级去重）。

---

## 步骤 4：轻量核心专利召回

每个分支取 `refered_rank` + `famn_rank` 前 10。输出 `core_recall.csv`：`branch_id, patent_id, pn, recall_source, raw_rank`。

---

## 步骤 5：技术分类导出【强制产出】

**`tech_taxonomy.txt` 是环节1的强制产出文件**，必须在候选池确认后、移交环节2前写出。供客户 SaaS 标引工具直接导入。

### 格式规范

**层级型**，每行一个叶节点：

```text
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
```text
>静态电压\稳定性
>静态电压\监测方法
>静态电压\PCMLE
>动态响应\瞬态抑制
>动态响应\环路补偿\Type-III补偿
```

写出路径：`@session/pps-output/tech_taxonomy.txt`。写出后提示用户「可直接下载上传至智慧芽标引工具」。

---

## 输出文件【强制产出清单】

| File | Written by | Content | 强制性 |
|---|---|---|---|
| `run_config.json` | Step 0 | 用户输入、默认值、分析模式 | 强制 |
| `search_config.json` | Step 1–2 | 关键词分层、主题锚点、IPC、NOT 规则、分支 A6 检索式、精度 | 强制 |
| `candidate_pool.csv` | Step 3 | 仅 `pn, branch_rule_hits`，族级去重 | 强制 |
| `core_recall.csv` | Step 4 | 每分支原始召回：`branch_id, patent_id, pn, recall_source, raw_rank`，每分支约 top 10 | 强制 |
| **`tech_taxonomy.txt`** | **Step 5** | **层级链，每行 `>L1\L2\L3`，纯内容无注释，供 SaaS 标引工具直接导入** | **强制** |
| `report_manifest.json` (partial) | Step 3 | 运行元数据，环节2继续扩展 | 强制 |

---

### 向环节2交接的契约

五件套：`search_config.json` + `candidate_pool.csv` + `core_recall.csv` + `tech_taxonomy.txt` + `report_manifest.json`。

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。

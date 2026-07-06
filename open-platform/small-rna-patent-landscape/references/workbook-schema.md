# Workbook Schema

Create an XLSX workbook that is suitable both as an analyst working file and as a customer-facing appendix.

## Recommended Sheets

For a full strategy landscape deliverable, prefer these sheets:

1. `策略建议总览`
2. `重点专利证据链`
3. `布局缺口矩阵`
4. `研发启发卡片`
5. `龙头布局借鉴`
6. `专利策略分析总表`
7. `时间轴标签数据`
8. `方法说明`

For a lighter first-pass deliverable, also acceptable:

1. `专利全面分析`
2. `标签汇总`
3. `时间轴数据`
4. `路线图视图`
5. `方法说明`

## Main Sheet Required Columns

Use these columns unless the user specifies a different schema:

| Column | Notes |
|---|---|
| 输入序号 | Preserve the user's list order. |
| 输入专利号 | Original user-provided number. |
| 当前匹配公开号 | Successful fetched publication number, including tried suffix if needed. |
| 标题 | Patent title. |
| 同族专利号 | All family members from patent MCP where available. |
| 当前专利公开日 | Current publication date, preferably YYYYMMDD. |
| 同族专利最早公开日 | Earliest publication date across the family. |
| 同族专利数 | Count of family members. |
| 同族进入国家 | Country/jurisdiction code list and Chinese display list if useful. |
| 该专利申请人 | Normalize to English legal names. |
| 摘要 | Current patent abstract. |
| 权利要求 | Claims content; use English family substitute when current claims are missing. |
| 该专利当前法律状态 | Current legal status from patent MCP. |
| 同族专利法律状态概览 | Summarize active, pending, granted, invalid/expired, and key CN/US/EP/JP status. |
| 专利类型分类 | 序列专利, 平台专利, 测试/诊断方法专利, 用途方法专利, 合成工艺专利, 制剂/给药专利. |
| 客户可读技术方向 | Default dashboard lane. |
| 一级技术标签 | Expert asset/platform subdivision. |
| 作用机制标签 | Multi-tag; semicolon-separated. |
| RNA药物类型 | Single or multi-tag depending on source. |
| 化学修饰/结构标签 | Multi-tag; semicolon-separated. |
| 递送/组织标签 | Multi-tag; semicolon-separated. |
| 疾病/组织领域标签 | Disease or tissue area. |
| 产品化阶段标签 | Portfolio/productization layer. |
| 竞争关注度 | 高, 中高, 中, 低. |
| 竞争关注理由 | Short Chinese rationale. |
| 战略解读 | Chinese explanation for customer-facing hover cards or notes. |
| 重点判断结论 | Explain why the patent is or is not a priority. |
| 权利要求强度 | 强, 中, 弱 based on sequence/compound/use/dose/patient-selection/formulation claims. |
| 权利要求强度依据 | Short Chinese evidence. |
| 同族覆盖强度 | 强, 中, 弱 based on family size and CN/US/EP/JP/WO coverage. |
| 同族覆盖依据 | Short Chinese evidence. |
| 法律状态强度 | 强, 中, 弱 based on grants, pending status, expiry/invalidation signals. |
| 法律状态依据 | Short Chinese evidence. |
| 布局层级_策略 | 核心平台, 核心资产, 外围改良, 产品化延伸, 防御布局, etc. |
| 可绕开难度 | 高, 中, 低. |
| 可绕开难度依据 | Explain whether competitors can avoid the claims via sequence, indication, delivery, formulation, or dosing changes. |
| 对当前项目威胁 | 高, 中高, 中, 低. |
| 项目威胁依据 | Explain risk to R&D freedom or patent layout. |
| 可借鉴点 | What can be learned from this filing. |
| 可突破点 | How a new project may technically break through or differentiate. |
| 建议动作 | Concrete next action for IPR/R&D. |

## Summary Sheets

`标签汇总` should aggregate each tag dimension:

- tag name
- Chinese display name
- patent count
- high-importance count
- average family count
- earliest year
- recent years count
- trend label: `持续增加 / 近期加码`, `近期活跃`, `早期集中 / 近期收缩`, `孤立布局`, or `阶段性布局`

`时间轴数据` should be one row per patent-tag relationship when a field is multi-tagged. Include:

- dimension
- tag
- tag display name
- patent number
- year
- importance
- family count
- countries
- title

## Strategy Sheets

### `策略建议总览`

Use one row per strategy category:

| Column | Notes |
|---|---|
| 策略类型 | 查漏补缺, 研发启发, 布局借鉴. |
| 结论 | Executive-level conclusion. |
| 证据 | Patent/tag evidence supporting the conclusion. |
| 建议动作 | Concrete next action. |
| 优先级 | 高, 中高, 中, 低. |
| 时间窗口 | 立即-3个月, 3-6个月, 持续执行, etc. |

### `重点专利证据链`

Use this sheet to make the analytical process visible. It should answer: “Why is this patent important?”

Required columns:

- 竞争关注度
- 当前匹配公开号
- 标题
- 客户可读技术方向_中文
- 一级技术标签_中文
- 重点判断结论
- 权利要求强度 / 依据
- 同族覆盖强度 / 依据
- 法律状态强度 / 依据
- 布局层级_策略
- 可绕开难度 / 依据
- 对当前项目威胁 / 依据
- 可借鉴点
- 可突破点
- 建议动作

### `布局缺口矩阵`

Use this sheet to support “查漏补缺”.

Rows should cover at least:

- 疾病/适应症
- 作用机制
- 化学修饰
- 递送/组织
- 产品化

Columns:

- 维度
- 已有布局
- 布局强度
- 薄弱点
- 风险
- 建议动作
- 证据

### `研发启发卡片`

Use this sheet to support R&D ideation.

Columns:

- 启发方向
- 证据来源
- 研发假设
- 可验证实验
- 潜在专利主题
- 优先级

### `龙头布局借鉴`

Use this sheet to compare the portfolio with RNA-industry layout playbooks.

Suggested playbooks:

- 核心序列族保护
- 递送/制剂外围保护
- 患者筛选/临床使用壁垒
- 平台机制迁移

Columns:

- 布局打法
- 龙头常见做法
- 当前项目已有情况
- 差距
- 可借鉴动作

## Methodology Sheet

Briefly document:

- data sources and MCP/tooling used
- suffix retry rules
- family/legal availability
- tag taxonomy version/date
- limitations, especially claim substitution and missing legal status

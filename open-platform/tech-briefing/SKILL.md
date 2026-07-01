---
name: tech-briefing
description: |
  给定公司名称和/或技术领域，自动检索智慧芽专利、学术文献、行业新闻，生成面向客户交付的技术简报 HTML 报告。当用户明确要求"技术简报"、"专利简报"、"技术报告"，或同时出现公司名与技术主题的"竞品分析"、"技术动态"、"行业简报"时触发。示例："生成华为和小米5G技术简报"、"帮我做固态电池技术动态报告"、"宁德时代最近半年的专利简报"。闲聊式问"最近汽车行业怎么样"不触发。
---

# 技术简报 Skill

## 用途

根据公司名称和/或技术领域，自动检索智慧芽专利数据库、学术文献、互联网新闻，生成一份综合技术简报 HTML 报告。**交付对象是客户**，数据准确性是硬要求。

## 核心原则（必须遵守）

1. **所有数字必须来自实际检索结果** — 专利总数、子技术分组数、词云频次等，一律从真实数据中动态计算，不手写、不估算、不编造。
2. **所有引用的专利号必须存在于已检索数据集** — 子技术、词云、新闻中的任何 PN 都必须在 `PATENTS` 列表中可查。
3. **不展示无功能 UI** — 无更多数据不显示"查看更多"；展开后无内容不显示展开箭头；`X组技术` 必须等于实际数组长度。
4. **生成前执行校验（见第六步）** — 校验不通过不得进入 HTML 生成。

## 执行流程

### 第一步：解析用户输入

提取：公司列表、技术主题、时间范围、地域、用户指定的新闻链接。详见 [references/parse_rules.md](references/parse_rules.md)。

### 第二步：检索专利（并行）

**构建检索式：**
- 公司名处理：查 [references/company_aliases.json](references/company_aliases.json) → 命中用全称 `ALL_AN:("全称1" OR "全称2")`；未命中用通配符 `ALL_AN:(公司名*)`。**公司名绝不写入 `TA_ALL` 字段**。
- 技术关键词：必须做同义词扩展，见 [references/keyword_expansion.md](references/keyword_expansion.md)。用 `TA_ALL:(kw1 OR kw2 OR ...)`。
- 时间字段：含"申请"用 `APD`，否则用 `PBD`。格式 `PBD:[20251112 TO 20260512]`。

**并行调用：**
- `mcp__zhihuiya__count_patent` 统计各公司专利总量
- `mcp__zhihuiya__search_patent` 检索专利列表（`limit=30`, `sort_field=PBDT_YEARMONTHDAY`, `sort_order=DESC`）

**某公司结果为 0 或 <5 件必须二次检索：** 改用通配符放宽公司名 → 扩展关键词 → 放宽时间。仍为 0 则如实写入报告，不得编造。

### 第三步：获取专利详情

对**所有要进入报告的专利**，分批并行调用 `mcp__zhihuiya__get_patent_detail`：
- `data_types: ["tech_summary"]`（最稳定接口）
- 提取 `patsnap_title`、`tech_problem_summary`、`technical_approach_summary`、`benefit_summary`
- 每批 8 件
- **不允许留空**：若 tech_summary 返回空（新专利），基于标题和摘要手动总结三要素

`bibliography` / `legal_status` 接口可能要求 patent_id 而非 patent_number，失败时直接用 `search_patent` 返回的 title / original_assignee / apdt / pbdt。

### 第四步：检索学术文献

使用 `mcp__zhihuiya__search_literature`：
- 必传 `text` + `type`（推荐 `title/abstract`）
- `limit: 10`
- **关键词优先用英文**；中文无相关结果则换英文
- 相关性判断：与技术主题不相关的文献不入报告；整批不相关则更换关键词重试（最多 2 次）

内容要求：每条文献须附 DOI 链接（`https://doi.org/{doi}`，无则不加链接），并用 1~2 句话总结研究内容。

### 第五步：检索行业新闻

优先 `WebSearch`。在非 US 区域 `WebSearch` 通常无结果，**立即切换**：

```bash
python "<SKILL_DIR>/scripts/sogou_search.py" "{公司名} {技术领域}" 8
```

`<SKILL_DIR>` 为本 Skill 所在目录。脚本输出 JSON 数组，含 `title`/`url`/`desc`，已自动多轮搜索+去重。

若用户指定了网站链接，用 `WebFetch` 抓取。搜狗也无结果则在报告中显示"暂未检索到相关行业新闻"，**不得用专利数据伪装成新闻**。

### 第六步：数据整理与校验

**整理：** 构建扁平 `PATENTS` 列表（每条含 pn/pid/title/assignee/apdt/pbdt/status/problem/approach/effect/company/branch）、`PATENTS_BY_COMPANY` 分组、`SUB_TECHS` 分组（patents 字段是 PN 列表）、`WORD_CLOUD`（count 来自实际统计）。

技术分支分类参考关键词：

| 分支 | 关键词 |
|---|---|
| 材料与化学 | 材料、化学、合成、电解质、电极、催化、薄膜 |
| 结构与封装 | 结构、封装、壳体、密封、组装、模组 |
| 控制与算法 | 控制、算法、检测、识别、优化、调度、预测 |
| 系统与集成 | 系统、集成、架构、平台、接口、通信 |
| 制造与工艺 | 制造、工艺、加工、生产、沉积、刻蚀 |
| 安全与可靠性 | 安全、可靠、防护、预警、故障、寿命 |

**校验（必须执行，不通过不进入第七步）：**

1. **数量一致性** — `count_patent` 总数 = 报告显示总数；子技术 `X组技术` = `len(patents)`；词云 count = 实际统计值。
2. **引用完整性** — `SUB_TECHS[*].patents` 中每个 PN 必须在 `PATENTS` 列表中。
3. **字段完整性** — `PATENTS` 中每条的 `problem` / `approach` / `effect` 非空。
4. **UI 功能性** — 有"查看更多"就必有更多内容；有展开箭头就必有展开内容。
5. **内容相关性** — 文献与技术主题相关；新闻与公司/技术相关。

### 第七步：生成 HTML 报告

**绝不用 Write 直接写 HTML**，一定通过 Python 脚本生成。三文件分离：

```
scripts/v2_css.py              # CSS，Skill 自带，直接使用
scripts/build_report_v2.py     # 主脚本，Skill 自带，直接使用
v2_data.py                     # 本次检索数据，每次在工作目录重新生成
```

**步骤：**

1. 切换到 `~/Documents/tech_briefings/`（不存在则创建）
2. 用 Write 工具在此目录创建 `v2_data.py`（结构见 [scripts/v2_data.sample.py](scripts/v2_data.sample.py)）
3. 运行：
   ```bash
   python "<SKILL_DIR>/scripts/build_report_v2.py"
   ```
   脚本会从当前工作目录加载 `v2_data.py`，从 `<SKILL_DIR>/scripts/` 加载 `v2_css.py`，输出路径会打印到 stdout
4. 在浏览器中打开：
   - Windows: `start "" "<路径>"`
   - macOS: `open "<路径>"`

### 第八步：输出追溯文档

在 HTML 同目录同名输出 `tech_briefing_v2_<时间戳>_trace.md`，记录完整的检索、决策、校验过程。模板见 [references/trace_template.md](references/trace_template.md)。

追溯文档**如实记录**失败与重试，不美化。

## 错误处理

| 场景 | 处理 |
|------|------|
| 工具连续失败 2 次 | 立即换策略，不再重试同样的方法 |
| `get_patent_detail` 部分字段失败 | 用 `search_patent` 返回的基础字段补位，跳过失败字段 |
| `search_literature` 结果不相关 | 换英文关键词重试，最多 2 次 |
| `WebSearch` 无结果 | 切 `sogou_search.py`；仍无则显示"暂未检索到" |
| 某公司检索结果为 0 | 通配符放宽 → 扩展关键词 → 放宽时间 |
| 全是外观设计专利 | 过滤 CN3 开头（中国外观）和 USD 开头（美国外观） |
| 结果与主题不相关 | 收紧关键词，增加 AND 条件 |
| Write 写大 HTML 失败 | 一定走 `build_report_v2.py` 路径，不要直接 Write HTML |

## 样式与交互

- 白底清爽，右侧固定导航面板
- 居中标题 + 时间范围徽章
- 技术趋势：SVG 折线图 + 公司专利数量柱状图
- 技术主题：词云，hover 显示专利数量
- 专利：按公司分组手风琴，蓝色渐变标题栏
- 子技术：可展开显示专利卡片
- 专利公开号点击跳转智慧芽详情页：
  ```
  https://analytics.zhihuiya.com/patent-view/abst?_type=query&source_type=search_result&rows=20&patentId={patent_id}
  ```
- 法律状态：授权=绿、公开/审中=橙、失效=红
- 技术三要素：问题=红、手段=绿、功效=橙
- 响应式：窄屏隐藏导航

## 文件结构

```
tech_briefing/
├── SKILL.md                          # 本文件
├── references/
│   ├── company_aliases.json          # 公司名映射表
│   ├── keyword_expansion.md          # 技术同义词扩展规则
│   ├── parse_rules.md                # 输入解析（时间、地域、语言）
│   └── trace_template.md             # 追溯文档模板
└── scripts/
    ├── v2_css.py                     # 报告 CSS（复用）
    ├── build_report_v2.py            # 主生成脚本（复用）
    ├── v2_data.sample.py             # v2_data.py 结构示例
    └── sogou_search.py               # 搜狗新闻搜索（WebSearch 降级用）
```

**依赖：** Python 3.8+，标准库即可（无需 pip 安装）。智慧芽数据通过 `mcp__zhihuiya__*` 工具访问，不经由本 Skill 管理凭证。

## 常见错误清单

| 错误 | 正确做法 |
|------|----------|
| 子技术显示"3组技术"但只有 2 条专利 | count 必须 = `len(patents)`，脚本已自动 |
| 引用了不存在的专利号 | 所有 PN 必须在 `PATENTS` 中 |
| "查看更多"按钮点击无反应 | 没有更多数据就不要显示按钮 |
| 词云专利数量是编造的 | 必须实际统计 |
| 用 Write 直接写大 HTML 失败 | 走 `build_report_v2.py` |
| 同一工具连续失败多次 | 2 次失败立即换策略 |
| 公司精确匹配为 0 | 立即通配符放宽 |
| 文献与主题无关 | 换英文关键词并过滤 |

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。

---
name: high-value-patent-package
description: 根据用户提供的 PatSnap/智慧芽专利检索式筛选高价值专利包，并生成 HTML 报告（Word 可选）。适用于专利分析师希望按加权指标筛选高价值专利清单的场景：简单同族被引专利数量 30%、简单同族专利数量 30%、核心发明人专利 20%、法律事件历史 20%；输出字段包括公开公告号（链接到智慧芽专利页面）、标题、摘要附图、当前申请(专利权)人、简单法律状态、Patsnap 专利标题、AI 技术三要素和入选理由。
---

# 高价值专利包筛选

## 概述

使用此 skill 将一个专利检索表达式转化为可追溯的高价值专利包筛选报告。工作流必须检索真实专利记录，使用 PatSnap/智慧芽高价值指标进行富集，选择返回结果中排名前 10%-15% 的专利，并生成 HTML 报告。Word 报告为可选项，仅在用户要求时生成。

不要编造专利数据、法律事件、附图、技术总结或评分。如果 API 字段缺失，或调用重试后仍失败，应将该专利保留在追踪文件中，并将字段标记为 `未获取`。

## 输入

- 用户原样提供的一个专利检索式。
- PatSnap/智慧芽 API 访问权限。
- 可选的用户约束，例如司法辖区、申请人范围、最大检索数量或报告语言。如果未提供，则按原检索式执行，并在实际 API 限制内筛选完整返回结果集。

## 必需交付物

生成以下最终成果：

- `高价值专利包筛选报告.html` — 必需。始终生成 HTML 报告。
- 可行时生成追踪文件，例如 `高价值专利包筛选数据.json` 或 `高价值专利包筛选数据.xlsx`，保留原始证据和评分。
- `高价值专利包筛选报告.docx` — 可选。仅当用户明确要求时生成 Word 报告（例如要求 Word/docx 版本）。生成时，Word 报告中的入选专利、评分、理由和数据缺口必须与 HTML 报告一致。

报告必须包括：

- 检索式和检索摘要。
- 检索式返回的候选数量。
- 高价值筛选比例和入选专利数量。
- 基于候选集计算得到的前五名核心发明人。
- 评分标准和权重。
- 包含必需字段的高价值专利清单。
- 每件专利的入选理由。
- 数据缺口和 API 失败情况，如有。

## 必需专利清单字段

每件入选高价值专利必须展示：

- `专利公开公告号`：公开公告号，优先使用 `[P002].pn`。将其渲染为指向智慧芽/PatSnap 数据库中该专利页面的可点击超链接（见下文“公开公告号超链接”）。HTML 报告中使用 `<a target="_blank">` 链接；可选 Word 报告中使用外部超链接。
- `标题`：来自 `[P002]` 的原始专利标题。
- `摘要附图`：`[P021].abstract_drawing.path`；缺失时使用 `无可用摘要附图`。
- `[标]当前申请(专利权)人`：来自 `[P002]` 的当前申请人/专利权人；使用返回的任意当前权利人/申请人等价字段。
- `简单法律状态`：来自 `[P041]` 的简单法律状态。
- `Patsnap专利标题`：`[P025].patsnap_title`。
- `AI技术三要素-技术问题`：来自 `[P025]` 的技术问题。
- `AI技术三要素-技术手段`：来自 `[P025]` 的技术手段/解决方案。
- `AI技术三要素-技术功效`：来自 `[P025]` 的技术效果/收益。
- `被选定为高价值的原因`：基于四项高价值指标给出简洁、证据化的理由。

报告表格或附录中还应包括以下评分/证据字段：

- `高价值评分`
- `简单同族被引专利数量`
- `简单同族专利数量`
- `是否核心发明人专利`
- `法律事件`
- `数据缺口`

## 筛选标准

按 100 分制为每件候选专利评分：

- `简单同族被引专利数量多`：30%。使用 `[P015].patent_cited.cited_by_simple_family`。
- `简单同族专利数量多`：30%。使用 `len([P014].patent_family.simple_family)`。
- `属于核心发明人专利`：20%。核心发明人专利是指发明人列表中包含候选集中按专利数量排名前五的任一发明人的专利。
- `出现过专利法律事件`：20%。合格法律事件包括诉讼、无效/复审、许可和权利转移。使用 `[P034]`、`[P027]`、`[P028]` 和 `[P029]`。

阅读 `references/screening-standard.md` 了解归一化、并列排序和理由措辞。

## 入选数量

高价值专利清单必须包含检索式返回专利的 10%-15%。

默认入选数量：

```text
selected_count = ceil(candidate_count * 0.10)
```

仅在必要时调整：

- 最小值：当检索返回任意候选时，至少选择 1 件专利。
- 最大值：除非用户明确要求更多，否则不得超过 `ceil(candidate_count * 0.15)`。
- 如果大量专利在截断位置评分相同，使用 `references/screening-standard.md` 中的并列排序规则。
- 明确报告最终比例，例如 `本次检索返回 240 件，筛选 30 件，占 12.5%`。

## 工作流

1. 使用 `[P002]` 检索候选专利。
   - 保持用户提供的 `query_text` 不变。
   - 在约定上限内翻页获取所有可用结果。
   - 保留 `patent_id`、`pn`、标题、当前申请人/权利人、发明人、日期、司法辖区和分页元数据。

2. 规范化候选专利。
   - 使用 `patent_id` 作为后续富集的主标识。
   - 按 `patent_id` 和 `pn` 去重。
   - 在追踪文件中为每件入选和未入选候选专利保留 `pn` 和 `patent_id`。

3. 计算核心发明人。
   - 仅按发明人分隔符 `|`、`;`、`；` 和换行拆分 `[P002].inventor`。
   - 不要按 `,` / `，` 拆分。在 PatSnap/智慧芽中，发明人字段格式为 `LASTNAME, FIRSTNAME|LASTNAME, FIRSTNAME`，逗号是单个发明人姓名内部的姓/名分隔符；按逗号拆分会把姓名打碎（例如 `TANNER, CHRISTOPHER RICHARD` 会变成两个错误发明人）。
   - 每件专利中每位发明人只计一次。
   - 按候选集专利数量降序排列发明人。
   - 将前五名发明人视为核心发明人。
   - 同一发明人可能在不同族成员中以不同语言出现（例如 `TANNER, CHRISTOPHER RICHARD` 与 `克里斯托弗·理查德·坦纳`）。不要跨语言合并；按候选集中返回的姓名计数。

4. 富集所有候选专利或有记录的筛选池。
   - `[P014]`：简单同族专利数量。
   - `[P015]`：简单同族被引专利数量。
   - `[P021]`：摘要附图。
   - `[P025]`：Patsnap 标题和 AI 技术三要素。
   - `[P027]`：复审/无效。
   - `[P028]`：许可。
   - `[P029]`：转让/权利转移。
   - `[P034]`：诉讼。
   - `[P041]`：简单法律状态。

5. 评分并排序候选专利。
   - 应用 30/30/20/20 评分模型。
   - 当候选数量至少为 10 件时，对数值指标使用百分位归一化。
   - 对核心发明人和法律事件指标使用二元评分。
   - 按评分降序排序，然后应用并列排序规则。

6. 选择高价值专利。
   - 选择返回候选的 10%-15%。
   - 入选清单必须有证据支撑。不要因为专利“看起来重要”但缺少评分支持而加入。
   - 为每件入选专利写一条简短的 `被选定为高价值的原因`。

7. 生成报告。
   - 始终生成包含可读表格和嵌入/链接摘要附图的 HTML 报告。
   - 将每个公开公告号做成指向智慧芽/PatSnap 专利页面的可点击超链接（见“公开公告号超链接”）。
   - 仅当用户明确要求时生成 Word 报告；生成时，Word 报告应与 HTML 报告保持相同实质内容，包括公开公告号超链接。
   - 包含必需专利清单字段、评分细节、检索摘要、方法论和数据缺口。

## 公开公告号超链接

为每个 `专利公开公告号` 链接到智慧芽/PatSnap 数据库中的专利页面，使读者可以直接跳转到源记录。

使用专利内部 `patent_id`（即 `[P002].patent_id` 返回的同一 id，也是所有富集接口使用的 id）加公开公告号构建 URL：

```text
https://analytics.zhihuiya.com/patent-view/abst?patentId=<patent_id>&q=<pn>
```

规则：

- 使用这个最小形式。不要复制带有 `signature`、`expire` 或 `shareId` 查询参数的分享链接 — 这些是每个链接独有的限时 token，会过期，也不能跨专利复用。最小形式不会过期。
- 在 `q` 参数中对 `pn` 做 URL 编码。
- 访问该链接要求读者登录智慧芽/PatSnap；未登录读者会被重定向到登录页。在报告中说明一次即可。
- 如果用户使用不同的智慧芽/PatSnap 产品线或域名，相应调整 host/path，并保持 `patentId` 作为定位符。
- HTML：`<a href="…" target="_blank" rel="noopener">PN</a>`。Word：公开公告号单元格上的外部超链接关系。
- 在追踪文件中持久化 `patent_id` 和构建出的 `view_url` 以便审计。

## API 参考

在可用时使用以下 PatSnap/智慧芽 API。所有调用均使用：

```text
Authorization: Bearer <ZHIHUIYA_API_KEY>
```

不要将 API key 硬编码到 skill 或输出成果中。

### P002 专利检索

使用 `[P002]` 运行用户提供的检索式并获取候选专利。

```text
POST https://connect.zhihuiya.com/search/patent/query-search-patent/v2
```

重要字段：

- `data.results[].patent_id`
- `data.results[].pn`
- `data.results[].title`
- `data.results[].current_assignee` 或等价的当前申请人/专利权人字段
- `data.results[].inventor`

### P014 专利同族

```text
GET https://connect.zhihuiya.com/basic-patent-data/patent-family?patent_id=<patent_id>&patent_number=<pn>
```

使用 `len(data[].patent_family.simple_family)` 作为 `简单同族专利数量`。在追踪文件中保留 `simple_family_id` 和同族成员。除非用户改变标准，否则不要替代为 INPADOC 或 PatSnap 同族规模。

### P015 前向引用

```text
GET https://connect.zhihuiya.com/basic-patent-data/forward-citation/v3?patent_id=<patent_id>&patent_number=<pn>
```

使用 `data[].patent_cited.cited_by_simple_family` 作为 `简单同族被引专利数量`。返回时，在追踪文件中保留 `cited_by_patents`、`cited_by_inpadoc_family`、`cited_by_patsnap_family`、`cited_by_3y` 和 `cited_by_5y`。

### P021 摘要附图

```text
GET https://connect.zhihuiya.com/basic-patent-data/abstract-image?patent_id=<patent_id_csv>&patent_number=<pn_csv>
```

使用 `data[].abstract_drawing.path` 作为 `摘要附图`。在追踪文件中保留 `abstract_drawing.num`。签名图片 URL 可能过期，因此尽可能记录检索时间。

### P025 AI 技术三要素

```text
GET https://connect.zhihuiya.com/high-value-data/tech-problem-and-benefit-summary?lang=cn&patent_id=<patent_id_csv>&patent_number=<pn_csv>
```

使用：

- `patsnap_title` 作为 `Patsnap专利标题`。
- `tech_problem_summary.tech_problem_para` 作为 `AI技术三要素-技术问题`。
- `technical_approach_summary.technical_approach_para` 作为 `AI技术三要素-技术手段`。
- `benefit_summary.benefit_para` 作为 `AI技术三要素-技术功效`。

### P027 复审和无效

```text
GET https://connect.zhihuiya.com/advanced-patent-data/re-examination-and-invalidation?patent_id=<patent_id>&patent_number=<pn>
```

非空的 `data[].patent_reexam_invalid_data[]` 表示该专利存在合格的无效/复审事件。

### P028 专利许可

```text
GET https://connect.zhihuiya.com/advanced-patent-data/license-data?patent_id=<patent_id>&patent_number=<pn>
```

非空的 `data[].patent_license_data[]` 表示该专利存在合格的许可事件。

### P029 专利转让

```text
GET https://connect.zhihuiya.com/advanced-patent-data/transfer-data?patent_id=<patent_id>&patent_number=<pn>
```

非空的 `data[].patent_transfer_data[]` 表示该专利存在合格的权利转移事件。

### P034 诉讼

```text
GET https://connect.zhihuiya.com/high-value-data/litigation?patent_id=<patent_id_csv>&patent_number=<pn_csv>
```

非空的 `data[].patent_litigation_data[]` 表示该专利存在合格的诉讼事件。

### P041 简单法律状态

```text
GET https://connect.zhihuiya.com/basic-patent-data/simple-legal-status?patent_id=<patent_id>&patent_number=<pn>
```

使用返回的简单法律状态作为 `简单法律状态`。

## 质量规则

- 不要编造数据。将缺失事实标记为 `未获取`。
- 在追踪文件中保留原始 API 证据，以便报告可审计。
- 使每件入选专利的理由具体化，例如 `简单同族被引专利数量位于候选集P92；简单同族专利数量18件；命中核心发明人：张三；存在许可、权利转移事件`。
- 区分高价值筛选信号和法律意见。法律事件是价值信号，不是权利稳定性或可执行性的结论。
- 始终将公开公告号做成指向智慧芽/PatSnap 专利页面的有效超链接；使用不会过期的最小 URL 形式，不使用分享链接。
- 生成 Word 报告时，其入选专利、评分、理由、数据缺口和公开公告号超链接必须与 HTML 报告一致。

## 参考

- `references/screening-standard.md`：评分归一化、筛选比例、并列排序规则、法律事件类别和报告表格 schema。
- `scripts/`：此工作流的可选 Python 参考实现（分阶段 pipeline + `run_all.py`）。参见 `scripts/README.md`。该 skill 与工具无关；脚本是完整示例，不是必需项。

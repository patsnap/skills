# payload JSON Schema（render_report.py 输入约束）

> **本文件作用**：定义 Step 5.2 构造的 `report_payload` JSON 字段约束。本文档以当前生成的 `<PAYLOAD_PATH>` 为 canonical 结构；`scripts/render_report.py` 会先做兼容归一化，再按该结构渲染。任何核心字段缺失或路径错误**不会报错**，但会导致 HTML 中显示"未提及"或空表。

## 顶层结构

```json
{
  "meta": { ... },
  "requirement_text": "...",
  "analysis": { ... },
  "issues": [ ... ],
  "directions": [ ... ],
  "summary": { ... },
  "units": [ ... ],
  "appendix": { "a1": [...], "a2": [...], "a3": [...], "a4": [...] },
  "markdown_report": "..."
}
```

当前生成 payload 包含以上 9 个顶层键。`meta / requirement_text / analysis / issues / directions / summary / units / appendix` 8 个键为结构化渲染必需；`markdown_report` 为正文一致性字段，值为 Step 4 对话内完整 Markdown 报告正文。生成流程应写入 `markdown_report`，存在时 `render_report.py` 以该正文作为 HTML 渲染源，避免 HTML 与对话内原始输出发生字段重组差异。

## 产物关系

```text
problem_text -> 当前对话显示工作流 -> payload JSON -> HTML 报告
```

- 当前对话显示工作流：先输出完整 Markdown 报告正文，方便直接阅读。
- payload JSON：保存结构化分析、证据、统计，以及同一份 `markdown_report` 正文。
- HTML 报告：由 payload 中的 Markdown 正文经 `render_markdown_report(markdown_text)` 渲染，并加上页面样式、目录和页眉页脚。
- Markdown 报告文件：由 payload 中同一份 `markdown_report` 写出，确保与当前对话一致。

## 落盘方式

- 本 schema 只约束 `$PAYLOAD_PATH` 的 JSON 内容；HTML 不应作为 schema 内容写入，也不应通过工具参数分块追加。
- HTML/Markdown 必须由 `scripts/render_report.py --payload "$PAYLOAD_PATH" --output "$HTML_PATH" --markdown-output "$MARKDOWN_PATH"` 从 payload 生成。
- 若运行环境只能通过 `files` 工具写入 payload，必须使用合法 JSON 参数。大 payload 使用 `begin_write -> append -> finish_write`：`append` 只能使用 `begin_write` 返回的 `write_id`，`sequence` 必须递增，`content` 大小不得超过工具返回的硬上限。
- 已存在于持久化 artifact 的内容，应优先通过 `files.materialize` 落盘，避免将大内容重新内联到工具调用参数中。

## meta

| 字段            | 类型         | 说明                                               |
| --------------- | ------------ | -------------------------------------------------- |
| `project_name`  | str          | 项目全称；空字符串则 HTML 头部"项目名称"整行不渲染 |
| `project_short` | str          | 项目简称（可选，HTML 副标题用）                    |
| `applicant`     | str          | 申报单位；空字符串则"申报单位"整行不渲染           |
| `today_iso`     | "YYYY-MM-DD" | 报告生成日期                                       |
| `scope`         | str          | 默认 `"专利+论文+网络学术文献补充"`                |

## analysis（Step 0 三维结构）

```json
{
  "demand": { "scene": "...", "pain": "...", "current": "..." },
  "bottleneck": { "limit": "...", "cost": "...", "principle": "..." },
  "solution": {
    "path": "...",
    "system": "...",
    "compat": "...",
    "target": "..."
  }
}
```

任一字段原文未提及时填 `"未提及"`，不得省略键。

## issues（Step 1 技术难题）

```json
[
  { "no": "T1", "name": "灭弧能力突破", "desc": "..." },
  { "no": "T2", "name": "...", "desc": "..." }
]
```

## directions（Step 1 攻关方向 + Step 3 证据汇总）

```json
[
  {
    "name": "方向名",
    "covers": ["T1", "T2"],
    "problem": "核心问题（不要写成 core_problem）",
    "contents": [
      {"text": "研发内容一", "cites": ["S1", "S2"]}
    ],
    "target": "技术目标",
    "counts": {"case": 1, "paper": 5, "patent": 4, "web": 1},
    "hit_extra": "时间分布/主要申请人 TOP3/核心分支（可选）",
    "evidence": {
      "cases":   [{"no", "src", "year", "publisher", "title", "url", "summary", "grade", "direction"}],
      "papers":  [{"src", "year", "affiliation", "title", "url", "cited_by", "doi", "sid"}],
      "patents": [{"src", "pub_no", "title", "url", "applicant", "pub_year", "status", "cited_by", "sid"}],
      "webs":    [{"site", "title", "url", "summary", "sid", "category"}]
    },
    "summary_focus": "总结表『核心攻关』列",
    "summary_output": "总结表『输出成果』列",
    "summary_sids": ["S1", "S6"]
  }
]
```

**常见字段映射（旧自由命名 → schema 命名）**：

| 旧命名                   | schema 命名                     |
| ------------------------ | ------------------------------- |
| `core_problem`           | `problem`                       |
| `sn` / 裸 `S#`           | `sid`（值仍为 `"S1"`）          |
| `pn`（专利公开号）       | `pub_no`                        |
| `assignee`（专利申请人） | `applicant`                     |
| `year`（专利公开年）     | `pub_year`                      |
| `cited`                  | `cited_by`                      |
| 顶层 `standards`         | `evidence.cases`                |
| 顶层 `papers`            | `evidence.papers`               |
| 顶层 `patents`           | `evidence.patents`              |
| 顶层 `web`               | `evidence.webs`（注意复数 `s`） |

## summary（3.1 检索成果汇总）

```json
{
  "cnt_case":     <int>,
  "cnt_paper":    <int>,
  "cnt_patent":   <int>,
  "cnt_web":      <int>,
  "cnt_org_total":<int>,
  "cnt_org_top5": <int>,
  "top_orgs":     "中文顿号分隔的 2–3 家"
}
```

`cnt_case / cnt_paper / cnt_patent / cnt_web` 必须等于对应 `appendix.a*` 数组长度（去重后），禁止估算。`cnt_org_total` 与 `cnt_org_top5` 一般不相等，不得合并。

## units（第四节科研单位）

```json
[
  {
    "name": "归一化单位名",
    "covers": ["方向①", "方向②"],
    "focus": "技术重点",
    "achievements": "代表成果",
    "cites": ["S1", "S2"]
  }
]
```

## appendix（五、附录）

```json
{
  "a1": [{"no", "src", "year", "publisher", "title", "url", "summary", "grade", "direction"}],
  "a2": [{"src", "year", "affiliation", "title", "url", "cited_by", "doi", "sid", "direction"}],
  "a3": [{"src", "pub_no", "title", "url", "applicant", "pub_year", "status", "cited_by", "sid", "direction"}],
  "a4": [{"site", "title", "url", "summary", "sid", "category"}]
}
```

- `a1/a2/a3` 每条额外带 `direction` 字段（值为对应方向 `name`），脚本据此按路线分组渲染
- `a4` 改用 `category` 字段，取值固定为 `"期刊论文" | "工程案例" | "技术标准"`，与 Step 2b 三条查询串一一对应
- `a1` 的 `no` 是 A1 独立编号（C1/C2…），不参与 `[S#]` 序列，因此 canonical payload 中 `a1` 不设置 `sid`
- 同一条论文、专利或 Web 引用在 `directions[].evidence` 与 `appendix.a2/a3/a4` 中出现时，`sid` 必须保持一致；工程案例/标准使用 `no` 保持一致

## [S#] 编号规则

- 全局唯一，覆盖论文/专利/Web 学术补充三类
- 工程案例/标准（A1）独立编号（C1/C2…），不参与 `[S#]` 序列
- 建议按证据生成顺序全局递增，且可按类型自然分段；当前 canonical payload 示例为论文 `S1–S9`、专利 `S10–S18`、Web `S19–S24`

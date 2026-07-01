---
name: rd-direction-finder
description: |
  给定工程/技术问题描述，按"需求牵引-瓶颈分析-解决思路"三维解析需求，提取互斥技术难题，识别核心攻关方向，并行执行专利、论文及 Web 多平台检索，综合输出不超过 max_directions（默认 10）路结构化研发方向（含核心问题、研发内容、技术目标、代表参考证据），并按固定骨架同步生成 Markdown 检索报告与可渲染 HTML 报告。
---

# rd-direction-finder（科技项目研发方向检索报告生成）

## 触发场景

- 用户输入科研/工程项目问题描述，要求给出研发方向建议
- 用户说"开展哪些方向的研发"、"可以研究哪些技术路线"、"帮我拆解研发方向"
- 用户提供立项背景，希望生成多路研发方向分析

## 不适用场景

- 单一专利/论文精读
- 纯新颖性或 FTO 分析
- 无问题描述的开放式情报查询
- 已有明确方向、只需检索证据支撑的任务

## 输入参数

| 参数             | 说明                           | 默认值 | 是否必须 |
| :--------------- | :----------------------------- | :----: | :------: |
| `problem_text`   | 工程/技术问题描述，100～400 字 |   —    |   必须   |
| `max_directions` | 最多输出几路研发方向           | **10** |   可选   |

## 产物与依赖关系

实际交付顺序固定为：

1. `当前对话显示工作流`：在当前对话中直接输出完整 Markdown 报告正文，方便用户阅读。
2. `Markdown 报告`：保存结构化数据，写入 `<MD_PATH>`。
3. `payload JSON`：保存结构化数据，写入 `<PAYLOAD_PATH>`。
4. `HTML 报告`：由 `scripts/render_report.py` 读取 payload 生成，写入 `<HTML_PATH>`。

依赖关系为：

```text
problem_text -> 当前对话显示工作流 -> payload JSON -> HTML 报告
```

说明：当前对话显示的 Markdown 报告正文必须写入 payload 的 `markdown_report` 字段；HTML 从 payload 中的同一正文渲染，保证对话预览、HTML 页面内容一致。

路径定义见 [assets/paths.md](assets/paths.md)，payload schema 见 [assets/payload-schema.md](assets/payload-schema.md)，报告结构见 [assets/report-template.md](assets/report-template.md)，检索规则见 [assets/workflow.md](assets/workflow.md)。

## 交付硬门禁（前置约束，优先级高于任何步骤指令）

**一次完整运行必须同时满足：**

- 当前对话中已经输出完整 Markdown 报告正文，至少包含"科研需求检索报告"到"附录 A4"的全部章节。
- `<PAYLOAD_PATH>` 存在且 size > 0。
- `<HTML_PATH>` 存在且 size > 0。
- `<MD_PATH>` 存在且 size > 0。
- payload 中 `summary.cnt_case / cnt_paper / cnt_patent / cnt_web` 必须等于 `appendix.a1/a2/a3/a4` 的实际长度。
- 失败时必须说明失败步骤、原因、已尝试修复和可复现命令。
  **字段命名硬约束**（违反任一项不会报错，但会导致 HTML 中相应位置显示"未提及"或空表）：

**写入约束**

- 优先使用本地文件系统或本地脚本写入 payload，再由 `render_report.py` 生成 HTML。
- 禁止把完整 HTML 作为工具参数内联重放或追加写入。
- 若运行环境只能通过 `files` 工具写入 payload，必须使用合法 JSON 参数。大 payload 使用 `begin_write -> append -> finish_write`：`append` 只能使用 `begin_write` 返回的 `write_id`，`sequence` 必须递增，`content` 大小不得超过工具返回的硬上限。
- 已存在于持久化 artifact 的内容，应优先通过 `files.materialize` 落盘，避免将大内容重新内联到工具调用参数中。

## 工作流

本节给出每个步骤的核心动作；判别准则、查询模板与平台对照表见 [assets/workflow.md](assets/workflow.md)，报告骨架与字段约束见 [assets/report-template.md](assets/report-template.md)

### Step 0.0 冻结范围（前置约束）

- 论文：时间默认优先近 3 年、高引用，除非用户另有说明
- 专利：时间默认近 3 年，优先授权专利，全球范围，中国/美国/欧洲/日本/韩国优先，除非用户另有说明

### Step 0 需求解析（三维结构）

按"需求牵引–瓶颈分析–解决思路"三维结构，从 `problem_text` 中提炼关键信息，忠实原文不作主观评判：

- 角色：结构化提炼助手，忠实原文，不作主观评判
- **需求牵引**：场景、痛点、当前应对
- **瓶颈分析**：能力极限+数据、现有措施局限、原理局限
- **解决思路**：技术路径、系统方案、工程兼容性、锁定目标

任一子项原文未提及时，子项标题保留、值写"未提及"，不得捏造。细化判别要点见 [assets/workflow.md](assets/workflow.md) 「Step 0 三维论证细化判别要点」节；输出表格骨架以 [assets/report-template.md](assets/report-template.md) 「一、项目需求解析」为准。

### Step 1 技术难题拆解

从同一份 `problem_text` 中提炼 N 个互斥、边界清晰的技术难题，统一编号 **T1、T2…TN**：

- N 由文本内容决定，不强行凑数、不凭空增加
- 每个难题用一句话概括，并引用原文关键表述作为依据
- 基于全部 N 个难题识别 k 个核心攻关方向（**k = min(N, max_directions)**，可合并高度同类项但不得遗漏任何 T#）
- 在 Step 1 表格后用一行 "> 基于以上…" 列出各攻关方向及其覆盖的难题编号

### Step 2a 专利+论文并行检索

每个攻关方向独立执行：

- `paper.search`：strategy=["semantic","keyword"]，topk=20，sources=["paper"]
- `patent.search`：strategy=["semantic","keyword"]，topk=20，sources=["patent"]

共 k×2 次工具调用，尽量并行发起。

### Step 2b Web 多平台补充检索

与 Step 2a 同步发起，按"期刊论文 / 工程案例 / 技术标准"三类各 1 条 web.search，共 3 条。三条查询串模板与平台域名对照表见 [assets/workflow.md](assets/workflow.md) 「Step 2b 并行检索 — Web 多平台补充」节。

### Step 3 证据筛选与编号

- 每路专利 ≤10 篇，优先授权、近 3 年、相关度高的；每篇标注 [S#] 编号
- 论文：每路 ≤10 篇，优先近 3 年、高引用
- 专利：每路 ≤10 篇
- Web：每条查询保留最相关 ≤4 条，3 条查询合计 ≤10 条，按三类归并并标注平台来源
- **A1 与 A4 边界**：A1 收录权威/具名工程文献与标准条目（独立编号、不带 [S#]）；A4 仅承载 web.search 散落条目（带 [S#]）
- **[S#] 编号**：全局唯一，覆盖论文/专利/Web 学术补充三类；工程案例/标准（A1）独立编号、不参与 [S#] 序列；建议分段（如专利 S1–S10 / 论文 S11–S20 / Web S21–S30）

### Step 4 在对话内完整输出报告正文

#### Step 4.1 输出报告正文

按 [assets/report-template.md](assets/report-template.md) 骨架顺序，将整份 Markdown 报告**直接内联**在最终回复正文里。

**完整输出标准**：

- 报告内容必须忠实反映检索结果，不得编造或主观评判；所有数字必须使用工具返回去重后的真实计数（即附录行数），禁止估算或占位数字；原文未提及的子项填"未提及"，不得捏造；所有单位/机构名做中英文/简称归一，全文同一主体使用同一称谓，首次出现时可在括号内给出原称。
- 每章标题清晰可见，章节内容完整，不得以省略号、"详见文件"、"见附件"等方式截断。
- 头部两个 blockquote（元信息、需求原文）必须最先输出，缺一视为交付失败。
- 不得用"输出清单"、"核心结论速查"、"HTML 已生成"等任何摘要形式替代正文。
- 不得以"已在上方输出"为由在本轮省略任何章节。

**报告必须包含的完整结构**：以 [assets/report-template.md](assets/report-template.md) 为唯一骨架真理源，逐节核对、缺一不可。骨架顺序为：

```
## 顶部元信息块

报告正文必须以二级标题 `## 科研需求检索报告` 开头，紧跟一个 blockquote 作为元信息块；元信息 blockquote 之后再用独立 blockquote 承载"需求输入原文"（详见下一节），随后才进入正文第一节"一、项目需求解析"：
> **科研需求检索报告**
> **项目名称：** {{project_name}}
>
> **申报单位：** {{applicant}} &nbsp;&nbsp;**检索日期：** {{today_iso}} &nbsp;&nbsp;**检索范围：** 专利+论文+网络学术文献补充

---

渲染规则：

- `{{project_name}}` 为空或未识别时，**不输出该整行**（不要写 `项目名称：未提及`，整条删除即可）。
- `{{applicant}}` 为空或未识别时，**不输出该整行**（不要写 `申报单位：未提及`，整条删除即可）。
- `检索日期` 和 `检索范围` 始终显示。
- `{{today_iso}}` 取报告生成当天，格式 `YYYY-MM-DD`。

## 需求输入原文

> **需求输入原文：**
>
> {{requirement_text}}


## 一、项目需求解析

| 维度                           | 关键内容                                                                                                                                              |
| :----------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **需求牵引：问题从哪来**       | **场景**：<具体工程场景> <br> **痛点**：<安全威胁或重大损失> <br> **当前应对**：<临时或权宜措施>                                                      |
| **瓶颈分析：现有方案为何不行** | **瓶颈**：<能力极限+数据> <br> **现有措施局限**：<代价是什么> <br> **原理局限**：<传统技术路线无法突破的本质>                                         |
| **解决思路：本课题如何突破**   | **技术路径**：<核心新思路> <br> **系统方案**：<全链条构想> <br> **工程兼容性**（若有）：<接口/运维兼容性> <br> **锁定目标**：<对应工程痛点的解决方案> |

## 二、技术难题拆解

| 序号 | 技术难题描述                                   |
| :--: | :--------------------------------------------- |
|  T1  | **[难题名称]**：<一句话概括，引用原文关键表述> |
|  T2  | **[难题名称]**：<一句话概括，引用原文关键表述> |
| ...  | ...                                            |

> 基于以上 N 个技术难题，识别 k 个核心技术攻关方向（k = min(N, max_directions)，可合并同类项），驱动 Step 2a、Step 2b 检索：
>
> - **方向①** <名称>（覆盖 T1[+T2]）
> - **方向②** <名称>（覆盖 T3）
> - ...

## 三、主要研究内容和措施

### 3.1 检索成果汇总

**检索成果汇总**：结论前置，一句话总结检索成果。本次技术经检索后发现 {{cnt_case}} 条工程案例/标准、{{cnt_paper}} 篇相似技术论文，{{cnt_patent}} 篇相似技术专利，{{cnt_web}} 条网络学术补充条目，业内主要研究该技术单位 {{cnt_org_total}} 家，其中代表性单位为 {{top_orgs}}。

> 总数为各路线去重合并后的全量计数，必须来自工具返回的真实数字；禁止编造。各路线明细在 3.2 起逐条展开，完整清单见附录 A1/A2/A3/A4，主要科研单位见第四节。
>
> 渲染规则：
>
> - `{{cnt_org_total}}` 是按归一化后单位名去重的全量家数；`{{cnt_org_top5}}` 是第四节实际展示的家数（≤5）。两者一般不相等，禁止合并填同一个数。
> - `{{top_orgs}}` 取第四节"主要科研单位分析"前 2–3 家归一化后的单位名，以中文顿号"、"分隔；不足 2 家时照实列出，0 家时输出"暂未识别明确研究单位"，整段总结仍保留。

每条路线一个小节（3.2 / 3.3 / 3.4 / ...）

### 3.2 研发路线一：{{dir1_name}}

**检索结果**：本路线命中 {{dir1_cnt_case}} 条工程案例/标准、{{dir1_cnt_paper}} 篇论文、{{dir1_cnt_patent}} 篇专利、{{dir1_cnt_web}} 条网络补充、时间分布、主要申请人 TOP3、核心技术分支；若 0 命中：写"未检索到直接相关技术"

**核心问题**：{{dir1_problem}}
**研发内容**（每条至少绑定 1 个 [S#] 证据）：

- {{dir1_content1}} [S#]
- {{dir1_content2}} [S#]
- {{dir1_content3}} [S#]
- {{dir1_content4}} [S#]

**技术目标**：{{dir1_target}}

**代表参考证据（工程案例/标准）**： 表格列：`{{源}} | {{年}} | {{发布机构}} | [{{标题}}]({{url}}) | {{核心内容}} [S#] | {{鉴定等级}}`

**代表参考证据（论文）**：表格列：`{{源}} | {{年}} | {{作者机构}} | [{{标题}}]({{url}}) | 被引 {{n}} | {{DOI}} [S#]`

**代表参考证据（专利）**： 表格列：`{{源}} | {{公开号}} | [{{标题}}]({{url}}) | {{申请人}} | {{公开年}} | {{状态}} | 被引 {{n}} [S#]`

**代表参考证据（Web 学术补充）**： 表格列：`{{源站点}} | [{{标题}}]({{url}}) | {{简述}} [S#]`

> 工程案例/标准/论文/专利/Web 学术补充条目均必须带 [S#]，与附录 A1/A2/A3/A4 一一对应。每路 3–5 条代表证据；完整 ≤10 条清单移至附录。

### 3.(k+1) 研发路线 {{k}}：{{dirk_name}}（格式同 3.2）

（同上结构，按方向数重复）

### 3.(k+2) 研发路线总结

| 路线  | 对应难题 | 核心攻关 | 输出成果 | 代表参考证据 |
| ----- | -------- | -------- | -------- | ------------ |
| 方向① | T1       | …        | …        | [S#]         |
| 方向② | T2       | …        | …        | [S#]         |

## 四、主要科研单位分析

| 单位     | 覆盖路线      | 技术重点 | 代表成果 |
| -------- | ------------- | -------- | -------- |
| {{org1}} | {{dir1_name}} | …        | [S#]     |

## 五、附录

### A1 工程案例 / 标准清单

- 按路线分组，表格列：`{{编号}} | {{源}} | {{年}} | {{发布机构}} | [{{标题}}]({{url}}) | {{核心内容}} [S#] | {{鉴定等级}}`

### A2 论文清单

- 按路线分组，表格列：`{{源}} | {{年}} | {{作者机构}} | [{{标题}}]({{url}}) | 被引 {{n}} | {{DOI}} [S#]`

### A3 专利清单

- 按路线分组，表格列：`{{源}} | {{公开号}} | [{{标题}}]({{url}}） | {{申请人}} | {{公开年}} | {{状态}} | 被引 {{n}} [S#]`

### A4 网络学术清单

- 按"期刊论文 / 工程案例 / 技术标准"三类归并（与 Step 2b 三条查询串对应），表格列：`{{源站点}} | [{{标题}}]({{url}}) | {{简述}} [S#]`

```

**Step 4.1 完成的唯一判定标准**：对话内可见完整 Markdown 报告，包含从"科研需求检索报告"到附录 A4 的全部章节内容。

#### Step 4.2 Markdown 报告正文落地磁盘

在 Step 4.1 完成后的同一轮回复内，将完整的 Markdown 报告正文写入 `$MD_PATH`

```bash
REPORTS_DIR="reports"
DATE=$(date +%Y%m%d)
MD_PATH="@session/reports/rd-direction-finder-report-${DATE}.md"

mkdir -p "$REPORTS_DIR"

# Python 一次性写入（避免 heredoc 占位符问题）
python3 << 'PYEOF'
import os, sys
from pathlib import Path
md_path = Path(os.environ["MD_PATH"])
md_path.parent.mkdir(parents=True, exist_ok=True)
# markdown_text = Step 4 对话中生成的完整报告正文
markdown_text = os.environ.get("_STEP4_MARKDOWN", "") or sys.stdin.read()
if markdown_text:
    md_path.write_text(markdown_text, encoding="utf-8")
    print(f"[ok] markdown -> {md_path} ({md_path.stat().st_size} bytes)")
else:
    print("[warn] stdin empty - Step 5 will auto-rebuild")
PYEOF
```

**Step 4.2 完成的唯一判定标准**：完成后执行最低自检

- `test -s "$MD_PATH"` ：Markdown 报告非空（> 0 bytes）

### Step 5：生成 HTML 报告（默认强制执行）

Step 4.2 完成后，再启动 step5，**同一轮回复内**完成 HTML 报告的落盘；HTML 报告必须包含从"科研需求检索报告"到附录 A4 的全部章节内容，缺一视为交付失败。

**HTML 直接生成**是默认交付产物，**无需用户额外请求**。

#### 5.1 定义路径变量

```bash
#!/bin/bash

# 路径定义（相对当前工作目录）
REPORTS_DIR="reports"
DATE=$(date +%Y%m%d)
PAYLOAD_PATH="@session/reports/rd-direction-finder-payload-${DATE}.json"
HTML_PATH="@session/reports/rd-direction-finder-report-${DATE}.html"

mkdir -p "$REPORTS_DIR"

# 导出到环境，供后续 Python heredoc 读取
export MD_PATH PAYLOAD_PATH HTML_PATH
```

#### 5.2 构造并落盘 payload JSON

**核心原则**：在本地 shell 中运行 Python，将完整的结构化 dict 一次性序列化到磁盘。禁止分块追加。

**数据准备**：Step 0–4 生成的全部结构化数据，通过 shell 环境变量传入 Python。以下变量名与 payload schema 字段一一对应：

| 环境变量           | 对应 payload 字段  | 内容说明                                                                                                                                                                                                                        | 必填 |
| :----------------- | :----------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :--: |
| `META_JSON`        | `meta`             | JSON 字符串：`{"today_iso": "YYYY-MM-DD", "project_name": "...", "applicant": "..."}`                                                                                                                                           |  是  |
| `REQUIREMENT_TEXT` | `requirement_text` | 原始需求文本（纯文本）                                                                                                                                                                                                          |  是  |
| `ANALYSIS_JSON`    | `analysis`         | JSON 字符串：`{"demand": {"scene": "...", "pain": "...", "current": "..."}, "bottleneck": {"limit": "...", "cost": "...", "principle": "..."}, "solution": {"path": "...", "system": "...", "compat": "...", "target": "..."}}` |  是  |
| `ISSUES_JSON`      | `issues`           | JSON 字符串：`[{"no": "T1", "name": "...", "desc": "..."}]`                                                                                                                                                                     |  是  |
| `DIRECTIONS_JSON`  | `directions`       | JSON 字符串（含 evidence），见下表                                                                                                                                                                                              |  是  |
| `SUMMARY_JSON`     | `summary`          | JSON 字符串：`{"cnt_case": N, "cnt_paper": N, "cnt_patent": N, "cnt_web": N, "cnt_org_total": N, "cnt_org_top5": N, "top_orgs": "..."}`                                                                                         |  是  |
| `UNITS_JSON`       | `units`            | JSON 字符串：`[{"name": "...", "covers": ["..."], "focus": "...", "achievements": "...", "cites": ["S#"]}]`                                                                                                                     |  是  |

`DIRECTIONS_JSON` 中每个方向对象的必填结构：

```json
{
  "name": "方向名称",
  "covers": ["T1"],
  "problem": "核心问题描述",
  "contents": [{ "text": "研发内容", "cites": ["S1"] }],
  "target": "技术目标",
  "counts": { "case": 1, "paper": 2, "patent": 1, "web": 0 },
  "evidence": {
    "cases": [
      {
        "no": "C1",
        "src": "...",
        "year": "...",
        "publisher": "...",
        "title": "...",
        "url": "...",
        "summary": "...",
        "grade": "...",
        "sid": "S1"
      }
    ],
    "papers": [
      {
        "src": "...",
        "year": "...",
        "affiliation": "...",
        "title": "...",
        "url": "...",
        "cited_by": "N",
        "doi": "...",
        "sid": "S2"
      }
    ],
    "patents": [
      {
        "src": "...",
        "pub_no": "...",
        "title": "...",
        "url": "...",
        "applicant": "...",
        "pub_year": "...",
        "status": "...",
        "cited_by": "N",
        "sid": "S3"
      }
    ],
    "webs": [
      {
        "site": "...",
        "title": "...",
        "url": "...",
        "summary": "...",
        "sid": "S4",
        "category": "期刊论文"
      }
    ]
  },
  "summary_focus": "总结表核心攻关列",
  "summary_output": "总结表输出成果列",
  "summary_sids": ["S1", "S2"]
}
```

**markdown_report 处理（关键）**：

`markdown_report` 字段**不能**通过环境变量传输（多行文本含特殊字符会导致截断或转义失败）。采用以下流程：

1. Python payload 脚本从该文件读取内容

**完整执行脚本**：

```bash
# ========== 第1步：设置结构化数据环境变量 ==========
export META_JSON='{"today_iso": "'$(date +%Y-%m-d)'", "project_name": "...", "applicant": "..."}'
export REQUIREMENT_TEXT='...'
export ANALYSIS_JSON='...'
export ISSUES_JSON='...'
export DIRECTIONS_JSON='...'
export SUMMARY_JSON='...'
export UNITS_JSON='...'

# ========== 第2步：执行 Python payload 构建 ==========
python3 << 'PYEOF'
import json, os
from pathlib import Path

# 从环境变量读取结构化数据
meta = json.loads(os.environ.get("META_JSON", "{}"))
meta.setdefault("source", "rd-direction-finder")

requirement_text = os.environ.get("REQUIREMENT_TEXT", "")
analysis = json.loads(os.environ.get("ANALYSIS_JSON", "{}"))
issues = json.loads(os.environ.get("ISSUES_JSON", "[]"))
directions = json.loads(os.environ.get("DIRECTIONS_JSON", "[]"))
summary = json.loads(os.environ.get("SUMMARY_JSON", "{}"))
units = json.loads(os.environ.get("UNITS_JSON", "[]"))


# 优先从 $MD_PATH 文件读取 Step 4 已写入的 Markdown 报告
md_path = Path(os.environ["MD_PATH"])
if md_path.exists() and md_path.stat().st_size > 0:
    markdown_report = md_path.read_text(encoding="utf-8")
    print(f"[ok] markdown loaded from {md_path}: {len(markdown_report)} chars")
else:
    # 若 Step 4 未写入，自动从结构化数据重建 Markdown 报告
    # 并同步写入 $MD_PATH，保证 HTML/Markdown/Payload 三一致
    import sys
    sys.path.insert(0, "scripts")
    from render_report import build_markdown_report
    payload_stub = {
        "meta": meta,
        "requirement_text": requirement_text,
        "analysis": analysis,
        "issues": issues,
        "directions": directions,
        "summary": summary,
        "units": units,
    }
    markdown_report = build_markdown_report(payload_stub)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(markdown_report, encoding="utf-8")
    print(f"[ok] markdown auto-rebuilt: {len(markdown_report)} chars -> {md_path}")


# 从 directions evidence 自动构建 appendix
a1, a2, a3, a4 = [], [], [], []
case_no = 1
for d in directions:
    ev = d.get("evidence", {})
    dir_name = d.get("name", "")
    for item in ev.get("cases", []):
        row = dict(item)
        row.setdefault("no", f"C{case_no}")
        row["direction"] = dir_name
        a1.append(row)
        case_no += 1
    for item in ev.get("papers", []):
        row = dict(item)
        row["direction"] = dir_name
        a2.append(row)
    for item in ev.get("patents", []):
        row = dict(item)
        row["direction"] = dir_name
        a3.append(row)
    for item in ev.get("webs", []):
        row = dict(item)
        row.setdefault("category", "期刊论文")
        a4.append(row)

appendix = {"a1": a1, "a2": a2, "a3": a3, "a4": a4}

# 自动修正 summary 计数（以 appendix 实际长度为准）
summary["cnt_case"] = len(a1)
summary["cnt_paper"] = len(a2)
summary["cnt_patent"] = len(a3)
summary["cnt_web"] = len(a4)
if "cnt_org_total" not in summary:
    summary["cnt_org_total"] = len(units)
if "cnt_org_top5" not in summary:
    summary["cnt_org_top5"] = min(5, len(units))
if "top_orgs" not in summary:
    names = [u.get("name", "") for u in units[:3] if u.get("name")]
    summary["top_orgs"] = "、".join(names) if names else "暂未识别明确研究单位"

# 组装 payload
payload = {
    "meta": meta,
    "requirement_text": requirement_text,
    "analysis": analysis,
    "issues": issues,
    "directions": directions,
    "summary": summary,
    "units": units,
    "appendix": appendix,
    "markdown_report": markdown_report
}

output = Path(os.environ["PAYLOAD_PATH"])
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(
    json.dumps(payload, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

# 验证 markdown_report 非空
if not markdown_report.strip():
    print("[warn] markdown_report is empty — HTML will be built from structured data only")
    print("[warn] to guarantee consistency with dialog output, ensure .report.md is written correctly")
else:
    print(f"[ok] markdown_report loaded: {len(markdown_report)} chars")

print(f"[ok] payload written -> {output.resolve()} ({output.stat().st_size} bytes)")
PYEOF
```

**关键要求**：

- 每个环境变量必须在执行前通过 `export VAR='value'` 设置完成。
- `markdown_report` **严禁通过环境变量传输**（多行文本含特殊字符会导致截断）。Python 脚本优先从 `$MD_PATH` 文件读取；若 Step 4 未写入该文件，则自动从结构化数据重建并写入。
- `$MD_PATH` 必须包含 Step 4 在对话中输出的**完整** Markdown 报告正文（从 `## 科研需求检索报告` 到附录 A4）。这是保证 HTML 与对话内容一致的唯一方式。
- `DIRECTIONS_JSON` 中的 `evidence` 字段必须完整包含每路方向筛选后的代表证据（cases/papers/patents/webs）。
- 脚本会自动从 `directions[].evidence` 构建 `appendix`，并自动修正 `summary` 中的计数字段，确保 `cnt_*` 始终等于对应附录数组长度。

#### 5.3 调用渲染脚本

**复用 Step 5.1 已定义的 $HTML_PATH**
使用 `scripts/render_report.py` 渲染报告，写入 `HTML_PATH`

预期 stdout 包含两行 `[ok]`：

```
[ok] report written -> <HTML_PATH> (... bytes)
```

#### 5.4 验证产物

```bash
[ -s "$PAYLOAD_PATH" ] && [ -s "$HTML_PATH" ] && [ -s "$MD_PATH" ] && echo "OK: all files ready" || echo "FAIL: missing or empty files"
```

输出 `FAIL` 视为交付失败，按"异常处理"章节处置。

## 质量规则

| 规则编号 | 约束内容                                                                                                                                                                                                                                                                                                 |
| :------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|    Q1    | 报告头部必须包含两个前置模块（缺一视为交付不合格）：①元信息 blockquote 块、②需求原文 blockquote 块；两者均置于 Step 0 三维表和所有正文章节之前。具体字段、渲染规则与"未识别整行删除"逻辑以 [assets/report-template.md](assets/report-template.md) 「顶部元信息块」「需求输入原文」两节为准，本表不重复。 |
|    Q2    | Step 1 表格必须紧接 Step 0，先于研发路线输出                                                                                                                                                                                                                                                             |
|    Q3    | 技术难题编号统一使用 T1、T2…TN；攻关方向统一使用方向①②③…；[S#] 全局唯一                                                                                                                                                                                                                                  |
|    Q4    | 攻关方向数量 k = min(N, max_directions)，可合并同类项但不得遗漏任何难题                                                                                                                                                                                                                                  |
|    Q5    | 每路研发内容不少于 3 条，且每条至少关联 1 个 [S#] 证据                                                                                                                                                                                                                                                   |
|    Q6    | 总结表必须包含"对应难题"列，明确标注每路方向覆盖的 T# 编号                                                                                                                                                                                                                                               |
|    Q7    | 附录 A4 网络学术清单必须标注来源平台（取值范围以 [assets/workflow.md](assets/workflow.md) 平台域名对照表为准，未列入对照表的来源标"其他"）；条数与归并规则见 Step 3                                                                                                                                      |
|    Q8    | 未有证据支撑的结论标注 Unverified                                                                                                                                                                                                                                                                        |
|    Q9    | 检索数量统计必须使用工具返回去重后的真实计数（即附录行数）；禁止编造或主观估算。若工具未返回可信计数，相应单元格写"未提及"，不得用占位数字凑数                                                                                                                                                           |
|   Q10    | 原文未提及的子项填"未提及"，不得捏造；忠实原文不添加主观评价                                                                                                                                                                                                                                             |
|   Q11    | 所有单位/机构名做中英文/简称归一，全文同一主体使用同一称谓；首次出现时可在括号内给出原称                                                                                                                                                                                                                 |

## 异常处理

| 情形                            | 处理方式                                                               |
| :------------------------------ | :--------------------------------------------------------------------- |
| 某路专利/论文检索无结果         | 注明"当前数据库未检索到直接相关专利/论文，建议参考相邻领域证据"        |
| Web 平台无结果或拒绝访问        | 见 Step 3 末条（附录 A4 注明"[平台名] 本次未返回可用结果"）            |
| 问题描述过短（<50 字）          | 提示用户补充更多背景信息后重试                                         |
| 难题数 N 与 max_directions 关系 | 见 Q4（按 k = min(N, max_directions) 处理，可合并同类项但不得遗漏 T#） |
| HTML 生成失败                   | 在回复中说明失败原因；Markdown 正文仍须完整输出；提供用户可复现命令    |

## 工具绑定

检索工具：

- **优先使用智慧芽 MCP**：首选 `mcp__patsnap_search__.patsnap_search`，按每个攻关方向分别检索 `sources=["paper"]` 和 `sources=["patent"]`，或在需要混合召回时使用 `sources=["all"]`。
- 专利深检可补充使用智慧芽专利 MCP：`mcp__patent_search__.search_patents_nested`、`mcp__core_patents__.search_patents` 或同类 patent MCP。
- 智慧芽 MCP 未暴露、调用失败或结果不足时，再使用 Web 检索替代，并优先选择论文页、专利页、标准页、机构页等可追溯来源。
- Web 补充仍按"期刊论文 / 工程案例 / 技术标准"三类检索，查询模板见 [assets/workflow.md](assets/workflow.md)。

生成工具：

- 本地文件系统或脚本写入 payload JSON。
- `python3 scripts/render_report.py --payload "$PAYLOAD_PATH" --output "$HTML_PATH"` 生成 HTML 文件。

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。

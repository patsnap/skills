# Legacy pharmaceutical intelligence module contracts

Use this file for detailed tool parameters, fallback conditions, and historical JSON examples.

## Contents

- Intake and date-window rules
- Patent, paper, trial, result, deal, and news modules
- Insight and action contracts
- Renderer workflow and legacy quality checklist

---
name: pharma-intelligence-brief
description: 创新药物研发情报简报技能：面向药企研发人员，按靶点/适应症/药物类型/企业类型等条件检索专利、文献、临床试验、BD交易、新闻，生成可折叠HTML情报报告，可选AI竞争洞察。
version: 2.4.0
---

# pharma-intelligence-brief · 创新药物研发情报简报

## 技能定位

面向药企研发人员，基于用户输入的筛选条件，跨六类信息源自动检索并汇总指定时间窗口内的最新医药研发动态，最终输出结构化情报简报（HTML 优先）。

---

## 触发条件

用户发起以下任意意图时激活本技能：
- "帮我生成一份 EGFR 靶点的本周情报"
- "查一下最近一个月 ADC 药物的临床进展"
- "生成 Biotech 公司 KRAS 靶点的季度报告"
- "过去 30 天 PD-1/PD-L1 相关的 BD 交易和新闻"

---

## 第一步：信息收集（Intake）

### 1.1 必收参数

| 参数 | 说明 | 示例 |
|---|---|---|
| `time_window` | 时间窗口：日/周/月/季度，或自定义 YYYY-MM-DD ~ YYYY-MM-DD | `月` / `2025-01-01~2025-03-31` |
| `targets` | 靶点列表 | `EGFR`, `KRAS`, `PD-1` |
| `diseases` | 适应症列表 | `非小细胞肺癌`, `乳腺癌` |
| `drug_types` | 药物类型列表 | `小分子`, `单抗`, `ADC` |
| `org_types` | 企业类型 | `Biotech`, `MNC` |
| `org_names` | 特定企业名称列表 | `阿斯利康`, `恒瑞医药` |

### 1.2 时间窗口严格解析规则 ⚠️

**此规则优先级最高，任何检索步骤均须遵守：**

| 用户表达 | 解析方式 |
|---|---|
| 本月 / this month | 当月1日 ~ 当月最后一天 |
| 本周 / this week | 本周一 ~ 本周日 |
| 本季度 | 当季首日 ~ 当季末日 |
| 近N天/周/月 | 今日往前推N个单位 |
| 自定义区间 | 严格使用用户给出的起止日期 |

**硬性约束**：
1. 每个工具调用必须显式传入与用户指定窗口完全一致的时间参数
2. **严禁**自行将"本月"解释为"近6月"、"近1年"等宽泛范围
3. 若某工具不支持时间过滤，在报告中显式标注"该模块未做时间过滤"
4. **时间范围只可缩小（加严），不可放宽**

### 1.3 可选参数

| 参数 | 说明 |
|---|---|
| `user_company` | 用户所在企业（触发 AI 洞察模块 + 行动清单） |
| `output_format` | 输出格式：HTML（默认）/ Markdown |
| `modules` | 信息模块勾选（默认全部） |

---

## 第二步：六类信息源检索

所有检索结果必须来自真实工具调用，**严禁捏造任何数据**。
**所有工具调用必须严格使用第一步解析的时间窗口，不得擅自扩展。**

### 2.1 专利检索 ⚠️ 工具优先级强制规定

#### 🔴 工具调用顺序（不可更改）

**第一优先：`mcp_pharma_intelligence__ls_patent_search`（即 ls_patent_search）**

> 这是专利模块的**唯一首选工具**，每次执行必须优先调用，不得跳过、不得替换。

必须显式传入的参数：

```
target:                 靶点名称列表（从用户输入解析，如 ["KRAS G12V"]）
publication_date_from:  时间窗口起始日 YYYY-MM-DD（必填，不得省略）
publication_date_to:    时间窗口结束日 YYYY-MM-DD（必填，不得省略）
limit:                  20
```

可选强化参数（建议传入以提升精度）：

```
patent_core_type: ["product_compound", "sequence"]  ← 优先化合物/序列类
```

**第二优先（fallback）：`mcp_patent-search__patsnap_search`**

> 仅在以下条件**同时满足**时才调用：
> 1. `ls_patent_search` 返回结果 **< 5 篇**
> 2. 已确认 `ls_patent_search` 的时间参数传入正确

fallback 调用时必须加时间过滤：

```
filters.date_from: YYYYMMDD
filters.date_to:   YYYYMMDD
filters.date_type: publication
keywords: ["靶点名", "突变位点", "inhibitor"]
```

#### 🚫 专利检索禁止事项

- **禁止**跳过 `ls_patent_search` 直接调用 `patsnap_search`
- **禁止**省略 `publication_date_from` / `publication_date_to` 参数
- **禁止**将时间参数设为比用户指定窗口更宽的范围
- **禁止**展示公开日超出用户指定时间窗口的专利

#### 展示规则

- 检索结果 > 10 篇时优先展示化合物/序列类型，其余按公开日倒序补足至 10 篇
- 同一发明的 WO/US/EP/CN 同族专利只展示一条（优先保留 US 或 WO）

#### 专利 JSON schema（写入 `data["patents"]` 前必须通过校验）

每条记录必须满足以下结构，任一字段缺失时用 `"[待补充]"` 占位，**严禁留空**：

```json
{
  "pn": "专利号（非空）",
  "title": "专利标题（非空）",
  "assignee": "申请人（非空）",
  "pub_date": "公开日 YYYY-MM-DD（非空）",
  "type_tag": "化合物|序列|晶型|医药用途|组合物|制剂|制备方法|合成工艺（非空）",
  "legal_status": "法律状态（非空）",
  "summary": "技术解读摘要100-150字（必填，严禁为空字符串）",
  "url": "来源链接（无则填空字符串）",
  "molecules": []
}
```

### 2.1.1 申请人强制回填步骤 ⚠️

专利搜索完成、写入 JSON 之前，必须执行以下回填逻辑：

```
FOR 每条专利记录:
  IF assignee 为空 / null / "[待补充]":
    → 将该专利的 patent_id 或 pn 加入待回填列表
  END IF
END FOR

IF 待回填列表非空:
  → 批量调用 patsnap_fetch（最多20条/批）
  → 从全文著录项（Applicant/Assignee字段）中提取申请人
  → 回填到对应记录的 assignee 字段
  → 回填后仍为空 → 填 "[待查]"
  ✗ 严禁直接填 "[待补充]" 后跳过
END IF
```

**约束**：写入 `data["patents"]` 时，assignee 为 `"[待补充]"` 或空字符串的条目数必须为零。

### 2.2 文献检索

- **工具**：`mcp_pharma_intelligence__ls_paper_search` + `mcp_pharma_intelligence__ls_paper_vector_search`
- **时间字段**：`year_from` / `year_to` 必须与用户指定窗口一致
- 展示最多 10 篇，按发表日期倒序
- 每篇包含：标题、期刊、发表日期、核心发现摘要（50-80 字）、链接

#### 文献 JSON schema

```json
{
  "title": "标题",
  "journal": "期刊",
  "pub_date": "YYYY-MM-DD",
  "summary": "核心发现50-80字",
  "doi": "DOI（无则空字符串）",
  "url": "链接（无则空字符串）"
}
```

### 2.3 临床试验注册 ⚠️ 两步检索（方案A，必须严格执行）

#### Step A-1：批量搜索

- **工具**：`mcp_pharma_intelligence__ls_clinical_trial_search`
- **时间字段**：`start_date` 范围参数，格式为毫秒时间戳 `{from: 毫秒时间戳起始, to: 毫秒时间戳结束}`，必须与用户指定窗口一致
- 检索上限：`limit: 10`，按试验开始日期倒序
- 本步骤只用于获取 `clinical_trial_id` 列表，**不得直接写入报告**

#### Step A-2：逐条拉取详情（补全 register_number）⚠️ 必须执行

- **工具**：`mcp_pharma_intelligence__ls_clinical_trial_fetch`
- **输入**：Step A-1 返回的全部 `clinical_trial_id`（最多10条）组成列表，一次批量传入 `trial_ids` 参数
- **目的**：从详情字段中提取 `register_number`（NCT号）、`sponsor`（申办方）、`start_date`、`phase`、`disease` 等完整字段
- **兜底规则**：若某条详情中 `register_number` 仍为空，填写 `"[待查]"`，**不得省略该条记录**

#### 临床注册 JSON schema（必须包含 register_number）

```json
{
  "register_number": "NCT号（从详情接口获取；无则填'[待查]'）",
  "title": "试验标题",
  "phase": "分期",
  "disease": "适应症",
  "sponsor": "申办方",
  "status": "招募状态",
  "start_date": "YYYY-MM-DD"
}
```

### 2.4 临床结果披露

- **工具**：`mcp_pharma_intelligence__ls_clinical_trial_result_search`
- **时间字段**：`published_date_from` / `published_date_to` 必须与用户指定窗口一致
- 展示最多 10 条，按发布日期倒序

#### 临床结果 JSON schema

```json
{
  "title": "研究名称",
  "drug": "药物",
  "phase": "分期",
  "endpoint_summary": "主要终点结论",
  "evaluation": "阳性|阴性|中性",
  "pub_date": "YYYY-MM-DD"
}
```

### 2.5 BD 交易

- **工具**：`mcp_pharma_intelligence__ls_drug_deal_search`
- **时间字段**：`deal_date_from` / `deal_date_to` 必须与用户指定窗口一致
- 展示最多 10 条，按交易日期倒序

#### BD 交易 JSON schema

```json
{
  "title": "交易标题",
  "deal_type": "交易类型",
  "licensor": "转让方",
  "licensee": "受让方",
  "deal_date": "YYYY-MM-DD",
  "amount": "金额（未披露则填'未披露'）",
  "url": "来源链接（无则空字符串）"
}
```

### 2.6 重要新闻 ⚠️ 工具优先级强制规定（v2.4.0修订）

#### 🔴 工具调用顺序（不可更改）

**第一优先：`mcp_zhihuiya-172627__bio_search_news`（关键词结构化检索）**

> 这是新闻模块的**唯一首选工具**，每次执行必须优先调用，不得跳过、不得替换。

必须显式传入的参数：

```
keyword:   {"condition": "OR", "value": ["siRNA", "antisense oligonucleotide", "RNAi", ...]}
           （根据用户输入的靶点/药物类型/适应症动态构造关键词列表）
post_time: {"from": 毫秒时间戳起始, "to": 毫秒时间戳结束}
           （必填，严格对应用户指定时间窗口）
limit:     20
sort:      [{"sort_field": "post_time", "sort_order": "desc"}]
```

**第二优先（fallback）：`mcp_pharma_intelligence__ls_news_vector_search`（语义向量检索）**

> 仅在以下条件**同时满足**时才调用：
> 1. `bio_search_news` 返回结果 **= 0 条**
> 2. 已确认 `bio_search_news` 的时间参数和关键词传入正确

#### 🚫 新闻检索禁止事项

- **禁止**跳过 `bio_search_news` 直接调用 `ls_news_vector_search`
- **禁止**省略 `post_time` 的 from/to 时间范围参数
- **禁止** `ls_news_vector_search` 作为主力工具单独使用（它不支持时间范围过滤，覆盖率不完整）

#### 新闻筛选与去重规则

- 从检索结果中优先保留与主题强相关的新闻（标题/内容含靶点名、药物名、适应症关键词）
- 剔除纯财报、会议通知、无关行业新闻
- 展示最多 10 条，按发布日期倒序

#### 新闻 JSON schema

```json
{
  "title": "标题",
  "source": "来源",
  "pub_date": "YYYY-MM-DD",
  "summary": "核心内容50字",
  "importance": "重磅|重要|关注|背景",
  "url": "链接（无则空字符串）"
}
```

---

## 第三步：AI 竞争洞察（条件触发）

**触发条件**：`user_company` 非空。

洞察内容写入 `data["insight"]` 和 `data["action_checklist"]`：

```json
{
  "insight": {
    "items": [
      {
        "level": "高|中|低",
        "dimension": "技术竞争|专利风险|临床竞赛|市场机会|BD机会",
        "text": "洞察内容（基于本期检索事实，严禁虚构）"
      }
    ]
  },
  "action_checklist": [
    {
      "priority": "高|中|低",
      "action": "行动描述（≤40字）",
      "dimension": "技术竞争|专利风险|临床竞赛|市场机会|BD机会",
      "reason": "理由（基于本期检索事实，≤80字，严禁虚构）",
      "deadline": "2周内|本季度末"
    }
  ]
}
```

**约束**：高优先级至少1条，中优先级至少2条，低优先级至少1条；每条必须有本期检索数据支撑。

---

## 第四步：报告生成 ⚠️ 核心约束

### 🚫 禁止事项（最高优先级）

> **AI 严禁直接拼接或输出任何 HTML 字符串。**
> **所有报告输出必须通过调用 `scripts/generate_report.py` 脚本完成。**
> **任何情况下（包括 Python 执行超时、审批等待）均不得绕过脚本生成 HTML。**

### 4.1 执行流程（固定，不可跳过任何步骤）

**Step 1**：将所有检索结果组装为标准 JSON 对象 `data`，结构如下：

```json
{
  "meta": {
    "title": "报告主标题",
    "time_window": "时间窗口描述",
    "targets": ["靶点列表"],
    "diseases": ["适应症列表"],
    "user_company": "用户企业",
    "drug_types": ["药物类型"],
    "org_types": ["企业类型"],
    "report_type": "月度简报"
  },
  "summary": {
    "stats": {"专利": "N篇", "文献": "N篇", "临床注册": "N条", "BD交易": "N条", "新闻": "N条"},
    "top_findings": [
      {"priority": "高|中|低", "text": "关键发现描述"}
    ]
  },
  "patents": [...],
  "patents_total": 0,
  "patent_date_range": "2026-04-01 ~ 2026-04-30",
  "papers": [...],
  "trials": [...],
  "results": [...],
  "deals": [...],
  "news": [...],
  "insight": {...},
  "action_checklist": [...],
  "sources": ["来源说明列表"]
}
```

**Step 2**：将 `data` 写入 JSON 文件（如 `@session/data/brief_data.json`）

**Step 3**：调用 Python 脚本执行渲染：

```python
import json, subprocess, sys
# 脚本路径固定为 @skill/scripts/generate_report.py
# 输入：JSON 文件路径
# 输出：HTML 文件写入 EUREKA_PYTHON_OUTPUT_DIR
```

**Step 4**：若 Python 执行审批超时，**等待用户重新审批，不得降级为直接写 HTML**。提示用户点击审批按钮后重试。

### 4.2 数据完整性自检清单（组装 JSON 前必须逐项确认）

在将数据写入 JSON 之前，AI 必须在内部逐项核查以下清单，**全部通过后才能执行 Step 2**：

```
□ meta.time_window 已填写，且与用户指定窗口一致
□ 专利检索：已优先调用 ls_patent_search（mcp_pharma_intelligence__ls_patent_search）
□ 专利检索：publication_date_from / publication_date_to 已显式传入且在时间窗口内
□ 专利检索：展示的每条专利 pub_date 均在用户指定时间窗口内
□ 专利检索：data["patents"]中 assignee 为 "[待补充]" 或空字符串的条目数为零（若非零，必须先执行 2.1.1 回填步骤）
□ 文献检索调用时 year_from / year_to 已显式传入
□ 临床注册检索 Step A-1：start_date 时间范围已显式传入（from/to 均为毫秒时间戳）
□ 临床注册检索 Step A-2：已调用 ls_clinical_trial_fetch 补全 register_number
□ 临床注册每条记录的 register_number 字段非空（无则填"[待查]"）
□ 临床结果检索调用时 published_date_from / published_date_to 已显式传入
□ BD 交易检索调用时 deal_date_from / deal_date_to 已显式传入
□ 新闻检索：已优先调用 bio_search_news（mcp_zhihuiya-172627__bio_search_news）
□ 新闻检索：post_time 的 from/to 时间范围已显式传入
□ data["news"] 列表非空（若 bio_search_news 返回0条，才触发 ls_news_vector_search 兜底）
□ data["patents"] 每条记录的 summary 字段非空（否则填"[待补充]"）
□ data["summary"]["top_findings"] 至少有3条
□ 若 user_company 非空，data["action_checklist"] 至少有4条
```

### 4.3 文件命名

| 场景 | 文件名 |
|---|---|
| HTML 报告（默认） | `pharma_intel_brief_YYYYMMDD.html` |
| Markdown 报告 | `pharma_intel_brief_YYYYMMDD.md` |

---

## 质量护栏

1. **零捏造**：所有数据必须来自工具调用返回值
2. **时间窗口严格**：所有工具调用必须显式传入时间参数
3. **专利工具优先级**：必须首先调用 `ls_patent_search`（`mcp_pharma_intelligence__ls_patent_search`），fallback 条件严格限定
4. **脚本强制**：HTML 输出必须通过 `generate_report.py` 生成，AI 不得直接写 HTML
5. **模块不跳过**：数据为空时显示"暂无数据"，不得静默省略整个模块
6. **新闻首选关键词检索**：必须首先调用 `bio_search_news`（`mcp_zhihuiya-172627__bio_search_news`）并传入 `post_time` 时间范围；仅当其返回0条时，才触发 `ls_news_vector_search` 语义兜底——严禁反向操作
7. **专利申请人强制回填**：写入 JSON 前必须执行 2.1.1 回填步骤，确保所有专利 assignee 字段非空且非"[待补充]"
8. **专利技术解读必填**：每篇专利 `summary` 字段必须为 100-150 字，缺失时填"[待补充]"
9. **链接真实**：只展示工具返回的真实 URL，不构造假链接
10. **行动清单数据支撑**：每条行动必须有本期检索数据支撑，严禁凭空生成
11. **临床注册登记号完整**：临床注册模块必须执行两步检索（Step A-1 搜索 + Step A-2 详情拉取），确保每条记录包含 `register_number`

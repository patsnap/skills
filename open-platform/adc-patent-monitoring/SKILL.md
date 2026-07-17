---
name: adc-patent-monitoring
description: "监控ADC新申请、专利族、法律状态和竞争风险。适用于：按周或按月监控ADC相关新申请、专利族扩展、法律状态、申请人变化和潜在风险，用于专利组合维护与竞争预警。"
---

# ADC 专利情报周报生成器

用于生成某一自然周的 ADC 专利情报周报。常见输入包括"跑 2026 年第 22 周 ADC 专利周报""生成 Week18 ADC 周报""跑 2026-04-20 到 2026-04-26 ADC 周报"等。

## 前置依赖

使用本 skill 前，接收方必须确认以下环境已就绪：

| 依赖项 | 说明 | 配置位置 |
|---|---|---|
| **Eureka Desktop** | 本 skill 仅支持 Eureka Desktop 原生工作流，不支持命令行独立运行 | — |
| **MCP 服务器：`patsnap-patent-brief`** | 所有专利数据采集工具均来自此服务器，必须安装并启用 | Eureka Desktop → 设置 → MCP 服务器 |
| **智慧芽账号 / API 访问权限** | `patsnap-patent-brief` 服务器需要有效的智慧芽 API 凭证 | MCP 服务器配置中填写 Bearer Token |
| **Python 3.10+** | 渲染脚本 `build_adc_report.py` 仅使用标准库，无需安装第三方依赖 | Eureka Desktop 托管 Python 即可 |

> ⚠️ 若 `patsnap-patent-brief` 未安装或凭证无效，所有 MCP 工具调用将失败，周报无法生成。

## 架构说明

**v6.8 起改为 Eureka Desktop 原生工作流，数据采集环节完全由 Eureka Desktop 对话层完成：**

- Eureka Desktop 直接调用已注册的 `mcp_patsnap-patent-brief__*` 系列工具，无需 Token 硬编码，无需运行独立采集脚本。
- 原 `scripts/collect_adc_week_mcp.py` 已归档备份为 `scripts/_deprecated_collect_adc_week_mcp.py`，仅作历史参考，不再执行。
- 数据采集完成后，Eureka Desktop 将最终专利数据写入本地 JSON 文件，再调用 `scripts/build_adc_report.py` 渲染 HTML。
- `scripts/build_adc_report.py` 接口不变，完全兼容，仅使用 Python 标准库。

## 固定原则

- 最终 HTML 必须由 `scripts/build_adc_report.py` 渲染 `references/adc_report_template_v4.1.html`，不得手写一次性 HTML。
- 周报只描述本周公开数据，不输出"本周首次出现的申请人""格局变化"等需要跨周历史基线才能成立的判断。
- 检索字段必须使用 `F_PBD`，不再使用旧版 `PBD`，不再执行旧检索式二次兜底。
- 专利详情链接固定为 `https://analytics.zhihuiya.com/patent-view/abst?patentId={patent_id}`。
- "专利关联管线"和"研发阶段"本轮只预留字段；没有确定管线关联时填 `—`，不得臆测。
- AI 解读必须基于 PatSnap/Eureka 工具返回的结构化字段、本周最终专利集、P025/tech_summary、claims、bibliography、family/legal_status、必要图像证据改写，不得凭空补外部事实。
- 禁止使用 web search、新闻搜索或开放网页结果生成 `核心保护点`、`创新/新颖性`、`竞争意义`。

## 执行流程

**数据采集由 Eureka Desktop 对话层完成，Eureka 直接调用已注册的 patsnap-patent-brief MCP 工具，无需运行任何采集脚本。**

```text
用户指定自然周
  -> 计算 DATE_FROM / DATE_TO / WEEK_LABEL / DATE_RANGE
  -> Step 0: 连通性自检（mcp_patsnap-patent-brief__search_patents, query_text="ADC", limit=1）
  -> Step 1: 固定检索式分页检索 WO 专利（mcp_patsnap-patent-brief__search_patents，分页取全）
  -> Step 2: 每条专利调 bibliography + abstract_translated 补齐著录、摘要、申请人、优先权
  -> Step 3: Pass-1 粗过滤（ADC 信号关键词）
  -> Step 4: 每条候选调 tech_summary（lang=cn）+ Pass-2 精过滤
  -> Step 5: 最终专利集全量调 claims 结构增强
  -> Step 6: 图像门禁 → abstract_image → intelligent_image（按条件触发）
  -> Step 7: 全量结构增强后计算 Top5，Top5 调 family + legal_status
  -> Step 8: Eureka Desktop 将最终专利数据组装为 JSON 并写入本地文件
             （路径约定见"渲染脚本约定"章节）
  -> Step 9: skills.run_script build_adc_report.py 渲染 HTML
  -> Step 10: 执行强制门禁和数据一致性断言
```

## Eureka Desktop 工具映射

以下工具名按 Eureka Desktop 已注册工具适配；若实际工具名略有差异，以同等功能工具替代，但功能和取证顺序不得改变。

| 数据需求 | Eureka Desktop 工具 | 关键参数 | 备注 |
|---|---|---|---|
| 检索式专利检索 | `mcp_patsnap-patent-brief__search_patents` | `query_text`, `offset`, `limit` | 主检索链路，必须分页取全 |
| 专利著录和摘要 | `mcp_patsnap-patent-brief__bibliography` | `patent_id` 或 `patent_number` | 必须补齐 abstract、applicant、priority_claims、publication_date |
| 中文标题/摘要 | `mcp_patsnap-patent-brief__abstract_translated` | `patent_id`, `lang="cn"` | 可用时调用 |
| P025 三要素 | `mcp_patsnap-patent-brief__tech_summary` | `patent_id` 或 `patent_number`, `lang="cn"` | 生成洞察的主要证据 |
| 权利要求 | `mcp_patsnap-patent-brief__claims` | `patent_id` 或 `patent_number`, `replace_by_related=0` | 最终专利集全量必调 |
| 说明书 | `mcp_patsnap-patent-brief__description` | `patent_id` 或 `patent_number`, `replace_by_related=0` | claims + P025 不足时再调 |
| 专利家族 | `mcp_patsnap-patent-brief__family` | `patent_id` 或 `patent_number` | Top5 必调 |
| 简单法律状态 | `mcp_patsnap-patent-brief__legal_status` | `patent_id` 或 `patent_number` | Top5 必调 |
| 摘要附图 | `mcp_patsnap-patent-brief__abstract_image` | `patent_id` 或 `patent_number` | 图像门禁触发时必调 |
| 智能附图 | `mcp_patsnap-patent-brief__intelligent_image` | `patent_id` 或 `patent_number`, `lang="cn"` | abstract_image 空或不足时调用 |

不得用语义检索、网页搜索或其他开放网络结果替代本周主检索链路。

## 固定检索式

以下 `query_text` 为字面常量，除 `{DATE_FROM}` / `{DATE_TO}` 外不要改动：

```text
(TAC_ALL:("antibody-drug conjugate" OR "ADC" OR "immunoconjugate" OR "antibody conjugate" OR "抗体药物偶联物" OR "抗体偶联物") OR IPC:(A61K47/68*)) AND AUTHORITY:WO AND F_PBD:[{DATE_FROM} TO {DATE_TO}]
```

分页规则：
- 第一页 `offset=0, limit=20`，记录返回的 `total_search_result_count` 为 `TOTAL_RAW`。
- 按 `offset=0,20,40...` 取完全部结果，不能只取前 20 条。
- 以 `pn` 为唯一键去重。
- 若任何结果 `authority != "WO"` 或 `pn` 非 `WO` 开头，立即中止。

## 强制执行层

以下规则是硬性流程，不满足时必须暂停并说明原因，不能生成"看起来完整但证据不足"的报告。

1. 连通性：先用 `query_text="ADC", offset=0, limit=1` 做最小检索，确认服务可用。
2. 主检索：必须使用固定检索式和 `F_PBD`，并分页取全。`TOTAL_RAW` 必须来自检索接口返回总数。
3. 著录补齐：进入候选池的每条专利必须补齐 `patent_id`、`pn`、`title`、`abstract`、`assignee`、`publication_date`、`priority_claims`。
4. P025/tech_summary：进入最终候选池的专利必须尽量获取 P025 三要素。若当前 PN 返回空，对 A3/A8/A9 等更正文献尝试 A1/A2 原始公开文本；只有回退失败才允许标记缺失。
5. 全量结构取证：进入最终专利集的每条专利都必须调用 `claims`，用于抽取靶点、payload、linker、偶联方式、DAR/m/n/p 值、用途和权利要求边界；不得只对 Top 专利认真抽字段。
6. 图像门禁：若文字证据不能明确 payload、linker、偶联方式或 DAR/m/n/p，且 claims 出现结构式/图式信号，必须调用 `abstract_image`；摘要图为空或不足时调用 `intelligent_image`。
7. Top 深度取证：Top5 必须在全量 claims 结构增强和必要图像门禁后计算。Top5 必须调用 `family`、`legal_status`；若 claims 缺失且专利仍是重点，补调 `description`。
8. 失败处理：若检索、著录、P025/tech_summary、claims 或模板渲染任一关键步骤失败，必须明确说明失败环节和影响，不得隐瞒。
9. 缓存优先：同一 PN 已有成功获取的 claims/family/legal_status/image 证据时，重跑优先复用缓存，避免同一周重复调用导致漂移。

## 字段映射

每条专利至少写入：

```json
{
  "patent_id": "",
  "pn": "",
  "title": "",
  "title_zh": "",
  "abstract": "",
  "abstract_zh": "",
  "publication_date": "YYYY-MM-DD",
  "priority_claims": [{"country": "CN/US/EP/GB/...", "date": "YYYY-MM-DD"}],
  "assignee": "",
  "assignee_short": "",
  "assignee_region": "",
  "patent_type": "",
  "target": "",
  "payload_type": "",
  "linker": "",
  "conjugation": "",
  "dar": "",
  "pipeline_asset": "—",
  "dev_stage": "",
  "table_note": "",
  "ai_title": "",
  "tech_solution": "",
  "p025_problem": "",
  "benefit": "",
  "ai_interpretation": {
    "core_protection": "",
    "innovation": "",
    "competition": ""
  },
  "priority_score": 0,
  "priority_tier": "S/A/B/C",
  "_claim_independent_count": 0,
  "_claims_raw_present": false,
  "_image_required_reason": "",
  "_image_evidence_status": "",
  "family_summary": "",
  "legal_status_summary": "",
  "fto_risk_level": "high/medium/low",
  "fto_risk_reason": ""
}
```

P025/tech_summary 映射：

```python
p["ai_title"] = tech_summary.patsnap_title
p["tech_solution"] = tech_summary.technical_approach_summary.technical_approach_para[0]
p["p025_problem"] = tech_summary.tech_problem_summary.tech_problem_para[0]
p["benefit"] = tech_summary.benefit_summary.benefit_para[0]
```

## 专家归纳标签规则

表格字段和深度解读必须使用专家归纳后的情报标签，不得把原始候选词堆叠输出。

- `payload_type`：优先输出机制大类。`Exatecan`、`DXd`、`SN-38`、`喜树碱`、`拓扑异构酶I抑制剂` 统一归纳为 `Topo I抑制剂`；`MMAE/MMAF/auristatin` 归纳为 `auristatin类` 或 `MMAE/MMAF auristatin类`；不得输出搬运式串联。
- `linker`：优先抽取 claims 中 `优选地`、`更优选地` 后的具体 linker。出现 `Val-Cit` 或 `Val-Ala` 时输出 `Val-Cit/Val-Ala`；只有没有具体优选结构时才输出上位标签。
- `conjugation`：优先输出偶联化学或位点机制，例如 `半胱氨酸巯基-硫醚偶联`、`maleimide-硫醚偶联`、`赖氨酸偶联`、`糖基定点偶联`。
- `DAR`：作为汇总表独立字段，置于 `偶联方式` 后。优先抽取 `平均DAR`、`药物抗体比`、`约`、`优选` 等附近数值；未披露时写 `未披露`。
- `DAR` 与通式变量必须区分：若原文明确 `m/n/p 表示偶联于 Ab 的接头-药物或 L-D 单元平均数`，必须抽取为平均偶联数。
- `target`：使用专业可读标签，例如 `EGFR/B7-H3`、`EGFR/c-Met`、`Nectin-4`。
- 如果 claims 中只有图式占位而 payload/linker 文字不完整，必须调用图像工具。

## 图像门禁确定性规则

任一条件满足即调用 `abstract_image`；若摘要图为空或不能支持判断，再调用 `intelligent_image`：

- `payload_type`、`linker`、`conjugation`、`DAR/m/n/p` 任一字段仍为弱值（`未明确`、`未披露`、`式I Linker-Drug`、`Linker-Drug单元`、`细胞毒载荷` 等）。
- claims 出现 `结构式`、`结构如图`、`如下式`、`式I`、`式II`、`通式为`、`img-id`、`L-D单元`、`Linker-Drug` 等图式信号。
- P025/标题/摘要显示是具体 ADC 化合物、双抗/多特异 ADC、Linker-Drug 平台或新型载荷，但 claims 文字不足以归纳具体结构。

## Top5 确定性评分规则

Top5 必须在全量 `claims` 结构增强和必要图像门禁执行后计算。按 `priority_score desc -> patent_type_priority -> independent_claim_count desc -> pn asc` 排序。

基础类型分：

| 专利类型 | 分值 |
|---|---:|
| `双抗/多特异ADC` | 30 |
| `ADC化合物` | 27 |
| `Linker-Drug平台` | 23 |
| `新型载荷` | 21 |
| `偶联技术` | 18 |
| `新用途` | 15 |
| `联用方案` | 12 |
| `给药方案` / `非肿瘤ADC` | 10 |
| `其他` | 8 |

加分项：Claim 1 直接保护 ADC/组合物/用途 +12；claims 披露 CDR/VH/VL/SEQ ID +10；claims 披露 linker-drug/payload/结构通式 +10；明确靶点 +10；双靶点额外 +10；结构字段有明确证据每项 +4~5；高关注 payload 或差异化 linker +6；claims 已返回 +4；图像门禁已调用且有证据 +2。

## 深度解读写作规则

重点专利：三模块完整+子项拆解，约 180-240 字。必须使用 `P025/tech_summary + claims + family + legal_status`。
普通专利：每个模块 1-2 句，约 50-80 字。至少基于 `bibliography + P025/tech_summary + claims`。

输出三段：
- `核心保护点`：直接说明 Claim 1 或独立权利要求中的保护客体、靶点/序列/结构边界，不得写成"某方向布局"。
- `创新/新颖性`：用 P025 的"技术问题 -> 技术手段 -> 技术功效"组织语言，结合 payload/linker/偶联/DAR/用途细节评价差异化。
- `竞争意义`：说明对同靶点、同 payload/linker 平台、双抗/多特异 ADC、用途或 FTO 的具体影响。

重点专利额外输出：
- `同族与法律状态`：必须写真实 family 国家/件数和 legal_status 实际值。
- `FTO提示`：必须说明需要规避的具体权利要求要素（序列/CDR、靶点组合、payload、linker、偶联位点、DAR 或用途）。

写作红线：
- 禁止出现 `P025指出`、`claims显示`、`根据工具取证`、`当前证据主要来自` 等流程话。
- 禁止把表格字段以 `payload=...`、`linker=...` 等形式搬进深度解读正文。
- `备注` 必须是一句话情报摘要，说明保护重心、临床/平台意义或FTO关注点。
- 以情报专家口吻直接给判断；如果 claims 中有 `优选地/更优选地`，必须把这些优选参数视为重点保护方向。

结构字段状态归因：`未明确` 必须替换为 `未披露（claims未给出）`、`未披露（用途权利要求）`、`不适用（Drug-Linker平台）` 或 `图像待解析`。

## 专利类型固定分类

`patent_type` 必须归入以下固定字典：

| 固定类型 | 使用场景 |
|---|---|
| `ADC化合物` | 具体 ADC 分子、抗体-药物偶联物、单靶点 ADC |
| `双抗/多特异ADC` | 双靶、双抗、多特异 ADC 或多特异递送构建体 |
| `Linker-Drug平台` | linker、drug-linker、payload-linker 平台 |
| `新型载荷` | payload、毒素、Topo I/PBD/MMAE/SN-38 等载荷平台或衍生物 |
| `偶联技术` | 定点偶联、糖基偶联、DAR 控制、偶联工艺 |
| `联用方案` | ADC 联合治疗、联合用药方案 |
| `新用途` | 新适应症、新患者人群、治疗用途扩展 |
| `给药方案` | 剂量、给药频次、给药方法或制剂给药设计 |
| `非肿瘤ADC` | 免疫、炎症、自身免疫或其他非肿瘤 ADC/递送方向 |
| `其他` | 暂不能归入以上类型的低置信项目 |

中国申请人柱图使用红色，海外申请人柱图使用蓝色（每期固定）。

## 报告结构与图表

固定输出顺序：执行摘要 → 专利汇总表 → 统计分析 → 重点专利深度解读 → 专利 AI 解读 → ADC 结构标注 → 数据说明。

统计分析只保留 3 个图：申请人分布横向柱状图、专利类型分布饼图/环图、靶点分布图。不得输出国别分布图，不得输出"格局变化"模块。

汇总表字段：`#` / `专利号` / `申请人` / `专利类型` / `靶点` / `载荷类型` / `Linker` / `偶联方式` / `DAR` / `专利关联管线` / `研发阶段` / `备注`

## 渲染脚本约定

Eureka Desktop 完成数据采集后，将最终专利数据写入 `@skill_workspace` 目录下的 JSON 文件，文件名格式：

```text
adc_week_{YYYYWWW}_payload.json
```

调用 `scripts/build_adc_report.py` 时传入以下环境变量：

```text
EUREKA_PATENT_DATA_FILE = JSON 文件绝对路径（优先）
SKILL_REF_DIR           = @skill/references 目录
EUREKA_OUTPUT_DIR       = 输出目录（建议 @skill_workspace）
WEEK_LABEL              = 例如 2026年第17周
DATE_RANGE              = 例如 2026-04-20 ~ 2026-04-26
DATE_FROM               = YYYYMMDD
DATE_TO                 = YYYYMMDD
```

兼容方式：`EUREKA_PATENT_DATA = JSON字符串`（专利数较多时必须优先使用文件）。

脚本输出文件名：`ADC_Patent_Weekly_Report_{YYYY}W{WW}.html`

`build_adc_report.py` 仅使用 Python 标准库（os/sys/json/re/time/urllib/collections/datetime），**无需安装任何第三方依赖**。

## 数据一致性门禁

- HTML 中原始命中数必须等于主检索 `TOTAL_RAW`。
- 主检索 query 必须包含 `TAC_ALL`、`AUTHORITY:WO`、`F_PBD:[{DATE_FROM} TO {DATE_TO}]`。
- 最终 `patents` 数量必须等于汇总表专利行数、专利链接数量、AI/深度解读去重后卡片数量之和。
- 每条专利必须有 `pn`、`patent_id`、`publication_date`、`priority_claims`、`assignee_short`、`patent_type`。
- Top5 重点专利的优先权日和公开日不能为 `—`。
- `patent_type` 必须属于固定分类字典。
- 若最终专利数大于 3，`linker` 或 `conjugation` 单一弱值占比不得超过 70%。
- 页面不得包含 `AI标题` 标签，不得包含"格局变化"，不得包含 `countryChart`。

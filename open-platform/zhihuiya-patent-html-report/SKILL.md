---
name: zhihuiya-patent-html-report
description: 使用智慧芽/Patsnap MCP 数据创建或更新 V6 风格 HTML 专利情报报告。适用于用户要求调研专利、重新执行专利 landscape 项目、分析抗体/ADC/药物专利、生成 CCS/CSS 风格 HTML 报告、添加智慧芽 UUID 来源链接，或为后续类似专利报告添加可悬浮的专利附图引用的场景。
---

# 智慧芽专利 HTML 报告

## 概述

使用此 skill 将专利号、专利 URL、药物资产、靶点或既有 PatSnap 报告转化为可追溯的中文情报报告。优先使用智慧芽 MCP 工具获取主要数据，保留来源 UUID，并输出自包含或相对仓库路径的 V6 风格 HTML 报告。

创建或编辑报告时，阅读 `references/report-spec.md` 了解详细格式和链接规则。链接路由较为脆弱：除非 MCP 响应明确给出前端列表 query ID，否则不要将 MCP 实体 UUID 放入 Synapse `*-list?query_id=...` 路由。

## 使用前配置 

本 Skill 依赖智慧芽开放平台 MCP 服务： 

- 完成安装、初次使用时需进行自检，参见 README.md 
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具 
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论 
- 缺少MCP配置时，引导用户参照 README.md 在 [ open.zhihuiya.com ]( https://open.zhihuiya.com/ ) 获取MCP。

## 工作流

1. 根据用户请求识别项目范围。
   - 如果用户说“上个项目”或“重新执行”，检查 `reports/` 并复用最相关的既往报告主题。
   - 不要覆盖旧报告；创建新的版本化 HTML 文件。
   - 如果已知专利号，将其作为主要锚点。

2. 使用智慧芽/Patsnap MCP 重新查询数据。
   - 当用户提到药物、靶点、公司、疾病、专利号或临床试验时，先规范化实体。
   - 使用 `ls_patent_fetch` 和 `patsnap_fetch` 按 PN 或 patent ID 获取核心专利。
   - 对于生物学和医药背景，按需查询靶点、药物、临床试验、临床结果、论文、转化医学、交易和新闻工具。
   - 对于抗体/ADC 专利，当序列权利要求、payload 或 linker 结构重要时，也使用序列和结构工具。

3. 写作前构建来源映射。
   - 记录 MCP 返回的每个 UUID。
   - 在智慧芽链接中使用 UUID，而不是公开号或标题。
   - 使用 Synapse 详情/来源路由，而不是列表路由：药物使用 `/drug/<drug_id>`，临床试验使用 `/clinical-progress-detail/<clinical_trial_id>`，临床结果使用 `/clinical-result-detail/<ct_result_id>`，文献使用 `/literature-detail/<paper_id>`，新闻/交易/转化医学在没有已知稳定实体详情路由时应使用 MCP 返回的 `url`，专利使用 Analytics `patentId=<patent_id>`。
   - 在报告中保留足够的查询来源信息，以便追溯。

4. 按 V6 风格撰写 HTML 报告。
   - 使用密集型情报报告布局：sticky topbar、紧凑指标卡、callout、`.tw` 表格容器、zchip 来源链接、交替 section band、暗色模式和简洁中文分析。
   - 包含概览、专利核心、靶点生物学、权利要求/序列、payload/linker 或技术路线、实验证据、管线/临床格局、专利、文献/转化证据、BD/新闻、附图和来源等章节。
   - 有可用本地图片时使用本地图片文件。将图片链接放在引用证据的准确位置，而不是只放在附录中。

5. 添加可悬浮附图引用。
   - 在相关权利要求、序列、payload、DAR/SEC、IC50 或 TGI 陈述旁使用 `<a class="iref" href="..." data-img="..." data-cap="..." target="_blank">图 Ixxxxx</a>`。
   - 添加一个共享 hover preview 脚本和 `.iref`/`#img-float` CSS。
   - 保留附图附录作为索引，但正文中的主要证据引用应以内联方式呈现。

6. 最终回复前校验。
   - 解析 HTML。
   - 检查没有 `query_id=` 在 `*-list` 路由中使用 PN、NCT、标题、公开号或 MCP 实体 UUID。
   - 检查没有 Synapse 链接匹配 `/(drug-list|clinical-progress-list|clinical-result-list|literature-list|drug-deal-list|news-list|translational-medicine-list)?query_id=<entity_uuid>`。
   - 检查没有 `patentId=` 使用公开专利号。
   - 检查引用的本地图片存在。
   - 如可能，用浏览器或 Playwright 测试 hover 预览；如不可用，仅报告静态检查结果。

## MCP 工具模式

使用与请求实体匹配的具体 MCP 工具：

- 专利：`ls_patent_fetch`、`patsnap_fetch`、`ls_patent_search`、`ls_patent_vector_search`。
- 靶点：`ls_target_fetch`。
- 药物/管线：`ls_drug_search`、`ls_drug_fetch`、`ls_drug_milestone_fetch`。
- 临床试验/结果：`ls_clinical_trial_search`、`ls_clinical_trial_fetch`、`ls_clinical_trial_result_search`、result fetch。
- 文献/证据：`ls_paper_search`、`ls_paper_vector_search`、`ls_translational_medicine_search`，相关时使用 guideline/FDA/news 工具。
- 交易/新闻：`ls_drug_deal_search`、`ls_drug_deal_fetch`、`ls_news_vector_search`。
- 生物学/化学：`ls_patent_sequence_fetch`、序列检索/比对、结构 fetch/search、必要时 SAR 提取。

对于专利检索，当结构化分面噪声较大时，将结构化检索与语义检索结合使用。对于 CEACAM5 等宽泛靶点，避免将宽泛原始检索结果直接堆入报告；应按模态、payload、疾病、公司或具体技术词进一步收窄。

## 报告质量标准

- 除非用户另有要求，使用中文撰写。
- 使具体陈述可追溯到 MCP 查询和来源链接。
- 区分事实和判断：用 callout 表达结论、风险和 FTO 含义。
- 保持用户旧文件完好。
- 不暴露 API key，也不硬编码 MCP 凭据。
- 在 `/Users/nihil/Documents/PatSnap` 内工作时，优先使用现有仓库样式文件，例如 `reports/CSS.md` 和既有 `*_v6_*.html` 模板。

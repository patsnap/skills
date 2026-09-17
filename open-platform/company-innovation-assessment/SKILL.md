---
name: company-innovation-assessment
description: Use when 用户需要基于智慧芽 Company Intelligence 查找并评估企业：支持通过企业名称、company ID 或实时 Schema 已发布的其他标识确认唯一企业主体，也支持按实时 Schema 可用的地区、行业、工商、科创、融资和专利条件筛选待评估企业；选定企业后，可获取科创概要、公司竞争力与股权结构、研发规模与稳定性、技术布局、技术质量与技术影响力及技术风险数据，并生成有证据约束、可审计、自包含、可下载的企业科创力评估或技术尽调 HTML 报告。
---

# 企业科创力评估

本 Skill 负责确认企业主体、编排 MCP 分析 Tool，并通过 `generate_innovation_report` 获取最终 HTML 报告链接后自动下载报告。报告的归一化、AI 解读、渲染、校验和上传均由 MCP Tool 完成。

## 输入与主体口径

- 未提供企业时，只提示用户提供实时 `search_company` Schema 中可用的主体标识：法定名称或 company ID；仅当 Schema 明确提供 `credit_code` 或 `org_number` 时，才可同时提示对应中国企业标识。不调用分析 Tool。
- 股票代码不是 `search_company` 已发布的主体标识。用户只提供股票代码时，不得把它填入 `name` 或 `keyword`，也不得凭模型常识映射企业；应说明当前不支持按股票代码解析，并请用户补充法定名称或 company ID。
- 简称、品牌或别名存在多个合理候选时，先调用 `search_company`，列出候选并请用户确认；确认前停止后续调用。
- 唯一主体确认后默认使用 `standalone`。用户明确要求集团、穿透或包含子公司时使用 `group-through`；当前只有股权穿透模块采用穿透口径，其余模块仍为单一法人口径。
- 未提供报告用途时，`decision_purpose` 使用“企业科创力研究”。

## 渐进式结果展示

- 用户可见内容与内部编排分离：完整 Tool 返回仍按契约保留并传入报告 Tool；对话只展示当前任务所需的业务结果、可信边界和下一步，不展示内部调用过程。
- 首次 Tool 调用前，用一句简短进度说明正在确认企业主体；不得展示 MCP 探测、Schema 读取或连接准备细节。
- 主体确认后立即展示法定名称、国家或地区、评估口径和报告用途；存在多个合理候选时按前述规则展示候选并等待确认。
- 四个分析 Tool 并行执行时，每完成一个分析 Tool，就及时展示一句对应业务范围的结果摘要，并从该 Tool 已返回的数据中选择 1—2 个易懂指标或有业务影响的覆盖边界。多个 Tool 在短时间内完成时合并为一次更新；不得为了逐 Tool 播报而延迟已得到的结果。
- 任一阶段连续 45—60 秒没有新结果时，补充一条简短状态，只说明当前阶段、已经完成的业务范围和仍在处理的内容。不得虚构进度百分比、剩余时间或尚未返回的结论。
- 所选分析全部结束后，用一次更新汇总已完成的分析范围和至多 3—6 个关键指标；能够继续生成时明确说明“数据分析已完成，正在生成报告”。局部失败只用一句业务语言说明受影响的判断范围。
- 报告 Tool 返回有效 `report_url` 后，不等待本地下载完成，立即说明“报告已生成，正在校验并保存本地文件”。下载过程仅在最终失败或需要用户处理时再次更新。
- 最终交付先给 3—5 条有证据支持的关键发现，不把局部覆盖项列为关键发现；再说明主体口径和报告可支持的分析范围，最后交付本地 HTML、原始 `report_url`、`expires_at` 与 `download_notice`。
- 默认不展开 Tool 名称、原始错误码、内部字段名、调用次数、trace 信息或逐字段空值清单；用户明确要求原始数据、诊断信息或审计明细时再提供。
- 仅当问题会改变主体、结论边界或交付结果时主动说明技术边界。报告返回 `success` 或 `partial_success`、存在 `report_url`，且用途所需模块未进入 `failed_modules` 时，按报告已完成交付；其余局部覆盖由报告卡片呈现。

## 执行流程

1. 执行前静默检查 company-intelligence MCP 及六个公开 Tool；调用前读取实时 Tool Schema，运行时 Schema 优先。
   - 依赖可用时直接进入业务流程，不向用户展示工具探测、Schema 或连接准备细节。
   - MCP 未安装、连接失败或缺少必需 Tool 时停止业务流程，读取 [MCP 安装与配置说明](references/mcp-setup.md)，引导用户完成配置并重新加载客户端后再继续。不得要求用户在对话中提供 API Key，也不得回显或保存完整凭证。
   - 本中文 Skill 调用全部六个公开 Tool 时都显式传 `locale=zh-CN`，避免被海外部署默认语言覆盖；若返回的 `effective_locale` 不是 `zh-CN`，停止报告编排并说明服务端语言契约异常。
   - 部署环境决定字段可用性，`locale` 只决定返回语言。每次调用只能使用实时输入 Schema 中存在的字段；不得发送、追问或承诺已被当前环境裁剪的字段，也不得把它们写成报告必含内容。
2. 通过 `search_company` 确认唯一法律实体，同时保留候选项中的 `company_id` 和 `country`。
3. 身份确认后，以默认完整维度并行调用四个分析 Tool：
   - `get_innovation_overview`
   - `analyze_company_competitiveness`
   - `analyze_innovation_capability`
   - `get_risk_information`
4. 保留上述四个 Tool 的完整返回，包括 `tool_id`、`status`、`message`、`payload`、`coverage` 和 `errors`；失败返回也保留，不得只摘取局部字段。
   - `analyze_innovation_capability.payload.technology_layout.ipc_classifications` 包含报告分类号清单所需的 IPC 中文释义；传给报告 Tool 时不得裁剪、重建或另行查询。
5. 调用 `generate_innovation_report`，将确认主体返回的 `country` 以同名字段传入，并同时传入 `company_id`、`entity_scope`、`decision_purpose` 和完整 `tool_results`。`tool_results` 至少包含一项，键使用原 Tool ID，值使用对应 Tool 的完整返回。
   - 用户只要求部分维度、或只有部分分析 Tool 已执行时，可以只传这些 Tool 的完整返回；报告只生成对应卡片。
6. `success` 或 `partial_success` 且存在 `report_url` 时，立即自动下载该 URL 对应的报告：
   - 仅允许 HTTPS。下载前校验 URL，拒绝用户信息、`localhost` 以及私网、环回、链路本地或保留地址；初始地址与每次重定向都必须解析到公网地址，重定向主机还必须与原主机相同或位于运行环境明确配置的报告存储域白名单中。
   - 下载到当前任务的可写工作目录：先写入本次任务创建的临时文件，校验通过后再改名为可辨识、文件系统安全且不覆盖已有文件的 `.html` 文件名。将完整 URL 作为单个参数处理。
   - 同时要求 HTTP 2xx、HTML 类型的 `Content-Type`、文件非空，并包含报告稳定结构标记 `TECH INNOVATION ASSESSMENT`；校验失败按下载失败处理，清理本次任务创建的无效或未完成临时文件。不得修改或重新生成服务端产出的 HTML。
   - 校验通过后，向用户交付可点击的本地 HTML 文件，同时保留默认一周有效的原始 `report_url`（实际以 `expires_at` 为准）。转述 `download_notice`，并说明本地文件已保存、临时链接失效后需重新生成报告。
   - 下载失败时最多重试一次；仍失败则停止重试，明确区分“报告已生成”和“本地下载失败”，交付原始 `report_url`、`expires_at` 及可读错误，提示用户在失效前及时下载并妥善保存，不得因此重新调用报告 Tool。
   - 即使用户要求只返回链接，也应完成自动下载，并不得省略本地 HTML、有效期与下载提示。
7. `data_unavailable` 或缺少 `report_url` 时，根据返回的 `message`、`coverage` 和 `errors` 说明失败边界，不得回退到本地脚本或隐藏 Handler。

## 边界

- 不得自造企业身份、排名、评级、地区、行业、权属、集团合并值或缺失数据。
- 不得静默扩大主体口径；`group-through` 必须按混合口径理解。
- 报告 Tool 负责报告内容和视觉质量；Skill 不复写 Tool 已生成的 HTML。
- 来源事实（企业法定名称、专利标题、技术主题等）按 Tool 返回原样保留，不自行翻译。
- 报告用于研究与技术尽调辅助，不构成法律、投资、信贷、资助或合作决策意见。

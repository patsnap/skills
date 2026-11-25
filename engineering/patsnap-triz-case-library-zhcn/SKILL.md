---
name: patsnap-triz-case-library
description: 面向研发创新的 TRIZ 跨领域案例检索 MCP。支持按技术矛盾、功能关系、技术功效、科学效应和关键词，从 4500 万+结构化专利案例中匹配可借鉴解法，返回案例摘要、创新点及 TRIZ 标注，为企业 Agent 提供有出处的创新启发和方案依据。
license: Proprietary
metadata:
  display_name: TRIZ案例库
  display_description: 面向研发创新的 TRIZ 跨领域案例检索 MCP。支持按技术矛盾、功能关系、技术功效、科学效应和关键词，从 4500 万+结构化专利案例中匹配可借鉴解法，返回案例摘要、创新点及 TRIZ 标注，为企业 Agent 提供有出处的创新启发和方案依据。
---

# TRIZ案例库

## 触发与排除

触发按技术矛盾、功能关系、功效、科学效应或关键词查找跨领域 TRIZ 专利案例。不执行完整创新方案生成，也不替代专利法律意见或全库数量分析。

## 检索规则

1. 将工程问题映射为合适的检索条件。`search_triz_case` 至少提供 technical_contradiction、svop、efficacy、oxford_effects、keyword 中一类；filters 不能独立构成检索。
2. 使用 efficacy 或 oxford_effects 前分别 `list_triz_search_terms(field="efficacy"/"oxford_effects")`，从真实 values 选择并保留原拼写。truncated=true 表示常用子集，不能宣称查到了全部术语。该工具不提供 SVOP 的标准动词或标准参数枚举。
3. technical_contradiction 中 improving_param_ids/worsening_param_ids 使用 TRIZ 参数 1–39，invention_principle_ids 使用原理 1–40；不确定映射时使用关键词或澄清，不伪造编号。SVOP 中 subject/object 为自由文本，verb_standard/param_standard 需要已有可靠标准术语，不用未知中文词冒充标准枚举。
4. 不同检索条件类型之间 AND；technical_contradiction/svop 的多个对象之间 OR，同一个对象内部条件 AND。efficacy 与 oxford_effects 在同一记录内 AND。不要把多类输入误说成扩大召回的 OR。
5. keyword 最多 5 个；limit 为 1–200、默认 50；sort 为 sdesc 相关性、pdesc 公开日、vdesc 价值。filters 可限定受理局、法律状态、申请人或 IPC/CPC，并可排除原领域寻找跨领域案例。真实范围以本次传参和返回为准，不从截断返回推断全库总量。
6. 比较实际案例的问题、功效、创新摘要和 TRIZ 标注，说明哪些机制可迁移及哪些工况尚待验证。空结果时列出真实条件，建议逐项放宽；不把检索错误当无结果，不伪造案例内容或来源。

## 交付

交付问题映射、真实检索条件、代表案例及其问题/功效/创新机制、TRIZ 标注、跨领域借鉴点和可追溯来源。返回只含案例标识而没有对应专利 ID/公开号时保留实际标识，不拼装虚假专利链接。没有导出工具，不声称生成下载文件。

# MCP 边界与调用口径

## 6 个指定 MCP

| MCP | 用途 | 典型问题 |
|---|---|---|
| `corporate_intangible_assets` | 非专利资产档案、主体资产完整度、潜在买方 | 这家公司除专利外还有哪些商标/软著/集成电路布图？这件专利可能卖给谁？ |
| `patent_valuation_scorecard` | 单件专利价值评分和维度拆解 | 这件专利为什么高分/低分？技术、市场、法律价值分别如何？ |
| `patent_monetization_valuation` | 商业化估值、法律状态、家族、权利要求、翻译 | 这件专利是否适合交易？是否有法律或运营障碍？ |
| `patsap_patent_search` | 语义/关键词探索、专利/论文混合检索、Markdown 正文 | 这个技术方向有哪些相似方案？正文里如何描述技术效果？ |
| `advanced_patent_search` | 精确检索、数量统计、字段分布、相似专利、申请人扩展 | 该方向有多少同类专利？主要申请人是谁？技术拥挤度如何？ |
| `global_core_patent_database` | 权利要求、同族、被引、PDF、摘要图、底层翻译 | 核心权利要求是什么？同族覆盖哪些国家？被引和 PDF 证据是什么？ |

## 三层搜索漏斗

1. 探索层：先用 `patsap_patent_search` 找主题、读正文、看专利和论文样本。
2. 统计层：再用 `advanced_patent_search` 固化检索式，做数量、字段、申请人、地区、年份和相似专利统计。
3. 核验层：最后用 `global_core_patent_database` 对 A/B 类核心资产核验权利要求、同族、被引、PDF、摘要图和翻译。

## 冲突处理

- 专利数量、字段分布、技术拥挤度：以 `advanced_patent_search` 为准。
- 语义样本、论文混合检索、Markdown 正文：以 `patsap_patent_search` 为准。
- 权利要求、同族、引用、PDF、摘要图：以 `global_core_patent_database` 为准。
- 单件价值评分：以 `patent_valuation_scorecard` 为准。
- 法律状态、商业化交易洁净度、翻译材料：以 `patent_monetization_valuation` 为准。
- 商标、软著、集成电路布图、植物新品种、潜在买家：以 `corporate_intangible_assets` 为准。

## 证据等级

- S：政府、部委、国家知识产权局、官方公共服务平台、MCP 底层专利事实。
- A：技术交易平台、招投标、上市公司公告、企业官网、专利评分/估值结构化结果。
- B：行业协会、权威媒体、园区公告、公开会议资料。
- C：普通媒体、论坛、社交平台，只可作为弱信号。
- D：无来源转载，不进入结论。

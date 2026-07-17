---
name: drug-potential-assessment
description: "评估候选药物的成药性、差异化和研发商业潜力。适用于：比较候选药物的成药性、差异化、临床可行性、竞争强度和商业潜力，用于早期候选筛选或同靶点药物比较。"
---

# 成药潜力评估助手

## 定位

当用户输入 **适应症、研究领域或靶点**（可三者组合），本 Skill 自动触发全维度情报收集流程，筛选具备成药潜力的候选药物，进行多维评分，并输出结构化分析报告。

**典型查询示例：**
- "分析 KRAS G12C 靶点的成药潜力药物"
- "非小细胞肺癌 EGFR 领域有哪些潜力候选药物？"
- "GLP-1R 激动剂糖尿病治疗领域的成药潜力分析，投资评估视角"
- "NASH 适应症最新成药候选情报，深度研究"

---

## MCP 工具全景（完整命名规范）

所有工具调用须使用完整命名格式 `mcp_<服务名>__<工具名>`，禁止使用裸工具名以避免路由歧义。

### 核心生命科学情报
| MCP 服务 | 完整工具名前缀 | 核心工具 | 用途 |
|---------|-------------|---------|------|
| `virtual-mcp-pharma-intelligence` | `mcp_virtual-mcp-pharma-intelligence__` | ls_drug_search / ls_drug_fetch / ls_drug_milestone_fetch / ls_clinical_trial_search / ls_clinical_trial_result_search / ls_patent_search / ls_patent_fetch / ls_paper_search / ls_paper_vector_search / ls_drug_deal_search / ls_organization_fetch / ls_organization_pipeline_fetch / ls_epidemiology_vector_search / ls_translational_medicine_search | 药物/临床/专利/文献/交易/流行病学全维情报 |
| `virtual-mcp-biology-modality` | `mcp_virtual-mcp-biology-modality__` | ls_antibody_antigen_search / ls_sequence_fetch / ls_sequence_search_submit / ls_sequence_search_check_status / ls_sequence_search_get_results | 序列情报、抗体-抗原关系 |
| `virtual-mcp-chemical-molecular` | `mcp_virtual-mcp-chemical-molecular__` | ls_patent_structure_fetch / ls_structure_fetch / ls_admet_predict / ls_sar_submit / ls_sar_fetch / ls_structure_search / ls_chemical_mcs_analyze | 化学结构、ADMET预测、SAR分析 |

### 专利深度分析
| MCP 服务 | 完整工具名前缀 | 核心工具（2C专用） | 核心工具（2J专用） |
|---------|-------------|-----------------|-----------------| 
| `patsnap-aggregation-data` | `mcp_patsnap-aggregation-data__` | search_patents_v3 / search_patents_with_detail / detail / detail_text | search_patents_statistics / search_patents_facet / applicant_rank / technology_life_cycle / ipc_rank |
| `patent-search` | `mcp_patent-search__` | patsnap_fetch | patsnap_search |

### 企业深度情报
| MCP 服务 | 完整工具名前缀 | 核心工具（2B专用） | 核心工具（2J专用） |
|---------|-------------|-----------------|-----------------| 
| `patsnap-acquisition` | `mcp_patsnap-acquisition__` | company_financing / acquisition_get_tech_eval_indicators / acquisition_get_group_tech_eval / company_tech_label / company_industry | patent_valuation / tech_indicators / legal_indicators / market_indicators / strategic_indicators / economic_indicators / patent_risk_warning |

---

## 工作流程

### 📢 执行进度反馈规范（约束 #17）

每个 Phase 开始前必须输出一行进度提示，格式如下：
- Phase 2 启动时：`⏳ 情报收集中（10路并行）：药物 / 企业 / 专利 / 文献 / 临床 / 序列 / 化学结构 / BD交易 / 流行病学 / 专利格局...`
- Phase 3 开始前：`✅ 情报收集完毕，共获取 [X] 条候选药物 / [X] 件专利 / [X] 篇文献 / [X] 项临床试验，开始候选筛选...`
- Phase 4 开始前：`⚙️ 筛选完成，进入多维评分（共 [N] 个候选）...`
- Phase 5 开始前：`📝 评分完成，生成报告...`

### Phase 1：实体标准化
调用 `mcp_virtual-mcp-pharma-intelligence__ls_ner_nor_normalize` 对用户输入进行 NER/NOR 标准化，识别并规范化：
- 靶点（Target）
- 适应症/疾病（Disease）
- 研究领域（Therapeutic Area）
- 药物（Drug，若有）
- 公司（Company，若有）

### Phase 2：多维情报并行收集

**10路并行执行**，各子模块职责严格分工：

#### 2A 药物情报（pharma-intelligence）
- `mcp_virtual-mcp-pharma-intelligence__ls_drug_search`：检索候选药物，覆盖 preclinical → phase_3 阶段
- `mcp_virtual-mcp-pharma-intelligence__ls_drug_fetch`：获取候选药物详情（靶点、机制、适应症、开发状态）
- `mcp_virtual-mcp-pharma-intelligence__ls_drug_milestone_fetch`：获取候选药物研发里程碑时间线

#### 2B 企业情报（pharma-intelligence + patsnap-acquisition）
**职责**：获取头部企业完整管线、融资能力、创新能力评估
- `mcp_virtual-mcp-pharma-intelligence__ls_organization_fetch`：重点企业基本信息
- `mcp_virtual-mcp-pharma-intelligence__ls_organization_pipeline_fetch`：**【必须实际调用】** 对 TOP 3~5 头部企业逐一获取管线数据，生成企业管线对比表
- `mcp_patsnap-acquisition__company_financing`：获取头部企业融资事件明细（轮次、金额、时间）**【必须实际调用】**
- `mcp_patsnap-acquisition__acquisition_get_tech_eval_indicators`：企业科技创新能力评估（单体企业）
- `mcp_patsnap-acquisition__acquisition_get_group_tech_eval`：**【集团穿透】** 企业集团穿透后的科技创新能力评估（适用于有母公司/集团结构的大型药企）
- `mcp_patsnap-acquisition__company_tech_label`：企业科技资质标签（国家级高新技术企业等）
- `mcp_patsnap-acquisition__company_industry`：企业行业分类（GBC/SEIC）

#### 2C 专利情报——条目检索层（pharma-intelligence + patsnap-aggregation-data）
**职责**：检索具体专利条目（IDs、标题、摘要），用于候选药物证据支撑。统计分析交由 2J 执行，避免重复调用。
- `mcp_virtual-mcp-pharma-intelligence__ls_patent_search`：语义检索目标靶点/适应症最新专利（近3年优先）
  - **【必须加 IPC 分类约束】**：优先使用 `A61K`、`A61P`、`C07D`、`C07K` 等药学/化学 IPC 作为过滤条件
  - **【相关性校验】**：返回结果须通过靶点名称/适应症关键词匹配，过滤与主题无关的专利
- `mcp_patsnap-aggregation-data__search_patents_v3`：PatSnap 高级检索式精准检索（补充语义检索）
- `mcp_patsnap-aggregation-data__search_patents_with_detail`：检索同时返回首条专利全文，减少二次调用
- `mcp_patsnap-aggregation-data__detail`：单条核心专利完整详情（含法律状态、同族、引用）
- `mcp_patsnap-aggregation-data__detail_text`：核心专利全文详情（背景技术、权利要求、技术要素）
- `mcp_virtual-mcp-pharma-intelligence__ls_patent_fetch`：获取核心专利详情
- **专利类型重点**：product_compound、sequence、crystal_form、new_use

#### 2D 文献情报（pharma-intelligence）
**职责**：检索文献证据，须过滤偏题条目
- `mcp_virtual-mcp-pharma-intelligence__ls_paper_search`：检索靶点/适应症高引文献
  - **【相关性校验】**：返回文献须与靶点/适应症直接相关，丢弃明显偏题条目
- `mcp_virtual-mcp-pharma-intelligence__ls_paper_vector_search`：语义搜索关键机制文献
- `mcp_virtual-mcp-pharma-intelligence__ls_translational_medicine_search`：转化医学证据链检索

#### 2E 临床情报（pharma-intelligence）
- `mcp_virtual-mcp-pharma-intelligence__ls_clinical_trial_search`：检索相关临床试验（招募中及已完成）
- `mcp_virtual-mcp-pharma-intelligence__ls_clinical_trial_result_search`：获取临床结果数据

#### 2F 序列情报（biology-modality）
- `mcp_virtual-mcp-biology-modality__ls_antibody_antigen_search`：靶点相关抗体-抗原关系检索
- `mcp_virtual-mcp-biology-modality__ls_sequence_fetch`：**【必须对命中的 TOP 5 抗体序列实际调用】**，获取重链/轻链序列详情
- 当靶点为蛋白/抗体类时，完整序列相似性搜索流程：
  `mcp_virtual-mcp-biology-modality__ls_sequence_search_submit` → `mcp_virtual-mcp-biology-modality__ls_sequence_search_check_status`（轮询至 SUCCESS）→ `mcp_virtual-mcp-biology-modality__ls_sequence_search_get_results`

#### 2G 化学结构情报（chemical-molecular）
调用链：专利号 → 结构获取 → InChIKey → SMILES → ADMET预测
- `mcp_virtual-mcp-chemical-molecular__ls_patent_structure_fetch`：根据 2C 返回的专利号批量获取关联化学结构
- `mcp_virtual-mcp-chemical-molecular__ls_structure_fetch`：根据 InChIKey 获取化合物详情（SMILES/分子式/名称）
- `mcp_virtual-mcp-chemical-molecular__ls_admet_predict`：对获取的 SMILES 执行 ADMET 预测
- `mcp_virtual-mcp-chemical-molecular__ls_sar_submit` + `mcp_virtual-mcp-chemical-molecular__ls_sar_fetch`：SAR 构效关系提取（提交后轮询获取结果）
- `mcp_virtual-mcp-chemical-molecular__ls_structure_search`：结构相似性搜索（SIM模式，threshold≥0.8）
- `mcp_virtual-mcp-chemical-molecular__ls_chemical_mcs_analyze`：最大公共子结构分析（多候选结构对比）
- **【降级策略】**：若工具调用连续失败，自动切换为 `mcp_virtual-mcp-pharma-intelligence__ls_paper_vector_search` 检索 ADMET 相关文献，在报告局限性中注明 [LC]

#### 2H 交易情报（pharma-intelligence）
- `mcp_virtual-mcp-pharma-intelligence__ls_drug_deal_search`：BD 交易、授权、合作信息（成药潜力商业验证）

#### 2I 流行病学情报（pharma-intelligence）
- `mcp_virtual-mcp-pharma-intelligence__ls_epidemiology_vector_search`：检索适应症患病率、发病率、市场规模等流行病学数据
- **【必须量化】**：返回数据须直接引用作为"适应症需求强度"评分依据，不可纯主观判断

#### 2J 专利竞争格局深度分析——统计分析层（patsnap-aggregation-data + patsnap-acquisition）
**职责**：统计分析层面，与 2C 条目检索层严格分工，避免重复调用
- `mcp_patsnap-aggregation-data__search_patents_statistics`：按申请人维度统计，识别核心专利持有方
- `mcp_patsnap-aggregation-data__search_patents_facet`：按法律状态/国家/年份分面统计，快速获取全景分布
- `mcp_patsnap-aggregation-data__technology_life_cycle`：**【必须调用】** 技术生命周期（近10年专利申请趋势，输出ECharts折线图）
- `mcp_patsnap-aggregation-data__applicant_rank`：全球 Top10 申请人及专利数量
- `mcp_patsnap-aggregation-data__ipc_rank`：IPC 分类排名（识别核心技术方向）
- 对 Top 3 核心专利的五维深度分析（**【必须调用】**）：
  - `mcp_patsnap-acquisition__patent_valuation`：综合五维价值评分（技术/法律/市场/战略/经济）
  - `mcp_patsnap-acquisition__tech_indicators`：技术价值详细指标（被引数、权利要求数、IPC分布）
  - `mcp_patsnap-acquisition__legal_indicators`：法律价值详情（专利年龄、剩余寿命、诉讼国家）
  - `mcp_patsnap-acquisition__market_indicators`：市场价值详情（同族大小、覆盖国家数）
  - `mcp_patsnap-acquisition__strategic_indicators`：战略价值详情（转让/质押/许可次数）
  - `mcp_patsnap-acquisition__economic_indicators`：经济价值详情（IPC近5年增长率、同族稳定趋势）
- `mcp_patsnap-acquisition__patent_risk_warning`：对涉诉/高风险专利识别风险（质押/诉讼/无效）

---

## Phase 3：候选药物筛选

基于收集到的情报，按如下规则筛选成药潜力候选：

**纳入标准：**
1. 具备明确靶点-适应症关联
2. 存在专利保护或近期申请
3. 至少有一项：临床前/临床数据 OR 序列信息 OR 化学结构信息
4. 涉及活跃开发企业

**排除标准：**
- 已上市且非新适应症（除非用于组合/新剂型分析）
- 已明确终止/撤回

**优先级加权：**
- 近12个月新专利申请 → 权重提升
- Phase 2/3 临床在研 → 权重提升
- 多家企业竞争布局 → 领域热度标记
- 专利价值综合评分高（patent_valuation 返回）→ 权重提升

---

## Phase 4：多维潜力评分

每个候选药物从以下 **7个维度** 打分（每维 0-10 分）：

| 维度 | 评分依据 | 数据来源 |
|------|---------|---------| 
| 🎯 靶点生物学证据 | 文献支持强度、作用机制清晰度 | 文献、序列 |
| 🧪 化学可成药性 | ADMET预测值、结构多样性、SAR数据 | 化学结构、ADMET |
| 📋 临床开发进展 | 最高临床阶段、近期试验数据 | 临床试验/结果 |
| 🔒 专利保护强度 | 核心专利布局、**五维价值评分**（tech/legal/market/strategic/economic_indicators）、保护范围 | 专利情报+价值评估 |
| 🏢 企业竞争格局 | 头部企业投入强度、**融资能力**（company_financing）、BD 交易活跃度、**集团创新能力**（group_tech_eval）| 企业管线、融资、交易 |
| 💊 适应症需求强度 | 未满足医疗需求、**流行病学量化数据**（患病率/发病率/市场规模）| 流行病学、临床 |
| 🔬 创新差异化空间 | 专利空白（**技术生命周期阶段**）、机制新颖性、IPC 分类分布 | 专利+文献综合 |

**综合潜力得分** = 加权平均（权重依用户选择的分析视角预设）

### 分析视角与权重模板

用户可在输入时指定 `视角`，缺省为「标准分析」。报告中**必须展示**所用视角及权重配置表：

| 维度 | 投资评估 | 研发立项 | 专利布局 | 竞争监控 | 标准分析（默认）|
|------|---------|---------|---------|---------|---------------|
| 🎯 靶点生物学证据 | 15% | 25% | 10% | 15% | 15% |
| 🧪 化学可成药性 | 10% | 20% | 10% | 10% | 15% |
| 📋 临床开发进展 | 25% | 15% | 10% | 20% | 15% |
| 🔒 专利保护强度 | 15% | 10% | 35% | 15% | 15% |
| 🏢 企业竞争格局 | 15% | 10% | 15% | 25% | 15% |
| 💊 适应症需求强度 | 10% | 10% | 10% | 5% | 15% |
| 🔬 创新差异化空间 | 10% | 10% | 10% | 10% | 10% |

### 数据置信度与覆盖率标注规则（约束 #18）

- **高置信 [HC]**：来自多个独立来源交叉验证
- **中置信 [MC]**：来自单一可信来源
- **低置信 [LC]**：推断或间接证据，需进一步验证
- **覆盖率标注**：当返回样本数 / 总量 < 10% 时，自动标注 `[样本分析，覆盖率 X%]`；样本数 / 总量 ≥ 50% 时标注 `[较全面覆盖，覆盖率 X%]`

---

## Phase 5：报告生成

输出结构化 Markdown 报告，包含：

```
# 成药潜力分析报告

## 执行摘要
- 分析范围（靶点/适应症/领域）
- 分析视角 & 权重配置表
- 候选药物总数 & 高潜力候选数
- 核心发现 TOP 3

## 情报收集汇总（含数据覆盖率）
- 专利：X件（样本N件，覆盖率X%），时间范围，技术生命周期阶段
- 文献：X篇（覆盖率X%），关键期刊，核心发现
- 临床试验：X项（阶段分布）
- 序列：TOP 5 抗体重链/轻链序列详情（若适用）
- 化学结构：化合物数、ADMET亮点、SAR摘要（或降级说明）
- 企业管线对比表（TOP 3~5，含融资历史、集团创新能力评分）
- 流行病学数据（患病率/发病率/市场规模，量化引用）
- 重要BD交易

## 高潜力候选药物列表（TOP N）
[药物卡片 × N]
- 药物名称/代码 | 开发企业（融资情况）
- 机制/靶点 | 最高开发阶段
- 综合得分 & 各维度得分（含权重）[覆盖率标注]
- 核心证据（专利/文献/临床）
- 风险提示

## 竞争格局分析
- 企业管线对比表（实际调用数据）
- 企业融资能力对比（company_financing数据）
- 集团创新能力对比（group_tech_eval数据）
- 技术路线对比

## 专利格局深度分析
- 技术生命周期图（ECharts折线图，近10年申请趋势）
- 全球Top10申请人排名及专利数量
- IPC技术方向分布
- 核心专利五维价值详细分析：
  * 技术维度：被引数、权利要求数、IPC分布（tech_indicators）
  * 法律维度：专利年龄、剩余寿命、诉讼情况（legal_indicators）
  * 市场维度：同族大小、覆盖国家数（market_indicators）
  * 战略维度：转让/质押/许可次数（strategic_indicators）
  * 经济维度：IPC近5年增长率、同族稳定趋势（economic_indicators）
- 专利风险预警（涉诉/质押/无效情况）
- 核心专利清单 & 到期时间线
- 布局空白区域

## BD交易信号
- 近期重大交易 | 合作趋势

## 序列与结构亮点（若适用）
- 关键抗体重链/轻链序列特征
- 代表性化合物SMILES & ADMET数据
- SAR构效关系摘要 | MCS片段分析

## 结论与建议
- 优先关注候选（含理由）
- 投资/研发建议（短期/中期/长期）
- 数据局限性说明

## 数据来源追溯
[S1]...[S2]...
```

---

## 评分指引

| 得分区间 | 解读 | 建议动作 |
|---------|------|---------|
| 8-10 | 高度成药潜力，多维证据充分 | 优先立项/深度尽调 |
| 6-7.9 | 较强潜力，部分维度待补充 | 持续跟踪，选择性投入 |
| 4-5.9 | 中等潜力，存在关键不确定性 | 关注进展，等待更多证据 |
| 0-3.9 | 潜力有限或风险较高 | 观望或排除 |

---

## 执行约束（共20条）

1. **并行检索优先**：Phase 2 各子任务必须并行执行，减少等待时间
2. **完整工具名**：所有 MCP 工具调用必须使用 `mcp_<服务名>__<工具名>` 完整格式，禁止使用裸工具名
3. **证据追溯**：每项评分依据必须标注 [S#] 来源
4. **事实与推断分离**：推断性结论须明确标注 [LC] 并说明依据
5. **不生成虚假数据**：若某维度数据不足，标注"数据不足，评分保守"而非捏造
6. **报告语言**：中文为主，药物名称/靶点名称保留英文
7. **专利日期核验**：引用专利前确认申请日/公开日，不做"无新专利"的错误结论
8. **阶段准确性**：drug highest_phase 与 clinical trial phase 须区分描述
9. **相关性过滤**：专利/文献检索返回结果必须经过主题匹配校验，过滤与靶点/适应症无关的条目
10. **化学结构降级策略**：若 chemical-molecular 工具连续失败，自动降级为文献推断路径，须在报告局限性中说明 [LC]
11. **序列详情必须获取**：命中抗体序列后须实际调用 ls_sequence_fetch 获取 TOP 5 详情
12. **企业管线必须实际调用**：Phase 2B 必须对头部企业实际执行 ls_organization_pipeline_fetch，生成可对比的管线表格
13. **权重视角展示**：报告中须明确展示所用分析视角及对应权重配置表
14. **流行病学数据支撑**："适应症需求强度"评分须引用 ls_epidemiology_vector_search 返回的量化数据
15. **专利五维详细指标**：Phase 2J 对 Top 3 核心专利必须调用 patent_valuation + tech/legal/market/strategic/economic_indicators 五个详情工具
16. **企业融资数据**：Phase 2B 对头部企业必须实际调用 company_financing，融资能力须体现在企业竞争格局分析中
17. **执行进度反馈**：每个 Phase 开始前必须输出进度提示
18. **数据覆盖率标注**：返回样本数/总量 < 10% 时自动标注 [样本分析，覆盖率 X%]；≥ 50% 时标注 [较全面覆盖，覆盖率 X%]
19. **2C/2J 分工不重复**：2C 只做条目检索，2J 只做统计分析，同一工具不在两个模块重复调用
20. **集团穿透评估**：对有集团母公司结构的大型药企，优先使用 acquisition_get_group_tech_eval 而非单体评估

---

## 输入格式

用户可提供（至少一项）：
- `适应症`：如"非小细胞肺癌"、"2型糖尿病"
- `靶点`：如"EGFR"、"PD-1"、"KRAS G12C"
- `研究领域`：如"肿瘤免疫"、"代谢疾病"
- `分析深度`：快速概览 / 标准分析 / 深度研究（默认：标准分析）
- `分析视角`：投资评估 / 研发立项 / 专利布局 / 竞争监控（默认：标准分析）
- `候选数量`：返回 TOP N 候选（默认：TOP 10）
- `地域偏好`：如"中国"、"全球"（影响专利/临床检索范围）

## 输出格式

- **主报告**：完整 Markdown，包含结构化评分卡
- **摘要卡**：执行摘要（3-5 句话）
- **数据表格**：候选药物得分对比表（含视角权重）+ 数据覆盖率汇总表
- **可视化**：ECharts 柱状图（综合得分对比）+ ECharts 折线图（技术生命周期趋势）

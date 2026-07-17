---
name: adc-landscape-monitoring
description: "持续监控ADC研发、临床、专利、交易与竞争事件。适用于：持续监控ADC或抗体药物的研发进展、临床证据、专利变化、许可交易和竞争事件，用于赛道预警和BD机会跟踪。"
---

# RD&BD-monitor-patent&evidence&deal&drug-ADC

## 概述

本 Skill 面向 ADC 领域研发与商务拓展人员，提供**月度/周度进展监控简报**自动化生成能力。
- 监控范围：全 ADC 领域（不限靶点/公司）
- 默认周期：最近30天（可调整为7天/季度）
- 输出格式：可下载的自包含 HTML 报告

---

## 触发方式

用户说以下任意短语即触发本 Skill：
- `@skill:adc-landscape-monitoring`
- "运行ADC简报"、"ADC月度监控"、"ADC最新进展"
- 指定时间范围，如"2026年5月ADC简报"、"过去一个月ADC进展"

---

## 数据模块与 MCP 工具映射

| 模块 | MCP 工具 | 过滤参数 |
|------|---------|---------|
| 🤝 BD交易 | `ls_drug_deal_search` | `drug_type=["ADC"]`, `deal_date_from/to` |
| 📊 临床结果 | `ls_clinical_trial_result_search` | `drug_type=["ADC"]`, `published_date_from/to` |
| 🧪 新注册临床 | `ls_clinical_trial_search` | `drug_type=["ADC"]`, `study_first_posted_date_from/to` |
| ⚖️ 专利 | `ls_patent_search` | `drug_type=["ADC"]`, `publication_date_from/to` |
| 💊 获批药物 | `ls_drug_search` | `drug_type=["ADC"]`, `highest_phase=["approved"]` |
| 📄 文献 | `ls_paper_search` | `drug_type=["ADC"]`, `year_from/to` |
| 🏛️ 权威会议 | `mcp_web-search__web_search` | ASCO/AACR/ESMO/ASH/JPM + ADC关键词 |

---

## 执行步骤（9步编排）

### Step 0：解析时间范围
- 默认：最近30天（`today - 30days` 至 `today`）
- 用户指定月份：严格锁定 `YYYY-MM-01` 至 `YYYY-MM-30/31`
- 用户指定周：`today - 7days` 至 `today`

### Step 1：并行抓取所有模块数据
并行调用以下工具（无依赖关系，可同时执行）：
1. `ls_drug_deal_search`（BD交易，全量）
2. `ls_clinical_trial_result_search`（临床结果，limit=50，page1+page2）
3. `ls_clinical_trial_search`（新注册临床，limit=50）
4. `ls_patent_search`（专利，limit=30）
5. `ls_drug_search`（获批药物，`highest_phase=approved`）
6. `mcp_web-search__web_search`（会议动态，按当月会议日历选词）

### Step 2A：BD交易模块处理
- 字段：`deal_title` / `deal_time` / `principle_organization` / `partner_organization` / `url`
- 链接：原始 `url` 字段优先；无则 `synapse.zhihuiya.com/news-detail/{deal_id}`
- 展示：全量展示（通常≤10笔），含双方公司、金额、交易类型标签

### Step 2B：临床结果模块处理
- 抓取：`ls_clinical_trial_result_search`（2页，共100条）
- 补充：对前8条调用 `ls_clinical_trial_result_fetch` 获取 `results[]` 原始数值
- **客观描述规范**：
  - 必填9字段：`trial_name` / `drug` / `target` / `indication` / `phase` / `sponsor_org` / `key_endpoints` / `publication_date` / `source_url`
  - 数字直接引用工具返回原始值；禁止"约"、"令人振奋"等修饰词
  - `results[]` 为空时标注"详细数据请点击来源链接查看"，禁止推测补填
  - 标题格式：`📊 临床结果（X条展示 / matched_total=Y条，日期范围）`
- 链接：`synapse.zhihuiya.com/clinical-result-detail/{ct_result_id}`
- 模块末尾必须生成**📋 本期临床结果小结**：数据范围/靶点列表/阶段分布/主要适应症

### Step 2C：新注册临床模块处理
- 精选8条（优先Ph3、知名企业、新靶点）
- 字段：`trial_title` / `phase` / `drug` / `target` / `indication` / `organization` / `clinical_trial_id`
- 链接：`synapse.zhihuiya.com/clinical-progress-detail/{clinical_trial_id}`

### Step 2D：专利模块处理
- 检索：`ls_patent_search`（`drug_type=["ADC"]`，严格锁定公开日期范围）
- 相关性过滤：标题/摘要须含 ADC / antibody-drug conjugate / 靶点名 / linker / payload 之一
- 非ADC专利（如机械/电力类）必须剔除，并在小结中注明剔除原因
- **客观描述规范**：
  - 技术标签仅从标题/摘要明确词汇提取，无法确认时标注"详见全文"
  - DAR值仅当权利要求/摘要明确数字时填写
  - 禁用表述："突破性专利"/"颠覆领域"/"极具商业价值"/"领先全球"
  - 推荐阅读使用7类维度代码：`NEW_TARGET` / `KEY_ASSIGNEE` / `TECH_CLASS` / `COMBO_THERAPY` / `PLATFORM_TECH` / `CLINICAL_RELEVANCE` / `GEOGRAPHY`
  - **AI技术三要素**：每件专利必须基于title+content提炼：技术问题 / 技术方案 / 技术效果（不可推测虚构）
- 卡片结构：专利号+法律状态+日期 → 标题 → 申请人（含国家）→ 技术标签 → 三要素 → 推荐原因 → 链接
- 模块末尾必须生成**📋 本期专利小结**：检索范围/技术分类/申请人地域/标题明确靶点/剔除说明
- 链接：`eureka.zhihuiya.com/view/#/fullText?patentId={id}`（id字段，非patent_id）

### Step 2E：获批药物模块处理
- 查询：`ls_drug_search`（`highest_phase=["approved"]`）
- 筛选：`first_approved_date` 在时间范围内的新批品种
- 字段：药物名/INN / 获批日期 / 公司（原研+持有）/ 靶点 / Payload类型 / Linker / DAR / 适应症
- 链接：`synapse.zhihuiya.com/drug-detail/{drug_id}`

### Step 3：三维去重频次统计
- 维度：靶点 / 公司 / 适应症
- 口径：同一来源内同一实体去重；跨来源（临床结果/临床试验/专利/BD/会议）频次累加
- 排除：未知/未披露/通用ADC等非具体实体
- 仅统计频次，不打分、不加权
- 统计说明框必须写明：监控范围/各来源采样量/matched_total/去重逻辑

### Step 4：权威会议模块
- 按当月日历判断相关会议（JPM=1月/AACR=4月/ASCO=5-6月/ESMO=9月/SABCS=12月/ASH=12月）
- 对进行中或刚结束的会议执行网络搜索抓取ADC相关摘要
- 标注来源可靠性：🟢高（多源一致）/ 🟡中（单源）/ ⚠️ Unverified（需原始摘要核实）
- 智慧芽数据库会议数据入库延迟约1-4周，需说明

### Step 5：趋势对比模块
- 与上期数据对比（如有）：临床数量↑↓ / BD金额↑↓ / 热门靶点变化 / 新涌现公司
- 无历史数据时标注"首期简报，无对比基准"

### Step 6：HTML报告渲染规范

#### 6.1 整体结构
```
报告头部（渐变横幅）
↓ 概览数据卡（7色分类，hover阴影）
↓ 执行摘要（双列网格，彩色竖线）
↓ 获批药物（绿色渐变背景，2×4参数网格）
↓ BD交易
↓ 临床结果（含小结）
↓ 新注册临床
↓ 专利精选（含三要素+小结）
↓ 靶点/公司/适应症可视化（彩色渐变横条图）
↓ 权威会议
↓ 趋势对比
↓ MCP工具统计面板（深色主题）
↓ 来源列表（分类展示）
```

#### 6.2 标签体系（8类，严格使用CSS class）
| 标签类型 | CSS类名 | 颜色 |
|---------|---------|------|
| 靶点 | `tag-target` | `#dbeafe / #1d4ed8` |
| Payload | `tag-payload` | `#dcfce7 / #15803d` |
| Linker | `tag-linker` | `#ede9fe / #6d28d9` |
| 适应症 | `tag-indication` | `#fef9c3 / #854d0e` |
| 公司 | `tag-company` | `#f1f5f9 / #374151` |
| 阶段 | `tag-phase` | `#f3e8ff / #7e22ce` |
| 地域 | `tag-geo` | `#ecfeff / #0e7490` |
| 推荐原因 | `tag-recommend` | `#4c1d95 / #ffffff` |

#### 6.3 紧凑卡片结构（所有模块统一）
- 内边距：`12px 14px`
- 标题行：实体名（粗体）+ badge群 + 日期（右对齐）
- 标签行：所有属性标签化，行内展示
- 数据框：仅原始数值，左侧彩色竖线
- 链接按钮：右下角，11px小字

#### 6.4 data-tags 规范
每张卡片 `data-tags` 属性必须包含：
`靶点（英文）/ 药物名 / 公司缩写 / 阶段 / 地域 / 技术类型 / 适应症关键词`

#### 6.5 搜索筛选框（3模块必须配置）
| 模块 | section id | 必配快捷筛选 |
|------|-----------|------------|
| 临床结果 | `section-clinical-results` | Phase 3 / HER2 / TROP2 / Positive |
| 新注册临床 | `section-clinical-trials` | Phase 3 / HER2 / 中国申请人 / NSCLC |
| 专利 | `section-patents` | HER2 / TROP2 / CN / Linker / Payload / WO |

JS函数：`filterCards(sectionId, query)` + `filterByTag(sectionId, tag)`，含计数实时更新。

### Step 7：链接校验
渲染前必须调用校验函数，禁止以下格式进入最终HTML：
- `clinical-results-detail`（多s）
- `clinical-trial-result-detail`（多trial）
- `clinical-trial-detail`（路径错误）
- `fulltext?patentid=`（大小写错误）
- `patent_id=`（下划线错误）

### Step 8：来源标记规范
参见 `references/zhihuiya_link_standard.md`，所有条目必须按分类展示：
1. 专利/论文证据
2. 智慧芽结构化数据（临床结果/临床试验/药物/BD交易）
3. 公开网页证据（标注Unverified）

---

## 输出文件命名规范

| 场景 | 文件名格式 |
|------|----------|
| 月度简报 | `adc_brief_YYYYMM.html` |
| 周度简报 | `adc_brief_week_YYYYWW.html` |
| 自定义范围 | `adc_brief_{date_from}_{date_to}.html` |

---

## 常见问题排查

| 问题 | 解决方案 |
|------|---------|
| 专利出现非ADC结果 | 执行标题关键词过滤；剔除并在小结注明 |
| 临床结果含主观评价 | 删除修饰词，仅保留工具返回原始数值 |
| 专利推荐理由夸大 | 改用7类维度代码对应的客观表述模板 |
| 链接无法打开 | 运行 `validate_zhihuiya_links()` 定位错误格式 |
| 搜索筛选不生效 | 检查 `data-tags` 是否包含目标关键词 |
| 标签未显示 | 检查 tag class 名与 CSS 定义是否一致 |
| `ls_news_vector_search` 返回空 | 切换至 `ls_financial_report_vector_search` 作为备用 |
| 会议数据智慧芽未入库 | 用网络搜索补充，标注Unverified，说明入库延迟原因 |
| 数字前后期不一致 | 检查时间过滤参数是否严格锁定，排查历史数据混入 |

---

## 引用的参考文档

- `references/zhihuiya_link_standard.md`：智慧芽链接规范（所有链接生成必须遵循）
- `references/adc_conference_calendar.md`：ADC领域权威会议日历
- `references/adc_target_glossary.md`：ADC靶点标准命名参照表

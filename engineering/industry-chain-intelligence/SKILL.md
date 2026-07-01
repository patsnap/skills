---
name: industry-chain-intelligence
description: |
  企业决策者产业链战略报告系统。面向企业CEO/CTO/战略总监，输入公司名称或产业链，
  一键生成10页白皮书风格HTML报告，涵盖产业链定位、上游卡脖子风险、下游市场格局、
  技术竞争态势、科创力雷达、趋势机会及行动路线图。
  视觉风格严格遵循 coolingstyle_v2_whitepaper.html 白皮书 DNA：象牙白底、深海军蓝标题、
  朱红强调、古金装饰、Noto Serif/Sans/Roboto Mono 字体三件套、960px宽/52px页边距。
  数据通过智慧芽MCP实时获取，图表默认统计范围2012-当前年月。
---

# 企业决策者产业链战略报告系统

## 角色定位

你是一位兼具**产业经济学家**、**技术战略顾问**与**数据可视化工程师**三重能力的分析系统。
受众是企业最高决策层（CEO/CTO/战略总监），报告须达到**政府红头文件**的权威感与
**贝恩/麦肯锡白皮书**的精炼美学。任何模糊表述、无来源结论均不可出现。

> **视觉黄金法则**：严格遵循 `coolingstyle_v2_whitepaper.html` 样式，使用象牙白底`#FCFAF2`
> 页面背景、古金边框装饰、朱红强调色，禁止使用纯白底`#FFFFFF`+灰色画布旧版风格。

---

## 触发词

用户说以下任意内容时启动本技能：
- "帮我分析 XX 公司的产业链"
- "生成 XX 产业链战略报告"
- "XX 公司产业链定位 / 上游风险 / 竞争分析"
- "一键报告 / 战略研判报告"
- 单独输入公司名称 + "产业链"
- 单独输入公司名称（结合上下文判断）

---

## 五阶段工作流

### Phase 0 · 输入解析（≤5s）

1. 识别实体类型：上市公司 / 私有企业 / 产业链泛名称
2. 调用 `industry_tech_chain` MCP 获取产业链归属节点
3. 若无法识别，输出澄清问句（仅问一次）
4. 确定报告编号：`ZSC-{YYYY}-{MMDD}`，密级默认"内部材料 · 核心级"

---

### Phase 1 · 并行数据采集（≤30s）

同步调用以下 MCP / API（任意接口失败不中断流程，对应模块标注"数据暂缺"）：

| 数据源 | MCP工具 | 用途 |
|--------|---------|------|
| 产业技术链 | `industry_tech_chain` | 产业链全景、节点专利量、位置定位 |
| 企业科创评分 | `company_strategy_map` + `company_key_technology` | 科创力评级AAA-CCC |
| 专利趋势 | `trends` + `company_patent_trends` | 近5年申请趋势 |
| 竞争格局 | `applicant_ranking` + `company_portfolio_overview` | Top5竞争对手 |
| 被引分析 | `most_cited` + `company_most_cited_latest` | 专利质量/引用率 |
| 法律状态 | `simple_legal_status` + `company_simple_legal_status` | 有效专利占比 |
| 技术词云 | `word_cloud` + `company_word_cloud` | 技术热点 |
| 旭日图 | `wheel_of_innovation` | 技术层级分布 |
| 发明人 | `inventor_ranking` | 核心研发人才（用于P5人才引进目标） |
| 专利价值 | `portfolio_value` | 专利价值分布 |
| 技术效果 | `technology_effect_distribution` + `company_tech_effect_dist` | 功效聚类（P6） |

**数据时间范围**：默认 2012-01-01 至当前年月
**标注规范**：每图表底部标注"数据来源：智慧芽，截至{当前年月}"

---

### Phase 2 · 结构化分析（LLM推理）

基于采集数据，依次生成10页分析内容，每页均须：
- **有据可查**：每项结论绑定数据字段或检索结果，标注 `[S#]`
- **量化为主**：百分比、绝对值、排名、评级优先于定性描述
- **风险分级**：红色=高风险、橙色=中风险、绿色=低风险（严格三级）
- **竞争对比**：本公司数据永远对比行业均值或Top3均值

---

## 10页固化内容结构（基于 coolingstyle_v2_whitepaper.html 精确版）

---

### P1 · 封面页

**固定组件（必须全部出现）：**
- `cover-top-bar`（3px朱红横线，负margin延伸全宽）
- `cover-gold-bar`（1px古金横线，负margin延伸全宽）
- `cover-classification`：行内框显示"内部材料 · 核心级"（朱红边框）
- `cover-meta`（flex横排4项）：报告编号 ZSC-YYYY-MMDD / 日期 / 数据截至 / 版本号
- `cover-title-eyebrow`（朱红mono小字大间距）："产业链战略研判报告"
- `cover-company`（serif 28px navy粗体）：公司全称
- `cover-report-title`（serif 20px）：《XX产业链战略研判报告》
- `cover-divider`：渐变金色横线
- `cover-findings`：核心结论摘要区
  - h4小标题（mono灰色大写间距）
  - 5条finding-item，每条含 `finding-num`（古金mono加粗）+ 摘要文字 + `[S#]` 来源标注
  - 结论01：专利总量/有效量/有效率/当年申请量/研发趋势判断
  - 结论02：核心IPC双核驱动或主要技术方向占比
  - 结论03：最高被引专利编号+被引次数+技术描述
  - 结论04：国际化/PCT布局状态（如为0则明确标注战略短板）
  - 结论05：核心技术效果词条+对应赛道战略价值
- `cover-strategy`（古金左竖线+浅金背景+serif斜体）：3句战略总建议，含近/中期方向

---

### P2 · 产业链全景与定位

**固定组件：**
- 页眉：`page-header`（公司名+报告编号）
- `section-num`：灰色48px mono大字 "02"
- `section-eyebrow`："Supply Chain Panorama"
- `section-title`（serif navy，下边朱红2px线）："产业链全景与定位"

**图1：产业链横流图 SVG**（viewBox 860×160）
- 4个节点块：上游（浅蓝背景`#F4F2EA`+朱红边框）/ 中游（浅金背景+古金边框）/ 本公司Target（深海军蓝背景+古金文字+星号）/ 下游（浅绿背景+绿边框）
- 延伸机会节点（浅蓝背景+navy虚线边框）
- 每个节点内：标题（加粗+色彩标识）+ 3行产品/技术内容 + 底部利润率/风险/CAGR小字
- 上游节点底部必须标注"⚠ 高卡脖子风险"（朱红）
- 箭头用 `<marker>` 定义灰色箭头，最后段用虚线表示延伸方向
- 图注+来源标注

**表1：产业链归属节点分布**（`data-table`）
- 三列：产业链名称 / 节点描述 / 专利数（tag标签）
- 来自 `industry_tech_chain` 实际数据

**右栏：**
- `insight-box gold`：利润池定位洞察（3句话：定位层级+成本压力来源+延伸路径）
- `kpi-row cols-3`：有效专利数（ok绿）/ 当年申请量（gold）/ 国际布局数（danger红）

---

### P3 · 上游供应链深度溯源（v2.0强化版）

**固定组件：**
- 页眉、`section-num` "03"、`section-eyebrow` "Upstream Intelligence"
- `section-title`："上游供应链深度溯源与卡脖子替代方案"

**图2：三级逆推链路 SVG**（viewBox 860×200）
- L0本公司节点（navy背景，居中）
- L1：4个上游节点（高风险朱红边框 / 中风险古金边框 / 低风险绿边框）
- L2：各L1节点下方的二级供应商节点，标注海外集中度或国产替代率
- 高风险节点（⚠+供应商名称+海外集中度%）：`#FDEAEA`背景+朱红边框
- 中风险节点（国产替代率%）：`#FDF8EC`背景+古金边框
- 低风险节点（替代可行性强）：`#EDFAED`背景+绿边框
- 连线用浅灰色虚线

**左栏：图3 关键材料国产化率进度条**
- 每项：`progress-item` = 物料名 + 百分比数字 + 进度条（fill-ok绿 / fill-warn橙 / fill-danger红）
- 5项物料，从高到低排列
- 底部标注"进度条为行业均值估算，非企业实际采购数据 · Unverified"

**右栏：🆕 v2.0 卡脖子节点 · 国产替代供应商匹配（3张 `supplier-card`）**
- 每张卡片包含：
  - `supplier-header`：供应商名称（navy加粗）+ 替代度★评级（tag标签）
  - `supplier-meta`：节点归属 + TRL成熟度等级
  - `supplier-action`：🔧 **本周可行动：** 具体联系建议/样品申请/最小起订量
- 三家供应商对应三个不同卡脖子节点（压缩机/制冷剂/阀门）
- TRL等级说明：9=成熟商用，7=准商用，6=小批量

---

### P4 · 专利布局与技术竞争全景

**固定组件：**
- 页眉、`section-num` "04"、`section-eyebrow` "Patent Landscape"
- `section-title`："专利布局与技术竞争全景"

**KPI行（`kpi-row cols-4`）：**
- 总申请量（默认border-left朱红）
- 有效专利数（ok绿）
- 当年申请量（gold，含授权率）
- PCT国际数（如为0则danger红色数字）

**图4：专利申请年度趋势柱状图 SVG**（viewBox 820×160）
- 无背景网格，基线水平线
- Y轴仅标注数值（灰色mono小字）
- 每年一根柱，navy色主柱
- 早期低申请量年份用古金半透明色区分
- **2024爆发年（或当年最高年）**：朱红色柱 + `★` 标注 + 红色加粗年份 + 右侧"XX年爆发"小红标签框
- 2026进行中年份：navy低透明度 + `4*` + "（进行中）"说明
- 底部标注数据来源+[S#]

**两栏：**
左栏：**图5 IPC技术领域分布 Top8表格**（`data-table`）
- 四列：IPC代码（navy mono）/ 技术方向 / 件数 / 占比（tag标签）
- 前两位IPC用 `tag-red` 高亮，中间用 `tag-gold`，其余用 `tag-grey`

右栏：**表2 高被引专利 TOP5**（`data-table`）
- 三列：专利号（mono小字）/ 主题描述 / 被引次数（tag标签）
- 第1位用 `tag-red`，第2-3位用 `tag-navy`，后续用 `tag-grey`
- 底部 `insight-box`：针对最高被引专利的续缴/衍生发明建议

---

### P5 · 科创力雷达 · 战略短板与人才引进目标（v2.0强化版）

**固定组件：**
- 页眉、`section-num` "05"、`section-eyebrow` "Innovation Radar"
- `section-title`："科创力雷达 · 战略短板与人才引进目标"

**两栏：**

**左栏：图6 科创力六维/八维雷达图 SVG**（viewBox 300×280）
- 同心多边形背景网格（stroke `#E0DDD4`）+ 轴线
- 实际数据多边形：朱红实线+20%透明朱红填充
- 数据维度（来自 `company_strategy_map`）：
  - 增长速度% / 专利复杂度% / 专利影响力% / 当前相关性% / 共同申请% / 国际化% / 科学含量%
  - **国际化%、科学含量%** 如为0或极低：轴标签加朱红色+`⚠`警示
- 雷达下方评分表（`data-table`，3列：维度/得分%/状态tag）
  - 良好：`tag-green`，中等：`tag-gold`，偏低：`tag-grey`，空白：`tag-red` + `⚠`

**右栏：**
- `insight-box navy`：核心差距定向分析（2条短板+补足路径，含具体工具如PCT/产学研）
- **🆕 v2.0 差距维度 · 人才引进目标清单（3张 `supplier-card`）**
  - 卡片1（`tag-red` P0优先级）：目标维度"国际化+PCT布局"
    - 所需专长：PCT申请经验、海外专利撰写
    - 👤 建议引进方向：有海外工作经历的同行业专利工程师（参考竞争对手/头部企业）
    - 🎯 HR行动：具体季度+猎头委托标准（有效PCT案件数量门槛）
  - 卡片2（`tag-gold` P1优先级）：目标维度"科学含量提升"
    - 所需专长：相关领域博士背景
    - 👤 参考案例：已有学术合作先例（如有）可复制，推荐华南高校/对口研究所
    - 🎯 HR行动：联合培养博士生申请/横向课题合作渠道
  - 卡片3（`tag-grey` P2优先级）：目标维度"共同申请提升"
    - 当前共同申请率+行业均值对比
    - 👤 策略：与主要客户开展技术联合开发
    - 🎯 BD行动：目标年度联合专利件数/签约时间

---

### P6 · 技术效果图谱 + 竞争专利到期窗口（v2.0强化版）

**固定组件：**
- 页眉、`section-num` "06"、`section-eyebrow` "Tech Effect & Patent Expiry"
- `section-title`："技术效果图谱 + 竞争专利到期窗口"

**两栏：**

**左栏：图7 核心技术效果分布**（`progress-item` 条形列表，来自 `company_tech_effect_dist`）
- 8项效果词条，从最高件数到最低
- 颜色：高频（fill-ok绿）/ 中频（fill-warn橙/黄）
- 最大值=100%基准，相对宽度
- 底部 `insight-box gold`：产品策略洞察（3个高频效果词组合揭示核心价值主张+最契合赛道）

**右栏：🆕 v2.0 竞争专利到期窗口（未来24个月内，`data-table`）**
- 四列：专利号（mono朱红）/ 主题摘要 / 预计到期月（tag标签）/ 行动建议
- 排序：最近到期在前
- 到期月tag颜色：未来6个月=`tag-red`，6-12个月=`tag-gold`，12-24个月=`tag-grey`
- 行动建议图标：
  - 📌 本季度启动改进版专利布局
  - 🔍 评估年费续缴价值
  - ✅ 高被引专利，优先续缴
- 底部说明："到期时间基于申请年计算，实际以国家知识产权局为准 · Unverified"
- `insight-box`：研发行动提示（提及最近到期专利件数+建议本季度启动布局）

---

### P7 · 下游市场机遇 · 政府培育 & 精准对接（v2.0强化版）

**固定组件：**
- 页眉、`section-num` "07"、`section-eyebrow` "Downstream Market"
- `section-title`："下游市场机遇 · 政府培育 & 精准对接"

**三栏市场赛道卡（`three-col`）：**
每栏格式：
- 顶部3px色线（赛道A=朱红 / 赛道B=古金 / 赛道C=navy）
- mono小字赛道标签（"赛道 A · [名称]"）
- 大号mono数字：CAGR%
- muted小字：CAGR来源时间段
- 12px正文：专利布局基础 + 目标客户类型
- 底部tag组合（高优先级/高成长/高溢价 + IP壁垒/技术匹配度/进入门槛）

**🆕 v2.0 专精特新/隐形冠军候选名单（`data-table`，5列）：**
- 列：评估维度 / 当前表现 / 专精特新达标线 / 缺口（tag）/ 政府支持路径
- 5项维度（必须覆盖）：
  1. 知识产权数量 → 与国家专精特新小巨人标准对比（≥5件）
  2. 高新技术企业认定 → 已获/未获状态
  3. 研发投入强度 → ≥3%营收，待核实则标"待确认"
  4. 国际化布局 → PCT数量，不足则`tag-red` ⚠
  5. 细分领域市占率 → 待核实则标"待确认"
- 缺口列：`tag-green`✅达标 / `tag-gold`待确认 / `tag-red`⚠不足
- 底部 `insight-box navy`：政府对接建议（直接可交科技局使用，含培育条件判断+重点支持方向）

---

### P8 · 技术热点词云 · 机会四象限

**固定组件：**
- 页眉、`section-num` "08"、`section-eyebrow` "Technology Trends & Opportunities"
- `section-title`："技术热点词云 · 机会四象限"

**图8：技术关键词词云（div模拟）**
- 背景：`bgalt`色块，`border-radius:4px`，居中文字布局
- 关键词字号梯度（32px最大→9px最小）+ 颜色：navy/朱红/古金/gray/green混用
- 来自 `company_word_cloud` 数据，Top20-25关键词

**图9：技术机会四象限 SVG**（viewBox 760×280）
- X轴=市场潜力，Y轴=专利成熟度
- 4个象限背景色块（半透明）：
  - 左上"⏰ 战略储备区"（浅金`#FEF9F0`）
  - 右上"⭐ 重点突破区"（浅绿`#EBF7EB`）
  - 左下"维持区"（浅灰）
  - 右下"🚀 当前优势区"（浅蓝`#F0F4FF`）
- 当前优势区：本公司核心产品（navy大圆）+ 相邻延伸（朱红中圆）
- 重点突破区：高成长赛道（绿中圆）+ 新兴赛道（金小圆）
- 战略储备区：长期蓄力方向（金小圆/灰小圆）
- 从"当前优势"到"重点突破"画虚线延伸路径+标注文字

---

### P9 · 竞争生态与合作伙伴五维互补评估（v2.0强化版）

**固定组件：**
- 页眉、`section-num` "09"、`section-eyebrow` "Competitive Ecosystem"
- `section-title`："竞争生态与合作伙伴五维互补评估"

**两栏：**

**左栏：表3 主要竞争对手清单（`data-table`，4列）**
- 列：企业名称 / 定位描述 / 威胁等级（tag-red高/tag-gold中/tag-grey低）/ 重叠度描述
- 5家竞争对手，按威胁等级降序
- 底部 `insight-box`：竞争护城河评估（指明本公司在细分市场（如100W以下微型）的差异化优势）

**右栏：🆕 v2.0 潜在合作伙伴五维互补评分（3张 `supplier-card`）**
- 每张卡片包含：
  - `supplier-header`：合作方名称 + 综合互补★评级（tag-navy/tag-green/tag-gold）
  - 五维评分grid（5列，每格独立背景色）：
    - **技术**（navy背景=高/灰背景=低）/ **渠道**（green背景=高/灰=低）/ **IP共创**（navy背景）/ **资源**（green背景）/ **风险**（风险越低越好：green低/yellow中/red高）
    - 评分0-100，mono加粗，下方维度名称（muted小字）
  - `supplier-action`：🤝 **合作建议：** 具体合作形式+目标产出（联合专利数/认证时间/渠道价值）
- 三家合作方代表三种类型：学术机构 / 下游客户（大厂采购）/ 平台型合作（渠道互补）

---

### P10 · 战略行动路线图 v2.0（三色预算标签+责任人）

**固定组件：**
- 页眉、`section-num` "10"、`section-eyebrow` "Strategic Roadmap v2.0"
- `section-title`："战略行动路线图 · 预算分级 · 责任人到位"

**两栏：**

**左栏：时间轴（`timeline`）**

短期行动（0–12个月）- 标题行（mono灰小字）：
- 行动1（`tl-dot red`）：专利到期更新+改进型布局
  - 时间：当年Q3/Q4 · 立即启动
  - `tl-title`：具体行动名称
  - `tl-desc`：具体专利号+行动内容
  - `tl-tags`：`budget-tag budget-green` 🟢 &lt;50万·3个月内 + `tag-grey`责任人：专利总监
- 行动2（`tl-dot red`）：供应商资质认证（卡脖子优先级最高节点）
  - `budget-tag budget-green` 🟢 &lt;10万·2个月内 + 责任人：采购总监
- 行动3（`tl-dot gold`）：产学研合作立项
  - `budget-tag budget-yellow` 🟡 50-200万·合同签约 + 责任人：技术总监/CEO
- 行动4（`tl-dot gold`）：政府补贴/出海/PCT申请启动
  - `budget-tag budget-green` 🟢 政府补贴覆盖70%成本 + 责任人：战略总监

中期行动（1–3年）- 标题行：
- 行动5（`tl-dot navy`）：行业主流客户Tier2认证
  - `budget-tag budget-yellow` 🟡 200-500万·认证+研发 + 责任人：CEO+市场总监
- 行动6（`tl-dot navy`）：国家专精特新小巨人申报
  - `budget-tag budget-red` 🔴 需董事会支持·战略级 + 责任人：CEO+政府关系

**右栏：图10 行动项优先级矩阵 SVG**（viewBox 360×240）
- 4象限：投入（Y轴高到低）× 战略价值（X轴低到高）
- 右上=立即执行（高价值高投入）/ 右下=高效低投入 / 左上=中期规划 / 左下=暂缓
- 6个数据点（对应6条行动项），标注简短行动名称
- 底部 `insight-box navy`：**CEO决策建议三级分类**
  - 🟢 **本月可批复（无需董事会）：** 具体行动名列举
  - 🟡 **下季度列入预算：** 具体行动名+预算区间
  - 🔴 **年度战略会议决策：** 具体行动名

**免责声明（固定末尾）：**
```
本报告基于智慧芽专利数据库生成，相关数据截至[当前年月]。专利到期时间为估算值，实际以国家知识产权局公告为准。供应商匹配、市场增速、利润率区间为综合分析与估算，标注"Unverified"项目需企业自行核实。本报告不构成任何投资建议，企业决策需结合实际情况综合判断。
数据来源：智慧芽（PatSnap），截至[当前年月] · 报告编号：ZSC-YYYY-MMDD
```

---

## 视觉规范 — v2.0 白皮书 DNA（固化自 coolingstyle_v2_whitepaper.html）

### CSS变量体系

```css
:root {
  --red:    #C02F2F;   /* 朱红     - 封面线/高风险/洞察框竖线/朱红强调 */
  --gold:   #C6A86B;   /* 古金     - 装饰/年份色/封面分割线/古金强调 */
  --navy:   #1C2F4E;   /* 深海军蓝 - 章节标题/表头/target节点/主数据 */
  --ink:    #2B2B2B;   /* 正文墨色 */
  --ivory:  #FCFAF2;   /* 象牙白   - 页面底色 */
  --bgalt:  #F4F2EA;   /* 背景交替色 */
  --muted:  #6B7280;   /* 静默灰   - 次要说明/图题编号/来源注释 */
  --border: #E0DDD4;   /* 边框色   - 表格分隔/KPI边框 */
  --ok:     #2E7D32;   /* 成功绿   - 达标/低风险 */
  --warn:   #C66B00;   /* 警告橙   - 中风险/待确认 */
  --danger: #C02F2F;   /* 危险红   = --red */
  --font-serif: 'Noto Serif SC', 'Georgia', serif;
  --font-sans:  'Noto Sans SC', 'Helvetica Neue', sans-serif;
  --font-mono:  'Roboto Mono', 'Courier New', monospace;
}
```

### 布局规范

- **页面容器**：`width:960px; background:var(--ivory); margin:32px auto; padding:52px; box-shadow:0 2px 12px rgba(0,0,0,.08)`
- **页面外框背景**：`body { background:#E8E8E8 }` — 灰色画布衬托象牙白纸张
- **页眉**：`display:flex; justify-content:space-between; border-bottom:1px solid var(--border); padding-bottom:10px; margin-bottom:36px; font-size:11px; font-family:var(--font-mono)`
- **页脚**：`display:flex; justify-content:space-between; border-top:1px solid var(--border); padding-top:10px; margin-top:36px; font-size:10px`

### 核心组件 CSS（精确类名，来自 v2.0 HTML）

```css
/* 封面 */
.cover-top-bar         { height:3px; background:var(--red); margin:-52px -52px 0 -52px; }
.cover-gold-bar        { height:1px; background:var(--gold); margin:0 -52px 40px -52px; }
.cover-classification  { border:1px solid var(--red); color:var(--red); font-size:10px; padding:2px 8px; font-family:var(--font-mono); letter-spacing:2px; margin-bottom:16px; }
.cover-meta            { display:flex; gap:24px; font-size:11px; color:var(--muted); font-family:var(--font-mono); margin-bottom:40px; }
.cover-meta span       { border:1px solid var(--border); padding:3px 10px; }
.cover-title-eyebrow   { font-size:11px; letter-spacing:3px; color:var(--red); text-transform:uppercase; font-family:var(--font-mono); margin-bottom:8px; }
.cover-company         { font-family:var(--font-serif); font-size:28px; font-weight:700; color:var(--navy); line-height:1.3; margin-bottom:6px; }
.cover-report-title    { font-family:var(--font-serif); font-size:20px; color:var(--ink); margin-bottom:32px; }
.cover-divider         { height:1px; background:linear-gradient(90deg,var(--gold),transparent); margin-bottom:28px; }
.finding-num           { font-family:var(--font-mono); color:var(--gold); font-weight:700; min-width:20px; }
.cover-strategy        { background:var(--bgalt); border-left:3px solid var(--gold); padding:14px 18px; font-family:var(--font-serif); font-size:13px; color:var(--navy); font-style:italic; }

/* 章节标题 */
.section-num           { font-size:48px; font-family:var(--font-mono); color:var(--border); line-height:1; margin-bottom:4px; }
.section-eyebrow       { font-size:10px; letter-spacing:3px; text-transform:uppercase; color:var(--red); font-family:var(--font-mono); margin-bottom:6px; }
.section-title         { font-family:var(--font-serif); font-size:22px; font-weight:700; color:var(--navy); border-bottom:2px solid var(--red); padding-bottom:8px; margin-bottom:24px; }

/* KPI卡 */
.kpi-row.cols-4        { display:grid; grid-template-columns:repeat(4,1fr); gap:16px; }
.kpi-row.cols-3        { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }
.kpi-card              { background:var(--bgalt); border-left:3px solid var(--red); padding:14px 16px; border-radius:0 4px 4px 0; }
.kpi-card.gold         { border-left-color:var(--gold); }
.kpi-card.navy         { border-left-color:var(--navy); }
.kpi-card.ok           { border-left-color:var(--ok); }
.kpi-value             { font-size:24px; font-family:var(--font-mono); font-weight:700; color:var(--navy); }

/* 洞察框 */
.insight-box           { background:#FEF2F2; border-left:3px solid var(--red); padding:14px 18px; margin:20px 0; font-size:13px; }
.insight-box.gold      { background:#FDFBF4; border-left-color:var(--gold); }
.insight-box.navy      { background:#F0F4F8; border-left-color:var(--navy); }

/* 数据表格 */
.data-table thead tr   { background:var(--navy); color:#fff; }
.data-table td         { padding:8px 12px; border-bottom:1px solid var(--border); }
.data-table tbody tr:nth-child(even) { background:var(--bgalt); }

/* Tag徽标 */
.tag-red               { background:#FDEAEA; color:var(--red); }
.tag-gold              { background:#FDF8EC; color:#8B6914; }
.tag-green             { background:#EDFAED; color:var(--ok); }
.tag-navy              { background:#EBF0F7; color:var(--navy); }
.tag-grey              { background:#F0F0F0; color:#555; }

/* 进度条 */
.progress-bar          { height:8px; background:#E8E6DE; border-radius:4px; }
.fill-ok               { background:var(--ok); }
.fill-warn             { background:var(--warn); }
.fill-danger           { background:var(--danger); }

/* 横向条形图 */
.bar-row               { display:flex; align-items:center; margin-bottom:10px; gap:10px; }
.bar-label             { font-size:12px; color:var(--gray); width:120px; text-align:right; }
.bar-track             { flex:1; height:20px; background:#F0F0F0; }
.bar-fill.primary      { background:var(--navy); }
.bar-fill.accent       { background:var(--red); }

/* 供应商/人才匹配卡 */
.supplier-card         { background:var(--bgalt); border:1px solid var(--border); border-radius:4px; padding:14px 16px; margin-bottom:12px; }
.supplier-header       { display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; }
.supplier-name         { font-weight:600; color:var(--navy); font-size:13px; }
.supplier-meta         { display:flex; gap:12px; font-size:11px; color:var(--muted); margin-bottom:6px; }
.supplier-action       { font-size:12px; border-top:1px solid var(--border); padding-top:8px; margin-top:8px; }

/* 预算标签 */
.budget-tag            { display:inline-flex; align-items:center; gap:5px; font-size:11px; padding:3px 10px; border-radius:12px; font-family:var(--font-mono); }
.budget-green          { background:#EDFAED; color:var(--ok); }
.budget-yellow         { background:#FDF8EC; color:var(--warn); }
.budget-red            { background:#FDEAEA; color:var(--danger); }

/* 时间轴 */
.timeline::before      { content:''; position:absolute; left:10px; top:0; bottom:0; width:2px; background:var(--border); }
.tl-dot.red            { border-color:var(--red); background:#fff; }
.tl-dot.gold           { border-color:var(--gold); background:#fff; }
.tl-dot.navy           { border-color:var(--navy); background:#fff; }

/* 页码 */
.page-num              { font-family:var(--font-mono); color:var(--gold); font-weight:500; }
```

### v2.0 新增组件

| 组件 | 用途 | 页面 |
|------|------|------|
| `supplier-card` | 供应商/合作伙伴/人才卡片 | P3/P5/P9 |
| `budget-tag budget-green/yellow/red` | 🟢🟡🔴三色预算标签 | P10 |
| 五维评分grid（5列inline-grid） | 合作伙伴五维互补 | P9 |
| 专利到期窗口表（4列data-table） | 竞争到期窗口 | P6 |
| 专精特新候选表（5列data-table） | 政府对接模块 | P7 |

### 严格禁止列表

| 禁止项 | 替代方案 |
|--------|---------| 
| 纯白 `#FFFFFF` 作页面背景 | 象牙白 `#FCFAF2`（var(--ivory)） |
| 纯白 `#FFFFFF` 作KPI/卡片背景 | `#F4F2EA`（var(--bgalt)） |
| 彩色KPI卡背景 | `bgalt` + 朱红/古金/navy左竖线区分 |
| 背景网格线 | 全部图表无网格，直接标注数值 |
| 阴影装饰圆/光晕效果 | 简洁边框+node类型色 |
| 彩色饼图图例 | stack-bar 或 SVG环图 + 外侧引线 |

---

### Phase 3 · HTML渲染

调用 `scripts/generate_report.py` 渲染最终HTML。

---

### Phase 4 · 输出交付

在对话中输出：
1. 报告摘要（5条核心结论，Markdown格式）
2. HTML文件链接（可点击预览）
3. 数据来源列表（[S1]-[S#]）
4. 提示："报告已生成，支持在浏览器中打印为PDF"

---

## 错误处理规范

| 错误类型 | 处理方式 |
|---------|---------| 
| MCP接口超时 | 对应模块显示"数据暂缺，请稍后重试" |
| 公司名称无法识别 | 输出澄清问句：候选公司名称列表 |
| 数据覆盖不足 | 标注实际数据截止日期 |
| HTML渲染失败 | 降级输出Markdown格式报告 |

---

## 输出质量检查清单（内部自查）

### 样式检查（v2.0 白皮书风格）
- [ ] 页面底色象牙白 `#FCFAF2`，body背景 `#E8E8E8`
- [ ] 封面：`cover-top-bar`(3px朱红) + `cover-gold-bar`(1px古金) 双线
- [ ] 封面：5条finding-item，每条有`finding-num`古金数字
- [ ] 章节标题：48px灰色mono大数字 + 朱红眉标 + serif h2 + 2px朱红底线
- [ ] 每页有页眉（公司名+报告编号）+ 页脚（来源+古金页码）
- [ ] `insight-box`：朱红/古金/navy三色变体正确使用
- [ ] `kpi-card`：`bgalt`背景 + 左竖线颜色区分状态
- [ ] `supplier-card`：P3供应商匹配/P5人才引进/P9合作伙伴 各3张
- [ ] `budget-tag`：P10时间轴每条行动项均有🟢🟡🔴标签+责任人
- [ ] P10底部有CEO三级决策建议框（`insight-box navy`）
- [ ] 所有图表扁平化，无背景网格线
- [ ] 免责声明在P10末尾，含报告编号

### 内容检查
- [ ] 10页结构完整，无缺页（P1封面~P10路线图）
- [ ] 每页至少1个图表或可视化元素
- [ ] v2.0落地模块全部到位：P3供应商卡/P5人才卡/P6到期窗口/P7专精特新/P9五维评分/P10预算标签
- [ ] 所有数字有数据来源绑定（[S#]标注）
- [ ] 封面有5条摘要（finding-num 01-05），古金色编号
- [ ] 页码连续（1-10），格式"- X -"古金色

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。

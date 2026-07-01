# 21小节填充规范

> **使用说明**：为每个小节定义：①输入数据（从哪个变量获取）②HTML结构（使用哪些CSS类）③强制元素（不可省略的内容）④填充示例。
> 生成报告时，按本节规范从`data`字典中提取数据，填入HTML骨架模板的对应位置。

---

## 【强制】结论框内联来源标记 `[S#]` 规范

**每条结论 `<li>` 的末尾必须包含 `[S#]` 标记**，没有 `[S#]` 的 `<li>` 结论视为 Unverified。

| 标记 | 含义 | 适用场景 |
|------|------|----------|
| `[S1]` | 企业情报（官网/工商/百科） | 成立时间、总部、注册资本、经营范围等基本信息 |
| `[S2]` | 企业年报/财报 | 营收、净利润、业务板块、客户信息等财务数据 |
| `[S3]` | PatSnap智慧芽专利数据库 | 专利数量、法律状态、价值、发明人、技术分类等专利数据 |
| `[S4]` | 行业报告/技术趋势 | 技术演进、竞品对标、产业梯队、前瞻方向等 |
| `[S5]` | 综合推导/分析师判断 | SWOT结论、缺口分析、策略建议、行动方案等 |

**格式**：`<li>结论文本 [S#]</li>`（`[S#]` 紧贴 `</li>` 前，与文本之间一个空格）

**示例**：
```html
<li>公司拥有519件全球专利，有效专利100件 [S3]</li>
<li>2025年实现营业收入约66.08亿元 [S2]</li>
<li>压缩机技术是核心优势，占专利总量52% [S5]</li>
```

---

## 全局数据字典结构（`data`）

```python
data = {
    # 封面页
    'company_en': '', 'company_cn': '', 'report_date': '',
    'data_source': '', 'data_source_hint': '',

    # 第一节（从企业情报获取）
    'sec1': { 'kpi_list': [], 'intro_text': '', 'conclusion': [] },

    # 第二节（从PatSnap名称变体获取）
    'sec2': { 'basic_info': [], 'name_variants': [], 'conclusion': [] },

    # 第三节（从企业年报+业务分析获取）
    'sec3': { 'curves': [], 'products': [], 'conclusion': [] },

    # ... 每小节对应一个字典
}
```

---

## 第一节：企业全景概述与核心KPI

**输入数据**：`data['sec1']`

**HTML结构**：
```html
<div class="section-title">一、企业全景概述与核心KPI</div>
<span class="section-subtitle">📊 适用场景：企业概览与核心KPI速览 &nbsp;|&nbsp; 关注角色：管理层、IP负责人、外部顾问</span>
<div class="kpi-grid">
  <!-- 12个kpi-card，4列×3行 -->
  <!-- 顺序：公司全称/成立时间/公司前身/总部位置/上市状态/最近一年营收/最近一年净利润/全球专利总量/当前有效专利/发明专利申请/授权发明/PCT国际申请 -->
</div>
<!-- 2-3段企业简介 -->
<div class="conclusion-box">...</div>
```

**强制元素**：
- [ ] 12格KPI网格（`.kpi-grid`包含12个`.kpi-card`）
- [ ] 营收标签格式：`最近一年营收（YYYY）`和`最近一年净利润（YYYY）`
- [ ] 2-3段企业简介文字
- [ ] 黄色结论框（`.conclusion-box`）含`本小节结论：`+`<ol>`（每条`<li>`末尾须含`[S#]`标记）+`.source-hint`

**数据字段**：
| 字段 | 来源 | 格式 |
|------|------|------|
| `kpi_list` | 企业情报+专利统计 | 12项字典列表：`{'label': '...', 'value': '...'}` |
| `intro_text` | 企业情报 | 2-3段HTML段落 |
| `conclusion` | 综合分析 | 3-5条字符串列表 |

---

## 第二节：企业基本信息与名称变体检索清单

**输入数据**：`data['sec2']`

**HTML结构**：
```html
<div class="section-title">二、企业基本信息与名称变体检索清单</div>
<span class="section-subtitle">🔍 适用场景：企业背景调查、名称防漏检核验 &nbsp;|&nbsp; 关注角色：IP部门、尽职调查人员</span>
<div class="two-col">
  <div><!-- 左：基本信息表格 --></div>
  <div><!-- 右：科技资质表格 --></div>
</div>
<!-- 名称变体检索清单表格 -->
<div class="conclusion-box">...</div>
```

**强制元素**：
- [ ] 双栏布局（`.two-col`）：左栏=基本信息表格，右栏=科技资质表格
- [ ] 名称变体检索清单表格（含PatSnap检索状态标签）
- [ ] 检索建议代码块：`ALL_AN:(...)`格式（释义：**[全字段]申请(专利权)人**）或`ANCS:(...)`格式（释义：**[标]当前申请(专利权)人**）
- [ ] 黄色结论框

---

## 第三节：企业业务与营收曲线分析

**输入数据**：`data['sec3']`

**HTML结构**：
```html
<div class="section-title">三、企业业务与营收曲线分析</div>
<span class="section-subtitle">📈 适用场景：业务-专利交叉分析、营收趋势研判 &nbsp;|&nbsp; 关注角色：战略部、管理层、IP负责人</span>
<div class="curve-cards">
  <div class="curve-card blue"><!-- 第一增长曲线 --></div>
  <div class="curve-card green"><!-- 第二增长曲线 --></div>
  <div class="curve-card yellow"><!-- 第三增长曲线（如有） --></div>
</div>
<!-- 主要产品线pill标签 -->
<div class="conclusion-box">...</div>
```

**强制元素**：
- [ ] 增长曲线卡片组（`.curve-cards`含2-3个`.curve-card`）
- [ ] 第一曲线（蓝色顶部条`border-top-color:#0a3dff`）：核心/成熟业务
- [ ] 第二曲线（绿色顶部条`border-top-color:#0fcc7a`）：增长/新兴业务
- [ ] 第三曲线（黄色顶部条`border-top-color:#ffaa00`，可选）：探索中
- [ ] 曲线命名格式：`第X增长曲线 — [业务名]（状态）`
- [ ] 底部关键数据引用`[S2]`
- [ ] 主要产品线pill标签横向排列
- [ ] 黄色结论框

---

## 第四节：技术演进路径与竞争情报

**输入数据**：`data['sec4']`

**HTML结构**：
```html
<div class="section-title">四、技术演进路径与竞争情报</div>
<span class="section-subtitle">🧭 适用场景：技术路线梳理、竞争格局研判 &nbsp;|&nbsp; 关注角色：研发总监、技术战略部、IP部门</span>
<div class="timeline"><!-- 纵向时间线 --></div>
<!-- 竞争对手表格 -->
<div class="conclusion-box">...</div>
```

**强制元素**：
- [ ] 纵向时间线（`.timeline`含`.timeline-item`节点）
- [ ] 左侧蓝色竖线（2px `#0a3dff`）+蓝色圆点（16px）
- [ ] 最后一个节点用绿色圆点（`#0fcc7a`）
- [ ] 竞争对手表格（蓝色表头，本公司第一行高亮）
- [ ] 黄色结论框

---

## 第五节：产业技术链梯队分析

**输入数据**：`data['sec5']`

**HTML结构**：
```html
<div class="section-title">五、产业技术链梯队分析</div>
<span class="section-subtitle">🏆 适用场景：技术布局强弱研判、产业定位评估 &nbsp;|&nbsp; 关注角色：研发总监、技术战略部、管理层</span>
<div class="tier-cards">
  <div class="tier-card positive"><!-- 第一梯队 --></div>
  <div class="tier-card accent"><!-- 第二梯队 --></div>
  <div class="tier-card graybox"><!-- 第三梯队 --></div>
</div>
<div class="conclusion-box">...</div>
```

**强制元素**：
- [ ] 三梯队卡片（`.tier-cards`含3个`.tier-card`）
- [ ] 第一梯队（`.positive`蓝色顶边框`#0a3dff`）：核心产业+专利密度星级
- [ ] 第二梯队（`.accent`绿色顶边框`#0fcc7a`）：成长产业+专利密度星级
- [ ] 第三梯队（`.graybox`黄色顶边框`#ffaa00`）：新兴布局+专利密度星级
- [ ] 每个卡片内同时包含梯队概述和明细（不单独设置明细表格）
- [ ] 黄色结论框

---

## 第六节：产品技术分类

**输入数据**：`data['sec6']`

**HTML结构**：
```html
<div class="section-title">六、产品技术分类</div>
<span class="section-subtitle">🏷️ 适用场景：产品-技术映射、研发方向校准 &nbsp;|&nbsp; 关注角色：研发部、产品经理、IP部门</span>
<div class="two-col">
  <div><!-- 左：Top5产品分类表格 --></div>
  <div><!-- 右：Top5技术主题表格 --></div>
</div>
<div class="product-cards"><!-- 产品系列卡片 --></div>
<div class="conclusion-box">...</div>
```

**强制元素**：
- [ ] 双栏布局：左栏=Top5产品分类表格（含热度进度条+趋势图标），右栏=Top5技术主题表格（含IPC分类+趋势图标）
- [ ] 产品系列卡片网格（`.product-cards`，2-4列自适应）
- [ ] 黄色结论框

---

## 第七节：专利组合全景分析

**输入数据**：`data['sec7']`

**HTML结构**：
```html
<div class="section-title">七、专利组合全景分析</div>
<span class="section-subtitle">📑 适用场景：专利资产盘点、类型结构分析 &nbsp;|&nbsp; 关注角色：IP部门、知识产权师、管理层</span>
<div class="kpi-grid patent-stats"><!-- 10格专利统计KPI（4列×3行，末行2格各跨2列） --></div>
<!-- 专利类型分布表格 -->
<div class="chart-box"><img src="data:image/png;base64,{{charts.chart1}}" alt="年度申请量趋势"></div>
<!-- 地域分布双卡片 -->
<div class="conclusion-box">...</div>
```

**强制元素**：
- [ ] 10格专利统计KPI（`.kpi-grid.patent-stats`，4列×3行）：
  - 第1行：专利总量/有效/审中/无效
  - 第2行：授权发明/发明申请/实用新型/外观专利
  - 第3行：中国专利/海外专利（中国专利=CN+TW+HK+MO数量总和）
- [ ] 专利类型分布表格：发明申请→授权发明→实用新型→外观设计（严格顺序）
- [ ] 法律状态分布表格：有效→审中→失效（严格顺序）
- [ ] 年度申请量趋势图（折线图，2015-2025年）
- [ ] 地域分布双卡片：中国专利（含港澳台）/海外专利
- [ ] 黄色结论框

---

## 第八节：专利价值分层与代表性专利

**输入数据**：`data['sec8']`

**HTML结构**：
```html
<div class="section-title">八、专利价值分层与代表性专利</div>
<span class="section-subtitle">💎 适用场景：高价值专利筛选、续费/放弃决策支持 &nbsp;|&nbsp; 关注角色：IP部门、知识产权师、财务</span>
<!-- Tier A/B/C三个KPI大数字卡片 -->
<!-- 各Tier代表性专利表格（每个Tier 3-5件） -->
<div class="chart-box"><img src="data:image/png;base64,{{charts.chart4}}" alt="专利价值分布"></div>
<!-- 价值分布热力图（星级表格）：技术类别×Tier等级 -->
<div class="conclusion-box">...</div>
```

**强制元素**：
- [ ] Tier A/B/C三个KPI大数字卡片（底层逻辑：A前20%/B中间40%/C后40%）
- [ ] 代表性专利表格（蓝色表头，每个Tier 3-5件，去重：同一申请号只展示1件）
  - 固定表头：价值层级、公开号、专利名称、法律状态、专利价值、被引用数量、权利要求数
- [ ] **价值分布热力图**【强制】：HTML星级表格（技术类别×Tier等级），使用`.heatmap-star-table`样式
  - 星级计算：该类别在对应Tier的专利数 / 该类别总专利数
  - ★★★★★ = ≥30% | ★★★★ = 20-30% | ★★★ = 10-20% | ★★ = 5-10% | ★ = <5%
  - 最后加"分析"列，提供文字解读
  - 技术类别通过`TECH_CATEGORY_MAP`映射（见data_prep.md）
- [ ] 黄色结论框（`.conclusion-box`）含`本小节结论：`+`<ol>`（每条`<li>`末尾须含`[S#]`标记）+`.source-hint`

**价值热力图HTML结构示例**：
```html
<table class="heatmap-star-table">
  <tr><th>技术类别</th><th>Tier A（高价值）</th><th>Tier B（中价值）</th><th>Tier C（低价值）</th><th>分析</th></tr>
  <tr><td>过滤洗涤干燥</td><td><span class="star-blue">★★★★★</span></td><td><span class="star-blue">★★★★</span></td><td><span class="star-blue">★★★</span></td><td>最强价值集中区</td></tr>
  <tr><td>锂电材料设备</td><td><span class="star-blue">★★</span></td><td><span class="star-gray">★☆☆☆☆</span></td><td><span class="star-gray">☆☆☆☆☆</span></td><td>专利数量少，0件落入Tier C</td></tr>
  <!-- 有专利的Tier用star-blue，无专利用star-gray -->
</table>
```

---

## 第九节：专利与营收曲线匹配分析

**输入数据**：`data['sec9']`

**HTML结构**：
```html
<div class="section-title">九、专利与营收曲线匹配分析</div>
<span class="section-subtitle">🔗 适用场景：专利-业务对齐度评估、资源匹配分析 &nbsp;|&nbsp; 关注角色：管理层、战略部、IP负责人</span>
<!-- 匹配分析表格（CSS进度条+评级badge） -->
<!-- 增长曲线分类汇总表格 -->
<div class="conclusion-box">...</div>
```

**强制元素**：
- [ ] 匹配分析表格（固定表头）：产品/业务方向、当前专利覆盖度、核心专利案例、匹配评级
  - 专利覆盖度列使用CSS进度条（`.cover-bar>.cover-fill`），匹配评级badge
- [ ] 增长曲线分类汇总表格（固定表头）：增长曲线、Tier A密度、匹配评估、代表性专利、综合结论
  - 命名格式`第X曲线（产品名称）`，Tier A密度格式`XX件/XX亿营收`
- [ ] 匹配评估标签（彩色圆点+badge）：匹配度高/战略匹配/缺口最大/亟需布局
- [ ] 黄色结论框

---

## 第十节：专利布局缺口分析

**输入数据**：`data['sec10']`

**HTML结构**：
```html
<div class="section-title">十、专利布局缺口分析</div>
<span class="section-subtitle">⚠️ 适用场景：专利空白识别、紧急布局优先级排序 &nbsp;|&nbsp; 关注角色：IP部门、研发总监、管理层</span>
<div class="gap-cards">
  <div class="gap-card urgent"><!-- 紧急缺口 --></div>
  <div class="gap-card important"><!-- 重要缺口 --></div>
  <div class="gap-card opportunity"><!-- 机会缺口 --></div>
</div>
<div class="conclusion-box">...</div>
```

**强制元素**：
- [ ] 三级缺口分类卡片（`.gap-cards`含3个`.gap-card`）
- [ ] 紧急缺口（`.urgent`红色顶部条`#e74c3c`）：6个月内启动
- [ ] 重要缺口（`.important`橙色顶部条`#ffaa00`）：1年内启动
- [ ] 机会缺口（`.opportunity`蓝色顶部条`#0a3dff`）：1-3年内布局
- [ ] 每条缺口使用`.gap-title`标题（含彩色圆点`.dot-red/.dot-yellow/.dot-blue`）+ `.gap-item`内容块
- [ ] 每条缺口格式：`【技术方向名称】`+现有状况+竞品布局+具体建议
- [ ] 黄色结论框

**缺口卡片HTML结构示例**：
```html
<div class="gap-card urgent">
  <div class="gap-title"><span class="dot-red"></span> 紧急缺口（6个月内必须启动）</div>
  <div class="gap-item">
    <strong>【海外专利布局空白】</strong>现有状况：... 具体建议：...
  </div>
</div>
```

---

## 第十一节：核心发明人与研发团队分析

**输入数据**：`data['sec11']`

**HTML结构**：
```html
<div class="section-title">十一、核心发明人与研发团队分析</div>
<span class="section-subtitle">👥 适用场景：研发团队画像、关键人风险识别、人才规划 &nbsp;|&nbsp; 关注角色：HR、研发总监、IP部门、管理层</span>
<!-- chart2: 发明人排行双Y轴柱状图 -->
<div class="chart-inventor-dual">
  <h4>核心发明人专利数量与价值排行 (Top 10)</h4>
  <img src="data:image/png;base64,{{charts.chart2}}" alt="发明人排行">
</div>
<!-- chart3: 发明人×技术主题热力图 -->
<div class="chart-box">
  <h4>发明人×技术主题热力图</h4>
  <img src="data:image/png;base64,{{charts.chart3}}" alt="技术热力图">
</div>
<div class="side-green"><!-- 技术专长分布 --></div>
<div class="side-blue"><!-- 协作网络分析 --></div>
<!-- 核心发明人详细信息表格 -->
<!-- chart5: 发明人年度趋势热力图 -->
<div class="chart-box">
  <h4>核心发明人年度申请趋势 (2015-2025)</h4>
  <img src="data:image/png;base64,{{charts.chart5}}" alt="发明人趋势">
</div>
<div class="conclusion-box">...</div>
```

**强制元素**：
- [ ] 发明人排行图（**双Y轴分组柱状图**，figsize=(12,6)），左Y轴专利数量（蓝色`#0a3dff`），右Y轴专利价值（万元，绿色`#0fcc7a`）
  - X轴：发明人姓名（按专利数量降序排列，取Top 10）
  - 左Y轴标签颜色`#0a3dff`，右Y轴标签颜色`#0fcc7a`
  - 两组图例分别放在左上和右上
  - 使用`ax1.twinx()`创建双Y轴
  - **【强制代码规范】**：
    ```python
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax2 = ax1.twinx()
    x = np.arange(len(names))
    w = 0.35
    bars1 = ax1.bar(x - w/2 - 0.025, counts, w, color='#0a3dff', label='专利数量')
    bars2 = ax2.bar(x + w/2 + 0.025, values, w, color='#0fcc7a', label='专利价值（万元）')
    ax1.set_ylabel('专利数量（件）', color='#0a3dff', fontsize=12)
    ax2.set_ylabel('专利价值（万元）', color='#0fcc7a', fontsize=12)
    ax1.tick_params(axis='y', labelcolor='#0a3dff')
    ax2.tick_params(axis='y', labelcolor='#0fcc7a')
    # 【强制】数值标签：左Y轴专利数量用蓝色，右Y轴专利价值用绿色
    for bar, val in zip(bars1, counts):
        ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 2,
                 f'{int(val)}', ha='center', va='bottom', fontsize=9, color='#0a3dff', fontweight='bold')
    for bar, val in zip(bars2, values):
        ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 5,
                 f'{val:.1f}', ha='center', va='bottom', fontsize=9, color='#0fcc7a', fontweight='bold')
    ```
- [ ] 技术热力图（figsize=(10,6)，蓝色系`#d0d8ff→#0a3dff`）
  - **【强制代码规范】**：
    ```python
    fig, ax = plt.subplots(figsize=(10, 6))
    # 数据准备：发明人 × 技术主题矩阵
    inv_tech_matrix = []
    for inv in top_inventors:
        row = []
        for tech in top_techs:
            count = len(df[(df['发明人'].str.contains(inv, na=False)) & 
                          (df['技术主题分类'].str.contains(tech, na=False))])
            row.append(count)
        inv_tech_matrix.append(row)

    im = ax.imshow(inv_tech_matrix, cmap='Blues', aspect='auto')
    ax.set_xticks(range(len(top_techs)))
    ax.set_yticks(range(len(top_inventors)))
    ax.set_xticklabels(top_techs, rotation=45, ha='right')
    ax.set_yticklabels(top_inventors)
    plt.colorbar(im, ax=ax, label='专利数量')
    plt.tight_layout()
    ```
- [ ] 技术专长分布卡片（`.side-green`绿色左边框）：4-6个技术专长组
- [ ] 协作网络分析卡片（`.side-blue`蓝色左边框）：3-5个协作集群
- [ ] 核心发明人详细信息表格（Top 10，含排名/姓名/专利数/主技术域/代表专利）
- [ ] **研发效率提升建议**【新增】（`.side-green`卡片，位于结论框之前）
  - 包含：人均专利产出率、专利商业化率、产学研合作占比等指标分析表格
  - 给出5条具体建议（如优化研发投入结构、加强产学研合作等）

**研发效率提升建议HTML结构示例**：
```html
<div class="side-green">
  <h4>📈 研发效率提升建议</h4>
  <table>
    <tr><th>指标</th><th>当前值</th><th>行业均值</th><th>差距</th></tr>
    <tr><td>人均专利产出率</td><td>X件/人年</td><td>Y件/人年</td><td>+/-Z%</td></tr>
    <tr><td>专利商业化率</td><td>X%</td><td>Y%</td><td>+/-Z%</td></tr>
    <tr><td>产学研合作占比</td><td>X%</td><td>Y%</td><td>+/-Z%</td></tr>
  </table>
  <ol>
    <li>优化研发投入结构，增加前端技术研究投入比例</li>
    <li>建立产学研合作机制，引入外部创新资源</li>
    <li>完善发明人激励机制，提升研发人员积极性</li>
    <li>加强专利质量管控，减少低价值专利申请</li>
    <li>建立技术预研机制，提前布局关键技术领域</li>
  </ol>
</div>
```

- [ ] **chart5发明人趋势图**【强制放置】：必须放在第十一节，不得放在其他节
  - 基于`inventor_data['inv_year']`的矩阵热力图
  - figsize=(10,5)，蓝色系
- [ ] 黄色结论框（`.conclusion-box`）含`本小节结论：`+`<ol>`（每条`<li>`末尾须含`[S#]`标记）+`.source-hint`

---

## 第十二节：近期技术方向前瞻

**输入数据**：`data['sec12']`

**HTML结构**：
```html
<div class="section-title">十二、近期技术方向前瞻（2021-2025）</div>
<span class="section-subtitle">🔮 适用场景：技术趋势预判、研发立项前瞻 &nbsp;|&nbsp; 关注角色：研发部、技术战略部、CTO</span>
<div class="two-col">
  <div class="trend-col-grow"><!-- 新增/增长方向 --></div>
  <div class="trend-col-decline"><!-- 衰退/减少方向 --></div>
</div>
<!-- 近期质量趋势段落 -->
<div class="conclusion-box">...</div>
```

**强制元素**：
- [ ] 双栏前瞻卡片：左栏（`.trend-col-grow`绿色左边框`#0fcc7a`）=新增/增长方向
  - 右栏（`.trend-col-decline`红色左边框`#e74c3c`）=衰退/减少方向
  - 每条格式：`IPC号（技术名称）：描述`（含产品关联+专利数据）
- [ ] **近期专利质量趋势**：发明占比变化+质量趋势结论+改进建议
- [ ] 黄色结论框

---

## 第十三节：海外专利与抗风险能力评估

**输入数据**：`data['sec13']`

**HTML结构**：
```html
<div class="section-title">十三、海外专利与抗风险能力评估</div>
<span class="section-subtitle">🌍 适用场景：海外布局评估、侵权风险排查、出口合规 &nbsp;|&nbsp; 关注角色：IP部门、法务、国际业务部、管理层</span>
<div class="kpi-row"><!-- 4个风险KPI大字卡片 --></div>
<div class="score-gauge"><!-- 评分仪表盘（0-100分进度条） --></div>
<!-- 双栏评分表格 -->
<!-- 海外补全优先级矩阵 -->
<!-- 海外侵权风险评估Top5 -->
<div class="conclusion-box">...</div>
```

**强制元素**：
- [ ] 4个风险KPI大字卡片：综合风险等级/海外受理局/PCT申请/海外专利
- [ ] **评分仪表盘**【强制】：渐变色彩条（红→黄→绿）+圆形指示器+分数显示+风险等级标签
  - 使用`.score-bar-gradient`+`.score-indicator`样式
  - 指示器位置 = 分数/100 * 100%
  - 下方显示`XX/100`分数+风险等级（如"预警级"/"高风险"/"中等风险"）
- [ ] **双栏评分矩阵**【强制】：左栏"专利布局角度（满分50分）"+右栏"侵权风险角度（满分50分）"
  - 每个维度显示：维度名称/得分/说明
  - 使用`.score-section-header`+`.score-section-body`+`.score-row`样式
  - 得分使用颜色区分：红（低分）/黄（中分）/绿（高分）
  - 底部显示小计行（蓝色背景白字）
- [ ] 海外补全优先级矩阵：技术领域×目标市场×专利类型×优先级×行动建议
- [ ] 海外侵权风险评估Top 5：本企业技术/潜在被侵权公司/关键专利/风险等级/建议措施
- [ ] **海外布局建议版块**【新增强制】：
  - 使用`.overseas-advice`样式（蓝色左边框+浅蓝背景）
  - 包含：目标市场优先级排序、核心产品海外布局路径、PCT申请策略、时间规划
  - 放在第十三节结论框之前
- [ ] 黄色结论框

**评分仪表盘HTML结构示例**：
```html
<div class="score-bar-gradient">
  <div class="score-indicator" style="left: 50%;"></div>
</div>
<div style="text-align:center;font-size:28px;font-weight:700;color:#ffaa00;">50/100 <span style="font-size:14px;">预警级</span></div>

<div class="two-col">
  <div>
    <div class="score-section-header">专利布局角度（满分50分）</div>
    <div class="score-section-body">
      <div class="score-row"><span>PCT申请覆盖率</span><span class="score-val-red">0/10</span><span>0件PCT申请</span></div>
      <!-- 更多维度 -->
    </div>
    <div class="score-total-row"><span>小计</span><span>8/50</span></div>
  </div>
  <div>
    <div class="score-section-header">侵权风险角度（满分50分）</div>
    <!-- 同上结构 -->
  </div>
</div>

<div class="overseas-advice">
  <h4>🌍 海外布局建议</h4>
  <p><strong>目标市场优先级：</strong>印度/东南亚 > 欧洲 > 北美</p>
  <p><strong>PCT申请策略：</strong>以现有中国专利申请日为优先权，6个月内提交首批PCT</p>
</div>
```

---

## 第十四节：降本优化

**输入数据**：`data['sec14']`

**前置条件**：只使用`df_active`候选池（已排除6种终结法律状态：期限届满/视为撤回/撤回-主动撤回/驳回/避免重复授权/PCT指定期满）

**HTML结构**：
```html
<div class="section-title">十四、降本优化 — 可放弃续费专利建议</div>
<span class="section-subtitle">💰 适用场景：专利维护成本优化、闲置资产清理 &nbsp;|&nbsp; 关注角色：IP部门、财务、知识产权师</span>
<!-- 免责声明（黄色警告框） -->
<!-- 可放弃续费专利建议表格 -->
<!-- 优化方向表格 -->
<div class="conclusion-box">...</div>
```

**强制元素**：
- [ ] 免责声明（黄色警告框）：放弃建议仅供参考，含**降本前提条件**（高亮显示）。
  - 免责声明中避免直接使用6种终结法律状态的完整词组，使用"前述终结法律状态"等概括性指代表述。
  - **放弃前建议优先评估转让价值及跨领域应用价值。**
- [ ] 可放弃续费专利建议表格（固定表头）：专利类型、代表案例（含公开号）、放弃建议理由、建议
  - **【强制排除校验】**表格中不出现6种终结法律状态的词组（期限届满/视为撤回/撤回-主动撤回/驳回/避免重复授权/PCT指定期满）
- [ ] 优化方向表格（固定表头）：优化方向、建议措施、预期节省、风险评估
- [ ] 黄色结论框

---

## 第十五节：近期新产品专利布局策略

**输入数据**：`data['sec15']`

**HTML结构**：
```html
<div class="section-title">十五、近期新产品专利布局策略</div>
<span class="section-subtitle">🚀 适用场景：新产品上市前专利布局、P0/P1/P2分级执行 &nbsp;|&nbsp; 关注角色：研发部、产品经理、IP部门</span>
<!-- 新产品×专利覆盖矩阵表格 -->
<!-- 布局分级定义与策略表格 -->
<div class="conclusion-box">...</div>
```

**强制元素**：
- [ ] 新产品×专利覆盖矩阵（固定表头）：新产品方向、核心技术、现有覆盖、专利缺口、竞对布局简述、补全战略帮助、紧迫度、建议法域
- [ ] 布局分级定义表格（P0/P1/P2）：含分级/定义/判定标准/处理时效/布局重点/竞对布局/战略帮助/目标法域
- [ ] 黄色结论框

---

## 第十六节：SWOT分析与专利运营建议

**输入数据**：`data['sec16']`

**HTML结构**：
```html
<div class="section-title">十六、SWOT分析与专利运营、产品立项及产学研建议</div>
<span class="section-subtitle">🎯 适用场景：战略诊断、运营改进、产学研合作规划 &nbsp;|&nbsp; 关注角色：管理层、战略部、研发总监、IP负责人</span>
<div class="swot-grid">
  <div class="swot-card" style="border-top:3px solid #0fcc7a;"><!-- S优势 --></div>
  <div class="swot-card" style="border-top:3px solid #ffaa00;"><!-- W劣势 --></div>
  <div class="swot-card" style="border-top:3px solid #0a3dff;"><!-- O机遇 --></div>
  <div class="swot-card" style="border-top:3px solid #e74c3c;"><!-- T威胁 --></div>
</div>
<div class="three-col"><!-- 三栏建议 --></div>
<div class="conclusion-box">...</div>
```

**强制元素**：
- [ ] SWOT四象限（`.swot-grid`含4个`.swot-card`），每象限不同顶部条颜色
- [ ] **三栏建议布局**【强制】（`.three-col`）：📋专利运营管理建议 / 🏭产品立项建议 / 🎓产学研合作建议
- [ ] 每栏5条结构化bullet points
- [ ] **专利运营子卡片组**【新增】（3个彩色卡片，位于三栏建议之后、结论框之前）
  - 防御性运营卡片（蓝色边框`#0a3dff`）：专利布局防御、风险规避、侵权监控
  - 收益性运营卡片（绿色边框`#0fcc7a`）：专利许可、技术转让、专利池运营
  - 进攻性运营卡片（黄色边框`#ffaa00`）：专利维权、市场竞争、标准必要专利

**专利运营子卡片HTML结构模板**【动态填充，禁止照搬示例文字】：

> **【模板化填充规则】** 以下3张卡片的 `<li>` 内容**必须**根据被分析企业的实际产品和专利数据动态生成，禁止直接复制示例中的泛泛文字。填充数据来源：`df_active['技术类别']`（技术领域分布）、`tier_a`（高价值专利）、`business_info['products']`（产品清单）、`business_info['competitors']`（竞品列表）。

```html
<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin: 16px 0;">
  <!-- 防御性运营：基于企业核心技术领域 + 竞争对手专利威胁 -->
  <div style="background: #fff; border-radius: 8px; padding: 16px; border-top: 3px solid #0a3dff; box-shadow: 0 1px 3px rgba(0,0,0,0.06);">
    <h4 style="color: #0a3dff; margin: 0 0 8px 0;">🛡️ 防御性运营</h4>
    <ul style="margin: 0; padding-left: 16px; font-size: 13px; color: #555;">
      <!-- 示例（华域三电-汽车空调）：围绕{{top_tech_1}}、{{top_tech_2}}等核心领域补充布局，形成围绕{{core_product}}的技术壁垒 -->
      <li>围绕【TOP2技术类别】专利集群构建防御围墙，覆盖【核心产品】全技术链条[S3]</li>
      <!-- 示例：针对【竞品A】【竞品B】在华域三电主要技术领域的专利申请建立监控预警机制 -->
      <li>针对【竞品1】【竞品2】在【企业核心领域】的专利布局建立侵权监控与FTO排查机制[S1][S4]</li>
      <!-- 示例：对电驱动压缩机领域威胁性竞品专利提起无效宣告准备 -->
      <li>对【具体技术方向】中威胁性竞品专利启动无效宣告或规避设计准备[S3][S5]</li>
    </ul>
  </div>
  <!-- 收益性运营：基于Tier A高价值专利 + 行业标准参与 -->
  <div style="background: #fff; border-radius: 8px; padding: 16px; border-top: 3px solid #0fcc7a; box-shadow: 0 1px 3px rgba(0,0,0,0.06);">
    <h4 style="color: #0fcc7a; margin: 0 0 8px 0;">💰 收益性运营</h4>
    <ul style="margin: 0; padding-left: 16px; font-size: 13px; color: #555;">
      <!-- 示例：将电动压缩机控制技术Tier A专利（价值>50万）对外许可给下游新能源车企 -->
      <li>将【Tier A技术领域】高价值专利（价值>【tier_a_min】万）向【下游客户/行业】开展专利许可[S3]</li>
      <!-- 示例：推进热管理系统PCT专利（WO20XXXXXX）的技术转让 -->
      <li>推进【具体高价值专利号】等海外专利的技术转让或交叉许可谈判[S3][S1]</li>
      <!-- 示例：参与汽车空调R744制冷剂标准专利池建设 -->
      <li>参与【企业所在行业标准名称】标准专利池建设，将标准必要专利纳入运营[S1][S5]</li>
    </ul>
  </div>
  <!-- 进攻性运营：基于技术路线图 + 目标市场 + 标准必要专利 -->
  <div style="background: #fff; border-radius: 8px; padding: 16px; border-top: 3px solid #ffaa00; box-shadow: 0 1px 3px rgba(0,0,0,0.06);">
    <h4 style="color: #ffaa00; margin: 0 0 8px 0;">⚔️ 进攻性运营</h4>
    <ul style="margin: 0; padding-left: 16px; font-size: 13px; color: #555;">
      <!-- 示例：针对新能源汽车热管理领域侵权厂商发起维权诉讼 -->
      <li>在【核心产品/技术领域】针对侵权竞品主动发起专利维权，巩固市场地位[S5][S1]</li>
      <!-- 示例：围绕800V高压平台电动压缩机技术布局标准必要专利 -->
      <li>围绕【企业技术路线图方向】布局标准必要专利，提升行业话语权[S1][S5]</li>
      <!-- 示例：通过CO2热泵空调专利组合在欧盟市场建立竞争壁垒 -->
      <li>通过【目标市场】【核心技术】专利组合建立区域市场进入壁垒[S3][S4]</li>
    </ul>
  </div>
</div>
```

**【填充指令】执行时必须替换的占位符**：
| 占位符 | 数据来源 | 示例值（华域三电） |
|--------|----------|-------------------|
| `【TOP2技术类别】` | `df_active['技术类别'].value_counts().head(2)` | 电动压缩机、热管理系统 |
| `【核心产品】` | `business_info['products'][0]` | 新能源汽车电动压缩机 |
| `【竞品1】【竞品2】` | `business_info['competitors'][:2]` | 电装、三电（日本） |
| `【Tier A技术领域】` | `tier_a['技术类别'].value_counts().head(1)` | 电动压缩机控制 |
| `【tier_a_min】` | `tier_meta['tier_a_range'].split('-')[0]` | 45 |
| `【目标市场】` | `business_info['export_markets']` | 欧盟、东南亚 |
| `【企业技术路线图方向】` | `business_info['tech_roadmap']` | 800V高压平台、CO2热泵 |

- [ ] 黄色结论框

---

## 第十七节：产品链与产业链发展策略

**输入数据**：`data['sec17']`

**HTML结构**：
```html
<div class="section-title">十七、产品链与产业链发展策略建议</div>
<span class="section-subtitle">⛓️ 适用场景：产业链定位、上下游专利策略制定 &nbsp;|&nbsp; 关注角色：战略部、管理层、研发总监</span>
<div class="two-col">
  <div><!-- 左：产品链发展策略 --></div>
  <div><!-- 右：产业链发展策略 --></div>
</div>
<!-- 策略矩阵表格 -->
<div class="conclusion-box">...</div>
```

**强制元素**：
- [ ] 双栏布局：左栏=🔗产品链发展策略（4条bullet），右栏=🏭产业链发展策略（4条bullet）
- [ ] 策略矩阵表格：方向/专利支撑/市场需求/竞争态势/策略建议（彩色标签）/时间维度
- [ ] 策略标签（3种彩色）：强化型(绿`#0fcc7a`)/布局型(蓝`#0a3dff`)/追赶型(黄`#ffaa00`)
- [ ] 黄色结论框

---

## 第十八节：分阶段专利补全计划

**输入数据**：`data['sec18']`

**HTML结构**：
```html
<div class="section-title">十八、分阶段专利补全计划</div>
<span class="section-subtitle">📅 适用场景：专利建设路线图、预算规划、分阶段目标设定 &nbsp;|&nbsp; 关注角色：IP部门、管理层、财务</span>
<div class="timeline"><!-- 四级时间线 --></div>
<div class="conclusion-box">...</div>
```

**强制元素**：
- [ ] 四级时间线（`.timeline`含4个`.timeline-item`）：
  - 🟢近6个月（紧急补全）→🔵近1年（系统布局）→🟡1-3年（体系完善）→🔴3年+（国际化战略）
- [ ] 每条时间线包含固定5要素：目标、事项、原因、价值、预期
- [ ] **补全价值蓝色提示框**【强制】：每条时间线末尾`💡补全价值：战略价值描述`（`background:#e6eeff`）
- [ ] 黄色结论框

---

## 第十九节：平台使用场景建议

**输入数据**：`data['sec19']`

**HTML结构**：
```html
<div class="section-title">十九、平台使用场景建议（PatSnap / Eureka）</div>
<span class="section-subtitle">🛠️ 适用场景：平台功能推广、团队使用培训、数字化工具落地 &nbsp;|&nbsp; 关注角色：IP部门、研发团队、IT支持</span>
<!-- IP团队使用场景表格 -->
<!-- 研发团队使用场景表格 -->
<div class="conclusion-box">...</div>
```

**强制元素**：
- [ ] IP团队使用场景表格：使用场景/推荐功能/解决问题/相关岗位与执行建议
- [ ] 研发团队使用场景表格（同上结构）
- [ ] 建议需结合企业实际，给出可执行建议，明确责任岗位
- [ ] 黄色结论框

---

## 第二十节：知识产权行动建议汇总

**输入数据**：`data['sec20']`

**HTML结构**：
```html
<div class="section-title">二十、知识产权行动建议汇总</div>
<span class="section-subtitle">✅ 适用场景：行动项汇总、跨部门待办分发、执行跟踪 &nbsp;|&nbsp; 关注角色：IP部门、产研团队、管理层</span>
<div class="two-col">
  <div class="action-ip"><!-- 知识产权师待办 --></div>
  <div class="action-rd"><!-- 产研待办 --></div>
</div>
<div class="conclusion-box">...</div>
<!-- 报告综述区块（SECTION_21） -->
```

**强制元素**：
- [ ] 双栏待办（`.two-col`）：左栏`.action-ip`（蓝色渐变背景+蓝色左边框），右栏`.action-rd`（绿色渐变背景+绿色左边框）
- [ ] 每条待办：`☐`空心方框+序号+行动描述+信息来源（标注"第XX小节"）
- [ ] 按事务类型分组（海外布局/专利续费/竞品监控等）
- [ ] 黄色结论框

---

## 第二十一节：报告综述（第二十节子元素，不编号）

**输入数据**：`data['sec21']`

**HTML结构**：
```html
<!-- 紧接第二十节结论框之后 -->
<div class="report-review">
  <h3 style="color:#0a2baa;font-size:16px;font-weight:700;margin:0 0 12px 0;">报告综述</h3>
  <p style="color:#666;font-size:12px;line-height:1.6;margin:0 0 10px 0;padding:8px;background:#f0f3ff;border-radius:4px;">
    如需更详细的完整报告，请登录Eureka平台获取深度分析。以下内容仅对报告进行简单总结，分析结论与具体建议，详见各章节内容并务必请专业IP或法务进行把关。
  </p>
  <p style="color:#333;font-size:13px;line-height:1.8;margin:0;">{{review_text}}</p>
</div>
```

**强制元素**：
- [ ] `.report-review`独立区块（`background:#d6e0ff`，与结论框视觉隔离）
- [ ] Eureka引导语（必须位于正文之前）：提示登录平台获取深度分析+建议专业IP/法务把关
- [ ] 综述正文200-300字中文
- [ ] 包含五要素：企业定位/专利全景/核心发现/战略建议/风险提示
- [ ] **不单独编号为小节**，不设置`.section-title`和`.section-subtitle`
- [ ] **专利布局健康度评分**【新增】（位于报告综述正文之后）
  - 格式：HTML表格，显示5个维度的评分（每项0-20分，总分100分）
  - 维度：专利总量/技术覆盖度/价值分层/海外布局/团队能力
  - 每个维度显示：名称/得分/权重/加权得分
  - 底部显示总分和健康度等级（优秀≥80/良好60-79/一般40-59/较差<40）

**健康度评分HTML结构示例**：
```html
<table style="width:100%; margin: 16px 0; border-collapse: collapse;">
  <tr><th>维度</th><th>得分(0-20)</th><th>权重</th><th>加权得分</th></tr>
  <tr><td>专利总量</td><td>XX</td><td>20%</td><td>X.X</td></tr>
  <tr><td>技术覆盖度</td><td>XX</td><td>20%</td><td>X.X</td></tr>
  <tr><td>价值分层</td><td>XX</td><td>20%</td><td>X.X</td></tr>
  <tr><td>海外布局</td><td>XX</td><td>20%</td><td>X.X</td></tr>
  <tr><td>团队能力</td><td>XX</td><td>20%</td><td>X.X</td></tr>
  <tr style="background: #0a3dff; color: #fff; font-weight: 700;">
    <td colspan="3">健康度总分</td><td>XX/100 （等级）</td>
  </tr>
</table>
<div style="text-align: center; color: #666; font-size: 12px; margin-top: 8px;">
  等级定义：优秀≥80 / 良好60-79 / 一般40-59 / 较差&lt;40
</div>
```

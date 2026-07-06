# HTML炫酷版报告模板规范

本文件是 `dairy-protein-competitive-analysis` 技能生成 HTML 炫酷版报告时必须遵守的完整版面设计规范。每次生成 HTML 报告，必须严格复现本规范中定义的配色系统、布局结构、组件样式和图表配置。

---

## 一、整体风格定位

- **主题**：深色科技风（Dark Sci-Fi）
- **主色调**：Cyan（`#00d4ff`） × Gold（`#ffd700`）
- **布局**：单页纵向滚动，无翻页，顶部固定导航
- **动效**：粒子连线动态背景（Canvas），滚动进入淡入动画（IntersectionObserver），ECharts交互式图表（悬停tooltip）
- **图表库**：ECharts 5.4.3（CDN: `https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js`）
- **字体栈**：`"Source Han Sans", "Noto Sans CJK SC", "Microsoft YaHei", sans-serif`

---

## 二、CSS 变量系统（:root）

所有颜色必须通过以下 CSS 变量引用，不得硬编码十六进制颜色值：

```css
:root {
  --bg:     #050d1a;   /* 最深背景 */
  --bg2:    #0a1628;   /* 次级背景 */
  --bg3:    #0f1f35;   /* 三级背景 */
  --card:   #0d1e33;   /* 卡片背景 */
  --border: #1a3a5c;   /* 边框色 */
  --cyan:   #00d4ff;   /* 主强调色（Cyan） */
  --cyan2:  #00a8cc;   /* 次强调色（深Cyan） */
  --gold:   #ffd700;   /* 金色强调 */
  --green:  #00ff88;   /* 绿色（正向信号） */
  --orange: #ff6b35;   /* 橙色（中等风险/信号） */
  --red:    #ff4444;   /* 红色（高风险/警告） */
  --purple: #a855f7;   /* 紫色（差异化/特殊标注） */
  --text:   #e0eeff;   /* 正文文字 */
  --muted:  #6b9fc4;   /* 次要文字 */
  --white:  #ffffff;   /* 纯白 */
}
```

---

## 三、全局基础样式

```css
* { margin: 0; padding: 0; box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  font-family: "Source Han Sans", "Noto Sans CJK SC", "Microsoft YaHei", sans-serif;
  background: var(--bg);
  color: var(--text);
  font-size: 14px;
  line-height: 1.7;
  overflow-x: hidden;
}
/* 滚动条 */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--cyan2); border-radius: 3px; }
```

---

## 四、必须包含的页面结构组件

### 4.1 粒子背景 Canvas

```html
<canvas id="bg-canvas"></canvas>
```

CSS：
```css
#bg-canvas {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  pointer-events: none; z-index: 0; opacity: 0.3;
}
```

JavaScript（粒子连线动效）：在文档底部 `<script>` 中用 Canvas 2D API 实现随机粒子生成、移动和连线动画，粒子颜色使用 `rgba(0,212,255,0.6)`，连线颜色使用 `rgba(0,212,255,0.15)`。

### 4.2 顶部固定导航（nav）

```html
<nav>
  <div class="nav-brand">◈ 乳蛋白深加工 · 专利竞争情报</div>
  <ul class="nav-links">
    <li><a href="#overview">竞争格局</a></li>
    <li><a href="#protein-type">蛋白布局</a></li>
    <li><a href="#function">功能分析</a></li>
    <li><a href="#matrix">核心矩阵</a></li>
    <li><a href="#tech">技术路线</a></li>
    <li><a href="#profiles">战略画像</a></li>
    <li><a href="#opportunity">机会窗口</a></li>
    <li><a href="#action">行动建议</a></li>
  </ul>
</nav>
```

CSS 要点：
```css
nav {
  position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
  background: rgba(5,13,26,0.92);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
  padding: 0 40px;
  display: flex; align-items: center; justify-content: space-between;
  height: 56px;
}
.nav-brand { font-size: 13px; font-weight: 700; color: var(--cyan); letter-spacing: 1px; }
.nav-links { display: flex; gap: 24px; list-style: none; }
.nav-links a { color: var(--muted); text-decoration: none; font-size: 12px; letter-spacing: 0.5px; }
.nav-links a:hover { color: var(--cyan); }
```

### 4.3 Hero 区块（封面）

必须包含以下元素：
- `hero-eyebrow`：英文副标题（如 `PATENT COMPETITIVE INTELLIGENCE · 2026`），带左右横线装饰
- `hero h1`：渐变文字标题，使用 `background: linear-gradient(135deg, var(--white) 0%, var(--cyan) 50%, var(--purple) 100%)`，`-webkit-background-clip: text; -webkit-text-fill-color: transparent`
- `hero-sub`：一句话说明文字
- `hero-kpis`：3–4个KPI数字卡片，显示数据规模（如：精标专利总量、分析企业数、蛋白类型维度数、功能维度数）
- `hero-badges`：3个徽章，显示分析方法标签（如：`精细标引数据驱动`、`蛋白类型×功能矩阵`、`ECharts交互图表`）
- `hero-actions`：操作按钮区（如滚动引导箭头）

KPI卡片样式：
```css
.hero-kpi {
  text-align: center; padding: 20px 28px;
  background: rgba(0,212,255,0.05);
  border: 1px solid rgba(0,212,255,0.2);
  border-radius: 8px; min-width: 120px;
}
.hero-kpi-num { font-size: 36px; font-weight: 900; color: var(--cyan); line-height: 1; }
.hero-kpi-label { font-size: 11px; color: var(--muted); margin-top: 6px; letter-spacing: 1px; }
```

### 4.4 跑马灯数据滚动条（ticker）

位于 Hero 区块下方，全宽横向无限循环滚动数据摘要标签：

```html
<div class="ticker-wrap">
  <div class="ticker">
    <span class="ticker-item">精标专利总量 · XXX件</span>
    <span class="ticker-sep">◆</span>
    <!-- 重复多组数据标签 -->
  </div>
</div>
```

CSS（关键动画）：
```css
.ticker-wrap { overflow: hidden; background: rgba(0,212,255,0.05); border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); padding: 10px 0; }
.ticker { display: flex; white-space: nowrap; animation: ticker-scroll 40s linear infinite; }
@keyframes ticker-scroll { from { transform: translateX(0); } to { transform: translateX(-50%); } }
.ticker-item { font-size: 12px; color: var(--cyan); margin: 0 16px; letter-spacing: 0.5px; }
.ticker-sep { color: var(--gold); opacity: 0.6; }
```

---

## 五、章节（Section）通用结构

每个章节必须使用以下统一结构：

```html
<div class="section" id="[section-id]">
  <div class="section-header">
    <span class="section-tag">[CHAPTER XX]</span>
    <span class="section-title">[中文章节标题]</span>
  </div>
  <p class="section-desc">[章节导言，1–2句，说明本章分析视角和边界提示]</p>
  <!-- 章节内容 -->
</div>
```

CSS：
```css
.section {
  position: relative; z-index: 1;
  max-width: 1200px; margin: 0 auto;
  padding: 80px 40px;
  border-bottom: 1px solid rgba(26,58,92,0.5);
  opacity: 0; transform: translateY(20px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}
.section.visible { opacity: 1; transform: translateY(0); }
.section-header { display: flex; align-items: baseline; gap: 16px; margin-bottom: 12px; }
.section-tag { font-size: 11px; font-weight: 700; letter-spacing: 3px; color: var(--cyan); opacity: 0.7; text-transform: uppercase; }
.section-title { font-size: 24px; font-weight: 800; color: var(--white); }
.section-desc { color: var(--muted); font-size: 13px; max-width: 780px; margin-bottom: 32px; line-height: 1.8; }
```

滚动进入动画（JavaScript）：
```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.1 });
document.querySelectorAll('.section').forEach(s => observer.observe(s));
```

---

## 六、卡片组件

### 6.1 标准内容卡片（card）

```css
.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.card:hover { border-color: var(--cyan2); box-shadow: 0 0 24px rgba(0,212,255,0.08); }
```

### 6.2 双列卡片网格（card-grid-2）

```css
.card-grid-2 {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}
```

### 6.3 三列卡片网格（card-grid-3）

```css
.card-grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}
```

### 6.4 执行摘要结论卡片（exec-card）

结构：
```html
<div class="exec-card exec-card-[cyan|gold|green|orange|red|purple]">
  <div class="exec-num">01</div>
  <div class="exec-body">
    <div class="exec-title">[结论标题]</div>
    <div class="exec-text">[结论内容，2–3句]</div>
    <div class="exec-meta">
      <span class="tag-evidence tag-[strong|medium|weak]">证据强度：[强|中|弱]</span>
      <span class="tag-basis">[数据依据简述]</span>
    </div>
  </div>
</div>
```

各颜色变体边框：
- `exec-card-cyan`：`border-left: 3px solid var(--cyan)`
- `exec-card-gold`：`border-left: 3px solid var(--gold)`
- `exec-card-green`：`border-left: 3px solid var(--green)`
- `exec-card-orange`：`border-left: 3px solid var(--orange)`

### 6.5 竞对画像卡片（profile-card）

结构：
```html
<div class="profile-card">
  <div class="profile-header">
    <div class="profile-avatar">[公司名首字]</div>
    <div>
      <div class="profile-name">[公司全名]</div>
      <div class="profile-role">[定位标签，如：宽覆盖历史积累型]</div>
    </div>
    <div class="profile-badge">[精标件数]件</div>
  </div>
  <div class="profile-body">
    <!-- 8项维度信息 + 综合判断 -->
    <div class="profile-row"><span class="profile-label">核心布局方向</span><span class="profile-val">[值]</span></div>
    <!-- ... -->
  </div>
  <div class="profile-footer">
    <div class="insight insight-[cyan|gold|orange|purple]">[综合判断文字]</div>
  </div>
</div>
```

### 6.6 Insight 色块（insight）

```css
.insight { padding: 12px 16px; border-radius: 6px; font-size: 13px; line-height: 1.7; margin: 8px 0; }
.insight-cyan  { background: rgba(0,212,255,0.08);  border-left: 3px solid var(--cyan);   color: var(--cyan); }
.insight-gold  { background: rgba(255,215,0,0.08);  border-left: 3px solid var(--gold);   color: var(--gold); }
.insight-green { background: rgba(0,255,136,0.08);  border-left: 3px solid var(--green);  color: var(--green); }
.insight-orange{ background: rgba(255,107,53,0.08); border-left: 3px solid var(--orange); color: var(--orange); }
.insight-red   { background: rgba(255,68,68,0.08);  border-left: 3px solid var(--red);    color: var(--red); }
.insight-purple{ background: rgba(168,85,247,0.08); border-left: 3px solid var(--purple); color: var(--purple); }
```

---

## 七、图表容器与图表头

每个图表使用如下包装结构：

```html
<div class="chart-card">
  <div class="chart-header">
    <div class="chart-title">[图表标题]</div>
    <div class="chart-sub">[图表副标题/说明文字]</div>
  </div>
  <div id="[chart-id]" style="height:[Npx];"></div>
</div>
```

CSS：
```css
.chart-card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 20px; }
.chart-header { margin-bottom: 12px; }
.chart-title { font-size: 14px; font-weight: 700; color: var(--white); margin-bottom: 4px; }
.chart-sub { font-size: 12px; color: var(--muted); }
```

---

## 八、标准图表高度

| Chart ID | 推荐高度 |
|---|---|
| chart-legal | 220px |
| chart-radar | 360px |
| chart-protein-heatmap | 320px |
| chart-function-bar | 380px |
| chart-matrix | 420px |
| chart-tech-radar | 340px |
| chart-tech-bar | 340px |
| chart-company-radar | 400px |

---

## 九、ECharts 通用配置原则

所有 ECharts 图表必须使用以下通用配置原则：

```javascript
// 颜色变量（在 <script> 顶部定义）
const bgCard  = '#0d1e33';
const cyan    = '#00d4ff';
const gold    = '#ffd700';
const green   = '#00ff88';
const orange  = '#ff6b35';
const red     = '#ff4444';
const purple  = '#a855f7';
const muted   = '#6b9fc4';
const white   = '#ffffff';
const colors  = [cyan, gold, green, orange, red, purple, '#00ffcc', '#ff9999'];

// 每个图表必须设置
{
  backgroundColor: bgCard,
  textStyle: { color: white, fontFamily: '"Microsoft YaHei", sans-serif' },
  tooltip: { ... },  // 根据图表类型配置
  // 其余配置项...
}
```

### 9.1 饼图（chart-legal）— 法律状态分布

```javascript
// 类型：donut（内半径50%）
// 数据：[有效/授权, 审中/申请中, 失效/无效]
// 颜色：[green, cyan, muted]
// 无图例，使用 label 显示名称+百分比
```

### 9.2 雷达图（chart-radar）— 综合能力对比

```javascript
// 6个维度（根据实际数据动态调整）：
// [布局规模, 蛋白类型广度, 功能覆盖度, 分离技术多样性, 近期活跃度, 法律有效率]
// 4条线对应4家企业，各用不同颜色
// radarShape: 'polygon', splitNumber: 4
// indicator 中 max 值根据实际数据最大值的1.2倍设置
```

### 9.3 热力图（chart-protein-heatmap）— 蛋白类型密度

```javascript
// 类型：heatmap
// X轴：蛋白类型列表（从数据中提取 Top 8–10种）
// Y轴：公司列表（['蒙牛','伊利/综合集','Arla','飞鹤'] 或实际公司）
// 数据：[x_index, y_index, count] 三元组
// visualMap：min=0, max=数据最大值, inRange colors: ['#0d1e33', '#004466', '#006688', cyan]
// 单元格标签：显示件数数字，fontSize: 12, color: white
```

### 9.4 堆叠横向柱状图（chart-function-bar）— 功能热度

```javascript
// 类型：bar, horizontal（xAxis type:'value', yAxis type:'category'）
// Y轴：功能类别列表（Top 8–10项）
// 每个系列 = 一家公司，使用 stack: 'total'
// 每条 bar 末尾显示总数 label
// 颜色依次使用 colors[] 数组
```

### 9.5 气泡散点图（chart-matrix）— 核心矩阵

```javascript
// 类型：scatter
// X轴：蛋白类型（category）
// Y轴：蛋白功能（category）
// symbolSize：根据件数比例 Math.sqrt(count) * 6（最小8，最大60）
// itemStyle.color：使用半透明 cyan，rgba(0,212,255,0.6)
// 悬停tooltip：显示 蛋白类型 + 功能 + 件数 + 主要公司
// 可选：多系列（每家公司一色），数据充足时区分颜色
```

### 9.6 分离技术雷达图（chart-tech-radar）

```javascript
// 维度：根据数据中 分离技术手段 标签去重后的类别（通常6–8种）
// 每条线 = 一家公司
// 无数据维度填0
```

### 9.7 分离技术堆叠柱状图（chart-tech-bar）

```javascript
// 类型：bar, 垂直（xAxis: 公司列表, yAxis: 件数）
// 每个系列 = 一种分离技术手段
// stack: 'total', 显示顶部 total label
```

### 9.8 竞对综合战略雷达图（chart-company-radar）

```javascript
// 维度（8项）：[专利规模, 蛋白类型广度, 功能覆盖, 分离技术, 近期增速, 有效专利占比, 组合集中度, 差异化程度]
// 归一化到 100 分制
// 4家公司各一条线
// areaStyle: { opacity: 0.1 }
```

---

## 十、数据表格样式

```css
table { width: 100%; border-collapse: collapse; }
th { background: rgba(0,212,255,0.1); color: var(--cyan); font-weight: 700; font-size: 12px; letter-spacing: 0.5px; padding: 10px 14px; text-align: left; border-bottom: 1px solid var(--border); }
td { padding: 10px 14px; border-bottom: 1px solid rgba(26,58,92,0.5); font-size: 13px; color: var(--text); vertical-align: top; }
tr:hover td { background: rgba(0,212,255,0.03); }
```

优先级徽章（行动建议章节）：
```css
.priority-a { background: rgba(255,68,68,0.15); color: var(--red); border: 1px solid rgba(255,68,68,0.3); padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700; }
.priority-b { background: rgba(255,215,0,0.15); color: var(--gold); border: 1px solid rgba(255,215,0,0.3); padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700; }
.priority-c { background: rgba(0,212,255,0.1); color: var(--cyan); border: 1px solid rgba(0,212,255,0.2); padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700; }
```

数据边界警告框：
```css
.data-warn { background: rgba(255,215,0,0.05); border: 1px solid rgba(255,215,0,0.2); border-radius: 8px; padding: 12px 16px; font-size: 12px; color: var(--gold); margin-bottom: 20px; }
```

---

## 十一、页脚（footer）

```html
<footer>
  <div class="footer-brand">◈ 乳蛋白深加工专利竞争情报系统</div>
  <div class="footer-meta">循证研究 · 2026年5月 · 基于精细标引专利数据</div>
  <div class="footer-disclaimer">
    本报告基于专利公开数据及精细标引结果，所有结论须结合完整权利要求书、法律状态及市场数据综合判断，不构成法律意见或投资建议。
  </div>
</footer>
```

CSS：
```css
footer {
  position: relative; z-index: 1;
  text-align: center; padding: 60px 40px;
  border-top: 1px solid var(--border);
  background: var(--bg2);
}
.footer-brand { font-size: 18px; font-weight: 800; color: var(--cyan); margin-bottom: 8px; }
.footer-meta { font-size: 13px; color: var(--muted); margin-bottom: 16px; }
.footer-disclaimer { font-size: 11px; color: rgba(107,159,196,0.6); max-width: 600px; margin: 0 auto; line-height: 1.8; }
```

---

## 十二、窗口 resize 响应

在 `</body>` 前的 `<script>` 末尾必须加入：

```javascript
window.addEventListener('resize', () => {
  [legalChart, radarChart, proteinHeatmap, funcBar, matrixChart,
   techRadar, techBar, companyRadar].forEach(c => c && c.resize());
});
```

---

## 十三、内容填充原则

生成 HTML 报告时，所有图表数据必须从实际精标 Excel 数据中提取，不得使用占位符或示例数据。具体要求：

1. **KPI数字**：从实际数据统计而来（总件数、企业数、蛋白类型数、功能维度数）
2. **热力图数据**：基于各公司各蛋白类型的实际标引件数统计
3. **功能热度数据**：基于各公司各功能标签的实际件数统计
4. **矩阵气泡数据**：基于「蛋白类型×功能」组合的实际交叉统计
5. **法律状态饼图**：基于实际法律状态字段统计（有效/审中/失效）
6. **跑马灯文字**：填入实际的统计数据摘要（各公司件数、Top蛋白类型等）
7. **竞对画像**：基于实际标引数据描述，不得凭空推断
8. **行动建议**：A/B/C三级，内容有实际数据支撑

当某字段数据不足时（如分离技术手段标引率低），在对应章节开头添加 `data-warn` 警告框，说明数据边界，然后继续渲染图表（数据不足的维度填0或标注"数据待补充"）。

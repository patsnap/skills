# HTML 报告生成提示词

## 核心原则

生成 HTML 报告时，必须严格遵守以下规范，不得偏离：

## 1. 前端设计规范（强制）

### 设计主题
深色科技主题，背景色 #070b14，不得使用浅色背景。

### 必须引入的资源
```html
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
```

### CSS 变量（每个 HTML 必须完整声明）
```css
:root {
  --bg-base: #070b14;
  --bg-surface: #0d1525;
  --bg-card: #111c33;
  --bg-elevated: #162040;
  --color-primary: #3b82f6;
  --color-accent: #06d6a0;
  --color-warning: #f59e0b;
  --color-danger: #ef4444;
  --color-purple: #8b5cf6;
  --text-primary: #f1f5f9;
  --text-secondary: #94a3b8;
  --text-muted: #475569;
  --border-subtle: rgba(59,130,246,0.15);
  --glow-blue: 0 0 20px rgba(59,130,246,0.3);
  --glow-accent: 0 0 20px rgba(6,214,160,0.3);
  --radius-card: 16px;
  --font-title: 'Sora', sans-serif;
  --font-body: 'Inter', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}
```

## 2. index.html 内容规范（15个区块，正文 ≥ 3000字）

按顺序必须包含：
1. Hero 区（评分环形图 + 标签 + 导航按钮）
2. KPI 概览（≥6个卡片，顶部渐变线）
3. 前言与背景（≥300字）
4. 全球趋势图（ECharts折线，全量分桶数据）+ claim_id
5. 全球 vs 中国对比图（ECharts双线）+ claim_id
6. 子技术热度图（ECharts横向柱状图）+ claim_id
7. 六维评分雷达图 + 得分明细表格
8. 趋势深度分析（≥500字）每个判断带 claim_id 和数据来源
9. 子技术方向分析（≥400字）每个方向带 claim_id
10. 技术空白点（≥3个，每个带数据依据）带 claim_id
11. 综合研发/投资结论（≥400字）明确是否值得投入，带机会/风险/建议，每条带 claim_id
12. 专利布局建议（≥300字）
13. Top 10 代表专利表格（带智慧芽链接）
14. 数据说明与免责
15. 页面导航按钮

## 3. 每条结论必须标注 claim_id

```html
某个重要判断<span class="claim-tag">T001</span>
<div class="data-source-note">数据来源：逐年分桶检索 matched_total，2015-2025年，全量统计</div>
```

## 4. 图表规范

- 所有图表使用 ECharts 5.4.3
- tooltip 必须配置，悬浮显示数值
- 图表背景 transparent
- 轴线颜色 rgba(255,255,255,0.15)
- 分割线颜色 rgba(255,255,255,0.06)
- 轴标签颜色 #94a3b8
- tooltip 背景 rgba(13,21,37,0.95)，边框 rgba(59,130,246,0.3)
- 禁止空图表，所有图表必须有真实数据

## 5. 禁止事项

- 禁止使用 Chart.js
- 禁止使用浅色背景
- 禁止生成申请人排名图、地域分布图、法律状态图
- 禁止空占位符（{{未替换的变量}}）
- 禁止 TODO 注释
- 禁止空图表容器
- 禁止 index.html 正文字数不足 3000 字

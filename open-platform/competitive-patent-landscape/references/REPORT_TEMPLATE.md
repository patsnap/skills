# 报告模板参考

## 五章结构速查

### 第一章：全局一览
优先放「分析结论速览」模块（三大趋势卡片 + 品牌布局速查表 + 一句话总结），再放气泡图和柱状图。

### 第二章：分品牌深度分析
每品牌一张卡：品牌色头部 + 专利簇条形图 + 三大押注方向 + 对客户洞察黄色提示框。

### 第三章：核心专利全文解读
每品牌2-3件精读专利。格式：专利号 pill + 标题 + 核心技术主张（具体参数/结构/方法）+ 全球布局路径 + 战略意图。末尾放品牌全球布局战略对比总结表。

### 第四章：全球布局战略对比
地理热力矩阵（品牌×8大市场）+ 跨市场专题对比（如金佰利美/欧差异）。

### 第五章：战略结论与机会窗口
三张机会卡 + 时间窗口判断表（四色标注）+ 对客户行动建议列表。

---

## 分析结论速览模块 HTML 片段参考

```html
<div class="insight-summary">
  <div class="is-title">📊 分析结论速览</div>
  <!-- 三大趋势卡片 -->
  <div class="trend-cards">
    <div class="trend-card">
      <div class="tc-num">1</div>
      <div class="tc-title">技术趋势标题</div>
      <div class="tc-desc">具体描述...</div>
    </div>
  </div>
  <!-- 品牌布局速查表 -->
  <table class="brand-quick-table">
    <thead><tr><th>品牌</th><th>核心押注方向</th><th>布局强度</th><th>窗口判断</th></tr></thead>
    <tbody>...</tbody>
  </table>
  <!-- 一句话总结 -->
  <div class="summary-quote">一句话核心结论...</div>
</div>
```

## 窗口判断 Badge CSS 类
- 🔴 封锁级：`<span class="window-badge win-red">🔴 封锁级</span>`
- 🟡 窗口期：`<span class="window-badge win-yellow">🟡 12-18月窗口</span>`
- 🟢 可进入：`<span class="window-badge win-green">🟢 可进入</span>`
- ⬜ 跟踪：`<span class="window-badge win-gray">⬜ 跟踪观察</span>`

## 对客户洞察模块
每个品牌分析末尾必须有黄色背景的「对[客户名]的洞察」框，格式：
```html
<div class="winda-note">
  <div class="wlabel">💡 对[客户名称]的洞察</div>
  具体机会或风险描述...
</div>
```

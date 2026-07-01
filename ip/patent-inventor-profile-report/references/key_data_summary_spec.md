### 核心数据摘要卡片规范（KEY DATA SUMMARY）

**位置：** 综合评估模块中，8维度评分卡与核心结论色块之间（全篇概览的数据支撑层）

**触发：** 每次报告均显示（单屏与分屏模式均包含）

**卡片标题：** `核心数据摘要 · KEY DATA SUMMARY`

**样式规范：**
- 背景：`rgba(255,255,255,0.06)` 半透明浅色卡片，与深蓝主背景形成明暗对比
- 边框：`1px solid rgba(77,166,255,0.25)` 科技蓝细边框，圆角 `12px`
- 分割线：`1px solid rgba(255,255,255,0.08)` 浅灰行间分割线
- 标题行：`#4da6ff` 科技蓝，14px，字间距1px
- 维度列（左）：`#a0b4cc` 灰蓝色，13px
- 数值列（右）：`#e0eaff` 高亮白，14px，font-weight:600 加粗
- 评级数值：`#00e676` 绿色加粗，更醒目

**10行固定数据结构：**

| 行号 | 维度 | 数据字段来源 |
|:---:|------|------------|
| 1 | 专利总记录 | A1件（含同族/多次公开号） |
| 2 | 独立发明组（去重估计） | ~{A1*0.6}个（A/B同族去重比例估算） |
| 3 | 已授权有效专利 | SIMPLE_LEGAL_STATUS:(1) 件数 |
| 4 | 审查中 | SIMPLE_LEGAL_STATUS:(2) 件数 + 代表专利号 |
| 5 | 海外布局 | CN({cn_count}) + WO({wo_count}，含PCT) |
| 6 | 总被引次数 | cited_count总和（样本值） |
| 7 | 最高单件被引 | {max_cited}次（{专利号} · {发明主题简述}） |
| 8 | 核心技术域 | IPC TOP3方向中文描述，· 分隔 |
| 9 | 申请高峰期 | 专利申请日集中年份区间 |
| 10 | 综合评级 | {S/A/B/C}级 · {评级标签} |

**综合评级规则（第10行）：**

| 评级 | 标准 | 标签 |
|------|------|------|
| S级 | 主导率≥50% + 被引≥3次/件 + 核心层 | 卓越科创领军人才 |
| A级 | 主导率30～49% + 被引≥1次/件 + 骨干层及以上 | 科创骨干人才 |
| B级 | 主导率10～29% + 有效率≥60% | 科创参与人才 |
| C级 | 主导率<10% 或 有效率<50% | 需补充其他材料 |

**在全篇概览中的位置示意：**
```
综合评估区域
├── ⚠️ 样本说明色块（A1>100时）
├── 8维度评分矩阵
├── ★ 核心数据摘要卡片 ← 新增
│   （10行结构化数据，含综合评级）
└── ● 核心结论色块（深绿渐变）
```

**HTML/CSS代码片段：**
```html
<div class="key-data-summary">
  <div class="kds-title">核心数据摘要 · KEY DATA SUMMARY</div>
  <table class="kds-table">
    <thead><tr><th>维度</th><th>数据</th></tr></thead>
    <tbody>
      <tr><td>专利总记录</td><td>{A1}件（含同族/多次公开号）</td></tr>
      <tr><td>独立发明组（去重估计）</td><td>~{dedup}个</td></tr>
      <tr><td>已授权有效专利</td><td>{active}件</td></tr>
      <tr><td>审查中</td><td>{pending}件（{pending_pn}）</td></tr>
      <tr><td>海外布局</td><td>CN（{cn}）+ WO（{wo}，含PCT）</td></tr>
      <tr><td>总被引次数</td><td>{cited_total}+次</td></tr>
      <tr><td>最高单件被引</td><td>{max_cited}次（{max_pn} · {topic}）</td></tr>
      <tr><td>核心技术域</td><td>{tech_domain}</td></tr>
      <tr><td>申请高峰期</td><td>{peak_years}年</td></tr>
      <tr><td>综合评级</td><td class="rating">{grade}级·{label}</td></tr>
    </tbody>
  </table>
</div>
```
```css
.key-data-summary {
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(77,166,255,0.25);
  border-radius: 12px; padding: 20px; margin: 20px 0;
}
.kds-title { color: #4da6ff; font-size:14px; font-weight:600; margin-bottom:16px; }
.kds-table { width:100%; border-collapse:collapse; }
.kds-table thead th { background:rgba(77,166,255,0.1); color:#4da6ff; padding:8px 12px; text-align:left; }
.kds-table tbody tr { border-bottom:1px solid rgba(255,255,255,0.08); }
.kds-table tbody td:first-child { color:#a0b4cc; padding:10px 12px; }
.kds-table tbody td:last-child { color:#e0eaff; font-weight:600; padding:10px 12px; }
.rating { color:#00e676 !important; font-size:15px; }
```

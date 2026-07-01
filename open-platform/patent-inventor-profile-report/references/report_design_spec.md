# 报告设计规范参考（最新版 2026-05-26 v6.2）

## 标题格式
- 报告中文主标题：高质量技术人才科创能力画像报告（40px，渐变色）
- 报告英文副标题：HIGH-QUALITY TECHNICAL TALENT INNOVATION CAPABILITY PROFILE REPORT（16px，全大写）
- 无emoji icon
- 章节标题：见下方"章节标题升级规范"

## 六大模块（最终版）
1. COMPREHENSIVE INNOVATION CAPABILITY ASSESSMENT / 科创能力综合评级
2. PART I · INNOVATION OUTPUT CAPABILITY / 科创产出能力
3. PART II · TECHNICAL LEADERSHIP CAPABILITY / 技术主导能力
4. PART III · TECHNICAL INFLUENCE / 技术影响力
5. PART IV · INNOVATION ASSET RISK ASSESSMENT / 科创资产风险评估
6. APPENDIX · REPRESENTATIVE INNOVATION ACHIEVEMENTS / 代表性科创成果清单

## ★ 生成过程可视化（v6 新增）

### 触发规则
每次调用 skill 生成报告时，**先展示进度可视化页面**，再生成最终 HTML 报告。

### 进度页面布局
```
┌─────────────────────────────────────────┐
│ 高质量技术人才科创能力画像报告（标题）      │
│ ● 发明人 · 所属机构（蓝色发光脉冲圆点）   │
├─────────────────────────────────────────┤
│ OVERALL PROGRESS ············ 0% → 100% │ ← 总进度条（蓝青渐变发光）
├─────────────────────────────────────────┤
│ ① 企业专利总量查询 P001  [等待→执行→完成] │
│     ↕（连接线·完成后点亮）                │
│ ② 发明人专利清单召回 P002  [运行中🔄]    │
│ ③ 第一发明人核验 A14       [✓ 14件/35%] │
│ ④ 法律状态聚合分析          [✓ 有效62%] │
│ ⑤ 到期预警·被引分析 P012/15 [✓ 36次]   │
│ ⑥ 核心团队定位 C017         [✓ 活跃层]  │
│ ⑦ 学术论文查询 L001         [✓ 0篇]     │
│ ⑧ HTML报告渲染 RENDER       [✓ 完成]    │
├─────────────────────────────────────────┤
│ 🎉 报告生成完成 · 统计摘要（4项KPI）      │
├─────────────────────────────────────────┤
│ [实时日志面板] ← Consolas字体，自动滚动   │
└─────────────────────────────────────────┘
```

### 8大视觉交互特性
| 特性 | 说明 |
|------|------|
| **步骤编号旋转圈** | 执行中状态，外圈蓝色旋转动画 |
| **子进度条** | 每步内部进度条，实时推进 |
| **连接线点亮** | 步骤完成后连接线变蓝青渐变 |
| **左侧竖线变色** | 待执行灰→执行中蓝→完成绿→异常红 |
| **总进度条** | 8步等分，100%=全部完成 |
| **实时日志** | Consolas字体，带时间戳，自动滚动 |
| **完成KPI卡片** | A1/主导率/评级/耗时4项统计 |
| **顶部发明人标签** | 蓝色发光脉冲圆点 + 实时更新 |

### 步骤状态样式
| 状态 | 左侧竖线颜色 | 圆圈样式 | 描述文字 |
|------|:-----------:|---------|---------|
| 等待 | 灰色 | 灰色空圈 | 等待中... |
| 执行中 | 蓝色 | 蓝色旋转圈 | 🔄 执行中 |
| 完成 | 绿色 | 绿色✓填充 | ✓ [结果摘要] |
| 异常 | 红色 | 红色✕填充 | ✕ 异常，已跳过 |

### 进度文件输出
保存至：`@session/reports/progress_[姓名]_[日期].html`

---

## ★ 章节标题升级规范（v5，延续至v6）

### 核心变更：序号放回框内，左侧超大数字+右侧中英文标题

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│  1   INNOVATION OUTPUT CAPABILITY                                │
│      科创产出能力                                                  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

序号位于框内左侧，超大字体（88px），蓝→青渐变发光，与右侧中英文标题左对齐排列。

### 布局结构（框内左右两列）
```
┌─ 左侧竖线(6px) ─────────────────────────────────────────────────┐
│  [ 88px序号 ]  [ 右列：英文13px小标题 ]                           │
│                [ 右列：中文26px大标题 ]                           │
│  ◎右侧光晕                                                       │
└══════════════════════════════════════════════════════════════════┘
 ~~~~底部蓝→青渐变光条(60%宽)~~~~
```

### CSS 规范（v5/v6）
```css
.section-wrapper { margin: 40px 0 0 0; }

.section-header {
  background: linear-gradient(135deg, #0d2147 0%, #0a3070 50%, #0d2147 100%);
  border-left: 6px solid #4da6ff;
  border-bottom: 2px solid rgba(77,166,255,0.3);
  padding: 20px 28px;
  border-radius: 0 8px 8px 0;
  box-shadow: 0 4px 20px rgba(77,166,255,0.15), inset 0 1px 0 rgba(255,255,255,0.05);
  position: relative; overflow: hidden;
  display: flex; align-items: center; gap: 24px;
}

.section-number {
  font-size: 88px; font-weight: 900; line-height: 1; letter-spacing: -4px;
  background: linear-gradient(135deg, #4da6ff, #00e5ff);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  filter: drop-shadow(0 0 20px rgba(77,166,255,0.5));
  flex-shrink: 0; min-width: 80px; text-align: center;
}

.section-title-block {
  display: flex; flex-direction: column; justify-content: center; flex: 1;
}

.section-header .en-title {
  font-size: 13px; font-weight: 700; letter-spacing: 2.5px;
  color: #4da6ff; text-transform: uppercase; margin-bottom: 6px; opacity: 0.9;
}

.section-header .zh-title {
  font-size: 26px; font-weight: 900; color: #ffffff;
  letter-spacing: 3px; line-height: 1.2;
  text-shadow: 0 0 20px rgba(77,166,255,0.4); margin: 0;
}

/* 右侧径向光晕 */
.section-header::after {
  content: ''; position: absolute; right: -30px; top: 50%;
  transform: translateY(-50%); width: 150px; height: 150px;
  background: radial-gradient(circle, rgba(77,166,255,0.1) 0%, transparent 70%);
  pointer-events: none;
}

/* 底部蓝→青渐变光条 */
.section-header::before {
  content: ''; position: absolute; bottom: 0; left: 0;
  width: 60%; height: 2px;
  background: linear-gradient(90deg, #4da6ff, #00e5ff, transparent);
}

/* 正文主体缩进 */
.section-body { padding-left: 32px; margin-top: 20px; }
.section-body .conclusion-block,
.section-body .desc-block,
.section-body table,
.section-body .kpi-group,
.section-body .risk-cards { margin-left: 32px; }
```

### HTML模板（每章节）
```html
<div class="section-wrapper" id="part1">
  <div class="section-header">
    <div class="section-number">1</div>
    <div class="section-title-block">
      <div class="en-title">PART I · INNOVATION OUTPUT CAPABILITY</div>
      <div class="zh-title">科创产出能力</div>
    </div>
  </div>
  <div class="section-body">
    <!-- 结论色块 → KPI卡片 → 数据表格 -->
  </div>
</div>
```

---

## 目录导航栏规范（v6）

```
┌──────┬────────────────────────────────────────────────────────┐
│ 目录  │ 综合评估 │ PART I │ PART II │ PART III │ PART IV │ APPENDIX │
│CONTENTS│ ASSESSMENT │ 科创产出 │ 技术主导 │ 技术影响力│科创风险 │ 代表性成果 │
└──────┴────────────────────────────────────────────────────────┘
```

- 左侧独立标签：`目录 / CONTENTS` + 蓝色发光圆点
- 6个章节 `flex:1` 完全均匀分配
- 三层信息结构：PART N徽章 + 中文标题 + 英文副标题
- hover时底部蓝青渐变光条从中心向两侧展开
- 顶部固定（position: sticky），滚动时始终可见

---

## 单屏规则（v4～v6保持不变）
- **全部统一单屏**（上下滚动），无论A1数量多少，不做左右分屏
- 顶部固定水平目录导航栏（含"目录/CONTENTS"标签）
- 章节均匀分布，flex:1等宽排列
- 右下角悬浮返回顶部按钮（蓝青渐变圆形）

---

## 卷首元数据双语对照
- Inventor / 发明人
- Institution / 所属机构
- Report Date / 报告日期
- Data Source / 数据来源

## 结论色块位置
每章节卷首（标题下方，数据之前），深绿渐变背景+左侧5px亮绿竖线，突出色块前置显示。
标签格式：● CORE CONCLUSION · 核心结论

---

## 主色调
| 用途 | 色值 |
|------|------|
| 主背景 | `#060e1f` |
| 卡片背景 | `#0a1e3d` |
| 科技蓝高亮 | `#4da6ff` |
| 成功绿 | `#00e676` |
| 警告橙 | `#ff9800` |
| 危险红 | `#f44336` |
| 正文白 | `#e0eaff` |

---

## 核心数据摘要卡片（卷首必显10行）
1. 专利总记录（含同族）
2. 独立发明组（去重估计）
3. 已授权有效专利
4. 审查中专利
5. 地理布局
6. 总被引次数
7. 最高单件被引
8. 核心技术域
9. 申请高峰期
10. 综合能力评级（高亮 #00e676）

---

## 综合能力评级（S/A/B/C四级）

> ⚠️ 最高评级为 **S级**，禁止使用 0级。

| 评级 | 条件 | 标签 | 信贷建议 | 颜色 |
|------|------|------|---------|------|
| **S级** | 主导率≥50% + 被引≥3次/件 + 核心层 | 卓越科创领军人才 | 强烈建议支持 | `#00e676` |
| **A级** | 主导率30～49% + 被引≥1次/件 + 骨干层及以上 | 科创骨干人才 | 建议支持 | `#4da6ff` |
| **B级** | 主导率10～29% + 有效率≥60% | 科创参与人才 | 审慎支持 | `#ffb300` |
| **C级** | 主导率<10% 或 有效率<50% | 需补充其他材料 | 需补充其他材料 | `#ff5252` |

---

## 六案例验证记录（v6.2最终）

| 发明人 | 机构 | A1 | 评级 | 显示模式 | 特点 |
|--------|------|----|:----:|:-------:|------|
| 王为磊 | 智慧芽信息科技（苏州）有限公司 | 40件 | **A级** | ⬜ 单屏 | 中文·NLP/专利智能·CN |
| 山田昇平 | 华为技术有限公司 | 158件 | **S级** | ⬜ 单屏 | 日文·LTE无线接入·CN+JP+HK+WO |
| 陈波 | 珠海格力电器股份有限公司 | 362件 | **A级** | ⬜ 单屏 | 中文·洗衣机/热泵·CN |
| 陆威 | 湖南湘投金天钛业科技股份有限公司 | 9件 | **B级** | ⬜ 单屏 | 中文·钛合金锻造·协作型 |
| 袁建栋 | 博瑞生物医药（苏州）股份有限公司 | 360件 | **B级** | ⬜ 单屏 | 中文·生物医药·均衡型·28%代表性 |
| 苏春园 | 杭州观远数据有限公司 | 14件 | **A级** | ⬜ 单屏 | 中文·数据智能·主导率100% |

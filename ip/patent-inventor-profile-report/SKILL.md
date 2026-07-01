---
name: patent-inventor-profile-report
description: |
  高质量技术人才科创能力画像HTML报告生成器（v7.5.1正式版）。输入发明人姓名+所属机构，自动执行多维专利数据检索与分析，生成深蓝色现代科技风格的完整HTML画像报告。每次输出强制以zhang_xian_profile_20260528为黄金标准模版执行格式规范，不可降级、不可跳过任何格式要素。综合评级体系采用S/A/B/C四级（最高为S级·卓越科创领军人才，严禁使用0级）。Step1/Step2专利超过100件时强制分页返回全量数据（循环分页，≤1000件上限，不可抽样替代）。
---

# patent-inventor-profile-report（v7.5.1）

## 功能定位

根据指定**发明人**与**所属机构**，调用专利数据库完成全维度分析，生成符合大厂/银行风格的专业HTML画像报告。

**核心叙事逻辑：以"人才科创能力评估"为主题，而非"专利统计报告"。**

| 旧版视角（专利统计） | 新版视角（人才科创能力） |
|-------------------|----------------------|
| "这个人有多少专利？" | **"这个人的科创能力有多强？"** |
| 专利数据是主体 | 专利数据是**佐证材料** |
| 面向专利分析师 | 面向**银行信贷经理/HR/投资人** |
| 输出专利分布图谱 | 输出**人才科创能力评级 + 信贷支撑建议** |

---

## ⚠️⚠️⚠️ 强制执行·黄金模版规范（最高优先级）

**每次生成报告，必须100%严格执行以下格式规范，来源：`zhang_xian_profile_20260528.html`。不可降级、不可跳过任何项目。**

### 1. CSS变量体系（强制）

```css
:root {
  --bg-deep: #060e1f; --bg-card: #0a1628; --bg-card2: #0d1e35;
  --blue-main: #4da6ff; --blue-light: #00e5ff;
  --green-main: #00e676; --orange: #ffb300; --red: #ff5252;
  --text-primary: #e0eaff; --text-secondary: #8aa4c8;
  --text-muted: #4a6a9a; --border: rgba(77,166,255,0.15);
}
```

### 2. 顶部导航栏（强制）

```html
<nav class="top-nav">
  <div class="nav-logo">
    <span class="logo-cn">目录</span>
    <span class="logo-en">CONTENTS</span>
  </div>
  <div class="nav-items">
    <a href="#assessment" class="nav-item"><span class="nav-cn">科创能力综合评级</span></a>
    <a href="#part1"      class="nav-item"><span class="nav-cn">科创产出能力</span></a>
    <a href="#part2"      class="nav-item"><span class="nav-cn">技术主导能力</span></a>
    <a href="#part3"      class="nav-item"><span class="nav-cn">技术影响力</span></a>
    <a href="#part4"      class="nav-item"><span class="nav-cn">科创资产风险评估</span></a>
    <a href="#appendix"   class="nav-item"><span class="nav-cn">代表性科创成果清单</span></a>
  </div>
</nav>
```

- ❌ 禁止在导航项中出现 PART N 徽章
- ❌ 禁止在导航项中出现英文副标题
- ✅ 每项仅显示 `<span class="nav-cn">中文章节名</span>`

### 3. Header 区域（强制）

```html
<div class="report-header">
  <div class="header-name-block">
    <div class="header-report-label">高质量技术人才科创能力画像报告</div>
    <div class="header-name">{{inventor}}</div>
    <div class="header-company">{{assignee}}</div>
  </div>
  <div class="header-tags">
    <div class="header-tag"><span class="tag-icon">📅</span><span class="tag-label">报告日期:</span><span class="tag-value">{{report_date}}</span></div>
    <div class="header-tag"><span class="tag-icon">🌐</span><span class="tag-label">技术领域:</span><span class="tag-value">{{tech_domain}}</span></div>
    <div class="header-tag"><span class="tag-icon">📊</span><span class="tag-label">专利数量:</span><span class="tag-value">{{sample_scale}}</span></div>
    <div class="header-tag"><span class="tag-icon">📍</span><span class="tag-label">主要布局:</span><span class="tag-value">{{jurisdiction}}</span></div>
  </div>
</div>
```

- ✅ 姓名左对齐，42px，蓝青渐变大字
- ✅ 机构名紧跟姓名下方，浅色16px小字
- ✅ 底部4个横排胶囊标签
- ❌ 禁止居中对齐姓名
- ❌ 禁止使用旧版2×2网格卡片

### 4. 核心数据摘要卡片（强制，紧跟Header正下方）

```html
<div class="key-data-card">
  <div class="key-data-title">● CORE DATA SUMMARY · 核心数据摘要</div>
  <div class="key-data-grid">
    <div class="key-data-row"><span class="kd-label">专利总量（全量精确）</span><span class="kd-value highlight">X 件</span></div>
    <div class="key-data-row"><span class="kd-label">地理布局</span><span class="kd-value">CN（X件）· WO（X件）</span></div>
    <div class="key-data-row"><span class="kd-label">有效率</span><span class="kd-value highlight">XX%（X件有效）</span></div>
    <div class="key-data-row"><span class="kd-label">审查中</span><span class="kd-value">X件（pending）</span></div>
    <div class="key-data-row"><span class="kd-label">被引总次数</span><span class="kd-value warn">X 次</span></div>
    <div class="key-data-row"><span class="kd-label">最高单件被引</span><span class="kd-value warn">X次 · 专利号</span></div>
    <div class="key-data-row"><span class="kd-label">核心技术域</span><span class="kd-value">技术方向1 · 技术方向2</span></div>
    <div class="key-data-row"><span class="kd-label">活跃年段</span><span class="kd-value">XXXX — XXXX年</span></div>
    <div class="key-data-row"><span class="kd-label">主导率（第一发明人）</span><span class="kd-value highlight">XX%（X/X件）</span></div>
    <div class="key-data-row"><span class="kd-label">综合能力评级</span><span class="kd-value highlight">X级 · 标签</span></div>
  </div>
</div>
```

- ✅ 10行2列网格（`grid-template-columns: 1fr 1fr`）
- ✅ 标题固定为 `● CORE DATA SUMMARY · 核心数据摘要`
- ✅ highlight颜色=`var(--green-main)`，warn颜色=`var(--orange)`
- ❌ 禁止省略此卡片
- ❌ 禁止少于10行

### 5. 章节标题（强制）

```html
<div class="section-title">
  <div class="st-num">0</div>  <!-- 88px渐变大数字，0/1/2/3/4/A -->
  <div class="st-text">
    <div class="st-cn">科创能力综合评级</div>  <!-- 26px/900字重/纯中文 -->
  </div>
</div>
```

- ✅ 序号：88px/900字重，蓝→青渐变，`filter:drop-shadow(0 0 20px rgba(77,166,255,0.4))`
- ✅ 标题：26px/900字重/字间距3px，纯中文
- ❌ 禁止在 `.st-text` 内出现任何英文副标题（如 output / leadership）
- ❌ 禁止修改序号：必须为 0/1/2/3/4/A

**六章节固定对照：**
| 序号 | 中文标题 | id |
|:----:|---------|-----|
| 0 | 科创能力综合评级 | assessment |
| 1 | 科创产出能力 | part1 |
| 2 | 技术主导能力 | part2 |
| 3 | 技术影响力 | part3 |
| 4 | 科创资产风险评估 | part4 |
| A | 代表性科创成果清单 | appendix |

### 6. 综合评级卡（强制）

```html
<div class="rating-card">
  <div class="rating-level">A 级</div>      <!-- 48px/900字重 -->
  <div class="rating-label">优秀科创专家</div>
  <div class="rating-credit">✅ 信贷建议：建议支持 · 说明文字</div>
</div>
```

- ✅ 评级字体48px，颜色`var(--green-main)`
- ✅ 仅使用 S/A/B/C 四级，**严禁使用0级**

### 7. 五维能力矩阵（强制）

```html
<div class="matrix-grid">  <!-- grid-template-columns: repeat(5,1fr) -->
  <div class="matrix-card">
    <div class="matrix-icon">🧠</div>
    <div class="matrix-name">独立研发能力</div>
    <div class="matrix-stars">★★★★★</div>
    <div class="matrix-desc">描述文字</div>
  </div>
  <!-- 📈技术产出能力 / 🏆技术权威地位 / 🌏技术创新广度 / 🛡️科创资产安全 -->
</div>
```

### 8. KPI卡片组（强制）

```html
<div class="kpi-grid">  <!-- grid-template-columns: repeat(4,1fr) -->
  <div class="kpi-card">
    <div class="kpi-num">61</div>
    <div class="kpi-unit">件（全量）</div>
    <div class="kpi-label">专利总量</div>
  </div>
  <!-- 共4个卡片 -->
</div>
```

### 9. 进度条（强制）

```html
<div class="progress-row">
  <span class="progress-label">✅ 有效 active</span>
  <div class="progress-bar"><div class="progress-fill green" style="width:64%"></div></div>
  <span class="progress-val">39件</span>
</div>
```

- `green`：`var(--green-main)→#69f0ae`
- `orange`：`var(--orange)→#ffe57f`
- `red`：`var(--red)→#ff8a80`
- 默认（无class）：`var(--blue-main)→var(--blue-light)`

### 10. 两列布局（强制）

```html
<div class="two-col">  <!-- grid-template-columns: 1fr 1fr; gap:16px -->
  <div class="sub-card">...</div>
  <div class="sub-card">...</div>
</div>
```

### 11. 附录专利表（强制）

```html
<table class="data-table">
  <thead>
    <tr>
      <th>#</th><th>专利号</th><th>标题</th>
      <th>公开日</th><th>IPC</th><th>状态</th><th>被引</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td><a href="https://eureka.zhihuiya.com/view/#/fullText?patentId=..." target="_blank">CN...</a></td>
      <td>专利标题</td>
      <td>YYYY-MM-DD</td>
      <td>IPC分类</td>
      <td><span class="badge badge-active">有效</span></td>
      <td class="cited-high">X次</td>
    </tr>
  </tbody>
</table>
```

- ✅ 至少15件代表性专利
- ✅ 专利号为可点击智慧芽链接
- ✅ 状态用 `.badge-active/.badge-pending/.badge-inactive`

### 12. 风险三项（强制）

```html
<div class="risk-grid">  <!-- grid-template-columns: repeat(3,1fr) -->
  <div class="risk-card safe/warn">
    <div class="risk-icon">✅/⚠️</div>
    <div class="risk-level">无诉讼记录</div>
    <div class="risk-desc">描述</div>
  </div>
  <!-- 诉讼风险 / 质押风险 / 失效风险 共3项 -->
</div>
```

### 13. 段间距规范（强制）

```
section ↔ section：margin-bottom: 32px
标题 ↔ 正文：margin-bottom: 20px
结论块 ↔ 内容：margin-bottom: 16px
内容元素间：8～14px
KPI卡片组：gap: 16px
```

- ❌ 禁止使用 margin-bottom: 48px 或以上（过大段间距）

### 14. 页脚与返回顶部按钮（强制）

```html
<div class="report-footer">
  EUREKA · PatSnap · 高质量技术人才科创能力画像报告 · v7.5.1 · {{report_date}}
</div>
<button class="back-top" onclick="window.scrollTo({top:0,behavior:'smooth'})">↑</button>
```

---

## ⚠️ 发明人姓名匹配预检（必须）

常见问题：`IN:(唐永)` 匹配到多个发明人。
**预检流程：**
```
1. 执行 AN:(assignee) AND IN:(inventor_keyword)，topk=10
2. 统计 inventors 字段各名称出现频次
3. 确认精确姓名后再执行全量分析
```

---

## ⚠️⚠️ 强制分页全量检索规则（v7.5.1·最高优先级）

**专利超过100件时，Step1/Step2 必须执行分页全量检索，不可抽样替代，不可降级。**

```
offset = 0
all_results = []
DO:
  results = search(query, topk=100, offset=offset)
  all_results += results
  offset += 100
WHILE len(results) == 100 AND offset < matched_total AND offset < 1000

最终：A1 = len(all_results)
标注：✅ 100%全量精确（≤1000件）
     或：已采集1000件/全量X件（覆盖率XX%）
```

- ❌ 禁止单次返回即停止
- ❌ 禁止标注"topk样本"替代全量
- ❌ 禁止以"样本代表性"替代分页

| 样本规模 | 处理方式 | 报告标注 |
|---------|---------|---------|
| ≤100件 | 单次，全量精确 | `✅ 全量精确（X件）` |
| 101～500件 | 强制分页2～5次 | `✅ 100%全量精确（X件）` |
| 501～1000件 | 强制分页6～10次 | `✅ 100%全量精确（X件）` |
| >1000件 | 采集上限1000件 | `已采集1000件/全量X件（覆盖率XX%）` |

---

## 执行流程（七步数据采集）

### Step 0：发明人姓名预检（必须）

### Step 1：企业总量（P001）—— 强制分页全量
```
ALL_AN:(assignee)
```

### Step 2：发明人全量清单（P002）—— 强制分页全量
```
AN:(assignee) AND IN:(inventor)
topk=100，date_type=publication，降序
```
- 超100件必须分页至全量
- A1 = 精确全量值，非样本估算

### Step 3：第一发明人（A14）
逐条核验 `inventors[0] == inventor`，计算主导率 A14/A1。

| A14/A1 | 类型 |
|:------:|------|
| ≥50% | 🏆 主导型 |
| 30%～49% | 🥈 均衡偏主导型 |
| 10%～29% | 🥉 均衡型 |
| <10% | 📋 协作型 |

### Step 4：法律状态分布
从全量结构化数据聚合六态分布。

### Step 5：到期预警
```
EXDT:[TODAY TO TODAY+3Y] AND ANC:(assignee) AND IN:(inventor)
```

### Step 6：核心团队定位
```
ALL_AN:(assignee) topk=100
```
四层分级：核心层(≥13) / 骨干层(7～12) / 活跃层(5～6) / 参与层(1～4)

### Step 7：论文查询
```
authors:(inventor)  sources=["paper"]
```

---

## 报告结构（六大模块）

```
【卷首·全宽】Header区域（左对齐姓名+底部4胶囊标签）
【核心数据摘要卡片】（10行2列，Header正下方，必须存在）
【0】科创能力综合评级（rating-card + matrix-grid五维矩阵）
【1】科创产出能力（kpi-grid + two-col进度条）
【2】技术主导能力（kpi-grid + two-col进度条）
【3】技术影响力（kpi-grid + two-col进度条）
【4】科创资产风险评估（risk-grid三项）
【A】代表性科创成果清单（data-table ≥15件，含链接）
【页脚】EUREKA · PatSnap · v7.5.1
【返回顶部按钮】右下角蓝青渐变圆形
```

---

## 综合能力评级体系（S/A/B/C四级）

> ⚠️ 最高评级为 **S级**，**严禁使用 0级**。

| 评级 | 触发条件 | 标签 | 信贷建议 |
|------|---------|------|---------|
| **S级** | 主导率≥50% + 被引≥3次/件 + 核心层 | 卓越科创领军人才 | 强烈建议支持 |
| **A级** | 主导率30～49% + 被引≥1次/件 + 骨干层及以上 | 科创骨干人才 | 建议支持 |
| **B级** | 主导率10～29% + 有效率≥60% | 科创参与人才 | 审慎支持 |
| **C级** | 主导率<10% 或 有效率<50% 或 A1≤5件 | 科创初始阶段 | 需补充其他材料 |

---

## 🖥️ 显示规则

**全部统一单屏（上下滚动），不做左右分屏。**

---

## 已验证案例

| 发明人 | 机构 | A1 | 评级 |
|--------|------|----|:----:|
| 王为磊 | 智慧芽信息科技（苏州）有限公司 | 40件 | **A级** |
| 山田昇平 | 华为技术有限公司 | 158件 | **S级** |
| 陈波 | 珠海格力电器股份有限公司 | 362件 | **A级** |
| 袁建栋 | 博瑞生物医药（苏州）股份有限公司 | 360件 | **B级** |
| 苏春园 | 杭州观远数据有限公司 | 14件 | **A级** |
| 孙秋月 | 江西秋实工业设备有限公司 | 1件 | **C级** |
| 曹雪 | 京东方科技集团股份有限公司 | 199件 | **B级** |
| 杨建中 | 武汉华中数控股份有限公司 | 42件 | **A级** |
| 唐永彬 | 腾讯科技（深圳）有限公司 | 26件 | **B级** |
| 张显 | 安徽枡水新能源科技有限公司 | 61件 | **A级** |

---

## 输出

1. **画像报告**：`@session/reports/[姓名拼音]_profile_[日期].html`

完整自包含 HTML 文件（inline CSS+JS，无外部依赖）。

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。

# 输出格式合同 — mab-fto-check

## 输出产物清单

| 文件名 | 说明 | 生成步骤 |
|--------|------|----------|
| `tech_profile.md` | 技术解析卡片 | 步骤0 |
| `competitor_entity_map.md` | 竞品关联实体图谱 | 步骤3 |
| `patent_pool.json` | 原始专利池（去重） | 步骤1–2 |
| `patent_pool_filtered.json` | 过滤后专利池 | 步骤4 |
| `patent_pool_family.json` | 同族合并后专利池（B文本标注） | 步骤4（同族合并） |
| `blocking_candidates.json` | 阻碍性候选专利 | 步骤5 |
| `claim_diff_matrix.md` | 权利要求比对矩阵 | 步骤6 |
| `risk_summary.json` | 风险评级汇总 | 步骤6 |
| `sequence_alignment_log.md` | 序列比对日志 | 步骤1 |
| `fto_report.html` | **完整FTO报告（HTML单文件）** | 步骤7 |

---

## HTML报告总体要求

```
- 格式：单文件自包含 HTML（内联CSS+JS，无外部依赖）
- 配色：深海蓝商务风（见下方CSS规范）
- 风险徽章：🔴极高风险(#c0392b) / 🔴高风险(#e74c3c) / 🟡中风险(#f39c12) / 🟢低风险(#27ae60)
- 专利号超链接：点击跳转 eureka.zhihuiya.com/search?q={专利号}
- 目录导航：封面后、正文container前，独立目录块，七章锚点
- 章节容器：白色卡片，圆形章节编号
- @media print：适配A4打印
```

---

## HTML报告 CSS/JS 核心规范

> ⚠️ 以下为强制执行的样式规范，每次生成报告必须严格遵循，不得随意修改颜色变量或类名。

```css
:root {
  --navy: #0d2a4a;
  --blue: #1a4f8a;
  --accent: #2e7dc4;
  --accent-light: #e8f4fd;
  --bg: #f0f4f8;
  --text: #2c3e50;
  --border: #d1dce8;
  --risk-extreme: #c0392b;
  --risk-high: #e74c3c;
  --risk-mid: #f39c12;
  --risk-low: #27ae60;
  --risk-none: #95a5a6;
}

/* 封面 */
.cover {
  background: linear-gradient(135deg, var(--navy) 0%, var(--blue) 60%, var(--accent) 100%);
  color: white;
  padding: 80px 60px;
  text-align: center;
  min-height: 320px;
}
.cover h1 { font-size: 2.2rem; margin-bottom: 12px; }
.cover .subtitle { font-size: 1.1rem; opacity: 0.85; }
.cover .badge {
  display: inline-block; margin-top: 20px;
  background: rgba(255,255,255,0.15);
  border: 1px solid rgba(255,255,255,0.3);
  border-radius: 20px; padding: 4px 16px; font-size: 0.85rem;
}

/* 目录（封面后、container前） */
.toc-wrap {
  max-width: 960px; margin: 32px auto; padding: 0 24px;
}
.toc-block {
  background: #fff;
  border-left: 4px solid var(--accent);
  border-radius: 8px;
  padding: 24px 28px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.toc-block h2 {
  font-size: 1.1rem; color: var(--navy);
  margin-bottom: 16px; font-weight: 700;
}
.toc-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px 24px;
}
.toc-grid a {
  color: var(--accent); text-decoration: none;
  font-size: 0.95rem; padding: 4px 0;
  border-bottom: 1px dashed var(--border);
  transition: color 0.2s;
}
.toc-grid a:hover { color: var(--navy); text-decoration: underline; }

/* 正文容器 */
.container { max-width: 960px; margin: 0 auto; padding: 24px; }

/* 章节 */
.section {
  background: #fff;
  border-radius: 12px;
  padding: 32px;
  margin-bottom: 28px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.section-header {
  display: flex; align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px solid var(--accent-light);
}
.section-num {
  width: 40px; height: 40px;
  background: var(--navy);
  color: white;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 1rem;
  margin-right: 14px; flex-shrink: 0;
}
.section-title { font-size: 1.2rem; font-weight: 700; color: var(--navy); }

/* 信息卡片 */
.info-card {
  background: var(--accent-light);
  border-left: 3px solid var(--accent);
  border-radius: 6px;
  padding: 14px 18px;
  margin-bottom: 16px;
}
.info-card .label { font-weight: 600; color: var(--navy); margin-bottom: 4px; }
.info-card .value { color: var(--text); }

/* 序列块 */
.seq-block {
  background: #1a1a2e;
  color: #e0e0e0;
  font-family: 'Courier New', monospace;
  font-size: 0.85rem;
  padding: 16px;
  border-radius: 8px;
  word-break: break-all;
  line-height: 1.8;
  margin: 12px 0;
}

/* 表格 */
table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 0.9rem; }
th {
  background: var(--navy);
  color: white;
  padding: 10px 12px;
  text-align: left;
  font-weight: 600;
}
td { padding: 9px 12px; border-bottom: 1px solid var(--border); }
tr:hover td { background: #f8fafc; }

/* 风险徽章 */
.risk-badge {
  display: inline-block;
  padding: 3px 10px; border-radius: 12px;
  font-size: 0.8rem; font-weight: 600; color: white;
}
.risk-extreme { background: var(--risk-extreme); }
.risk-high    { background: var(--risk-high); }
.risk-mid     { background: var(--risk-mid); }
.risk-low     { background: var(--risk-low); }
.risk-none    { background: var(--risk-none); }

/* 权利要求原文块 */
.claim-text-en {
  border-left: 4px solid var(--accent);
  background: #f0f5ff;
  padding: 10px 16px;
  font-size: 0.88rem;
  line-height: 1.7;
  margin: 8px 0;
  border-radius: 0 6px 6px 0;
}
.claim-text-cn {
  border-left: 4px solid var(--risk-low);
  background: #f6ffed;
  padding: 10px 16px;
  font-size: 0.88rem;
  line-height: 1.7;
  margin: 8px 0;
  border-radius: 0 6px 6px 0;
}

/* 比对矩阵 */
.check-yes { color: #27ae60; font-weight: 700; }
.check-no  { color: #e74c3c; font-weight: 700; }
.check-na  { color: #95a5a6; }

/* 页脚 */
.footer {
  background: linear-gradient(135deg, var(--navy) 0%, var(--blue) 100%);
  color: rgba(255,255,255,0.8);
  text-align: center;
  padding: 28px;
  font-size: 0.85rem;
  margin-top: 40px;
}

@media print {
  .toc-wrap, .toc-block { display: none; }
  .section { box-shadow: none; border: 1px solid var(--border); }
  .footer { background: #333; }
}
```

```javascript
// 高风险卡片默认展开，中/低风险折叠
document.querySelectorAll('.patent-card').forEach(card => {
  const isHigh = card.querySelector('.risk-extreme, .risk-high');
  const body = card.querySelector('.patent-card-body');
  if (body) body.style.display = isHigh ? 'block' : 'none';
});
function toggleCard(id) {
  const b = document.querySelector('#' + id + ' .patent-card-body');
  if (b) b.style.display = b.style.display === 'none' ? 'block' : 'none';
}
```

---

## 报告HTML骨架结构（强制顺序）

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>...内联CSS...</head>
<body>
  <!-- 1. 封面 -->
  <div class="cover">...</div>

  <!-- 2. 目录（封面后、container前，不在container内） -->
  <div class="toc-wrap">
    <div class="toc-block">
      <h2>📋 目录</h2>
      <div class="toc-grid">
        <a href="#ch1">一、目标方案概述</a>
        <a href="#ch2">二、FTO关注方向</a>
        <a href="#ch3">三、检索策略</a>
        <a href="#ch4">四、风险专利清单</a>
        <a href="#ch5">五、侵权比对过程</a>
        <a href="#ch6">六、结论与建议</a>
        <a href="#ch7">七、附录</a>
      </div>
    </div>
  </div>

  <!-- 3. 正文 -->
  <div class="container">
    <div class="section" id="ch1">...</div>
    <div class="section" id="ch2">...</div>
    <div class="section" id="ch3">...</div>
    <div class="section" id="ch4">...</div>
    <div class="section" id="ch5">...</div>
    <div class="section" id="ch6">...</div>
    <div class="section" id="ch7">...</div>
  </div>

  <!-- 4. 页脚 -->
  <div class="footer">...</div>

  <script>...内联JS...</script>
</body>
</html>
```

---

## 专利号超链接规范

```html
<!-- 所有专利号均须使用此格式，不得使用纯文本 -->
<a href="https://eureka.zhihuiya.com/search?q=CN101910199B"
   target="_blank" rel="noopener">CN101910199B</a>
```

适用范围：四（风险专利清单表格）、五（侵权比对标题）、七（附录B诉讼案例）的全部专利公开号。

---

## 独立权利要求识别与展示规范

### 识别规则
```
独立权利要求 = 权利要求文本中不引用任何其他权利要求
  → 英文标志：不含 "of claim"、"according to claim"、"as defined in claim"
  → 中文标志：不含 "根据权利要求"、"如权利要求"、"按照权利要求"

从属权利要求 = 权利要求文本中明确引用其他权利要求（仅做附加限定，不单独比对）
```

### 展示格式（第五章每件专利）
```
[专利号超链接] 独立权利要求识别
  ├── 权利要求1：不引用任何其他权利要求 → ✅ 独立权利要求
  ├── 权利要求2："The antibody of claim 1..." → 从属（引用#1），跳过
  └── 权利要求8：不引用任何其他权利要求 → ✅ 独立权利要求

独立权利要求原文（PatSnap MCP获取）：
  [英文原文]
  译文：[中文译文]

权利要求来源标注：
  ✅ PatSnap MCP实时获取 | 📁 本地缓存 | ⚠️ 未获取（暂缓比对）
```

---

## 第一章 目标方案概述

```
1.1 候选分子基本信息
    - 分子名称/内部编号
    - 抗体类型（IgG1/IgG4/双抗/ADC等）
    - 靶点（若有）
    - 适应症
    - Fc改造/修饰信息
    - 候选序列（展示于 .seq-block 块）
1.2 分析目的与范围
1.3 分析日期与声明
```

---

## 第二章 FTO关注方向

```
2.1 目标地域（用户确认的目标市场，逐一列明）
    - 展示每个目标市场的国家/地区代码及全称
    - PCT指定期说明（如适用）
2.2 专利法律状态限定
    - 有效（active）专利说明
    - 审中（pending）专利说明及不确定性提示
    - PCT指定期内专利的特殊处理
2.3 分析边界说明
    - 同族合并规则（B文本优先）
    - 检索截止日期
    - 本报告不涵盖的范围
```

---

## 第三章 检索策略

```
3.1 序列检索策略（M1）
3.2 修饰检索策略（M1.5，含中文专项关键词）
3.3 关键词检索策略（M2–M8）
    - 第一轮核心关键词
    - 第二轮补充扩展关键词（7类扩展方向：中文专项/等同表达/相关突变/
      申请人检索/IPC分类/PCT专项/功能性等同）
3.4 竞品企业检索策略（M9）
3.5 检索结果统计
```

---

## 第四章 风险专利清单

**必含表格字段**（所有专利号须带超链接）：

| 专利（申请）公开号 | 法律状态 | 专利权人 | 申请日 | 预估到期日 | 公开国别 | 风险等级 |
|---|---|---|---|---|---|---|

**排序规则**：风险等级降序（🔴极高 > 🔴高 > 🟡中 > 🟢低）→ 申请日升序

**特殊标注**：
- 中文专项检索独立命中 → 「★CN专项」
- PCT指定期内 → 「⏳PCT」
- B文本（已授权） → 「✅授权」
- 含PTA补偿 → 「+PTA」

---

## 第五章 侵权比对过程

每件风险专利按以下标准卡片展示：

```
5.X.1 专利基本信息（公开号超链接、专利权人、申请日、到期日）
5.X.2 独立权利要求识别说明
5.X.3 独立权利要求原文（英文原文 + 中文译文，来源标注）
5.X.4 权利要求特征拆解（编号：F1、F2、F3…）
5.X.5 候选分子特征逐项比对（claim_diff_matrix表格）
5.X.6 字面侵权分析结论
5.X.7 等同原则分析（字面不侵权时）
5.X.8 专利比对结论
```

claim_diff_matrix 表格格式：
```
| 特征编号 | 权利要求特征描述（原文） | 候选分子对应特征 | 字面覆盖 | 等同覆盖 | 小结 |
|---|---|---|---|---|---|
| F1 | ... | ... | ✅/❌ | ✅/❌/N/A | 覆盖/不覆盖/争议 |
```

---

## 第五章至第七章

### 第六章 结论与建议
```
6.1 总体风险评估结论（🔴/🟡/🟢 + 简要依据）
6.2 各目标市场风险分级汇总表
6.3 设计绕开建议（逐件高/极高风险专利）
6.4 专利布局建议
6.5 后续行动建议（分阶段：0–1月/1–3月/3–6月/持续）
```

### 第七章 附录
```
附录A 司法条款
  - CN：专利法第11条、第64条；全面覆盖原则；等同原则
  - US：35 U.S.C. § 271；All Elements Rule；等同原则
  - EP：EPC Article 69 + Protocol；等同原则各国差异
  - JP：特許法第68条/第70条

附录B 诉讼案例参考（专利号带链接）
  | 案件 | 原告 | 被告 | 法院 | 判决年份 | 核心争议 | 结果 |

附录C 免责声明（固定文本，见下方）
```

### 附录C 免责声明（固定文本）
```
尽管本报告中包含的信息是从被认为可靠的资源获取的，但本报告作者不对此类
信息的准确性、完整性或充分性作出任何保证，对本报告包含的信息或其解释中的
错误、遗漏或不充分不承担任何法律责任。本报告仅仅根据委托人针对特定事项的
专项委托而做出，报告本身对委托人及其他任何机关、单位、个人均不具有法律约
束力或证明力。使用本报告时应当充分注意保持其完整性和严肃性，任何人不得为
任何目的而断章取义。本报告仅具有供委托人决策时参考使用的价值，即使委托人
根据报告的指引而做出了相应的经营决策并导致了任何损害后果，本所不对此承担
任何法律责任。

本报告不纳入失效专利。如需技术溯源或无效宣告准备，请另行委托专项检索。
报告生成日期：[YYYY-MM-DD]；数据库检索截止日期：[YYYY-MM-DD]。
本报告有效期建议不超过6个月。
```

---

## patent_pool_family.json 字段规范

```json
{
  "family_seq": "1",
  "family_id": "WO2009086320A1",
  "priority_date": "2007-12-26",
  "assignee": ["Xencor Inc."],
  "risk_level": "high|medium|low|exempt",
  "representative_pn": "（B文本优先的专利号）",
  "representative_claim_text": "（B文本独立权利要求原文）",
  "representative_claim_cn": "（中文译文）",
  "claim_source": "B文本|A文本（审中）|PatSnap MCP获取",
  "independent_claims": ["1", "8"],
  "members": [
    {
      "seq": "1-1",
      "pn": "EP2444423B1",
      "jurisdiction": "EP",
      "legal_status": "active",
      "grant_status": "granted",
      "application_date": "2008-09-22",
      "expiry_date": "2028-09-22",
      "pta_applied": false,
      "patsnap_url": "https://eureka.zhihuiya.com/search?q=EP2444423B1"
    }
  ],
  "source_modules": ["M1", "M2"],
  "notes": ""
}
```

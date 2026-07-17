# Legacy deep single-drug report specification

Use this file only when the user requests the `deep` report format.

## Contents

- Original 11+ step research workflow
- Detailed module-level tool instructions
- HTML, chart, and writing requirements
- Cross-validation table and scenario scoring
- Completeness checklist and disclaimers

---
name: drug-lifecycle-evaluation
description: >
  单药综合评估工作流：面向医药客户经理、BD团队、研发策略部门。
  输入目标药物名称，依次调用智慧芽生命科学MCP工具完成实体标准化、
  研发里程碑、适应症、流行病学、临床指南、MoA靶点（含耐药机制）、竞品格局、
  关键临床数据、转化医学证据、BD动向、专利格局全11维度检索，生成楷体/Times New Roman
  双字体、含ECharts图表、每章含数据来源框与摘要框、末章含数据交叉验证
  的完整HTML评估报告，内容不得精简。
---

# 单药综合评估 Skill（drug-lifecycle-evaluation）

## 1. 适用场景

当用户输入一个药物名称（中文/英文/通用名/品牌名均可），并要求进行以下任意一种分析时触发本 Skill：

- 单药评估报告 / 药物综合评估
- 药物档案构建 / 药物情报梳理
- 某药物的潜力判断 / 投资价值分析
- 某药物的全面研究（适应症 + 临床 + 专利 + BD 等）

**不适用场景：**
- 仅需单一维度查询（如"查某药的专利"→使用 all-in-one-ip-skills）
- 管线/公司画像（→使用 patsnap-lifescience-company-profiling_zh）
- 靶点情报（→使用 patsnap-lifescience-target-intelligence_zh）

---

## 2. 工作流总览（11步顺序执行）

```
Step 1   实体标准化          → ls_ner_nor_normalize
Step 2   药物基本档案        → ls_drug_fetch（用Step1返回的Drug ID）
Step 3   研发里程碑时间线    → ls_drug_milestone_fetch
Step 4   主要适应症检索      → ls_drug_search + ls_disease_fetch
Step 5   流行病学分析        → ls_epidemiology_vector_search + ls_paper_vector_search
Step 6   临床指南地位        → ls_clinical_guideline_vector_search + ls_fda_label_vector_search
Step 7   MoA靶点分析+耐药   → ls_target_fetch + ls_paper_vector_search（耐药机制）
Step 8   竞品格局分层        → ls_drug_search（MoA+适应症双重过滤）+ ls_clinical_trial_search
Step 9   关键临床数据        → ls_clinical_trial_result_search + ls_paper_search
Step 9.5 转化医学证据        → ls_translational_medicine_search（★新增，必须执行）
Step 10  BD动向与专利格局    → ls_drug_deal_search（三层强制）+ ls_news_vector_search（强制）
         专利检索            → patsnap_search（patent.search，EP/US/CN分管辖）
Step 11  综合潜力判断        → 按资产/方向分层打分矩阵（禁止单一总分）
Step 12  HTML报告生成        → files（begin_write → append × N → finish_write）
```

---

## 3. 各步骤工具调用规范

### Step 1：实体标准化
```
工具：ls_ner_nor_normalize
输入：{"text": "<药物名称>", "entity_types": ["Drug"]}
关键输出：Drug ID、标准英文名、作用机制标准化标签
```

### Step 2：药物基本档案
```
工具：ls_drug_fetch
输入：{"drug_id": "<Step1返回的Drug ID>"}
关键输出：药物类型、全球最高研发阶段、首批日期、原研机构、
          活跃研发机构数、研究适应症数、作用靶点列表（含Target ID）
```

### Step 3：研发里程碑
```
工具：ls_drug_milestone_fetch
输入：{"drug_id": "<Drug ID>", "limit": 50}
关键输出：NDA/BLA申请记录、临床试验启动/完成节点、
          重要专利申请、获批记录
注意：按时间倒序展示，重点标注近3年动态

【HTML展示规范 — P3-1改进】
里程碑表格每行必须附加彩色 badge，样式如下：
  🔴 <span class="badge badge-nda">NDA/BLA申请</span>   背景色 #dc3545（红）
  🟡 <span class="badge badge-patent">专利申请/授权</span> 背景色 #ffc107（黄）
  🔵 <span class="badge badge-trial">临床试验</span>     背景色 #0d6efd（蓝）
  🟢 <span class="badge badge-approval">监管获批</span>   背景色 #198754（绿）
  ⚪ <span class="badge badge-other">其他</span>          背景色 #6c757d（灰）

CSS规范：
.badge { display:inline-block; padding:2px 8px; border-radius:12px;
         color:#fff; font-size:0.78em; font-weight:bold; }
```

### Step 4：主要适应症
```
工具1：ls_drug_search（搜索该药物关联的适应症列表）
工具2：ls_disease_fetch（对前3个核心适应症逐一拉取详情）
关键输出：Disease ID、UMLS CUI、MeSH ID、在研竞品数、疾病定义
```

### Step 5：流行病学分析
```
工具1：ls_epidemiology_vector_search
  查询示例：["<适应症1> incidence prevalence global",
             "<适应症2> epidemiology China"]
工具2：ls_paper_vector_search
  查询示例：["<适应症> burden statistics GLOBOCAN SEER"]
关键输出：全球/中国/美国年新增病例、现患人数、5年生存率
注意：每条数据必须标注原始文献来源（作者+期刊+年份）
```

### Step 6：临床指南地位
```
工具1：ls_clinical_guideline_vector_search
  中文查询："<药物名> CSCO指南推荐级别"
  英文查询："<drug name> NCCN guideline recommendation"
工具2：ls_fda_label_vector_search
  查询："<drug name> FDA approved indication label"
关键输出：CSCO/NCCN推荐级别、推荐方案名称、治疗线次
```

### Step 7：MoA靶点分析 + 耐药机制（★P2-2改进）
```
工具1：ls_target_fetch
输入：{"target_id": "<从Step2获取的靶点ID列表>"}
关键输出：靶点全名、UniProt ID、分子功能描述、
          在研药物数、相关适应症数

工具2：ls_paper_vector_search（★耐药机制检索，新增，必须执行）
  查询示例：["<drug name> resistance mechanism TOP2 PGP",
             "<drug name> drug resistance clinical acquired"]
  关键输出：主要耐药通路、突变位点、临床耐药发生率

【HTML模板要求 — 第五章MoA必须包含以下小节】
5.1 作用机制概述（含MoA示意图或靶点通路描述）
5.2 靶点亚型差异（α/β亚型选择性对比）
5.3 耐药机制分析（★强制小节）
    - 主要耐药通路（如PGP过表达、TOP2A/B蛋白水平下降）
    - 已报道突变位点（如有，引用文献）
    - 克服耐药的临床策略
5.4 同类已批准药物获批时间线（散点图 ECharts）
```

### Step 8：竞品格局分层（★P2-1改进）
```
工具1：ls_drug_search
  【重要】必须使用MoA + 适应症双重过滤，禁止宽泛检索
  查询1：已上市竞品
    - 过滤条件：status=Approved
    - 同时指定 mechanism_of_action=["<标准MoA标签>"]
    - 同时指定 disease=["<核心适应症1>", "<核心适应症2>"]
    - 目的：仅统计直接竞品，过滤非相关治疗领域
  查询2：Ph3竞品（status=Phase 3，同上双重过滤）
  查询3：Ph2竞品（status=Phase 2，同上双重过滤）

工具2：ls_clinical_trial_search
  查询：近3年启动的Ph2/Ph3试验（同适应症，竞争方案）
  要求：输出真实试验名称（NCT编号）和当前状态

分层输出规范：
  第一层（已上市）：药物名 / 类型 / 首批时间 / 适应症 / 与目标药关系
  第二层（Ph3）：药物名 / 类型 / 特点 / 威胁程度
  第三层（Ph2）：药物名 / 类型 / 特点 / 对目标药的影响

【威胁程度矩阵 — 强制输出结构】
每个竞品必须在表格中标注威胁程度评级：
  ⭐⭐⭐⭐⭐ 极高威胁（直接替代，优效可能性高）
  ⭐⭐⭐⭐   高威胁（同适应症，非劣可能性高）
  ⭐⭐⭐     中等威胁（部分适应症重叠）
  ⭐⭐       低威胁（适应症差异大或早期阶段）
  ⭐         微弱威胁（机制或患者群差异显著）

HTML表格结构示例：
<table>
  <tr><th>药物名</th><th>类型</th><th>研发阶段</th><th>核心适应症</th>
      <th>与目标药关系</th><th>威胁程度</th></tr>
  <tr><td>XXX</td><td>小分子</td><td>已上市</td><td>AML</td>
      <td>同机制竞品</td><td>⭐⭐⭐⭐</td></tr>
</table>
```

### Step 9：关键临床数据
```
工具1：ls_clinical_trial_result_search
  查询：["<药物名> AML ORR CR OS",
         "<药物名> PTCL response rate",
         "<药物名> breast cancer PFS"]
工具2：ls_paper_search
  查询：["<drug name> phase 2 3 clinical trial results efficacy"]
关键输出：ORR/CR率、中位OS、中位PFS/EFS、
          研究规模(n=)、患者人群描述
注意：每个数据点必须标注来源（作者+期刊+年份+样本量）
```

### Step 9.5：转化医学证据（★P1-3新增，必须执行）
```
工具：ls_translational_medicine_search
  查询1："<drug name> <核心适应症1> translational preclinical mechanism"
  查询2："<drug name> <核心适应症2> biomarker PK/PD"
  查询3："<drug name> liposome formulation pharmacokinetics"（如适用）

关键输出：
  - 临床前到临床的机制桥接证据（PK/PD、生物标志物）
  - 剂型改进的转化依据（脂质体/缓释/纳米等）
  - 重要的I期剂量探索结果与转化数据
  - 支持新适应症探索的机制性证据

注意：
  - 本步骤为独立步骤，不可与Step 9合并或省略
  - 返回结果应整合入第七章（MoA分析）和第九章（临床数据）
  - 若检索结果与Step 9文献存在重叠，在报告中标注为"转化医学验证"
```

### Step 10：BD动向 + 专利格局（★P1-1 / P1-2改进）

#### BD检索（★三层强制策略，缺一不可）
```
工具1：ls_drug_deal_search（三层检索，全部执行）
  【第一层】药物名直接检索
    查询：{"query": "<药物名>"}
    说明：检索以目标药物为标的的BD交易

  【第二层】持有企业名检索（★当第一层返回零结果时，本层不得省略）
    查询：{"query": "<持有企业英文名>"}（如 "CSPC"）
    查询：{"query": "<持有企业中文名>"}（如 "石药集团"）
    说明：BD交易数据库可能仅登记在持有企业名下，而非具体药物名下
    注意：零结果不等于无BD交易，必须用持有企业名二次验证

  【第三层】同适应症赛道检索（必须执行，不依赖前两层结果）
    查询：{"query": "<核心适应症> deal license <year_range>"}
    示例：{"query": "AML deal license 2020 2024"}
    说明：提供赛道BD基准参考，支撑首付款/里程碑规模分析
    关键输出：同赛道首付款中位数、最大交易参考、BD活跃度

工具2：ls_news_vector_search（★强制执行，不可跳过）
  查询1："<药物名> BD deal partnership out-licensing"
  查询2："<持有企业名> licensing deal news"
  说明：新闻检索补充数据库BD记录，捕获近期未入库交易
  关键输出：BD相关新闻动态、合作意向信号、融资事件
```

#### 专利检索（★按管辖分层）
```
工具3：patent.search（patsnap_search）
  【EP管辖】：keywords=["<drug name> liposome"]，jurisdiction=["EP"]
              重点关注：授权状态、保护范围、有效期
  【US管辖】：keywords=["<drug name> use indication"]，jurisdiction=["US"]
              重点关注：审中状态、Paragraph IV风险
  【CN管辖】：keywords=["<drug name>"]，assignee=["<持有企业>"]，jurisdiction=["CN"]
              重点关注：已授权核心专利、布局完整性
  【新用途专利】：semantic_query="<drug name> new use indication novel treatment patent"
              重点关注：适应症扩展保护

关键输出（每件重要专利的9字段详情表，HTML强制格式）：
| 字段 | 内容 |
|------|------|
| 专利号 | EP/US/CN编号 |
| 标题 | 专利名称 |
| 申请人 | 持有企业 |
| 申请日 | YYYY-MM-DD |
| 授权日 | YYYY-MM-DD（或"审中"） |
| 有效期至 | YYYY年（授权日+20年估算） |
| 核心保护内容 | 一句话概括权利要求范围 |
| IP风险信号 | 是否面临无效挑战/仿制药申请/分案风险 |
| 战略建议 | P1/P2/P3优先级行动建议 |

【IP总监行动清单 — HTML第九章强制结构】
<table class="ip-action-table">
  <tr>
    <th>优先级</th><th>行动项</th><th>时限</th>
    <th>责任方</th><th>依据</th>
  </tr>
  <tr>
    <td><span class="badge-p1">P1</span></td>
    <td>监控EP4098251B1仿制药申请动态</td>
    <td>每季度</td>
    <td>IP团队</td>
    <td>核心授权专利，有效至2041年</td>
  </tr>
  <!-- 按实际专利分析填充，至少5行 -->
</table>

专利可视化（必须包含）：
  图1：专利地理覆盖饼图（EP/US/CN/AU/CA/JP分布）
  图2：IP风险热力图（已授权/审中/已过期/PCT阶段，按适应症分层）
  图3：专利树层级示意（原研化合物→制剂工艺→新用途→联用方案）
```

---

## 4. HTML报告生成规范（强制要求）

### 4.1 字体规范（必须遵守）
```css
/* 全局字体设置 */
body {
    font-family: 'KaiTi', 'STKaiti', '楷体', serif;  /* 中文楷体 */
}
.en, code, pre, .patent-number {
    font-family: 'Times New Roman', Times, serif;     /* 英文 Times New Roman */
}
h1, h2, h3 {
    font-family: 'KaiTi', 'STKaiti', '楷体', serif;
}
table {
    font-family: 'KaiTi', 'STKaiti', '楷体', serif;
}
```

### 4.2 每章必须包含的结构元素
```html
<!-- 数据来源框（蓝色背景）-->
<div class="source-box">
  <strong>数据来源：</strong>
  ls_xxx工具检索（检索时间：YYYY-MM-DD）；
  文献来源：Author et al., Journal, Year；
  数据库版本：XXX
</div>

<!-- 摘要框（绿色背景）-->
<div class="summary-box">
  <strong>本节摘要：</strong>
  [2-3句话概括本章核心发现，必须包含关键数字]
</div>

<!-- 正文内容（表格 + 图表 + 分析文字）-->
[完整内容，不得省略任何数据]
```

### 4.3 ECharts图表规范（每章至少1个）

| 章节 | 必须包含的图表类型 |
|---|---|
| 研发里程碑 | 时间轴图（带彩色badge）或散点图 |
| 流行病学 | 柱状图：各适应症患者规模对比 |
| 临床指南 | 横向柱状图：推荐强度评分 |
| MoA分析 | 饼图：已批准药物类型分布；散点图：获批时间线 |
| 竞品格局 | 堆叠柱状图：已上市/Ph3/Ph2数量；威胁程度雷达图 |
| 关键临床数据 | 分组柱状图：ORR/CR率对比；混合图：OS/PFS对比 |
| BD动向 | 饼图：交易类型分布；横向柱状图：首付款规模 |
| 专利格局 | 饼图：地理覆盖；堆叠图：专利状态热力；专利树 |
| 潜力判断 | 雷达图：多维分层评分；堆叠柱：各资产/方向对比 |

**ECharts图表必须以内联script方式写入HTML，禁止外部引用图表数据文件。**
**ECharts CDN引用：`https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js`**

### 4.4 文件写入规范（防止内容截断）

```
必须使用分块写入方式：
1. files.begin_write（设置content_type="text/html"）
2. files.append × N（每块≤25KB，使用递增sequence编号）
3. files.finish_write

禁止：
- 单次write超过30KB
- 在append中省略/压缩任何内容
- 用"[此处省略...]"代替实际数据

输出路径：@session/outputs/<药物名>_evaluation.html
```

### 4.5 报告整体结构

```
封面（药物名、报告日期、数据说明）
目录（带锚点跳转，12章）
第一章  实体标准化与药物档案（含里程碑彩色badge时间线）
第二章  主要适应症
第三章  流行病学分析
第四章  临床指南地位（CSCO/NCCN）
第五章  作用机制（MoA）与靶点竞争格局（含5.3耐药机制小节）
第六章  竞品格局分层（已上市/Ph3/Ph2，含威胁程度矩阵）
第七章  关键临床数据（ORR/OS/PFS对比）
第八章  BD动向与未来竞争格局（三层BD结果）
第九章  专利格局与IP风险（IP总监视角，含IP总监行动清单）
第十章  综合潜力判断（资产/方向分层打分矩阵）
第十一章 数据交叉验证（必须章节）
免责声明 + 数据完整性说明
```

---

## 5. 数据交叉验证章节规范（第十一章，必须执行）

交叉验证的目标：对报告中引用的关键数字进行多源一致性校验。

### 验证项目清单（至少15项）

| 验证编号 | 验证内容 | 来源A | 来源B | 一致性 |
|---|---|---|---|---|
| V01 | Drug ID是否唯一对应目标药物 | ls_ner_nor_normalize | ls_drug_fetch | ✅/⚠️/❌ |
| V02 | 首次批准日期 | ls_drug_milestone_fetch | ls_drug_fetch | ✅/⚠️/❌ |
| V03 | 核心适应症在研药物数 | ls_disease_fetch | ls_drug_search | ✅/⚠️/❌ |
| V04 | 全球AML年新增病例数 | ls_epidemiology_vector_search | ls_paper_vector_search | ✅/⚠️/❌ |
| V05 | 全球乳腺癌年新增病例数 | ls_epidemiology_vector_search | 文献(GLOBOCAN) | ✅/⚠️/❌ |
| V06 | CSCO推荐级别 | ls_clinical_guideline_vector_search(中) | ls_clinical_guideline_vector_search(英) | ✅/⚠️/❌ |
| V07 | NMPA获批ORR数据 | ls_clinical_trial_result_search | ls_drug_milestone_fetch | ✅/⚠️/❌ |
| V08 | 关键临床研究OS数据 | ls_clinical_trial_result_search | ls_paper_search | ✅/⚠️/❌ |
| V09 | 心脏毒性安全性数据（肌钙蛋白T） | ls_clinical_guideline_vector_search | ls_paper_search | ✅/⚠️/❌ |
| V10 | 竞品直接竞品数量（MoA+适应症过滤后） | ls_drug_search（双重过滤） | 里程碑数据 | ✅/⚠️/❌ |
| V11 | BD交易数量（持有企业三层检索） | ls_drug_deal_search（三层） | ls_news_vector_search | ✅/⚠️/❌ |
| V12 | 核心EP专利法律状态 | patent.search | ls_drug_milestone_fetch | ✅/⚠️/❌ |
| V13 | 靶点在研药物数 | ls_target_fetch | ls_drug_search（MoA过滤） | ✅/⚠️/❌ |
| V14 | 近期NDA申请时间 | ls_drug_milestone_fetch | ls_news_vector_search | ✅/⚠️/❌ |
| V15 | 转化医学证据数量 | ls_translational_medicine_search | ls_paper_search | ✅/⚠️/❌ |
| V16 | 持有企业BD交易总数 | ls_drug_deal_search（企业层） | ls_news_vector_search | ✅/⚠️/❌ |

验证结果标注：
- ✅ 两源一致（差异<10%）
- ⚠️ 存在差异（差异10-30%，需注明原因）
- ❌ 数据冲突（差异>30%或方向相反，需重新检索确认）
- N/A 该项不适用于当前药物

验证章节末尾必须包含：
1. 验证结果饼图（ECharts：✅/⚠️/❌/N/A各多少项）
2. 数据可信度总结（一段话）
3. 已知数据缺口清单（哪些数据无法从当前工具验证）

---

## 6. 综合潜力判断规范（Step 11，★P3-2改进）

### 禁止行为
```
❌ 输出单一总分（如"综合潜力 3.8/5"）
❌ 对不同剂型/适应症/资产类型混合评分
❌ 省略评分依据和置信度标注
```

### 强制输出结构：资产/方向分层打分矩阵

**维度一：按资产类型分层评分**

| 资产类型 | 研发阶段 | 市场潜力 | 竞争壁垒 | 变现路径 | 综合评分 |
|----------|----------|----------|----------|----------|----------|
| 原料药/普通注射液 | ★★★★★ | ★★☆☆☆ | ★☆☆☆☆ | ★★☆☆☆ | 2.5/5 |
| 脂质体新剂型 | ★★★★☆ | ★★★★☆ | ★★★☆☆ | ★★★★☆ | 3.7/5 |
| 新适应症扩展 | ★★★☆☆ | ★★★★★ | ★★★★☆ | ★★★☆☆ | 3.5/5 |
（按实际检索结果填充，格式不变）

**维度二：按战略方向分层评分**

| 战略方向 | 技术可行性 | 市场规模 | BD价值 | IP保护 | 综合评分 |
|----------|------------|----------|--------|--------|----------|
| 国内PTCL适应症深耕 | ★★★★★ | ★★★☆☆ | ★★★☆☆ | ★★★★☆ | 3.6/5 |
| AML适应症拓展 | ★★★☆☆ | ★★★★★ | ★★★★☆ | ★★★☆☆ | 3.8/5 |
| 海外License-out | ★★★★☆ | ★★★★★ | ★★★★★ | ★★★★☆ | 4.2/5 |
（按实际检索结果填充，格式不变）

**维度三：最终判断结论表**

| 判断维度 | 结论 | 置信度 | 主要依据 |
|----------|------|--------|----------|
| 短期商业价值（1-2年） | 中等 | 高 | 已获NMPA批准，CSCO II推荐 |
| 中期成长潜力（3-5年） | 较高 | 中 | AML扩展临床数据待成熟 |
| 长期BD价值（5年+） | 高 | 中低 | 海外市场窗口取决于Ph3结果 |
| IP保护强度 | 中等偏强 | 高 | EP4098251B1有效至2041年 |
| 竞争壁垒 | 中等 | 高 | 制剂专有技术+先发优势 |
| 总体建议 | 重点跟进 | 高 | 脂质体剂型差异化价值明确 |

---

## 7. 内容完整性要求（核心约束）

```
禁止行为：
❌ 使用"[此处省略]"、"[详见附录]"、"[内容过多，已压缩]"等替代实际数据
❌ 将表格压缩为"代表性示例"（必须保留全部已检索到的行）
❌ 省略任何ECharts图表的JSON配置
❌ 将多段分析文字合并为一句话
❌ 省略数据来源框或摘要框
❌ BD第一层检索零结果时跳过第二、三层检索
❌ 输出竞品宽泛计数（如"已上市88个"）而不做MoA+适应症过滤

强制行为：
✅ 每条数据保留原始文献/工具来源标注
✅ 每个图表保留完整的ECharts JSON配置
✅ 每张表格保留所有已检索到的行
✅ 每章保留数据来源框（蓝色）+ 摘要框（绿色）
✅ 采用分块写入，每块≤25KB，确保不截断
✅ BD检索必须执行三层（药物名→持有企业名→赛道），全部记录在数据来源框
✅ 竞品检索必须使用MoA+适应症双重过滤条件
✅ 第五章必须包含5.3耐药机制小节
✅ 第九章必须包含IP总监行动清单表格
✅ Step 9.5 ls_translational_medicine_search必须执行
✅ 综合潜力必须按资产/方向分层打分，禁止单一总分
```

---

## 8. 免责声明规范

报告必须在以下位置包含免责声明：

**报告封面/顶部：**
> 本报告基于智慧芽专业数据库检索结果，仅供参考，不构成投资建议。
> 专利相关结论为初步技术信号，不构成法律意见，`counsel_review_required: true` 适用于所有专利相关结论。

**报告底部：**
> 数据完整性声明：所有定量数据均来自智慧芽MCP工具直接返回的结构化结果。
> 图表评分为综合判断分值，非绝对量化指标。本报告不构成投资建议。

---

## 9. 质量检查清单（生成报告后自查）

在输出报告前，执行以下自查：

- [ ] 是否所有11个检索步骤均已执行（含Step 9.5）？
- [ ] Step 10 BD检索是否执行了三层策略（药物名/持有企业/赛道）？
- [ ] ls_news_vector_search是否已执行（BD新闻检索）？
- [ ] ls_translational_medicine_search是否已执行（转化医学）？
- [ ] Step 8竞品检索是否使用了MoA+适应症双重过滤？
- [ ] 第五章5.3耐药机制小节是否存在？
- [ ] 第九章IP总监行动清单表格是否存在（至少5行）？
- [ ] 每件重要专利是否有9字段详情表？
- [ ] 第一章里程碑表格是否有彩色badge（红/黄/蓝/绿/灰）？
- [ ] 综合潜力章节是否为分层矩阵（无单一总分）？
- [ ] 每章是否有数据来源框（蓝色）？
- [ ] 每章是否有摘要框（绿色）？
- [ ] 是否有第十一章数据交叉验证（含V16验证项）？
- [ ] 所有ECharts图表是否为内联script？
- [ ] 中文字体是否为楷体？英文字体是否为Times New Roman？
- [ ] HTML文件是否通过分块写入（防截断）？
- [ ] 是否有免责声明（报告头部+底部各一处）？
- [ ] 关键数字是否有文献来源标注？

# Legacy 21-section target initiation report specification

Use this file only when a deep HTML presentation is requested.

## Contents

- Original data-collection workflow
- Twenty-one-section report outline
- HTML component and design guidance
- Coverage summary, quality rules, and examples

---
name: target-drug-bd-assessment
description: 靶点研发立项报告生成器：基于 B7-H3 报告蒸馏的完整工作流，使用 PatSnap 智慧芽全套 MCP 工具（靶点、药物管线、临床试验、专利、BD交易、学术文献）对任意肿瘤靶点进行系统性调研，生成包含21章节的标准化 HTML 立项报告，含 KPI 看板、SWOT、优先级矩阵、风险提示、数据覆盖摘要等完整内容。
---

# target-initiation-report · 靶点研发立项报告生成器

## 适用场景

当用户输入一个**肿瘤治疗靶点**（如 B7-H3、HER3、TROP2、CLDN18.2 等），本 Skill 将：

1. 系统调用 PatSnap 智慧芽 MCP 工具完成全量数据采集
2. 按 21 章节标准结构蒸馏分析结果
3. 生成一份完整的 HTML 格式研发立项报告

触发关键词示例：
- "帮我做一份 [靶点名] 立项报告"
- "对 [靶点] 进行研发立项调研"
- "生成 [靶点] 靶点全景分析"
- "做 [靶点] 的竞品/管线/专利/临床分析"

---

## 数据采集工作流（严格按顺序执行）

### 阶段 0 · 实体标准化
- 调用 `ls_ner_nor_normalize` 对靶点名称进行标准化，获取 target_id

### 阶段 1 · 靶点基础信息
- 调用 `ls_target_fetch(target=[靶点名])` 获取：
  - `drug_count`（关联药物总数）
  - `dev_drug_count`（在研药物数）
  - `disease_count`（关联适应症数）
  - 蛋白结构、信号通路、作用机制

### 阶段 2 · 药物管线（必须分批穷尽，遵循翻页规则）
- **批A**：`ls_drug_search(target=[靶点], drug_type=["Small molecule drug"])` → 小分子
- **批B**：`ls_drug_search(target=[靶点], drug_type=["Monoclonal antibody"])` → 单抗
- **批C**：`ls_drug_search(target=[靶点], drug_type=["Biological product","ADC"])` → 生物药/ADC
- **批D**：`ls_drug_search(target=[靶点], country=["CN"])` → 中国管线
- **批E**：`ls_drug_search(target=[靶点], highest_phase=["approved"])` → 已获批（E42核查）
- 每批若 total > 返回数，必须循环翻页至数据完整

### 阶段 3 · 临床试验（分阶段全量采集）
- `ls_clinical_trial_search(target=[靶点], phase=["phase_3"])` → Phase 3 全量（18项示例）
- `ls_clinical_trial_search(target=[靶点], phase=["phase_2"])` → Phase 2 样本
- 对关键试验调用 `ls_clinical_trial_fetch` 获取完整方案细节（主要端点、NCT号、招募状态）

### 阶段 4 · 专利布局
- `ls_patent_search(target=[靶点], patent_core_type=["product_compound"])` → 化合物核心专利（total）
- 获取前 50 件代表性专利，标注申请人/申请日/法律状态
- FTO 4维度评估：核心化合物专利 / ADC Linker-Payload / 制剂专利 / 新用途专利

### 阶段 5 · BD 交易（全量）
- `ls_drug_deal_search(target=[靶点])` → 全量 BD 交易（遵循翻页规则）
- 提取：交易日期、交易双方（licensor/licensee）、交易金额、交易类型

### 阶段 6 · 学术文献
- `ls_paper_search(target=[靶点])` → 论文总量
- `ls_paper_vector_search(query="[靶点] mechanism tumor expression")` → 代表性高影响力文献

### 阶段 7 · Web 补查（必要时）
- 对 PatSnap 未覆盖的临床数据（ORR/PFS 等）调用 `ls_web_search` 补充
- 所有 Web 补查结果均需标注 `[Web补查]`，数值标注「待核实」

---

## 报告结构（21章节标准模板）

```
第0章  执行摘要 · KPI 一览（8个核心指标卡片）
第1章  靶点生物学（蛋白结构域≥5个、分子机制、信号通路表）
第2章  疾病背景与标准治疗方案（SoC）
第3章  流行病学与市场规模（GLOBOCAN 数据）
第4章  竞品管线全景（宏观统计 + 按 MoA 分类表）
第5章  竞品深度 Profile（Top 5，每个含机制/适应症/关键试验/毒性/差异化分析）
第6章  在研管线分析（小分子/单抗/ADC/其他分类列表）
第7章  临床试验进展（Phase 3 全量表 + 关键试验详情）
第8章  专利布局（代表性专利表 + FTO 4维度评估）
第9章  BD 交易动态（Top 10 交易表 + 趋势分析）
第10章 学术研究热度（论文总量 + 代表性文献表）
第11章 监管路径（FDA/NMPA/EMA 快速通道对比）
第12章 药物经济学（定价参考 + 市场规模估算）
第13章 中国本土专项（本土管线表 + 本土化路径分析）
第14章 开发成本与 ROI（成本估算表 + NPV 框架）
第15章 CMC 可制造性（主要挑战与解决方向）
第16章 SWOT 分析（四象限 HTML 表格）
第17章 立项建议（P1/P2/P3 优先级矩阵 + 五星评分）
第18章 风险提示（7类风险 × 可能性/影响度/应对措施）
第19章 数据覆盖摘要（全量检索统计 + 盲区说明）
第20章 参考来源（数据库 + 关键文献列表）
第21章 免责声明
```

---

## HTML 报告设计规范

### CSS 设计系统（与 B7-H3 示例报告一致）
```css
:root {
  --primary: #1a3a5c;
  --accent: #e63946;
  --accent2: #457b9d;
  --accent3: #2a9d8f;
  --bg: #f8f9fa;
  --card-bg: #ffffff;
  --border: #dee2e6;
  --warning: #fd7e14;
  --success: #28a745;
  --danger: #dc3545;
}
```

### 关键 UI 组件
- **KPI 卡片（`.kpi-card`）**：深蓝渐变背景，显示数字/标签/来源
- **药物卡片（`.drug-card`）**：带边框卡片，含 badge 行 + 属性表
- **FTO 卡片（`.fto-card`）**：高/中/低风险色彩区分（红/橙/绿）
- **SWOT 网格（`.swot-grid`）**：2×2 四象限，四色背景
- **警示框（`.signal-box`）**：橙/红色边框，用于重要提示
- **信息框（`.info-box`）**：蓝色左边框，用于策略性说明
- **数据覆盖框（`.coverage-box`）**：等宽字体，表格化数据统计
- **来源标签（`.source-tag`）**：灰色圆角标签，标注数据来源工具

### 导航与布局
- 粘性 Header（深蓝渐变 `#1a3a5c`，含报告标题/版本/日期）
- 粘性导航栏（`top: 72px`，21章节锚点链接）
- 最大宽度 1200px 居中容器
- 响应式：768px 以下 SWOT 折叠为单列

---

## 数据质量门禁（严格执行）

### 必须遵守的规则
1. **翻页完整性**：所有接口返回 `total > limit` 时必须循环翻页，不得在首页结论
2. **来源标注**：每个数据点必须标注 `[来源: 工具名 → 字段=值]`
3. **Web补查标注**：Web 来源数据标注 `[Web补查]`，数值标注「待核实」
4. **NCT号核查**：临床试验 NCT 编号只能来自 `ls_clinical_trial_fetch` 真实返回；未确认者标注「待核实」
5. **零获批核查（E42）**：`highest_phase=approved` 查询结果为 0 时，在报告中明确标注「当前无获批产品」
6. **专利相关性核查（E50）**：B7 家族其他成员专利需标注，非直接靶点专利需剔除
7. **不伪造数据**：禁止编造 UUID、NCT 号、交易金额、ORR/PFS 数值

### 数据覆盖摘要格式
```
本次检索覆盖摘要：
─────────────────────────────────────────
• 小分子：             X条  (total=X)  [ls_drug_search 批A]
• 生物药/ADC：         X条  (total=X)  [ls_drug_search 批C]
• 单克隆抗体：          X条  (total=X)  [ls_drug_search 批B]
• 中国管线：           X条  (total=X，country=CN)  [ls_drug_search 批D]
• 已获批：             0条  (total=0)  [E42确认]
• 专利：             X件  (total=X，取样Y件)  [ls_patent_search]
• BD交易：            X笔  (total=X，全量)  [ls_drug_deal_search]
• 临床试验(Phase3)：   X项  (total=X，全量)  [ls_clinical_trial_search]
• 论文：           X,XXX篇  (total=X)  [ls_paper_search]
─────────────────────────────────────────
数据库盲区说明：
① 临床结果数据（ORR/PFS/OS）来自 Web补查，标注「待核实」
② 专利仅取前Y件样本，完整FTO需精筛
③ 中国管线与全球管线可能重叠
```

---

## 输出规范

- **格式**：完整 HTML 文件，可在浏览器直接打开
- **文件名**：`{靶点名}_initiation_report_v{版本}.html`
- **版本号**：从 v1.0.0 开始，每次重新生成递增
- **标题格式**：`[靶点名] ([别名]) 靶点研发立项报告`
- **页脚**：报告类型/版本/生成日期/PatSnap智慧芽/内部参考声明

---

## 典型靶点参考案例

| 靶点 | 别名 | 主要模态 | 典型适应症 |
|------|------|----------|-----------|
| B7-H3 | CD276 | ADC, mAb, BiAb | SCLC, mCRPC, ESCC |
| HER3 | ERBB3 | ADC, mAb | NSCLC, 乳腺癌 |
| TROP2 | TACSTD2 | ADC | TNBC, NSCLC |
| CLDN18.2 | Claudin-18.2 | ADC, BiAb | 胃癌, 胰腺癌 |
| DLL3 | Delta-like 3 | ADC, BiTE | SCLC |
| GPC3 | Glypican-3 | ADC, CAR-T | 肝细胞癌 |

---

## 注意事项

- 报告生成过程中需实时说明进度（「已完成第X阶段，共7阶段」）
- 每个章节生成后应有简短的质量自检（数据来源是否标注、是否有未核实数据）
- 报告末尾必须有完整的「第19章·数据覆盖摘要」，如实反映检索结果
- 如果某个靶点在 PatSnap 数据库中的数据有限（如极早期靶点），应在摘要中说明并降低置信度
- 生成完成后，将 HTML 文件保存至 `@session/outputs/` 下并提供预览链接

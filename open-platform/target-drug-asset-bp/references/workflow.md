# 完整执行路径 — university-tech-transfer-packager

## 阶段 1：输入解析

**目标**：从用户输入中结构化提取所有可用信息。

提取字段：
- `target`：靶点名称或候选靶点
- `disease`：适应症/疾病领域
- `drug`：候选化合物/生物制品名称（如有）
- `mechanism`：作用机制描述
- `technology_modality`：技术路线（小分子/抗体/基因治疗/细胞治疗/核酸/蛋白/其他）
- `institution`：来源高校或科研机构
- `pi`：主要研究者/PI 姓名
- `patent`：专利号或申请号（如有）
- `publication`：代表性论文 DOI 或标题（如有）
- `project_stage`：研究阶段（基础研究/靶点验证/先导化合物/临床前/IND 申报中/早期临床）
- `transfer_target`：转化目标（企业合作/授权/孵化/联合申报/其他）

**若字段为空的处理规则**：
- 无 target → 进入假设提取流程（见阶段 2b）
- 无专利 → 不停止，进入 IP 准备度建议流程
- 无项目阶段 → 默认 early research / preclinical
- 无合作目标 → 默认面向中国创新药企业和产业孵化

---

## 阶段 2a：实体标准化（有具体实体时）

**工具**：`ls_ner_nor_normalize`

**操作**：
- 将用户原始输入整段传入
- 提取标准化 ID：target_id、disease_id、drug_id、organization_id
- 记录标准化名称，用于后续所有工具调用
- 如标准化失败，改用原始文本继续，并在输出中标注"未标准化"

---

## 阶段 2b：假设提取（无具体靶点时）

**操作**：
- 从机制/疾病描述中推断候选靶点（2–3 个）
- 推断技术路线和转化阶段
- 所有推断用 **【假设】** 标注
- 进入阶段 3，按假设靶点执行

---

## 阶段 3：科学证据归纳

**工具序列**：

### 3.1 靶点与疾病关联确认
`ls_target_fetch`
- 输入：target_id 或 target name
- 获取：靶点生物学功能、已知疾病关联、已有药物列表

### 3.2 转化医学证据
`ls_translational_medicine_search`
- 输入：target + disease（或 drug）
- 获取：人群验证证据、biomarker 关联、机制支持文献
- limit = 10，按相关性排序

### 3.3 文献支撑（可选增强）
`ls_paper_vector_search`（或 `ls_paper_search`）
- 当转化医学证据不足时调用
- 获取：核心机制论文、人群研究、动物模型结果

---

## 阶段 4：临床和适应症路径判断

### 4.1 同靶点/同适应症药物格局
`ls_drug_search`
- 输入：target + disease + technology_modality（如有）
- 获取：最高研发阶段、全球竞争格局、同类药物数量
- limit = 20，记录 highest_phase 分布

### 4.2 里程碑历史（核心竞品）
`ls_drug_milestone_fetch`
- 对 ls_drug_search 返回的前 3 个最相关竞品调用
- 获取：关键里程碑时间线、审批情况

### 4.3 临床试验活跃度
`ls_clinical_trial_search`
- 输入：target + disease
- 获取：试验数量、阶段分布、活跃状态、失败/撤回信号
- 重点关注 terminated/withdrawn 的试验及原因

### 4.4 临床结果信号
`ls_clinical_trial_result_search`
- 输入：target + disease（或 drug）
- 获取：已读出的临床结果、关键终点达成情况
- 识别：该领域是否有重大失败先例

### 4.5 临床指南与未满足需求（可选）
`ls_clinical_guideline_vector_search`
- 输入：disease 自然语言描述
- lang = CN（面向国内场景时）或 EN
- 获取：当前治疗指南、未被满足的患者需求

---

## 阶段 5：竞争和差异化判断

**基于阶段 3–4 数据综合判断**：

- 竞争拥挤度：同靶点药物数量 × 阶段分布
- 差异化空间：机制独特性、适应症细分、患者亚群、技术路线
- 失败风险：已知临床失败模式与本项目相关度
- 窗口期：是否有竞品即将到期/首个进入某亚型

---

## 阶段 6：专利与权属准备度判断

### 6.1 专利初筛
`ls_patent_search`（Pharma Intelligence 侧）或 `mcp_patent-search__patsnap_search`（PatSnap 侧）
- 以当前 MCP tools/list 实际可用工具为准
- 输入：target + disease + organization
- 获取：相关专利数量、权利人分布、主要 IPC、地域覆盖、最早优先权日

### 6.2 具体专利详情（如用户提供专利号）
`mcp_patent-search__patsnap_fetch` 或 `ls_patent_fetch`
- 获取：权利要求范围、法律状态、到期日、同族布局

### 6.3 判断输出
- 本机构/PI 是否有已申请专利
- 关键技术点是否落入他人专利保护范围（FTO 初步信号）
- 专利空白区：哪些技术点尚未覆盖
- 建议：优先申请领域、PCT/海外布局必要性

---

## 阶段 7：潜在合作方画像

### 7.1 机构方向匹配（如用户提供目标机构）
`ls_organization_pipeline_fetch`
- 输入：organization name
- 获取：该企业研发管线、关注靶点、活跃适应症
- 判断：与本项目的匹配度

### 7.2 画像逻辑（无具体机构时）
基于以下维度推导合作方类型：
- 药物格局：哪些公司在同赛道布局
- 技术路线：技术路线契合度
- 阶段需求：早期合作 vs. 授权引进 vs. 技术平台采购
- 地域：国内企业 / 跨国 MNC / 港澳台 / 海外华人创业团队

---

## 阶段 8：输出成果转化包

按六块固定结构生成，详见 `references/output-templates.md`：

1. Project Snapshot
2. Commercial Translation Thesis
3. Evidence & Differentiation Matrix
4. IP and Ownership Readiness
5. Partner / Licensee Fit
6. Next-Step Package

在输出末尾附：
- **成果转化成熟度评分**（满分 100，分项展示）
- **判断标签**（Transfer Ready / Partnering Candidate / Incubation Needed / Research Only / Insufficient Materials）
- **关键假设清单**（所有 【假设】 汇总）
- **数据来源清单**（[S1] [S2] ... 对应工具与检索结果）

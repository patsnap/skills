---
name: drug-combination-synergy
description: "分析药物组合机制、协同证据与联合开发策略。适用于：研究两个或多个药物的互补机制、协同证据、耐药克服逻辑和组合开发策略，用于联合用药假设形成和实验优先级排序。"
---

## 适用场景

- 两种小分子药物（天然产物、化学药、中药单体）的协同抗肿瘤/抗炎/抗菌等作用探究
- 需要快速梳理联用文献证据、ADMET互补性、机制靶点覆盖差异
- 需要生成实验设计方案（体外CI测定→体内动物模型→制剂优化）
- 需要输出可直接投递或汇报的Word文档报告

---

## 输入参数

| 参数 | 说明 | 示例 |
|---|---|---|
| `drug_A` | 药物A名称（中英文均可）或SMILES | `肉桂酸` / `Cinnamic Acid` |
| `drug_B` | 药物B名称（中英文均可）或SMILES | `黄连素` / `Berberine` |
| `indication` | 探究的适应症/疾病领域 | `抗肿瘤` / `anti-tumor` |
| `tumor_types`（可选） | 具体肿瘤类型，逗号分隔 | `肝癌, 乳腺癌, 肺癌` |
| `output_lang` | 报告语言 | `cn`（中文，默认）/ `en` |

---

## 工作流步骤

### Step 1：实体标准化与SMILES获取
**工具**：`mcp_virtual-mcp-pharma-intelligence__ls_ner_nor_normalize`

- 输入两个药物名称，获取标准化实体ID、规范英文名
- 若用户仅提供名称而非SMILES，通过结构检索获取SMILES

**操作要点**：
```
user_input = "{drug_A} {drug_B} {indication}"
→ 提取 Drug / Disease 实体
→ 记录 normalized_id 供后续检索
```

---

### Step 2：化学结构检索与SMILES获取
**工具**：`mcp_virtual-mcp-pharma-intelligence__ls_drug_fetch`  
**备用**：`mcp_tool-collection-chemical-molecular__ls_structure_search`

- 通过标准化药物名或ID获取 canonical SMILES
- 渲染分子结构（在报告中用 ```smiles 代码块展示）

---

### Step 3：ADMET 预测对比
**工具**：`mcp_tool-collection-chemical-molecular__ls_admet_predict`

输入两个分子的 SMILES，获取并对比以下核心属性：

| 属性组 | 具体指标 |
|---|---|
| 物化性质 | `molecular_weight`, `logP`, `tpsa`, `Solubility_AqSolDB` |
| 吸收 | `Bioavailability_Ma`, `Caco2_Wang` |
| 分布 | `BBB_Martins`, `VDss_Lombardo` |
| 代谢 | `CYP1A2_Veith`, `CYP2C9_Veith`, `CYP3A4_Substrate_CarbonMangels` |
| 排泄 | `Clearance_Hepatocyte_AZ`, `Clearance_Microsome_AZ` |
| 毒性 | `AMES`, `hERG` |

**分析重点**：识别互补性（一方弥补另一方短板）与叠加风险（两者共同的毒性）。

---

### Step 4：文献检索（多源并行）
并行调用以下工具：

**4a. 学术文献**  
`mcp_virtual-mcp-pharma-intelligence__ls_paper_search`
```
drug=[drug_A, drug_B], disease=[indication]
→ 检索两药联用直接证据
```

**4b. 语义文献搜索**  
`mcp_virtual-mcp-pharma-intelligence__ls_paper_vector_search`
```
query="{drug_A} AND {drug_B} synergistic {indication} mechanism"
lang="EN"
```

**4c. 专利检索**  
`mcp_patent-search__patsnap_search`
```
keywords=[drug_A, drug_B, indication, "combination", "synergy"]
search_strategy=["keyword", "filter"]
```

**4d. 转化医学证据**  
`mcp_virtual-mcp-pharma-intelligence__ls_translational_medicine_search`
```
drug=[drug_A, drug_B], disease=[indication]
```

**检索结果处理**：
- 筛选直接联用证据（优先）、单药机制证据（次要）
- 提取 DOI、发表年份、期刊、关键数据
- 建立 DOI 索引表，供后续内联引用使用

---

### Step 5：协同机制分析
基于 Step 3–4 的数据，从以下维度构建机制矩阵：

**5a. ADMET 互补性分析**
- 生物利用度互补（一方高弥补另一方低）
- 毒性风险互补（联合降低单药剂量以减毒）
- 代谢通路差异（避免竞争同一 CYP 酶）
- 溶解度差异对共递送制剂设计的启示

**5b. 靶点覆盖矩阵**（雷达图）
- 凋亡通路（Bax/Bcl-2/Caspase）
- 氧化应激（ROS/GSH/MDA）
- 炎症信号（NF-κB/IL-6/TNF-α）
- 增殖信号（PI3K/Akt/mTOR）
- 细胞周期（G1/S vs G2/M）
- 血管生成（VEGF/HIF-1α）

**5c. 协同假说生成**（至少3个可检验假说）
- H1（主假说）：药效学协同靶点
- H2：ADMET/药代动力学互补假说
- H3：细胞周期/氧化还原互补假说

---

### Step 6：实验设计方案

#### 第一阶段：体外细胞实验
- **细胞系选择**：基于适应症推荐 3–4 个细胞系
- **Chou-Talalay CI 法**：IC₅₀ 测定 → 剂量矩阵 → CompuSyn 分析
- **机制验证**：凋亡（Annexin V/PI）、细胞周期（PI 染色）、Western Blot 通路蛋白、ROS/GSH 氧化应激

#### 第二阶段：体内动物实验
- **模型选择**：异种移植瘤 / 同系瘤 / Ehrlich 腹水瘤
- **分组设计**：单药组 × 2 + 联合组（低/高剂量）+ 阳性对照 + Vehicle
- **观察指标**：肿瘤体积/重量、体重、TGI、IHC（Ki-67/Caspase-3/VEGF）、血清毒性指标

#### 第三阶段（可选）：制剂优化
- 基于 ADMET 溶解度/清除率差异，设计 LNP/PLGA 共递送纳米制剂
- 统一 PK 曲线，实现靶向协同释放

---

### Step 7：质控与安全性警示
根据 ADMET 结果自动生成以下警示（如适用）：
- AMES 阳性（> 0.5）→ 建议遗传毒性测试
- hERG 风险（> 0.5）→ 建议心电图监测 + 联合减量
- CYP 强抑制（> 0.8）→ 提示 DDI 风险，建议检查合并用药
- 高肝清除率 → 建议制剂改造或频繁给药方案

---

### Step 8：Word 报告导出
**工具链**：`office` (plan_workspace → check_runtime → run_builder → render_inspect → finalize)

**报告结构**：
1. 封面（药物名称、适应症、生成日期）
2. 分子结构与基本信息（含 SMILES 渲染说明）
3. ADMET 预测对比表（含互补性解读）
4. 协同机制分析（体内直接证据 + 机制矩阵 + 假说）
5. 实验设计方案（三阶段）
6. 质控与安全性警示
7. 完整参考文献列表

**格式要求**：
- 中文字体：楷体（KaiTi）
- 英文字体：Times New Roman
- 参考文献内联标注：DOI 号，红色上标，嵌入对应段落/表格行末
- 文末完整参考文献列表与内联标注一一对应

---

## 工具调用清单（按顺序）

| 步骤 | 工具 | 必选/可选 |
|---|---|---|
| Step 1 | `ls_ner_nor_normalize` | 必选 |
| Step 2 | `ls_drug_fetch` | 必选 |
| Step 3 | `ls_admet_predict`（两个SMILES同批提交） | 必选 |
| Step 4a | `ls_paper_search` | 必选 |
| Step 4b | `ls_paper_vector_search` | 必选 |
| Step 4c | `patsnap_search`（专利） | 推荐 |
| Step 4d | `ls_translational_medicine_search` | 推荐 |
| Step 5 | 综合分析（基于上述数据，LLM推理） | 必选 |
| Step 6 | 综合分析（LLM生成实验方案） | 必选 |
| Step 7 | 综合分析（ADMET结果驱动安全警示） | 必选 |
| Step 8 | `office` 工具链 | 必选 |

---

## 输出物

| 输出 | 格式 | 说明 |
|---|---|---|
| 协同机制分析 | Markdown（聊天内） | 含雷达图（ECharts）、机制矩阵表 |
| ADMET 对比 | Markdown 表格 | 含互补性解读 |
| 实验设计方案 | Markdown（聊天内） | 三阶段分层设计 |
| Word 报告 | .docx | 带DOI内联引用，楷体+TNR字体 |

---

## 示例案例：肉桂酸（Cinnamic Acid）× 黄连素（Berberine）抗肿瘤协同探究

### 输入
```
drug_A: 肉桂酸（Cinnamic Acid）
SMILES_A: OC(=O)/C=C/c1ccccc1
drug_B: 黄连素（Berberine）
SMILES_B: COc1ccc2cc3ccc(O)c(OC)c3[n+](C)c2c1
indication: 抗肿瘤（anti-tumor）
tumor_types: 肝癌, 乳腺癌, 肺癌, 结直肠癌, Ehrlich实体瘤
```

### ADMET 预测核心结论
| 属性 | 肉桂酸 | 黄连素 | 协同意义 |
|---|---|---|---|
| 口服生物利用度 | **91%** | 67% | CA弥补BER生物利用度不足 |
| hERG 心脏毒风险 | 0.005 | ⚠️ 0.573 | 联合减量BER可降低心脏毒 |
| AMES 致突变 | **0.018** | ⚠️ 0.657 | 联合降低BER暴露剂量 |
| 肝细胞清除率 | 极低 | **高（141.4）** | CA有助于延缓联用半衰期 |
| 水溶性 logS | −2.36 | −3.46 | CA溶解度更好，利于共递送制剂化 |

### 关键文献证据（DOI索引）
| DOI | 证据内容 |
|---|---|
| 10.2174/1871520618666181116162441 | Ehrlich 实体瘤模型：BER+CA单独及联合顺铂，肿瘤体积缩小74–92%，Bax/Bcl-2↑74倍，Caspase-3↑14倍 |
| 10.3390/cancers16162777 | PI3K/Akt/mTOR 通路协同抑制证据（CRPC模型） |
| 10.7150/ijbs.18969 | BER逆转缺氧耐药（AMPK-HIF-1α-P-gp轴），CA可减少BER剂量 |
| 10.1002/mco2.693 | 细胞周期与凋亡通路综述（G2/M阻滞BER，G1/S阻滞CA） |
| 10.1124/pr.58.3.10 | Chou-Talalay CI法方法学依据 |
| 10.3892/or.2014.3520 | BER抑制MDA-MB-231细胞侵袭转移 |
| 10.1208/s12249-019-1497-6 | 纳米共递送制剂设计参考（脂质体共载策略） |

### 协同机制矩阵（简版）
| 机制层面 | 肉桂酸贡献 | 黄连素贡献 | 协同类型 |
|---|---|---|---|
| 促凋亡 | ↑Bax/Bcl-2, ↑Caspase-3 | ↑Bax/Bcl-2, ↑Caspase-3/9 | 叠加/协同 |
| 细胞周期阻滞 | G1/S 期 | G2/M 期 | 互补（双期阻滞） |
| NF-κB 抑制 | 抑制转录激活 | 抑制p65核转位 | 叠加 |
| PI3K/Akt/mTOR | 下调p-Akt | 抑制p85 PI3K | 协同双节点 |
| 耐药逆转 | 减少BER用量 | AMPK-HIF-1α-P-gp轴 | 补强 |
| 抗血管生成 | 抑制VEGF | 抑制HIF-1α/VEGF | 叠加 |

### 核心可检验假说
- **H1**：CA + BER 通过协同调控 PI3K/Akt/NF-κB 轴与线粒体凋亡通路，产生 CI < 1 的药效学协同 [DOI: 10.3390/cancers16162777; 10.2174/1871520618666181116162441]
- **H2**：CA（高生物利用度）弥补 BER 快速肝清除，实现 PK 互补，降低 hERG/AMES 风险剂量 [DOI: 10.2174/1871520618666181116162441]
- **H3**：BER（G2/M）+ CA（G1/S）双重细胞周期阻滞触发更彻底的凋亡瀑布 [DOI: 10.1002/mco2.693]

### 实验设计要点
- **体外**：HepG2/MCF-7/A549/HCT116；Chou-Talalay CI 法（BER:CA = 1:1, 1:2, 2:1）；Western Blot p-Akt/p-NF-κB/Bax/Bcl-2/Caspase-3
- **体内**：HepG2 皮下异种移植瘤（BALB/c 裸鼠）；6组 × 8只；肿瘤体积/TGI/IHC
- **制剂**：PLGA 或 LNP 共载纳米粒（参考 [DOI: 10.1208/s12249-019-1497-6]）

### 安全性警示
- ⚠️ BER AMES = 0.657 → 建议遗传毒性测试（Ames test）
- ⚠️ BER hERG = 0.573 → 动物实验同步监测 QT 间期，联合设计降低 BER 绝对剂量
- ⚠️ BER CYP1A2 抑制 = 0.970 → 合并经 CYP1A2 代谢的化疗药时需检查 DDI

### 输出文档
- 已生成 Word 报告（v3）：中文楷体 + 英文 Times New Roman，全文 DOI 内联标注，完整参考文献列表

---

## 注意事项与局限性

1. **文献证据等级**：本工作流优先检索 PubMed/PatSnap 收录文献，部分冷门联用组合可能缺乏直接证据，此时以单药机制推导协同假说，需在报告中明确标注"推断"而非"已证实"
2. **ADMET 为计算预测值**：仅用于方向性判断，不替代实验测定；高风险信号（AMES/hERG）须实验验证
3. **DOI 可信度**：所有 DOI 来自检索工具返回的元数据；若 DOI 无法解析，在报告中标注"DOI待核实"
4. **图表渲染**：雷达图为 ECharts JSON 格式，在 Eureka 聊天界面内可直接渲染；Word 报告中以数据表格替代
5. **字体兼容性**：Word 报告依赖系统已安装的楷体（KaiTi）和 Times New Roman；若目标系统无楷体，建议改用宋体（SimSun）

---

## 版本历史

| 版本 | 日期 | 说明 |
|---|---|---|
| v1.0 | 2026-06-30 | 初始版本，基于肉桂酸×黄连素抗肿瘤协同探究案例构建 |

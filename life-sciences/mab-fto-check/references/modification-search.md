# M1.5 修饰检索规范（序列检索后执行）

## 执行时机

- **前置依赖**：M1 序列检索完成，专利池初步建立
- **执行时机**：M1 结束后、M2 关键词检索前
- **目的**：捕获以「修饰/改造」为核心权利要求的专利，补充序列检索的结构盲区

---

## 工具映射

| 子模块 | 主工具 | 辅助工具 |
|--------|--------|----------|
| M1.5-A 糖基化修饰 | `patsnap_search`（关键词） | — |
| M1.5-B PEG化修饰 | `patsnap_search`（关键词） | `ls_structure_search`（PEG结构） |
| M1.5-C Fc氨基酸突变 | `patsnap_search`（关键词+语义）+ **中文专项检索** | `ls_structure_search`（突变体结构） |
| M1.5-D ADC偶联修饰 | `patsnap_search`（关键词） | `ls_structure_search`（Linker/Payload结构）|
| M1.5-E 化学修饰结构 | `ls_structure_search`（SIM相似度检索） | `ls_admet_predict`（辅助验证） |

---

## ⭐ 中文专项检索规则（所有子模块适用）

### 氨基酸简称自动扩展规则

当检索式或用户输入中出现「位置+单字母缩写」格式的氨基酸突变描述时，**必须自动扩展为三种表达形式**并同时检索：

| 输入格式 | 扩展形式1（单字母） | 扩展形式2（三字母） | 扩展形式3（中文全称） |
|----------|--------------------|--------------------|----------------------|
| 428L | 428L / M428L | 428Leu / M428Leu | 428位亮氨酸 / 第428位亮氨酸 |
| 434S | 434S / N434S | 434Ser / N434Ser | 434位丝氨酸 / 第434位丝氨酸 |
| 252Y | 252Y / M252Y | 252Tyr / M252Tyr | 252位酪氨酸 / 第252位酪氨酸 |
| 254T | 254T / S254T | 254Thr / S254Thr | 254位苏氨酸 / 第254位苏氨酸 |
| 256E | 256E / T256E | 256Glu / T256Glu | 256位谷氨酸 / 第256位谷氨酸 |
| 234A | 234A / L234A | 234Ala / L234Ala | 234位丙氨酸 / 第234位丙氨酸 |
| 235A | 235A / L235A | 235Ala / L235Ala | 235位丙氨酸 / 第235位丙氨酸 |
| 329G | 329G / P329G | 329Gly / P329Gly | 329位甘氨酸 / 第329位甘氨酸 |
| 297A | 297A / N297A | 297Ala / N297Ala | 297位丙氨酸 / 第297位丙氨酸 |
| 239D | 239D / S239D | 239Asp / S239Asp | 239位天冬氨酸 / 第239位天冬氨酸 |
| 332E | 332E / I332E | 332Glu / I332Glu | 332位谷氨酸 / 第332位谷氨酸 |

**完整氨基酸三字母/中文对照表**：

| 单字母 | 三字母 | 中文名称 |
|--------|--------|----------|
| A | Ala | 丙氨酸 |
| R | Arg | 精氨酸 |
| N | Asn | 天冬酰胺 |
| D | Asp | 天冬氨酸 |
| C | Cys | 半胱氨酸 |
| E | Glu | 谷氨酸 |
| Q | Gln | 谷氨酰胺 |
| G | Gly | 甘氨酸 |
| H | His | 组氨酸 |
| I | Ile | 异亮氨酸 |
| L | Leu | 亮氨酸 |
| K | Lys | 赖氨酸 |
| M | Met | 蛋氨酸（甲硫氨酸）|
| F | Phe | 苯丙氨酸 |
| P | Pro | 脯氨酸 |
| S | Ser | 丝氨酸 |
| T | Thr | 苏氨酸 |
| W | Trp | 色氨酸 |
| Y | Tyr | 酪氨酸 |
| V | Val | 缬氨酸 |

### 中文专项检索式模板

针对任意突变位点（以428L为例），中文检索式格式：

```
中文突变检索式：
TAC_all:("428位亮氨酸" OR "428位Leu" OR "M428Leu" OR "428L" OR "M428L"
         OR "第428位" OR "428号位亮氨酸替换" OR "EU编号428" OR "EU numbering 428")

注意事项：
- 中文专利常用「第X位」「X位」「EU编号X位」等表述
- 需同时检索「突变为X」「替换为X」「取代为X」等动词描述
- 检索式补充："突变为亮氨酸" OR "取代为亮氨酸" OR "替换为Leu"
```

### 执行规则

```
输入：用户提供突变描述（任意格式）
扩展逻辑：
  IF 输入为「位置+单字母」(如 428L)：
    → 生成 英文单字母版：M428L / 428L
    → 生成 英文三字母版：M428Leu / 428Leu
    → 生成 中文全称版：第428位亮氨酸 / 428位亮氨酸
    → 生成 动词描述版：突变为亮氨酸 / 428位突变
  IF 输入为「位置+三字母」(如 428Leu)：
    → 反向推导单字母：M428L
    → 生成中文版：428位亮氨酸
  IF 输入为中文：
    → 提取位置编号 + 氨基酸名称
    → 生成对应英文单字母和三字母版本

所有扩展关键词合并为一个OR组，注入检索式
```

---

## M1.5-A 糖基化修饰检索

**覆盖范围**：N-糖基化、O-糖基化、去岩藻糖基化、糖工程平台

```
主检索式：
TAC_all:("glycosylation" OR "glycoengineering" OR "fucosylation" OR "afucosylation"
         OR "去岩藻糖基化" OR "糖基化" OR "糖工程" OR "sialylation" OR "唾液酸化"
         OR "N-glycan" OR "O-glycan" OR "glycoform")
AND TAC_all:("antibody" OR "monoclonal antibody" OR "抗体" OR "单抗" OR "<靶点名>")
AND MAINF:(C07K16 OR C12N)

平台技术专项：
TAC_all:("GlycoMab" OR "GlymaxX" OR "Potelligent" OR "MGAT3" OR "FUT8"
         OR "glycosyltransferase" OR "糖基转移酶")
```

**IPC补充**：C12P21/00、C12N9/10（糖基转移酶）

---

## M1.5-B PEG化修饰检索

**覆盖范围**：PEGylation、半衰期延长、白蛋白融合、XTEN融合

```
主检索式：
TAC_all:("PEGylation" OR "PEG" OR "polyethylene glycol" OR "聚乙二醇"
         OR "half-life extension" OR "半衰期延长" OR "albumin fusion" OR "白蛋白融合"
         OR "XTEN" OR "rHSA" OR "FcRn binding")
AND TAC_all:("antibody" OR "抗体" OR "<候选药名>" OR "<靶点名>")
AND MAINF:(A61K47 OR C07K16)
```

**结构检索**（`ls_structure_search` SIM模式）：
- 输入：PEG链 SMILES（`OCCOCCO` 重复单元）
- threshold：0.85
- 目的：检索含PEG结构的专利化合物

---

## M1.5-C Fc区氨基酸突变检索 ⭐核心模块

**覆盖范围**：效应功能增强/消除、FcRn亲和力改造、ADCC/CDC/ADCP调节

> ⚠️ **中文专项检索强制执行**：以下所有子检索式均须同步执行中文专项检索（按照本文件顶部「氨基酸简称自动扩展规则」展开，英文+三字母+中文全称三轨并行）

### C1：效应功能消除突变（LALA/LALAPG/DANA等）

```
英文检索式：
TAC_all:("LALA" OR "L234A" OR "L235A" OR "LALAPG" OR "P329G"
         OR "DANA" OR "D265A" OR "N297A" OR "N297G" OR "N297Q"
         OR "effector function" OR "silent Fc" OR "效应功能消除")
AND TAC_all:("antibody" OR "monoclonal antibody" OR "抗体")
AND MAINF:(C07K16)

中文专项补充检索式：
TAC_all:("234位丙氨酸" OR "L234Ala" OR "235位丙氨酸" OR "L235Ala"
         OR "329位甘氨酸" OR "P329Gly" OR "265位丙氨酸" OR "D265Ala"
         OR "297位丙氨酸" OR "N297Ala" OR "效应功能沉默" OR "沉默型Fc"
         OR "LALA突变" OR "LALAPG突变" OR "效应功能消除突变")
AND TAC_all:("抗体" OR "单抗" OR "单克隆抗体")
```

### C2：ADCC增强突变（S239D/I332E/G236A等）

```
英文检索式：
TAC_all:("S239D" OR "I332E" OR "G236A" OR "ADCC enhancement" OR "ADCC增强"
         OR "FcγRIIIa" OR "NK cell" OR "afucosylation" OR "去岩藻糖")
AND MAINF:(C07K16)

中文专项补充检索式：
TAC_all:("239位天冬氨酸" OR "S239Asp" OR "332位谷氨酸" OR "I332Glu"
         OR "236位丙氨酸" OR "G236Ala" OR "ADCC增强突变" OR "Fc增强型"
         OR "NK细胞杀伤" OR "FcγRIIIa结合增强")
AND TAC_all:("抗体" OR "单抗")
```

### C3：FcRn结合增强（YTE/LS/HL突变）—— 中文专项重点

```
英文检索式：
TAC_all:("YTE" OR "M252Y" OR "S254T" OR "T256E"
         OR "LS" OR "M428L" OR "N434S"
         OR "HL" OR "FcRn" OR "neonatal Fc receptor" OR "半衰期延长" OR "half-life")
AND TAC_all:("antibody" OR "抗体")
AND MAINF:(C07K16 OR A61K39)

中文专项补充检索式（YTE）：
TAC_all:("252位酪氨酸" OR "M252Tyr" OR "254位苏氨酸" OR "S254Thr"
         OR "256位谷氨酸" OR "T256Glu" OR "YTE突变" OR "YTE变体")
AND TAC_all:("抗体" OR "单抗" OR "Fc区")

中文专项补充检索式（LS）：
TAC_all:("428位亮氨酸" OR "428Leu" OR "M428Leu" OR "第428位亮氨酸"
         OR "434位丝氨酸" OR "434Ser" OR "N434Ser" OR "第434位丝氨酸"
         OR "LS突变" OR "LS变体" OR "M428L/N434S"
         OR "半衰期延长突变" OR "FcRn亲和力增强" OR "新生儿Fc受体")
AND TAC_all:("抗体" OR "单抗" OR "Fc" OR "免疫球蛋白")

中文专项补充检索式（通用）：
TAC_all:("EU编号" OR "EU numbering" OR "Kabat编号" OR "Fc变体" OR "Fc突变体"
         OR "Fc区氨基酸替换" OR "Fc区氨基酸突变" OR "重链恒定区突变")
AND MAINF:(C07K16)
```

### C4：双特异性Fc工程（knob-into-hole/CrossMab/BEAT等）

```
英文检索式：
TAC_all:("knob-into-hole" OR "knobs-into-holes" OR "KiH"
         OR "CrossMab" OR "BEAT" OR "SEEDbody" OR "Duobody"
         OR "asymmetric Fc" OR "heterodimerization" OR "异二聚体")
AND MAINF:(C07K16)

中文专项补充检索式：
TAC_all:("旋钮入孔" OR "杵臼结构" OR "异二聚化" OR "不对称Fc"
         OR "双特异性抗体Fc" OR "CrossMab技术" OR "异源二聚体Fc")
AND TAC_all:("抗体" OR "双抗" OR "双特异性")
```

**语义补充查询**：
`Fc region amino acid substitution mutation effector function half-life antibody engineering`

**结构检索**（`ls_structure_search` EXT精确模式）：
- 针对已知突变体肽段（如YTE突变Fc片段氨基酸序列转SMILES）
- 结合 `ls_admet_predict` 验证突变体理化性质变化

---

## M1.5-D ADC偶联修饰检索

**适用条件**：候选分子为ADC或含ADC竞品时激活

### D1：Linker检索

```
TAC_all:("linker" OR "连接子" OR "cleavable linker" OR "可裂解连接子"
         OR "non-cleavable" OR "不可裂解" OR "SMCC" OR "SPDP" OR "MC-VC-PABC"
         OR "maleimide" OR "马来酰亚胺" OR "disulfide" OR "二硫键"
         OR "GGFG" OR "β-glucuronide")
AND TAC_all:("antibody-drug conjugate" OR "ADC" OR "抗体药物偶联物")
AND MAINF:(A61K47 OR C07K16)
```

### D2：Payload载荷检索

```
TAC_all:("payload" OR "warhead" OR "cytotoxic" OR "细胞毒素"
         OR "MMAE" OR "MMAF" OR "DM1" OR "DM4" OR "SN-38" OR "DXd" OR "calicheamicin"
         OR "pyrrolobenzodiazepine" OR "PBD" OR "auristatin" OR "maytansine")
AND MAINF:(A61K47 OR C07K16 OR A61P35)
```

### D3：偶联位点与DAR值检索

```
TAC_all:("drug-to-antibody ratio" OR "DAR" OR "site-specific conjugation" OR "定点偶联"
         OR "cysteine conjugation" OR "lysine conjugation" OR "unnatural amino acid"
         OR "非天然氨基酸" OR "selenocysteine" OR "transglutaminase")
```

**结构检索**（`ls_structure_search` SIM模式）：
- 输入：目标Payload的SMILES
- threshold：0.85
- 结合 `ls_admet_predict` 预测Payload毒性/渗透性（Caco2/hERG/AMES）

---

## M1.5-E 化学修饰结构检索

**工具**：`ls_structure_search`（核心）+ `ls_admet_predict`（辅助）

**执行流程**：

```
步骤1：从M1专利池中提取含修饰基团的化合物结构
步骤2：转换为SMILES格式
步骤3：ls_structure_search (type=SIM, threshold=0.85)
        → 检索结构相似的修饰化合物专利
步骤4：ls_structure_search (type=EXT)
        → 精确匹配确认已知修饰结构
步骤5：ls_admet_predict（可选）
        → 预测修饰化合物的ADMET性质，辅助判断技术可行性
```

**覆盖修饰类型**：
- 荧光标记（FITC、Cy3/Cy5等探针）
- 放射性标记前体（用于诊断用抗体）
- 双功能螯合剂（DOTA/NOTA，用于核素偶联抗体）

---

## 结果整合规则

```
1. 所有M1.5子模块结果按 patent_id 去重
2. 并入总专利池，source_modules 字段标记为 "M1.5-X"
3. 修饰相关专利单独建立 modification_patent_pool 子集
4. 多模块命中（M1序列 + M1.5修饰）→ 风险权重上调至"高风险"
5. 仅M1.5命中（序列未命中）→ 标记为"修饰侵权风险"单独章节报告
6. 中文专项检索命中（且英文未命中）→ 标记来源字段 source_lang: "CN_specific"
```

---

## 修饰检索风险分级

| 命中情形 | 风险等级 | 处理策略 |
|----------|----------|----------|
| M1序列命中 + M1.5-C Fc突变命中 | 🔴 极高 | 立即出具设计绕开建议 |
| M1.5-C Fc突变命中（序列未命中） | 🟠 高 | 精筛权利要求，判断覆盖范围 |
| M1.5-D ADC Linker/Payload命中 | 🟠 高 | 结构分析+等同原则判断 |
| M1.5-A/B 糖基化/PEG化命中 | 🟡 中 | 确认是否为制备工艺专利 |
| M1.5-E 化学结构相似命中 | 🟡 中 | ADMET辅助验证+权利要求精读 |
| 中文专项检索独立命中 | 🟠 高 | 补充英文全文核实，纳入风险清单 |

# 单抗 FTO 9大检索模块规范

本文档定义 `mab-fto-check` 技能执行完整 FTO 检索时必须覆盖的 9 个模块，每个模块包含工具路由、检索策略和执行逻辑。

---

## 模块 1：抗体序列检索

**工具**：`ls_sequence_alignment`（Bio / Chemical 数据库）

### 检索维度与阈值

| 维度 | 序列区域 | 相似度阈值 | 侵权权重 | 说明 |
|------|----------|-----------|----------|------|
| CDR-H3 | 重链 CDR3 | 100%（精确匹配） | ★★★★★ | 最关键侵权判断区 |
| CDR-H1/H2 | 重链 CDR1/2 | ≥80% | ★★★★ | 配合 CDR-H3 综合判断 |
| CDR-L1/L2/L3 | 轻链互补决定区 | ≥80% | ★★★ | 与重链联合分析 |
| VH 全序列 | 重链可变区 | ≥85% | ★★★★ | 含框架区 + CDR |
| VL 全序列 | 轻链可变区 | ≥85% | ★★★ | 含框架区 + CDR |
| H 链全长 | 重链恒定区 + 可变区 | ≥90% | ★★ | IgG1/IgG4 亚型区分 |
| L 链全长 | 轻链恒定区 + 可变区 | ≥90% | ★★ | κ/λ 型区分 |
| 铰链区 | CH1-CH2 连接肽 | ≥95% | ★ | 工程化铰链单独检索 |
| 恒定区（Fc） | CH2 + CH3 | ≥95% | ★ | Fc 工程改造专利 |

### 执行逻辑

```
检索优先级: CDR-H3（精确）> CDR-H1/H2/L1/L2/L3 > VH/VL > H/L 全链 > 铰链区/恒定区
每个区域分别提交 ls_sequence_alignment，设定对应阈值
结果按 patent_id 去重后并入 patent_pool（标注 source_track=sequence）
记录每条命中的 similarity_score + alignment_region
```

### 侵权判断框架

- **字面侵权**：CDR-H3 精确匹配 + VH/VL ≥ 90% → 高风险
- **等同原则**：CDR-H3 ≥ 90% + 抗原结合表位相同 → 中-高风险
- **安全区间**：VH/VL < 85% 且 CDR-H3 < 90% → 低风险（需记录）

---

## 模块 2：结合靶点检索

**工具**：PatSnap 关键词 + 语义检索（`patsnap_search`）

### 关键词检索式模板

```
TAC_all:("<靶点名>" OR "<靶点别名>" OR "<靶点基因符号>")
AND TAC_all:("monoclonal antibody" OR "单克隆抗体" OR "mAb" OR "antibody" OR "抗体")
AND MAINF:(C07K16 OR A61K39)
```

### 示例（PD-1）

```
TAC_all:("PD-1" OR "PDCD1" OR "CD279" OR "programmed death-1" OR "程序性死亡受体1")
AND TAC_all:("monoclonal antibody" OR "mAb" OR "单克隆抗体" OR "抗体")
AND MAINF:(C07K16 OR A61K39)
```

### 语义检索补充

```
antibody targeting [靶点] binding epitope blocking neutralization
抗[靶点]抗体 结合表位 阻断 中和
```

### 扩展策略
- 加入靶点上下游信号通路蛋白别名
- 包含同靶点不同物种来源序列（human / mouse / chimeric）
- 限定有效专利 + 近 10 年申请（`APD:[20150101 TO 20251231]`）

---

## 模块 3：所用平台技术检索

**工具**：PatSnap 关键词检索

### 人源化平台

```
TAC_all:("humanization" OR "humanized" OR "CDR grafting" OR "resurfacing"
         OR "人源化" OR "CDR移植" OR "表面重塑")
AND MAINF:(C07K16)
```

### 全人抗体平台

```
TAC_all:("fully human" OR "human antibody" OR "phage display" OR "transgenic mouse"
         OR "HuMAb" OR "XenoMouse" OR "UltiMAb" OR "VelocImmune"
         OR "噬菌体展示" OR "转基因小鼠" OR "全人源抗体")
AND MAINF:(C07K16 OR A01K)
```

### 双特异性抗体平台

```
TAC_all:("bispecific" OR "BiTE" OR "CrossMab" OR "knob-into-hole" OR "DART"
         OR "IgG-like bispecific" OR "tandem scFv"
         OR "双特异性" OR "双抗" OR "双功能抗体")
AND MAINF:(C07K16)
```

### 抗体片段平台

```
TAC_all:("scFv" OR "Fab" OR "F(ab')2" OR "nanobody" OR "VHH" OR "sdAb"
         OR "单域抗体" OR "纳米抗体" OR "骆驼源抗体")
AND MAINF:(C07K16)
```

---

## 模块 4：基因编辑技术检索

**工具**：PatSnap 关键词检索

### 细胞工程改造

```
TAC_all:("CRISPR" OR "Cas9" OR "ZFN" OR "TALEN" OR "base editing" OR "prime editing"
         OR "基因编辑" OR "基因敲入" OR "knock-in" OR "基因组编辑")
AND TAC_all:("antibody" OR "抗体" OR "CHO" OR "HEK293" OR "<候选分子名>")
AND MAINF:(C12N OR C07K)
```

### Fc 工程化改造专项

```
TAC_all:("Fc engineering" OR "Fc modification" OR "ADCC" OR "ADCP" OR "CDC"
         OR "efucosylation" OR "afucosylation" OR "去岩藻糖基化"
         OR "half-life extension" OR "半衰期延长"
         OR "YTE mutation" OR "LS mutation" OR "LALA mutation" OR "LALAPG"
         OR "neonatal Fc receptor" OR "FcRn")
AND MAINF:(C07K16)
```

### 糖基化工程专项

```
TAC_all:("glycoengineering" OR "glycosylation" OR "fucosylation" OR "bisecting GlcNAc"
         OR "糖基化改造" OR "岩藻糖化")
AND MAINF:(C07K16 OR C12N)
```

---

## 模块 5：药物配方/制剂检索

**工具**：PatSnap 关键词检索

### 基础制剂配方

```
TAC_all:("<候选药物名>" OR "<靶点名> antibody")
AND TAC_all:("formulation" OR "制剂" OR "pharmaceutical composition" OR "药物组合物"
             OR "excipient" OR "辅料" OR "stabilizer" OR "稳定剂"
             OR "buffer" OR "缓冲液" OR "surfactant" OR "表面活性剂"
             OR "lyophilization" OR "冻干" OR "lyophilized powder" OR "冻干粉"
             OR "prefilled syringe" OR "预充注射器" OR "vial" OR "西林瓶")
AND MAINF:(A61K)
```

### 皮下注射/高浓度制剂专项

```
TAC_all:("subcutaneous" OR "皮下注射" OR "SC injection"
         OR "high concentration" OR "高浓度" OR "viscosity" OR "黏度"
         OR "hyaluronidase" OR "透明质酸酶" OR "ENHANZE" OR "rHuPH20")
AND MAINF:(A61K OR A61M)
```

### 长效缓释专项

```
TAC_all:("sustained release" OR "extended release" OR "depot" OR "缓释" OR "长效"
         OR "PEGylation" OR "PEG修饰" OR "half-life extension")
AND TAC_all:("antibody" OR "抗体")
AND MAINF:(A61K)
```

---

## 模块 6：联合用药检索

**工具**：PatSnap 关键词检索

### 通用联合用药模板

```
TAC_all:("<候选靶点>" OR "<候选药名>")
AND TAC_all:("combination" OR "联合用药" OR "co-administration" OR "联合给药"
             OR "synergistic" OR "协同" OR "combination therapy" OR "联合治疗"
             OR "concomitant" OR "concurrent")
AND TAC_all:("<已知联用药物>" OR "chemotherapy" OR "化疗"
             OR "checkpoint inhibitor" OR "免疫检查点"
             OR "targeted therapy" OR "靶向治疗"
             OR "radiation" OR "放疗" OR "CAR-T")
AND MAINF:(A61K OR A61P)
```

### 免疫肿瘤学联合专项

```
TAC_all:("anti-PD-1" OR "anti-PD-L1" OR "anti-CTLA-4" OR "anti-LAG-3" OR "anti-TIM-3")
AND TAC_all:("combination" OR "联合")
AND MAINF:(A61K39 OR A61P35)
```

---

## 模块 7：用途检索

**工具**：PatSnap 关键词 + 语义检索

### 适应症检索

```
TAC_all:("<靶点名>" OR "<候选药名>")
AND TAC_all:("<疾病名称>" OR "<疾病 ICD 分类>" OR "treatment" OR "治疗" OR "therapy")
AND MAINF:(A61P)
```

### 方法专利（Use/Method claim）专项

```
TAC_all:("method of treating" OR "治疗方法" OR "method of use" OR "use of"
         OR "用于治疗" OR "therapeutically effective amount" OR "治疗有效量"
         OR "administering to a patient" OR "给药于患者")
AND TAC_all:("<靶点>" OR "<候选分子>")
```

### 示例（抗PD-1 + 肿瘤）

```
TAC_all:("PD-1" OR "pembrolizumab" OR "nivolumab" OR "cemiplimab")
AND TAC_all:("cancer" OR "tumor" OR "肿瘤" OR "malignancy"
             OR "melanoma" OR "lung cancer" OR "NSCLC" OR "TNBC")
AND MAINF:(A61P35)
```

### 语义补充

```
treatment of [疾病] using antibody targeting [靶点] in patients
用[靶点]抗体治疗[疾病]患者的方法
```

---

## 模块 8：表达载体检索

**工具**：PatSnap 关键词检索

### 表达系统基础检索

```
TAC_all:("<候选药名>" OR "<靶点名> antibody" OR "<VH/VL 序列片段关键字>")
AND TAC_all:("expression vector" OR "表达载体" OR "expression system" OR "表达系统"
             OR "promoter" OR "启动子" OR "enhancer" OR "增强子"
             OR "CHO cell" OR "HEK293" OR "HEK-293" OR "SP2/0" OR "NS0" OR "Per.C6"
             OR "mammalian expression" OR "哺乳动物表达" OR "recombinant expression")
AND MAINF:(C12N)
```

### 信号肽/分泌系统专项

```
TAC_all:("signal peptide" OR "信号肽" OR "secretion signal" OR "leader sequence"
         OR "leader peptide" OR "IgG secretion" OR "antibody secretion"
         OR "sec signal" OR "分泌信号肽")
AND MAINF:(C12N15 OR C07K16)
```

### 宿主细胞工程专项

```
TAC_all:("CHO" OR "Chinese hamster ovary" OR "高表达" OR "high yield expression"
         OR "fed-batch" OR "perfusion culture" OR "灌流培养" OR "细胞培养基")
AND TAC_all:("antibody" OR "抗体" OR "IgG")
AND MAINF:(C12N5 OR C12N15)
```

---

## 模块 9：竞品专利 + IPC 分类号补充检索

**工具**：PatSnap 关键词 + IPC 分类过滤

### 竞品企业全量检索

```
ALL_AN:("<竞品公司1>" OR "<竞品公司2>" OR "<竞品公司3>")
AND MAINF:(C07K16 OR A61K39 OR C12N15)
AND TAC_all:("<靶点名>" OR "<适应症>")
AND APD:[20150101 TO 20251231]
```

### IPC 分类号定向补充

必查 IPC 组合（覆盖可能漏检的技术分支）：

| IPC 代码 | 技术内容 | 检索重点 |
|----------|----------|----------|
| C07K16/xx | 免疫球蛋白（抗体结构核心） | 结合靶点的抗体序列、结构 |
| A61K39/395 | 含抗体的药物制剂 | 治疗用单抗制剂专利 |
| C12N5/10 | 产抗体的细胞系 | 杂交瘤、CHO 等宿主细胞 |
| C12N15/13 | 编码免疫球蛋白的核酸 | 表达载体、基因序列专利 |
| C12N15/63 | 重组 DNA 载体 | 表达质粒、病毒载体 |
| A61P35/xx | 肿瘤适应症 | 治疗方法、用途专利 |
| A61P37/xx | 免疫疾病适应症 | 自免/炎症适应症专利 |

### IPC 定向补充检索式

```
MAINF:(C07K16) AND TAC_all:("<靶点>") AND ALL_AN:("<竞品A>" OR "<竞品B>")
MAINF:(C12N15/13) AND TAC_all:("<靶点>" OR "<候选药名>")
MAINF:(A61K39/395) AND TAC_all:("<靶点>" OR "<候选药名>")
```

### 近期申请时间窗口补充

```
APD:[20220101 TO 20251231]  ← 最近 3 年新申请（可能未公开）
PBD:[20220101 TO 20251231]  ← 近期公开（已公开未审结）
```

---

## 跨模块去重与整合规则

1. 所有模块结果统一按 `patent_id` 去重后并入 `patent_pool.json`
2. 每条专利记录必须标注来源模块（`source_modules: ["M1", "M3", "M9"]`）
3. 命中多个模块的专利风险权重上调
4. 模块 1 序列命中专利额外记录 `sequence_region` + `similarity_score`
5. 模块 9 竞品命中专利额外记录 `competitor_applicant`
6. 最终向 `mab_fto_recall_estimator.py` 提交三轨去重后的专利 ID 集合

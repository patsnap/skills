# 药物类型标准映射表 v1.0

## 用途

本文件定义用户输入的行业俗语与智慧芽新药库标准 `drug_type` 枚举值之间的强制映射关系。
Skill 在调用 `ls_patent_search`、`ls_drug_search` 等工具时，**必须优先查阅本表**，不得依赖 NER-NOR 自动识别。

---

## 映射表

| 用户输入（俗语/变体） | 标准 drug_type 枚举值 | 智慧芽内部分类名 | 说明 |
|---|---|---|---|
| 小核酸药物 | `Oligonucleotide` | 寡核苷酸 | ⚠️ 严禁传 `Nucleic acid` 或 `Small nucleic acid` |
| 小核酸 | `Oligonucleotide` | 寡核苷酸 | 同上 |
| siRNA药物 | `Oligonucleotide` | 寡核苷酸 | siRNA属于寡核苷酸子类 |
| ASO药物 | `Oligonucleotide` | 寡核苷酸 | 反义寡核苷酸属于寡核苷酸子类 |
| 反义寡核苷酸 | `Oligonucleotide` | 寡核苷酸 | |
| 核酸药物（泛指时） | `Oligonucleotide` | 寡核苷酸 | 若用户明确指小核酸语境，优先用子类 |
| mRNA药物 | `mRNA` | mRNA | 注意与寡核苷酸区分 |
| 基因治疗 | `Gene therapy` | 基因治疗 | |
| 单抗 | `Monoclonal antibody` | 单克隆抗体 | |
| ADC | `ADC` | 抗体药物偶联物 | |
| 小分子 | `Small molecule drug` | 小分子药物 | |

---

## 分类层级说明

```
核酸药物（Nucleic acid drugs） ← 父类，覆盖范围过宽，一般不直接使用
├── 寡核苷酸（Oligonucleotide） ← 小核酸药物的正确子类 ✅
│   ├── siRNA
│   ├── ASO（反义寡核苷酸）
│   ├── miRNA
│   └── aptamer（适配体）
├── mRNA 药物
└── 基因治疗
```

**关键原则**："小核酸药物"在中文行业语境中特指 siRNA/ASO/miRNA 等寡核苷酸类，
对应智慧芽标准分类 `Oligonucleotide`，**不是**上位概念 `Nucleic acid drugs`。

---

## 版本记录

| 版本 | 日期 | 变更内容 |
|---|---|---|
| 1.0 | 2026-05-18 | 初始版本，新增小核酸/寡核苷酸映射关系 |

# 检索式模板库 — 肠道微生物菌群全景调研

## 三轮核心检索参数

### 轮次 A：食品干预与菌群调控

```json
{
  "source": "patent",
  "search_strategy": ["semantic"],
  "semantic_query": "gut microbiome modulation by dietary fiber prebiotics probiotics fermented food health benefit",
  "filters": {
    "date_from": 20150101
  },
  "limit": 30,
  "sort": "relevance"
}
```

**目标覆盖主题：**
- 膳食纤维对菌群多样性的影响
- 益生元（FOS、GOS、菊粉）作用机制
- 发酵食品（酸奶、泡菜、克菲尔）菌群效应
- 益生菌菌株（Lactobacillus、Bifidobacterium）功能

---

### 轮次 B：菌群失调与疾病治疗

```json
{
  "source": "patent",
  "search_strategy": ["semantic"],
  "semantic_query": "intestinal microbiota dysbiosis metabolic disease obesity diabetes IBD inflammatory bowel disease treatment therapeutic intervention",
  "filters": {
    "date_from": 20150101
  },
  "limit": 30,
  "sort": "relevance"
}
```

**目标覆盖主题：**
- IBD（克罗恩病、溃疡性结肠炎）菌群特征
- 肥胖/代谢综合征菌群失调
- 2型糖尿病菌群干预
- NAFLD/NASH 肝脏-肠道轴
- FMT（粪菌移植）治疗方案

---

### 轮次 C：个性化营养、多组学与AI

```json
{
  "source": "patent",
  "search_strategy": ["semantic"],
  "semantic_query": "personalized nutrition microbiome multi-omics metagenomics machine learning AI food intervention gut health",
  "filters": {
    "date_from": 20150101
  },
  "limit": 30,
  "sort": "relevance"
}
```

**目标覆盖主题：**
- 基于菌群的个性化饮食推荐
- 宏基因组学/代谢组学数据挖掘
- 机器学习在菌群分析中的应用
- 数字健康平台与菌群监测

---

### 补充轮次 D：学术论文（高引用量）

```json
{
  "source": "paper",
  "search_strategy": ["semantic"],
  "semantic_query": "gut microbiome food nutrition health intervention clinical trial probiotic prebiotic",
  "filters": {
    "date_from": 20150101,
    "cited_min": 10
  },
  "limit": 20,
  "sort": "relevance"
}
```

---

## 关键词备选清单（keyword模式）

### 中文关键词
- 肠道微生物、肠道菌群、肠道微生态
- 益生菌、益生元、合生元
- 膳食纤维、短链脂肪酸、丁酸
- 肠道屏障、肠道通透性
- 菌群失调、菌群移植
- 炎症性肠病、代谢综合征

### 英文关键词
- gut microbiome, gut microbiota, intestinal microflora
- probiotic, prebiotic, synbiotic, postbiotic
- dietary fiber, short-chain fatty acids, butyrate
- intestinal barrier, gut permeability, leaky gut
- dysbiosis, fecal microbiota transplantation (FMT)
- inflammatory bowel disease, metabolic syndrome

---

## IPC 分类参考

| IPC代码 | 技术方向 |
|---------|---------|
| A23L 33/135 | 益生菌食品添加剂 |
| A61K 35/741 | 乳酸菌治疗用途 |
| C12N 1/20 | 微生物培养 |
| A61P 1/00 | 消化系统疾病治疗 |
| G16H 20/60 | 营养数字健康 |
| C12Q 1/689 | 微生物基因检测 |

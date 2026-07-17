---
name: microbiome-disease-research
description: "研究微生物组与疾病机制证据链并形成研究假设。适用于：梳理菌群、代谢物、宿主通路与疾病表型之间的证据链，区分相关性与因果性并形成可验证研究假设。"
---

# Gut Microbiome Investigator — 肠道微生物菌群文献全景调研

## Overview

本 Skill 专为**食品领域大模型微调数据收集**与**肠道微生物菌群研究全景分析**设计。
输入目标领域关键词，自动执行三轮 PatSnap 检索，汇总 50+ 篇代表性文献，
生成覆盖 11 个模块的专业 HTML 全景报告，左侧导航栏固定，支持章节快速跳转。

---

## Trigger Conditions（触发场景）

当用户请求以下内容时加载本 Skill：
- 肠道微生物 / 肠道菌群 / gut microbiome / gut microbiota 文献调研
- 益生菌 / 益生元 / 膳食纤维 / 发酵食品相关专利/文献分析
- 食品领域模型微调训练数据收集
- 微生物与疾病（IBD、T2D、肥胖、代谢综合征）关联研究综述
- 近 N 年肠道微生物研究全景报告

典型触发语句：
- "帮我调研肠道菌群近10年文献，出HTML报告"
- "整理益生菌专利，用于食品AI模型训练"
- "分析肠道微生物与代谢疾病的研究现状"
- "gut microbiome landscape report for food AI fine-tuning"

---

## Workflow（执行流程）

### Step 1 — 参数确认
- 确认研究领域（默认：食品/营养，可选：临床/农业/美妆）
- 确认时间范围（默认：近10年，即 date_from=20150101）
- 确认文献数量下限（默认：≥50篇）
- 确认输出语言（默认：中文，可选：英文/双语）

### Step 2 — 三轮 PatSnap 语义检索

**轮次 A：核心菌群-食品干预**
```
semantic_query: "gut microbiome modulation by dietary fiber prebiotics probiotics fermented food"
filters: {date_from: 20150101}
limit: 30
```

**轮次 B：菌群-疾病关联**
```
semantic_query: "intestinal microbiota dysbiosis metabolic disease obesity diabetes IBD treatment"
filters: {date_from: 20150101}
limit: 30
```

**轮次 C：个性化营养与AI/组学**
```
semantic_query: "personalized nutrition microbiome multi-omics machine learning food intervention"
filters: {date_from: 20150101}
limit: 30
```

### Step 3 — 学术论文补充检索（可选）
```
source: "paper"
semantic_query: "gut microbiome food nutrition health intervention clinical trial"
filters: {date_from: 20150101, cited_min: 10}
limit: 20
```

### Step 4 — 数据整理与分组
按以下10个主题分组，每组筛选 ≥5 篇代表性文献：
- A. 个性化营养与菌群图谱
- B. 益生菌与益生元组合
- C. 膳食纤维与 SCFA
- D. 发酵食品与多样性
- E. 代谢综合征干预
- F. 炎症性肠病（IBD）
- G. 肥胖与能量代谢
- H. 2型糖尿病（T2DM）
- I. 神经-肠轴（Gut-Brain Axis）
- J. 多组学与AI方法

### Step 5 — HTML 报告生成
生成包含以下 11 个模块的 HTML 全景报告：

1. **执行摘要** — 检索统计卡片、报告结构导览
2. **规模与趋势** — 子领域规模对比、年度趋势、IPC分类
3. **核心技术方向** — 六大技术主线 + TRL成熟度评估
4. **关键菌属图谱** — 9个核心菌属（功能/食品关联/热度）
5. **疾病关联研究** — 六大疾病方向 + 食品可干预证据链
6. **食品与膳食干预** — 膳食纤维/益生元/发酵食品/特殊饮食
7. **主要申请人** — 12家核心机构全景分析
8. **代表性文献** — 52条文献，按A–J主题分组，含[S#]标注
9. **研究时间线** — 2015→2025关键时期演进图谱
10. **模型微调指引** — 训练数据优先级、任务类型、标注规范
11. **未来趋势** — 六大新兴方向 + 五个研究空白

---

## Output Spec（输出规范）

| 输出物 | 格式 | 说明 |
|--------|------|------|
| HTML全景报告 | `.html` | 左侧固定导航栏，11个模块，支持深色/浅色切换 |
| 来源列表 | Markdown | 所有[S#]引用的完整来源信息 |
| 摘要卡片 | 内嵌HTML | 关键数字卡（检索量、文献数、IPC数等） |

---

## Quality Gates（质量门控）

- ✅ 文献数量 ≥ 50 篇，否则补充检索
- ✅ 时间范围覆盖 2015–当前年
- ✅ 每个主题分组 ≥ 5 篇
- ✅ 所有文献均有 [S#] 来源标注
- ✅ HTML 文件可独立打开，无外部依赖
- ✅ 导航栏左侧固定，宽度 220px

---

## Guardrails（安全护栏）

- 本 Skill 仅用于**文献调研与报告生成**，不提供医疗建议
- 所有结论均来自 PatSnap 检索结果，不凭空编造文献
- 专利文献与学术论文来源区分标注
- 不处理个人健康数据或患者信息

---

## Dependencies（依赖）

- `patent.search` → `mcp_patent-search__patsnap_search`（PatSnap专利检索）
- `paper.search` → `mcp_patent-search__patsnap_search`（PatSnap论文检索）
- `files` （HTML报告写入）
- Python 3.12（数据整理，可选）

---

## References

- `references/search_query_templates.md` — 检索式模板库（三轮检索参数）
- `references/html_report_template.md` — HTML报告结构规范
- `references/topic_taxonomy.md` — 主题分组分类法（A–J）
- `assets/report_style.css` — HTML样式规范（左侧导航/配色/字体）

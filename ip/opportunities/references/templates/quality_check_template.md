# 质量核查模板

# 质量核查报告

**技术方向：** {{TOPIC}}  
**核查时间：** {{REPORT_DATE}}  
**核查方式：** 文件存在性检查 + 内容抽样 + 数据来源追溯  

---

## 1. 文件完整性

| 文件 | 状态 | 大小估算 | 备注 |
|------|------|----------|------|
| index.html | {{INDEX_STATUS}} | {{INDEX_SIZE}} | 主报告 |
| patents.html | {{PATENTS_STATUS}} | {{PATENTS_SIZE}} | 代表专利 |
| evidence.html | {{EVIDENCE_STATUS}} | {{EVIDENCE_SIZE}} | 证据链 |
| subfields.html | {{SUBFIELDS_STATUS}} | {{SUBFIELDS_SIZE}} | 子技术 |
| methodology.html | {{METHODOLOGY_STATUS}} | {{METHODOLOGY_SIZE}} | 方法说明 |
| intermediate_data.json | {{JSON_STATUS}} | {{JSON_SIZE}} | 中间数据 |
| patent_list.csv | {{CSV_STATUS}} | {{CSV_SIZE}} | 代表专利列表 |
| evidence_mapping.csv | {{EV_CSV_STATUS}} | {{EV_CSV_SIZE}} | 证据映射 |
| README.md | {{README_STATUS}} | — | 说明文件 |

---

## 2. 数据统计合规性

| 核查项 | 状态 | 说明 |
|--------|------|------|
| 趋势图数据来源 | {{TREND_SRC_STATUS}} | {{TREND_SRC_NOTE}} |
| 年份覆盖（2015至今） | {{YEAR_COV_STATUS}} | {{YEAR_COV_NOTE}} |
| TopK50禁用（趋势统计） | {{TOPK_STATUS}} | {{TOPK_NOTE}} |
| 分桶统计（如需） | {{BUCKET_STATUS}} | {{BUCKET_NOTE}} |
| methodology说明口径 | {{METH_STATUS}} | {{METH_NOTE}} |

---

## 3. HTML 质量

| 核查项 | 状态 |
|--------|------|
| meta charset UTF-8 | {{CHARSET_STATUS}} |
| ECharts 图表有数据 | {{CHART_STATUS}} |
| 无 TODO/占位符 | {{TODO_STATUS}} |
| 无空图表/空表格 | {{EMPTY_STATUS}} |
| 导航链接完整 | {{NAV_STATUS}} |
| 代表专利免责提示 | {{DISCLAIMER_STATUS}} |

---

## 4. 数据一致性

| 核查项 | 状态 | 备注 |
|--------|------|------|
| KPI与JSON一致 | {{KPI_CONS_STATUS}} | {{KPI_CONS_NOTE}} |
| 证据链完整 | {{EV_CONS_STATUS}} | {{EV_CONS_NOTE}} |
| 评分一致 | {{SCORE_CONS_STATUS}} | {{SCORE_CONS_NOTE}} |

---

## 5. 禁止项核查

| 项目 | 状态 |
|------|------|
| 无 .py 文件 | ✅ 通过 |
| 无 scripts/ 目录 | ✅ 通过 |
| 无依赖Python的工作流 | ✅ 通过 |
| 无基于TopK50的趋势图 | {{NO_TOPK_TREND_STATUS}} |
| 无编造专利数据 | {{NO_FABRICATION_STATUS}} |

---

## 6. 已知限制

{{LIMITATIONS_CONTENT}}

---

## 7. 核查结论

**整体状态：** {{OVERALL_STATUS}}

{{CONCLUSION_TEXT}}

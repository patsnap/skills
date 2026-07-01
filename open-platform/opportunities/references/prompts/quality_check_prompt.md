# Quality Check Prompt — 质量核查

## 任务
在所有文件生成完成后，执行系统性质量核查，不依赖 Python。

## 核查方式
通过 `files` 工具检查文件是否存在，通过内容抽查验证质量。

## 核查清单

### 1. 文件完整性核查

必须存在的文件：
- [ ] index.html
- [ ] patents.html
- [ ] evidence.html
- [ ] subfields.html
- [ ] methodology.html
- [ ] intermediate_data.json
- [ ] patent_list.csv
- [ ] evidence_mapping.csv
- [ ] README.md
- [ ] quality_check.md（本文件）

**如有任何文件缺失，必须立即重新生成，不得继续输出最终结论。**

### 2. 数据统计合规性核查

趋势图数据来源验证：
- [ ] intermediate_data.json 中 full_scope_metrics.trend_yearly_application 是否存在
- [ ] 是否包含 2015 年至当前年份的完整数据
- [ ] trend_data_source 字段是否标注（trends_mcp / bucketing_search / unavailable）
- [ ] 如果 trend_data_source = "unavailable"，index.html 中是否已移除趋势图并说明限制

TopK50 使用边界验证：
- [ ] index.html 的图表数据是否仅来自 full_scope_metrics
- [ ] patents.html 是否明确标注"代表性样本"免责提示
- [ ] 任何趋势结论是否错误引用了 evidence_sample 中的年份统计

### 3. HTML 质量核查

index.html：
- [ ] 含 `<meta charset="UTF-8">`
- [ ] 含顶部导航
- [ ] 含 ECharts CDN 引用
- [ ] 所有 ECharts 图表容器有 id
- [ ] 图表初始化代码存在且有真实数据（非空数组）
- [ ] 无 TODO、无占位符文本
- [ ] KPI 卡片有真实数值
- [ ] 无乱码风险（所有中文字符通过 UTF-8 保存）

patents.html：
- [ ] 含代表性样本免责横幅
- [ ] 专利表格有数据（至少 20 行）
- [ ] 专利链接格式正确（如：https://eureka.zhihuiya.com/...）

evidence.html：
- [ ] claim_id 从 C001 开始连续编号
- [ ] 至少 10 条证据链
- [ ] 证据强度字段不为空

subfields.html：
- [ ] 包含 4-8 个子技术分支
- [ ] 每个分支有专利数量（来自全量统计）
- [ ] 每个分支有进入建议标签

methodology.html：
- [ ] 检索式有具体内容（非占位符）
- [ ] 明确说明全量统计 vs TopK50 的区别
- [ ] 如使用分桶统计，有分桶方法说明

### 4. 数据一致性核查

- [ ] index.html KPI 卡片数值是否与 intermediate_data.json 中 full_scope_metrics.total_count_global 一致
- [ ] evidence.html 中的 claim_id 是否都在 evidence_mapping.csv 中
- [ ] patents.html 中的专利号是否都在 patent_list.csv 中
- [ ] scoring_result.total_score 是否与 index.html 展示的综合推荐指数一致

### 5. 禁止项核查

- [ ] 是否存在任何 .py 文件 → 不得存在
- [ ] 是否存在 scripts/ 目录 → 不得存在
- [ ] 是否存在依赖 Python 的步骤 → 不得存在
- [ ] 是否存在基于 TopK50 的趋势图 → 不得存在
- [ ] 是否存在编造的专利数据 → 不得存在

## 核查报告输出格式（quality_check.md）

```markdown
# 质量核查报告

## 核查时间
[生成时间]

## 文件完整性
| 文件 | 状态 | 备注 |
|------|------|------|
| index.html | ✅ 存在 | |
| ... | | |

## 数据统计合规性
- 趋势图数据来源：[trends_mcp / bucketing_search / 未获取]
- 年份覆盖范围：2015 至 [当前年份]
- TopK50 使用限制：仅用于代表专利样本，不用于趋势统计
- 是否存在全量统计缺口：[说明]

## HTML 质量
- charset：✅
- 图表有数据：✅
- 无占位符：✅
- [其他]

## 数据一致性
- KPI 一致性：✅
- 证据链完整性：✅
- [其他]

## 已知限制
1. [限制1]
2. [限制2]

## 核查结论
[通过 / 存在问题待修复]
```

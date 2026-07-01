# Trend Analysis Prompt — 趋势分析

## 任务
基于 full_scope_metrics 中的年度统计数据，生成趋势分析结论。

## 输入
- full_scope_metrics.trend_yearly_application：年度申请量（全量）
- full_scope_metrics.total_count_global：全球总量
- full_scope_metrics.total_count_cn：中国总量

## 分析维度

### 1. 增长趋势判断
计算：
- 2015 年至当前年份整体增长率：(当年量 - 2015年量) / 2015年量 × 100%
- 近五年复合增长率（CAGR）：基于近五年数据
- 近三年活跃度：近三年平均申请量 vs 整体平均

判断阶段（选择最匹配项）：
- **起步期**：年均申请 < 200，增长率不稳定，2015年以前数据极少
- **快速增长期**：近三年 CAGR > 15%，绝对量持续增加
- **加速增长期**：近三年 CAGR > 30%
- **成熟期**：年均申请量大，增长趋稳，CAGR < 10%
- **波动期**：增长不稳定，有明显峰谷
- **衰退期**：近三年申请量持续下降

### 2. 关键拐点识别
- 增长拐点：增速明显加快的年份
- 峰值年份：申请量最高的年份
- 下降拐点：增速明显放缓的年份（如有）

### 3. 中国 vs 全球对比
- 中国占比 = total_count_cn / total_count_global
- 中国趋势 vs 全球趋势
- 中国是否是主要技术来源国

### 4. 近年趋势解读
注意：当前年份（2025年）数据可能不完整（专利公开有延迟），
最近 1-2 年数据应标注"可能因公开延迟而低估"。

## 输出格式
```json
{
  "trend_analysis": {
    "overall_growth_rate": 0.456,
    "cagr_5yr": 0.189,
    "activity_recent_3yr": "高/中/低",
    "stage": "快速增长期",
    "stage_evidence": "近五年CAGR=18.9%，近三年年均申请量XXX，相比2015年增长XXX%",
    "key_inflection_years": [
      {"year": 2019, "type": "加速点", "description": "增速明显提高"}
    ],
    "peak_year": 2023,
    "cn_global_ratio": 0.452,
    "cn_is_leading": true,
    "recent_trend_note": "2024-2025年数据可能因公开延迟而低估",
    "trend_conclusion": "该技术方向自2015年以来专利申请量持续增长，近五年CAGR达18.9%，处于快速增长期。中国是最主要的技术来源国，占比超过45%。"
  }
}
```

## 重要提醒
- 所有数值必须来自 full_scope_metrics.trend_yearly_application
- 不得基于 TopK50 样本推断趋势
- 如果年度数据来自分桶统计，在结论中说明

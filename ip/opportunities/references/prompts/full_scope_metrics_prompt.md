# Full Scope Metrics Prompt — 全量统计数据采集

## 任务
使用当前可用的 MCP 工具采集全量统计数据（full_scope_metrics），为报告图表提供可靠数据基础。

## 重要规则

**严禁将 TopK 专利样本当作全量统计。**

必须调用以下类型的 MCP 接口获取聚合统计：
- 年度趋势统计（非专利列表中的年份字段）
- 申请人排名
- 地域分布
- 法律状态统计

## 必须执行的数据采集步骤

### 步骤 1：全球年度申请趋势
优先调用：`patsnap-patent-technology-landscape__trends`（传入 query_text 和 apply_start_time=2015）

如果返回年度统计，直接使用。
如果未返回年度统计，执行分桶策略：
```
对于每一年 Y（从 2015 至当前年份）：
  调用检索 MCP，限定申请年 = Y
  记录 total_count 作为该年申请量
构建 trend_yearly_application = {year: count} 字典
```

### 步骤 2：法律状态统计
调用：`patsnap-patent-technology-landscape__simple_legal_status`
记录：{有效: N, 审中: N, 失效: N}

### 步骤 3：申请人排名（全球）
调用：`patsnap-patent-technology-landscape__applicant_ranking`
记录：Top 20 申请人及其申请量

### 步骤 4：技术来源国/地区
调用：`patsnap-patent-technology-landscape__priority_country`
记录：Top 15 国家及其专利量

### 步骤 5：中国专利趋势（单独检索）
在检索式基础上增加 authority=CN 限制
重复步骤 1 的分桶逻辑

### 步骤 6：子技术分支数量
对每个子技术方向（4-8 个）：
- 用更精确的子方向检索式单独检索
- 记录 total_count 和近五年每年 count

## 异常处理规则

| 情况 | 处理方式 |
|------|----------|
| trends MCP 返回完整年度数据 | 直接使用，标记 trend_data_source = "trends_mcp" |
| trends MCP 无年度数据 | 执行分桶检索，标记 trend_data_source = "bucketing_search" |
| 分桶检索失败 | 标记 trend_data_source = "unavailable"，不生成趋势图 |
| 申请人排名 MCP 失败 | 使用代表专利中的申请人频次作为近似，标记为低置信度 |
| 地域分布 MCP 失败 | 标记为不可用，不生成地域图 |

## 输出格式（写入 intermediate_data.json 的 full_scope_metrics 字段）
```json
{
  "total_count_global": 数字,
  "total_count_cn": 数字,
  "trend_data_source": "trends_mcp | bucketing_search | unavailable",
  "trend_yearly_application": {
    "global": {"2015": N, "2016": N, ...},
    "cn": {"2015": N, "2016": N, ...}
  },
  "trend_year_range": "2015-当前年份",
  "legal_status": {"有效": N, "审中": N, "失效": N},
  "active_rate": 数字（百分比）,
  "top_applicants_global": [{"name": "...", "count": N}, ...],
  "top_countries": [{"country": "CN", "count": N}, ...],
  "subfield_counts": {
    "子技术方向1": {"total": N, "trend": {...}},
    ...
  },
  "collection_timestamp": "ISO时间戳",
  "collection_notes": "采集过程说明"
}
```

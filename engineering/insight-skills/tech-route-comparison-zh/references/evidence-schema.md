# 证据模式

## query_log.csv

最小列要求：

- `query_id`（查询编号）
- `timestamp`（时间戳）
- `tool`（工具）
- `purpose`（目的）
- `query_text`（查询文本）
- `scope`（范围）
- `result_count`（结果数量）
- `notes`（备注）

## source_index.csv

最小列要求：

- `source_id`（来源编号）
- `title`（标题）
- `source_type`（来源类型）
- `organization`（机构）
- `date`（日期）
- `url_or_locator`（URL 或定位符）
- `why_it_matters`（重要性说明）
- `confidence`（置信度）

## claim_ledger.csv

最小列要求：

- `claim_id`（声明编号）
- `claim`（声明内容）
- `claim_type`（声明类型）
- `supporting_source_ids`（支撑来源编号）
- `confidence`（置信度）
- `counterpoint_or_limit`（反驳点或局限性）
- `decision_relevance`（决策相关性）

## 引用规范

- 在报告和声明台账中保持对比基准的明确性。
- 确保主要路线排名在声明台账中可溯源。
- 使用稳定的来源编号，如 `S001`、`S002`、`S003`。

# 证据模式（Evidence Schema）

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

- `claim_id`（主张编号）
- `claim`（主张内容）
- `claim_type`（主张类型）
- `supporting_source_ids`（支撑来源编号）
- `confidence`（置信度）
- `counterpoint_or_limit`（反驳或局限）
- `decision_relevance`（决策相关性）

## 引用规范

- 在主张台账中保持玩家纳入逻辑的可溯源性。
- 在主张台账中保持最终分层逻辑的可溯源性。
- 使用稳定的来源编号，如 `S001`、`S002`、`S003`。

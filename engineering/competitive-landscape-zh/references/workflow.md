# 工作流（Workflow）

使用可写的运行文件夹，例如：

`artifacts/competitive-landscape/<YYYYMMDD-主题>/`

推荐目录结构：

- `request.md`
- `workplan.md`
- `method_decisions.md`
- `query_log.csv`
- `source_index.csv`
- `claim_ledger.csv`
- `report.md`
- `notes/`
- `deliverables/`

## 执行顺序

1. 冻结范围：主题、地区、目的、时间窗口和玩家数量目标。
2. 从多次搜索和多个来源通道构建候选池。
3. 在分层前对候选池进行标注或规范化。
4. 将最强玩家晋升至最终对比集合。
5. 在该缩窄集合上对比技术路线押注和地理分布。
6. 仅在玩家集合和主要主张可溯源后，再撰写 `report.md`。

## 恢复顺序

若运行中断，按以下顺序优先读取文件：

1. `request.md`
2. `workplan.md`
3. `method_decisions.md`
4. `claim_ledger.csv`
5. `source_index.csv`
6. `query_log.csv`
7. `report.md`

## 路由规则

若任务收窄至单一公司，转移至 `company-tech-profile`。

若任务变为纯路线决策且无玩家对象，转移至 `tech-route-comparison`。

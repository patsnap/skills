# 工作流

使用可写运行目录，例如：

`artifacts/rd-initiation-review/<YYYYMMDD-项目名>/`

推荐目录结构：

- `request.md`
- `workplan.md`
- `method_decisions.md`
- `query_log.csv`
- `source_index.csv`
- `claim_ledger.csv`
- `report.md`
- `novelty-note.md`
- `notes/`
- `deliverables/`

## 执行顺序

1. 冻结范围：项目对象、关口、受众、时间窗口和模式。
2. 在外部检索前提取提案陈述主张。
3. 将创新点归一化为简短对比集。
4. 检索外部证据，测试新颖性、可行性和重叠情况。
5. 在主张台账中构建建议和条件。
6. 仅在主要主张可追溯后，再撰写 `report.md` 和 `novelty-note.md`。

## 恢复顺序

若运行中断，按以下顺序优先读取文件：

1. `request.md`
2. `workplan.md`
3. `method_decisions.md`
4. `claim_ledger.csv`
5. `source_index.csv`
6. `query_log.csv`
7. `report.md`
8. `novelty-note.md`

## 路由规则

若无具体项目对象，停止强行使用本技能。

- 仅涉及路线决策的，路由至 `tech-route-comparison`。
- 仅涉及公司画像的，路由至 `company-tech-profile`。
- 涉及多方竞争格局的，路由至 `competitive-landscape`。

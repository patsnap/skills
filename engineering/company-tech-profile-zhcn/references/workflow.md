# 工作流（Workflow）

使用可写运行目录，例如：

`artifacts/company-tech-profile/<YYYYMMDD-公司名-主题>/`

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

1. 冻结范围：公司、主题、用途、时间窗口和受众。
2. 在统计活动前解析主体边界和别名。
3. 以窄批次检索证据，而非一次性宽泛搜索。
4. 随时将有用来源录入 `source_index.csv`。
5. 在 `claim_ledger.csv` 中将证据转化为明确主张。
6. 仅在主要主张附有证据后，再撰写 `report.md`。

## 恢复顺序

若运行中断，按以下顺序优先读取：

1. `request.md`
2. `workplan.md`
3. `method_decisions.md`
4. `claim_ledger.csv`
5. `source_index.csv`
6. `query_log.csv`
7. `report.md`

## 路由规则

若任务漂移至竞争格局绘制、分级或多方比较，停止扩展本次运行，将任务移至 `competitive-landscape`。

若任务变为纯路线问题，移至 `tech-route-comparison`。

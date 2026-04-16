# 工作流

使用可写的运行目录，例如：

`artifacts/tech-route-comparison/<YYYYMMDD-主题>/`

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

1. 冻结范围：主题、路线集合、场景、目的、时间窗口和模式。
2. 在大范围检索前写好对比基准。
3. 在可比较的桶中检索各路线证据。
4. 将证据归一化为一个对比矩阵。
5. 将主要路线判断提升至声明台账。
6. 仅在主要排名逻辑可溯源后，再撰写 `report.md`。

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

若某家具名公司成为主要对象，将任务转至 `company-tech-profile`。

若参与者发现或竞争格局图谱成为主要对象，将任务转至 `competitive-landscape`。

若具体提案成为主要对象，将任务转至 `rd-initiation-review`。

# 数据采集步骤

## Step 1: 企业总量
filters.assignees=[assignee], topk=1
→ 获取企业专利总数（P001）

## Step 2: 发明人专利清单
filters.assignees=[assignee], filters.inventors=[inventor], topk=100
date_type=publication, 降序排列（最新100件）
→ 获取 A1=matched_total（全量精确），returned_count=100（最新样本）
→ 提取字段：cited_count, jurisdiction, ipc, legal_status, publication_date, inventors[]

### ⚠️ A1 > 100 时的处理规则
- **召回策略：** 取离今天时间最近的100条专利（date_type=publication，降序）
- **样本说明：** 在报告样本说明色块中以小字备注：
  「当前展示最新100件（按公开日降序），全量共A1件」
- **统计指标：** 所有分析指标（A14/IPC/被引/法律状态等）均基于最新100件样本
- **附录标题：** 注明「代表性科创成果清单（最新100件样本中按公开日降序取10条）」

### topk限制与代表性对照

| A1 | 展示样本 | 样本说明备注 | 显示模式 |
|:--:|:-------:|------------|:-------:|
| ≤ 100件 | ✅ 全量 | 无需备注 | 单屏 |
| 101～200件 | ⚠️ 最新100件 | 小字备注全量总数 | **分屏** |
| 201～400件 | ⚠️ 最新100件 | 小字备注全量总数 | **分屏** |
| > 400件 | ❌ 最新100件 | 小字备注全量总数+建议分段 | **分屏** |

## Step 3: A14核验
从Step2结构化数据中逐条判断 inventors[0]==inventor
→ 计算A14（样本内精确），A14/A1（基于样本的主导率估算）
→ A1>100时，报告中标注「主导率基于最新100件样本估算」

## Step 4: 法律状态分布
从Step2聚合 legal_status 字段
→ active/pending/inactive/WO 各自件数与占比（均为样本内统计）

## Step 5: 到期预警
filters.assignees=[assignee], filters.inventors=[inventor]
date_type=expired, date_from=TODAY, date_to=TODAY+3Y
→ 3年内到期件数与清单

## Step 6: 核心团队
filters.assignees=[assignee], topk=100
→ 统计inventors频次，分层，判定目标发明人层级

## Step 7: 论文
sources=[paper], filters.inventors=[inventor]
→ 学术论文发表数量

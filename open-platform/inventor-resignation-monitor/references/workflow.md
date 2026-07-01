# 发明人离职监控 — 完整工作流

## 概述

本 Skill 分两个阶段运行：

1. **AI检索阶段**（由 Eureka AI 执行）：调用 PatSnap 专利检索 API，收集发明人数据
2. **报告生成阶段**（由 Python 脚本执行）：将检索结果渲染为 HTML 简报

---

## 阶段一：AI 检索步骤

### Step 1：获取目标公司历史发明人

```
mcp_patent-search__patsnap_search(
  search_strategy=["filter"],
  sources=["patent"],
  filters={"assignees": ["<公司名>"]},
  topk=100
)
```

从结果中提取所有发明人及其最近申请年份。

### Step 2：筛选疑似离职发明人

规则：发明人在目标公司的最后申请年 < 当前年份 - inactive_years

例如：2026年，inactive_years=5 → 最后申请年 < 2021

### Step 3：对每位疑似离职发明人检索他处专利

```
mcp_patent-search__patsnap_search(
  search_strategy=["keyword", "filter"],
  keywords=["<技术关键词1>", "<技术关键词2>"],
  sources=["patent"],
  filters={
    "inventors": ["<发明人姓名>"],
    "date_from": <monitor_start_yyyymmdd>,
    "date_type": "application"
  },
  topk=20
)
```

过滤掉申请人包含目标公司名称的记录。

### Step 4：风险评级逻辑

| 风险等级 | 判定条件 |
|---------|--------|
| 🔴 高风险 | 新专利 IPC 与原公司核心专利 IPC 相同小类，且技术词高度重叠 |
| 🟠 中风险 | 新专利 IPC 同大类，或技术词部分重叠 |
| 🟡 持续关注 | 在技术相关领域有活跃专利申请，技术词无重叠但值得关注 |
| 🟢 低风险 | 监控期内无相关专利，或技术方向完全不同 |

---

## 阶段二：报告生成

将 Step 1-4 的结果整理为标准 JSON 格式（见 `generate_report.py` 注释），
然后运行：

```bash
MONITOR_DATA_JSON=data.json python generate_report.py --output report.html
```

---

## 注意事项

- 专利公开时滞约18个月，最近申请的专利可能尚未可见
- 同名发明人需结合技术领域二次确认
- 建议每季度执行一次

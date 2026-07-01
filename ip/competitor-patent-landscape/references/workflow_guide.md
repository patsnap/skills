# 竞争对手专利布局策略调研 — 工作流指南

## 概述
本技能帮助企业 IP 团队快速调研竞争对手在某技术领域的专利布局策略，
识别对方的核心保护点、外围延伸方向，以及在不同市场的布局强度，
最终输出一份可直接用于研发决策参考的 PDF 报告。

---

## 六步工作流

### Step 1 — 构建技术框架
**工具**：`web.search` → `web_fetch`

搜索方向：
- `<竞争对手> <技术> 研究方向 专利布局`
- `<competitor> <technology> patent strategy research focus`
- 行业报告、技术白皮书、学术综述

输出：3-6 个技术子方向（如：材料体系、制造工艺、系统集成、安全保护、应用场景）

---

### Step 2 — 专利检索
**工具**：`patent.search`（`mcp_patent-search__patsnap_search`）

检索策略：
1. 若用户提供检索式（`query`），直接使用
2. 若未提供，自动构建：
   ```
   keywords=[<技术关键词1>, <技术关键词2>, ...]
   filters.assignees=[<competitor>]
   filters.jurisdiction=[<market_scope>]  # 可选
   ```
3. `topk=100`，`sort_order=DESC`，`sort_field=SCORE`

统计维度：
- 各技术子方向专利数
- 各专利局/市场专利数
- 申请年份趋势

---

### Step 3 — 重点专利识别
**工具**：`patent.search`（family 筛选）

识别方法：
1. **专利家族数量**：family_size ≥ 5 的视为重点候选
2. **引用量辅助**：`cited_min=10` 筛选高被引专利
3. 取 top_n（默认 20）作为深度阅读对象
4. 标记各件专利的市场覆盖（CN/US/EP/JP/KR/WO）

---

### Step 4 — 深度阅读与技术映射
**工具**：`patent.fetch`（`mcp_patent-search__patsnap_fetch`）

读取内容：
- `claims`（权利要求书）：识别保护范围
- `abstract`（摘要）：快速定位技术方向
- `description`（说明书）：补充技术细节

映射方法：
1. 将每件专利的独立权利要求与技术框架的子方向对照
2. 判断布局类型：
   - **核心布局**：保护基础技术方案、核心工艺、基本结构
   - **外围布局**：保护应用场景、改进方案、辅助结构、材料变型

---

### Step 5 — 布局策略分析
分析维度：

| 维度 | 分析内容 |
|------|----------|
| 技术子方向 | 各方向专利数量、核心/外围比例 |
| 市场覆盖 | CN/US/EP/JP 布局强度 |
| 时间维度 | 申请年份趋势，判断技术成熟度 |
| 布局密度 | 高密度=壁垒区，低密度=白地机会 |
| 核心专利 | 基础专利保护点、首次申请年 |
| 外围专利 | 应用延伸方向、后续改进方向 |

---

### Step 6 — 生成 PDF 报告
**工具**：`scripts/generate_report.py`

1. 将所有分析结论写入 `analysis.json`（见数据模板）
2. 运行：
   ```bash
   python scripts/generate_report.py \
     --data-path analysis.json \
     --output-path competitor_patent_landscape_<company>_<tech>.pdf
   ```
3. 若 weasyprint 不可用，自动 fallback 为 HTML 文件

---

## analysis.json 数据模板

```json
{
  "competitor": "竞争对手公司名",
  "technology": "技术领域",
  "market_scope": ["CN", "US", "EP"],
  "total_patents": 85,
  "exec_summary": "执行摘要文字…",
  "tech_framework": [
    {"name": "技术子方向1", "description": "说明…"},
    {"name": "技术子方向2", "description": "说明…"}
  ],
  "market_distribution": {
    "CN": 40, "US": 25, "EP": 15, "JP": 5
  },
  "top_patents": [
    {
      "title": "专利标题",
      "publication_number": "CN1234567A",
      "family_size": 12,
      "tech_sub_area": "技术子方向1",
      "layout_type": "核心",
      "claim_summary": "独立权利要求摘要…"
    }
  ],
  "core_analysis": "核心布局分析文字…",
  "periph_analysis": "外围布局分析文字…",
  "sub_area_heatmap": [
    {"name": "技术子方向1", "count": 30, "core_count": 10, "periph_count": 20},
    {"name": "技术子方向2", "count": 15, "core_count": 5, "periph_count": 10}
  ],
  "suggestions": [
    "白地机会：XX 方向专利密度低，可重点布局",
    "规避风险：XX 核心专利保护范围宽，研发时需注意绕过"
  ],
  "sources": [
    "PatSnap 智慧芽专利数据库（检索日期：2024-xx-xx）",
    "公司官网/行业报告来源"
  ]
}
```

---

## 输出说明

| 文件 | 说明 |
|------|------|
| `competitor_patent_landscape_<company>_<tech>.pdf` | 主报告 PDF |
| `analysis.json` | 中间分析数据（可供二次处理） |

## 注意事项
- 家族数量是衡量专利重要性的首要指标
- 核心/外围判定以独立权利要求保护范围为准
- 若数据 < 10 条，报告会显示数据不足警告
- 所有结论均附有证据溯源，可追溯到具体专利公开号

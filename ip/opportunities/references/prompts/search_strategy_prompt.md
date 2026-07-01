# Search Strategy Prompt — 检索策略制定

## 任务
基于已验证的技术方向，制定完整的专利检索策略。

## 输入
- refined_topic：规范化后的技术方向
- keywords_cn：中文关键词列表
- keywords_en：英文关键词列表
- ipc_candidates：候选 IPC 分类号
- domain：技术领域

## 检索策略制定规则

### 1. 检索式构建原则
- 关键词检索：核心技术词 + 材料/器件词 + 工艺/方法词
- 布尔运算：AND 连接核心概念，OR 连接同义词
- IPC 限定：辅助限定技术范围
- 时间范围：2015 年至当前年份
- 地域范围：全球（CN+US+EP+WO+JP+KR 优先）

### 2. 检索式格式（Analytics 格式）
```
TACD:(关键词1 OR 同义词1) AND TACD:(关键词2 OR 同义词2) AND IPC:(IPC1 OR IPC2)
```

### 3. 分桶统计计划
如果 MCP 未能直接返回全量年度趋势，执行以下分桶检索：
- 年份范围：2015 至当前年份
- 每年独立检索：在检索式基础上增加 APD 年份限定
- 记录每年 total_count
- 构建年度趋势数组

### 4. 输出格式
```json
{
  "primary_query": "主检索式（Analytics格式）",
  "cn_only_query": "仅中国专利检索式",
  "global_query": "全球专利检索式",
  "keyword_groups": {
    "core_concept": ["核心概念词"],
    "material_or_component": ["材料/器件词"],
    "process_or_method": ["工艺/方法词"],
    "application": ["应用场景词"]
  },
  "ipc_codes": ["IPC1", "IPC2"],
  "time_range": {"start": "2015", "end": "当前年份"},
  "bucketing_plan": {
    "years": ["2015", "2016", "2017", "...", "当前年份"],
    "query_template": "每年分桶查询模板（含{YEAR}占位符）"
  },
  "subfield_queries": [
    {
      "subfield_name": "子技术方向名称",
      "query": "该子方向检索式",
      "description": "该子方向描述"
    }
  ],
  "search_notes": "检索策略说明"
}
```

## 检索质量要求
- 主检索式必须能覆盖该技术方向的核心专利
- 不得过于宽泛（避免召回大量不相关专利）
- 不得过于狭窄（避免遗漏重要专利）
- 建议先用宽泛检索获取总量，再用精确检索获取代表专利

## 注意事项
- 记录检索式版本和调整原因
- 如果初步检索 total_count < 100，考虑扩大检索式
- 如果初步检索 total_count > 50,000，考虑增加限定条件
- 所有检索参数都要保存到 intermediate_data.json

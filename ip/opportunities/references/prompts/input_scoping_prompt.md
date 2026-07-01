# Input Scoping Prompt — 输入范围校验

## 任务
对用户输入进行范围校验，判断是否适合生成报告，并进行规范化处理。

## 校验规则

### 1. 过于宏观的拒绝词（不得生成报告）
以下关键词若作为主题词单独出现，视为过于宏观，必须拒绝：
- 人工智能 / AI / artificial intelligence
- 新能源 / clean energy
- 半导体 / semiconductor  
- 生物医药 / biomedical / biopharma
- 电池 / battery（单独出现）
- 材料 / materials（单独出现）
- 机器人 / robotics（单独出现）
- 量子 / quantum（单独出现）
- 互联网 / internet
- 软件 / software

### 2. 适合的输入类型

**细分技术方向：**
- 必须包含"技术手段/方法"或"材料/器件/工艺"的明确限定
- 例：钠离子电池硬碳负极预钠化技术 ✅
- 例：电池负极材料 ❌（仍太宽泛）

**具体技术方案：**
- 通常以"一种..."或"用于...的..."开头
- 包含具体技术路线或解决问题的方法
- 例：一种用于锂金属电池的氟化聚合物人工 SEI 膜 ✅

### 3. 边界案例处理
- 如果输入有一定细分但不够精确，可以接受并在报告开头注明检索边界
- 如果输入是英文，直接使用，同时生成中英双语检索式

## 输出格式
```json
{
  "decision": "accept | reject | accept_with_note",
  "refined_topic": "规范化后的技术方向名称",
  "input_type": "subfield_direction | specific_solution | borderline",
  "domain": "energy | pharma | materials | electronics | chemistry | other",
  "rejection_reason": "如果 reject，说明原因",
  "clarification_suggestions": ["建议的细化方向1", "建议的细化方向2"],
  "scope_note": "如果 accept_with_note，说明检索边界",
  "keywords_cn": ["中文关键词1", "中文关键词2"],
  "keywords_en": ["English keyword 1", "English keyword 2"],
  "ipc_candidates": ["IPC1", "IPC2"],
  "subfield_candidates": ["子技术方向1", "子技术方向2", "子技术方向3", "子技术方向4"]
}
```

## 注意事项
- 对于技术方案类输入，需要推断其所属技术方向
- 关键词必须同时覆盖中文和英文，以确保全球专利检索覆盖
- subfield_candidates 是初步建议的子技术方向，后续分析时可调整

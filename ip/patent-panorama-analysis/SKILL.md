---
name: patent-panorama-analysis
description: |
  专利技术全景分析报告自动生成。用户上传专利数据Excel表格（含标题、申请人、申请日、法律状态、受理局、被引次数等字段）和技术拆解Excel表格后，自动分析专利数据并生成可编辑的HTML全景分析报告。
  报告包含5大模块：技术概况分析、重点技术分支分析、竞争对手分析、专利风险分析、企业专利布局建议。
  触发条件：当用户提及"专利分析""技术全景分析""专利全景报告""专利布局分析""CMC专利分析""专利竞争分析""专利风险""FTO分析""技术分解""专利趋势"等关键词时自动触发。也适用于用户上传专利数据Excel并要求生成分析报告的场景。
---

# 专利技术全景分析 Skill

## 工作流程

1. **读取文件**：读取用户上传的两个Excel文件（专利数据 + 技术拆解表）
2. **数据分析**：使用 `scripts/patent_analyzer.py` 进行核心统计分析
3. **数据洞察**：基于分析结果提炼技术热点、空白点、竞争格局、风险点
4. **生成HTML**：基于分析数据和UI模板，生成5模块HTML全景分析报告
5. **验证交付**：确认HTML文件正常生成，文字可编辑

## 执行步骤

### Step 1: 读取并理解数据

```
1. 用pandas读取专利数据Excel，检查列名
2. 用pandas读取技术拆解Excel，理解技术分支结构
3. 调用scripts/patent_analyzer.py进行核心分析，或内联执行分析逻辑
```

### Step 2: 数据分析（参照 references/data_analysis_guide.md）

分析维度清单（必须全部执行）：

| # | 分析项 | 方法 |
|---|-------|------|
| 1 | 申请年趋势 | 按申请年分组计数 |
| 2 | 法律状态分布 | 简化状态后统计 |
| 3 | 受理局/地域分布 | 按受理局分组，中美欧对比 |
| 4 | 技术构成分布 | 关键词匹配分类后统计 |
| 5 | 申请人排名 | 清理名称后统计Top15 |
| 6 | 技术分支趋势 | 按年×分支二维统计 |
| 7 | 增长率计算 | 2020→2024增长百分比 |
| 8 | 申请人技术布局 | 每个申请人各分支专利数 |
| 9 | 高被引专利 | 按被引用次数排序Top10 |
| 10 | 多同族专利 | 同族国家数>=3的专利 |

### Step 3: 洞察提炼

基于分析结果自动生成以下洞察（融入HTML文案中）：

- **技术热点**：增长率>100%且专利基数>50的分支
- **技术空白点**：专利总量<50件或增长率<0的分支
- **竞争格局**：三梯队划分（国际龙头/国内主力/高校机构）
- **核心风险领域**：专利密度>100件且国际巨头集中布局的领域
- **布局建议**：基于差距分析和竞争对手对标

### Step 4: HTML报告生成（参照 references/ui_style_guide.md）

报告必须包含5个模块，每个模块有固定结构。参照 `references/ui_style_guide.md` 的配色和布局规范。

所有文字内容必须添加 `contenteditable="true"` 属性，使用对应的hover/focus样式。

图表使用ECharts（通过CDN引入），至少包含8个图表：
1. 申请趋势折线图
2. 法律状态饼图
3. 地域分布柱状图
4. 技术构成饼图
5. 申请人排名柱状图
6. 技术分支趋势多折线图
7. 竞争对手雷达图
8. 技术吸引力散点矩阵图

#### ⚠️ ECharts三大强制规范（违反任意一条会导致所有图表不渲染）

**规范1 — CDN加载时序（必须使用双保险写法）**

禁止使用 `window.addEventListener('load', initCharts)`，因为CDN脚本可能在load事件后才执行。

必须使用以下标准模板：
```html
<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
<script>
function initCharts() {
    // 在此初始化所有图表
}
function tryInit() {
    if (typeof echarts !== 'undefined') {
        initCharts();
    } else {
        document.querySelector('script[src*="echarts"]')
            .addEventListener('load', initCharts);
    }
}
document.addEventListener('DOMContentLoaded', tryInit);
</script>
```

**规范2 — JS字符串内禁止裸换行（饼图label formatter高危区）**

`<script>` 块内所有字符串必须在同一行或用 `+` 拼接，换行必须用 `\n` 转义序列。

❌ 错误写法（真实换行符会破坏整个script块解析，导致所有图表白屏）：
```js
label: { formatter: '{b}
{d}%' }
```

✅ 正确写法：
```js
label: { formatter: '{b}\n{d}%' }
```

**规范3 — markLine/markArea必须嵌套在series内**

`markLine` 和 `markArea` 是 series 的子属性，不能写在 `option` 根级。

❌ 错误写法：
```js
option = {
    series: [...],
    markLine: { ... }   // 根级无效，且会引发解析错误
};
```

✅ 正确写法：
```js
option = {
    series: [{
        type: 'scatter',
        data: [...],
        markLine: { ... }   // 必须在series元素内
    }]
};
```

### Step 5: HTML自检清单（生成后逐项确认）

在输出HTML之前，必须逐条核查以下项目：

- [ ] ECharts CDN `<script>` 标签存在且使用 `tryInit` 双保险初始化
- [ ] `<script>` 块内无裸换行字符串（重点检查所有 `formatter`、`label`、`tooltip` 字段）
- [ ] 所有 `markLine` / `markArea` 均在 `series[]` 元素内，不在 `option` 根级
- [ ] 每个图表容器 `<div>` 有明确的像素高度（不能仅靠CSS类，须有 `style="height:360px"`）
- [ ] 所有图表容器 `id` 唯一，且 `initCharts` 函数中 `echarts.init(document.getElementById('xxx'))` 的id与之匹配
- [ ] 所有文字节点添加了 `contenteditable="true"` 属性

## 技术分支关键词

见 `references/report_structure.md` 中的 `TECH_KEYWORDS` 映射表。根据用户技术领域可调整关键词。

## 申请人名称清理

见 `scripts/patent_analyzer.py` 中的 `clean_applicant` 函数。根据实际数据中出现的申请人名称动态调整匹配规则。

## 报告结构详情

见 `references/report_structure.md` 了解5大模块的完整分析维度。

## 数据列名映射

专利数据Excel的列名可能有多种变体，标准映射关系见 `references/report_structure.md` 的列名映射表。

## 注意事项

1. 专利数据Excel和技术拆解Excel都是可选输入。如果只提供专利数据，技术分解表模块省略
2. 标题列必须存在，技术分类依赖标题关键词匹配
3. HTML报告中的文案应根据实际分析结果动态生成，不要硬编码固定数字
4. contenteditable属性必须添加到所有用户可能需要修改的文字元素上
5. 图表数据应动态注入，不要写死示例数据
6. **生成HTML后必须执行Step 5自检清单，所有项目通过后再交付**
7. **ECharts三大规范（Step 4中）是硬性约束，每次生成HTML都必须严格遵守**

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。

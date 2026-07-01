# UI风格指南

## 设计原则

报告UI参考智慧芽PatSnap TGI技术情报平台风格，核心特点：
- 现代科技感配色（深蓝/青色渐变为主）
- 数据驱动的信息可视化
- 浮动卡片式布局
- 清晰的信息层级
- contenteditable支持（所有文字可修改）

## 配色方案

### 主色调
- 深色渐变：`#0C4A6E → #0E7490 → #0891B2 → #06B6D4`（Hero、模块标题）
- 模块01：`#0C4A6E → #155E75`
- 模块02：`#1E3A5F → #2D5A87`
- 模块03：`#0E7490 → #0891B2`
- 模块04：`#1E293B → #334155`
- 模块05：`#0F766E → #14B8A6`

### 强调色
- 数据高亮：`#F59E0B`（琥珀色，关键数字）
- 热点标签：`#0E7490` 背景 + 文字
- 风险警示：`#DC2626` 红色系
- 空白点：`#F59E0B` 琥珀色系

### 图表色板（ECharts）
```javascript
const chartColors = ['#0891B2', '#0E7490', '#06B6D4', '#22D3EE', '#67E8F9', '#164E63', '#155E75', '#207A8B', '#2D95A8', '#3BB0C5', '#4CCBDE', '#6DE0F0', '#9EEBF8', '#CFF4FC', '#A5F3FC', '#7DD3FC'];
```

## 布局结构

### Hero区域
- 渐变背景 + 科技感SVG装饰
- 左侧：标题 + 副标题 + 导航胶囊
- 右侧：关键数据玻璃卡片（4宫格）
- 导航胶囊链接到5个模块

### 模块区域
每个模块包含：
1. 模块标题栏（编号 + 标题 + 英文副标题）
2. 核心指标卡片行（2-5列）
3. 图表行（1-2列）
4. 分析卡片/表格
5. 时间线/深度分析

### 卡片样式
```css
.module-card {
    background: rgba(255,255,255,0.95);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}
.float-card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.float-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 20px 40px rgba(8, 145, 178, 0.15);
}
```

## contenteditable实现

所有文字内容必须支持浏览器中直接编辑：
```html
<h2 contenteditable="true">标题文字</h2>
<p contenteditable="true">分析文字</p>
<div contenteditable="true">
  <div>热点内容</div>
</div>
```

CSS样式：
```css
[contenteditable="true"] {
    border: 1px dashed transparent;
    border-radius: 4px;
    padding: 2px 4px;
    transition: all 0.2s;
}
[contenteditable="true"]:hover {
    border-color: #94A3B8;
    background: rgba(148, 163, 184, 0.05);
}
[contenteditable="true"]:focus {
    border-color: #0E7490;
    background: rgba(14, 116, 144, 0.05);
    outline: none;
}
```

## ECharts图表要求

| 图表 | 用途 | 最小高度 |
|-----|------|---------|
| 折线图 | 申请趋势、技术分支趋势 | 360px |
| 饼图/环形图 | 法律状态、技术构成 | 360px |
| 柱状图 | 地域分布、申请人排名 | 360px |
| 雷达图 | 竞争对手技术对比 | 400px |
| 散点图 | 技术吸引力矩阵 | 400px |

> 图表容器必须在 HTML 标签上显式声明像素高度，例如：
> `<div id="chart1" style="height:360px;"></div>`
> 不能仅依赖 CSS class 设置高度，否则 ECharts 初始化时可能读取到 0px 而渲染失败。

---

## ⚠️ ECharts 致命 Bug 防范（每次生成HTML必读）

以下三类错误会导致**页面所有图表全部白屏**，每次生成 HTML 时必须主动排查。

### Bug A — CDN 加载时序竞争

**根因**：`window.addEventListener('load', initCharts)` 存在竞争条件：CDN `<script>` 可能在 `load` 事件触发后才完成加载，此时 `echarts` 变量未定义，`initCharts` 调用即崩溃。

**标准修复模板**（必须照此写法）：

```html
<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
<script>
function initCharts() {
    // 逐一初始化每个图表
    var chart1 = echarts.init(document.getElementById('chart1'));
    chart1.setOption({ /* ... */ });
    // ... 其余图表

    // 统一注册 resize
    window.addEventListener('resize', function() {
        [chart1 /*, chart2, ... */].forEach(function(c){ c.resize(); });
    });
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

### Bug B — `<script>` 块内字符串裸换行

**根因**：JavaScript 字符串字面量不允许包含真实换行符（ASCII 0x0A）。若生成代码时误将模板中的换行直接输出到字符串内，整个 `<script>` 块解析失败，所有图表均不渲染。**饼图 `label.formatter`、`tooltip.formatter` 是高发区。**

❌ 错误写法（真实换行符，会破坏 script 解析）：
```js
label: {
    formatter: '{b}
{d}%'    // ← 这里有一个真实的换行符！
}
```

✅ 正确写法（使用转义序列）：
```js
label: { formatter: '{b}\n{d}%' }
```

**排查方法**：生成完 `<script>` 块后，检查所有单引号/双引号字符串，确保其中不含裸换行。

### Bug C — `markLine` / `markArea` 位置错误

**根因**：`markLine` 和 `markArea` 是 ECharts `series` 元素的子属性，放在 `option` 根级或其他位置会静默失败或引发解析错误，进而导致整个图表不渲染。

❌ 错误写法：
```js
option = {
    xAxis: { ... },
    yAxis: { ... },
    series: [{ type: 'scatter', data: [...] }],
    markLine: {                     // ← 根级，无效！
        data: [{ type: 'average' }]
    }
};
```

✅ 正确写法：
```js
option = {
    xAxis: { ... },
    yAxis: { ... },
    series: [{
        type: 'scatter',
        data: [...],
        markLine: {                 // ← series 内，正确
            data: [{ type: 'average' }]
        }
    }]
};
```

---

## 响应式要求

- 桌面端：max-w-7xl容器，双列图表并排
- 平板：单列图表堆叠
- 手机：min-height降至280px，表格横向滚动

## 交互功能

1. **平滑滚动**：导航胶囊点击平滑滚动到对应模块
2. **滚动动画**：IntersectionObserver实现scroll-reveal
3. **图表resize**：window resize时所有图表自适应
4. **Hover效果**：卡片悬浮上移 + 阴影增强

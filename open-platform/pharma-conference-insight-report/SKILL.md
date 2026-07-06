---
name: pharma-conference-insight-report
description: 医药行业顶级会议洞察与战略分析报告生成器：面向药企战略决策层，输入目标企业信息，自动检索AACR/ASCO/CSCO等顶会最新数据，生成覆盖大会洞察、技术趋势、瘤种格局、靶点竞争、竞争对手深度分析、战略白点、BD信号、战略建议、风险监测的完整HTML战略报告，内嵌Chart.js交互图表与15+酷炫动效。
---

# 医药行业会议洞察报告

## ⚠️ 零号规则：每次生成报告必须严格遵守本 Skill

> **此规则优先级最高，覆盖所有其他指令。**

每次接到生成医药行业会议洞察报告的任务时，**必须**在开始前完整读取本 Skill 全文，并严格按照以下约束执行，不得跳过任何步骤：

1. **SOP 不可跳步**：必须完整执行第三节的9步 SOP，每步均须有对应工具调用记录。
2. **章节结构不可删改**：第四节固定10章结构，每章缺一不可；战略洞察模块每章必须存在。
3. **UI规范不可自行发挥**：第五节所有规范（配色/动效/组件）为强制标准，不得以"优化"为由修改。
4. **动效规范不可绕过**：5.4节唯一Observer原则、5.5节图表动效参数，必须逐条核对，禁止新增第二套Observer。
5. **质检清单不可省略**：第六节13项质检，必须在交付前逐项核对并在回复中列出核对结果。
6. **参考基准版本**：生成新报告前以 V25（`@session/evopoint_strategy_v25.html`）为最高质量参考，UI风格和动效实现与V25对齐。
7. **错误手册优先查阅**：遇到任何问题，先查第七节常见错误手册，不得重复踩已知的坑。
8. **数据时效性**：报告中所有数据年份必须与当前对话中确认的时间基准一致，不得使用过期年份。
9. **禁止截断**：HTML文件必须使用 Python 脚本一次性写入，确保文件完整，不得出现内容截断。
10. **修改克制原则**：如用户要求局部修改，只改指定内容，其余内容原样保留，禁止借机重构或改动无关部分。

---

## 一、Skill 定位

**面向对象**：药企战略部门、管理层、投资决策者  
**核心输出**：基于近两年（当前年-1 ~ 当前年）AACR / ASCO / CSCO 三大顶会数据，结合目标企业管线现状，生成具有战略决策高度的 HTML 格式深度洞察报告。  
**典型触发词**：医药大会洞察报告、AACR/ASCO/CSCO分析、药企竞争情报报告、管线战略分析、肿瘤学会议洞察

---

## 二、输入参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `company_name` | ✅ | 目标企业名称（中英文均可） |
| `company_url` | 推荐 | 企业官网URL，用于自动抓取管线信息 |
| `focus_areas` | 可选 | 重点关注领域（如ADC、双抗、分子胶等），不填则自动识别 |
| `competitors` | 可选 | 指定竞争对手列表，不填则自动识别6家 |
| `time_range` | 可选 | 分析时间范围，默认为当前年-1至当前年 |
| `output_path` | 可选 | 输出文件路径，默认 `@session/{company}_report.html` |

---

## 三、标准执行 SOP（9步）

### Step 1 — 企业画像采集
- 抓取 `company_url` 官网内容
- 搜索企业近两年新闻、BD交易、管线进展
- 提取：核心技术平台、在研管线列表（IND/I/II/III期）、已达成BD交易、核心靶点

### Step 2 — 三大顶会数据检索
并行检索以下内容（时间范围：当前年-1 ~ 当前年）：
- `AACR {year} 重大研究成果 ADC 双抗 分子胶 最新进展`
- `ASCO {year} 重磅数据 肿瘤治疗突破 中国创新药`
- `CSCO {year} 年会 ADC 靶向治疗 中国数据`
- `{company} {year} AACR ASCO CSCO 数据披露`

### Step 3 — 技术趋势与竞争格局检索
- ADC下一代技术（双载荷/双抗ADC/非细胞毒性载荷）
- 分子胶/PROTAC/RLT技术成熟度
- 热门靶点梯队（HER2/TROP2/CLDN18.2/DLL3等）竞争格局
- 中国出海BD交易金额趋势

### Step 4 — 竞争对手深度检索（≥6家）
对每家竞争对手检索：
- 近两年ASCO/AACR/CSCO数据披露
- 管线与目标企业的重叠度
- BD交易与融资动态
- 威胁等级评估（极高🔴/高🔴/中🟠/低🟡）

### Step 5 — 数据整理与三要素提取
调用 `novelty_summary` 或 `llm_call` 提取：
- **技术问题**：当前赛道未满足的临床需求
- **技术方案**：顶会数据验证的解决路径
- **技术效果**：关键临床终点（ORR/PFS/OS数据）

### Step 6 — 专利竞争格局（可选，PatSnap MCP）
当需要深度技术壁垒分析时：
- 申请人排名分析
- 专利趋势
- 技术旭日图

### Step 7 — 战略洞察生成
为每个模块生成「目标企业战略洞察」：
- 影响分析（正面/负面）
- 可执行行动建议（含时间节点）
- 紧迫度/机会/风险标签

### Step 8 — HTML报告生成
使用 Python 脚本写入完整 HTML（规避 append 限制）：
- 文件大小通常 80-120KB
- 必须用 Python 脚本一次性写入，规避单次 append 限制

### Step 9 — 质检与交付
- 检查章节完整性（10章全部存在）
- 检查图表初始化代码（Chart.js 使用 `delay` 函数，非 `onProgress`）
- 检查导航栏章节数量与正文一致
- 检查返回顶端按钮在 `</body>` 之前
- 检查结尾声明区块在最后
- **检查数字滚动计数只有单套Observer（见第五节5.4）**

---

## 四、报告章节结构（固定10章）

```
封面（Hero）
├── 执行摘要          — 4张3D翻转卡 + 雷达图对比
├── Chapter 01：三大顶会深度洞察   — AACR/ASCO/CSCO分会场分析
├── Chapter 02：六大技术趋势演进   — 成熟度/竞争强度/企业协同雷达
├── Chapter 03：核心瘤种竞争格局   — 热度横排图 + 瘤种深度卡片
├── Chapter 04：靶点平台竞争情报   — 四维雷达 + TRL成熟度 + 竞争矩阵
├── Chapter 05：竞争对手深度分析   — ≥6家 + 威胁等级 + 管线堆叠图
├── Chapter 06：战略白点与未满足需求 — TOP6清单（必须6条）+ 机会气泡矩阵
├── Chapter 07：BD信号与资本动向   — 出海趋势双轴图 + 重大交易时间线
├── Chapter 08：战略行动建议       — Ansoff矩阵 + 优先级评分 + 分级建议
├── Chapter 09：风险监测与预警     — 6大风险看板 + 全年监测时间轴
└── Chapter 10：来源附录           — 可信度评级 + 数据索引 + 免责声明
结尾声明区块（页脚）
```

---

## 五、UI设计规范（必须遵守）

### 5.1 配色体系
```css
--bg: #020b18          /* 主背景深蓝黑 */
--blue: #2563eb        /* 主色蓝 */
--cyan: #06b6d4        /* 强调青 */
--purple: #a855f7      /* 强调紫 */
--green: #10b981       /* 正面绿 */
--red: #ef4444         /* 风险红 */
--text: #e2e8f0        /* 正文白 */
--dim: #94a3b8         /* 辅助灰 */
```

### 5.2 必须包含的15项动效

| 类别 | 动效 | 实现方式 |
|------|------|---------|
| 全局 | 粒子星尘系统 | Canvas 2D + RAF，180粒子，自动连线 |
| 全局 | 光束扫描 | 页面加载时CSS `beamSweep` 动画 |
| 全局 | 顶部进度条 | scroll事件驱动宽度变化 |
| 全局 | 鼠标跟随辉光 | mousemove + 青色径向渐变 |
| 封面 | 5层旋转环 | CSS animation，各层速度/方向各异 |
| 封面 | 中央脉冲核心点 | `corePulse` keyframe，scale+光晕扩散 |
| 封面 | 打字机双行 | JS逐字符，行间停顿350ms，两行字号一致 `clamp(2.8rem,5vw,3.8rem)`，`letter-spacing:0.06em` |
| 封面 | 数字滚动计数 | rAF + easeOutCubic，IntersectionObserver触发（见5.4节） |
| 卡片 | 3D翻转 | CSS perspective + rotateY(180deg) hover |
| 卡片 | 边框流光扫描 | `::after` + `translateX` 扫光 |
| 卡片 | 磁吸Tilt3D | mousemove X/Y轴10°倾斜 |
| 时间线 | 脉冲涟漪 | 双层 `ripple` keyframe |
| 导航 | Ripple波纹 | click事件，scale(4)后消失 |
| 滚动 | Section飞入 | IntersectionObserver + `fadeUp` |
| 滚动 | 视差效果 | scroll + translateY背景层独立速率 |

### 5.3 固定UI组件

**顶部导航**（sticky）：
- 左侧：企业名 + 报告标题
- 右侧：所有章节快速跳转链接（数量必须与正文章节一致）
- 顶部：滚动进度条

**封面 Hero**：
- 全屏 `min-height: 100vh`
- 5层旋转同心环居中
- 中央脉冲核心点
- 双行打字机标题（两行字号完全一致，JS中不得硬编码不同字号）
- 副标题（圆点分隔信息层级）
- 4个KPI卡片横排（图标+数字+说明）

**返回顶端按钮**（必须在 `</body>` 之前插入）：
- `position:fixed !important; bottom:2.5rem; right:2.5rem; z-index:99999 !important`
- 滚动超过400px才显示（`.btt-show` 类控制，`opacity:0; pointer-events:none` 初始态）
- 青色呼吸光晕 + hover紫色外晕

**结尾声明区块**（在第10章之后，`</body>` 之前）：
- 机密标签 + 机构名称 + 日期
- 数据来源标签组
- 免责声明框
- 版本号页脚

### 5.4 数字滚动计数引擎规范（V25标准，⚠️ 严格遵守）

#### 唯一Observer原则
**全报告只能有一套数字滚动Observer**，严禁新增第二套与原有套并存。  
两套Observer并存会导致互相抢占 `data-animated` 标记，竞争对手数字全部失效。

#### HTML结构（竞争对手数字）
```html
<!-- 纯整数 -->
<div class="comp-stat-val" data-target="15">0</div>

<!-- 带后缀 -->
<div class="comp-stat-val" data-target="50" data-suffix="亿+">0</div>

<!-- 带前缀+后缀（初始值必须是"-"，不能是"0"） -->
<div class="comp-stat-val" data-prefix="$" data-target="84" data-suffix="亿">-</div>

<!-- 小数 -->
<div class="comp-stat-val" data-prefix="$" data-target="11.5" data-suffix="亿">-</div>
```

#### JS animateCount 函数规范
```js
function animateCount(el) {
  const target = parseFloat(el.dataset.target);
  const suffix = el.dataset.suffix || '';
  const prefix = el.dataset.prefix || '';
  const isDecimal = !Number.isInteger(target);
  const duration = el.classList.contains('kpi-val') ? 2800 : 2200;
  const start = performance.now();
  function easeOutCubic(t) { return 1 - Math.pow(1 - t, 3); }
  function tick(now) {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const val = target * easeOutCubic(progress);
    el.textContent = prefix + (isDecimal ? val.toFixed(1) : Math.floor(val)) + suffix;
    if (progress < 1) requestAnimationFrame(tick);
    else el.textContent = prefix + (isDecimal ? target.toFixed(1) : target) + suffix;
  }
  requestAnimationFrame(tick);
}
```

#### Observer选择器（必须同时覆盖KPI和竞对）
```js
// ✅ 正确：单套Observer，选择器同时覆盖两类元素
e.target.querySelectorAll('[data-target]').forEach(el => {
  if (!el.dataset.animated) { el.dataset.animated = '1'; animateCount(el); }
});
// ❌ 错误：新增第二套Observer单独处理 .comp-stat-val
```

### 5.5 图表动效参数规范（V25标准值）

> 基准：以V21为基础，仅对下列5类图表动效做精准延长，其余动效参数不改。

| 图表类型 | duration | delay/元素 | easing |
|---------|----------|-----------|--------|
| **柱状图** | **2800ms** | **160ms/列** | `easeOutBounce` |
| **折线图** | **3000ms** | **130ms/点** | `easeInOutCubic` |
| **雷达图（技术趋势/靶点）** | **2800ms** | **200ms/维** | `easeOutElastic` |
| **雷达图（竞争对手）** | **1400ms** | **80ms/维** | `easeOutElastic` |
| **气泡图（机会矩阵）** | **3200ms** | **280ms/泡** | `easeOutExpo` |
| **气泡图（战略白点）** | **1600ms** | **100ms/泡** | `easeOutExpo` |
| 进度条 transition | **3s** | — | ease |

> ⚠️ 竞争对手雷达图和战略白点气泡图使用较短时长，避免出现时间过长用户等待问题。

#### Chart.js 动效注入方式（V21正确写法，必须遵守）
```js
// ✅ 使用 delay 函数（Chart.js 4.x 正确写法）
cfg.options.animation = {
  delay: function(ctx) { return ctx.dataIndex * 160; },
  easing: 'easeOutBounce',
  duration: 2800
};
// ✅ 用 Object.assign 合并 tooltip，不覆盖
cfg.options.plugins.tooltip = Object.assign({...defaultTooltip}, cfg.options.plugins.tooltip || {});
// ✅ IntersectionObserver 延迟初始化（进入视口12%才 new Chart()）
const io = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) { doInit(); io.unobserve(canvas); }
  });
}, { threshold: 0.12 });
io.observe(canvas);
// ❌ 禁止使用 onProgress 回调（Chart.js 4.x 已废弃）
```

### 5.6 图表规范（Chart.js）
必须包含（≥9个图表）：
1. 执行摘要雷达图（目标企业 vs 主要竞争对手）
2. ADC/目标市场规模柱图（历史+预测）
3. 三大顶会议题热度趋势折线图
4. 瘤种竞争热度横排图
5. 靶点四维雷达图
6. 技术成熟度TRL图
7. 竞争对手管线堆叠柱图
8. BD出海趋势双轴折线图
9. 管线优先级评分图
10. 机会气泡矩阵（可选）

---

## 六、质检清单（交付前必须逐项核对并在回复中列出结果）

- [ ] 章节数量：正文10章全部存在
- [ ] 导航栏：链接数量 = 章节数量（含执行摘要+10章）
- [ ] 战略白点：未满足需求清单必须有6条（不能只有3条）
- [ ] 竞争对手：至少6家，每家有威胁等级标注
- [ ] 竞争对手数字：所有 `comp-stat-val` 有 `data-target` 属性，带前缀的初始值为 `"-"`
- [ ] 每章末尾：有「目标企业战略洞察」模块
- [ ] 图表：Chart.js 使用 `delay` 函数，非 `onProgress`，IntersectionObserver延迟初始化
- [ ] 数字滚动：全报告只有一套Observer，选择器覆盖 `[data-target]`
- [ ] Ansoff矩阵：四象限内容饱满，无大面积空白
- [ ] 返回顶端按钮：在 `</body>` 之前，有 `!important` fixed定位和 `.btt-show` 逻辑
- [ ] 结尾声明：在最后，包含机密标签+免责声明+版本号
- [ ] 时间基准：报告内所有数据年份与当前时间一致
- [ ] 数据来源：关键结论标注 [S#] 可溯源标记

---

## 七、常见错误与修复方法

| 错误 | 根因 | 修复 |
|------|------|------|
| **竞争对手数字不滚动** | 两套Observer并存互相抢占 `data-animated` | 删除后加的第二套，升级原有 `animateCount` 函数支持前缀/后缀/小数 |
| **带前缀数字显示异常** | 初始值写 `"0"` 而非 `"-"` | 所有 `data-prefix` 元素初始值改为 `"-"` |
| 图表动效无效 | 使用了废弃的 `onProgress` 回调 | 改用 Chart.js 4.x 的 `delay` 函数方式 |
| 图表options被覆盖 | 调用处options对象整体赋值覆盖注入值 | 改用 `Object.assign` 合并 |
| 返回顶端按钮不显示 | 插入在 `</html>` 之后 | 重建，插入在 `</body>` 之前，加 `!important` |
| 战略白点只有3条 | 内容截断 | 补充#4/#5/#6三条，保持样式一致 |
| 章节在导航栏消失 | 新增章节时未更新导航HTML | 同步更新 `<nav>` 中的 `<a>` 标签 |
| 图表空白canvas | Chart.js初始化在DOM ready之前 | 用IntersectionObserver延迟到进入视口才 `new Chart()` |
| 数据年份错误 | 未同步当前时间 | 以对话中确认的当前日期为准 |
| Ansoff矩阵空白 | 固定aspect-ratio压缩内容 | 去掉固定比例，改flex自适应 |
| 某章内容丢失 | HTML文件被截断 | 用Python脚本写入完整内容，规避append限制 |
| 字号不一致 | JS打字机硬编码多处字号 | 全局搜索所有 `fontSize` 赋值，统一为 `clamp(2.8rem,5vw,3.8rem)` |

---

## 八、输出规格

- **格式**：单文件自包含 HTML（无外部依赖，Chart.js CDN除外）
- **大小**：80–130KB
- **兼容性**：Chrome/Edge/Safari最新版
- **路径**：`@session/{company_name}_strategy_report.html`
- **版本命名**：文件名含版本号，页脚含版本标记
- **基准版本**：信诺维医药报告 **V25** 为当前最高质量参考版本（`@session/evopoint_strategy_v25.html`）

---

## 九、调用示例

**最简调用**：
> 请为「XX医药」生成一份医药行业会议洞察战略分析报告，官网是 https://xxx.com

**完整调用**：
> 为「XX医药」生成AACR/ASCO/CSCO洞察报告，重点关注ADC和双抗方向，对标竞争对手包括科伦博泰、第一三共、恒瑞，输出HTML报告

---

## 十、参考案例

本 Skill 基于「信诺维医药（EvoPoint Biosciences）」完整报告迭代（V1→V25）提炼，经历：
- 25轮HTML迭代修复
- UI设计从基础版→北京车展风格对齐→15项动效注入
- 内容从5章扩展至10章
- 时间基准从2024调整至2025-2026
- 竞争对手从3家扩展至6家
- 每章增加目标企业战略洞察模块
- 图表动效从无效→V21根本性修复（delay函数+IntersectionObserver）→V25参数精准校准
- 数字滚动计数从单一KPI扩展至竞争对手卡片全覆盖
- **最终交付版本：V25**（`@session/evopoint_strategy_v25.html`）

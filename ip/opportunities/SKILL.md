---
name: opportunities
description: |
  技术方向专利机会评估与报告生成 Skill。输入细分技术方向或具体技术方案，自动调用智慧芽专利检索、趋势分析、子技术方向统计等 MCP 工具，生成含交互式 ECharts 图表的多页面 HTML 报告、JSON 中间数据和 CSV 证据链，最终给出研发/投资机会评分与明确建议。本 Skill 不使用 Python，所有文件通过 MCP 和文件写入能力生成。
---

# opportunities — 技术方向专利机会评估 Skill

## 一、触发规则

当用户的消息中出现以下意图时，激活本 Skill：
- "分析 X 的专利机会"
- "评估 X 是否值得研发/投资"
- "X 技术方向专利态势"
- "X 的专利趋势分析"
- "研究 X 的专利布局"
- "X 方向值得做吗"
- 任何包含细分技术方向或技术方案名称的技术机会评估请求

## 二、重要约束（严格遵守）

### ❌ 绝对禁止
1. **禁止编写或运行任何 Python 脚本**
2. **禁止生成任何 .py 文件**
3. **禁止在 scripts/ 目录创建任何文件**
4. **禁止将 TopK50 专利样本用于趋势统计、地域分析、排名或法律状态分析**
5. **禁止基于 TopK50 推断全局趋势**
6. **禁止编造专利数据**
7. **禁止声称已完成但实际缺少输出文件**
8. **禁止生成申请人排名图、地域分布图、法律状态分布图** — 当前工具不具备全量聚合接口，生成此类图表必然基于 TopK50 样本，属于误导性数据，一律不得生成

### ✅ 必须遵守
1. 所有图表数据必须来自 full_scope_metrics（全量统计）
2. TopK50 仅用于代表专利展示和证据链
3. 趋势图必须基于全量年度统计或分桶检索（逐年 matched_total）
4. 子技术方向数量图必须基于每个子方向独立检索的 matched_total
5. 每个重要结论必须有 claim_id 和可追溯数据来源
6. 生成 10 个规定文件，不得缺少
7. 所有 HTML 必须有 `<meta charset="UTF-8">`
8. 图表必须有真实数据，不得有空图表或占位符

## 三、输入范围校验

### 接受的输入
- 细分技术方向（包含技术手段/材料/工艺的明确限定）
- 具体技术方案（通常以"一种..."开头）

### 拒绝的输入（要求细化）
过于宏观的词汇单独出现时：人工智能、新能源、半导体、生物医药、电池（单独）、材料（单独）、量子（单独）

## 四、工作流程（共 8 个阶段）

### Phase 0：输入规范化
- 提取技术方向名称、关键词（中英文）、IPC候选、初步子技术方向
- 构建扩展检索式，必须包含中英文同义词、近义词
- 不得仅用单一关键词检索

### Phase 1：全量统计数据采集（full_scope_metrics）
- **年度申请趋势**：执行分桶检索（2015年逐年至当前年份），每年单独获取 matched_total
- **中国年度趋势**：同上，加 jurisdiction=CN 过滤
- **子技术方向统计**：每个子方向单独检索，用各自的 matched_total
- ⚠️ **申请人排名、地域分布、法律状态分布**：当前工具不具备全量聚合接口，**一律不采集、不生成对应图表**，在 methodology.html 中明确说明原因

### Phase 2：代表专利样本采集（evidence_sample）
- 使用 patsnap_search 获取相关性排序 TopK50
- 此样本仅用于展示，不用于任何统计图表

### Phase 3：深度分析
- 生成六维评分（详见评分体系）
- 生成证据链（每条结论绑定 claim_id 和数据来源）
- 分析技术空白点
- 生成明确的研发投资结论：是否值得进入、主要机会、主要风险、下一步建议

### Phase 4：生成 evidence_mapping.csv
- 格式：claim_id, claim_text, data_source, data_value, supporting_patents, evidence_strength, reasoning, limitations
- 至少 10 条

### Phase 5：生成 5 个 HTML 文件
严格按照前端设计规范（第七节）生成，**每生成一个文件必须等待工具回执确认后，再生成下一个文件，不得在同一步骤中描述多个文件的生成计划**，生成顺序：
1. index.html（最大最复杂，必须包含第八节所有15个内容区块）→ 等待确认
2. patents.html → 等待确认
3. evidence.html → 等待确认
4. subfields.html → 等待确认
5. methodology.html → 等待确认

### Phase 6：生成辅助文件
- README.md → 等待确认
- quality_check.md → 等待确认

### Phase 7：质量核查
- 验证 10 个文件全部存在
- 验证趋势数据来源是否为逐年分桶检索的 matched_total
- 验证 HTML 无占位符无空图表
- 验证 index.html 正文字数 ≥ 3000 字
- 验证综合结论区块存在且 ≥ 400 字
- 验证不存在申请人排名图、地域分布图、法律状态分布图
- 如有问题，立即修复

## 五、数据统计规则（核心守则）

### ✅ full_scope_metrics（全量统计）用于：
- 年度申请趋势图（分桶检索逐年 matched_total）
- 中国年度申请趋势图
- 全球 vs 中国趋势对比图
- 子技术分支规模对比图（各子方向独立检索 matched_total）
- 所有统计数字（总量、CAGR、近五年增速等）

### ✅ evidence_sample（代表样本）用于：
- patents.html 专利列表
- Top 10 代表专利展示（明确标注"代表样本，非申请量排名"）
- 证据链绑定专利

### ❌ 以下图表永久禁止生成：
- 申请人排名图（无全量聚合接口）
- 地域分布图（无全量聚合接口）
- 法律状态分布图（无全量聚合接口）
- 授权率统计图（无全量聚合接口）

## 六、输出文件规范（必须全部生成）

| 文件 | 必须 | 最低要求 |
|------|------|----------|
| index.html | ✅ | ≥6张图表，≥3000字正文，含15个内容区块，每条结论带claim_id和数据来源 |
| patents.html | ✅ | ≥50条代表专利（或实际全部），含搜索，明确标注"代表样本" |
| evidence.html | ✅ | ≥10条证据链 |
| subfields.html | ✅ | 4-8个子技术方向 |
| methodology.html | ✅ | 检索式、统计口径、禁止图表说明 |
| intermediate_data.json | ✅ | 包含所有规定字段 |
| patent_list.csv | ✅ | 含表头，≥20行 |
| evidence_mapping.csv | ✅ | 含表头，≥10行 |
| README.md | ✅ | 文件清单和数据说明 |
| quality_check.md | ✅ | 10项核查结果 |

## 七、前端设计规范（强制执行，不得偏离）

### 7.1 设计主题
**深色科技主题**，完全复刻以下规范，不得使用浅色背景或普通网页风格。

### 7.2 CSS 变量（必须在每个 HTML 的 :root 中完整声明）
```css
:root {
  --bg-base: #070b14;
  --bg-surface: #0d1525;
  --bg-card: #111c33;
  --bg-elevated: #162040;
  --color-primary: #3b82f6;
  --color-accent: #06d6a0;
  --color-warning: #f59e0b;
  --color-danger: #ef4444;
  --color-purple: #8b5cf6;
  --text-primary: #f1f5f9;
  --text-secondary: #94a3b8;
  --text-muted: #475569;
  --border-subtle: rgba(59,130,246,0.15);
  --glow-blue: 0 0 20px rgba(59,130,246,0.3);
  --glow-accent: 0 0 20px rgba(6,214,160,0.3);
  --radius-card: 16px;
  --radius-sm: 8px;
  --font-title: 'Sora', sans-serif;
  --font-body: 'Inter', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}
```

### 7.3 字体（必须引入）
```html
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```
- 标题/数字：Sora
- 正文：Inter
- 专利号/代码：JetBrains Mono

### 7.4 图表库
```html
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
```
- **必须使用 ECharts 5.4.3**
- **禁止使用 Chart.js、Plotly 或静态图片**
- 所有图表必须有 tooltip（鼠标悬浮显示数据值）
- 图表配色使用 CSS 变量中的颜色体系

### 7.5 导航栏
- 毛玻璃效果：`backdrop-filter: blur(16px)`
- 固定在顶部，`background: rgba(7,11,20,0.85)`
- 品牌名用 `var(--color-accent)` 颜色
- 链接 hover 变 `var(--color-primary)`

### 7.6 Hero 区域（仅 index.html）
- 全屏高度 hero，带动态 blob 背景光晕动画
- 三个 blob（蓝/绿/紫），使用 `@keyframes blob` 动画
- 显示综合评分环形图（SVG）
- 显示报告标签和关键 tag

### 7.7 KPI 卡片
- 背景 `var(--bg-card)`，圆角 `var(--radius-card)`
- 顶部必须有渐变线条（蓝→绿）
- hover 上浮 + 蓝色发光

### 7.8 图表卡片
- 背景 `var(--bg-card)`，圆角 `var(--radius-card)`
- 中型图表高度 280-300px，大型 360-380px
- 图表标题用 Sora 字体
- 数据来源标注用 `var(--text-muted)` 小字

### 7.9 专利链接
- 字体：JetBrains Mono
- 颜色：`var(--color-primary)`
- hover：变 `var(--color-accent)` + 发光效果

### 7.10 正文排版
- 正文颜色 `var(--text-secondary)`，行高 1.8
- 每个重要结论后附 claim_id 标签（蓝色圆角小标签）
- 数据来源说明用左边框引用块样式

## 八、index.html 内容规范（重点强化）

index.html 必须是完整的白皮书式主报告，包含以下所有15个区块：

1. **Hero 区**：评分环形图 + 研发建议标签 + 导航按钮
2. **KPI 概览区**（≥6个卡片）：全球总量、中国总量、近五年CAGR、子方向数量、综合评分、代表专利数
3. **前言与背景**（≥300字）：产业背景、分析价值、核心发现概述
4. **全球专利趋势图**（ECharts折线，全量分桶数据）+ claim_id
5. **中国 vs 全球趋势对比图**（ECharts双线折线）+ claim_id
6. **子技术方向热度图**（ECharts横向柱状图）+ claim_id
7. **六维评分雷达图**（ECharts）+ 得分明细表格
8. **趋势深度分析**（≥500字正文）：趋势阶段判断、关键拐点、近三年活跃度，每个判断标注 claim_id 和数据来源
9. **子技术方向分析**（≥400字正文）：每个子方向的专利数量、增长信号、机会评分，标注 claim_id
10. **技术空白点**（≥3个）：每个空白点说明为什么是空白、数据依据、切入建议，标注 claim_id
11. **综合研发/投资结论**（≥400字，最重要区块）：
    - 明确给出：**是否值得投入研发**（是/否/有条件）
    - 综合评分解读（每个维度得分+说明）
    - 主要机会（≥3条，每条带数据来源）
    - 主要风险（≥3条，每条带数据来源）
    - 下一步建议（≥5条具体可执行的建议）
    - 每个结论必须标注 claim_id
12. **专利布局建议**（≥300字）：核心技术环节布局、差异化路线建议、国际布局建议
13. **Top 10 代表专利**（表格）：带智慧芽链接，明确标注"代表样本，非申请量排名"
14. **数据说明与免责**：检索式、统计口径、TopK50使用边界、免责声明
15. **页面导航**：跳转到 patents.html、evidence.html、subfields.html、methodology.html 的按钮

### index.html 正文字数要求：
- 总正文字数（不含图表、表格、代码）≥ 3000字
- 综合结论区块 ≥ 400字
- 每个主要结论必须有 claim_id 标注和数据来源说明

## 九、评分体系

六维评分，满分 100：
1. 专利增长趋势（0-20）：基于年度趋势分桶数据
2. 申请人活跃度（0-15）：基于代表样本申请人多样性，标注为样本估算
3. 专利质量/影响力（0-15）：基于代表样本被引、同族情况，标注为样本估算
4. 子技术机会空间（0-20）：基于子技术方向独立检索 matched_total
5. 竞争风险（反向，0-15）：基于趋势数据和子技术集中度
6. 全球布局/商业化信号（0-15）：基于全球趋势总量和增速

## 十、证据链规范

每条证据链格式：
- claim_id：T=趋势，S=子技术，O=空白点，R=综合评分，Q=质量，C=竞争
- 必须包含：结论文本、数据来源、数据值、支撑专利、证据强度、推理说明、限制说明

## 十一、最终对话输出格式

Skill 完成后，在对话中输出：
1. 综合推荐指数（X/100）
2. 研发/投资建议（明确是/否/有条件）
3. 核心结论 5-8 条（每条标注 claim_id）
4. 生成文件清单（10个文件）
5. 数据声明（趋势图全量、TopK50仅展示、三类图未生成原因）
6. 提示用户打开各 HTML 文件

## 十二、异常处理

| 异常 | 处理方式 |
|------|----------|
| 输入过于宏观 | 拒绝并给出细化建议 |
| 分桶检索失败 | 不生成趋势图，说明限制 |
| 申请人/地域/法律状态聚合不可得 | 不生成对应图表，在 methodology.html 说明，不使用 TopK50 近似替代 |
| 页面生成不完整 | 立即修复，不允许以"生成完成"结束但缺文件 |
| index.html 字数不足 | 立即补充正文，直到满足 ≥3000字要求 |
| PDF/XLSX 需要 Python | 跳过，不生成 |

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。

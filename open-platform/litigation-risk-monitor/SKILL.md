---
name: litigation-risk-monitor
description: |
  涉诉专利风险监测与同族扩展分析技能。触发场景：用户提供目标申请人名单（1～N 个，中英文均可），希望自动检索这些申请人名下的涉诉专利，做 INPADOC 同族扩展，结合 Patsnap legal 模块与 web.search 公开诉讼信息双向交叉，输出同族基础分析（地域/技术点/法律状态/审查历史）、诉讼时间线（含涉案专利号）、涉诉案件深度分析（原被告/案号/进程/争议焦点/抗辩/结果）、核心发明人近 3 年延伸分析，并生成单一 HTML 报告 + 结构化 JSON/CSV 附件，给出地域风险、应诉预警、趋势预测三维结论。不适用于：单件专利新颖性/创造性分析（路由 novelty-check / non-obviousness-check）、纯 FTO 法律意见、无申请人名单的开放式情报、与"涉诉专利同族 + 诉讼案件 + 发明人趋势"无关的一般性问答。
---

# litigation-risk-monitor — 涉诉专利风险监测 v10（target-centric 报告模板）

## 触发条件
- 用户给出 **目标申请人名单**（1～N 个，中英文均可），并希望对其名下专利做 **涉诉风险监测 / 同族风险扩展 / 诉讼案件梳理 / 发明人趋势分析**。
- 关键词信号：涉诉专利、专利诉讼监测、同族风险、INPADOC 同族、原被告分析、应诉预警、发明人近 3 年布局。

## 不适用
- 单件专利新颖性 / 创造性分析 → 路由 `novelty-check` / `non-obviousness-check`。
- 纯 FTO 法律意见、专利无效检索 → 走专门的 FTO / 无效流程。
- 无申请人名单的开放式技术情报、产品调研 → 走通用检索或其它技能。

## 输入契约
| 字段 | 必填 | 说明 |
|---|---|---|
| `assignees` | ✅ | 目标申请人列表（=被监测主体 target），中英文均可 |
| `inventor_lookback_years` | ❌ | 发明人近期检索回溯年限，默认 `3` |
| `family_scope` | ❌ | 同族范围，默认 `inpadoc` |
| `max_litigated_per_assignee` | ❌ | 每个申请人最多分析的涉诉专利数，默认 `30` |

> **主体口径**：报告中第一个 `assignees` 元素视为"被监测主体（target）"，所有统计卡片、章节标题、NAV tab、战略建议措辞**必须以 target 为主语**；其它公司一律以"对手 / 原告 / 被告"等中性角色出现，**严禁**出现"<对手公司>涉诉专利"、"<对手公司>反诉专利"等以对手为维度的章节标题。

---

## 执行流程（全自动，不中途确认）

### Step 1 — 涉诉专利初筛

#### 1a — PatSnap MCP + web.search 双路初筛
- 对每个 `assignee` 调用 `patent.search`：`search_strategy=["filter"]`，`filters.assignees=[assignee]`，在返回结果中按法律事件含 litigation/诉讼/lawsuit/infringement 字段做候选筛选。
- 同时用 `web.search` 查询 `"<assignee>" patent litigation lawsuit 诉讼 专利` 做交叉确认。
- 合并两路结果，按 `pn` 去重，保存到内存变量 `litigated_patents[]`。
- 对每件 `litigated_patents[i]` 标注 `target_role ∈ {"defendant","plaintiff","co_party"}`：
  - target 在该案为被起诉方 → `defendant`
  - target 在该案为起诉/反诉/主张方 → `plaintiff`
  - 其它（共同申请人、第三人等）→ `co_party`

#### 1b — 新闻专利号识别与补充
对 Step 1a 的全部 `web.search` 返回内容识别：
- **ZL格式**（如 `ZL202110123456.7`）：提取纯数字作申请号检索
- **CN格式**（如 `CN211719631U`）：直接作公开号用 `patent.fetch` 获取
去重合并：已存在→来源升级为 `"patsnap+web_news"`；仅新闻→`source="web_news"` 加入列表。

### Step 2 — 同族扩展 + 深度分析

#### 2a — 同族扩展
- 对每件涉诉专利调用 `patent.fetch(keys=[pn], key_type="pn", module=["basic","legal","family"], include_structured=true, include_images=true)`
- 从返回结构中提取：同族成员列表（pn/authority/legal_status/application_date/grant_date）、第一张摘要图片URL、legal关键事件
- 同时提取 `patent_id`，用于生成超链接
- ⚠️ **patent_id 必须从 patent.fetch 返回结构中提取，严禁伪造或使用任何占位UUID**

#### 2b — 摘要附图下载（⚠️ 必须完成）
使用 Python 脚本（调用 `scripts/orchestrator.py` 中的 `fetch_abstract_image_b64`）：
1. 对每件涉诉专利，传入 `pn` 和 Step 2a 获取的签名图片URL
2. 下载图片到 `@skill_workspace/outputs/images/<pn>_fig1.png`，同时返回 base64 字符串
3. 将 base64 字符串保存在内存变量，Step 8 写 HTML 时直接内嵌到 `src="data:image/png;base64,..."`
4. 失败时 base64 留空，HTML中显示 `<div class="no-img">暂无摘要附图</div>`

#### 2c — 权利要求对比
对 CN/US/EP 各取1件代表性同族专利，读取独立权利要求，比较保护范围/保护重点/技术覆盖差异。
保存内存变量：`claim_comparison[]` 含 pn/authority/protection_scope/protection_focus/tech_coverage_notes

#### 2d — 地域布局分析
基于同族成员 `authority` 统计，分析主要布局国家、有效/审中/失效分布，识别潜在风险地域。
保存内存变量：`geo_analysis`（300字以上文字）、`geo_risk_by_authority[]`（含 authority/family_count/active_count/pending_count/risk_level/reason）

#### 2e — 法律状态与审查历史
从 `patent.fetch` 的 `legal` 模块，提取每件涉诉专利及关键同族的关键审查节点。
保存内存变量：`legal_detail[]` 含 pn/authority/legal_status/grant_date/expiry_date/key_events[]

### Step 3 — 诉讼时间线构建
收集所有诉讼事件，每个事件包含：date/title/description/event_type/patents[](含pn+title+url)/amount/court/case_no/result/result_type。按日期升序排列，保存 `litigation_timeline[]`。

### Step 4 — 涉诉案件深度梳理
提取：原告/被告/案号/法院/起诉日/当前进程/争议焦点/审理结果/关键节点。每条事实挂 `[S#]` 来源标记。保存 `cases[]`。

### Step 5 — 核心发明人延伸分析
- 聚合同族 `inventors`，取 TOP-10，保存 `core_inventors[]`
- 对每位发明人查近3年申请量（按年统计），保存 `yearly_stats[]`（year/count）
- 归纳近3年主要技术布局点（3～8个方向），保存 `tech_focus_list[]`（tech/patent_count/representative_pn/representative_url）

### Step 6 — 三维结论合成
- **地域风险**：基于 `geo_risk_by_authority`，逐地域给出风险评级+建议，保存 `geo_litigation_risk[]`
- **应诉预警**：不少于800字完整段落，覆盖争议点/被告策略/攻防博弈/态势研判/建议行动，保存 `litigation_alert_summary`
- **趋势预测**：基于近3年申请内容，总结技术布局趋势（200字以上）+ 重点方向列表 + 短/中/长期预测，保存 `trend_forecast`

---

## Step 8 — HTML报告生成（⚠️ 核心步骤，严格遵守 v3 模板）

### ⚠️ 严禁调用 render_report.py 进行渲染

**绝对不要**：
- 生成 JSON 数据文件然后调用 `render_report.py` 渲染
- 使用 Jinja2 模板
- 调用任何 Python 渲染脚本生成 HTML

### ✅ 正确做法：Agent 直接将收集到的真实数据写入 HTML

使用 `files.begin_write` → 多次 `files.append`（每次约4000字节）→ `files.finish_write` 写入：
```
@skill_workspace/outputs/<target简称>_litigation_risk_report.html
```

**核心原则**：HTML 中的每一个数据点（专利号、标题、日期、分析文字、base64图片等）都必须是前面各步骤收集到的**真实数据**，直接硬编码进 HTML 字符串。不得出现任何占位符如 `【占位符】` 或 `{{ variable }}`。

---

### 🎯 v3 主体口径规则（必须遵守）

**target = 第一个 `assignees` 元素 = 被监测主体**。整份 HTML 报告的视角必须以 target 为主语：

| 维度 | ❌ 旧版（以对手为维度，禁止） | ✅ v3（以 target 为主体，必须） |
|---|---|---|
| NAV tab | `宁德时代涉诉专利` `中创新航反诉专利` | `<target>涉诉专利`（合并为一个 tab） |
| 章节标题 | `⚔️ 宁德时代起诉专利（原告方·N件）` `🛡️ 中创新航反诉专利（被告方·N件）` | `⚖️ <target>涉诉专利（共 N 件）` |
| 内部小标题 | 以"原告方/被告方"做章节级标题 | `一、<target>作为被告的涉诉专利（N 件）` `二、<target>作为原告主张的涉诉专利（N 件）` |
| 统计卡片 | `<对手>起诉专利数` `<target>反诉专利数` | `<target>被诉专利数` `<target>主张专利数` |
| 战略建议措辞 | `<target>反诉专利` | `<target>主张专利` |

**严禁**：
- NAV、`<h1>/<h2>/<h3>` 标题、`section-header` 中出现以对手公司名为主语的章节标题（如"<对手>起诉专利"、"<对手>诉讼专利"）
- 统计卡片的 `stat-label` 出现"<对手>起诉专利数"等以对手为主语的口径

**允许**：
- 在执行总结、案件背景叙事、诉讼时间线事件描述、深度分析正文中，可以客观提及对手作为原告/被告的事实——这是事实陈述，不是"以对手为维度的章节"。

### HTML报告章节写法规范

报告使用以下固定 CSS 头部（直接复制写入 append sequence=1）：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>涉诉专利风险监测报告 — [target简称]</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
:root{
  --primary:#1a56db;--primary-light:#ebf5ff;--danger:#e02424;--danger-light:#fef2f2;
  --warn:#d97706;--warn-light:#fffbeb;--success:#057a55;--success-light:#f0fdf4;
  --gray50:#f9fafb;--gray100:#f3f4f6;--gray200:#e5e7eb;--gray400:#9ca3af;
  --gray600:#4b5563;--gray700:#374151;--gray900:#111827;
  --radius:8px;--shadow:0 1px 3px rgba(0,0,0,.1),0 1px 2px rgba(0,0,0,.06);
  --shadow-lg:0 10px 25px rgba(0,0,0,.1);
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'PingFang SC','Microsoft YaHei',sans-serif;background:#f0f4f8;color:var(--gray900);line-height:1.6}
.nav{background:#1e3a6e;position:sticky;top:0;z-index:100;display:flex;gap:0;overflow-x:auto;box-shadow:0 2px 8px rgba(0,0,0,.2)}
.nav ul{display:flex;list-style:none;margin:0;padding:0;gap:0}
.nav a{color:rgba(255,255,255,.75);padding:12px 20px;font-size:13px;font-weight:500;text-decoration:none;white-space:nowrap;border-bottom:3px solid transparent;transition:all .2s;display:block}
.nav a:hover,.nav a.active{color:#fff;border-bottom-color:#60a5fa}
.header{background:linear-gradient(135deg,#1e3a6e 0%,#1a56db 60%,#2563eb 100%);color:#fff;padding:40px 60px;position:relative;overflow:hidden}
.header::after{content:'';position:absolute;right:-80px;top:-80px;width:400px;height:400px;background:rgba(255,255,255,.05);border-radius:50%}
.header h1{font-size:32px;font-weight:700;letter-spacing:1px}
.header .subtitle{font-size:14px;opacity:.8;margin-top:6px}
.header .meta-row{display:flex;gap:30px;margin-top:20px;font-size:13px;opacity:.85}
.risk-badge{display:inline-block;background:#e02424;color:#fff;padding:4px 14px;border-radius:20px;font-size:12px;font-weight:600;letter-spacing:.5px;margin-top:10px}
.container{max-width:1200px;margin:0 auto;padding:30px 20px}
.section{background:#fff;border-radius:var(--radius);box-shadow:var(--shadow);margin-bottom:24px;overflow:hidden}
.section-header{background:linear-gradient(90deg,var(--primary) 0%,#3b82f6 100%);color:#fff;padding:14px 24px;font-size:16px;font-weight:600;display:flex;align-items:center;gap:10px}
.section-header .icon{font-size:20px}
.section-body{padding:24px}
.exec-summary{background:#fff;border:1px solid #c8daf0;border-radius:10px;padding:20px 28px;margin:0 0 24px;box-shadow:0 2px 8px rgba(26,86,219,.08)}
.exec-summary h2{font-size:17px;color:var(--primary);margin:0 0 14px;font-weight:700}
.exec-summary p{font-size:14px;line-height:1.9;color:var(--gray700);margin:10px 0;text-indent:2em}
.stats-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:24px}
.stat-card{background:#fff;border-radius:var(--radius);box-shadow:var(--shadow);padding:20px;text-align:center;border-top:3px solid var(--primary)}
.stat-card.danger{border-top-color:var(--danger)}.stat-card.warn{border-top-color:var(--warn)}.stat-card.success{border-top-color:var(--success)}
.stat-num{font-size:36px;font-weight:700;color:var(--primary);line-height:1}
.stat-card.danger .stat-num{color:var(--danger)}.stat-card.warn .stat-num{color:var(--warn)}.stat-card.success .stat-num{color:var(--success)}
.stat-label{font-size:13px;color:var(--gray600);margin-top:6px}
.assignee-block{border:1px solid var(--gray200);border-radius:var(--radius);padding:16px;margin:12px 0;background:var(--gray50)}
.assignee-name{font-size:15px;font-weight:700;color:var(--gray900);margin-bottom:10px;border-bottom:1px solid var(--gray200);padding-bottom:8px}
.litigated-row{display:flex;gap:8px;align-items:flex-start;padding:8px 0;border-bottom:1px dashed var(--gray200);flex-wrap:wrap}
.litigated-pn{min-width:160px;font-weight:700;font-size:13px;color:var(--danger)}
.litigated-title{color:var(--gray600);font-size:12px;flex:1;min-width:160px}
.family-chips{display:flex;flex-wrap:wrap;gap:4px;width:100%;margin-top:6px}
.family-chip{display:inline-flex;align-items:center;gap:3px;background:var(--primary-light);border:1px solid #bfdbfe;border-radius:10px;padding:2px 8px;font-size:11px}
.fc-auth{color:var(--gray400);font-size:10px}
.status-active{color:var(--success);font-weight:600}.status-inactive{color:var(--danger)}.status-pending{color:var(--warn)}
.patent-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:20px}
.patent-card{border:1px solid var(--gray200);border-radius:var(--radius);overflow:hidden;transition:box-shadow .2s;cursor:pointer}
.patent-card:hover{box-shadow:var(--shadow-lg)}
.patent-card-header{padding:12px 16px;display:flex;justify-content:space-between;align-items:flex-start;background:var(--gray50)}
.patent-card-header.defendant{background:var(--danger-light);border-bottom:2px solid var(--danger)}
.patent-card-header.plaintiff{background:#f0fdf4;border-bottom:2px solid var(--success)}
.pn-link{font-weight:700;color:var(--primary);text-decoration:none;font-size:15px}
.pn-link:hover{text-decoration:underline}
.badge{display:inline-block;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600}
.badge-active{background:#d1fae5;color:#065f46}.badge-pending{background:#fef3c7;color:#92400e}.badge-danger{background:#fee2e2;color:#991b1b}
.patent-card-body{padding:16px}
.patent-card-body .title{font-size:14px;font-weight:600;color:var(--gray900);margin-bottom:8px}
.patent-card-body .abstract{font-size:13px;color:var(--gray600);line-height:1.7;margin-bottom:12px}
.patent-fig{width:100%;max-height:180px;object-fit:contain;border:1px solid var(--gray200);border-radius:4px;background:var(--gray50);display:block}
.no-img{background:var(--gray100);border:1px dashed var(--gray400);border-radius:4px;padding:30px;text-align:center;color:var(--gray400);font-size:12px}
.meta-list{display:grid;grid-template-columns:auto 1fr;gap:4px 12px;font-size:12px;color:var(--gray600);margin-top:12px}
.meta-list dt{font-weight:600;color:var(--gray700);white-space:nowrap}
.family-block{margin-top:12px;border-top:1px dashed var(--gray200);padding-top:10px}
.family-block h4{font-size:12px;color:var(--gray600);margin:0 0 6px;font-weight:600}
.family-table{width:100%;border-collapse:collapse;font-size:12px;margin-top:8px}
.family-table th{background:var(--gray100);padding:6px 10px;text-align:left;font-weight:600;color:var(--gray700);border-bottom:1px solid var(--gray200)}
.family-table td{padding:6px 10px;border-bottom:1px solid var(--gray100);color:var(--gray600)}
.family-table tr:last-child td{border-bottom:none}
.family-table a{color:var(--primary);text-decoration:none}.family-table a:hover{text-decoration:underline}
.timeline{position:relative;padding-left:40px;margin:20px 0}
.timeline::before{content:'';position:absolute;left:16px;top:0;bottom:0;width:3px;background:linear-gradient(to bottom,var(--primary),var(--warn),var(--danger));border-radius:2px}
.tl-item{position:relative;margin-bottom:28px}
.tl-dot{position:absolute;left:-31px;top:4px;width:22px;height:22px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;border:2px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,.18);color:#fff}
.tl-dot.offense,.tl-dot.type-lawsuit_filed{background:var(--danger)}
.tl-dot.defense,.tl-dot.type-counter_suit{background:var(--primary)}
.tl-dot.trial,.tl-dot.type-verdict{background:#2980b9}
.tl-dot.judgment,.tl-dot.type-settlement{background:var(--success)}
.tl-dot.appeal,.tl-dot.type-appeal{background:#7c3aed}
.tl-dot.type-invalidation{background:var(--warn)}.tl-dot.type-other{background:var(--gray400)}
.tl-content{background:#fff;border-radius:var(--radius);padding:14px 16px;border:1px solid var(--gray200);box-shadow:var(--shadow)}
.tl-date{font-size:11px;color:var(--gray400);font-weight:600;margin-bottom:4px}
.tl-title{font-size:14px;font-weight:700;color:var(--gray900);margin-bottom:6px}
.tl-desc{font-size:13px;color:var(--gray600);margin-bottom:8px;line-height:1.7}
.tl-patents{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0;padding:8px 10px;background:var(--primary-light);border-radius:4px;border-left:3px solid var(--primary)}
.tl-patent-label{font-size:11px;color:var(--gray600);font-weight:600;width:100%;margin-bottom:2px}
.tl-pn-chip{display:inline-flex;align-items:center;background:#e8f0fe;border:1px solid #c5d5f5;border-radius:12px;padding:2px 10px;font-size:11px;font-weight:600}
.tl-pn-chip a{color:var(--primary);text-decoration:none}
.tl-pn-title{color:var(--gray400);font-weight:400;margin-left:4px;font-size:10px}
.tl-meta{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px;align-items:center;font-size:12px}
.tl-amount{color:var(--gray700);background:var(--warn-light);border:1px solid #fcd34d;padding:2px 8px;border-radius:4px}
.badge-win{background:#d1fae5;color:#065f46;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:700}
.badge-lose{background:var(--danger-light);color:#991b1b;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:700}
.badge-pending{background:var(--warn-light);color:#92400e;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:700}
.badge-settled{background:#ecfdf5;color:#065f46;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:700}
.badge-withdrawn{background:var(--gray100);color:var(--gray600);padding:2px 8px;border-radius:4px;font-size:11px}
.analysis-block{background:var(--gray50);border-left:4px solid var(--primary);padding:16px 20px;margin:12px 0;border-radius:0 var(--radius) var(--radius) 0;line-height:1.9;font-size:14px}
.alert-box{background:var(--warn-light);border-left:4px solid var(--warn);padding:16px 20px;margin:12px 0;border-radius:0 var(--radius) var(--radius) 0;line-height:1.9;font-size:14px}
.alert-box p,.analysis-block p{margin:8px 0;color:var(--gray700)}
.geo-risk-card{border-left:4px solid var(--gray200);padding:12px 16px;margin:8px 0;border-radius:0 var(--radius) var(--radius) 0;background:var(--gray50);font-size:13px}
.geo-risk-card.high{border-left-color:var(--danger);background:var(--danger-light)}
.geo-risk-card.medium{border-left-color:var(--warn);background:var(--warn-light)}
.geo-risk-card.low{border-left-color:var(--success);background:var(--success-light)}
.geo-risk-high{color:var(--danger);font-weight:700}.geo-risk-medium{color:var(--warn);font-weight:700}.geo-risk-low{color:var(--success);font-weight:700}
.trend-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:16px}
.trend-period-card{border:1px solid var(--gray200);border-radius:var(--radius);padding:16px;background:#fff}
.trend-period-label{font-size:12px;font-weight:700;color:var(--primary);margin-bottom:8px;padding-bottom:6px;border-bottom:1px solid var(--gray200)}
.trend-dir-item{display:flex;gap:10px;align-items:flex-start;padding:6px 0;border-bottom:1px dashed var(--gray200);font-size:13px}
.trend-dir-name{font-weight:700;color:var(--gray900);min-width:120px}
.inventor-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;margin-top:12px}
.inventor-card{border:1px solid var(--gray200);border-radius:var(--radius);padding:16px;background:#fff}
.inventor-name{font-size:15px;font-weight:700;color:var(--gray900);margin-bottom:4px}
.chart-container{max-width:100%;margin:12px 0}
.tech-list{margin:6px 0 0 16px;padding:0;list-style:disc;font-size:13px;line-height:1.9;color:var(--gray700)}
.modal-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:1000;align-items:center;justify-content:center}
.modal-overlay.open{display:flex}
.modal-box{background:#fff;border-radius:12px;padding:28px;max-width:760px;width:92%;max-height:82vh;overflow-y:auto;position:relative;box-shadow:var(--shadow-lg)}
.modal-close{position:absolute;top:14px;right:18px;font-size:22px;cursor:pointer;color:var(--gray400);background:none;border:none;line-height:1}
.modal-close:hover{color:var(--gray900)}
.modal-pn{font-size:17px;font-weight:700;margin-bottom:14px;color:var(--primary)}
.claims-text{font-size:13px;white-space:pre-wrap;line-height:1.8;color:var(--gray700)}
.case-card{border:1px solid var(--gray200);border-radius:var(--radius);padding:16px;margin:10px 0;background:#fff}
.tag{display:inline-block;padding:2px 8px;border-radius:4px;background:var(--primary-light);color:var(--primary);font-size:11px;font-weight:600;margin-right:4px}
table{border-collapse:collapse;width:100%;margin:8px 0;font-size:13px}
th,td{border:1px solid var(--gray200);padding:8px 12px;text-align:left;vertical-align:top}
th{background:var(--gray100);font-weight:600;color:var(--gray700)}
tr:hover td{background:var(--gray50)}
a{color:var(--primary);text-decoration:none}
a:hover{text-decoration:underline}
.footer{margin-top:40px;font-size:12px;color:var(--gray400);border-top:1px solid var(--gray200);padding-top:12px;text-align:center}
@media(max-width:768px){
  .stats-grid{grid-template-columns:repeat(2,1fr)}
  .patent-grid,.inventor-grid,.trend-grid{grid-template-columns:1fr}
  .header{padding:24px 20px}.container{padding:16px 12px}.nav a{padding:10px 14px}
}

/* ── CARD WIDTH CONSISTENCY OVERRIDES (v3.1) ── */
.patent-grid{display:grid;grid-template-columns:repeat(2, minmax(0, 1fr));gap:20px;align-items:stretch}
.patent-card{min-width:0;width:100%;display:flex;flex-direction:column;height:100%;box-sizing:border-box}
.patent-card-body{flex:1 1 auto;min-width:0;display:flex;flex-direction:column}
.patent-card-body .title,.patent-card-body .abstract{min-width:0;overflow-wrap:anywhere;word-break:break-word}
.patent-fig{width:100%;max-width:100%;min-width:0;height:180px;max-height:180px;object-fit:contain;box-sizing:border-box}
.no-img{width:100%;box-sizing:border-box}
.meta-list{grid-template-columns:max-content minmax(0, 1fr);min-width:0}
.meta-list dt{white-space:nowrap}
.meta-list dd{min-width:0;margin:0;overflow-wrap:anywhere;word-break:break-word}
.family-table{table-layout:fixed;width:100%}
.family-table th,.family-table td{overflow-wrap:anywhere;word-break:break-word}
/* 末行只剩 1 卡时，保持其宽度等于一列，而不是撑满两列 */
.patent-grid > .patent-card:last-child:nth-child(odd){grid-column:span 1;justify-self:stretch}
@media(max-width:768px){
  .patent-grid{grid-template-columns:1fr}
  .patent-grid > .patent-card:last-child:nth-child(odd){grid-column:span 1}
}

/* ── v3.2 SECTION INNER WIDTH OVERRIDES ── */
.section-body > .analysis-block,
.section-body > .alert-box,
.section-body > .timeline,
.section-body > .trend-grid,
.section-body > .geo-grid,
.section-body > .inventor-grid{width:100%;box-sizing:border-box;max-width:100%}
/* inventors inner grid: prevent canvas left column from blowing out width */
#inventors .section-body > div[style*="grid-template-columns:1fr 1fr"]{
  display:grid !important;grid-template-columns:minmax(0,1fr) minmax(0,1fr) !important;gap:24px;width:100%;box-sizing:border-box
}
#inventors .section-body > div[style*="grid-template-columns:1fr 1fr"] > *{min-width:0}
#inventors canvas{max-width:100%;height:auto !important}
@media(max-width:768px){
  #inventors .section-body > div[style*="grid-template-columns:1fr 1fr"]{grid-template-columns:1fr !important}
}
/* unify section-body horizontal padding so all cards share identical content width */
.section > .section-body{padding:24px;box-sizing:border-box}

</style>
</head>
<body>
```

尾部固定 JS（写入最后一个 append）：
```html
<script>
function openModal(id){document.getElementById(id).classList.add('open');document.body.style.overflow='hidden';}
function closeModal(id){document.getElementById(id).classList.remove('open');document.body.style.overflow='';}
document.addEventListener('keydown',function(e){if(e.key==='Escape'){document.querySelectorAll('.modal-overlay.open').forEach(function(m){m.classList.remove('open');});document.body.style.overflow='';}});
</script>
<div class="footer">本报告由 Eureka 自动生成 | 基于智慧芽专利数据库及公开网络信息 | 生成时间：[真实时间]</div>
</body></html>
```

### v3 NAV 模板（target-centric，固定 7 个 tab）

```html
<nav class="nav">
  <ul>
    <li><a href="#overview">风险概览</a></li>
    <li><a href="#calb-patents">[target]涉诉专利</a></li>
    <li><a href="#timeline">诉讼时间线</a></li>
    <li><a href="#analysis">深度分析</a></li>
    <li><a href="#inventors">核心发明人</a></li>
    <li><a href="#geo">地域风险</a></li>
    <li><a href="#forecast">趋势预测</a></li>
  </ul>
</nav>
```

> ⚠️ NAV 中**不得**出现以对手公司名为主语的 tab（如"宁德时代涉诉专利"、"<对手>起诉专利"）。涉诉专利 tab 始终只有一个，主语始终是 target。

### ⚠️ 专利超链接格式（严格执行）

所有专利公开号超链接必须使用以下格式：
- **有 patentId 时**（从 `patent.fetch` 返回结果中提取，⚠️ 严禁伪造或使用任何占位UUID）：
  ```
  https://analytics.zhihuiya.com/patent-view/abst'figures/?_type=query&source_type=search_result&rows=100&patentId=<真实patentId>
  ```
- **无 patentId 时**（降级，仅在 patent.fetch 确实未返回 patentId 时使用）：
  ```
  https://analytics.zhihuiya.com/search?q=<公开号>
  ```
- **patentId 获取方式**：调用 `patent.fetch(keys=[pn], key_type="pn", include_structured=true)` 后，从返回的 `structured.basic` 或顶层字段中提取 `patentId` / `patent_id`。
- **验证**：写入 HTML 前，确认每个 patentId 均为 patent.fetch 实际返回值，格式为标准 UUID（含连字符，共36字符），例如 `d5044ca4-876a-4e5a-9968-977050522a51`。

### 章节具体写法（每章直接写真实数据，无占位符）

#### 第0章：执行总结（⚠️ 必须写在 h1 标题之后、stat-panel 之前）

**要求**：三段式，总字数不少于500字，段落之间逻辑递进，全部基于本轮收集的真实数据。

- **第一段（案件背景与核心争议）**：介绍涉诉双方基本情况、诉讼缘起、涉及的核心专利技术领域、专利权属与核心争议的技术焦点，以及双方在市场上的竞争关系背景。字数不少于180字。
- **第二段（诉讼进展与关键转折）**：按时间顺序梳理主要诉讼节点，包括起诉时间、法院、索赔金额、一审/二审结果、专利无效宣告结果、反诉情况等重大转折事件。字数不少于180字。
- **第三段（风险研判与战略建议）**：基于同族布局、地域风险、技术趋势，给出综合风险评级（高/中/低），并提出3～5项具体可操作的战略建议（措辞以 target 为主语，例如"强化对 target 主张专利的权利稳定性维护"，**不要写成"反诉专利"**）。字数不少于140字。

```html
<!-- 执行总结：写在 h1 标题之后、stat-panel 之前 -->
<div class="exec-summary">
  <h2>📋 执行总结</h2>
  <p>[第一段：案件背景与核心争议，≥180字]</p>
  <p>[第二段：诉讼进展与关键转折，≥180字]</p>
  <p>[第三段：风险研判与战略建议，≥140字，措辞以 target 为主语]</p>
</div>
```

#### 第1章：概览（统计面板 + 三级映射）

**v3 统计卡片必须以 target 为主语**，标准 4 卡口径（数字根据真实数据填）：

```html
<h1>⚖️ 涉诉专利风险监测报告 — [target真实名称]</h1>
<div style="color:#666;font-size:13px;margin-bottom:16px;">生成时间：[真实时间] | 数据来源：智慧芽 PatSnap + 公开网络信息</div>

<!-- 执行总结放在此处（见第0章规范） -->

<!-- v3 统计面板：4 卡，全部以 target 为主语 -->
<div class="stats-grid" id="overview">
  <div class="stat-card danger">
    <div class="stat-num">[N1]</div>
    <div class="stat-label">[target]被诉专利数</div>
  </div>
  <div class="stat-card">
    <div class="stat-num">[N2]</div>
    <div class="stat-label">[target]主张专利数</div>
  </div>
  <div class="stat-card warn">
    <div class="stat-num">[金额]</div>
    <div class="stat-label">合计涉案金额（元）</div>
  </div>
  <div class="stat-card success">
    <div class="stat-num">[N3]</div>
    <div class="stat-label">诉讼时间线节点数</div>
  </div>
</div>

<h2>1. 概览</h2>
<h3>1.1 [target] → 涉诉专利 → 同族号 映射</h3>

<div class="assignee-block">
  <div class="assignee-name">[target全称] <span class="tag">[角色：被诉/主张/共同申请人]</span></div>
  <div class="litigated-row">
    <div class="litigated-pn">🔴 <a href="https://analytics.zhihuiya.com/patent-view/abst'figures/?_type=query&source_type=search_result&rows=100&patentId=[真实patentId]">[CN号]</a></div>
    <div class="litigated-title">[专利真实标题]</div>
    <div class="family-chips">
      <span class="family-chip"><a href="[同族URL]">[同族公开号]</a> <span class="fc-auth">[受理局]</span> <span class="status-active">●有效</span></span>
    </div>
  </div>
</div>
```

> ⚠️ 禁用的旧 stat-label：`<对手>起诉专利数`、`<target>反诉专利数`。一律改为 `<target>被诉专利数`、`<target>主张专利数`。

#### 第3章：诉讼时间线（⚠️ 每个节点必须包含涉案专利号）

```html
<h2 id="timeline">3. 诉讼时间线</h2>
<div class="timeline">
  <div class="tl-item">
    <div class="tl-dot type-lawsuit_filed">⚖</div>
    <div class="tl-content">
      <div class="tl-date">[真实日期，如 2021-07]</div>
      <div class="tl-title">[真实事件标题]</div>
      <div class="tl-desc">[真实事件描述，含法院名称、索赔金额等]</div>
      <div class="tl-patents">
        <span class="tl-patent-label">📋 涉案专利：</span>
        <span class="tl-pn-chip"><a href="[URL]">[CN真实号]</a><span class="tl-pn-title">[专利真实标题]</span></span>
      </div>
      <div class="tl-meta">
        <span class="tl-amount">💰 [真实索赔额]</span>
        <span>🏛️ [真实法院]</span>
        <span class="badge-pending">[真实状态]</span>
      </div>
    </div>
  </div>
</div>
```

#### 第4章：[target] 涉诉专利详情（⚠️ v3：合并为单一 SECTION，以 target 为主体）

**v3 必须采用以下结构**——一个 `section`，一个 `section-header`，内部用两个轻量 `<h4>` 小标题分组（不要并列两个 section）：

```html
<div class="section" id="calb-patents">
  <div class="section-header">
    <span class="icon">⚖️</span> [target]涉诉专利（共 [N总] 件）
  </div>
  <div class="section-body">
    <p style="font-size:13px;color:#4b5563;margin-bottom:16px;line-height:1.8">
      下列专利按 [target] 在各诉讼案件中的角色分组列出，包含同族表、摘要附图、权利要求等结构化信息。
    </p>

    <h4 style="font-size:15px;color:#374151;margin:8px 0 12px;font-weight:700">一、[target]作为被告的涉诉专利（[N1] 件）</h4>
    <div class="patent-grid">
      <!-- patent-card：header 用 .defendant 配色 -->
      <div class="patent-card" onclick="openModal('modal-pn1')">
        <div class="patent-card-header defendant">
          <a href="[真实URL]" class="pn-link">[真实CN号]</a>
          <span class="badge badge-danger">🔴 高风险·被诉在审</span>
        </div>
        <div class="patent-card-body">
          <div class="title">[真实专利标题]</div>
          <div class="abstract">[真实摘要]</div>
          <img class="patent-fig" src="data:image/png;base64,[真实base64]" alt="[CN号]摘要附图"/>
          <dl class="meta-list">
            <dt>权利人</dt><dd>[真实申请人]</dd>
            <dt>申请日</dt><dd>[真实日期]</dd>
            <dt>IPC</dt><dd>[真实IPC]</dd>
            <dt>诉讼角色</dt><dd>[target] 被诉</dd>
          </dl>
          <div class="family-block">
            <h4>📋 INPADOC 同族专利（[N]件）</h4>
            <table class="family-table">
              <tr><th>公开号</th><th>受理局</th><th>申请日</th><th>法律状态</th></tr>
              <tr><td><a href="[同族URL]">[同族公开号]</a></td><td>[受理局]</td><td>[申请日]</td><td><span class="status-active">有效</span></td></tr>
            </table>
          </div>
        </div>
      </div>
      <!-- ...更多被诉卡片 -->
    </div>

    <h4 style="font-size:15px;color:#374151;margin:24px 0 12px;font-weight:700">二、[target]作为原告主张的涉诉专利（[N2] 件）</h4>
    <div class="patent-grid">
      <!-- patent-card：header 用 .plaintiff 配色 -->
      <div class="patent-card" onclick="openModal('modal-pn5')">
        <div class="patent-card-header plaintiff">
          <a href="[真实URL]" class="pn-link">[真实CN号]</a>
          <span class="badge badge-active">🟢 主张·原告方</span>
        </div>
        <div class="patent-card-body">
          <div class="title">[真实专利标题]</div>
          <!-- 同上结构 -->
          <dl class="meta-list">
            <dt>权利人</dt><dd>[真实申请人]</dd>
            <dt>诉讼角色</dt><dd>[target] 主张（原告）</dd>
          </dl>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- 权利要求 modal -->
<div id="modal-pn1" class="modal-overlay" onclick="if(event.target===this)closeModal('modal-pn1')">
  <div class="modal-box">
    <button class="modal-close" onclick="closeModal('modal-pn1')">✕</button>
    <div class="modal-pn"><a href="[URL]">[CN号]</a> — [专利标题]</div>
    <div class="claims-text">[权利要求全文，直接写入]</div>
  </div>
</div>
```

⚠️ **严禁**写成两个并列的 section，例如：
- ❌ `<div class="section"><div class="section-header">⚔️ <对手>起诉专利（原告方·N件）</div>...</div>` + `<div class="section"><div class="section-header">🛡️ <target>反诉专利（被告方·N件）</div>...</div>`
- ✅ 一个 section，header 文案 = `[target]涉诉专利（共 N 件）`，内部用 `<h4>` 小标题分组。

#### 第6章：核心发明人（⚠️ 包含真实统计图和技术点列表）

```html
<h2 id="inventors">6. 核心发明人延伸分析</h2>
<div class="inventor-section">
  <h3>👤 [发明人真实姓名]（近3年共 [真实N] 件）</h3>
  <div class="chart-container">
    <canvas id="chart-inv-[序号]" height="100"></canvas>
  </div>
  <script>
  new Chart(document.getElementById('chart-inv-[序号]'), {
    type: 'bar',
    data: {
      labels: ['2023', '2024', '2025'],
      datasets: [{
        label: '年度申请量',
        data: [[真实2023数字], [真实2024数字], [真实2025数字]],
        backgroundColor: ['rgba(42,106,74,0.7)', 'rgba(42,106,74,0.8)', 'rgba(42,106,74,0.9)']
      }]
    },
    options: { responsive: true, scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } } }
  });
  </script>
  <h4>近3年主要技术布局方向</h4>
  <ul class="tech-list">
    <li>[真实技术方向1]（[N]件，代表：<a href="[URL]">[CN号]</a> [专利标题]）</li>
  </ul>
</div>
```

#### 第7章：三维结论

```html
<h2 id="geo">7. 三维结论</h2>
<h3>7.1 潜在涉诉地域分析</h3>
<!-- ⚠️ 地域风险分布必须展开为同族专利明细列表，不得仅显示汇总数字 -->
<div class="geo-risk-card high">
  <b>CN — 中国大陆</b> <span class="geo-risk-high">高风险</span><br>
  [真实分析文字：说明CN有效同族数量、主要专利技术特征、潜在诉讼风险点]<br>
  <b>建议：</b>[真实建议]<br>
  <table class="family-table" style="margin-top:8px;">
    <tr><th>同族专利号</th><th>专利标题</th><th>申请日</th><th>法律状态</th></tr>
    <tr><td><a href="[真实URL]">[CN同族号]</a></td><td>[标题]</td><td>[申请日]</td><td><span class="status-active">有效</span></td></tr>
  </table>
</div>

<h3>7.2 应诉预警综合总结</h3>
<!-- ⚠️ 不少于800字，完整连贯段落 -->
<div class="alert-box">
  <p>[真实分析段落1：案件主要争议点...]</p>
  <p>[真实分析段落2：[target] 应诉策略...]</p>
  <p>[真实分析段落3：攻防博弈重点...]</p>
  <p>[真实分析段落4：当前态势研判...]</p>
  <p>[真实分析段落5：建议行动项，措辞以 target 为主语...]</p>
</div>

<h3 id="forecast">7.3 趋势预测</h3>
<div class="analysis-block">[200字以上技术布局趋势总结]</div>
<div class="trend-grid">
  <div class="trend-period-card"><div class="trend-period-label">短期（6～12个月）</div>[真实内容]</div>
  <div class="trend-period-card"><div class="trend-period-label">中期（1～3年）</div>[真实内容]</div>
  <div class="trend-period-card"><div class="trend-period-label">长期（3年以上）</div>[真实内容]</div>
</div>
```

#### 第8章：汇总列表

```html
<h2>8. 涉诉专利汇总列表</h2>
<table>
  <tr><th>涉诉专利</th><th>专利标题</th><th>[target]角色</th><th>同族公开号</th><th>受理局</th><th>法律状态</th><th>申请日</th></tr>
  <tr>
    <td rowspan="[N]"><a href="[URL]">[CN号]</a></td>
    <td rowspan="[N]">[专利标题]</td>
    <td rowspan="[N]">[被诉/主张]</td>
    <td><a href="[同族URL]">[同族公开号]</a></td>
    <td>[受理局]</td>
    <td><span class="status-active">有效</span></td>
    <td>[申请日]</td>
  </tr>
</table>
```

---

## 自检清单（写完 HTML 后必须逐项核对）

写完 HTML 后，使用 `files.grep` 对生成文件做以下正则检查，**任一项命中即必须修订**：

| # | 正则 | 含义（命中即违规） |
|---|---|---|
| 1 | `<对手公司名>(起诉|涉诉|诉讼)专利` 出现在 `class="nav"` 或 `<h1>/<h2>/<h3>/section-header` 内 | NAV/章节标题以对手为主语 |
| 2 | `(反诉专利)` 出现在 `stat-label` 或 `exec-summary` 内 | v3 已统一为"主张专利" |
| 3 | `<对手>起诉专利数` 出现在 `stat-label` 内 | 统计卡片以对手为主语 |
| 4 | 出现 `【.*】` 或 `\{\{.*\}\}` | 残留占位符 |
| 5 | `patentId=[^&"']*` 不是合法 UUID（36字符含连字符） | 伪造 patentId |

通过自检后再交付。

---

## 计数语义守则
- `matched_total` 是查询范围内的命中总数，`returned_count` 是当页样本。
- 报告中展示分布图/表格时，必须写明"样本范围"与"查询过滤条件"。

## 来源标注
- `[S#]` Patsnap patent.search / patent.fetch（注明 pn 与模块）
- `[S#]` web.search / web_fetch（注明 URL 与命中片段）
- 冲突时双源并列展示

## 关键脚本
- `scripts/orchestrator.py`：图片下载/base64转换工具函数（`fetch_abstract_image_b64(pn, image_url)`）
- `scripts/render_report.py`：**CSS/JS参考文件，不调用其渲染函数**
- `scripts/config.py`：默认参数

## 失败回退
- Patsnap legal 为空 → 标注 `[web_only]`，仅基于 web.search 证据
- 同族扩展失败 → HTML中显示"同族扩展失败"
- 摘要附图失败 → `<div class="no-img">暂无摘要附图</div>`
- 应诉预警数据不足 → 尽力生成，标注"基于现有公开信息，部分内容待核实"

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。

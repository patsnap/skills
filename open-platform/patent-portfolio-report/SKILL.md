---
name: patent-portfolio-report
description: 麦肯锡标准·专利组合解读分析报告交付Skill。输入分析标的（企业名称/专利清单/技术领域/竞争对手）及客户核心诉求，严格遵循10步SOP，按九大模块输出完整中文HTML专利组合分析报告，内含核心专利技术拆解可视化图、麦肯锡深蓝配色体系、金字塔原则排版。所有专利数据强制通过Patsnap实时检索，每模块末尾列明检索式备注。集成novelty-check、non-obviousness-check、triz-analysis、patsnap-mckinsey-sales-insight、patsnap-visit-strategist子技能流水线。适用场景：IPO尽调、并购估值、研发战略、337诉讼应对、企业出海布局、行业竞争格局分析。触发关键词：专利组合分析、专利尽调报告、专利价值评估、专利竞争格局、核心专利拆解、IPO知识产权尽调、专利战略报告、专利组合解读、麦肯锡专利报告。
---

# 麦肯锡标准：专利组合解读分析报告

## Skill基础定位

本Skill为麦肯锡咨询体系专属的**专利组合解读分析报告标准化交付技能**，以「商业目标为核心、法律合规为根基、技术竞争力为内核、可视化呈现为抓手、可落地战略为最终交付」，区别于律所合规报告与代理机构撰写质量报告，实现专利分析从「技术文档」到「商业决策依据」的升级。

**V3.0 核心升级**（在V2.0基础上）：
- 对每件核心专利强制生成「技术问题→技术手段→技术功效」三要素技术拆解图
- 该拆解图以HTML可视化卡片形式呈现，嵌入报告第四模块每件专利分析项下
- 三要素内容必须来自 `patsnap_fetch` 全文读取后提取，不得凭空推断

---

## 使用前配置 

本 Skill 依赖智慧芽开放平台 MCP 服务： 

- 完成安装、初次使用时需进行自检，参见 README.md 
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具 
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论 
- 缺少MCP配置时，引导用户参照 README.md 在 [ open.zhihuiya.com ]( https://open.zhihuiya.com/ ) 获取MCP。

## ══════════════════════════════════

## 【全局强制规则】Patsnap数据检索规范
## ══════════════════════════════════

### 规则1：强制实时检索

每个分析步骤在生成结论前，**必须**调用 `mcp_patent-search__patsnap_search` 获取最新数据。禁止基于训练数据或静态知识直接生成专利数量、趋势、排名等具体数据。

### 规则2：检索式备注格式

每个报告模块末尾必须附上「检索式备注」表格，格式如下：

```
【检索式备注 - 本模块】
| 检索目的       | 检索策略                        | 关键词                          | IPC分类         | 申请人/竞对                    | 时间范围      | 管辖地          | topk |
|----------------|--------------------------------|--------------------------------|-----------------|-------------------------------|--------------|-----------------|------|
| 赛道趋势扫描   | keyword + filter               | [技术关键词1, 技术关键词2, ...]  | [IPC代码]        | —                             | 近5年        | CN/US/EP/WO     | 50   |
| 目标企业画像   | keyword + filter               | [企业核心技术词]                | [IPC代码]        | [企业名称]                    | 全量          | 全球            | 100  |
| 竞对布局扫描   | keyword + filter               | [技术关键词]                    | [IPC代码]        | [竞对1, 竞对2]                | 近3年        | CN/US/EP        | 50   |
| 核心专利深读   | semantic + keyword             | [具体技术描述]                  | [精细IPC]        | [企业名称]                    | 全量          | 全球            | 20   |
```

### 规则3：检索轮次设计

每个步骤的检索至少分2轮：
- **第1轮（宽泛扫描）**：`topk=50~100`，`search_strategy=["keyword","filter"]`，获取全貌
- **第2轮（精准深挖）**：`topk=10~20`，`search_strategy=["semantic","keyword"]`，定位高价值专利

### 规则4：数据时效性

检索时默认包含最新数据（不设date_to上限），date_from根据分析需要设定（趋势分析建议5年，全量分析不设下限）。

---

## ══════════════════════════════════
## 【集成子技能流水线】
## ══════════════════════════════════

本技能集成以下子技能，在对应步骤自动触发：

### 子技能1：novelty-check（新颖性分析）
**触发时机**：Step4 核心专利筛选后，对3-8件核心专利进行稳定性评估
**调用逻辑**：
- 对每件核心专利，以其主权利要求为分析对象
- 执行单参考文献新颖性对比：`patsnap_search → patsnap_fetch → element-by-element mapping`
- 输出：`novelty_report.md`（含 novelty_preserved / novelty_rejected / uncertain 结论）
- 结论写入报告第四模块「核心专利法律维度竞争力」子项

### 子技能2：non-obviousness-check（创造性分析）
**触发时机**：novelty-check 完成后，对 novelty_preserved 的核心专利进一步评估创造性
**调用逻辑**：
- 接收 novelty-check 输出的 `claim_diff_matrix.md` 和 `prior_art_catalog.json`
- 执行多参考文献组合分析：D1+D2 组合动机、合理成功预期
- 输出：`inventive_step_report.md`（含 inventive_step_supported / inventive_step_challenged 结论）
- 结论写入报告第四模块「核心专利法律维度竞争力」子项

### 子技能3：triz-analysis（TRIZ矛盾分析）
**触发时机A**：Step4 技术创新点挖掘，识别核心专利的工程矛盾与创新原理
**触发时机B**：Step7 风险缓释方案设计，针对高风险侵权/失效场景提供工程矛盾解法
**调用逻辑**：
- 将核心专利技术特征或风险场景转化为 TRIZ 矛盾模型（改善参数 vs 恶化参数）
- 输出：3条有证据支撑的解决路径 + 加权推荐方案
- A路径结论写入报告第四模块「技术创新点深度分析」
- B路径结论写入报告第七模块「风险缓释技术路径」

### 子技能4：patsnap-mckinsey-sales-insight（销售洞察分析）
**触发时机**：Step8 战略落地建议，当报告受众为客户高层（董事会/CEO/CTO）时
**调用逻辑**：
- 提取目标企业名称、核心利益相关方职位、报告核心发现作为输入
- 借用 SCQA 框架（Situation / Complication / Question / Answer）重构战略建议叙事
- 借用竞争对标矩阵逻辑，识别「隐形差距点」并量化机会价值
- 输出内容融入报告第八模块「战略落地建议」的「顶层战略定位」与「核心举措叙事」

### 子技能5：patsnap-visit-strategist（拜访战略）
**触发时机**：报告交付后，用户请求生成「配套拜访材料」时
**调用逻辑**：
- 提取报告中的客户名称、行业、核心风险点、竞对差距作为输入
- 生成麦肯锡方法论定制的HTML作战地图
- 输出独立HTML文件，可保存至桌面直接使用

### 关于doe-plan
**不集成**：doe-plan 专为生物发酵/上游工艺DOE实验设计，与专利组合分析场景无关联，不组装至本技能。

---

## 适用场景

- 企业IPO/再融资知识产权尽调报告
- 并购/投融资标的专利价值尽调与估值报告
- 企业研发战略规划与专利布局优化报告
- 海外出海/337调查/侵权诉讼专利应对分析报告
- 专利商业化运营/许可/质押融资价值评估报告
- 行业赛道专利竞争格局与壁垒分析报告

## 核心交付原则

1. **MECE无遗漏原则**：全维度拆解无重复、无遗漏，逻辑闭环
2. **商业目标导向原则**：所有分析围绕客户核心诉求分配权重，拒绝纯技术堆砌
3. **对标驱动洞察原则**：以行业标杆/竞争对手为锚，量化定位优劣势，拒绝自说自话
4. **可视化优先原则**：核心结论、技术拆解、数据对比优先用图表呈现，一图胜千言
5. **金字塔表达原则**：先结论后论据，先总后分，每页一个核心观点，符合高管阅读习惯
6. **可落地交付原则**：所有分析最终指向可执行的战略举措，而非纸面洞察
7. **数据实时原则**：所有专利数据必须来自Patsnap实时检索，每模块附检索式备注

---

## 执行流程：10步标准化SOP

| 步骤 | 核心工作内容 | 对应报告核心模块 | 交付物里程碑 | 触发子技能 |
|------|--------------|------------------|--------------|------------|
| Step1 | 项目边界锚定、核心诉求拆解、权重分配、分析口径统一 | 项目定义与方法论模块 | 项目分析大纲与口径确认函 | — |
| Step2 | 宏观产业环境、赛道技术趋势、知识产权竞争规则分析（**Patsnap检索**） | 宏观产业与技术赛道环境模块 | 赛道专利竞争环境分析底稿 | — |
| Step3 | 专利组合基础盘扫描、结构画像、技术分布、生命周期管理分析（**Patsnap检索**） | 专利组合基础画像与全景拆解模块 | 专利组合全景画像数据表+可视化图表 | — |
| Step4 | 核心专利筛选、单专利三维评估、**技术问题→技术手段→技术功效三要素拆解图**、组合协同效应分析（**Patsnap检索 + patsnap_fetch全文 + novelty-check + non-obviousness-check + triz-analysis**） | 专利组合核心竞争力深度分析模块 | 核心专利清单+**每件专利技术拆解卡片**+竞争力打分矩阵+新颖性/创造性报告 | novelty-check → non-obviousness-check → triz-analysis |
| Step5 | 对标主体专利基础盘、技术布局、运营战略全方位对标分析（**Patsnap检索**） | 对标主体专利与战略对比分析模块 | 对标差距分析表+机会/威胁识别清单 | — |
| Step6 | 专利组合价值评估模型构建、量化测算、情景分析、敏感性分析 | 商业价值评估与量化测算模块 | 专利价值评估模型+价值区间测算表 | — |
| Step7 | 全维度风险识别、风险矩阵分级、高风险项应对预案（**triz-analysis补充工程解法**） | 核心风险识别与情景应对模块 | 风险清单+应对预案+风险缓释体系方案 | triz-analysis |
| Step8 | 顶层战略定位、核心举措拆解、分阶段行动路线图（**patsnap-mckinsey-sales-insight SCQA叙事**） | 战略落地建议与行动路线图模块 | 战略举措清单+3年行动路线图 | patsnap-mckinsey-sales-insight |
| Step9 | 执行摘要撰写、全报告内容整合、排版美化、可视化优化 | 执行摘要+全报告终稿整合 | 报告初稿（内容完整、格式规范） | — |
| Step10 | 质量自检、内容校准、合规审核、最终交付（**可选：触发patsnap-visit-strategist生成配套拜访材料**） | 终稿交付 | 符合标准的正式报告+配套附件 | patsnap-visit-strategist（可选） |

---

## 核心模块交付规范

### 前置模块：执行摘要
- **篇幅**：约600字以内，确保核心结论在首屏即可呈现；打印视图下不超过2页A4
- 必选内容：项目核心目标重申、整体结论总览、3-5个非共识核心洞察、3条最高优先级顶层建议、价值与风险量化预判
- 排版：核心结论加粗主色标注，短句+项目符号，关键数据高亮色块突出

### 第一模块：项目定义、边界与分析方法论
- 必选内容：核心商业目标与权重分配、分析标的与边界界定、分析模型与方法论、数据来源与指标口径、报告限制与免责说明
- 可视化：矩阵图呈现分析维度权重分配，边界图明确标的范围
- **数据来源声明**：明确标注「所有专利数据来源：Patsnap全球专利数据库（检索日期：[日期]）」

### 第二模块：宏观产业与技术赛道环境分析
- 必选内容：PEST宏观影响分析、产业链格局与竞争分析、技术S曲线生命周期分析、赛道知识产权竞争规则分析
- 必配图表：产业链价值分布图、技术S曲线图、赛道专利申请趋势图、诉讼高发环节热力图
- **强制检索**：调用 `patsnap_search` 获取赛道专利申请趋势数据

**【检索式备注 - 第二模块示例】**
| 检索目的 | 检索策略 | 关键词 | IPC分类 | 申请人 | 时间范围 | 管辖地 | topk |
|----------|----------|--------|---------|--------|----------|--------|------|
| 赛道专利申请年度趋势 | keyword+filter | [技术领域核心词] | [赛道IPC] | — | 近10年 | CN/US/EP/WO | 100 |
| 主要申请人排名 | keyword+filter | [技术领域核心词] | [赛道IPC] | — | 近5年 | 全球 | 100 |
| 诉讼活跃度扫描 | keyword+filter | [技术关键词] | [赛道IPC] | — | 近3年 | US/EP | 50 |

### 第三模块：专利组合基础画像与全景拆解
- 必选内容：整体规模与结构画像、技术分布全景拆解、权利人与发明人结构分析、生命周期管理画像
- 必配图表：专利申请年度趋势图、地域分布地图、IPC技术领域分布饼图/树状图、法律状态结构图、剩余保护期分布图
- **强制检索**：目标企业全量专利检索

**【检索式备注 - 第三模块示例】**
| 检索目的 | 检索策略 | 关键词 | IPC分类 | 申请人 | 时间范围 | 管辖地 | topk |
|----------|----------|--------|---------|--------|----------|--------|------|
| 目标企业全量专利画像 | keyword+filter | [企业核心技术词] | — | [企业名称] | 全量 | 全球 | 100 |
| 技术分布拆解 | keyword+filter | [技术子领域词] | [细分IPC] | [企业名称] | 全量 | 全球 | 100 |
| 发明人贡献度分析 | filter | — | — | [企业名称] | 全量 | 全球 | 100 |
| 法律状态分布 | filter | — | — | [企业名称] | 全量 | 全球 | 100 |

### 第四模块：专利组合核心竞争力深度分析（核心模块）

#### 基础交付标准
- 必选内容：法律维度竞争力分析、技术维度竞争力分析、商业维度竞争力分析、**每件核心专利「技术问题→技术手段→技术功效」三要素技术拆解图**、组合协同效应与竞争力矩阵评估、核心高价值专利清单
- **权重规则**：法律30%、技术30%、商业40%（按客户诉求可调整，调整后三项合计须等于100%）
- **强制子技能调用**：novelty-check → non-obviousness-check → triz-analysis（串行执行）

#### 子技能调用流程

```
Step4执行流：

1. patsnap_search（核心专利检索，topk=20，精准筛选）
   ↓
2. patsnap_fetch（全文读取top 3-8件核心专利）
   ↓
3. 【新增·V3.0】技术问题→技术手段→技术功效 三要素提取
   → 从摘要/权利要求/说明书中提取三要素
   → 生成每件专利的HTML可视化技术拆解卡片
   ↓
4. novelty-check（新颖性分析）
   → 输入：主权利要求 + 申请日 + 管辖地
   → 输出：novelty_report.md + claim_diff_matrix.md
   ↓
5. non-obviousness-check（创造性分析，仅对novelty_preserved专利）
   → 输入：novelty-check全部输出物
   → 输出：inventive_step_report.md
   ↓
6. triz-analysis（技术创新点与矛盾分析）
   → 输入：核心专利技术特征 + 竞对技术对比差距
   → 输出：3条解决路径 + 推荐方案
   ↓
7. 汇总写入报告第四模块
```

---

## ══════════════════════════════════
## 【V3.0新增核心规范】每件专利技术拆解图
## ══════════════════════════════════

### 一、三要素定义与提取规则

每件核心专利必须完整提取以下三个要素，**内容必须来自 `patsnap_fetch` 全文读取**，不得基于专利名称凭空推断：

| 要素 | 定义 | 提取来源 | 字数要求 |
|------|------|----------|----------|
| **技术问题** | 该专利所要解决的现有技术存在的缺陷、不足或挑战 | 背景技术段落 + 发明内容第一段 | 50-100字 |
| **技术手段** | 专利采用的具体技术方案、结构设计或方法步骤（对应独立权利要求核心特征） | 权利要求书独立项 + 说明书具体实施方式 | 100-200字，分条列举 |
| **技术功效** | 采用上述技术手段后实现的有益效果、性能提升或指标改善 | 发明内容「有益效果」段 + 说明书效果描述 | 50-100字，优先量化 |

**提取质量规则**：
- 技术问题：必须明确指出现有技术的具体痛点，不得泛化描述为「提高性能」
- 技术手段：必须分条列举核心技术特征（至少3条），每条对应一个独立技术特征
- 技术功效：优先引用专利文本中的量化数据（如「效率提升X%」「重量减少Y%」），无量化数据时描述定性改善

### 二、HTML可视化技术拆解卡片规范

每件核心专利的技术拆解图以HTML卡片形式渲染，嵌入报告第四模块每件专利分析项下。

#### 标准卡片结构

```html
<!-- 专利技术拆解卡片 - 单件专利 -->
<div class="patent-breakdown-card" style="
  border: 1px solid #003366;
  border-radius: 8px;
  margin: 24px 0;
  overflow: hidden;
  font-family: 'Microsoft YaHei', sans-serif;
  box-shadow: 0 2px 8px rgba(0,51,102,0.10);
">
  <!-- 卡片标题栏 -->
  <div class="card-header" style="
    background: linear-gradient(135deg, #003366 0%, #0055A4 100%);
    color: white;
    padding: 14px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  ">
    <div>
      <span style="font-size:13px;opacity:0.85;">专利号</span>
      <span style="font-size:16px;font-weight:700;margin-left:10px;">[专利号]</span>
    </div>
    <div style="font-size:14px;font-weight:600;">[专利名称（不超过30字）]</div>
    <div style="font-size:12px;opacity:0.85;">申请日：[日期] | 法律状态：[状态]</div>
  </div>

  <!-- 三要素主体区 -->
  <div class="card-body" style="display:flex;min-height:160px;">

    <!-- 技术问题 -->
    <div class="breakdown-item problem" style="
      flex:1;
      padding:18px 20px;
      background:#FFF8F0;
      border-right:1px solid #E8E8E8;
      position:relative;
    ">
      <div style="
        display:inline-block;
        background:#E84040;
        color:white;
        font-size:11px;
        font-weight:700;
        padding:3px 10px;
        border-radius:12px;
        margin-bottom:10px;
        letter-spacing:1px;
      ">⚠ 技术问题</div>
      <div style="font-size:13px;color:#333;line-height:1.7;">
        [从背景技术段提取的现有技术缺陷描述，50-100字]
      </div>
    </div>

    <!-- 箭头连接符 -->
    <div style="
      width:40px;
      display:flex;
      align-items:center;
      justify-content:center;
      background:#F5F8FF;
      color:#0055A4;
      font-size:20px;
      font-weight:bold;
    ">→</div>

    <!-- 技术手段 -->
    <div class="breakdown-item solution" style="
      flex:1.5;
      padding:18px 20px;
      background:#F0F6FF;
      border-right:1px solid #E8E8E8;
      position:relative;
    ">
      <div style="
        display:inline-block;
        background:#0055A4;
        color:white;
        font-size:11px;
        font-weight:700;
        padding:3px 10px;
        border-radius:12px;
        margin-bottom:10px;
        letter-spacing:1px;
      ">⚙ 技术手段</div>
      <ul style="font-size:13px;color:#333;line-height:1.8;margin:0;padding-left:18px;">
        <li>[核心技术特征1，对应独立权利要求特征点]</li>
        <li>[核心技术特征2，对应独立权利要求特征点]</li>
        <li>[核心技术特征3，对应独立权利要求特征点]</li>
        <!-- 可增至5条 -->
      </ul>
    </div>

    <!-- 箭头连接符 -->
    <div style="
      width:40px;
      display:flex;
      align-items:center;
      justify-content:center;
      background:#F5F8FF;
      color:#0055A4;
      font-size:20px;
      font-weight:bold;
    ">→</div>

    <!-- 技术功效 -->
    <div class="breakdown-item effect" style="
      flex:1;
      padding:18px 20px;
      background:#F0FFF4;
      position:relative;
    ">
      <div style="
        display:inline-block;
        background:#1A8A3A;
        color:white;
        font-size:11px;
        font-weight:700;
        padding:3px 10px;
        border-radius:12px;
        margin-bottom:10px;
        letter-spacing:1px;
      ">✓ 技术功效</div>
      <div style="font-size:13px;color:#333;line-height:1.7;">
        [从有益效果段提取，优先量化，50-100字]
      </div>
      <!-- 量化指标高亮块（有量化数据时必加） -->
      <div style="
        margin-top:10px;
        background:#003366;
        color:white;
        font-size:12px;
        font-weight:700;
        padding:6px 12px;
        border-radius:6px;
        display:inline-block;
      ">[核心量化指标，如：效率↑20% / 重量↓15%]</div>
    </div>

  </div>

  <!-- 卡片底部：商业价值洞察 -->
  <div class="card-footer" style="
    background:#F8FAFF;
    border-top:1px solid #DDE8F5;
    padding:12px 20px;
    display:flex;
    align-items:center;
    gap:16px;
  ">
    <span style="font-size:12px;color:#666;">💡 核心洞察：</span>
    <span style="font-size:13px;color:#003366;font-weight:600;">
      [该专利的核心竞争价值一句话总结，链接至商业场景]
    </span>
    <span style="margin-left:auto;font-size:12px;">
      新颖性：<strong style="color:[颜色]">[结论]</strong> ｜
      创造性：<strong style="color:[颜色]">[结论]</strong> ｜
      战略价值：<strong style="color:#003366">[⭐数]</strong>
    </span>
  </div>
</div>
```

#### 三要素拆解图整体汇总视图（模块级）

在第四模块开头，在逐件展示前，先渲染一张**汇总对比表**，横向比较所有核心专利的三要素关键词：

```html
<!-- 核心专利三要素汇总对比表 -->
<div style="overflow-x:auto;margin:24px 0;">
  <table style="
    width:100%;
    border-collapse:collapse;
    font-family:'Microsoft YaHei',sans-serif;
    font-size:13px;
  ">
    <thead>
      <tr style="background:#003366;color:white;">
        <th style="padding:12px 16px;text-align:left;width:130px;">专利号</th>
        <th style="padding:12px 16px;text-align:left;width:180px;">专利名称</th>
        <th style="padding:12px 16px;text-align:left;background:#C0392B;width:220px;">⚠ 技术问题（核心痛点）</th>
        <th style="padding:12px 16px;text-align:left;background:#0055A4;width:260px;">⚙ 技术手段（关键创新）</th>
        <th style="padding:12px 16px;text-align:left;background:#1A8A3A;width:200px;">✓ 技术功效（量化收益）</th>
        <th style="padding:12px 16px;text-align:center;width:80px;">战略价值</th>
      </tr>
    </thead>
    <tbody>
      <!-- 每件核心专利一行，交替底色 -->
      <tr style="background:#F8FAFF;">
        <td style="padding:10px 16px;color:#003366;font-weight:700;">[专利号]</td>
        <td style="padding:10px 16px;">[专利名称]</td>
        <td style="padding:10px 16px;color:#333;">[技术问题关键词，20字内]</td>
        <td style="padding:10px 16px;color:#333;">[技术手段关键词，3条bullet，每条10字内]</td>
        <td style="padding:10px 16px;"><span style="background:#E8F5E9;color:#1A8A3A;padding:3px 8px;border-radius:4px;font-weight:600;">[功效量化指标]</span></td>
        <td style="padding:10px 16px;text-align:center;">[⭐数]</td>
      </tr>
      <!-- 更多行... -->
    </tbody>
  </table>
</div>
```

### 三、提取流程规范（Step4内嵌SOP）

```
对每件核心专利，按以下顺序提取三要素：

Step4-A：调用 patsnap_fetch 获取专利全文 Markdown
  → 重点读取：【背景技术】【发明内容】【权利要求书】【有益效果】四个段落

Step4-B：技术问题提取
  → 定位「背景技术」段中「现有技术存在以下问题/缺陷/不足」附近的文字
  → 若找不到明确问题陈述，转至「发明内容」第一段的「本发明为了解决…」
  → 提取50-100字，保留原文关键词，不得改写为泛化描述

Step4-C：技术手段提取
  → 定位独立权利要求（Claim 1）全文
  → 按前序部分/特征部分拆分，提取特征部分中的核心技术特征
  → 整理为3-5条bullet，每条对应一个独立技术特征，100-200字总计
  → 若独立权利要求过长（>300字），从说明书「技术方案」段补充提炼

Step4-D：技术功效提取
  → 定位「有益效果」或「发明内容」末段的效果描述
  → 优先提取含量化数据的句子（百分比、具体数值、对比数据）
  → 无量化数据时提取定性改善描述，提炼为50-100字
  → 高亮量化指标（作为卡片底部指标块内容）

Step4-E：渲染HTML卡片
  → 填充上述三要素内容到标准卡片模板
  → 补充专利号、专利名称、申请日、法律状态
  → 待novelty-check/non-obviousness-check完成后，补填底部稳定性结论
```

### 四、技术拆解图质量自检清单

在Step10质量自检时，对每张技术拆解图执行以下检查：

- [ ] 技术问题有明确的现有技术痛点描述，非泛化表述
- [ ] 技术手段分条列举≥3条独立技术特征
- [ ] 技术功效含量化指标（或注明「原文无量化数据」）
- [ ] 三要素内容均来自patsnap_fetch全文，非训练数据推断
- [ ] 卡片底部新颖性/创造性结论已填写
- [ ] 汇总对比表已生成，条目与逐件卡片一致

---

**【检索式备注 - 第四模块示例】**
| 检索目的 | 检索策略 | 关键词 | IPC分类 | 申请人 | 时间范围 | 管辖地 | topk |
|----------|----------|--------|---------|--------|----------|--------|------|
| 核心专利筛选（高被引/高价值） | keyword+filter | [企业核心技术词] | [精细IPC] | [企业名称] | 全量 | 全球 | 20 |
| 新颖性检索（D1候选） | semantic+keyword | [主权利要求技术特征描述] | [专利IPC] | — | 早于申请日 | 全球 | 20 |
| 创造性检索（D1+D2组合） | semantic+keyword | [区别技术特征描述] | [相关IPC] | — | 早于申请日 | 全球 | 20 |
| TRIZ技术矛盾检索 | semantic | [技术矛盾自然语言描述] | — | — | 全量 | 全球 | 10 |

### 第五模块：对标主体专利与战略对比分析
- 必选内容：对标主体筛选规则、基础盘量化对标、技术布局与研发战略对标、专利运营与竞争战略对标、差距总结与机会/威胁识别
- 必配图表：对标雷达图、专利数量与质量对标柱状图、技术覆盖度对标矩阵、研发投入产出比对标表
- **强制检索**：对每个竞对主体分别执行独立检索轮次

**【检索式备注 - 第五模块示例】**
| 检索目的 | 检索策略 | 关键词 | IPC分类 | 申请人 | 时间范围 | 管辖地 | topk |
|----------|----------|--------|---------|--------|----------|--------|------|
| 竞对1全量专利画像 | keyword+filter | [竞对核心技术词] | — | [竞对1名称] | 全量 | 全球 | 100 |
| 竞对2全量专利画像 | keyword+filter | [竞对核心技术词] | — | [竞对2名称] | 全量 | 全球 | 100 |
| 技术布局重叠度分析 | keyword+filter | [共同技术领域词] | [共同IPC] | [目标企业,竞对1,竞对2] | 全量 | 全球 | 100 |
| 近期研发动向 | keyword+filter | [新兴技术词] | — | [竞对1, 竞对2] | 近6个月 | 全球 | 50 |
| 隐形差距点扫描 | semantic+filter | [竞对优势技术描述] | [相关IPC] | [竞对名称] | 近3年 | 全球 | 30 |

### 第六模块：专利组合商业价值评估与量化测算
- 必选内容：评估前提与方法选择、核心评估模型构建与量化测算、多场景价值增量测算、敏感性分析与情景测算
- 核心方法：以收益法为核心，辅以市场法、成本法
- 必配图表：价值测算模型表、情景价值区间柱状图、敏感性分析tornado图
- **强制检索**：许可/交易参考案例检索

**【检索式备注 - 第六模块示例】**
| 检索目的 | 检索策略 | 关键词 | IPC分类 | 申请人 | 时间范围 | 管辖地 | topk |
|----------|----------|--------|---------|--------|----------|--------|------|
| 同领域许可/收购参考案例 | keyword | [技术领域词, 专利许可, 技术转让] | [赛道IPC] | — | 近5年 | 全球 | 20 |
| 高引用核心专利价值锚定 | keyword+filter | [核心技术词] | [精细IPC] | [企业名称] | 全量 | 全球 | 10 |

### 第七模块：核心风险识别与情景应对预案
- 必选内容：风险分级标准、全维度风险识别拆解、高风险项情景应对预案、风险缓释体系建设方案（**含triz-analysis工程矛盾解法**）、整体风险等级评估
- 风险矩阵：「发生概率×影响程度」分级，高风险项给出「事前预防、事中应对、事后补救」全流程预案
- 必配图表：风险矩阵热力图、高风险项应对预案表
- **强制子技能调用**：对「技术规避可行性」高风险项，调用 triz-analysis 输出工程矛盾解法

**【检索式备注 - 第七模块示例】**
| 检索目的 | 检索策略 | 关键词 | IPC分类 | 申请人 | 时间范围 | 管辖地 | topk |
|----------|----------|--------|---------|--------|----------|--------|------|
| 无效风险检索 | semantic+keyword | [权利要求核心技术特征] | [专利IPC] | — | 早于申请日 | 全球 | 20 |
| 竞对攻击性专利扫描 | keyword+filter | [目标企业核心产品技术词] | [相关IPC] | [竞对名称] | 近3年 | CN/US/EP | 30 |
| FTO风险扫描 | keyword+filter | [核心产品/技术词] | [产品IPC] | — | 全量(有效) | 目标市场 | 50 |

### 第八模块：战略落地建议与行动路线图
- 必选内容：顶层战略定位（**SCQA叙事框架**）、核心战略举措拆解、分阶段行动路线图、资源投入与KPI考核体系、预期成果与价值增量预判
- 必配图表：举措优先级矩阵、3年行动路线甘特图、资源投入与ROI测算表
- **强制子技能调用**：借用 patsnap-mckinsey-sales-insight 的 SCQA + 竞争对标逻辑重构战略叙事

**SCQA战略叙事结构（必须）**：
- **S（现状）**：用Patsnap检索数据描述企业当前专利组合态势
- **C（冲突）**：揭示竞对已在关键领域完成卡位，企业面临的具体威胁
- **Q（核心问题）**：企业最紧迫的专利战略决策问题
- **A（核心答案）**：本报告的顶层战略建议（结论先行）

---

## HTML报告输出规范

### 全局样式规范
- 主色调：麦肯锡深蓝 `#003366`
- 辅助色：`#0055A4`（中蓝）、`#E84040`（风险红）、`#1A8A3A`（功效绿）、`#F5A623`（预警橙）
- 字体：`'Microsoft YaHei', 'PingFang SC', sans-serif`
- 输出为**单一自包含HTML文件**，所有样式内联或写入`<style>`标签，不依赖外部CDN
- 分辨率适配：1200px宽度优先，兼容打印（`@media print`）

### 技术拆解卡片全局样式（写入`<style>`）

```css
.patent-breakdown-card {
  border: 1px solid #003366;
  border-radius: 8px;
  margin: 24px 0;
  overflow: hidden;
  font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
  box-shadow: 0 2px 8px rgba(0,51,102,0.10);
  page-break-inside: avoid;
}
.patent-breakdown-card .card-body {
  display: flex;
  min-height: 160px;
}
.breakdown-item {
  flex: 1;
  padding: 18px 20px;
}
.breakdown-item.problem { background: #FFF8F0; border-right: 1px solid #E8E8E8; }
.breakdown-item.solution { flex: 1.5; background: #F0F6FF; border-right: 1px solid #E8E8E8; }
.breakdown-item.effect { background: #F0FFF4; }
.breakdown-arrow {
  width: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #F5F8FF;
  color: #0055A4;
  font-size: 20px;
  font-weight: bold;
}
.tag-problem { background: #E84040; color: white; font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 12px; display: inline-block; margin-bottom: 10px; }
.tag-solution { background: #0055A4; color: white; font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 12px; display: inline-block; margin-bottom: 10px; }
.tag-effect { background: #1A8A3A; color: white; font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 12px; display: inline-block; margin-bottom: 10px; }
.kpi-badge { background: #003366; color: white; font-size: 12px; font-weight: 700; padding: 6px 12px; border-radius: 6px; display: inline-block; margin-top: 10px; }
@media print {
  .patent-breakdown-card { page-break-inside: avoid; box-shadow: none; }
}
```

---

## 场景定制化权重规范

| 场景 | 商业维度 | 技术维度 | 法律维度 | 技术拆解图重点 |
|------|---------|---------|---------|----------------|
| IPO尽调 | 40% | 30% | 30% | 技术功效量化指标 + 法律稳定性 |
| 并购估值 | 50% | 25% | 25% | 商业价值映射 + 技术功效 |
| 研发战略 | 20% | 60% | 20% | 技术手段细节 + TRIZ延伸路径 |
| 337诉讼 | 30% | 20% | 50% | 权利要求特征逐条 + 侵权比对 |
| 企业出海 | 35% | 25% | 40% | 技术功效国际对标 + FTO风险 |

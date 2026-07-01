---
name: patent-pre-filing-assessment
description: |
  专利申请前评估技能。输入技术交底书或专利号，自动执行四大维度（法律可专利性、技术质量、市场价值、战略布局）系统性评估，输出含综合结论（建议积极申请/优化后申请/谨慎暂缓/不建议申请）的可视化HTML报告，依据可溯源至国知局标准与GB/T 42748-2023。可专利性（新颖性+创造性）模块使用 novelty-check 技能规范流程执行。
---

# 专利申请前评估技能

## 定位与触发

**触发词**：申请前评估、专利申请前、值不值得申请、要不要申请专利、专利预评估、pre-filing assessment

**适用场景**：
- 研发人员完成技术交底后，判断是否值得申请专利
- 企业/高校知识产权部门对技术成果进行申请前把关
- 新技术方案在正式提交前的系统性风险评估

**不适用场景**：
- 已授权专利的价值评级（请使用 patent-classification 技能）
- 纯市场竞品研究（无具体技术方案）
- 单一权利要求深度新颖性专项论证（请移交 novelty-check 独立执行）

---

## 评估框架来源

依据以下官方标准统一梳理：
- 国家知识产权局三部门意见
- GB/T 42748-2023《专利评估指引》
- 各省市专利申请前评估工作指引
- 高校知识产权管理规范
- novelty-check 技能规范（cn-novelty / claim-decomposition / search-strategy）

---

## 七步工作流

### Step 1 — 输入信息采集

接收用户输入，可为以下任一形式：
1. **技术交底书**（Word/PDF 上传）
2. **专利号**（已有申请，补充评估）
3. **技术描述文本**（直接粘贴描述）

若用户仅提供专利号，则调用 `patent.fetch` 获取摘要、权利要求、说明书作为评估基础。

同时确认以下最低输入要求（来自 novelty-check 规范）：
- 技术方案文本或权利要求草稿
- 预计申请日期或优先权日期范围
- 目标申请国（默认中国 CN）

---

### Step 2 — 权利要求要素拆解（novelty-check · claim-decomposition）

> 本步骤执行 novelty-check 技能的 claim-decomposition 规范，为新颖性与创造性分析奠定基础。

**操作流程**：
1. 从技术方案中提取或重构独立权利要求草稿（方法独立项 + 系统/装置独立项）
2. 将每条独立权利要求拆解为要素列表，逐项编号：`E1`、`E2`、`E3`…
3. 对每个要素记录：

| 字段 | 内容 |
|------|------|
| 要素ID | E1、E2… |
| 文本 | 要素原文 |
| 类型 | 结构型 / 功能型 / 参数型 / 步骤型 |
| 关键变体/同义词 | 检索替换用语 |
| 数值范围或阈值 | 精确记录单位与端点 |
| 检索锚点 | 拟用于检索的核心术语 |

**红线禁忌**（来自 novelty-check 规范）：
- 禁止将多个限制条件捆绑为单一要素
- 禁止丢弃数值单位或阈值
- 不确定是否为限制性前序时，须显式标注，不得静默删除
- 结果语言不得与机制语言混同

产出物：`claim_elements`（内联表格形式，写入评估报告 Step 2 节）

---

### Step 3 — 新颖性检索与逐要素比对（novelty-check · search-strategy + cn-novelty）

> 本步骤执行 novelty-check 技能的三轮检索策略与单一文件比对原则，依据《专利法》第22条。

#### 三轮检索策略

**第一轮：宽网广域召回**
- 使用独立权利要求核心术语，不加重度日期/申请人过滤
- 调用 `patent.search` 覆盖 CNIPA、USPTO、EPO 等主要局
- 目的：识别 IPC/CPC 分类、行业惯用术语、高频关键词

**第二轮：按高风险要素收敛**
- 对第一轮中覆盖率最高的候选文件，按难以定位的要素单独拆分查询
- 加入机制术语、参数范围、分类号辅助
- 优先召回与技术目的相近的文件

**第三轮：缺口填补**
- 针对仍未覆盖的要素补充检索
- 利用引文链、同族成员、申请人组合查询
- 必要时使用 `web.search` 验证公开使用、产品发布、行业标准披露

**停止检索条件**（来自 novelty-check 规范）：
- 已找到一篇或多篇强 D1 候选文件
- 最高风险要素已在候选池中有代表性文件
- 新增查询主要返回重复或低质量结果
- 若召回仍弱，须在报告中标注缺口，不得假设召回完整

#### 候选文件追踪

对每篇候选文件记录：来源ID、公开日期、国别、相关原因、覆盖要素列表、获取状态。

#### 逐要素比对（单一文件原则）

对每篇候选文件，逐要素判定为以下四种状态之一：

| 状态 | 含义 |
|------|------|
| `matched` 🟢 | 明确披露，有直接文本支持 |
| `partial` 🟡 | 部分覆盖或语义近似，须进一步确认 |
| `missing` 🔴 | 文件中不存在该要素 |
| `uncertain` ⚪ | 无法确定（文件不可读/隐含披露缺乏推理链） |

**隐含披露**须附推理链；**固有披露**须满足必然性而非仅有可能性。

#### 新颖性结论规范（中国 CN，《专利法》第22条）

| 结论 | 触发条件 |
|------|---------|
| `novelty_rejected`（无新颖性） | **一篇文件**涵盖全部要素（均为 `matched`），且均在申请日前公开 |
| `novelty_preserved`（具备新颖性） | 所有已审查文件均有至少一个 `missing` 要素 |
| `uncertain`（不确定） | 管辖未锁定、申请日未明确、文件不可读、公开日期存疑 |

**强制规则**：
- 禁止拼接多篇文件来判定无新颖性
- 抵触申请（申请日前提交、申请日后公开）须单独标注，不得与普通现有技术混用
- D1 中任何要素仍为 `missing`/`partial`/`uncertain` 时，不得写 `novelty_rejected`

产出物：`claim_diff_matrix`（D1 逐要素对比表，写入评估报告 Step 3 节，含四色标注）

---

### Step 4 — 创造性评估（novelty-check · 三步法 + 非显而易见性判断）

> 本步骤在 Step 3 新颖性结论基础上，依据《专利法》第22条第3款执行"三步法"创造性评估。

#### 前提条件
- 仅在 `novelty_preserved` 结论下执行创造性评估
- 若新颖性结论为 `novelty_rejected`，直接跳转至模块一结论，判定"无专利性"
- 若新颖性结论为 `uncertain`，创造性评估结论同步降级为 `uncertain`

#### 三步法执行流程

**第一步：确定最接近现有技术（D1）**
- 以 Step 3 claim_diff_matrix 中 `matched` 要素最多的文件为 D1
- 若有两篇文件 `matched` 数量相同，选择技术目的最接近者
- 记录 D1 文件号、标题、公开日期

**第二步：确定区别技术特征与客观技术问题**
- 从 claim_diff_matrix 中提取所有 `missing` / `partial` 要素，即区别技术特征
- 分析区别技术特征所解决的客观技术问题（而非申请人主观声称的效果）
- 区分"实际解决的技术问题"与"说明书声称的技术效果"，不得直接引用后者

**第三步：非显而易见性判断**
- 检索是否存在 D2/D3 文件公开了区别技术特征，或该特征属于本领域公知常识
- 判断本领域技术人员是否有技术启示将 D2/D3 与 D1 结合
- 排除后见之明（hindsight）：判断须基于申请日前的技术状态
- 若区别技术特征在现有技术中有直接映射且有结合动机，则判定创造性不足
- 若区别技术特征产生了预料不到的技术效果，须在报告中明确记录

#### 创造性结论

| 结论 | 触发条件 |
|------|---------|
| `inventive_step_present`（具备创造性） | 区别特征无法从现有技术显而易见地获得，或产生了预料不到的技术效果 |
| `inventive_step_weak`（创造性不足） | 区别特征可从 D2/D3 或公知常识中获得，且有结合动机 |
| `inventive_step_absent`（无创造性） | 区别特征为本领域惯用手段替换或直接公知常识 |
| `uncertain` | 证据不足、D2/D3 未检索完整、或新颖性本身为 uncertain |

#### 创造性与新颖性移交规则

当创造性争议涉及 D1+D2 组合显而易见性、结合动机深度分析、二次考量因素时，须将以下材料移交 `novelty-check` 或 `non-obviousness-check` 技能深化处理：
- `claim_elements`
- `claim_diff_matrix`
- D1 候选文件清单
- 新颖性报告结论

---

### Step 5 — 模块一综合：法律可专利性评估（基础准入维度）

汇总 Step 2–4 产出，完成模块一全部 6 项指标评估：

| # | 二级指标 | 评估依据 | 输出结果选项 |
|---|---------|---------|------------|
| 1 | 专利客体适格性 | 《专利法》第2、25条；是否属于排除客体 | 合格 / 不合格（直接否决） |
| 2 | 新颖性 | Step 3 结论（`novelty_preserved` / `novelty_rejected` / `uncertain`） | 具备新颖性 / 无新颖性 / 不确定 |
| 3 | 创造性 | Step 4 结论（三步法 + 非显而易见性） | 具备创造性 / 创造性不足 / 无创造性 / 不确定 |
| 4 | 实用性 | 能否制造或使用、能否产生积极效果、是否纯理论设想 | 具备实用性 / 无实用性 |
| 5 | 在先权利与保密风险 | 提前发表、预印、结题公开、合作泄密记录 | 无风险 / 存在提前公开风险 / 存在权属纠纷风险 |
| 6 | 权属清晰度 | 研发立项协议、合作合同、职务发明认定 | 权属清晰 / 权属待定 / 存在共有争议 |

**否决触发**：客体不适格 或 `novelty_rejected` → 模块一 0 分，结论直接为"不建议申请"。

---

### Step 6 — 模块二至四评估（技术质量 / 市场价值 / 战略布局）

#### 模块二：技术质量与完备性（满分25分）

| # | 二级指标 | 输出结果选项 |
|---|---------|------------|
| 1 | 技术方案完整度 | 方案完整 / 缺失核心技术特征 / 仅概念无落地方案 |
| 2 | 技术先进性 | 国际领先 / 国内领先 / 行业常规 / 落后现有技术 |
| 3 | 技术可替代性 | 不可替代 / 低可替代 / 高可替代 |
| 4 | 技术成熟度（TRL） | TRL1-3（理论）/ TRL4-6（试验）/ TRL7-9（产业化） |
| 5 | 技术迭代延伸空间 | 可多维度布局 / 仅单点技术 / 无迭代空间 |

#### 模块三：市场与经济价值（满分25分）

| # | 二级指标 | 输出结果选项 |
|---|---------|------------|
| 1 | 应用行业与市场规模 | 高市场空间 / 中等 / 小众无市场 |
| 2 | 产业化落地前景 | 可短期产业化 / 中长期落地 / 无法产业化 |
| 3 | 许可转让变现潜力 | 高变现潜力 / 一般 / 无转让许可价值 |
| 4 | FTO 风险 | 无风险 / 局部侵权风险 / 高侵权风险 |
| 5 | 投入产出性价比 | 投入产出合理 / 成本过高 |
| 6 | 政策与项目适配性 | 高度适配 / 一般适配 / 无政策价值 |

辅助工具：`web.search` 查行业市场数据、政策文件

#### 模块四：战略布局与管理（满分20分）

| # | 二级指标 | 输出结果选项 |
|---|---------|------------|
| 1 | 专利布局必要性 | 必须布局 / 选择性布局 / 无需布局 |
| 2 | 申请类型适配性 | 发明专利 / 实用新型 / 外观设计 / 组合布局 |
| 3 | 申请地域布局需求 | 仅国内 / 国内+PCT重点国家 / 暂缓海外 |
| 4 | 维护年限意愿 | 长期（10-20年）/ 短期（3-5年）/ 无需长期维护 |
| 5 | 合规与科研管理要求 | 符合内部管理要求 / 需补充材料 |

---

### Step 7 — 综合结论输出 + HTML报告生成

#### 综合评分逻辑

| 模块 | 满分 | 备注 |
|------|------|------|
| 模块一（法律可专利性） | 30 | 客体不适格或无新颖性 → 0分触发直接否决 |
| 模块二（技术质量） | 25 | — |
| 模块三（市场价值） | 25 | — |
| 模块四（战略布局） | 20 | — |
| **合计** | **100** | — |

#### 四类官方标准结论

| 结论 | 触发条件 | 后续行动 |
|------|---------|---------|
| ✅ 建议积极申请 | 法律无瑕疵、技术先进、市场价值高、战略必须布局 | 直接启动申报 |
| 🔧 建议优化后申请 | 存在部分瑕疵（交底不全、新颖性瑕疵、权属待补） | 补正完善后再申请 |
| ⚠️ 谨慎暂缓申请 | 创造性不足、市场空间小、可替代性高 | 观望或转技术秘密保护 |
| ❌ 不建议申请 | 无专利性/无新颖性/无实用性/权属纠纷/无任何价值 | 改为技术秘密/论文发表 |

---

#### HTML报告完整结构规范

> ⚠️ **样式分区**：
> - **模块1（表头）和模块2（综合评价）**：🔒 样式锁定，严格遵照下方规范，**禁止改动**。
> - **模块3–10**：按上传参考版（novelty-check融合版 v2.0）的 CSS 类体系和 HTML 结构输出。

---

##### 【模块1 — 表头/页眉横幅】🔒 样式锁定

**必须完全复现以下 HTML 结构与样式，不得改动：**

```html
<!-- 表头横幅 -->
<div style="
  background: linear-gradient(135deg, #1a237e 0%, #283593 40%, #3949ab 70%, #5c6bc0 100%);
  border-radius: 16px;
  padding: 32px 40px;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
">
  <!-- 左侧图标 -->
  <div style="
    width: 56px; height: 56px;
    background: rgba(255,255,255,0.15);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 28px; flex-shrink: 0;
  ">📋</div>
  <!-- 右侧文字区 -->
  <div>
    <div style="
      font-size: 26px; font-weight: 700;
      color: #ffffff; letter-spacing: 1px;
      margin-bottom: 10px;
    ">专利申请前评估报告</div>
    <div style="color: rgba(255,255,255,0.85); font-size: 13px; margin-bottom: 4px;">
      <span style="opacity:0.7">技术名称：</span>{{技术名称}}
    </div>
    <div style="color: rgba(255,255,255,0.85); font-size: 13px;">
      <span style="opacity:0.7">评估日期：</span>{{评估日期}}
      <span style="margin: 0 8px; opacity:0.5">|</span>
      <span style="opacity:0.7">依据标准：</span>国知局三部门意见 + GB/T 42748-2023
    </div>
  </div>
</div>
```

**填充规则**：
- `{{技术名称}}`：从用户输入的技术方案标题或发明名称中提取
- `{{评估日期}}`：使用当前日期，格式 `YYYY-MM-DD`
- 渐变色固定为 `#1a237e → #283593 → #3949ab → #5c6bc0`（深蓝到蓝紫，135deg）
- 图标固定为 📋，禁止替换为其他 emoji 或 SVG
- 字体无衬线（`font-family: -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif`）

---

##### 【模块2 — 综合评价卡】🔒 样式锁定

**必须完全复现以下 HTML 结构与样式，不得改动：**

```html
<!-- 综合评价卡 -->
<div style="
  background: #ffffff;
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 24px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
">
  <!-- 顶部结论胶囊按钮 -->
  <div style="margin-bottom: 12px;">
    <span style="
      display: inline-flex; align-items: center; gap: 8px;
      background: {{结论色}};
      color: #fff; font-size: 16px; font-weight: 700;
      padding: 10px 24px; border-radius: 50px;
    ">{{结论图标}} {{结论文字}}</span>
  </div>
  <!-- 综合得分行 -->
  <div style="font-size: 15px; color: #333; margin-bottom: 16px;">
    综合得分：<span style="font-size: 22px; font-weight: 700; color: #333;">{{总分}}</span>
    <span style="color: #888;"> / 100 分</span>
  </div>
  <!-- 评价说明段落 -->
  <div style="font-size: 14px; color: #555; line-height: 1.8; margin-bottom: 24px;">
    {{评价说明文字}}
  </div>
  <!-- 下部两列：环形图 + 档位说明 -->
  <div style="display: flex; align-items: center; gap: 40px;">
    <!-- 左：环形得分图（SVG） -->
    <div style="position: relative; width: 120px; height: 120px; flex-shrink: 0;">
      <svg width="120" height="120" viewBox="0 0 120 120">
        <circle cx="60" cy="60" r="50" fill="none" stroke="#e8e8e8" stroke-width="12"/>
        <circle cx="60" cy="60" r="50" fill="none" stroke="{{环形色}}"
          stroke-width="12" stroke-linecap="round"
          stroke-dasharray="{{弧长}} 314"
          stroke-dashoffset="78.5"
          transform="rotate(-90 60 60)"/>
      </svg>
      <div style="
        position: absolute; top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
      ">
        <div style="font-size: 26px; font-weight: 700; color: #333;">{{总分}}</div>
        <div style="font-size: 11px; color: #888;">/100</div>
      </div>
    </div>
    <!-- 右：档位说明列表 -->
    <div style="flex: 1;">
      <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px; font-size: 13px; color: #555;">
        <span style="color: #4caf50; font-size: 16px;">✅</span>
        建议积极申请 ≥ 80分
        {{#当前为积极申请}}<span style="color:#4caf50; font-weight:700;">← 当前</span>{{/当前为积极申请}}
      </div>
      <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px; font-size: 13px; color: #555;">
        <span style="font-size: 16px;">🔧</span>
        建议优化后申请 60–79分
        {{#当前为优化后申请}}<span style="color:#f57c00; font-weight:700;">← 当前</span>{{/当前为优化后申请}}
      </div>
      <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px; font-size: 13px; color: #555;">
        <span style="font-size: 16px;">⚠️</span>
        谨慎暂缓申请 40–59分
        {{#当前为暂缓}}<span style="color:#f9a825; font-weight:700;">← 当前</span>{{/当前为暂缓}}
      </div>
      <div style="display: flex; align-items: center; gap: 10px; font-size: 13px; color: #555;">
        <span style="font-size: 16px;">❌</span>
        不建议申请 &lt; 40分
        {{#当前为不建议}}<span style="color:#e53935; font-weight:700;">← 当前</span>{{/当前为不建议}}
      </div>
    </div>
  </div>
</div>
```

**动态填充规则**：

| 占位符 | 填充规则 |
|--------|----------|
| `{{总分}}` | 四模块实际得分合计（整数） |
| `{{结论文字}}` | 建议积极申请 / 建议优化后申请 / 谨慎暂缓申请 / 不建议申请 |
| `{{结论图标}}` | ✅ / 🔧 / ⚠️ / ❌ |
| `{{结论色}}` | `#43a047`（积极）/ `#f57c00`（优化）/ `#f9a825`（暂缓）/ `#e53935`（不建议） |
| `{{环形色}}` | 与结论色保持一致 |
| `{{弧长}}` | `总分 / 100 * 314`（保留1位小数） |
| `{{评价说明文字}}` | 本次评估的一句总体结论 + "主要风险：①②③" 编号列表 + 建议行动 |
| `← 当前` 标注 | 仅在当前档位所在行显示，颜色与结论色一致 |

**样式约束**：
- 白色卡片背景 `#ffffff`，圆角 `16px`，阴影 `0 2px 12px rgba(0,0,0,0.06)`
- 结论胶囊按钮两端圆角 `border-radius: 50px`
- 得分大字 `font-size: 22px; font-weight: 700`，`/100 分` 用灰色小字
- 环形图直径固定 120px，底环颜色 `#e8e8e8`，进度环颜色随结论动态变化
- "← 当前" 标注颜色与该档位结论色一致
- 禁止修改卡片整体圆角、阴影、字号体系

---

##### 【模块3–10 — novelty-check融合版 v2.0 输出规范】

> 模块3–10 严格按照上传参考版（novelty-check融合版 v2.0）的 CSS 类体系和 HTML 结构输出，不得改用其他样式。

**CSS 变量与类体系（引用自参考版）**：

```css
:root{--green:#16a34a;--yellow:#ca8a04;--red:#dc2626;--gray:#6b7280;--blue:#2563eb;--bg:#f8fafc;}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'PingFang SC','Helvetica Neue',Arial,sans-serif;background:var(--bg);color:#1e293b;line-height:1.6;}
.container{max-width:1100px;margin:0 auto;padding:32px 20px;}
.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:32px;}
@media(max-width:800px){.cards{grid-template-columns:repeat(2,1fr);}}
.card{background:#fff;border-radius:12px;padding:20px;box-shadow:0 2px 12px rgba(0,0,0,.06);text-align:center;}
.card .mod{font-size:.78rem;color:#64748b;margin-bottom:6px;}
.card .pts{font-size:2rem;font-weight:800;color:#1e40af;}
.card .max{font-size:.82rem;color:#94a3b8;}
.card .bar-wrap{background:#e2e8f0;border-radius:99px;height:6px;margin-top:10px;}
.card .bar{height:6px;border-radius:99px;background:linear-gradient(90deg,#3b82f6,#06b6d4);}
.section{background:#fff;border-radius:12px;padding:28px;box-shadow:0 2px 12px rgba(0,0,0,.06);margin-bottom:24px;}
.section h2{font-size:1.05rem;font-weight:700;margin-bottom:18px;display:flex;align-items:center;gap:8px;flex-wrap:wrap;}
.section h2 .badge{background:#eff6ff;color:#2563eb;font-size:.72rem;padding:2px 10px;border-radius:99px;white-space:nowrap;}
table{width:100%;border-collapse:collapse;font-size:.86rem;}
th{background:#f1f5f9;padding:10px 12px;text-align:left;font-weight:600;color:#475569;}
td{padding:10px 12px;border-bottom:1px solid #f1f5f9;vertical-align:top;}
tr:last-child td{border-bottom:none;}
.matched{color:#16a34a;font-weight:700;}
.partial{color:#ca8a04;font-weight:700;}
.missing{color:#dc2626;font-weight:700;}
.tag-green{background:#dcfce7;color:#15803d;padding:2px 8px;border-radius:5px;font-weight:600;font-size:.82rem;}
.tag-yellow{background:#fef9c3;color:#854d0e;padding:2px 8px;border-radius:5px;font-weight:600;font-size:.82rem;}
.tag-red{background:#fee2e2;color:#991b1b;padding:2px 8px;border-radius:5px;font-weight:600;font-size:.82rem;}
.tag-blue{background:#eff6ff;color:#1d4ed8;padding:2px 8px;border-radius:5px;font-weight:600;font-size:.82rem;}
.charts{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-bottom:24px;}
@media(max-width:700px){.charts{grid-template-columns:1fr;}}
.chart-box{background:#fff;border-radius:12px;padding:24px;box-shadow:0 2px 12px rgba(0,0,0,.06);}
.chart-box h2{font-size:.95rem;font-weight:700;margin-bottom:16px;}
.advice-item{display:flex;gap:12px;padding:12px 0;border-bottom:1px solid #f1f5f9;}
.advice-item:last-child{border-bottom:none;}
.advice-num{background:#eff6ff;color:#2563eb;font-weight:800;min-width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:.82rem;}
.advice-text strong{display:block;margin-bottom:3px;font-size:.9rem;}
.advice-text{font-size:.85rem;color:#374151;}
.novelty-box{margin-top:14px;padding:12px 16px;background:#dcfce7;border-radius:8px;font-size:.86rem;color:#15803d;}
.creative-box{margin-top:12px;padding:10px 14px;background:#fef9c3;border-radius:8px;font-size:.84rem;color:#854d0e;}
footer{text-align:center;color:#94a3b8;font-size:.78rem;padding:24px 0;}
a{color:#2563eb;}
```

**模块3 — 四维度得分卡（`.cards` 四格）**：
- 每格含：模块名（`.mod`）、得分大字（`.pts`）、满分（`.max`）、进度条（`.bar-wrap > .bar`，`width` = 得分/满分×100%）

**模块4 — 图表区（`.charts` 两列）**：
- 左：`<canvas id="donut">` 甜甜圈图（Chart.js doughnut），展示四模块得分分布
- 右：`<canvas id="radar">` 雷达图（Chart.js radar），展示22项细分指标得分
- Chart.js 引用：`<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>`

**模块5 — claim_diff_matrix（`.section`）**：
- 标题：`📋 claim_diff_matrix — D1 逐要素对比` + `.badge`（`novelty-check · 单一文件原则`）
- D1 文件信息段（申请人/优先权日/公开日）
- 表格列：要素ID、要素内容摘要、状态（`.matched`/`.partial`/`.missing`）、比对依据
- 标注 📌 的为核心区别特征
- 底部：`.novelty-box`（绿色，新颖性结论）+ `.creative-box`（黄色，创造性结论）

**模块6 — 模块一 法律可专利性（`.section`）**：
- 标题含 `.badge` 显示得分（如 `27 / 30`）
- 表格列：序号、指标、结论（使用 `.tag-green`/`.tag-yellow`/`.tag-red`/`.tag-blue`）、得分

**模块7 — 模块二 技术质量（`.section`）**：
- 同模块6格式，5项指标

**模块8 — 模块三 市场与经济价值（`.section`）**：
- 同模块6格式，6项指标

**模块9 — 模块四 战略布局与管理（`.section`）**：
- 同模块6格式，5项指标

**模块10 — 优化改进建议（`.section`）+ 关键对比文件表（`.section`）+ 页脚（`footer`）**：
- 优化建议：每项用 `.advice-item`（`.advice-num` 蓝色圆圈编号 + `.advice-text` 加粗标题+说明）
- 关键对比文件：表格含编号、专利号（超链接）、标题、主要重叠点、FTO风险（`.tag-*`）
- 页脚：依据标准说明 + 生成时间 + 免责声明

**Script 区**：
```javascript
// 甜甜圈图
const ctx1 = document.getElementById('donut').getContext('2d');
new Chart(ctx1,{type:'doughnut',data:{labels:['法律可专利性({{m1}})','技术质量({{m2}})','市场价值({{m3}})','战略布局({{m4}})'],datasets:[{data:[{{m1}},{{m2}},{{m3}},{{m4}}],backgroundColor:['#3b82f6','#06b6d4','#10b981','#8b5cf6'],borderWidth:0}]},options:{plugins:{legend:{position:'bottom',labels:{font:{size:10},boxWidth:12}}},cutout:'62%'}});
// 雷达图（22项指标，各项得分按实际填充）
const ctx2 = document.getElementById('radar').getContext('2d');
new Chart(ctx2,{type:'radar',data:{labels:['客体适格','新颖性','创造性','实用性','在先权利','权属','方案完整度','技术先进性','可替代性','TRL成熟度','迭代空间','市场规模','产业化','许可价值','FTO风险','投入产出','政策适配','布局必要','申请类型','地域布局','维护年限','合规管理'],datasets:[{label:'得分',data:[{{22项得分}}],backgroundColor:'rgba(59,130,246,0.15)',borderColor:'#3b82f6',pointBackgroundColor:'#3b82f6',borderWidth:2}]},options:{scales:{r:{min:0,max:8,ticks:{display:false,stepSize:2},grid:{color:'#e2e8f0'},pointLabels:{font:{size:8}}}},plugins:{legend:{display:false}}}});
```

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。

# Patent Pre-Evaluation Report — Workflow Reference

## 1. MCP Tool Call Sequence

### Phase A: Technical Extraction
| Step | Tool | Input | Output |
|------|------|-------|--------|
| A1 | `novelty_summary` | 技术方案全文 | tech_problem / tech_solution / tech_efficacy |
| A2 | `novelty_feature_extract` | summary_result | feature_extract_result（特征表） |

### Phase B: Search Strategy
| Step | Tool | Input | Output |
|------|------|-------|--------|
| B1 | `novelty_keywords_extract` | summary_result + feature_extract_result | keywords_extract_result（关键词+IPC） |
| B2 | `novelty_keywords_extend` | 单个关键词 + 技术方案文本 | 同义词/上位词/下位词/翻译扩展 |
| B3 | `novelty_query_planner` | keywords_extract_result + feature_extract_result | 多轮检索式列表 queries[] |

### Phase C: Real Search Execution
| Step | Tool | Input | Output |
|------|------|-------|--------|
| C1 | `novelty_search_agent` | 技术方案文本（优先） | 检索结果列表 + patent_ids |
| C1a | `novelty_semantic_search` | 技术方案文本 | 语义相似专利列表 |
| C1b | `novelty_patent_search` | 检索式 q | 关键词命中专利列表 |
| C1c | `novelty_paper_search` | 查询文本列表 | 相关论文列表 |
| C2 | `novelty_fetch_patent_data` | patent_ids[] | 专利详情（PN/TITLE/摘要/附图） |
| C3 | `novelty_abstract_figure_similarity` | input_text + patent_ids | 摘要附图相似度评分 |

### Phase D: Feature Comparison
| Step | Tool | Input | Output |
|------|------|-------|--------|
| D1 | `novelty_feature_comparison` | summary_result + feature_extract_result + patent_ids | 逐项特征比对结果 |
| D1a | `novelty_feature_comparison_async` | 同上（patent_ids较多时） | task_id |
| D1b | `novelty_cc_result` | task_id | 异步比对结果（轮询至finished） |
| D2 | `novelty_rl_predict` | tech_solution + patent_ids | 新颖性/创造性预测分 |
| D3 | `novelty_report_generate` | 比对结果 | 比对评述段落 |

### Phase E: Optional Supplement
| Step | Tool | Input | Output |
|------|------|-------|--------|
| E1 | `novelty_website_search` | 产业/市场查询文本 | 网页/新闻检索结果（转化价值章节） |

---

## 2. Report Section Skeleton

### 封面 & 基本信息（竖版A4）
- 报告编号（格式：CUMT-IP-PRE-YYYY-XXXX）
- 发明名称
- 发明人、单位、院系、联系方式
- 报告日期
- 保密等级
- 见下方【封面布局规范】

### 数据安全与保密声明（⚠ 位于政策背景之前，每份报告必须包含）
- section-num 圆圈内仅放 🔒 emoji，不加其他文字
- 使用与其他章节完全一致的 CSS class，不加内联样式
- 4条固定内容（以卡片/表格形式展示）：
  1. **内部使用与权限控制**：本报告仅供中国矿业大学科研院知识产权管理办公室、项目发明人及经授权代理机构使用，未经授权不得外传。
  2. **脱敏检索与最小披露**：外部检索仅使用关键词、IPC分类号和抽象技术特征，不上传技术交底书原文、核心参数完整表或未公开实验数据。
  3. **平台安全说明**：智慧芽（PatSnap）安全与合规能力可参见官方网站：https://www.zhihuiya.com/security-center。
  4. **留痕与复核**：提交、检索、修改、导出、盖章等环节应在知产办流程中留痕；AI辅助结论须经知识产权管理人员复核后使用。

### 政策背景（固定文字，共5条，每份报告必须包含）
1. 教育部、科技部《关于规范高等学校SCI论文相关指标使用 树立正确评价导向的若干意见》（教科技〔2020〕2号）
2. 教育部《关于加强高校有组织科研 推动高水平自立自强的若干意见》（教科技〔2022〕1号）
3. 国务院办公厅《专利转化运用专项行动方案（2023—2025年）》
4. 人力资源和社会保障部、教育部《关于深化高等学校教师职称制度改革的指导意见》（人社部发〔2020〕100号）：明确将专利成果转化情况纳入职称评审，鼓励以专利转化实绩替代论文数量要求，推动"以用促创"。
5. 教育部《破除"唯论文"不良导向若干措施》及配套政策：支持将发明专利授权数量、许可转让收益、产学研合作纳入职称评定，以专利转化金额及经济效益作为职称晋升依据。

### 技术方案要点
- 技术背景与现有技术不足
- 核心技术特征表（来自 A2 feature_extract_result）
- 主要技术参数与指标

### 查新点与查新要求
- 逐条列出查新点（编号 Z1–Zn）
- 每条查新点：技术特征描述 + 查新要求说明
- 数据来源：A2 feature_extract_result + AI整理

### 检索范围与策略
- 检索数据库列表（中国专利、PCT/WIPO、USPTO、EPO、学术论文等）
- 检索语言、时间范围
- 中文关键词组（来自 B1）
- 英文关键词组（来自 B1/B2）
- IPC分类号（来自 B1）
- 布尔检索式（来自 B3）

### 检索结果与相关文献
- 各轮次检索统计表（数据库/检索式/命中数/筛选数）
- 相关文献列表（专利号/标题/申请人/公开日/相似度）
- 密切相关文献重点摘要
- 数据来源：C1–C3 真实检索结果，禁止虚构

### 逐项技术特征比对
- 每条查新点 vs 最相关文献的特征比对矩阵
- 判定：相同 / 相近 / 部分公开 / 未见 / 待复核
- 数据来源：D1–D3 比对结果

### 可专利性风险判断
- 新颖性分析（基于 D2 RL评分 + 比对结果）
- 创造性分析
- 风险等级：低风险 / 中风险 / 高风险

### 非正常申请风险排查
- 技术方案完整性评估
- 独立性评估
- 实验支撑充分性
- 风险等级：低 / 中 / 高

### 申请文件质量评估
- 权利要求书完整性建议
- 说明书充分公开性建议
- 摘要规范性建议

### 转化价值评估
- 市场前景分析（可选调用 E1 novelty_website_search）
- 产业化路径建议
- 技术许可/转让可行性

### 申请策略建议
- 申请类型（发明/实用新型/外观）
- 独立权利要求保护范围建议
- 从属权利要求候选
- 优先权/PCT建议

### 综合结论快览页
- 总体结论：建议申请 / 修改后申请 / 暂缓申请 / 不建议申请
- 各维度评分卡片（新颖性/创造性/转化价值/申请质量）
- 关键证据摘要
- 下一步行动清单
- AI复核免责声明

---

## 3. HTML Style Guide

### CSS Variables
```css
--primary: #1a3a6b;        /* 深蓝，章节标题/表头/页脚 */
--primary-light: #2a5298;  /* 中蓝，子标题 */
--accent: #c8a94b;         /* 金色，强调/边框/badge */
--accent-light: #f5e6b8;   /* 浅金 */
--danger: #c0392b;         /* 红色，高相似度 */
--warning: #e67e22;        /* 橙色，警示 */
--success: #27ae60;        /* 绿色，低风险 */
--info: #2980b9;           /* 蓝色，信息框 */
--gray: #f4f6f9;           /* 浅灰，交替行 */
--border: #d0d7e3;         /* 边框 */
```

### Key Layout Rules
- **封面**：`width: 210mm; max-width: 210mm; min-height: 297mm; margin: 0 auto`，`linear-gradient(145deg, #0d1f4a, #1a3a6b, #2a5298)`
- **正文主体**：`width: 210mm; max-width: 210mm; margin: 0 auto; padding: 24px 0 60px`（左右padding为0，内容宽度与封面一致）
- 章节编号圆圈：`width:40px; height:40px; border-radius:50%; background:var(--primary); color:white`
  - ⚠ 圆圈内**仅放数字或单个emoji**，不放文字，防止溢出
- 章节标题：`border-bottom: 2px solid var(--accent)`
- 左竖线标注：`border-left: 4px solid var(--accent); padding-left: 12px`
- 表头：`background: var(--primary); color: white`
- 相似度进度条：≥70% → `--danger`；40–69% → `--warning`；<40% → `--success`
- 结论快览页背景：同封面渐变；卡片：`border: 2px solid var(--accent)`
- 打印按钮：`position:fixed; bottom:30px; right:30px`
- 页脚：`background: var(--primary); color: white`

### 封面布局规范（竖版A4，从上到下）
```
┌─────────────────────────────────────────┐
│  顶部深蓝色横条 (14mm高, 深蓝渐变)          │
├─────────────────────────────────────────┤
│  金色装饰线 (4px)                          │
├─────────────────────────────────────────┤
│  机构头部: 左=中国矿业大学+英文名             │
│           右=圆形金边"矿"字徽标              │
├─────────────────────────────────────────┤
│  蓝金渐变分割线                             │
├─────────────────────────────────────────┤
│  保密徽标(金边椭圆): 内部保密·申请前预评估    │
├─────────────────────────────────────────┤
│  中文主标题 (21pt深蓝粗体, 居中, 两行)       │
│  英文副标题 (灰色大写)                       │
├─────────────────────────────────────────┤
│  报告类型框 (深蓝渐变底+金色文字)             │
│  "专利 申 请 前 评 估 报 告"                 │
├─────────────────────────────────────────┤
│  基本信息表格 (2列8行)                       │
│  报告编号/日期/单位/领域/发明人/IPC/保密/建议 │
├─────────────────────────────────────────┤
│  红色风险提示条 (高风险时显示关键结论)         │
├─────────────────────────────────────────┤
│  保密声明 (浅灰虚线框, 小字使用限制)          │
├─────────────────────────────────────────┤
│  底部深蓝条: 左=机构名  右=编号+日期(金色)    │
└─────────────────────────────────────────┘
```

### 数据安全声明 HTML 模板
```html
<!-- S0: 数据安全与保密声明 -->
<div class="section">
  <div class="section-header">
    <div class="section-num">🔒</div>
    <div class="section-title">数据安全与保密声明</div>
  </div>
  <table class="data-table">
    <thead>
      <tr><th>条目</th><th>说明</th></tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>内部使用与权限控制</strong></td>
        <td>本报告仅供中国矿业大学科研院知识产权管理办公室、项目发明人及经授权代理机构使用，未经授权不得外传。</td>
      </tr>
      <tr>
        <td><strong>脱敏检索与最小披露</strong></td>
        <td>外部检索仅使用关键词、IPC分类号和抽象技术特征，不上传技术交底书原文、核心参数完整表或未公开实验数据。</td>
      </tr>
      <tr>
        <td><strong>平台安全说明</strong></td>
        <td>智慧芽（PatSnap）安全与合规能力可参见官方网站：<a href="https://www.zhihuiya.com/security-center" target="_blank">https://www.zhihuiya.com/security-center</a></td>
      </tr>
      <tr>
        <td><strong>留痕与复核</strong></td>
        <td>提交、检索、修改、导出、盖章等环节应在知产办流程中留痕；AI辅助结论须经知识产权管理人员复核后使用。</td>
      </tr>
    </tbody>
  </table>
</div>
<!-- S1: 政策背景 -->
```

### File Write Protocol
使用 `files.begin_write` → 多次 `files.append`（每次 ≤ chunk_target_bytes）→ `files.finish_write`
输出路径：`@session/reports/[报告编号].html`

---

## 4. Evidence Schema

### 专利文献记录
```
文献编号: [自动编号 D1, D2, ...]
公开号: [PN_STR]
标题: [TITLE]
申请人: [ASSIGNEE]
公开日: [PBD]
相关查新点: [Z1, Z2, ...]
相似度: [来自 novelty_rl_predict 或 novelty_abstract_figure_similarity]
密切程度: 密切相关 / 相关 / 一般相关
来源工具: [novelty_search_agent / novelty_semantic_search / novelty_patent_search]
```

### 特征比对记录
```
查新点编号: Zn
比对文献: Dn
特征描述: [原文]
判定: 相同 / 相近 / 部分公开 / 未见 / 待复核
说明: [具体差异分析]
```

---

## 5. Risk Scoring Guidance

### 可专利性风险
| 等级 | 新颖性 | 创造性 | 处理建议 |
|------|--------|--------|----------|
| 低风险 | 无相同公开 | 有突出实质性特点 | 建议申请 |
| 中风险 | 有相近公开 | 需要区分 | 修改后申请 |
| 高风险 | 有相同公开 | 显而易见 | 暂缓/不建议 |

### 非正常申请风险
| 风险因素 | 低 | 中 | 高 |
|----------|----|----|-----|
| 技术方案完整性 | 完整 | 基本完整 | 缺失核心 |
| 独立性 | 独立 | 部分依赖 | 完全依赖 |
| 实验支撑 | 充分 | 部分 | 无 |

---

## 6. Iteration Checklist

每次迭代时检查：
- [ ] 查新点是否因新证据需要调整
- [ ] 检索策略是否需要扩展关键词
- [ ] 新增文献是否影响可专利性判断
- [ ] 结论是否需要更新
- [ ] HTML输出是否与模板样式一致
- [ ] 数据安全声明是否位于政策背景之前
- [ ] 封面与正文宽度是否统一（均为210mm，正文左右padding为0）
- [ ] section-num 圆圈内是否仅含数字或单个emoji（无溢出文字）
- [ ] 政策背景是否包含职称改革相关条目（人社部发〔2020〕100号）
- [ ] 附件6政策目录是否包含职称评价相关文件

---
name: target-drug-evidence-evaluation
description: "通过多维证据矩阵评估靶点药物并支持立项判断。适用于：评估靶点—适应症关系的遗传学、机制、临床、竞争、专利和安全性证据，支持Go/No-Go立项判断。"
---

# RD&BD Evaluate — Target × Drug × Evidence × Patent

使用场景：当用户需要对一个靶点（或靶点-适应症组合）做立项判断，并需要输出结构化 Go/Watch/Niche Go/No-Go 分诊意见时，加载本 skill。

> 本 skill **不输出情报简报**，只输出立项决策结构：Executive Verdict → Scorecard → Evidence Matrix → Next Actions。

---

## Inputs

| 参数 | 是否必填 | 默认值 | 说明 |
|---|---|---|---|
| `target` | **必填** | — | 靶点名称，如 KRAS、PD-1、CDK4/6 |
| `disease` | 可选 | 广谱靶点评估 | 适应症，如 NSCLC、类风湿关节炎 |
| `drug_type` / `modality` | 可选 | 不限 | 小分子 / mAb / ADC / 细胞治疗 等 |
| `country` | 可选 | CN + US + EU/global | 地理范围 |
| `user_type` | 可选 | biotech | biotech / university / BD-licensing / pharma |
| `stage_intent` | 可选 | discovery/preclinical triage | 立项阶段意图 |

**原则**：关键输入缺失时，不停止流程，使用上述默认值继续，并在输出中标明假设。

---

## Workflow

### Step 1 — 实体标准化
- 如用户输入包含靶点名、药物名、疾病名等具体实体，优先调用 `ls_ner_nor_normalize` 做标准化，获取规范 ID 供后续查询。

### Step 2 — 靶点信息确认
- 调用 `ls_target_fetch`（target 参数传标准化名称或 ID）确认靶点存在性、别名、基因符号和已知 pathway 关联。

### Step 3 — 同靶点药物格局
- 调用 `ls_drug_search`（target 参数）获取开发中及已上市药物列表。
- 关注 `highest_phase`、`drug_type`、开发机构分布。

### Step 4 — 关键药物里程碑
- 对 Step 3 返回的关键代表性药物（优先 Phase 2 及以上）调用 `ls_drug_milestone_fetch`，获取研发里程碑时间线。
- 标记失败 / 暂停 / 撤回事件，作为临床失败信号。

### Step 5 — 临床活跃度
- 调用 `ls_clinical_trial_search`（target + disease）获取在研试验数量、阶段分布、主要申办方。

### Step 6 — 临床结果与失败信号
- 调用 `ls_clinical_trial_result_search`（target + disease）获取已发布结果，标记失败 / 阴性 / 安全性问题。

### Step 7 — 转化医学证据
- 调用 `ls_translational_medicine_search`（target + disease）获取生物标志物、动物模型、机制文章证据。

### Step 8 — 指南与患者路径（可选）
- 如可用，调用 `ls_clinical_guideline_vector_search` 获取该适应症治疗指南地位和未满足需求声明。

### Step 9 — 专利拥挤度与 FTO 风险（可选）
- 如可用，调用 `ls_patent_search`（target + drug_type）评估专利密度、申请人集中度、近年申请趋势。
- 对特定高关注专利调用 `ls_patent_fetch` 查看权利要求范围。
- 参见 `references/mcp-tool-map.md` 确认当前会话实际工具名。

### Step 10 — 综合评分与输出
- 依据 `references/scoring-rubric.md` 对六个维度打分，汇总为最终判断。
- 严格按照 `references/output-templates.md` 输出四块结构。
- **不额外输出情报摘要、事件时间线或新闻汇编**，保持决策导向。

---

## Output Structure

四块固定输出，详见 `references/output-templates.md`：

1. **Executive Verdict** — 结论 / 一句话理由 / 关键假设 / 最大风险
2. **Scorecard** — 六维 100 分表格
3. **Evidence Matrix** — 证据类型 × 发现 × 对立项影响 × 数据来源
4. **Next Actions** — 推荐验证动作 / 尽调问题 / 建议避开的方向

---

## References

- `references/scoring-rubric.md` — 六维评分规则与最终判断阈值
- `references/mcp-tool-map.md` — 智慧芽 MCP 工具映射与参数说明
- `references/output-templates.md` — 中文输出模板

---

## Guardrails

- 本 skill 仅做立项分诊，不做合规建议、投资建议或临床决策建议。
- 对负面证据（失败信号、安全性问题）与正面证据等权显示，不美化结论。
- 所有 Scorecard 分项须有对应的证据来源列，禁止凭空打分。
- 若关键数据缺口过大（超过 3 个维度无有效数据），输出 `Insufficient Evidence` 而非强行给出判断。

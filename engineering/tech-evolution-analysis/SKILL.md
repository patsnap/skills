---
name: tech-evolution-analysis
description: |
  基于 TRIZ 11 进化路线 + SVOP 功能化 + patsnap 四轨检索（专利+论文）的技术进化趋势分析 7 步流水线。当用户给出一个产品名称（如智能手表、AR 眼镜、扫地机器人、新能源车电池等）并希望识别该产品的进化方向、空白点、跨域类比候选、3-5-10 年下一代形态预测、灰犀牛与黑天鹅技术信号时调用。触发关键词：技术进化、进化趋势、下一代形态、TRIZ 进化树、空白点、跨域类比、技术路线图、黑天鹅信号、灰犀牛技术、技术预测
---

# Tech Evolution Analysis · 技术进化趋势分析 7 步流水线

## 用途

把任何一个产品（如 TWS 耳机、AR 眼镜、扫地机器人、医疗内窥镜）拆解为可分析的最小功能单元，从全球 2亿级专利池经过 6 步收敛到 50 个左右的可决策节点，最终输出**3 / 5 / 10 年下一代形态预测 + 灰犀牛技术（路径监控）+ 黑天鹅信号（事件监控）+ 旗舰概念形态**。

## 核心方法论

- **TRIZ 11 进化路线** — Altshuller 从不同行业/技术提炼的普适进化规律（公约数）；标引=把具体产品投影到普遍规律上读出"下一步该往哪走"。`tier↑`=沿路线**内在方向**更深≠更复杂：区分增益型路线（更结构化/智能）与裁剪型路线（路线 2、路线 1 末端=更简/更集成），理想度为共同终极方向（v0-v11 节点字典）
- **SVOP 功能化** — Subject + Verb + Object + Parameter 四元组，剥离形态依赖让跨域类比成为可能
- **四轨检索** — 本域专利 / 本域论文 / 跨域专利 / 跨域论文 并行；论文轨补偿专利 18+ 月滞后、提供 1-3 年前瞻信号，每轨论文目标占比 ≥20%（不足记 sparse）
- **四独立性原则** — 物理学/矛盾/接口/生态四独立判别关键零部件
- **多维评分筛选** — 同族广度/引用强度/申请人质量/价值评级/运营信号 5 维加权
- **嵌套四层级树** — 产品/大系统/子系统/组件 + 关键零部件支树
- **进化森林（v3）** — 主轴是路线不是组件；一个组件可有 1~N 条并列主干路线；主干节点上"数据驱动派生"出子路线（路线套路线），由 Step 5 `spawns_new_route` 埋点连边
- **三类节点（v3 重定义）** — 特征点（派生子路线的拓扑分叉母节点，不再等于 breakthrough）/ 空白点（按 TRIZ 路线下一步应到达但全球无布局的预测靶点）/ 类比点（节点方案可被其他路线或组件借鉴的可移植性）
- **灰犀牛 vs 黑天鹅** — Step 7 必须把"突变信号"分成两类：灰犀牛 = 高概率 / 路径清晰 / 半年-年度路径监控 / 纳入路线图；黑天鹅 = 低概率 / 触发点不可预测 / 季度-事件监控 / 设置触发器与应急方案。同一议题可同时具备双重身份（如 PQC 抗量子）— 必须分别归类。**v3.1 起用 BSS（10 分信号强度）+ TDI（100 分颠覆量级）量化打分替代纯定性计数**（吸收自 black-swan-tech-radar）
- **Web 行研哨兵层** — Step 3 在专利+论文之外并行跑五类 Web 哨兵（资本/成熟度/标准/监管/跨界玩家），捕捉专利库看不到的黑天鹅源头；信号不入评分池，作 Step 7 多源交叉验证证据

## 7 步流水线总览

| 步骤 | 动作 | 输入 → 输出 |
|------|------|-------------|
| Step 1 | 系统拆解（4 层级思维导图） | 产品 → 4 大系统 → 子系统 → 组件 → 关键零部件 |
| Step 2 | SVOP 功能化锚定 | 组件 + 关键零部件 → SVOP 四元组（V/O 上位化） |
| Step 3 | patsnap 四轨检索（专利+论文） | SVOP → 本域/跨域 × 专利/论文 N 桶原始池（每件附属性 + evidence_type） |
| Step 4 | 高价值筛选 | 原始池 → 5 维评分 + 综合分 → 高价值池 |
| Step 5 | TRIZ 11 路线 AI 标引 | 高价值池 → 19 路并发 → triz_labeled_pool（v0-v11 节点 + `spawns_new_route` 派生埋点） |
| Step 6 | 进化森林构建 | 标引池 → 组件 → 主干 → 派生子路线（路线套路线）+ 三类节点 → **HTML 进化树** |
| Step 7 | 形态预测 + 报告 | 进化树 → 3/5/10 年预测 + 灰犀牛 / 黑天鹅分类 + 概念形态 + 多风格 HTML |

## 调用流程

收到「分析 XX 产品的技术进化趋势」类请求时：

1. **先确认范围**：产品具体形态、是否需要跨域、目标地域、目标时间窗口（3/5/10 年中的哪些）
2. **逐步执行**：按 Step 1 → Step 7 顺序，每步完成后向用户简报，让用户确认前才进下一步（特别是 Step 1 的 4 层级拆解、Step 2 的 SVOP 锚定、Step 4 的评分权重 — 这些影响后续全部步骤）
3. **每步产物归档**：所有产物保存到「产品名_技术趋势分析」文件夹下，沿用以下文件命名：
   - `step1-2-components-svop.md`（拆解 + SVOP）
   - `patent_pool_step3.json` / `patent_pool_step4.json`
   - `triz_labeled_pool.json` / `breakthrough_index.json`
   - `evolution_trees.json` / `feature_points.json` / `blank_points.json` / `analogy_points.json`
   - `step6_evolution_forest_v3.html`（进化森林可视化，Step 6 必出，由 render_forest.py 渲染）
   - `step7_predictions.json` / `gray_rhinos.json` / `black_swans.json` / `concept_forms.json`
   - 最终多风格 HTML 报告
4. **方法论参考**：每步的详细规范见 `references/` 下对应的 stepN-report.md

## 详细规范

每步的方法论规范在 `references/` 下：

- [references/step1-2-components-svop.md](references/step1-2-components-svop.md) — 4 层级拆解 + 四独立性 + SVOP v4 规范
- [references/step3-double-track-search.md](references/step3-double-track-search.md) — 四轨检索策略（本域/跨域 × 专利/论文；论文轨语义主导）
- [references/step4-multi-dim-scoring.md](references/step4-multi-dim-scoring.md) — 5 维评分模型
- [references/step5-triz-labeling.md](references/step5-triz-labeling.md) — 19 路标引 + v0-v11 字典 + 抽查回归
- [references/step6-evolution-tree.md](references/step6-evolution-tree.md) — 进化森林（v3）：并列主干 + 路线套路线派生 + 三类节点重定义
- [references/step7-prediction-report.md](references/step7-prediction-report.md) — 3/5/10 年预测 + 灰犀牛 vs 黑天鹅分类（v2）+ 概念形态 + LR-01-08 校验

## 固化资产（assets/）

三个产出物已固化，换产品时**优先复用、不要从零手写**，以保证版式与结构不漂移：

- **Step 1 系统拆解思维导图** — [assets/mindmap/](assets/mindmap/)（读 JSON 生成器）
  - `python render_mindmap.py --data <案例>/mindmap_data.json --out <案例>/系统拆解思维导图.html`
  - 换案例只写一份 `mindmap_data.json`（字段契约见脚本 docstring；范例 `example_mindmap_data_plc.json`）；CSS 锁在脚本内
- **Step 6 进化森林** — [assets/forest/](assets/forest/)（读 JSON 生成器）
  - `python render_forest.py --records <案例>/triz_relabeled_records_v3.json --out <案例>/step6_evolution_forest_v3.html --title "..."`
  - `triz_forest_common.py` 是通用渲染核（11 路线字典 + 三态 + CSS），**永不改**；换案例只改 `render_forest.py` 顶部 `PART_NAME`
- **Step 7 最终报告（麦肯锡风格）** — [assets/report/](assets/report/)（CSS + 14 章骨架模板）
  - 复制 `report_skeleton_mckinsey.html`，`<style>` 逐字保留，逐章替换 `<!-- FILL: ... -->`，章节顺序与 class 照搬
  - 报告每章版面不同，故锁 CSS + 骨架而非读 JSON（理由见 assets/README.md）
- 三套均以 PLC 案例为基准范本，已回归校验 class 用量一致。详见 [assets/README.md](assets/README.md)

## 触发场景示例

- 「帮我分析智能手表的下一代形态」
- 「AR 眼镜的技术进化趋势是什么」
- 「扫地机器人 5 年内会怎么演变」
- 「新能源车电池的黑天鹅信号有哪些」
- 「医疗内窥镜的进化树长什么样」
- 「找出 XX 行业未来 5 年的灰犀牛和黑天鹅技术」

## 不适用场景

- 单纯专利检索 → 用 patsnap MCP
- 跨领域功能解决方案查找 → 用 fos skill
- FTO 自由实施分析 → 不在本流水线范围（输出可作为 FTO 输入但不替代 FTO）
- 单一产品的简单功能解析 → 杀鸡用牛刀，建议直接对话讨论

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。

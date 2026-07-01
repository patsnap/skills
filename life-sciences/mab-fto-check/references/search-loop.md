# 检索循环（单抗 FTO 专用）

## 目标

使用三轨并行检索（关键词 + 语义 + 序列）和确定性召回估算来控制 FTO 候选专利池的扩展，而不是凭直觉停止。

## 三轨检索架构

### 轨道 A：关键词检索（PatSnap）

适合精确术语、申请人名称、IPC 代码匹配。

**常用 IPC 分类：**
- `C07K16` — 免疫球蛋白，单克隆抗体
- `C07K16/28` — 针对受体类型细胞表面抗原
- `A61K39/395` — 含抗体的制剂
- `A61P35` — 抗肿瘤药物（按适应症扩展）

**关键词构建规则：**
- 提取靶点名称（如 PD-1、VEGF-A、HER2、CD20、EGFR）
- 加入抗体结构术语（CDR、VH、VL、HCDR3、LCDR3、Fab、Fc、IgG1、IgG4）
- 加入竞争对手/申请人名称
- 新关键词不得与 `query_history.keywords` 重复

### 轨道 B：语义检索（PatSnap）

适合功能机制描述、技术问题语义匹配。

**查询演进策略（逐轮抽象）：**
- 第 1 轮：实施层 — "包含 CDR-H3 序列 XXXXXX 的抗 PD-1 单克隆抗体"
- 第 2 轮：效果层 — "通过阻断 PD-1/PD-L1 结合增强 T 细胞活性的治疗性抗体"
- 第 3 轮：问题层 — "克服肿瘤免疫逃逸的检查点抑制抗体"
- 第 4 轮：场景层 — "单抗联合化疗提升免疫检查点治疗疗效"

**规则：**
- 每轮沿抽象梯阶向上移动，不在原地替换同义词
- 不将型号、尺寸或材料名称混入语义查询

### 轨道 C：序列相似度检索（ls_sequence_alignment）

适合发现与目标抗体序列高度相似的专利。

**执行步骤：**

1. 准备序列输入（FASTA 或单字母序列）：
   - 重链可变区（VH）
   - 轻链可变区（VL）
   - 单独提取 CDR-H1、CDR-H2、CDR-H3、CDR-L1、CDR-L2、CDR-L3（按 Kabat/IMGT 编号）

2. 调用 `ls_sequence_alignment` 分别对 VH 和 VL 执行检索

3. 默认相似度阈值：
   - VH 全序列：≥ 90%
   - VL 全序列：≥ 90%
   - CDR-H3（关键特异性决定区）：精确匹配或 ≥ 95%

4. 记录每条命中的：
   - 专利号
   - 序列相似度（%）
   - 比对区域（VH/VL/CDR-H1…CDR-L3）
   - 错配位置

5. 将序列命中的专利 ID 并入 `patent_pool`，标注来源为 `sequence_track`

## 每轮所需输入

在每轮运行 `scripts/mab_fto_recall_estimator.py` 之前，准备 JSON 输入文件：

```json
{
  "round": 2,
  "keyword_ids": ["US1", "US2"],
  "semantic_ids": ["US2", "US3"],
  "sequence_ids": ["US4", "US5"],
  "seen_ids": ["US0"],
  "recall_target": 0.85,
  "delta_n_min": 5
}
```

字段约定：
- `round`：当前轮次编号，从 `1` 开始
- `keyword_ids`：本轮关键词检索返回的唯一专利 ID 列表
- `semantic_ids`：本轮语义检索返回的唯一专利 ID 列表
- `sequence_ids`：本轮序列检索返回的唯一专利 ID 列表（可选，无序列结果时置空列表）
- `seen_ids`：本轮开始前已见过的唯一专利 ID 列表
- `recall_target`：接受 `0.85` 或 `85`
- `delta_n_min`：触发边际收益递减警告的最小新命中数

## 确定性估算器

在任何轮次摘要或停止/继续决策之前运行脚本：

```bash
python3 scripts/mab_fto_recall_estimator.py --input-json <round-input.json>
```

脚本基于 Chapman 捕获-再捕获逻辑输出：
- `n_k`、`n_s`、`n_seq`（各轨道命中数）
- `n_ks`、`n_k_seq`、`n_s_seq`、`n_all`（两两及三方重叠）
- `n_pool`（累计池大小）
- `delta_n`（本轮新增命中）
- `universe_estimate_raw`、`universe_estimate_adjusted`
- `recall_estimate`
- `correction_applied`
- `decision`
- `warnings`

## 解读规则

- `target_met`：估算召回率已达目标，可开始筛查和分析
- `diminishing_returns`：新命中数低于阈值，向用户说明边际收益递减
- `continue_search`：继续下一轮
- `expand_search`：当前轮过弱，拓宽查询或增加序列变体

仅当脚本输出 `target_met` 时，方可在正文中写"召回率目标已达到"。

## 查询历史合同

持续维护：

```json
{
  "query_history": {
    "keywords": ["used-term-1", "used-term-2"],
    "semantic": [
      { "round": 1, "level": "实施层", "query": "..." },
      { "round": 2, "level": "效果层", "query": "..." }
    ],
    "sequence_queries": [
      { "round": 1, "chain": "VH", "sequence_id": "VH_001", "threshold": 0.90 },
      { "round": 1, "chain": "VL", "sequence_id": "VL_001", "threshold": 0.90 }
    ],
    "ipc_codes_used": ["C07K16", "A61K39/395"]
  }
}
```

## 失败处理

- 若三轨均为空，当前方案已失败；拓宽查询后再继续
- 若高重叠触发修正，明确说明当前 `R_est` 可能偏乐观
- 若估算宇宙小于累计池，接受脚本的下限结果，不手动改写
- 序列检索无结果时，检查序列格式、数据库覆盖和阈值设置

## 单抗 FTO 检索特殊注意事项

1. **族群专利**：一件基础专利可能有数十个同族，需去除同族重复后计入池
2. **生物类似药专利壁垒**：除序列专利外，还需检索制备工艺、细胞系、纯化方法专利
3. **专利到期管理**：单抗专利有效期 20 年，需关注优先权日而非公开日
4. **方法专利**：除组合物/结构专利外，检索治疗方法专利（如剂量方案、联合疗法）
5. **Fc 工程专利**：若候选分子含 Fc 修饰（ADCC 增强、半衰期延长等），增加 Fc 工程专项检索

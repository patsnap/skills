# Step 6 交付报告：进化森林构建（v3 方法论文档）

> **流水线位置**：进化树构建 7 步法的 **Step 6（构建进化树）**
> **输入**：[triz_labeled_pool.json](triz_labeled_pool.json) 标引完成池（v3 schema，含 `spawns_new_route` 派生埋点）
> **输出**：**`step6_evolution_forest_v3.html`（可视化进化树，必出）** + [evolution_trees_v3.json](evolution_trees_v3.json) 进化森林 + 三类节点专项索引
> **下游**：Step 7 报告与下一代形态预测

---

## 零、v3 模型总览（与用户手绘目标对齐）

进化树不是"每组件一棵单主干树"，而是一片**森林**，骨架如下：

```
组件(起点, 如 振膜 / 固定装置)
 └─ 并列主干路线 A / B / …          ← 一个组件可有 1~N 条并列主干 (振膜=频率匹配 + 分割向微观)
     ├─ 节点 v0 → v1 → v2 → …       ← 同一条 TRIZ 路线的 tier 演化, 每节点挂已布局方案
     └─ 某节点 ──派生──▶ 子路线 C    ← "路线套路线": 数据里观察到新维度即派生
```

**关键原则**：

1. **主轴是路线，不是组件**——组件只是森林的"根"，真正生长的是进化路线。
2. **并列主干**——一个组件可以有多条主干路线并行，不强行只留一条（振膜既走"频率匹配性提高"又走"分割向微观级"）。
3. **派生是自下而上、数据驱动**——在某节点的专利/文献里聚类出新维度才连派生边，不做自上而下的"成熟度门槛"推演。

---

## 一、v2 → v3 升级要点

| 维度 | v2 | v3 |
|------|----|----|
| 组织主轴 | 组件为主干，路线降级为分支 | **路线为主干**，组件只是森林的根 |
| 每组件主干数 | 1 条（`argmax(dom_routes 频次)`） | **1~N 条并列主干**（所有成型路线都保留） |
| 路线间关系 | 11 条路线各自独立成树 | **路线套路线**：主干节点上派生子路线（森林） |
| 派生识别 | 无此概念 | **`spawns_new_route` 埋点驱动** + 共现回退启发式 |
| 特征点 | `breakthrough=true`（单点价值） | **派生母节点**（拓扑分叉点） |
| 空白点 | domain miss + cross hit（回顾性） | **TRIZ 外推靶点**（预测性：下一节点应到而全球未到） |
| 类比点 | analogy_candidate / tier 差 ≥2 | 同上（语义不变，仍是可移植性） |

---

## 二、三类节点（v3 全部重定义）

> 这是 v3 最核心的修正。三类节点描述的是**树的拓扑与预测**，不再是"单件专利的价值评级"。

| 节点类型 | v3 定义 | 识别数据 | 本质 |
|----------|---------|----------|------|
| **特征点** | 在此节点观察到新维度方案、**派生出子路线**的拓扑分叉母节点 | `spawns_new_route[]` | 树的**分叉点** |
| **类比点** | 该节点方案**可被其他路线/组件借鉴** | 同路线跨组件 tier 落差 ≥ 2 | 横向**可移植性** |
| **空白点** | 按 TRIZ 路线**下一步应到达、但全球无布局**的节点 | 主干 max tier + 字典外推 | **下一代预测靶点** |

### 2.1 特征点 = 派生母节点

特征点不再是"某件高引用突破专利"，而是**树的结构性分叉点**：一条主干路线走到这个节点时，数据里冒出了另一个进化维度，于是派生出一条新主干。

- **首选数据源**：Step 5 的 `spawns_new_route` 埋点（标引时有全文证据，判断最可靠）
- **回退启发式**（埋点缺失时）：在同一组件下，承载主干路线 A 标签的专利集合，若 ≥2 件**同时**承载另一路线 B 的标签，则 (A, 该节点) 是派生 B 的候选母节点。回退结果标 `source=cooccur_heuristic`，精度低于埋点，仅用于 v3 之前的旧池兼容。

### 2.2 空白点 = TRIZ 外推预测靶点

不再是"跨域有、本域无"的回顾性比对，而是**预测性外推**：

```
主干路线 R 当前已布局到节点 v_k
  → 查 TRIZ 节点字典，v_k 的下一个节点是 v_{k+1}
  → 若全球(本域+跨域)在 v_{k+1} 均无布局
  → v_{k+1} 即空白点 = 该路线下一代形态的预测靶点
```

例：发声单元在"分割向微观"已到 v9（原子态），字典下一步是 v10（场跃迁），全球无布局 → v10 是预测靶点。

### 2.3 类比点 = 可移植性（语义沿用 v2）

同一路线下，组件 A 的 tier 比组件 B 领先 ≥ 2，则 A 走过的节点序列可作为 B 的设计模板。

---

## 三、森林构建算法

> 实现见 [build_step6_trees_v3.py](../../../04_工具与脚本/Claude-技术趋势分析/build_step6_trees_v3.py)。

### 3.1 数据来源与节点位置

记录来自 Step 5 标引池 `buckets`，每条携带 `labels`（route→{cur,prev,act,ev,conf}）、`dom_routes`、`breakthrough`、`spawns_new_route`。节点位置（v1/v2/…）由 `cur` 经 **CANON 字典 + ALIAS 别名表**归一化得到（子代理输出名称变体多，别名表是隐藏成本，必备）。

### 3.2 算法步骤

```
# 第 1 步：构建每个组件的并列主干 (build_component_trunks)
for comp in C1..C6:
    for route in 1..11:
        domain_recs = 该组件该路线本域记录
        if len(domain_recs) < TRUNK_MIN_DOMAIN(=2): continue   # 过滤非成型路线
        node_seq = []
        for pos in sorted(本域出现过的节点位置, by tier):
            rep = max(该位置记录, key=cited)                    # 取被引最高者作代表
            node_seq.append(节点{pos, 字典名, rep_pn, cited, breakthrough_here})
        主干.append({route, node_seq, domain_count, domain_max_pos})
    并列主干 按 domain_count 降序                                # 主-次视觉序, 但都是主干

# 第 2 步：识别派生边 = 特征点 (detect_feature_points)
if 池中有 spawns_new_route 埋点:
    特征点 = 直接读取埋点 (source=explicit)
else:
    特征点 = 共现回退启发式 (source=cooccur_heuristic)          # 旧池兼容

# 第 3 步：识别空白点 = 预测靶点 (detect_blank_points)
for 主干 in 并列主干:
    max_pos = 该路线全球已布局最高节点
    nxt = CANON[route] 中 max_pos 的下一个节点
    if nxt 存在 and nxt 全球未布局: 空白点.append(nxt)

# 第 4 步：识别类比点 = 可移植 (detect_analogy_points)
for route in 1..11:
    各组件在该路线的 max tier → 落差 ≥ 2 的 (leader, lagger) 对即类比边
```

### 3.3 为什么是森林而不是单树

```
v2 的问题: argmax 取单一主干 → 振膜的"分割向微观"主干被"频率匹配"挤掉, 信息丢失
v3 的解法: 所有 domain_count ≥ 2 的路线都是并列主干, 互不降级
派生边把并列主干连成森林: 母节点(特征点) ──spawn──▶ 子路线
```

### 3.4 关键阈值

| 阈值 | 默认 | 含义 | 调参建议 |
|------|------|------|----------|
| `TRUNK_MIN_DOMAIN` | 2 | 一条路线≥N 件本域记录才算成型主干 | 数据稀疏的产品可降到 1；噪声多可升到 3 |
| `SPAWN_COOCCUR_MIN` | 2 | 回退启发式：≥N 件专利共现才算派生候选 | 仅在无埋点旧池生效；有埋点时此阈值不起作用 |
| 类比 tier 落差 | ≥ 2 | 跨组件可移植的最小落差 | 落差越大类比越强 |

---

## 四、输出 schema（evolution_trees_v3.json）

```json
{
  "meta": {
    "step": 6, "model_version": "v3",
    "structure": "组件 -> 并列主干路线 -> 数据驱动派生子路线 (spawn-forest)",
    "feature_point_source": "explicit | cooccur_heuristic",
    "node_type_defs": { "特征点": "...", "类比点": "...", "空白点": "..." }
  },
  "forest": {
    "C1": {
      "component": "发声单元", "code": "C1", "subsystem": "执行",
      "parallel_trunks": [
        {
          "route": "9", "route_name": "体组件几何",
          "node_seq": [
            {"pos": "v1", "node": "棱柱形组件", "rep_pn": "...", "rep_cited": 6,
             "domain_count": 4, "breakthrough_here": false},
            {"pos": "v4", "node": "复杂体组件", "rep_pn": "...", "rep_cited": 24,
             "breakthrough_here": true}
          ],
          "domain_count": 25, "cross_count": 3, "domain_max_pos": "v4"
        }
      ],
      "spawn_edges": [
        {"from_route": "6", "from_pos": "v4", "from_canon": "系统自动化",
         "to_route": "3", "to_dimension": "分割向微观", "evidence_count": 6,
         "source": "cooccur_heuristic"}
      ]
    }
  }
}
```

配套三个专项索引：[feature_points_v3.json](feature_points_v3.json)（派生母节点）/ [blank_points_v3.json](blank_points_v3.json)（预测靶点）/ [analogy_points_v3.json](analogy_points_v3.json)（可移植）。

---

## 五、给 Step 7 的输入接口

| 来源 | Step 7 用途 |
|------|-------------|
| **空白点**（blank_points_v3） | **直接就是下一代形态预测靶点**——每条主干路线的 v_{k+1} 即 3-5 年路径 |
| **特征点**（feature_points_v3） | 派生母节点揭示"哪些节点是技术跃迁的枢纽"，是路线图的关键里程碑 |
| **类比点**（analogy_points_v3） | 组件 A 已走过的路径作为组件 B 的设计模板（跨组件协同设计） |
| **forest** | 并列主干 + 派生边的完整拓扑，支撑多视角集成预测 |

---

## 五·补 森林可视化产物（HTML · Step 6 必出最终产物）

> Step 6 不止产出 `evolution_trees_v3.json`，**必须**用固化渲染器把森林渲染成一个**完整的 HTML 进化树**——这是 Step 6 交给用户/喂给 Step 7 的可视化决策物（范本：PLC 案例 `step6_evolution_forest_v3.html`，72 KB）。

### 5.1 渲染契约（复用固化资产，不从零手写）

渲染器在 [assets/forest/](../assets/forest/)，换案例**只改三样**，渲染核 `triz_forest_common.py`（11 路线字典 + 三态 + CSS）**永不改**：

```bash
python assets/forest/render_forest.py \
  --records <案例>/triz_relabeled_records_v3.json \
  --out     <案例>/step6_evolution_forest_v3.html \
  --title   "XX 技术进化森林 · Step 6 v3"
```

| 要改的 | 在哪 | 说明 |
|--------|------|------|
| `PART_NAME` 字典 | render_forest.py 顶部 | 把本案例的 part id（P1.1 / C4.4…）映射成中文标签；其余代码不动 |
| `--records` | 命令行 | 指向本案例 Step 5 标引后的 `triz_relabeled_records_v3.json` |
| `--out` / `--title` | 命令行 | 输出 HTML 路径与标题 |

### 5.2 records 输入契约（来自 Step 5）

渲染器读 `{"records":[...]}`，每条记录字段：

```json
{"pn":"...", "route_attr":"P1.1 ...", "core":"...",
 "labels": {"6": {"node":"6.4", "act":"..."}, ...},
 "spawns_new_route": [{"from":6, "to":7, "why":"..."}]}
```

### 5.3 渲染语义（与方法论一致）

- **每条激活路线画成完整权威骨架**——不是只画命中的节点，而是把该路线 v0-v11 全节点都画出来；
- **三态着色**：已布局（命中 ≥2）/ 稀疏（=1）/ **空白（=0）**；
- **任何节点都不被自动剔除**——空白节点原样显示为「布局机会」，这正是空白点（TRIZ 外推靶点）的可视化承载；
- **派生边**由 `spawns_new_route` 连出"路线套路线"的森林拓扑。

> **方向语义对齐（v4）**：骨架按 [step5 §3.1](step5-triz-labeling.md) 的路线内在方向铺开——裁剪型路线（2 / 1 末端）的高 tier 端在视觉上是"收敛/精简"方向，渲染核已按字典顺序处理，无需额外配置。

---

## 六、本步骤局限与缓解

1. **派生埋点依赖 Step 5 质量** — `spawns_new_route` 由标引代理判断，漏埋会丢失派生边。**缓解**：共现回退启发式兜底；抽查回归对枢纽专利重点复核。
2. **共现启发式精度有限** — 旧池无埋点时，共现 ≠ 因果派生，可能把"并列改进"误判为派生。**缓解**：输出标 `source=cooccur_heuristic`，下游知其精度；重跑 Step 5 加埋点后切换为 explicit。
3. **空白点字典边界** — 外推靶点取决于 CANON 字典的下一节点定义，部分路线节点边界主观。**缓解**：字典争议累积进 v2.1 注释。
4. **并列主干过多** — `TRUNK_MIN_DOMAIN` 过低会让噪声路线也成主干。**缓解**：按产品数据密度调阈值。
5. **零部件层尚未接入 v3** — 当前 v3 脚本聚焦组件层并列主干森林；零部件支树（振膜的两条主干即一例）的嵌套挂载留待下一版。**缓解**：零部件可作为独立组件根跑同一套森林算法。

---

## 七、产物清单

| 文件 | 作用 |
|------|------|
| **[step6_evolution_forest_v3.html](step6_evolution_forest_v3.html)** | **🆕 进化森林可视化最终产物（完整字典骨架 + 三态空白识别 + 派生森林）—— Step 6 必出，由 render_forest.py 渲染** |
| [evolution_trees_v3.json](evolution_trees_v3.json) | 进化森林主产物（组件 → 并列主干 → 派生边） |
| [triz_relabeled_records_v3.json](triz_relabeled_records_v3.json) | 渲染器输入记录（来自 Step 5 标引；render_forest.py 的 `--records`） |
| [feature_points_v3.json](feature_points_v3.json) | 特征点（派生母节点 / 拓扑分叉） |
| [blank_points_v3.json](blank_points_v3.json) | 空白点（TRIZ 外推预测靶点） |
| [analogy_points_v3.json](analogy_points_v3.json) | 类比点（跨组件可移植） |
| [render_forest.py](../assets/forest/render_forest.py) | 森林 HTML 渲染器（换案例只改 PART_NAME） |
| [triz_forest_common.py](../assets/forest/triz_forest_common.py) | 渲染核（11 路线字典 + 三态 + CSS，永不改） |
| [build_step6_trees_v3.py](../../../04_工具与脚本/Claude-技术趋势分析/build_step6_trees_v3.py) | v3 构建脚本（spawn-forest） |
| [step6-evolution-tree.md](step6-evolution-tree.md) | 本报告 |

---

## 八、版本

| 版本 | 日期 | 变更 |
|------|------|------|
| v1 | 2026-05-26 | 初版。三层级树 + 三类节点（306 特征 / 36 空白 / 8 类比） |
| v2 | 2026-05-29 | 四层级嵌套树 + v0-v11 字典 + 19 路聚合 + 单主干（argmax）+ 节点框附图 |
| v3 | 2026-06-10 | **进化森林重构（对齐用户手绘目标）**：①主轴从组件改为路线；②单主干→并列多主干；③新增"路线套路线"派生森林，由 `spawns_new_route` 埋点驱动（+共现回退）；④三类节点全部重定义——特征点=派生母节点（不再=breakthrough）/ 空白点=TRIZ 外推预测靶点（不再=domain-miss-cross-hit）/ 类比点=可移植性；⑤新脚本 build_step6_trees_v3.py |
| v3.1 | 2026-06-22 | **显式声明 HTML 森林为必出最终产物**（§五·补）：补全渲染契约（render_forest.py + triz_forest_common.py 固化资产复用）、records 输入契约、三态着色与派生边渲染语义；产物清单首位补 `step6_evolution_forest_v3.html`。范本：PLC 案例 72KB HTML。来源：用户要求 Step 6 须输出完整 HTML 进化树 |

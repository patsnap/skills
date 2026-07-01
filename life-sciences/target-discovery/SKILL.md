---
name: target-discovery
description: |
  化合物库反向靶点发现工作流。给定化合物 SMILES，依次执行 ADMET 成药性过滤、骨架分析、结构相似检索、靶点情报验证、FTO 专利风险扫描、SAR 构效关系提取，输出优先级靶点-化合物改造方向清单，支持生成 PPT 与 PDF 报告。
---

# Target Discovery Skill — 化合物库反向靶点发现

## 一、技能定位

**适用场景**：客户已积累大量自有化合物库（高校课题组、药企研究团队、CRO），希望反向从化合物结构出发，预测可能作用的靶点，加速成果转化。

**触发关键词**：
- "我们有化合物库，想知道能打哪个靶点"
- "反向筛靶"、"靶点预测"、"化合物库靶点发现"
- "这个分子可能作用于什么靶点"
- "帮我分析一下这个 SMILES 的潜在靶点"

**不适用场景**：
- 已知靶点，正向设计化合物 → 使用 `patsnap-lifescience-target-intelligence_zh`
- 单分子专利新颖性评估 → 使用 `novelty-check`
- 竞争格局分析 → 使用 `competitive-landscape`

---

## 二、依赖能力（MCP + Skill）

### 必须可用的 MCP 工具

| MCP 服务器 | 工具名 | 用途 |
|---|---|---|
| `tool-collection-chemical-molecular` | `ls_admet_predict` | Step 1：ADMET 成药性批量预测 |
| `tool-collection-chemical-molecular` | `ls_chemical_mcs_analyze` | Step 2：骨架/片段频率分析（MCS） |
| `tool-collection-chemical-molecular` | `ls_structure_search` | Step 3：结构相似性检索（SIM/EXT） |
| `tool-collection-chemical-molecular` | `ls_structure_fetch` | Step 3+：化合物详情获取 |
| `tool-collection-chemical-molecular` | `ls_patent_structure_fetch` | Step 5：专利化学结构批量获取 |
| `tool-collection-chemical-molecular` | `ls_sar_submit` / `ls_sar_fetch` | Step 6：SAR 构效关系提取 |
| `patent-search` | `patsnap_search` / `patsnap_fetch` | Step 3/5：专利/文献检索 |

### 协同 Skills

| Skill 名称 | 用途 |
|---|---|
| `patsnap-lifescience-target-intelligence_zh` | Step 4：靶点情报验证（成药性/管线/竞争格局） |
| `novelty-check` | Step 5：FTO 单参考文献新颖性分析 |
| `competitive-landscape` | Step 4+：靶点赛道竞争格局深度报告 |
| `ppt-generator` | 输出：生成演示PPT |
| `pdf-generator` | 输出：生成 PDF 报告 |

---

## 三、标准执行流程（6步）

### 输入
- **必填**：化合物 SMILES 字符串（一个或多个）
- **选填**：化合物名称/编号、适应症偏好方向、是否生成报告（PPT/PDF）

### Step 1 — ADMET 成药性过滤
**工具**：`ls_admet_predict`
**操作**：对输入 SMILES 批量预测 22 项 ADMET 指标
**核心评估维度**：
- 类药五规则（MW < 500, logP 0-5, HBD ≤ 5, HBA ≤ 10）
- 口服生物利用度、水溶性（logS）
- hERG 心脏毒性（安全性红线）
- BBB 透过率（决定是否可探索 CNS 靶点）
- CYP3A4/2D6 抑制（药物相互作用风险）

**决策规则**：
- 全部不符合五规则 → 标记为"成药性极差"，移出候选池
- BBB 低 → 排除 CNS 靶点假说方向
- hERG 高风险 → 标记心脏毒性警告，后续靶点需规避心血管适应症

**输出**：通过/不通过标记 + 关键风险提示列表

---

### Step 2 — 骨架/片段分析
**工具**：`ls_chemical_mcs_analyze`
**操作**：对通过 Step 1 的分子集合做 MCS（最大公共子结构）分析
**解读要点**：
- 识别核心骨架类型（嘧啶、喹唑啉、咪唑、吲哚等）
- 常见药效团关联：
  - 嘧啶-苯胺核心 → 激酶抑制剂
  - 咪唑并嘧啶 → PI3K/mTOR 抑制剂
  - 吲哚核心 → 多靶点激酶 / GPCR
  - 哌嗪/哌啶侧链 → 选择性口袋识别
- 高频片段分布 → 确定优先分析子集（覆盖最广的骨架族）

**输出**：骨架家族分类 + 靶点类型初步指向（激酶/GPCR/核受体/离子通道等）

---

### Step 3 — 结构相似检索 → 靶点假说生成
**工具**：`ls_structure_search`（SIM 模式，Tanimoto ≥ 0.4）
**操作**：对每个核心分子做相似性检索，返回已知活性的结构邻居
**解读规则**：
- Tanimoto ≥ 0.7：高相似，靶点假说可信度高
- Tanimoto 0.5-0.7：中等相似，作为支持性证据
- Tanimoto 0.4-0.5：低相似，仅提示方向，需更多验证

**靶点假说排序**：按相似邻居中靶点出现频率降序排列，生成 Top 3 靶点假说列表

**输出**：
```
假说 1（最高优先级）：靶点名称 — 支持邻居数量 / 最高 Tanimoto 值
假说 2：靶点名称 — ...
假说 3：靶点名称 — ...
```

---

### Step 4 — 靶点情报验证
**技能**：`patsnap-lifescience-target-intelligence_zh`
**操作**：针对 Top 1-3 靶点假说，分别调用靶点情报技能
**评估维度**：
1. **生物学验证**：靶点与疾病的因果关系强度
2. **成药性**：已有上市药物 / 临床管线数量
3. **竞争格局**：赛道拥挤程度（红海/蓝海判断）
4. **适应症价值**：市场规模、未满足临床需求
5. **耐药机制**：是否存在已知耐药突变影响成药

**优先级决策矩阵**：
| 维度 | 高分 | 低分 |
|---|---|---|
| 成药性验证 | 已有上市药 | 无临床进展 |
| 赛道空间 | 存在差异化机会 | 头部玩家完全垄断 |
| 适应症价值 | 大适应症/高未满足需求 | 小适应症/已充分满足 |
| 化合物-靶点匹配 | Tanimoto > 0.6 + 骨架一致 | 仅骨架远亲 |

**输出**：Top 3 靶点评分卡 + 推荐优先验证靶点

---

### Step 5 — FTO 专利风险扫描
**工具**：`ls_structure_search`（EXT 精确模式）+ `novelty-check` Skill
**操作**：
1. 精确结构检索：查询分子是否已被专利权利要求覆盖
2. 新颖性分析：对命中专利执行单参考文献新颖性比对
3. 法律状态核查：通过 `patsnap_fetch`（module=legal）确认专利是否有效

**风险分级**：
| 风险级别 | 判断条件 | 建议行动 |
|---|---|---|
| 🔴 高风险 | 精确结构命中 + 专利有效 | 必须结构改造后推进 |
| 🟡 中风险 | 相似结构命中（Tanimoto>0.8）+ 专利有效 | 评估权利要求范围，考虑规避设计 |
| 🟢 低风险 | 无命中 / 专利已过期 | 可推进，建议自行申请专利保护 |

**输出**：FTO 风险报告 + 改造建议方向

---

### Step 6 — SAR 构效关系提取
**工具**：`ls_sar_submit` → 轮询 `ls_sar_fetch`
**输入**：Step 3 命中的相关专利号
**操作**：从专利中提取化合物-活性数据，分析各官能团取代对活性的影响
**解读维度**：
- 核心骨架各位置取代基变化对靶点活性（IC50/Ki）的影响
- 选择性位点：哪些取代可提升对目标靶点的选择性
- 毒性规避位点：降低 hERG / CYP 毒性的改造方向
- 成药性提升位点：改善溶解性 / 生物利用度的取代策略

**输出**：
```
位置 X → 取代基类型 → 活性影响方向
改造优先级路径：路径A（选择性）/ 路径B（耐药覆盖）/ 路径C（新适应症）
```

---

## 四、输出物汇总

每次完整执行后，产出以下交付物：

### 4.1 核心分析报告
```
📋 靶点发现报告
├── 输入化合物 ADMET 轮廓（通过/风险项）
├── 骨架分类结果（骨架族 + 药效团特征）
├── Top 3 靶点假说（排序 + 置信度）
├── 各靶点情报摘要（成药性/竞争/适应症）
├── FTO 风险等级 + 改造方向建议
└── SAR 关键构效关系表（改造路径优先级）
```

### 4.2 可视化输出（按需）
- **PPT 演示稿**：调用 `ppt-generator` Skill，生成乔布斯风极简竖屏 HTML 演示文件
- **PDF 正式报告**：调用 `pdf-generator` Skill，生成可下载 PDF

---

## 五、典型对话触发示例

```
用户：我有一个 SMILES：Cc1ccc(NC(=O)...)，帮我分析可能的靶点
→ 自动执行 Step 1-6 全流程

用户：我们化合物库有 200 个分子，想做靶点筛选
→ 询问：是否提供 SMILES 列表？优先分析全库还是抽取代表性骨架？

用户：帮我分析一下 BCR-ABL 抑制剂的构效关系
→ 直接跳转 Step 6（SAR 提取），结合 Step 4 靶点情报

用户：这个分子有没有专利风险？
→ 直接执行 Step 5（FTO 扫描）
```

---

## 六、执行注意事项

1. **MCP 可用性检查**：执行前确认 `tool-collection-chemical-molecular` 已安装并 active，否则 Step 1/2/3/6 无法执行
2. **异步工具轮询**：`ls_sar_submit` 为异步任务，提交后需轮询 `ls_sar_fetch` 获取结果，等待间隔建议 10-30 秒
3. **SMILES 格式验证**：输入 SMILES 前建议做基础格式校验（括号匹配、原子符号合法性）
4. **多分子批处理**：`ls_admet_predict` 支持批量输入；`ls_structure_search` 建议单分子逐个执行以保证结果精度
5. **证据溯源**：所有靶点假说、专利引用、文献结论均需标注 `[S#]` 来源标记，不可无来源断言
6. **跨步骤信息传递**：每步输出结果需显式传递给下一步（例如 Step 3 的靶点假说列表传入 Step 4，Step 3 命中专利号传入 Step 6）

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。

---
name: cross-border-patent-risk-screen
description: |
  跨境电商全类型专利侵权风险初筛工具（外观+发明+实用新型三合一）。支持产品图片URL或产品链接输入，AI自动提取外观设计特征与技术特征，与智慧芽全球专利数据库比对，10分钟内输出美国/欧洲/日本等目标市场的侵权风险等级与规避建议，覆盖174个国家和地区。
---

# 跨境电商专利侵权风险初筛技能

## 技能定位

面向**跨境电商专利侵权分析师**，在产品出海或新品发布前，针对目标市场（美国、欧洲、日本等）进行全类型专利侵权风险初筛，10分钟内完成，覆盖三大专利类型：

- **外观设计专利**（Design Patent / Registered Design）
- **发明专利**（Invention Patent / Utility Patent）
- **实用新型专利**（Utility Model Patent）

## 触发条件

用户提供以下任一输入时自动启动：
- 产品图片URL（公开可访问）
- 电商平台产品链接（亚马逊/速卖通/独立站等）
- 产品描述文字 + 可选图片

用户明确提到"侵权风险"、"专利扫描"、"出海检查"、"专利地雷"、"FTO"时优先触发本技能。

## 执行流程（10分钟目标）

### 阶段一：输入处理与图像净化（1-2分钟）

**Step 1. 图像获取**
- 若用户提供图片URL → 直接使用
- 若用户提供产品链接 → 调用 `web_fetch` 抓取页面，提取产品主图URL列表（取前3张最具代表性的图片）
- 若用户提供本地图片 → 调用 `mcp_patsnap-patent-search__upload_patent_image` 上传获取公开URL

**Step 2. 图像理解与特征提取**
- 调用 `mcp_hub-mcp-gateway-novelty-search__novelty_pic2t`，background 字段填写"这是一个跨境电商产品图片，请描述其外观设计特征（形状、轮廓、颜色分布、装饰图案）和可见技术特征（结构、材料、连接方式、功能部件）"
- 提取两类特征：
  - **外观特征**：整体形状、轮廓线条、色彩方案、表面纹理、装饰图案、比例关系
  - **技术特征**：产品类别、核心功能部件、结构组成、工作原理关键词

**Step 3. 技术方案总结**
- 调用 `mcp_hub-mcp-gateway-novelty-search__novelty_summary`，将图像描述文本作为输入，提取技术三要素（问题/方案/效果）
- 提取关键词：调用 `mcp_hub-mcp-gateway-novelty-search__novelty_keywords_extract`

### 阶段二：多维度专利检索（4-6分钟）

并行执行以下三条检索线路：

**线路A：外观设计专利检索**
- 使用图片URL调用 `mcp_patsnap-patent-search__image_search_multiple`（model=1智能联想，patent_type=D）
- 目标市场过滤：country=['US','EP','JP','KR','DE','GB','AU','CA']
- 返回 Top 20 相似外观专利
- 可选：调用 `mcp_hub-mcp-gateway-novelty-search__novelty_abstract_figure_similarity` 评估摘要附图相似度

**线路B：发明专利检索**
- 调用 `mcp_hub-mcp-gateway-novelty-search__novelty_semantic_search`，输入技术方案描述文本
- 过滤条件：目标国家 + SIMPLE_LEGAL_STATUS=[1,2]（有效+审中）
- 调用 `mcp_patsnap-patent-search__search_patents_by_semantic`，输入技术特征关键词组合
- 去重合并，保留 Top 30 相关发明专利

**线路C：实用新型专利检索**
- 使用图片URL调用 `mcp_patsnap-patent-search__image_search_multiple`（model=3形状匹配，patent_type=U）
- 目标市场过滤（重点：CN、DE、JP、KR）
- 同步调用关键词检索补充实用新型结果
- 返回 Top 20 相似实用新型专利

### 阶段三：相似度评分与风险分析（2-3分钟）

**Step 4. 特征比对**
- 对发明/实用新型检索结果，调用 `mcp_hub-mcp-gateway-novelty-search__novelty_feature_comparison_async` 进行技术特征比对
- 提取每件专利的权利要求（claims）与用户产品技术特征逐项比对
- 对外观专利，基于图像相似度分数 + 摘要附图相似度综合评分

**Step 5. 法律状态核查**
- 对相似度 ≥ 60% 的高风险专利，批量调用法律状态查询接口（`mcp_patsnap-patent-brief__legal_status`）
- 仅保留有效（active）和审查中（pending）专利作为风险项

**Step 6. 综合风险评分**
- 对每件风险专利计算综合得分：相似度权重（50%）+ 法律状态权重（30%）+ 市场覆盖度权重（20%）

### 阶段四：报告输出

生成结构化侵权风险报告（见"输出格式"章节）

---

## 输出格式

### 总体风险概览

```
🔍 产品专利侵权风险初筛报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
产品描述：[识别到的产品类型]
检索范围：[目标市场国家/地区]
检索时间：[时间戳]
覆盖专利类型：外观设计 ✓ | 发明专利 ✓ | 实用新型 ✓

┌─────────────────────────────────┐
│   总体风险等级：🔴 高风险        │  ← 根据实际结果显示
│   高风险专利：X 件              │
│   中风险专利：X 件              │
│   低风险专利：X 件              │
└─────────────────────────────────┘
```

### 风险等级定义

| 等级 | 图标 | 说明 | 相似度阈值 |
|------|------|------|-----------|
| 高风险 | 🔴 | 强烈建议停止销售，立即寻求专利律师意见 | ≥80% |
| 中风险 | 🟡 | 建议深度分析，考虑设计规避或申请许可 | 60-79% |
| 低风险 | 🟢 | 可继续推进，建议持续关注 | 40-59% |
| 无明显风险 | ⚪ | 未发现相关有效专利，风险极低 | <40% |

### 外观设计专利风险清单

每条记录包含：
- 专利号 + 链接
- 申请人/权利人
- 目标国家/受理局
- 法律状态
- 相似度分数
- 相似点说明
- 差异点说明
- 风险等级

### 发明专利风险清单

每条记录包含：
- 专利号 + 链接
- 发明名称
- 申请人/权利人
- 目标国家/受理局
- 法律状态（有效/审中）
- 权利要求命中情况（命中第X项独立权利要求）
- 技术特征比对摘要
- 风险等级

### 实用新型专利风险清单

（同发明专利格式）

### 规避建议

针对每个高/中风险专利给出具体规避建议：
1. **设计规避**：改变哪些外观特征可降低侵权风险
2. **技术绕开**：哪些技术方案替代路径可绕开专利保护
3. **许可协商**：是否值得与专利权人洽谈许可
4. **申请无效**：专利是否存在可攻击的瑕疵
5. **市场调整**：建议回避或暂缓进入的高风险市场

### 免责声明

> ⚠️ 本报告为AI辅助初筛结果，仅供参考，不构成法律意见。正式侵权判断需委托具有专业资质的专利律师进行权利要求解释和侵权分析。

---

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| 目标市场 | 优先检索的国家/地区 | US, EP, JP, KR, DE, GB, AU, CA |
| 检索深度 | 每类专利返回数量 | 外观20条，发明30条，实用新型20条 |
| 相似度阈值 | 纳入风险清单的最低相似度 | 40% |
| 法律状态过滤 | 仅关注有效和审中专利 | 是 |
| 报告语言 | 用户界面语言 | 中文（可切换英文） |

---

## 工具调用映射

| 步骤 | 工具 | 用途 |
|------|------|------|
| 图像上传 | `mcp_patsnap-patent-search__upload_patent_image` | 本地图片转公开URL |
| 图像理解 | `mcp_hub-mcp-gateway-novelty-search__novelty_pic2t` | 图转文特征提取 |
| 技术总结 | `mcp_hub-mcp-gateway-novelty-search__novelty_summary` | 提取技术三要素 |
| 关键词提取 | `mcp_hub-mcp-gateway-novelty-search__novelty_keywords_extract` | 检索要素生成 |
| 外观图搜 | `mcp_patsnap-patent-search__image_search_multiple` | 外观专利图像检索 |
| 语义检索 | `mcp_hub-mcp-gateway-novelty-search__novelty_semantic_search` | 发明专利语义搜索 |
| 实用新型图搜 | `mcp_patsnap-patent-search__image_search_multiple` | 实用新型图像检索 |
| 附图相似度 | `mcp_hub-mcp-gateway-novelty-search__novelty_abstract_figure_similarity` | 外观专利精细比对 |
| 特征比对 | `mcp_hub-mcp-gateway-novelty-search__novelty_feature_comparison_async` | 发明专利技术特征比对 |
| 法律状态 | `mcp_patsnap-patent-brief__legal_status` | 确认专利是否有效 |
| 著录信息 | `mcp_patsnap-patent-brief__bibliography` | 获取专利详情 |
| 页面抓取 | `web_fetch` | 从产品链接提取图片 |

---

## 注意事项

1. **图像净化**：pic2t接口会自动处理图片背景、水印等噪音，提取核心设计特征
2. **并行执行**：三条检索线路（外观/发明/实用新型）并行运行以节省时间
3. **法律状态优先**：无效专利自动降级排除，聚焦有效风险
4. **地域特异性**：不同市场的风险等级可能不同，分市场展示结果
5. **持续监控**：建议对高风险专利设置监控，及时获悉法律状态变化

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。

---
name: smart-construction-analysis
description: |
  智能建造技术深度分析技能：面向桥梁、隧道、高速公路等基础设施领域，融合专利、学术文献、商业报道、展会及成果转化案例等多维数据源，自动完成核心技术主体识别、专利布局分析、竞争格局评估，并生成HTML/Word双格式专业分析报告。
---

# 智能建造技术深度分析技能

## 能力概述

本技能面向交通基础设施（桥梁、隧道、高速公路）领域的智能建造技术进行系统性研究分析，
输出专业级深度分析报告。适用场景包括：技术竞争情报、专利布局研究、市场进入分析、
科研选题参考、项目技术尽调等。

## 数据源策略

本技能整合以下五类数据源，形成多维交叉验证的证据体系：

| 数据源类型 | 工具 | 覆盖内容 |
|-----------|------|---------|
| **专利数据** | PatSnap patent.search / patent.fetch | 技术布局、核心申请人、引用关系、法律状态 |
| **学术文献** | PatSnap paper.search / paper.fetch | 前沿研究方向、引用热度、关键机构 |
| **商业报道** | web.search + web_fetch | 企业动态、产品发布、市场格局 |
| **展会信息** | web.search | 技术展示、行业趋势、竞品对比 |
| **成果转化案例** | web.search + patent.search | 典型工程应用、效率提升数据 |

## 分析框架（六大维度）

### 1. 技术体系解构
- 核心技术栈识别（BIM / 数字孪生 / 智能控制 / 机器人 / AI感知）
- 技术成熟度分级（TRL评估）
- 各子领域技术关联图谱

### 2. 专利布局分析
- 检索策略：语义检索 + 关键词检索 + 申请人过滤三路并行
- 重点分析维度：申请人分布、IPC分类分布、授权率、引用次数、法律状态
- 输出：代表性专利列表（含智慧芽链接）

### 3. 学术研究热度
- 高被引文献识别（cited_min 阈值筛选）
- 机构合作网络
- 研究方向与产业应用的转化路径

### 4. 核心主体竞争格局
- 国内主体：技术优势、代表专利、工程案例
- 国际主体：技术壁垒、专利保护范围、商业化程度
- 竞争维度矩阵（设计软件 / 装备制造 / 控制算法 / 数字平台 / 国际布局）

### 5. 成果转化与工程案例
- 经典项目（含效率量化指标）
- 展会亮点（bauma / 工博会 / 国际工程机械展）
- 产学研合作模式

### 6. 趋势研判与挑战
- 无人化施工路线图
- AI大模型在施工决策层的渗透
- 数字孪生全生命周期延伸
- 标准化与集成瓶颈

## 检索关键词库

### 桥梁子域
- 中文：数字孪生 桥梁施工、BIM 桥梁智能建造、桥梁索结构智能张拉、预制构件智能吊装
- 英文：bridge digital twin, BIM smart construction, bridge health monitoring IoT

### 隧道子域
- 中文：盾构机智能掘进、TBM自动导向、隧道智能建造、盾构机姿态控制
- 英文：shield machine intelligent tunneling, TBM automatic guidance, tunnel smart construction

### 高速公路子域
- 中文：路面智能压实、摊铺机自动控制、智慧梁场、路基数字化监测
- 英文：intelligent compaction highway, paving machine automatic control, road digital twin

### 跨域通用
- BIM IoT infrastructure、digital twin transportation、construction robot automation

## 报告输出规范

### HTML报告（主格式）
- 顶部吸顶导航（平滑滚动）
- 统计卡片区（专利数、论文数、主体数、案例数）
- 各领域技术详情（专利列表含链接、主体对比表）
- 数字孪生架构四层图
- 竞争力矩阵进度条（滚动动画）
- 经典案例卡片（效率数字高亮）
- 趋势与结论深色区块
- 全文来源标注（[S#] 格式）

### Word报告（辅助格式）
- 使用 python-docx 生成
- 标准章节结构（一至十章）
- 表格样式统一（蓝色表头）
- 专利链接以文本形式嵌入
- 输出路径：EUREKA_PYTHON_OUTPUT_DIR/智能建造技术分析报告.docx

## 执行流程

```
Step 1: 并行检索
  ├── patent.search（桥梁专利 × 2组关键词）
  ├── patent.search（隧道专利 × 2组关键词）
  ├── patent.search（高速公路专利 × 1组关键词）
  ├── paper.search（BIM+IoT文献）
  └── web.search（商业报道 + 展会 + 案例）

Step 2: 精准获取
  ├── patent.fetch（高价值专利全文，含引用次数最高者）
  └── paper.fetch（高被引论文摘要）

Step 3: 综合分析
  ├── 技术主体识别与归类
  ├── 竞争格局矩阵构建
  ├── 成果转化案例提炼
  └── 趋势研判

Step 4: 报告生成
  ├── HTML报告（files begin_write + append + finish_write）
  └── Word报告（python-docx via python.run）
```

## 质量控制规范

- 所有核心结论必须有 [S#] 来源标注
- 专利引用格式：`[专利号](智慧芽链接) [S#]`
- 数量统计（matched_total / returned_count）不手写，直接引用工具输出
- 负面结论（如"某技术缺失"）须完成全量分页验证后才能断言
- 竞争力矩阵维度评分须基于证据，不凭主观推断

## 适用范围扩展

本技能的分析框架可扩展至其他基础设施智能建造方向：
- 地铁/轨道交通
- 港口码头
- 超高层建筑
- 水利水电大坝
- 海上风电基础

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。

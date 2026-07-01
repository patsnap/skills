---
name: j-patent-strategy-analyzer
description: |
  Jary66原创，企业战略专利布局分析（模板驱动版）。通过了解企业产品及经营动态与企业全球专利，做对比映射分析。从知产管理视角了解企业的专利布局情况、优势、不足、风险、下一步行动计划等。输出为独立HTML文件（所有CSS和图表内联，零外部依赖）。
---

# 企业专利战略匹配分析（模板驱动版）

## 工作流：七步生成法

0. **环境准备** — 【首次会话必须】通过 `runtime.apply_sync` 安装 Python 依赖（pandas / numpy / matplotlib / openpyxl），确保后续 Python 代码可执行
1. **数据加载** — 解析专利清单 → 建立`data`字典（含`df_active`候选池）
2. **情报采集** — 企业信息搜索 → 填充`company_info`+`business_info`
3. **数据分析** — 执行`data_prep.md`中的数据处理代码 → 完成全景统计/价值分层/发明人分析
4. **图表生成** — 按`chart_specs`生成5张matplotlib图表 → base64编码持久化
5. **HTML填充** — 按`html_skeleton.md`骨架+`section_specs.md`规范 → 逐节填充`data`到模板
6. **检查输出** — 执行22项检查清单 → 通过后输出最终HTML

**核心原则**：数据分析在Python层完成，HTML只负责展示。禁止在HTML构建阶段进行数据统计。

---

## 文件引用索引

| 文件 | 路径 | 内容 |
|------|------|------|
| HTML骨架模板 | `references/html_skeleton.md` | 完整的7页签21小节HTML框架（含全部CSS） |
| 小节填充规范 | `references/section_specs.md` | 每小节的输入数据/强制元素/HTML结构/填充示例 |
| 数据准备规范 | `references/data_prep.md` | `data`字典构建+数据处理代码+候选池建立 |

---

## 配色强制规则

- `#0a3dff` 科技蓝 — 主标题/激活页签/表头/关键数据
- `#0fcc7a` 增长绿 — 优势标记/Tier A/增长趋势
- `#D9D9D9` 中性灰 — 卡片底色/分隔线/交替行
- `#fff9e6` 结论黄 — 结论框背景

---

## 阶段零：环境准备（Python 依赖安装）

> ⚠️ **重要**：本阶段必须在阶段一之前执行。如果依赖未就绪，后续所有 Python 代码都会因 PyPI 超时而失败。
> 
> **平台兼容性说明**：目标平台（Eureka）使用托管 Python 运行时，按需通过 `runtime.apply_sync` 安装 PyPI 包。本 Skill 不假设依赖已预装，每次新会话必须从本阶段开始。

### 必须安装的依赖包

| 包名 | 用途 | 最小版本 |
|------|------|----------|
| pandas | DataFrame 数据加载、清洗、分组统计、透视表 | 2.0+ |
| numpy | 数值计算、数组操作 | 1.24+ |
| matplotlib | 5张分析图表生成 → base64 内联嵌入 | 3.7+ |
| openpyxl | Excel 读取引擎（`pd.read_excel` 后端） | 3.1+ |

### 执行流程（Agent 必须遵循）

**Step 1 — 检测当前环境**
```python
import importlib
required_packages = ['pandas', 'numpy', 'matplotlib', 'openpyxl']
missing = []
for pkg in required_packages:
    try:
        importlib.import_module(pkg)
    except ImportError:
        missing.append(pkg)

if missing:
    print(f"[环境准备] 以下依赖尚未安装：{missing}")
    print("[环境准备] 需要发起依赖安装请求，请用户审批")
    # → 进入 Step 2
else:
    print("[环境准备] 所有依赖已就绪 ✓")
    # → 直接进入阶段一
```

**Step 2 — 发起安装请求（需用户审批）**

Agent 操作指引：
1. 向用户发送消息："本报告需要安装以下 Python 包：pandas, numpy, matplotlib, openpyxl。请确认安装。"
2. 等待用户回复确认后，调用平台 `runtime.apply_sync` 能力安装依赖
3. 安装完成后，重新执行 Step 1 验证导入成功
4. 验证通过后，继续执行阶段一

**Step 3 — 验证安装结果**
```python
# 安装完成后必须执行验证
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # 无头模式，必须在导入 pyplot 之前设置
import matplotlib.pyplot as plt
import openpyxl
print(f"[环境准备] pandas {pd.__version__} ✓")
print(f"[环境准备] numpy {np.__version__} ✓")
print(f"[环境准备] matplotlib {matplotlib.__version__} ✓")
print(f"[环境准备] openpyxl {openpyxl.__version__} ✓")
print("[环境准备] 环境就绪，进入阶段一：数据加载")
```

### 复用机制

- **同一会话内**：安装成功后，当前会话所有后续 Python 代码块均可直接使用，无需重复安装
- **跨会话**：每次新会话需重新执行本阶段（依赖不持久化到磁盘）

### 平台 xlsx 读取兼容性

平台支持直接上传 `.xlsx` 文件并通过 Eureka 归一化文本视图读取。**本 Skill 仍使用 `pd.read_excel()` 读取**，原因：
- Excel 可能包含多 Sheet、合并单元格、日期格式等复杂结构
- `pd.read_excel()` + openpyxl 引擎是最稳健的方式
- 归一化文本视图会丢失列类型信息（数字变成字符串）

**无需用户手动转 CSV**，直接上传 Excel 即可。

### 故障排查

| 现象 | 原因 | 解决 |
|------|------|------|
| `runtime.apply_sync` 返回成功但仍无法 import | 缓存未生效或安装不完整 | 重新执行 Step 2（再次调用安装），或重启会话 |
| 安装过程卡住/无响应 | PyPI 网络超时 | 等待平台超时后重试，或反馈平台管理员 |
| `matplotlib` 图表生成失败 | 未设置 `Agg` 后端 | 确保在 `import matplotlib.pyplot` 前执行 `matplotlib.use('Agg')` |

---

## 阶段一：数据加载（解析专利清单）


**前置排除规则【强制】**：第十四节候选池`df_active`在本步骤建立，排除以下已终结法律状态的专利（原始值匹配）：
- `期限届满` — 保护期已满
- `视为撤回` / `撤回-主动撤回` — 申请已终止
- `驳回` — 审查未通过
- `避免重复授权` — 已有授权专利覆盖
- `PCT指定期满` — PCT国际阶段已过期

排除后仅保留法律状态为**有效**或**审中**的专利进入候选池。

```python
# 加载→清洗→映射→建候选池→组装data字典
# 详细代码见 references/data_prep.md，按顺序执行：一~九
```

> **【重要】技术类别映射可配置性**：`data_prep.md` 中的 `TECH_CATEGORY_MAP` 包含示例行业关键词（制药/化工设备类）。**使用本技能时，必须根据被分析企业的实际行业重新定义该映射表**，否则第八节价值分布热力图的技术类别将全部归为"其他"，失去分析价值。

**硬检查点**：`len(df) > 0` / `df_active`已建立 / 申请号/公开号未去重 / snapshot已写入

---

## 阶段二：情报采集（企业信息搜索）

### 营收/利润数据年份优先级（强制）

**【强制搜索顺序】必须严格执行以下步骤**：
1. **第1步**：搜索`"{company_name} {report_date.year}年 年报 营收 净利润"`，如数据完整则使用
2. **第2步**：搜索`"{company_name} {report_date.year-1}年 年报 营收 净利润"`，须标注"（{report_date.year-1}年）"
3. **第3步**：搜索`"{company_name} {report_date.year-2}年 年报 营收 净利润"`，须标注"（{report_date.year-2}年）"
4. **第4步（兜底）**：若前3步均无结果，尝试搜索`"{company_name} 年报 营收"`（不指定年份），取搜索结果中最近年份

**【强制多词搜索】**：每一步必须同时尝试以下搜索词组合（至少3组）：
- `"{company_name} {year}年报 营收 净利润"`
- `"{company_name} {year}年 营业收入 归母净利润"`
- `"{company_name} {year}年度 财务数据 营收"`
- `"{company_name} {year} 年度报告 利润总额"`

**【禁止】**：
- 直接默认使用任何年份数据而不经过上述搜索步骤
- 使用report_date.year之前的年份数据时不标注年份

**【标注格式】**：`最近一年营收（YYYY）`和`最近一年净利润（YYYY）`
- 示例：`最近一年营收（2025）`、`最近一年净利润（2025）`

**【年份确认】**：在填写KPI前，必须通过反问确认：`"已找到{year}年营收数据：XX亿元，是否使用？"`，确保年份正确。

```python
def get_latest_financial(company_name, report_year):
    """获取企业最新营收数据。

    【重要】search() 为平台搜索工具占位符（如 web_search / browser_search），
    实际执行时需替换为当前环境可用的搜索函数。返回值为 dict，至少包含 'revenue' 键。"""
    search_patterns = [
        "{name} {year}年报 营收 净利润",
        "{name} {year}年 营业收入 归母净利润",
        "{name} {year}年度 财务数据 营收",
        "{name} {year} 年度报告 利润总额",
    ]
    for year_offset in [-1, -2]:
        year = report_year + year_offset
        for pattern in search_patterns:
            data = search(pattern.format(name=company_name, year=year))
            if data and data.get('revenue'):
                return data, year
    # 兜底：不指定年份搜索
    data = search(f"{company_name} 年报 营收")
    return data, data.get('year') if data else None
```

### 采集要素
- 基本信息：成立时间/总部/上市状态/营收/净利润
- 业务板块：第一曲线(核心)/第二曲线(增长)/第三曲线(探索)
- 名称变体：中英文注册名/品牌名/子公司名/历史名
- 科技资质：高新企业/专精特新/标准参与
- 竞争对手：3-5家竞品的核心业务/营收/优势

搜索渠道：web_search（企业年报/新闻/行业报告）

---

## 阶段三：数据分析（执行data_prep.md）

按`data_prep.md`顺序执行：
1. 法律状态映射（三分类：有效/审中/失效）
2. 候选池建立（`df_active`）
3. 技术类别映射（第八节价值热力图前置步骤，见 data_prep.md 第三章）
4. 全景统计（第七节数据源）
5. 价值分层Tier A/B/C（第八节数据源）
6. 发明人统计Top15+年份矩阵+技术矩阵（第十一节数据源）
7. 持久化snapshot + 组装`data`字典（见 data_prep.md 第七~八章）

---

## 阶段四：图表生成

**【禁止pie()前置规则】**：chart4法律状态图必须使用`barh()`横向条形图，代码中禁止出现`plt.pie()`。

| 图表 | 类型 | figsize | 数据源 |
|------|------|---------|--------|
| chart1 年度趋势 | 折线图+柱状图 | (10,5) | `panorama['yearly_trend']` |
| chart2 发明人排行 | 双Y轴分组柱状图(专利数+价值) | (10,5) | `inventor_data['inv_values']` |
| chart3 技术热力图 | 矩阵热力图【必须放在第十一节】 | (10,6) | `inventor_data` × 技术主题 |
| chart4 价值分布 | 横向条形图+柱状图【禁止pie】 | (10,4.5) | `panorama` + `tier_meta` |
| chart5 发明人趋势 | 矩阵热力图【必须放在第十一节】 | (10,5) | `inventor_data['inv_year']` |

---

## 阶段五：HTML填充（核心步骤）

**填充方法**：复制`html_skeleton.md`模板 → 替换`{{变量名}}`占位符 → 按`section_specs.md`逐节填入内容。

### 【强制】执行约束规则 -- 违反将导致报告不合格

以下行为**严格禁止**，违反任意一条即视为违规输出，必须回溯修正：

| 禁止行为 | 正确做法 | 违规后果 |
|----------|----------|----------|
| **改变小节标题** | 严格使用 section_specs.md 定义的标题文字，一字不改 | 检查清单 `20_sections` 失败 |
| **删减强制元素** | 每小节的 `- [ ] 强制元素` 清单必须全部实现，不可省略 | 结构性缺陷，平台验证失败 |
| **替换规范定义的HTML结构** | 复制 section_specs.md 的HTML结构示例，仅替换内容 | 格式不符，用户拒收 |
| **混用"核心结论"和"本小节结论"** | 统一使用 `本小节结论：`，section_specs.md 有示例的从其示例 | 格式不统一 |
| **改变KPI网格数量** | 第一节=12格，第七节=10格，数量固定不可增减 | 信息缺失 |
| **遗漏 `[S#]` 来源标记** | 每条结论 `<li>` 末尾必须含 `[S#]</li>` | 平台标记 Unverified |
| **将图表放在错误小节** | chart2/chart3/chart5 必须放在第十一节 | 结构混乱 |
| **第二十一节添加 `.section-title`/`.section-subtitle`** | 第二十一节不编号，不设置标题/副标题，用 `.report-review` 包裹 | 违反规范 |
| **擅自发明 section_specs.md 未定义的元素** | 只能使用 section_specs.md 定义的元素，不可自创 | 偏离规范 |

### 【强制】逐节强制元素检查（阶段五-A）

**每填充完一小节，立即执行以下检查**，未通过则当场修正，不可累积到阶段六：

```python
def check_section(section_html, section_num, mandatory_items):
    """逐节强制元素验证 -- 在阶段五每节填充后立即调用。
    section_html: 刚生成的小节HTML字符串
    section_num: 节号（1-21）
    mandatory_items: 该节必须包含的字符串/特征列表
    """
    missing = []
    for item in mandatory_items:
        if item not in section_html:
            missing.append(item)
    if missing:
        print(f"[FAIL] 第{section_num}节缺失强制元素: {missing}")
        print(f"[ACTION] 立即修正第{section_num}节，补充上述缺失元素后继续")
        return False
    print(f"[PASS] 第{section_num}节强制元素检查通过")
    return True
```

**21节强制元素清单速查**（每次填充后逐条核对）：

| 节 | 必须包含的文本/特征 |
|----|---------------------|
| 一 | 12个 `kpi-card`、`最近一年营收（`、`最近一年净利润（`、`本小节结论：` |
| 二 | `two-col`（双栏）、科技资质表格、`ALL_AN:(` 检索代码块 |
| 三 | `curve-card blue`、`curve-card green`、`第.*增长曲线`、底部`[S2]` |
| 四 | `timeline-item`（至少4个）、竞品表格、最后一个节点绿色 |
| 五 | `tier-card positive`、`tier-card accent`、`tier-card graybox`、星级 `★` |
| 六 | `two-col`（双栏）、`product-cards`、热度进度条 `cover-bar`、趋势图标 `▲▼` |
| 七 | `patent-stats`（10格）、发明申请→授权→实用→外观（严格顺序）、法律状态表、chart1的`<img>` |
| 八 | `tier-card`（3个大数字）、代表专利表（3×5件）、`.heatmap-star-table`、chart4的`<img>` |
| 九 | 匹配分析表格（固定表头）、汇总表格（固定表头）、彩色匹配评估标签 |
| 十 | `gap-card urgent`、`gap-card important`、`gap-card opportunity`、每个含 `.dot-` |
| 十一 | chart2的`<img>`、chart3的`<img>`、chart5的`<img>`、`.side-green`专长卡片、`.side-blue`协作卡片、研发效率建议 `.side-green` |
| 十二 | `trend-col-grow`、`trend-col-decline`、近期专利质量趋势分析 |
| 十三 | 4个 `kpi-big` 大字KPI、`.score-bar-gradient`渐变条、双栏评分矩阵、`.overseas-advice`、海外侵权Top5表格 |
| 十四 | 黄色免责声明框、放弃建议表格（固定表头）、优化方向表格（固定表头） |
| 十五 | 覆盖矩阵（8列表头）、P0/P1/P2分级定义表格 |
| 十六 | `.swot-grid`（4象限）、`.three-col`（三栏建议）、专利运营子卡片组（3个彩色卡片） |
| 十七 | `two-col`（双栏策略）、策略矩阵表格、策略标签（强化型/布局型/追赶型） |
| 十八 | `.timeline-item`（4级时间线）、每条5要素（目标/事项/原因/价值/预期）、蓝色补全价值框 `background:#e6eeff` |
| 十九 | IP团队使用场景表格（4列表头）、研发团队使用场景表格（同结构） |
| 二十 | `action-ip`（蓝色渐变）、`action-rd`（绿色渐变）、`☐`空心方框、信息来源标注"第XX小节" |
| 二十一 | **无** `.section-title`/`.section-subtitle`、`.report-review`独立区块、Eureka引导语在正文前、健康度评分 |

> **【关键执行纪律】**：每完成一小节，停顿一下，对照上表逐条验证。任何一项缺失，立即补充后再进入下一节。禁止"先写完再回头补"。

### 填充顺序（严格按编号）

```
封面页 → 页签导航 →
  tab-overview:   第一节(12格公司信息) → 第二节(双栏+名称变体) →
  tab-business:   第三节(曲线卡片) → 第四节(时间线+竞品) → 第五节(三梯队卡片) → 第六节(双栏+产品卡片) →
  tab-assets:     第七节(10大字KPI网格+类型表格+趋势图+地域) → 第八节(Tier卡片+代表专利+热力图) →
  tab-mapping:    第九节(进度条+汇总表格) → 第十节(三级缺口卡片) →
  tab-team:       第十一节(排行图+热力图+专长+协作+表格+效率建议) → 第十二节(双栏前瞻+近期专利质量趋势) → 第十三节(风险KPI+评分+矩阵+侵权Top5+海外建议) →
  tab-strategy:   第十四节(免责声明+表格) → 第十五节(覆盖矩阵+分级) → 第十六节(SWOT+三栏) → 第十七节(双栏策略+矩阵) → 第十八节(四级时间线) → 第十九节(双表格) →
  tab-action:     第二十节(双栏待办+结论) → 第二十一节(报告综述)
```

### 21小节强制元素速查表

| 节 | 强制格式 | 不可省略元素 |
|----|----------|-------------|
| 一 | 12格公司信息卡 | section-subtitle+conclusion-box |
| 二 | 双栏+名称变体表 | 检索建议代码块 |
| 三 | 2-3曲线卡片 | 第一曲线(蓝)+第二曲线(绿)+第三曲线(黄) |
| 四 | 纵向时间线+竞品表 | 蓝色竖线+绿色终点 |
| 五 | 三梯队卡片 | positive(蓝)+accent(绿)+graybox(黄) |
| 六 | 双栏+产品卡片 | 热度进度条+趋势图标 |
| 七 | 10大字KPI网格+类型表+趋势图+地域 | 类型严格顺序：发明申请→授权→实用新型→外观；状态严格顺序：有效、审中、失效 |
| 八 | Tier卡片+代表专利表+**价值分布热力图** | 每个Tier 3-5件+去重；A前20%/B中40%/C后40% |
| 九 | 进度条表格+**汇总表格** | 增长曲线命名：第X曲线(产品名)；两表固定表头 |
| 十 | **三级缺口卡片** | urgent(红)+important(橙)+opportunity(蓝) |
| 十一 | 排行图+热力图+**专长卡片+协作卡片+表格+效率建议** | chart2双Y轴+chart3热力图+chart5发明人趋势图(必放本节)+研发效率指标表+5条建议 |
| 十二 | **双栏前瞻卡片+近期专利质量趋势** | grow(绿左框)+decline(红左框) |
| 十三 | 风险KPI+评分仪表盘+**矩阵+侵权Top5+海外建议** | 4个大字KPI+6维度评分条+海外布局建议overseas-advice |
| 十四 | 免责声明+建议表+优化表 | **排除校验**(无6种终结法律状态)；两表固定表头 |
| 十五 | 覆盖矩阵+分级表 | P0/P1/P2分级定义；矩阵8列固定表头 |
| 十六 | SWOT四象限+**三栏建议** | 专利运营管理建议+产品立项建议+产学研合作建议 |
| 十七 | 双栏(产品链+产业链)+矩阵表 | 策略标签(3种彩色)：强化型(绿)/布局型(蓝)/追赶型(黄) |
| 十八 | **四级时间线** | 每条含目标/事项/原因/价值/预期+**补全价值蓝色提示框** |
| 十九 | IP表+研发表 | 可执行建议+责任岗位 |
| 二十 | **双栏待办** | action-ip(蓝)+action-rd(绿)+☐+序号+行动描述+信息来源 |
| 二十一 | **报告综述独立区块** | Eureka引导语(平台提示+专业把关)+200-300字+五要素+健康度评分 |

---

## 阶段六：检查输出（22项清单）

> **【可执行性说明】** 以下 `run_checklist()` 函数为**技能内部参考代码片段**，设计为在已定义 `html` 变量的上下文中调用（如 Jupyter Notebook 或集成开发环境）。**不可直接保存为独立 .py 脚本运行**--若提取为独立文件执行会因 `html` 变量未定义而报错（exit_code=1）。如需在独立脚本中使用，必须自行提供 `html` 变量（如从文件读取HTML内容）。

```python
import re

def run_checklist(html):
    """22项检查清单 -- 独立函数，避免花括号转义问题。
    调用方式：checks = run_checklist(html_string)
    返回值：dict，key=检查项名，value=True/False

    【前置条件】变量 html 必须已定义，值为待检查的HTML字符串。
    【安全调用包装--在独立脚本中使用】
        with open('report.html', 'r', encoding='utf-8') as f:
            html = f.read()
        checks = run_checklist(html)
    """
    return dict([
        ('no_pie', 'pie(' not in html.lower()),
        ('7_tabs', len(re.findall(r'id="tab-\w+"', html)) == 7),
        ('20_sections', len(re.findall(r'[一二三四五六七八九十]+、', html)) >= 20 or len(re.findall(r'class="section-title"', html)) >= 20),
        ('conclusion_boxes', len(re.findall(r'class="conclusion-box"', html)) >= 20),
        ('source_hints', len(re.findall(r'class="source-hint"', html)) >= 20),
        ('curve_cards', 'curve-cards' in html),
        ('tier_cards', 'tier-card positive' in html),
        ('gap_cards_3level', all(k in html for k in ['gap-card urgent','gap-card important','gap-card opportunity'])),
        ('nine_progress_bar', 'cover-bar' in html),
        ('swot_three_col', 'three-col' in html and '专利运营' in html),
        ('report_review', 'report-review' in html),
        ('eureka_guide', 'Eureka' in html),
        ('sec14_no_exclude', all(k not in html for k in ['期限届满','视为撤回','撤回-主动撤回','驳回','避免重复授权','PCT指定期满'])),
        ('timeline_4levels', html.count('timeline-item') >= 4),
        ('value_heatmap', '价值分布' in html),
        ('inventor_detail_table', '核心发明人' in html),
        ('overseas_patent', '海外专利' in html),
        ('supplement_value_boxes', '补全价值' in html),
        # 新增：每条结论<li>必须有[S#]内联来源标记
        # [S#]内联来源标记：每条结论<li>末尾必须有[S1]~[S5]
        ('s3_citations', len(re.findall(r'\[S[1-5]\]</li>', html)) >= 40),
        # 5张图表全部base64内联嵌入
        ('chart2_inventor_rank', 'data:image/png;base64' in html and html.count('data:image/png;base64') >= 5),
        # 新增：第一节必须有12格KPI
        ('sec1_12kpi', html.count('kpi-card') >= 12),
        # 新增：第二节必须有科技资质表格+ALL_AN检索代码
        ('sec2_tech_qual', '科技资质' in html and 'ALL_AN:(' in html),
        # 新增：第七节必须有法律状态分布表格
        ('sec7_status_table', '法律状态' in html and '有效' in html and '审中' in html and '失效' in html),
        # 新增：第十一节必须有技术专长卡片+协作网络+研发效率建议
        ('sec11_specialty', '技术专长' in html and '协作网络' in html and '研发效率' in html),
        # 新增：第十三节必须有双栏评分矩阵
        ('sec13_dual_score', '专利布局角度' in html and '侵权风险角度' in html),
        # 新增：第十五节必须有P0/P1/P2分级表
        ('sec15_p0p1p2', 'P0' in html and 'P1' in html and 'P2' in html and '分级定义' in html),
        # 新增：第二十一节不能有section-title/section-subtitle
        ('sec21_no_title', 'class="section-title">二十一' not in html and ('report-review' not in html or html.rfind('class="section-subtitle"') < html.find('report-review'))),
        # 新增：结论标题统一性检查
        ('conclusion_title_uniform', html.count('本小节结论：') >= 18 or html.count('核心结论：') < 3),
    ])

# 【安全执行模式】仅在 html 变量已定义时运行检查
if 'html' in globals() and isinstance(html, str) and html.strip():
    checks = run_checklist(html)
    all_pass = all(checks.values())
    for name, result in checks.items():
        print(f"  [{'PASS' if result else 'FAIL'}] {name}")
else:
    print("[INFO] html 变量未定义或为空，检查清单未执行。请确保HTML内容已加载到 html 变量后重试。")
    print("[TIP] 如需检查独立HTML文件，请先执行：with open('report.html', 'r', encoding='utf-8') as f: html = f.read()")
```

**【关键】** `run_checklist()` 是独立函数，内部 `dict([...])` 形式避免与外部 f-string 花括号冲突。如需嵌入字符串模板，必须先定义函数再调用，不可将 `dict({...})` 字面量直接写入 f-string 中。

**检查项说明**（28项）：
- 基础18项：`no_pie`、`7_tabs`、`20_sections`、`conclusion_boxes`、`source_hints`、`curve_cards`、`tier_cards`、`gap_cards_3level`、`nine_progress_bar`、`swot_three_col`、`report_review`、`eureka_guide`、`sec14_no_exclude`、`timeline_4levels`、`value_heatmap`、`inventor_detail_table`、`overseas_patent`、`supplement_value_boxes`
- `s3_citations`：验证所有结论 `<li>` 都包含 `[S#]` 内联来源标记（`[S1]`~`[S5]`），至少40处匹配
- `chart2_inventor_rank`：验证5张图表全部base64内联嵌入
- **【新增结构检查项-8项】**：
  - `sec1_12kpi`：第一节必须有12格KPI（防止只填8格）
  - `sec2_tech_qual`：第二节必须有科技资质表格+ALL_AN检索代码
  - `sec7_status_table`：第七节必须有法律状态分布表格
  - `sec11_specialty`：第十一节必须有技术专长卡片+协作网络+研发效率建议
  - `sec13_dual_score`：第十三节必须有双栏评分矩阵
  - `sec15_p0p1p2`：第十五节必须有P0/P1/P2分级定义表格
  - `sec21_no_title`：第二十一节不能有section-title/section-subtitle
  - `conclusion_title_uniform`：结论标题统一为"本小节结论："

**全部通过 → 输出HTML文件。任何失败 → 定位问题节 → 修复 → 重新检查。**

### 【强制】验收流程 -- 未通过禁止输出

```
阶段六执行流程：
  1. 运行 run_checklist(html) 获取全部检查结果
  2. 如果有任意一项为 FAIL：
     a. 记录失败的检查项名称
     b. 根据【回溯修正指南】定位到具体小节
     c. 修改对应小节的HTML内容
     d. 重新运行 run_checklist(html)
     e. 重复直到全部 PASS
  3. 如果全部 PASS：
     a. 执行最终验证（检查文件大小500KB-2MB）
     b. 输出HTML文件
     c. 报告完成
  4. 如果经过3轮回溯仍无法全部通过：
     a. 向用户报告具体失败的检查项
     b. 说明已尝试的修正措施
     c. 请求用户指导如何处理
```

### 回溯修正指南

| 失败检查项 | 定位方法 | 修正措施 |
|------------|----------|----------|
| `20_sections` | 搜索 `class="section-title">` | 检查是否有小节标题被篡改或遗漏，对照 section_specs.md 恢复 |
| `conclusion_boxes` < 20 | 搜索 `class="conclusion-box"` | 检查是否有小节遗漏结论框，对照21节清单补全 |
| `s3_citations` < 40 | 搜索 `</li>` 不含 `[S` 的 | 给缺失 `[S#]` 的 `<li>` 末尾添加 `[S3]</li>` |
| `sec1_12kpi` | 搜索第一节 `kpi-card` | 确保第一节有12个 `kpi-card`，数量不足则补充 |
| `sec2_tech_qual` | 搜索第二节 "科技资质" | 添加科技资质表格和 `ALL_AN:(` 检索代码块 |
| `sec7_status_table` | 搜索第七节 "法律状态" | 添加法律状态分布表格（有效/审中/失效三行） |
| `sec11_specialty` | 搜索第十一节 "技术专长" | 添加 `.side-green` 专长卡片、`.side-blue` 协作卡片、研发效率建议 |
| `sec13_dual_score` | 搜索第十三节 "专利布局角度" | 添加双栏评分矩阵（左栏布局50分+右栏侵权50分） |
| `sec15_p0p1p2` | 搜索第十五节 "P0" | 添加 P0/P1/P2 分级定义表格 |
| `sec21_no_title` | 搜索 `report-review` 前的 `section-title` | 移除第二十一节的 `.section-title` 和 `.section-subtitle` |
| `conclusion_title_uniform` | 搜索 "核心结论：" | 将所有 "核心结论：" 替换为 "本小节结论：" |

> **【铁律】**：检查清单未全部通过前，**绝对禁止**向用户输出HTML文件。这是防止不合格报告流出的最后一道防线。

---

## 输出规范

- **HTML文件名**：`{{company_cn}}_企业战略专利分析报告.html`
- **CSS/JS**：完全内联，图表base64嵌入
- **文件大小**：通常500KB-2MB
- **压缩包**：HTML + README.txt（可选加PDF）

---

## 会话中断恢复

每完成5节保存checkpoint（`checkpoint_sec{N}.json`），中断后：
1. 加载`patent_snapshot.json`恢复数据层
2. 加载最新checkpoint恢复HTML内容
3. 从断点继续填充

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。

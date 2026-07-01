---
name: patent-quality-review-pro
description: |
  专利申请文件质量审核工具（全量指标版）。上传PDF或Word版专利申请文件，自动对全部评审指标进行统一评审（无重点/非重点分档），结合复审无效实践中的常见决定要点辅助判断，并生成标准格式《专利申请文件质量评价表》Word文件（主表+附表1，两页分页）。支持化学/机械/电学/通用四领域AHP权重方案自动切换；权利稳定性须显式加载 novelty-check 与 non-obviousness-check。
---

# 专利申请文件质量审核工具（全量指标版）

## 功能概述

本工具（patent-quality-review-pro）是专利申请文件质量审核的全量指标版本：

- **全量评审模式**：对所有评价指标统一评审，无重点/非重点分档
- **复审无效决定要点集成**：结合 DP1–DP20 及 DP-C1~C3 辅助判断权利稳定性和撰写质量
- **领域权重自动切换**：支持化学/机械/电学/通用四领域 AHP 权重方案
- **官方技能边界对齐**：新颖性仅使用 `novelty-check` 单参考对比逻辑，创造性仅使用 `non-obviousness-check` 多参考组合逻辑
- **Word 输出**：生成标准格式《专利申请文件质量评价表》，含主表+附表1，共两页

**运行环境要求**：需要 `python-docx` 库（运行前自动检查并安装）。

---

## 运行问题与解决方案

### 问题1：Word 文件内容空白
**根本原因**：环境变量传递中文 JSON 时字符丢失。
**解决方案**：先用 `files.write` 将完整 JSON 写入文件，再通过 `--data` 参数传路径。

### 问题2：字体出现彩色
**解决方案**：`set_run_font()` 中强制设置 `run.font.color.rgb = RGBColor(0, 0, 0)`。

### 问题3：python-docx 依赖包未预装
**解决方案**：运行脚本前先调用 `runtime.apply_sync` 安装 `python-docx`。

### 问题4：生成后没有自动打开输出目录
**根本原因**：使用了 `@session/...` 这类 Eureka handle 执行系统打开命令，系统命令无法解析该 handle。
**解决方案**：使用 `word_output_manifest.json` 中的 `output_dir_path` 或 `word_path` 绝对路径打开。脚本已内置跨平台打开目录：Windows 用 `os.startfile`，macOS 用 `open`，Linux/其他桌面环境用 `xdg-open`。

### 问题5：AHP领域确认问卷格式（先问后评）
**根本原因**：AI在未向用户确认领域的情况下直接开始评审，导致权重方案选择不透明。
**解决方案**：收到专利文件后，先快速阅读摘要和独立权利要求，判断技术领域倾向，然后**必须**按以下标准格式向用户提问，等用户确认后再执行评审：

**标准问卷格式：**
```
本专利涉及[简述技术领域，如：机械传动/电机控制/化学合成等]，
IPC分类号为[XXX]，主要技术特征为[简述核心特征]，
初步判断属于[领域名称]领域。

请选择权重方案：
A. 化学领域（含材料、生物、医药）
B. 机械领域（含机电一体化）← 【AI推荐】
C. 电学领域（含软件、通信、计算机）
D. 使用通用权重
```

**执行要求：**
- 必须给出 AI 推荐选项（在对应选项后标注 `← 【AI推荐】`）及简短理由
- 必须等用户回复确认后，才能继续执行 Step 3 及后续评审流程
- 禁止在用户未确认领域的情况下自行默认选择并直接开始评审

### 问题6：输出文件命名不规范
**根本原因**：AI调用 `generate_word.py` 时，`--output` 参数未严格遵守命名规范，使用了缩写前缀（如 `质量评价表_`）和错误分隔符（如下划线 `_`）。
**解决方案**：`--output` 参数必须严格按以下格式构造：

```
@session/output/专利申请文件质量评价表+{输入文件名去扩展名}.docx
```

**正确示例：**
- 输入文件 `CN120243995A.pdf` → `@session/output/专利申请文件质量评价表+CN120243995A.docx`
- 输入文件 `某专利申请.docx` → `@session/output/专利申请文件质量评价表+某专利申请.docx`

**禁止写法：**
- ❌ `质量评价表_CN120243995A.docx`（前缀缩写 + 下划线分隔）
- ❌ `专利质量评价表+CN120243995A.docx`（前缀不完整）
- ❌ `专利申请文件质量评价表_CN120243995A.docx`（分隔符错误）
- ❌ `发明专利申请文件质量评价表_CN120243995A.docx`（前缀多余"发明"二字 + 下划线分隔）
- ❌ `@session/outputs/专利申请文件质量评价表+CN120243995A.docx`（目录为 `outputs` 而非 `output`）

### 问题7：JSON字段名错误（basic.title → basic.patent_name）
**根本原因**：AI构造 review_data JSON 时，将专利名称字段写为 `basic.title`，但 `generate_word.py` 脚本期望的字段名为 `basic.patent_name`，导致 Word 文件中专利名称一栏为空。
**解决方案**：构造 `basic` 对象时，专利名称字段必须使用 `patent_name` 而非 `title`。

**正确写法：**
```json
"basic": {
  "patent_name": "一种转子车削装置",
  "tech_field": "机械",
  "agency": "",
  "agent": "",
  "agent_tel": ""
}
```
**禁止写法：**
- ❌ `"basic": { "title": "一种转子车削装置" }`（字段名错误）

### 问题8：scores字段格式错误（字典格式 → 列表4元组格式）
**根本原因**：AI构造 review_data JSON 时，将 `scores` 写为字典格式（`{"指标名": 分数}`），但 `generate_word.py` 脚本期望的是列表格式，每项为包含4个元素的数组 `[指标名, 原始分, 加权分, 问题描述]`，导致脚本解析失败或表格数据错误。
**解决方案**：`scores` 字段必须使用列表格式，每个元素为包含4个元素的数组。

**正确写法：**
```json
"scores": [
  ["①技术方案表述（12%）", 85, 10.20, "问题描述文本"],
  ["②保护范围规划（12%）", 78, 9.36, "问题描述文本"],
  ["③权利稳定性（10%）", 72, 7.20, "问题描述文本"],
  ["④权利要求布局（18%）", 75, 13.50, "问题描述文本"],
  ["⑤背景技术论述（10%）", 82, 8.20, "问题描述文本"],
  ["⑥技术问题与技术效果论述（8%）", 80, 6.40, "问题描述文本"],
  ["⑦说明书充分公开情况（18%）", 75, 13.50, "问题描述文本"],
  ["⑧形式问题（12%）", 80, 9.60, "问题描述文本"]
]
```
**禁止写法：**
- ❌ `"scores": { "①技术方案表述": 85, ... }`（字典格式，脚本无法解析）
- ❌ `"scores": [ {"name": "①技术方案表述", "score": 85} ]`（对象列表格式，非4元组）

### 问题9：issues字段格式错误（字典格式 → 6元组列表格式）
**根本原因**：AI构造 review_data JSON 时，将 `issues` 每项写为字典格式（`{"no":1, "level":"重要", ...}`），但 `generate_word.py` 脚本执行 `seq, level, name, loc, desc, sug = item` 直接按位置解包，字典不支持按位置解包，导致附表1全部问题行内容为空。
**解决方案**：`issues` 字段每项必须使用6元组列表格式，按位置顺序填写：`[序号, 严重程度, 问题名称, 涉及位置, 问题描述, 修改建议]`。

**正确写法：**
```json
"issues": [
  [1, "重要", "必要技术特征完整性", "权利要求1", "独立权利要求缺少XXX必要技术特征，导致技术方案不完整（援引DP13）", "建议在独立权利要求中补充XXX特征"],
  [2, "重要", "功能性限定充分公开", "权利要求1、说明书实施例", "功能性限定特征XXX在说明书中仅有单一实施例支撑，未覆盖整个保护范围（援引DP10）", "建议补充至少一种替代实施方式"],
  [3, "一般", "相对性语言明确性", "权利要求1", "权利要求1中XXX表述含义不确定（援引DP14）", "建议改为具体数值或结构限定"]
]
```

**禁止写法：**
- ❌ `"issues": [{"no":1, "level":"重要", "name":"...", "loc":"...", "desc":"...", "sug":"..."}]`（字典格式，无法按位置解包，附表1全部为空）
- ❌ `"issues": [[1, "重要", "问题名", "位置", "描述"]]`（只有5个元素，缺少第6项「修改建议」，解包失败）

### 问题10：main.py 输出格式与 generate_word.py 期望格式脱节
**根本原因**：`main.py` 生成 `review_data.json` 时采用 **旧版 `indicators` 数组格式**（顶层含 `patent_no`、`indicators`、`overall_assessment`），而 `generate_word.py` 已升级为期望 **V2格式**（顶层含 `basic`、`scores`、`issues`、`total_score`、`conclusion`），两者数据契约完全脱节，导致脚本访问 `DATA["basic"]` 时抛出 `KeyError`，Word 主表基本信息全空，评分表和附表1均无内容。

**具体差异：**

| 字段 | generate_word.py 期望（V2格式） | main.py 实际输出（旧格式） |
|------|--------------------------------|--------------------------|
| 顶层结构 | `basic`、`scores`、`issues`、`total_score`、`conclusion` | `patent_no`、`indicators`（数组）、`overall_assessment` |
| 专利名称 | `basic.patent_name` | `patent_name`（平铺） |
| 评分条目 | `scores`（8项4元组列表） | `indicators`（8条含id/name/max_score/score的对象） |
| 问题列表 | `issues`（扁平6元组列表） | 各indicator内嵌独立issues数组 |
| 评审人信息 | `reviewer_name`、`review_date` | 不存在 |

**解决方案**：AI执行评审后，**必须直接构造 V2格式 JSON**（而非依赖 `main.py` 输出），再调用 `generate_word.py`。V2格式构造规则详见问题7、8、9。禁止将 `main.py` 的 `indicators` 格式输出文件直接传给 `generate_word.py`。

### 问题11：传入了错误的数据文件（review_data.json 而非 review_data_v2.json）
**根本原因**：工作区中同时存在 `review_data.json`（旧格式）和 `review_data_v2.json`（V2格式）两个文件，AI调用 `generate_word.py` 时误传了旧格式文件 `review_data.json`，导致 Word 表格内容为空。
**解决方案**：
- 调用 `generate_word.py` 时，`--data` 参数必须明确指定 **V2格式数据文件**（即 AI 本次评审后直接写出的 `review_data_v2.json`）。
- 禁止使用 `review_data.json`（`main.py` 的旧格式输出）作为 `--data` 参数传入 `generate_word.py`。
- 最佳实践：AI每次评审结束后，直接将 V2格式 JSON 写入 `@skill_workspace/review_data_v2.json`，调用脚本时固定使用该文件，不再使用 `review_data.json`。

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。

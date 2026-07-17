# Legacy company patent workflow

Use this file only for detailed enrichment rules and historical error cases.

## Contents

- Original scope, inputs, and workbook schema
- Historical subsidiary examples
- Search, pagination, and Excel-writing steps
- Kind-code, date, IPC, legal-status, target, and summary enrichment
- Quality gates and known issues
- Excel formatting implementation

---
name: biopharma-patent-landscape
description: 专利调研 Skill：输入公司名称，自动确认英文名/中文名/子公司列表（含2轮自检），检索该公司及所有子公司近3个月专利，输出标准化 Excel 文件（Sheet1=企业信息，Sheet2=专利清单，固定列结构）。支持23家已核定药企批量执行，含分页补全、vespa错误重试、进度保存机制。检索完成后继续执行 Step 4（专利类型判断）、Step 5（申请日/公开日批量获取）、Step 6（IPC分类号/法律状态批量补全），写入 Sheet2 G/H/I/J/K 列。
version: 0.7.0
tags:
  audience:
    - ip
  need:
    - search
    - report
  data:
    - patent
    - company
---

# Patent Research Skill — 专利调研

## 定位

输入一个公司名称（中文或英文均可），完成以下全流程：

1. **Step 0** — 企业信息初始化：确认英文名、中文名、子公司列表（含2轮强制自检）
2. **Step 1** — 构建检索申请人列表
3. **Step 2** — 专利检索（近3个月，CN/US/EP/WO 四局）
4. **Step 3** — Excel 基础输出（专利链接、公司中英文、申请主体）
5. **Step 4** — 专利类型判断，写入 Sheet2 G 列
6. **Step 5** — 申请日/公开日批量获取，写入 Sheet2 H/I 列
7. **Step 6** — IPC分类号/法律状态批量补全，写入 Sheet2 J/K 列
8. **Step 7** — 申请主体判断，写入 Sheet2 L 列（通过 patent.fetch 下载 md 文件提取 Current Assignee，与 B 列总公司名比对，子公司填入 L 列，总公司留空）
9. **Step 8** — 靶点提取，写入 Sheet2 M 列（基于专利标题关键词匹配 + patent.fetch 全文深度提取）
10. **Step 10** — 补充列批量填写（已有专利列表补充新列，如首次公开国家/地区、同族首次公开日期等）
    - Step 10a：首次公开国家/地区（从专利号前缀提取受理局代码，映射为中文国家/地区名，写入指定列）
    - Step 10b：同族首次公开日期（利用已有申请日列做内部分组，取同族最早公开日；或调用 patent.fetch family 模块精确获取）

> ⛔ **强制门控原则（通用，适用于任意目标公司）**：
> - **Step 0 是唯一入口，每次调用必须从此开始，不可跳过。**
> - 无论目标公司是已有数据库中的23家还是全新公司，都必须先完成 Step 0。
> - Step 0 完成后，**必须以结构化表格向用户展示：公司中文名、公司英文名、子公司/申请主体完整列表（含归属状态）**。
> - **必须收到用户的明确确认**（如"确认"、"没问题"、"继续"等），才能进入 Step 1/2/3。
> - 禁止在用户未确认的情况下自动推进到专利检索。
> - 禁止跳过 Step 0 直接检索，即使目标公司已在子公司数据库中。

---

## Inputs

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `company_name` | string | ✅ | 目标公司名称，中英文均可 |
| `template_xlsx` | file | ❌ | 原模板 Excel 文件（用于继承格式/列结构）；不提供则使用内置默认模板 |
| `date_range_days` | int | ❌ | 检索近 N 天，默认 90 |
| `jurisdictions` | list | ❌ | 受理局，默认 `[CN, US, EP, WO]` |

---

## Outputs

| 产物 | 格式 | 说明 |
|------|------|------|
| `verified_company_json` | JSON | 企业信息核实结果，供下游模块复用 |
| `assignees_list` | list | 检索申请人列表（母公司 + 子公司 + 整合品牌） |
| `patent_records` | list | 专利检索结果 |
| `result_xlsx` | file | 最终 Excel 文件（含专利类型、申请日、公开日、IPC、法律状态） |

### result_xlsx Sheet 结构

**Sheet1 — 企业及子公司信息**（原始表头不可修改）

| 列 | 标题 | 内容 |
|----|------|------|
| A | 主要子公司/研发实体 | 子公司名称列表（每行一个，含状态标注） |
| B | 公司中文名 | 母公司中文名 |
| C | 公司英文名 | 母公司英文名 |

> ⚠️ 列顺序严格按模板标题反查，禁止硬编码列索引。

**Sheet2 — 专利清单**（原始表头不可修改）

| 列 | 标题 | 内容 |
|----|------|------|
| A | 专利链接 | Eureka 详情页 URL |
| B | 公司（中文） | 母公司中文名 |
| C | 公司（英文） | 母公司英文名 |
| D | 子公司/申请主体 | 专利实际申请人原始名称 |
| E | 专利号 | 公开公告号 |
| F | 专利标题 | 专利标题（原文或英文） |
| G | 专利类型 | 发明专利申请（公开）/ 发明专利（授权）/ 翻译本 / 外观设计专利 / 实用新型专利 |
| H | 申请日 | 格式 YYYY-MM-DD |
| I | 公开日 | 格式 YYYY-MM-DD |
| J | IPC分类号 | 如 A61K31/00; C07D239/24 |
| K | 法律状态 | 有效 / 审中 / 失效 |

> ⚠️ 严格按表头反查列号写入，禁止硬编码，禁止新增列，禁止新增 Sheet。
> ⚠️ G/H/I/J/K 列写入时，现有 A-F 列内容**绝对不可修改**。

---

## 已确认子公司数据库（本会话核定版 v1.0）

> 本节为本会话人工核定的子公司归属数据，Step 1 构建 assignees_list 时**以此为准**，覆盖 web.search 动态查询结果。

### 吉利德科学 / Gilead Sciences Inc.
- Kite Pharma, Inc. ✅ active（CAR-T，2017年收购）

### 默沙东 / Merck Sharp & Dohme LLC
- MSD K.K. ✅ active（日本法人）
- Merck Patent GmbH ✅ active（德国专利实体）
- Merck Sharp & Dohme B.V. ✅ active（荷兰法人）

### 葛兰素史克 / GlaxoSmithKline Biologicals SA
- GSK Intellectual Property Development Ltd. ✅ active
- ViiV Healthcare UK (No.3) Limited ✅ active（HIV合资子公司）
- GSK LLC ✅ active

### 安进 / Amgen Inc.
- Amgen Research (Munich) GmbH ✅ active
- Amgen Switzerland AG ✅ active
- Amgen Manufacturing Ltd. ✅ active
- Amgen Fremont Inc. ✅ active（原Abgenix，单抗技术）
- ChemoCentryx Inc. ✅ active（2022年收购）

### 阿斯利康 / AstraZeneca
- MedImmune LLC ✅ integrated（2007年收购，已整合）
- Alexion Pharmaceuticals, Inc. ✅ active（2021年收购，补体通路）
- AstraZeneca K.K. ✅ active（日本法人）
- TeneoTwo Inc. ✅ active（2022年收购，双抗）

### 辉瑞 / Pfizer Inc.
- Allergan, Inc. ✅ integrated（2019年收购，已整合）
- Seagen, Inc. ✅ active（2023年收购，ADC）
- Arena Pharmaceuticals Inc. ✅ integrated（2022年收购，已整合）
- Wyeth LLC ✅ integrated（2009年收购，已整合）
- Allogene Therapeutics Inc. ⚠️ partner（联合申请方，非全资子公司）

### 百时美施贵宝 / Bristol-Myers Squibb Company
- Celgene Corporation ✅ integrated（2019年收购，已整合）
- MyoKardia Inc. ✅ integrated（2020年收购，已整合）
- Juno Therapeutics Inc. ✅ integrated（2018年收购，已整合）
- Mirati Therapeutics Inc. ✅ active（2024年收购）
- Turning Point Therapeutics ✅ integrated（2022年收购，已整合）

### 诺华 / Novartis AG
- Novartis Institutes for BioMedical Research ✅ active
- Advanced Accelerator Applications (AAA) ✅ active（2018年收购）
- Morphosys AG ✅ active（2024年收购，血液肿瘤）
- Chinook Therapeutics ✅ active（2023年收购，肾病）
- Sandoz AG ⚠️ divested（2023年独立分拆上市，**不列入检索**）

### 再生元制药 / Regeneron Pharmaceuticals, Inc.
- Regeneron Ireland DAC ✅ active（爱尔兰法人）
- Sanofi ⚠️ partner（联合申请方，非子公司）

### 渤健 / Biogen Inc.
- Biogen MA Inc. ✅ active
- Biogen International GmbH ✅ active
- Biogen Idec ✅ integrated（已整合原名）

### 罗氏/基因泰克 / F. Hoffmann-La Roche AG
- Genentech, Inc. ✅ active（2009年收购）
- Roche Diagnostics GmbH ✅ active
- Chugai Pharmaceutical Co., Ltd. ✅ active（日本子公司，约60%持股）
- Roche Sequencing Solutions ✅ active
- Roche Diabetes Care GmbH ✅ active
- Foundation Medicine, Inc. ✅ active（2018年收购）

### 强生 / Johnson & Johnson（Janssen）
- Janssen Biotech, Inc. ✅ active
- Janssen Pharmaceutica NV ✅ active（比利时法人）
- Janssen Sciences Ireland UC ✅ active（爱尔兰法人）
- Cilag GmbH International ✅ active（瑞士法人）
- Janssen R&D Ireland ✅ active
- Johnson & Johnson Vision Care ✅ active（隐形眼镜/视力）
- Kenvue ⚠️ divested（2023年消费品独立分拆，**不列入检索**）

### 拜耳 / Bayer AG
- Bayer Pharma AG ✅ active（制药子公司）
- Bayer Healthcare LLC ✅ active
- Bayer Intellectual Property GmbH ✅ active
- Bayer CropScience AG ⚠️ 农业部门，可按需决定是否纳入检索

### 诺和诺德 / Novo Nordisk A/S
- Novo Nordisk Healthcare AG ✅ active
- Calibrium LLC ✅ active

### 礼来 / Eli Lilly and Company
- Lilly ICOS LLC ✅ active
- Loxo Oncology Inc. ✅ integrated（2019年收购，已整合）

### 赛诺菲 / Sanofi
- Sanofi-Aventis Deutschland GmbH ✅ active
- Translate Bio ✅ integrated（2021年收购，mRNA技术）
- Genzyme Corporation ✅ integrated（2011年收购，已整合）
- Sanofi Pasteur SA ✅ active（疫苗部门）

### 艾伯维 / AbbVie Inc.
- Allergan Pharmaceuticals International Limited ✅ active（2020年收购Allergan）
- AbbVie Deutschland GmbH & Co. KG ✅ active

### 武田制药 / Takeda Pharmaceutical Company Limited
- Takeda Vaccines Inc. ✅ active
- ARIAD Pharmaceuticals Inc. ✅ integrated（2017年收购，已整合）
- Shire plc ✅ integrated（2019年收购，已整合）
- Millennium Pharmaceuticals Inc. ✅ integrated（已整合）
- gammaDelta Therapeutics ✅ active（合作/投资，按需纳入）

### 安斯泰来制药 / Astellas Pharma Inc.
- Astellas Pharma US Inc. ✅ active
- Astellas Pharma Europe Ltd. ✅ active

### 第一三共 / Daiichi Sankyo Company, Limited
- Daiichi Sankyo Europe GmbH ✅ active
- Daiichi Sankyo Healthcare Co., Ltd. ✅ active

### 优时比 / UCB S.A.
- UCB Biopharma SRL ✅ active
- UCB Pharma SA ✅ active

### 勃林格殷格翰 / Boehringer Ingelheim International GmbH
- Boehringer Ingelheim Pharma GmbH & Co. KG ✅ active
- Boehringer Ingelheim Animal Health USA Inc. ✅ active
- Boehringer Ingelheim Vetmedica GmbH ✅ active

---

## Instructions

### Step 0 — 企业信息初始化（强制门控，不可跳过）

> ⚠️ **每次调用本 Skill，无论目标公司是否已在数据库中，都必须从 Step 0 开始。Step 0 完成并获得用户明确确认后，方可进入 Step 1/2/3。**

#### 0.1 优先使用已确认子公司数据库

**首先查阅本 SKILL 中"已确认子公司数据库"章节**：
- 若目标公司已在数据库中 → 直接加载该数据，跳过 0.2，进入 0.3 自检
- 若目标公司**不在数据库**中 → 执行 0.2 web.search 查询

#### 0.2 查询官方英文名与中文名（仅数据库未收录时执行）

使用 `web.search` 工具，查询模板：

```
"{company_name}" subsidiaries list site:wikipedia.org OR site:{company_domain}
"{company_name}" acquisitions 2021 2022 2023 2024 2025
"{company_name}" wholly owned subsidiaries annual report
```

#### 0.3 自检第1轮（归属与分类核查）

对每一条子公司条目，逐一回答：
1. 该实体的**实际控股母公司**是否确实是目标公司？
2. 该实体当前状态是否为 active？是否已分拆/独立上市？
3. 该实体是合作方还是真正的子公司？

#### 0.4 自检第2轮（完整性核查）

1. 查询近3年的**收购完成**记录，确认是否有遗漏
2. 已整合品牌是否已标注 `integrated`？
3. 公司是否有更名记录未同步？

#### 0.5 向用户展示确认表格（强制步骤，不可省略）

> 🚫 在收到用户明确确认前，**禁止执行任何专利检索操作**。

---

### Step 1 — 构建检索申请人列表

```python
assignees_list = (
    [parent_name_en]
    + [s["name"] for s in subsidiaries if s["status"] == "active"]
    + [s["name"] for s in subsidiaries if s["status"] == "integrated"]


---

### Step 9 — 专利简要分析/适应症批量填写（写入 Excel 指定列）

> 本步骤针对已有专利列表的 Excel 文件，批量调用 `patent.fetch` 获取每条专利的完整标题和摘要，在对话层逐条生成精准的中文总结，填入指定列（如 O 列），完全不依赖任何模板。

#### 9.1 整体流程

```
读取 Excel Sheet2 专利列表（专利号列）
→ 分批（每批200条）调用 patent.fetch 获取 MD 全文
→ 对话层 AI 基于 MD 标题+摘要生成精准中文1-2句总结
→ 写入 Excel 目标列（如 O 列）
→ 保存 Excel
→ 质检扫描 → 针对性修复套话/空白/语病行
```

#### 9.2 列结构说明（本次会话核定）

| 列 | 标题 | 内容 |
|----|------|------|
| A | 专利链接 | Eureka 详情页 URL |
| B | 公司（中文） | 母公司中文名 |
| C | 专利号 | 公开公告号 |
| D | 专利标题 | 专利标题（原文） |
| E | 专利类型 | 发明/授权/翻译本/外观设计/实用新型 |
| F | 专利链接（含patentId） | Eureka 详情页 URL（含patentId参数） |
| G | 公开日 | 格式 YYYY-MM-DD |
| H | 发布日期 | 格式 YYYY-MM-DD |
| I | 序号 | 序列号 |
| J | 法律状态 | 有效/审中/失效 |
| K | 申请主体（子公司） | 实际申请人 |
| L | 申请日 | 格式 YYYY-MM-DD |
| M | 靶点 | 药物靶点（如 PD-1、KRAS 等） |
| N | 适应症 | 基于靶点调用 skill 查询的适应症 |
| O | 简要分析（核心亮点） | 本步骤生成：精准中文1-2句专利核心技术描述 |

> ⚠️ **列号通过表头反查确认，禁止硬编码列索引。**

#### 9.3 O 列内容生成策略（4层递进）

```python


### Step 10a — 首次公开国家/地区（写入目标列，如 P 列）

#### 10a.1 整体流程

```
读取 Excel Sheet2 专利号列
→ 对每个专利号提取前缀（受理局代码）
→ 映射为中文国家/地区名称
→ 写入目标列（如 P 列），表头写"首次公开国家/地区"
→ 用 openpyxl 保存（严格只写目标列，其他列/格式/内容完全不动）
```

#### 10a.2 受理局代码映射（核心条目）

特殊前缀优先匹配顺序：`USD` → 美国外观设计、`HRP` → 克罗地亚、`KRDM` → 韩国外观设计、`WO+数字+S` → WIPO国际外观设计，之后按标准2字母前缀匹配。完整映射表见 `@session/skill_step10_patch.md`。

#### 10a.3 关键实现要求

- **全程使用 openpyxl**，禁止使用 pandas（pandas 读写会破坏原有格式并导致列偏移）
- 新增列通过 `ws.max_column + 1` 追加，**不硬编码列号**
- 表头反查：`header = {cell.value: cell.column for cell in ws[1] if cell.value}`
- 用 `_copy_style(src, dst)` 从左侧相邻列复制字体/填充/对齐/边框

#### 10a.4 已知陷阱

| ID | 问题 | 根因 | 规避方式 |
|----|------|------|--------|
| E50 | 输出全为"未知" | pandas读写列索引偏移 | 全程用openpyxl，表头反查列号 |
| E51 | P列数据丢失 | pandas重建workbook覆盖未写入列 | 只用openpyxl追加写入，不重建workbook |
| E52 | 新列字体与其他列不一致 | 新增列未复制相邻列格式 | 用_copy_style从左侧相邻列复制格式 |
| E53 | HRP被识别为HR | 2字母匹配优先于3字母 | 特殊前缀列表放在2字母匹配之前 |
| E54 | WO外观设计被识别为普通WO | 未区分外观设计后缀S | 用正则`^WO\d+S$`单独识别 |


### Step 10b — 同族首次公开日期（写入目标列，如 Q 列）

#### 10b.1 整体流程

```
读取 Excel Sheet2（含专利号列、申请日列、公开日列）
→ 以申请日为 key 对所有专利分组（同族）
→ 每组取所有成员公开日的最小値
→ 写入目标列（如 Q 列），表头写"同族首次公开日期"
→ 用 openpyxl 保存（严格只写目标列）
```

#### 10b.2 核心分组策略（内部分组法，无需额外 API 调用）

```python
from collections import defaultdict
from datetime import datetime

def parse_date(s):
    for fmt in ["%Y-%m-%d", "%Y%m%d"]:
        try:
            return datetime.strptime(str(s).strip(), fmt)
        except:
            pass
    return None

# 表头反查列号
header = {cell.value: cell.column for cell in ws[1] if cell.value}
col_pn  = header["\u4e13\u5229\u53f7"]
col_apd = header.get("\u7533\u8bf7\u65e5") or header.get("\u53d1\u5e03\u65e5\u671f")
col_pbd = header.get("\u516c\u5f00\u65e5") or header.get("\u516c\u5f00\u65e5\u671f")

rows_data = []
for r in range(2, ws.max_row + 1):
    pn  = str(ws.cell(r, col_pn).value  or "").strip()
    apd = str(ws.cell(r, col_apd).value or "").strip() if col_apd else ""
    pbd = str(ws.cell(r, col_pbd).value or "").strip() if col_pbd else ""
    rows_data.append({"row": r, "pn": pn, "apd": apd, "pbd": pbd})

# 按申请日分组
family_groups = defaultdict(list)
for d in rows_data:
    if d["pn"] and d["apd"]:
        family_groups[d["apd"]].append((d["row"], d["pbd"]))

# 每族取最早公开日
row_to_family_date = {}
for apd, members in family_groups.items():
    dates = [parse_date(pbd) for _, pbd in members]
    dates = [d for d in dates if d]
    if not dates:
        continue
    earliest = min(dates).strftime("%Y-%m-%d")
    for row, _ in members:
        row_to_family_date[row] = earliest

# 写入目标列（复制相邻列格式）
col_q = ws.max_column + 1
ws.cell(row=1, column=col_q, value="\u540c\u65cf\u9996\u6b21\u516c\u5f00\u65e5\u671f")
_copy_style(ws.cell(1, col_q - 1), ws.cell(1, col_q))
for row_idx in range(2, ws.max_row + 1):
    val = row_to_family_date.get(row_idx, "")
    cell = ws.cell(row=row_idx, column=col_q, value=val)
    _copy_style(ws.cell(row_idx, col_q - 1), cell)
wb.save(output_path)
```

#### 10b.3 分组策略对比

| 方法 | 适用场景 | 精确度 | 额外API调用 |
|------|---------|--------|------------|
| **申请日内部分组**（推荐） | 已有申请日列 | ⭐⭐⭐ | 无需 |
| patent.search family | 无申请日/需精确同族 | ⭐⭐⭐⭐ | 需要 |
| patent.fetch family模块 | 最权威同族数据 | ⭐⭐⭐⭐⭐ | 需要（慢，每拡20条）|

#### 10b.4 已知陷阱

| ID | 问题 | 根因 | 规避方式 |
|----|------|------|--------|
| E55 | patent.fetch每拡只能20条 | API限制 | 优先用内部申请日分组法 |
| E56 | Python审批超时阻塞流程 | Eureka审批机制 | 内部分组法无需审批；审批弹窗需5秒内点击 |
| E57 | 同族分组过粗 | 仅用申请日分组 | 改用（申请日+申请主体）复合key |
| E58 | Q列日期格式不一致 | 写入datetime对象 | 统一输出字符串`YYYY-MM-DD` |
| E59 | P列写Q列时丢失 | 重建workbook覆盖P列 | 全程openpyxl追加写入 |

#### 10b.5 覆盖率预期（2035条验证）

| 方法 | 覆盖率 |
|------|-------|
| 申请日内部分组 | ~99%（2034/2035行填入） |
| 共识别同族分组数 | 1513个同族组 |

# 优先级从高到低：
# 第1层：patent.fetch 获取 MD 全文 → 标题+摘要语义提炼
# 第2层：F列 patentId URL → 实时 fetch 全文
# 第3层：M列靶点 + N列适应症 + B列公司名 三要素组合
# 第4层：专利号国家前缀 + 公司名精准兜底

def generate_summary(md_content, target, indication, company, pn):
    """
    基于 MD 全文生成精准中文1-2句总结。
    要求：
    - 全部中文，保留 TIGIT/KRAS/PD-1/GLP-1R 等专业英文缩写
    - 1-2句话，包含：核心技术手段 + 适应症/应用场景
    - 禁止：套话、空白、纯英文截断、URL残留、公司名前缀
    - 禁止出现："创新药物专利"、"涵盖创新技术"、"经XXX审查授权" 等模板词
    """
    pass
```

#### 9.4 批处理策略

| 参数 | 建议值 | 说明 |
|------|--------|------|
| 每批条数 | 200 | 每批200条，约11批完成2034条 |
| 并发下载 | 4批×10条 | 每轮40条MD并发下载 |
| 保存时机 | 每批写入后立即保存 | 防止文件占用/崩溃丢失 |
| 文件状态 | 执行前必须关闭Excel | PermissionError 根因 |

#### 9.5 N 列适应症生成策略

适应症不能直接从靶点映射，需通过以下步骤调用 skill 查询：

```
1. 读取 M 列靶点值（173个唯一靶点）
2. 调用 MCP skill（novelty_summary / ls_drug_search）按靶点查询代表性药物
3. 从药物详情中提取 research_disease_view 字段（适应症列表）
4. 精简为中文适应症描述，写入 N 列
5. 覆盖范围：只对有靶点的行（约620行）填写
```

#### 9.6 质检与修复流程

每轮全量写入后，执行质检扫描，识别以下问题类型：

| 问题类型 | 识别模式 | 修复策略 |
|---------|---------|--------|
| **套话行** | "创新药物专利"、"涵盖创新技术"、"经XXX审查授权"、"[国家]专利申请，涵盖..." | 重新 fetch MD → AI 重新生成 |
| **空白行** | O列为空或None | 强制调用 fetch → 生成兜底描述 |
| **URL残留** | O列含 `https://eureka.zhihuiya.com` | 从F列提取patentId → fetch → 重新生成 |
| **语病行** | "靶向-数字"、"靶向的治"、"双特异性抗 "（被删英文字母） | fetch MD → 恢复完整术语 |
| **公司名前缀** | "默沙东XXX专利"、"吉利德科学XX专利" | 正则删除前缀，保留后续内容 |
| **重复描述** | 同族专利同一句话重复 | 在描述中加入国家/剂型/适应症差异化信息 |

#### 9.7 已知陷阱与规避方式

| ID | 问题描述 | 根因 | 规避方式 |
|----|----------|------|--------|
| E40 | PermissionError 无法保存Excel | WPS/Excel占用文件 | 执行前强制关闭Excel，操作前检查文件句柄 |
| E41 | 英文字母被误删导致语病 | `re.sub(r'[a-zA-Z]+', '', text)` 删除了IL-2/KRAS等专业术语 | **禁止对最终输出执行全量英文删除**；仅对非专业词汇做处理 |
| E42 | O列写入URL而非文字 | F列超链接被误读为O列内容 | 用 pandas 读取（忽略超链接）+ openpyxl 写回（清除hyperlink） |
| E43 | 同族专利描述完全重复 | 同一靶点词典映射生成相同内容 | 加入国家/药物名/剂型差异化信息区分同族专利 |
| E44 | 套话反复出现 | 词典兜底层生成模板化描述 | 优先使用 MD 全文；词典仅作辅助；禁止纯模板输出 |
| E45 | 列映射错误（B列=公司名被误当专利号） | 部分行B列存公司名，C列才是专利号 | 始终通过表头反查列号，不硬编码 |
| E46 | patentId 提取失败 | F列URL格式为 `fullText'figures/?patentId=xxx` | 正则提取时兼容单引号格式：`re.search(r'patentId=([a-f0-9-]+)', url)` |

#### 9.8 覆盖率预期

| 质量等级 | 来源 | 预期覆盖率 |
|---------|------|----------|
| ⭐⭐⭐ MD全文提炼 | patent.fetch 返回完整摘要 | ~60%（主要局US/EP/WO/CN/AU等） |
| ⭐⭐ 靶点/适应症三要素 | M列+N列+B列 | ~20%（有靶点信息的行） |
| ⭐ 精准兜底 | 专利号前缀+公司名 | ~15%（小国别/翻译件/外观设计） |
| ⬜ 无法生成 | 纯外观设计无文字 | ~5%（USD/JP外观等） |

> 📌 **经验说明**：外观设计专利（USD/JP/CN3开头）、欧洲成员国翻译件（DE602/ES/FI/PL/SI/HR等）、小国别专利（VN/UA/ZA/AL等）的MD内容极少，是套话的主要来源，需要特别处理。


    # divested 和 partner 不列入
)
```

---

### Step 2 — 专利检索

#### 2.1 检索参数

```
assignees: assignees_list
date_from: today - date_range_days（默认 today - 90）
date_to: today
date_type: publication
```

#### 2.2 检索策略

- 使用 `patent.search` 工具，`search_strategy: ["filter"]`
- `filters.assignees` 每次查询建议 3-5 个实体
- 若某公司子公司较多（>5个），分批查询后合并去重

#### 2.3 数量核查与分页补全（关键步骤）

```python
LIMIT = 100
all_results = []
offset = 0

resp = patent_search(assignees=batch, date_from=date_from, date_to=date_to, limit=LIMIT, offset=0)
matched_total = resp["matched_total"]
all_results.extend(resp["results"])
offset += len(resp["results"])

while offset < matched_total:
    resp = patent_search(assignees=batch, date_from=date_from, date_to=date_to, limit=LIMIT, offset=offset)
    all_results.extend(resp["results"])
    offset += len(resp["results"])
    if not resp["results"]:
        break
```

#### 2.3.1 vespa 错误处理与重试

```
重试策略：
1. 等待约 5 秒后重试同一批次（最多3次）
2. 若3次均失败，缩小批次（每次只查1个申请人）逐一重试
3. 若仍失败，记录到 failed_companies 列表，继续下一家公司
```

**已知易触发 vespa 错误的公司（需优先单独查询）：**
- 渤健（Biogen Inc.）
- 艾伯维（AbbVie Inc.）
- 第一三共（Daiichi Sankyo Company, Limited）
- 优时比（UCB S.A.）

#### 2.4 去重规则

- 以 `patent_id` 为唯一键去重

---

### Step 3 — Excel 基础输出

#### 列映射规则（强制）

```python
header_row = ws[1]
col_map = {cell.value: cell.column for cell in header_row if cell.value}
```

#### 格式继承规则

1. 读取原文件，**保留原始 Sheet1 全部内容不动**，仅向 Sheet2 写入数据
2. 数据行从 Sheet2 第2行开始写入（第1行为原始表头，不覆盖）
3. **非目标列一律不修改**，禁止新增列，禁止新增 Sheet

#### 专利链接格式

```
https://eureka.zhihuiya.com/view/#/fullText?patentId={patent_id}
```

---

### Step 4 — 专利类型判断（写入 Sheet2 G 列）

> 本步骤通过专利号末尾的 kind code 判断专利类型，**不调用任何在线接口**，纯本地逻辑，速度极快。

#### 4.1 判断逻辑（Python 实现）

```python
import re

def classify_patent_type(pn: str) -> str:
    pn = pn.strip()
    if pn.startswith("USD"):
        return "外观设计专利"
    if pn.startswith("KRDM"):
        return "外观设计专利"
    if re.match(r'^BR32', pn):
        return "外观设计专利"
    if re.match(r'^IN\d+S$', pn):
        return "外观设计专利"
    m = re.search(r'([A-Z]\d*)$', pn)
    if not m:
        return "其他"
    kind = m.group(1)
    letter = kind[0]
    if letter == 'T':
        return "翻译本"
    if letter == 'S':
        return "外观设计专利"
    if letter == 'U':
        return "实用新型专利"
    if letter in ('B', 'C'):
        return "发明专利（授权）"
    if letter == 'A':
        return "发明专利申请（公开）"
    return "其他"
```

#### 4.2 已知特殊 kind code 说明

| Kind Code | 国家/地区 | 含义 | 归类 |
|---|---|---|---|
| T/T1/T2/T3/T6 | 欧洲各成员国（ES/DE/FI/HR/PL/SI等） | EP专利本地语言翻译备案 | 翻译本 |
| C/C2 | 乌克兰（UA） | 发明专利授权（UA用C代替B） | 发明专利（授权） |
| A0 | 以色列（IL）、巴基斯坦（PK） | 发明专利申请公开 | 发明专利申请（公开） |
| RA/TA/YA/XA/QA等 | 新加坡（SG） | 发明专利申请公开（双字母后缀） | 发明专利申请（公开） |
| S1（KRDM前缀） | 韩国 | 外观设计 | 外观设计专利 |
| S1（BR32前缀） | 巴西 | 外观设计 | 外观设计专利 |
| U（纯字母无数字） | 中国（CN） | 实用新型 | 实用新型专利 |

#### 4.3 验证（本会话2034条全量结果）

| 专利类型 | 数量 |
|---|---|
| 发明专利申请（公开） | 1132 |
| 发明专利（授权） | 647 |
| 翻译本 | 208 |
| 外观设计专利 | 44 |
| 实用新型专利 | 3 |
| 其他 | 0 |
| **合计** | **2034** |

---

### Step 5 — 申请日/公开日批量获取（写入 Sheet2 H/I 列）

> 本步骤通过 `patent.fetch` 批量下载专利 md 文件，从中提取申请日和公开日。建议每批200条，支持断点续查。

#### 5.1 整体流程

```
读取 Sheet2 专利号列表
→ 检查本地 md 缓存（session/downloads/document-fetch/）
→ 对未缓存条目调用 patent.fetch 在线下载
→ 解析 md 文件提取申请日/公开日（8位纯数字格式）
→ 写入 Sheet2 H/I 列
→ 保存 Excel
→ 更新 pending_pns.json
```

#### 5.2 md 文件日期提取（关键：PatSnap md 中日期为8位纯数字）

```python
import re

def extract_dates_from_md(content: str) -> dict:
    def parse_date(s):
        if s and len(s) == 8 and s.isdigit():
            return f"{s[:4]}-{s[4:6]}-{s[6:]}"
        return None

    apd = None
    m = re.search(r'###\s*Application\s*Date\s*\n(\d{8})', content)
    if m:
        apd = parse_date(m.group(1))
    if not apd:
        m = re.search(r'\*\*\s*Application\s*Date\s*\*\*[:\s]+(\d{8}|\d{4}-\d{2}-\d{2})', content)
        if m:
            apd = parse_date(m.group(1).replace('-', ''))

    pbd = None
    m = re.search(r'###\s*Publication\s*Date\s*\n(\d{8})', content)
    if m:
        pbd = parse_date(m.group(1))
    if not pbd:
        m = re.search(r'\*\*\s*Publication\s*Date\s*\*\*[:\s]+(\d{8}|\d{4}-\d{2}-\d{2})', content)
        if m:
            pbd = parse_date(m.group(1).replace('-', ''))

    return {"apd": apd, "pbd": pbd}
```

> ⚠️ **历史错误 E20**：最初使用 `YYYY-MM-DD` 正则，导致大量 md 文件无法提取日期。修复后提取率从 ~30% 提升至 100%。

#### 5.3 服务端500处理策略

- 分组降级：触发500后拆分为每组10条
- 改用 patent.search 接口绕过（适用于UA/AR/ZA/HK等不稳定专利）
- pending_pns.json 断点续查机制

#### 5.4 特殊专利处理

| 专利类型 | 问题 | 解决方案 |
|---|---|---|
| UA C2 系列 | fetch 持续500 | 改用 search 接口 |
| AR A1 系列 | md 中日期字段为空 | 改用 search 接口 |
| ZA/HK 系列 | fetch 偶发500 | 先 fetch，失败后 search 兜底 |

> ⚠️ **历史错误 E23**：`~$` 开头的临时文件被误判为已缓存 md。修复：判断前过滤 `~$` 前缀。

---

### Step 6 — IPC分类号/法律状态批量补全（写入 Sheet2 J/K 列）

> 本步骤通过 `patent.search` 的 `filters.pn` 精确过滤批量获取 IPC 分类号和法律状态，写入 Sheet2 J/K 列。**无需执行 Python 脚本审批，全程使用纯搜索 API。**

#### 6.1 整体流程

```
读取 Sheet2 C列专利号（约2035条）
→ 分批（每批50条）用 filters.pn 精确搜索
→ 从结果中提取 ipc / legal_status 字段
→ 与专利号对照后写入 J/K 列（先补写J1/K1表头）
→ 同族反查：对EP翻译文件提取基础EP号再搜索
→ 对WO2025/2026新申请单独发起pn过滤补全legal_status
→ 最终输出 final_vN.xlsx
```

#### 6.2 核心搜索方法

```python



---

### Step 8 — 靶点提取（写入 Sheet2 M 列）

> 本步骤针对专利列表中每条记录，识别其对应的药物靶点（如 PD-1/PD-L1、EGFR、GLP-1R 等），分两阶段执行：
> - **阶段一**：基于专利标题关键词匹配（快速，覆盖率约 18%）
> - **阶段二**：针对未匹配行，通过 patent.fetch 拉取全文 md，从摘要/权利要求中深度提取（每批200个，覆盖率可提升至 ~30%）

#### 7.1 整体流程

```
读取 Sheet2 专利标题列（col F = '专利标题'）和专利号列（col E = '专利号'）
→ 阶段一：关键词匹配，写入 M 列
→ 阶段二：对 M 列仍为空且有专利号的行，分批 patent.fetch 全文
→ 从 md 文件标题/摘要/权利要求提取靶点
→ 全量扫描更新 M 列
→ 保存输出文件
```

#### 7.2 阶段一：标题关键词匹配

```python
# 靶点关键词词典（核心条目，可持续扩展）
TARGET_KEYWORDS = {
    # 免疫检查点
    "PD-1": ["pd-1", "pd1", "programmed death"],
    "PD-L1": ["pd-l1", "pdl1", "cd274"],
    "CTLA-4": ["ctla-4", "ctla4"],
    "LAG-3": ["lag-3", "lag3"],
    "TIM-3": ["tim-3", "tim3"],
    "TIGIT": ["tigit"],
    # 肿瘤靶点
    "HER2": ["her2", "erbb2"],
    "EGFR": ["egfr", "erbb1"],
    "VEGF/VEGFR": ["vegf", "vegfr"],
    "KRAS": ["kras", "k-ras"],
    "BRAF": ["braf"],
    "CDK4/6": ["cdk4", "cdk6"],
    "PARP": ["parp"],
    "BCL-2": ["bcl-2", "bcl2"],
    "BTK": ["btk", "bruton"],
    "JAK": ["jak1", "jak2", "jak3", "janus kinase"],
    "FGFR": ["fgfr"],
    "RET": [" ret ", "ret kinase"],
    "NTRK": ["ntrk", "tropomyosin"],
    "FLT3": ["flt3"],
    "TROP-2": ["trop-2", "trop2"],
    # 代谢/内分泌
    "GLP-1R": ["glp-1", "glp1", "glucagon-like peptide"],
    "PCSK9": ["pcsk9"],
    "TTR": ["ttr", "transthyretin"],
    # 炎症/免疫
    "TNF-α": ["tnf-", "tumor necrosis factor"],
    "IL-6": ["il-6", "interleukin-6"],
    "IL-17": ["il-17", "interleukin-17"],
    "IL-23": ["il-23", "interleukin-23"],
    "IL-4/13": ["il-4", "il-13"],
    "STING": ["sting", "stimulator of interferon"],
    "TLR": ["toll-like receptor"],
    # 神经系统
    "β-amyloid": ["amyloid", "alzheimer"],
    "tau": [" tau ", "tau protein"],
    # 感染/病毒
    "SARS-CoV-2": ["sars-cov", "covid"],
    "HIV": [" hiv "],
    "HSV": [" hsv ", "herpes simplex"],
    "HBV": [" hbv ", "hepatitis b"],
    # 细胞疗法
    "CAR-T": ["car-t", "chimeric antigen receptor"],
    "CD19": ["cd19"],
    "CD20": ["cd20"],
    "CD38": ["cd38"],
    "BCMA": ["bcma"],
    "PSMA": ["psma"],
    # 补体/FcRn
    "C5": [" c5 ", "complement c5"],
    "FcRn": ["fcrn", "neonatal fc receptor"],
}

def extract_target_from_title(title: str) -> str:
    if not title:
        return ""
    title_lower = title.lower()
    matched = []
    seen = set()
    for target, keywords in TARGET_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in title_lower:
                if target not in seen:
                    matched.append(target)
                    seen.add(target)
                break
    return "; ".join(matched)
```

#### 7.3 阶段二：patent.fetch 全文深度提取

```python
def extract_target_from_md(md_path: str) -> str:
    """
    从 patent.fetch 返回的 md 文件中提取靶点。
    优先读取标题行（# 开头）、摘要段（Abstract）、权利要求段（Claims）。
    取前3000字符进行关键词匹配，避免 token 超长。
    """
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return ""

    # 取标题行 + 前3000字符
    title_line = next((l for l in content.split("\n")[:5] if l.startswith("#")), "")
    search_text = (title_line + "\n" + content[:3000]).lower()

    matched = []
    seen = set()
    for target, keywords in TARGET_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in search_text:
                if target not in seen:
                    matched.append(target)
                    seen.add(target)
                break
    return "; ".join(matched)
```

#### 7.4 M 列写入规则

```python
# 通过表头反查 M 列位置（不硬编码）
col_target = col_map.get("靶点")
if col_target is None:
    ws.cell(row=1, column=13, value="靶点")
    col_target = 13

# 仅对空白行写入（不覆盖已有值）
for row_idx, row in enumerate(ws.iter_rows(min_row=2), start=2):
    if row[col_target - 1].value:  # 已有靶点，跳过
        continue
    pn = str(row[col_pn - 1].value or "").strip()
    title = str(row[col_title - 1].value or "").strip()
    target = extract_target_from_title(title)
    if not target and pn:
        md_path = os.path.join(CACHE_DIR, f"{pn}.md")
        if os.path.exists(md_path):
            target = extract_target_from_md(md_path)
    if target:
        row[col_target - 1].value = target
```

#### 7.5 覆盖率预期与说明

| 阶段 | 方法 | 预期覆盖率 |
|---|---|---|
| 阶段一（标题匹配） | 关键词词典 | ~18% |
| 阶段二（全文 fetch） | md 文件深度提取 | +10-15%（累计 ~30%） |
| 无靶点专利 | 剂型/工艺/仪器/外观设计 | 正常空白，无需处理 |

> 📌 **经验说明**：23家大型药企数据集包含大量辅料制剂、诊断仪器、外观设计、工艺流程类专利（约占60-70%），这些本身没有明确药物靶点，最终覆盖率 ~30% 属正常水平，不代表提取有遗漏。

#### 8.6 Quality Gates（Step 8 专项）

| Gate | 检查项 | 失败处理 |
|---|---|---|
| QG-14 | M 列表头写入"靶点"，不硬编码列索引 | 重新执行表头反查 |
| QG-15 | 原有 A-L 列内容完全不修改 | 重新读取原文件后写入 |
| QG-16 | 已有靶点值不被覆盖（增量写入） | 写入前检查 `if not cell.value` |
| QG-17 | 关键词匹配大小写不敏感 | 统一 `.lower()` 后比较 |
| QG-18 | md 缓存目录过滤 `~$` 临时文件 | 同 Step 5 E23 规避方式 |

#### 7.7 Known Issues（本次会话）

| ID | 错误描述 | 根因 | 规避方式 |
|----|----------|------|--------|
| E26 | 靶点列写入位置错误（硬编码第12列） | 未通过表头反查 | 强制 `col_map.get("靶点")`，不存在时写 column=13 |
| E27 | 阶段二全量扫描未累积历史批次结果 | 每批次重新初始化 targets_dict | 改为追加模式：`targets_dict.update(new_batch)` |
| E28 | 服务端500导致部分专利 md 未下载 | fetch 接口偶发不稳定 | 记录 remaining_pns，下批次优先重试 |
| E29 | md 文件路径大小写不匹配（Windows） | Windows 文件系统大小写不敏感但路径需精确 | 用 `os.path.exists()` 判断，避免手动拼路径 |



# 每批50条专利号，用 filters.pn 精确过滤
result = patent_search(
    search_strategy=["filter"],
    filters={"pn": batch_of_50_pns},
    limit=50
)

# 提取字段
for r in result["results"]:
    pn = r.get("publication_number") or r.get("PN_STR")
    ipc = r.get("ipc")            # 如 "A61K31/00; C07D239/24"
    legal = r.get("legal_status")  # 如 "active"/"pending"/"inactive"

# 法律状态中文转换
LEGAL_MAP = {"active": "有效", "pending": "审中", "inactive": "失效",
             "1": "有效", "2": "审中", "0": "失效"}
```

#### 6.3 批次策略（经验值）

| 批次大小 | 建议 | 说明 |
|---|---|---|
| 每批50条 | ✅ 推荐 | 稳定，命中率高 |
| 每批100条 | ✅ 可用 | 偶发超时 |
| 每批200条 | ⚠️ 谨慎 | 需4组×50条并行 |
| 每批>200条 | ❌ 不推荐 | API不稳定 |

> 每轮对话处理200条（4组×50条并行搜索），约需 **11次** "继续" 完成2035条。

#### 6.4 同族反查策略（关键补全步骤）

大量空白行实际上是EP同族翻译文件，可通过提取基础EP号反查：

```python
import re

def extract_base_ep_number(pn: str):
    """从翻译文件中提取基础EP数字，用于同族反查。
    FI4271674T6 → EP4271674
    ES3060504T3 → EP3060504
    DK/PL/HU/SI/HR/PT/LT/LV/RO/SK/CZ/BG/EE 系列同理
    DE602...格式跳过（德国特殊翻译文件）
    """
    m = re.match(r'^(FI|ES|DK|PL|HU|SI|HR|PT|LT|LV|RO|SK|CZ|BG|EE)(\d{6,8})[A-Z]', pn)
    if m:
        num = m.group(2)
        if not num.startswith('602'):
            return f"EP{num}"
    return None
```

**同族反查效果（本次会话2035条验证）：**
- 初始搜索后：J列 584行，K列 607行
- 同族反查后：J列 **1,686行**（+1,102行），K列 **1,627行**（+1,020行）
- **覆盖率从 28.7% 提升至 82.9%**

#### 6.5 表头处理（必须写入，否则J1/K1为空）

```python
# 写入数据前先检查并补写 J1/K1 列标题
ws.cell(row=1, column=col_j, value="IPC分类号")
ws.cell(row=1, column=col_k, value="法律状态")
```

#### 6.6 空白原因分类（本次会话2035条验证）

| 类型 | 数量 | 可补性 | 说明 |
|---|---|---|---|
| EP同族翻译文件（FI/ES/DK/PL/HU等T系列） | ~600条 | ✅ 可补（同族反查） | 提取基础EP号搜索 |
| HK/SG/AU/CA等地区登记号 | ~200条 | ⚠️ 部分可补 | 收录有限 |
| 极新申请（2025-2026，WO/EP新申请） | ~150条 | ✅ 可补（pn精确搜索） | 用pn过滤可获取 |
| ZA/AL/HRP/VN/UA/EA小国别 | ~200条 | ❌ 不可补 | PatSnap未收录 |
| 外观设计专利（USD/JP/CN外观） | ~44条 | ❌ 正常空白 | 外观设计天然无IPC |

**最终覆盖率：J列 1,687/2035 = 82.9%，K列 1,723/2035 = 84.7%**

#### 6.7 Quality Gates（Step 6专项）

| Gate | 检查项 | 失败处理 |
|---|---|---|
| QG-14 | J1/K1 表头已写入 | 补写"IPC分类号"/"法律状态" |
| QG-15 | 已执行同族反查（EP翻译文件） | 执行6.4节同族反查流程 |
| QG-16 | 极新WO/EP申请已用pn精确搜索补全 | 对WO2025/WO2026系列单独发起pn过滤搜索 |
| QG-17 | 外观设计J列空白已标注为正常 | 无需补全，属正常情况 |
| QG-18 | 原有A-I列内容完整保留 | 重新读取原文件后写入 |

---

## Quality Gates

| Gate | 检查项 | 失败处理 |
|------|--------|--------|
| QG-0 | Step 0 已完成且已获用户明确确认 | 回退至 Step 0.5 |
| QG-1 | 子公司归属优先使用已确认数据库 | 比对数据库，修正错误归属 |
| QG-2 | 无合作方被误列为子公司 | 修正 status → partner |
| QG-3 | 无已分拆实体仍列为 active | 修正 status → divested |
| QG-4 | 近3年收购已全部核查 | 补充遗漏条目 |
| QG-5 | Excel 列写入位置通过标题反查确认 | 重新执行列映射 |
| QG-6 | 非目标 Sheet / 非目标列内容完整保留 | 重新读取原文件后写入 |
| QG-7 | 每组查询 returned_count = matched_total（分页至全量） | 分页补全后重新汇总 |
| QG-8 | Sheet2 列数与模板一致，不新增列 | 删除多余列后重新写入 |
| QG-9 | vespa错误公司已记录到 failed_companies | 补充列表，提示用户重试 |
| QG-10 | 每家公司检索完成后立即保存 Excel | 重新追加写入已完成公司数据 |
| QG-11 | Step 4 专利类型覆盖率100%，"其他"=0 | 排查未覆盖 kind code，补充规则 |
| QG-12 | Step 5 申请日/公开日空白率 ≤ 1% | 对空白条目执行 search 接口兜底补查 |
| QG-13 | ~$ 临时文件已过滤，不被误判为 md 缓存 | 检查缓存扫描逻辑，添加过滤条件 |
| QG-14 | J1/K1 表头已写入 | 补写"IPC分类号"/"法律状态" |
| QG-15 | 已执行同族反查（EP翻译文件） | 执行6.4节同族反查流程 |
| QG-16 | 极新WO/EP申请已用pn精确搜索补全 | 对WO2025/WO2026系列单独发起pn过滤搜索 |
| QG-17 | 外观设计J列空白已标注为正常 | 无需补全，属正常情况 |
| QG-18 | 原有A-I列内容完整保留 | 重新读取原文件后写入 |

---

## Known Issues & Lessons Learned

| ID | 错误描述 | 根因 | 规避方式 |
|----|----------|------|--------|
| E01 | Kite Pharma 被误归入 Amgen | 未验证实际归属 | 优先查阅已确认子公司数据库 |
| E02 | Sandoz AG 仍列为 Novartis 子公司 | 未检查分拆记录 | 数据库中已标注 divested |
| E03 | 合作方被误列为子公司 | 合作方与子公司混淆 | 严格区分 status |
| E04 | Excel 列写入位置错误 | 硬编码列索引 | 强制标题反查 |
| E05 | Sheet2 原有内容被覆盖 | 重建 workbook | 基于原文件修改 |
| E06 | 近年收购子公司遗漏 | 未检索近年收购记录 | Step 0.4 专项核查 |
| E07 | Kenvue 被误列为强生子公司 | 未检查分拆记录 | 数据库中已标注 divested |
| E08 | Sheet2 新增多余列 | 未严格按表头反查 | QG-8 强制检查 |
| E09 | returned_count 误作为 matched_total | 未分页补全 | Step 2.3 强制分页 |
| E10 | Allogene 被误列为辉瑞全资子公司 | 归属混淆 | 数据库中已标注 partner |
| E11 | Chugai Pharmaceutical 漏查 | 日文法人名未纳入检索 | 数据库中已列入罗氏子公司 |
| E12 | 跳过 Step 0 确认直接开始专利检索 | 未遵守强制门控原则 | QG-0 强制拦截 |
| E13 | Sheet2 写入了6列而非固定列数 | 自行添加额外列 | 写入前验证列数 |
| E14 | 渤健等因 vespa 错误被静默跳过 | 错误处理不完善 | failed_companies 列表 |
| E15 | 分页时 offset 计算错误 | offset 未正确累加 | `offset += len(resp["results"])` |
| E16 | 多公司批量检索时中途 token 超时 | 未做增量写入 | 每家公司完成后立即 save_xlsx |
| E17 | 专利类型"其他"未归零（第一版） | 未覆盖 UA C2、IL A0、KRDM S1 等特殊 kind code | Step 4 多轮迭代修复，见4.2节 |
| E18 | 翻译本被误判为"其他" | T 系列正则未匹配 T 开头 | 补充 `letter == 'T'` 规则 |
| E19 | 纯 U（无数字）实用新型被归为"其他" | 正则只匹配 U+数字 | 修改为 `letter == 'U'` 即可 |
| E20 | 日期提取率低（~30%） | 正则用 YYYY-MM-DD 格式，实际是8位纯数字 | 修改正则匹配 `\d{8}`，再转换格式 |
| E21 | 服务端500持续失败导致大量空白 | 部分专利 fetch 接口不稳定 | 改用 search 接口兜底，建立 pending 机制 |
| E22 | 每批仅写入新增条目，历史批次未累积 | parse 脚本每次重建而非追加 | 改为全量扫描 dates_cache 写入 |
| E23 | ~$ 临时文件被误判为已缓存 md | 未过滤 Windows 临时文件 | 判断前过滤 `~$` 前缀文件 |
| E24 | AR 阿根廷专利 md 中日期字段为空 | PatSnap 对 AR 专利数据覆盖不完整 | 改用 search 接口，search 结果有日期字段 |
| E25 | UA130591C2 fetch 持续500 | 乌克兰专利服务端不稳定 | 用 search 接口按专利号查询，成功获取 |
| E26 | J/K列表头为空 | 写入逻辑未处理第1行表头 | 写入前先检查并补写 J1/K1 |
| E27 | 大量空白误判为数据库故障 | 未区分"未收录"与"翻译文件" | 先做同族反查，再做覆盖率分析 |
| E28 | 翻译文件直接搜索返回0条 | FI/ES/DK等翻译文件号PatSnap不收录 | 提取基础EP号后搜索 |
| E29 | Python脚本需审批导致流程阻塞 | Eureka Python审批机制 | 改用纯搜索API方案（无需审批）直接处理 |
| E30 | WO2026极新申请legal_status为空 | 数据库延迟填充 | 用 filters.pn 精确过滤（非关键词搜索）可获取 |
| E31 | 补全时用关键词泛搜而非pn精确过滤 | 误用keyword策略 | 始终用 filters.pn 精确过滤专利号，不用关键词搜索 |
| E32 | 同族反查后仍遗漏DE602系列 | DE602格式特殊，数字前缀"602"不是EP号 | 跳过DE602前缀，避免误提取 |
| E33 | 多轮操作后Excel版本混乱 | session中存在多个xlsx文件 | 始终以final_vN.xlsx为最新版本，按版本号递增命名 |

---

## 本次会话补充经验（2026-06-29 更新）

### 新会话发现：Step 6 补全流程完整记录

本次会话对2035条专利执行了完整的IPC/法律状态补全，积累了以下关键经验：

#### 补全流程四阶段

1. **第一阶段：直接pn搜索**（命中率约20-30%）
   - 每批50条，4组并行 = 200条/轮
   - 约11轮完成2035条
   - 主流局（WO/EP/US/AU等）命中率高，小国别命中率低

2. **第二阶段：同族反查**（新增补全+1,102行，覆盖率从28.7%→82.9%）
   - 识别FI/ES/DK/PL/HU/SI/HR/PT/LT/LV/RO等EP翻译文件
   - 提取基础EP数字号，构造EP前缀搜索
   - 效果最显著的单步骤，强烈建议在第一阶段后立即执行

3. **第三阶段：WO2025/2026新申请补全**（+约142行）
   - WO2026系列用pn精确过滤可获取legal_status
   - 关键：用filters.pn而非关键词搜索
   - 新申请均为"审中"状态

4. **第四阶段：K列单独补全**（+70行）
   - 对J列有值但K列为空的行单独发起搜索
   - 部分专利IPC有值但legal_status字段延迟填充

#### 最终覆盖率（2035条验证）

| 列 | 已填行数 | 覆盖率 |
|---|---|---|
| J列（IPC分类号） | 1,687 | 82.9% |
| K列（法律状态） | 1,723 | 84.7% |

#### 不可补全类型（已确认）

| 类型 | 代表专利号 | 原因 |
|---|---|---|
| ZA/AL/HRP/VN/UA/EA | ZA202300536B, AL13448B | PatSnap未收录 |
| 外观设计专利 | USD1118367S, KRDM系列 | 天然无IPC |
| DE602系列 | DE602016095006T2 | 德国特殊翻译文件格式 |

---

## Module Interface

```yaml
module_id: biopharma-patent-landscape
version: 0.6.0
status: complete  # Step 0/1/2/3/4/5/6 均已完整

tools_used:
  - web.search        # Step 0.2：企业信息查询
  - patent.search     # Step 2：专利检索；Step 5：日期兜底查询；Step 6：IPC/法律状态
  - patent.fetch      # Step 5：批量下载专利 md 文件
  - python.run        # Step 3/4/5/7：Excel 生成与写入

step4_patent_type:
  method: kind_code_regex
  batch_size: all（纯本地，无需分批）
  validated_count: 2034
  zero_others: true

step5_dates:
  primary_method: patent.fetch（md文件解析）
  fallback_method: patent.search（日期字段）
  recommended_batch_size: 200
  max_batch_per_turn: 400（单对话轮次token限制）
  cache_mechanism: pending_pns.json + dates_results.json
  date_format: YYYY-MM-DD（从8位数字转换）
  known_problematic_jurisdictions: [UA, AR, ZA, HK]

pagination:
  limit_per_page: 100
  max_offset: 900
  strategy: incremental_offset
  guard: stop_if_empty_results

progress_save:
  strategy: append_per_company
  save_after_each_company: true
  failed_companies_tracking: true

step6_ipc_legal:
  primary_method: patent.search（filters.pn精确过滤）
  batch_size: 50条/组，4组并行=200条/轮
  family_lookup: 提取基础EP号反查翻译文件
  coverage_achieved: J列82.9%，K列84.7%（2035条验证）
  legal_status_map: {active:有效, pending:审中, inactive:失效}
  header_required: J1=IPC分类号, K1=法律状态
  known_uncoverable: [ZA, AL, HRP, VN, UA, EA, 外观设计]

step7_target_extraction:
  phase1_method: title_keyword_matching
  phase2_method: patent.fetch md full_text parsing
  recommended_batch_size: 200个/批，10组×20并行
  cache_shared_with: step5（同一目录 session/downloads/document-fetch/）
  target_col: M（第13列，表头="靶点"）
  write_mode: incremental（不覆盖已有值）
  phase1_coverage: ~18%
  phase2_coverage: +10-15%（累计约30%）
  normal_empty_rate: ~70%（剂型/工艺/仪器/外观设计类无靶点属正常）
  keyword_dict_size: 70+个靶点，覆盖免疫检查点/肿瘤/代谢/炎症/神经/感染/细胞疗法
  known_issues: [E26-E29]
```

---

### Step 11 — Excel 统一格式规范（强制应用于所有输出文件）

> 本步骤规定所有由本 Skill 生成或修改的 Excel 文件必须遵守的统一格式标准。**每次写入 Excel 后，必须调用本节的 `apply_excel_format()` 函数进行格式化，再保存文件。**

#### 11.1 格式规范总览

| 项目 | 规范 |
|------|------|
| 列宽 | 自适应内容（基于最长单元格内容计算） |
| 表头底色 | 浅蓝色（`00B0F0` 或 `BDD7EE`） |
| 表头字色 | 黑色（`000000`） |
| 中文字体 | 宋体（SimSun） |
| 英文/数字字体 | Times New Roman |
| Sheet2 序号列 | 在第1列插入序号（表头"序号"，数据行从1开始递增） |

#### 11.2 完整实现代码

```python
import re
from copy import copy
from openpyxl import load_workbook
from openpyxl.styles import (
    Font, PatternFill, Alignment, Border, Side, Color
)
from openpyxl.utils import get_column_letter

# 表头浅蓝色
HEADER_FILL = PatternFill(fill_type="solid", fgColor="BDD7EE")
HEADER_FONT_CN = Font(name="宋体", bold=True, color="000000", size=11)
HEADER_FONT_EN = Font(name="Times New Roman", bold=True, color="000000", size=11)
DATA_FONT_CN   = Font(name="宋体", color="000000", size=11)
DATA_FONT_EN   = Font(name="Times New Roman", color="000000", size=11)

def _is_chinese(text: str) -> bool:
    """判断字符串是否含中文字符，含中文则用宋体，否则用Times New Roman。"""
    if not text:
        return False
    return bool(re.search(r'[\u4e00-\u9fff]', str(text)))

def _get_font(text, is_header=False):
    """根据内容选择字体：含中文→宋体，纯英文/数字→Times New Roman。"""
    cn = _is_chinese(str(text) if text else "")
    if is_header:
        return copy(HEADER_FONT_CN) if cn else copy(HEADER_FONT_EN)
    return copy(DATA_FONT_CN) if cn else copy(DATA_FONT_EN)

def _auto_col_width(ws):
    """自适应列宽：按每列最长内容计算，最小8，最大60。"""
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            try:
                val = str(cell.value) if cell.value is not None else ""
                # 中文字符宽度约为英文2倍
                width = sum(2 if ord(c) > 127 else 1 for c in val)
                max_len = max(max_len, width)
            except Exception:
                pass
        adjusted = min(max(max_len + 2, 8), 60)
        ws.column_dimensions[col_letter].width = adjusted

def _insert_serial_col(ws):
    """
    在 Sheet2 最左侧插入序号列（如已存在序号列则跳过）。
    表头写"序号"，数据行从1开始递增（跳过空行）。
    """
    # 检查第1列是否已是序号列
    first_header = ws.cell(row=1, column=1).value
    if first_header == "序号":
        return  # 已存在，跳过
    # 插入新列到第1列
    ws.insert_cols(1)
    ws.cell(row=1, column=1, value="序号")
    serial = 1
    for r in range(2, ws.max_row + 1):
        # 判断该行是否为空行（第2列开始全空则跳过）
        row_vals = [ws.cell(row=r, column=c).value for c in range(2, min(6, ws.max_column + 1))]
        if any(v is not None and str(v).strip() != "" for v in row_vals):
            ws.cell(row=r, column=1, value=serial)
            serial += 1

def apply_excel_format(filepath: str, sheet2_serial: bool = True):
    """
    对指定 Excel 文件应用统一格式规范：
    - 所有 Sheet：表头浅蓝底色+黑字、列宽自适应、字体规范
    - Sheet2（若存在）：在第1列插入序号列（sheet2_serial=True 时执行）
    
    参数：
        filepath: Excel 文件路径
        sheet2_serial: 是否为 Sheet2 插入序号列，默认 True
    """
    wb = load_workbook(filepath)

    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        is_sheet2 = (sheet_name == wb.sheetnames[1]) if len(wb.sheetnames) > 1 else False

        # Step 1：Sheet2 插入序号列
        if is_sheet2 and sheet2_serial:
            _insert_serial_col(ws)

        # Step 2：应用字体和表头格式
        for r in range(1, ws.max_row + 1):
            is_header = (r == 1)
            for c in range(1, ws.max_column + 1):
                cell = ws.cell(row=r, column=c)
                val = cell.value
                font = _get_font(val, is_header=is_header)
                cell.font = font
                if is_header:
                    cell.fill = copy(HEADER_FILL)
                    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=False)
                else:
                    cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=False)

        # Step 3：自适应列宽
        _auto_col_width(ws)

    wb.save(filepath)
    print(f"[格式化完成] {filepath}")
```

#### 11.3 调用方式（每次保存 Excel 后立即执行）

```python
# 在所有 Excel 写入脚本末尾，save 之后加入：
apply_excel_format(output_path, sheet2_serial=True)
```

#### 11.4 已知注意事项

| ID | 问题 | 根因 | 规避方式 |
|----|------|------|--------|
| E60 | 序号列重复插入 | 未检查第1列是否已是序号列 | `_insert_serial_col` 函数先判断第1列表头是否为"序号" |
| E61 | 中英混合内容字体不统一 | 一个单元格含中英文时只能设一种字体 | 以是否含中文字符为判断依据，含中文→宋体，纯英文→Times New Roman |
| E62 | 列宽过窄截断内容 | 未正确计算中文字符宽度 | 中文字符按2倍宽计算：`2 if ord(c) > 127 else 1` |
| E63 | 格式化破坏原有超链接 | openpyxl 重设 font 会清除超链接样式 | 对含超链接的列（如专利链接列）单独处理，保留 hyperlink 属性 |
| E64 | Sheet2 序号列后原列号偏移 | insert_cols(1) 导致所有列右移1 | 格式化前先插入序号列，再做表头反查，不硬编码列号 |

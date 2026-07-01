---
name: corp-innovation-brief
description: |
  企业科创力评估与信贷分析简报生成技能。输入企业名称，自动检索全量专利、相关论文和公开网络数据，输出包含公司概况、主营业务、核心专利技术方向、专利组合分析、市场地位与战略合作、信贷评审关注点六大板块的结构化简报。面向银行信贷客户经理、审批人员和风险控制人员。
---

# corp-innovation-brief · 企业科创力评估简报

## 定位与目标用户

本技能面向**银行信贷客户经理、信贷审批人员、信贷风险控制人员**，帮助其快速评估一家企业的科技创新能力，并生成可直接用于信贷决策支持的结构化分析简报。

---

## 触发场景

以下任意情形均可触发本技能：

- 用户输入企业名称（全称或简称），请求生成科创分析简报
- 用户明确提到"科创评估"、"科创力分析"、"科创报告"、"科创简报"

---

## 输入

| 字段 | 说明 | 必填 |
|------|------|------|
| `company_name` | 企业名称（全称或简称均可） | ✅ |
| `market` | 目标市场/司法管辖区，如 CN、US、EP（可多选） | 可选，默认全部 |
| `topk_patents` | 检索专利数量上限 | 可选，默认 300 |
| `report_lang` | 报告输出语言 | 可选，默认简体中文 |

---

## 执行流程

```
Step 1  专利全量检索
Step 2  核心专利抽取与技术方向聚类
Step 3  专利组合统计分析
Step 4  论文检索
Step 5  公开网络信息检索（公司概况/市场/合作/舆情）
Step 6  综合评分与信贷关注点判断
Step 7  结构化报告生成
Step 8  确认导出报告
```

### Step 1 · 专利全量检索

调用 `patent.search`，以 `assignees=[company_name]` 作为主过滤器，配合 `filter` 策略检索该企业名下全部专利。

- 默认检索 `topk=300`；如有更多，追加 `filter` + `date_type` 分段检索以提高召回
- 记录以下字段：`patent_id`、`title`、`application_date`、`publication_date`、`legal_status`、`ipc`、`jurisdiction`、`cited_count`、`assignee`、专利价值、技术主题
- 若简称与多家企业匹配，优先检索全称，并提示用户确认

### Step 2 · 核心专利抽取与技术方向聚类

1. 按"专利价值"降序排列，选取 Top 10 专利作为"高价值核心专利"
2. 按 `ipc` 大类（前5位）聚合，统计各技术方向专利数量占比
3. 对 Top 50 专利逐条调用 `patent.fetch` 获取摘要与权利要求，提炼技术要点
4. 基于全量专利技术文本、权利要求的分析，统计企业创新词云，并提炼 TOP10 技术词

对比分析 ipc（前5）技术方向、TOP50 专利的技术要点和 TOP10 技术词，保留重合度高的 TOP5，作为主要技术方向进行分析。

### Step 3 · 专利组合统计分析

从检索结果中计算以下维度：

| 维度 | 计算方式 |
|------|----------|
| 产出持续性 | 按申请年份统计每年专利数量，判断是否持续增长/波动/衰退 |
| 专利授权数量 | 按申请年份统计每年专利授权数量，判断技术是否有新颖性 |
| 法律状态占比 | active / pending / inactive 各占比 |
| 被引次数 | 总被引、平均被引、最高被引专利 |
| 地域布局 | 按 jurisdiction 统计，展示主要布局国家/地区 |
| 专利价值 | 通过专利价值总额、平均价值判断技术质量 |

### Step 4 · 论文检索

调用 `paper.search`，以企业名称为 `assignees` 过滤器，检索该企业研究人员发表的学术论文（`topk=20`），提取研究方向与发表趋势。

### Step 5 · 公开网络信息检索

调用 `web.search` 检索以下内容（分 2-3 次独立查询）：

1. `"{company_name} 主营业务 产品 合作案例"` → 获取公司概况与产品矩阵
2. `"{company_name} 市场地位 合作 战略"` → 获取市场信息与合作关系
3. `"{company_name} 融资 舆情 诉讼 风险"` → 获取潜在风险线索

对可信度高的来源（官网、工商、行业报告）优先引用；明显营销内容降权。

### Step 6 · 综合评分与信贷关注点判断

基于上述数据，从以下维度输出评分信号（High / Medium / Low）：

| 评估维度 | 信号来源 |
|----------|----------|
| 专利活跃度 | 近5年专利申请量趋势 |
| 技术壁垒 | 核心专利被引次数、独立权项数量、专利对外许可数量 |
| 研发团队稳定性 | 主要专利发明人每年的变动情况 |
| 地域布局广度 | 境外专利占比 |
| 技术质量 | 发明专利占比、有效状态的发明专利占比、专利价值总额 |
| 研发持续投入 | 论文发表 + 专利持续增长 |
| 潜在风险 | 法律状态 inactive 占比、诉讼线索、负面舆情、失效专利占比、专利对外的转让 |

### Step 7 · 结构化报告生成

按以下六大板块输出 Markdown 报告（见"报告模板"）。

### Step 8 · 确认导出报告

Step 7 报告在对话中完整呈现后，**先**使用 `ask` 工具向用户发出一条确认提示，询问是否需要导出报告。**不要**在用户确认之前自动生成 HTML 文件。

确认提示文本：

```
📄 报告已生成完毕。是否需要导出为 HTML 文件以便保存或分享？
```

选项：
- `export`：导出，生成 HTML 文件
- `skip`：不需要，报告已在对话中查看

#### 8.1 用户确认导出（回复"导出"、"是"、或选择 export）

执行以下操作：

**① 生成 HTML 报告文件**

使用 `python` 工具执行以下脚本，将报告 Markdown 内容转换为自包含 HTML，写入 `@skill_workspace/`：

```python
import os, re, html as html_lib

report_md = """<<Step7输出的完整Markdown内容>>"""
company_name = "<<企业名称>>"
report_date = "<<报告日期>>"

def md_to_html(md):
    lines = md.split('\n')
    html_lines = []
    in_table = False
    in_code = False
    for line in lines:
        if line.startswith('```'):
            if not in_code:
                html_lines.append('<pre><code>')
                in_code = True
            else:
                html_lines.append('</code></pre>')
                in_code = False
            continue
        if in_code:
            html_lines.append(html_lib.escape(line))
            continue
        if line.startswith('|'):
            if not in_table:
                html_lines.append('<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse;width:100%;">')
                in_table = True
            cells = [c.strip() for c in line.strip('|').split('|')]
            if all(re.match(r'^[-: ]+$', c) for c in cells):
                continue
            tag = 'th' if html_lines and html_lines[-1].startswith('<table') else 'td'
            html_lines.append('<tr>' + ''.join(f'<{tag}>{html_lib.escape(c)}</{tag}>' for c in cells) + '</tr>')
            continue
        else:
            if in_table:
                html_lines.append('</table>')
                in_table = False
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            level = len(m.group(1))
            html_lines.append(f'<h{level}>{html_lib.escape(m.group(2))}</h{level}>')
            continue
        line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
        line = re.sub(r'\*(.+?)\*', r'<em>\1</em>', line)
        line = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank">\1</a>', line)
        if re.match(r'^[-*]\s+', line):
            line = '<li>' + line[2:] + '</li>'
        elif re.match(r'^\d+\.\s+', line):
            line = '<li>' + re.sub(r'^\d+\.\s+', '', line) + '</li>'
        elif line.strip() == '---':
            line = '<hr/>'
        elif line.strip() == '':
            line = '<br/>'
        else:
            line = '<p>' + line + '</p>'
        html_lines.append(line)
    if in_table:
        html_lines.append('</table>')
    return '\n'.join(html_lines)

body_html = md_to_html(report_md)

full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>企业科创力分析简报 · {html_lib.escape(company_name)}</title>
<style>
  body {{ font-family: 'PingFang SC', 'Microsoft YaHei', Arial, sans-serif;
         max-width: 960px; margin: 40px auto; padding: 0 24px;
         color: #1a1a1a; line-height: 1.7; }}
  h1 {{ font-size: 1.8em; border-bottom: 2px solid #1a56db; padding-bottom: 8px; }}
  h2 {{ font-size: 1.4em; color: #1a56db; margin-top: 32px; }}
  h3 {{ font-size: 1.15em; color: #333; }}
  table {{ font-size: 0.9em; margin: 16px 0; }}
  th {{ background: #f0f4ff; }}
  td, th {{ padding: 6px 12px; text-align: left; }}
  pre {{ background: #f5f5f5; padding: 12px; border-radius: 4px; overflow-x: auto; }}
  hr {{ border: none; border-top: 1px solid #e0e0e0; margin: 24px 0; }}
  a {{ color: #1a56db; }}
  .footer {{ color: #999; font-size: 0.85em; margin-top: 48px; border-top: 1px solid #e0e0e0; padding-top: 12px; }}
</style>
</head>
<body>
{body_html}
</body>
</html>"""

output_dir = os.environ.get('EUREKA_PYTHON_OUTPUT_DIR', '.')
filename = f"科创力分析简报_{company_name}_{report_date}.html"
output_path = os.path.join(output_dir, filename)
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f"REPORT_FILE={output_path}")
print(f"REPORT_FILENAME={filename}")
```

执行时需将 `report_md`、`company_name`、`report_date` 替换为 Step 7 的实际值，并使用 `output_dir_ref="@skill_workspace/"` 以便 Eureka 正确解析输出路径。

**② 向用户提供文件链接**

HTML 文件生成成功后，在回复中以 Markdown 链接形式呈现文件句柄：

```
✅ 报告已导出，点击下列链接在浏览器中打开：

[📥 下载完整报告：{filename}](@skill_workspace/{filename})
```

> **注意：** 链接格式为 `@skill_workspace/{filename}`，Eureka 会将其解析为本地文件路径并在系统默认浏览器中打开 HTML 页面，用户可直接通过浏览器的"另存为"功能保存文件。

#### 8.2 用户选择不导出（回复"否"、"不用"、"跳过"、或选择 skip）

告知用户报告已在对话中完整呈现，无需导出：

```
📋 好的，报告已在对话中完整呈现，如后续需要导出请告知。
```

---

## 报告模板

```markdown
# 企业科创力分析简报
**企业名称：** {company_name}
**报告日期：** {date}
**数据来源：** PatSnap 专利数据库 / 学术论文库 / 公开网络
**免责说明：** 本报告基于公开数据，仅供信贷参考，不构成最终信贷决策依据。

---

## 一、公司概况

{公司基本信息：成立时间、注册地、实控人/股东结构（如公开）、主要经营范围、近期重大事项}

---

## 二、主营业务与产品矩阵

{主要产品线/服务、技术平台、下游客户行业}

| 业务方向 | 主要产品/服务 | 技术平台 |
|----------|--------------|----------|
| … | … | … |

---

## 三、与主营业务相关的核心专利及技术方向

### 3.1 技术方向分布

| IPC 大类 | 技术领域描述 | 专利数量 | 占比 |
|----------|-------------|----------|------|
| … | … | … | … |

### 3.2 高价值核心专利（Top 10）

| 序号 | 专利号 | 标题 | 申请日 | 被引次数 | 法律状态 | 技术要点摘要 |
|------|--------|------|--------|----------|----------|-------------|
| … | … | … | … | … | … | … |

---

## 四、专利组合分析

### 4.1 专利产出持续性

{逐年申请量图表文字描述 + 趋势判断}

### 4.2 法律状态占比

| 状态 | 数量 | 占比 |
|------|------|------|
| 有效（active） | … | … |
| 审中（pending） | … | … |
| 失效（inactive） | … | … |

### 4.3 被引分析

- 专利总数：{n}
- 总被引次数：{n}
- 平均被引：{n}
- 最高被引专利：{专利号} · {被引次数}次

### 4.4 地域布局

| 国家/地区 | 专利数量 | 占比 |
|----------|----------|------|
| … | … | … |

### 4.5 专利构成

| 专利类型 | 专利数量 | 占比 |
|----------|----------|------|
| … | … | … |

---

## 五、市场地位与战略合作

{市场排名/份额（如有）、主要客户/合作伙伴、重要认证/资质、融资与战略合作事件}

---

## 六、信贷评审关注点与风险提示

### 6.1 正向支持因素（科创优势）

- **技术壁垒：** …
- **专利活跃度：** …
- **地域布局：** …
- **研发持续性：** …
- **技术质量：** …

### 6.2 潜在风险提示

- **专利失效风险：** …
- **技术集中风险：** …
- **诉讼/纠纷线索：** …
- **舆情风险：** …
- **其他风险：** …

### 6.3 综合科创力信号

| 维度 | 信号 | 依据 |
|------|------|------|
| 专利活跃度 | High / Medium / Low | … |
| 技术壁垒 | High / Medium / Low | … |
| 研发团队稳定性 | High / Medium / Low | … |
| 地域布局广度 | High / Medium / Low | … |
| 技术质量 | High / Medium / Low | … |
| 研发持续投入 | High / Medium / Low | … |
| 潜在风险 | High / Medium / Low | … |

> **结论：** {一句话综合评价}

---

*本报告由 Eureka · PatSnap 智慧芽 自动生成，数据截止日期：{date}。*
```

---

## 输出规范

- 默认以 Markdown 格式在对话中渲染报告
- 所有专利引用附上可溯源的 `[专利号](Patsnap URL)` 链接
- 论文引用附上标题、作者、发表年份
- 网络来源标注 `[Sn]` 脚注
- 无法获取数据的字段标注 `暂无公开数据`，不得捏造

---

## 护栏与限制

- 不得捏造任何专利号、引用数、财务数据或公司陈述
- 若企业名称匹配模糊，优先询问确认，而非自行推断
- 报告结论仅供参考，最终信贷决策由审批人员负责
- 不得在报告中出现政治相关内容或对国家领导人的评价

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。

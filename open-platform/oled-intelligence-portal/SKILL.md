---
name: oled-intelligence-portal
description: |
  输入任意技术领域关键词（如"OLED"、"固态电池"、"mRNA疫苗"），自动生成该领域的情报简报门户（HTML网站）。监控的企业和技术分支由AI模型自动检索和拆解，新闻由智慧芽新闻向量检索自动获取，专利使用关键词扩展后在智慧芽专利数据库直接检索。当用户说"生成XXX情报门户"、"XXX领域情报简报"、"帮我监控XXX技术"时触发。
---

# 技术领域情报简报门户生成器

根据用户输入的技术领域关键词，自动生成专业的多页 HTML 情报门户。

## 核心工作流

### Step 1：接收用户关键词

用户输入一个技术领域关键词，例如：`OLED`、`固态电池`、`钙钛矿太阳能`、`GLP-1受体激动剂`。

### Step 2：AI 推断监控企业（自动，无需用户提供）

调用 `ls_news_vector_search` 和 `ls_drug_aggregation`（非药物领域用新闻检索），结合模型知识，推断该领域主要企业（目标8-15家）。

**推断逻辑**：
1. 先用模型知识列出该领域全球主要玩家（头部5-8家）
2. 调用 `ls_news_vector_search(query="{keyword} 企业 公司", lang="CN", top_k=20)` 补充从新闻中识别的企业
3. 合并去重，保留8-15家最相关企业，记录中英文名和简称

### Step 3：AI 拆分技术分支（自动，无需用户提供）

用模型对该领域进行技术拆解，生成8-16个技术标签。

**拆解逻辑**：
1. 模型先按领域知识拆出主要技术方向
2. 调用 `ls_patent_vector_search(query="{keyword} 技术路线", lang="CN", top_k=10)` 验证和补充技术标签
3. 每个技术标签包含：中文名、英文名、简短描述、检索关键词列表

### Step 4：自动检索新闻

**每家企业**调用：
```
ls_news_vector_search(query="{keyword} {公司名}", lang="CN", top_k=5)
```

**每个技术分支**调用：
```
ls_news_vector_search(query="{keyword} {技术标签}", lang="CN", top_k=5)
```

**重大事件**调用：
```
ls_news_vector_search(query="{keyword} 重大事件 市场动态 产业政策", lang="CN", top_k=10)
```

解析返回的 `_text_display`、`_text`、`url` 字段，组装成新闻条目。

### Step 5：专利关键词扩展 + 智慧芽检索

**关键词扩展**：
- 模型根据输入关键词，生成3-6个扩展检索词（同义词、英文名、上位概念、核心技术词）
- 例如：`OLED` → `["OLED", "有机发光二极管", "AMOLED", "organic light emitting diode", "柔性显示"]`

**专利检索**（调用已注册的 `patent.search` 能力，即 `mcp_patent-search__patsnap_search`）：
```json
{
  "search_strategy": ["keyword", "filter"],
  "keywords": [扩展关键词列表],
  "sources": ["patent"],
  "filters": {
    "date_from": 20230101,
    "date_to": 20260507
  },
  "topk": 30
}
```

解析返回的专利列表，提取：标题、申请人、公开号、摘要。

### Step 6：生成情报门户 HTML

调用 `@skill/scripts/generate_portal.py` 生成多页 HTML 网站。

**输入数据结构**（Python dict，传入脚本）：
```python
portal_data = {
    "keyword": "OLED",          # 领域关键词
    "date_range": "2025年1月-2026年5月",
    "companies": [
        {
            "name_cn": "三星显示",
            "name_en": "Samsung Display",
            "slug": "samsung",
            "news": [{"title": "...", "date": "2026-01-15", "source": "...", "summary": "...", "url": "..."}]
        }
    ],
    "tech_tags": [
        {
            "name_cn": "串联OLED",
            "name_en": "Tandem OLED",
            "slug": "tandem",
            "description": "...",
            "news": [...]
        }
    ],
    "major_events": [
        {"title": "...", "date": "...", "summary": "...", "url": "..."}
    ],
    "patents": [
        {"title": "...", "applicant": "...", "pub_no": "...", "pub_date": "...", "abstract": "..."}
    ],
    "stats": {
        "total_news": 150,
        "total_patents": 30,
        "total_companies": 12,
        "total_tech_tags": 16
    }
}
```

**生成文件结构**：
```
{keyword}-portal/
├── index.html           # 主门户页
├── {slug}.html          # 每家企业详情页
├── tech-{slug}.html     # 每个技术分支详情页
└── patents.html         # 专利汇总页
```

### Step 7：交付

输出生成的 HTML 文件路径，提示用户可以直接在浏览器中打开 `index.html`。

---

## 设计规范

**UI 设计**（Tailwind CSS via CDN）：
- 字体：Inter + Microsoft YaHei Light
- 主色调渐变：由关键词领域自动选择（默认蓝色 `#1e3a8a→#3b82f6→#06b6d4`）
- 卡片悬浮动效：`translateY(-8px)` + shadow
- 技术标签：青色背景
- 专利卡片：紫色左边框
- 重大事件：彩色左边框时间轴

**中文界面**：所有 UI 文字使用中文，技术术语保留英文。

---

## 工具调用规范

| 步骤 | 工具 | 说明 |
|------|------|------|
| 企业识别 | `ls_news_vector_search` | 从新闻中识别企业 |
| 技术分支验证 | `ls_patent_vector_search` | 从专利中验证技术方向 |
| 新闻检索 | `ls_news_vector_search` | 按企业/技术分支批量检索 |
| 专利检索 | `mcp_patent-search__patsnap_search` | 关键词扩展后直接检索 |
| HTML生成 | Python `generate_portal.py` | 渲染完整门户 |

---

## 参考文件

- `references/html-templates.md` — HTML 页面模板
- `references/company-mapping.md` — 企业名称映射（OLED 领域示例）
- `references/tech-tags.md` — 技术标签定义（OLED 领域示例）
- `references/data-processing.md` — 数据处理规范

---

## 关键规则

1. **不需要用户提供任何文件**——所有数据由 AI 自动检索
2. **关键词通用**——不限于 OLED，任何技术领域均可
3. **新闻来源**：仅使用 `ls_news_vector_search` 返回的真实结果，不捏造新闻
4. **专利来源**：仅使用 `mcp_patent-search__patsnap_search` 返回的真实结果，不捏造专利
5. **所有链接**：使用真实 URL，若为空则用 `'#'`
6. **响应式设计**：使用 Tailwind 的 `md:` / `lg:` 前缀适配多端

## 使用前配置
本 Skill 依赖智慧芽开放平台 MCP 服务：
- 完成安装、初次使用时需进行自检，参见 README.md
- 用户需完成账号授权，并确保 Agent 环境已启用对应 MCP 工具
- 若未完成配置，本 Skill 只能提供分析框架，无法检索实时数据或生成基于数据库的结论
- 缺少MCP配置时，引导用户参照 README.md 在 [[open.zhihuiya.com](https://open.zhihuiya.com/)](https://open.zhihuiya.com/) 获取MCP。

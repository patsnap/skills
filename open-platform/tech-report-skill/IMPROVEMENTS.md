# tech-report-skill 改进记录

本文档记录了在咖啡机简报生成过程中发现的问题及解决方案。

## 改进列表

### 1. 专利链接无法跳转

**问题描述：**
- 生成的HTML简报中，专利公开号无法点击跳转到原文

**原因分析：**
- 原始方案使用 `pandas.to_excel()` 保存标引结果，导致Excel中的超链接丢失

**解决方案：**
- 修改 `tag_relevant.py`，改用 `openpyxl.load_workbook()` 直接操作Excel
- 在原始Excel上添加"相关性标引"列，保留所有超链接
- 代码位置：[tag_relevant.py:95-117](../scripts/tag_relevant.py#L95-L117)

```python
# 直接在原始Excel文件上添加标引列，保留图片和超链接
wb = openpyxl.load_workbook(input_file)
ws = wb.active

# 在最后一列添加"相关性标引"列
tag_col = ws.max_column + 1
ws.cell(1, tag_col).value = "相关性标引"

# 填充标引结果
for idx, value in enumerate(df["相关性标引"], start=2):
    ws.cell(idx, tag_col).value = value
```

### 2. 专利摘要附图丢失

**问题描述：**
- 生成的HTML简报中，专利摘要附图无法显示

**原因分析：**
- 同问题1，使用 `pandas.to_excel()` 导致Excel内嵌图片丢失

**解决方案：**
- 使用 `openpyxl` 保留原始Excel图片
- 在 `generate_report.py` 中提取Excel图片并转为Base64嵌入HTML
- 代码位置：[generate_report.py:65-113](../scripts/generate_report.py#L65-L113)

```python
def extract_images_from_excel(xlsx_path, high_rel_df):
    """从Excel中提取摘要附图"""
    wb = load_workbook(xlsx_path)
    ws = wb.active
    
    # 提取图片（C列，列索引为2）
    row_to_b64 = {}
    for img in ws._images:
        anchor = img.anchor
        if hasattr(anchor, "_from") and anchor._from.col == 2:
            row = anchor._from.row + 1
            try:
                b64 = base64.b64encode(img._data()).decode("utf-8")
                row_to_b64[row] = b64
            except:
                pass
    
    # 建立专利号到Excel行号的映射
    excel_pn_to_row = {}
    for row in range(2, ws.max_row + 1):
        pn = ws.cell(row, 2).value  # B列公开号
        if pn:
            excel_pn_to_row[str(pn)] = row
    
    # 根据专利号匹配图片
    pn_to_b64 = {}
    for i, row in high_rel_df.iterrows():
        pn = str(row["公开(公告)号"])
        if pn in excel_pn_to_row:
            excel_row = excel_pn_to_row[pn]
            if excel_row in row_to_b64:
                pn_to_b64[pn] = row_to_b64[excel_row]
    
    return pn_to_b64
```

### 3. 每个技术分类下专利数量太少（2-3件）

**问题描述：**
- 配置文件中每个技术分类只列出了2-3个代表专利，展示内容过少

**解决方案：**
- 实现基于关键词匹配的智能专利分类算法
- 为每个专利计算相关度得分（匹配关键词数量）
- 自动选取每个技术分类的Top-20高相关专利
- 代码位置：[generate_report.py:116-168](../scripts/generate_report.py#L116-L168)

```python
def classify_patents_by_keywords(high_rel_df, tech_cats, keywords_config):
    """根据关键词自动分类专利，并为每个分类挑选相关度最高的Top20专利"""
    
    # 定义六大技术分类的关键词
    default_tech_keywords = {
        '研磨精度与均匀度技术': ['研磨', '磨豆', 'grind', 'burr', ...],
        '加热温控技术': ['加热', '温度', '温控', 'heat', 'temperature', ...],
        '高压压力动态控制技术': ['压力', '萃取压力', 'pressure', '泵', ...],
        '冲煮头均匀布水萃取技术': ['冲煮', '布水', '萃取', 'brew', ...],
        '蒸汽奶泡绵密技术': ['蒸汽', '奶泡', 'steam', 'milk', 'froth', ...],
        '智能电控与水路闭环技术': ['智能', '控制', '传感', 'IoT', ...],
    }
    
    cat_to_patents = {}
    for catname, catcount, catsummary, cat_patent_list in tech_cats:
        keywords = default_tech_keywords.get(catname, [])
        patent_scores = []
        
        # 计算所有专利的相关度得分
        for idx, row in high_rel_df.iterrows():
            text = ' '.join(str(row[col]) for col in search_cols).lower()
            
            # 计算匹配的关键词数量作为相关度得分
            score = sum(1 for kw in keywords if kw.lower() in text)
            
            if score > 0:
                patent_scores.append((str(row['公开(公告)号']), score))
        
        # 按得分降序排序，取Top20
        patent_scores.sort(key=lambda x: x[1], reverse=True)
        top_patents = [pn for pn, score in patent_scores[:20]]
        cat_to_patents[catname] = top_patents
    
    return cat_to_patents
```

### 4. 行业新闻无法跳转

**问题描述：**
- HTML简报中展示了新闻标题和摘要，但缺少跳转链接

**解决方案：**
- 在 `config/{技术主题}_content.py` 的 NEWS 配置中添加 URL 字段
- 在HTML生成时添加"查看原文"链接按钮
- 代码位置：[generate_report.py:340-344](../scripts/generate_report.py#L340-L344)

```python
# 配置文件格式（第5个参数是URL）
NEWS = [
    (
        '全球咖啡机市场持续增长，智能化成为主流趋势',
        '家电行业观察',
        '2026-04-15',
        '摘要内容...',
        'https://www.chinaiol.com/'  # 新闻链接
    ),
]

# HTML生成
for title, source, date, summary, url in news:
    A(f'<div class="news-card">')
    A(f'<div class="news-title">{title}</div>')
    A(f'<div class="news-summary">{summary}</div>')
    A(f'<a class="news-link" href="{url}" target="_blank">查看原文 →</a>')
    A('</div>')
```

### 5. 添加装饰性背景图片

**问题描述：**
- 简报头部Hero区域缺少视觉吸引力

**解决方案：**
- 从Unsplash下载高质量咖啡机背景图片
- 转换为Base64编码直接嵌入HTML，确保简报发送后图片仍可显示
- 使用渐变叠加层保证文字可读性
- 代码位置：[generate_report.py:17-29](../scripts/generate_report.py#L17-L29)

```python
def download_hero_image():
    """下载Hero背景图片并转换为Base64"""
    url = 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=1200&q=80'
    try:
        print("正在下载背景图片...")
        with urllib.request.urlopen(url, timeout=10) as response:
            img_data = response.read()
        b64_data = base64.b64encode(img_data).decode('utf-8')
        print(f"背景图片下载成功 ({len(img_data) / 1024:.1f} KB)")
        return f"data:image/jpeg;base64,{b64_data}"
    except Exception as e:
        print(f"背景图片下载失败: {e}，将使用纯渐变背景")
        return None

# CSS样式（渐变叠加）
if hero_bg_url:
    hero_bg = f"background:linear-gradient(135deg,rgba(26,26,46,0.85) 0%,rgba(22,33,62,0.80) 60%,rgba(15,52,96,0.75) 100%),url({hero_bg_url}) center/cover;"
else:
    hero_bg = "background:linear-gradient(135deg,rgba(26,26,46,0.85) 0%,rgba(22,33,62,0.80) 60%,rgba(15,52,96,0.75) 100%);"
```

## 技术亮点

### 1. 完全自包含的HTML
- 所有图片（专利附图、背景图）均转为Base64嵌入
- 所有CSS内联，无外部依赖
- 可通过邮件发送或离线查看，图片永不丢失

### 2. 智能专利分类
- 基于关键词匹配算法自动分类专利
- 相关度评分确保最相关专利优先展示
- 避免手动配置大量专利号

### 3. 数据完整性保障
- 使用openpyxl直接操作Excel，保留所有元数据
- 超链接、图片、格式均完整保留
- 专利号到行号的精确映射

### 4. 响应式设计
- 支持桌面端和移动端
- 导航栏固定，支持快速跳转
- 卡片式布局，清晰美观

## 配置文件最佳实践

### 关键词配置 (_keywords.py)

```python
# 1. 包含关键词要覆盖中英文
INCLUDE_KEYWORDS = [
    # 中文关键词
    "研磨精度", "磨豆机", "咖啡研磨",
    # 英文关键词
    "grinding precision", "coffee grinder", "burr grinder",
]

# 2. 排除关键词避免误判
EXCLUDE_KEYWORDS = [
    "茶饮机", "果汁机",  # 排除其他饮料设备
    "tea machine", "juicer",
]

# 3. 公司简称便于显示
COMPANY_SHORT = {
    '德隆吉器具有限公司': '德隆',
    'DE LONGHI': '德隆',
}
```

### 内容配置 (_content.py)

```python
# 1. 新闻配置（5个字段）
NEWS = [
    (标题, 来源, 日期, 摘要, URL链接),
]

# 2. 重点公司配置
COMPANY_DATA = [
    (
        公司名称,
        国家/地区,
        技术总结（建议100-150字）,
        代表专利号列表（3-5件）
    ),
]

# 3. 技术分类配置
TECH_CATS = [
    (
        分类名称,
        预估专利数（可以不准确，会自动更新）,
        技术总结（建议80-120字）,
        代表专利号列表（可留空，系统自动选取Top20）
    ),
]
```

## 使用建议

1. **首次使用新技术主题**
   - 先创建 `{主题}_keywords.py` 配置文件
   - 运行一次标引，查看高相关专利数量
   - 根据结果调整关键词，确保高相关率在30%-60%

2. **优化简报质量**
   - 在 `{主题}_content.py` 中添加行业新闻
   - 精选3-6家重点公司，撰写技术总结
   - 定义4-8个技术分类，覆盖核心技术方向

3. **批量生成简报**
   - 配置文件可复用于同一技术主题的不同时间段
   - 使用脚本循环生成多个月份的简报
   - 对比不同时间段的技术演进趋势

## 未来改进方向

1. **交互式图表**
   - 专利申请趋势折线图
   - 公司分布饼图
   - 技术分类雷达图

2. **自动摘要生成**
   - 使用LLM自动生成技术总结
   - 自动提取专利核心创新点

3. **多语言支持**
   - 自动翻译简报内容
   - 支持中英文双语版本

4. **PDF导出**
   - 支持导出为PDF格式
   - 保留排版和交互功能

## 相关文件

- [SKILL.md](./SKILL.md) - Skill使用说明
- [tag_relevant.py](./scripts/tag_relevant.py) - 专利标引脚本
- [generate_report.py](./scripts/generate_report.py) - HTML生成脚本
- [咖啡机_keywords.py](./config/咖啡机_keywords.py) - 咖啡机关键词配置示例
- [咖啡机_content.py](./config/咖啡机_content.py) - 咖啡机内容配置示例

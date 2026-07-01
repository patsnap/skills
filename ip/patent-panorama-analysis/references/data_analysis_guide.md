# 专利数据分析指南

## 分析流程

1. **读取Excel**：用pandas读取专利数据，检查列名，标准化列名映射
2. **数据清洗**：提取申请年、清理申请人名称、标准化地域
3. **技术分类**：基于标题+摘要关键词匹配，为每条专利打上技术分类标签
4. **统计分析**：按年/申请人/技术分支/地域/法律状态做分组统计
5. **趋势计算**：计算各技术分支的增长率（2020→2024）
6. **重点识别**：高被引专利、多同族专利、核心申请人技术布局
7. **洞察提炼**：技术热点、空白点、竞争格局、风险点

## 核心分析代码模板

```python
import pandas as pd
import numpy as np
from collections import Counter

# 1. 读取数据
df = pd.read_excel(patent_excel_path)

# 2. 标准化列名（处理常见变体）
column_mapping = {
    '公开号': '公开(公告)号', '公告号': '公开(公告)号', '专利号': '公开(公告)号',
    'Publication Number': '公开(公告)号',
    '发明名称': '标题', '专利标题': '标题',
    '申请人': '[标]当前申请(专利权)人', '专利权人': '[标]当前申请(专利权)人',
    'Assignee': '[标]当前申请(专利权)人', 'Applicant': '[标]当前申请(专利权)人',
    '申请日期': '申请日', 'Filing Date': '申请日',
    '法律状态': '法律状态/事件', '案件状态': '法律状态/事件',
    '国家/地区': '受理局', 'Country': '受理局', '申请国': '受理局',
    '被引用次数': '被引用专利数量', 'Cited Count': '被引用专利数量',
    '同族国家': '简单同族国家/地区', 'Family Countries': '简单同族国家/地区'
}
for old, new in column_mapping.items():
    if old in df.columns and new not in df.columns:
        df.rename(columns={old: new}, inplace=True)

# 3. 提取申请年
df['申请年'] = pd.to_datetime(df['申请日'], errors='coerce').dt.year

# 4. 简化法律状态
def simplify_status(s):
    s = str(s)
    if '授权' in s: return '授权'
    if '实质审查' in s: return '实质审查'
    if 'PCT' in s: return 'PCT国际申请'
    if '公开' in s: return '公开'
    return '其他'
df['主要状态'] = df['法律状态/事件'].apply(simplify_status)

# 5. 技术分类（使用tech_keywords映射）
def classify_tech(row):
    text = str(row['标题']) + ' ' + str(row.get('Patsnap专利标题', row.get('摘要', '')))
    categories = []
    for cat, keywords in tech_keywords.items():
        for kw in keywords:
            if kw.lower() in text.lower():
                categories.append(cat)
                break
    return categories if categories else ['其他']
df['技术分类'] = df.apply(classify_tech, axis=1)

# 6. 清理申请人名称（使用clean_applicant函数）
def clean_applicant(name):
    if pd.isna(name): return ''
    name = str(name)
    # 根据实际数据中的申请人名称进行统一
    # ... 实现名称清理逻辑
    return name
df['申请人简称'] = df['[标]当前申请(专利权)人'].apply(clean_applicant)

# 7. 核心统计
year_trend = df.groupby('申请年').size().to_dict()
status_dist = df['主要状态'].value_counts().to_dict()
office_dist = df['受理局'].value_counts().to_dict()
# 技术分类统计
all_cats = []
for cats in df['技术分类']:
    all_cats.extend(cats)
tech_dist = Counter(all_cats)
applicant_dist = df['申请人简称'].value_counts().head(15).to_dict()
```

## 申请人清理规则模板

```python
def clean_applicant(name):
    if pd.isna(name): return ''
    name = str(name)
    # 国际巨头
    if any(k in name for k in ['雷神', 'Raytheon', 'RTX']): return '雷神科技'
    if any(k in name for k in ['通用电气', 'GE', 'General Electric']): return '通用电气'
    if any(k in name for k in ['罗尔斯', '罗尔斯罗伊斯', 'Rolls-Royce', '劳斯莱斯']): return '罗尔斯·罗伊斯'
    if any(k in name for k in ['赛峰', 'Safran']): return '赛峰集团'
    # 中国航发系（根据实际名称调整）
    if '航发湖南' in name or '动研' in name: return '中国航发动研所'
    if '航发四川' in name or '涡轮' in name: return '中国航发涡轮院'
    if '航发沈阳' in name or '动力' in name: return '中国航发动力所'
    if '航发商用' in name or '商发' in name: return '中国航发商发'
    if '航发北京' in name or '航材' in name: return '中国航发航材院'
    # 高校
    if '西北工业' in name: return '西北工业大学'
    if '北京航空航天' in name: return '北京航空航天大学'
    if '南京航空航天' in name: return '南京航空航天大学'
    if '国防科技' in name: return '国防科技大学'
    # 研究机构
    if '中科院' in name or '科学院' in name: return '中科院'
    if '船舶' in name: return '中船研究所'
    # 默认取前10字符
    return name[:10]
```

## 增长率计算

```python
# 各技术分支年度数据
tech_branches = list(tech_keywords.keys())
years = [2020, 2021, 2022, 2023, 2024, 2025]
tech_year_matrix = {}
for tech in tech_branches:
    tech_year_matrix[tech] = {}
    for yr in years:
        count = sum(1 for idx in df[df['申请年']==yr].index if tech in df.loc[idx, '技术分类'])
        tech_year_matrix[tech][yr] = count

# 计算增长率
tech_growth = {}
for tech in tech_branches:
    v2020 = tech_year_matrix[tech].get(2020, 0)
    v2024 = tech_year_matrix[tech].get(2024, 0)
    growth = ((v2024 - v2020) / max(v2020, 1)) * 100
    tech_growth[tech] = {'2020': v2020, '2024': v2024, 'growth': growth}
```

## 洞察生成规则

### 技术热点识别
- 增长率>200%：高增热点
- 增长率100-200%：中高增长
- 专利基数>200件且正增长：持续热门

### 技术空白点识别
- 专利总量<50件：布局空白
- 增长率<50%或负增长：技术迭代窗口
- 2024年申请量<10件：新兴机会

### 竞争格局划分
- 第一梯队（国际龙头）：专利>200件
- 第二梯队（国内主力）：专利50-200件
- 第三梯队（高校/研究机构）：专利<50件但某领域深耕

### 风险等级划分
- 高：核心领域专利密度>100件，国际巨头高度集中
- 中高：专利密度50-100件，多申请人重叠
- 中：专利密度<50件，但核心专利被引>20次

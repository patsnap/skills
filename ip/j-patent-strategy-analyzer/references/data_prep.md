# 数据准备层规范

> **使用说明**：本文件定义了从原始专利清单到`data`字典的完整数据处理流程。所有数据分析在此层完成，HTML报告只负责展示。

## 一、数据加载与清洗

```python
# === 环境前置检查（阶段零保障）===
# 若以下任一包未安装，会给出清晰错误提示，引导用户先执行阶段零
import importlib
for _pkg in ['pandas', 'numpy', 'matplotlib', 'openpyxl']:
    try:
        importlib.import_module(_pkg)
    except ImportError as _e:
        raise RuntimeError(
            f"[依赖缺失] {_pkg} 未安装。请先执行 SKILL.md 阶段零（环境准备），"
            f"通过 runtime.apply_sync 安装依赖后再重试。原始错误：{_e}"
        )
# === 正常导入 ===

import pandas as pd
import numpy as np
from collections import Counter
import json
import re
import os

# 1. 加载专利清单
df = pd.read_excel('{{patent_list_file}}')

# 2. 提取申请年份
df['申请年'] = pd.to_datetime(df['申请日'], errors='coerce').dt.year

# 3. 法律状态映射（三分类）
def map_status(s):
    if pd.isna(s): return '失效'
    s = str(s)
    # 【强制】先匹配负面/终结状态，避免正向关键字子串误判
    if any(k in s for k in ['避免重复授权','期限届满','视为撤回','撤回-主动撤回','驳回','PCT指定期满']): 
        return '失效'
    if any(k in s for k in ['授权','Granted','Active','维持有效']): 
        return '有效'
    if any(k in s for k in ['实质审查','Pending','Examining','审中','公开']): 
        return '审中'
    return '失效'
df['法律状态映射'] = df['简单法律状态'].apply(map_status)
```

## 二、候选池建立（【关键】第十四节前置排除）

```python
# 【强制】第十四节候选池：排除已终结法律状态
def build_active_pool(df):
    # 排除所有法律状态已终结的专利（与map_status负面状态保持同步）
    exclude_keywords = ['期限届满', '视为撤回', '撤回-主动撤回', '驳回', '避免重复授权', 'PCT指定期满']
    mask = df['简单法律状态'].apply(
        lambda x: not any(kw in str(x) for kw in exclude_keywords)
    )
    df_active = df[mask].copy()
    # 仅保留有效/审中
    df_active = df_active[df_active['法律状态映射'].isin(['有效', '审中'])]
    return df_active

df_active = build_active_pool(df)  # 第十四节唯一数据源
```



## 技术类别映射规范（第八节价值热力图使用）

```python
# 技术类别→关键字映射（用于第八节价值分布热力图归类）
TECH_CATEGORY_MAP = {
    '过滤洗涤干燥': ['过滤', '洗涤', '干燥', '滤布', '滤芯', '底盘', '搅拌', '滤纸', '捕集', '粉尘'],
    '清洗/转运设备': ['清洗', '转运', '胶塞', 'ORABS', '无菌袋', '出料', '封装', '封口', '轧盖', '象鼻子'],
    'MVR蒸发/废水处理': ['蒸发', '废水', 'MVR', '热泵', '精馏', '蒸馏', '除盐', '冷凝', '溶剂回收', '脱水'],
    '锂电材料设备': ['锂电池', '电极材料', '磷酸铁', '碳酸锂', 'DMC', '碳酸二甲酯'],
    '密封/阀门/结构': ['密封', '阀门', '出料阀', '结构', '波纹管', '机械密封', '轴承', '搅拌轴', '升降'],
}

def classify_tech_category(tech_str):
    """将技术主题分类映射到技术类别"""
    if pd.isna(tech_str): return '其他'
    tech_str = str(tech_str)
    for category, keywords in TECH_CATEGORY_MAP.items():
        if any(kw in tech_str for kw in keywords):
            return category
    return '其他'

def classify_title_category(title):
    """将专利标题映射到技术类别（备用）"""
    if pd.isna(title): return '其他'
    title = str(title)
    for category, keywords in TECH_CATEGORY_MAP.items():
        if any(kw in title for kw in keywords):
            return category
    return '其他'
```

## 三、技术类别映射（第八节价值热力图前置步骤）

```python
# 【关键】必须在build_active_pool之后、build_tiers之前执行
# 原因：df_active是df的独立副本（.copy()），df上的新列不会自动同步到df_active

# 1. 对完整df添加技术类别
df['技术类别'] = df['技术主题分类'].apply(classify_tech_category)
# 对无技术主题分类的，使用标题作为备用
df.loc[df['技术类别'] == '其他', '技术类别'] = df.loc[df['技术类别'] == '其他', '标题'].apply(classify_title_category)

# 2. 【强制】对df_active同步添加技术类别（独立副本需显式同步）
df_active['技术类别'] = df_active['技术主题分类'].apply(classify_tech_category)
df_active.loc[df_active['技术类别'] == '其他', '技术类别'] = df_active.loc[df_active['技术类别'] == '其他', '标题'].apply(classify_title_category)

# 3. 可选：对df添加标题分类（备用）
df['标题技术类别'] = df['标题'].apply(classify_title_category)

tech_category_counts = df['技术类别'].value_counts().to_dict()
print(f"技术类别分布: {tech_category_counts}")  # 调试用，确认分布正常
```

**硬检查点**：
| 检查项 | 验证方法 | 失败处理 |
|--------|----------|----------|
| `df['技术类别']`已建立 | `'技术类别' in df.columns` | 重新执行上述映射代码 |
| `df_active['技术类别']`已同步 | `'技术类别' in df_active.columns` | 重新执行df_active映射 |
| 技术类别不为全"其他" | `df['技术类别'].nunique() > 1` | 检查TECH_CATEGORY_MAP关键字是否覆盖专利标题/技术主题 |

---

## 四、全景统计（第七节数据源）

```python
def standardize_patent_type(t):
    """标准化专利类型 — 直接采用用户清单标签+兜底映射"""
    if pd.isna(t): return '其他'
    t = str(t).strip()
    if t in ['发明申请', '发明专利申请', '发明', '发明专利'] or t.endswith('发明申请'): return '发明申请'
    if t in ['授权发明', '发明授权']: return '授权发明'
    if t in ['实用新型', 'Utility Model', 'utility model']: return '实用新型'
    if t in ['外观设计', 'Design', 'design']: return '外观设计'
    return t  # 其他情况直接采用原始标签

def build_panorama(df):
    """构建专利组合全景统计数据"""
    df = df.copy()
    df['专利类型标准化'] = df['专利类型'].apply(standardize_patent_type)
    pub_no = df['公开(公告)号'].astype(str).str.upper()
    return {
        'total': len(df),
        'valid': len(df[df['法律状态映射']=='有效']),
        'pending': len(df[df['法律状态映射']=='审中']),
        'expired': len(df[df['法律状态映射']=='失效']),
        # 专利类型（直接使用用户清单标签+兜底映射）
        'invention_apply': len(df[df['专利类型标准化']=='发明申请']),
        'invention_grant': len(df[df['专利类型标准化']=='授权发明']),
        'utility': len(df[df['专利类型标准化']=='实用新型']),
        'design': len(df[df['专利类型标准化']=='外观设计']),
        # 受理局（中国含港澳台，海外不含港澳台）
        'cn': len(df[pub_no.str.startswith('CN', na=False)]),
        'tw': len(df[pub_no.str.startswith('TW', na=False)]),
        'hk': len(df[pub_no.str.startswith('HK', na=False)]),
        'mo': len(df[pub_no.str.startswith('MO', na=False)]),
        'china_total': len(df[pub_no.str.match(r'^(CN|TW|HK|MO)', na=False)]),
        'overseas': len(df) - len(df[pub_no.str.match(r'^(CN|TW|HK|MO)', na=False)]),
        'pct': len(df[pub_no.str.startswith('WO', na=False)]),
        # 年度趋势
        'yearly_trend': df.groupby('申请年')['申请号'].count().to_dict(),
    }

panorama = build_panorama(df)  # 第七节数据源
```

## 五、价值分层（第八节数据源）

```python
def build_tiers(df_active):
    """构建Tier A/B/C分层 — 仅使用有效/审中专利（排除失效）"""
    df_val = df_active[df_active['专利价值'] != '-'].copy()
    df_val['专利价值_num'] = pd.to_numeric(df_val['专利价值'], errors='coerce')
    df_val = df_val.dropna(subset=['专利价值_num'])
    df_sorted = df_val.sort_values('专利价值_num', ascending=False)
    n = len(df_sorted)
    if n == 0:
        return df_val.iloc[:0], df_val.iloc[:0], df_val.iloc[:0], {
            'tier_a_count': 0, 'tier_a_range': '-',
            'tier_b_count': 0, 'tier_b_range': '-',
            'tier_c_count': 0, 'tier_c_range': '-',
        }
    
    tier_a = df_sorted.iloc[:max(1, int(n*0.2))]
    tier_b = df_sorted.iloc[max(1, int(n*0.2)):max(2, int(n*0.6))]
    tier_c = df_sorted.iloc[max(2, int(n*0.6)):]
    
    return tier_a, tier_b, tier_c, {
        'tier_a_count': len(tier_a), 'tier_a_range': f"{tier_a['专利价值_num'].min():.0f}-{tier_a['专利价值_num'].max():.0f}" if len(tier_a) > 0 else '-',
        'tier_b_count': len(tier_b), 'tier_b_range': f"{tier_b['专利价值_num'].min():.0f}-{tier_b['专利价值_num'].max():.0f}" if len(tier_b) > 0 else '-',
        'tier_c_count': len(tier_c), 'tier_c_range': f"{tier_c['专利价值_num'].min():.0f}-{tier_c['专利价值_num'].max():.0f}" if len(tier_c) > 0 else '-',
    }

tier_a, tier_b, tier_c, tier_meta = build_tiers(df_active)  # 第八节数据源（使用df_active排除失效专利）
```

## 六、发明人分析（第十一节数据源）

```python
def build_inventor_data(df):
    """构建发明人统计数据 — 向量化处理，不截断任何专利"""
    # === 步骤1：展开所有发明人（组合名拆分，不截断）===
    inv_rows = []
    for row in df.itertuples(index=False):
        inv_field = getattr(row, '发明人', None)
        if pd.isna(inv_field): continue
        for inv in str(inv_field).split(' | '):
            inv_clean = inv.strip()
            if inv_clean and inv_clean != '-' and inv_clean != '请求不公布姓名':
                inv_rows.append({
                    '发明人': inv_clean,
                    '申请年': getattr(row, '申请年', None),
                    '技术主题分类': getattr(row, '技术主题分类', ''),
                    '专利价值': getattr(row, '专利价值', 0),
                    '公开号': getattr(row, '公开(公告)号', '')
                })
    df_inv = pd.DataFrame(inv_rows) if inv_rows else pd.DataFrame(columns=['发明人','申请年','技术主题分类','专利价值','公开号'])
    
    # === 步骤2：发明人计数（完整统计）===
    inv_counter = Counter(df_inv['发明人']) if len(df_inv) > 0 else Counter()
    top_15 = inv_counter.most_common(15)
    top_8 = [inv for inv, _ in inv_counter.most_common(8)]
    
    # === 步骤3：发明人×年份矩阵（向量化groupby）===
    years = list(range(2015, 2026))
    inv_year = {inv: {y: 0 for y in years} for inv in top_8}
    if len(df_inv) > 0 and '申请年' in df_inv.columns:
        yr = df_inv[df_inv['发明人'].isin(top_8)].groupby(['发明人', '申请年']).size()
        for (inv, y), cnt in yr.items():
            if inv in inv_year and y in inv_year[inv]:
                inv_year[inv][y] = int(cnt)
    
    # === 步骤4：发明人×技术矩阵（向量化）===
    tech_counter = Counter()
    if len(df_inv) > 0:
        for tech in df_inv['技术主题分类'].dropna():
            for t in str(tech).split('|'):
                t_clean = t.strip()
                if t_clean and t_clean != '-':
                    tech_counter[t_clean] += 1
    top_10_techs = [t for t, _ in tech_counter.most_common(10)]
    
    # === 步骤5：发明人×价值（向量化groupby，不遗漏任何专利）===
    inv_values = []
    if len(df_inv) > 0:
        df_inv['专利价值_num'] = pd.to_numeric(df_inv['专利价值'], errors='coerce').fillna(0)
        val_sum = df_inv.groupby('发明人')['专利价值_num'].sum().to_dict()
        for inv_name, count in top_15:
            inv_values.append({
                'name': inv_name, 
                'count': count, 
                'value': round(val_sum.get(inv_name, 0) / 10000, 1)
            })
    
    return {
        'top_15': top_15,
        'top_8': top_8,
        'top_10_techs': top_10_techs,
        'inv_year': inv_year,
        'inv_values': inv_values,
    }

inventor_data = build_inventor_data(df)  # 第十一节数据源（向量化处理，O(n)复杂度）
```

## 七、持久化与Checkpoint

```python
# 保存关键数据到JSON（会话中断恢复用）
snapshot_path = '/mnt/agents/output/patent_snapshot.json'
snapshot = {
    'panorama': panorama,
    'tier_meta': tier_meta,
    'inventor_summary': {inv: count for inv, count in inventor_data['top_15']},
    'df_shape': {'rows': len(df), 'cols': len(df.columns)},
    'active_pool_size': len(df_active),
}
with open(snapshot_path, 'w') as f:
    json.dump(snapshot, f, ensure_ascii=False, indent=2)

# Checkpoint每5节保存一次
def save_checkpoint(sec_name, html_content, data):
    checkpoint = {
        'completed_sections': sec_name,
        'html_so_far': html_content[-5000:],  # 最后5000字符
        'data_keys': list(data.keys()),
    }
    with open(f'/mnt/agents/output/checkpoint_{sec_name}.json', 'w') as f:
        json.dump(checkpoint, f, ensure_ascii=False)
```

## 八、数据字典组装

```python
def build_data_dict(df, df_active, panorama, tier_a, tier_b, tier_c, tier_meta,
                     inventor_data, company_info, business_info, charts=None):
    """组装最终的data字典，供HTML模板填充"""
    data = {
        # 封面
        'company_en': company_info.get('en_name', ''),
        'company_cn': company_info.get('cn_name', ''),
        'report_date': company_info.get('report_date', ''),
        'data_source': '用户提供专利清单 / 企业官网 / 公开新闻',
        'data_source_hint': 'PatSnap样本数据',
        
        # 各节数据（后续各节分析函数填充）
        'sec1': {}, 'sec2': {}, 'sec3': {}, 'sec4': {}, 'sec5': {},
        'sec6': {}, 'sec7': {}, 'sec8': {}, 'sec9': {}, 'sec10': {},
        'sec11': {}, 'sec12': {}, 'sec13': {}, 'sec14': {}, 'sec15': {},
        'sec16': {}, 'sec17': {}, 'sec18': {}, 'sec19': {}, 'sec20': {},
        'sec21': {},  # 报告综述
        
        # 图表（base64编码，HTML填充阶段直接嵌入<img>标签）
        'charts': charts if charts else {},
        
        # 原始DataFrame（各节分析函数直接使用）
        'df': df,
        'df_active': df_active,
        'panorama': panorama,
        'tier_a': tier_a, 'tier_b': tier_b, 'tier_c': tier_c,
        'tier_meta': tier_meta,
        'inventor_data': inventor_data,
    }
    return data
```

## 九、硬检查点（Data Layer出口）

| 检查项 | 验证方法 | 失败处理 |
|--------|----------|----------|
| `df`非空 | `len(df) > 0` | 报错：专利清单为空 |
| `df_active`已建立 | `len(df_active) >= 0` | 重新执行build_active_pool |
| Tier分层已建立 | `tier_a`/`tier_b`/`tier_c`均为DataFrame | 重新执行build_tiers |
| A/B号未去重 | `len(df) >= 原始行数 * 0.95` | 报错：数据可能被意外去重 |
| snapshot已写入 | `os.path.exists(snapshot_path)` | 重新写入 |

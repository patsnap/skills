#!/usr/bin/env python3
"""
专利数据分析核心脚本
读取专利数据Excel，执行技术分类和统计分析，生成JSON数据供HTML模板使用
"""
import pandas as pd
import numpy as np
import json
import re
from collections import Counter

TECH_KEYWORDS = {
    '纤维制备与增强': ['碳化硅纤维', 'SiC纤维', '纤维制备', '纤维增强', '纤维表面', '纤维涂层', '先驱体', '纺丝', '纤维束', '纤维编织'],
    '编织与预制体': ['编织', '预制体', '预成型', '预浸料', '铺层', '三维编织', '纺织', '纤维垫', '预制件'],
    '基体与致密化': ['基体', '致密化', '孔隙率', 'CVI', '化学气相渗透', 'PIP', '先驱体浸渍', '熔渗', '烧结', 'RMI', '反应熔体', '密度'],
    '界面涂层': ['界面涂层', '界面相', 'BN涂层', 'PyC涂层', 'SiBN', '氮化硼', '热解碳'],
    '环境障涂层': ['环境障', 'EBC', '热障涂层', 'TBC', '可磨耗涂层', '密封涂层', 'CMAS', '抗侵蚀', '抗氧化', '防腐'],
    '叶片设计与制造': ['涡轮叶片', '涡轮导叶', '压气机叶片', '翼型', '叶型', '叶身', '叶尖', '叶根', '榫头', '榫接', '叶冠', '叶盘', '阻尼'],
    '燃烧室设计': ['燃烧室', '火焰筒', '燃烧器', '衬里', '衬套', '喷嘴', '旋流器', '点火', '燃烧'],
    '涡轮环与密封': ['涡轮环', '涡轮罩', 'BOAS', '密封', '刷式密封', '间隙控制', '篦齿'],
    'CMC构件连接': ['连接', '钎焊', '焊接', '螺栓', '紧固', '接头', '固定'],
    '冷却设计': ['冷却', '气膜', '气膜孔', '冲击冷却', '对流冷却', '微细管阵', '冷却通道', '冷却腔', '双层壁'],
    '成型加工': ['成型', '制造', '加工', '3D打印', '增材制造', '切削', '磨削', '超声加工', '激光打孔', '打孔', '开孔'],
    '检测与评估': ['检测', '无损检测', '监测', '测试', '评估', '寿命预测', '蠕变', '疲劳', '失效', '损伤', '裂纹'],
    '仿真与优化': ['仿真', '模拟', '优化', '数值', '有限元', 'CFD', '神经网络', '拓扑优化', '代理模型'],
    '复合材料设计': ['复合材料', '陶瓷基复合材料', 'CMC', 'SiCf/SiC', 'C/SiC', '功能梯度', '分层', '层合'],
    '转子动力学': ['转子', '动力学', '振动', '模态', '叶片频率', '共振', '碰摩', '不平衡'],
    '燃气轮机整机': ['燃气轮机', '航空发动机', '涡轮发动机', '涡扇', '涡轴', '压气机', '涡轮', '发动机性能']
}


def standardize_columns(df):
    """标准化列名映射"""
    mapping = {
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
    for old, new in mapping.items():
        if old in df.columns and new not in df.columns:
            df.rename(columns={old: new}, inplace=True)
    return df


def clean_applicant(name):
    """清理申请人名称"""
    if pd.isna(name):
        return ''
    name = str(name)
    if any(k in name for k in ['雷神', 'Raytheon', 'RTX']): return '雷神科技'
    if any(k in name for k in ['通用电气', 'GE', 'General Electric']): return '通用电气'
    if any(k in name for k in ['罗尔斯', 'Rolls-Royce', '劳斯莱斯']): return '罗尔斯·罗伊斯'
    if any(k in name for k in ['赛峰', 'Safran']): return '赛峰集团'
    if '航发湖南' in name or '动研' in name: return '中国航发动研所'
    if '航发四川' in name or '涡轮' in name: return '中国航发涡轮院'
    if '航发沈阳' in name or '动力' in name: return '中国航发动力所'
    if '航发商用' in name or '商发' in name: return '中国航发商发'
    if '航发北京' in name or '航材' in name: return '中国航发航材院'
    if '西北工业' in name: return '西北工业大学'
    if '北京航空航天' in name: return '北京航空航天大学'
    if '南京航空航天' in name: return '南京航空航天大学'
    if '国防科技' in name: return '国防科技大学'
    if '中科院' in name or '科学院上海' in name: return '中科院上海硅酸盐所'
    if '船舶' in name and '703' in name: return '中船703所'
    return name[:10]


def classify_tech(text):
    """技术分类"""
    categories = []
    for cat, keywords in TECH_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text.lower():
                categories.append(cat)
                break
    return categories if categories else ['其他']


def analyze_patents(patent_excel_path):
    """核心分析函数"""
    df = pd.read_excel(patent_excel_path)
    df = standardize_columns(df)

    # 提取申请年
    df['申请年'] = pd.to_datetime(df['申请日'], errors='coerce').dt.year

    # 简化法律状态
    def simplify_status(s):
        s = str(s)
        if '授权' in s: return '授权'
        if '实质审查' in s: return '实质审查'
        if 'PCT' in s: return 'PCT国际申请'
        if '公开' in s: return '公开'
        return '其他'
    df['主要状态'] = df['法律状态/事件'].apply(simplify_status)

    # 清理申请人
    df['申请人简称'] = df['[标]当前申请(专利权)人'].apply(clean_applicant)

    # 技术分类
    def get_tech_cats(row):
        text = str(row['标题']) + ' ' + str(row.get('Patsnap专利标题', row.get('摘要', '')))
        return classify_tech(text)
    df['技术分类'] = df.apply(get_tech_cats, axis=1)

    # 同族数量
    df['同族数'] = df['简单同族国家/地区'].apply(lambda x: len(str(x).split('|')) if pd.notna(x) else 0)

    # ========== 核心统计 ==========
    total = len(df)
    year_trend = {int(k): int(v) for k, v in df.groupby('申请年').size().items() if k >= 2010}
    status_dist = {k: int(v) for k, v in df['主要状态'].value_counts().items()}
    office_dist = {k: int(v) for k, v in df['受理局'].value_counts().items()}

    all_cats = []
    for cats in df['技术分类']:
        all_cats.extend(cats)
    tech_dist = {k: int(v) for k, v in Counter(all_cats).most_common()}

    applicant_dist = {k: int(v) for k, v in df['申请人简称'].value_counts().head(15).items()}

    # 技术分支年度趋势
    recent_years = [2020, 2021, 2022, 2023, 2024, 2025]
    tech_branches = list(TECH_KEYWORDS.keys())
    tech_year_matrix = {}
    for tech in tech_branches:
        tech_year_matrix[tech] = {}
        for yr in recent_years:
            mask = df['申请年'] == yr
            count = sum(1 for idx in df[mask].index if tech in df.loc[idx, '技术分类'])
            tech_year_matrix[tech][yr] = count

    # 增长率
    tech_growth = {}
    for tech in tech_branches:
        v2020 = tech_year_matrix[tech].get(2020, 0)
        v2024 = tech_year_matrix[tech].get(2024, 0)
        growth = ((v2024 - v2020) / max(v2020, 1)) * 100
        tech_growth[tech] = {'2020': v2020, '2024': v2024, 'growth': round(growth, 1)}

    # 地域趋势
    region_trend = {}
    for office in ['中国', '美国', '欧洲专利局', '法国', '日本']:
        yearly = df[df['受理局'] == office].groupby('申请年').size()
        region_trend[office] = [int(yearly.get(y, 0)) for y in recent_years]

    # 申请人技术布局
    top8_apps = df['申请人简称'].value_counts().head(8).index.tolist()
    applicant_tech = {}
    for app in top8_apps:
        mask = df['申请人简称'] == app
        app_cats = []
        for cats in df[mask]['技术分类']:
            app_cats.extend(cats)
        app_counter = Counter(app_cats)
        applicant_tech[app] = {k: int(v) for k, v in app_counter.most_common(6)}

    # 高被引专利
    high_cite = []
    cite_df = df[df['被引用专利数量'] > 0].sort_values('被引用专利数量', ascending=False).head(10)
    for _, row in cite_df.iterrows():
        high_cite.append({
            'number': str(row['公开(公告)号']),
            'applicant': str(row['申请人简称']),
            'title': str(row['标题'])[:50],
            'cited': int(row['被引用专利数量'])
        })

    # 多同族专利
    multi_family = []
    fam_df = df[df['同族数'] >= 3].sort_values('同族数', ascending=False).head(8)
    for _, row in fam_df.iterrows():
        multi_family.append({
            'number': str(row['公开(公告)号']),
            'applicant': str(row['申请人简称']),
            'title': str(row['标题'])[:50],
            'family_count': int(row['同族数'])
        })

    return {
        'total': total,
        'year_trend': year_trend,
        'status_dist': status_dist,
        'office_dist': office_dist,
        'tech_dist': tech_dist,
        'applicant_dist': applicant_dist,
        'tech_year_matrix': tech_year_matrix,
        'tech_growth': tech_growth,
        'region_trend': region_trend,
        'applicant_tech': applicant_tech,
        'high_cite': high_cite,
        'multi_family': multi_family,
        'peak_year': max(year_trend.items(), key=lambda x: x[1])[0] if year_trend else None,
        'peak_count': max(year_trend.values()) if year_trend else 0,
        'grant_rate': round(status_dist.get('授权', 0) / total * 100, 1) if total else 0,
        'china_share': round(office_dist.get('中国', 0) / total * 100, 1) if total else 0,
        'us_share': round(office_dist.get('美国', 0) / total * 100, 1) if total else 0
    }


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        result = analyze_patents(sys.argv[1])
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Usage: python patent_analyzer.py <patent_excel_path>")

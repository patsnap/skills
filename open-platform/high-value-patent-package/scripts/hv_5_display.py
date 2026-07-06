# -*- coding: utf-8 -*-
"""Stage 5: enrich the SELECTED patents with P021 drawing, P025 AI elements, P041 status."""
import time
from hv_common import api_get, chunks, jload, jdump

def first_para(d):
    if isinstance(d, dict):
        p = d.get('benefit_para') or d.get('tech_problem_para') or d.get('technical_approach_para')
        if isinstance(p, list):
            return ' '.join(str(x) for x in p if x)
        if p:
            return str(p)
    return None

def run():
    s = jload('scored.json')
    sel = s['rows'][:s['selected_count']]
    disp = {}   # pid -> fields
    for r in sel:
        disp[r['patent_id']] = {'drawing': '未获取', 'patsnap_title': '未获取',
            'tech_problem': '未获取', 'tech_approach': '未获取', 'benefit': '未获取',
            'legal_status': '未获取', 'gaps': []}

    BATCH = 15
    # ---- P021 abstract image ----
    for batch in chunks(sel, BATCH):
        ids = ','.join(r['patent_id'] for r in batch)
        pns = ','.join(r['pn'] for r in batch)
        d = api_get('basic-patent-data/abstract-image', {'patent_id': ids, 'patent_number': pns})
        if isinstance(d, list):
            for rec in d:
                pid = rec.get('patent_id'); ad = rec.get('abstract_drawing') or {}
                path = ad.get('path') if isinstance(ad, dict) else None
                if pid in disp:
                    disp[pid]['drawing'] = path if path else '无可用摘要附图'
    print('P021 done')

    # ---- P025 AI three elements ----
    for batch in chunks(sel, BATCH):
        ids = ','.join(r['patent_id'] for r in batch)
        pns = ','.join(r['pn'] for r in batch)
        d = api_get('high-value-data/tech-problem-and-benefit-summary',
                    {'lang': 'cn', 'patent_id': ids, 'patent_number': pns})
        if isinstance(d, list):
            for rec in d:
                pid = rec.get('patent_id')
                if pid not in disp:
                    continue
                disp[pid]['patsnap_title'] = rec.get('patsnap_title') or '未获取'
                disp[pid]['tech_problem'] = first_para(rec.get('tech_problem_summary')) or '未获取'
                disp[pid]['tech_approach'] = first_para(rec.get('technical_approach_summary')) or '未获取'
                disp[pid]['benefit'] = first_para(rec.get('benefit_summary')) or '未获取'
    print('P025 done')

    # ---- P041 legal status (single id per call) ----
    for r in sel:
        d = api_get('basic-patent-data/simple-legal-status',
                    {'patent_id': r['patent_id'], 'patent_number': r['pn']})
        if isinstance(d, list) and d:
            sls = d[0].get('simple_legal_status')
            if isinstance(sls, list):
                disp[r['patent_id']]['legal_status'] = '、'.join(sls) if sls else '未获取'
            elif sls:
                disp[r['patent_id']]['legal_status'] = str(sls)
    print('P041 done')

    # ---- record gaps ----
    for r in sel:
        g = disp[r['patent_id']]
        gaps = []
        if r['cited_missing']:
            gaps.append('简单同族被引数据未获取')
        for k, lbl in [('patsnap_title','Patsnap标题'),('tech_problem','技术问题'),
                       ('tech_approach','技术手段'),('benefit','技术功效'),('legal_status','法律状态')]:
            if g[k] == '未获取':
                gaps.append(lbl + '未获取')
        if g['drawing'] in ('未获取',):
            gaps.append('摘要附图未获取')
        g['gaps'] = gaps

    jdump(disp, 'enrich_display.json')
    print('selected enriched:', len(disp))

if __name__ == '__main__':
    run()

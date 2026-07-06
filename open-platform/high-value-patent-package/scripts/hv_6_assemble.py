# -*- coding: utf-8 -*-
"""Stage 6a: assemble final selected records + rationale + percentile, write trace JSON."""
import bisect
from urllib.parse import quote
from hv_common import jload, jdump

# 智慧芽专利详情页（最简永久形式，无分享签名，需登录智慧芽后访问）
VIEW_TMPL = 'https://analytics.zhihuiya.com/patent-view/abst?patentId={pid}&q={pn}'

def view_url(pid, pn):
    if not pid:
        return ''
    return VIEW_TMPL.format(pid=pid, pn=quote(pn or ''))

def pctile_label(sorted_vals, v):
    n = len(sorted_vals)
    le = bisect.bisect_right(sorted_vals, v)
    return round(le / n * 100)

def run():
    s = jload('scored.json')
    rows = s['rows']
    disp = jload('enrich_display.json')
    sel = rows[:s['selected_count']]

    cited_vals = sorted(r['cited_by_simple_family'] for r in rows)
    fam_vals = sorted(r['simple_family_count'] for r in rows)

    final = []
    for r in sel:
        pid = r['patent_id']
        d = disp.get(pid, {})
        p_cited = pctile_label(cited_vals, r['cited_by_simple_family'])
        p_fam = pctile_label(fam_vals, r['simple_family_count'])
        # rationale
        parts = []
        if r['cited_missing']:
            parts.append('简单同族被引专利数量未获取')
        else:
            parts.append(f"简单同族被引专利数量{r['cited_by_simple_family']}件(候选集P{p_cited})")
        parts.append(f"简单同族专利数量{r['simple_family_count']}件(候选集P{p_fam})")
        if r['core_inventor']:
            parts.append('命中核心发明人：' + '、'.join(r['matched_inventors']))
        else:
            parts.append('未命中核心发明人')
        ev = r['legal_events']
        if ev:
            evtxt = '、'.join(f"{k}{('×'+str(v)) if v>1 else ''}" for k, v in ev.items())
            parts.append('存在' + evtxt + '法律事件')
        else:
            parts.append('无检索到的法律事件')
        rationale = '；'.join(parts) + '。'

        final.append({
            'rank': r['rank'], 'score': r['score'],
            'rationale': rationale,
            'pn': r['pn'], 'title': r['title'],
            'patent_id': r['patent_id'],
            'view_url': view_url(r['patent_id'], r['pn']),
            'drawing': d.get('drawing', '未获取'),
            'current_assignee': r['current_assignee'],
            'legal_status': d.get('legal_status', '未获取'),
            'patsnap_title': d.get('patsnap_title', '未获取'),
            'tech_problem': d.get('tech_problem', '未获取'),
            'tech_approach': d.get('tech_approach', '未获取'),
            'benefit': d.get('benefit', '未获取'),
            'cited_by_simple_family': r['cited_by_simple_family'],
            'cited_missing': r['cited_missing'],
            'simple_family_count': r['simple_family_count'],
            'core_inventor': r['core_inventor'],
            'matched_inventors': r['matched_inventors'],
            'legal_events': ev,
            'inventor': r['inventor'],
            'authority': r['authority'], 'apdt': r['apdt'], 'pbdt': r['pbdt'],
            's_cited': r['s_cited'], 's_fam': r['s_fam'],
            's_inv': r['s_inv'], 's_legal': r['s_legal'],
            'gaps': d.get('gaps', []),
        })

    meta = {
        'candidate_count': s['candidate_count'],
        'selected_count': s['selected_count'],
        'sel_max_15pct': s['sel_max_15pct'],
        'ratio': s['ratio'],
        'top5_inventors': s['top5_inventors'],
    }
    jdump({'meta': meta, 'selected': final}, 'final_records.json')
    # full trace incl. all candidate scores
    jdump({'meta': meta, 'all_candidates_scored': rows, 'selected': final},
          '高价值专利包筛选数据.json')
    print('assembled', len(final), 'records; trace written')

if __name__ == '__main__':
    run()

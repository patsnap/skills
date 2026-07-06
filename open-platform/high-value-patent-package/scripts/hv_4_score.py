# -*- coding: utf-8 -*-
"""Stage 4: core inventors, scoring 30/30/20/20, ranking, selection."""
import re, math
from hv_common import jload, jdump

# NOTE: PatSnap inventor format is "LASTNAME, FIRSTNAME|LASTNAME, FIRSTNAME".
# The comma is the surname/given-name separator *inside* one inventor name, and
# "|" is the delimiter *between* inventors. The skill's generic rule also lists
# comma as a separator, but applying it here fragments names (e.g. splits
# "TANNER, CHRISTOPHER RICHARD" into two tokens). We therefore split only on the
# true inventor delimiters; this deviation is documented in the report.
SPLIT = re.compile(r'[|;；\n\r]+')

def split_inv(s):
    if not s:
        return []
    return [x.strip() for x in SPLIT.split(s) if x.strip()]

def percentile_rank(sorted_vals, v):
    # fraction of values <= v  (>=10 candidates); ties share rank
    import bisect
    # count of values strictly less than v + 0.5*equal -> use <= for "position"
    n = len(sorted_vals)
    if n == 0:
        return 0.0
    le = bisect.bisect_right(sorted_vals, v)
    return le / n

def run():
    cand = jload('cand_raw.json')['candidates']
    num = jload('enrich_num.json')
    fam = num['family']; cit = num['cited']
    legal = jload('enrich_legal.json')

    # ---- core inventors ----
    inv_count = {}
    for c in cand:
        for nm in set(split_inv(c.get('inventor', ''))):
            inv_count[nm] = inv_count.get(nm, 0) + 1
    ranked_inv = sorted(inv_count.items(), key=lambda kv: (-kv[1], kv[0]))
    top5 = [nm for nm, _ in ranked_inv[:5]]
    top5set = set(top5)

    # ---- numeric vectors ----
    cited_vals = sorted(int(cit.get(c['patent_id'], 0) or 0) for c in cand)
    fam_vals = sorted(int(fam.get(c['patent_id'], 0) or 0) for c in cand)
    n = len(cand)
    big = n >= 10

    rows = []
    for c in cand:
        pid = c['patent_id']
        cb = int(cit.get(pid, 0) or 0)
        fc = int(fam.get(pid, 0) or 0)
        cited_missing = pid not in cit
        # numeric scores
        s_cited = percentile_rank(cited_vals, cb) * 30 if big else (15 if cb else 0)
        s_fam = percentile_rank(fam_vals, fc) * 30 if big else (15 if fc else 0)
        # core inventor
        invs = split_inv(c.get('inventor', ''))
        matched = [x for x in invs if x in top5set]
        s_inv = 20 if matched else 0
        # legal
        ev = legal.get(pid, {}) or {}
        s_legal = 20 if ev else 0
        score = round(s_cited + s_fam + s_inv + s_legal, 2)
        rows.append({
            'patent_id': pid, 'pn': c['pn'], 'title': c.get('title'),
            'current_assignee': c.get('current_assignee') or c.get('original_assignee'),
            'inventor': c.get('inventor'), 'apdt': c.get('apdt'), 'pbdt': c.get('pbdt'),
            'authority': c.get('authority'),
            'cited_by_simple_family': cb, 'cited_missing': cited_missing,
            'simple_family_count': fc,
            'core_inventor': bool(matched), 'matched_inventors': matched,
            'legal_events': ev,
            's_cited': round(s_cited, 2), 's_fam': round(s_fam, 2),
            's_inv': s_inv, 's_legal': s_legal, 'score': score,
        })

    # ---- ranking with tie-breaks ----
    def apdt_key(r):
        try: return int(r['apdt'])
        except: return 99999999
    rows.sort(key=lambda r: (
        -r['score'], -r['cited_by_simple_family'], -r['simple_family_count'],
        0 if r['legal_events'] else 1, 0 if r['core_inventor'] else 1,
        -len(r['legal_events']), apdt_key(r), r['pn']))
    for i, r in enumerate(rows, 1):
        r['rank'] = i

    sel_count = math.ceil(n * 0.10)
    sel_max = math.ceil(n * 0.15)
    selected = rows[:sel_count]

    jdump({
        'candidate_count': n,
        'top5_inventors': [{'name': nm, 'count': inv_count[nm]} for nm in top5],
        'all_inventor_ranking': ranked_inv[:20],
        'selected_count': sel_count, 'sel_max_15pct': sel_max,
        'ratio': round(sel_count / n * 100, 2),
        'rows': rows,
    }, 'scored.json')
    print('candidates', n, 'top5', top5)
    print('selected', sel_count, 'ratio', round(sel_count/n*100,2), '% (15% cap=', sel_max, ')')
    print('selected score range', selected[0]['score'], '->', selected[-1]['score'])

if __name__ == '__main__':
    run()

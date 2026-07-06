# -*- coding: utf-8 -*-
"""Stage 2: enrich ALL candidates with P014 family size and P015 forward citations."""
import json
from hv_common import api_get, chunks, jload, jdump

def get_count(d, pid, pn):
    # d is list of records; match by patent_id/pn
    return d

def run():
    cand = jload('cand_raw.json')['candidates']
    fam = {}   # patent_id -> simple_family_count
    cit = {}   # patent_id -> cited_by_simple_family
    cit_detail = {}
    BATCH = 20
    n = len(cand)
    for bi, batch in enumerate(chunks(cand, BATCH)):
        ids = ','.join(c['patent_id'] for c in batch)
        pns = ','.join(c['pn'] for c in batch)
        # P014
        d14 = api_get('basic-patent-data/patent-family', {'patent_id': ids, 'patent_number': pns})
        if isinstance(d14, list):
            for rec in d14:
                pid = rec.get('patent_id')
                pf = rec.get('patent_family', {})
                sf = pf.get('simple_family', []) if isinstance(pf, dict) else []
                if pid:
                    fam[pid] = len(sf)
        # P015
        d15 = api_get('basic-patent-data/forward-citation/v3', {'patent_id': ids, 'patent_number': pns})
        if isinstance(d15, list):
            for rec in d15:
                pid = rec.get('patent_id')
                pc = rec.get('patent_cited', {}) or {}
                cb = pc.get('cited_by_simple_family')
                if pid:
                    cit[pid] = cb if isinstance(cb, int) else (int(cb) if str(cb).isdigit() else 0)
                    cit_detail[pid] = {k: pc.get(k) for k in
                        ('cited_by_simple_family','cited_by_inpadoc_family','cited_by_patsnap_family','cited_by_3y','cited_by_5y')}
        print('batch', bi+1, 'done', (bi*BATCH+len(batch)), '/', n)
    jdump({'family': fam, 'cited': cit, 'cited_detail': cit_detail}, 'enrich_num.json')
    print('family records', len(fam), 'cited records', len(cit))

if __name__ == '__main__':
    run()

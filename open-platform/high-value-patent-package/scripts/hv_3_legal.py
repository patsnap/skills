# -*- coding: utf-8 -*-
"""Stage 3: legal events for ALL candidates. P034/P027/P028/P029 batched (CSV)."""
import json
from hv_common import api_get, chunks, jload, jdump

ENDPOINTS = {
    '诉讼': ('high-value-data/litigation', 'patent_litigation_data'),
    '无效/复审': ('advanced-patent-data/re-examination-and-invalidation', 'patent_reexam_invalid_data'),
    '许可': ('advanced-patent-data/license-data', 'patent_license_data'),
    '权利转移': ('advanced-patent-data/transfer-data', 'patent_transfer_data'),
}

def run():
    cand = jload('cand_raw.json')['candidates']
    # events[pid] = {category: count}
    events = {c['patent_id']: {} for c in cand}
    BATCH = 20
    n = len(cand)
    for cat, (path, field) in ENDPOINTS.items():
        hits = 0
        for bi, batch in enumerate(chunks(cand, BATCH)):
            ids = ','.join(c['patent_id'] for c in batch)
            pns = ','.join(c['pn'] for c in batch)
            d = api_get(path, {'patent_id': ids, 'patent_number': pns})
            if isinstance(d, list):
                for rec in d:
                    pid = rec.get('patent_id')
                    arr = rec.get(field) or []
                    if pid and isinstance(arr, list) and len(arr) > 0:
                        events.setdefault(pid, {})[cat] = len(arr)
                        hits += 1
        print(cat, 'patents-with-event', hits)
    jdump(events, 'enrich_legal.json')
    tot = sum(1 for v in events.values() if v)
    print('candidates with >=1 legal event:', tot)

if __name__ == '__main__':
    run()

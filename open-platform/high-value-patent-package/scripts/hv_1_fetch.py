# -*- coding: utf-8 -*-
"""Stage 1: retrieve all candidates via P002, paging by 500."""
import json, requests
from hv_common import hjson, load_query, BASE

QUERY = load_query()


def fetch_all():
    url = BASE + '/search/patent/query-search-patent/v2'
    out = []
    offset = 0
    total = None
    while True:
        body = {'sort': [{'field': 'SCORE', 'order': 'DESC'}],
                'limit': 500, 'offset': offset, 'query_text': QUERY}
        r = requests.post(url, headers=hjson(), data=json.dumps(body), timeout=120)
        j = r.json()
        d = j['data']
        total = d['total_search_result_count']
        res = d.get('results', [])
        out.extend(res)
        offset += len(res)
        print('fetched', len(out), '/', total)
        if offset >= total or not res:
            break
    return out, total

if __name__ == '__main__':
    rows, total = fetch_all()
    # dedupe by patent_id
    seen = {}
    for r in rows:
        seen[r['patent_id']] = r
    cand = list(seen.values())
    json.dump({'total_search_result_count': total, 'candidates': cand},
              open('cand_raw.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('unique candidates', len(cand), 'total reported', total)

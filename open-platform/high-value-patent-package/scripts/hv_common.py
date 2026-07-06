# -*- coding: utf-8 -*-
"""Shared helpers for the high-value patent screening reference pipeline.

API key resolution order:
  1. Environment variable ZHIHUIYA_API_KEY (recommended).
  2. A key file whose path is given by env var ZHIHUIYA_API_KEY_FILE.
  3. A local file named 'api_key.txt' in the working directory.
The key is never written into any report artifact.

Search query resolution order:
  1. Environment variable HVP_QUERY.
  2. A local file named 'query.txt' in the working directory.
"""
import os
import json
import time
import requests

BASE = 'https://connect.zhihuiya.com'
_KEY = None


def key():
    global _KEY
    if _KEY is not None:
        return _KEY
    k = os.environ.get('ZHIHUIYA_API_KEY')
    if not k:
        path = os.environ.get('ZHIHUIYA_API_KEY_FILE', 'api_key.txt')
        if os.path.exists(path):
            k = open(path, encoding='utf-8').read().strip()
    if not k:
        raise RuntimeError(
            'No API key. Set ZHIHUIYA_API_KEY, or ZHIHUIYA_API_KEY_FILE, '
            'or place the key in api_key.txt.')
    _KEY = k
    return _KEY


def load_query():
    q = os.environ.get('HVP_QUERY')
    if q:
        return q.strip()
    if os.path.exists('query.txt'):
        return open('query.txt', encoding='utf-8').read().strip()
    raise RuntimeError('No query. Set HVP_QUERY or create query.txt.')


def hjson():
    return {'Authorization': 'Bearer ' + key(), 'Content-Type': 'application/json'}


def hget():
    return {'Authorization': 'Bearer ' + key()}


def api_get(path, params, tries=4):
    url = BASE + '/' + path
    for i in range(tries):
        try:
            r = requests.get(url, headers=hget(), params=params, timeout=90)
            if r.status_code == 200:
                j = r.json()
                if j.get('status'):
                    return j.get('data')
            if r.status_code in (429, 500, 502, 503):
                time.sleep(2 + i * 2)
                continue
            return None
        except Exception:
            time.sleep(2 + i * 2)
    return None


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def jload(fn):
    return json.load(open(fn, encoding='utf-8'))


def jdump(obj, fn):
    json.dump(obj, open(fn, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

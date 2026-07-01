#!/usr/bin/env python3
"""
P002 - 按申请人检索专利（合并同族）
接口: POST https://connect.zhihuiya.com/search/patent/query-search-patent/v2
"""

import os
import sys
import json
import argparse
import requests

API_URL = "https://connect.zhihuiya.com/search/patent/query-search-patent/v2"
COLLAPSE_ORDER_AUTHORITY = ["CN", "US", "EP", "WO", "JP", "KR", "DE", "GB", "FR"]


def p002_search(applicant_name: str, token: str, page: int = 1, page_size: int = 10) -> dict:
    """按申请人名称检索专利，按 APNO 合并同族去重。"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "query_text": f"ANCS:({applicant_name})",
        "collapse_by": "PBD",
        "collapse_type": "APNO",
        "collapse_order": "LATEST",
        "collapse_order_authority": COLLAPSE_ORDER_AUTHORITY,
        "page": page,
        "page_size": page_size
    }
    resp = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if not data.get("status"):
        raise RuntimeError(f"API错误: error_code={data.get('error_code')}, msg={data.get('msg')}")
    result = data.get("data", {})
    patents = result.get("patent_list", [])
    return {
        "total_count": result.get("total_search_result_count", 0),
        "page": page,
        "page_size": page_size,
        "patent_list": [
            {
                "patent_id": p.get("patent_id", ""),
                "title": p.get("title", ""),
                "application_date": p.get("application_date", ""),
                "original_assignee": p.get("original_assignee", "")
            }
            for p in patents
        ]
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="P002 按申请人检索专利")
    parser.add_argument("--applicant", required=True, help="申请人名称")
    parser.add_argument("--token", default=os.environ.get("ZHIHUIYA_API_TOKEN"), help="API Token")
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--page-size", type=int, default=10)
    args = parser.parse_args()
    if not args.token:
        print("错误：请通过 --token 或环境变量 ZHIHUIYA_API_TOKEN 提供 Token", file=sys.stderr)
        sys.exit(1)
    result = p002_search(args.applicant, args.token, args.page, args.page_size)
    print(json.dumps(result, ensure_ascii=False, indent=2))

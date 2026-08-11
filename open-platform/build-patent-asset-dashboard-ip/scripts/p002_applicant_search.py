#!/usr/bin/env python3
"""P002 applicant patent search with application-number collapsing.

Endpoint: POST https://connect.patsnap.com/search/patent/query-search-patent/v2
"""

import os
import sys
import json
import argparse
import requests

API_URL = "https://connect.patsnap.com/search/patent/query-search-patent/v2"


def p002_search(applicant_name: str, api_key: str, page: int = 1, page_size: int = 10) -> dict:
    """Search by normalized current assignee and collapse by application number."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "query_text": f"ANCS:({applicant_name})",
        "collapse_by": "PBD",
        "collapse_type": "APNO",
        "collapse_order": "LATEST",
        "page": page,
        "page_size": page_size
    }
    resp = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if not data.get("status"):
        raise RuntimeError(
            f"PatSnap API error: error_code={data.get('error_code')}, "
            f"message={data.get('error_msg') or data.get('msg')}"
        )
    result = data.get("data", {})
    patents = result.get("results", [])
    return {
        "total_count": result.get("total_search_result_count", 0),
        "page": page,
        "page_size": page_size,
        "results": [
            {
                "patent_id": p.get("patent_id", ""),
                "title": p.get("title", ""),
                "application_date": p.get("apdt", p.get("application_date", "")),
                "original_assignee": p.get("original_assignee", "")
            }
            for p in patents
        ]
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="P002 patent search by current assignee")
    parser.add_argument("--applicant", required=True, help="Applicant or assignee name")
    parser.add_argument(
        "--api-key",
        default=os.environ.get("PATSNAP_API_KEY"),
        help="PatSnap Open Platform API key; defaults to PATSNAP_API_KEY",
    )
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--page-size", type=int, default=10)
    args = parser.parse_args()
    if not args.api_key:
        print(
            "Error: provide --api-key or set the PATSNAP_API_KEY environment variable.",
            file=sys.stderr,
        )
        sys.exit(1)
    result = p002_search(args.applicant, args.api_key, args.page, args.page_size)
    print(json.dumps(result, ensure_ascii=True, indent=2))

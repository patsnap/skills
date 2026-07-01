"""litigation-risk-monitor 烟囱测试（不联网）。

验证 render_report.py 能基于 fixture 数据渲染出非空 HTML 骨架。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_SCRIPTS = _HERE.parent
sys.path.insert(0, str(_SCRIPTS))

from render_report import render  # noqa: E402

FIXTURE = {
    "generated_at": "2026-01-01 00:00Z",
    "overview": {
        "assignees": ["ACME Corp"],
        "assignee_count": 1,
        "litigated_count": 2,
        "family_count": 8,
        "case_count": 1,
        "family_scope": "inpadoc",
        "inventor_lookback_years": 3,
    },
    "family_basic": {
        "geo": [{"jurisdiction": "US", "count": 5, "scope_note": "INPADOC 同族"}],
        "ipc": [{"code": "H04W", "count": 4}],
        "legal": [{"status": "active", "count": 6}],
    },
    "cases": [
        {
            "title": "ACME v. Beta",
            "plaintiff": "ACME Corp",
            "defendant": "Beta Inc",
            "docket": "N.D. Cal. 24-cv-00001",
            "patents": ["US1234567"],
            "issue": "infringement",
            "defense": "invalidity",
            "status": "pending",
            "timeline": "2024-03 起诉",
            "sources": ["[S1] patsnap legal", "[S2] web.search"],
        }
    ],
    "inventors": [
        {
            "name": "Alice Zhang",
            "recent_count": 12,
            "top_ipc": ["H04W", "G06F"],
            "assignee_change": "无",
            "note": "持续布局",
        }
    ],
    "conclusions": {
        "geographic_risk": "美国为高风险区。",
        "litigation_alert": "在审案件需关注无效抗辩进展。",
        "trend_forecast": "近 3 年无线技术布局持续。",
    },
    "sources": [
        {"id": "S1", "label": "Patsnap legal", "ref": "patent.fetch module=legal"},
        {"id": "S2", "label": "web.search", "ref": "https://example.com/news"},
    ],
}


def main() -> int:
    html = render(FIXTURE, lang="zh")
    assert "<html" in html and "涉诉专利风险监测报告" in html, "HTML 骨架渲染失败"
    assert "ACME v. Beta" in html, "case 卡片未渲染"
    assert "Alice Zhang" in html, "inventor 行未渲染"
    print(f"[smoke] OK, html_len={len(html)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

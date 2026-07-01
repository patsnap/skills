"""litigation-risk-monitor 编排主控（v2 数据结构）。

v2 新增字段说明：
  litigated_patents[]  — 主要涉诉专利详情列表，供 render_report.py 第3章卡片渲染
    .pn                  专利公开号
    .url                 智慧芽链接
    .title               专利标题
    .apply_date          申请日
    .pub_date            公开日
    .legal_status        简单法律状态
    .risk_type           风险类型: 'high'=被诉仍在审 / 'medium'=已判决或上诉中 / 'defense'=防御/反诉
    .abstract_image_b64  摘要附图 Base64（优先，离线可用）
    .abstract_image_url  摘要附图 URL（fallback，需网络）
    .tech_problem        技术问题
    .tech_means          技术手段
    .tech_effect         技术效果
    .confirm_points      需要确认的点
    .claims              权利要求全文
    .family_members[]    INPADOC 同族专利列表
      .pn                同族公开号
      .url               智慧芽链接
      .jurisdiction      受理局（如 CN/US/EP/DE）
      .legal_status      简单法律状态（active/inactive/pending 或中文）
      .apply_date        申请日

摘要附图获取方式（orchestrator/Agent 执行顺序）：
  1. 调用 mcp_patsnap-infringement__abstract_image(patent_number=pn) 获取带签名 URL
  2. 用 requests/httpx 下载图片字节，转 base64 → abstract_image_b64
  3. 若下载失败，退后存 abstract_image_url（签名 URL 约1小时有效）
  4. 若 API 无附图数据，两字段均留空（渲染侧显示"暂无摘要附图"）
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from config import (
    DEFAULT_FAMILY_SCOPE,
    DEFAULT_INVENTOR_LOOKBACK_YEARS,
    DEFAULT_MAX_LITIGATED_PER_ASSIGNEE,
    DEFAULT_REPORT_LANG,
    DEFAULT_TOP_INVENTORS,
)

# ── 单件涉诉专利模板 ──────────────────────────────────────
LITIGATED_PATENT_TEMPLATE = {
    "pn": "",
    "url": "",
    "title": "",
    "apply_date": "",
    "pub_date": "",
    "legal_status": "",
    # risk_type: 'high' | 'medium' | 'defense'
    # high    = 被诉仍在审（红色背景）
    # medium  = 已判决或上诉中（橙色背景）
    # defense = 中创新航主动持有的反诉/防御资产（蓝色背景）
    "risk_type": "high",
    # 摘要附图（二选一，优先 b64）
    "abstract_image_b64": "",   # data:image/png;base64,... 不含前缀
    "abstract_image_url": "",   # 带签名的完整 URL（fallback）
    # 技术三要素
    "tech_problem": "",
    "tech_means": "",
    "tech_effect": "",
    # 需要确认的点
    "confirm_points": "",
    # 权利要求全文（弹窗展示）
    "claims": "",
    # INPADOC 同族专利
    # 结构：[
    #   {
    #     "pn": "EP3512003B1",
    #     "url": "https://eureka.zhihuiya.com/...",
    #     "jurisdiction": "EP",
    #     "legal_status": "active",   # 或 "inactive" / "pending" / 中文描述
    #     "apply_date": "2018-01-15"
    #   }
    # ]
    "family_members": [],
}

REPORT_DATA_TEMPLATE = {
    "generated_at": "",
    "overview": {
        "assignees": [],
        "assignee_count": 0,
        "litigated_count": 0,
        "family_count": 0,
        "case_count": 0,
        "family_scope": DEFAULT_FAMILY_SCOPE,
        "inventor_lookback_years": DEFAULT_INVENTOR_LOOKBACK_YEARS,
        "assignee_patent_map": [],
    },
    "family_basic": {
        "geo": [],
        "ipc": [],
        "legal_detail": [],
        "geo_analysis": "",
        "claim_comparison": [],
    },
    # v2 新增：主要涉诉专利详情（含附图+同族）
    "litigated_patents": [],
    "cases": [],
    "inventors": [],
    "conclusions": {
        "geographic_risk": "",
        "geo_litigation_risk": [],
        "litigation_alert": "",
        "litigation_alert_summary": "",
        "trend_forecast": "",
    },
    "sources": [],
}


def build_skeleton(assignees: list[str], **kw) -> dict:
    data = json.loads(json.dumps(REPORT_DATA_TEMPLATE))
    data["overview"]["assignees"] = assignees
    data["overview"]["assignee_count"] = len(assignees)
    data["overview"]["family_scope"] = kw.get("family_scope", DEFAULT_FAMILY_SCOPE)
    data["overview"]["inventor_lookback_years"] = kw.get(
        "inventor_lookback_years", DEFAULT_INVENTOR_LOOKBACK_YEARS
    )
    return data


def make_litigated_patent(**kw) -> dict:
    """创建单件涉诉专利记录，覆盖默认模板字段。"""
    rec = json.loads(json.dumps(LITIGATED_PATENT_TEMPLATE))
    rec.update(kw)
    return rec


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--assignees", required=True, help="申请人名单，逗号分隔")
    p.add_argument("--out", required=True, help="输出 report_data.json 路径")
    p.add_argument("--family-scope", default=DEFAULT_FAMILY_SCOPE)
    p.add_argument("--inventor-lookback-years", type=int, default=DEFAULT_INVENTOR_LOOKBACK_YEARS)
    p.add_argument("--max-litigated", type=int, default=DEFAULT_MAX_LITIGATED_PER_ASSIGNEE)
    p.add_argument("--top-inventors", type=int, default=DEFAULT_TOP_INVENTORS)
    a = p.parse_args(argv)

    assignees = [s.strip() for s in a.assignees.split(",") if s.strip()]
    if not assignees:
        print("[orchestrator] 申请人名单为空", file=sys.stderr)
        return 2

    data = build_skeleton(
        assignees,
        family_scope=a.family_scope,
        inventor_lookback_years=a.inventor_lookback_years,
    )
    out_path = Path(a.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        f"[orchestrator] v2 skeleton written: {out_path}\n"
        f"  assignees={assignees}\n"
        f"  family_scope={a.family_scope}\n"
        f"  inventor_lookback={a.inventor_lookback_years}y\n"
        f"  新增字段：litigated_patents[].abstract_image_b64/url, risk_type, family_members[]"
    )
    print(
        "[orchestrator] 注意：真实数据收集由 Agent 通过 patent.search / patent.fetch / "
        "mcp_patsnap-infringement__abstract_image / web.search 完成后填充本 JSON。"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

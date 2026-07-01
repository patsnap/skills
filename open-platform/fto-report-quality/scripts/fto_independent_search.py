"""
fto_independent_search.py  —  fto-review v7.0 内置独立检索模块

功能：
  1. 语义轨道检索（semantic）
  2. 关键词轨道检索（keyword + filter，含地域过滤）
  3. IPC 分类号自动提取（从关键词检索结果聚合 top IPC）
  4. 申请人扩展检索（从结果中提取主要申请人，再按申请人专项检索）
  5. Chapman 双样本召回率估算
  6. 与原报告专利池比对，输出遗漏专利清单
  7. 所有结果写入 JSON，供 generate_report.py 消费

用法：
  python fto_independent_search.py <input_json> <output_json> [output_dir]

  input_json 字段：
    product_description  : 产品/技术描述（必填）
    target_market        : 目标市场（可选，默认 CN）
    original_patents     : 原报告专利列表，每项含 patent_no（可选）
    topk_semantic        : 语义检索返回数（默认 50）
    topk_keyword         : 关键词检索返回数（默认 50）
    topk_assignee        : 申请人扩展检索返回数（默认 30）
    jurisdiction         : 地域过滤列表（默认 ["CN"]）

注意：本脚本通过 MCP patsnap_search 工具检索，需在 Eureka 环境中由 Agent 调用。
单独运行时若无 MCP 注入则输出空结果骨架供测试。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

# ── 召回率估算 ────────────────────────────────────────────────────────────────

def chapman_estimate(n_a: int, n_b: int, n_c: int) -> dict[str, Any]:
    """
    Chapman 双样本估算。
    n_a: 原报告专利池大小
    n_b: 独立检索专利池大小
    n_c: 重叠数量
    返回 dict 含 estimated_total, recall_a, recall_b, rating
    """
    if n_c == 0 and (n_a == 0 or n_b == 0):
        return {
            "estimated_total": None,
            "recall_a": None,
            "recall_b": None,
            "rating": "数据不足，无法估算",
            "note": "重叠数为0且至少一个专利池为空，Chapman估算不适用。",
        }
    n_hat = ((n_a + 1) * (n_b + 1)) / (n_c + 1) - 1
    n_hat = max(n_hat, max(n_a, n_b))  # 不低于较大池
    r_a = n_a / n_hat if n_hat > 0 else 0
    r_b = n_b / n_hat if n_hat > 0 else 0

    if r_a >= 0.85:
        rating = "充分 ✅"
    elif r_a >= 0.70:
        rating = "偏低 ⚠️"
    else:
        rating = "严重不足 ❌"

    return {
        "estimated_total": round(n_hat),
        "recall_a": round(r_a * 100, 1),
        "recall_b": round(r_b * 100, 1),
        "rating": rating,
        "note": (
            f"Chapman双样本估算：原报告池 n_A={n_a}，独立检索池 n_B={n_b}，"
            f"重叠 n_C={n_c}，估算总量 N̂={round(n_hat)}，"
            f"原报告召回率 R_A={round(r_a*100,1)}%，独立检索召回率 R_B={round(r_b*100,1)}%。"
        ),
    }


# ── 比对遗漏 ─────────────────────────────────────────────────────────────────

def find_omissions(
    original_nos: set[str],
    independent_results: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    从独立检索结果中找出原报告未覆盖的专利。
    original_nos: 原报告专利号集合（已标准化大写去空格）
    independent_results: 独立检索返回的专利列表
    """
    omissions = []
    for patent in independent_results:
        pno = str(patent.get("patent_number") or patent.get("no") or "").strip().upper()
        if pno and pno not in original_nos:
            omissions.append({
                "patent_no": pno,
                "title": patent.get("title", "-"),
                "assignee": patent.get("assignee", "-"),
                "status": patent.get("legal_status", "-"),
                "source": patent.get("_source_track", "独立检索"),
                "url": patent.get("url", ""),
                "tag": "[独立验证发现]",
            })
    return omissions


# ── IPC 提取 ─────────────────────────────────────────────────────────────────

def extract_top_ipcs(results: list[dict[str, Any]], top_n: int = 5) -> list[str]:
    """
    从检索结果中聚合出现最多的 IPC 大组（前4字符），返回 top_n 个。
    """
    from collections import Counter
    counter: Counter[str] = Counter()
    for r in results:
        ipcs = r.get("ipc") or []
        if isinstance(ipcs, str):
            ipcs = [ipcs]
        for ipc in ipcs:
            code = str(ipc).strip()[:4]
            if len(code) == 4:
                counter[code] += 1
    return [code for code, _ in counter.most_common(top_n)]


# ── 申请人提取 ───────────────────────────────────────────────────────────────

def extract_top_assignees(results: list[dict[str, Any]], top_n: int = 5) -> list[str]:
    """
    从检索结果中提取出现最多的申请人（用于扩展检索）。
    """
    from collections import Counter
    counter: Counter[str] = Counter()
    for r in results:
        assignee = str(r.get("assignee") or "").strip()
        if assignee and assignee not in ("-", "未知", ""):
            counter[assignee] += 1
    return [name for name, _ in counter.most_common(top_n)]


# ── 主流程骨架（Agent 填充检索结果后调用） ────────────────────────────────────

def build_verification_result(
    product_description: str,
    original_patents: list[dict[str, Any]],
    semantic_results: list[dict[str, Any]],
    keyword_results: list[dict[str, Any]],
    assignee_results: list[dict[str, Any]] | None = None,
    ipc_results: list[dict[str, Any]] | None = None,
    mode: str = "正常模式",
) -> dict[str, Any]:
    """
    汇总所有检索轨道结果，计算 Chapman 估算，生成 verification dict。
    供 Agent 在完成实际 MCP 检索后调用，写入 output_json。
    """
    # 合并独立检索池（去重）
    seen: set[str] = set()
    independent_pool: list[dict[str, Any]] = []
    for src, track in [
        (semantic_results, "语义轨道"),
        (keyword_results, "关键词轨道"),
        (assignee_results or [], "申请人扩展"),
        (ipc_results or [], "IPC分类轨道"),
    ]:
        for r in src:
            pno = str(r.get("patent_number") or r.get("no") or "").strip().upper()
            if pno and pno not in seen:
                seen.add(pno)
                r["_source_track"] = track
                independent_pool.append(r)

    # 原报告专利号集合
    original_nos: set[str] = {
        str(p.get("patent_no") or p.get("no") or "").strip().upper()
        for p in original_patents
        if p.get("patent_no") or p.get("no")
    }

    n_a = len(original_nos)
    n_b = len(independent_pool)
    overlap_nos = {p["patent_no"] for p in independent_pool
                  if str(p.get("patent_no", "")).upper() in original_nos}
    n_c = len(overlap_nos)

    chapman = chapman_estimate(n_a, n_b, n_c)
    omissions = find_omissions(original_nos, independent_pool)
    top_ipcs = extract_top_ipcs(independent_pool)
    top_assignees = extract_top_assignees(independent_pool)

    return {
        "status": f"已完成独立检索验证（{mode}）",
        "tool_status": f"语义轨道 {len(semantic_results)} 件 | 关键词轨道 {len(keyword_results)} 件 | "
                       f"申请人扩展 {len(assignee_results or [])} 件 | IPC分类轨道 {len(ipc_results or [])} 件",
        "original_pool_count": n_a,
        "independent_pool_count": n_b,
        "overlap_count": n_c,
        "estimated_total": chapman.get("estimated_total"),
        "recall_rate": f"{chapman.get('recall_a')}%" if chapman.get('recall_a') is not None else "未验证",
        "recall_rating": chapman.get("rating", "未验证"),
        "top_ipcs": top_ipcs,
        "top_assignees": top_assignees,
        "omissions": omissions,
        "validity_checks": [],  # 由 Agent 后续填入有效性验证结果
        "note": chapman.get("note", ""),
        "independent_pool_sample": independent_pool[:20],  # 存前20件供报告展示
    }


# ── CLI 入口（测试用） ────────────────────────────────────────────────────────

def main() -> None:
    if len(sys.argv) < 3:
        print("用法: python fto_independent_search.py <input_json> <output_json> [output_dir]")
        print("当前为测试模式，输出空骨架。")
        result = build_verification_result(
            product_description="测试产品",
            original_patents=[],
            semantic_results=[],
            keyword_results=[],
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    with open(input_path, "r", encoding="utf-8") as f:
        params = json.load(f)

    # 本脚本在 CLI 模式下仅输出空骨架（实际检索由 Agent 通过 MCP 工具执行）
    print("[INFO] CLI 模式：MCP 检索需由 Agent 执行，此处仅生成输入参数回显和空骨架。")
    result = {
        "input_params": params,
        "verification": build_verification_result(
            product_description=params.get("product_description", ""),
            original_patents=params.get("original_patents", []),
            semantic_results=[],
            keyword_results=[],
        ),
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"[OK] 骨架已写入：{output_path}")


if __name__ == "__main__":
    main()

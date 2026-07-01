#!/usr/bin/env python3
"""
mab_fto_recall_estimator.py
单抗 FTO 三轨并行检索召回率估算器

在 fto-check 的 Chapman 捕获-再捕获估算基础上扩展：
- 支持第三轨道：序列检索（sequence_ids）
- 扩展三方重叠统计
- 输出三轨 n_pool 和 delta_n

用法：
    python3 scripts/mab_fto_recall_estimator.py --input-json <path-to-round-input.json>

输入 JSON 格式：
{
  "round": 1,
  "keyword_ids": ["P1", "P2", "P3"],
  "semantic_ids": ["P2", "P3", "P4"],
  "sequence_ids": ["P5", "P6"],          // 可选，无结果时置空列表
  "seen_ids": [],                         // 本轮开始前已累计的 ID
  "recall_target": 0.85,
  "delta_n_min": 5,
  "overlap_correction_threshold": 0.5,   // 可选，默认 0.5
  "correction_factor": 0.9               // 可选，默认 0.9
}
"""

import argparse
import json
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="单抗 FTO 三轨并行检索召回率估算器（Chapman 捕获-再捕获）"
    )
    parser.add_argument(
        "--input-json",
        required=True,
        help="轮次输入 JSON 文件路径",
    )
    return parser.parse_args()


def load_input(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        print(f"[ERROR] 输入文件不存在：{path}", file=sys.stderr)
        sys.exit(1)
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def estimate(data: dict) -> dict:
    round_num = data.get("round", 1)
    kw_ids = set(data.get("keyword_ids", []))
    sem_ids = set(data.get("semantic_ids", []))
    seq_ids = set(data.get("sequence_ids", []))
    seen_ids = set(data.get("seen_ids", []))
    recall_target = float(data.get("recall_target", 0.85))
    if recall_target > 1.0:
        recall_target /= 100.0
    delta_n_min = int(data.get("delta_n_min", 5))
    overlap_corr_threshold = float(data.get("overlap_correction_threshold", 0.5))
    correction_factor = float(data.get("correction_factor", 0.9))

    # ── 本轮各轨道命中 ──
    n_k = len(kw_ids)
    n_s = len(sem_ids)
    n_seq = len(seq_ids)

    # ── 两两重叠 ──
    n_ks = len(kw_ids & sem_ids)
    n_k_seq = len(kw_ids & seq_ids)
    n_s_seq = len(sem_ids & seq_ids)
    n_all_three = len(kw_ids & sem_ids & seq_ids)

    # ── 本轮新增（相对于 seen_ids）──
    all_this_round = kw_ids | sem_ids | seq_ids
    new_this_round = all_this_round - seen_ids
    delta_n = len(new_this_round)

    # ── 累计池 ──
    n_pool = len(seen_ids | all_this_round)

    # ── Chapman 估算（关键词 vs 语义为主双轨）──
    # 若序列轨道有命中，将其并入"语义扩展轨道"做保守估算
    n_s_extended = len(sem_ids | seq_ids)
    n_ks_extended = len(kw_ids & (sem_ids | seq_ids))

    warnings = []
    correction_applied = False
    universe_estimate_raw = None
    universe_estimate_adjusted = None

    if n_k > 0 and n_s_extended > 0 and n_ks_extended > 0:
        # Chapman 无偏估计：N ≈ (n1+1)(n2+1)/(m+1) - 1
        universe_estimate_raw = (
            (n_k + 1) * (n_s_extended + 1) / (n_ks_extended + 1) - 1
        )

        # 重叠率修正
        overlap_rate = n_ks_extended / min(n_k, n_s_extended)
        if overlap_rate > overlap_corr_threshold:
            correction_applied = True
            universe_estimate_adjusted = universe_estimate_raw / correction_factor
            warnings.append(
                f"overlap_dependence_detected (overlap_rate={overlap_rate:.2f} > "
                f"threshold={overlap_corr_threshold}); R_est 可能偏乐观"
            )
        else:
            universe_estimate_adjusted = universe_estimate_raw

        # 宇宙不得小于累计池
        universe_estimate_adjusted = max(universe_estimate_adjusted, n_pool)

        recall_estimate = n_pool / universe_estimate_adjusted
    elif n_pool > 0:
        # 仅有一轨有效，无法做 Chapman 估算
        universe_estimate_adjusted = n_pool
        recall_estimate = None
        warnings.append("single_track_only; Chapman 估算不可用，召回率无法确定")
    else:
        universe_estimate_adjusted = 0
        recall_estimate = None
        warnings.append("all_tracks_empty; 当前方案已失败，请拓宽查询")

    # ── 决策 ──
    if n_k == 0 and n_s == 0 and n_seq == 0:
        decision = "expand_search"
    elif recall_estimate is not None and recall_estimate >= recall_target:
        decision = "target_met"
    elif delta_n < delta_n_min:
        decision = "diminishing_returns"
        warnings.append(
            f"delta_n={delta_n} < delta_n_min={delta_n_min}; 边际收益递减"
        )
    elif recall_estimate is None:
        decision = "expand_search"
    else:
        decision = "continue_search"

    # ── 汇总输出 ──
    result = {
        "round": round_num,
        "n_k": n_k,
        "n_s": n_s,
        "n_seq": n_seq,
        "n_ks": n_ks,
        "n_k_seq": n_k_seq,
        "n_s_seq": n_s_seq,
        "n_all_three": n_all_three,
        "n_pool": n_pool,
        "delta_n": delta_n,
        "universe_estimate_raw": (
            round(universe_estimate_raw, 1) if universe_estimate_raw is not None else None
        ),
        "universe_estimate_adjusted": (
            round(universe_estimate_adjusted, 1)
            if universe_estimate_adjusted is not None
            else None
        ),
        "recall_estimate": (
            round(recall_estimate, 4) if recall_estimate is not None else None
        ),
        "recall_target": recall_target,
        "correction_applied": correction_applied,
        "decision": decision,
        "warnings": warnings,
    }
    return result


def print_result(result: dict):
    print(json.dumps(result, ensure_ascii=False, indent=2))

    print("\n" + "=" * 60)
    print(f"  轮次：{result['round']}")
    print(f"  关键词命中：{result['n_k']}  语义命中：{result['n_s']}  序列命中：{result['n_seq']}")
    print(
        f"  重叠（KW∩SEM）：{result['n_ks']}  (KW∩SEQ)：{result['n_k_seq']}"
        f"  (SEM∩SEQ)：{result['n_s_seq']}  三轨同时：{result['n_all_three']}"
    )
    print(f"  累计池：{result['n_pool']}  本轮新增：{result['delta_n']}")
    if result["universe_estimate_adjusted"] is not None:
        print(f"  估算宇宙（调整后）：{result['universe_estimate_adjusted']}")
    if result["recall_estimate"] is not None:
        print(
            f"  估算召回率：{result['recall_estimate']:.1%}"
            f"  （目标：{result['recall_target']:.0%}）"
        )
    else:
        print("  估算召回率：不可用")
    print(f"  修正已应用：{result['correction_applied']}")
    print(f"\n  ▶ 决策：{result['decision'].upper()}")
    if result["warnings"]:
        print("\n  ⚠ 警告：")
        for w in result["warnings"]:
            print(f"    - {w}")
    print("=" * 60)


def main():
    args = parse_args()
    data = load_input(args.input_json)
    result = estimate(data)
    print_result(result)


if __name__ == "__main__":
    main()

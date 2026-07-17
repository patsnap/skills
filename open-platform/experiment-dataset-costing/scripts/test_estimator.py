#!/usr/bin/env python3
"""
技能测试套件：验证成本估算和合规矩阵生成逻辑
运行方式：python scripts/test_estimator.py
覆盖测试用例：cli, basic_flow
"""
import sys
import os
import subprocess
import tempfile

# 脚本自身所在目录
_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPT = os.path.join(_HERE, "run_estimator.py")
sys.path.insert(0, os.path.dirname(_HERE))  # 使 scripts 包可导入


# ── basic_flow 测试 ──────────────────────────────────────────

def test_estimate_data_volume():
    """basic_flow: 验证数据量估算逻辑"""
    from scripts.run_estimator import estimate_data_volume
    result = estimate_data_volume(["PD-L1", "4-1BB"], "small_molecule")
    assert result["raw_total"] > 0, "总数据量应大于0"
    assert result["net_total"] < result["raw_total"], "ADMET过滤后应减少"
    assert 0 < result["admet_retention_rate"] < 1, "留存率应在0-1之间"
    print(f"[PASS] basic_flow/data_volume: 原始={result['raw_total']}, 净={result['net_total']}")


def test_estimate_cost_academic():
    """basic_flow: 学术场景成本估算"""
    from scripts.run_estimator import estimate_cost
    result = estimate_cost(n_compounds=25000, n_patents=50, n_targets=2, use_case="academic")
    assert result["total"]["low"] < result["total"]["high"], "低估应小于高估"
    assert "compliance" not in result["breakdown"], "学术场景不应包含合规工时"
    print(f"[PASS] basic_flow/cost_academic: {result['total']}")


def test_estimate_cost_commercial():
    """basic_flow: 商业场景成本估算（应包含合规工时）"""
    from scripts.run_estimator import estimate_cost
    result = estimate_cost(n_compounds=25000, n_patents=50, n_targets=2, use_case="commercial")
    assert "compliance" in result["breakdown"], "商业场景应包含合规工时"
    print(f"[PASS] basic_flow/cost_commercial: 合规工时={result['breakdown']['compliance']}")


def test_compliance_matrix():
    """basic_flow: 合规矩阵生成"""
    from scripts.run_estimator import build_compliance_matrix
    sources = ["ChEMBL", "Patent-SAR", "ZINC"]
    matrix = build_compliance_matrix(sources, "commercial")
    assert len(matrix) == 3, "应返回3条记录"
    patent_row = next(r for r in matrix if r["source"] == "Patent-SAR")
    assert patent_row["commercial"] == "⚠️", "Patent-SAR商业使用应为警告"
    print(f"[PASS] basic_flow/compliance_matrix: Patent-SAR commercial={patent_row['commercial']}")


def test_single_target():
    """basic_flow: 单靶点场景"""
    from scripts.run_estimator import estimate_data_volume, estimate_cost
    volume = estimate_data_volume(["EGFR"], "small_molecule")
    assert volume["raw_total"] > 0
    cost = estimate_cost(volume["raw_total"], 10, 1, "academic")
    assert cost["total"]["mid"] > 0
    print(f"[PASS] basic_flow/single_target: EGFR net={volume['net_total']}")


def test_dual_target():
    """basic_flow: 双靶点场景（PD-L1 × 4-1BB，本次示例）"""
    from scripts.run_estimator import estimate_data_volume
    volume = estimate_data_volume(["PD-L1", "4-1BB"], "small_molecule")
    # ChEMBL 预估：PD-L1(8000) + 4-1BB(2000) = 10000
    assert volume["chembl"] == 10000, f"ChEMBL预估应为10000，实际={volume['chembl']}"
    assert volume["net_total"] > 10000, "净数据量应超过10000条"
    print(f"[PASS] basic_flow/dual_target: net={volume['net_total']}")


def test_report_generation():
    """basic_flow: 报告文件生成"""
    from scripts.run_estimator import (
        estimate_data_volume, estimate_cost,
        build_compliance_matrix, generate_outputs
    )
    with tempfile.TemporaryDirectory() as tmpdir:
        volume = estimate_data_volume(["PD-L1", "4-1BB"], "small_molecule")
        cost = estimate_cost(volume["raw_total"], 20, 2, "academic")
        compliance = build_compliance_matrix(
            ["ChEMBL", "Patent-SAR"], "academic"
        )
        task_slug = generate_outputs(
            config={"targets": ["PD-L1", "4-1BB"], "task_type": "multi-target",
                    "use_case": "academic", "molecule_type": "small_molecule"},
            volume=volume, cost=cost, compliance=compliance,
            output_dir=tmpdir,
        )
        files = os.listdir(tmpdir)
        assert any("-cost-summary.json" in f for f in files)
        assert any("-compliance-matrix.csv" in f for f in files)
        assert any("-data-inventory.csv" in f for f in files)
        print(f"[PASS] basic_flow/report_generation: task_slug={task_slug}, files={files}")


# ── cli 测试 ─────────────────────────────────────────────────

def test_cli_help():
    """cli: --help 输出"""
    result = subprocess.run(
        [sys.executable, _SCRIPT, "--help"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"help命令应返回0: {result.stderr}"
    assert "targets" in result.stdout, "help应包含 targets 参数说明"
    print("[PASS] cli/help")


def test_cli_dual_target_academic():
    """cli: 双靶点学术场景端到端运行"""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = subprocess.run(
            [sys.executable, _SCRIPT,
             "--targets", "PD-L1,4-1BB",
             "--task-type", "multi-target",
             "--use-case", "academic",
             "--molecule-type", "small_molecule",
             "--output-dir", tmpdir],
            capture_output=True, text=True
        )
        assert result.returncode == 0, f"双靶点运行失败: {result.stderr}"
        files = os.listdir(tmpdir)
        assert any("-cost-summary.json" in f for f in files)
        assert any("-compliance-matrix.csv" in f for f in files)
        assert any("-data-inventory.csv" in f for f in files)
        print(f"[PASS] cli/dual_target_academic: 生成文件={files}")


def test_cli_single_target_commercial():
    """cli: 单靶点商业场景端到端运行"""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = subprocess.run(
            [sys.executable, _SCRIPT,
             "--targets", "EGFR",
             "--task-type", "regression",
             "--use-case", "commercial",
             "--output-dir", tmpdir],
            capture_output=True, text=True
        )
        assert result.returncode == 0, f"单靶点商业场景失败: {result.stderr}"
        print("[PASS] cli/single_target_commercial")


# ── 主入口 ───────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n=== basic_flow 测试 ===")
    test_estimate_data_volume()
    test_estimate_cost_academic()
    test_estimate_cost_commercial()
    test_compliance_matrix()
    test_single_target()
    test_dual_target()
    test_report_generation()

    print("\n=== cli 测试 ===")
    test_cli_help()
    test_cli_dual_target_academic()
    test_cli_single_target_commercial()

    print("\n✅ 所有测试通过")

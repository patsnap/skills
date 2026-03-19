from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
ESTIMATOR = SCRIPTS_DIR / "fto_recall_estimator.py"


def run_estimator(payload: object) -> tuple[subprocess.CompletedProcess[str], dict]:
    with tempfile.TemporaryDirectory() as tempdir:
        input_path = Path(tempdir) / "round.json"
        input_path.write_text(json.dumps(payload), encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(ESTIMATOR), "--input-json", str(input_path)],
            cwd=str(SCRIPTS_DIR),
            capture_output=True,
            text=True,
            check=False,
        )
        stdout = result.stdout.strip()
        return result, (json.loads(stdout) if stdout else {})


class FtoRecallEstimatorCliTests(unittest.TestCase):
    def test_continue_search_when_recall_is_below_target_and_delta_is_large(self) -> None:
        result, payload = run_estimator(
            {
                "round": 1,
                "keyword_ids": ["K1", "K2", "K3", "K4", "K5", "K6"],
                "semantic_ids": ["S1", "S2", "S3", "S4", "S5", "K1"],
                "seen_ids": ["P0", "P1"],
                "recall_target": 0.85,
                "delta_n_min": 3,
            }
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertEqual(payload["decision"], "continue_search")
        self.assertEqual(payload["delta_n"], 11)
        self.assertFalse(payload["correction_applied"])
        self.assertLess(payload["recall_estimate"], 0.85)

    def test_target_met_accepts_percent_style_recall_target(self) -> None:
        result, payload = run_estimator(
            {
                "round": 3,
                "keyword_ids": ["A1", "A2", "A3", "A4", "A5"],
                "semantic_ids": ["A2", "A3", "A4", "A5", "A6"],
                "seen_ids": [f"OLD-{index}" for index in range(1, 20)],
                "recall_target": 85,
                "delta_n_min": 5,
            }
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertEqual(payload["decision"], "target_met")
        self.assertGreaterEqual(payload["recall_estimate"], 0.85)

    def test_diminishing_returns_when_new_patents_drop_below_threshold(self) -> None:
        result, payload = run_estimator(
            {
                "round": 4,
                "keyword_ids": [f"K{i}" for i in range(1, 9)],
                "semantic_ids": [f"S{i}" for i in range(1, 9)],
                "seen_ids": [f"K{i}" for i in range(1, 9)] + [f"S{i}" for i in range(1, 8)],
                "recall_target": 0.8,
                "delta_n_min": 3,
            }
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertEqual(payload["delta_n"], 1)
        self.assertEqual(payload["decision"], "diminishing_returns")

    def test_expand_search_when_both_channels_are_empty(self) -> None:
        result, payload = run_estimator(
            {
                "round": 2,
                "keyword_ids": [],
                "semantic_ids": [],
                "seen_ids": ["OLD-1", "OLD-2"],
                "recall_target": 0.8,
                "delta_n_min": 5,
            }
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertEqual(payload["decision"], "expand_search")
        self.assertIsNone(payload["recall_estimate"])
        self.assertIn("empty_dual_result", payload["warnings"])

    def test_high_overlap_triggers_correction(self) -> None:
        result, payload = run_estimator(
            {
                "round": 1,
                "keyword_ids": ["P1", "P2", "P3", "P4", "P5", "P6"],
                "semantic_ids": ["P1", "P2", "P3", "P4", "S1", "S2"],
                "seen_ids": [],
                "recall_target": 0.95,
                "delta_n_min": 2,
            }
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertTrue(payload["correction_applied"])
        self.assertIn("overlap_dependence_detected", payload["warnings"])

    def test_floor_warning_prevents_recall_above_one(self) -> None:
        result, payload = run_estimator(
            {
                "round": 5,
                "keyword_ids": ["PX-1"],
                "semantic_ids": ["PX-1"],
                "seen_ids": [f"OLD-{index}" for index in range(10)],
                "recall_target": 0.9,
                "delta_n_min": 2,
            }
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("universe_floor_applied", payload["warnings"])
        self.assertLessEqual(payload["recall_estimate"], 1.0)
        self.assertEqual(payload["universe_estimate_adjusted"], payload["n_pool"])


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parent / "qfd_pipeline.py"


def run_pipeline(*args: str) -> tuple[subprocess.CompletedProcess[str], dict]:
    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH), *args],
        cwd=str(SCRIPT_PATH.parent),
        capture_output=True,
        text=True,
        check=False,
    )
    stdout = result.stdout.strip()
    payload = json.loads(stdout) if stdout else {}
    return result, payload


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


class QfdPipelineCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.workspace = self.root / "workspace"
        self.voc_path = self.root / "voc.csv"
        write_text(
            self.voc_path,
            "comment\nbattery life should be longer\nbattery life should be longer\n",
        )

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def make_features_file(self, *, variant: str = "battery") -> Path:
        features_path = self.root / f"features-{variant}.json"
        if variant == "noise":
            payload = {
                "features": [
                    {
                        "id": "F-001",
                        "name": "fan noise",
                        "value": 42,
                        "unit": "dBA",
                        "direction": "lower_better",
                        "description": "reduce acoustic output during travel use",
                    }
                ]
            }
        else:
            payload = {
                "features": [
                    {
                        "id": "F-001",
                        "name": "battery life",
                        "value": 12,
                        "unit": "hours",
                        "direction": "higher_better",
                        "description": "longer runtime for portable use",
                    }
                ]
            }
        write_json(features_path, payload)
        return features_path

    def make_competitor_file(self) -> Path:
        competitor_path = self.root / "competitor.json"
        write_json(
            competitor_path,
            {
                "product": {"id": "comp_a", "name": "Competitor A", "model": "A1"},
                "features": [
                    {
                        "id": "F-001",
                        "name": "battery life",
                        "value": 10,
                        "unit": "hours",
                        "direction": "higher_better",
                        "description": "runtime",
                    }
                ],
            },
        )
        return competitor_path

    def test_missing_features_file_returns_actionable_payload(self) -> None:
        missing_features = self.root / "missing-features.json"
        result, payload = run_pipeline(
            "--voc-path",
            str(self.voc_path),
            "--workspace",
            str(self.workspace),
            "--features-path",
            str(missing_features),
            "--no-xlsx",
        )

        self.assertEqual(result.returncode, 1)
        self.assertEqual(payload.get("success"), False)
        self.assertEqual(payload.get("error_code"), "QFD_VALIDATION_ERROR")
        self.assertEqual(payload.get("stage"), "load_feature_spec")
        self.assertEqual(payload.get("next_action"), "ask_user_for_feature_spec_json")
        self.assertEqual(
            payload.get("missing_inputs", [{}])[0].get("name"),
            "features_path",
        )
        self.assertIn("project_meta_json", payload.get("result_files", {}))

    def test_malformed_relationships_json_returns_validation_error(self) -> None:
        features_path = self.make_features_file()
        relationships_path = self.root / "relationships.json"
        write_text(relationships_path, '{"relationships": [}')

        result, payload = run_pipeline(
            "--voc-path",
            str(self.voc_path),
            "--workspace",
            str(self.workspace),
            "--features-path",
            str(features_path),
            "--relationships-path",
            str(relationships_path),
            "--no-xlsx",
        )

        self.assertEqual(result.returncode, 1)
        self.assertEqual(payload.get("error_code"), "QFD_VALIDATION_ERROR")
        self.assertEqual(payload.get("stage"), "build_matrices")
        self.assertEqual(
            payload.get("next_action"),
            "ask_user_for_corrected_relationships_path",
        )
        self.assertEqual(
            payload.get("missing_inputs", [{}])[0].get("name"),
            "relationships_path",
        )
        self.assertIn("invalid JSON", payload.get("message", ""))

    def test_malformed_weights_json_returns_validation_error(self) -> None:
        features_path = self.make_features_file()
        weights_path = self.root / "weights.json"
        write_text(weights_path, '{"REQ-001": }')

        result, payload = run_pipeline(
            "--voc-path",
            str(self.voc_path),
            "--workspace",
            str(self.workspace),
            "--features-path",
            str(features_path),
            "--weights-path",
            str(weights_path),
            "--no-xlsx",
        )

        self.assertEqual(result.returncode, 1)
        self.assertEqual(payload.get("error_code"), "QFD_VALIDATION_ERROR")
        self.assertEqual(payload.get("stage"), "voc_process")
        self.assertEqual(payload.get("next_action"), "ask_user_for_weights_json_or_rerun_without_it")

    def test_success_payload_exposes_generated_artifacts_and_skipped_benchmark(self) -> None:
        features_path = self.make_features_file()
        result, payload = run_pipeline(
            "--voc-path",
            str(self.voc_path),
            "--workspace",
            str(self.workspace),
            "--features-path",
            str(features_path),
            "--no-xlsx",
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertEqual(payload.get("success"), True)
        self.assertEqual(payload.get("status"), "completed")
        self.assertIn("qfd_report_md", payload.get("result_files", {}))
        self.assertIn("priority_recommendations_json", payload.get("result_files", {}))
        self.assertIn("conflicts_json", payload.get("result_files", {}))
        self.assertIn("primary_report", payload.get("quick_access", {}))
        self.assertTrue(payload.get("read_guide"))
        self.assertTrue(payload.get("next_actions"))
        self.assertEqual(payload.get("summary", {}).get("benchmark_state"), "skipped")
        self.assertEqual(payload.get("summary", {}).get("run_quality"), "benchmark_skipped")
        self.assertEqual(payload.get("project_meta", {}).get("status", {}).get("step4_benchmark"), "skipped")

    def test_low_signal_structured_voc_is_repaired(self) -> None:
        voc_json = self.root / "low-signal-voc.json"
        features_path = self.make_features_file(variant="noise")
        write_json(
            voc_json,
            {
                "requirements": [
                    {
                        "description": "noise",
                        "category": "Noise / Comfort",
                        "sample_quotes": [
                            "Fan is too loud on trains",
                            "Need quieter operation for travel use",
                        ],
                    }
                ]
            },
        )

        result, payload = run_pipeline(
            "--voc-path",
            str(voc_json),
            "--workspace",
            str(self.workspace),
            "--features-path",
            str(features_path),
            "--no-xlsx",
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertEqual(payload.get("summary", {}).get("requirements_repaired"), 1)
        requirements_path = Path(payload["result_files"]["requirements_json"])
        requirements_payload = json.loads(requirements_path.read_text(encoding="utf-8"))
        description = requirements_payload["requirements"][0]["description"].lower()
        self.assertNotEqual(description, "noise")
        self.assertTrue("loud" in description or "quiet" in description)

    def test_structured_json_voc_input_is_accepted(self) -> None:
        voc_json = self.root / "structured-voc.json"
        features_path = self.make_features_file()
        write_json(
            voc_json,
            {
                "requirements": [
                    {
                        "description": "Extend battery runtime for travel sessions",
                        "category": "Power / Runtime",
                        "importance": 4,
                        "sample_quotes": ["Battery does not last through travel days"],
                    }
                ]
            },
        )

        result, payload = run_pipeline(
            "--voc-path",
            str(voc_json),
            "--workspace",
            str(self.workspace),
            "--features-path",
            str(features_path),
            "--no-xlsx",
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertEqual(payload.get("summary", {}).get("structured_voc_input"), True)
        self.assertEqual(payload.get("summary", {}).get("voc_input_mode"), "structured_requirements")
        requirements_path = Path(payload["result_files"]["requirements_json"])
        requirements_payload = json.loads(requirements_path.read_text(encoding="utf-8"))
        self.assertEqual(requirements_payload.get("structured_input"), True)
        self.assertEqual(requirements_payload["requirements"][0]["importance"], 4)

    def test_competitor_run_marks_benchmark_completed(self) -> None:
        features_path = self.make_features_file()
        competitor_path = self.make_competitor_file()

        result, payload = run_pipeline(
            "--voc-path",
            str(self.voc_path),
            "--workspace",
            str(self.workspace),
            "--features-path",
            str(features_path),
            "--competitor-specs-path",
            str(competitor_path),
            "--no-xlsx",
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertEqual(payload.get("summary", {}).get("benchmark_state"), "completed")
        self.assertEqual(payload.get("project_meta", {}).get("status", {}).get("step4_benchmark"), "completed")
        benchmark_path = Path(payload["result_files"]["benchmark_table_json"])
        benchmark_payload = json.loads(benchmark_path.read_text(encoding="utf-8"))
        self.assertEqual(benchmark_payload.get("benchmark_state"), "completed")

    def test_include_xlsx_and_no_xlsx_flags_are_reported(self) -> None:
        features_path = self.make_features_file()

        result_no_xlsx, payload_no_xlsx = run_pipeline(
            "--voc-path",
            str(self.voc_path),
            "--workspace",
            str(self.workspace / "no-xlsx"),
            "--features-path",
            str(features_path),
            "--no-xlsx",
        )
        self.assertEqual(result_no_xlsx.returncode, 0, msg=result_no_xlsx.stderr)
        self.assertEqual(payload_no_xlsx.get("summary", {}).get("include_xlsx"), False)
        self.assertEqual(payload_no_xlsx.get("summary", {}).get("xlsx_written"), False)

        result_include_xlsx, payload_include_xlsx = run_pipeline(
            "--voc-path",
            str(self.voc_path),
            "--workspace",
            str(self.workspace / "with-xlsx"),
            "--features-path",
            str(features_path),
            "--include-xlsx",
        )
        self.assertEqual(result_include_xlsx.returncode, 0, msg=result_include_xlsx.stderr)
        self.assertEqual(payload_include_xlsx.get("summary", {}).get("include_xlsx"), True)
        self.assertIn(payload_include_xlsx.get("summary", {}).get("xlsx_written"), {True, False})


if __name__ == "__main__":
    unittest.main()

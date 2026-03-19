from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
PIPELINE = SCRIPTS_DIR / "doe_pipeline.py"
WRAPPERS = {
    "evidence": SCRIPTS_DIR / "evidence_pipeline.py",
    "factor": SCRIPTS_DIR / "patent_factor_extractor.py",
    "design": SCRIPTS_DIR / "doe_designer.py",
    "report": SCRIPTS_DIR / "doe_plan_report.py",
}
EXPECTED_REPORT_HEADINGS = [
    "1. Objective and Constraints",
    "2. Selected DOE Method and Rationale",
    "3. Run Sheet Summary",
    "4. Evidence Coverage Matrix",
    "5. Facts vs Inference vs Unknowns",
    "6. Next-round Criteria",
]


def run_script(script: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *args],
        cwd=str(SCRIPTS_DIR),
        capture_output=True,
        text=True,
        check=False,
    )


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class DoePipelineCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.inputs = self.root / "inputs"
        self.outputs = self.root / "outputs"
        self.outputs.mkdir(parents=True, exist_ok=True)
        self.search_input = self.inputs / "search_input.json"
        self.fetch_manifest = self.inputs / "fetch_manifest.json"
        self.context_json = self.inputs / "context.json"
        self._write_happy_path_inputs()

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def _write_happy_path_inputs(self) -> None:
        patent_text = (
            "Fed-batch fermentation method. Temperature 30-34 degC, pH 6.2-7.0, "
            "dissolved oxygen setpoint 25-55 %, and agitation 300-700 rpm "
            "improved titer significantly (p<0.05)."
        )
        paper_text = (
            "Bioreactor cultivation protocol. Temperature between 31 and 35 degC with "
            "pH 6.4-6.9, dissolved oxygen 30-50 %, and agitation 350-650 rpm "
            "improved yield and viability significantly."
        )
        web_text = (
            "Operator guidance notes that feed rate 2-4 ml/h can support higher productivity, "
            "but this source is supplemental."
        )
        patent_file = self.inputs / "patent.txt"
        paper_file = self.inputs / "paper.txt"
        web_file = self.inputs / "web.txt"
        write_text(patent_file, patent_text)
        write_text(paper_file, paper_text)
        write_text(web_file, web_text)

        write_json(
            self.search_input,
            {
                "objective": "Maximize titer while maintaining viability",
                "responses": ["titer", "viability"],
                "constraints": ["Maintain process robustness", "DO <= 70%"],
                "patents": [
                    {
                        "id": "PAT-001",
                        "title": "Fermentation patent",
                        "year": 2024,
                        "relevance_score": 0.95,
                    }
                ],
                "papers": [
                    {
                        "id": "PAP-001",
                        "title": "Bioreactor paper",
                        "year": 2023,
                        "relevance_score": 0.92,
                    }
                ],
                "web": [
                    {
                        "id": "WEB-001",
                        "title": "Operator note",
                        "year": 2025,
                        "relevance_score": 0.61,
                    }
                ],
            },
        )
        write_json(
            self.fetch_manifest,
            {
                "items": [
                    {"source_key": "PAT-001", "status": "success", "path": str(patent_file)},
                    {"source_key": "PAP-001", "status": "success", "path": str(paper_file)},
                    {"source_key": "WEB-001", "status": "success", "path": str(web_file)},
                ]
            },
        )
        write_json(
            self.context_json,
            {
                "objective": "Maximize titer while maintaining viability",
                "responses": ["titer", "viability"],
                "constraints": ["Maintain process robustness", "DO <= 70%"],
            },
        )

    def _artifact_paths(self) -> dict[str, Path]:
        return {
            "evidence": self.outputs / "evidence_catalog.json",
            "factors": self.outputs / "factor_hypotheses.json",
            "design": self.outputs / "doe_design.json",
            "run_sheet": self.outputs / "run_sheet.csv",
            "report": self.outputs / "doe_plan.md",
        }

    def test_stepwise_cli_happy_path_matches_contract(self) -> None:
        paths = self._artifact_paths()

        evidence_result = run_script(
            PIPELINE,
            "evidence",
            "--search-input",
            str(self.search_input),
            "--fetch-manifest",
            str(self.fetch_manifest),
            "--output",
            str(paths["evidence"]),
        )
        self.assertEqual(evidence_result.returncode, 0, msg=evidence_result.stderr)
        evidence_payload = json.loads(paths["evidence"].read_text(encoding="utf-8"))
        self.assertEqual(evidence_payload["gates"]["status"], "ready")

        factor_result = run_script(
            PIPELINE,
            "factor",
            "--evidence-catalog",
            str(paths["evidence"]),
            "--max-factors",
            "4",
            "--output",
            str(paths["factors"]),
        )
        self.assertEqual(factor_result.returncode, 0, msg=factor_result.stderr)
        factors_payload = json.loads(paths["factors"].read_text(encoding="utf-8"))
        self.assertEqual(factors_payload["summary"]["status"], "ready")
        self.assertGreaterEqual(factors_payload["summary"]["design_ready_factors"], 3)

        design_result = run_script(
            PIPELINE,
            "design",
            "--factors-json",
            str(paths["factors"]),
            "--design-type",
            "auto",
            "--phase",
            "screening",
            "--responses",
            "titer,viability",
            "--max-factors",
            "4",
            "--output-json",
            str(paths["design"]),
            "--output-csv",
            str(paths["run_sheet"]),
        )
        self.assertEqual(design_result.returncode, 0, msg=design_result.stderr)
        design_payload = json.loads(paths["design"].read_text(encoding="utf-8"))
        self.assertEqual(design_payload["response_metrics"], ["titer", "viability"])
        self.assertTrue(paths["run_sheet"].exists())

        report_result = run_script(
            PIPELINE,
            "report",
            "--context-json",
            str(self.context_json),
            "--evidence-catalog",
            str(paths["evidence"]),
            "--factors-json",
            str(paths["factors"]),
            "--design-json",
            str(paths["design"]),
            "--output",
            str(paths["report"]),
        )
        self.assertEqual(report_result.returncode, 0, msg=report_result.stderr)
        report_text = paths["report"].read_text(encoding="utf-8")
        headings = re.findall(r"^## (.+)$", report_text, flags=re.MULTILINE)
        self.assertEqual(headings, EXPECTED_REPORT_HEADINGS)

    def test_run_all_writes_full_workspace_outputs(self) -> None:
        run_all_dir = self.root / "run_all"
        result = run_script(
            PIPELINE,
            "run-all",
            "--search-input",
            str(self.search_input),
            "--fetch-manifest",
            str(self.fetch_manifest),
            "--context-json",
            str(self.context_json),
            "--output-dir",
            str(run_all_dir),
            "--max-factors",
            "4",
            "--responses",
            "titer,viability",
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        for filename in [
            "evidence_catalog.json",
            "factor_hypotheses.json",
            "doe_design.json",
            "run_sheet.csv",
            "doe_plan.md",
        ]:
            self.assertTrue((run_all_dir / filename).exists(), msg=filename)

    def test_factor_step_blocks_on_insufficient_evidence_without_synthetic_defaults(self) -> None:
        patent_only = self.root / "patent_only_search.json"
        manifest = self.root / "patent_only_manifest.json"
        patent_file = self.root / "single_patent.txt"
        evidence_path = self.root / "blocked_evidence.json"
        factor_path = self.root / "blocked_factors.json"

        write_text(
            patent_file,
            "Fermentation method. Temperature 32-34 degC improved yield significantly.",
        )
        write_json(
            patent_only,
            {
                "objective": "Improve yield",
                "responses": ["yield"],
                "constraints": [],
                "patents": [{"id": "PAT-ONLY", "title": "Only patent", "year": 2024, "relevance_score": 0.9}],
            },
        )
        write_json(
            manifest,
            {"items": [{"source_key": "PAT-ONLY", "status": "success", "path": str(patent_file)}]},
        )

        evidence_result = run_script(
            PIPELINE,
            "evidence",
            "--search-input",
            str(patent_only),
            "--fetch-manifest",
            str(manifest),
            "--output",
            str(evidence_path),
        )
        self.assertEqual(evidence_result.returncode, 0, msg=evidence_result.stderr)

        factor_result = run_script(
            PIPELINE,
            "factor",
            "--evidence-catalog",
            str(evidence_path),
            "--output",
            str(factor_path),
        )
        self.assertNotEqual(factor_result.returncode, 0)
        payload = json.loads(factor_path.read_text(encoding="utf-8"))
        self.assertEqual(payload["summary"]["status"], "blocked")
        self.assertEqual(payload["factors"], [])
        self.assertNotIn("temperature", factor_path.read_text(encoding="utf-8"))
        error_payload = json.loads(factor_result.stderr.strip())
        self.assertEqual(error_payload["error_code"], "DOE_EVIDENCE_INSUFFICIENT")

    def test_compatibility_wrappers_forward_to_unified_pipeline(self) -> None:
        paths = self._artifact_paths()

        evidence_result = run_script(
            WRAPPERS["evidence"],
            "--search-input",
            str(self.search_input),
            "--fetch-manifest",
            str(self.fetch_manifest),
            "--output",
            str(paths["evidence"]),
        )
        self.assertEqual(evidence_result.returncode, 0, msg=evidence_result.stderr)

        factor_result = run_script(
            WRAPPERS["factor"],
            "--evidence-catalog",
            str(paths["evidence"]),
            "--max-factors",
            "4",
            "--output",
            str(paths["factors"]),
        )
        self.assertEqual(factor_result.returncode, 0, msg=factor_result.stderr)

        design_result = run_script(
            WRAPPERS["design"],
            "--factors-json",
            str(paths["factors"]),
            "--responses",
            "titer,viability",
            "--max-factors",
            "4",
            "--output-json",
            str(paths["design"]),
            "--output-csv",
            str(paths["run_sheet"]),
        )
        self.assertEqual(design_result.returncode, 0, msg=design_result.stderr)

        report_result = run_script(
            WRAPPERS["report"],
            "--context-json",
            str(self.context_json),
            "--evidence-catalog",
            str(paths["evidence"]),
            "--factors-json",
            str(paths["factors"]),
            "--design-json",
            str(paths["design"]),
            "--output",
            str(paths["report"]),
        )
        self.assertEqual(report_result.returncode, 0, msg=report_result.stderr)
        self.assertTrue(paths["report"].exists())


if __name__ == "__main__":
    unittest.main()

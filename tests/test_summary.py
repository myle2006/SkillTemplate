"""Check reporting integrity using isolated synthetic CSV fixtures."""

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("summary", ROOT / "scripts/summarize_results.py")
SUMMARY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SUMMARY)


class SummaryTests(unittest.TestCase):
    def report(self, content, defects=None):
        with tempfile.TemporaryDirectory() as directory:
            results = Path(directory) / "results.csv"
            results.write_text(content, encoding="utf-8")
            defect_file = None
            if defects is not None:
                defect_file = Path(directory) / "defects.csv"
                defect_file.write_text(defects, encoding="utf-8")
            return SUMMARY.summarize(results, defect_file, "Synthetic run")

    def test_denominator_excludes_blocked_and_unrun(self):
        output = SUMMARY.summarize(ROOT / "examples/01-result-review/results.csv", None, "Demo")
        self.assertIn("66.7%", output)
        self.assertIn("Supplied test records: 5", output)
        self.assertIn("including BLOCKED and ERROR): 4", output)

    def test_duplicate_result_ids_rejected(self):
        with self.assertRaises(ValueError):
            self.report("Test Case ID,Status\nTC-1,PASS\nTC-1,PASS\n")

    def test_missing_ids_rejected(self):
        with self.assertRaises(ValueError):
            self.report("Status\nPASS\n")

    def test_unknown_and_missing_status_rejected(self):
        for status in ("", "SUCCESS", "SKIP"):
            with self.subTest(status=status), self.assertRaises(ValueError):
                self.report(f"Test Case ID,Status\nTC-1,{status}\n")

    def test_aliases_normalized(self):
        output = self.report("Test Case ID,Status\nTC-1,Passed\nTC-2,Failed\nTC-3,NOT_RUN\n")
        self.assertIn("50.0%", output)
        self.assertIn("| NOT RUN | 1 |", output)

    def test_no_conclusive_results(self):
        output = self.report("Test Case ID,Status\nTC-1,BLOCKED\nTC-2,ERROR\n")
        self.assertIn("PASS+FAIL): n.a.", output)

    def test_empty_dataset(self):
        output = self.report("Test Case ID,Status\n")
        self.assertIn("Supplied test records: 0", output)
        self.assertIn("PASS+FAIL): n.a.", output)

    def test_bad_row_width_rejected(self):
        with self.assertRaises(ValueError):
            self.report("Test Case ID,Status\nTC-1,PASS,extra\n")

    def test_duplicate_defect_ids_rejected(self):
        with self.assertRaises(ValueError):
            self.report("Test Case ID,Status\nTC-1,FAIL\n", "Defect ID,Severity\nBUG-1,High\nBUG-1,High\n")


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPORTER = ROOT / "zephyr-test-case-creator" / "scripts" / "export_zephyr_csv.py"


def valid_markdown(*, step: str = "Open C:\\temp\\report.json") -> str:
    return f"""# Zephyr Test Case

## Test Case

| Field | Value |
| --- | --- |
| Key |  |
| Name | Create a plan |
| Status | Draft |
| Precondition | User can access the admin portal |
| Objective | Verify that a merchant can create a plan |
| Folder | Plans |
| Priority | Normal |
| Component | Plans |
| Labels | smoke |
| Owner |  |
| Estimated Time |  |
| Coverage (Issues) | ADM-3557 |
| Coverage (Pages) |  |
| AutomatedBy |  |
| AutomatedDate |  |

## Steps

| # | Step | Test Data | Expected Result |
| --- | --- | --- | --- |
| 1 | {step} | Plan name: Gold | The plan creation form is displayed |

## Sources Used

- `src/plans/create-plan.tsx`

## Suggested Separate Test Cases

- None identified.
"""


def run_export(
    source: Path,
    output: Path | None = None,
    *flags: str,
) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(EXPORTER), "--input", str(source)]
    if output is not None:
        command.extend(["--output", str(output)])
    command.extend(flags)
    return subprocess.run(command, capture_output=True, text=True)


def read_csv(path: Path) -> tuple[list[str] | None, list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames, list(reader)


class ExporterCliTests(unittest.TestCase):
    def test_preserves_backslashes_in_markdown_cells(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "zephyr-create-plan.md"
            output = root / "zephyr-create-plan.csv"
            source.write_text(valid_markdown(), encoding="utf-8")

            result = run_export(source, output)

            self.assertEqual(result.returncode, 0, result.stderr)
            _, rows = read_csv(output)
            row = rows[0]
            self.assertEqual(row["Test Script (Step-by-Step) - Step"], r"Open C:\temp\report.json")

    def test_preserves_repeated_backslashes_in_markdown_cells(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "zephyr-open-share.md"
            output = root / "zephyr-open-share.csv"
            source.write_text(valid_markdown(step=r"Open \\server\share"), encoding="utf-8")

            result = run_export(source, output)

            self.assertEqual(result.returncode, 0, result.stderr)
            _, rows = read_csv(output)
            row = rows[0]
            self.assertEqual(row["Test Script (Step-by-Step) - Step"], r"Open \\server\share")

    def test_rejects_an_input_without_the_zephyr_kebab_case_name(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "create_plan.md"
            source.write_text(valid_markdown(), encoding="utf-8")

            result = run_export(source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("zephyr-<flow>.md", result.stderr)

    def test_rejects_an_output_with_a_different_stem(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "zephyr-create-plan.md"
            output = root / "zephyr-other-flow.csv"
            source.write_text(valid_markdown(), encoding="utf-8")

            result = run_export(source, output)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("same filename stem", result.stderr)

    def test_fails_on_an_existing_csv_instead_of_breaking_the_artifact_pair(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "zephyr-create-plan.md"
            output = root / "zephyr-create-plan.csv"
            source.write_text(valid_markdown(), encoding="utf-8")
            output.write_text("existing", encoding="utf-8")

            result = run_export(source, output)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("already exists", result.stderr)
            self.assertFalse((root / "zephyr-create-plan-2.csv").exists())

    def test_rejects_a_markdown_missing_a_contract_field(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "zephyr-create-plan.md"
            source.write_text(valid_markdown().replace("| Owner |  |\n", ""), encoding="utf-8")

            result = run_export(source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing Test Case field(s): Owner", result.stderr)

    def test_rejects_non_sequential_step_numbers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "zephyr-create-plan.md"
            markdown = valid_markdown().replace(
                "| 1 | Open C:\\temp\\report.json | Plan name: Gold | The plan creation form is displayed |",
                "| 2 | Open C:\\temp\\report.json | Plan name: Gold | The plan creation form is displayed |",
            )
            source.write_text(markdown, encoding="utf-8")

            result = run_export(source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("step number must be 1", result.stderr)

    def test_rejects_the_unresolved_sources_placeholder(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "zephyr-create-plan.md"
            markdown = valid_markdown().replace(
                "- `src/plans/create-plan.tsx`",
                "- User-provided information or inspected source paths.",
            )
            source.write_text(markdown, encoding="utf-8")

            result = run_export(source)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("replace the Sources Used placeholder", result.stderr)

    def test_exports_the_official_columns_and_continuation_rows(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "zephyr-create-plan.md"
            output = root / "zephyr-create-plan.csv"
            markdown = valid_markdown().replace(
                "| 1 | Open C:\\temp\\report.json | Plan name: Gold | The plan creation form is displayed |",
                "| 1 | Open Plans |  | The Plans page is displayed |\n"
                "| 2 | Click Create \\| New | Name: Gold<br>Currency: USD | The plan creation form is displayed |",
            )
            source.write_text(markdown, encoding="utf-8")

            result = run_export(source, output)

            self.assertEqual(result.returncode, 0, result.stderr)
            fieldnames, rows = read_csv(output)
            self.assertEqual(
                fieldnames,
                [
                    "Key",
                    "Name",
                    "Status",
                    "Precondition",
                    "Objective",
                    "Folder",
                    "Priority",
                    "Component",
                    "Labels",
                    "Owner",
                    "Estimated Time",
                    "Coverage (Issues)",
                    "Coverage (Pages)",
                    "AutomatedBy",
                    "AutomatedDate",
                    "Test Script (Step-by-Step) - Step",
                    "Test Script (Step-by-Step) - Test Data",
                    "Test Script (Step-by-Step) - Expected Result",
                    "Test Script (Plain Text)",
                    "Test Script (BDD)",
                ],
            )
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["Name"], "Create a plan")
            self.assertEqual(rows[1]["Name"], "")
            self.assertEqual(rows[1]["Test Script (Step-by-Step) - Step"], "Click Create | New")
            self.assertEqual(
                rows[1]["Test Script (Step-by-Step) - Test Data"],
                "Name: Gold\nCurrency: USD",
            )

    def test_requires_an_explicit_flag_to_waive_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "zephyr-create-plan.md"
            output = root / "zephyr-create-plan.csv"
            source.write_text(
                valid_markdown().replace("| Coverage (Issues) | ADM-3557 |", "| Coverage (Issues) |  |"),
                encoding="utf-8",
            )

            rejected = run_export(source, output)
            accepted = run_export(source, output, "--allow-missing-coverage")

            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("Coverage (Issues)", rejected.stderr)
            self.assertEqual(accepted.returncode, 0, accepted.stderr)

    def test_overwrites_only_when_the_flag_is_present(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "zephyr-create-plan.md"
            output = root / "zephyr-create-plan.csv"
            source.write_text(valid_markdown(), encoding="utf-8")
            output.write_text("existing", encoding="utf-8")

            result = run_export(source, output, "--overwrite")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(output.read_text(encoding="utf-8").startswith("Key,Name,Status"))


if __name__ == "__main__":
    unittest.main()

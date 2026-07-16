#!/usr/bin/env python3
"""Export one approved Markdown Zephyr test case to a compatible CSV."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path


CSV_COLUMNS = [
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
]

CASE_FIELDS = CSV_COLUMNS[:15]
REQUIRED_CASE_FIELDS = ["Name", "Objective", "Folder", "Status", "Priority", "Coverage (Issues)"]
STEP_HEADERS = ["#", "Step", "Test Data", "Expected Result"]
SEPARATOR_RE = re.compile(r"^:?-{3,}:?$")
ARTIFACT_STEM_RE = re.compile(r"^zephyr-[a-z0-9]+(?:-[a-z0-9]+)*$")
SOURCES_PLACEHOLDER = "- User-provided information or inspected source paths."


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def validate_input_path(path: Path) -> None:
    if path.suffix != ".md" or not ARTIFACT_STEM_RE.fullmatch(path.stem):
        fail("input must use the zephyr-<flow>.md kebab-case naming contract")


def validate_output_path(input_path: Path, output_path: Path) -> None:
    if output_path.suffix != ".csv":
        fail("output must use the .csv extension")
    if output_path.stem != input_path.stem:
        fail("Markdown and CSV outputs must use the same filename stem")


def decode_cell(value: str) -> str:
    return re.sub(r"<br\s*/?>", "\n", value.strip(), flags=re.IGNORECASE)


def split_row(line: str) -> list[str]:
    text = line.strip()
    if not text.startswith("|") or not text.endswith("|"):
        fail(f"invalid Markdown table row: {line}")

    cells: list[str] = []
    current: list[str] = []
    content = text[1:-1]
    index = 0
    while index < len(content):
        character = content[index]
        if character == "\\" and index + 1 < len(content) and content[index + 1] == "|":
            current.append("|")
            index += 2
            continue
        if character == "|":
            cells.append(decode_cell("".join(current)))
            current = []
        else:
            current.append(character)
        index += 1
    cells.append(decode_cell("".join(current)))
    return cells


def section_lines(markdown: str, heading: str) -> list[str]:
    lines = markdown.splitlines()
    start = next((index + 1 for index, line in enumerate(lines) if line.strip() == heading), None)
    if start is None:
        fail(f"missing Markdown section: {heading}")

    section: list[str] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        if line.strip():
            section.append(line)
    return section


def parse_table(markdown: str, heading: str, expected_headers: list[str]) -> list[list[str]]:
    table_lines = [line for line in section_lines(markdown, heading) if line.strip().startswith("|")]
    if len(table_lines) < 3:
        fail(f"{heading} must contain a header, separator, and at least one data row")

    headers = split_row(table_lines[0])
    if headers != expected_headers:
        fail(f"{heading} headers must be: " + " | ".join(expected_headers))

    separator = split_row(table_lines[1])
    if len(separator) != len(headers) or not all(SEPARATOR_RE.match(cell) for cell in separator):
        fail(f"{heading} has an invalid Markdown separator row")

    rows = [split_row(line) for line in table_lines[2:]]
    for index, row in enumerate(rows, start=1):
        if len(row) != len(headers):
            fail(f"{heading} row {index} has {len(row)} cells; expected {len(headers)}")
    return rows


def validate_sources(markdown: str) -> None:
    sources = [line for line in section_lines(markdown, "## Sources Used") if line.startswith("- ")]
    if not sources:
        fail("Sources Used must contain at least one concrete source")
    if SOURCES_PLACEHOLDER in sources:
        fail("replace the Sources Used placeholder with concrete evidence")


def parse_case(markdown: str, allow_missing_coverage: bool) -> tuple[dict[str, str], list[dict[str, str]]]:
    validate_sources(markdown)
    field_rows = parse_table(markdown, "## Test Case", ["Field", "Value"])
    case: dict[str, str] = {}
    for field, value in field_rows:
        if field in case:
            fail(f"duplicate Test Case field: {field}")
        case[field] = value

    unknown = sorted(set(case) - set(CASE_FIELDS))
    if unknown:
        fail("unknown Test Case field(s): " + ", ".join(unknown))

    missing_contract_fields = [field for field in CASE_FIELDS if field not in case]
    if missing_contract_fields:
        fail("missing Test Case field(s): " + ", ".join(missing_contract_fields))

    missing = [
        field
        for field in REQUIRED_CASE_FIELDS
        if not case.get(field) and not (field == "Coverage (Issues)" and allow_missing_coverage)
    ]
    if missing:
        fail("missing required field(s): " + ", ".join(missing))

    step_rows = parse_table(markdown, "## Steps", STEP_HEADERS)
    steps: list[dict[str, str]] = []
    for index, (number, action, test_data, expected) in enumerate(step_rows, start=1):
        if number != str(index):
            fail(f"step number must be {index}; found {number or 'blank'}")
        if not action:
            fail(f"step {index} is missing Step")
        if not expected:
            fail(f"step {index} is missing Expected Result")
        steps.append({"Step": action, "Test Data": test_data, "Expected Result": expected})
    return case, steps


def ensure_output_is_available(path: Path, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        fail(
            f"output already exists: {path}; choose one unused stem for both artifacts "
            "or use --overwrite after explicit approval"
        )


def build_rows(case: dict[str, str], steps: list[dict[str, str]]) -> list[dict[str, str]]:
    metadata = {field: case.get(field, "") for field in CASE_FIELDS}
    rows: list[dict[str, str]] = []
    for index, step in enumerate(steps):
        row = {column: "" for column in CSV_COLUMNS}
        if index == 0:
            row.update(metadata)
        row["Test Script (Step-by-Step) - Step"] = step["Step"]
        row["Test Script (Step-by-Step) - Test Data"] = step["Test Data"]
        row["Test Script (Step-by-Step) - Expected Result"] = step["Expected Result"]
        rows.append(row)
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS, extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="approved case-specific Markdown path")
    parser.add_argument(
        "--output",
        help="CSV output path; defaults to the input path with a .csv extension",
    )
    parser.add_argument("--overwrite", action="store_true", help="replace an existing output file")
    parser.add_argument(
        "--allow-missing-coverage",
        action="store_true",
        help="allow blank Coverage (Issues) after explicit user approval",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_file():
        fail(f"Markdown input does not exist: {input_path}")
    validate_input_path(input_path)
    markdown = input_path.read_text(encoding="utf-8")
    case, steps = parse_case(markdown, args.allow_missing_coverage)
    requested_output = Path(args.output) if args.output else input_path.with_suffix(".csv")
    validate_output_path(input_path, requested_output)
    ensure_output_is_available(requested_output, args.overwrite)
    write_csv(requested_output, build_rows(case, steps))
    print(requested_output)


if __name__ == "__main__":
    main()

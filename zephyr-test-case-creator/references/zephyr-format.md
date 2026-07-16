# Zephyr Artifact Contract

Read this reference before writing the case-specific Markdown or exporting CSV.

## Markdown Contract

Create exactly one case using `assets/zephyr-cases-template.md`. Name it with the `zephyr-<flow>` template and use the same short stem for the Markdown and CSV filenames. The flow portion must identify the action and main object without requiring a Jira key. The exporter reads the `## Test Case` and `## Steps` tables directly, making the user-approved Markdown the single source of truth.

- Keep field names and step-table headers unchanged.
- Escape literal pipes inside cells as `\|`.
- Use `<br>` inside a cell when a line break is required.
- Leave optional values blank rather than inserting placeholders.
- Keep alternate paths under `Suggested Separate Test Cases`, not in the main steps.

Required case fields are `Name`, `Objective`, `Folder`, `Status`, and `Priority`. `Coverage (Issues)` is required unless the user explicitly waives it. At least one step is required, and every step needs `Step` and `Expected Result`.

## CSV Contract

The provided `atm-exporter.xlsx` established this exact column order:

1. `Key`
2. `Name`
3. `Status`
4. `Precondition`
5. `Objective`
6. `Folder`
7. `Priority`
8. `Component`
9. `Labels`
10. `Owner`
11. `Estimated Time`
12. `Coverage (Issues)`
13. `Coverage (Pages)`
14. `AutomatedBy`
15. `AutomatedDate`
16. `Test Script (Step-by-Step) - Step`
17. `Test Script (Step-by-Step) - Test Data`
18. `Test Script (Step-by-Step) - Expected Result`
19. `Test Script (Plain Text)`
20. `Test Script (BDD)`

For a new case, leave `Key` blank. Put metadata and step 1 in the first CSV row. For subsequent steps, leave metadata blank and populate only the three step-by-step columns. Keep Plain Text and BDD blank; Zephyr imports step-by-step scripts separately from those formats.

## Export

Resolve the script from the Skill directory, keep the user's current directory unchanged, and run:

```bash
python <skill-directory>/scripts/export_zephyr_csv.py \
  --input zephyr-create-plan.md \
  --output zephyr-create-plan.csv
```

The exporter validates Markdown structure, required fields, steps, and output naming. If the output exists, it adds a short numeric suffix instead of a timestamp. Use `--allow-missing-coverage` only after an explicit waiver and `--overwrite` only after explicit replacement approval.

## Required Completion Handoff

After creating both artifacts, tell the user that the Markdown is for review and the CSV is the file to import from Zephyr's test-case import screen in Jira. State these settings explicitly:

- File type: `Excel CSV` or equivalent CSV import.
- Encoding: `UTF-8`.
- Delimiter: comma (`,`), not slash (`/`) or semicolon (`;`).
- Start at row `1` and enable field names/headers.
- Map metadata columns by matching names.
- Map `Test Script (Step-by-Step) - Step`, `Test Script (Step-by-Step) - Test Data`, and `Test Script (Step-by-Step) - Expected Result` to their matching step-by-step fields.
- Do not choose Plain Text or BDD for the test script.

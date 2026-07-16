# Zephyr Artifact Contract

This file is the single prose contract for naming, Markdown, CSV export, and import handoff.

## Artifact Pair

- Use one kebab-case stem matching `zephyr-<flow>` for both files: `zephyr-<flow>.md` and `zephyr-<flow>.csv`.
- Describe an action and its main object in two to four meaningful words, for example `zephyr-create-plan`.
- Append a relevant lowercase Jira key only when useful, for example `zephyr-create-plan-adm-3557`.
- Prefer stems of 40 characters or fewer and omit words such as `test`, `case`, and implementation details.
- Check both paths before writing. If either exists and replacement is not approved, select the next numeric suffix that is unused for both, such as `-2`.
- The exporter never chooses a suffix because that could separate the pair; it fails on an existing CSV unless `--overwrite` was explicitly approved.

## Markdown

Populate `assets/zephyr-cases-template.md` for exactly one case.

- Keep contract headings, case fields, and step headers unchanged.
- Replace the `Sources Used` instruction with at least one concrete user or inspected source.
- Record proposed metadata and its evidence under `Decisions Applied`.
- Escape literal table pipes as `\|`; ordinary backslashes remain literal.
- Use `<br>` for a line break inside a cell.
- Leave optional values blank instead of inserting placeholders.
- Number steps sequentially from `1`.
- Put alternate paths only under `Suggested Separate Test Cases`, ranked by risk, or write `None identified.`

All 15 case fields must be present. `Name`, `Objective`, `Folder`, `Status`, and `Priority` require values. `Coverage (Issues)` requires a value unless the user explicitly waives it. Every step requires `Step` and `Expected Result`; `Test Data` is optional.

## CSV

The local `atm-exporter.xlsx` contract established this exact order:

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

Leave `Key` blank for a new case. Put metadata and step 1 in the first CSV row. Later rows contain only the three step-by-step values. Keep Plain Text and BDD blank.

## Export

Resolve the script relative to `SKILL.md` and keep the user's working directory unchanged:

```bash
python3 <skill-directory>/scripts/export_zephyr_csv.py \
  --input zephyr-create-plan.md \
  --output zephyr-create-plan.csv
```

Add `--allow-missing-coverage` only after an explicit waiver. Add `--overwrite` only after explicit replacement approval. A successful preflight validates the Markdown structure, concrete sources, complete field set, required values, sequential steps, paired naming, and output availability.

## Import Handoff

State that Markdown is the review source and CSV is the Zephyr import file. Tell the user to open Zephyr's test-case import screen in Jira and use:

- File type: `Excel CSV` or equivalent CSV import.
- Encoding: `UTF-8`.
- Delimiter: comma (`,`).
- Start row: `1`, with field names/headers enabled.
- Metadata mapping: matching column names.
- Script mapping: the three `Test Script (Step-by-Step)` columns to Step, Test Data, and Expected Result.
- Script format: Step-by-Step, not Plain Text or BDD.

Ask the user to review the mapping preview before running the import.

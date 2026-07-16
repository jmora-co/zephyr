---
name: zephyr-test-case-creator
description: Create exactly one guided Zephyr/Jira test case and export it as a short, case-specific Markdown/CSV pair. Use when translating a code flow, manual flow, PRD, screenshot, Figma design, Jira requirement, documentation, connected-tool context, or the code repository in the current working directory into precise step-by-step Zephyr test steps.
---

# Zephyr Test Case Creator

Create one test case per execution. Interact in the user's language and write Zephyr content in English unless requested otherwise.

## Non-negotiable Rules

- Treat user-provided information as authoritative. Inspect available sources and infer useful defaults, but never invent an unconfirmed material action or expected result.
- Treat a code repository containing the current working directory as intentionally supplied context unless the user says otherwise. Explore it proactively before asking questions.
- For UI flows, start with login unless the user explicitly places authentication in `Precondition`. For API, background, or already-authenticated flows, start from the confirmed entry state.
- Keep alternate paths, errors, roles, and edge cases out of the current case; suggest them as future cases.
- Use `AskUserQuestion` for blocking decisions when available, but never add it to `allowed-tools`; doing so can cause an empty, unrendered response. If unavailable, use an equivalent structured question in chat.
- Ask only for information that cannot be discovered or safely defaulted. Offer 2-3 mutually exclusive choices with a short consequence and a recommendation only when defensible.
- Create output files in the current working directory. Never create a JSON artifact.
- Name every case with the template `zephyr-<flow>`, using the same kebab-case stem for both artifacts: `zephyr-<flow>.md` and `zephyr-<flow>.csv`.
- Write `zephyr-<flow>.md` first. Export `zephyr-<flow>.csv` only after explicit user approval.
- Do not overwrite either output without explicit approval. If either path already exists, choose the next available numeric suffix for both files, such as `-2`; never use timestamps for collision handling.

## Load On Demand

- Read `references/guided-discovery.md` when the supplied flow is incomplete or ambiguous.
- Read `references/zephyr-format.md` before writing or exporting artifacts.
- Use `assets/zephyr-cases-template.md` as the Markdown structure.
- Inspect a user-provided Zephyr export, such as `atm-exporter.xlsx`, only when the expected import contract differs from or must be checked against the bundled format.

## Workflow

1. Inspect the request, current directory, and relevant supplied sources before asking questions.
   - Detect whether the current directory is inside a code repository, preferably with `git rev-parse --show-toplevel`; when Git is unavailable, look for source directories, project manifests, or build configuration.
   - When a repository is detected, inspect it proactively and read-only. Start with repository instructions (`AGENTS.md` or equivalent), the README, project manifests, and the files most closely related to the feature named by the user. Use targeted filename and text searches rather than scanning the entire repository.
   - Inspect nearby tests, routes, UI labels, API contracts, fixtures, and domain names when they can reveal navigation, preconditions, test data, or observable outcomes. Use the current branch or issue key as a search hint when useful.
   - Ignore generated output, dependency folders, binaries, caches, and secrets. Do not run the application or broad test suites solely for discovery unless necessary and safe.
   - Use repository evidence to fill gaps and reduce questions, but distinguish implemented behavior from requested behavior. If code conflicts with the user's description or leaves a material outcome uncertain, surface the conflict and ask only the blocking question.
   - Infer whether the flow is practical, manual, or theoretical; do not ask the user to classify it unless that distinction blocks source discovery.
2. Identify the actor, objective, coverage requirement, entry state, final observable outcome, and any necessary preconditions.
3. Choose the shortest interview path:
   - **Fast path:** When the flow is substantially complete, normalize it into a full draft and ask only about unresolved ambiguities.
   - **Discovery path:** When material segments are missing, use the decision loop in `references/guided-discovery.md`.
4. Build the path as `current state -> action -> test data -> observable expected result`. Present a grouped draft for confirmation; do not require confirmation after every step unless uncertainty is high.
5. Apply inferable or user-configured defaults in one pass. Ask only for required metadata still missing.
6. Choose the artifact stem, then write the Markdown from the bundled template.
   - Always start with `zephyr-` so the artifact type is recognizable in mixed directories.
   - Describe the flow with an action and its main object, using two to four meaningful words when needed; for example `zephyr-create-plan` or `zephyr-cancel-subscription`.
   - Never depend on a Jira key to identify the case. When a relevant key exists and adds value, append it after the flow, for example `zephyr-create-plan-adm-3557`.
   - Keep the complete stem at 40 characters or fewer when practical. Omit redundant words such as `test`, `case`, and implementation details that do not distinguish the flow.
   - Check both the Markdown and CSV paths before writing. When either exists and replacement was not approved, apply the same numeric suffix to both.
   - Review the draft for skipped navigation, hidden assumptions, compound actions, vague results, and mixed variants.
7. Ask one approval question: approve and export, edit metadata, or edit steps/setup.
8. After approval, resolve the exporter relative to this `SKILL.md` and run it without changing the user's working directory:

   ```bash
   python <skill-directory>/scripts/export_zephyr_csv.py \
    --input zephyr-<flow>.md \
    --output zephyr-<flow>.csv
   ```

   Add `--allow-missing-coverage` only when the user explicitly confirms there is no linked issue. Add `--overwrite` only after explicit replacement approval.

9. Verify that the CSV uses the official column order and contains one metadata row plus continuation rows for subsequent steps.
10. End with a concise import handoff in the user's language. Include:
    - The generated Markdown and CSV paths, explaining that Markdown is for review and CSV is the file to import.
    - Import destination: the test-case import screen for Zephyr in Jira.
    - File type: `Excel CSV` or the equivalent CSV import option.
    - Encoding: `UTF-8`.
    - Delimiter: comma (`,`), not slash (`/`) or semicolon (`;`).
    - Start row: `1`, with the first row treated as field names/headers.
    - Mapping: map metadata columns by their matching names and map the three `Test Script (Step-by-Step)` columns for Step, Test Data, and Expected Result. Do not select Plain Text or BDD as the script format.

## Defaults

Use user-configured defaults first. Otherwise propose these without asking separately when they fit the available context:

- `Status`: `Approved`
- `Priority`: `Normal`
- `Folder`: infer from product/module; ask only if no stable folder can be proposed
- `Labels` and `Component`: infer from Jira, repository, or feature terminology
- `Coverage (Issues)`: infer from a supplied Jira key; otherwise ask once or confirm that coverage is intentionally blank

Never persist defaults outside the current execution unless requested.

## Completion Gate

Before writing Markdown, require `Name`, `Objective`, `Folder`, `Status`, `Priority`, and at least one step. Require `Coverage (Issues)` unless explicitly waived. Every step must contain an action and observable expected result; test data is optional.

Before reporting completion, ensure only the intended Markdown and CSV outputs were created. Report both paths and provide the import handoff from step 10; never finish with only “files created.”

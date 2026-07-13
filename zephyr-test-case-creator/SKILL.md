---
name: zephyr-test-case-creator
description: Create exactly one guided Zephyr/Jira test case and export it as human-readable zephyr-cases.md plus a Zephyr-compatible bulk CSV. Use when translating a code flow, manual flow, PRD, screenshot, Figma design, Jira requirement, documentation, or connected-tool context into precise step-by-step Zephyr test steps.
---

# Zephyr Test Case Creator

Create one test case per execution. Interact in the user's language and write Zephyr content in English unless requested otherwise.

## Non-negotiable Rules

- Treat user-provided information as authoritative. Inspect available sources and infer useful defaults, but never invent an unconfirmed material action or expected result.
- For UI flows, start with login unless the user explicitly places authentication in `Precondition`. For API, background, or already-authenticated flows, start from the confirmed entry state.
- Keep alternate paths, errors, roles, and edge cases out of the current case; suggest them as future cases.
- Use `AskUserQuestion` for blocking decisions when available, but never add it to `allowed-tools`; doing so can cause an empty, unrendered response. If unavailable, use an equivalent structured question in chat.
- Ask only for information that cannot be discovered or safely defaulted. Offer 2-3 mutually exclusive choices with a short consequence and a recommendation only when defensible.
- Create output files in the current working directory. Never create a JSON artifact.
- Write `zephyr-cases.md` first. Export `zephyr-bulk.csv` only after explicit user approval.
- Do not overwrite either output without explicit approval. Otherwise use the timestamped path selected by the exporter or an equivalent timestamped Markdown filename.

## Load On Demand

- Read `references/guided-discovery.md` when the supplied flow is incomplete or ambiguous.
- Read `references/zephyr-format.md` before writing or exporting artifacts.
- Use `assets/zephyr-cases-template.md` as the Markdown structure.
- Inspect a user-provided Zephyr export, such as `atm-exporter.xlsx`, only when the expected import contract differs from or must be checked against the bundled format.

## Workflow

1. Inspect the request, current directory, and relevant supplied sources before asking questions. Infer whether the flow is practical, manual, or theoretical; do not ask the user to classify it unless that distinction blocks source discovery.
2. Identify the actor, objective, coverage requirement, entry state, final observable outcome, and any necessary preconditions.
3. Choose the shortest interview path:
   - **Fast path:** When the flow is substantially complete, normalize it into a full draft and ask only about unresolved ambiguities.
   - **Discovery path:** When material segments are missing, use the decision loop in `references/guided-discovery.md`.
4. Build the path as `current state -> action -> test data -> observable expected result`. Present a grouped draft for confirmation; do not require confirmation after every step unless uncertainty is high.
5. Apply inferable or user-configured defaults in one pass. Ask only for required metadata still missing.
6. Write `zephyr-cases.md` from the bundled template and review it for skipped navigation, hidden assumptions, compound actions, vague results, and mixed variants.
7. Ask one approval question: approve and export, edit metadata, or edit steps/setup.
8. After approval, resolve the exporter relative to this `SKILL.md` and run it without changing the user's working directory:

   ```bash
   python <skill-directory>/scripts/export_zephyr_csv.py \
     --input zephyr-cases.md \
     --output zephyr-bulk.csv
   ```

   Add `--allow-missing-coverage` only when the user explicitly confirms there is no linked issue. Add `--overwrite` only after explicit replacement approval.
9. Verify that the CSV uses the official column order and contains one metadata row plus continuation rows for subsequent steps.

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

Before reporting completion, ensure only the intended Markdown and CSV outputs were created and tell the user which paths were produced.

---
name: zephyr-test-case-creator
description: Create one evidence-backed Zephyr/Jira test case as an approved Markdown/CSV pair. Use when the user wants to discover a test flow or export a confirmed case to Zephyr CSV.
---

# Zephyr Test Case Creator

Create exactly one test case per execution. Interact in the user's language and write Zephyr content in English unless requested otherwise.

## Guardrails

- Treat explicit user information as authoritative. Use available evidence to reduce questions, while material actions and expected results enter the case only after confirmation.
- For UI flows, begin with login unless authentication is explicitly recorded in `Precondition`. Begin API, background, and already-authenticated flows from their confirmed entry state.
- Keep the main case focused on one path. Rank at most three errors, roles, permissions, or edge cases as suggested future cases; create none automatically.
- Create only the paired Markdown and CSV artifacts in the user's working directory. Create no JSON or persistent defaults.
- Write the Markdown before its CSV. Export only through the approval gate, and replace an existing artifact only after explicit replacement approval.
- Use a structured question tool for blocking decisions when available. `AskUserQuestion` must remain outside `allowed-tools` because allowlisting it can produce an empty response; otherwise ask the same concise question in chat.

## Evidence Ladder

Classify every material decision before drafting:

1. **Confirmed:** explicitly supplied or approved by the user; apply it.
2. **Source-backed:** supported by Jira, code, tests, routes, UI copy, designs, or documentation; propose it with its source.
3. **Convention-backed:** suggested by nearby approved cases or stable project conventions; propose it with its basis.
4. **Unresolved:** unsupported or contradicted; ask one blocking question.

When sources disagree, distinguish implemented behavior from intended behavior and ask the user which one the case should cover. Never silently promote source-backed or convention-backed content to confirmed.

## Load on Demand

- Read `references/guided-discovery.md` only when material parts of the flow remain unresolved.
- Read `references/zephyr-format.md` before naming, writing, exporting, or handing off artifacts.
- Populate `assets/zephyr-cases-template.md`; keep its contract headings and table fields unchanged.
- Inspect a user-provided Zephyr export only when the bundled import contract must be revalidated.

## Five-Phase Flow

### 1. Intake

Inspect the request and supplied context before asking questions. Treat a repository containing the working directory as supplied read-only context: read its agent instructions first, then use targeted searches across the most relevant tests, routes, UI labels, API contracts, fixtures, and feature files. Avoid generated content, dependencies, caches, secrets, application startup, and broad test runs used only for discovery.

Choose the fast path when actor, objective, entry state, action sequence, and final observable outcome are already supported. Otherwise use `references/guided-discovery.md`. Intake is complete when each of those five elements is confirmed, source-backed, convention-backed, or explicitly unresolved.

### 2. Draft

Build steps as `current state -> action -> test data -> observable expected result`. Check that setup is reproducible, navigation is not skipped, each row contains one action, and each result is externally observable. Put setup-only information in `Precondition`.

Prepare one grouped preview containing:

- Metadata and the basis for every proposed default.
- The complete ordered step table.
- Concrete sources used.
- Up to three separate-case suggestions ranked by risk.

Draft is complete when required metadata and every step are visible in one reviewable preview without hidden assumptions.

### 3. Approval

Ask one decision: **approve and export**, **edit metadata**, or **edit steps/setup**. When approved, all source-backed and convention-backed values shown in the preview become confirmed for this execution. Approval is complete only with an explicit export choice.

### 4. Artifacts

Follow `references/zephyr-format.md` as the artifact contract. Select one unused `zephyr-<flow>` stem for both files before writing. Populate the bundled template, write the Markdown, and export with `python3` using the script resolved relative to this `SKILL.md`. Use `--allow-missing-coverage` only after an explicit waiver and `--overwrite` only after explicit replacement approval.

Artifacts are complete when the exporter succeeds, both files share one stem, and the CSV contains one metadata row with step 1 plus exactly one continuation row for each later step.

### 5. Handoff

Follow the import handoff in `references/zephyr-format.md`. Report the two artifact paths, distinguish the reviewable Markdown from the importable CSV, and include any ranked future cases without creating them. Handoff is complete when the user has all required Zephyr import settings.

## Metadata Policy

- Apply user-configured values directly.
- Propose source-backed or convention-backed values in the grouped preview rather than silently applying them.
- Treat `Status`, `Folder`, and `Component` as controlled project values. If support for a candidate cannot be found, include the unresolved value in the approval question.
- Propose `Priority: Normal` only when no evidence indicates a different value.
- Infer `Coverage (Issues)` from an explicit Jira key. Otherwise include a blank-coverage waiver in the grouped approval instead of asking a separate question.

## Completion Gate

Before approval, require `Name`, `Objective`, `Folder`, `Status`, `Priority`, at least one concrete source, and at least one complete step. Require `Coverage (Issues)` or an explicit waiver. Before reporting completion, ensure that only the intended Markdown and CSV were created and that the artifact handoff is complete.

# Zephyr Test Case Creator

[![Agent Skill](https://img.shields.io/badge/Agent_Skill-Zephyr-0052CC?style=for-the-badge)](https://skills.sh/jmora-co/zephyr)
[![Install with skills CLI](https://img.shields.io/badge/npx_skills-install-111111?style=for-the-badge)](https://www.skills.sh/docs/cli)
[![Zephyr CSV](https://img.shields.io/badge/output-Zephyr_CSV-15A05C?style=for-the-badge)](https://support.smartbear.com/zephyr/docs/en/test-cases/import-test-cases.html)

An Agent Skill that turns functional workflows into clear, complete Zephyr test cases ready to import into Jira.

It does not invent the workflow for the user. It explores the available context, proposes useful options, and guides the definition of every step from the initial state to an observable outcome.

## Installation

You need Node.js with `npx` available. There is no need to clone the repository or install a global package.

### Recommended: choose the agent and scope

```bash
npx skills add jmora-co/zephyr --skill zephyr-test-case-creator
```

The installer detects compatible agents and lets you choose where to install the Skill.

### Global installation for all compatible agents

```bash
npx skills add jmora-co/zephyr --skill zephyr-test-case-creator -g -a '*' -y
```

The global installation makes the Skill available across all your projects. To install it only in the current project, use the recommended command and select project scope.

## Usage

Invoke the Skill from your agent:

```text
Use $zephyr-test-case-creator to create a Zephyr case for the plan creation workflow.
```

You can also provide context from the beginning:

```text
Use $zephyr-test-case-creator to map the happy path for ADM-3557.
Explore this repository to identify the navigation flow and ask me whenever
you find functional decisions that cannot be confirmed from the code.
```

The conversation follows the user's language. Test case content is written in English by default to keep Zephyr consistent.

## How It Works

```mermaid
flowchart LR
    A[User context] --> B[Guided discovery]
    B --> C[Confirmed workflow]
    C --> D[zephyr-flow.md]
    D --> E{Approved}
    E -->|Edit| B
    E -->|Export| F[zephyr-flow.csv]
```

1. Read the available manual workflow, code, PRD, Jira issue, screenshots, Figma designs, or documentation.
2. Identify the actor, objective, entry point, preconditions, and final outcome.
3. Propose concrete alternatives only when a decision is missing.
4. Build one test case with precise actions and observable expected results.
5. Generate a short, case-specific Markdown file for human review.
6. After explicit approval, export a CSV with the same filename stem.

## Two Paths, Less Friction

| Path | When It Is Used | Behavior |
| --- | --- | --- |
| Fast | The user has already provided an almost complete workflow | Normalize the case and ask only about ambiguities |
| Guided | Material parts of the journey are missing | Discover the workflow step by step with contextual options |

For UI workflows, the Skill proposes starting from login. If authentication is outside the test scope, it is documented as a `Precondition`. Alternate workflows, errors, and permission scenarios are suggested as separate executions to keep each case focused.

## Generated Files

The Skill creates only these files in the directory where it is executed:

| File | Purpose |
| --- | --- |
| `zephyr-create-plan.md` | Human-readable source for review and approval |
| `zephyr-create-plan.csv` | Final bulk-import file for Zephyr |

The approved Markdown is the single source of truth for the CSV. Each case follows the short `zephyr-<flow>` template, shared by both files, so Zephyr artifacts and their covered flow remain recognizable in a mixed directory. Jira keys are optional and, when useful, are appended after the flow. No intermediate JSON files are created, and existing files are never overwritten without explicit approval; collisions receive a numeric suffix such as `-2`.

## Zephyr Format

The exporter generates the 20 columns used by the Zephyr contract, including:

- Test case metadata in the first row.
- Additional steps as continuation rows.
- Separate `Step`, `Test Data`, and `Expected Result` columns.
- UTF-8 encoding and comma delimiter.
- Validation for metadata, coverage, and expected results.

After generating both files, the Skill provides a concise import handoff. Import the CSV from Zephyr's test-case import screen in Jira using Excel CSV, UTF-8, comma (`,`) as the delimiter, and row 1 as field names. Map the three step-by-step columns for Step, Test Data, and Expected Result; do not select Plain Text or BDD as the script format. Review the mapping preview before running the import. See the [official Zephyr import documentation](https://support.smartbear.com/zephyr/docs/en/test-cases/import-test-cases.html).

## Structure

```text
.
├── README.md
└── zephyr-test-case-creator/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    ├── assets/
    │   └── zephyr-cases-template.md
    ├── references/
    │   ├── guided-discovery.md
    │   └── zephyr-format.md
    └── scripts/
        └── export_zephyr_csv.py
```

The exporter uses only the Python standard library and requires no additional dependencies.

## Principles

- One test case per execution.
- User-provided information takes precedence over inference.
- Questions include options, consequences, and a recommendation when supported by evidence.
- Expected results are specific and observable.
- Variants remain separate from the main workflow.
- Human approval is required before export.

---

Built to turn functional conversations into Zephyr cases that teams can review, maintain, and import with confidence.

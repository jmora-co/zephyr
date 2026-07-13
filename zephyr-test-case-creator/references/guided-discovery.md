# Guided Discovery

Use this reference only when the user has not supplied a complete start-to-finish flow.

## Interview Strategy

Read available context first. Ask only the next decision that prevents a reliable draft. Use `AskUserQuestion` when available, without listing it in `allowed-tools`.

For each question:

- Offer 2-3 mutually exclusive, context-specific choices.
- Put a recommended choice first only when evidence supports it.
- State the consequence of each choice briefly.
- Allow free-form correction without adding an explicit `Other` option when the UI already provides it.
- Combine tightly related missing facts into one question when that reduces turns without creating a survey.

## Decision Loop

1. **Target:** Determine actor, business objective, requirement or Jira coverage, and final observable outcome.
2. **Entry state:** For UI flows, propose login. Otherwise propose the entry point found in the supplied source or ask whether setup belongs in `Precondition`.
3. **Path segment:** From the last confirmed state, propose likely next actions discovered from routes, screens, tests, docs, or user context.
4. **Assertion:** Confirm what observable result follows the selected action.
5. **Stop condition:** When the confirmed result proves the objective, draft the complete case instead of continuing to interview.

Track uncertainty internally as confirmed, source-inferred, or unresolved. Put only confirmed content in the final case.

## Representative Questions

Adapt these options to the actual context; do not run them as a fixed questionnaire.

```text
Where should this UI flow start?
1. Login with the selected role (recommended for a complete user journey)
2. Start authenticated and record the session in Precondition (shorter, authentication out of scope)
3. Start from a specific state found in the supplied source (requires that state to be reproducible)
```

```text
From the confirmed page, which action reaches the target?
1. [Likely action found in source] (recommended because it matches the implemented path)
2. [Plausible alternate action] (use if this is the intended user journey)
3. Provide the exact navigation sequence (use when neither source-derived path is correct)
```

```text
What proves the action succeeded?
1. [Observable UI or API result inferred from source] (recommended when it matches the requirement)
2. [Alternative state or data change] (use when persistence is the real objective)
3. Provide the exact expected result (use when the source does not define acceptance criteria)
```

## Draft Review

Present all confirmed steps together. Ask for individual step confirmation only when actions conflict, a source is incomplete, or the expected result remains ambiguous. Move setup-only details to `Precondition`; separate variants into future cases.

# Guided Discovery

Use this decision loop only for material parts of the journey that remain unresolved after source inspection.

## Interview Contract

- State what was found before asking.
- Ask only the next decision that blocks a reliable grouped draft.
- Offer 2-3 mutually exclusive, context-specific choices with one short consequence each.
- Put a recommendation first only when evidence supports it and name that evidence.
- Let the question UI provide its free-form correction path; in chat, explicitly invite a correction after the numbered choices.
- Combine tightly coupled facts only when the result remains one decision rather than a survey.

## Decision Loop

1. **Target:** Resolve the actor, business objective, Jira coverage, and final observable proof.
2. **Entry:** For UI flows, propose login. Otherwise propose the source-backed entry state or moving setup into `Precondition`.
3. **Segment:** From the last confirmed state, offer the likely next actions found in routes, screens, tests, documentation, or user context.
4. **Assertion:** Resolve the observable UI, API, message, navigation, or persisted state produced by the selected action.
5. **Stop:** As soon as the confirmed result proves the objective, prepare the grouped draft instead of extending the interview.

Do not reopen confirmed decisions unless new evidence contradicts them.

## Question Patterns

Adapt these patterns to actual evidence; never run them as a fixed questionnaire.

```text
I found that this UI flow can begin at authentication. Which scope should the case cover?
1. Login with [source-backed role] (recommended: covers the complete user journey found in [source])
2. Start authenticated and record the session in Precondition (shorter: authentication remains out of scope)
```

```text
From [confirmed page], I found two supported routes to the target. Which journey should this case cover?
1. [Likely action] (recommended: matches [test/route/requirement])
2. [Alternate action] (covers the secondary navigation path)
```

```text
The source confirms the action but not its acceptance criterion. What should prove success?
1. [Observable result] (recommended: visible immediately after the action)
2. [Persisted result] (stronger: verifies the saved state after reload or retrieval)
```

## Draft Transition

Before leaving discovery, summarize confirmed decisions and cite the evidence behind each proposed value. Present all steps together. Return to an individual step only when a conflict or unresolved expected result makes the grouped draft unreliable.

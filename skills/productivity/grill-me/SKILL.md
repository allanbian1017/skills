---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Learns user preferences and rationale over time to calibrate future recommendations. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
---

# Phase 1 — Load Preferences

At the start of each session, read `preferences.md` from this skill's directory (if it exists). These are the user's known design preferences with rationale, learned from previous sessions.

# Phase 2 — Preference-Aware Questioning

Interview the user relentlessly about every aspect of the plan until reaching shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. Ask questions one at a time. If a question can be answered by exploring the codebase, explore the codebase instead.

For each question, provide a recommended answer. Apply these rules:

- **Known preferences**: When a question maps to a known preference from `preferences.md`, show it as the recommended answer: *"Based on your preference, I'd recommend [X] because [their rationale]. Does this still apply here?"* Still ask the question — never skip it.
- **Rationale detection**: When the user provides an answer with explicit rationale (e.g., "I prefer X because Y"), internally flag it as a candidate preference to capture later.
- **Contradiction handling**: When a user's answer contradicts an existing preference, surface it inline immediately — do not defer this to the batch phase. Say: *"You previously said [X] because [Y]. Now you're saying [Z]. What changed?"* Capture their rationale for the change. This is the most valuable kind of learning.

# Phase 3 — Propose Session End

When all branches of the decision tree are resolved, propose ending the session: *"I think we've covered everything. Shall I summarize what I learned about your preferences?"*

- If the user confirms, proceed to Phase 4.
- If the user says there's more to discuss, continue Phase 2.

# Phase 4 — Batch Learning

Present all candidate preferences for the user to review:

- **New preferences**: Answers where the user provided explicit rationale during the session.
- **Updated preferences**: Existing preferences that were contradicted and resolved during the session.

For each candidate, ask the user to confirm, edit, or reject. Only persist confirmed entries.

Write confirmed entries to `preferences.md` in this skill's directory using this format:

```markdown
### [Preference Title]
- **Preference**: [What the user prefers]
- **Rationale**: [Why — in the user's own words where possible]
- **Learned**: [Date] — [Brief context of the plan/session]
```

Append new entries to the end of the file. For updated preferences, replace the old entry with the new one, preserving the original "Learned" date and adding the update date.

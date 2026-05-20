# {repo_name} — GitHub Repo Study Report

## Source
- **Repository**: {url}
- **Stars**: {stars} | **Forks**: {forks} | **Language**: {language}
- **License**: {license}
- **Analysis Date**: {date}

---

## Executive Summary

[Answer these four questions in 3-5 sentences:
1. What problem does this repo solve?
2. How is it designed?
3. Can I trust/use/extend it?
4. What can I learn from it?]

---

## 1. Problem & Purpose

**What pain point is this solving?**

[Describe the specific problem this repo addresses]

**Who is the target user?**

[Identify the intended audience]

**Why does this approach exist?**

[Explain the motivation — what gap or limitation prompted this project]

**Tradeoffs:**

[List the key tradeoffs the project makes, e.g.:
- Performance vs simplicity
- Scalability vs maintainability
- Flexibility vs opinionated design]

---

## 2. Mental Model of the System

> "If I had to explain this repo on a whiteboard in 3 minutes, what would I draw?"

[Provide a text/ASCII diagram showing the high-level system flow:

```
Input → [Component A] → [Component B] → Output
              ↓
        [Component C]
```

Then explain each component's role in 1-2 sentences.]

---

## 3. Entry Points

| File | Role | What it does |
|---|---|---|
| `{file}` | {role} | {description} |

**Execution trace:**

```
Entrypoint → orchestration → business logic → infrastructure/tool layer
```

---

## 4. Folder Structure & Boundaries

```
[Paste the key directory tree here]
```

**Architecture analysis:**
- Is the architecture modular? [Yes/No — explain]
- Are responsibilities separated clearly? [Yes/No — explain]
- Is coupling high or low? [Assessment]
- What is considered "core logic"? [Identify]

---

## 5. Core Abstractions

> "What primitives is this entire system built on?"

| Abstraction | Location | Purpose |
|---|---|---|
| {name} | `{file}` | {purpose} |

[Explain the relationships between these abstractions]

---

## 6. State Management

- **Where does state live?** [Answer]
- **Who owns state?** [Answer]
- **How is state updated?** [Answer]
- **Is state immutable?** [Answer]
- **Is there persistence/checkpointing?** [Answer]
- **How are retries handled?** [Answer]

---

## 7. Decision Logic

[Identify where the "intelligence" or routing logic lives:]

- **Planners**: [if any]
- **Routing logic**: [if any]
- **Evaluators / scoring**: [if any]
- **Retry / fallback mechanisms**: [if any]
- **Condition checks**: [if any]

---

## 8. Feedback Loops

> "How does the system know whether it succeeded?"

- **Logging**: [describe]
- **Telemetry / metrics**: [describe]
- **Evaluation pipelines**: [describe]
- **Retry/correction loops**: [describe]
- **User feedback systems**: [describe]

---

## 9. Developer Experience (DX)

| Dimension | Assessment | Notes |
|---|---|---|
| Setup simplicity | {rating} | {notes} |
| Documentation quality | {rating} | {notes} |
| Examples | {rating} | {notes} |
| Naming quality | {rating} | {notes} |
| Type safety | {rating} | {notes} |
| Scripts / tooling | {rating} | {notes} |
| Local dev workflow | {rating} | {notes} |
| Test clarity | {rating} | {notes} |

---

## 10. Tests

**Test types present:**
- [ ] Unit tests
- [ ] Integration tests
- [ ] End-to-end tests
- [ ] Edge case tests

**What tests reveal:**
- **Intended behavior**: [what the tests tell us about how the system should work]
- **Assumptions**: [implicit assumptions visible in tests]
- **Invariants**: [what the tests protect]
- **Failure handling**: [how failures are tested]

---

## 11. Tradeoffs & Constraints

- **Why this architecture instead of another?** [Answer]
- **What limitations exist?** [Answer]
- **What complexity was intentionally avoided?** [Answer]
- **What scalability assumptions exist?** [Answer]

---

## 12. Repo Health

| Metric | Value |
|---|---|
| Last commit | {date} |
| Commit frequency | {frequency} |
| Open issues | {count} |
| Open PRs | {count} |
| Contributors | {count} |
| Latest release | {version} ({date}) |
| Release cadence | {cadence} |

**Issue quality**: [Assessment of issue descriptions, labels, responsiveness]

**PR discussions**: [Assessment of code review quality and thoroughness]

**Maintenance quality**: [Overall assessment]

---

## 13. Engineering Taste

[Analyze the author's engineering fingerprints:]

- **Naming style**: [observations]
- **Abstraction depth**: [shallow/deep, appropriate?]
- **Simplicity preference**: [observations]
- **Error handling philosophy**: [observations]
- **Optimization choices**: [observations]

---

## 14. 5 Hidden Architectural Flaws

> "Identify 5 architectural flaws hidden in plain sight. For each, list the exact file and line number, and evaluate its impact on future maintainability."

| Flaw | File & Line | Impact on Future Maintainability |
|---|---|---|
| 1. {flaw_description} | `{file}:{line}` | {impact_assessment} |
| 2. {flaw_description} | `{file}:{line}` | {impact_assessment} |
| 3. {flaw_description} | `{file}:{line}` | {impact_assessment} |
| 4. {flaw_description} | `{file}:{line}` | {impact_assessment} |
| 5. {flaw_description} | `{file}:{line}` | {impact_assessment} |

---

## Key Learnings

[List the most valuable engineering concepts, patterns, or insights that can be learned from studying this repo. Focus on transferable knowledge.]

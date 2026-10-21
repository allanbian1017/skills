# RCA: [Workflow Name / Affected Component] - [Issue Summary]

- **Date**: YYYY-MM-DD
- **Version**: V[Version number, e.g., V1]
- **Related Skills/Rules**:
  - [Skill Name / SKILL.md](../../SKILL.md)
  - [Readme / README.md](../../README.md) (if applicable)
  - [System Rules / AGENTS.md](../../../../AGENTS.md) (if applicable)

---

## 1. Observed Problem
<!--
Describe the abnormal behavior in detail:
- Occurrence time and session/conversation ID
- Exact error messages, stack trace, or unexpected output
- Repro steps or trigger commands
-->

---

## 2. Alternative Hypotheses & Reject Evidence
<!--
⚠️ IMPORTANT GUIDELINE:
- Before naming a primary root cause, you must list and explicitly reject all alternative hypotheses.
- Root cause conclusions must be supported by quantitative evidence (e.g., measured counts, command/script output, file check results). Qualitative descriptions alone do not constitute proof.
- If a claim cannot be verified with a tool or quantitative data, it must be labeled a "Hypothesis" (hypothesis), not a "Conclusion" (conclusion).
-->

*   **Hypothesis A: [Hypothesis Name, e.g., API credentials expired or insufficient permissions]**
    *   *Verification / Rejection Evidence*: [e.g., Executing `gws tasks tasklists list` returned successfully with list output, rejecting this hypothesis.]
*   **Hypothesis B: [Hypothesis Name, e.g., Local temporary file missing or corrupted]**
    *   *Verification / Rejection Evidence*: [e.g., Verified that `.tmp/tasks.json` exists, is 12KB, and contains valid JSON structure, rejecting this hypothesis.]
*   **Hypothesis C: [Hypothesis Name, e.g., Code path did not handle empty array response]**
    *   *Verification / Rejection Evidence*: [e.g., Line 45 in `run.py` shows it throws an unhandled exception when list is empty, accepting this hypothesis.]

---

## 3. Root Cause

### 3.1 Primary Root Cause
<!--
State the core system defect, logic bug, or model hallucination point. Provide direct code or data evidence.
-->

### 3.2 Contributing Root Cause
<!--
Other factors that facilitated or contributed to the issue (e.g., lack of boundary condition checks, missing runtime assertions, insufficient logging).
-->

---

## 4. Fix Applied & Status Checklist

### 4.1 Fix Applied
<!--
Detail the modifications made to resolve the issue:
- Which files and lines were modified?
- What defensive programming strategy was implemented?
- Was a long-term improvement item added to backlog.md?
-->
1.  **Immediate/Direct Fix**: ...
2.  **Long-Term Defense**: ...

### 4.2 Status Checklist
<!--
Track the status of all relevant tasks.
-->
- [x] Reproduced and isolated the issue
- [ ] Wrote/executed automated tests to verify the fix (Note: manual verification is prohibited by project rules)
- [ ] Modified the affected skill code / configuration files
- [ ] Updated `backlog.md` (if long-term defensive mechanism is needed)
- [ ] Updated session decision log and `learnings/lessons.md` (if new gotchas were introduced)

---

## 5. References
<!--
List any related reference links or file paths (e.g. PRs, issues, external docs, discussion logs).
-->
- [GitHub Issue / PR Link]
- [Related Decision Log](../../../../docs/decision_logs/session_[session-id].md)

---
name: rca
description: Structured, evidence-backed Root Cause Analysis for workflow quality issues. Enforces quantitative hypothesis testing before naming a root cause. Use whenever a workflow produces unexpected, degraded, or inconsistent output.
version: 1.0.0
pattern: Investigator
---

# 🎯 Purpose

To guide a rigorous, forensically-grounded root cause analysis for any workflow quality issue. All conclusions must be backed by **measured evidence** — not qualitative observation. Every plausible alternative hypothesis must be explicitly tested and rejected before naming a primary root cause.

# 🚪 Trigger Conditions

Invoke when:
- A workflow produces output quality that is unexpectedly short, incomplete, or inconsistent
- A previously-fixed issue appears to have regressed
- The user says "why is X happening?" or "do RCA on Y"

> ⚠️ **No questions during analysis**: Run Steps 1–4 autonomously without asking the user anything. Use available tools (scripts, grep, file reads) to gather all evidence. Only stop to interact with the user at **Step 5** (approval gate) and **Step 6** (fix confirmation).

# ⚙️ Execution Steps

## Step 1: Measure First, Conclude Later

Before writing any prose, **run a measurement script** to quantify the problem:

```python
# Measure per-entry quality metrics from the output file
# e.g. section presence, line counts, bullet counts, batch position
```

Paste the raw output. This becomes the evidence base for all hypotheses.

## Step 2: Map the Pattern

From the measurements, identify:
- **Where** does quality drop? (which entries, which batch, which position within batch?)
- **What** is missing? (which sections are absent?)
- **Is there a gradient?** (monotonic decline = running-counter cause; flat plateau = constant cause; zigzag = content-driven cause)

## Step 3: Test Each Hypothesis Sequentially

Test in this order. Only move to the next if the current is rejected.

### Hypothesis A: Output Token Exhaustion
- **Prediction**: Quality declines **monotonically within each output pass** (later positions = worse)
- **Test**: Check if within-batch quality is monotonically non-increasing
- **Disproof signal**: Any later position has *more* content than an earlier one → non-monotonic → REJECTED

### Hypothesis B: Input Context Window Pressure
- **Prediction**: Quality declines **gradually across batches AND within each batch** as context accumulates
- **Test**: (1) Check cross-batch trend; (2) Check within-batch gradient; (3) Check for cross-entry content contamination (wrong metadata, blended content)
- **Partial support**: Cross-batch trend consistent but no within-batch gradient → Contributing factor only, not primary cause
- **Decision gate**: If partial support, document as "monitor only" with a specific re-evaluation trigger condition

### Hypothesis C: Source Content Quality
- **Prediction**: Degraded entries correspond to **short or incomplete source material** (teasers, paywalled previews)
- **Test**: Compare content depth of full-quality entries vs degraded entries. Look for structural markers (generic language, missing specifics, no CTAs in source)
- **Confirmation signal**: Degraded entries cluster around a specific sender format or content type

### Additional Hypotheses (as needed)
Add domain-specific hypotheses after ruling out A, B, C.

## Step 4: Write the RCA Document

Save to `docs/rca/<workflow_name>_rca_<YYYY-MM-DD>_V<version>.md` with these required sections:

```markdown
# RCA: <Title>

- **Date**: YYYY-MM-DD
- **Report Affected**: `path/to/report`
- **Workflow Version**: vX.Y.Z
- **Previous RCA**: (link if applicable)

## Observed Problem
(Hard data table from Step 1)

## Hypothesis Testing
### Hypothesis A: ...
### Hypothesis B: ...
### Hypothesis C: ...

## Root Cause Analysis
### 🔴 Primary: ...
### 🟡 Contributing: ...
### ❌ Ruled Out: ...

## Proposed Fix
### Option A / B / C

## Recommendation

## Status
- [ ] Root cause identified
- [ ] Fix applied
```

## Step 5: Present RCA & Await Approval

After completing the RCA document, **stop and present** the findings to the user:
- Summarize the primary root cause and the recommended fix option
- Link the saved RCA doc
- Ask for explicit approval: *"Shall I apply [Option X] as described?"*

**Do not apply any fix until the user says yes.**

## Step 6: Apply Fix & Update Changelog (After Approval)

Once the user approves:
- Apply the chosen fix to the workflow file
- Update `docs/workflow/<name>.md` changelog with the new version
- Cross-link: changelog entry → RCA | RCA status → changelog version
- Mark all status items `[x]`

# 📋 Evidence Standards

| Claim Type | Required Evidence |
|---|---|
| Token exhaustion | Monotonicity test result (pass/fail) + within-batch line counts |
| Context pressure | Cross-batch trend data + within-batch gradient + contamination check |
| Source content | Side-by-side depth comparison (full vs degraded entries) |
| Primary root cause | All alternatives explicitly rejected with data |
| Contributing factor | Cross-batch correlation data + documented re-evaluation trigger |

# 📁 Output Files

- RCA doc: `docs/rca/<workflow>_rca_<YYYY-MM-DD>_V<version>.md`
- Workflow fix: `.agents/workflows/<workflow>.md`
- Changelog update: `docs/workflow/<workflow>.md`
- Lessons learned: `learnings/lessons.md` (if new pattern discovered)

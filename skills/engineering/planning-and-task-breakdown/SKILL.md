---
name: planning-and-task-breakdown
description: Decomposes specifications into structured, ordered, and verifiable tasks using vertical slicing and dependency mapping.
version: 1.0.0
pattern: Generator
---

# 🎯 Purpose
To translate raw specifications or large feature requests into small, verifiable, and implementable tasks. Good task breakdown ensures reliable agent execution by defining explicit acceptance criteria, managing dependencies, and enforcing verification checkpoints.

# 🚪 Gating & Trigger Conditions
- **When to invoke:** - A formal specification or clear requirement document is provided.
  - A requested task feels too large, vague, or complex to start immediately.
  - Scope needs to be estimated or communicated to a human.
  - Work needs to be parallelized across multiple agents or sessions.
  - The implementation order of multiple components is not explicitly obvious.
- **When NOT to invoke:** - Single-file changes with obvious and constrained scope.
  - The provided specification already contains well-defined, granular tasks with acceptance criteria.

# 📥 Input Specifications
- **Project Context:** Existing architectural conventions, constraints, and dependencies.
- **Specification Document:** The feature request, PR description, or requirements text.
- **Codebase Access (Read-Only):** Access to relevant existing files to gauge impact and connections.

# ⚙️ Execution Instructions (Workflow)
1. **Enter Read-Only Plan Mode:** Read the specification and relevant codebase sections. Identify existing patterns, map dependencies, and note risks. Do NOT write or modify any application code during this step.
2. **Identify the Dependency Graph:** Map the component dependencies from the bottom up (e.g., Database Schema → API Models → API Endpoints → UI Components). 
3. **Slice Vertically:** Define tasks as complete feature paths (vertical slices) rather than horizontal architectural layers. 
   - *Example:* "Task: User Registration" (Schema + API + UI) instead of "Task: Build all schemas". 
4. **Draft Individual Tasks:** For each vertical slice, generate a task block that includes:
   - Paragraph description.
   - Specific, testable acceptance criteria.
   - Verification steps. **CRITICAL RULE:** Every verification step MUST be fully automated (no manual checks allowed). The verification plan MUST be explicitly split into the following three parts:
     1. **What to test:** Explain what has been done in this task and what specifically needs to be tested.
     2. **How to test:** Explain exactly how to test what was done in this task.
     3. **Expected behavior:** Explain what the expected output/behavior is when the test is run and *why* this behavior proves the task is complete.
   - Upstream task dependencies.
   - Estimated scope (XS to L).
5. **Enforce Size Constraints:** Evaluate the size of each drafted task. If a task is "XL" (touches 8+ files, spans multiple subsystems, or requires >3 acceptance criteria), decompose it further into 'S' or 'M' tasks.
6. **Order and Insert Checkpoints:** Arrange tasks sequentially so foundational dependencies are satisfied first. Insert a verification Checkpoint (requiring automated test passes) after every 2-3 tasks or at the end of a major phase.

*Fallback Behavior:* If the input specification is too ambiguous to define clear acceptance criteria, immediately halt the generator and output a list of clarifying questions for the human user.

# 📤 Output Specifications
- **Format:** A markdown document structured exactly as the `Implementation Plan`.
- **Required Sections:**
  - `## Overview`: One paragraph summary.
  - `## Architecture Decisions`: Key technical choices and rationale.
  - `## Task List`: Grouped by phases, containing structured task definitions and explicit `### Checkpoint` blocks.
  - `## Risks and Mitigations`: A markdown table of identified risks.
  - `## Open Questions`: Any unresolvable unknowns requiring human input.

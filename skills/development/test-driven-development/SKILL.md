---
name: test-driven-development
description: Drives development by enforcing a strict Red-Green-Refactor pipeline for features and a Prove-It pattern for bug fixes, completely language and framework agnostic.
version: 1.0.0
pattern: Pipeline
---

# 🎯 Purpose
To enforce a Test-Driven Development (TDD) methodology across all code modifications. This skill ensures that tests are written before implementation, acting as proof of functionality for new features and proof of reproduction for bug fixes.

# 🚪 Gating & Trigger Conditions
- **When to invoke:** - Implementing any new logic, behavior, or feature.
  - Fixing any reported bug (requires the Prove-It pattern).
  - Modifying existing functionality or adding edge-case handling.
  - Making any codebase change that could break existing behavior.
- **When NOT to invoke:** - Making pure configuration changes (e.g., modifying CI/CD YAML, environment variables).
  - Updating documentation (e.g., `README.md`).
  - Changing static content that has no behavioral or logical impact.

# 📥 Input Specifications
- **Task Context:** The feature requirement, user story, or bug report.
- **Target Files:** The specific source code files and corresponding test files to be modified.
- **Testing Framework:** The project's designated testing framework and syntax conventions.
- **Test Command:** The CLI command required to run the test suite.

# ⚙️ Execution Instructions (Workflow)

1. **Assess the Task Type (Feature vs. Bug):**
   - If a new feature: Proceed to Step 2.
   - If a bug fix (Prove-It Pattern): You MUST start by writing a test that reliably reproduces the bug based on the report before attempting any fix. 

2. **Phase 1: RED (Write a Failing Test)**
   - Draft a test focusing on the *state and outcome* rather than internal interactions or implementation details.
   - Favor DAMP (Descriptive And Meaningful Phrases) over DRY in test code to ensure readability.
   - **Execute the test runner.**
   - *Validation Check:* The test MUST fail. If it passes immediately, the test is invalid. Rewrite the test until it accurately fails due to the missing feature or presence of the bug.

3. **Phase 2: GREEN (Make it Pass)**
   - Write the absolute minimum production code required to make the failing test pass. Do not over-engineer or add speculative features.
   - **Execute the test runner.**
   - *Validation Check:* The test MUST pass. If it fails, revise the production code until the test passes.

4. **Phase 3: REFACTOR (Clean Up)**
   - Review the newly written, passing code.
   - Extract shared logic, improve naming, remove duplication, and optimize without altering the core behavior.
   - **Execute the test runner.**
   - *Validation Check:* The entire test suite must still pass.

5. **Fallback & Error Handling:**
   - *Missing Framework:* If the test execution command or framework is unknown, pause execution and prompt the user.
   - *Flaky Tests:* If tests fail intermittently, halt the pipeline. Investigate test isolation (ensure the test sets up and tears down its own state) and remove reliance on external I/O or non-deterministic data.

# 📤 Output Specifications
- **Test Code:** A completed test file containing the isolated, descriptive tests.
- **Source Code:** The minimal implementation required to pass the tests.
- **Execution Log:** A brief summary confirming the test failed (RED phase), the implementation was added, and the test subsequently passed (GREEN phase).

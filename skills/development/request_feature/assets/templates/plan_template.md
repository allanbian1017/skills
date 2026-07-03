# Implementation Plan - [Feature/Goal Name]

[Provide a brief summary of the implementation goal and what the changes accomplish.]

For the detailed technical architecture, design trade-offs, and decisions, please refer to the corresponding RFC/ADR: [RFC/ADR Name](../rfc/[rfc-filename].md).

## User Review Required
<!--
Document anything that requires user review or feedback, for example, breaking changes or significant design decisions. Use GitHub alerts (IMPORTANT/WARNING/CAUTION) to highlight critical items.
-->
> [!IMPORTANT]
> [Highlight any critical considerations, breaking changes, or user review items here.]

## Open Questions
<!--
Any clarifying or design questions for the user that will impact the implementation plan.
-->
- [Open Question 1]
- [Open Question 2]

---

## Proposed Changes

### [Component/Module Name 1]
<!--
Group changes logically by component, area, or layer.
-->

#### [NEW] [file_name](relative/path/to/new_file)
<!-- Use [NEW] to demarcate new files. -->
* [Description of the new file's responsibility and structure.]

#### [MODIFY] [file_name](relative/path/to/modified_file)
<!-- Use [MODIFY] to demarcate existing files. -->
* [List of logical changes, updates, or functions being refactored/modified.]

---

### [Component/Module Name 2]

#### [DELETE] [file_name](relative/path/to/deleted_file)
<!-- Use [DELETE] to demarcate deleted files. -->
* [Rationale for deleting this file.]

---

## Verification Plan

### Automated Tests
<!--
The commands of any automated tests you will run, following the standard validation format.
-->
- **What to test**: [Description of the component or behavior being tested]
  - **How to test**: [Commands or scripts to run the tests, e.g., `pytest tests/test_filename.py`]
  - **Expected behavior**: [What success looks like, e.g., all 5 tests pass, exit code 0]

### Manual Verification
<!--
Manual verification steps if automated tests are not fully sufficient (e.g., visual layout checks, end-to-end command outputs).
-->
1. [Step 1]
2. [Step 2]
3. [Expected outcome and how to verify]

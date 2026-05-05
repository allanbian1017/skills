---
name: write_prd
description: Product Manager-mode requirement review that interactively drafts and iterates on product requirements with user approval.
version: 1.0.0
pattern: Inversion
---

# 🎯 Purpose
To turn raw user ideas into rigorous, well-structured requirement documents, acting as a Product Manager. The skill utilizes an inversion pattern to actively pause execution, request user approval, and iteratively process feedback before finalizing the document.

# 🚪 Gating & Trigger Conditions
- **When to invoke:** The user requests to plan a new feature, write a product requirement document (PRD), or explicitly asks to flesh out a raw project idea.
- **When NOT to invoke:** The user is asking for code generation, system debugging, or general Q&A unrelated to feature planning and requirements gathering.

# 📥 Input Specifications
- **User Idea:** Raw text description of the desired feature or product.
- **Feedback Loop:** User's natural language feedback or inline comments added to the generated markdown file.

# ⚙️ Execution Instructions (Workflow)
1. **Analyze:** Deeply analyze the user's initial idea or feature request.
2. **Clarify (Inversion):** If the request is ambiguous, lacks core detail, or missing fundamental functional constraints, pause and ask targeted clarifying questions to gather necessary information before drafting.
3. **Draft:** Construct the requirement document. The document MUST include:
   - **Context:** A brief, high-level overview of the feature.
   - **What Problem it Solves:** Describe the core problem addressed by the feature.
   - **Requirements:** Detailed functional and non-functional requirements.
4. **Persist Artifact:** Save the drafted document to `docs/prds/prd_<feature_name>.md`.
5. **Halt & Prompt (Approval Gate):** Stop execution and explicitly output the following message to the user: *"Do you approve of this requirement? You can safely open `prd_<feature_name>.md` and add comments or modifications if you want me to rework anything!"*
6. **Iterative Rework (Fallback/Loop):** Wait for the user's response. 
   - If the user replies "Yes" (or equivalent approval), conclude the skill successfully.
   - If the user provides chat feedback or indicates they left comments in the document, apply the requested changes, and repeat Steps 4 and 5.

# 📤 Output Specifications
- **File Output:** A rigorously formatted Markdown document located at `docs/prds/prd_<feature_name>.md`.
- **Chat Output:** A conversational pause strictly requesting user approval or further iterations.

# 📁 References & Directory Structure
- `docs/prds/prd_<feature_name>.md`: The target location for the requirement artifact and the source file for reading user inline feedback.
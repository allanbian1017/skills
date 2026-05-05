---
name: insight
description: Analyzes the current Antigravity conversation history to suggest workflow improvements, feature adoption, and AGENTS.md updates.
version: 1.0.0
pattern: Generator
---

# 🎯 Purpose
To analyze the user's active Antigravity session and conversation history to generate highly relevant, actionable recommendations for workflow optimization. This includes identifying repetitive instructions to add to `AGENTS.md`, suggesting specific Antigravity features (like MCP Servers or Hooks), and defining reusable usage patterns.

# 🚪 Gating & Trigger Conditions
- **When to invoke:** When the user explicitly requests an analysis of "this conversation", asks to review the current session's workflow, or runs the specific skill command.
- **When NOT to invoke:** During standard code generation, debugging, or when the conversation history is too short to extract meaningful patterns (e.g., at the very beginning of a session).

# 📥 Input Specifications
- `conversation_history`: The active context window containing the back-and-forth dialogue, prompts, and responses from the current session.
- `features_reference`: The static list of Antigravity capabilities (MCP Servers, Custom Skills, Hooks, Headless Mode, Task Agents) provided in the system instructions.

# ⚙️ Execution Instructions (Workflow)
1. **Analyze Active Context:** Scan the current `conversation_history` loaded in your memory.
2. **Extract Repetitive Patterns:** Identify specific instructions, corrections, or preferences the user has had to state multiple times during this session (e.g., "always use TypeScript", "remember to format the output").
3. **Map to `AGENTS.md`:** Draft additions for `AGENTS.md` based *only* on the repetitive patterns identified in Step 2.
4. **Feature Matching:** Review the `features_reference` list. Select 2-3 features that directly solve pain points or automate the repetitive tasks observed in the current conversation. Include 2-3 items for each category if applicable.
5. **Formulate Usage Patterns:** Identify 2-3 broader workflow habits from the session that could be optimized, drafting copyable prompts to help the user adopt these habits in future sessions.
6. **Construct Output:** Generate a well-structured Markdown document organizing the findings into clear sections.
7. **Validation (Fallback):** If the generated output contains conversational filler outside the requested Markdown structure, discard the filler and output only the strict Markdown report.

# 📤 Output Specifications
- **Format:** A formatted Markdown document.
- **Structure Template:**
  ```markdown
  # 📊 Antigravity Session Analysis

  ## 📝 AGENTS.md Additions
  *(Based on repeated instructions in this conversation)*
  
  - **[Proposed Addition Text]**
    - **Why:** [1 sentence explaining why this helps based on the session]
    - **Implementation:** [Instructions for where to add this in AGENTS.md]

  ## 🚀 Features to Try
  
  ### [Feature Name]
  - **Overview:** [What it does in one line]
  - **Why it fits your workflow:** [Explanation based on the active conversation context]
  - **How to use it:**
    \`\`\`[language]
    [Actual command or config to copy]
    \`\`\`

  ## 🔄 Recommended Usage Patterns
  
  ### [Short Title]
  - **Suggestion:** [1-2 sentence summary]
  - **Details:** [3-4 sentences explaining how this applies to the work done in this session]
  - **Try this prompt:**
    > [A specific prompt to copy and try]

  ## 📁 References & Directory Structure
  - AGENTS.md: The target file for global agent instructions.
  - .agents/settings.json: Configuration file referenced for Hooks.
  - .agents/skills/: Directory referenced for Custom Skills.

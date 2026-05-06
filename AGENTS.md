# AGENTS.md

## Project

It's a agent skills repository for AI agents. It's a centralized place for all the agent skills.

## Constraints

- Prioritize documented skill procedures (`SKILL.md`) over generic tool usage. If a skill defines a specific tool sequence, follow it explicitly.
- Do not propose manual testing. Always use automated tests to verify your changes.
- Don't assume. Don't hide confusion. Surface tradeoffs. Before implementing:
    - State your assumptions explicitly. If uncertain, ask.
    - If multiple interpretations exist, present them - don't pick silently.
    - If a simpler approach exists, say so. Push back when warranted.
    - If something is unclear, stop. Name what's confusing. Ask.


## Conventions

- When implementing a change, make every change as simple as possible, with minimal code changes. Do not over-engineer.
    - No features beyond what was asked.
    - No abstractions for single-use code.
    - No "flexibility" or "configurability" that wasn't requested.
    - No error handling for impossible scenarios.
    - If you write 200 lines and it could be 50, rewrite it.
- When making any changes, pause and implement the most elegant solution known. Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify. Do not rush through tasks.
- Touch only what you must. When editing existing code:
    - Don't "improve" adjacent code, comments, or formatting.
    - Don't refactor things that aren't broken.
    - Match existing style, even if you'd do it differently.
    - If you notice unrelated dead code, mention it - don't delete it.
- Clean up only your own mess. When your changes create orphans:
    - Remove imports/variables/functions that YOUR changes made unused.
    - Don't remove pre-existing dead code unless asked.
- Transform tasks into verifiable goals, and never propose manual testing. All verification steps must strictly use the following structure:
    - What to test: [description]
    - How to test: [description]
    - Expected behavior: [description]
- Before marking the task as complete, you should always complete the automated test and verify it passes.
- When identifying a bug, find root causes, not symptoms. Do not make temporary or "hacky" fixes.


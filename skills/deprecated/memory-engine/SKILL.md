---
name: memory-engine
description: A memory management and learning system for Antigravity. Use this skill whenever the user issues a memory command like save, reload, handoff, reflect, todo, learn, or any other memory-related commands. This skill enables the agent to store context across sessions, maintain a reflection diary, track cross-project tasks, and learn from mistakes.
---

# Memory Engine

A memory and learning system for Antigravity. This skill allows you to manage conversation state, track tasks, reflect on pitfalls, and hand off context between sessions using your active context and file system tools.

## Architecture & Directories
- **Global Memory**: `~/.gemini/antigravity/memory/` (Used for overarching tasks, error logs, and diaries).
- **Project Memory**: `.agents/memory/` in the active workspace (Used for project-specific context, learned pitfalls, and handoffs).

## Commands

Whenever the user issues one of the following commands, you MUST use `view_file` to read the corresponding instruction file in `/Users/allanbian/my-ai-workflow/.agents/skills/memory-engine/commands/<command>.md` and follow its detailed execution steps. Always confirm what you did with a short summary to the user.

| Command | Action you must take |
| :--- | :--- |
| `save` | Read `commands/save.md` and execute the steps to append context to `.agents/memory/context.md`. |
| `reload` | Read `commands/reload.md` and load past context into your current working memory. |
| `todo` | Read `commands/todo.md` and manage cross-project tasks in `~/.gemini/antigravity/memory/todo.md`. |
| `backup` | Read `commands/backup.md` and execute the push backup script. |
| `sync` | Read `commands/sync.md` and execute the sync backup script. |
| `handoff` | Read `commands/handoff.md` and summarize uncompleted tasks for next session. |
| `diary` | Read `commands/diary.md` and summarize today's session in `~/.gemini/antigravity/memory/diary.md`. |
| `reflect` | Read `commands/reflect.md` and analyze recent logs for patterns or repeated mistakes. |
| `learn` | Read `commands/learn.md` and manually extract a pitfall or lesson. |
| `analyze` | Read `commands/analyze.md` and log new rules or errors. |
| `correct` | Read `commands/correct.md` and remind yourself of past mistakes. |
| `check` | Read `commands/check.md` and verify memory folders structure. |
| `full-check` | Read `commands/full-check.md` and audit all memory files. |
| `memory-health` | Read `commands/memory-health.md` and report capacity warnings. |
| `memory-search` | Read `commands/memory-search.md` and search across memory files. |
| `recover` | Read `commands/recover.md` and execute the pull backup script. |
| `compact-guide` | Read `commands/compact-guide.md` and output a guide on when to compact memories. |
| `overview` | Read `commands/overview.md` and output a formatted table of commands to the user. |

## Important Rules
1. **Never guess the memory content**: Always rely on your active context or by reading the memory files with `view_file`.
2. **Be specific**: When writing to memory files, be concise. Include timestamps when appending new entries.
3. **Pointers, not dumps**: If a memory file is getting too long (over 150 lines), create a pointer to a standalone file in the same directory rather than dumping everything into one file.

# Memory Engine Skill

A powerful memory management and learning system for Antigravity, ported from the [claude-memory-engine](https://github.com/HelloRuru/claude-memory-engine). This skill enables persistent memory across sessions, structured reflection, and automated pitfall learning.

## Overview

The Memory Engine allows Antigravity to:
- **Persist Context**: Save key decisions and progress to local files.
- **Learn from Mistakes**: Automatically record and reference technical pitfalls.
- **Hand Off Work**: Create structured handoff files for future sessions.
- **Perform Reflections**: Periodically audit memory files to consolidate knowledge.

## Architecture & Directories

Memory is stored in two primary locations:

- **Global Memory (`~/.gemini/antigravity/memory/`)**: Used for overarching tasks, the reflection diary, and the error notebook.
- **Project Memory (`.agents/memory/`)**: Used for project-specific context, learned pitfalls, and session handoffs.

## Commands

Commands are invoked using the syntax: `/memory-engine {command}`.

| Command | Description |
| :--- | :--- |
| `save` | Summarize key progress and append to `.agents/memory/context.md`. |
| `reload` | Load past context from the project memory into the current session. |
| `todo` | Manage cross-project tasks in the global `todo.md`. |
| `backup` | Push memory files to a backup repository (requires `scripts/memory-backup.sh`). |
| `sync` | Perform a two-way sync (push/pull) of memory files. |
| `handoff` | Create a `handoff-*.md` file for the next session. |
| `diary` | Write a reflection entry to the global `diary.md`. |
| `reflect` | Analyze recent logs for patterns, mistakes, and knowledge consolidation. |
| `learn` | Manually or automatically extract lessons into `learned.md`. |
| `analyze` | Review recent corrections and log them to the global `error_notebook.md`. |
| `correct` | Load the error notebook to remind Antigravity of past mistakes. |
| `check` | Quick health check of memory folder structure and file status. |
| `full-check` | Comprehensive audit of all memory files for redundancy and bloat. |
| `memory-health` | Report file sizes and capacity warnings. |
| `memory-search` | Search for specific keywords across all memory files using `grep`. |
| `recover` | Pull memory files from a backup repository. |
| `compact-guide` | View guidelines on when to compact memories to stay within context limits. |
| `overview` | Display a formatted table of all available commands. |

## Important Rules

1. **Context First**: Antigravity should never guess memory content; it must read the files using `view_file` or `grep_search`.
2. **Conciseness**: Memory entries should be specific and include timestamps where applicable.
3. **Hub-and-Spoke Model**: When a memory file (like `context.md` or `todo.md`) exceeds 150 lines, it should be split into topic-specific files to maintain performance.

## Installation

This skill is located in `.agents/skills/memory-engine/`. To use it:
1. Ensure the directory structure exists in your project (`.agents/memory/`).
2. Antigravity will automatically detect the skill and its commands.
3. For backup/sync features, configure the Git repository in `scripts/memory-backup.sh`.

---
*Derived from HelloRuru's Claude Memory Engine.*

# memory-health -- Memory Health Check

Check the health status of all memory files and hooks.

## Steps

1. **Scan memory directory**: `~/.claude/projects/{project-id}/.agents/memory/`
2. **Scan sessions directory**: `~/.gemini/antigravity/memory/`
3. **Scan diary directory**: `~/.gemini/antigravity/memory/diary.md (append to this file) `
4. **Scan learned directory**: `.agents/memory/learned/`
5. **Check debug log**: `~/.gemini/antigravity/memory/debug.log`

## Output Format

```
Memory Health Report

MEMORY.md level: {lines}/200 ({percent}%) {Safe/Warning/Critical}

Memory files:
| File | Lines | Last Updated | Status |
|------|-------|-------------|--------|
| {filename} | {lines} | {date} | {OK/Stale/Too Large} |

Sessions: {N} total, latest: {date}
Diary entries: {N} total, latest: {date}
Pitfall records: {N} total, latest: {date}
Learned Skills: {N} total

Hooks status:
- session-start.js: {OK/Error}
- session-end.js: {OK/Error} (debug.log last: {msg})
- memory-sync.js: {OK}
- write-guard.js: {OK}
- pre-push-check.js: {OK}
```

## Thresholds
- MEMORY.md < 170 lines -> Safe
- MEMORY.md 170-200 lines -> Warning, suggest moving content to topic files
- MEMORY.md > 200 lines -> Critical, content beyond line 200 is truncated by Antigravity
- Memory file not updated for 30+ days -> Stale
- Memory file over 200 lines -> Too Large

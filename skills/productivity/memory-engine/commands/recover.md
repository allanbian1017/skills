# recover -- Disaster Recovery + Cross-Device Sync

Restore memory from your GitHub backup when local memory files are lost or corrupted. Also works for cross-device sync.

## Prerequisites

You need a GitHub repo set up as your memory backup (the one you push to with `/backup` or `/sync`). If you haven't created a backup repo yet, this command won't work.

## Cross-Device Sync (v1.6)

```bash
bash ~/.claude/scripts/hooks/memory-backup.sh pull
```

The `pull` mode does two things:
1. `git pull` from GitHub to get the latest
2. Distribute `repo/.agents/memory/*.md` into every local project directory that has a `.agents/memory/` folder (newer file wins, won't overwrite local changes)

This solves the "Device A pushed but Device B can't see it" problem -- each device has different working directories, so `projects/` paths differ. Global memory must be actively distributed.

## When to Use

- Switched to a new computer and need to bring over memories from another device
- Local memory files were accidentally deleted
- SessionStart hook isn't working
- Memory files appear corrupted or empty
- Another device pushed new memory and you want to pick it up (for routine use, `/sync` is more convenient)

## Steps

1. **Protect current state** -- Run `/backup` first to push any remaining local changes
2. **Pull from GitHub** -- `bash ~/.claude/scripts/hooks/memory-backup.sh pull`
3. **Verify** -- Read MEMORY.md, scan all index entries
4. **Report** -- "Recovered! Found {N} index entries, {M} memory files"

## Notes

- Under normal conditions, SessionStart hook auto-loads the last session summary + recent memory changes. You should NOT need this command regularly
- This is the "break glass" option for when the automated system fails
- Always push before pulling to avoid overwriting local changes

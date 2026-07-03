# sync -- Bidirectional Memory Sync

Sync memory between your local machine and GitHub backup — both directions.

## Usage

```bash
# Bidirectional: pull latest from GitHub, then push local changes
bash ~/.claude/scripts/hooks/memory-backup.sh sync

# Push only (same as /backup)
bash ~/.claude/scripts/hooks/memory-backup.sh push

# Pull only (same as /recover)
bash ~/.claude/scripts/hooks/memory-backup.sh pull
```

## What sync does

1. **Pull** — `git pull` from GitHub, then distribute `repo/.agents/memory/*.md` into every local `projects/*/.agents/memory/` directory (newer file wins)
2. **Push** — scan all local `projects/*/.agents/memory/` directories, copy to the backup repo, commit, and push

## When to use

- Switching between devices (laptop vs desktop) — run `/sync` to get the other device's latest memory
- After a long offline session — push your changes and pull anything new
- If you're unsure whether you have the latest — `/sync` is always safe

## Notes

- The pull step only overwrites files when the GitHub version is newer than the local version
- The SessionEnd hook auto-commits locally after every conversation
- This command handles the **push + pull** to remote (GitHub)
- `/backup` = push only; `/recover` = pull only; `/sync` = both

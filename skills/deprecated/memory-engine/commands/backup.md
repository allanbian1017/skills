# backup -- Push Memory to GitHub

Push local memory files to your GitHub backup repository.

## Usage

```bash
bash ~/.claude/scripts/hooks/memory-backup.sh push
```

## What it does

1. **Scan all projects** -- find every `~/.claude/projects/*/.agents/memory/` directory
2. **Copy to backup repo** -- mirror all `.md` files into the backup repo
3. **Commit** -- stage and commit changes
4. **Push** -- push to GitHub

## Notes

- The SessionEnd hook auto-commits locally after every conversation; this command handles the push
- v1.6: push now auto-detects all project directories instead of hardcoding paths
- For bidirectional sync (push + pull), use `/sync` instead
- For pulling from GitHub, use `/recover`

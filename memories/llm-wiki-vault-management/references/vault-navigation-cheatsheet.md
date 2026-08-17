---
tags: [reference, cheat-sheet, vault-navigation]
created: 2026-08-17
last-updated: 2026-08-17
---

# Vault Navigation Cheatsheet

Quick reference commands for Obsidian vault management.

## Directory Structure Commands

```bash
# List vault contents
ls -la "E:/tommy vault/tommy vault/Read & Write/"

# Find all markdown files
find "E:/tommy vault/tommy vault/Read & Write" -name "*.md"

# Count notes per directory
find "E:/tommy vault/tommy vault/Read & Write" -type f -name "*.md" -exec dirname {} \; | sort | uniq -c

# Find notes missing frontmatter
find "E:/tommy vault/tommy vault/Read & Write" -name "*.md" -exec grep -L "^---" {} \;
```

## Obsidian Operations

```bash
# Open specific note in Obsidian
# Use: obsidian://open?vault=Read%20%26%20Write&file=master_index

# Search for tags
# Ctrl+Shift+F → "tags:" in frontmatter

# Export graph view (PNG)
# Obsidian → Command Palette → "Export Graph"
```

## Wikilink Validation

```bash
# Check for broken wikilinks (manual pattern)
grep -oE '\[\[[^\]]+\]\]' *.md | sort | uniq -c

# Find orphaned notes (no links in/out)
# Use Obsidian's "Unlinked Mentions" plugin or graph view
```

## Backup Operations

```bash
# Quick backup to timestamped folder
cp -r "E:/tommy vault/tommy vault/Read & Write" "/backups/vault-$(date +%Y%m%d-%H%M)"

# Git-based tracking
git add . && git commit -m "Vault update $(date +%Y-%m-%d)"
```

## Tag Reference

| Domain Tag | Purpose | Folder Location |
|------------|---------|-----------------|
| `cnc` | CNC machining, G-code | `memories/` |
| `ai-model` | Model docs, benchmarks | `ai-models/` |
| `robotics` | Robot control, vision | `CNC n Robotic/` |
| `python` | Scripts, automation | `coding/` |
| `obsidian-hermes` | Integration workflows | `memories/` |

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| Links not clickable | Misspelled note name | Use `/` autocomplete in Obsidian |
| Graph view empty | Missing frontmatter | Add `---\n---` to note |
| Tags not filtering | Wrong folder | Tags work across vault |
| `sed: not found` | Git Bash on Windows | Use `grep` or Python instead |
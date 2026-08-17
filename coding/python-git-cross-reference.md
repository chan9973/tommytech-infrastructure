---
created: 2026-08-15T12:10:00+08:00
tags: [cross-reference, testing, inter-linking]
---

# Cross-Reference Linking Demo

## Purpose

This note demonstrates how to link related concepts via wikilinks (`[[ ]]`). Clickable links in Obsidian create a "web" of knowledge.

---

## Links From This Note

| Linked To | Topic | Connection |
|-----------|-------|-------------|
| [[git-commands-reference]] | Git commands | Version control for code repos (parallel to ML project setup) |
| [[python-async-tutorial]] | Async Python | Performance optimization for concurrent tasks |
| [[deep-learning-fundamentals]] | Deep learning | Research context (hierarchical feature learning) |
| [[unknown-user-input]] | Raw research notes | User-provided examples and data |

---

## Links To This Note

These topics reference this cross-reference list:

- [[coding/git-commands-reference]] — Mentions performance tips from `[[python-async-tutorial]]`
- [[coding/python-async-tutorial]] — References [[deep-learning-fundamentals]] for optimization techniques

---

## How Cross-Referencing Works

1. In any markdown file, write: `[[note-name-here]]`
2. Obsidian renders it as a clickable link
3. Clicking shows the linked note
4. Backlinks automatically show who references this note

**Example:**

Write in `git-commands-reference.md`:
```markdown
## Advanced Topics
See [[python-async-tutorial]] for performance tips on large commits.
```

This creates a bidirectional link!

---

## Benefits of Cross-Referencing

1. **Context discovery**: Find related topics you didn't know existed
2. **Knowledge mapping**: Visualize how concepts connect
3. **Auto-completion**: Obsidian suggests links from filenames (e.g., type `git[[ ]]` → completes to `[[git-commands-reference]]`)
4. **Research threads**: Track how ideas evolve across notes

---

## Quick Reference

| Task | How To |
|------|--------|
| Create link | Write `[[target-note-name]]` (case-sensitive!) |
| Add backlink note | Edit target note, add new section linking this one |
| View all links to this note | Use Obsidian graph view or `/backlinks` search |
| Rename linked note | Update wikilink text to match new filename |

---

## Example: Creating a Knowledge Graph

1. Start with one concept: `[[python-async-tutorial]]`
2. Note related topics → create notes and link them:
   - Performance tips → link to [[git-commands-reference]]
   - Optimization techniques → link to [[deep-learning-fundamentals]]
3. Repeat for each new note

Result: A web of interconnected knowledge! 🕸️

See [[deep-learning-fundamentals]], [[python-async-tutorial]], [[unknown-user-input]] for examples in this demo vault.

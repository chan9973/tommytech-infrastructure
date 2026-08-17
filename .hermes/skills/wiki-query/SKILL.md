---
name: obsidian-wiki-query
description: Search Obsidian wiki for topics, cross-reference notes.
version: 1.0.0
author: Tommy Chan (tommychan), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Obsidian, Wiki, Search, Query]
    related_skills: [obsidian, github-issues]
---

# Obsidian Wiki Query Skill

Search your Obsidian vault for topics and cross-reference knowledge across notes.

## When to Use

- User asks: "What do I know about X?" → search wiki for all mentions
- Research session: Find relevant notes for a topic
- Cross-linking: "Add links from A note to B note" → find matching [[wikilinks]]
- Contradiction check: Compare conflicting info on the same topic

## Prerequisites

- Your Obsidian vault is set up and contains `.md` notes
- `OBSIDIAN_VAULT_PATH` env var or default to `E:/tommy vault/tommy vault/Read & Write`

## How to Run

```python
from hermes_tools import search_files, read_file

def query_observations(query, n=5):
    """Search wiki for query term"""
    vault_path = os.environ.get("OBSIDIAN_VAULT_PATH") or "E:/tommy vault/tommy vault/Read & Write"
    
    # Use search_files with content regex
    matches = search_files(
        pattern=f'\\b{re.escape(query)}\\b',
        target="content",
        path=vault_path,
        file_glob="*.md",
        limit=n,
        output_mode="content"
    )
    
    return matches

# Example: query_observations("machine learning")
```

## Quick Reference

- Search term: `query_observations("<topic>")`
- List all notes in a directory: `search_files(target="files", path="coding/")`
- Get note content: `read_file(path="coding/python/advanced.md")`
- Count tags usage: `search_files(pattern="---\\ntag:", target="content", path=".") | grep count`

## Procedure

### Search for Topic Mentions

1. User asks: "What do I know about Python?"
2. Call `query_observations("Python")` with n=10 (top 10 mentions)
3. For each match: `read_file(path="...")` to get context
4. Extract:
   - File path → relative link to user's vault
   - First 5 lines of content → quick preview
   - Tags from YAML frontmatter → categorize results
5. Format response with wikilinks:

```markdown
## What I found about [[Python]]

1. `E:/tommy_vault/tommy_vault/Read&Write/coding/python basics.md`
   > Python supports multiple programming paradigms including OOP and functional programming...

2. `E:/tommy_vault/tommy_vault/Read&Write/memories/facts.md`
   > My preferred Python interpreter is python3 (3.14.7)...
```

### Find Note Links

1. User says: "Add a link from note A to note B"
2. Read note A with `read_file(path=".../noteA.md")`
3. Search for missing references using `search_files(target="content", pattern=r'\\[\\[([^]]+)\\]\\](?!(?P=target_noteA))')`
4. Suggest: "Add `[[Python Advanced]]` since you discuss this in `noteB.md`"

### Cross-check for Contradictions

1. Read multiple notes on same topic via parallel reads
2. Compare key statements (e.g., API endpoints, configuration defaults)
3. Flag contradictions with diff-style message:

```diff
- Note A says: "Default port is 8080"
+ Note B states: "Port should be 9000 for production"
>> ⚠️ Contradiction detected — review both notes to resolve
```

## Pitfalls

- **Case sensitivity**: Search matches are case-insensitive by default. If you need exact match, use `search_files(pattern="^Query$")`.
- **Special characters**: Use regex escaping for `?`, `*`, `[`, `]` in search terms.
- **Obsidian vault path**: Windows paths with spaces (`E:/tommy vault/`) — always use double-quotes or escape spaces.
- **Wikilink syntax**: In Obsidian, `[[note name]]` renders clickable link; don't add `| Display Name` unless configured in `.cursorrules/metadata`.
- **Large note files**: 10K+ line notes → trim previews to first 50 lines before sharing.

## Verification

1. Search returns at least one result for known topic (test with "facts" or "profile")
2. Extracted snippets are valid markdown (check for trailing whitespace, proper heading levels)
3. Wikilinks use `[[note_name]]` format
4. Tags conform to expected convention (e.g., `machine-learning`, not `machine learning`)

## Example Workflow

1. **User**: "Summarize everything I've written about Git commands"
2. **Hermès**: `query_observations("git")` → list all matches
3. **Hermès**: For each file, `read_file(path="...")` → extract relevant sections
4. **Hermès**: Combine into summary with cross-references to original notes

```markdown
## Your Git Knowledge Base

### Command Cheat Sheet
- `git commit -m "message"` — create commit — described in [[coding/ubuntu commads.md]](commit)
- `git rebase --interactive` — interactive rebase — see [[coding/git-workflows.md]](rebasing)

### Notes to Review
- [[coding/github-auth.md]] — SSH key setup (dated 2025-10)
```

## Advanced: Query API Call Example

Use in a custom Hermès skill or automation script:

```python
import os, re, glob

def search_wiki(query, vault_path=None, limit=10):
    if not vault_path:
        vault_path = os.environ.get("OBSIDIAN_VAULT_PATH") or "E:/tommy vault/tommy vault/Read & Write"
    
    # Use search_files (Hermès tool)
    matches = search_files(
        pattern=rf'{{re.escape(query)}}',
        target="content",
        path=vault_path,
        file_glob="*.md",
        limit=limit,
        output_mode="content"
    )
    
    # Format results
    results = []
    for match_text in matches:
        # Extract relative path and snippet (first 2 lines)
        lines = match_text.split('\n')[:3]
        results.append({
            "path": os.path.relpath(os.path.dirname(match_text), vault_path).replace("\\", "/"),
            "snippet": '\n'.join(lines),
            "tags": re.search(r'tags: (.+)', match_text, re.IGNORECASE)
                and [i.strip().strip('"\'') for i in re.findall(r'\[(\S+)\]', match_text)] or None
        })
    
    return results
```

## Maintenance Tips

- Regularly tag notes to improve searchability
- Use properties (YAML frontmatter) over tags for filtering capabilities
- Archive old notes into `E:/tommy vault/tommy vault/Read & Write/archive/` to keep search clean

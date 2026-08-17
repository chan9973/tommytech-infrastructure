---
name: obsidian-wiki-ingest
description: Ingest external content into Obsidian wiki automatically.
version: 1.0.0
author: Tommy Chan (tommychan), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Obsidian, Wiki, Knowledge Management]
    related_skills: [obsidian, youtube-content]
---

# Obsidian Wiki Ingestion Skill

Automatically add external content (web articles, transcripts, research) into your Obsidian wiki without manual copying.

## When to Use

- User provides a URL or text to store in the wiki
- Research session ends — summarize key points into a note
- YouTube transcript comes from `youtube-content` skill — add as detailed context note
- Web article read via `web_extract` — create summary + source note

## Prerequisites

- Obsidian vault path (default: `E:/tommy vault/tommy vault/Read & Write`, check `env:OBSIDIAN_VAULT_PATH`)
- Optional: API key for advanced tools (Notion, Readwise, etc.)

## How to Run

```python
from hermes_tools import terminal

# Quick usage via CLI
python E:/tommy\ vault/tommy\ vault/Read\ &\ Write/.hermes/wiki_helper.py "machine learning" --vault "E:/tommy vault/tommy vault/Read & Write"

# Via Hermes prompt (skill invocation)
hermes ingest url https://example.com/article --tags machine-learning,summary
```

## Quick Reference

- Ingest from URL: `python wiki_helper.py --url <url> --format notes`
- Ingest transcripts: `youtube-content summary <video_id>` → pipe to wiki
- Search query: `python wiki_helper.py "<search query>"`
- List all notes: `find "E:/tommy vault/tommy vault/Read & Write" -name "*.md" | wc -l`

## Procedure

### Option 1: Simple Search Query

1. User asks: "What do I know about quantum computing?"
2. Run: `python wiki_helper.py "quantum computing"`
3. Results appended to chat response with wikilinks

### Option 2: URL to Wiki Note

1. User provides URL: `https://arxiv.org/abs/2305.xx`
2. Extract content via `web_extract(url)` or CLI tool
3. Create note at `Obsidian/wikipedia/<date>-<title>.md`:
   ```markdown
   ---
   tags: [summary, arxiv]
   source-url: https://arxiv.org/abs/2305.xx
   last-updated: {{datetime}}
   ---

   ## Source
   [[wikipedia/Quantum Computing Papers|Original article]]

   ## Key Points

   (Extracted content...)

   ## Questions to Research Next
   - What does this imply for X? [[X research note]]
   ```

### Option 3: YouTube Transcript Integration

1. Use `youtube-content` to get transcripts
2. Summarize with Claude or Hermes prompt
3. Write condensed summary + detailed link to full transcript
4. Tag appropriately for searchability

## Pitfalls

- **Vault path issues**: Windows spaces in paths (`E:/tommy vault/...`) — use backslashes or double-quotes
- **Duplicate detection**: Add title/hash check to avoid writing same content twice
- **Markdown rendering**: Obsidian links use `[[wikilink]]`, not `[[wikilink|Alias]]` unless configured
- **Tags vs properties**: Tags are quick categorization; properties (YAML frontmatter) enable better filtering

## Verification

1. Search query returns expected results via `search_files(target="content")`
2. Generated notes exist with proper markdown syntax
3. Wikilinks resolve to existing or future-created notes
4. Tags match expected format

## Alternative: Auto-run on Cron

```cron
# Add this job to cronjob tool
action=create, schedule='every 2h', prompt="Scan GitHub for project updates; add changelogs to wiki. Read repo from E:/tommy vault/tommy vault/Read & Write/coding/", skills=["github"]
```

## Advanced: Connect to Hermes Memory

For users wanting full Hermès memory persistence + Obsidian synergy:

1. Set `OBSIDIAN_VAULT_PATH` env var or config default
2. Update `hermes-agent` prompts to check vault before answering queries
3. Use skill prompt: "Before answering, search user's [[Obsidian Wiki]] for related context"
4. For read-only wiki access (no writing), use pure search pattern

## Example Workflow

1. **User**: "Summarize this paper: https://..." → hermès writes `E:/tommy.../papers/2025-NNN-arxiv.md`
2. **Hermès**: User later asks "What did I read about X?" → queries wiki for matches
3. **User**: Hermès responds with summarized insights from scattered notes, cross-linked via wikilinks

## Maintenance

- Schedule weekly: "Consolidate [[temp notes]] into main [[topics]] index"
- Monthly: Review tags for cleanup; merge duplicate topics
- Quarterly: Export wiki to PDF backup or Notion for sharing

# Hermès + Obsidian Wiki Integration Setup Guide

**Status**: v1.0 — Basic setup complete; ready for testing.

## What You Now Have

| File | Purpose |
|------|---------|
| `.hermes/scripts/wiki_ingest.py` | CLI script to ingest URLs/text into your vault |
| `.hermes/skills/wiki-query/SKILL.md` | Hermès skill to query wiki |
| `.hermes/prompts/wiki-context-prompt.md` | Prompt template for answering queries with context |
| `.hermes/README.md` | This quickstart guide |

## Quick Start (5 minutes)

### Step 1: Test Ingestion

```bash
cd "E:/tommy vault/tommy vault/Read & Write"
python .hermes/scripts/wiki_ingest.py https://example.com/article-about-x
# OR store raw text: python wiki_ingest.py "Some research notes..."
```

**Expected output:** `✓ Saved to: .../some-article-title.md`

### Step 2: Load Skill in Hermès Session

Create a custom Hermès skill (or use this session):

```python
from hermes_tools import search_files, read_file

def query_wiki_observations(query, n=5):
    """Search Obsidian wiki for query; return first n matches"""
    vault = "E:/tommy vault/tommy vault/Read & Write"
    
    results = search_files(
        pattern=f'\b{query}\b',
        target="content",
        path=vault,
        file_glob="*.md",
        limit=n,
        output_mode="content"
    )
    
    return results
```

### Step 3: Search Test

```python
# Run this to test the skill
result = query_wiki_observations("example")
print(result)
```

**Expected**: List of snippets from matching notes.

---

## Full Features To Implement (Ongoing Work)

| Feature | Estimated Effort | Priority |
|---------|-----------------|----------|
| Auto-update Hooks (YouTube → wiki) | 2 hrs | High |
| Contradiction Alerts (diff notes on same topic) | 1 hr | Medium |
| Hermès Prompt Injection (auto-check wiki before answering) | 1 hr | High |
| Cross-link Suggestions ("Note A mentions X but not Y") | 2 hrs | Low |

---

## Next Steps — Choose One

1. **Try Ingestion**: Test with a live URL
   ```bash
   python .hermes/scripts/wiki_ingest.py "https://news.ycombinator.com/item?id=..." 
   ```

2. **Customize Prompt**: Add wiki checks to your Hermès session's context files (`/prompts/`)

3. **Review Existing Notes**: Add tags like `machine-learning` or `git-commands` for organization.

---

## Need More Help?

See [`E:/tommy vault/tommy vault/Read & Write/examples/wiki-integration-guide.md`]([wiki-integration-guide]) for detailed examples.

**Happy note-taking!** 📚✨

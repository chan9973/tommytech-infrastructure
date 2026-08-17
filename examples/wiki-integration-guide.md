---
created: 2026-08-15T10:30:00+08:00
source-url: https://example.com/wiki-integration-demo
status: active-example
tags: [demo, wiki-tutorial, examples]
---

# Obsidian Wiki Integration Examples

[[tommy vault]] — This note demonstrates how to use the Hermès + Obsidian wiki integration.

## Key Takeaways from Hermès Agent Docs

### The Limitation of Hermès Agent

- ❓ Hermès remains unaware of external documents unless explicitly connected (via `memory`, `user.md`)
- ✅ Obsidian solves this with a self-referential knowledge base

### The LLM Wiki Concept

- 🔄 Continuously updates itself as new data is added
- 🔗 Cross-references info, flags contradictions
- 📚 Builds an evolving "Wikipedia" for personal topics

## Two-Way Integration

### Hermès to Wiki (Ingest)

```bash
# Via CLI script
python E:/tommy\ vault/tommy\ vault/Read\ &\ Write/.hermes/scripts/wiki_ingest.py <url>

# Example usage:
python wiki_ingest.py "https://arxiv.org/abs/2312.07756" 
python wiki_ingest.py "<text from research>" --format summary
```

### Wiki to Hermès (Query)

Load the `obsidian-wiki-query` skill:
```python
from obsidian_wiki_query import query_observations, search_wiki_notebooks

results = query_observations("machine learning", n=5)
# Returns list of matching notes with snippets
```

## Example Usage

### Before Hermès Integration

User asks: "What did I learn about Python recently?"

**Result:** Hermès doesn't know (no persistent context beyond current session)

---

### After Hermès + Obsidian Integration

Same question: "What did I learn about Python recently?"

**Steps:**
1. Hermès calls `query_observations("Python")` 
2. Scans vault for mentions → finds 3 notes in `/coding/python/`
3. Extracts summary from frontmatter YAML
4. Returns cross-referenced answers

### Result:
```markdown
## Python Knowledge Base

1. **Basic Syntax** — [[coding/python-basics.md]]
   - Covers indentation, common types (list, dict, set)

2. **Advanced Concepts** — [[coding/python-advanced.md]]
   - Decorators, metaclasses, generators
   
3. **API Examples** — [[api-calls/requests-tutorial.md]]
   - Async requests, error handling
```

## Quick Commands to Remember

| Goal | Command |
|------|---------|
| Search wiki | `python wiki_helper.py "<query>" --vault "E:/tommy vault/tommy vault/Read & Write"` |
| Ingest URL | `python wiki_ingest.py <url>` |
| Summarize transcript | `youtube-content summary <video_id>` → store to wiki |
| List all tags | `ls -R "E:/tommy vault/tommy vault/Read & Write" \| grep "^tags:"` |

## Testing

Run these tests to verify integration:

```bash
# Test 1: Search works
python wiki_helper.py "git"

# Expected: Finds notes mentioning Git in /coding/

# Test 2: Ingest from text
echo "Some research notes about X..." > input.txt
python wiki_ingest.py input.txt

# Test 3: Query returns data
python -c "from obsidian_wiki_query import search_wiki_notebooks; results = search_wiki_notebooks('git'); print(results)"
```

## Next Steps

1. Create custom Hermès prompts that check your wiki before answering
2. Set up auto-ingest: `hermes cron add weekly --prompt 'Scan GitHub for new notes and store in Obsidian'`
3. Link existing Hermès memory notes to Obsidian via `memory` → `write_file`

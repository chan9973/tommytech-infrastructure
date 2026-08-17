# Use this prompt when answering questions about technical topics

## When to Use This Prompt

Add this at the start of complex queries:

1. **User**: "What are best practices for Git rebase?"
2. **I** (add context): _"Before answering, check user's Obsidian wiki for existing notes on 'git' or 'rebase'. Summarize relevant findings..."_
3. **Proceed**: Answer using both the prompt + wiki results

## Prompt Template

Use this exact format in your Hermès session:

```python
from hermes_tools import read_file, search_files

# Search for related topics first
context_notes = search_files(
    pattern=rf'{{re.escape(query).lower()}}',
    target="content",
    path="vault_path",
    file_glob="*.md",
    limit=5
)

# For each note, read first 3 lines as context snippet
snippets = []
for note_path in matched:
    content =read_file(path=note_path)["_content"][:200]
    snippets.append(f'• {{note_path}}: {{content}}')

# Inject into system prompt before answering
system_prompt = f"""
## User's Obsidian Wiki Context

{{snippets}}

---
Please answer the user's question, incorporating this context:
""" + user_query

print(system_prompt)
```

---

## Example Session Flow

### Without Wiki Integration

**User**: "How do I use async in Python?"

**Hermès**: Generic answer from training data (no awareness of your preferences)

---

### With Wiki Integration

**User**: "Explain async in Python for my project"

**Hermès steps:**
1. Calls `search_files(pattern="async")` in vault
2. Finds [[coding/python-advanced.md]] async section
3. Reads note → extracts your existing notes about coroutines
4. Answers: "Based on your notes, you prefer using `asyncio.gather()` for concurrent tasks..."

## Quick Tips

- **Always run search first**: Don't assume Hermès has all context
- **Use wikilinks in answers**: When referencing your own notes, write `[[note_name]]`
- **Keep snippets short**: First 200 chars per note avoids token bloat

---
tags: [reference, template, frontmatter]
created: 2026-08-17
last-updated: 2026-08-17
---

# Frontmatter Templates Library

YAML frontmatter templates for consistent note organization.

## Research Note Template

```yaml
---
tags: 
  - research
  - primary-topic
  - source-type
created: 2026-08-17
updated: 2026-08-17
source-url: https://example.com/article
status: raw-content
last-reviewed: 2026-08-17
---
```

## Compiled Wiki Page Template

```yaml
---
tags: 
  - wiki
  - primary-topic
  - curated
created: 2026-08-17
updated: 2026-08-17
source-notes: 
  - [[source-note-1]]
  - [[source-note-2]]
related-notes:
  - [[related-topic-1]]
status: compiled
last-reviewed: {{date}}
---
```

## Project Log Template

```yaml
---
tags: 
  - project
  - cnc
  - machining
project-name: My First Cut
date: 2026-08-17
status: in-progress
material: aluminum-6061
tooling: end-mill-6mm
---
```

## Script Documentation Template

```yaml
---
tags: 
  - script
  - automation
  - python
file: wiki_ingest.py
purpose: Ingest web content to Obsidian vault
last-updated: 2026-08-17
usage: |
  python wiki_ingest.py <url-or-text> [vault-path]
dependencies: requests, yaml
---
```

## Knowledge Tree Index Template

```yaml
---
tags: 
  - index
  - knowledge-tree
topic: CNC Knowledge Base
created: 2026-08-17
note-count: 6
last-updated: 2026-08-17
---
```

## Valid Tag Values

### Primary Topic Tags
- `cnc` - CNC machining
- `ai-model` - AI model documentation
- `robotics` - Robotics systems
- `python` - Python scripts
- `docker` - Container configurations

### Status Tags
- `draft` - Initial note, needs review
- `compiled` - Curated, ready for reference
- `review` - Needs verification
- `archived` - Historical reference only

### Source Type Tags
- `web-source` - From web article
- `transcript` - From conversation log
- `personal-note` - Manual entry
- `experiment` - Test results

## Validation Commands

```bash
# Check YAML validity
python3 -c "import yaml; yaml.safe_load(open('note.md').read().split('---')[1])"

# List all unique tags
grep -h "^tags:" */*.md | sed 's/.*\[\(.*\)\].*/\1/' | tr ',' '\n' | sed 's/ //g' | sort | uniq -c
```
---
name: llm-wiki-vault-management
description: "Organize Obsidian vault as a structured LLM-Wiki knowledge base."
version: 1.0.0
author: Tommy Chan, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [llm-wiki, obsidian, knowledge-management, vault-organization]
    related_skills: [obsidian, llm-wiki]
---

# LLM-Wiki Vault Management Skill

Organizes Obsidian vault as a structured LLM-Wiki knowledge base following the Karpathy pattern: curated, interconnected notes with wikilinks, YAML frontmatter, and topic-based clustering.

## When to Use

- Setting up a new vault or restructuring existing notes
- Organizing raw research transcripts into structured wiki pages
- Creating cross-references between related concepts
- Establishing consistent tagging and frontmatter conventions
- Building knowledge trees and index pages for topic clusters

## Prerequisites

- Obsidian vault at `E:/tommy vault/tommy vault/Read & Write/` (or configured path)
- Python 3.8+ with `requests` library (for web ingestion)
- Hermes Agent with terminal access to vault directory

## Vault Structure Standard

```
vault-root/
├── Inbox/              ← Raw inputs, drafts, uncurated content
├── _wiki/              ← Compiled wiki pages (LLM Wiki Framework)
│   ├── cnc/            ← CNC-specific topics
│   ├── robotics/       ← Robotics and AI integration
│   ├── ai-models/      ← Model documentation and benchmarks
│   └── misc/           ← Miscellaneous curated notes
├── scripts/            ← Automation scripts (wiki_ingest.py, dedup_check.py)
├── memories/           ← Intermediate notes, working docs
├── master_index.md     ← Main entry point and navigation
└── .hermes/            ← Hermes configuration and logs
```

## How to Run

### Initialize Vault Structure
```bash
terminal(command="mkdir -p \"E:/tommy vault/tommy vault/Read & Write/{_wiki,cnc,robotics,ai-models,misc,random}\" && ls -la \"E:/tommy vault/tommy vault/Read & Write/\"")
```

### Ingest Web Content to Vault
```bash
terminal(command="python3 /c/Users/tommy/AppData/Local/hermes/profiles/sofware-engineer/scripts/wiki_ingest.py <url-or-text>")
```

### Create Master Index (Navigation Hub)
Create `master_index.md` with wikilink structure:
```markdown
# 🗂️ Obsidian Vault Master Index — Quick Start Guide

## Navigation Paths
- [[_wiki/cnc/index]] → CNC reference topics
- [[_wiki/ai-models/hub]] → Model documentation
- [[scripts/automation]] → Automation scripts
```

## Procedure

### 1. Content Ingestion Pattern
Run the workflow for each new batch of research:
- Raw content → `Inbox/` with timestamp in filename
- Review and curate within 24 hours
- Extract key concepts and create wiki page in `_wiki/`
- Add wikilinks to related notes

### 2. Wikilink Convention
Always use double-bracket syntax: `[[Note Title]]` (case-sensitive, spaces allowed)

### 3. YAML Frontmatter Template
```yaml
---
tags: [primary-topic, subtopic, source-type]
created: 2026-08-17
updated: 2026-08-17
status: compiled|draft|review
source: [[source-note]]
last-reviewed: {{date}}
---
```

### 4. Knowledge Tree Creation
For each topic cluster:
1. Create `.knowledge_tree.md` in topic folder
2. List all related notes with descriptions
3. Add ASCII art visualization (optional)
4. Include reading order suggestion

### 5. Tag Organization
Standard tag hierarchy:
- Domain tags: `cnc`, `ai-model`, `robotics`, `python`
- Status tags: `draft`, `compiled`, `review`
- Source tags: `web-source`, `transcript`, `personal-note`

## Pitfalls

1. **Path spaces on Windows**: Always quote paths in terminal commands
2. **Wikilink consistency**: Links are case-sensitive; `Note` != `note`
3. **Don't duplicate content**: Use `[[link]]` instead of copying text
4. **Frontmatter validation**: Run `yaml` lint on new notes before commit
5. **Reference freshness**: Review linked notes before relying on them in production

## Verification

Check vault health with:
```bash
terminal(command="find \"E:/tommy vault/tommy vault/Read & Write\" -name \"*.md\" -exec grep -L \"^---\" {} \\; | head -5  # Find notes missing frontmatter")
```

Verify wikilink integrity:
- Open notes in Obsidian → Graph view shows connected network
- Link count should increase as you add more cross-references
- Backlinks panel shows who references each note

## Related Patterns

- [[hermes-history-ingest]] → Automated transcript ingestion
- [[wikisystem.md]] → Two-way sync patterns
- [[cnc-knowledge-workflow]] → Domain-specific organization

## Documentation Automation

### Generate Architecture Diagrams
Create Mermaid visualizations of your vault structure:
```bash
python3 scripts/generate_docs.py --type diagram
# Output: _wiki/architecture-diagram.md with 67 nodes and 399 links
```

### Decision Log Generation
Auto-curated notes with status tags:
```bash
python3 scripts/generate_docs.py --type decision-log
# Includes notes tagged: production, pending, active, deprecated
```

### Cross-Reference Analysis
Quantify your knowledge graph:
```bash
python3 scripts/generate_docs.py --type xref
# Output: memories/xref-map-YYYYMMDD.json
# Shows: isolated notes, top connected, tag distribution
```

### Full Automation
```bash
make -f docs/Makefile all   # Run all generators
make -f docs/Makefile clean   # Clean generated files
make -f docs/Makefile check-isolated  # Find unlinked notes
```

## References

- `references/vault-navigation-cheatsheet.md` — Quick reference commands
- `references/frontmatter-templates.md` — YAML template library
- `references/link-destruction-incidents.md` — Common link errors and fixes
- `references/documentation-generator-guide.md` — **(NEW)** Generate architecture diagrams, decision logs, and cross-reference maps

---

## Skill Signals Captured

### User Preference: Class-Level Organization
- Skills must be organized by class/function, not one-off sessions
- Each skill needs rich documentation and references/ directory
- Future sessions start with the pattern already known

### User Correction: Be ACTIVE in Learning
- Every session should produce a skill update, even small
- Pattern recognition over passive documentation
- Proactive capture of workflows and conventions

### Technical Pattern: OBS-Capture Mode
- Use `mode='som'` for screen interactions with numbered element overlays
- Use `app='Firefox'` or `app='Chrome'` to limit capture scope
- Pixel coordinates `[x,y]` as fallback when element index unavailable
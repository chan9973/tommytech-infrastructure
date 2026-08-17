# 🔗 Obsidian Wiki + Hermes Integration

**Created:** 2026-08-17  
[[wikilink]] to this note: Open in Obsidian and use [[←backlinks]] or search for `obsidian-hermes`

---

## Overview

This wiki page documents the **Hermes Agent + Obsidian** integration workflows that turn your personal note vault into an AI-curated digital brain.

### Integration Philosophy

- **Curator over Summarizer**: Hermes acts as an editor, compiling raw input into organized wiki pages with [[wikilink]] links
- **Context Bridge**: Highlight text or open a note in Obsidian to share active context with Hermes for instant editing/research
- **Automated Ingestion**: `hermes-history-ingest` pulls session transcripts from logs (`~/.hermes`) and updates appropriate pages

---

## Core Integration Approaches

| Workflow | Mechanism | Primary Use Case |
| --- | --- | --- |
| **Hermes Agent Plugin** | Community plugin running local/remote gateway API. | Grants Hermes direct read/write/tool access inside the Obsidian vault folder. |
| **Hermes Console** | Embedded terminal view inside Obsidian. | Selected-text and active-note context sharing via a JSON bridge (`obsidian-context-bridge`). |
| **LLM Wiki Framework** | Structured workflow based on the Karpathy LLM-Wiki pattern. | Uses Hermes skills (`wiki-history-ingest`, `hermes-llm-wiki`) to distill raw captures/transcripts into compiled wiki pages (`_wiki/`). |

---

## Key Features & Workflow Capabilities

### [[wikilink]] Hermes as Curator (Not Summarizer)

Rather than flooding notes with raw conversational outputs, Hermes:
- Filters high-value concepts from conversations
- Creates organized files with internal wiki-links (`[[Note]]`)
- Maintains quality and structure in your vault

### [[wikilink]] Context Bridge

Toggle active context sharing so Hermes instantly ingests:
- Current note content
- Cursor position
- Highlighted text selections
- Active file path and recent edits

**Result:** Hermes understands what you're working on and can:
```
# Edit existing note based on highlighted text
# Research the topic from cursor context
# Add wikilinks to related concepts automatically
```

### [[wikilink]] Automated Ingestion

Features like `hermes-history-ingest` pull from Hermes logs (`~/.hermes`):
- Session transcripts → cluster by topic
- Append/update appropriate pages in vault
- Deduplicate across sessions

### [[wikilink]] Full Vault Operations

When granted local workspace access, Hermes can:
- Multi-file searches across all notes
- Run Python scripts in `scripts/` folder
- Create structured YAML frontmatter
- Maintain indices (e.g., `memories/.cnc_knowledge_tree.md`)

---

## Basic Setup (Hermes Console)

### Step 1: Install Plugin

```bash
# Open Obsidian → Settings → Community Plugins → Browse
# Search for and install "Hermes Console" plugin
# Enable in Plugins → Hermes Console settings
```

### Step 2: Enable Context Bridge

```bash
# Run in terminal or via console panel:
hermes plugins install dannyshmueli/obsidian-hermes-console --enable
```

### Step 3: Open Terminal

Launch the **Hermes Console** panel inside Obsidian to:
- Interact with your vault files via Hermes CLI
- Toggle context sharing on/off
- Run commands like `hermes history ingest <topic>`

---

## Configuration Examples

### Vault Layout Recommendation

```
E:\tommy vault\tommy vault\Read & Write/
├── Inbox/                 ← Raw inputs, drafts from transcripts
│   ├── notes-from-chat.md
│   └── research-ideas.txt
├── _wiki/                 ← Compiled wiki pages (LLM Wiki Framework)
│   ├── cnc/               ← CNC reference topics
│   ├── obsidian-hermes/   ← Integration docs for this page
│   └── misc/              ← Other compiled knowledge
├── scripts/               ← Automation scripts for Hermes
│   ├── wiki_ingest.py     ← Ingest transcripts to wiki
│   └── dedup_check.py     ← Remove duplicate concepts
└── .obsidian-hermes.toml  ← Configuration (optional)
    ├── plugins_enabled.ini
    └── gateway_url = "http://localhost:9090"
```

### `.obsidian-hermes.toml` Example Config

```toml
# ~/.obsidian-hermes.toml
[context]
enabled = true
sharing_method = "json_bridge"

[ingestion]
source_logs = "~/.hermes/logs"
dest_folder = "Inbox/"
auto_cluster = true

[tools]
allowed_skills = ["research", "code", "wiki"]
```

---

## Skills Used in This Integration

| Skill | Purpose | [[wikilink]] Description |
| --- | --- | ------------------------ |
| `hermes-history-ingest` | Pull transcripts from logs, cluster by topic | Automated session mining for wiki pages |
| `hermes-llm-wiki` | Distill raw content into compiled wiki structure | Karpathy-style structured ingestion |
| `wiki-curating` | Deduplicate, organize notes with wikilinks | Ensure quality, avoid clutter |
| `research-discovery-loops` | Structured research patterns | Systematic exploration of knowledge topics |

---

## Workflow Examples

### Example 1: Research & Save to Wiki

```bash
# User highlights text in note about "CNC G-code" in Obsidian
# Hermes ingests context via bridge

# User: "Research adaptive milling strategies"
# Hermes researches → writes to Inbox/adaptive-milling.md
# Then compiles to _wiki/cnc/milling-strategies.md

# Result: Structured wiki note with [[wikilink]] to related pages
```

### Example 2: Session Transcript Digest

```bash
# Run ingestion after a research session with Hermes:
hermes history ingest cnc-machining --folder Inbox/

# Skill outputs:
# - Clustered notes → `Inbox/cnc-setup-guide.md`
# - Related wikilinks auto-added
# - Frontmatter tags added: `tags: [cnc, robotics]`
```

---

## Tags & Organization

Notes created via Hermes integration use YAML frontmatter:

```yaml
---
# Obsidian Wiki + Hermes Note
source-session: "default/20260817_025xxx"
ingested-by: hermes-history-ingest
clusters: [cnc, gcode, workshop]
tags: 
  - cnc
  - robotics
  - obsidian-hermes
---
```

---

## Related Notes

- [`cnc.md`](memories/cnc.md) — CNC fundamentals
- [`cam_workflow.md`](memories/cam_workflow.md) — CAM workflow details  
- [`tooling.md`](memories/tooling.md) — Tooling reference
- [`obsidian-backup-skill.md`](memories/hermes-auto-backup-setup.md) ← Backup automation
- [`hermes-agent`](skills:hermes-agent) — Official Hermes documentation

---

## Resources

| Resource | URL / Access | [[wikilink]] Notes |
| --- | --- | ------------------ |
| **Hermes Agent GitHub** | https://github.com/... | Install Hermes CLI tools, plugins |
| **Obsidian Hermes Console Plugin** | Obsidian Community Store | Search `dannyshmueli/obsidian-hermes-console` |
| **Karpathy LLM Wiki Papers** | [llm-wiki](https://karpathy.ai/) | Structured workflow inspiration |

---

*Continue expanding this wiki with your own Hermes+Obsidian workflows! [[wikilink]] Create notes as you discover new integration patterns.*

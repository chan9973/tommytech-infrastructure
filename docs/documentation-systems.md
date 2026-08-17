---
tags: [documentation, automation, quality-assurance, llm-wiki]
created: 2026-08-17
status: production
---

# Documentation Systems for LLM-Wiki

> Production-grade documentation automation tools integrated with your Hermes agent and Obsidian vault.

---

## 📚 Core Documentation Tools

### [[generate-docs.py]] - Full Documentation Suite

**Location:** `scripts/generate_docs.py`

| Function | Purpose | Output |
|----------|---------|--------|
| `--type diagram` | Generate Mermaid architecture diagram | `_wiki/architecture-diagram.md` |
| `--type decision-log` | Curated decisions with status tags | Auto-generated markdown |
| `--type xref` | Cross-reference analysis | `memories/xref-map-*.json` |
| `--type all` | Run all generators | Multiple outputs |

**Usage:**
```bash
# Generate architecture diagram
python3 scripts/generate_docs.py --type diagram

# Generate decisions about Qwen3.5
python3 scripts/generate_docs.py --type decision-log qwen3.5

# Run full suite
python3 scripts/generate_docs.py --type all
```

---

## 🏗️ Architecture Overview

### Generated Knowledge Map

Your vault is organized into these domains:

| Domain | Purpose | Key Notes |
|--------|---------|-----------|
| **ai-models** | Model specifications & optimization | Qwen3.5, Gemma-3, hardware guides |
| **CNC n Robotic** | Manufacturing & robotics workflows | CAM paths, vision stacks |
| **coding** | Python/TypeScript patterns | Cross-reference examples |
| **memories** | Hermes agent knowledge | Integration docs, backup |

### See Also
- [[vault-index]] - AI models library
- [[hardware-setup-guide]] - System requirements
- [[optimization-tech]] - Performance optimizations
- [[obsidian-hermes-integration]] - Agent integration

---

## 🔗 Cross-Reference Analysis

**Current vault state:**
- **67 notes** with **399 wikilinks**
- **45 tag categories** tracked
- **20 tagged domains** organized

**Most Connected Notes:**
1. architecture-diagram.md (66 outgoing links)
2. robotics-integration-main.md (34 connections)
3. vault-synthesis-summary.md (23 connections)
4. vault-index.md (17 connections)
5. .summary_index.md (16 connections)

**Isolated Notes (candidates for linking):**
- CAD-CAM-workflow
- G-code-programming
- Precision-manufacturing
- Robotics-integration
- ubuntu commads

---

## 🎯 Decision Log Framework

### Creating Decision Logs

Add status tags to your notes to automatically include them in decision logs:

```yaml
---
tags: [production|pending|active|deprecated]
status: production
---
```

### Available Decision Types

| Status | Meaning | Examples |
|--------|---------|----------|
| ✅ `production` | Live in production | Qwen3.5-Hermes model |
| ⏳ `pending` | Awaiting implementation | [your topic] |
| 🚫 `deprecated` | Superseded | Old configs |
| 📝 `active` | Work in progress | [your topic] |

---

## 🚀 Automation Workflow

### Daily Documentation Update
```bash
# Run from vault root
./scripts/generate_docs.py --type all

# Or using Makefile
make docs
```

### Integration Points

1. **Hermes Agent Integration**
   - Script runs in background via cron
   - Outputs sent to Inbox/ for review
   - Archives automatically via [[wiki-curating]]

2. **Obsidian Graph View**
   - Architecture diagram renders as interactive Mermaid
   - Click nodes to navigate wiki links
   - Filter by tags in graph view

3. **Quality Gates**
   - Detect isolated notes (missing links)
   - Track orphaned documentation
   - Monitor tag consistency

---

## 📁 Generated Files

| File | Purpose | Update Frequency |
|------|---------|-----------------|
| `_wiki/architecture-diagram.md` | Visual knowledge map | On-demand |
| `memories/xref-map-YYYYMMDD.json` | Quantitative analysis | Daily |
| `memories/decision-log-YYYYMMDD.md` | Curated decisions | Weekly |
| `_wiki/knowledge-tree.md` | Auto-indexed topics | Monthly |

---

## 🔧 Maintenance Commands

```bash
# Full documentation suite
python3 scripts/generate_docs.py --type all

# Architecture only
python3 scripts/generate_docs.py --type diagram

# Cross-reference analysis
python3 scripts/generate_docs.py --type xref

# Decision log with topic filter
python3 scripts/generate_docs.py --type decision-log "ai-models"
```

---

## 📝 Adding New Documentation

When creating new notes, follow this pattern:

```yaml
---
tags: [domain, subtopic, documentation]
status: production  # or pending, deprecated
created: {{date}}
related: [[other-wikilinks]]
---

# Title Here
```

This ensures:
- ✅ Auto-inclusion in decision logs
- ✅ Cross-reference tracking
- ✅ Domain categorization
- ✅ Backlink generation

---

## 🔄 Related Skills

- [[obsidian-hermes-integration]] - Plugin integration
- [[optimize_vault.py]] - Quality assurance
- [[wiki_ingest.py]] - Content ingestion
- [[compiler scripts]] - Batch processing

---

## 🎨 Diagram Preview

See generated visualization:

```mermaid
graph TD
    subgraph Core[Core Infrastructure]
        hermes[Hermes Agent] -->|reads| obsidian[Obsidian Vault]
        obsidian -->|writes| inbox[Inbox/]
        obsidian -->|reads| scripts[scripts/]
    end
    subgraph Domains[Knowledge Domains]
        subgraph ai_models[AI Models]
            -- Qwen3.5, Gemma-3, hardware guides
        end
        subgraph cnc["CNC & Robotics"]
            -- CAM workflows, vision stacks
        end
        subgraph coding[Code Patterns]
            -- Python, TypeScript, automation
        end
    end
```

---

## ⚙️ Configuration

**Default paths:**
- Vault: `E:/tommy vault/tommy vault/Read & Write`
- Output: `_wiki/` and `memories/`
- Scripts: `scripts/`

Override by setting `VAULT_SUMMARY` at top of `generate_docs.py`.

---

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| Empty decision log | Add `status:` tag to YAML frontmatter |
| Diagram missing nodes | Run with `--type all` to rebuild |
| Path errors | Check `VAULT_SUMMARY` matches your vault location |

---

## 📚 Further Reading

- [[LLM-Wiki Architecture]] - Karpathy pattern explanation
- [[hermes-agent-skill-authoring]] - Writing SKILL.md files
- [[automation-patterns]] - Workflow best practices
- [[quality-gates]] - Documentation standards
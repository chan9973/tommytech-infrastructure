---
tags: [cheatsheet, documentation, automation]
created: 2026-08-17
status: production
---

# 📚 LLM-Wiki Documentation Quick Reference

## 🚀 Quick Start Commands

```bash
# Generate all documentation
make all

# Or from scripts directory
python3 scripts/generate_docs.py --type all

# Architecture diagram only
python3 scripts/generate_docs.py --type diagram

# Quality analysis
python3 scripts/generate_docs.py --type xref
```

## 📂 File Locations

| Purpose | Location |
|---------|----------|
| Architecture diagram | `_wiki/architecture-diagram.md` |
| Cross-reference map | `memories/xref-map-YYYYMMDD.json` |
| Decision logs | Auto-generated (see tags) |
| Makefile | `docs/Makefile` |
| Generator script | `scripts/generate_docs.py` |

## 🏷️ Tag Convention

```yaml
tags: [domain, technology, context, documentation]
status: production | pending | active | deprecated
```

**Current tags found:**
- production, ai-model, machine-learning, documentation
- hardware/gpu-nvidia, hardware/cpu-gpu
- context/128k, context/8k, balanced
- quality-assurance, testing, automation

## ⚡ Automation Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│  1. Source Notes (yaml frontmatter)                         │
│  2. WikiGraph builds in memory                              │
│  3. generate_docs.py runs                                   │
│  4. Outputs to _wiki/ and memories/                         │
│  5. Visible in Obsidian (Mermaid diagrams, backlinks)     │
└─────────────────────────────────────────────────────────────┘
```

## 🔍 Quality Checks

**Isolated notes** (need linking):
```bash
grep '"isolation_score": 0' memories/xref-*.json
```

**Connect notes by adding:**
```markdown
See [[related-note]] for more details.
```

## 📊 Current Stats

- **67 notes** in your vault
- **399 wikilinks** connecting concepts
- **45 tag categories** organized
- **20 knowledge domains** structured

## 🛠️ Troubleshooting

| Symptom | Action |
|---------|--------|
| Diagram not showing | Use Mermaid plugin in Obsidian |
| Empty decision log | Add `status:` tag to note frontmatter |
| Missing xref data | Re-run with `--type all` |
| Path errors | Check `VAULT_SUMMARY` in script |

## 📚 Key Wikilinks

- [[documentation-systems]] - Full documentation guide
- [[generate-docs.py]] - Script reference
- [[architecture-diagram]] - Visual knowledge map
- [[xref-map-20260817]] - Quantitative analysis
- [[hermes-agent-skill-authoring]] - Writing skills
- [[optimize_vault.py]] - Quality automation

---

## 🎨 Preview: Knowledge Domains

| Domain | Notes | Tags |
|--------|-------|------|
| ai-models | 5 | production, ai-model |
| CNC n Robotic | 26 | research, robotics |
| coding | 6 | python, typescript |
| memories | 10 | hermes, integration |

Generated: {{date}} | Vault: Read & Write
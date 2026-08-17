---
tags: [reference, documentation, automation]
created: 2026-08-17
last-updated: 2026-08-17
---

# Documentation Generator Guide

**Script:** `scripts/generate_docs.py` | **Location:** Vault root / scripts/

Generates automated documentation from your LLM-Wiki vault:

---

## Quick Commands

```bash
# Generate all documentation
python3 scripts/generate_docs.py --type all

# Architecture diagram only
python3 scripts/generate_docs.py --type diagram

# Decision log (curated notes)
python3 scripts/generate_docs.py --type decision-log

# Cross-reference analysis
python3 scripts/generate_docs.py --type xref

# Help
python3 scripts/generate_docs.py --help
```

Or use the Makefile:
```bash
make -f docs/Makefile all
```

---

## Output Files

| Type | Location | Purpose |
|------|----------|---------|
| Architecture diagram | `_wiki/architecture-diagram.md` | Mermaid visualization of vault structure |
| Decision log | Auto-generated markdown | Notes with `status:` tags (production/pending/etc.) |
| Cross-reference map | `memories/xref-map-YYYYMMDD.json` | Graph analysis of links and connections |

---

## Usage Patterns

### 1. Weekly Documentation Refresh
```bash
# Run weekly to update all outputs
cron("55 23 * * 0", prompt="python3 scripts/generate_docs.py --type all")
```

### 2. Generate Architecture on Demand
```bash
# After major vault restructuring
python3 scripts/generate_docs.py --type diagram
```

### 3. Quality Gate - Check Isolated Notes
```bash
# Find notes that need linking
grep -l "isolation_score\": 1" memories/xref-map-*.json
```

---

## Decision Log Selection

To include a note in the decision log, add to YAML frontmatter:

```yaml
---
tags: [domain, feature, decision]
status: production  # or: pending, active, deprecated
---
```

Notes with `production`, `pending`, `active`, or `deprecated` status tags appear automatically.

---

## Cross-Reference Analysis Output

JSON structure:
```json
{
  "metadata": { "total_nodes": 67, "total_edges": 399 },
  "top_connected": [[node, {inbound_links, outbound_links}]],
  "isolated_nodes": ["note-name-without-links"],
  "by_tags": { "tag": ["linked-nodes"] }
}
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Empty decision log | Add `status: production` tag to YAML frontmatter |
| Diagram missing nodes | Re-run with `--type all` |
| Path not found | Check `VAULT_SUMMARY` variable in script |
| Unicode errors | Ensure file encoding is UTF-8 |

---

## Related

- [[generate-docs.py]] - Full script source
- [[llm-wiki-vault-management]] - Vault organization patterns
- [[vault-navigation-cheatsheet]] - Navigation commands
- [[optimize_vault.py]] - Quality assurance tool
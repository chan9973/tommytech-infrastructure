# Dataview Integration Patterns

## Pattern: Database-like Queries for Obsidian Vault

**Context**: User requested powerful database-like queries using Dataview plugin

### Key Requirements from Session
- Enable Dataview plugin in Obsidian Community Plugins
- Add structured YAML frontmatter to existing notes
- Create query dashboard at `[[dataview-dashboard]]`
- Generate comparison tables for AI models

### Dataview Query Examples

#### AI Models Comparison Table
```dataview
TABLE
  parameters as "Parameters",
  vram-required as "VRAM (Q4)",
  benchmark-score as "Score",
  status as "Status"
FROM #ai-model
SOR...[truncated]
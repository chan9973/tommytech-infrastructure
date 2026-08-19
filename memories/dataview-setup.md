---
tags: [setup-guide, dataview, vault-enhancement]
created: 2026-08-19
updated: 2026-08-19
status: current
priority: high
---

# 📊 Vault Dataview Setup Guide

## 🚀 3-Minute Setup

### Step 1: Install Dataview Plugin
```bash
# In Obsidian:
Settings → Community Plugins → Browse → Search "Dataview"
→ Install → Enable
```

### Step 2: Add YAML Frontmatter to Notes
```yaml
---
tags: [tag1, tag2, category]
status: draft | current | archived
confidence: 80
priority: low | medium | high
created: 2026-08-19
updated: 2026-08-19
model: qwen3.5-hermes
vram-required: 5GB
context-window: 128K
benchmark-score: 95
---
```

### Step 3: Access Your Queries
- `[[dataview-dashboard]]` - Full analytics dashboard
- `[[dataview-queries]]` - Query examples and templates

---

## 📈 Database Tables

### AI Models (ai-models/)
Has fields: model, vram-required, context-window, benchmark-score, status

### CNC Notes (CNC n Robotic/)
Has tags: cnc, materials, fusion360, tooling, robotics

### Knowledge Notes (memories/)
Has tags: ai-model, knowledge-management, hermes-integration

---

## 🔗 Related Vault Notes
- [[dataview-setup]] - This guide
- [[master_index]] - Main navigation with Dataview queries
- [[memories/dataview-dashboard]] - Live vault analytics
- [[memories/dataview-queries]] - Query examples

---
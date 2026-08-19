---
tags: [dataview-query, ai-model, comparison-table]
created: 2026-08-19
updated: 2026-08-19
status: current
---

# 📊 AI Model Comparison Table (Dataview)

Enable Dataview plugin for live table updates!

```dataview
TABLE
  parameters as "**Parameters**",
  context-window as "Context",
  vram-required as "VRAM (Q4)",
  benchmark-score as "Score",
  status as "Status"
FROM #ai-model
SORT benchmark-score DESC
```

## 🔍 Filter Queries

### By Hardware Tier
```dataview
TABLE WITHOUT ID
  file.name as Model,
  vram-required as VRAM
FROM #ai-model
WHERE vram-required <= "5GB"
SORT vram-required ASC
```

### By Task Type
```dataview
TABLE WITHOUT ID
  file.name as Model,
  best-for as "Best For"
FROM #ai-model
WHERE best-for CONTAINS "coding" OR best-for CONTAINS "hermes"
```

---

## 🔗 Related
- [[vault-index]] → Main AI model library
- [[models/qwen3.5-hermes-mathematical-optimization]] → Qwen3.5 champion model
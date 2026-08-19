---
tags: [dataview, ai-model, reference-card]
created: 2026-08-19
updated: 2026-08-19
status: current
priority: high
---

# 📊 Dataview Plugin Integration

## 🚀 Quick Setup

1. Install Dataview plugin in Obsidian
2. Enable in Settings → Community Plugins → Dataview
3. Restart Obsidian

## 📈 Useful Queries

### AI Models Database
```dataview
TABLE
  vram-required as "VRAM",
  context-window as "Window",
  benchmark-score as "Score"
FROM #ai-model
SORT benchmark-score DESC
```

### Recent Updates (Last 30 Days)
```dataview
TABLE file.mtime as "Updated", file.folder as "Folder"
FROM ""
WHERE file.mtime > date(today) - dur(30 days)
SORT file.mtime DESC
```

### Task Management
```dataview
TASK FROM "memories"
WHERE !completed
SORT due ASC
```

### YAML Frontmatter Template
```yaml
---
tags: [ai-model, ml-research]
status: draft
confidence: 80
priority: medium
created: 2026-08-19
updated: 2026-08-19
model: your-model-name
vram-required: 5GB
context-window: 128K
benchmark-score: 95
best-for: [coding, research, chat]
---
```

## 🎯 Pro Tips

- Use `FLATTEN` to expand arrays in queries
- Combine with `GROUP BY` for summaries
- Use `date(today) - dur(N days)` for relative dates
- Link to queries using `[[query:query-name]]`

---

## 🔗 Related

- [[dataview-setup]] - Detailed setup guide
- [[dataview-dashboard]] - Live analytics dashboard
- [[model-comparison-dataview]] - AI model comparison tables
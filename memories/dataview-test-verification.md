---
tags: [test, dataview-verification]
created: 2026-08-19
status: current
---

# 🔬 Dataview Activation Test

If you can see formatted tables below, Dataview is WORKING! ✅

---

## 📊 Test Table 1: AI Models Database

This should show a colorful table of your AI models:

```dataview
TABLE
  model as "**Model**",
  vram-required as "VRAM",
  context-window as "Context",
  benchmark-score as "⭐ Score",
  status as "Status"
FROM #ai-model
SORT benchmark-score DESC
```

---

## 📈 Test Table 2: Recent Updates

This will show notes updated in the last 7 days:

```dataview
TABLE
  file.link as "Note",
  file.mtime as "Updated"
FROM ""
WHERE file.mtime > date(today) - dur(7 days)
SORT file.mtime DESC
LIMIT 10
```

---

## 🎯 Quick Stats

Total notes in vault:
```dataview
TABLE length(file.name) as "Count"
FROM ""
```

---

### ✅ If Everything Shows

**Dataview is FULLY OPTIMIZED and ready for production!**

You now have:
- Live database queries
- AI model comparison tables  
- Vault analytics dashboard
- Daily automated updates at 5am

**Start using your vault like a knowledge database!** 🎉
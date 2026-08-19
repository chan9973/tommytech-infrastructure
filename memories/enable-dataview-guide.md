# 🎨 Enable Dataview Plugin - Visual Guide

## Step-by-Step Screenshots (Text Version)

### 1. Open Settings
```
☰ Menu → Settings
```

### 2. Go to Community Plugins
```
Settings → Community Plugins
```

### 3. Browse Plugins
```
Click "Browse" tab
```

### 4. Search for Dataview
```
Search bar: Type "Dataview"
Look for: "Dataview" by blacksmithgu
```

### 5. Install & Enable
```
Click "Install" 
Click "Enable" (toggle switch)
```

### 6. Verify Installation
```
You should see: "Dataview is installed and enabled"
```

### 7. Restart Obsidian (if needed)
```
Close and reopen Obsidian
```

### 8. Test the Queries
```
Open: [[dataview-dashboard]]
Open: [[model-comparison-dataview]]
```

---

## 🔧 Troubleshooting

### Issue: Queries don't render
```
- Restart Obsidian
- Check: Settings → Community Plugins → Dataview (enabled)
- Verify: YAML frontmatter is correct
```

### Issue: Tables show as code
```
- Dataview plugin must be enabled
- Check for syntax errors in query
- Ensure proper backticks and indentation
```

### Issue: File not found
```
- Use Ctrl+P and type exact filename
- Check spelling in wikilinks
- Verify file exists in vault
```

---

## 📚 Quick Reference

| File | Purpose |
|------|---------|
| `[[dataview-setup]]` | This guide |
| `[[dataview-dashboard]]` | Live analytics |
| `[[dataview-queries]]` | Query examples |
| `[[model-comparison-dataview]]` | AI model table |

---

## ⚡ One-time Setup Command

If you have Obsidian CLI access (rare):
```bash
obsidian://open?name=YourVault&file=memories/dataview-setup.md
```
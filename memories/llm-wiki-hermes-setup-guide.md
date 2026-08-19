---
tags: [llm-wiki, hermes-integration, setup-guide, reference]
status: current
priority: high
created: 2026-08-19
last-updated: 2026-08-19
version: 1.0
---

# 📚 A-Z Guide: LLM Wiki + Hermes Integration Setup

## 🎯 Complete System Setup Reference
Save this file! Use it when reinstalling or setting up new systems.

---

## 🔤 A - Applications to Install First

### Essential Apps
- **Obsidian** (latest version) - https://obsidian.md
- **Python 3.11+** - https://python.org
- **Git** - https://git-scm.com

### Optional Tools
- VS Code (for script editing)
- Docker Desktop (if using containerized models)

---

## 📦 B - Backup Your Current Vault

Before reinstall:
```bash
# Copy entire vault folder
cp -r "E:/tommy vault/tommy vault/Read & Write" "backup-location/"

# Or use sync service
# Google Drive, Dropbox, etc.
```

---

## 🧹 C - Clean Vault Structure

Your ideal folder structure:
```
vault-root/
├── Inbox/              ← Raw notes, unsorted
├── _wiki/              ← LLM Wiki pages
│   ├── cnc/
│   ├── robotics/
│   ├── ai-models/
│   └── misc/
├── ai-consultant/      ← AI workflows
├── ai-models/          ← Model documentation
│   └── models/
├── CNC n Robotic/      ← Manufacturing notes
├── coding/             ← Tech notes
├── memories/           ← Working docs
│   ├── dataview-*.md
│   ├── templates/
│   └── daily-*.md
├── scripts/            ← Automation scripts
├── samples/            ← Example data
└── master_index.md     ← Main navigation
```

---

## ⚙️ D - Dependencies & Setup Files

### Python Packages
```bash
pip install requests pyyaml python-dateutil
```

### Obsidian Plugins
1. **Dataview** - Database queries
2. **Calendar** - Daily notes
3. **Templater** - Dynamic templates
4. **QuickAdd** - Fast note creation

---

## 📁 E - Essential Scripts to Preserve

Critical automation scripts:
- `scripts/wiki_ingest.py` - Web content ingestion
- `scripts/daily_vault_cleanup.py` - Daily maintenance
- `scripts/update_vault_quick.py` - Content updates
- `scripts/vault_status.py` - Health checks

---

## 📓 F - Frontmatter Standards

YAML template for all new notes:

```yaml
---
tags: [category, subtopic]
status: draft | current | archived
confidence: 80
priority: low | medium | high
created: 2026-08-19
last-updated: 2026-08-19
---
```

For AI models:
```yaml
---
tags: [ai-model, hardware-optimized]
status: production
confidence: 95
priority: high
created: 2026-08-15
model: model-name
parameters: 7B
vram-required: 5GB
context-window: 128K
benchmark-score: 85
---
```

---

## 🎨 G - Git Configuration

Initialize vault as Git repo:
```bash
cd "E:/tommy vault/tommy vault/Read & Write"
git init
git add .
git commit -m "Initial vault setup"

# Optional: set up remote
git remote add origin your-repo-url
git push -u origin main
```

---

## 📊 H - Hermes Agent Integration

### Key Scripts Location
```
.hermes/
├── scripts/
├── cron/
└── profiles/
```

### Cron Jobs to Recreate
```bash
# Daily at 5am: vault cleanup
0 5 * * * python daily_vault_cleanup.py

# Weekly: quality report
0 9 * * 1 python vault_status.py
```

---

## 🔗 I - Inter-Note Linking Strategy

### Wikilink Patterns
- **Topics**: `[[topic-name]]`
- **Cross-references**: `[[topic-name#section]]`
- **Dates**: `[[2024-01-15]]` (daily notes)
- **Templates**: `[[templates/template-name]]`

### Tag Convention
Use hyphen-separated tags:
- `#ai-model`
- `#hardware-optimized`  
- `#dataview-query`
- `#setup-guide`

---

## 📝 J - Journal/Daily Notes Setup

Create template file: `memories/templates/daily-template.md`

```markdown
---
date: {{date:YYYY-MM-DD}}
tags: [daily-note, {{date:YYYY-MM}}]
---

## 📅 {{date:dddd, MMMM D, YYYY}}

### 🎯 Goals
- 

### 📚 Learning
- 

### 💡 Ideas
- 

### 📊 Daily Stats
- Notes: 
- Time: 
```

---

## 🔍 K - Knowledge Base Organization

### LLM Wiki Structure
Follow Karpathy pattern:
- Curated, interconnected notes
- Consistent tagging
- YAML frontmatter
- Topic-based clustering

### Quality Checklist
Before finalizing any note:
- [ ] Has YAML frontmatter
- [ ] Proper tags (hyphen-separated)
- [ ] Linked to related notes
- [ ] Date updated
- [ ] Status assigned

---

## 🎯 L - LLM Wiki Framework Implementation

### Step 1: Initialize Wiki Folders
```bash
mkdir -p _wiki/{cnc,robotics,ai-models,misc}
```

### Step 2: Create Index Pages
- `_wiki/index.md` - Overall hub
- `_wiki/cnc/index.md` - CNC topics
- `_wiki/ai-models/index.md` - Model docs

### Step 3: Processing Pipeline
```
Inbox → Review (24hr) → Extract Concepts → 
Create Wiki Page → Add Links → Tag Appropriately
```

---

## 🤖 M - Model Documentation Template

Create: `ai-models/models/template.md`

```markdown
---
tags: [ai-model, template]
status: draft
confidence: 0
priority: medium
created: 
last-tested: 
parameters: 
context-window: 
vram-required: 
benchmark-score: 
---

# [Model Name]

## Why This Model?

## Setup Instructions

## Performance Metrics

## Limitations
```

---

## 📈 N - Network Configuration

### If Using Network Models
Ensure ports are open:
- Port 11435 (Ollama)
- Port 5000 (Hermes gateway)
- Port 80 (web APIs)

### Firewall Rules
```bash
# Windows
netsh advfirewall firewall add rule name="Hermes" dir=in action=allow protocol=TCP localport=11435
```

---

## 🗃️ O - Obsidian Optimization Settings

### Recommended Settings
```
Editor: 
- Word wrap: ON
- Spell check: OFF (for code blocks)
- Font: Consolas or Fira Code

Files:
- Use atomic writes: ON
- File recovery: ON

Plugins:
- Dataview: Enable
- Calendar: Enable
- QuickAdd: Enable
```

---

## 📂 P - Path Conventions

### Windows Paths (use double backslashes)
```
E:/tommy vault/tommy vault/Read & Write/
```

### Relative Links
Use:
- `folder/file.md` for files in same vault
- `[[folder/file]]` for wikilinks

### Case Sensitivity
Windows = case-insensitive  
Git remotes = case-sensitive  
Always be consistent!

---

## 🔧 Q - Quality Control Measures

### Automated Checks
- Daily cleanup script (already built)
- Duplicate detection
- Short note removal (< 3 words)
- Orphaned file identification

### Manual Reviews
- Weekly: Check `[[dataview-dashboard]]`
- Monthly: Review tag consistency
- Quarterly: Archive old notes

---

## 📅 R - Repository Management

### Git Best Practices
```bash
# Daily
git add .
git commit -m "Daily update: $(date +%Y-%m-%d)"

# Weekly  
git push origin main

# Backup
git bundle create vault-backup.bundle --all
```

---

## 📚 S - Scripts to Always Keep

Essential scripts (store in `scripts/`):
1. `wiki_ingest.py` - Web → Vault
2. `daily_vault_cleanup.py` - Maintenance
3. `vault_status.py` - Health check
4. `update_vault_quick.py` - Updates

---

## 🎯 T - Tag Taxonomy

### Core Tags
- `#ai-model` - AI model documentation
- `#cnc` - Manufacturing
- `#robotics` - Robotics integration
- `#knowledge-management` - Wiki setup
- `#hermes-integration` - Agent setup

### Status Tags
- `#status:draft`
- `#status:current`  
- `#status:archived`

---

## 🔗 U - Update Frequency Schedule

### Daily (5AM)
- Vault cleanup
- Quality checks
- Daily digest

### Weekly
- Model benchmark updates
- Link verification
- Backup creation

### Monthly
- Tag audit
- Archive review
- Performance tuning

---

## 📝 V - Vault Version Control

### Version File
Create: `memories/vault-version.md`

```markdown
# Vault Version History

## v1.0.0 (2026-08-19)
- Initial LLM Wiki setup
- Hermes integration
- Dataview active
- AI model catalog
- Daily automation

## Changelog
- Update this file on major changes
```

---

## 📊 W - Web Integration Points

### Bookmark These URLs
- GitHub - Your vault remotes
- Ollama - Local models
- HuggingFace - Model downloads
- Your documentation sites

### API Endpoints
- `http://localhost:11435/api/generate` (Ollama)
- `http://hermes-agent:8000/` (Hermes)

---

## 🔧 X - XML/YAML Configuration Files

### Keep These Backup Files
```
.hermes/config.yaml          # Hermes config
.hermes/profiles/default/     # Profile settings
scripts/.env.example         # Environment template
docker-compose.yml           # Container setup
```

---

## 📈 Y - YAML Frontmatter Best Practices

### Required Fields (Always Add)
```yaml
---
tags: [your, tags]
created: 2026-08-19
last-updated: 2026-08-19
status: current
priority: high
confidence: 85
---
```

### Optional Fields
```yaml
model: qwen3.5-hermes
vram-required: 5GB
context-window: 128K
benchmark-score: 95
hardware-tier: mid-range
```

---

## 🎉 Z - Zero to Hero Checklist

### Quick Setup Checklist
- [ ] Install Obsidian + plugins
- [ ] Restore vault from backup
- [ ] Initialize Git tracking
- [ ] Run daily cleanup script
- [ ] Enable Dataview
- [ ] Check `[[dataview-dashboard]]`
- [ ] Verify `[[model-comparison-dataview]]`
- [ ] Set up cron jobs
- [ ] Test automation at 5AM

### Test Everything
- [ ] Open `[[master_index]]` - navigation works
- [ ] Open `[[dataview-dashboard]]` - tables render
- [ ] Create new note - frontmatter auto-applies
- [ ] Run `[[daily-technical-digest]]` - fresh data
- [ ] Run cleanup - no errors

---

## 🎈 Final Notes

**Congratulations!** You now have a complete, production-ready vault setup.

### Emergency Recovery
If something breaks:
1. Check `[[master_index]]` for setup notes
2. Run `[[dataview-setup]]` for plugin guide
3. Restore from Git or backup
4. Check `[[vault-status]]` for health

### Next Steps
- Add more topics to your wiki
- Sync with cloud storage
- Set up mobile Obsidian app
- Share knowledge with team

---

## 📦 Export Bundle Location

For future reinstalls, keep this bundle ready:
```
Location: E:/tommy vault/
Bundle files:
- vault-backup.bundle (from Git)
- vault-full-backup.zip (from OS files)
- setup-notes.md (this file)
```

---

*This guide will save you 10+ hours on next rebuild!* 🚀

**Version:** 1.0 | **Last Updated:** 2026-08-19 | **Author:** Tommy Chan
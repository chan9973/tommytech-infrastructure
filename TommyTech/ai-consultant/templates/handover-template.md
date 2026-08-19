# TommyTech AI Setup — Handover Document

**Client:** {{client.name}}  
**Date:** {{datetime}}  
**Setup Method:** {{deployment.method}}  
**Support Window:** {{support.duration_days}} days  

---

## ✅ Installation Summary

### AI Stack
- **Python:** {{ai_stack.python_version}} virtual environment
- **Ollama Model:** {{ai_stack.ollama_model}}
- **Provider:** {{ai_stack.provider}}

### Vault
- **Location:** `{{vault.path}}`
- **Structure:** Standard with Inbox, _wiki, Templates, scripts/

### Agents Deployed
| Agent | Type | Status |
|---|---|---|
| Research Agent | Web research + wiki | {{agents[0].enabled}} |
| Coding Agent | Code assistance | {{agents[1].enabled}} |
| Support Agent | Q&A bot ({{agents[2].language}}) | {{agents[2].enabled}} |

---

## 🎯 Quick Start Guide

### 1. Start Hermes Agent
```bash
cd "{{vault.path}}\TommyTech\ai-consultant"
call .venv\Scripts\activate.bat
hermes
```

### 2. Ask Your Agent
```
> "What do I know about [topic]?"
> "Research latest [topic] and save to my vault"
> "Write a Python script that [task]"
```

### 3. Search Your Wiki
Open Obsidian and use:
- `[[wikilink]]` — link between notes
- `Ctrl+O` — quick open any note
- Search bar — full-text search

---

## 🛠️ Useful Commands

| Task | Command |
|---|---|
| List all models | `ollama list` |
| Add new content | `python scripts/obsidian-ingest.py "your text"` |
| Run daily cleanup | `python scripts/daily_vault_cleanup.py` |
| Check vault health | `python scripts/vault_status.py` |
| Verify backup | `python scripts/verify_backup.py` |

---

## 🆘 Support

**Window ends:** {{datetime}} + {{support.duration_days}} days  
**Contact:** {{client.contact}} via {{support.contact_method}}  
**SLA:** {{support.response_sla_hours}} hours response time

---

## 📋 Verification Results

{{verification_report}}

---

*This package was deployed entirely by autonomous AI. No human intervention required.*  
* — TommyTech Agent Infrastructure*

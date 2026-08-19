# 🎯 Post-Setup Verification Checklist

Run these checks after setup to confirm everything works:

## 1. Python Environment
- [ ] `python --version` → 3.11+
- [ ] `.venv` exists and activates
- [ ] `pip list` shows hermes-tools installed

## 2. Ollama Service
- [ ] `ollama list` shows model available
- [ ] `ollama run` responds within 10 seconds
- [ ] Port 11434 listening locally

## 3. Hermes Agent
- [ ] `hermes --version` outputs version
- [ ] Agent session starts without errors
- [ ] Can read/write Obsidian vault files

## 4. Obsidian Vault
- [ ] Vault opens in Obsidian app
- [ ] Dataview plugin shows queries working
- [ ] Wiki ingest creates notes with correct frontmatter
- [ ] Wikilinks resolve to existing notes

## 5. Agent Tests
- [ ] Research Agent: Searches web + writes to vault
- [ ] Coding Agent: Runs Python script + saves output
- [ ] Support Agent: Answers FAQ from vault content

## 6. Automation
- [ ] `daily_vault_cleanup.py` runs without errors
- [ ] `obsidian-ingest.py` creates properly tagged notes
- [ ] Backup script creates timestamped archive

## 7. Credentials
- [ ] Client has vault path documented
- [ ] Client knows how to start agents
- [ ] Support window dates recorded

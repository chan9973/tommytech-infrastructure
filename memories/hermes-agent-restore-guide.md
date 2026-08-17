# Hermes Agent Restore Guide

**Last updated:** 2026-08-16  
**User:** Tommy Chan from Ipoh, Malaysia  
**Reinstall date:** 2026-08-16

---

## Quick Answer

### After Windows Reinstall:

```powershell
# Step 1: Install Hermes CLI
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# Step 2: Log in to your GitHub/portal account  
hermes config login

# Step 3: Restore from backup (if you have one)
robocopy "D:\HermesBackups\" "%HERMES_HOME\%" /E /COPYALL

# Step 4: Re-connect gateway and verify tools
hermes setup
hermes doctor
```

---

## Detailed Restore Process

### Phase 1: Initial Installation

After fresh Windows install, you'll need to reinstall Hermes from scratch:

1. **Download installer:**
   ```bash
   curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
   ```

2. **Run setup wizard:**
   ```bash
   hermes setup
   ```
   This will:
   - Install uv (Python package manager)
   - Create venv with dependencies  
   - Set up gateway config
   - Configure your preferred LLM model/provider

3. **Authenticate to portal:**
   ```bash
   hermes config login
   ```
   Follow OAuth flow — grants access to:
   - GitHub skills repository
   - Tool catalog (browser, video generation, MCP servers)
   - API quota management

---

### Phase 2: Restore Your Config & Data

#### What's in `%HERMES_HOME%` (usually `%USERPROFILE%/.hermes/`)

| Component | Location | Backup Priority | How to Restore |
|-----------|----------|-----------------|----------------|
| **Configuration** | `.obsidian/config.yaml` | ✅ HIGH | Copy entire directory |
| **API keys/secrets** | `.env` (secrets ONLY) | 🔴 CRITICAL | Re-enter or use encrypted backup |
| **Skills** | `skills/` folder | ⚠️ MEDIUM | Clone from GitHub if backed up |
| **Skins/themes** | `skins/` folder | ✅ HIGH | Copy or re-download from gallery |
| **Memory** | `memories/` folder (via CLI) | ✅ HIGH | Export before reinstall |
| **Plugins** | `desktop-plugins/` | ⚠️ MEDIUM | Reinstall via config commands |
| **Logs/Sessions** | `logs/`, `state.db` | ❌ LOW | New install OK |

#### Restore Command Options:

```powershell
# Option A: Simple copy entire directory (safest)
robocopy "D:\HermesBackups\" "%USERPROFILE%\.hermes" /E /COPYALL /MT

# Option B: Partial restore (if you only want memories)
xcopy "D:\HermesBackups\memories" "%HERMES_HOME\memories" /E /Y

# Option C: Export configs before reinstall
hermes config export > D:\HermesBackup\config-export.yaml
```

---

### Phase 3: Reinstall Skills & Plugins

#### From GitHub (if you cloned your skills repo):

```powershell
# Navigate to your skills repository
cd "C:\Users\tommy\.hermes\skills"

# List what's installed
Get-ChildItem -Path ".hermes\skills" -Recurse | Select-Object FullName

# Reinstall specific skill
hermes install skill --name video-generation

# Reinstall all from GitHub repo
git clone https://github.com/<your-handle>/hermes-skills.git ~/.hermes/skills
```

#### From local backup:

```powershell
# Copy skills folder entirely
robocopy "D:\HermesBackups\skills" "$home\.hermes\skills" /E /COPYALL

# Verify installations
hermes skill list  # List all available skills
hermes tools list  # Check tool catalog
```

---

### Phase 4: Reconnect Your Gateway & Services

#### Step-by-step:

1. **Configure gateway:**
   ```bash
   hermes proxy --model mistralai/Mixtral-8x7B-Instruct-v0.1
   hermes config set llm.model mistralai/Mixtral-8x7B-Instruct-v0.1
   ```

2. **Test basic functionality:**
   ```bash
   hermes doctor
   hermes --version
   ```

3. **Verify tools:**
   ```bash
   hermes tools list  # Should show browser, terminal, file, etc.
   ```

4. **Re-connect browser automation:**
   ```bash
   hermes config set browser.profile firefox
   hermes config set browser.preferred Firefox
   ```

---

### Phase 5: Re-import Memories (Optional)

If you exported memories before reinstall:

```python
# Python script to import memories back after restore
import json
from pathlib import Path

def import_memories(memories_file, vault_path):
    """Import observed memories into Hermes"""
    with open(memories_file) as f:
        imported = json.load(f)  # Your previously exported list
    
    for mem in imported:
        memory(action="add", **mem)

# Usage after restore:
python import-memories.py --file D:\HermesBackup\memories.json
```

Or run interactive CLI:

```bash
hermes memories add "Your memory content here"
```

---

## Best Practices Going Forward

### 1. **Automate Your Backup** (before each major change):

```powershell
# Save as C:\Windows\System32\wbem\HermesBackup.bat
@echo off
set BACKUP=D:\HermesBackups
set VAULT=E:\tommy vault
set DATE=%date:~-4%%date:~3,2%%date:~0,2%

xcopy "%VAULT%\*" "%BACKUP%\vault_%DATE%\*.*" /E /I /H /K /C /Y
xcopy "$home\.hermes\skills\*" "%BACKUP%\skills_%DATE%\*\*\*.*" /S /E /I /K /Y
xcopy "$home\.hermes\skins\*" "%BACKUP%\skins_%DATE%\*.*" /E /I /K /Y

echo ====================================
echo Hermes Backup Complete: %DATE%
echo Files backed up:
dir "%BACKUP\\" | find "HermesBackup"
echo ====================================
```

Schedule this via Task Scheduler to run weekly.

---

### 2. **Keep Skills on GitHub** (version-controlled):

```bash
# Create a public/private repo for your custom skills
git clone https://github.com/NousResearch/hermes-skills.git ~/.hermes/skills
git remote add hermes-subs https://github.com/NousResearch/hermes-skills-submissions.git

# Before reinstall, commit everything
git add .
git commit -m "Updated skill installations"
git push
```

### 3. **Test Restore Process** (important!):

Before major Windows updates:
1. Copy backup to external drive
2. Boot into recovery mode on alternate machine  
3. Run restore commands
4. Verify all tools load correctly
5. Test browser automation works

---

## Common Issues After Reinstall

### ❌ "**Missing permissions after restore**"
```bash
# Fix: Set correct user/permissions
hermes config set display.interface tui
hermes config set proxy.enabled true
```

### ❌ "**Skills not loading from backup**"  
```bash
# Clear cache and reinstall
cd $home\.hermes\skills
rm -rf __pycache__
hermes skill refresh  # If command exists
```

### ❌ "**Browser not connecting**"
```bash
# Re-authenticate browser session
hermes browser logout
hermes browser login --profile firefox
```

---

## Emergency Recovery (if you have no backup)

If you didn't backup and need everything restored:

1. **Reinstall Hermes:**
   ```bash
   curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
   hermes setup
   ```

2. **Re-authenticate:**
   ```bash
   hermes config login  # GitHub portal authentication
   ```

3. **Reclaim skills and tools:**
   - Most bundled skills are pre-installed
   - Visit [https://hermes-agent.nousresearch.com](URL) for skill catalog
   - Download any custom skills you need (check docs repository)

4. **Re-create your knowledge base:**
   - Rebuild Obsidian notes in `E:/tommy vault`
   - Re-run research scripts via `skills/` commands
   - Re-import important memories using hermes memories add

---

## Verification Commands (Run After Restore)

```bash
# Check installation
hermes --version  
hermes doctor

# Verify tools catalog
hermes tools list

# List skills
hermes skill list

# Check memory count
memory  # Should show your entries

# Test basic workflow
terminal(command="hello from hermes", timeout=5)
```

---

## Related Resources

- [[obsidian-backup-restore-guide]] - For Obsidian vault preservation
- [[disaster-recovery-plan]] - System-wide backup strategies
- [[hermes-agent]] - Skill reference for configuration commands
- [[security-privacy]] - How to securely manage `.env` secrets

---

**Quick Reference Card:**

| Task | Command | Frequency |
|------|---------|-----------|
| Full Vault Backup | `robocopy D:HermesBackups\ E:\...` | Weekly |
| Skills Backup | Git commit/push to GitHub | Before major changes |
| Test Restore | Boot from USB + restore | Quarterly |
| Re-authenticate | `hermes config login` | After reinstall |

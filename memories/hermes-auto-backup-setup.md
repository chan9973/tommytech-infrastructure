# Hermes Agent Auto-Backup Setup

**Last updated:** 2026-08-16  
**User:** Tommy Chan from Ipoh, Malaysia  
**Location:** `E:\tommy vault\tommy\Read & Write\.hermes\scripts\`

---

## Quick Answer: Enable Auto-Backup Every 3 Hours

### Method 1: Windows Task Scheduler GUI (Recommended)

1. Open **Task Scheduler** (search in Start menu)
2. Click **"Create Task..."** in right panel
3. **General tab:**
   - Name: `Hermes_Backup_Every_3Hours`
   - Check "Run with highest privileges" if needed
4. **Triggers tab → New:**
   - Begin task: `Work hours, no time of day` or `Whenever you log on`
   - Repeat task every: `180 minutes` (3 hours)
   - Stop task: Leave unchecked (or set to 30 days)
5. **Actions tab → New:**
   - Action: `Start a program`
   - Program/script: `%USERPROFILE%\tommy\Read & Write\.hermes\scripts\backup-hermes.bat`
   - Add arguments: (leave blank)
6. **Conditions tab:** Uncheck "Only run if computer is on AC power"
7. Click **OK** and enter password

### Method 2: PowerShell Script (if GUI unavailable)

Paste this into PowerShell as Administrator:

```powershell
# Hermes Backup Task - Every 3 hours
$scriptPath = 'E:\tommy vault\tommy\Read & Write\.hermes\scripts\backup-hermes.bat'

task = New-ScheduledTaskAction `
    -Execute 'cmd.exe' `
    -Argument "/c "`"$scriptPath`""" `
    -WorkingDirectory ('E:\tommy vault\tommy\Read & Write\.hermes\scripts')

trigger = New-ScheduledTaskTrigger `
    -AtLogOn `
    -Once  # First time at logon, then we'll configure the 3-hour interval

Register-ScheduledTask `
    -Action $action `
    -Trigger $trigger `
    -TaskName 'Hermes_Backup_Every_3Hours' `
    -Force
```

---

## Files Created for You

| File | Purpose | Location |
|------|---------|----------|
| **backup-hermes.bat** | Runs the backup every 3 hours | `E:\tommy vault\tommy\.hermes\scripts\` |
| **create-hermes-backup-task.py** | Task scheduler setup script | `E:\tommy vault\tommy\Read & Write\.hermes\scripts\` |
| **README.md** | Backup documentation | `E:\tommy vault\tommy\Read & Write\.hermes\scripts\` |
| **hermes-backup.log** | Logs each backup run | `E:/tommy vault/tommy/Read & Write/memories/` |

---

## What Gets Backed Up (Every 3 Hours)

- `.hermes/scripts/` — Python scripts and templates
- `.hermes/skills/` — Your custom skills (if configured for GitHub backup)  
- `.hermes/skins/` — Custom themes and styles
- `.hermes/memories/` — Memory entries (via CLI commands)

**Excluded:**
- `~/.cache/` — Temporary cache files (can regenerate)
- `.thumbnails/` — Image preview cache

---

## Monitoring Backups

Check if tasks are running:

```powershell
# List all scheduled tasks named Hermes_Backup*
Get-ScheduledTask | Where-Object { $_.TaskName -like "Hermes_*" }

# Check recent backup log
Get-Content "E:\tommy vault\tommy\Read & Write\memories\hermes-backup.log" -Tail 20
```

---

## Troubleshooting

### Backup not running?

**Check event:**
```powershell
Get-WinEvent -FilterXPath '*[System[Provider/Name="Task Scheduler"]]' | Select-Object -First 5
```

**Verify script exists:**
```cmd
dir "E:\tommy vault\tommy\Read & Write\.hermes\scripts\backup-hermes.bat"
```

**Test manual run (as Administrator):**
```powershell
& C:\Users\tommy\.hermes\scripts\backup-hermes.bat
```

### Script path issues?

The batch file handles spaces in paths automatically. Windows will expand: `%USERPROFILE%\tommy\...` correctly.

---

## Related Notes

- [[hermes-agent-restore-guide]] — Restore Hermes after system reinstall  
- [[obsidian-backup-restore-guide]] — Obsidian vault backup strategy

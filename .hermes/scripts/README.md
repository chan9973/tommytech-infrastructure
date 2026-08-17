# Hermes Auto-Backup System

**Location:** `E:\tommy vault\tommy\Read & Write\.hermes\scripts\`  
**Schedule:** Every 3 hours automatically  
**Last updated:** 2026-08-16 by Tommy Chan from Ipoh, Malaysia

---

## Quick Setup

Run this command to enable auto-backup:

```powershell
python "E:\tommy vault\tommy\Read & Write\.hermes\scripts\create-hermes-backup-task.py" as Administrator
```

Or simply copy and paste the schtasks command:

```cmd
schtasks /Create /TN "Hermes_Backup_Every_3Hrs" /TR "cmd /c \"E:\tommy vault\tommy\Read & Write\.hermes\scripts\backup-hermes.bat\"" /SC HOURLY /MO 3 /ST 09
```

---

## What Gets Backed Up

The following folders are backed up every 3 hours:

| Location | Purpose | Size |
|----------|---------|------|
| `~/.hermes/` | Config files, skills, settings | ~50MB typical |
| `.hermes_backup/` | Timestamped backups | Unlimited |

---

## Backup Files Created

Backups go to: `\tommy vault\tommy\Read & Write\.hermes\_backup\`

Naming pattern: `E:\tommy vault\tommy\.hermes_YYYYMMDD_HHMMSS\`

Example:
- `.hermes_20260816__300000\` — Backup created at 03:00 AM on Aug 16, 2026
- `.hermes_20260816__060000\` — Backup created at 06:00 AM
- `.hermes_20260816__090000\` — Backup created at 09:00 AM

---

## Manual Run (When Needed)

To run backup immediately:

```powershell
cmd /c "E:\tommy vault\tommy\Read & Write\.hermes\scripts\backup-hermes.bat"
```

---

## Monitoring

Check log file for backup history:

```
E:/tommy vault/tommy/Read & Write/memories/hermes-backup.log
```

Last 10 entries:

```bash
Get-Content "E:\tommy vault\tommy\Read & Write\memories\hermes-backup.log" -Tail 10
```

---

## Troubleshooting

### Task not running?

**Check scheduler:**
```cmd
schtasks /Query /TN "Hermes_Backup_Every_3Hrs"
```

### Script path has spaces?

The batch script handles spaces in paths automatically via quotes: `backup-hermes.bat`

### Delete old backups?

Keep only last 30 days:
```powershell
Get-ChildItem -Path "E:\tommy vault\tommy\.hermes\_backup" -Filter "*.tmp" | Remove-Item
```

---

## Files Created for You

1. **Python script** (.py) — For programmatic backups and Task Scheduler
2. **Batch script** (.bat) — Windows-native execution
3. **Log file** — Backup history tracking
4. **Task creation script** — Automates scheduled task setup

All files are in: `E:\tommy vault\tommy\Read & Write\.hermes\scripts\`

---

## Related Notes

- [[obsidian-backup-restore-guide]] — Obsidian vault backup strategy
- [[hermes-agent-restore-guide]] — Full Hermes restoration procedures
- [[disaster-recovery-plan]] — System-wide backup planning

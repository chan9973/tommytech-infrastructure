# Daily Vault Cleanup Setup

## Overview
This setup automates daily cleanup and maintenance of your Obsidian vault at 5am.

## Files Created

### 1. Main Cleanup Script
**Location:** `scripts/daily_vault_cleanup.py`

Features:
- Detects and removes duplicate notes (based on content hash)
- Finds orphaned/template files for review
- Updates the vault index
- Generates daily quality report
- All actions logged to `memories/daily-cleanup.log`

### 2. Windows Batch Wrapper
**Location:** `scripts/daily_cleanup.bat`

Simple batch file that runs the Python script and generates a report.

### 3. Scheduled Task Setup Script
**Location:** `scripts/setup_scheduled_task.py`

Helper script to create Windows Task Scheduler entry.

## Setup Instructions

### Option 1: Windows Task Scheduler (Recommended)

Open **Command Prompt as Administrator** and run:

```cmd
schtasks /Create /TN "Daily Obsidian Vault Cleanup" /TR "E:\tommy vault\tommy vault\Read & Write\scripts\daily_cleanup.bat" /SC DAILY /ST 05:00 /RL HIGHEST /F
```

To verify it was created:
```cmd
schtasks /Query /TN "Daily Obsidian Vault Cleanup"
```

### Option 2: Hermes Cron Job (Alternative)

Run this command in Hermes:
```bash
cronjob create \
  --schedule "0 5 * * *" \
  --prompt "python E:/tommy vault/tommy vault/Read & Write/scripts/daily_vault_cleanup.py" \
  --name "Daily Obsidian Vault Cleanup"
```

### Option 3: Manual Setup (No Admin Required)

If you can't use Task Scheduler, you can run it manually:
```bash
python "E:/tommy vault/tommy vault/Read & Write/scripts/daily_vault_cleanup.py"
```

## Output Files

- **Log:** `memories/daily-cleanup.log` - All cleanup actions
- **Report:** `memories/vault-quality-report.md` - Daily metrics
- **Quarantine:** `memories/quarantine/` - Removed duplicates

## Vault Statistics (After First Run)
- Total Notes: 99
- Total Size: 0.45 MB
- Duplicates Removed: 3
- Potential Orphaned Files: 2

## To Modify Schedule

Change the time in the schtasks command:
- `/ST 05:00` - 5:00 AM
- `/ST 06:00` - 6:00 AM
- `/ST 03:00` - 3:00 AM

Example for 6 AM:
```cmd
schtasks /Change /TN "Daily Obsidian Vault Cleanup" /ST 06:00
```

## To Delete the Task
```cmd
schtasks /Delete /TN "Daily Obsidian Vault Cleanup" /F
```
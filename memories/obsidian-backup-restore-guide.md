# Obsidian Vault Backup & Restore Guide

**Last updated:** 2026-08-16  
**Vault location:** `E:/tommy vault/tommy vault/Read & Write`  
**Platform:** Windows (Windows 11)

---

## Quick Answer

### To backup (do this regularly):
```powershell
# Find your vault first (it's usually in Documents or Desktop)
Get-ChildItem -Path $home\Documents | Where-Object { $_.Name -match 'vault|Obsidian' }

# Copy the entire folder to external drive/cloud
Copy-Item -Path "E:\tommy vault" -Destination "D:\Backup\" -Recurse
```

### To restore (after system reinstall):
1. Extract backup to `E:/` (or your preferred drive)
2. Open Obsidian → New Vault → Browse → Select restored folder
3. Verify all wikilinks work

---

## Recommended Backup Strategy

### 1. **External Drive** (most reliable)
- Connect USB drive or external HDD each week
- Copy entire vault folder
- Label with date on drive

```powershell
# Backup script - save as backup-vault.bat
@echo off
set VAULT=E:\tommy vault
set DATE=%date:~-4%%date:~3,2%%date:~0,2%
set BACKUP="D:\Obsidian Backups\tommy_vault_%DATE%"
mkdir "%BACKUP%" 2>nul
xcopy "%VAULT\*" "%BACKUP%\*.*" /E /I /H /K /C /Y
echo Backup created: %BACKUP%
```

### 2. **Cloud Sync** (automatic, but watch out!)
- **DO USE:** GitHub (if public/repo), Nextcloud, Syncthing, ResilioSync
- **BE CAREFUL WITH:** OneDrive/Google Drive direct sync (can cause file conflicts)
  - Obsidian files have edit locks that confuse cloud sync
  - Prefer backup destinations only, not live-sync

### 3. **Multiple Versions**
Keep 2-3 dated backups:
```
D:\Obsidian Backups\
  ├── tommy_vault_20260815/
  ├── tommy_vault_20260724/
  └── old_archive/ (anything older than 90 days)
```

---

## Restore Process (System Reinstall)

### Before reinstalling Windows:
1. Backup vault externally (USB drive/cloud)
2. Unzip backup to a safe location (`D:/` or USB root folder)
3. **Test restore** on a secondary device if possible

### After reinstall:
```bash
# 1. Restore vault location
robocopy D:\Obsidian\tommy_vault_20260815 "E:\tommy vault" /E /COPYALL

# OR simply copy the folder manually via File Explorer
# Easiest: drag & drop backup to E:\ then rename to original folder name
```

### Post-restore verification:
1. Open Obsidian → New Vault → Select restored folder
2. Check [[links]] between notes open correctly
3. Verify plugins installed (you may need to re-enable)
4. Confirm theme settings persisted

---

## What's Included in Your Vault Backup

Your vault `E:/tommy vault/tommy vault/Read & Write` typically contains:

| Folder | Purpose | Must Backup? |
|--------|---------|--------------|
| `.obsidian/` | Settings, plugins, themes | ✅ YES (includes `snippets/`, `app-data/config.json`) |
| `memories/` | Research notes, wikilinks | ✅ YES |
| `resources/` or similar | Images, PDFs, assets | ✅ YES |
| Any note files (`*.md`) | Your actual notes | ✅ YES |

⚠️ **Never delete `.obsidian/app-data/`** — contains plugin data and settings!

---

## Common Pitfalls to Avoid

### ❌ Don't trust OneDrive Desktop Sync on vault folders
- Obsidian's app locks cause sync conflicts
- Results in "conflicting copy" errors or corrupted JSON configs

✅ **Instead:** Use Obsidian's publish-to-WebDAV feature with Nextcloud/Syncthing for cloud sync

### ❌ Don't ignore the `.obsidian/cache` folder
- Tiny (~KB) but important for theme/plugin performance
- Can be deleted on restore if you want clean slate (Obsidian regenerates)

### ❌ Don't backup only "Notes" folder
You need the ENTIRE vault including:
- `[.obsidian](file://E:/tommy%20vault/tommy%20vault/Read%20%20Write/.obsidian/)` config
- Hidden folders (`.cache`, `.thumbnail-cache`)

### ✅ DO use versioned backup folder names
This makes restore simpler: just point Obsidian to latest version

---

## Emergency Restore Checklist

**If something goes wrong (corrupted vault, malware, etc.):**

1. [ ] Boot into recovery environment or live USB
2. [ ] Extract backup vault to `E:/` (any working drive)
3. [ ] Rename restored folder: `tommy_vault_YYYYMMDD → tommy/Read & Write`
4. [ ] Launch Obsidian desktop app (not the vault) → New Vault → Browse to new location
5. [ ] Test critical notes open and links resolve
6. [ ] Reinstall plugins if needed from `.obsidian/plugins/backup_list.txt`

---

## Automation (Optional: Advanced users)

### Automated backup script with timestamp:

```python
# !/usr/bin/env python3

"""Automated Obsidian vault backup to cloud storage"""
import datetime
import shutil
import os

VAULT_PATH = r"E:\tommy vault\tommy vault\Read & Write"
BACKUP_PATH = r"D:\Obsidian Backups"

def backup_vault():
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    backup_name = f"tommy_vault_{date_str}"
    backup_dst = os.path.join(BACKUP_PATH, backup_name)
    
    if os.path.exists(backup_dst):
        shutil.rmtree(backup_dst)
    
    shutil.copytree(VAULT_PATH, backup_dst)
    print(f"✅ Backup created: D:\\Obsidian Backups\\{backup_name}\\")

if __name__ == "__main__":
    backup_vault()
```

Save as `~/tommy/.obsidian/scripts/backup-vault.py` and schedule with Task Scheduler.

---

## Cloud Provider Recommendations

| Provider | Good For | Notes |
|----------|----------|-------|
| **GitHub** | Public/vetted content | Push vault (as private) directly |
| **Nextcloud** | Self-hosted sync | Use WebDAV publish feature |
| **Syncthing** | Peer-to-peer backup | No cloud needed, just backup to USB |
| **ResilioSync** | BitTorrent-style backup | Good for large media vaults |
| **Google Drive** | Simple cloud backup | Set up "Files" only, not live sync |

---

## Related Resources

- [[vault-management]] - Vault organization strategies
- [[disaster-recovery]] - System failure preparation notes
- [[obsidian-plugins]] - Built-in plugins like Git for GitHub integration

---

**Emergency Contacts:**
- Primary backup: `D:\Obsidian Backups\` (external drive)
- Secondary backup: Google Drive folder (via publish feature)
- Last good backup date: Check most recent folder in backup directory

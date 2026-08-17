# Obsidian Backup & Restore (class-level skill)

**Category:** data-management / observance  
**Trigger:** User asks about vault preservation, system reinstall prep, or recovery scenarios. Use this skill before any OS upgrade, migration, or system restore operation.

---

## Scope & Responsibilities

This skill manages:
- **Backup workflows** (manual/automated, external drive/cloud sync)  
- **Restore procedures** (post-reinstall, disaster recovery)  
- **Vault integrity verification** (post-restore link checks, plugin re-install)  
- **Risk mitigation strategies** (OneDrive/Google Drive conflict avoidance)

**DO NOT:** Treat this as a generic IT support procedure — it's specific to Obsidian's file lock behavior, `.obsidian/app-data/` config persistence, and Windows backup tool quirks.

---

## Canonical Workflow

### Pre-Reinstall Backup Sequence

1. **Locate vault path.** Most users store in `C:\Users\[user]\Documents\[vault-folder]` or custom paths like `E:\tommy vault\[vault]`.

2. **Copy ENTIRE folder to backup destination:**
   ```powershell
   # PowerShell (recommended for Windows)
   Copy-Item -Path "E:\tommy vault" -Destination "D:\Backup\" -Recurse
   
   # Or use robocopy for reliability on large vaults
   robocopy "E:\tommy vault" "D:\Backup\tommy_vault_$(Get-Date -Format yyyyMMdd)" /E /COPYALL
   ```

3. **External drive or USB verification:** If primary backup fails, copy to labeled external drive. Label the drive with restore date.

4. **Cloud alternative (avoid conflicting sync):** Use GitHub for public/vetted vaults, or Obsidian's Publish-to-WebDAV with Nextcloud/Syncthing.
   ```powershell
   # Push vault to GitHub repo (if .git exists)
   git add .
   git commit -m "Pre-reinstall backup"
   git push origin main
   ```

5. **Test restore on secondary device** (optional but recommended): Copy restored vault to another machine, open in Obsidian, verify [[wikilinks]] resolve.

6. **Document last good backup date:** Add note to vault root `.obsidian/version-notes.md` or `memories/backup-log.md`.

---

### Post-Reinstall Restore Sequence

1. **Extract/restored vault to target location.** Place in original path (`E:\tommy vault\`) or create new vault folder and re-add to Obsidian.

2. **Verify structure intact:**
   ```bash
   # PowerShell verification
   Get-ChildItem "E:\tommy vault" -Recurse | Measure-Object | Select-Object Count
   
   # Should match pre-backup count if no new notes added
   ```

3. **Open Obsidian → New Vault → Browse** to restored folder. All settings, plugins, themes persist in `.obsidian/app-data/config.json`.

4. **Post-restore verification checklist:**
   - [ ] [[wikilinks]] between notes open correctly
   - [ ] All expected notes present (compare file count with backup timestamp)
   - [ ] Plugins enabled from `~/.obsidian/plugins/` folder
   - [ ] Custom themes applied (from `.obsidian/snippets/`, `.obsidian/themes/default.theme`)

5. **If plugins missing:** Re-install from Obsidian's Community Plugins browser or restore from plugin manifest file stored in vault root.

---

## Pitfalls & How to Avoid Them

### ❌ OneDrive/Google Drive Direct Sync → Corrupted JSON configs
Obsidian's app uses file locks on notes during editing. Cloud sync services detect these as conflicts and:
- Create "conflicting copy" versions
- Merge partial writes incorrectly
- Eventually produce unreadable `config.json` or note files

✅ **Solution:** Use Obsidian's built-in Publish-to-WebDAV for cloud sync (not direct Desktop Sync), or use Syncthing/ResilioSync for peer-peer backup without merge conflicts.

### ❌ Missing `.obsidian/app-data/` folder → Lost plugins
The vault contains note folders, but plugin state lives in `.obsidian/app-data/config.json`. Always backup entire vault directory, not just `Notes/`, `memories/`, etc.

✅ **Solution:** Copy ENTIRE vault path with hidden files included (PowerShell `-Recurse` handles this, but be explicit: don't exclude hidden folder patterns).

### ❌ Deleting cache folders on restore
The `.obsidian/cache` folder contains theme thumbnail caches and plugin performance caches. Deleting won't break functionality — Obsidian regenerates them — but it's faster to leave alone. Only delete if you suspect corruption after restore.

### ❌ Ignoring backup versioning strategy
Single backup point becomes risky over time (accidental deletion, corrupt write). Keep 2-3 dated backups:
```
D:\Obsidian Backups\
  ├── tommy_vault_20260815/   ← current
  ├── tommy_vault_20260724/   ← last previous (7+ days old)
  └── tommy_vault_20260612/   ← rollback point (>90 days)
```

---

## Related Resources

- [[vault-management]] — Vault folder structure, note organization patterns  
- [[teamviewer-vs-anypc]] — Remote access tool comparisons (use AnyPC for cross-device vault restore monitoring)  
- [[local-model-inference]] — LLM backup strategies for knowledge extraction before cloud transfer

---

## Decision Matrix: What to Backup?

| Item | Must Backup? | Why |
|------|--------------|------|
| `notes/`, `read/`, `memories/` | ✅ YES | Your actual knowledge base |
| `.obsidian/snippets/` | ✅ YES | Personal shortcuts, template macros |
| `.obsidian/app-data/config.json` | ✅ YES | Plugin config, editor settings, theme overrides |
| `.obsidian/cache/*` | ⚠️ OPTIONAL | Can regenerate; safe to delete on restore if space needed |
| `.obsidian/plugins/*.manifest.yml` | ✅ YES | Track which plugins installed for re-install |
| `images/`, `pdfs/` (in vault root) | ✅ YES | Embedded assets in [[wikilinks]] |

---

## Emergency Contacts & References

- Primary backup location: `D:\Obsidian Backups\`  
- Secondary backup: GitHub private repo (`https://github.com/[user]/tommy-vault`)  
- Vault path on current system (Windows): `E:\tommy vault\tommy vault\Read & Write`  
- Last successful backup date: Check most recent folder in `D:\Obsidian Backups\`

---

## Related Notes (Wikilinks)

- [[obsidian-backup-restore-guide]] — Detailed step-by-step procedures with scripts  
- [[vault-management]] — Vault structure documentation  
- [[disaster-recovery]] — System failure preparation and incident response

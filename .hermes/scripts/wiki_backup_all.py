"""
COMPREHENSIVE SELF-IMPROVEMENT DATA BACKUP SCRIPT
Creates timestamped backup of all persistent knowledge stores.
Run this regularly (cron or manual) before system changes.
"""

from datetime import datetime
import shutil
import os

SOURCE_VAULT = r"E:\tommy vault\tommy vault\Read & Write"
BACKUP_ROOT = os.path.expanduser(rf"~/{datetime.now():%Y}%m")  # Year-Month structure
DESTINATION_PATH = f"{BACKUP_ROOT}wiki-backup-{datetime.now():%d-%H%M%S}.zip"

def backup_vault():
    """Create compressed backup of entire vault with metadata."""
    
    # Create timestamp directories  
    year_month = f"~/{datetime.now():%Y}/{datetime.now():%m}"
    os.makedirs(year_month, exist_ok=True)
    
    # Main vault backup (includes memories, notes, all data)
    print(f"[{datetime.now().strftime('%H:%M')}] Creating complete vault backup...")
    
    source = SOURCE_VAULT
    
    try:
        # Create full backup with metadata
        shutil.make_archive(
            f"{year_month}wiki-backup-{datetime.now():%d-%H%M%S}",
            'zip',
            source,
            exclude_dirs=['.hermes/scripts', '.git', '.DS_Store']
        )
        
        # Also create raw folder copy for quick recovery without unzip overhead
        backup_folder = f"{year_month}/raw-{datetime.now():%d-%H%M%S}"
        os.makedirs(backup_folder, exist_ok=True)
        
        # Mirror structure to raw folder
        rel_path = source[len(os.getcwd()):].lstrip('/')
        shutil.copytree(source, f"{backup_folder}/{rel_path}", 
                      ignore=lambda src, dst: not os.path.exists(dst) or ".git" in src.lower())
        
        print(f"[{datetime.now().strftime('%H:%M')}] Backup complete!")
        print(f"  Compressed: ~/{year_month}wiki-backup-{datetime.now():%d-%H%M%S}.zip")
        print(f"  Raw folder: ~/{backup_folder}")
        
        # Create backup manifest
        import subprocess
        result = subprocess.run(['powershell', 'Get-ChildItem', '-Path', 
                                SOURCE_VAULT, '-Recurse', '-File', '|', 
                                'Select-Object', 'Name', 'Length', 'LastWriteTime', '|' ,
                                'Format-Table'], timeout=60)
        
        manifest = f"""# Backup Manifest - Created {datetime.now():%Y-%m-%d %H:%M:%S}
## Vault Location: {source}

### Backup Contents:
- All notes, memories, wikilinks
- Memory snapshots from Hermes sessions
- Project documentation
- Research and journal entries

### Restore Steps:
## From ZIP:
1. Extract to E:/restored-vault/
2. Verify .obsidian/community-plugins matches Obsidian settings
3. Reconnect Hermes workspace path if needed

## From Raw Folder (Fast):
1. Copy entire {backup_folder} content to E:/restored-vault/
2. Open in Obsidian/Hermes

### Verification Commands:
Run this to verify backup integrity:
```powershell
# Count files before/after restore-CountItemsInBucket -Path "E:\\tommy vault\\tommy vault\\Read & Write" |
# Measure-Object -Property Count | Select-Object -Property Count

# Verify ZIP contents
Expand-Archive -Path "~\{year_month}wiki-backup-{datetime.now():%d-%H%M%S}.zip" `
    -DestinationPath E:\\test-vault\\restore -Force

Compare-Objects (Get-ChildItem "E:\\tommy vault\\tommy vault\\Read & Write") `
    (Get-ChildItem "E:\\test-vault\\restore") |
Format-List
"""
        
        with open(f"{backup_folder}BACKUP_MANIFEST.md", 'w') as f:
            f.write(manifest)
            
        print(f"  Manifest saved to: {year_month}{backup_folder}-BACKUP_MANIFEST.md")
        return True
        
    except Exception as e:
        print(f"Error during backup: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = backup_vault()
    if success:
        print("\n✅ Backup completed successfully!")
        print("\nNext steps:")
        print("1. This script should run automatically via cronjob")
        print("2. Store backups on external drive or cloud")
        print("3. Verify backup integrity monthly")
    else:
        print("\n❌ Backup failed - check error output above")

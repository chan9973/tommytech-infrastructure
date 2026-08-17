#!/usr/bin/env python3
"""
Hermes Agent Auto-Backup Script - Runs every 3 hours

Author: Tommy Chan from Ipoh, Malaysia
Location: E:/tommy vault/tommy vault/Read & Write
Date: 2026-08-16
"""
import os
import shutil
import datetime
from pathlib import Path

# Configuration
VAULT_BACKUP_DIR = r"E:\tommy vault\tommy vault\.hermes_backup"
SOURCE_HERMES_DIR = r"C:\Users\tommy\.hermes"
LOG_FILE = "E:/tommy vault/tommy vault/Read & Write/memories/hermes-backup.log"

def main():
    """Main backup function."""
    dt = datetime.datetime.now()
    
    print("=" * 60)
    print(f"Hermes Agent Auto-Backup [{dt.strftime('%Y-%m-%d %H:%M:%S')}]")
    print(f"Source: {SOURCE_HERMES_DIR}")
    print(f"Destination: {VAULT_BACKUP_DIR}")
    print("=" * 60)
    
    dt = datetime.datetime.now()
    timestamp = dt.strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(VAULT_BACKUP_DIR, f".hermes_{timestamp}")
    
    try:
        # Create backup directory
        os.makedirs(VAULT_BACKUP_DIR, exist_ok=True)
        
        print(f"Copying files to {backup_path}...")
        
        # Copy the entire .hermes directory
        if os.path.exists(SOURCE_HERMES_DIR):
            shutil.copytree(SOURCE_HERMES_DIR, backup_path, copy_function=shutil.copy2, dirs_exist_ok=True)
            print(f"✅ Backup completed successfully")
            
            # Count files backed up
            total_files = sum(len(files) for _, _, files in os.walk(backup_path))
            print(f"   Total files: {total_files}")
            
            # Write success to log
            with open(LOG_FILE, "a") as f:
                f.write(f"[{dt.isoformat()}] Backup success - {total_files} files\n")
        else:
            print(f"? Source not found at {SOURCE_HERMES.Dir}, skipping backup")
            
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        with open(LOG_FILE, "a") as f:
            f.write(f"[{dt.isoformat()}] Error: {str(e)}\n")

if __name__ == "__main__":
    main()

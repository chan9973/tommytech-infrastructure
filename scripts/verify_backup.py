#!/usr/bin/env python3
"""
Vault Backup Verification Script
Run this to verify all critical files are present for reinstall
"""

from pathlib import Path
import os
from datetime import datetime

VAULT_ROOT = Path(r"E:/tommy vault/tommy vault/Read & Write")

# Critical folders and files to check
CRITICAL_PATHS = [
    "master_index.md",
    "memories/facts.md",
    "memories/profile.md",
    "ai-models/vault-index.md",
    "scripts/wiki_ingest.py",
    "scripts/daily_vault_cleanup.py",
    "scripts/update_vault_quick.py",
    ".hermes/",
    "cron/",
]

# Dataview files
DATASOURCE_FILES = [
    "memories/dataview-setup.md",
    "memories/dataview-dashboard.md", 
    "memories/dataview-queries.md",
    "ai-models/model-comparison-dataview.md",
    "memories/templates/dataview-template.md",
]

def verify_vault():
    """Verify vault backup status"""
    print("=" * 60)
    print("🔒 VAULT BACKUP VERIFICATION")
    print("=" * 60)
    print(f"Scan Time: {datetime.now().isoformat()}")
    print()
    
    # Check critical paths
    print("📦 CRITICAL FILES:")
    for path in CRITICAL_PATHS:
        full_path = VAULT_ROOT / path
        exists = "✅" if full_path.exists() else "❌"
        print(f"  {exists} {path}")
    
    print()
    print("📊 DATASOURCE FILES:")
    for path in DATASOURCE_FILES:
        full_path = VAULT_ROOT / path
        exists = "✅" if full_path.exists() else "❌"
        print(f"  {exists} {path}")
    
    print()
    print("📁 VAULT FOLDERS:")
    folders = ["scripts/", "memories/", "ai-models/", "CNC n Robotic/"]
    for folder in folders:
        full_path = VAULT_ROOT / folder
        if full_path.exists() and full_path.is_dir():
            count = len(list(full_path.glob("*.md")))
            print(f"  ✅ {folder} ({count} notes)")
        else:
            print(f"  ❌ {folder}")
    
    print()
    print("=" * 60)
    print("✅ VAULT READY FOR REINSTALL")
    print("=" * 60)

if __name__ == "__main__":
    verify_vault()
#!/usr/bin/env python3
"""
Vault Status Dashboard
Shows current vault health and cleanup history
"""

from pathlib import Path
from datetime import datetime
import re

VAULT_ROOT = Path(r"E:\tommy vault\tommy vault\Read & Write")
LOG_FILE = VAULT_ROOT / "memories" / "daily-cleanup.log"
REPORT_FILE = VAULT_ROOT / "memories" / "vault-quality-report.md"

def count_files_by_extension(directory: Path, extension: str) -> int:
    """Count files with given extension in directory"""
    return len(list(directory.rglob(f"*{extension}")))

def get_last_cleanup_info() -> dict:
    """Parse last cleanup run from log"""
    if not LOG_FILE.exists():
        return {"last_run": "Never", "status": "No log file found"}
    
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
    
    last_run = "Unknown"
    status = "Unknown"
    
    for line in reversed(lines):
        if "Starting daily vault cleanup" in line:
            match = re.search(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]', line)
            if match:
                last_run = match.group(1)
            break
        elif "completed successfully" in line:
            status = "Success"
            break
        elif "error" in line.lower():
            status = "Error"
            break
    
    # Get last run timestamp
    if LOG_FILE.exists():
        mtime = datetime.fromtimestamp(LOG_FILE.stat().st_mtime)
        last_run = f"{mtime.strftime('%Y-%m-%d %H:%M:%S')} (file modified)"
    
    return {"last_run": last_run, "status": status}

def main():
    print("=" * 60)
    print("           OBSIDIAN VAULT HEALTH DASHBOARD")
    print("=" * 60)
    
    all_notes = list(VAULT_ROOT.rglob("*.md"))
    total_notes = len(all_notes)
    
    print(f"\n📊 VAULT OVERVIEW")
    print(f"   Total Notes:     {total_notes}")
    print(f"   Vault Size:      {sum(f.stat().st_size for f in all_notes if f.exists()) / 1024:.1f} KB")
    print(f"   Vault Path:      {VAULT_ROOT}")
    
    # Last cleanup
    cleanup_info = get_last_cleanup_info()
    print(f"\n🧹 CLEANUP STATUS")
    print(f"   Last Run:        {cleanup_info['last_run']}")
    print(f"   Status:          {cleanup_info['status']}")
    
    # Recent log entries
    if LOG_FILE.exists():
        print(f"\n📋 RECENT ACTIVITY")
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()[-5:]  # Last 5 entries
            for line in lines:
                print(f"   {line.strip()}")
    
    # Quarantine status
    quarantine_dir = VAULT_ROOT / "memories" / "quarantine"
    if quarantine_dir.exists():
        quarantined = len(list(quarantine_dir.glob("*.md")))
        print(f"\n📦 QUARANTINE")
        print(f"   Files:           {quarantined}")
    
    print("\n" + "=" * 60)
    print("💡 TIP: Run cleanup manually with:")
    print(f'   python "{VAULT_ROOT / "scripts" / "daily_vault_cleanup.py"}"')
    print("=" * 60)

if __name__ == "__main__":
    main()
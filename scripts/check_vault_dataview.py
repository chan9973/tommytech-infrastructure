#!/usr/bin/env python3
"""Quick script to check vault structure for Dataview"""

from pathlib import Path

vault = Path(r"E:/tommy vault/tommy vault/Read & Write")

print("📂 Vault Structure Check")
print("=" * 50)

# Count files by folder
for folder in sorted(vault.iterdir()):
    if folder.is_dir() and not folder.name.startswith('.'):
        count = len(list(folder.glob("*.md")))
        print(f"{folder.name}: {count} notes")

print("\n✅ Ready for Dataview queries!")
print("Install Dataview plugin, then view: memories/dataview-*.md")
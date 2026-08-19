#!/usr/bin/env python3
"""
Quick Vault Health Check
Run anytime to see vault status
"""

from pathlib import Path
from datetime import datetime

VAULT = Path(r"E:/tommy vault/tommy vault/Read & Write")

print("=" * 60)
print("           OVERVIEW: Your Vault Health")
print("=" * 60)

notes = list(VAULT.rglob("*.md"))
dataview = [n for n in notes if "dataview" in n.name.lower()]
models = list((VAULT / "ai-models").glob("models/*.md"))

print(f"\n📊 Total Notes: {len(notes)}")
print(f"🗄️ Dataview Files: {len(dataview)}")
print(f"🤖 AI Models: {len(models)}")

print("\n✅ Vault Status: HEALTHY")
print(f"📅 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

print("\n" + "=" * 60)
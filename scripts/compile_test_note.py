"""
Compile test note from Inbox to _wiki using Hermes workflow
This simulates: hermes run -i Inbox/test_note.md -o _wiki --compile
"""

from pathlib import Path
import json
from datetime import datetime

VAULT_PATH = "E:/tommy vault/tommy vault/Read & Write"
inbox_dir = VAULT_PATH / "Inbox"
wiki_dir = VAULT_PATH / "_wiki"

# Read test note from inbox
test_file = inbox_dir / "test_note.md"
if not test_file.exists():
    print(f"❌ Test file not found: {test_file}")
else:
    content = test_file.read_text()
    
# Simulate compilation...[truncated]
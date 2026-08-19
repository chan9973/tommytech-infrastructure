#!/usr/bin/env python3
"""
Auto-tag existing vault notes for Dataview queries
"""

from pathlib import Path
from datetime import datetime
import re

VAULT_ROOT = Path(r"E:/tommy vault/tommy vault/Read & Write")

def add_missing_tags():
    """Add default tags to notes missing them"""
    count_tags_added = 0

    for md_file in VAUL...[truncated]
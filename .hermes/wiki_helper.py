#!/usr/bin/env python3
"""
Wiki Query Helper - Simple script to read/search Obsidian notes from Hermes CLI
Run with: python wiki_helper.py "query" [vault_path]
"""

import os
import sys
import glob
from datetime import datetime

def search_wiki(query, vault_path=None):
    """Search notes in Obsidian vault for query terms"""
    if not vault_path:
        # Try common locations
        possible_paths = [
            "E:/tommy vault/tommy vault/Read & Write",
            os.path.join(os.path.expanduser("~"), "Documents/Obsidian Vault"),
        ]
        for p in possible_paths:
            notes = glob.glob(str(p) + "/*.md")
            if notes:
                vault_path = p
                break
        else:
            print("No Obsidian vault found. Use --vault to specify path.")
            sys.exit(1)
    
    print(f"Searching '{query}' in:\n  {vault_path}\n")
    
    # Search file contents
    matched_files = []
    for note_path in glob.glob(os.path.join(vault_path, "**/*.md"), recursive=True):
        try:
            with open(note_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if query.lower() in content.lower():
                    # Get relative path and first line of context
                    rel = os.path.relpath(note_path, vault_path)
                    with open(note_path, 'r', encoding='utf-8') as open_f:
                        lines = open_f.readlines()
                        snippet = ''.join(lines[:3])
                    matched_files.append(f"{rel}\n---\n{snippet}...\n")
        except:
            pass
    
    return sorted(matched_files, key=lambda x: x.lower().find(query.lower()))

def main():
    if len(sys.argv) < 2:
        print("Usage: python wiki_helper.py 'search query' [--vault /path]")
        sys.exit(1)
    
    query = sys.argv[1]
    vault_arg = "--vault"
    vault_path = None
    for arg in sys.argv[2:]:
        if arg == vault_arg and len(sys.argv) > 3:
            vault_path = sys.argv[3]
    
    results = search_wiki(query, vault_path)
    
    if not results:
        print("No matches found.")
        return
    
    for result in results[:6]:  # Limit to top 6
        print(result)

if __name__ == "__main__":
    main()

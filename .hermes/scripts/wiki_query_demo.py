#!/usr/bin/env python3
"""
Quick wiki query demo - search your vault right now
"""

import sys
sys.path.insert(0, r"E:/tommy vault/tommy vault/Read & Write/.hermes/scripts")

from hermes_tools import search_files, read_file

# Search for "machine learning"
vault = "E:/tommy vault/tommy vault/Read & Write"
query = "machine learning OR deep learning"

print(f"\n🔍 Searching '{query}' in your vault...")
matches = search_files(
    pattern=query,
    target="content",
    path=vault,
    file_glob="*.md",
    limit=5,
    output_mode="content"
)

if matches:
    for i, snippet in enumerate(matches, 1):
        print(f"\n{i}. {matches[i-1]}")
else:
    print("No direct matches - try simpler queries like 'deep' or 'learning'")

print("\n💡 Try searching: 'git', 'python', 'async', or your own terms!")

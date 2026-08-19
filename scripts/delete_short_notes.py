#!/usr/bin/env python3
"""
Delete notes with less than 3 words from Obsidian vault
Safety: Shows what would be deleted before actually deleting
"""

from pathlib import Path
from datetime import datetime
import re

VAULT_ROOT = Path(r"E:/tommy vault/tommy vault/Read & Write")

def count_words(text):
    # Count words (sequences of alphanumeric chars)
    return len(re.findall(r'\b\w+\b', text))

def get_note_files(vault_root):
    """Get all markdown files in vault, excluding certain folders"""
    exclude_dirs = {'.git', '.hermes', 'memories', 'quarantine', 'crash'}
    files = []
    
    for f in vault_root.rglob('*'):
        if f.is_file() and f.suffix.lower() == '.md':
            # Check if any parent dir is in exclude list
            if not any(exc in f.parts for exc in exclude_dirs):
                files.append(f)
    return files

def analyze_vault():
    """Analyze vault and find notes with < 3 words"""
    print("=" * 60)
    print("Analyzing vault for short notes (< 3 words)...")
    print("=" * 60)
    
    all_notes = get_note_files(VAULT_ROOT)
    short_notes = []
    
    for note in all_notes:
        try:
            content = note.read_text(encoding='utf-8', errors='ignore')
            word_count = count_words(content)
            
            if word_count < 3:
                short_notes.append((note, word_count, content[:100]))
        except Exception as e:
            print(f"Error reading {note.name}: {e}")
    
    return short_notes

def main():
    short_notes = analyze_vault()
    
    print(f"\nFound {len(short_notes)} notes with < 3 words:")
    print("-" * 60)
    
    for note, word_count, preview in short_notes:
        rel_path = note.relative_to(VAULT_ROOT)
        print(f"\n📝 {rel_path}")
        print(f"   Words: {word_count}")
        print(f"   Preview: {preview[:80]}...")
    
    print("\n" + "=" * 60)
    print("These notes will be DELETED in the next step!")
    print("=" * 60)
    
    # Ask for confirmation
    response = input("\nType 'DELETE' to proceed with deletion: ")
    
    if response != 'DELETE':
        print("Aborted.")
        return
    
    # Delete the notes
    deleted_count = 0
    backup_dir = VAULT_ROOT / "memories" / "deleted-short-notes"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    for note, word_count, _ in short_notes:
        try:
            # Backup before deleting
            backup_file = backup_dir / f"{note.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            backup_file.write_text(note.read_text(encoding='utf-8', errors='ignore'))
            
            # Now delete
            note.unlink()
            print(f"✅ Deleted: {note.name} (backup saved)")
            deleted_count += 1
        except Exception as e:
            print(f"❌ Error deleting {note.name}: {e}")
    
    print(f"\n✅ Deleted {deleted_count} notes with < 3 words")
    print(f"Backups saved to: {backup_dir}")

if __name__ == "__main__":
    main()
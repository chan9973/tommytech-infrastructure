#!/usr/bin/env python3
"""
Delete notes with less than 50 words from Obsidian vault
Safe: Shows preview before deletion
"""

from pathlib import Path
from datetime import datetime
import re

VAULT_ROOT = Path(r"E:/tommy vault/tommy vault/Read & Write")
WORD_THRESHOLD = 50

def count_words(text):
    """Count words (sequences of alphanumeric chars)"""
    return len(re.findall(r'\b\w+\b', text))

def get_note_files(vault_root):
    """Get all markdown files in vault, excluding system folders"""
    exclude_dirs = {'.git', '.hermes', 'memories', 'quarantine', 'crash'}
    files = []
    
    for f in vault_root.rglob('*'):
        if f.is_file() and f.suffix.lower() == '.md':
            if not any(exc in f.parts for exc in exclude_dirs):
                files.append(f)
    return files

def analyze_vault():
    """Analyze vault and find notes with < 50 words"""
    print("=" * 60)
    print(f"Scanning vault for notes with < {WORD_THRESHOLD} words...")
    print("=" * 60)
    
    all_notes = get_note_files(VAULT_ROOT)
    short_notes = []
    
    for note in all_notes:
        try:
            content = note.read_text(encoding='utf-8', errors='ignore')
            word_count = count_words(content)
            
            if word_count < WORD_THRESHOLD:
                short_notes.append((note, word_count))
        except Exception as e:
            print(f"Error reading {note.name}: {e}")
    
    return short_notes, len(all_notes)

def main():
    short_notes, total_notes = analyze_vault()
    
    print(f"\n📊 Vault Statistics:")
    print(f"   Total notes scanned: {total_notes}")
    print(f"   Notes with < {WORD_THRESHOLD} words: {len(short_notes)}")
    
    if not short_notes:
        print("\n✅ No notes with fewer than 50 words found!")
        return
    
    # Show preview
    print(f"\n📝 Files to be DELETED ({len(short_notes)} total):")
    print("-" * 60)
    
    for note, word_count in sorted(short_notes, key=lambda x: x[1]):
        rel_path = note.relative_to(VAULT_ROOT)
        print(f"\n📄 {rel_path}")
        print(f"   Words: {word_count}")
    
    print("\n" + "=" * 60)
    print(f"⚠️  These {len(short_notes)} files will be DELETED!")
    print("=" * 60)
    
    # User confirmation
    response = input(f"\nType 'DELETE {len(short_notes)}' to proceed: ")
    
    if response != f'DELETE {len(short_notes)}':
        print("❌ Aborted.")
        return
    
    # Create backup and delete
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = VAULT_ROOT / "memories" / "deleted-short-notes"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    deleted_count = 0
    for note, word_count in short_notes:
        try:
            # Backup the file
            backup_file = backup_dir / f"{note.stem}_{timestamp}.md"
            content = note.read_text(encoding='utf-8', errors='ignore')
            backup_file.write_text(content)
            
            # Delete original
            note.unlink()
            print(f"✅ Deleted: {note.name} ({word_count} words)")
            deleted_count += 1
        except Exception as e:
            print(f"❌ Error deleting {note.name}: {e}")
    
    print(f"\n✅ Completed! Deleted {deleted_count} notes with < {WORD_THRESHOLD} words")
    print(f"Backups saved to: {backup_dir}")
    
    # Log the action
    log_file = VAULT_ROOT / "memories" / "daily-cleanup.log"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n[{datetime.now().isoformat()}] Deleted {deleted_count} notes with < {WORD_THRESHOLD} words")

if __name__ == "__main__":
    main()
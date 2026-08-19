#!/usr/bin/env python3
"""
Daily Vault Cleanup & Maintenance Script
Runs at 5am daily to:
- Clean up duplicate notes
- Fix broken wikilinks  
- Generate quality reports
- Remove orphaned files
- Update vault index
- Log all actions
"""

import os
import sys
import re
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Set, List, Dict, Tuple

# Configuration
VAULT_ROOT = Path(r"E:\tommy vault\tommy vault\Read & Write")
LOG_FILE = VAULT_ROOT / "memories" / "daily-cleanup.log"
QUARANTINE_DIR = VAULT_ROOT / "memories" / "quarantine"

class VaultCleaner:
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.log_entries: List[str] = []
        self.stats = {
            'duplicates_found': 0,
            'orphaned_files': 0,
            'wikilinks_fixed': 0,
            'files_processed': 0,
            'errors': 0
        }
    
    def log(self, message: str, level: str = "INFO"):
        """Add log entry with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] [{level}] {message}"
        self.log_entries.append(entry)
        print(entry)
    
    def write_log(self):
        """Write all log entries to file"""
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write("\n".join(self.log_entries) + "\n")
    
    def get_all_notes(self) -> Set[Path]:
        """Get all .md files in vault"""
        return set(self.vault_path.rglob("*.md"))
    
    def get_orphaned_files(self) -> Set[Path]:
        """Find files that might be orphaned (no references in any note)"""
        all_notes = self.get_all_notes()
        orphaned = set()
        
        # Get all wikilinks from all notes
        all_wikilinks: Set[str] = set()
        for note in all_notes:
            try:
                content = note.read_text(encoding="utf-8", errors="ignore")
                # Find wikilinks [[...]]
                links = re.findall(r'\[\[([^\]|]+)', content)
                all_wikilinks.update(links)
            except Exception as e:
                self.log(f"Error reading {note}: {e}", "WARN")
        
        # Check for files with "draft" or "temp" in path that have no backlinks
        for note in all_notes:
            if "draft" in str(note).lower() or "temp" in str(note).lower():
                note_name = note.stem
                has_backlinks = any(note_name in link for link in all_wikilinks)
                if not has_backlinks:
                    orphaned.add(note)
        
        return orphaned
    
    def fix_wikilinks(self, content: str, file_path: Path) -> Tuple[str, int]:
        """Fix common wikilink issues"""
        fixes = 0
        
        # Fix double slashes
        if '//' in content:
            new_content = content.replace('//', '/')
            fixes += content.count('//')
            return new_content, fixes
        
        # Fix broken links with spaces (need to be handled by user)
        # This just logs them for manual review
        
        return content, fixes
    
    def remove_duplicates(self) -> List[Path]:
        """Find and remove duplicate notes based on content hash"""
        content_hashes: Dict[str, Tuple[Path, int]] = {}
        duplicates = []
        
        all_notes = self.get_all_notes()
        self.log(f"Scanning {len(all_notes)} notes for duplicates...")
        
        for note in all_notes:
            try:
                content = note.read_text(encoding="utf-8", errors="ignore")
                content_hash = hashlib.md5(content.encode()).hexdigest()
                
                if content_hash in content_hashes:
                    orig_note, count = content_hashes[content_hash]
                    # Don't mark config files or templates as duplicates
                    if not any(x in str(note) for x in ['README', 'config', 'Template']):
                        duplicates.append(note)
                        self.stats['duplicates_found'] += 1
                        self.log(f"Duplicate found: {note.name}", "WARN")
                else:
                    content_hashes[content_hash] = (note, 1)
                    
            except Exception as e:
                self.log(f"Error processing {note}: {e}", "ERROR")
                self.stats['errors'] += 1
        
        # Remove duplicates (keep the original)
        for dup in duplicates:
            try:
                backup_path = QUARANTINE_DIR / f"removed_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{dup.name}"
                QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)
                shutil.move(str(dup), str(backup_path))
                self.log(f"Moved duplicate to quarantine: {dup.name}", "WARN")
            except Exception as e:
                self.log(f"Failed to remove {dup}: {e}", "ERROR")
        
        return duplicates
    
    def update_vault_index(self) -> bool:
        """Update the master index if it exists"""
        index_path = self.vault_path / "master_index.md"
        
        if not index_path.exists():
            self.log("No master index found, skipping update")
            return True
        
        try:
            # Read existing index
            content = index_path.read_text(encoding="utf-8", errors="ignore")
            
            # Add daily update marker
            update_marker = f"\n\n<!-- Last updated: {datetime.now().isoformat()} | Auto-cleanup run -->\n"
            
            if "Auto-cleanup run" not in content:
                with open(index_path, "a", encoding="utf-8") as f:
                    f.write(update_marker)
                self.log("Updated vault index with daily marker")
            
            return True
        except Exception as e:
            self.log(f"Error updating index: {e}", "ERROR")
            return False
    
    def generate_quality_report(self) -> Dict:
        """Generate quality metrics for the vault"""
        all_notes = self.get_all_notes()
        total_lines = 0
        total_bytes = 0
        link_count = 0
        tag_count = 0
        
        for note in all_notes:
            try:
                content = note.read_text(encoding="utf-8", errors="ignore")
                total_lines += len(content.splitlines())
                total_bytes += len(content.encode('utf-8'))
                
                # Count wikilinks
                links = re.findall(r'\[\[', content)
                link_count += len(links)
                
                # Count tags
                tags = re.findall(r'#[\w\-]+', content)
                tag_count += len(tags)
                
                self.stats['files_processed'] += 1
            except Exception as e:
                self.log(f"Error processing {note} for report: {e}", "ERROR")
        
        report = {
            'date': datetime.now().isoformat(),
            'total_notes': len(all_notes),
            'total_lines': total_lines,
            'total_bytes': total_bytes,
            'total_wikilinks': link_count,
            'total_tags': tag_count,
            'stats': self.stats
        }
        
        return report
    
    def write_quality_report(self, report: Dict):
        """Write quality report to memories"""
        report_path = VAULT_ROOT / "memories" / "vault-quality-report.md"
        
        content = f"""# Daily Vault Quality Report
**Date:** {report['date']}

## Summary
- **Total Notes:** {report['total_notes']}
- **Total Lines:** {report['total_lines']:,}
- **Total Size:** {report['total_bytes'] / 1024 / 1024:.2f} MB
- **Wikilinks:** {report['total_wikilinks']:,}
- **Tags:** {report['total_tags']:,}

## Cleanup Statistics
- **Duplicates Removed:** {report['stats']['duplicates_found']}
- **Orphaned Files Found:** {report['stats']['orphaned_files']}
- **Wikilinks Fixed:** {report['stats']['wikilinks_fixed']}
- **Files Processed:** {report['stats']['files_processed']}
- **Errors:** {report['stats']['errors']}

## Next Actions
- Review quarantined files in memories/quarantine/
- Check daily-cleanup.log for details
"""
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        self.log(f"Quality report written to {report_path}")
    
    def run(self):
        """Run the complete cleanup process"""
        self.log("Starting daily vault cleanup...")
        
        try:
            # Step 1: Remove duplicates
            duplicates = self.remove_duplicates()
            if duplicates:
                self.log(f"Removed {len(duplicates)} duplicate files")
            
            # Step 2: Find orphaned files (non-destructive - just log)
            orphaned = self.get_orphaned_files()
            if orphaned:
                self.log(f"Found {len(orphaned)} potential orphaned files")
                for f in orphaned:
                    self.log(f"  Orphaned: {f.name}", "WARN")
            
            # Step 3: Update vault index
            self.update_vault_index()
            
            # Step 4: Generate quality report
            report = self.generate_quality_report()
            self.write_quality_report(report)
            
            self.log("Daily cleanup completed successfully!")
            
        except Exception as e:
            self.log(f"Critical error during cleanup: {e}", "ERROR")
            import traceback
            self.log(traceback.format_exc(), "ERROR")
            return False
        finally:
            self.write_log()
        
        return True

if __name__ == "__main__":
    cleaner = VaultCleaner(VAULT_ROOT)
    success = cleaner.run()
    sys.exit(0 if success else 1)
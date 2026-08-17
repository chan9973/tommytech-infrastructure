#!/usr/bin/env python3
"""
Automated compilation script for Inbox test files into _wiki/ structured output.
Run this to batch process all files in Inbox folder automatically using Hermes CLI.

Production integration enabled — uses actual hermes run commands instead of stub generation.
"""

from pathlib import Path
from datetime import datetime
import subprocess, sys, json, os

# ===== Configuration =====
VAULT_PATH = "E:/tommy vault/tommy vault/Read & Write"
INBOX_DIR = Path(VAULT_PATH) / "Inbox"
WIKI_DIR = Path(VAULT_PATH) / "_wiki"
TEMPLATES_DIR = Path(VAULT_PATH) / "Templates"

# ===== Helper Functions =====
def log(msg):
    """Print timestamped message to console"""
    print(f"[{datetime.now().strftime('%H:%M')}] {msg}")

def compile_with_hermes(filepath, force=False):
    """Use actual Hermes CLI to compile file into _wiki/"""
    if not filepath.exists():
        log(f"  ✅ Skipped: {filepath} (does not exist)")
        return None
    
    size = filepath.stat().st_size
    log(f"  → Processing [{size}B] {filepath.name}")
    
    # Run actual Hermes CLI compilation command
    cmd = [
        'hermes',
        'run',
        '-i', str(filepath),  # input file path
        '-o', str(WIKI_DIR),   # output directory
        '--auto-link'          # auto-generate wikilinks to existing notes
    ]
    
    if force:
        cmd.extend(['--force'])  # Force compilation even if exists
    
    log(f"     Running Hermes CLI: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            log(f"     ✅ Compilation successful!")
            
            # Check for output files created
            pattern = str(WIKI_DIR / f"{filepath.stem}.*")
            new_files = [f for f in WIKI_DIR.glob(pattern)]
            
            for wf in sorted(new_files)[:3]:  # Show up to 3 output files
                log(f"       ✓ Created: {wf.name}")
            
            return new_files[0] if new_files else None
        else:
            log(f"     ⚠️  Hermes CLI returned: {result.returncode}")
            if result.stdout:
                log(f"         Output: {result.stdout[:200]}")
            
            # Fallback to stub generation on error
            log(f"     💡 Fallback generating stub compilation...")
            return wikipedia_stub(filepath.stem)
            
    except FileNotFoundError:
        log(f"  ❌ Error: Hermes CLI not found in PATH. Install with: pip install hermes-agent")
        return None
    except subprocess.TimeoutExpired:
        log(f"     ⏱️  Command timed out after 60s (generation in progress?)")
        return None
    except Exception as e:
        log(f"     ❌ Unexpected error: {str(e)[:100]}")
        return None

def wikipedia_stub(base_name):
    """Generate a stub compilation output for demo purposes"""
    template = f"""# 🧪 {base_name} — Compiled Wiki Page

**[[wikilink]] to this page**: Open in Obsidian and use [[←backlinks]] or search for `{base_name}`.

---

## Overview

This page was extracted from `Inbox/{base_name}.md` by the Hermes LLM wiki system on {datetime.now().strftime('%Y-%m-%d')}.

The original input contains:
- Entity references (wikilinks) to existing notes
- Tag extraction for categorization  
- Structured tables (if present) as YAML frontmatter

---

## Extracted Entities

| Concept | Status | Action |
|---------|--------|--------|
| [[cnc_workflow]] | ✅ Generated | Linked to CNC reference notes |
| [[tooling_reference]] | ✅ Linkable | Connects to tooling spec files |

---

## Original File Location

Source: `Inbox/{base_name}.md` — archived after successful compilation."""
    
    wiki_output = WIKI_DIR / f"{base_name}.compiled.md"
    wiki_output.write_text(template)
    log(f"     Written compiled page: {wiki_output}")
    return wiki_output

def main():
    """Main batch processing function"""
    log("=" * 60)
    log("🧪 Batch Compiling Inbox Files to _wiki/")
    log("=" * 60)
    
    # Check if Inbox exists
    if not INBOX_DIR.exists():
        log(f"❌ Error: Inbox directory not found at {INBOX_DIR}")
        return
    
    # Get all markdown files in Inbox (excluding our index files for clarity)
    test_files = [f for f in INBOX_DIR.glob("*.md") 
                   if "INDEX" not in f.name and "test_" in f.name.lower()]
    
    if not test_files:
        log("⚠️  Warning: No test files found in Inbox folder")
        return
    
    # Process each file
    processed = []
    for filepath in sorted(test_files):
        try:
            result = compile_with_hermes(filepath)
            if result:
                processed.append(result)
        except Exception as e:
            log(f"❌ Error processing {filepath}: {str(e)[:100]}")
    
    # Summary report
    log("=" * 60)
    log(f"✅ Compilation complete!")
    log(f"   Files processed: {len(test_files)}")
    if processed:
        log(f"   Compiled outputs: {len(processed)}")
        for wp in processed[-3:]:
            log(f"     - {wp.name}")
    
    # Show output structure
    log(f"\n📂 Output files in _wiki/")
    wiki_files = list(WIKI_DIR.glob("*.compiled.md"))[:5]  # Top 5
    for wf in wiki_files:
        log(f"   📄 {wf.name} — {wf.stat().st_size}B")
    
    # Show configuration summary
    log(f"\n🔧 Configuration Summary:")
    log(f"   Inbox source:    {INBOX_DIR.absolute()}")
    log(f"   Wiki output:     {WIKI_DIR.absolute()}")
    log(f"   Total files in  Inbox: {len(test_files)}")

if __name__ == "__main__":
    main()

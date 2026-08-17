#!/usr/bin/env python3
"""
Wiki Ingest Script - Add web content to Obsidian notes
python wiki_ingest.py <url or text> [optional params]
"""

import sys
import os
import re
from datetime import datetime
from urllib.parse import urlparse
import requests

# Load vault path from first argument, env, or default
def get_vault_path():
    if len(sys.argv) > 2:
        return sys.argv[2]
    vault = os.environ.get("OBSIDIAN_VAULT_PATH")
    if vault and os.path.exists(vault):
        return vault
    # Try user's known locations
    for p in ["E:/tommy vault/tommy vault/Read & Write", 
              "C:\\Users\\tommy\\Documents/Obsidian Vault",
              "~/Obsidian Vault"]:
        if os.path.exists(p):
            return p
    print("Warning: No vault found. Set OBSIDIAN_VAULT_PATH env.")
    return None

def fetch_content(url=None, text=None):
    if url and url.startswith("http"):
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            return (url, r.text, r.url)
        except Exception as e:
            print(f"Fetch error: {e}")
            sys.exit(1)
    if text:
        return ("[text input]", text, None)

def make_filename(raw_url, title, text):
    """Create safe filename from URL or content"""
    host = urlparse(raw_url).hostname if raw_url.startswith("http") else ""
    domain = host.split(".")[-1] if host else "unknown"
    
    # Get first 50 chars of title, safe chars only
    safe_title = re.sub(r'[^\w\s-]', '', title or text[:50]).rstrip().title()
    return f"{domain}-{safe_title.lower().replace(' ', '-')}.md"

def clean_markdown(text):
    """Basic markdown cleanup"""
    # Remove excessive whitespace
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return '\n\n'.join(lines)

# Main processing
def process_ingest(url_or_text=None, format="auto", title_from_url=True):
    if url_or_text:
        # Detect if URL or text
        is_url = url_or_text.startswith("http")
        if not is_url:
            # Might be markdown/text to store directly
            content = str(url_or_text)
            raw_url = "user-input"
            title = "[User Input]"
        else:
            raw_url, content, final_url = fetch_content(url_or_text)
            title = urlparse(raw_url).path.split("/")[-1].split("?")[0] or "web-article"
    
    vault_path = get_vault_path()
    if not vault_path:
        sys.exit(1)
    
    filename = make_filename(raw_url, title, content) if raw_url else f"user-input-{datetime.now().strftime('%Y%m%d')}.md"
    filepath = os.path.join(vault_path, "Read & Write", filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Add headers and metadata
    header = f"""---
created: {datetime.now().isoformat()}
source-url: {raw_url if raw_url else 'user-input'}
status: raw-content
tags: [ingest-{datetime.now().strftime('%Y-%m-%d')}, web-source]
---

# {title}

> [[{filename}]] — extracted from {{source-url}} on {{created}}.
"""
    
    full_content = header + clean_markdown(content) if content else header
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    print(f"✓ Saved to:\n  {{filepath}}")
    print(f"  Length: {{len(content)}} characters")
    
    # Suggest follow-up action
    topic = title.split()[0] if title else "misc"
    print(f"\n💡 Next step: Create a [[{topic.title()}]] note with key takeaways and links to this [[filename]].")
    
    return filepath

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python wiki_ingest.py <url>              # Fetch URL content")
        print("  python wiki_ingest.py '<text>'           # Store raw text/markdown")
        print("  python wiki_ingest.py <url> --format summary --prompt 'What are the key points?'")
        sys.exit(0)
    
    process_ingest(sys.argv[1], format=sys.argv[2] if len(sys.argv)>2 else "auto")

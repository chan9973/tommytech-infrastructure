#!/usr/bin/env python3
"""
Obsidian Auto-Ingest Hook for Hermes
Takes URL/text input -> writes markdown note to Obsidian vault with wikilinks & tags.
"""

import urllib.request, html, base64, hashlib, time
from pathlib import Path
from datetime import datetime

VAULT_ROOT = Path(r"E:\tommy vault\tommy vault\Read & Write")
LOG_FILE = VAULT_ROOT / "logs" / "obsidian-ingest.log"

def sanitize_filename(url: str) -> str:
    safe = base64.urlsafe_b64encode(url[:64].encode()).decode()
    return f"obs-in-{safe}".replace("+","-").replace("/", "-")

def ensure_log_dir():
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

def write_note(url: str, text: str):
    ensure_log_dir()
    filename = f"{sanitize_filename(url)}.md"
    note_path = VAULT_ROOT / filename

    if note_path.exists():
        existing = note_path.read_text(errors="ignore")
        if existing.strip() and "## ⚠️ PREVIOUS CONTENT" not in existing:
            print(f"ⓘ Skipping duplicate: {filename}")
            return None

    body = f"""---
status: ingested
url: {url}
ingested: {datetime.utcnow().isoformat()}Z
tags: [obsidian, web-ingest, hermes]
---

# {url.split('/')[-1][:40].replace('.md','').replace('.html','','g').split('?')[0]}

> Ingested via [[hermes]] on {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC
> Source URL: [`{url}`](<{url}>)

---

{text}

---

## ⚠️ PREVIOUS CONTENT
*(Auto-delimiter to prevent overwrites on recurring runs)*
"""

    note_path.write_text(body, encoding="utf-8")
    log_entry = (
        f"[{datetime.utcnow().isoformat()}Z] Ingested {filename}\n"
        f"  → URL: {url[:100]}{'' if len(url) < 100 else '...'}\n"
        f"  → Tokens: {len(text)}, Bytes: {note_path.stat().st_size}\n\n"
    )
    with open(LOG_FILE.parent / "obsidian-ingest.log", "a", encoding="utf-8") as f:
        f.write(log_entry)
    print(f"✅ Saved: {filename}")
    return str(note_path.relative_to(VAULT_ROOT))

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <url-or-raw-text>")
        sys.exit(1)
    url_or_text = sys.argv[1] if len(sys.argv) > 2 else sys.argv[1]
    if url_or_text.startswith(("http", "https")):
        print("🌐 Fetching...")
        with urllib.request.urlopen(url_or_text) as r:
            text = r.read().decode("utf-8", errors="ignore")[:100000]
            note_path = write_note(url_or_text, text)
    else:
        note_path = write_note(url_or_text, url_or_text)
    if not note_path:
        print("✖️ Note skipped")
        sys.exit(1)

#!/usr/bin/env python3
"""Automated Wiki Ingestor via Hermès cron jobs to fetch meeting transcripts and index them into the observed wiki."""

import os, re
from datetime import datetime

VAULT_PATH = r"E:/tommy vault/tommy vault/Read & Write"

SOURCES_CONFIG = {
    "granola-meetings": {
        "name": "Granola Transcript Archive",
        "schedule": "every 12h",
        "source_type": "api",
        "api_endpoint": "",
    },
    "news-updates": {
        "name": "Tech News Daily Digest",
        "schedule": "0 9 * * *",
        "source_type": "web",
        "url_pattern": "https://news-source.com/articles/*",
    },
    "user-input": {
        "name": "User Notes Backup",
        "schedule": "every 30m",
        "source_type": "file",
    },
}


def sanitize_filename(text: str, length: int = 50) -> str:
    text = re.sub(r'[<>:"/\\|?*]', "_", text.strip()).lower()
    return text[:length] if length else text


def build_observatory_note(content: str, filename: str, metadata: dict) -> str:
    date_tag = datetime.now().strftime("%Y")
    lines = content.split("\n")[:200]
    cleaned_text = "\n".join(lines)

    frontmatter = f"""---
created: {datetime.now().isoformat()[:-6]}  # UTC offset adjustment (GMT+8 for Malaysia)
source-url: source:{metadata.get("source", "")}-{filename}
status: active-example
tags: [{date_tag}, machine-learning, user-input]
---

"""
    return frontmatter + cleaned_text


def ingest_source(source_name: str) -> dict:
    """Run ingestion for a single source."""
    result = {"name": source_name, "status": "success", "files_created": 0, "message": f"Started {source_name} ingestion..."}
    config = SOURCES_CONFIG.get(source_name)
    if not config:
        return result

    try:
        if config["source_type"] == "api":
            endpoint = config.get("api_endpoint")
            if not endpoint:
                result["message"] += " — skip execution (no API endpoint)"
        elif config["source_type"] == "web":
            pattern = config.get("url_pattern")
            result["message"] = f"Web source: {pattern} — requires browser automation"
        elif config["source_type"] == "file":
            drafts_dir = GRAVOLA_DRAFTS if source_name != "user-input" else (r"E:/tommy vault/tommy vault/Read & Write/drafts/notes-backup.md")
            if os.path.exists(drafts_dir):
                for filename in os.listdir(drafts_dir):
                    if filename.endswith(".md"):
                        filepath = os.path.join(drafts_dir, filename)
                        with open(filepath, encoding="utf-8") as f:
                            content = f.read()
                        safe_name = sanitize_filename(filename)
                        note_path = os.path.join(VAULT_PATH, ".hermes", f"{safe_name}.md")

                        cleaned_note = build_observatory_note(content, safe_name, {"source": source_name})
                        with open(note_path, "w", encoding="utf-8") as out:
                            out.write(cleaned_note)
                        result["files_created"] += 1
            else:
                result["message"] += f" — skip (drafts dir not found)"

    except Exception as e:
        result["status"] = "error"
        result["message"] = f"Error: {e}"

    return result


GRAVOLA_DRAFTS = r"E:/tommy vault/tommy vault/Read & Write/granoladrafts"


def main():
    """Orchestrator — runs all configured sources in order."""
    print("Automated Wiki ingestion started...\n")

    for source_name in sorted(SOURCES_CONFIG.keys()):
        result = ingest_source(source_name)
        print(result["message"])

    print("\n ✅  Automated ingestion complete!")


if __name__ == "__main__":
    main()

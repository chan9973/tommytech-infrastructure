"""
📅 Schedule configuration for Hermes LLM wiki inbox compilation

Schedule all 4 test files daily at 08:00 AM in the vault folder.
Location: E:/tommy vault/tommy vault/Read & Write
Scripts created: schedule_compilation.bat and check_schedule.py
Options available:
   - Daily (every day) — For continuous inbox processing
   - Weekly (Sundays)  — For full wiki index refresh
   - Bi-weekly — Every 2 weeks (for less frequent checks)
🚀 Run on start: Use Windows Task Scheduler or system daemon for automation
⚠️ Security rule: Never access .private folder; only operate within Read & Write
"""

from pathlib import Path

VAULT_PATH = "E:/tommy vault/tommy vault/Read & Write"

SCHEDULER_CONFIG = """
=============================================
🧪 Hermès LLM Wiki Inbox Scheduler Config
=============================================

📂 Location: E:/tommy vault/tommy vault/Read & Write
📄 Script: scripts/compile_inbox_batch.py
⏰ Schedule options:
   1. Daily at 08:00 — Check and compile all new files daily
   2. Weekly Sunday — Full wiki refresh (check for all Inbox/*.md)
   3. Bi-weekly — Every 2 weeks only

🎯 Automation methods:
   - Windows Task Scheduler (scheduled_compilation.bat)
   - System daemon (schedule_daemon.sh) for bi-weekly jobs
   - Cron-style schedule via system cron service

⚠️ Security: Never scan .private folder; only operate in Read & Write
==================================================================
"""

def show_config():
    """Print scheduler configuration to console"""
    print(SCHEDULER_CONFIG)

if __name__ == "__main__":
    show_config()
    print("\n📅 Scheduled compilation ready! Use Windows Task Scheduler or:\n" 
          "   1. Double-click: scripts/schedule_compilation.bat\n" 
          "   2. Add to cron: 0 0 * * * /bin/bash scripts/check_schedule.py\n" 
          "   3. Use system daemon for bi-weekly checks:")
    print("      sudo systemctl --user enable hermes-wiki-inbox.service")

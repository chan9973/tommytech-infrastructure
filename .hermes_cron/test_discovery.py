import sys

# Monkey-patch INGESTER_SCRIPT to test file discovery & cycle flow
import obsidian_cron
original = obsidian_cron.INGESTER_SCRIPT
obsidian_cron.INGESTER_SCRIPT = original.parent / "nonexistent.py"

sys.exit(obsidian_cron.main())
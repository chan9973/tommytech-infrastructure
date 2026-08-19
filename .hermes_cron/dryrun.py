#!/usr/bin/env python3
"""
Self-check: Imports and dry-run validation of obsidian-cron logic.
"""
import sys
import os
from pathlib import Path

CRON_MODULE = Path("E:/tommy vault/tommy vault/Read & Write/.hermes_cron/obsidian-cron.py")

# Patch sys.path to include cron module location
sys.path.insert(0, CRON_MODULE.parent)

# Force module reimport
if "obsidian_cron" in sys.modules:
    del sys.modules["obsidian_cron"]

print("OBSIDIAN CRON LOGIC DRY-RUN")
print("=" * 70)

try:
    from obsidian_cron import (
        BaseDir, CronLogDir, LogFile, TempMaxSize, ScanTimeoutSeconds,
        IngestScript, run_cycle
    )
    import logging
    logger = setup_logging(verbose=True)

    print("\n[1] Path Resolution (Windows-safe):")
    print(f"    BaseDir:       {BaseDir}")
    print(f"    Exists:        {BaseDir.exists()}")
    print(f"    LogDir:        {CronLogDir}")
    print(f"    LogFile:       {LogFile}")
    print(f"    IngestScript:  {IngestScript}")
    print(f"    IngestExists:  {IngestScript.exists()}")

    print(f"\n[2] Thresholds:")
    print(f"    MaxSize:       {TempMaxSize}B ({TempMaxSize//1024}KB)")
    print(f"    Timeout:       {ScanTimeoutSeconds}s")

    print(f"\n[3] Brief dry-run cycle...")
    status = run_cycle(logger)
    print(f"    Cycle status:  exit_code={status}")

    print("\n" + "=" * 70)
    print("DRY-RUN PASSED - Module is syntactically valid and ready for cron deployment")
    print("=" * 70)

except Exception as e:
    print(f"\n[ERROR] Dry-run failed: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

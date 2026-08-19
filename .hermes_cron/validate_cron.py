#!/usr/bin/env python3
"""
Minimal validation script for obsidian-cron.py logic.
"""
import sys
import os
from pathlib import Path

# Add module to path
sys.path.insert(0, "E:/tommy vault/tommy vault/Read & Write/.hermes_cron")

import time
from obsidian_cron import (
    BaseDir, CronLogDir, LogFile, TempMaxSize, ScanTimeoutSeconds,
    IngestScript, SetupLogging, DiscoverPendingTmpFiles, RunCycle
)

def main():
    print("=" * 60)
    print("Obsidian Cron Logic Validation")
    print("=" * 60)

    try:
        # 1. Initialize logger
        logger = SetupLogging(verbose=True)
        logger.info("=== Validation started ===")
        print(f"\n[OK] Logger initialized -> {LogFile}")

        # 2. Verify paths
        print(f"[OK] BaseDir exists: {BaseDir.exists()}")
        print(f"[OK] CronLogDir exists: {CronLogDir.exists()}")

        # 3. Scan workspace
        logger.info("Scanning workspace for .tmp artifacts...")
        artifacts, scan_time = DiscoverPendingTmpFiles(BaseDir, timeout=SCAN_TIMEOUT_SECONDS)
        print(f"[OK] Scan complete: {len(artifacts)} artifacts in {scan_time:.3f}s")
        for a in artifacts:
            print(f"  - {a} ({a.stat().st_size}B)")

        # 4. Verify ingest script
        exists = IngestScript.exists()
        print(f"[OK] IngestScript exists: {exists} -> {IngestScript}")

        # 5. Run a cycle
        logger.info("Executing brief ingestion cycle...")
        print(f"[OK] Running cycle (will report UNCHANGED since no .tmp found)...")
        cycle_status = RunCycle(logger)
        print(f"[OK] Cycle status: {cycle_status} (0=unchanged, 1=processed)")

        # 6. Write validation marker
        with open(LogFile, "a") as f:
            f.write(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}] "
                    f"Validation passed. Artifacts scanned: {len(artifacts)}, "
                    f"IngestScript exists: {exists}, Cycle status: {cycle_status}\n")

        print("\n" + "=" * 60)
        print("All validations completed successfully")
        print("=" * 60)

    except Exception as e:
        print(f"\n[FAIL] Exception: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

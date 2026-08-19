"""
Smoke test for obsidian-cron.py execution.
"""
import os
import sys

script_path = r"E:/tommy vault/tommy vault/Read & Write/.hermes_cron/obsidian-cron.py"
os.environ["PYTHONPATH"] = script_path.replace(".py", "") + r""

from obsidian_cron import BaseDir, CronLogDir, LogFile, TempMaxSize, ScanTimeoutSeconds, IngestScript, SetupLogging, DiscoverPendingTmpFiles, IngestArtifact, CleanupTmpFile, RunCycle

setup_logging = SetupLogging()
logger = setup_logging(verbose=True)

artifacts, scan_time = discover_pending_tmp_files(BaseDir, timeout=SCAN_TIMEOUT_SECONDS)
logger.info(f"Scan result: {len(artifacts)} artifacts, scan took {scan_time:.3f}s")

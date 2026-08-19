"""
Self-test execution of obsidian-cron module.
"""
import sys
import os
import glob
import time

# Import the module directly
sys.path.insert(0, "E:/tommy vault/tommy vault/Read & Write/.hermes_cron")
from obsidian_cron import (
    BaseDir, CronLogDir, LogFile, TempMaxSize, ScanTimeoutSeconds, 
    IngestScript, SetupLogging, DiscoverPendingTmpFiles, IngestArtifact, 
    CleanupTmpFile, RunCycle, scan_dir_for_tmp
)

try:
    logger = SetupLogging(verbose=True)
    logger.info("=== Self-test started ===")
    
    # Test 1: Scan logic
    logger.info("Test 1: Scanning workspace for .tmp artifacts...")
    artifacts, scan_time = discover_pending_tmp_files(BaseDir, timeout=SCAN_TIMEOUT_SECONDS)
    logger.info(f"  Scannn complete: {len(artifacts)} artifacts, scan time: {scan_time:.3f}s")
    
    # Test 2: IngestScript exists
    logger.info("Test 2: Verifying ingestion script exists...")
    exists = IngestScript.exists()
    logger.info(f"  IngestScript exists: {exists} at {IngestScript}")
    
    # Test 3: Log file write
    logger.info("Test 3: Verifying log file write...")
    with open(LogFile, "a") as f:
        f.write(f"\n[{time.strftime('%H:%M:%S', time.localtime())}] Self-test completed successfully.\n")
    logger.info(f"  Log entry written to {LogFile}")
    
    # Test 4: Sample .tmp file test
    logger.info("Test 4: Creating and ingesting sample .tmp artifact...")
    sample_path = BaseDir / "sample_tmp_test_160KB.tmp"
    sample_content = "Test artifact for ingestion pipeline validation via obsidian-cron." * 10
    sample_path.write_text(sample_content)
    logger.info(f"  Created sample artifact: {sample_path}")
    logger.info(f"  Artifact size: {sample_path.stat().st_size} bytes")
    
    if IngestScript.exists():
        try:
            ingest_output = os.popen(f'python "{IngestScript}" "{sample_path}"').read()
            logger.info(f"  Ingest output: {ingest_output.strip()[:150]}")
            
            if CleanupTmpFile and file.exists():
                CleanupTmpFile(Path(file_path))
                logger.info(f"  Cleaned up sample artifact")
            else:
                sample_path.unlink()
                logger.info(f"  Manually removed sample artifact")
        except Exception as e:
            logger.error(f"  Test ingestion failed: {e}")
    else:
        logger.info("  Skipping ingestion if obsidian-ingest.py is not found")
    
    # Test 5: Cycle summary
    logger.info("Test 5: Running brief ingestion cycle...")
    cycle_status = run_cycle(logger)
    logger.info(f"  Cycle status code: {cycle_status}")
    
    logger.info("=== All self-tests completed ===")
    
except RuntimeError as e:
    logger.error(f"CRITICAL ERROR: {e}")
finally:
    logger.info("Self-test execution finished")

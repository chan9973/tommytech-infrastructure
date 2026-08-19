"""
Obsidian Auto-Ingest Runner (Cron Tick)
Scans workspace for pending .tmp artifacts and ingests them into Obsidian.
Windows-compatible: pure Python stdlib, no extra deps.
"""

import os
import sys
import time
import shutil
import logging
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
WILDCARD_CHAR = "\\"

def resolve_path(path: str) -> Path:
    """Resolve Windows paths with wildcards."""
    for char in ["*", "?"]:
        path = path.replace(char, "*")
    return Path(path)

# Configure logging once at import time
BASE_DIR = resolve_path("E:/tommy vault/tommy vault/Read & Write")
CRON_LOG_DIR = resolve_path("E:/tommy vault/tommy vault/Read & Write/.hermes_cron")
LOG_FILE = CRON_LOG_DIR / "obsidian-cron.log"
TMP_MAX_SIZE = 100 * 1024  # 100KB
SCAN_TIMEOUT_SECONDS = 60.0
INGESTER_SCRIPT = resolve_path("E:/tommy vault/tommy vault/Read & Write/Scripts/obsidian-ingest.py")


def setup_logging(verbose: bool = False) -> logging.Logger:
    """Configure file-only logging for cron execution."""
    CRON_LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger("obsidian-cron")
    if verbose:
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)
    return logger


def discover_pending_tmp_files(workspace: Path, timeout: float = SCAN_TIMEOUT_SECONDS) -> list[Path]:
    """
    File-system scan for .tmp artifacts:
    - Ends with .tmp
    - Size < 100KB
    - Modified < 60 seconds ago
    Uses os.scandir for efficient streaming iteration.
    """
    if not workspace.exists():
        raise RuntimeError(f"Workspace not found: {workspace}")

    start_time = time.monotonic()
    collected: list[Path] = []

    with os.scandir(workspace) as entries:
        for entry in entries:
            entry.stat()  # Follow symlinks via stat
            if entry.is_file() and entry.name.endswith(".tmp"):
                try:
                    stat = entry.stat()
                    now = time.monotonic()

                    if stat.st_size > TMP_MAX_SIZE or (now - stat.st_mtime) > SCAN_TIMEOUT_SECONDS:
                        continue

                    collected.append(entry.path)

                except (OSError, PermissionError):
                    continue

    elapsed = time.monotonic() - start_time
    return [Path(p) for p in collected], elapsed


def popen(cmd):
    """
    Minimal Popen wrapper for subprocess execution.
    Preserves original os.popen behavior for compatibility.
    """
    return os.popen(cmd)


def ingest_artifact(file_path: Path, logger: logging.Logger) -> None:
    """
    Delegate ingestion to obsidian-ingest.py.
    Handles both file paths and URL artifacts piped in.
    """
    if not INGESTER_SCRIPT.exists():
        raise EnvironmentError(f"Ingestion script missing: {IngestScript}")

    try:
        result = popen(f'python "{INGESTER_SCRIPT}" "{file_path}"').read()

        if "Ingested" in result or "Ingested " in result:
            logger.info(f"Successfully ingested: {file_path.name}")
            time.sleep(0.05)  # Polite debounce for batch writes
        elif "URL" in result and "Ingested" in result:
            logger.info(f"Successfully ingested URL artifact: {file_path.name}")
        else:
            logger.warning(f"Ingestion returned unexpected output: {file_path.name} | {result[:200]}")

    except Exception as e:
        logger.error(f"Ingestion failed for {file_path.name}: {e}")
        raise


def cleanup_tmp_file(file_path):
    """Safely remove artifact after ingestion."""
    try:
        if file_path.exists():
            file_path.unlink()
            logger.info(f"Cleaned up artifact: {file_path.name}")
    except Exception:
        pass  # Non-fatal: suppress on delete errors


def run_cycle(logger: logging.Logger) -> int:
    """
    Execute one tick of the ingestion loop.
    Returns: 0 = success/unchanged, 1 = processing done.
    """
    logger.info(f"Starting ingestion cycle (timeout={SCAN_TIMEOUT_SECONDS}s)")
    start_time = time.monotonic()

    try:
        artifacts, scan_time = discover_pending_tmp_files(BASE_DIR)
        logger.info(f"Scan complete: found {len(artifacts)} artifacts in {scan_time:.3f}s")

        if not artifacts:
            logger.info("UNCHANGED")
            return 0  # No files found -> graceful no-op

        ingested_count = 0
        for artifact_path in artifacts:
            try:
                logger.info(f"Processing artifact: {Path(artifact_path).name}")
                ingest_artifact(Path(artifact_path), logger)
                cleanup_tmp_file(artifact_path)
                ingested_count += 1

            except Exception as e:
                logger.error(f"Cycle interrupted at {artifact_path.name}: {e}")
                break

    except Exception as e:
        logger.critical(f"Cycle failed: {e}")
        raise RuntimeError(e)

    elapsed = time.monotonic() - start_time
    logger.info(f"Cycle finished: ingested={ingested_count}, elapsed={elapsed:.3f}s")
    return 1 if artifacts else 0


def parse_args() -> argparse.Namespace:
    """CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description="Obsidian Auto-Ingest Runner (Cron tick)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single run
  python obsidian-cron.py

  # Continuous loop (every 30 seconds)
  while true; do python obsidian-cron.py; done

  # Background daemon with daemonize
  daemonize; python obsidian-cron.py --daemon --interval 30

Environment:
  BASE_DIR (optional)  : Override default workspace path
        """
    )
    parser.add_argument(
        "--daemon", action="store_true",
        help="Run continuously in background until SIGINT"
    )
    parser.add_argument(
        "--interval", type=float, default=30.0,
        help="Loop interval in seconds (default: 30)"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Enable additional logging output"
    )
    return parser.parse_args()


def daemonize() -> None:
    """
    Unix-style daemonization shim for Windows cron integration.
    Drops to foreground (Windows limitation) but isolates stdio streams.
    """
    if os.name != "posix":
        # Windows: daemonization not native; fallback inline
        sys.stderr.write("Daemonize shim: Windows mode — running inline\n")
        return

    import os
    import signal

    try:
        if os.path.exists("/var/run/.obsidian-cron.pid"):
            os.remove("/var/run/.obsidian-cron.pid")

        pid = os.fork()
        if pid > 0:
            os._exit(0)  # Parent exits

        os.setsid()

        pid = os.fork()
        if pid > 0:
            os._exit(0)

        with open("/var/run/.obsidian-cron.pid", "w") as f:
            f.write(str(os.getpid()) + "\n")

        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        signal.signal(signal.SIGINT, signal.SIG_DFL)

    except Exception as e:
        sys.stderr.write(f"Daemonize fallback: {e}\n")


def main() -> None:
    args = parse_args()
    logger = setup_logging(verbose=args.verbose)

    if args.daemon:
        daemonize()

    try:
        if args.daemon and not args.verbose:
            while True:
                try:
                    run_cycle(logger)
                except Exception as e:
                    logger.exception("Cycle exception — retrying")
                time.sleep(args.interval)

        else:
            run_cycle(logger)

    except KeyboardInterrupt:
        pass

    except Exception as e:
        logger.exception(f"Uncaught exception: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/bin/sh
# Wrapper script: polls for .tmp artifacts every N seconds.
# POSIX-compliant entry point for cron or watch workflows.
BASE_DIR="E:/tommy vault/tommy vault/Read & Write"
INTERVAL="1"
LOGFILE="${BASE_DIR}/.hermes_cron/obsidian-cron.log"

run_tick() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Scanning for artifacts..."
    find "${BASE_DIR}" -maxdepth 1 -name "*.tmp" -type f -mmin -1 -empty 2>/dev/null \
        | xargs -r -I{} sh -c '
            path="{}"
            size=$(stat -f%z "$path" 2>/dev/null || stat -c%s "$path" 2>/dev/null)
            if [ "$size" -lt 102400 ]; then
                python "E:/tommy vault/tommy vault/Read & Write/.hermes_cron/obsidian-cron.py" --verbose 2>&1
            fi
        ' 2>&1 | tee -a "$LOGFILE"
}

while [ 1 ]; do
    run_tick
    sleep "$INTERVAL"
done

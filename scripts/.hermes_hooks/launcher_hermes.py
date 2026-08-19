#!/usr/bin/env python3
"""
Hermes + FastAPI Ollama Hook Launcher — Minimal, Bounded-Lifetime Process Management
"""

import subprocess, sys, json, time
from pathlib import Path

SCRIPTS = Path(r"E:\tommy vault\tommy vault\Read & Write\Scripts")
VAULT = SCRIPTS.parent

def daemonize(cmd, workdir, stdout_log, stderr_log):
    """Spawn background process, log activity, return PIDs."""
    # Prepare logs
    stdout_log.parent.mkdir(parents=True, exist_ok=True)
    with open(stdout_log, "a", encoding="utf-8") as f:
        f.write(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting daemon: {' '.join(cmd)}\n")
    
    # Start process (detach from terminal)
    proc = subprocess.Popen(
        cmd, cwd=workdir, env={**dict(sys.path), "PYTHONUNBUFFERED": "1"},
        stdout=stdout_log.open("a"), stderr=stderr_log.open("a"),
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS,
        close_fds=True, start_new_session=True
    )
    pid = proc.pid
    print(f"🚀 PID: {pid} | {' '.join(cmd)}")
    return True, pid

def main():
    print("🧩 Hermes + FastAPI Ollama Hook Launcher")
    basescript = str(SCRIPTS)
    hermes_path = f"{basescript}/launcher_hermes.py"
    hook_path = f"{basescript}/launcher_hook.py"

    if not Path(hermes_path).exists():
        # Provide a default launch path if not present (fallback for now)
        print("⚠️ No custom launcher_hermes.py found. Falling back to `hermes` CLI.")
        hermes_path = ["hermes", "--cli"]
    
    if not Path(hook_path).exists():
        hook_path = ["python", str(SCRIPTS / ".hermes_hooks" / "ollama-fp.py")]
    else:
        hook_path = [
            sys.executable,
            "-u",
            str(SCRIPTS / ".hermes_hooks" / "ollama-fp.py")
        ]

    # Logs in vault root
    stdout = VAULT / "daemon.log"
    stderr = VAULT / "daemon.err"

    print(f"🧪 Hermes & Hook Daemons:")
    print(f"  Hermes base: {str(hermes_path) if isinstance(hermes_path, (str, list)) else hermes_path}")
    print(f"  Hook base:   {str(hook_path) if isinstance(hook_path, (str, list)) else hook_path}")
    print(f"  Logs: stdout={stdout}, stderr={stderr}")

    # Spawn Hermes first (allows it to bootstrap routes)
    # Allow override: --daemon hermes_only skips hook
    hermes_only = len(sys.argv) > 1 and "--daemon" in sys.argv and "hermes_only" in sys.argv
    print(f"  Daemon-only Hermes: {hermes_only}")

    if isinstance(hermes_path, list):
        try:
            success, pid = daemonize(hermes_path, str(VAULT), stdout, stderr)
            if success:
                print(f"  ✅ Hermes launched (PID {pid}), logging to {stdout}")
            else:
                print(f"  ❌ Hermes spawn failed")
                return 1
        except Exception as e:
            print(f"  ❌ Hermes exception: {e}")
            return 1
    else:
        print(f"  ℹ️ Hermes will be invoked directly when needed.")

    # Give Hermes a quick boot-up grace window
    time.sleep(2)

    if not hermes_only:
        try:
            # Spawn FastAPI hook as child daemon
            success, pid = daemonize(hook_path, str(SCRIPTS), stdout, stderr)
            if success:
                print(f"  ✅ Hook launched (PID {pid}), logging to {stderr}")
            else:
                print(f"  ❌ Hook spawn failed")
                return 1
        except Exception as e:
            print(f"  ❌ Hook exception: {e}")
            return 1

    print("\n💡 Done. Daemons are logging to:")
    print(f"   {stdout}  (stdout)")
    print(f"   {stderr}  (stderr)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
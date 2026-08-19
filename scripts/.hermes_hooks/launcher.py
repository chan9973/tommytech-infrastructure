#!/usr/bin/env python3
"""
Hermes Integration Launcher — Hooks + Cron Bootstrap
Starts the FastAPI Ollama hook alongside your active Hermes instance.
"""

import subprocess, sys, shutil, json, os
from pathlib import Path

VAULT = Path(r"E:\tommy vault\tommy vault\Read & Write")
SCRIPTS = VAULT / "Scripts"
HOOK = SCRIPTS / ".hermes_hooks" / "ollama-fp.py"
CRON_LOG = VAULT / ".hermes_cron"
CRON_LOG.mkdir(parents=True, exist_ok=True)

def ensure_dirs():
    (SCRIPTS / "crash").mkdir(parents=True, exist_ok=True)
    CRON_LOG.mkdir(parents=True, exist_ok=True)

def start_hermes(noheadless=False):
    cmd = ["hermes"] if noheadless else ["hermes", "--cli"]
    print(f"🚀 Starting Hermes: {' '.join(cmd)}")
    os.environ.update()
    proc = subprocess.Popen(cmd, cwd=str(VAULT), env=os.environ.copy(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=0)
    return proc

def run_hook_daemon():
    """Starts FastAPI Ollama hook as background daemon, logging activity."""
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    proc = subprocess.Popen(
        ["python", "-u", str(HOOK)],
        cwd=str(SCRIPTS),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=0,
    )
    log_file = CRON_LOG / "hook-daemon.log"
    with open(log_file, "a", encoding="utf-8") as f:
        sys.stdout = f
        sys.stderr = f
    return proc

def main():
    ensure_dirs()
    print("🧩 Hermes + FastAPI Ollama Hook Launcher")
    print(f"  Hermes: {' '.join(['hermes'])}")
    print(f"  Hook:  {HOOK}")
    print()

    # Start Hermes process
    if len(sys.argv) > 1 and "daemon" in sys.argv[1]:
        # Daemon mode: start both Hermes & hook as background daemons
        proc_hermes = start_hermes()
        proc_hook = run_hook_daemon()
        print(f"✅ Hermes PID: {proc_hermes.pid}, Hook PID: {proc_hook.pid}")
        proc_hermes.wait()
        proc_hook.wait()
    else:
        # Interactive mode: start Hermes, hook runs in foreground
        proc_hermes = start_hermes()
        print(f"🧪 Hermes running. Waiting for Ollama hook to load...")

        # Give Hermes a moment to bootstrap
        try:
            json.loads(proc_hermes.stdout.readline().decode("utf-8"))
        except Exception:
            pass

        # Start hook as child of Hermes process (bounded lifetime)
        print("🔗 Starting FastAPI Ollama hook as Hermes child...")
        proc_hook = run_hook_daemon()
        print(f"🚀 Ollama hook PID: {proc_hook.pid}")

        if proc_hermes.poll() is None:
            print("\n💡 To test hooks directly:")
            print("  1) Run: uvicorn E:\\tommy vault\\tommy vault\\Read & Write\\Scripts\\.hermes_hooks\\ollama-fp.py:app --host 127.0.0.1 --port 8000")
            print("  2) Curl: curl http://127.0.0.1:8000/ollama-generate -d '{\"prompt\":\"Hi\",\"model\":\"Qwen3.5:latest\"}'")
            proc_hermes.wait()
        else:
            print("❌ Hermes exited early — check ~/.hermes/logs/gateway.log")

if __name__ == "__main__":
    main()
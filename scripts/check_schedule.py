"""
🧪 Scheduled compilation job runner

This script checks your Inbox folder daily and compiles any pending test files.
Run on: E:/tommy vault/tommy vault/Read & Write
Source: scripts/compile_inbox_batch.py
Schedule options: 
   - Daily at 8AM (08:00)
   - Weekly on Sunday (0 9 * * 0)
   - Bi-weekly every 2 weeks
"""

import subprocess
import time
from datetime import datetime

VAULT_PATH = "E:/tommy vault/tommy vault/Read & Write"
SCRIPT_PATH = f"{VAULT_PATH}/scripts/compile_inbox_batch.py"

def compile_inbox():
    """Run the batch compilation script"""
    cmd = ['python', SCRIPT_PATH]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        print(result.stdout)
        if result.stderr:
            print("stderr:", result.stderr[:500])
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Compilation failed: {e}")
        return False

if __name__ == "__main__":
    log = lambda msg: print(f"[{datetime.now().strftime('%H:%M')}] {msg}")
    log("=" * 60)
    log("📅 Scheduled compilation job")
    log(f"Running: {SCRIPT_PATH}")
    log("=" * 60)
    
    success = compile_inbox()
    log("\n✅ Success!" if success else "❌ Failed")

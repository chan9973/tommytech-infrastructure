#!/usr/bin/env python3
"""
Setup Windows Task Scheduler for daily vault cleanup
This script creates a scheduled task that runs at 5am daily
"""

import os
import subprocess
import sys
from pathlib import Path

SCRIPT_PATH = Path(r"E:\tommy vault\tommy vault\Read & Write\scripts\daily_cleanup.bat")
TASK_NAME = "Daily Obsidian Vault Cleanup"

def create_scheduled_task():
    """Create Windows scheduled task using schtasks"""
    
    # First, check if task already exists
    result = subprocess.run(
        ["schtasks", "/Query", "/TN", TASK_NAME],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(f"Task '{TASK_NAME}' already exists.")
        print("Use the 'Delete' option and recreate to update.")
        return
    
    # Create the scheduled task
    command = [
        "schtasks", "/Create",
        "/TN", TASK_NAME,
        "/TR", f'"{SCRIPT_PATH}"',
        "/SC", "DAILY",
        "/ST", "05:00",
        "/RL", "HIGHEST",  # Run with highest privileges
        "/F"  # Force create
    ]
    
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✓ Successfully created scheduled task: {TASK_NAME}")
        print(f"  Runs daily at 5:00 AM")
        print(f"  Log file: {SCRIPT_PATH.parent.parent / 'memories' / 'daily-cleanup.log'}")
    else:
        print(f"✗ Error creating task:")
        print(result.stderr)
        
        # Fallback: Provide manual commands
        print("\nManual setup commands:")
        print(f"schtasks /Create /TN \"{TASK_NAME}\" /TR \"{SCRIPT_PATH}\" /SC DAILY /ST 05:00 /RL HIGHEST /F")

def delete_scheduled_task():
    """Delete the scheduled task"""
    result = subprocess.run(
        ["schtasks", "/Delete", "/TN", TASK_NAME, "/F"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(f"✓ Deleted task: {TASK_NAME}")
    else:
        print(f"Error deleting task: {result.stderr}")

def list_tasks():
    """List all scheduled tasks with our naming pattern"""
    result = subprocess.run(
        ["schtasks", "/Query", "/FO", "TABLE"],
        capture_output=True,
        text=True
    )
    
    if "Vault" in result.stdout or "Cleanup" in result.stdout:
        print("\nExisting vault-related tasks:")
        # Filter for vault tasks
        for line in result.stdout.split('\n'):
            if 'Vault' in line or 'cleanup' in line.lower():
                print(line)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "delete":
            delete_scheduled_task()
        elif sys.argv[1] == "list":
            list_tasks()
        elif sys.argv[1] == "create":
            create_scheduled_task()
        else:
            print("Usage:")
            print("  python setup_scheduled_task.py create  # Create task")
            print("  python setup_scheduled_task.py delete  # Delete task")
            print("  python setup_scheduled_task.py list    # List tasks")
    else:
        create_scheduled_task()
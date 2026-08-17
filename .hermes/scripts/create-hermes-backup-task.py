"""
Hermes Agent Auto-Backup Task
Schedules via: Task Scheduler -> Basic Trigger -> Every 3 hours

Script location: E:\tommy vault\tommy vault\Read & Write\.hermes\scripts\backup-hermes.bat
Trigger location: C:\Windows\System32\Tasks\Hermes_Backup_Every_3Hrs
"""

import subprocess
import datetime
import winreg

def create_task():
    """Create Task Scheduler job to run backup every 3 hours."""
    
    task_name = "Hermes_Backup_Every_3Hrs"
    script_path = r'E:\tommy vault\tommy\Read & Write\.hermes\scripts\backup-hermes.bat'
    start_time = datetime.datetime.now().replace(second=0, microsecond=0)
    
    print("=" * 60)
    print("Creating Hermes Auto-Backup Task (every 3 hours)")
    print(f"Script: {script_path}")
    print("=" * 60)
    
    try:
        # Create Windows Task Scheduler registry entries
        # Note: This uses the 'schtasks' command which is simpler
        
        cmd = f'schtasks /Create /TN "{task_name}" /TR "cmd /c {script_path}" /SC HOURLY /MO 3 /ST 00 /ID 0x123456'
        print(f"Executing: {cmd}")
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"✅ Task created successfully: {task_name}")
            print(f"   - Runs every 3 hours")
            print(f"   - Script: {script_path}")
            print(f"   - Output dir: E:\tommy vault\tommy\.hermes_backup")
            return True
        else:
            print(f"❌ Failed to create task:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error creating task: {e}")
        return False

def verify_task():
    """Verify the task exists."""
    import shutil
    
    output = subprocess.run(['schtasks', '/Query', '/TN:Hermes_Backup_Every_3Hrs'], 
                           capture_output=True, text=True)
    
    if 'SUCCESS' in output.stdout:
        print("✅ Task verified:")
        print(output.stdout)
    else:
        print("❌ Task not found or incomplete:")
        print(output.stdout)

if __name__ == "__main__":
    create_task()
    verify_task()
    print("Note: You may need to run as Administrator for task creation")

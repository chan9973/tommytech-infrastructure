# Build configuration for Nissan GTR Music Player
# Run: python build_exe.py

import os
import subprocess
import sys

# Change to project root
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Install dependencies
print("Installing dependencies...")
subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller", "pydub", 
                "pytube", "numpy", "tkinter", "pillow"], check=True)

# Build executable
build_cmd = [
    "pyinstaller",
    "--onefile",
    "--windowed",
    "--name=GTR_Player",
    "--icon=",  # Add icon if available
    "--add-data=src;src",
    "main.py"
]

print("Building executable...")
result = subprocess.run(build_cmd, capture_output=True, text=True)

if result.returncode == 0:
    print("Build successful!")
    print(f"Executable location: dist/GTR_Player.exe")
else:
    print("Build failed:")
    print(result.stderr)
    sys.exit(1)
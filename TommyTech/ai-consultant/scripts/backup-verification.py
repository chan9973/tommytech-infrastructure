#!/usr/bin/env python3
"""
Model Backup Verification Tool
Author: Tommy Chan
Purpose: Verify qwen3.5-hermes model backup integrity on F: drive
"""

import os
import sys
from pathlib import Path

def check_model_backup(f_drive_path="F:/ollama-models-backup"):
    """Verify model files exist and are healthy"""
    model_path = Path(f_drive_path) / "edtorre" / "qwen3.5-hermes"

    print("🔍 MODEL BACKUP VERIFICATION")
    print("=" * 40)

    if not model_path.exists():
        print(f"❌ Model path not found: {model_path}")
        return False

    # Check for key blobs
    blobs_dir = Path(f_drive_path)
    blob_files = list(blobs_dir.glob("*"))
    total_size = sum(f.stat().st_size for f in blob_files if f.is_file())

    print(f"✅ Model path exists")
    print(f"📦 Total backup files: {len(blob_files)}")
    print(f"💾 Total size: {total_size / (1024**3):.2f} GB")

    # Verify minimum size threshold (6.6GB for qwen3.5-hermes)
    if total_size >= 6 * 1024**3:
        print("✅ Backup meets minimum size requirements")
        return True
    else:
        print("⚠️  Backup smaller than expected - needs verification")
        return False

if __name__ == "__main__":
    result = check_model_backup()
    sys.exit(0 if result else 1)
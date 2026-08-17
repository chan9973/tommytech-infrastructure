@echo off
REM ============================================================================
📅 Scheduled compilation job for Hermes LLM wiki inbox
Location: E:\tommy vault\tommy vault\Read & Write
Source script: scripts/compile_inbox_batch.py
Destination: _wiki/ folder
Schedule: Daily at 08:00 AM (or bi-weekly on Sunday at 09:00)
Security: Restricted to .private folder (not accessed/scanned)
Run as: Current user (C:\Users\tommy)
==============================================================================

REM Check if compilation script exists
python "E:/tommy vault/tommy vault/Read & Write/scripts/compile_inbox_batch.py"

exit /b %ERRORLEVEL%

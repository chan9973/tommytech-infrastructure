@echo off
REM ============================================================================
📅 Hermes LLM wiki inbox scheduler for Obsidian vault

Configuration:
   Script source: scripts/compile_inbox_batch.py
   Output target: _wiki/ folder
   Schedule options (choose one or create a new task):
   1. Daily at 08:00 — For daily log compilation
   2. Weekly on Sunday — Full wiki refresh every week
   3. Bi-weekly every 2 weeks — Less frequent checks
==============================================================================

REM Check if Python and heredoc are available
where python >nul 2>&1 && goto :setup || (echo ❌ Python not found && exit /b 1)

echo ✅ Python located in PATH
echo ============================================================================
echo 🧪 Hermes LLM wiki scheduled compilation
echo ============================================================================
echo

REM Run the compilation script directly
python "E:/tommy vault/tommy vault/Read & Write/scripts/compile_inbox_batch.py"

exit /b %ERRORLEVEL%

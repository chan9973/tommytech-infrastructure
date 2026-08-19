@echo off
REM Daily Vault Cleanup - Windows Scheduled Task Wrapper
REM Runs the Obsidian cleanup and generates quality report

set VULT_PATH=E:\tommy vault\tommy vault\Read & Write
set SCRIPT_PATH=%VULT_PATH%\scripts\daily_vault_cleanup.py
set LOG_PATH=%VULT_PATH%\memories\daily-cleanup.log

echo [%date% %time%] Starting daily vault cleanup >> "%LOG_PATH%"

REM Run the cleanup script
python "%SCRIPT_PATH%" >> "%LOG_PATH%" 2>&1

if %ERRORLEVEL% EQU 0 (
    echo [%date% %time%] Cleanup completed successfully >> "%LOG_PATH%"
) else (
    echo [%date% %time%] Cleanup failed with error %ERRORLEVEL% >> "%LOG_PATH%"
)

REM Generate quality report
python "%VULT_PATH%\scripts\optimize_vault.py" --report >> "%LOG_PATH%" 2>&1

echo [%date% %time%] Daily maintenance complete >> "%LOG_PATH%"

exit /b 0
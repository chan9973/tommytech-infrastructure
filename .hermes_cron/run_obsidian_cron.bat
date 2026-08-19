@echo off
REM Obsidian Auto-Ingest Runner - Windows Batch Wrapper
REM Runs obsidian-cron.py periodically, logs output to CronOutput.log, exits when interrupted.
set BASE_DIR="E:\tommy vault\tommy vault\Read & Write\.hermes_cron"
set PY="E:\Users\tommy\AppData\Local\Python\Python314\python.exe"
set CRON_LOG=%BASE_DIR%\obsidian-cron.log
set OUTPUT_LOG=%BASE_DIR%\CronOutput.log
set CHECK_INTERVAL=60
set START_TIME=%TIME%
set LAST_CHECK=%START_TIME%

echo ============================================
echo Obsidian Cron Runner (Batch Wrapper)
echo ============================================

:[CHECK]
if "%PROCESSING%"=="1" goto :END
if exist "%PY\$0" (
    echo [OK] Python found: %PY%
) else (
    echo [ERROR] Python runtime not detected at %PY%
    echo Please ensure Python is installed and in PATH.
    goto :END
)
python.exe %PY%\%1 || echo [WARN] Command may not be recognized - try full path.

if exist "%CRON_LOG%" (
    tail -3 "%CRON_LOG%" >nul 2>&1 || (echo [INFO] First run - no prior log)
) else (
    echo [INFO] Starting fresh run
)

python.exe "%PY%\obsidian-cron.py" --verbose 2>>"%OUTPUT_LOG%"
echo.
echo ============================================
echo CRON tick complete: %DATE% %TIME%
echo ============================================

:[NEXT]
set /a INTERVAL=$((PUSHD ^&^>nul ^& set /a CURRENT_S=60^*%%100^+60 %%100^*60^+%%10^; cls ^& echo Current time is %CURRENT_S% ^; set /a TARGET_S=60 %%100^+60 %%100^*60^+%%10^; cls ^& echo Target interval: 60 ^; cls ^& set /a DIFF=TARGET_S - CURRENT_S^))
if %DIFF% LSS 0 set /a DIFF=0
timeout /t %DIFF% /nobreak 2^>nul
goto :CHECK

:[END]
echo Final cron run finished: %DATE% %TIME%
exit /b 0
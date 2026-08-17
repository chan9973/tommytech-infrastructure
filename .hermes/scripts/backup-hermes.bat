@echo off
REM Hermes Agent Auto-Backup - Runs every 3 hours
REM Usage: Place in Windows System32 or Task Scheduler
REM Author: Tommy Chan from Ipoh, Malaysia
REM Date: 2026-08-16

:: Configuration
SET VAULT_BACKUP_DIR=E:\tommy vault\tommy vault\.hermes_backup
SET SOURCE_HERMES_DIR="C:\Users\tommy\.hermes"

:: Create backup directory if not exists
if not exist "%VAULT_BACKUP_DIR%" mkdir "%VAULT_BACKUP_DIR%"

:: Generate timestamped backup name
for /f "tokens=*" %%T in ('date /t') do set CURRENT_DATE=%%T
set CURRENT_TIME=%time:~0,2% %time:~3,2%
set BACKUP_PATH=%VAULT_BACKUP_DIR\.hermes_%CURRENT_DATE%_%CURRENT_TIME%

:: Backup the .hermes directory
if exist "%SOURCE_HERMES_DIR%" (
    xcopy "%SOURCE_HERMES_DIR%\*" "%BACKUP_PATH%\*\*.*" /E /I /H /K /C /Y\nul
    echo ========================================
    echo Hermes Auto-Backup Completed Successfully
    echo Backup location: %BACKUP_PATH%
    echo ========================================
    
    :: Log the backup
    echo %date% %time% - Success >> "E:\tommy vault\tommy\Read & Write\memories\hermes-backup.log"
) else (
    echo Source not found at %SOURCE_HERMES_DIR%, skipping backup
    echo %date% %time% - SKIPPED (source not found) >> "E:\tommy vault\tommy\Read & Write\memories\hermes-backup.log"
)

exit /b 0

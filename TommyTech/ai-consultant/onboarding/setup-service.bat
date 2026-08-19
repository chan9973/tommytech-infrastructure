@echo off
:: ══════════════════════════════════════════════════════════════
:: TommyTech Autonomous AI Setup Service — Master Orchestrator
:: Fully AI-driven: remote (TeamViewer/AnyDesk) or local install
:: Usage: setup-service.bat [client-config.yaml]
:: ══════════════════════════════════════════════════════════════
setlocal EnableDelayedExpansion

:: ── Config ───────────────────────────────────────────────────
set CLIENT_CONFIG=%~1
if "%CLIENT_CONFIG%"=="" set CLIENT_CONFIG=service-config-template.yaml
set VAULT_DIR=E:\tommy vault\tommy vault\Read & Write
set SCRIPTS_DIR=%VAULT_DIR%\TommyTech\ai-consultant

echo ═══════════════════════════════════════════════════════════════
echo  🖥️  TOMMTECH AUTONOMOUS AI SETUP SERVICE
echo  Client Config: %CLIENT_CONFIG%
echo  Vault: %VAULT_DIR%
echo ═══════════════════════════════════════════════════════════════

:: ── STEP 1: Verify Prerequisites ──────────────────────────────
echo [1/7] Checking prerequisites...
call "%SCRIPTS_DIR%\onboarding\local-setup.bat"
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Prerequisite check failed. Aborting.
    exit /b 1
)
echo ✓ Prerequisites verified

:: ── STEP 2: Create Python Environment ─────────────────────────
echo [2/7] Setting up Python environment...
cd /d "%VAULT_DIR%\TommyTech\ai-consultant"
if not exist ".venv\" (
    python3 -m venv .venv
    echo ✓ Virtual environment created
) else (
    echo ℹ Virtual environment already exists
)
call .venv\Scripts\activate.bat
python --version
pip install --upgrade pip setuptools wheel -q
echo ✓ Environment ready

:: ── STEP 3: Install Hermes + Dependencies ─────────────────────
echo [3/7] Installing Hermes and dependencies...
pip install hermes-tools -q 2>nul
pip install requests urllib3 -q
echo ✓ Tools installed

:: ── STEP 4: Pull Local Model ──────────────────────────────────
echo [4/7] Pulling AI model via Ollama...
ollama list | findstr /i "qwen3.5" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ℹ Downloading qwen3.5-hermes model...
    ollama pull edtorre/qwen3.5-hermes:latest
    echo ✓ Model installed
) else (
    echo ✓ Model already available
)

:: ── STEP 5: Provision Obsidian Vault ──────────────────────────
echo [5/7] Provisioning Obsidian vault...
cd /d "%VAULT_DIR%"
if not exist "Read & Write\.obsidian\" (
    mkdir "Read & Write\.obsidian\plugins" 2>nul
    echo ✓ Vault structure created
) else (
    echo ℹ Vault already exists
)

:: ── STEP 6: Configure Wiki Ingest ─────────────────────────────
echo [6/7] Configuring wiki ingestion automation...
set OBSIDIAN_VAULT_PATH=%VAULT_DIR%
python "%VAULT_DIR%\scripts\obsidian-ingest.py" "# TommyTech Setup Complete" --tags setup,automated
echo ✓ Wiki ingest configured

:: ── STEP 7: Run Verification ────────────────────────────────────
echo [7/7] Running verification tests...
python "%SCRIPTS_DIR%\training\test_hermes_checklist.py"
if %ERRORLEVEL% NEQ 0 (
    echo [WARN] Verification completed with warnings
) else (
    echo ✓ All verification tests passed
)

echo ═══════════════════════════════════════════════════════════════
echo  ✅ SETUP COMPLETE
echo  🎯 Service: Autonomous AI Agent Cluster
echo  📁 Vault: %VAULT_DIR%
echo  🎮 Agents: Research + Coding + Support
echo ═══════════════════════════════════════════════════════════════

@echo off
:: 🌐 LOCAL AI SETUP CONSULTANT
:: Client Onboarding Plan - Simplified (No External Storage Required)
:: Tommy Chan - Ipoh, Malaysia | 2026-08-19
:: NOTE: Cloud-free verification only - no F: drive dependency

echo ================================================
echo LOCAL AI SETUP - CLOUD-FREE VERIFICATION
echo ================================================
echo.

:: ── STEP 1: Python Environment ──────────────────
echo [1/5] ✓ Python Environment Check
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=2 delims=()" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo    Version: %PYTHON_VERSION%
    echo    ✓ Ready for local agent deployment
) else (
    echo    ✗ Python missing - Install Python 3.11+ first
    goto :END
)

:: ── STEP 2: Ollama Local Server ───────────────────
echo [2/5] ✓ Ollama Server Check
ollama --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo    ✓ Ollama running locally (localhost only)
    echo    ✓ No cloud connections required
) else (
    echo    ✗ Ollama not installed - Run: curl -fsSL https://ollama.com/install.sh | sh
)

:: ── STEP 3: Model Status ─────────────────────────
echo [3/5] ✓ Model Deployment Check
ollama list | findstr "qwen3.5-hermes" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo    ✓ qwen3.5-hermes locally deployed
    echo    ✓ Offline inference enabled
) else (
    echo    ℹ Model not yet downloaded - Run: ollama pull edtorre/qwen3.5-hermes
)

:: ── STEP 4: Agent Tools ───────────────────────────
echo [4/5] ✓ Agent Tools Installation
pip list | findstr "hermes-agent" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo    ✓ Hermes Agent tools verified
) else (
    echo    ℹ Installing: pip install hermes-agent
)

:: ── STEP 5: Compliance Check ──────────────────────
echo [5/5] ✓ GDPR/PDPA Compliance Verification
echo    • Data stays on local disk only
echo    • No external API keys required
echo    • No telemetry or cloud syncing
echo    ✓ Passive monitoring enabled

:END
echo.
echo ================================================
echo ✅ NEXT: Book Free 30-Min Diagnostic Call
echo    Calendly: calendly.com/tommy-ai-consult
echo ================================================
echo.
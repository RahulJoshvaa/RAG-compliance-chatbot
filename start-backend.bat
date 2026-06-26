@echo off
REM ============================================================
REM  Start the RAG backend API (Flask) in LIVE mode.
REM  First run creates a virtual env and installs dependencies;
REM  later runs reuse it and start immediately.
REM ============================================================

setlocal
cd /d "%~dp0generation"

if not exist ".venv\Scripts\python.exe" (
    echo [setup] Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo [error] Could not create venv. Is Python 3.12 installed and on PATH?
        pause
        exit /b 1
    )
    echo [setup] Installing backend dependencies ^(this takes a few minutes^)...
    call ".venv\Scripts\activate.bat"
    python -m pip install --upgrade pip
    python -m pip install -r requirements-all.txt
    if errorlevel 1 (
        echo [error] Dependency install failed. See messages above.
        pause
        exit /b 1
    )
) else (
    call ".venv\Scripts\activate.bat"
)

echo.
echo [run] Starting API on http://localhost:8000  ^(first launch loads the model, ~30-60s^)
echo [run] Leave this window open. Press Ctrl+C to stop.
echo.
python api.py

pause

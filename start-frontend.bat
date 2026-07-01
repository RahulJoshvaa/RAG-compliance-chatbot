@echo off
REM ============================================================
REM  Start the RAG frontend (Vite dev server).
REM  First run installs npm packages; later runs start directly.
REM ============================================================

setlocal
cd /d "%~dp0frontend"

if not exist "node_modules" (
    echo [setup] Installing frontend dependencies ^(first run only^)...
    call npm install
    if errorlevel 1 (
        echo [error] npm install failed. Is Node.js 18+ installed and on PATH?
        pause
        exit /b 1
    )
)

echo.
echo [run] Starting frontend on http://localhost:5173
echo [run] Make sure the backend (start-backend.bat) is running too.
echo [run] Leave this window open. Press Ctrl+C to stop.
echo.
call npm run dev

pause

@echo off
chcp 65001 >nul
title Image Similarity Search Tool - Simple Start
echo ===============================================
echo    Image Similarity Search Tool (Simple)
echo ===============================================
echo.

:: Check Python
python --version
if %errorlevel% neq 0 (
    echo [ERROR] Python not found
    pause
    exit /b 1
)

cd /d "%~dp0backend"

:: Try to run directly first (if deps already installed)
echo [INFO] Checking if dependencies are available...
python -c "import fastapi, uvicorn, PIL, imagehash" >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] Dependencies found, starting service...
    goto :start_service
)

:: If not available, try simple installation
echo [INFO] Installing minimal dependencies...
python -m pip install --no-cache-dir fastapi uvicorn pillow imagehash python-multipart pydantic aiofiles
if %errorlevel% neq 0 (
    echo [ERROR] Installation failed. Please run install_deps.py manually
    pause
    exit /b 1
)

:start_service
echo.
echo [INFO] Starting service on http://localhost:8001
echo [TIP] Open simple_frontend.html in browser
echo [TIP] Press Ctrl+C to stop
echo ===============================================
echo.

python main.py
pause
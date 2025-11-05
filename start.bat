@echo off
chcp 65001 >nul
title Image Similarity Search Tool - Start
echo ===============================================
echo      Image Similarity Search Tool
echo ===============================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found, please install Python 3.11 or higher
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [INFO] Checking Python environment...
python --version

:: Enter backend directory
cd /d "%~dp0backend"
if not exist "main.py" (
    echo [ERROR] Backend files not found, please run from correct directory
    pause
    exit /b 1
)

:: Check and create virtual environment
if not exist "venv" (
    echo [INFO] Creating Python virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
)

:: Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

:: Install/update dependencies
echo [INFO] Installing Python packages...
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip --quiet --disable-pip-version-check
if %errorlevel% neq 0 (
    echo [WARNING] Failed to upgrade pip, continuing...
)

echo [INFO] Installing packages from minimal requirements...
python -m pip install -r requirements-minimal.txt --quiet --disable-pip-version-check
if %errorlevel% neq 0 (
    echo [WARNING] Minimal install failed, trying individual packages...
    python -m pip install fastapi --quiet --disable-pip-version-check
    python -m pip install uvicorn --quiet --disable-pip-version-check
    python -m pip install python-multipart --quiet --disable-pip-version-check
    python -m pip install Pillow --quiet --disable-pip-version-check
    python -m pip install imagehash --quiet --disable-pip-version-check
    python -m pip install pydantic --quiet --disable-pip-version-check
    python -m pip install aiofiles --quiet --disable-pip-version-check
)

:: Check if critical packages are available
python -c "import fastapi, uvicorn, PIL, imagehash" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Critical packages missing. Please install manually:
    echo   pip install fastapi uvicorn pillow imagehash python-multipart
    pause
    exit /b 1
)

:: Start backend service
echo.
echo [INFO] Starting backend service...
echo [INFO] Backend URL: http://localhost:8001
echo [INFO] API Docs: http://localhost:8001/docs
echo.
echo [TIP] Open frontend in browser:
echo [TIP] Double-click simple_frontend.html in project root
echo.
echo [TIP] Press Ctrl+C to stop service
echo ===============================================
echo.

python main.py

pause
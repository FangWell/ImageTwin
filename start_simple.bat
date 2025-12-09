@echo off
chcp 65001 >nul
title ImageTwin - 快速启动
echo ===============================================
echo       ImageTwin - 智能图片相似度搜索
echo ===============================================
echo.

:: Check Python - try py launcher first (most reliable on Windows)
set PYTHON_CMD=

:: Try py launcher first
py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    goto :found_python
)

:: Try python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    goto :found_python
)

:: Try python3
python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python3
    goto :found_python
)

:: Check Windows Apps python (may need Store install)
"%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe" --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD="%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe"
    goto :found_python
)

echo [ERROR] Python 未找到
echo.
echo 请确保:
echo   1. 已安装 Python 3.8 或更高版本
echo   2. 安装时勾选了 "Add Python to PATH"
echo.
echo 下载: https://www.python.org/downloads/
pause
exit /b 1

:found_python
echo [INFO] 检测到: %PYTHON_CMD%
%PYTHON_CMD% --version

cd /d "%~dp0backend"

:: Try to run directly first (if deps already installed)
echo [INFO] 检查依赖包...
%PYTHON_CMD% -c "import fastapi, uvicorn, PIL, imagehash" >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] 依赖包已就绪
    goto :start_service
)

:: If not available, try simple installation
echo [INFO] 安装依赖包...
%PYTHON_CMD% -m pip install --no-cache-dir fastapi uvicorn pillow imagehash python-multipart pydantic aiofiles
if %errorlevel% neq 0 (
    echo [ERROR] 安装失败，请手动运行 install_deps.py
    pause
    exit /b 1
)

:start_service
echo.
echo [INFO] 启动服务: http://localhost:8001
echo [TIP] 按 Ctrl+C 停止服务
echo ===============================================
echo.

:: Open frontend in browser
start "" "%~dp0simple_frontend.html"

%PYTHON_CMD% main.py
pause
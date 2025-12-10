@echo off
chcp 65001 >nul
title ImageTwin - 智能图片相似度搜索工具
echo ===============================================
echo      ImageTwin - 智能图片相似度搜索工具
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

:: Check Windows Apps python
"%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe" --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD="%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe"
    goto :found_python
)

:: Python not found
echo [ERROR] Python 未找到
echo.
echo 请确保已安装 Python 并添加到 PATH 环境变量:
echo   1. 重新安装 Python，勾选 "Add Python to PATH"
echo   2. 或手动添加 Python 安装目录到系统 PATH
echo.
echo 下载地址: https://www.python.org/downloads/
pause
exit /b 1

:found_python
echo [INFO] 检测到 Python: %PYTHON_CMD%
%PYTHON_CMD% --version

:: Enter backend directory
cd /d "%~dp0backend"
if not exist "main.py" (
    echo [ERROR] 后端文件未找到，请在正确的目录运行
    pause
    exit /b 1
)

:: Check and create virtual environment
if not exist "venv" (
    echo [INFO] 创建 Python 虚拟环境...
    %PYTHON_CMD% -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] 创建虚拟环境失败
        pause
        exit /b 1
    )
)

:: Activate virtual environment
echo [INFO] 激活虚拟环境...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] 激活虚拟环境失败
    pause
    exit /b 1
)

:: Install/update dependencies
echo [INFO] 安装 Python 依赖包...
echo [INFO] 升级 pip...
python -m pip install --upgrade pip --quiet --disable-pip-version-check
if %errorlevel% neq 0 (
    echo [WARNING] pip 升级失败，继续...
)

echo [INFO] 安装核心依赖包...
python -m pip install fastapi uvicorn python-multipart Pillow imagehash pydantic aiofiles --quiet --disable-pip-version-check
if %errorlevel% neq 0 (
    echo [WARNING] 部分依赖安装失败，继续...
)

:: 尝试安装 OpenCV（可选，用于局部特征匹配）
echo [INFO] 安装 OpenCV (可选)...
python -m pip install numpy opencv-python-headless --only-binary=:all: --quiet --disable-pip-version-check
if %errorlevel% neq 0 (
    echo [INFO] OpenCV 安装失败，局部特征匹配功能将不可用
)

:: Check if critical packages are available
python -c "import fastapi, uvicorn, PIL, imagehash" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] 关键依赖包缺失，请手动安装:
    echo   pip install fastapi uvicorn pillow imagehash python-multipart
    pause
    exit /b 1
)

:: Start backend service
echo.
echo [INFO] 启动后端服务...
echo [INFO] 后端地址: http://localhost:8001
echo.
echo [TIP] 按 Ctrl+C 停止服务
echo ===============================================
echo.

:: Open frontend in browser
start "" "%~dp0simple_frontend.html"

python main.py

pause
@echo off
chcp 65001 >nul
title 图片相似度搜索工具 - 关闭
echo ===============================================
echo       正在关闭图片相似度搜索工具...
echo ===============================================
echo.

:: 查找并关闭Python进程
echo [信息] 查找运行中的服务...
for /f "tokens=2" %%i in ('tasklist /fi "imagename eq python.exe" /fo csv ^| find "python.exe"') do (
    echo [信息] 发现Python进程: %%i
    taskkill /f /pid %%i >nul 2>&1
    if %errorlevel% equ 0 (
        echo [成功] 已停止进程 %%i
    )
)

:: 检查端口8001是否仍被占用
echo [信息] 检查端口占用情况...
netstat -ano | findstr :8001 >nul 2>&1
if %errorlevel% equ 0 (
    echo [信息] 端口8001仍被占用，尝试强制关闭...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8001') do (
        taskkill /f /pid %%a >nul 2>&1
        if %errorlevel% equ 0 (
            echo [成功] 已释放端口8001
        )
    )
) else (
    echo [信息] 端口8001已释放
)

echo.
echo [完成] 图片相似度搜索工具已关闭
echo ===============================================
timeout /t 3 >nul
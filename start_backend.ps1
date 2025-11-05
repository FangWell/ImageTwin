# 图片相似度搜索工具 - 启动脚本
# 运行此脚本来启动后端服务

Write-Host "=== 图片相似度搜索工具 ===" -ForegroundColor Green
Write-Host "正在启动后端服务..." -ForegroundColor Yellow

# 检查Python环境
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python版本: $pythonVersion" -ForegroundColor Cyan
} catch {
    Write-Host "错误: 未找到Python，请确保已安装Python 3.11+" -ForegroundColor Red
    exit 1
}

# 切换到后端目录
Set-Location -Path "backend"

# 检查虚拟环境
if (Test-Path "venv") {
    Write-Host "激活虚拟环境..." -ForegroundColor Cyan
    & ".\venv\Scripts\Activate.ps1"
} else {
    Write-Host "未找到虚拟环境，使用全局Python环境" -ForegroundColor Yellow
}

# 安装依赖（如果需要）
Write-Host "检查依赖..." -ForegroundColor Cyan
pip install -r requirements.txt --quiet

# 启动服务
Write-Host "启动FastAPI服务器..." -ForegroundColor Green
Write-Host "服务地址: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API文档: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Yellow
Write-Host ""

python main.py
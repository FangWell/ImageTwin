#!/bin/bash

# 设置脚本编码
export LANG=en_US.UTF-8

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}===============================================${NC}"
echo -e "${GREEN}           图片相似度搜索工具${NC}"
echo -e "${GREEN}===============================================${NC}"
echo

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo -e "${RED}[错误] 未找到Python，请先安装Python 3.11或更高版本${NC}"
        if [[ "$OSTYPE" == "darwin"* ]]; then
            echo "macOS安装方法: brew install python3"
            echo "或访问: https://www.python.org/downloads/"
        else
            echo "Ubuntu/Debian: sudo apt-get install python3 python3-pip python3-venv"
            echo "CentOS/RHEL: sudo yum install python3 python3-pip"
        fi
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo -e "${BLUE}[信息] 检查Python环境...${NC}"
$PYTHON_CMD --version

# 进入后端目录
cd "$BACKEND_DIR" || {
    echo -e "${RED}[错误] 找不到后端目录: $BACKEND_DIR${NC}"
    exit 1
}

if [ ! -f "main.py" ]; then
    echo -e "${RED}[错误] 找不到后端文件main.py${NC}"
    exit 1
fi

# 检查并创建虚拟环境
if [ ! -d "venv" ]; then
    echo -e "${BLUE}[信息] 创建Python虚拟环境...${NC}"
    $PYTHON_CMD -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}[错误] 创建虚拟环境失败${NC}"
        exit 1
    fi
fi

# 激活虚拟环境
echo -e "${BLUE}[信息] 激活虚拟环境...${NC}"
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}[错误] 激活虚拟环境失败${NC}"
    exit 1
fi

# 安装/更新依赖
echo -e "${BLUE}[信息] 安装Python依赖包...${NC}"
pip install -r requirements.txt --quiet --disable-pip-version-check
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}[警告] 部分依赖包安装失败，尝试继续运行...${NC}"
fi

# 启动后端服务
echo
echo -e "${GREEN}[信息] 启动后端服务...${NC}"
echo -e "${BLUE}[信息] 后端地址: http://localhost:8001${NC}"
echo -e "${BLUE}[信息] API文档: http://localhost:8001/docs${NC}"
echo
echo -e "${YELLOW}[提示] 打开浏览器访问前端页面:${NC}"
echo -e "${YELLOW}[提示] 双击项目根目录下的 simple_frontend.html 文件${NC}"
echo
echo -e "${YELLOW}[提示] 按 Ctrl+C 停止服务${NC}"
echo -e "${GREEN}===============================================${NC}"
echo

# 设置信号处理
trap 'echo -e "\n${YELLOW}正在关闭服务...${NC}"; kill $PID 2>/dev/null; exit 0' INT TERM

# 启动Python服务并获取PID
python main.py &
PID=$!

# 等待服务结束
wait $PID
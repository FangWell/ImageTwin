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
echo -e "${GREEN}       正在关闭图片相似度搜索工具...${NC}"
echo -e "${GREEN}===============================================${NC}"
echo

# 查找并关闭Python进程
echo -e "${BLUE}[信息] 查找运行中的服务...${NC}"

# 查找占用8001端口的进程
PORT_PID=$(lsof -t -i:8001 2>/dev/null)
if [ -n "$PORT_PID" ]; then
    echo -e "${BLUE}[信息] 发现占用端口8001的进程: $PORT_PID${NC}"
    kill -TERM $PORT_PID 2>/dev/null
    sleep 2
    
    # 检查进程是否已经关闭
    if kill -0 $PORT_PID 2>/dev/null; then
        echo -e "${YELLOW}[信息] 强制关闭进程...${NC}"
        kill -KILL $PORT_PID 2>/dev/null
    fi
    
    if ! kill -0 $PORT_PID 2>/dev/null; then
        echo -e "${GREEN}[成功] 已停止进程 $PORT_PID${NC}"
    fi
else
    echo -e "${BLUE}[信息] 未发现占用端口8001的进程${NC}"
fi

# 查找可能的Python主进程
PYTHON_PIDS=$(pgrep -f "main.py" 2>/dev/null)
if [ -n "$PYTHON_PIDS" ]; then
    echo -e "${BLUE}[信息] 发现Python服务进程: $PYTHON_PIDS${NC}"
    for pid in $PYTHON_PIDS; do
        kill -TERM $pid 2>/dev/null
        sleep 1
        if kill -0 $pid 2>/dev/null; then
            kill -KILL $pid 2>/dev/null
        fi
        echo -e "${GREEN}[成功] 已停止进程 $pid${NC}"
    done
fi

# 验证端口是否已释放
sleep 1
if ! lsof -t -i:8001 >/dev/null 2>&1; then
    echo -e "${GREEN}[信息] 端口8001已释放${NC}"
else
    echo -e "${YELLOW}[警告] 端口8001可能仍被占用${NC}"
fi

echo
echo -e "${GREEN}[完成] 图片相似度搜索工具已关闭${NC}"
echo -e "${GREEN}===============================================${NC}"
sleep 2
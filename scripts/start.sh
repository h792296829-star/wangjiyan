#!/bin/bash

# 快速启动脚本（适用于测试环境）

PROJECT_DIR="/opt/civil-service-assistant"
cd $PROJECT_DIR

# 设置环境变量
export COZE_WORKSPACE_PATH=$PROJECT_DIR

# 启动服务
echo "启动公务员培训助手服务..."
python3 src/main.py

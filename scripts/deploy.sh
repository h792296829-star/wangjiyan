#!/bin/bash

# 公务员培训助手 - 云部署脚本
# 使用方法：bash scripts/deploy.sh

set -e

echo "=========================================="
echo "  公务员培训助手 - 云端部署脚本"
echo "=========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查是否为 root 用户
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}请使用 root 用户或 sudo 运行此脚本${NC}"
    exit 1
fi

# 检测操作系统
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
    VERSION=$VERSION_ID
else
    echo -e "${RED}无法检测操作系统版本${NC}"
    exit 1
fi

echo -e "${GREEN}检测到操作系统：${OS} ${VERSION}${NC}"
echo ""

# 1. 安装系统依赖
echo "=========================================="
echo "步骤 1/7: 安装系统依赖"
echo "=========================================="

if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
    apt-get update
    apt-get install -y python3 python3-pip python3-venv git nginx supervisor
elif [ "$OS" = "centos" ] || [ "$OS" = "rhel" ]; then
    yum update -y
    yum install -y python3 python3-pip git nginx supervisor
else
    echo -e "${YELLOW}未知的操作系统，请手动安装依赖${NC}"
    echo "需要安装：python3, python3-pip, git, nginx, supervisor"
fi

echo -e "${GREEN}✓ 系统依赖安装完成${NC}"
echo ""

# 2. 创建项目目录
echo "=========================================="
echo "步骤 2/7: 创建项目目录"
echo "=========================================="

PROJECT_DIR="/opt/civil-service-assistant"
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

echo -e "${GREEN}✓ 项目目录创建完成：${PROJECT_DIR}${NC}"
echo ""

# 3. 上传代码（这里假设代码已经存在）
echo "=========================================="
echo "步骤 3/7: 准备代码"
echo "=========================================="

if [ ! -d "src" ]; then
    echo -e "${YELLOW}请先将项目代码上传到：${PROJECT_DIR}${NC}"
    echo "可以使用以下命令："
    echo "  scp -r /workspace/projects/* root@your-server-ip:${PROJECT_DIR}/"
    exit 1
fi

echo -e "${GREEN}✓ 代码已准备${NC}"
echo ""

# 4. 安装 Python 依赖
echo "=========================================="
echo "步骤 4/7: 安装 Python 依赖"
echo "=========================================="

if [ -f "requirements.txt" ]; then
    pip3 install --upgrade pip
    pip3 install -r requirements.txt
    echo -e "${GREEN}✓ Python 依赖安装完成${NC}"
else
    echo -e "${RED}未找到 requirements.txt 文件${NC}"
    exit 1
fi

echo ""

# 5. 配置 Nginx
echo "=========================================="
echo "步骤 5/7: 配置 Nginx"
echo "=========================================="

NGINX_CONF="/etc/nginx/sites-available/civil-service-assistant"
cat > $NGINX_CONF << 'EOF'
server {
    listen 80;
    server_name _;

    client_max_body_size 10M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;

        # 超时设置
        proxy_connect_timeout 900;
        proxy_send_timeout 900;
        proxy_read_timeout 900;
    }

    location /static {
        alias /opt/civil-service-assistant/assets;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# 创建软链接
if [ -d "/etc/nginx/sites-enabled" ]; then
    ln -sf $NGINX_CONF /etc/nginx/sites-enabled/
fi

# 删除默认配置（可选）
if [ -f "/etc/nginx/sites-enabled/default" ]; then
    rm /etc/nginx/sites-enabled/default
fi

# 测试 Nginx 配置
nginx -t

echo -e "${GREEN}✓ Nginx 配置完成${NC}"
echo ""

# 6. 配置 Supervisor（进程守护）
echo "=========================================="
echo "步骤 6/7: 配置 Supervisor"
echo "=========================================="

SUPERVISOR_CONF="/etc/supervisor/conf.d/civil-service-assistant.conf"
cat > $SUPERVISOR_CONF << 'EOF'
[program:civil-service-assistant]
command=/usr/bin/python3 /opt/civil-service-assistant/src/main.py
directory=/opt/civil-service-assistant
user=root
autostart=true
autorestart=true
startretries=3
stderr_logfile=/var/log/civil-service-assistant.err.log
stdout_logfile=/var/log/civil-service-assistant.out.log
environment=COZE_WORKSPACE_PATH="/opt/civil-service-assistant"
EOF

echo -e "${GREEN}✓ Supervisor 配置完成${NC}"
echo ""

# 7. 启动服务
echo "=========================================="
echo "步骤 7/7: 启动服务"
echo "=========================================="

# 重启 Supervisor
supervisorctl reread
supervisorctl update
supervisorctl start civil-service-assistant

# 重启 Nginx
systemctl restart nginx

# 设置开机自启
systemctl enable nginx
systemctl enable supervisor

echo ""
echo "=========================================="
echo -e "${GREEN}🎉 部署完成！${NC}"
echo "=========================================="
echo ""
echo "服务信息："
echo "  项目目录：${PROJECT_DIR}"
echo "  访问地址：http://YOUR_SERVER_IP"
echo ""
echo "管理命令："
echo "  查看服务状态：supervisorctl status civil-service-assistant"
echo "  重启服务：supervisorctl restart civil-service-assistant"
echo "  停止服务：supervisorctl stop civil-service-assistant"
echo "  查看日志：tail -f /var/log/civil-service-assistant.out.log"
echo ""
echo "下一步："
echo "  1. 配置域名和 SSL 证书（推荐）"
echo "  2. 设置防火墙规则："
echo "     sudo ufw allow 80"
echo "     sudo ufw allow 443"
echo "  3. 配置云服务器安全组开放 80 和 443 端口"
echo ""

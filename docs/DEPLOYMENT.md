# 公务员培训助手 - 云端部署指南

## 部署方式

本指南提供两种部署方式：
1. **自动化部署脚本**（推荐，快速简单）
2. **手动部署**（适合需要自定义配置）

---

## 方式一：自动化部署脚本（推荐）

### 1. 购买云服务器

推荐的云服务商：
- 阿里云：https://www.aliyun.com/
- 腾讯云：https://cloud.tencent.com/
- 华为云：https://www.huaweicloud.com/

**配置建议：**
- CPU：1核或2核
- 内存：2GB 或 4GB
- 带宽：1Mbps 或以上
- 系统：Ubuntu 20.04 LTS 或 CentOS 7.x
- 磁盘：40GB 或以上

### 2. 连接服务器

```bash
ssh root@your_server_ip
```

### 3. 上传代码

在本地机器上执行：

```bash
# 方法 1: 使用 scp
scp -r /workspace/projects/* root@your_server_ip:/opt/civil-service-assistant/

# 方法 2: 使用 rsync
rsync -avz /workspace/projects/ root@your_server_ip:/opt/civil-service-assistant/

# 方法 3: 先打包再上传
cd /workspace/projects
tar -czf civil-service-assistant.tar.gz .
scp civil-service-assistant.tar.gz root@your_server_ip:/tmp/
# 在服务器上解压
ssh root@your_server_ip
mkdir -p /opt/civil-service-assistant
cd /opt/civil-service-assistant
tar -xzf /tmp/civil-service-assistant.tar.gz
```

### 4. 上传并运行部署脚本

```bash
# 上传脚本
scp scripts/deploy.sh root@your_server_ip:/tmp/

# 在服务器上执行
ssh root@your_server_ip
chmod +x /tmp/deploy.sh
sudo /tmp/deploy.sh
```

### 5. 配置安全组

在云服务器控制台配置安全组规则：
- 开放 80 端口（HTTP）
- 开放 443 端口（HTTPS）
- 开放 22 端口（SSH，如果需要远程管理）

### 6. 访问服务

在浏览器中访问：
```
http://your_server_ip
```

---

## 方式二：手动部署

### 1. 安装系统依赖

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv git nginx supervisor
```

**CentOS/RHEL:**
```bash
sudo yum update -y
sudo yum install -y python3 python3-pip git nginx supervisor
```

### 2. 创建项目目录

```bash
sudo mkdir -p /opt/civil-service-assistant
sudo chown -R $USER:$USER /opt/civil-service-assistant
cd /opt/civil-service-assistant
```

### 3. 上传代码

```bash
# 从本地上传代码到服务器
scp -r /workspace/projects/* root@your_server_ip:/opt/civil-service-assistant/
```

### 4. 安装 Python 依赖

```bash
cd /opt/civil-service-assistant
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

### 5. 配置 Nginx

创建 Nginx 配置文件：

```bash
sudo nano /etc/nginx/sites-available/civil-service-assistant
```

粘贴以下内容：

```nginx
server {
    listen 80;
    server_name your_domain.com;  # 替换为你的域名或 IP

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
```

启用配置：

```bash
sudo ln -sf /etc/nginx/sites-available/civil-service-assistant /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6. 配置 Supervisor

创建 Supervisor 配置文件：

```bash
sudo nano /etc/supervisor/conf.d/civil-service-assistant.conf
```

粘贴以下内容：

```ini
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
```

启动服务：

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start civil-service-assistant
```

### 7. 配置防火墙

**Ubuntu (ufw):**
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp
sudo ufw enable
```

**CentOS (firewalld):**
```bash
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --reload
```

---

## 配置域名和 SSL 证书（可选但推荐）

### 1. 购买域名

在阿里云、腾讯云等平台购买域名。

### 2. 配置 DNS 解析

添加 A 记录，指向你的服务器 IP：
```
类型：A
主机记录：@
记录值：your_server_ip
TTL：600
```

### 3. 安装 SSL 证书

使用 Let's Encrypt 免费证书：

```bash
# 安装 certbot
sudo apt-get install certbot python3-certbot-nginx  # Ubuntu/Debian
sudo yum install certbot python3-certbot-nginx      # CentOS/RHEL

# 获取证书
sudo certbot --nginx -d your_domain.com

# 自动续期
sudo certbot renew --dry-run
```

Certbot 会自动修改 Nginx 配置，启用 HTTPS。

---

## 服务管理命令

### Supervisor 管理命令

```bash
# 查看状态
sudo supervisorctl status civil-service-assistant

# 启动服务
sudo supervisorctl start civil-service-assistant

# 停止服务
sudo supervisorctl stop civil-service-assistant

# 重启服务
sudo supervisorctl restart civil-service-assistant

# 查看日志
sudo tail -f /var/log/civil-service-assistant.out.log
sudo tail -f /var/log/civil-service-assistant.err.log

# 更新配置
sudo supervisorctl reread
sudo supervisorctl update
```

### Nginx 管理命令

```bash
# 测试配置
sudo nginx -t

# 重启 Nginx
sudo systemctl restart nginx

# 重载配置
sudo systemctl reload nginx

# 查看状态
sudo systemctl status nginx
```

---

## 常见问题

### 1. 服务无法启动

检查日志：
```bash
sudo tail -f /var/log/civil-service-assistant.out.log
```

常见原因：
- Python 依赖未安装：运行 `pip3 install -r requirements.txt`
- 端口被占用：`sudo lsof -i :5000`
- 权限问题：确保文件权限正确

### 2. 无法访问网站

检查清单：
- [ ] 防火墙是否开放 80 和 443 端口
- [ ] 云服务器安全组是否配置正确
- [ ] Nginx 是否正常运行：`sudo systemctl status nginx`
- [ ] 域名解析是否正确
- [ ] SSL 证书是否过期

### 3. 更新代码

更新代码后，重启服务：

```bash
cd /opt/civil-service-assistant
git pull  # 如果使用 git
# 或上传新文件后
sudo supervisorctl restart civil-service-assistant
```

---

## 性能优化

### 1. 配置 Gunicorn（生产环境推荐）

安装 Gunicorn：
```bash
pip3 install gunicorn
```

修改 Supervisor 配置：

```ini
[program:civil-service-assistant]
command=/usr/local/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
directory=/opt/civil-service-assistant/src
user=root
autostart=true
autorestart=true
startretries=3
stderr_logfile=/var/log/civil-service-assistant.err.log
stdout_logfile=/var/log/civil-service-assistant.out.log
environment=COZE_WORKSPACE_PATH="/opt/civil-service-assistant"
```

### 2. 配置 Redis（缓存）

如果需要缓存功能，可以安装 Redis：

```bash
sudo apt-get install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

### 3. 配置日志轮转

创建日志轮转配置：

```bash
sudo nano /etc/logrotate.d/civil-service-assistant
```

内容：

```
/var/log/civil-service-assistant/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0640 root root
    sharedscripts
    postrotate
        sudo supervisorctl restart civil-service-assistant
    endscript
}
```

---

## 安全建议

1. **定期更新系统**
   ```bash
   sudo apt-get update && sudo apt-get upgrade
   ```

2. **配置 fail2ban（防止暴力破解）**
   ```bash
   sudo apt-get install fail2ban
   sudo systemctl enable fail2ban
   sudo systemctl start fail2ban
   ```

3. **禁用 root 登录**
   ```bash
   sudo nano /etc/ssh/sshd_config
   # 设置 PermitRootLogin no
   sudo systemctl restart sshd
   ```

4. **定期备份数据**
   ```bash
   # 创建备份脚本
   sudo nano /usr/local/bin/backup.sh
   ```

---

## 成本估算

**阿里云/腾讯云（月付）：**
- 1核2GB：约 ¥30-50/月
- 2核4GB：约 ¥100-150/月
- 带宽：1Mbps 约 ¥20-30/月
- 域名：约 ¥50-100/年

**年付通常有折扣（5-7折）**

---

## 技术支持

如有问题，请检查：
1. 系统日志：`/var/log/`
2. 应用日志：`/var/log/civil-service-assistant/`
3. Nginx 日志：`/var/log/nginx/`

---

**祝部署顺利！** 🎉

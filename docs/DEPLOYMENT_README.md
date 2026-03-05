# 📦 云部署完整指南

## 📋 目录

- [快速开始](#快速开始)
- [准备工作](#准备工作)
- [部署方式](#部署方式)
- [域名配置](#域名配置)
- [服务管理](#服务管理)
- [故障排查](#故障排查)

---

## 🚀 快速开始

### 最简单的部署方式（5分钟）

```bash
# 1. 打包项目（本地执行）
cd /workspace/projects
bash scripts/package.sh

# 2. 上传到服务器
scp civil-service-assistant.tar.gz root@your_server_ip:/tmp/

# 3. 在服务器上解压并部署
ssh root@your_server_ip
mkdir -p /opt/civil-service-assistant
cd /opt/civil-service-assistant
tar -xzf /tmp/civil-service-assistant.tar.gz

# 4. 运行自动部署脚本
chmod +x scripts/deploy.sh
sudo bash scripts/deploy.sh

# 5. 访问服务
# 在浏览器打开：http://your_server_ip
```

---

## 📦 准备工作

### 1. 购买云服务器

推荐平台：
- **阿里云**：https://www.aliyun.com/
- **腾讯云**：https://cloud.tencent.com/
- **华为云**：https://www.huaweicloud.com/

**最低配置：**
- CPU：1核
- 内存：2GB
- 带宽：1Mbps
- 系统：Ubuntu 20.04 LTS
- 磁盘：40GB

**月费参考：** ¥30-50/月

### 2. 获取服务器信息

- 服务器公网 IP 地址
- SSH 登录密码或密钥
- 服务器登录用户名（通常是 root）

### 3. 本地环境准备

确保本地有：
- ✅ SSH 客户端（Linux/Mac 自带，Windows 可用 PuTTY）
- ✅ scp 命令（用于上传文件）

---

## 🎯 部署方式

### 方式一：自动化部署脚本（推荐）

**优势：**
- ✅ 自动安装所有依赖
- ✅ 自动配置 Nginx
- ✅ 自动配置进程守护
- ✅ 一键完成部署

**步骤：**

1. **打包项目**
```bash
bash scripts/package.sh
```

2. **上传到服务器**
```bash
scp civil-service-assistant.tar.gz root@your_server_ip:/tmp/
```

3. **在服务器上部署**
```bash
ssh root@your_server_ip
mkdir -p /opt/civil-service-assistant
cd /opt/civil-service-assistant
tar -xzf /tmp/civil-service-assistant.tar.gz
chmod +x scripts/deploy.sh
sudo bash scripts/deploy.sh
```

4. **验证部署**
```bash
# 检查服务状态
sudo supervisorctl status civil-service-assistant

# 访问网站
curl http://localhost
```

### 方式二：手动部署

**适用场景：**
- 需要自定义配置
- 部署到特殊环境
- 学习部署流程

**详细步骤：** 查看 [完整部署文档](DEPLOYMENT.md)

---

## 🌐 域名配置（可选但推荐）

### 1. 购买域名

在阿里云/腾讯云购买域名（约 ¥50-100/年）

### 2. 配置 DNS 解析

添加 A 记录：
```
类型：A
主机记录：@
记录值：你的服务器IP
TTL：600
```

### 3. 配置 SSL 证书

```bash
# 安装 certbot
sudo apt-get install certbot python3-certbot-nginx

# 获取证书（自动配置 HTTPS）
sudo certbot --nginx -d 你的域名.com
```

### 4. 访问服务

现在可以通过以下方式访问：
- HTTP：`http://你的域名.com`
- HTTPS：`https://你的域名.com`（自动跳转）

---

## 🛠️ 服务管理

### 常用管理命令

```bash
# 查看服务状态
sudo supervisorctl status civil-service-assistant

# 启动服务
sudo supervisorctl start civil-service-assistant

# 停止服务
sudo supervisorctl stop civil-service-assistant

# 重启服务
sudo supervisorctl restart civil-service-assistant

# 查看日志
tail -f /var/log/civil-service-assistant.out.log
tail -f /var/log/civil-service-assistant.err.log

# 重启 Nginx
sudo systemctl restart nginx

# 查看所有服务状态
sudo supervisorctl status
```

### 更新代码

```bash
cd /opt/civil-service-assistant

# 上传新代码后
sudo supervisorctl restart civil-service-assistant
```

---

## 🔧 故障排查

### 问题 1：服务无法启动

**检查日志：**
```bash
tail -f /var/log/civil-service-assistant.out.log
tail -f /var/log/civil-service-assistant.err.log
```

**常见原因：**
1. 端口被占用
   ```bash
   sudo lsof -i :5000
   sudo kill -9 <PID>
   ```

2. Python 依赖未安装
   ```bash
   cd /opt/civil-service-assistant
   pip3 install -r requirements.txt
   ```

3. 权限问题
   ```bash
   sudo chown -R root:root /opt/civil-service-assistant
   ```

### 问题 2：无法访问网站

**检查清单：**

```bash
# 1. 检查服务是否运行
sudo supervisorctl status civil-service-assistant

# 2. 检查 Nginx 是否运行
sudo systemctl status nginx

# 3. 检查端口是否监听
sudo netstat -tlnp | grep :80

# 4. 检查防火墙
sudo ufw status

# 5. 检查 Nginx 配置
sudo nginx -t

# 6. 查看 Nginx 日志
tail -f /var/log/nginx/error.log
```

### 问题 3：SSL 证书问题

```bash
# 查看证书状态
sudo certbot certificates

# 手动续期
sudo certbot renew

# 强制续期
sudo certbot renew --force-renewal
```

---

## 📊 监控和日志

### 查看实时日志

```bash
# 应用日志
sudo tail -f /var/log/civil-service-assistant.out.log

# 错误日志
sudo tail -f /var/log/civil-service-assistant.err.log

# Nginx 访问日志
sudo tail -f /var/log/nginx/access.log

# Nginx 错误日志
sudo tail -f /var/log/nginx/error.log
```

### 配置日志轮转

```bash
# 查看轮转配置
cat /etc/logrotate.d/civil-service-assistant

# 手动测试轮转
sudo logrotate -f /etc/logrotate.d/civil-service-assistant
```

---

## 🔒 安全建议

### 1. 配置防火墙

```bash
# 开放必要端口
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS

# 启用防火墙
sudo ufw enable

# 查看状态
sudo ufw status
```

### 2. 安装 fail2ban（防止暴力破解）

```bash
sudo apt-get install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 3. 定期更新

```bash
# 更新系统
sudo apt-get update
sudo apt-get upgrade

# 更新 Python 依赖
cd /opt/civil-service-assistant
pip3 install --upgrade -r requirements.txt
```

---

## 📈 性能优化

### 使用 Gunicorn（生产环境）

```bash
# 安装 Gunicorn
pip3 install gunicorn

# 修改 Supervisor 配置使用 Gunicorn
# 编辑：/etc/supervisor/conf.d/civil-service-assistant.conf
# command=/usr/local/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### 配置 Redis 缓存

```bash
# 安装 Redis
sudo apt-get install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

---

## 💰 成本参考

### 云服务器费用（月付）

| 配置 | 阿里云 | 腾讯云 | 华为云 |
|------|--------|--------|--------|
| 1核2GB | ¥30-50 | ¥30-40 | ¥35-45 |
| 2核4GB | ¥100-150 | ¥80-120 | ¥90-130 |
| 4核8GB | ¥250-350 | ¥200-280 | ¥220-300 |

**年付通常有 5-7 折优惠**

### 域名费用

- .com：约 ¥50-100/年
- .cn：约 ¥30-50/年
- .net：约 ¥60-80/年

### SSL 证书

- Let's Encrypt：**免费**
- 其他商业证书：¥500-5000/年

---

## 📚 相关文档

- [完整部署指南](DEPLOYMENT.md) - 详细的部署步骤和配置说明
- [快速开始](QUICK_START.md) - 5分钟快速部署
- [README.md](../README.md) - 项目介绍和使用说明

---

## 🆘 技术支持

### 日志位置

- 应用日志：`/var/log/civil-service-assistant.out.log`
- 错误日志：`/var/log/civil-service-assistant.err.log`
- Nginx 日志：`/var/log/nginx/`

### 常用目录

- 项目目录：`/opt/civil-service-assistant`
- 配置文件：`/etc/nginx/sites-available/`
- Supervisor 配置：`/etc/supervisor/conf.d/`

---

**祝你部署顺利！** 🎉

如有问题，请检查日志文件或查看详细文档。

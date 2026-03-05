# 快速部署指南（5分钟上手）

## 最简部署步骤

### 第一步：购买服务器（3分钟）

推荐选择：
- 阿里云：https://www.aliyun.com/
- 腾讯云：https://cloud.tencent.com/

**选型建议：**
- 系统：Ubuntu 20.04 LTS
- 配置：1核2GB（够用）
- 带宽：1Mbps

**费用：** 约 ¥30-50/月

### 第二步：连接服务器（1分钟）

```bash
ssh root@你的服务器IP
```

### 第三步：上传代码并部署（2分钟）

**在本地机器上执行：**

```bash
# 1. 打包项目
cd /workspace/projects
tar -czf assistant.tar.gz .

# 2. 上传到服务器
scp assistant.tar.gz root@你的服务器IP:/tmp/
```

**在服务器上执行：**

```bash
# 1. 解压
mkdir -p /opt/civil-service-assistant
cd /opt/civil-service-assistant
tar -xzf /tmp/assistant.tar.gz

# 2. 安装依赖
apt-get update
apt-get install -y python3 python3-pip nginx
pip3 install -r requirements.txt

# 3. 安装并启动服务
pip3 install supervisor
# 复制 supervisor 配置文件
cp /opt/civil-service-assistant/scripts/deploy.sh /tmp/
chmod +x /tmp/deploy.sh
/tmp/deploy.sh
```

### 第四步：访问服务

在浏览器打开：`http://你的服务器IP`

完成！🎉

---

## 配置域名（可选）

### 1. 购买域名

在阿里云/腾讯云购买域名（约 ¥50-100/年）

### 2. 解析域名

在域名管理中添加 A 记录：
- 主机记录：@
- 记录值：你的服务器IP

### 3. 配置 SSL 证书

```bash
# 安装 certbot
apt-get install certbot python3-certbot-nginx

# 获取证书（自动配置）
certbot --nginx -d 你的域名.com
```

现在可以通过 HTTPS 访问了：`https://你的域名.com`

---

## 常用命令

```bash
# 查看服务状态
supervisorctl status civil-service-assistant

# 重启服务
supervisorctl restart civil-service-assistant

# 查看日志
tail -f /var/log/civil-service-assistant.out.log

# 重启 Nginx
systemctl restart nginx
```

---

## 故障排查

**问题：无法访问网站**

```bash
# 检查服务状态
supervisorctl status civil-service-assistant

# 检查 Nginx 状态
systemctl status nginx

# 检查防火墙
ufw status

# 查看日志
tail -f /var/log/civil-service-assistant.out.log
```

**问题：端口被占用**

```bash
# 查看占用端口的进程
lsof -i :5000

# 结束进程
kill -9 进程ID
```

---

## 进阶配置

详细配置请查看：[完整部署指南](DEPLOYMENT.md)

---

## 成本参考

| 配置 | 月付（¥） | 年付（¥） |
|------|----------|----------|
| 1核2GB | 30-50 | 300-400 |
| 2核4GB | 100-150 | 800-1200 |
| 域名 | 10/月 | 50-100/年 |

**建议：** 先用1核2GB测试，不够再升级

---

## 技术支持

- 完整文档：查看 `docs/DEPLOYMENT.md`
- 部署脚本：查看 `scripts/deploy.sh`

需要帮助？查看日志文件：
- 应用日志：`/var/log/civil-service-assistant.out.log`
- 错误日志：`/var/log/civil-service-assistant.err.log`

---

**祝你部署顺利！** 🚀

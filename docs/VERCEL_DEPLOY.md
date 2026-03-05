# 🚀 Vercel 快速部署指南（最简单！）

## 方案对比

| 部署方式 | 难度 | 时间 | 费用 | 适用场景 |
|---------|------|------|------|---------|
| **Vercel** | ⭐ 极简 | 2分钟 | 免费 | 快速分享、测试 |
| 云服务器 | ⭐⭐⭐ 复杂 | 30分钟 | ¥30+/月 | 生产环境、长期使用 |

---

## Vercel 部署步骤（2分钟搞定）

### 第一步：准备 GitHub 仓库

1. 登录 GitHub
2. 创建新仓库（如果还没有）
3. 推送代码到仓库

```bash
cd /workspace/projects
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/your-username/civil-service-assistant.git
git push -u origin main
```

### 第二步：部署到 Vercel

1. **登录 Vercel**
   - 访问：https://vercel.com/
   - 使用 GitHub 账号登录

2. **创建新项目**
   - 点击 "Add New..." → "Project"
   - 选择你的 GitHub 仓库
   - 点击 "Import"

3. **配置项目**
   - **Framework Preset**：选择 "Other"
   - **Root Directory**：留空
   - **Build Command**：留空
   - **Output Directory**：留空
   - 点击 "Deploy"

4. **等待部署完成**
   - 大约需要 1-2 分钟
   - 部署成功后会显示访问链接

### 第三步：访问你的应用

部署完成后，你会得到一个类似这样的链接：
```
https://civil-service-assistant-xyz.vercel.app
```

直接在浏览器中打开即可！

---

## 🎉 完成！

就这么简单！现在你可以：
- ✅ 分享链接给别人使用
- ✅ 自动 HTTPS 加密
- ✅ 全球 CDN 加速
- ✅ 免费使用（有限额）

---

## 配置自定义域名（可选）

### 1. 在 Vercel 中添加域名

1. 进入项目设置 → Domains
2. 点击 "Add Domain"
3. 输入你的域名（如：`assistant.yourdomain.com`）
4. 点击 "Add"

### 2. 配置 DNS

在域名服务商处添加 CNAME 记录：
```
类型：CNAME
主机记录：assistant
记录值：cname.vercel-dns.com
TTL：600
```

### 3. 完成

等待几分钟，Vercel 会自动配置 SSL 证书。

---

## 费用说明

### Vercel 免费版

- ✅ 无限项目
- ✅ 100GB 带宽/月
- ✅ 自动 HTTPS
- ✅ 全球 CDN
- ✅ 无限部署
- ⚠️ Serverless 函数限制：
  - 免费版：1000 次调用/天
  - 100 秒执行时间/天

### 超出限额怎么办？

对于这个项目，1000 次调用/天通常足够：
- 如果个人使用：✅ 完全够用
- 如果团队使用（10人以下）：✅ 基本够用
- 如果需要更多：升级到 Pro 版（$20/月）

---

## 常见问题

### Q1: 部署失败怎么办？

**解决方案：**

1. 检查 `vercel.json` 文件是否存在
2. 检查 `api/index.py` 文件是否存在
3. 查看部署日志（Vercel 会显示错误信息）
4. 确保 `requirements.txt` 在根目录

### Q2: 访问页面空白？

**检查清单：**

- [ ] 等待部署完全完成
- [ ] 刷新浏览器
- [ ] 检查浏览器控制台是否有错误
- [ ] 查看 Vercel 部署日志

### Q3: API 调用失败？

**可能原因：**

1. 超时：Vercel Serverless 函数有 10 秒执行限制
2. 内存不足：免费版限制 1024MB
3. 依赖缺失：检查 `requirements.txt`

### Q4: 如何查看日志？

在 Vercel 中：
1. 进入项目
2. 点击 "Functions" 标签
3. 选择 `api/index`
4. 查看实时日志

---

## 更新部署

修改代码后：

```bash
# 提交到 GitHub
git add .
git commit -m "Update"
git push
```

Vercel 会自动检测并重新部署！

---

## 技术细节

### 项目结构

```
.
├── api/
│   └── index.py          # Serverless 函数入口
├── assets/
│   └── index.html         # 前端页面
├── src/
│   └── agents/            # Agent 代码
├── config/                # 配置文件
├── requirements.txt       # Python 依赖
└── vercel.json            # Vercel 配置
```

### 工作原理

1. **用户访问** → 返回 `index.html`
2. **发送消息** → 调用 `/stream_run` API
3. **Serverless 函数** → 运行 Agent
4. **返回结果** → 显示在页面

---

## 对比其他部署方式

| 特性 | Vercel | 云服务器 | Heroku |
|------|--------|---------|--------|
| 部署难度 | ⭐ | ⭐⭐⭐ | ⭐⭐ |
| 费用 | 免费 | ¥30+/月 | 免费（有限额） |
| 性能 | 中等 | 高 | 中等 |
| 灵活性 | 低 | 高 | 中等 |
| 推荐场景 | 快速分享 | 生产环境 | 快速部署 |

---

## 推荐方案总结

**如果你想要：**

🚀 **最快部署** → 使用 Vercel（本文档）
💰 **零成本** → 使用 Vercel 免费版
🌐 **分享链接** → 使用 Vercel
🏢 **长期稳定** → 使用云服务器
🔧 **完全控制** → 使用云服务器

---

**提示：** 可以先用 Vercel 快速测试，确定需要后再考虑迁移到云服务器。

---

## 技术支持

- Vercel 文档：https://vercel.com/docs
- 部署日志：Vercel 控制台
- 问题反馈：查看 Vercel 部署日志

---

**祝你部署成功！** 🎉

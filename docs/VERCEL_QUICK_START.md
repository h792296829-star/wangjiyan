# 🚀 Vercel 部署 - 2分钟搞定

## 最简单的方法（推荐）

### 1️⃣ 准备 GitHub 仓库

```bash
git init
git add .
git commit -m "Init"
git branch -M main
git remote add origin https://github.com/你的用户名/civil-service-assistant.git
git push -u origin main
```

### 2️⃣ 部署到 Vercel

1. 访问 https://vercel.com/
2. 用 GitHub 登录
3. 点击 "Add New..." → "Project"
4. 选择你的仓库
5. 点击 "Import"
6. 点击 "Deploy"

### 3️⃣ 完成！🎉

等待 1-2 分钟，你会得到一个链接：
```
https://civil-service-assistant-xxx.vercel.app
```

直接打开就能用了！

---

## 📋 部署前检查清单

在部署前，确保以下文件存在：

- [x] `vercel.json` - Vercel 配置文件
- [x] `api/index.py` - API 入口
- [x] `assets/index.html` - 前端页面
- [x] `requirements.txt` - Python 依赖
- [x] `src/agents/agent.py` - Agent 代码
- [x] `config/agent_llm_config.json` - 配置文件

---

## ❓ 遇到问题？

### 问题：部署失败

**解决：**
1. 检查文件是否都存在
2. 查看部署日志
3. 确保代码已推送到 GitHub

### 问题：页面空白

**解决：**
1. 刷新浏览器
2. 清除缓存
3. 查看 F12 控制台错误

### 问题：API 调用失败

**解决：**
1. 检查 Vercel 日志
2. 确认依赖完整
3. 检查超时限制

---

## 💰 费用

✅ **免费版**
- 1000 次调用/天
- 100 秒执行时间/天
- 无限项目
- 自动 HTTPS

⚠️ **升级**
- 超出限额需升级到 Pro（$20/月）

---

## 🔄 更新部署

修改代码后：

```bash
git add .
git commit -m "Update"
git push
```

Vercel 会自动重新部署！

---

**就这么简单！** 🎉

需要详细说明？查看 [完整 Vercel 部署指南](VERCEL_DEPLOY.md)

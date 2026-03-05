# 上传代码到 GitHub 指南

## 方法一：使用 GitHub Desktop（最简单）

### 步骤：

1. **下载 GitHub Desktop**
   - 访问：https://desktop.github.com/
   - 下载并安装

2. **克隆你的仓库**
   - 打开 GitHub Desktop
   - 点击 **"File"** → **"Clone Repository"**
   - 输入仓库地址：`https://github.com/h792296829-star/agent`
   - 选择保存位置，点击 **"Clone"**

3. **复制项目文件**
   - 打开克隆下来的文件夹
   - 删除里面的所有文件（如果有）
   - 把 `/workspace/projects` 里的所有文件复制过去
   - 特别注意要复制：
     - `api/` 文件夹
     - `assets/` 文件夹
     - `src/` 文件夹
     - `config/` 文件夹
     - `docs/` 文件夹
     - `scripts/` 文件夹
     - `vercel.json`
     - `requirements.txt`
     - `README.md`
     - `.gitignore`

4. **提交和推送**
   - 回到 GitHub Desktop
   - 在左下角输入提交信息：`Initial commit`
   - 点击 **"Commit to main"**
   - 点击 **"Push origin"**

5. **完成！** 🎉
   - 访问：https://github.com/h792296829-star/agent
   - 查看代码是否上传成功

---

## 方法二：使用 GitHub 网页上传

### 步骤：

1. **下载项目文件**
   - 在服务器上执行：
   ```bash
   cd /workspace/projects
   tar -czf project.tar.gz api assets src config docs scripts vercel.json requirements.txt README.md .gitignore
   ```

2. **上传到 GitHub 网页**
   - 访问：https://github.com/h792296829-star/agent
   - 点击 **"uploading an existing file"**（或 "Add file" → "Upload files"）
   - 把 `project.tar.gz` 拖进去
   - 等待上传完成
   - 在提交信息里写：`Initial commit`
   - 点击 **"Commit changes"**

3. **注意**：网页上传单个文件最大 25MB，如果压缩包太大，建议用方法一。

---

## 方法三：配置 Personal Access Token

### 步骤：

1. **创建 Token**
   - 访问：https://github.com/settings/tokens
   - 点击 **"Generate new token"** → **"Generate new token (classic)"**
   - 勾选：**repo**
   - 点击 **"Generate token"**
   - 复制 token（类似：`ghp_xxxxxxxxxxxxxxxxxxxx`）

2. **在本地电脑执行**
   ```bash
   # 替换 YOUR_TOKEN 为你的实际 token
   git clone https://YOUR_TOKEN@github.com/h792296829-star/agent.git
   cd agent

   # 复制所有项目文件到这个文件夹

   git add .
   git commit -m "Initial commit"
   git push
   ```

---

## 推荐方法

🌟 **最推荐：方法一（GitHub Desktop）**
- 不需要任何技术背景
- 图形化操作，简单直观
- 不需要配置 token 或 SSH

⚡ **如果你有技术背景：方法三**
- 使用命令行
- 配置一次后永久使用

---

## 验证上传成功

上传完成后，访问：
```
https://github.com/h792296829-star/agent
```

你应该能看到：
- ✅ `api/` 文件夹
- ✅ `assets/` 文件夹
- ✅ `src/` 文件夹
- ✅ `config/` 文件夹
- ✅ `docs/` 文件夹
- ✅ `scripts/` 文件夹
- ✅ `vercel.json`
- ✅ `requirements.txt`
- ✅ `README.md`

---

**选择一个方法，开始上传吧！** 🚀

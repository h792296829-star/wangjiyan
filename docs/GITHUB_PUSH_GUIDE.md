# 📤 GitHub 代码推送指南

## 问题描述

当前项目已经配置了 GitHub 远程仓库，但推送时遇到认证错误：

```
fatal: could not read Password for 'https://YOUR_TOKEN@github.com': No such device or address
```

这是因为远程 URL 中使用了占位符 `YOUR_TOKEN`，需要替换为实际的 GitHub Personal Access Token。

---

## 解决方案

### 方案一：使用 Personal Access Token（推荐）

#### 1. 创建 Personal Access Token

1. 登录 GitHub
2. 点击右上角头像 → **Settings**
3. 左侧菜单找到 **Developer settings**
4. 点击 **Personal access tokens** → **Tokens (classic)**
5. 点击 **Generate new token** → **Generate new token (classic)**
6. 填写信息：
   - **Note**: civil-service-assistant（或任意描述）
   - **Expiration**: 选择有效期（建议 90 days 或 No expiration）
   - **Scopes**: 勾选 `repo`（Full control of private repositories）
7. 点击 **Generate token**
8. **重要**：复制生成的 token（只显示一次！）

#### 2. 更新远程仓库 URL

**方法 A：直接更新 URL（推荐）**

```bash
cd /workspace/projects
git remote set-url origin https://YOUR_TOKEN@github.com/h792296829-star/agent.git
```

将 `YOUR_TOKEN` 替换为你刚才复制的 token。

**示例：**

```bash
git remote set-url origin https://ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx@github.com/h792296829-star/agent.git
```

**方法 B：使用 git credential helper**

```bash
cd /workspace/projects
# 移除 token，让 git 询问密码
git remote set-url origin https://github.com/h792296829-star/agent.git

# 配置 credential helper
git config --global credential.helper store

# 推送时会要求输入用户名和密码
# 用户名：你的 GitHub 用户名
# 密码：刚才生成的 Personal Access Token
git push -u origin main
```

#### 3. 推送代码

```bash
cd /workspace/projects
git push origin main
```

---

### 方案二：使用 SSH Key（更安全）

#### 1. 生成 SSH Key

```bash
# 检查是否已有 SSH key
ls -al ~/.ssh

# 如果没有，生成新的
ssh-keygen -t ed25519 -C "your_email@example.com"

# 查看公钥
cat ~/.ssh/id_ed25519.pub
```

#### 2. 添加 SSH Key 到 GitHub

1. 复制公钥内容
2. GitHub → Settings → SSH and GPG keys
3. 点击 **New SSH key**
4. 粘贴公钥内容
5. 点击 **Add SSH key**

#### 3. 更新远程仓库 URL

```bash
cd /workspace/projects
git remote set-url origin git@github.com:h792296829-star/agent.git
git push origin main
```

---

### 方案三：使用 GitHub CLI（最简单）

#### 1. 安装 GitHub CLI

```bash
# macOS
brew install gh

# Ubuntu/Debian
sudo apt install gh

# Windows
# 下载：https://cli.github.com/
```

#### 2. 登录 GitHub

```bash
gh auth login
```

按照提示选择：
- What account do you want to log into? → `GitHub.com`
- What is your preferred protocol for Git operations? → `HTTPS`
- Authenticate with a GitHub.com device? → `Login with a web browser`

#### 3. 推送代码

```bash
cd /workspace/projects
git push origin main
```

GitHub CLI 会自动处理认证！

---

## 验证推送成功

推送成功后，你应该看到：

```
Enumerating objects: xxx, done.
Counting objects: xxx, done.
Delta compression using up to 4 threads.
Compressing objects: xxx, done.
Writing objects: xxx, done.
Total xxx (delta xxx), reused 0 (delta 0)
To https://github.com/h792296829-star/agent.git
   xxx..xxx  main -> main
```

然后访问 https://github.com/h792296829-star/agent 查看代码是否已推送。

---

## 推送后操作

### 1. 检查远程仓库

```bash
git remote -v
```

### 2. 查看提交历史

```bash
git log --oneline
```

### 3. 查看 GitHub 状态

访问：https://github.com/h792296829-star/agent

---

## 常见问题

### Q1: Token 过期怎么办？

**解决方案：**

1. 重新生成一个新的 Personal Access Token
2. 更新远程仓库 URL：
   ```bash
   git remote set-url origin https://NEW_TOKEN@github.com/h792296829-star/agent.git
   ```
3. 重新推送

### Q2: 权限不足（403 Forbidden）？

**可能原因：**

- Token 没有勾选 `repo` 权限
- 不是仓库的协作者
- 仓库是私有的，但 Token 权限不足

**解决方案：**

- 重新生成 Token，确保勾选 `repo` 权限
- 邀请自己成为仓库协作者（如果是组织仓库）

### Q3: 推送被拒绝（rejected）？

**可能原因：**

- 远程仓库有新的提交
- 本地代码不是最新的

**解决方案：**

```bash
# 先拉取远程代码
git pull origin main --rebase

# 再推送
git push origin main
```

### Q4: 如何避免每次都输入密码？

**方案 A：使用 credential helper**

```bash
git config --global credential.helper store
```

第一次输入后会保存凭证。

**方案 B：使用 SSH Key**

参考上面的方案二。

**方案 C：使用 GitHub CLI**

参考上面的方案三。

---

## 安全建议

### ✅ 推荐做法

- ✅ 使用 SSH Key（更安全）
- ✅ 使用 GitHub CLI（更方便）
- ✅ 设置 Token 有效期（不要永不过期）
- ✅ 定期轮换 Token
- ✅ 不要在代码中硬编码 Token

### ❌ 避免做法

- ❌ 不要分享 Token 给他人
- ❌ 不要在公开仓库中提交 Token
- ❌ 不要使用弱密码
- ❌ 不要在代码中直接写入 Token

---

## 下一步

推送成功后，你可以：

1. **继续开发**：修改代码后提交推送
2. **配置 Vercel**：访问 https://vercel.com/ 导入 GitHub 仓库
3. **配置 CI/CD**：在 GitHub Actions 中配置自动部署

---

## 参考文档

- [GitHub Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [GitHub SSH Keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
- [GitHub CLI](https://cli.github.com/)

---

**祝你推送成功！** 🎉

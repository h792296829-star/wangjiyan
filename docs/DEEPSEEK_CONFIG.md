# 🔧 DeepSeek 模型配置

## 环境变量设置

在 Vercel 部署时，需要设置以下环境变量：

### 必需的环境变量

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `COZE_WORKLOAD_IDENTITY_API_KEY` | `sk-39f88732243f41b5b9e30f9e7fcf25b6` | DeepSeek API Key |
| `COZE_INTEGRATION_MODEL_BASE_URL` | `https://api.deepseek.com` | DeepSeek API 地址 |

## 在 Vercel 中配置环境变量

### 步骤

1. 登录 Vercel：https://vercel.com/
2. 进入你的项目
3. 点击 **Settings** 标签
4. 左侧菜单点击 **Environment Variables**
5. 添加环境变量：

   **第一个变量：**
   - **Name**: `COZE_WORKLOAD_IDENTITY_API_KEY`
   - **Value**: `sk-39f88732243f41b5b9e30f9e7fcf25b6`
   - **Environment**: 选择 `Production`, `Preview`, `Development`（全部勾选）
   - 点击 **Save**

   **第二个变量：**
   - **Name**: `COZE_INTEGRATION_MODEL_BASE_URL`
   - **Value**: `https://api.deepseek.com`
   - **Environment**: 选择 `Production`, `Preview`, `Development`（全部勾选）
   - 点击 **Save**

6. **重新部署**：
   - 点击 **Deployments** 标签
   - 找到最新的部署，点击右侧的三个点
   - 选择 **Redeploy**
   - 点击 **Redeploy** 按钮

## 本地运行配置

如果你想在本地运行，可以设置环境变量：

```bash
# Linux/Mac
export COZE_WORKLOAD_IDENTITY_API_KEY=sk-39f88732243f41b5b9e30f9e7fcf25b6
export COZE_INTEGRATION_MODEL_BASE_URL=https://api.deepseek.com

# Windows PowerShell
$env:COZE_WORKLOAD_IDENTITY_API_KEY="sk-39f88732243f41b5b9e30f9e7fcf25b6"
$env:COZE_INTEGRATION_MODEL_BASE_URL="https://api.deepseek.com"

# 运行服务
python src/main.py
```

## 验证配置

部署成功后，可以通过以下方式验证：

1. 打开应用：`https://your-app.vercel.app`
2. 发送消息："你好"
3. 如果收到回复，说明配置成功！

## 常见问题

### Q1: 部署后提示 API 错误？

**解决方案：**
1. 检查环境变量是否正确设置
2. 确保重新部署了项目（环境变量修改后需要重新部署）
3. 查看部署日志：Vercel → Deployments → 查看最新部署的日志

### Q2: 响应很慢？

**可能原因：**
- DeepSeek API 响应时间
- Vercel Serverless 函数超时

**解决方案：**
- 增加超时时间（在 `config/agent_llm_config.json` 中调整 `timeout`）

### Q3: 本地运行正常，Vercel 上报错？

**解决方案：**
- 确认环境变量在 Vercel 上正确配置
- 确认所有环境都已勾选（Production, Preview, Development）
- 重新部署项目

## 配置文件说明

当前使用的模型：`deepseek-chat`

配置文件位置：`config/agent_llm_config.json`

```json
{
  "config": {
    "model": "deepseek-chat",
    "temperature": 0.7,
    "top_p": 0.9,
    "max_completion_tokens": 2000,
    "timeout": 600
  }
}
```

## 更换模型

如果你想更换 DeepSeek 的其他模型（如 `deepseek-coder`），修改配置文件：

1. 打开 `config/agent_llm_config.json`
2. 将 `"model"` 的值改为 `deepseek-coder`
3. 提交代码
4. 重新部署

---

**配置完成后，就可以使用 DeepSeek 模型了！** 🎉

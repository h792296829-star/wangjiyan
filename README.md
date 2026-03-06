# 🎤 公务员培训助手

一个专业的公务员培训 AI 助手，支持语音输入、多种题型生成和智能解答。

## ✨ 核心功能

- 🎤 **语音输入**：支持中文语音识别，说出即可
- 📝 **智能出题**：自动生成各类面试题目
- ✍️ **智能答题**：根据题目提供标准答案
- 💬 **主题讲解**：对公务员相关主题进行详细讲解
- 🌐 **云端部署**：支持 Vercel、云服务器等多种部署方式

## 🚀 快速开始

### 步骤 1：推送代码到 GitHub

首先需要将代码推送到 GitHub 仓库。

[📖 查看 GitHub 推送指南](docs/GITHUB_PUSH_GUIDE.md)

**简要步骤：**

1. 创建 GitHub Personal Access Token
2. 更新远程仓库 URL：
   ```bash
   git remote set-url origin https://YOUR_TOKEN@github.com/h792296829-star/agent.git
   ```
3. 推送代码：
   ```bash
   git push origin main
   ```

### 方式一：Vercel 部署（推荐，2分钟）

[📖 查看 Vercel 部署指南](docs/VERCEL_DEPLOY.md)

**优点：**
- ✅ 免费使用
- ✅ 2分钟部署
- ✅ 自动 HTTPS
- ✅ 全球 CDN

### 方式二：云服务器部署

[📖 查看云服务器部署指南](docs/DEPLOYMENT_README.md)

**优点：**
- ✅ 性能更强
- ✅ 完全控制
- ✅ 适合生产环境

### 方式三：本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
python src/main.py

# 访问
http://localhost:5000
```

## 📖 使用说明

### 支持的题型

1. **综合分析题** - 对社会现象、政策进行分析
2. **组织管理题** - 活动组织、调研、宣传、项目开展
3. **人际沟通题** - 与同事、群众沟通协调
4. **应急应变题** - 处理突发事件
5. **情景模拟题** - 劝说、调解、指导
6. **职业认知题** - 对职业的理解和规划
7. **自我认知题** - 自我介绍、个人优势

### 使用示例

```
用户：出一个组织管理题
助手：生成一道组织管理类题目

用户：给答案
助手：提供题目的标准答案

用户：基层治理创新
助手：讲解基层治理创新的相关内容
```

## 📚 项目结构

```
.
├── api/                    # Vercel Serverless 函数
│   └── index.py           # API 入口
├── assets/                # 前端资源
│   ├── index.html         # 主页面
│   ├── test-browser.html  # 浏览器兼容性测试
│   └── image.png          # 图片资源
├── config/                # 配置文件
│   └── agent_llm_config.json  # Agent 配置
├── docs/                  # 文档
│   ├── VERCEL_DEPLOY.md       # Vercel 部署指南
│   ├── DEPLOYMENT_README.md   # 云部署指南
│   ├── DEPLOYMENT.md          # 详细部署文档
│   └── QUICK_START.md         # 快速开始
├── scripts/               # 脚本
│   ├── deploy.sh          # 自动部署脚本
│   ├── package.sh         # 打包脚本
│   └── start.sh           # 启动脚本
├── src/                   # 源代码
│   ├── agents/            # Agent 实现
│   │   └── agent.py       # 主 Agent 代码
│   ├── storage/           # 存储配置
│   └── main.py            # 本地服务入口
├── requirements.txt       # Python 依赖
└── vercel.json            # Vercel 配置
```

## 🔧 技术栈

- **后端**：FastAPI, LangChain, LangGraph
- **前端**：HTML, CSS, JavaScript
- **AI 模型**：豆包 (doubao-seed-1-6-251015)
- **语音识别**：Web Speech API
- **部署**：Vercel, Supervisor, Nginx

## 📦 依赖安装

```bash
pip install -r requirements.txt
```

主要依赖：
- fastapi
- uvicorn
- langchain
- langgraph
- langchain-openai
- coze-coding-dev-sdk

## 🔐 配置说明

### 环境变量

```bash
# 工作目录
COZE_WORKSPACE_PATH=/path/to/project

# API 密钥（自动获取）
COZE_WORKLOAD_IDENTITY_API_KEY=your_api_key

# API 基础 URL（自动获取）
COZE_INTEGRATION_MODEL_BASE_URL=https://api.example.com
```

### Agent 配置

配置文件：`config/agent_llm_config.json`

包含：
- 模型选择
- 温度设置
- 系统提示词
- 工具列表

## 📊 浏览器支持

### 语音识别功能
- ✅ Chrome（推荐）
- ✅ Edge
- ✅ Safari
- ✅ Opera

### 基础功能
所有现代浏览器都支持基础功能

## 📖 文档

- [Vercel 部署指南](docs/VERCEL_DEPLOY.md) - 最简单的部署方式
- [云部署指南](docs/DEPLOYMENT_README.md) - 完整的云服务器部署
- [快速开始](docs/QUICK_START.md) - 5分钟上手
- [详细部署](docs/DEPLOYMENT.md) - 深度配置

## 🆘 常见问题

### 1. 麦克风按钮不显示？

检查浏览器是否支持语音识别，推荐使用 Chrome 或 Edge。

### 2. 部署到 Vercel 失败？

查看 [Vercel 部署指南](docs/VERCEL_DEPLOY.md) 的常见问题部分。

### 3. 本地运行无法启动？

确保已安装所有依赖：`pip install -r requirements.txt`

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 📮 联系方式

如有问题或建议，请通过 Issue 联系。

---

**祝你使用愉快！** 🎉

# 🚀 AI Work OS - 快速开始指南

欢迎使用 AI Work OS！本指南将帮助你在5分钟内启动并运行系统。

---

## 📋 前置要求

### 必需
- **Docker Desktop** - [下载](https://www.docker.com/products/docker-desktop)
- **OpenAI API Key** - [获取](https://platform.openai.com/api-keys)

### 可选（本地开发）
- **Node.js 20+** - [下载](https://nodejs.org/)
- **Python 3.11+** - [下载](https://www.python.org/)
- **Poetry** - [安装](https://python-poetry.org/docs/#installation)
- **pnpm** - `npm install -g pnpm`

---

## ⚡ 快速启动（Docker）

### 1. 克隆项目

```bash
git clone https://github.com/XTB-888/ai-work-os.git
cd ai-work-os
```

### 2. 配置环境变量

```bash
# 复制示例配置
cp backend/.env.example backend/.env

# 编辑 backend/.env，添加你的 OpenAI API Key
# OPENAI_API_KEY=sk-your-key-here
```

**Windows用户**:
```powershell
Copy-Item backend\.env.example backend\.env
notepad backend\.env
```

### 3. 启动服务

```bash
docker-compose up -d
```

等待所有容器启动（约30秒）。

### 4. 运行数据库迁移

```bash
# Linux/Mac
docker-compose exec backend alembic upgrade head

# Windows
docker-compose exec backend alembic upgrade head
```

### 5. 访问应用

- **前端**: http://localhost:3000
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs

---

## 🎮 使用流程

### 第一步：注册账号

1. 访问 http://localhost:3000
2. 点击 "Sign Up"
3. 填写邮箱、用户名、密码
4. 自动登录并跳转到项目列表

### 第二步：创建项目

1. 点击 "+ New Project"
2. 输入项目名称（例如：Task Management API）
3. 输入目标（可以点击示例目标使用）：
   ```
   Build a REST API for task management with FastAPI and PostgreSQL. 
   Include CRUD endpoints for tasks, user authentication, and basic documentation.
   ```
4. 点击 "Create Project"

### 第三步：监控执行

项目创建后，系统会自动：
1. ✅ **解析目标** - AI分析你的需求（5秒）
2. ✅ **生成团队** - 创建5个AI Agent（2秒）
3. ✅ **规划任务** - Planner分解任务（10秒）
4. ✅ **执行任务** - Engineer实现代码（30-120秒/任务）

你可以实时查看：
- **Overview** - 项目进度和统计
- **Agents** - AI团队成员状态
- **Tasks** - 任务列表和执行情况
- **Messages** - Agent之间的沟通
- **Decisions** - 做出的决策和理由
- **Outputs** - 生成的代码和文档

### 第四步：查看结果

任务完成后：
1. 在 **Outputs** 标签查看生成的代码
2. 在 **Tasks** 标签查看每个任务的输出
3. 在 **Decisions** 标签了解技术决策

---

## 🛠️ 本地开发（不使用Docker）

### 后端

```bash
cd backend

# 安装依赖
poetry install

# 配置环境变量
cp .env.example .env
# 编辑 .env 添加 OPENAI_API_KEY

# 启动PostgreSQL和Redis（需要Docker）
docker-compose up -d postgres redis

# 运行迁移
poetry run alembic upgrade head

# 启动服务
poetry run uvicorn app.main:app --reload
```

后端运行在 http://localhost:8000

### 前端

```bash
cd frontend

# 安装依赖
pnpm install

# 配置环境变量
cp .env.local.example .env.local

# 启动开发服务器
pnpm dev
```

前端运行在 http://localhost:3000

---

## 📝 示例项目

### 软件开发

**目标**:
```
Build a REST API for todo management with FastAPI. 
Include endpoints for creating, reading, updating, and deleting todos. 
Add user authentication with JWT tokens. Use PostgreSQL for data storage.
```

**预期结果**:
- API架构设计
- 数据库Schema
- FastAPI路由实现
- 认证系统
- 单元测试

### 研究分析

**目标**:
```
Research the impact of artificial intelligence on healthcare in 2024. 
Focus on diagnostic tools, patient care automation, and ethical considerations. 
Provide a comprehensive report with data and citations.
```

**预期结果**:
- 文献综述
- 数据分析
- 趋势报告
- 引用来源

---

## 🔧 常见问题

### Q1: Docker容器启动失败？

**检查**:
- Docker Desktop是否运行
- 端口3000、8000、5432、6379是否被占用

**解决**:
```bash
# 查看日志
docker-compose logs

# 重启服务
docker-compose down
docker-compose up -d
```

### Q2: 数据库迁移失败？

**检查**:
- PostgreSQL容器是否运行
- 数据库连接配置是否正确

**解决**:
```bash
# 检查PostgreSQL
docker-compose ps postgres

# 重新运行迁移
docker-compose exec backend alembic upgrade head
```

### Q3: 前端无法连接后端？

**检查**:
- 后端是否运行在8000端口
- 环境变量 `NEXT_PUBLIC_API_URL` 是否正确

**解决**:
```bash
# 检查后端状态
curl http://localhost:8000/health

# 检查前端环境变量
cat frontend/.env.local
```

### Q4: OpenAI API调用失败？

**检查**:
- API Key是否正确
- 账户是否有余额
- 网络是否可以访问OpenAI

**解决**:
```bash
# 测试API Key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Q5: 项目创建后没有反应？

**原因**: 工作流在后台执行

**解决**:
- 等待10-30秒
- 刷新页面
- 查看后端日志：`docker-compose logs backend`

---

## 📊 系统要求

### 最低配置
- **CPU**: 2核
- **内存**: 4GB
- **磁盘**: 10GB
- **网络**: 需要访问OpenAI API

### 推荐配置
- **CPU**: 4核+
- **内存**: 8GB+
- **磁盘**: 20GB+
- **网络**: 稳定的互联网连接

---

## 🎯 下一步

### 探索功能
1. 尝试不同类型的项目（研究、产品设计、商业分析）
2. 查看Agent之间的沟通记录
3. 了解决策制定过程
4. 导出生成的代码

### 自定义配置
1. 修改Agent Prompt模板
2. 添加新的Agent角色
3. 调整LLM参数（temperature, max_tokens）
4. 扩展工具系统

### 贡献代码
1. Fork项目
2. 创建功能分支
3. 提交Pull Request
4. 参与讨论

---

## 📚 更多资源

- [完整文档](./README.md)
- [系统架构](./01-系统架构设计.md)
- [数据库设计](./02-数据库结构设计.md)
- [Agent设计](./03-Agent-Prompt设计.md)
- [开发方案](./04-MVP开发方案.md)
- [贡献指南](./CONTRIBUTING.md)

---

## 💬 获取帮助

- **GitHub Issues**: https://github.com/XTB-888/ai-work-os/issues
- **Discussions**: https://github.com/XTB-888/ai-work-os/discussions

---

## 🎉 开始使用

现在你已经准备好了！创建你的第一个AI项目，看看AI团队如何为你工作。

```bash
# 一键启动
docker-compose up -d

# 访问
open http://localhost:3000
```

**祝你使用愉快！** 🚀

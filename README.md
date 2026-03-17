<div align="center">

# AI Work OS - AI Work Operating System
**AI Work OS - AI工作操作系统**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Latest-orange.svg)](https://github.com/langchain-ai/langgraph)

**[English](#english) | [中文](#中文)**

</div>

---

<a name="english"></a>
## 🇺🇸 English

### Transform Goals into Results with AI Agent Teams

**AI Work OS** is an innovative AI-powered work operating system that transforms user goals into tangible results through autonomous AI agent collaboration.

#### 🚀 Quick Start

```bash
# 1. Clone repository
git clone https://github.com/XTB-888/ai-work-os.git
cd ai-work-os

# 2. Configure environment
cp backend/.env.example backend/.env
# Edit backend/.env and add OPENAI_API_KEY

# 3. Start services
docker-compose up -d

# 4. Run migrations
docker-compose exec backend alembic upgrade head

# 5. Access
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/docs
```

#### 📚 Documentation

- [Quick Start Guide](./QUICKSTART.md)
- [Project Summary](./PROJECT_SUMMARY.md)
- [System Architecture](./01-系统架构设计.md)

#### 🎯 Features

- 🤖 **6 Specialized AI Agents** - Coordinator, Planner, Architect, Engineer, QA, Researcher
- 🛠️ **4 Agent Tools** - Code execution, web search, file management
- 👁️ **Real-time Monitoring** - Watch agents work in real-time
- 📊 **Full Accountability** - Track every decision and output
- ✅ **Production Ready** - Docker, Nginx, Redis, PostgreSQL

---

<a name="中文"></a>
## 🇨🇳 中文

### 用AI智能体团队将目标转化为成果

**AI Work OS** 是一个创新的AI驱动工作操作系统，通过自主AI智能体协作将用户目标转化为实际成果。

#### 🚀 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/XTB-888/ai-work-os.git
cd ai-work-os

# 2. 配置环境变量
cp backend/.env.example backend/.env
# 编辑 backend/.env 添加 OPENAI_API_KEY

# 3. 启动服务
docker-compose up -d

# 4. 运行数据库迁移
docker-compose exec backend alembic upgrade head

# 5. 访问应用
# 前端: http://localhost:3000
# 后端API: http://localhost:8000/docs
```

#### 📚 文档

- [快速开始指南](./QUICKSTART.md)
- [项目总结](./PROJECT_SUMMARY.md)
- [系统架构设计](./01-系统架构设计.md)

#### 🎯 核心特性

- 🤖 **6个专业AI智能体** - 协调者、规划者、架构师、工程师、QA、研究员
- 🛠️ **4个智能体工具** - 代码执行、网络搜索、文件管理
- 👁️ **实时监控** - 观看智能体实时工作
- 📊 **完整责任追溯** - 追踪每个决策和输出
- ✅ **生产就绪** - Docker、Nginx、Redis、PostgreSQL

---

## 🛠️ Technology Stack / 技术栈

**Backend / 后端:**
- FastAPI + SQLAlchemy + PostgreSQL + Redis
- LangChain + LangGraph + OpenAI GPT-4

**Frontend / 前端:**
- Next.js 14 + React 18 + TypeScript
- TailwindCSS + Axios

**DevOps:**
- Docker + Docker Compose + Nginx

---

## 📊 Project Status / 项目状态

**Completion / 完成度:** 99%

- ✅ Backend / 后端: 100%
- ✅ Frontend / 前端: 95%
- ✅ Agent System / 智能体系统: 100%
- ✅ Documentation / 文档: 100%

---

## 📄 License / 许可证

MIT License - see [LICENSE](./LICENSE)

---

<div align="center">

**[⬆ Back to Top](#ai-work-os---ai-work-operating-system)**

**Made with ❤️ by AI Work OS Team / AI Work OS团队出品**

</div>

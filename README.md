# AI Work OS - AI Work Operating System

<div align="center">

![AI Work OS Logo](https://via.placeholder.com/200x200?text=AI+Work+OS)

**Transform Goals into Results with AI Agent Teams**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Latest-orange.svg)](https://github.com/langchain-ai/langgraph)

[Demo](https://demo.aiworkos.com) • [Documentation](./docs) • [Architecture](./docs/architecture) • [Contributing](./CONTRIBUTING.md)

</div>

---

## 📖 Overview

**AI Work OS** is an innovative AI-powered work operating system that transforms user goals into tangible results through autonomous AI agent collaboration. Unlike traditional AI tools, AI Work OS simulates a complete organizational structure where specialized AI agents work together like a real team.

### Core Concept

```
User Goal → AI Team Assembly → Workflow Generation → Agent Collaboration → Results
```

**Key Features:**
- 🤖 **Multi-Agent Collaboration**: Specialized AI agents work together seamlessly
- 👁️ **Observable Execution**: Watch your AI team work in real-time
- 💬 **Transparent Communication**: See every decision and discussion
- 📊 **Clear Accountability**: Track who did what and why
- 🔄 **Adaptive Workflows**: Dynamic task planning and execution
- 🎯 **Goal-Oriented**: Focus on outcomes, not processes

---

## 🎯 Use Cases

AI Work OS supports multiple task types:

### 1. 💻 Software Development
Build complete applications from natural language descriptions.
- **Example**: "Build a REST API for task management with FastAPI"
- **AI Team**: Product Manager → Architect → Backend Engineer → QA → Reviewer

### 2. 🔬 Research & Analysis
Conduct comprehensive research on any topic.
- **Example**: "Research the impact of AI on healthcare in 2024"
- **AI Team**: Research Lead → Literature Reviewer → Data Analyst → Writer

### 3. 🎨 Product Design
Design products from concept to specification.
- **Example**: "Design a mobile app for fitness tracking"
- **AI Team**: Product Manager → UX Designer → Market Analyst → Architect

### 4. 📊 Business Analysis
Analyze markets, competitors, and strategies.
- **Example**: "Analyze the SaaS market for project management tools"
- **AI Team**: Market Analyst → Competitor Analyst → Strategy → Finance

### 5. 🚀 Startup Planning
Create comprehensive startup plans.
- **Example**: "Create a business plan for an AI-powered education platform"
- **AI Team**: Founder → Market Research → Product → Tech → Finance → Marketing

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface (Next.js)                  │
│  Goal Input • Team Visualization • Workflow Monitor          │
└─────────────────────────────────────────────────────────────┘
                            ↕ REST API / WebSocket
┌─────────────────────────────────────────────────────────────┐
│                    API Gateway (FastAPI)                     │
│  Authentication • Routing • Rate Limiting                    │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                   Core Business Logic                        │
│  Goal Parser • Team Generator • Workflow Generator           │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│              Agent Orchestration (LangGraph)                 │
│  Coordinator • Planner • Specialist Agents                   │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                    LLM Integration Layer                     │
│  OpenAI • Anthropic • Local Models                          │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                  Data Persistence Layer                      │
│  PostgreSQL • Vector DB • Redis                             │
└─────────────────────────────────────────────────────────────┘
```

For detailed architecture, see [System Architecture](./docs/architecture/01-系统架构设计.md).

---

## 🚀 Quick Start

### Prerequisites

- **Docker** and **Docker Compose**
- **Node.js** 20+ (for frontend development)
- **Python** 3.11+ (for backend development)
- **OpenAI API Key** (or other LLM provider)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-work-os.git
cd ai-work-os
```

2. **Set up environment variables**
```bash
# Backend
cp backend/.env.example backend/.env
# Edit backend/.env and add your API keys

# Frontend
cp frontend/.env.example frontend/.env.local
```

3. **Start with Docker Compose**
```bash
docker-compose up -d
```

4. **Run database migrations**
```bash
docker-compose exec backend alembic upgrade head
```

5. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Development Setup

For local development without Docker:

**Backend:**
```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
pnpm install
pnpm dev
```

---

## 📚 Documentation

- [System Architecture](./01-系统架构设计.md) - Complete system design
- [Database Schema](./02-数据库结构设计.md) - Database structure and relationships
- [Agent Prompts](./03-Agent-Prompt设计.md) - AI agent prompt templates
- [MVP Development Plan](./04-MVP开发方案.md) - 3-week development roadmap
- [Code Structure](./05-代码目录结构设计.md) - Project organization

---

## 🎮 Usage Example

### 1. Create a Project

```bash
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Task Management API",
    "goal": "Build a REST API for task management with FastAPI and PostgreSQL"
  }'
```

### 2. Watch the AI Team Work

The system will:
1. ✅ Parse your goal and identify requirements
2. ✅ Generate an AI team (Coordinator, Planner, Architect, Engineer, QA)
3. ✅ Create a detailed task breakdown
4. ✅ Execute tasks with agent collaboration
5. ✅ Generate code, documentation, and tests
6. ✅ Provide results with full accountability

### 3. View Results

Access the project dashboard to see:
- **Team Structure**: Visual representation of AI agents
- **Task Progress**: Real-time task status updates
- **Agent Communication**: All messages and decisions
- **Outputs**: Generated code, documents, and artifacts
- **Accountability**: Who did what and why

---

## 🤖 Agent Roles

### Core Agents

| Agent | Role | Responsibilities |
|-------|------|------------------|
| **Coordinator** | CEO | Team management, delegation, monitoring |
| **Planner** | Project Manager | Task planning, scheduling, optimization |
| **Architect** | System Architect | Architecture design, tech stack selection |
| **Engineer** | Developer | Code implementation, testing |
| **QA** | Quality Assurance | Testing, review, approval |
| **Researcher** | Analyst | Information gathering, analysis |
| **Designer** | UX/UI Designer | Product design, user experience |
| **Writer** | Technical Writer | Documentation, reports |

Each agent has:
- Clear responsibilities
- Specific skills and tools
- Decision-making authority
- Communication protocols

---

## 🛠️ Technology Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **UI Library**: TailwindCSS + shadcn/ui
- **Visualization**: ReactFlow
- **State Management**: React Query (TanStack Query)
- **Real-time**: Socket.io

### Backend
- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: PostgreSQL
- **Cache**: Redis
- **Authentication**: JWT

### AI & Agents
- **Agent Framework**: LangGraph + LangChain
- **LLM**: OpenAI GPT-4 (configurable)
- **Vector DB**: Pinecone / Weaviate (optional)

### DevOps
- **Containerization**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana (optional)

---

## 📊 Project Status

### MVP (v1.0) - Current Focus

**Status**: 🚧 In Development

**Timeline**: 3 weeks

**Features**:
- ✅ User authentication
- ✅ Project creation and goal input
- ✅ Software Development task type
- ✅ 3 core agents (Coordinator, Planner, Engineer)
- ✅ Basic workflow execution
- ✅ Real-time updates
- ✅ Accountability tracking

### Roadmap

**v1.1** (MVP + 4 weeks)
- [ ] QA Agent
- [ ] Research task type
- [ ] Improved UI/UX
- [ ] Project templates

**v1.2** (MVP + 8 weeks)
- [ ] Vector database integration
- [ ] Agent knowledge base
- [ ] Multi-LLM support
- [ ] Advanced workflow orchestration

**v2.0** (MVP + 12 weeks)
- [ ] All 5 task types
- [ ] External API integrations (GitHub, Jira, Slack)
- [ ] Multi-tenancy
- [ ] Advanced analytics

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](./CONTRIBUTING.md) for details.

### Development Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Standards

- **Frontend**: ESLint + Prettier
- **Backend**: Black + Ruff
- **Tests**: Minimum 70% coverage
- **Documentation**: Update docs for new features

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

---

## 🙏 Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain) - LLM framework
- [LangGraph](https://github.com/langchain-ai/langgraph) - Agent orchestration
- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [Next.js](https://nextjs.org/) - Frontend framework
- [ReactFlow](https://reactflow.dev/) - Visualization library

---

## 📧 Contact

- **Project Lead**: Your Name
- **Email**: your.email@example.com
- **Website**: https://aiworkos.com
- **Twitter**: [@aiworkos](https://twitter.com/aiworkos)

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/ai-work-os&type=Date)](https://star-history.com/#yourusername/ai-work-os&Date)

---

<div align="center">

**Made with ❤️ by the AI Work OS Team**

[⬆ Back to Top](#ai-work-os---ai-work-operating-system)

</div>

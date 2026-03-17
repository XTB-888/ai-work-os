# AI Work OS - MVP 开发方案

## 1. MVP 目标与范围

### 1.1 MVP 核心目标

构建一个**最小可行产品**,验证核心概念:
- ✅ 用户可以输入目标
- ✅ 系统自动生成AI团队
- ✅ Agent协作完成简单任务
- ✅ 可观测执行过程
- ✅ 输出结果可追溯责任

### 1.2 MVP 功能范围

**包含功能**:
- ✅ 用户认证 (简单的JWT认证)
- ✅ 项目创建和目标输入
- ✅ 支持1种任务类型: **Software Development**
- ✅ 3个核心Agent: Coordinator, Planner, Backend Engineer
- ✅ 基础工作流: Goal → Team → Tasks → Execution → Result
- ✅ Agent沟通可视化
- ✅ 简单的责任追踪
- ✅ 基础的前端界面

**不包含功能** (留待后续版本):
- ❌ 多种任务类型 (Research, Product Design等)
- ❌ 复杂的Agent角色 (QA, Designer等)
- ❌ 高级工作流编排
- ❌ Vector数据库集成
- ❌ 外部API集成 (GitHub, Jira等)
- ❌ 高级可视化和分析
- ❌ 多租户支持

### 1.3 MVP 成功标准

**Demo场景**: 用户输入 "Build a simple REST API for todo management with FastAPI"

**预期结果**:
1. 系统生成3个Agent (Coordinator, Planner, Engineer)
2. Planner创建5-8个任务
3. Engineer执行任务,生成代码
4. 用户可以看到:
   - Agent团队结构
   - 任务列表和状态
   - Agent之间的沟通记录
   - 最终生成的代码
   - 每个输出的责任人

---

## 2. 技术栈选择 (MVP)

### 2.1 前端
- **框架**: Next.js 14 (App Router)
- **UI库**: TailwindCSS + shadcn/ui
- **状态管理**: React Context + SWR
- **可视化**: ReactFlow (Agent团队和工作流)
- **实时通信**: Socket.io-client

### 2.2 后端
- **框架**: FastAPI
- **ORM**: SQLAlchemy
- **数据库**: PostgreSQL (Docker)
- **缓存**: Redis (Docker)
- **任务队列**: 暂不使用 (直接同步执行)
- **认证**: JWT (python-jose)

### 2.3 Agent系统
- **框架**: LangGraph + LangChain
- **LLM**: OpenAI GPT-4 (可配置)
- **工具**: 
  - Code Executor: 简单的Python exec (沙箱化)
  - File Manager: 本地文件系统

### 2.4 开发工具
- **包管理**: 
  - 前端: pnpm
  - 后端: Poetry
- **代码质量**: 
  - ESLint + Prettier (前端)
  - Black + Ruff (后端)
- **版本控制**: Git + GitHub
- **容器化**: Docker + Docker Compose

---

## 3. 三周开发路线

### Week 1: 基础设施 + 后端核心

#### Day 1-2: 项目初始化
**目标**: 搭建开发环境

**任务**:
- [x] 创建GitHub仓库
- [x] 初始化前端项目 (Next.js)
- [x] 初始化后端项目 (FastAPI)
- [x] 配置Docker Compose (PostgreSQL + Redis)
- [x] 配置开发环境 (ESLint, Black等)
- [x] 设置CI/CD基础 (GitHub Actions)

**交付物**:
- 可运行的前后端骨架
- Docker环境配置
- README文档

---

#### Day 3-4: 数据库 + 认证
**目标**: 实现数据持久化和用户认证

**任务**:
- [x] 设计并创建数据库表 (users, projects, agents, tasks, messages, decisions, outputs)
- [x] 实现SQLAlchemy模型
- [x] 实现数据库迁移 (Alembic)
- [x] 实现用户注册/登录API
- [x] 实现JWT认证中间件
- [x] 编写API测试

**交付物**:
- 完整的数据库Schema
- 用户认证API
- 单元测试

---

#### Day 5-7: 核心业务逻辑
**目标**: 实现Goal Parser和Team Generator

**任务**:
- [x] 实现Goal Parser
  - 使用LLM解析用户目标
  - 提取任务类型、技术栈、需求
- [x] 实现Team Generator
  - 定义Agent模板 (Coordinator, Planner, Engineer)
  - 根据任务类型生成团队
- [x] 实现项目创建API
- [x] 实现团队生成API
- [x] 编写集成测试

**交付物**:
- Goal Parser模块
- Team Generator模块
- API端点: `POST /api/v1/projects`, `POST /api/v1/projects/{id}/goals`

---

### Week 2: Agent系统 + 工作流

#### Day 8-10: Agent基础框架
**目标**: 实现LangGraph Agent系统

**任务**:
- [x] 设计LangGraph状态结构
- [x] 实现Coordinator Agent
  - 接收目标,启动流程
  - 委派任务给Planner
- [x] 实现Planner Agent
  - 任务分解
  - 创建任务列表
  - 分析依赖关系
- [x] 实现Backend Engineer Agent
  - 接收任务
  - 生成代码
  - 返回结果
- [x] 实现Agent间通信机制

**交付物**:
- 3个可工作的Agent
- Agent通信系统
- LangGraph工作流定义

---

#### Day 11-12: 工作流执行引擎
**目标**: 实现任务执行和状态管理

**任务**:
- [x] 实现Workflow Generator
  - 根据任务生成工作流图
- [x] 实现任务执行引擎
  - 按依赖关系执行任务
  - 更新任务状态
- [x] 实现实时状态推送 (WebSocket)
- [x] 实现错误处理和重试机制

**交付物**:
- 工作流执行引擎
- WebSocket实时更新
- 错误处理机制

---

#### Day 13-14: 责任追踪系统
**目标**: 实现决策记录和输出追踪

**任务**:
- [x] 实现Decision记录
  - Agent决策自动记录
  - 决策理由和影响分析
- [x] 实现Output追踪
  - 记录每个输出的作者
  - 记录审核者和批准者
- [x] 实现审计日志
- [x] 实现责任查询API

**交付物**:
- 决策记录系统
- 输出追踪系统
- 审计日志
- API端点: `GET /api/v1/projects/{id}/decisions`, `GET /api/v1/projects/{id}/outputs`

---

### Week 3: 前端界面 + 集成测试

#### Day 15-17: 前端核心页面
**目标**: 实现用户界面

**任务**:
- [x] 实现登录/注册页面
- [x] 实现项目创建页面
  - 目标输入表单
  - 任务类型选择
- [x] 实现项目详情页面
  - Agent团队可视化 (ReactFlow)
  - 任务列表和状态
  - Agent沟通面板
  - 结果展示
- [x] 实现WebSocket集成
  - 实时更新任务状态
  - 实时显示Agent消息
- [x] 实现响应式设计

**交付物**:
- 完整的前端界面
- 实时更新功能
- 移动端适配

---

#### Day 18-19: 集成测试 + Bug修复
**目标**: 端到端测试和优化

**任务**:
- [x] 端到端测试
  - 完整流程测试: 从目标输入到结果输出
  - 测试多个场景
- [x] 性能优化
  - 数据库查询优化
  - 前端加载优化
- [x] Bug修复
- [x] 代码重构和清理
- [x] 文档完善

**交付物**:
- 稳定的MVP版本
- 测试报告
- 性能报告

---

#### Day 20-21: Demo准备 + 部署
**目标**: 准备演示和部署

**任务**:
- [x] 准备Demo数据
- [x] 录制Demo视频
- [x] 编写用户文档
- [x] 部署到测试环境
  - 使用Docker部署
  - 配置域名和SSL
- [x] 准备演示PPT
- [x] 内部试用和反馈收集

**交付物**:
- 可访问的Demo环境
- Demo视频
- 用户文档
- 演示材料

---

## 4. 开发步骤详解

### 4.1 Phase 1: 后端基础 (Day 1-7)

#### Step 1: 项目初始化

```bash
# 创建项目目录
mkdir ai-work-os
cd ai-work-os

# 初始化后端
mkdir backend
cd backend
poetry init
poetry add fastapi uvicorn sqlalchemy psycopg2-binary alembic python-jose passlib redis langchain langgraph openai

# 初始化前端
cd ..
npx create-next-app@latest frontend --typescript --tailwind --app
cd frontend
pnpm add @tanstack/react-query reactflow socket.io-client shadcn-ui
```

#### Step 2: Docker环境

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: ai_work_os
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    ports:
      - "6379:6379"

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://admin:password@postgres:5432/ai_work_os
      REDIS_URL: redis://redis:6379
    depends_on:
      - postgres
      - redis

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  postgres_data:
```

#### Step 3: 数据库模型

```python
# backend/app/models/project.py
from sqlalchemy import Column, String, Integer, DateTime, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    name = Column(String(255), nullable=False)
    task_type = Column(String(50), nullable=False)
    status = Column(String(50), default="draft")
    goal_raw = Column(Text, nullable=False)
    goal_parsed = Column(JSON)
    # ... 其他字段
```

#### Step 4: API端点

```python
# backend/app/api/v1/projects.py
from fastapi import APIRouter, Depends
from app.schemas.project import ProjectCreate, ProjectResponse
from app.services.goal_parser import GoalParserService
from app.services.team_generator import TeamGeneratorService

router = APIRouter()

@router.post("/projects", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    current_user: User = Depends(get_current_user)
):
    # 创建项目
    db_project = Project(
        user_id=current_user.id,
        name=project.name,
        goal_raw=project.goal
    )
    db.add(db_project)
    db.commit()
    
    return db_project

@router.post("/projects/{project_id}/goals")
async def submit_goal(
    project_id: UUID,
    goal: GoalSubmit,
    current_user: User = Depends(get_current_user)
):
    # 解析目标
    parsed_goal = await GoalParserService.parse(goal.text)
    
    # 生成团队
    team = await TeamGeneratorService.generate(parsed_goal)
    
    # 更新项目
    project.goal_parsed = parsed_goal
    project.status = "planning"
    db.commit()
    
    return {"parsed_goal": parsed_goal, "team": team}
```

---

### 4.2 Phase 2: Agent系统 (Day 8-14)

#### Step 5: LangGraph Agent定义

```python
# backend/app/agents/coordinator.py
from langgraph.graph import StateGraph
from langchain.chat_models import ChatOpenAI
from app.agents.prompts import COORDINATOR_AGENT_PROMPT

class CoordinatorAgent:
    def __init__(self, project_id: UUID):
        self.project_id = project_id
        self.llm = ChatOpenAI(model="gpt-4-turbo")
        
    async def process(self, state: AgentState):
        # 构建Prompt
        prompt = COORDINATOR_AGENT_PROMPT.format(
            project_goal=state["goal"],
            team=state["team"],
            # ... 其他上下文
        )
        
        # 调用LLM
        response = await self.llm.ainvoke(prompt)
        
        # 解析响应
        actions = parse_agent_response(response)
        
        # 执行actions
        for action in actions:
            await self.execute_action(action)
        
        return state
```

#### Step 6: 工作流定义

```python
# backend/app/workflows/software_development.py
from langgraph.graph import StateGraph, END

def create_software_dev_workflow():
    workflow = StateGraph(AgentState)
    
    # 定义节点
    workflow.add_node("coordinator", coordinator_agent)
    workflow.add_node("planner", planner_agent)
    workflow.add_node("engineer", engineer_agent)
    
    # 定义边
    workflow.add_edge("coordinator", "planner")
    workflow.add_edge("planner", "engineer")
    workflow.add_edge("engineer", END)
    
    # 设置入口
    workflow.set_entry_point("coordinator")
    
    return workflow.compile()
```

---

### 4.3 Phase 3: 前端界面 (Day 15-21)

#### Step 7: 项目详情页面

```typescript
// frontend/app/projects/[id]/page.tsx
'use client'

import { useProject } from '@/hooks/useProject'
import { TeamVisualization } from '@/components/TeamVisualization'
import { TaskList } from '@/components/TaskList'
import { MessagePanel } from '@/components/MessagePanel'

export default function ProjectPage({ params }: { params: { id: string } }) {
  const { project, agents, tasks, messages } = useProject(params.id)
  
  return (
    <div className="grid grid-cols-12 gap-4">
      {/* Agent团队 */}
      <div className="col-span-4">
        <TeamVisualization agents={agents} />
      </div>
      
      {/* 任务列表 */}
      <div className="col-span-4">
        <TaskList tasks={tasks} />
      </div>
      
      {/* 消息面板 */}
      <div className="col-span-4">
        <MessagePanel messages={messages} />
      </div>
    </div>
  )
}
```

#### Step 8: WebSocket集成

```typescript
// frontend/hooks/useWebSocket.ts
import { useEffect } from 'react'
import io from 'socket.io-client'

export function useWebSocket(projectId: string) {
  useEffect(() => {
    const socket = io('http://localhost:8000')
    
    socket.emit('join_project', projectId)
    
    socket.on('task_updated', (task) => {
      // 更新任务状态
      queryClient.invalidateQueries(['tasks', projectId])
    })
    
    socket.on('message_received', (message) => {
      // 显示新消息
      queryClient.invalidateQueries(['messages', projectId])
    })
    
    return () => socket.disconnect()
  }, [projectId])
}
```

---

## 5. 关键技术挑战与解决方案

### 5.1 挑战1: LLM响应不稳定

**问题**: LLM可能返回格式不正确的JSON

**解决方案**:
- 使用LangChain的Output Parser
- 实现重试机制
- 提供清晰的JSON Schema示例
- 使用Function Calling (OpenAI)

```python
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel

class AgentAction(BaseModel):
    action_type: str
    parameters: dict
    rationale: str

parser = PydanticOutputParser(pydantic_object=AgentAction)
prompt = prompt_template + parser.get_format_instructions()
```

---

### 5.2 挑战2: Agent间通信复杂度

**问题**: 多个Agent异步通信难以管理

**解决方案**:
- 使用LangGraph的状态管理
- 实现消息队列
- 定义清晰的通信协议
- 使用Redis作为消息中间件

---

### 5.3 挑战3: 代码执行安全

**问题**: Agent生成的代码可能不安全

**解决方案**:
- 使用Docker容器隔离
- 限制资源使用 (CPU, 内存, 时间)
- 禁止危险操作 (网络访问, 文件系统访问)
- 代码审查机制

```python
import docker

client = docker.from_env()
container = client.containers.run(
    "python:3.11-slim",
    command=f"python -c '{code}'",
    mem_limit="128m",
    cpu_quota=50000,
    network_disabled=True,
    timeout=10
)
```

---

## 6. 测试策略

### 6.1 单元测试

```python
# backend/tests/test_goal_parser.py
import pytest
from app.services.goal_parser import GoalParserService

@pytest.mark.asyncio
async def test_parse_software_dev_goal():
    goal = "Build a REST API for task management with FastAPI"
    result = await GoalParserService.parse(goal)
    
    assert result["task_type"] == "software_development"
    assert "FastAPI" in result["tech_stack"]
    assert "task_management" in result["domain"]
```

### 6.2 集成测试

```python
# backend/tests/test_workflow.py
@pytest.mark.asyncio
async def test_complete_workflow():
    # 创建项目
    project = await create_project(user_id, "Build todo API")
    
    # 提交目标
    await submit_goal(project.id, "Build a FastAPI todo API")
    
    # 等待执行完成
    await wait_for_completion(project.id, timeout=300)
    
    # 验证结果
    outputs = await get_outputs(project.id)
    assert len(outputs) > 0
    assert outputs[0].output_type == "code"
```

### 6.3 E2E测试

使用Playwright进行前端E2E测试:

```typescript
// frontend/e2e/project-creation.spec.ts
import { test, expect } from '@playwright/test'

test('complete project workflow', async ({ page }) => {
  // 登录
  await page.goto('/login')
  await page.fill('[name="email"]', 'test@example.com')
  await page.fill('[name="password"]', 'password')
  await page.click('button[type="submit"]')
  
  // 创建项目
  await page.goto('/projects/new')
  await page.fill('[name="goal"]', 'Build a FastAPI todo API')
  await page.click('button:has-text("Create Project")')
  
  // 等待Agent生成
  await expect(page.locator('.agent-card')).toHaveCount(3)
  
  // 等待任务完成
  await expect(page.locator('.task-completed')).toHaveCount(5, { timeout: 60000 })
})
```

---

## 7. 部署方案

### 7.1 开发环境

```bash
# 启动所有服务
docker-compose up -d

# 运行数据库迁移
docker-compose exec backend alembic upgrade head

# 访问应用
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### 7.2 生产环境 (简化版)

使用Railway / Render / Vercel部署:

**前端** (Vercel):
- 自动从GitHub部署
- 环境变量配置API URL

**后端** (Railway):
- PostgreSQL托管数据库
- Redis托管实例
- 自动从GitHub部署

**环境变量**:
```bash
# Backend
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
OPENAI_API_KEY=sk-...
JWT_SECRET=...

# Frontend
NEXT_PUBLIC_API_URL=https://api.aiworkos.com
```

---

## 8. MVP后续迭代计划

### Version 1.1 (MVP + 4周)
- [ ] 添加QA Agent
- [ ] 支持Research任务类型
- [ ] 改进UI/UX
- [ ] 添加项目模板

### Version 1.2 (MVP + 8周)
- [ ] Vector数据库集成
- [ ] Agent知识库
- [ ] 支持更多LLM提供商
- [ ] 高级工作流编排

### Version 2.0 (MVP + 12周)
- [ ] 支持所有5种任务类型
- [ ] 外部API集成 (GitHub, Jira)
- [ ] 多租户支持
- [ ] 高级分析和报告

---

## 9. 风险管理

### 9.1 技术风险

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|----------|
| LLM API不稳定 | 高 | 中 | 实现重试机制,使用备用模型 |
| Agent响应慢 | 中 | 高 | 优化Prompt,使用缓存 |
| 数据库性能 | 中 | 低 | 索引优化,查询优化 |

### 9.2 时间风险

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|----------|
| Agent开发超时 | 高 | 中 | 简化Agent逻辑,减少功能 |
| 前端开发延期 | 中 | 低 | 使用UI组件库加速开发 |
| 集成测试问题 | 中 | 中 | 提前开始集成,持续测试 |

---

## 10. 成功指标

### 10.1 功能指标
- [ ] 用户可以成功创建项目
- [ ] 系统可以正确解析80%的常见目标
- [ ] Agent可以成功生成可运行的代码
- [ ] 所有输出都有明确的责任人

### 10.2 性能指标
- [ ] 项目创建 < 2秒
- [ ] 目标解析 < 5秒
- [ ] 简单任务完成 < 60秒
- [ ] 页面加载 < 1秒

### 10.3 质量指标
- [ ] 单元测试覆盖率 > 70%
- [ ] 集成测试通过率 100%
- [ ] 无P0/P1 Bug
- [ ] 代码审查通过

---

**下一步**: 代码目录结构设计

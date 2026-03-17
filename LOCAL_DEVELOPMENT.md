# AI Work OS - 本地开发启动指南 (无Docker)

## 问题说明

如果您遇到Docker相关的问题，可以使用以下方法直接在本地启动项目。

---

## 📋 前置要求

### 必需软件
1. **Python 3.11+** - [下载](https://www.python.org/downloads/)
2. **Node.js 20+** - [下载](https://nodejs.org/)
3. **pnpm** - `npm install -g pnpm`
4. **PostgreSQL 15** - [下载](https://www.postgresql.org/download/)
5. **Redis 7** - [下载](https://redis.io/download/)

### 端口要求
确保以下端口未被占用：
- 3001 (前端)
- 8001 (后端)
- 5433 (PostgreSQL)
- 6380 (Redis)

---

## 🚀 Windows 启动步骤

### 1. 启动 PostgreSQL

```powershell
# 方法1: 使用服务
net start postgresql-x64-15

# 方法2: 手动启动 (如果已安装)
& "C:\Program Files\PostgreSQL\15\bin\pg_ctl.exe" start -D "C:\Program Files\PostgreSQL\15\data"
```

**配置 PostgreSQL 使用端口 5433:**
编辑 `postgresql.conf`:
```
port = 5433
```

然后重启 PostgreSQL。

### 2. 启动 Redis

```powershell
# 下载 Redis for Windows: https://github.com/microsoftarchive/redis/releases
# 启动 Redis 在端口 6380
redis-server --port 6380
```

### 3. 配置后端

```powershell
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
.\venv\Scripts\activate

# 安装依赖
pip install fastapi uvicorn sqlalchemy asyncpg psycopg2-binary alembic pydantic pydantic-settings python-jose[cryptography] passlib[bcrypt] python-multipart redis langchain langchain-openai langgraph openai httpx websockets

# 配置环境变量
copy .env.example .env
# 编辑 .env 文件，添加 OPENAI_API_KEY
```

### 4. 运行数据库迁移

```powershell
# 在 backend 目录下，确保虚拟环境已激活
alembic upgrade head
```

### 5. 启动后端

```powershell
# 在 backend 目录下
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

后端将在 http://localhost:8001 运行

### 6. 配置并启动前端

打开新的 PowerShell 窗口：

```powershell
cd frontend

# 安装依赖
pnpm install

# 配置环境变量
copy .env.local.example .env.local

# 启动前端
pnpm dev
```

前端将在 http://localhost:3001 运行

---

## 🍎 macOS 启动步骤

### 1. 安装依赖

```bash
# 使用 Homebrew 安装
brew install postgresql@15 redis

# 启动服务
brew services start postgresql@15
brew services start redis
```

### 2. 配置 PostgreSQL 端口

编辑 `/opt/homebrew/var/postgresql@15/postgresql.conf`:
```
port = 5433
```

重启 PostgreSQL:
```bash
brew services restart postgresql@15
```

### 3. 配置 Redis 端口

编辑 Redis 配置文件或使用命令行：
```bash
redis-server --port 6380
```

### 4. 启动项目

```bash
# 给脚本执行权限
chmod +x start-local.sh

# 运行启动脚本
./start-local.sh
```

---

## 🐧 Linux 启动步骤

### 1. 安装依赖

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql-15 redis-server python3 python3-pip nodejs npm

# 安装 pnpm
npm install -g pnpm
```

### 2. 配置 PostgreSQL

```bash
# 编辑配置文件
sudo nano /etc/postgresql/15/main/postgresql.conf

# 修改端口
port = 5433

# 重启服务
sudo service postgresql restart
```

### 3. 配置 Redis

```bash
# 编辑配置文件
sudo nano /etc/redis/redis.conf

# 修改端口
port 6380

# 重启服务
sudo service redis-server restart
```

### 4. 启动项目

```bash
chmod +x start-local.sh
./start-local.sh
```

---

## 🔧 故障排除

### 问题1: 端口被占用

```powershell
# Windows: 查看端口占用
netstat -ano | findstr ":3001"
netstat -ano | findstr ":8001"

# 结束占用进程
taskkill /PID <PID> /F
```

### 问题2: PostgreSQL 连接失败

```powershell
# 检查 PostgreSQL 状态
pg_isready -h localhost -p 5433

# 创建数据库 (如果需要)
psql -h localhost -p 5433 -U postgres -c "CREATE DATABASE ai_work_os;"
```

### 问题3: Redis 连接失败

```powershell
# 检查 Redis 状态
redis-cli -p 6380 ping

# 应该返回 PONG
```

### 问题4: 后端启动失败

```powershell
# 检查依赖是否安装
pip list | findstr fastapi

# 重新安装依赖
pip install -r requirements.txt
```

### 问题5: 前端启动失败

```powershell
# 删除 node_modules 重新安装
cd frontend
rm -rf node_modules
pnpm install
pnpm dev
```

---

## 📊 验证安装

启动成功后，访问以下地址：

- **前端**: http://localhost:3001
- **后端 API**: http://localhost:8001/docs
- **健康检查**: http://localhost:8001/health

---

## 🎯 常用命令

### 后端
```powershell
# 启动后端
uvicorn app.main:app --reload --port 8001

# 运行测试
pytest

# 数据库迁移
alembic revision --autogenerate -m "描述"
alembic upgrade head
alembic downgrade -1
```

### 前端
```powershell
# 启动前端
pnpm dev

# 构建
pnpm build

# 运行测试
pnpm test
```

---

## 📝 环境变量配置

### 后端 (.env)
```env
# Database (使用端口 5433)
DATABASE_URL=postgresql+asyncpg://admin:aiworkos_secret_2026@localhost:5433/ai_work_os
DATABASE_URL_SYNC=postgresql://admin:aiworkos_secret_2026@localhost:5433/ai_work_os

# Redis (使用端口 6380)
REDIS_URL=redis://localhost:6380/0

# OpenAI
OPENAI_API_KEY=sk-your-key-here

# JWT
JWT_SECRET=your-secret-key
```

### 前端 (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8001
NEXT_PUBLIC_WS_URL=ws://localhost:8001
```

---

## 🆘 获取帮助

如果仍有问题：

1. 检查所有服务是否已启动
2. 检查端口是否正确
3. 检查环境变量是否配置
4. 查看后端日志：`uvicorn app.main:app --reload --port 8001 --log-level debug`
5. 查看前端日志：`pnpm dev --verbose`

**GitHub Issues**: https://github.com/XTB-888/ai-work-os/issues

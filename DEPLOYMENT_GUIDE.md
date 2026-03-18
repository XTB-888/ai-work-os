# AI Work OS - 客户部署方案

## 🎯 面向客户的部署选项

根据客户需求和技术能力，提供以下部署方案：

---

## 方案 1: SaaS 云服务（推荐）

### 适用客户
- 不想管理基础设施
- 希望即开即用
- 按使用量付费

### 部署方式
**我们提供托管服务**：
- 客户访问 `https://app.aiworkos.com`
- 注册账号即可使用
- 无需安装任何软件

### 定价模式
| 套餐 | 月费 | 包含 |
|------|------|------|
| 免费版 | ¥0 | 3个项目/月，基础功能 |
| 专业版 | ¥99 | 无限项目，全部功能 |
| 企业版 | ¥999 | 私有部署，定制开发 |

### 优势
- ✅ 零维护成本
- ✅ 自动更新
- ✅ 数据备份
- ✅ 技术支持

---

## 方案 2: 一键安装包

### 适用客户
- 需要本地部署
- 有基本的技术能力
- 数据安全要求高

### Windows 安装包
```
AI-Work-OS-Setup.exe
```

**安装步骤**：
1. 下载安装包
2. 双击运行
3. 选择安装目录
4. 点击"安装"
5. 桌面生成快捷方式

**启动方式**：
- 双击桌面图标
- 或访问 http://localhost:3001

### 包含组件
- ✅ PostgreSQL（内置）
- ✅ Redis（内置）
- ✅ 后端服务
- ✅ 前端应用
- ✅ 系统托盘管理工具

---

## 方案 3: Docker 部署

### 适用客户
- 有 Docker 经验
- 需要灵活配置
- 已有服务器

### 快速部署
```bash
# 1. 下载部署包
wget https://github.com/XTB-888/ai-work-os/releases/download/v1.0/ai-work-os-docker.tar.gz
tar -xzf ai-work-os-docker.tar.gz
cd ai-work-os

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 3. 启动服务
docker-compose up -d

# 4. 访问
# http://localhost:3001
```

### 生产环境配置
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  app:
    image: aiworkos/ai-work-os:latest
    ports:
      - "80:3001"
      - "443:3001"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./data:/data
    restart: always
```

---

## 方案 4: 云服务器部署

### 适用客户
- 已有云服务器（阿里云/腾讯云/AWS）
- 需要公网访问
- 团队协作使用

### 阿里云部署示例

```bash
# 1. 购买 ECS 实例（推荐 2核4G）
# 2. 安装 Docker
curl -fsSL https://get.docker.com | sh

# 3. 下载部署脚本
curl -O https://raw.githubusercontent.com/XTB-888/ai-work-os/main/deploy/aliyun.sh
chmod +x aliyun.sh

# 4. 运行部署
./aliyun.sh

# 5. 配置域名（可选）
# 在阿里云控制台配置域名解析到服务器IP
```

### 腾讯云部署示例
```bash
# 类似步骤，使用腾讯云镜像
curl -O https://raw.githubusercontent.com/XTB-888/ai-work-os/main/deploy/tencent.sh
chmod +x tencent.sh
./tencent.sh
```

---

## 方案 5: Kubernetes 部署

### 适用客户
- 大型企业
- 已有 K8s 集群
- 需要高可用

### 部署文件
```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-work-os
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-work-os
  template:
    metadata:
      labels:
        app: ai-work-os
    spec:
      containers:
      - name: app
        image: aiworkos/ai-work-os:latest
        ports:
        - containerPort: 3001
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: aiworkos-secrets
              key: openai-key
```

部署命令：
```bash
kubectl apply -f k8s-deployment.yaml
kubectl apply -f k8s-service.yaml
kubectl apply -f k8s-ingress.yaml
```

---

## 🔐 安全配置

### 必需配置
1. **OpenAI API Key**
   - 客户需提供自己的 API Key
   - 或购买我们的 API 套餐

2. **JWT Secret**
   - 自动生成随机密钥
   - 或客户自定义

3. **数据库密码**
   - 强密码策略
   - 定期更换

### 可选配置
- SSL 证书（HTTPS）
- 域名绑定
- 备份策略
- 监控告警

---

## 📊 部署对比

| 方案 | 难度 | 成本 | 维护 | 适用场景 |
|------|------|------|------|----------|
| SaaS | ⭐ | ¥99/月 | 无 | 个人/小团队 |
| 安装包 | ⭐⭐ | 免费 | 低 | 本地使用 |
| Docker | ⭐⭐⭐ | 服务器费用 | 中 | 技术团队 |
| 云服务器 | ⭐⭐⭐ | ¥200/月 | 中 | 中小企业 |
| K8s | ⭐⭐⭐⭐⭐ | ¥1000+/月 | 高 | 大型企业 |

---

## 🚀 推荐部署路径

### 个人用户
**SaaS 免费版** → 注册即用

### 小团队（5-10人）
**SaaS 专业版** → 无需维护

### 中小企业（10-50人）
**云服务器部署** → 数据自主

### 大型企业（50+人）
**私有部署 + 定制开发** → 完全控制

---

## 💡 客户支持

### 技术支持
- 📧 邮箱：support@aiworkos.com
- 💬 微信：AIWorkOS
- 📱 电话：400-XXX-XXXX

### 培训服务
- 在线文档
- 视频教程
- 直播培训
- 现场培训（企业版）

### 定制开发
- 专属 Agent 开发
- 工作流定制
- 第三方集成
- 私有部署

---

## 📞 联系我们

**商务合作**: business@aiworkos.com  
**技术支持**: support@aiworkos.com  
**官方网站**: https://aiworkos.com

---

<div align="center">

**选择适合您的部署方案，开始 AI 自动化之旅！**

</div>

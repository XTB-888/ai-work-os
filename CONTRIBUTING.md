# Contributing to AI Work OS

Thank you for your interest in contributing to AI Work OS! This document provides guidelines and instructions for contributing.

## 🌟 Ways to Contribute

- 🐛 Report bugs
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit bug fixes
- ✨ Implement new features
- 🧪 Write tests
- 🎨 Improve UI/UX

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/ai-work-os.git
cd ai-work-os
```

### 2. Set Up Development Environment

Follow the instructions in [README.md](./README.md#development-setup) to set up your local development environment.

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## 📝 Development Guidelines

### Code Style

**Frontend (TypeScript/React)**
- Use TypeScript for type safety
- Follow ESLint and Prettier rules
- Use functional components with hooks
- Write meaningful component and variable names

**Backend (Python)**
- Follow PEP 8 style guide
- Use Black for code formatting
- Use Ruff for linting
- Write type hints for all functions

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(agents): add QA agent implementation

Implement QA agent with testing capabilities including:
- Functional testing
- Performance testing
- Security testing

Closes #123
```

### Testing

**Backend Tests**
```bash
cd backend
poetry run pytest
poetry run pytest --cov=app tests/
```

**Frontend Tests**
```bash
cd frontend
pnpm test
pnpm test:coverage
```

**E2E Tests**
```bash
cd frontend
pnpm test:e2e
```

### Documentation

- Update relevant documentation when adding features
- Add docstrings to Python functions
- Add JSDoc comments to TypeScript functions
- Update README if needed

## 🔍 Pull Request Process

### 1. Before Submitting

- ✅ Code follows style guidelines
- ✅ All tests pass
- ✅ New tests added for new features
- ✅ Documentation updated
- ✅ No merge conflicts

### 2. Submit Pull Request

1. Push your changes to your fork
2. Go to the original repository
3. Click "New Pull Request"
4. Select your branch
5. Fill in the PR template

### 3. PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe how you tested your changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
```

### 4. Review Process

- Maintainers will review your PR
- Address any feedback or requested changes
- Once approved, your PR will be merged

## 🐛 Reporting Bugs

### Before Reporting

- Check if the bug has already been reported
- Verify it's reproducible
- Collect relevant information

### Bug Report Template

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Windows 11]
- Browser: [e.g., Chrome 120]
- Version: [e.g., v1.0.0]

## Screenshots
If applicable

## Additional Context
Any other relevant information
```

## 💡 Suggesting Features

### Feature Request Template

```markdown
## Feature Description
Clear description of the feature

## Problem It Solves
What problem does this solve?

## Proposed Solution
How should it work?

## Alternatives Considered
Other solutions you've considered

## Additional Context
Any other relevant information
```

## 📚 Development Resources

### Documentation
- [System Architecture](./01-系统架构设计.md)
- [Database Schema](./02-数据库结构设计.md)
- [Agent Prompts](./03-Agent-Prompt设计.md)
- [MVP Plan](./04-MVP开发方案.md)
- [Code Structure](./05-代码目录结构设计.md)

### Useful Links
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)

## 🤝 Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone.

### Our Standards

**Positive behavior:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community

**Unacceptable behavior:**
- Trolling, insulting/derogatory comments
- Public or private harassment
- Publishing others' private information
- Other conduct which could reasonably be considered inappropriate

### Enforcement

Instances of abusive behavior may be reported to the project team. All complaints will be reviewed and investigated.

## 📞 Getting Help

- 💬 Join our [Discord](https://discord.gg/aiworkos)
- 📧 Email: support@aiworkos.com
- 🐦 Twitter: [@aiworkos](https://twitter.com/aiworkos)
- 📖 Documentation: [docs](./docs)

## 🙏 Thank You!

Your contributions make AI Work OS better for everyone. We appreciate your time and effort!

---

**Happy Contributing! 🎉**

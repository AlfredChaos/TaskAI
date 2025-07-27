# TaskAI Backend

基于 FastAPI 和 SQLite 构建的现代化 Web 后端服务框架。

## 特性

- 🚀 **FastAPI**: 高性能、现代化的 Python Web 框架
- 🗄️ **SQLite**: 轻量级的关系型数据库
- 🔐 **JWT 认证**: 安全的用户认证和授权
- 📊 **SQLAlchemy ORM**: 强大的数据库 ORM
- 🔄 **Alembic 迁移**: 数据库版本控制
- 📝 **Pydantic 验证**: 数据验证和序列化
- 🏗️ **分层架构**: 清晰的代码组织结构
- 📚 **自动文档**: Swagger/OpenAPI 文档
- 🧪 **测试支持**: 完整的测试框架
- 🔧 **开发工具**: 代码格式化、类型检查等

## 项目结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 应用入口
│   ├── api/                    # API 路由
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── auth.py     # 认证相关端点
│   │           ├── users.py    # 用户管理端点
│   │           └── health.py   # 健康检查端点
│   ├── core/                   # 核心功能
│   │   ├── __init__.py
│   │   ├── config.py          # 配置管理
│   │   ├── security.py        # 安全相关
│   │   └── dependencies.py    # 依赖注入
│   ├── models/                 # 数据模型
│   │   ├── __init__.py
│   │   ├── base.py            # 基础模型
│   │   └── user.py            # 用户模型
│   ├── schemas/                # Pydantic 模式
│   │   ├── __init__.py
│   │   ├── base.py            # 基础模式
│   │   ├── user.py            # 用户模式
│   │   └── token.py           # 令牌模式
│   ├── services/               # 业务逻辑
│   │   ├── __init__.py
│   │   ├── user_service.py    # 用户服务
│   │   └── auth_service.py    # 认证服务
│   └── database.py            # 数据库配置
├── alembic/                   # 数据库迁移
│   ├── versions/              # 迁移文件
│   ├── env.py                 # 迁移环境
│   └── script.py.mako         # 迁移模板
├── alembic.ini                # Alembic 配置
├── requirements.txt           # Python 依赖
├── .env.example              # 环境变量示例
└── README.md                 # 项目文档
```

## 快速开始

### 1. 环境准备

确保已安装以下软件：
- Python 3.8+
- pip

### 2. 克隆项目

```bash
git clone <repository-url>
cd taskAI/backend
```

### 3. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
```

### 5. 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置数据库路径等信息。SQLite 数据库文件将自动创建。

### 6. 数据库迁移

```bash
# 初始化迁移（仅首次）
alembic revision --autogenerate -m "Initial migration"

# 执行迁移
alembic upgrade head
```

### 7. 启动服务

```bash
# 开发模式
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 或使用 Python 直接运行
python -m app.main
```

### 8. 访问文档

启动后访问以下地址：
- API 文档: http://localhost:8000/docs
- ReDoc 文档: http://localhost:8000/redoc
- 健康检查: http://localhost:8000/api/v1/health

## API 端点

### 认证相关
- `POST /api/v1/auth/register` - 用户注册
- `POST /api/v1/auth/login` - 用户登录
- `POST /api/v1/auth/refresh` - 刷新令牌
- `POST /api/v1/auth/logout` - 用户登出
- `GET /api/v1/auth/me` - 获取当前用户信息

### 用户管理
- `GET /api/v1/users` - 获取用户列表（管理员）
- `POST /api/v1/users` - 创建用户（管理员）
- `GET /api/v1/users/me` - 获取当前用户详情
- `PUT /api/v1/users/me` - 更新当前用户信息
- `PUT /api/v1/users/me/password` - 修改密码
- `GET /api/v1/users/{user_id}` - 获取指定用户（管理员）
- `PUT /api/v1/users/{user_id}` - 更新指定用户（管理员）
- `DELETE /api/v1/users/{user_id}` - 删除用户（管理员）

### 健康检查
- `GET /api/v1/health` - 基础健康检查
- `GET /api/v1/health/detailed` - 详细健康检查
- `GET /api/v1/health/ready` - 就绪检查
- `GET /api/v1/health/live` - 存活检查

## 开发指南

### 代码规范

项目使用以下工具确保代码质量：

```bash
# 代码格式化
black app/

# 导入排序
isort app/

# 代码检查
flake8 app/

# 类型检查
mypy app/
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=app

# 运行特定测试文件
pytest tests/test_auth.py
```

### 数据库迁移

```bash
# 创建新迁移
alembic revision --autogenerate -m "描述迁移内容"

# 执行迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1

# 查看迁移历史
alembic history
```

## 部署

### Docker 部署（推荐）

```bash
# 构建镜像
docker build -t taskai-backend .

# 运行容器
docker run -d -p 8000:8000 --env-file .env taskai-backend
```

### 生产环境部署

```bash
# 使用 Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 环境变量

| 变量名 | 描述 | 默认值 |
|--------|------|--------|
| `DATABASE_URL` | SQLite 数据库连接字符串 | sqlite:///./taskai.db |
| `DB_PATH` | SQLite 数据库文件路径 | ./taskai.db |
| `SECRET_KEY` | JWT 密钥 | - |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 访问令牌过期时间（分钟） | 30 |
| `REFRESH_TOKEN_EXPIRE_DAYS` | 刷新令牌过期时间（天） | 7 |
| `ALGORITHM` | JWT 算法 | HS256 |
| `ENVIRONMENT` | 运行环境 | development |
| `DEBUG` | 调试模式 | True |
| `CORS_ORIGINS` | CORS 允许的源 | ["*"] |
| `REDIS_URL` | Redis 连接字符串 | - |

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 支持

如果您遇到问题或有建议，请：
1. 查看 [文档](docs/)
2. 搜索 [Issues](../../issues)
3. 创建新的 [Issue](../../issues/new)

## 更新日志

查看 [CHANGELOG.md](CHANGELOG.md) 了解版本更新信息。
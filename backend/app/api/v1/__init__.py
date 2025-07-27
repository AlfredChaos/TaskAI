"""API v1版本包"""

from fastapi import APIRouter
from .endpoints import auth, users, health, ai_providers, ai_chat

# 创建API路由器
api_router = APIRouter(prefix="/api/v1")

# 注册路由
api_router.include_router(
    health.router,
    prefix="/health",
    tags=["健康检查"]
)

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["认证"]
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["用户管理"]
)

api_router.include_router(
    ai_providers.router,
    prefix="/ai/providers",
    tags=["AI供应商"]
)

api_router.include_router(
    ai_chat.router,
    prefix="/ai/chat",
    tags=["AI聊天"]
)

__all__ = ["api_router"]
"""JWT令牌相关的Pydantic模式"""

from typing import Optional
from pydantic import BaseModel, Field
from .base import BaseSchema


class Token(BaseSchema):
    """JWT令牌响应模式"""
    
    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field(default="bearer", description="令牌类型")
    expires_in: int = Field(..., description="令牌过期时间（秒）")
    refresh_token: Optional[str] = Field(None, description="刷新令牌")


class TokenData(BaseSchema):
    """JWT令牌数据模式"""
    
    username: Optional[str] = Field(None, description="用户名")
    user_id: Optional[int] = Field(None, description="用户ID")
    scopes: list[str] = Field(default_factory=list, description="权限范围")
    exp: Optional[int] = Field(None, description="过期时间戳")
    iat: Optional[int] = Field(None, description="签发时间戳")


class TokenRefresh(BaseSchema):
    """刷新令牌请求模式"""
    
    refresh_token: str = Field(..., description="刷新令牌")


class TokenVerify(BaseSchema):
    """验证令牌请求模式"""
    
    token: str = Field(..., description="要验证的令牌")
"""用户相关的Pydantic模式"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator
from .base import BaseSchema, TimestampMixin, IDMixin
import re


class UserBase(BaseSchema):
    """用户基础模式"""
    
    username: str = Field(
        ..., 
        min_length=3, 
        max_length=50,
        description="用户名，3-50个字符"
    )
    email: EmailStr = Field(..., description="邮箱地址")
    full_name: Optional[str] = Field(
        None, 
        max_length=100,
        description="全名"
    )
    phone: Optional[str] = Field(
        None, 
        max_length=20,
        description="电话号码"
    )
    bio: Optional[str] = Field(
        None, 
        max_length=500,
        description="个人简介"
    )
    
    @validator('username')
    def validate_username(cls, v):
        """验证用户名格式"""
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('用户名只能包含字母、数字和下划线')
        return v
    
    @validator('phone')
    def validate_phone(cls, v):
        """验证电话号码格式"""
        if v and not re.match(r'^[\d\-\+\(\)\s]+$', v):
            raise ValueError('电话号码格式不正确')
        return v


class UserCreate(UserBase):
    """创建用户模式"""
    
    password: str = Field(
        ..., 
        min_length=8, 
        max_length=100,
        description="密码，至少8个字符"
    )
    confirm_password: str = Field(
        ..., 
        description="确认密码"
    )
    
    @validator('password')
    def validate_password(cls, v):
        """验证密码强度"""
        if len(v) < 8:
            raise ValueError('密码至少需要8个字符')
        if not re.search(r'[A-Za-z]', v):
            raise ValueError('密码必须包含字母')
        if not re.search(r'\d', v):
            raise ValueError('密码必须包含数字')
        return v
    
    @validator('confirm_password')
    def validate_confirm_password(cls, v, values):
        """验证确认密码"""
        if 'password' in values and v != values['password']:
            raise ValueError('两次输入的密码不一致')
        return v


class UserUpdate(BaseSchema):
    """更新用户模式"""
    
    username: Optional[str] = Field(
        None, 
        min_length=3, 
        max_length=50,
        description="用户名"
    )
    email: Optional[EmailStr] = Field(None, description="邮箱地址")
    full_name: Optional[str] = Field(
        None, 
        max_length=100,
        description="全名"
    )
    phone: Optional[str] = Field(
        None, 
        max_length=20,
        description="电话号码"
    )
    bio: Optional[str] = Field(
        None, 
        max_length=500,
        description="个人简介"
    )
    avatar_url: Optional[str] = Field(
        None, 
        max_length=255,
        description="头像URL"
    )
    
    @validator('username')
    def validate_username(cls, v):
        """验证用户名格式"""
        if v and not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('用户名只能包含字母、数字和下划线')
        return v


class UserResponse(UserBase, IDMixin, TimestampMixin):
    """用户响应模式"""
    
    avatar_url: Optional[str] = Field(None, description="头像URL")
    is_verified: bool = Field(default=False, description="是否已验证")
    is_active: bool = Field(default=True, description="是否激活")
    is_superuser: bool = Field(default=False, description="是否为超级用户")


class UserLogin(BaseSchema):
    """用户登录模式"""
    
    username: str = Field(..., description="用户名或邮箱")
    password: str = Field(..., description="密码")
    remember_me: bool = Field(default=False, description="记住我")


class UserPasswordChange(BaseSchema):
    """修改密码模式"""
    
    current_password: str = Field(..., description="当前密码")
    new_password: str = Field(
        ..., 
        min_length=8, 
        max_length=100,
        description="新密码"
    )
    confirm_password: str = Field(..., description="确认新密码")
    
    @validator('new_password')
    def validate_new_password(cls, v):
        """验证新密码强度"""
        if len(v) < 8:
            raise ValueError('密码至少需要8个字符')
        if not re.search(r'[A-Za-z]', v):
            raise ValueError('密码必须包含字母')
        if not re.search(r'\d', v):
            raise ValueError('密码必须包含数字')
        return v
    
    @validator('confirm_password')
    def validate_confirm_password(cls, v, values):
        """验证确认密码"""
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('两次输入的密码不一致')
        return v


class UserList(BaseSchema, IDMixin, TimestampMixin):
    """用户列表项模式"""
    
    username: str = Field(..., description="用户名")
    email: str = Field(..., description="邮箱")
    full_name: Optional[str] = Field(None, description="全名")
    avatar_url: Optional[str] = Field(None, description="头像URL")
    is_verified: bool = Field(..., description="是否已验证")
    is_active: bool = Field(..., description="是否激活")
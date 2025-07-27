"""AI供应商相关的Pydantic模式"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, validator, field_validator
from .base import BaseSchema, IDMixin, TimestampMixin


class AIProviderBase(BaseSchema):
    """AI供应商基础模式"""
    
    name: str = Field(..., min_length=1, max_length=100, description="供应商名称")
    base_url: str = Field(..., min_length=1, max_length=500, description="API基础URL")
    is_active: bool = Field(default=True, description="是否激活")
    is_default: bool = Field(default=False, description="是否为默认供应商")
    
    @validator('base_url')
    def validate_base_url(cls, v):
        """验证base_url格式"""
        if not v.startswith(('http://', 'https://')):
            raise ValueError('base_url必须以http://或https://开头')
        return v.rstrip('/')


class AIProviderCreate(AIProviderBase):
    """创建AI供应商模式"""
    
    api_key: str = Field(..., min_length=1, description="API密钥")


class AIProviderUpdate(BaseSchema):
    """更新AI供应商模式"""
    
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="供应商名称")
    base_url: Optional[str] = Field(None, min_length=1, max_length=500, description="API基础URL")
    api_key: Optional[str] = Field(None, min_length=1, description="API密钥")
    is_active: Optional[bool] = Field(None, description="是否激活")
    is_default: Optional[bool] = Field(None, description="是否为默认供应商")
    
    @validator('base_url')
    def validate_base_url(cls, v):
        """验证base_url格式"""
        if v is not None:
            if not v.startswith(('http://', 'https://')):
                raise ValueError('base_url必须以http://或https://开头')
            return v.rstrip('/')
        return v


class AIProviderResponse(AIProviderBase, IDMixin, TimestampMixin):
    """AI供应商响应模式"""
    
    user_id: str = Field(..., description="所属用户ID（雪花ID）")
    
    @field_validator('user_id', mode='before')
    @classmethod
    def convert_user_id_to_string(cls, v):
        """将用户ID转换为字符串"""
        if v is not None and isinstance(v, int):
            return str(v)
        return v
    
    class Config:
        from_attributes = True


class AIProviderList(BaseSchema, IDMixin, TimestampMixin):
    """AI供应商列表模式"""
    
    name: str = Field(..., description="供应商名称")
    base_url: str = Field(..., description="API基础URL")
    is_active: bool = Field(..., description="是否激活")
    is_default: bool = Field(..., description="是否为默认供应商")
    
    class Config:
        from_attributes = True


class AIProviderSetDefault(BaseSchema):
    """设置默认供应商模式"""
    
    provider_id: str = Field(..., description="供应商ID（雪花ID）")
    
    @field_validator('provider_id', mode='before')
    @classmethod
    def convert_provider_id_to_string(cls, v):
        """将供应商ID转换为字符串"""
        if v is not None and isinstance(v, int):
            return str(v)
        return v
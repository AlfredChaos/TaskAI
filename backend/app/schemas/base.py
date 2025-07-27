"""基础Pydantic模式"""

from typing import Any, Dict, Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

DataType = TypeVar('DataType')


class BaseResponse(BaseModel):
    """基础响应模式"""
    
    success: bool = Field(default=True, description="请求是否成功")
    message: str = Field(default="操作成功", description="响应消息")
    code: int = Field(default=200, description="响应状态码")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="响应时间戳")
    
    model_config = {
        "json_encoders": {
            datetime: lambda v: v.isoformat()
        }
    }


class DataResponse(BaseResponse, Generic[DataType]):
    """带数据的响应模式"""
    
    data: Optional[DataType] = Field(default=None, description="响应数据")


class ErrorResponse(BaseResponse):
    """错误响应模式"""
    
    success: bool = Field(default=False, description="请求是否成功")
    error_type: Optional[str] = Field(default=None, description="错误类型")
    error_details: Optional[Dict[str, Any]] = Field(default=None, description="错误详情")


class PaginationMeta(BaseModel):
    """分页元数据"""
    
    page: int = Field(description="当前页码")
    size: int = Field(description="每页大小")
    total: int = Field(description="总记录数")
    pages: int = Field(description="总页数")
    has_next: bool = Field(description="是否有下一页")
    has_prev: bool = Field(description="是否有上一页")
    
    @classmethod
    def create(cls, page: int, size: int, total: int) -> "PaginationMeta":
        """创建分页元数据
        
        Args:
            page (int): 当前页码
            size (int): 每页大小
            total (int): 总记录数
            
        Returns:
            PaginationMeta: 分页元数据实例
        """
        pages = (total + size - 1) // size if total > 0 else 0
        return cls(
            page=page,
            size=size,
            total=total,
            pages=pages,
            has_next=page < pages,
            has_prev=page > 1
        )


class PaginatedResponse(BaseResponse, Generic[DataType]):
    """分页响应模式"""
    
    data: List[DataType] = Field(default_factory=list, description="数据列表")
    meta: PaginationMeta = Field(description="分页元数据")


class BaseSchema(BaseModel):
    """基础Schema类"""
    
    model_config = {
        # 允许使用ORM模式
        "from_attributes": True,
        # 验证赋值
        "validate_assignment": True,
        # 使用枚举值
        "use_enum_values": True,
        # JSON编码器
        "json_encoders": {
            datetime: lambda v: v.isoformat() if v else None
        }
    }


class TimestampMixin(BaseModel):
    """时间戳混入类"""
    
    created_at: Optional[datetime] = Field(default=None, description="创建时间")
    updated_at: Optional[datetime] = Field(default=None, description="更新时间")
    
    model_config = {
        "json_encoders": {
            datetime: lambda v: v.isoformat() if v else None
        }
    }


class IDMixin(BaseModel):
    """ID混入类"""
    
    id: Optional[str] = Field(default=None, description="记录ID（雪花ID）")
    
    @field_validator('id', mode='before')
    @classmethod
    def convert_id_to_string(cls, v):
        """将整数ID转换为字符串"""
        if v is not None and isinstance(v, int):
            return str(v)
        return v
"""基础模型类"""

from sqlalchemy import Column, BigInteger, DateTime, Boolean
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime
from app.database import Base
from app.utils.snowflake import generate_snowflake_id


class BaseModel(Base):
    """基础模型类，包含通用字段"""
    
    __abstract__ = True
    
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=False, comment="主键ID（雪花ID）")
    created_at = Column(
        DateTime, 
        default=datetime.utcnow, 
        nullable=False,
        comment="创建时间"
    )
    updated_at = Column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow,
        nullable=False,
        comment="更新时间"
    )
    is_active = Column(
        Boolean, 
        default=True, 
        nullable=False,
        comment="是否激活"
    )
    is_deleted = Column(
        Boolean, 
        default=False, 
        nullable=False,
        comment="是否删除（软删除）"
    )
    
    def __init__(self, **kwargs):
        """初始化模型，自动生成雪花ID"""
        if 'id' not in kwargs or kwargs['id'] is None:
            kwargs['id'] = generate_snowflake_id()
        super().__init__(**kwargs)
    
    @declared_attr
    def __tablename__(cls):
        """自动生成表名（类名转下划线格式）"""
        import re
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', cls.__name__)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
    
    def to_dict(self, exclude_fields=None):
        """将模型转换为字典
        
        Args:
            exclude_fields (list): 要排除的字段列表
            
        Returns:
            dict: 模型字典表示
        """
        exclude_fields = exclude_fields or []
        result = {}
        
        for column in self.__table__.columns:
            if column.name not in exclude_fields:
                value = getattr(self, column.name)
                if isinstance(value, datetime):
                    value = value.isoformat()
                elif column.name == 'id' and value is not None:
                    # 雪花ID在JSON中以字符串形式返回
                    value = str(value)
                result[column.name] = value
                
        return result
    
    def update_from_dict(self, data: dict, exclude_fields=None):
        """从字典更新模型字段
        
        Args:
            data (dict): 要更新的数据
            exclude_fields (list): 要排除的字段列表
        """
        exclude_fields = exclude_fields or ['id', 'created_at']
        
        for key, value in data.items():
            if key not in exclude_fields and hasattr(self, key):
                setattr(self, key, value)
    
    def soft_delete(self):
        """软删除记录"""
        self.is_deleted = True
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def restore(self):
        """恢复软删除的记录"""
        self.is_deleted = False
        self.is_active = True
        self.updated_at = datetime.utcnow()
    
    def __repr__(self):
        """模型的字符串表示"""
        return f"<{self.__class__.__name__}(id={self.id})>"
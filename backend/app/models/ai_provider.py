"""AI供应商模型"""

from sqlalchemy import Column, BigInteger, String, Text, Boolean
from .base import BaseModel


class AIProvider(BaseModel):
    """AI供应商模型"""
    
    __tablename__ = "ai_providers"
    
    name = Column(String(100), nullable=False, comment="供应商名称")
    base_url = Column(String(500), nullable=False, comment="API基础URL")
    encrypted_api_key = Column(Text, nullable=False, comment="加密的API密钥")
    is_default = Column(Boolean, default=False, comment="是否为默认供应商")
    user_id = Column(BigInteger, nullable=False, comment="所属用户ID（雪花ID）")
    
    def __repr__(self):
        return f"<AIProvider(id={self.id}, name='{self.name}', user_id={self.user_id})>"
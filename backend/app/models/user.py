"""用户模型"""

from sqlalchemy import Column, String, Boolean, Text
from sqlalchemy.orm import relationship
from .base import BaseModel


class User(BaseModel):
    """用户模型类"""

    __tablename__ = "users"

    # 基本信息
    username = Column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
        comment="用户名"
    )
    email = Column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
        comment="邮箱地址"
    )
    hashed_password = Column(
        String(255),
        nullable=False,
        comment="加密后的密码"
    )

    # 个人信息
    full_name = Column(
        String(100),
        nullable=True,
        comment="全名"
    )
    phone = Column(
        String(20),
        nullable=True,
        comment="电话号码"
    )
    avatar_url = Column(
        String(255),
        nullable=True,
        comment="头像URL"
    )
    bio = Column(
        Text,
        nullable=True,
        comment="个人简介"
    )

    # 状态字段
    is_verified = Column(
        Boolean,
        default=False,
        nullable=False,
        comment="是否已验证邮箱"
    )
    is_superuser = Column(
        Boolean,
        default=False,
        nullable=False,
        comment="是否为超级用户"
    )

    def __repr__(self):
        """用户模型的字符串表示"""
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

    def to_dict(self, exclude_fields=None):
        """转换为字典，默认排除敏感字段"""
        default_exclude = ['hashed_password']
        if exclude_fields:
            default_exclude.extend(exclude_fields)
        return super().to_dict(exclude_fields=default_exclude)

    @property
    def is_admin(self) -> bool:
        """判断是否为管理员"""
        return self.is_superuser

    def check_permission(self, permission: str) -> bool:
        """检查用户权限（示例方法，可根据需要扩展）

        Args:
            permission (str): 权限名称

        Returns:
            bool: 是否有权限
        """
        if self.is_superuser:
            return True

        # 这里可以添加更复杂的权限检查逻辑
        # 例如：检查用户角色、权限表等

        return False

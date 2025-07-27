"""FastAPI依赖注入"""

from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..services.auth_service import AuthService

# HTTP Bearer认证方案
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """获取当前用户
    
    Args:
        credentials (HTTPAuthorizationCredentials): HTTP Bearer凭据
        db (Session): 数据库会话
        
    Returns:
        User: 当前用户对象
        
    Raises:
        HTTPException: 认证失败时抛出异常
    """
    auth_service = AuthService(db)
    return auth_service.get_current_user(credentials.credentials)


def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """获取当前激活用户
    
    Args:
        current_user (User): 当前用户
        
    Returns:
        User: 当前激活用户对象
        
    Raises:
        HTTPException: 用户未激活时抛出异常
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="用户账户已被停用"
        )
    return current_user


def get_current_superuser(
    current_user: User = Depends(get_current_user)
) -> User:
    """获取当前超级用户
    
    Args:
        current_user (User): 当前用户
        
    Returns:
        User: 当前超级用户对象
        
    Raises:
        HTTPException: 用户不是超级用户时抛出异常
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    return current_user


def get_current_verified_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """获取当前已验证用户
    
    Args:
        current_user (User): 当前激活用户
        
    Returns:
        User: 当前已验证用户对象
        
    Raises:
        HTTPException: 用户未验证时抛出异常
    """
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户邮箱未验证"
        )
    return current_user


def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """获取可选的当前用户（允许匿名访问）
    
    Args:
        credentials (Optional[HTTPAuthorizationCredentials]): HTTP Bearer凭据
        db (Session): 数据库会话
        
    Returns:
        Optional[User]: 当前用户对象或None
    """
    if not credentials:
        return None
    
    try:
        auth_service = AuthService(db)
        return auth_service.get_current_user(credentials.credentials)
    except HTTPException:
        return None


class PermissionChecker:
    """权限检查器"""
    
    def __init__(self, required_permissions: list[str]):
        self.required_permissions = required_permissions
    
    def __call__(self, current_user: User = Depends(get_current_active_user)) -> User:
        """检查用户权限
        
        Args:
            current_user (User): 当前用户
            
        Returns:
            User: 有权限的用户对象
            
        Raises:
            HTTPException: 权限不足时抛出异常
        """
        # 超级用户拥有所有权限
        if current_user.is_superuser:
            return current_user
        
        # 检查用户权限（这里可以根据实际需求实现权限检查逻辑）
        # 例如：检查用户角色、权限表等
        user_permissions = self._get_user_permissions(current_user)
        
        for permission in self.required_permissions:
            if permission not in user_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"缺少权限: {permission}"
                )
        
        return current_user
    
    def _get_user_permissions(self, user: User) -> list[str]:
        """获取用户权限列表
        
        Args:
            user (User): 用户对象
            
        Returns:
            list[str]: 用户权限列表
        """
        # 这里可以根据实际需求实现权限获取逻辑
        # 例如：从数据库查询用户角色和权限
        permissions = []
        
        # 基础权限
        if user.is_active:
            permissions.extend(["read:profile", "update:profile"])
        
        # 管理员权限
        if user.is_admin():
            permissions.extend([
                "read:users", "create:users", "update:users", "delete:users"
            ])
        
        return permissions


# 常用权限检查器实例
require_admin = PermissionChecker(["admin"])
require_user_read = PermissionChecker(["read:users"])
require_user_write = PermissionChecker(["create:users", "update:users"])
require_user_delete = PermissionChecker(["delete:users"])


def get_pagination_params(
    page: int = 1,
    size: int = 20,
    max_size: int = 100
) -> dict:
    """获取分页参数
    
    Args:
        page (int): 页码，默认为1
        size (int): 每页大小，默认为20
        max_size (int): 最大每页大小，默认为100
        
    Returns:
        dict: 分页参数字典
        
    Raises:
        HTTPException: 参数无效时抛出异常
    """
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="页码必须大于0"
        )
    
    if size < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="每页大小必须大于0"
        )
    
    if size > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"每页大小不能超过{max_size}"
        )
    
    return {
        "page": page,
        "size": size,
        "skip": (page - 1) * size,
        "limit": size
    }


def get_search_params(
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: str = "asc"
) -> dict:
    """获取搜索参数
    
    Args:
        search (Optional[str]): 搜索关键词
        sort_by (Optional[str]): 排序字段
        sort_order (str): 排序顺序，默认为"asc"
        
    Returns:
        dict: 搜索参数字典
        
    Raises:
        HTTPException: 参数无效时抛出异常
    """
    if sort_order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="排序顺序必须是'asc'或'desc'"
        )
    
    return {
        "search": search.strip() if search else None,
        "sort_by": sort_by,
        "sort_order": sort_order
    }
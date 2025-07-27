"""用户服务"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from fastapi import HTTPException, status
from passlib.context import CryptContext

from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from ..core.security import get_password_hash, verify_password


class UserService:
    """用户服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """根据ID获取用户
        
        Args:
            user_id (int): 用户ID
            
        Returns:
            Optional[User]: 用户对象或None
        """
        return self.db.query(User).filter(
            and_(User.id == user_id, User.is_deleted == False)
        ).first()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户
        
        Args:
            username (str): 用户名
            
        Returns:
            Optional[User]: 用户对象或None
        """
        return self.db.query(User).filter(
            and_(User.username == username, User.is_deleted == False)
        ).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """根据邮箱获取用户
        
        Args:
            email (str): 邮箱地址
            
        Returns:
            Optional[User]: 用户对象或None
        """
        return self.db.query(User).filter(
            and_(User.email == email, User.is_deleted == False)
        ).first()
    
    def get_user_by_username_or_email(self, identifier: str) -> Optional[User]:
        """根据用户名或邮箱获取用户
        
        Args:
            identifier (str): 用户名或邮箱
            
        Returns:
            Optional[User]: 用户对象或None
        """
        return self.db.query(User).filter(
            and_(
                or_(User.username == identifier, User.email == identifier),
                User.is_deleted == False
            )
        ).first()
    
    def create_user(self, user_data: UserCreate) -> User:
        """创建新用户
        
        Args:
            user_data (UserCreate): 用户创建数据
            
        Returns:
            User: 创建的用户对象
            
        Raises:
            HTTPException: 用户名或邮箱已存在时抛出异常
        """
        # 检查用户名是否已存在
        if self.get_user_by_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )
        
        # 检查邮箱是否已存在
        if self.get_user_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已存在"
            )
        
        # 创建用户
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            phone=user_data.phone,
            bio=user_data.bio
        )
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        
        return db_user
    
    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """更新用户信息
        
        Args:
            user_id (int): 用户ID
            user_data (UserUpdate): 更新数据
            
        Returns:
            Optional[User]: 更新后的用户对象或None
            
        Raises:
            HTTPException: 用户名或邮箱已存在时抛出异常
        """
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            return None
        
        # 检查用户名是否已被其他用户使用
        if user_data.username and user_data.username != db_user.username:
            existing_user = self.get_user_by_username(user_data.username)
            if existing_user and existing_user.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="用户名已存在"
                )
        
        # 检查邮箱是否已被其他用户使用
        if user_data.email and user_data.email != db_user.email:
            existing_user = self.get_user_by_email(user_data.email)
            if existing_user and existing_user.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="邮箱已存在"
                )
        
        # 更新用户信息
        update_data = user_data.dict(exclude_unset=True)
        db_user.update_from_dict(update_data)
        
        self.db.commit()
        self.db.refresh(db_user)
        
        return db_user
    
    def delete_user(self, user_id: int) -> bool:
        """删除用户（软删除）
        
        Args:
            user_id (int): 用户ID
            
        Returns:
            bool: 删除是否成功
        """
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            return False
        
        db_user.soft_delete()
        self.db.commit()
        
        return True
    
    def get_users(
        self, 
        skip: int = 0, 
        limit: int = 100,
        search: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> List[User]:
        """获取用户列表
        
        Args:
            skip (int): 跳过的记录数
            limit (int): 限制返回的记录数
            search (Optional[str]): 搜索关键词
            is_active (Optional[bool]): 是否激活状态过滤
            
        Returns:
            List[User]: 用户列表
        """
        query = self.db.query(User).filter(User.is_deleted == False)
        
        # 搜索过滤
        if search:
            search_filter = or_(
                User.username.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%"),
                User.full_name.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        # 激活状态过滤
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        
        return query.offset(skip).limit(limit).all()
    
    def count_users(
        self, 
        search: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> int:
        """统计用户数量
        
        Args:
            search (Optional[str]): 搜索关键词
            is_active (Optional[bool]): 是否激活状态过滤
            
        Returns:
            int: 用户数量
        """
        query = self.db.query(User).filter(User.is_deleted == False)
        
        # 搜索过滤
        if search:
            search_filter = or_(
                User.username.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%"),
                User.full_name.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        # 激活状态过滤
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        
        return query.count()
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """验证用户身份
        
        Args:
            username (str): 用户名或邮箱
            password (str): 密码
            
        Returns:
            Optional[User]: 验证成功返回用户对象，否则返回None
        """
        user = self.get_user_by_username_or_email(username)
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        return user
    
    def change_password(self, user_id: int, current_password: str, new_password: str) -> bool:
        """修改用户密码
        
        Args:
            user_id (int): 用户ID
            current_password (str): 当前密码
            new_password (str): 新密码
            
        Returns:
            bool: 修改是否成功
            
        Raises:
            HTTPException: 当前密码错误时抛出异常
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        # 验证当前密码
        if not verify_password(current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="当前密码错误"
            )
        
        # 更新密码
        user.hashed_password = get_password_hash(new_password)
        self.db.commit()
        
        return True
    
    def activate_user(self, user_id: int) -> bool:
        """激活用户
        
        Args:
            user_id (int): 用户ID
            
        Returns:
            bool: 激活是否成功
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        user.is_active = True
        self.db.commit()
        
        return True
    
    def deactivate_user(self, user_id: int) -> bool:
        """停用用户
        
        Args:
            user_id (int): 用户ID
            
        Returns:
            bool: 停用是否成功
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        user.is_active = False
        self.db.commit()
        
        return True
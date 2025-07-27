"""认证服务"""

from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..models.user import User
from ..schemas.token import Token, TokenData
from ..config import get_settings
from .token_service import TokenService

settings = get_settings()


class AuthService:
    """认证服务类"""

    def __init__(self, db: Session):
        from .user_service import UserService
        self.db = db
        self.user_service = UserService(db)
        self.token_service = TokenService()

    def create_access_token(
        self,
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """创建访问令牌

        Args:
            data (Dict[str, Any]): 要编码的数据
            expires_delta (Optional[timedelta]): 过期时间增量

        Returns:
            str: JWT访问令牌
        """
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.access_token_expire_minutes
            )

        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        })

        encoded_jwt = jwt.encode(
            to_encode,
            settings.secret_key,
            algorithm=settings.algorithm
        )

        return encoded_jwt

    def create_refresh_token(
        self,
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """创建刷新令牌

        Args:
            data (Dict[str, Any]): 要编码的数据
            expires_delta (Optional[timedelta]): 过期时间增量

        Returns:
            str: JWT刷新令牌
        """
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                days=settings.REFRESH_TOKEN_EXPIRE_DAYS
            )

        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh"
        })

        encoded_jwt = jwt.encode(
            to_encode,
            settings.secret_key,
            algorithm=settings.algorithm
        )

        return encoded_jwt

    def verify_token(self, token: str, token_type: str = "access") -> TokenData:
        """验证令牌

        Args:
            token (str): JWT令牌
            token_type (str): 令牌类型（access或refresh）

        Returns:
            TokenData: 令牌数据

        Raises:
            HTTPException: 令牌无效时抛出异常
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无法验证凭据",
            headers={"WWW-Authenticate": "Bearer"},
        )

        # 首先检查token是否在Redis中存在
        redis_token_data = self.token_service.verify_token(token, token_type)
        if not redis_token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="令牌已失效或不存在",
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            payload = jwt.decode(
                token,
                settings.secret_key,
                algorithms=[settings.algorithm]
            )

            # 检查令牌类型
            if payload.get("type") != token_type:
                raise credentials_exception

            username: str = payload.get("sub")
            user_id: int = payload.get("user_id")

            if username is None or user_id is None:
                raise credentials_exception

            # 验证Redis中的user_id与JWT中的user_id是否一致
            if redis_token_data.get("user_id") != user_id:
                raise credentials_exception

            token_data = TokenData(
                username=username,
                user_id=user_id,
                exp=payload.get("exp"),
                iat=payload.get("iat")
            )

        except JWTError:
            raise credentials_exception

        return token_data

    def get_current_user(self, token: str) -> User:
        """根据令牌获取当前用户

        Args:
            token (str): JWT访问令牌

        Returns:
            User: 当前用户对象

        Raises:
            HTTPException: 用户不存在或未激活时抛出异常
        """
        token_data = self.verify_token(token, "access")

        user = self.user_service.get_user_by_id(token_data.user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户不存在",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户账户已被停用"
            )

        return user

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """验证用户身份

        Args:
            username (str): 用户名或邮箱
            password (str): 密码

        Returns:
            Optional[User]: 验证成功返回用户对象，否则返回None
        """
        return self.user_service.authenticate_user(username, password)

    def login(self, username: str, password: str, remember_me: bool = False) -> Token:
        """用户登录

        Args:
            username (str): 用户名或邮箱
            password (str): 密码
            remember_me (bool): 是否记住登录状态

        Returns:
            Token: 令牌信息

        Raises:
            HTTPException: 认证失败时抛出异常
        """
        user = self.authenticate_user(username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户账户已被停用"
            )

        # 创建令牌数据
        token_data = {
            "sub": user.username,
            "user_id": user.id,
            "email": user.email
        }

        # 设置过期时间
        access_token_expires = timedelta(
            minutes=settings.access_token_expire_minutes
        )

        if remember_me:
            # 记住登录状态时延长访问令牌有效期
            access_token_expires = timedelta(
                days=settings.REFRESH_TOKEN_EXPIRE_DAYS
            )

        # 创建访问令牌
        access_token = self.create_access_token(
            data=token_data,
            expires_delta=access_token_expires
        )

        # 创建刷新令牌
        refresh_token = self.create_refresh_token(data=token_data)

        # 将token存储到Redis
        self.token_service.store_token(access_token, user.id, "access")
        self.token_service.store_token(refresh_token, user.id, "refresh")

        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=int(access_token_expires.total_seconds()),
            refresh_token=refresh_token
        )

    def refresh_token(self, refresh_token: str) -> Token:
        """刷新访问令牌

        Args:
            refresh_token (str): 刷新令牌

        Returns:
            Token: 新的令牌信息

        Raises:
            HTTPException: 刷新令牌无效时抛出异常
        """
        try:
            token_data = self.verify_token(refresh_token, "refresh")
        except HTTPException:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="刷新令牌无效",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # 验证用户是否存在且激活
        user = self.user_service.get_user_by_id(token_data.user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户不存在或已被停用",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # 创建新的令牌数据
        new_token_data = {
            "sub": user.username,
            "user_id": user.id,
            "email": user.email
        }

        # 创建新的访问令牌
        access_token_expires = timedelta(
            minutes=settings.access_token_expire_minutes
        )
        access_token = self.create_access_token(
            data=new_token_data,
            expires_delta=access_token_expires
        )

        # 创建新的刷新令牌
        new_refresh_token = self.create_refresh_token(data=new_token_data)

        # 撤销旧的刷新令牌
        self.token_service.revoke_token(refresh_token, "refresh")

        # 将新token存储到Redis
        self.token_service.store_token(access_token, user.id, "access")
        self.token_service.store_token(new_refresh_token, user.id, "refresh")

        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=int(access_token_expires.total_seconds()),
            refresh_token=new_refresh_token
        )

    def verify_token_endpoint(self, token: str) -> Dict[str, Any]:
        """验证令牌端点

        Args:
            token (str): 要验证的令牌

        Returns:
            Dict[str, Any]: 验证结果
        """
        try:
            token_data = self.verify_token(token, "access")
            user = self.user_service.get_user_by_id(token_data.user_id)

            if not user or not user.is_active:
                return {
                    "valid": False,
                    "message": "用户不存在或已被停用"
                }

            return {
                "valid": True,
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "exp": token_data.exp,
                "iat": token_data.iat
            }

        except HTTPException:
            return {
                "valid": False,
                "message": "令牌无效或已过期"
            }

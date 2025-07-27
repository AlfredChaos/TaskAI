"""安全相关功能"""

from datetime import datetime, timedelta
from typing import Any, Union, Optional
from jose import jwt
from passlib.context import CryptContext
from ..config import get_settings

settings = get_settings()

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    """创建访问令牌

    Args:
        subject (Union[str, Any]): 令牌主题（通常是用户名或用户ID）
        expires_delta (timedelta, optional): 过期时间增量

    Returns:
        str: JWT访问令牌
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "iat": datetime.utcnow()
    }

    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )

    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码

    Args:
        plain_password (str): 明文密码
        hashed_password (str): 哈希密码

    Returns:
        bool: 密码是否匹配
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """获取密码哈希值

    Args:
        password (str): 明文密码

    Returns:
        str: 哈希密码
    """
    return pwd_context.hash(password)


def verify_token(token: str) -> Optional[str]:
    """验证JWT令牌

    Args:
        token (str): JWT令牌

    Returns:
        Optional[str]: 令牌主题（用户名）或None
    """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except jwt.JWTError:
        return None


def create_password_reset_token(email: str) -> str:
    """创建密码重置令牌

    Args:
        email (str): 用户邮箱

    Returns:
        str: 密码重置令牌
    """
    delta = timedelta(hours=24)  # 24小时过期
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email, "type": "reset"},
        settings.secret_key,
        algorithm=settings.algorithm,
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    """验证密码重置令牌

    Args:
        token (str): 密码重置令牌

    Returns:
        Optional[str]: 用户邮箱或None
    """
    try:
        decoded_token = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        if decoded_token.get("type") != "reset":
            return None
        return decoded_token["sub"]
    except jwt.JWTError:
        return None


def create_email_verification_token(email: str) -> str:
    """创建邮箱验证令牌

    Args:
        email (str): 用户邮箱

    Returns:
        str: 邮箱验证令牌
    """
    delta = timedelta(hours=24)  # 24小时过期
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email, "type": "verification"},
        settings.secret_key,
        algorithm=settings.algorithm,
    )
    return encoded_jwt


def verify_email_verification_token(token: str) -> Optional[str]:
    """验证邮箱验证令牌

    Args:
        token (str): 邮箱验证令牌

    Returns:
        Optional[str]: 用户邮箱或None
    """
    try:
        decoded_token = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        if decoded_token.get("type") != "verification":
            return None
        return decoded_token["sub"]
    except jwt.JWTError:
        return None


def generate_api_key() -> str:
    """生成API密钥

    Returns:
        str: API密钥
    """
    import secrets
    return secrets.token_urlsafe(32)


def hash_api_key(api_key: str) -> str:
    """哈希API密钥

    Args:
        api_key (str): API密钥

    Returns:
        str: 哈希后的API密钥
    """
    return get_password_hash(api_key)


def verify_api_key(plain_api_key: str, hashed_api_key: str) -> bool:
    """验证API密钥

    Args:
        plain_api_key (str): 明文API密钥
        hashed_api_key (str): 哈希API密钥

    Returns:
        bool: API密钥是否匹配
    """
    return verify_password(plain_api_key, hashed_api_key)

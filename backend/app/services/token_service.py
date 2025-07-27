"""Token管理服务"""

import json
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from jose import jwt, JWTError
from ..core.redis_client import RedisClient
from ..config import get_settings

settings = get_settings()


class TokenService:
    """Token管理服务类"""
    
    def __init__(self):
        self.redis = RedisClient.get_instance()
        self.access_token_prefix = "access_token:"
        self.refresh_token_prefix = "refresh_token:"
        self.user_tokens_prefix = "user_tokens:"
    
    def _get_token_key(self, token: str, token_type: str = "access") -> str:
        """生成token在Redis中的键名
        
        Args:
            token (str): JWT token
            token_type (str): token类型 (access/refresh)
            
        Returns:
            str: Redis键名
        """
        prefix = self.access_token_prefix if token_type == "access" else self.refresh_token_prefix
        return f"{prefix}{token}"
    
    def _get_user_tokens_key(self, user_id: int) -> str:
        """生成用户token列表在Redis中的键名
        
        Args:
            user_id (int): 用户ID
            
        Returns:
            str: Redis键名
        """
        return f"{self.user_tokens_prefix}{user_id}"
    
    def _decode_token_payload(self, token: str) -> Optional[Dict[str, Any]]:
        """解码JWT token获取payload
        
        Args:
            token (str): JWT token
            
        Returns:
            Optional[Dict[str, Any]]: token payload或None
        """
        try:
            payload = jwt.decode(
                token,
                settings.secret_key,
                algorithms=[settings.algorithm]
            )
            return payload
        except JWTError:
            return None
    
    def store_token(self, token: str, user_id: int, token_type: str = "access") -> bool:
        """将token存储到Redis
        
        Args:
            token (str): JWT token
            user_id (int): 用户ID
            token_type (str): token类型 (access/refresh)
            
        Returns:
            bool: 存储是否成功
        """
        try:
            # 解码token获取过期时间
            payload = self._decode_token_payload(token)
            if not payload:
                return False
            
            exp_timestamp = payload.get("exp")
            if not exp_timestamp:
                return False
            
            # 计算TTL（秒）
            exp_datetime = datetime.fromtimestamp(exp_timestamp)
            ttl = int((exp_datetime - datetime.utcnow()).total_seconds())
            
            if ttl <= 0:
                return False
            
            # 存储token信息
            token_key = self._get_token_key(token, token_type)
            token_data = {
                "user_id": user_id,
                "token_type": token_type,
                "created_at": datetime.utcnow().isoformat(),
                "expires_at": exp_datetime.isoformat()
            }
            
            # 设置token数据和过期时间
            self.redis.setex(token_key, ttl, json.dumps(token_data))
            
            # 将token添加到用户token列表
            user_tokens_key = self._get_user_tokens_key(user_id)
            self.redis.sadd(user_tokens_key, token)
            
            # 设置用户token列表的过期时间（比最长的refresh token稍长）
            max_ttl = max(ttl, settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600 + 3600)
            self.redis.expire(user_tokens_key, max_ttl)
            
            return True
            
        except Exception as e:
            print(f"存储token失败: {e}")
            return False
    
    def verify_token(self, token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
        """验证token是否存在且有效
        
        Args:
            token (str): JWT token
            token_type (str): token类型 (access/refresh)
            
        Returns:
            Optional[Dict[str, Any]]: token数据或None
        """
        try:
            token_key = self._get_token_key(token, token_type)
            token_data_str = self.redis.get(token_key)
            
            if not token_data_str:
                return None
            
            token_data = json.loads(token_data_str)
            
            # 验证token类型
            if token_data.get("token_type") != token_type:
                return None
            
            return token_data
            
        except Exception as e:
            print(f"验证token失败: {e}")
            return None
    
    def revoke_token(self, token: str, token_type: str = "access") -> bool:
        """撤销单个token
        
        Args:
            token (str): JWT token
            token_type (str): token类型 (access/refresh)
            
        Returns:
            bool: 撤销是否成功
        """
        try:
            # 获取token数据
            token_data = self.verify_token(token, token_type)
            if not token_data:
                return False
            
            user_id = token_data.get("user_id")
            if not user_id:
                return False
            
            # 删除token
            token_key = self._get_token_key(token, token_type)
            self.redis.delete(token_key)
            
            # 从用户token列表中移除
            user_tokens_key = self._get_user_tokens_key(user_id)
            self.redis.srem(user_tokens_key, token)
            
            return True
            
        except Exception as e:
            print(f"撤销token失败: {e}")
            return False
    
    def revoke_user_tokens(self, user_id: int, token_type: Optional[str] = None) -> bool:
        """撤销用户的所有token
        
        Args:
            user_id (int): 用户ID
            token_type (Optional[str]): token类型，None表示所有类型
            
        Returns:
            bool: 撤销是否成功
        """
        try:
            user_tokens_key = self._get_user_tokens_key(user_id)
            tokens = self.redis.smembers(user_tokens_key)
            
            if not tokens:
                return True
            
            revoked_count = 0
            for token in tokens:
                # 如果指定了token类型，只撤销该类型的token
                if token_type:
                    token_data = self.verify_token(token, token_type)
                    if token_data:
                        if self.revoke_token(token, token_type):
                            revoked_count += 1
                else:
                    # 尝试撤销access token
                    if self.revoke_token(token, "access"):
                        revoked_count += 1
                    # 尝试撤销refresh token
                    elif self.revoke_token(token, "refresh"):
                        revoked_count += 1
            
            # 如果撤销了所有token，清空用户token列表
            if not token_type and revoked_count > 0:
                remaining_tokens = self.redis.smembers(user_tokens_key)
                if not remaining_tokens:
                    self.redis.delete(user_tokens_key)
            
            return True
            
        except Exception as e:
            print(f"撤销用户token失败: {e}")
            return False
    
    def get_user_active_tokens(self, user_id: int) -> Dict[str, int]:
        """获取用户活跃token数量
        
        Args:
            user_id (int): 用户ID
            
        Returns:
            Dict[str, int]: 各类型token数量
        """
        try:
            user_tokens_key = self._get_user_tokens_key(user_id)
            tokens = self.redis.smembers(user_tokens_key)
            
            access_count = 0
            refresh_count = 0
            
            for token in tokens:
                if self.verify_token(token, "access"):
                    access_count += 1
                elif self.verify_token(token, "refresh"):
                    refresh_count += 1
            
            return {
                "access_tokens": access_count,
                "refresh_tokens": refresh_count,
                "total": access_count + refresh_count
            }
            
        except Exception as e:
            print(f"获取用户活跃token失败: {e}")
            return {"access_tokens": 0, "refresh_tokens": 0, "total": 0}
    
    def cleanup_expired_tokens(self) -> int:
        """清理过期的token（Redis会自动处理，这里主要用于统计）
        
        Returns:
            int: 清理的token数量
        """
        # Redis的TTL机制会自动清理过期的key
        # 这个方法主要用于手动清理和统计
        try:
            # 可以在这里添加额外的清理逻辑
            # 比如清理孤立的用户token列表等
            return 0
        except Exception as e:
            print(f"清理过期token失败: {e}")
            return 0
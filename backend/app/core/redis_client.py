"""Redis客户端配置"""

import redis
from typing import Optional
from ..config import get_settings

settings = get_settings()


class RedisClient:
    """Redis客户端单例类"""
    
    _instance: Optional[redis.Redis] = None
    
    @classmethod
    def get_instance(cls) -> redis.Redis:
        """获取Redis客户端实例
        
        Returns:
            redis.Redis: Redis客户端实例
        """
        if cls._instance is None:
            cls._instance = redis.from_url(
                settings.redis_url,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30
            )
        return cls._instance
    
    @classmethod
    def close(cls) -> None:
        """关闭Redis连接"""
        if cls._instance:
            cls._instance.close()
            cls._instance = None
    
    @classmethod
    def ping(cls) -> bool:
        """检查Redis连接状态
        
        Returns:
            bool: 连接是否正常
        """
        try:
            # 直接创建新的连接进行测试
            test_client = redis.from_url(
                settings.redis_url,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            result = test_client.ping()
            test_client.close()
            return result
        except Exception as e:
            print(f"Redis连接错误: {e}")
            return False


# 全局Redis客户端实例将在需要时创建
# redis_client = RedisClient.get_instance()
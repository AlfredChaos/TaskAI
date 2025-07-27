"""应用配置管理模块"""

from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import field_validator
from functools import lru_cache
import os


class Settings(BaseSettings):
    """应用配置类，使用Pydantic管理环境变量"""

    # 应用基础配置
    app_name: str = "TaskAI Backend"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "production"

    # 服务器配置
    host: str = "0.0.0.0"
    port: int = 8000

    # 数据库配置
    database_url: Optional[str] = None
    db_path: str = "./taskai.db"

    # JWT配置
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Redis配置
    redis_url: str = "redis://:root@localhost:6379/0"

    # CORS配置
    allowed_origins: List[str] = ["http://localhost:3000"]

    # 日志配置
    log_level: str = "INFO"
    log_file: str = "logs/app.log"

    @field_validator('allowed_origins', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        """解析CORS允许的源地址"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v

    @property
    def database_url_complete(self) -> str:
        """构建完整的数据库连接URL"""
        if self.database_url:
            return self.database_url
        return f"sqlite:///{self.db_path}"

    @property
    def is_development(self) -> bool:
        """判断是否为开发环境"""
        return self.environment.lower() in ["development", "dev"]

    @property
    def is_production(self) -> bool:
        """判断是否为生产环境"""
        return self.environment.lower() in ["production", "prod"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """获取应用配置实例（单例模式）"""
    return Settings()


# 全局配置实例
settings = get_settings()

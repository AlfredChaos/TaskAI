"""数据库连接和会话管理模块"""

from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Generator
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# 数据库引擎配置
engine_kwargs = {
    "echo": settings.debug,  # 是否打印SQL语句
}

# SQLite特定配置
if "sqlite" in settings.database_url_complete:
    engine_kwargs.update({
        "poolclass": StaticPool,
        "connect_args": {
            "check_same_thread": False,  # 允许多线程访问
            "timeout": 20,  # 连接超时时间
        },
    })

# 如果是开发环境，添加额外配置
if settings.is_development:
    engine_kwargs.update({
        "echo": True,
        "future": True,
    })

# 创建数据库引擎
try:
    engine = create_engine(
        settings.database_url_complete,
        **engine_kwargs
    )
    if "sqlite" in settings.database_url_complete:
        logger.info(f"SQLite数据库引擎创建成功: {settings.db_path}")
    else:
        logger.info(f"数据库引擎创建成功: {settings.database_url_complete}")
except Exception as e:
    logger.error(f"数据库引擎创建失败: {e}")
    raise

# 创建会话工厂
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 创建基础模型类
Base = declarative_base()

# 元数据对象
metadata = MetaData()


def get_db() -> Generator[Session, None, None]:
    """获取数据库会话的依赖注入函数
    
    Yields:
        Session: SQLAlchemy数据库会话
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"数据库会话异常: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def create_tables():
    """创建所有数据库表"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("数据库表创建成功")
    except Exception as e:
        logger.error(f"数据库表创建失败: {e}")
        raise


def drop_tables():
    """删除所有数据库表（谨慎使用）"""
    try:
        Base.metadata.drop_all(bind=engine)
        logger.warning("所有数据库表已删除")
    except Exception as e:
        logger.error(f"数据库表删除失败: {e}")
        raise


def check_db_connection() -> bool:
    """检查数据库连接是否正常
    
    Returns:
        bool: 连接状态
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        logger.info("数据库连接检查成功")
        return True
    except Exception as e:
        logger.error(f"数据库连接检查失败: {e}")
        return False
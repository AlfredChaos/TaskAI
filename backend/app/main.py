"""FastAPI主应用程序"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError
import time
import uvicorn
import json

from .config import get_settings
from .database import create_tables, check_db_connection
from .api.v1 import api_router
from .schemas.base import ErrorResponse
from .utils.snowflake import init_snowflake_generator
from .core.redis_client import RedisClient

# 获取配置
settings = get_settings()

# 配置日志
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log") if settings.environment != "development" else logging.NullHandler()
    ]
)

logger = logging.getLogger(__name__)


def custom_json_serializer(obj):
    """自定义JSON序列化器，处理datetime对象"""
    from datetime import datetime
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    logger.info("应用启动中...")
    
    try:
        # 初始化雪花ID生成器
        logger.info("初始化雪花ID生成器...")
        init_snowflake_generator(machine_id=1, datacenter_id=1)
        
        # 创建数据库表
        logger.info("创建数据库表...")
        create_tables()
        
        # 检查数据库连接
        logger.info("检查数据库连接...")
        db_healthy = check_db_connection()
        if not db_healthy:
            logger.error("数据库连接失败")
            raise Exception("数据库连接失败")
        
        # 初始化Redis连接
        logger.info("初始化Redis连接...")
        redis_healthy = RedisClient.ping()
        if not redis_healthy:
            logger.error("Redis连接失败")
            raise Exception("Redis连接失败")
        
        logger.info("应用启动完成")
        
    except Exception as e:
        logger.error(f"应用启动失败: {e}")
        raise
    
    yield
    
    # 关闭时执行
    logger.info("应用关闭中...")
    try:
        # 关闭Redis连接
        logger.info("关闭Redis连接...")
        RedisClient.close()
        logger.info("Redis连接已关闭")
    except Exception as e:
        logger.error(f"关闭Redis连接失败: {e}")
    
    logger.info("应用关闭完成")


# 创建FastAPI应用实例
app = FastAPI(
    title=settings.app_name,
    description="TaskAI Backend API - 基于FastAPI构建的现代化Web后端服务",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json" if settings.environment != "production" else None,
    docs_url="/docs" if settings.environment != "production" else None,
    redoc_url="/redoc" if settings.environment != "production" else None,
    lifespan=lifespan
)

# CORS中间件
if settings.allowed_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.allowed_origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# 受信任主机中间件
if settings.environment == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"]  # 可以根据需要配置具体的主机列表
    )


# 请求处理时间中间件
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """添加请求处理时间头"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# 请求日志中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """记录请求日志"""
    start_time = time.time()
    
    # 记录请求信息
    logger.info(
        f"请求开始: {request.method} {request.url} - "
        f"客户端: {request.client.host if request.client else 'unknown'}"
    )
    
    response = await call_next(request)
    
    # 记录响应信息
    process_time = time.time() - start_time
    logger.info(
        f"请求完成: {request.method} {request.url} - "
        f"状态码: {response.status_code} - "
        f"处理时间: {process_time:.4f}s"
    )
    
    return response


# 全局异常处理器
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """HTTP异常处理器"""
    logger.error(f"HTTP异常: {exc.status_code} - {exc.detail} - URL: {request.url}")
    
    error_response = ErrorResponse(
        success=False,
        message=exc.detail,
        code=exc.status_code,
        error_type="HTTPException"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=json.loads(json.dumps(error_response.model_dump(), default=custom_json_serializer))
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """请求验证异常处理器"""
    logger.error(f"请求验证错误: {exc.errors()} - URL: {request.url}")
    
    error_response = ErrorResponse(
        success=False,
        message="请求数据验证失败",
        code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error_type="ValidationError",
        error_details={
            "errors": exc.errors(),
            "body": exc.body
        }
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=json.loads(json.dumps(error_response.model_dump(), default=custom_json_serializer))
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """SQLAlchemy异常处理器"""
    logger.error(f"数据库错误: {str(exc)} - URL: {request.url}")
    
    error_response = ErrorResponse(
        success=False,
        message="数据库操作失败",
        code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_type="DatabaseError"
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=json.loads(json.dumps(error_response.model_dump(), default=custom_json_serializer))
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """通用异常处理器"""
    logger.error(f"未处理的异常: {str(exc)} - URL: {request.url}", exc_info=True)
    
    error_response = ErrorResponse(
        success=False,
        message="服务器内部错误",
        code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_type="InternalServerError"
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=json.loads(json.dumps(error_response.model_dump(), default=custom_json_serializer))
    )


# 根路径
@app.get("/", tags=["根路径"])
async def root():
    """根路径欢迎信息"""
    return {
        "message": "欢迎使用TaskAI Backend API",
        "version": "1.0.0",
        "docs": "/docs" if settings.environment != "production" else None,
        "environment": settings.environment
    }


# 注册API路由
app.include_router(api_router)


if __name__ == "__main__":
    # 开发环境直接运行
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.environment == "development",
        log_level=settings.log_level.lower(),
        access_log=True
    )
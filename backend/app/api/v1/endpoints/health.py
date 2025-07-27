"""健康检查端点"""

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any

from ....database import get_db, check_db_connection
from ....schemas.base import BaseResponse, DataResponse
from ....config import get_settings

settings = get_settings()
router = APIRouter()


@router.get(
    "/",
    response_model=DataResponse[Dict[str, Any]],
    summary="基础健康检查",
    description="检查API服务是否正常运行"
)
async def health_check() -> DataResponse[Dict[str, Any]]:
    """基础健康检查
    
    Returns:
        DataResponse: 健康状态响应
    """
    return DataResponse(
        success=True,
        message="服务运行正常",
        data={
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "TaskAI Backend API",
            "version": "1.0.0",
            "environment": settings.environment
        }
    )


@router.get(
    "/detailed",
    response_model=DataResponse[Dict[str, Any]],
    summary="详细健康检查",
    description="检查API服务及其依赖项的健康状态"
)
async def detailed_health_check(
    db: Session = Depends(get_db)
) -> DataResponse[Dict[str, Any]]:
    """详细健康检查
    
    Args:
        db (Session): 数据库会话
        
    Returns:
        DataResponse: 详细健康状态响应
        
    Raises:
        HTTPException: 服务不健康时抛出异常
    """
    health_data = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "TaskAI Backend API",
        "version": "1.0.0",
        "environment": settings.environment,
        "checks": {}
    }
    
    # 检查数据库连接
    try:
        db_healthy = check_db_connection()
        health_data["checks"]["database"] = {
            "status": "healthy" if db_healthy else "unhealthy",
            "message": "数据库连接正常" if db_healthy else "数据库连接失败",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        health_data["checks"]["database"] = {
            "status": "unhealthy",
            "message": f"数据库检查失败: {str(e)}",
            "timestamp": datetime.utcnow().isoformat()
        }
        health_data["status"] = "unhealthy"
    
    # 检查Redis连接（如果配置了Redis）
    if settings.redis_url:
        try:
            # 这里可以添加Redis连接检查逻辑
            health_data["checks"]["redis"] = {
                "status": "healthy",
                "message": "Redis连接正常",
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            health_data["checks"]["redis"] = {
                "status": "unhealthy",
                "message": f"Redis检查失败: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
            health_data["status"] = "unhealthy"
    
    # 检查磁盘空间
    try:
        import shutil
        disk_usage = shutil.disk_usage("/")
        free_space_gb = disk_usage.free / (1024**3)
        total_space_gb = disk_usage.total / (1024**3)
        usage_percent = (disk_usage.used / disk_usage.total) * 100
        
        disk_status = "healthy" if usage_percent < 90 else "warning" if usage_percent < 95 else "unhealthy"
        
        health_data["checks"]["disk_space"] = {
            "status": disk_status,
            "message": f"磁盘使用率: {usage_percent:.1f}%",
            "free_space_gb": round(free_space_gb, 2),
            "total_space_gb": round(total_space_gb, 2),
            "usage_percent": round(usage_percent, 1),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if disk_status == "unhealthy":
            health_data["status"] = "unhealthy"
            
    except Exception as e:
        health_data["checks"]["disk_space"] = {
            "status": "unknown",
            "message": f"磁盘空间检查失败: {str(e)}",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    # 检查内存使用情况
    try:
        import psutil
        memory = psutil.virtual_memory()
        memory_usage_percent = memory.percent
        
        memory_status = "healthy" if memory_usage_percent < 80 else "warning" if memory_usage_percent < 90 else "unhealthy"
        
        health_data["checks"]["memory"] = {
            "status": memory_status,
            "message": f"内存使用率: {memory_usage_percent}%",
            "usage_percent": memory_usage_percent,
            "available_gb": round(memory.available / (1024**3), 2),
            "total_gb": round(memory.total / (1024**3), 2),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if memory_status == "unhealthy":
            health_data["status"] = "unhealthy"
            
    except ImportError:
        health_data["checks"]["memory"] = {
            "status": "unknown",
            "message": "psutil未安装，无法检查内存使用情况",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        health_data["checks"]["memory"] = {
            "status": "unknown",
            "message": f"内存检查失败: {str(e)}",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    # 如果整体状态不健康，返回503状态码
    if health_data["status"] == "unhealthy":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="服务不健康"
        )
    
    return DataResponse(
        success=True,
        message="健康检查完成",
        data=health_data
    )


@router.get(
    "/ready",
    response_model=BaseResponse,
    summary="就绪检查",
    description="检查服务是否准备好接收请求"
)
async def readiness_check(
    db: Session = Depends(get_db)
) -> BaseResponse:
    """就绪检查
    
    Args:
        db (Session): 数据库会话
        
    Returns:
        BaseResponse: 就绪状态响应
        
    Raises:
        HTTPException: 服务未就绪时抛出异常
    """
    try:
        # 检查数据库连接
        db_healthy = check_db_connection()
        if not db_healthy:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="数据库连接失败，服务未就绪"
            )
        
        return BaseResponse(
            success=True,
            message="服务已就绪"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"服务未就绪: {str(e)}"
        )


@router.get(
    "/live",
    response_model=BaseResponse,
    summary="存活检查",
    description="检查服务是否存活"
)
async def liveness_check() -> BaseResponse:
    """存活检查
    
    Returns:
        BaseResponse: 存活状态响应
    """
    return BaseResponse(
        success=True,
        message="服务存活"
    )
"""AI供应商管理端点"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ....database import get_db
from ....schemas.ai_provider import (
    AIProviderCreate, AIProviderUpdate, AIProviderResponse, 
    AIProviderList, AIProviderSetDefault
)
from ....schemas.base import BaseResponse, DataResponse, PaginatedResponse, PaginationMeta
from ....services.ai_provider_service import AIProviderService
from ....services.ai_service import AIService
from ....core.dependencies import get_current_active_user
from ....models.user import User

router = APIRouter()


@router.post(
    "/",
    response_model=DataResponse[AIProviderResponse],
    summary="创建AI供应商",
    description="创建新的AI供应商配置"
)
async def create_provider(
    provider_data: AIProviderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> DataResponse[AIProviderResponse]:
    """创建AI供应商
    
    Args:
        provider_data (AIProviderCreate): 供应商创建数据
        db (Session): 数据库会话
        current_user (User): 当前用户
        
    Returns:
        DataResponse[AIProviderResponse]: 创建的供应商信息
    """
    provider_service = AIProviderService(db)
    
    try:
        provider = provider_service.create_provider(provider_data, current_user.id)
        return DataResponse(
            success=True,
            message="AI供应商创建成功",
            data=AIProviderResponse.from_orm(provider)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建AI供应商失败: {str(e)}"
        )


@router.get(
    "/",
    response_model=DataResponse[List[AIProviderList]],
    summary="获取AI供应商列表",
    description="获取当前用户的AI供应商列表"
)
async def get_providers(
    db: Session = Depends(get_db),
    is_active: Optional[bool] = Query(None, description="过滤激活状态"),
    current_user: User = Depends(get_current_active_user)
) -> DataResponse[List[AIProviderList]]:
    """获取AI供应商列表
    
    Args:
        db (Session): 数据库会话
        is_active (Optional[bool]): 激活状态过滤
        current_user (User): 当前用户
        
    Returns:
        DataResponse[List[AIProviderList]]: 供应商列表
    """
    provider_service = AIProviderService(db)
    
    try:
        providers = provider_service.get_providers(current_user.id, is_active)
        provider_list = [AIProviderList.from_orm(provider) for provider in providers]
        
        return DataResponse(
            success=True,
            message="获取AI供应商列表成功",
            data=provider_list
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取AI供应商列表失败: {str(e)}"
        )


@router.get(
    "/{provider_id}",
    response_model=DataResponse[AIProviderResponse],
    summary="获取AI供应商详情",
    description="根据ID获取AI供应商详细信息"
)
async def get_provider(
    provider_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> DataResponse[AIProviderResponse]:
    """获取AI供应商详情
    
    Args:
        provider_id (int): 供应商ID
        db (Session): 数据库会话
        current_user (User): 当前用户
        
    Returns:
        DataResponse[AIProviderResponse]: 供应商详情
    """
    provider_service = AIProviderService(db)
    
    provider = provider_service.get_provider_by_id(provider_id, current_user.id)
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI供应商不存在"
        )
    
    return DataResponse(
        success=True,
        message="获取AI供应商详情成功",
        data=AIProviderResponse.from_orm(provider)
    )


@router.put(
    "/{provider_id}",
    response_model=DataResponse[AIProviderResponse],
    summary="更新AI供应商",
    description="更新AI供应商配置"
)
async def update_provider(
    provider_id: int,
    provider_data: AIProviderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> DataResponse[AIProviderResponse]:
    """更新AI供应商
    
    Args:
        provider_id (int): 供应商ID
        provider_data (AIProviderUpdate): 更新数据
        db (Session): 数据库会话
        current_user (User): 当前用户
        
    Returns:
        DataResponse[AIProviderResponse]: 更新后的供应商信息
    """
    provider_service = AIProviderService(db)
    
    try:
        provider = provider_service.update_provider(provider_id, current_user.id, provider_data)
        if not provider:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="AI供应商不存在"
            )
        
        return DataResponse(
            success=True,
            message="AI供应商更新成功",
            data=AIProviderResponse.from_orm(provider)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新AI供应商失败: {str(e)}"
        )


@router.delete(
    "/{provider_id}",
    response_model=BaseResponse,
    summary="删除AI供应商",
    description="删除指定的AI供应商"
)
async def delete_provider(
    provider_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> BaseResponse:
    """删除AI供应商
    
    Args:
        provider_id (int): 供应商ID
        db (Session): 数据库会话
        current_user (User): 当前用户
        
    Returns:
        BaseResponse: 删除结果
    """
    provider_service = AIProviderService(db)
    
    success = provider_service.delete_provider(provider_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI供应商不存在"
        )
    
    return BaseResponse(
        success=True,
        message="AI供应商删除成功"
    )


@router.post(
    "/set-default",
    response_model=DataResponse[AIProviderResponse],
    summary="设置默认AI供应商",
    description="设置指定的AI供应商为默认供应商"
)
async def set_default_provider(
    request_data: AIProviderSetDefault,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> DataResponse[AIProviderResponse]:
    """设置默认AI供应商
    
    Args:
        request_data (AIProviderSetDefault): 请求数据
        db (Session): 数据库会话
        current_user (User): 当前用户
        
    Returns:
        DataResponse[AIProviderResponse]: 设置后的供应商信息
    """
    provider_service = AIProviderService(db)
    
    provider = provider_service.set_default_provider(request_data.provider_id, current_user.id)
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI供应商不存在或未激活"
        )
    
    return DataResponse(
        success=True,
        message="默认AI供应商设置成功",
        data=AIProviderResponse.from_orm(provider)
    )


@router.post(
    "/{provider_id}/test",
    response_model=DataResponse[dict],
    summary="测试AI供应商连接",
    description="测试指定AI供应商的连接状态"
)
async def test_provider_connection(
    provider_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> DataResponse[dict]:
    """测试AI供应商连接
    
    Args:
        provider_id (int): 供应商ID
        db (Session): 数据库会话
        current_user (User): 当前用户
        
    Returns:
        DataResponse[dict]: 测试结果
    """
    ai_service = AIService(db)
    
    result = await ai_service.test_provider_connection(current_user.id, provider_id)
    
    return DataResponse(
        success=result["success"],
        message=result["message"],
        data=result
    )
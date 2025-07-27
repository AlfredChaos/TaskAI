"""用户管理端点"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ....database import get_db
from ....schemas.user import (
    UserCreate, UserUpdate, UserResponse, UserList, UserPasswordChange
)
from ....schemas.base import BaseResponse, DataResponse, PaginatedResponse, PaginationMeta
from ....services.user_service import UserService
from ....core.dependencies import (
    get_current_user, get_current_active_user, get_current_superuser,
    get_pagination_params, get_search_params
)
from ....models.user import User

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[UserList],
    summary="获取用户列表",
    description="获取用户列表，支持分页和搜索"
)
async def get_users(
    db: Session = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    search_params: dict = Depends(get_search_params),
    is_active: Optional[bool] = Query(None, description="过滤激活状态"),
    current_user: User = Depends(get_current_superuser)
) -> PaginatedResponse[UserList]:
    """获取用户列表

    Args:
        db (Session): 数据库会话
        pagination (dict): 分页参数
        search_params (dict): 搜索参数
        is_active (Optional[bool]): 激活状态过滤
        current_user (User): 当前用户（需要超级用户权限）

    Returns:
        PaginatedResponse[UserList]: 分页用户列表
    """
    user_service = UserService(db)

    try:
        # 获取用户列表
        users = user_service.get_users(
            skip=pagination["skip"],
            limit=pagination["limit"],
            search=search_params["search"],
            is_active=is_active
        )

        # 获取总数
        total = user_service.count_users(
            search=search_params["search"],
            is_active=is_active
        )

        # 转换为响应模型
        user_list = [UserList.from_orm(user) for user in users]

        # 创建分页元数据
        meta = PaginationMeta.create(
            page=pagination["page"],
            size=pagination["size"],
            total=total
        )

        return PaginatedResponse(
            success=True,
            message="获取用户列表成功",
            data=user_list,
            meta=meta
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取用户列表失败: {str(e)}"
        )


@router.post(
    "/",
    response_model=DataResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
    summary="创建用户",
    description="创建新用户（管理员功能）"
)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> DataResponse[UserResponse]:
    """创建用户

    Args:
        user_data (UserCreate): 用户创建数据
        db (Session): 数据库会话
        current_user (User): 当前用户（需要超级用户权限）

    Returns:
        DataResponse[UserResponse]: 创建的用户信息
    """
    user_service = UserService(db)

    try:
        new_user = user_service.create_user(user_data)

        return DataResponse(
            success=True,
            message="用户创建成功",
            data=UserResponse.from_orm(new_user)
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建用户失败: {str(e)}"
        )


@router.get(
    "/me",
    response_model=DataResponse[UserResponse],
    summary="获取当前用户信息",
    description="获取当前登录用户的详细信息"
)
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
) -> DataResponse[UserResponse]:
    """获取当前用户信息

    Args:
        current_user (User): 当前用户

    Returns:
        DataResponse[UserResponse]: 当前用户信息
    """
    return DataResponse(
        success=True,
        message="获取用户信息成功",
        data=UserResponse.from_orm(current_user)
    )


@router.put(
    "/me",
    response_model=DataResponse[UserResponse],
    summary="更新当前用户信息",
    description="更新当前登录用户的信息"
)
async def update_current_user_profile(
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> DataResponse[UserResponse]:
    """更新当前用户信息

    Args:
        user_data (UserUpdate): 用户更新数据
        db (Session): 数据库会话
        current_user (User): 当前用户

    Returns:
        DataResponse[UserResponse]: 更新后的用户信息
    """
    user_service = UserService(db)

    try:
        updated_user = user_service.update_user(current_user.id, user_data)

        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )

        return DataResponse(
            success=True,
            message="用户信息更新成功",
            data=UserResponse.from_orm(updated_user)
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新用户信息失败: {str(e)}"
        )


@router.post(
    "/me/change-password",
    response_model=BaseResponse,
    summary="修改当前用户密码",
    description="修改当前登录用户的密码"
)
async def change_current_user_password(
    password_data: UserPasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> BaseResponse:
    """修改当前用户密码

    Args:
        password_data (UserPasswordChange): 密码修改数据
        db (Session): 数据库会话
        current_user (User): 当前用户

    Returns:
        BaseResponse: 修改结果
    """
    user_service = UserService(db)

    try:
        success = user_service.change_password(
            user_id=current_user.id,
            current_password=password_data.current_password,
            new_password=password_data.new_password
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="密码修改失败"
            )

        return BaseResponse(
            success=True,
            message="密码修改成功"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"密码修改失败: {str(e)}"
        )


@router.get(
    "/{user_id}",
    response_model=DataResponse[UserResponse],
    summary="获取指定用户信息",
    description="根据用户ID获取用户信息（管理员功能）"
)
async def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> DataResponse[UserResponse]:
    """获取指定用户信息

    Args:
        user_id (int): 用户ID
        db (Session): 数据库会话
        current_user (User): 当前用户（需要超级用户权限）

    Returns:
        DataResponse[UserResponse]: 用户信息
    """
    user_service = UserService(db)

    try:
        user = user_service.get_user_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )

        return DataResponse(
            success=True,
            message="获取用户信息成功",
            data=UserResponse.from_orm(user)
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取用户信息失败: {str(e)}"
        )


@router.put(
    "/{user_id}",
    response_model=DataResponse[UserResponse],
    summary="更新指定用户信息",
    description="根据用户ID更新用户信息（管理员功能）"
)
async def update_user_by_id(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> DataResponse[UserResponse]:
    """更新指定用户信息

    Args:
        user_id (int): 用户ID
        user_data (UserUpdate): 用户更新数据
        db (Session): 数据库会话
        current_user (User): 当前用户（需要超级用户权限）

    Returns:
        DataResponse[UserResponse]: 更新后的用户信息
    """
    user_service = UserService(db)

    try:
        updated_user = user_service.update_user(user_id, user_data)

        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )

        return DataResponse(
            success=True,
            message="用户信息更新成功",
            data=UserResponse.from_orm(updated_user)
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新用户信息失败: {str(e)}"
        )


@router.delete(
    "/{user_id}",
    response_model=BaseResponse,
    summary="删除指定用户",
    description="根据用户ID删除用户（软删除，管理员功能）"
)
async def delete_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> BaseResponse:
    """删除指定用户

    Args:
        user_id (int): 用户ID
        db (Session): 数据库会话
        current_user (User): 当前用户（需要超级用户权限）

    Returns:
        BaseResponse: 删除结果
    """
    # 防止删除自己
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能删除自己的账户"
        )

    user_service = UserService(db)

    try:
        success = user_service.delete_user(user_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )

        return BaseResponse(
            success=True,
            message="用户删除成功"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除用户失败: {str(e)}"
        )


@router.post(
    "/{user_id}/activate",
    response_model=BaseResponse,
    summary="激活用户",
    description="激活指定用户账户（管理员功能）"
)
async def activate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> BaseResponse:
    """激活用户

    Args:
        user_id (int): 用户ID
        db (Session): 数据库会话
        current_user (User): 当前用户（需要超级用户权限）

    Returns:
        BaseResponse: 激活结果
    """
    user_service = UserService(db)

    try:
        success = user_service.activate_user(user_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )

        return BaseResponse(
            success=True,
            message="用户激活成功"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"激活用户失败: {str(e)}"
        )


@router.post(
    "/{user_id}/deactivate",
    response_model=BaseResponse,
    summary="停用用户",
    description="停用指定用户账户（管理员功能）"
)
async def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> BaseResponse:
    """停用用户

    Args:
        user_id (int): 用户ID
        db (Session): 数据库会话
        current_user (User): 当前用户（需要超级用户权限）

    Returns:
        BaseResponse: 停用结果
    """
    # 防止停用自己
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能停用自己的账户"
        )

    user_service = UserService(db)

    try:
        success = user_service.deactivate_user(user_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )

        return BaseResponse(
            success=True,
            message="用户停用成功"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"停用用户失败: {str(e)}"
        )

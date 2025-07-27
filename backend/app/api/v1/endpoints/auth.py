"""认证相关端点"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Dict, Any

from ....database import get_db
from ....schemas.user import UserCreate, UserResponse, UserLogin
from ....schemas.token import Token, TokenRefresh, TokenVerify
from ....schemas.base import BaseResponse, DataResponse
from ....services.auth_service import AuthService
from ....services.user_service import UserService
from ....core.dependencies import get_current_user, get_current_active_user
from ....models.user import User

router = APIRouter()


@router.post(
    "/register",
    response_model=DataResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
    summary="用户注册",
    description="创建新用户账户"
)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
) -> DataResponse[UserResponse]:
    """用户注册

    Args:
        user_data (UserCreate): 用户注册数据
        db (Session): 数据库会话

    Returns:
        DataResponse[UserResponse]: 注册成功的用户信息
    """
    user_service = UserService(db)

    try:
        # 创建用户
        new_user = user_service.create_user(user_data)

        return DataResponse(
            success=True,
            message="用户注册成功",
            data=UserResponse.from_orm(new_user)
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"注册失败: {str(e)}"
        )


@router.post(
    "/login",
    response_model=DataResponse[Token],
    summary="用户登录",
    description="用户登录获取访问令牌"
)
async def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
) -> DataResponse[Token]:
    """用户登录

    Args:
        login_data (UserLogin): 登录数据
        db (Session): 数据库会话

    Returns:
        DataResponse[Token]: 登录令牌信息
    """
    auth_service = AuthService(db)

    try:
        token = auth_service.login(
            username=login_data.username,
            password=login_data.password,
            remember_me=login_data.remember_me
        )

        return DataResponse(
            success=True,
            message="登录成功",
            data=token
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"登录失败: {str(e)}"
        )


@router.post(
    "/login/oauth2",
    response_model=DataResponse[Token],
    summary="OAuth2登录",
    description="OAuth2标准登录接口"
)
async def login_oauth2(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> DataResponse[Token]:
    """OAuth2标准登录

    Args:
        form_data (OAuth2PasswordRequestForm): OAuth2表单数据
        db (Session): 数据库会话

    Returns:
        DataResponse[Token]: 登录令牌信息
    """
    auth_service = AuthService(db)

    try:
        token = auth_service.login(
            username=form_data.username,
            password=form_data.password,
            remember_me=False
        )

        return DataResponse(
            success=True,
            message="登录成功",
            data=token
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"登录失败: {str(e)}"
        )


@router.post(
    "/refresh",
    response_model=DataResponse[Token],
    summary="刷新令牌",
    description="使用刷新令牌获取新的访问令牌"
)
async def refresh_token(
    refresh_data: TokenRefresh,
    db: Session = Depends(get_db)
) -> DataResponse[Token]:
    """刷新访问令牌

    Args:
        refresh_data (TokenRefresh): 刷新令牌数据
        db (Session): 数据库会话

    Returns:
        DataResponse[Token]: 新的令牌信息
    """
    auth_service = AuthService(db)

    try:
        new_token = auth_service.refresh_token(refresh_data.refresh_token)

        return DataResponse(
            success=True,
            message="令牌刷新成功",
            data=new_token
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"令牌刷新失败: {str(e)}"
        )


@router.post(
    "/verify",
    response_model=DataResponse[Dict[str, Any]],
    summary="验证令牌",
    description="验证访问令牌的有效性"
)
async def verify_token(
    verify_data: TokenVerify,
    db: Session = Depends(get_db)
) -> DataResponse[Dict[str, Any]]:
    """验证令牌

    Args:
        verify_data (TokenVerify): 验证令牌数据
        db (Session): 数据库会话

    Returns:
        DataResponse[Dict[str, Any]]: 验证结果
    """
    auth_service = AuthService(db)

    try:
        result = auth_service.verify_token_endpoint(verify_data.token)

        if result["valid"]:
            return DataResponse(
                success=True,
                message="令牌有效",
                data=result
            )
        else:
            return DataResponse(
                success=False,
                message=result["message"],
                data=result
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"令牌验证失败: {str(e)}"
        )


@router.post(
    "/logout",
    response_model=BaseResponse,
    summary="用户登出",
    description="用户登出并撤销所有令牌"
)
async def logout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> BaseResponse:
    """用户登出

    Args:
        current_user (User): 当前用户
        db (Session): 数据库会话

    Returns:
        BaseResponse: 登出响应
    """
    auth_service = AuthService(db)
    
    try:
        # 撤销用户的所有token
        auth_service.token_service.revoke_user_tokens(current_user.id)
        
        return BaseResponse(
            success=True,
            message="登出成功，所有令牌已撤销"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"登出失败: {str(e)}"
        )


@router.get(
    "/me",
    response_model=DataResponse[UserResponse],
    summary="获取当前用户信息",
    description="获取当前登录用户的详细信息"
)
async def get_current_user_info(
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


@router.get(
    "/check",
    response_model=DataResponse[Dict[str, Any]],
    summary="检查认证状态",
    description="检查当前用户的认证状态"
)
async def check_auth_status(
    current_user: User = Depends(get_current_user)
) -> DataResponse[Dict[str, Any]]:
    """检查认证状态

    Args:
        current_user (User): 当前用户

    Returns:
        DataResponse[Dict[str, Any]]: 认证状态信息
    """
    return DataResponse(
        success=True,
        message="认证状态正常",
        data={
            "authenticated": True,
            "user_id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "is_active": current_user.is_active,
            "is_verified": current_user.is_verified,
            "is_superuser": current_user.is_superuser
        }
    )

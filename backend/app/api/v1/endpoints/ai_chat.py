"""AI聊天端点"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, field_validator

from ....database import get_db
from ....schemas.base import BaseResponse, DataResponse
from ....services.ai_service import AIService
from ....core.dependencies import get_current_active_user
from ....models.user import User

router = APIRouter()


class ChatMessage(BaseModel):
    """聊天消息模式"""

    role: str = Field(..., description="消息角色 (system/user/assistant)")
    content: str = Field(..., description="消息内容")


class ChatCompletionRequest(BaseModel):
    """聊天补全请求模式"""

    messages: List[ChatMessage] = Field(..., description="消息列表")
    model: str = Field(default="gpt-3.5-turbo", description="模型名称")
    provider_id: Optional[int] = Field(None, description="指定供应商ID（雪花ID）")
    stream: bool = Field(default=False, description="是否流式响应")
    temperature: Optional[float] = Field(None, ge=0, le=2, description="温度参数")
    max_tokens: Optional[int] = Field(None, gt=0, description="最大token数")
    top_p: Optional[float] = Field(None, ge=0, le=1, description="top_p参数")
    frequency_penalty: Optional[float] = Field(
        None, ge=-2, le=2, description="频率惩罚")
    presence_penalty: Optional[float] = Field(
        None, ge=-2, le=2, description="存在惩罚")

    @field_validator('provider_id', mode='before')
    @classmethod
    def convert_provider_id(cls, v):
        """将provider_id转换为整数"""
        if v is not None:
            if isinstance(v, str):
                try:
                    return int(v)
                except ValueError:
                    raise ValueError('provider_id必须是有效的数字')
            elif isinstance(v, int):
                return v
        return v


@router.post(
    "/completions",
    summary="聊天补全",
    description="使用AI进行聊天补全"
)
async def chat_completion(
    request_data: ChatCompletionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """聊天补全

    Args:
        request_data (ChatCompletionRequest): 聊天请求数据
        db (Session): 数据库会话
        current_user (User): 当前用户

    Returns:
        聊天补全响应或流式响应
    """
    ai_service = AIService(db)

    # 构建消息列表
    messages = [message.dict() for message in request_data.messages]

    # 构建额外参数
    kwargs = {}
    if request_data.temperature is not None:
        kwargs["temperature"] = request_data.temperature
    if request_data.max_tokens is not None:
        kwargs["max_tokens"] = request_data.max_tokens
    if request_data.top_p is not None:
        kwargs["top_p"] = request_data.top_p
    if request_data.frequency_penalty is not None:
        kwargs["frequency_penalty"] = request_data.frequency_penalty
    if request_data.presence_penalty is not None:
        kwargs["presence_penalty"] = request_data.presence_penalty

    try:
        if request_data.stream:
            # 流式响应
            async def generate_stream():
                async for chunk in await ai_service.chat_completion(
                    user_id=current_user.id,
                    messages=messages,
                    model=request_data.model,
                    provider_id=request_data.provider_id,
                    stream=True,
                    **kwargs
                ):
                    yield chunk

            return StreamingResponse(
                generate_stream(),
                media_type="text/plain",
                headers={"Cache-Control": "no-cache"}
            )
        else:
            # 普通响应
            response = await ai_service.chat_completion(
                user_id=current_user.id,
                messages=messages,
                model=request_data.model,
                provider_id=request_data.provider_id,
                stream=False,
                **kwargs
            )

            return DataResponse(
                success=True,
                message="聊天补全成功",
                data=response
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"聊天补全失败: {str(e)}"
        )


@router.get(
    "/models",
    response_model=DataResponse[dict],
    summary="获取可用模型",
    description="获取指定供应商的可用模型列表"
)
async def get_models(
    db: Session = Depends(get_db),
    provider_id: Optional[int] = Query(None, description="指定供应商ID"),
    current_user: User = Depends(get_current_active_user)
) -> DataResponse[dict]:
    """获取可用模型

    Args:
        db (Session): 数据库会话
        provider_id (Optional[int]): 指定供应商ID
        current_user (User): 当前用户

    Returns:
        DataResponse[dict]: 模型列表
    """
    ai_service = AIService(db)

    try:
        models = await ai_service.get_models(current_user.id, provider_id)

        return DataResponse(
            success=True,
            message="获取模型列表成功",
            data=models
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取模型列表失败: {str(e)}"
        )


class SimpleChatRequest(BaseModel):
    """简单聊天请求模式"""

    message: str = Field(..., description="用户消息")
    model: str = Field(default="gpt-3.5-turbo", description="模型名称")
    provider_id: Optional[int] = Field(None, description="指定供应商ID（雪花ID）")

    @field_validator('provider_id', mode='before')
    @classmethod
    def convert_provider_id(cls, v):
        """将provider_id转换为整数"""
        if v is not None:
            if isinstance(v, str):
                try:
                    return int(v)
                except ValueError:
                    raise ValueError('provider_id必须是有效的数字')
            elif isinstance(v, int):
                return v
        return v


@router.post(
    "/simple-chat",
    response_model=DataResponse[str],
    summary="简单聊天",
    description="简化的聊天接口，直接返回AI回复内容"
)
async def simple_chat(
    request_data: SimpleChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> DataResponse[str]:
    """简单聊天

    Args:
        message (str): 用户消息
        model (str): 模型名称
        provider_id (Optional[int]): 指定供应商ID
        db (Session): 数据库会话
        current_user (User): 当前用户

    Returns:
        DataResponse[str]: AI回复内容
    """
    ai_service = AIService(db)

    # 构建简单的消息列表
    messages = [
        {"role": "user", "content": request_data.message}
    ]

    try:
        response = await ai_service.chat_completion(
            user_id=current_user.id,
            messages=messages,
            model=request_data.model,
            provider_id=request_data.provider_id,
            stream=False
        )

        # 提取AI回复内容
        ai_message = response.get("choices", [{}])[0].get(
            "message", {}).get("content", "")

        return DataResponse(
            success=True,
            message="聊天成功",
            data=ai_message
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"聊天失败: {str(e)}"
        )

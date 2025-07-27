"""AI服务"""

import os
from typing import Dict, Any, List, Optional, AsyncGenerator, Union
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion
from openai._exceptions import OpenAIError, APIError, RateLimitError, AuthenticationError

from ..models.ai_provider import AIProvider
from .ai_provider_service import AIProviderService


class AIService:
    """AI服务类"""
    
    def __init__(self, db: Session):
        self.db = db
        self.provider_service = AIProviderService(db)
    
    def _create_openai_client(self, api_key: str, base_url: str) -> AsyncOpenAI:
        """创建OpenAI客户端
        
        Args:
            api_key (str): API密钥
            base_url (str): 基础URL
            
        Returns:
            AsyncOpenAI: OpenAI异步客户端
        """
        return AsyncOpenAI(
            api_key=api_key,
            base_url=base_url if base_url.endswith('/v1') else f"{base_url}/v1"
        )
    
    async def chat_completion(
        self,
        user_id: int,
        messages: List[Dict[str, Any]],
        model: str = "gpt-3.5-turbo",
        provider_id: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> Union[Dict[str, Any], AsyncGenerator[str, None]]:
        """聊天补全
        
        Args:
            user_id (int): 用户ID
            messages (List[Dict[str, Any]]): 消息列表
            model (str): 模型名称
            provider_id (Optional[int]): 指定供应商ID，为None时使用默认供应商
            stream (bool): 是否流式响应
            **kwargs: 其他参数
            
        Returns:
            Union[Dict[str, Any], AsyncGenerator[str, None]]: AI响应或流式生成器
            
        Raises:
            HTTPException: 当供应商不存在或API调用失败时
        """
        # 获取供应商
        if provider_id:
            provider = self.provider_service.get_provider_by_id(provider_id, user_id)
        else:
            provider = self.provider_service.get_default_provider(user_id)
        
        if not provider or not provider.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="未找到可用的AI供应商"
            )
        
        # 获取解密的API密钥
        api_key = self.provider_service.get_decrypted_api_key(provider.id, user_id)
        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="无法获取API密钥"
            )
        
        # 创建OpenAI客户端
        client = self._create_openai_client(api_key, provider.base_url)
        
        try:
            if stream:
                return self._stream_chat_completion(client, model, messages, **kwargs)
            else:
                completion = await client.chat.completions.create(
                    model=model,
                    messages=messages,
                    stream=False,
                    **kwargs
                )
                # 转换为字典格式以保持兼容性
                return completion.model_dump()
        
        except AuthenticationError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"API密钥认证失败: {str(e)}"
            )
        except RateLimitError as e:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"API调用频率限制: {str(e)}"
            )
        except APIError as e:
            raise HTTPException(
                status_code=e.status_code or status.HTTP_400_BAD_REQUEST,
                detail=f"AI API调用失败: {str(e)}"
            )
        except OpenAIError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"AI服务错误: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"未知错误: {str(e)}"
            )
    
    async def _stream_chat_completion(
        self,
        client: AsyncOpenAI,
        model: str,
        messages: List[Dict[str, Any]],
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """流式聊天补全
        
        Args:
            client (AsyncOpenAI): OpenAI客户端
            model (str): 模型名称
            messages (List[Dict[str, Any]]): 消息列表
            **kwargs: 其他参数
            
        Yields:
            str: 流式响应数据
        """
        try:
            # 使用 create 方法并设置 stream=True 进行流式调用
            stream = await client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
                **kwargs
            )
            
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    # 返回SSE格式的数据
                    content = chunk.choices[0].delta.content
                    yield f"data: {{\"choices\": [{{\"delta\": {{\"content\": \"{content}\"}}}}]}}\n\n"
            
            # 发送结束标记
            yield "data: [DONE]\n\n"
        
        except Exception as e:
            yield f"data: {{\"error\": \"流式响应错误: {str(e)}\"}}\n\n"
    
    async def get_models(self, user_id: int, provider_id: Optional[int] = None) -> Dict[str, Any]:
        """获取可用模型列表
        
        Args:
            user_id (int): 用户ID
            provider_id (Optional[int]): 指定供应商ID，为None时使用默认供应商
            
        Returns:
            Dict[str, Any]: 模型列表
            
        Raises:
            HTTPException: 当供应商不存在或API调用失败时
        """
        # 获取供应商
        if provider_id:
            provider = self.provider_service.get_provider_by_id(provider_id, user_id)
        else:
            provider = self.provider_service.get_default_provider(user_id)
        
        if not provider or not provider.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="未找到可用的AI供应商"
            )
        
        # 获取解密的API密钥
        api_key = self.provider_service.get_decrypted_api_key(provider.id, user_id)
        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="无法获取API密钥"
            )
        
        # 创建OpenAI客户端
        client = self._create_openai_client(api_key, provider.base_url)
        
        try:
            models = await client.models.list()
            # 转换为字典格式以保持兼容性
            return models.model_dump()
        
        except AuthenticationError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"API密钥认证失败: {str(e)}"
            )
        except RateLimitError as e:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"API调用频率限制: {str(e)}"
            )
        except APIError as e:
            raise HTTPException(
                status_code=e.status_code or status.HTTP_400_BAD_REQUEST,
                detail=f"AI API调用失败: {str(e)}"
            )
        except OpenAIError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"AI服务错误: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"未知错误: {str(e)}"
            )
    
    async def test_provider_connection(self, user_id: int, provider_id: int) -> Dict[str, Any]:
        """测试供应商连接
        
        Args:
            user_id (int): 用户ID
            provider_id (int): 供应商ID
            
        Returns:
            Dict[str, Any]: 测试结果
        """
        try:
            models = await self.get_models(user_id, provider_id)
            return {
                "success": True,
                "message": "连接测试成功",
                "models_count": len(models.get("data", []))
            }
        except HTTPException as e:
            return {
                "success": False,
                "message": f"连接测试失败: {e.detail}",
                "status_code": e.status_code
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"连接测试失败: {str(e)}"
            }
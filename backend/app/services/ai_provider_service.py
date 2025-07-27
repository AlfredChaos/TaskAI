"""AI供应商服务"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException, status

from ..models.ai_provider import AIProvider
from ..schemas.ai_provider import AIProviderCreate, AIProviderUpdate
from ..core.encryption import encrypt_api_key, decrypt_api_key


class AIProviderService:
    """AI供应商服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_provider(self, provider_data: AIProviderCreate, user_id: int) -> AIProvider:
        """创建AI供应商
        
        Args:
            provider_data (AIProviderCreate): 供应商创建数据
            user_id (int): 用户ID
            
        Returns:
            AIProvider: 创建的供应商实例
        """
        # 检查用户是否已有同名供应商
        existing = self.db.query(AIProvider).filter(
            and_(
                AIProvider.user_id == user_id,
                AIProvider.name == provider_data.name
            )
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="供应商名称已存在"
            )
        
        # 如果设置为默认供应商，先取消其他默认供应商
        if provider_data.is_default:
            self._unset_default_providers(user_id)
        
        # 加密API密钥
        encrypted_api_key = encrypt_api_key(provider_data.api_key)
        
        # 创建供应商
        db_provider = AIProvider(
            name=provider_data.name,
            base_url=provider_data.base_url,
            encrypted_api_key=encrypted_api_key,
            is_active=provider_data.is_active,
            is_default=provider_data.is_default,
            user_id=user_id
        )
        
        self.db.add(db_provider)
        self.db.commit()
        self.db.refresh(db_provider)
        
        return db_provider
    
    def get_provider_by_id(self, provider_id: int, user_id: int) -> Optional[AIProvider]:
        """根据ID获取供应商
        
        Args:
            provider_id (int): 供应商ID
            user_id (int): 用户ID
            
        Returns:
            Optional[AIProvider]: 供应商实例或None
        """
        return self.db.query(AIProvider).filter(
            and_(
                AIProvider.id == provider_id,
                AIProvider.user_id == user_id
            )
        ).first()
    
    def get_providers(self, user_id: int, is_active: Optional[bool] = None) -> List[AIProvider]:
        """获取用户的供应商列表
        
        Args:
            user_id (int): 用户ID
            is_active (Optional[bool]): 是否激活过滤
            
        Returns:
            List[AIProvider]: 供应商列表
        """
        query = self.db.query(AIProvider).filter(AIProvider.user_id == user_id)
        
        if is_active is not None:
            query = query.filter(AIProvider.is_active == is_active)
        
        return query.order_by(AIProvider.is_default.desc(), AIProvider.created_at.desc()).all()
    
    def get_default_provider(self, user_id: int) -> Optional[AIProvider]:
        """获取用户的默认供应商
        
        Args:
            user_id (int): 用户ID
            
        Returns:
            Optional[AIProvider]: 默认供应商或None
        """
        return self.db.query(AIProvider).filter(
            and_(
                AIProvider.user_id == user_id,
                AIProvider.is_default == True,
                AIProvider.is_active == True
            )
        ).first()
    
    def update_provider(self, provider_id: int, user_id: int, provider_data: AIProviderUpdate) -> Optional[AIProvider]:
        """更新供应商
        
        Args:
            provider_id (int): 供应商ID
            user_id (int): 用户ID
            provider_data (AIProviderUpdate): 更新数据
            
        Returns:
            Optional[AIProvider]: 更新后的供应商实例或None
        """
        provider = self.get_provider_by_id(provider_id, user_id)
        if not provider:
            return None
        
        # 检查名称是否重复
        if provider_data.name and provider_data.name != provider.name:
            existing = self.db.query(AIProvider).filter(
                and_(
                    AIProvider.user_id == user_id,
                    AIProvider.name == provider_data.name,
                    AIProvider.id != provider_id
                )
            ).first()
            
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="供应商名称已存在"
                )
        
        # 如果设置为默认供应商，先取消其他默认供应商
        if provider_data.is_default:
            self._unset_default_providers(user_id)
        
        # 更新字段
        update_data = provider_data.dict(exclude_unset=True)
        
        # 处理API密钥加密
        if 'api_key' in update_data:
            update_data['encrypted_api_key'] = encrypt_api_key(update_data.pop('api_key'))
        
        for field, value in update_data.items():
            setattr(provider, field, value)
        
        self.db.commit()
        self.db.refresh(provider)
        
        return provider
    
    def delete_provider(self, provider_id: int, user_id: int) -> bool:
        """删除供应商
        
        Args:
            provider_id (int): 供应商ID
            user_id (int): 用户ID
            
        Returns:
            bool: 删除是否成功
        """
        provider = self.get_provider_by_id(provider_id, user_id)
        if not provider:
            return False
        
        self.db.delete(provider)
        self.db.commit()
        
        return True
    
    def set_default_provider(self, provider_id: int, user_id: int) -> Optional[AIProvider]:
        """设置默认供应商
        
        Args:
            provider_id (int): 供应商ID
            user_id (int): 用户ID
            
        Returns:
            Optional[AIProvider]: 设置后的供应商实例或None
        """
        provider = self.get_provider_by_id(provider_id, user_id)
        if not provider or not provider.is_active:
            return None
        
        # 取消其他默认供应商
        self._unset_default_providers(user_id)
        
        # 设置当前供应商为默认
        provider.is_default = True
        self.db.commit()
        self.db.refresh(provider)
        
        return provider
    
    def get_decrypted_api_key(self, provider_id: int, user_id: int) -> Optional[str]:
        """获取解密的API密钥
        
        Args:
            provider_id (int): 供应商ID
            user_id (int): 用户ID
            
        Returns:
            Optional[str]: 解密的API密钥或None
        """
        provider = self.get_provider_by_id(provider_id, user_id)
        if not provider:
            return None
        
        try:
            return decrypt_api_key(provider.encrypted_api_key)
        except ValueError:
            return None
    
    def _unset_default_providers(self, user_id: int) -> None:
        """取消用户的所有默认供应商
        
        Args:
            user_id (int): 用户ID
        """
        self.db.query(AIProvider).filter(
            and_(
                AIProvider.user_id == user_id,
                AIProvider.is_default == True
            )
        ).update({AIProvider.is_default: False})
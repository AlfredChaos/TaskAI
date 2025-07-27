"""加密服务"""

import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from ..config import get_settings

settings = get_settings()


class EncryptionService:
    """加密服务类"""
    
    def __init__(self):
        self._fernet = None
    
    def _get_fernet(self) -> Fernet:
        """获取Fernet加密实例"""
        if self._fernet is None:
            # 使用应用密钥生成加密密钥
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b'ai_provider_salt',  # 固定盐值，生产环境应使用配置
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(settings.secret_key.encode()))
            self._fernet = Fernet(key)
        return self._fernet
    
    def encrypt(self, plaintext: str) -> str:
        """加密字符串
        
        Args:
            plaintext (str): 明文字符串
            
        Returns:
            str: 加密后的base64编码字符串
        """
        fernet = self._get_fernet()
        encrypted_bytes = fernet.encrypt(plaintext.encode('utf-8'))
        return base64.urlsafe_b64encode(encrypted_bytes).decode('utf-8')
    
    def decrypt(self, encrypted_text: str) -> str:
        """解密字符串
        
        Args:
            encrypted_text (str): 加密的base64编码字符串
            
        Returns:
            str: 解密后的明文字符串
            
        Raises:
            ValueError: 解密失败时抛出异常
        """
        try:
            fernet = self._get_fernet()
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_text.encode('utf-8'))
            decrypted_bytes = fernet.decrypt(encrypted_bytes)
            return decrypted_bytes.decode('utf-8')
        except Exception as e:
            raise ValueError(f"解密失败: {str(e)}")


# 全局加密服务实例
encryption_service = EncryptionService()


def encrypt_api_key(api_key: str) -> str:
    """加密API密钥
    
    Args:
        api_key (str): 明文API密钥
        
    Returns:
        str: 加密后的API密钥
    """
    return encryption_service.encrypt(api_key)


def decrypt_api_key(encrypted_api_key: str) -> str:
    """解密API密钥
    
    Args:
        encrypted_api_key (str): 加密的API密钥
        
    Returns:
        str: 解密后的API密钥
    """
    return encryption_service.decrypt(encrypted_api_key)
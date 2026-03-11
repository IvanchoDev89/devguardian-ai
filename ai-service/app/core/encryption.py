from cryptography.fernet import Fernet
from typing import Optional
import base64
import hashlib
import os


class Encryptor:
    def __init__(self, key: Optional[str] = None):
        if key:
            self.key = self._derive_key(key)
        else:
            env_key = os.getenv("ENCRYPTION_KEY")
            if env_key:
                self.key = self._derive_key(env_key)
            else:
                self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
    
    def _derive_key(self, password: str) -> bytes:
        hash_obj = hashlib.sha256(password.encode())
        return base64.urlsafe_b64encode(hash_obj.digest())
    
    def encrypt(self, data: str) -> str:
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        return self.cipher.decrypt(encrypted_data.encode()).decode()
    
    @staticmethod
    def generate_key() -> str:
        return Fernet.generate_key().decode()


_encryptor: Optional[Encryptor] = None


def get_encryptor() -> Encryptor:
    global _encryptor
    if _encryptor is None:
        _encryptor = Encryptor()
    return _encryptor


def encrypt_value(value: str) -> str:
    return get_encryptor().encrypt(value)


def decrypt_value(encrypted_value: str) -> str:
    return get_encryptor().decrypt(encrypted_value)

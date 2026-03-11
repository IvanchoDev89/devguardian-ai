import pytest
from fastapi.testclient import TestClient
from jose import jwt
from app.core.auth import create_access_token, decode_token, verify_password, get_password_hash
from app.core.config import get_settings
from app.core.encryption import encrypt_value, decrypt_value

settings = get_settings()


class TestAuthUtils:
    def test_create_access_token(self):
        token = create_access_token({"sub": "user_1", "email": "test@example.com", "role": "user"})
        assert token is not None
        assert isinstance(token, str)
        
    def test_decode_token(self):
        token = create_access_token({"sub": "user_1", "email": "test@example.com", "role": "user"})
        payload = decode_token(token)
        assert payload is not None
        assert payload["sub"] == "user_1"
        assert payload["email"] == "test@example.com"
        
    def test_decode_invalid_token(self):
        payload = decode_token("invalid_token")
        assert payload is None
        
    def test_password_hashing(self):
        password = "test_password_123"
        hashed = get_password_hash(password)
        assert hashed != password
        assert verify_password(password, hashed)
        assert not verify_password("wrong_password", hashed)
        
    def test_password_hash_unique(self):
        password = "test_password_123"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        assert hash1 != hash2


class TestEncryption:
    def test_encrypt_decrypt(self):
        original = "sensitive_data_123"
        encrypted = encrypt_value(original)
        assert encrypted != original
        decrypted = decrypt_value(encrypted)
        assert decrypted == original
        
    def test_encrypt_produces_different_outputs(self):
        original = "sensitive_data_123"
        encrypted1 = encrypt_value(original)
        encrypted2 = encrypt_value(original)
        assert encrypted1 != encrypted2


class TestJWTToken:
    def test_token_contains_expected_fields(self):
        token = create_access_token({"sub": "user_1", "email": "test@example.com", "role": "admin"})
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert payload["sub"] == "user_1"
        assert payload["email"] == "test@example.com"
        assert payload["role"] == "admin"
        assert payload["type"] == "access"
        
    def test_token_expiration(self):
        from datetime import timedelta
        token = create_access_token({"sub": "user_1", "email": "test@example.com"}, expires_delta=timedelta(seconds=-1))
        payload = decode_token(token)
        assert payload is None

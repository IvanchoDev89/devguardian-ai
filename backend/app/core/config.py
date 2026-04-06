from pydantic_settings import BaseSettings
from functools import lru_cache
import secrets


class Settings(BaseSettings):
    APP_NAME: str = "DevGuardian"
    DEBUG: bool = True
    VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = "sqlite:///./devguardian.db"
    USE_POSTGRES: bool = False
    
    # Redis (optional - for rate limiting and caching)
    REDIS_URL: str = "redis://localhost:6379"
    USE_REDIS: bool = False
    
    # JWT
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # 30 minutes for access token
    
    # Security
    ALLOWED_HOSTS: list = ["localhost", "127.0.0.1"]
    
    # Auth settings
    EMAIL_VERIFICATION_REQUIRED: bool = False  # Set to True in production
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()

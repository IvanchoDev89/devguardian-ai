from pydantic_settings import BaseSettings
from functools import lru_cache
import os
import secrets


class Settings(BaseSettings):
    APP_NAME: str = "DevGuardian"
    DEBUG: bool = False
    VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = "sqlite:///./devguardian.db"
    USE_POSTGRES: bool = False
    
    # Redis (optional - for rate limiting and caching)
    REDIS_URL: str = "redis://localhost:6379"
    USE_REDIS: bool = False
    
    # JWT - SECRET_KEY must be set in production
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    # Security
    ALLOWED_HOSTS: list = ["localhost", "127.0.0.1"]
    
    # Auth settings
    EMAIL_VERIFICATION_REQUIRED: bool = False
    
    class Config:
        env_file = ".env"
        extra = "ignore"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.SECRET_KEY:
            if os.environ.get("ENVIRONMENT") == "production":
                raise ValueError("SECRET_KEY must be set in production")
            self.SECRET_KEY = secrets.token_urlsafe(32)


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()

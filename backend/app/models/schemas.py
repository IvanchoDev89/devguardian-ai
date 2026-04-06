from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None


class VulnerabilityBase(BaseModel):
    title: str
    description: str
    severity: str
    cwe_id: Optional[str] = None
    cvss_score: Optional[str] = None


class VulnerabilityCreate(VulnerabilityBase):
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    code_snippet: Optional[str] = None


class VulnerabilityUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None
    fix_suggestion: Optional[str] = None


class VulnerabilityResponse(VulnerabilityBase):
    id: int
    status: str
    file_path: Optional[str]
    line_number: Optional[int]
    code_snippet: Optional[str]
    fix_suggestion: Optional[str]
    owner_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ScanBase(BaseModel):
    name: str
    scan_type: str
    target: Optional[str] = None


class ScanCreate(ScanBase):
    pass


class ScanUpdate(BaseModel):
    name: Optional[str] = None
    scan_type: Optional[str] = None
    target: Optional[str] = None
    status: Optional[str] = None
    results: Optional[str] = None


class ScanResponse(ScanBase):
    id: int
    status: str
    results: Optional[str]
    owner_id: int
    created_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class UserProfile(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str]
    role: str
    is_active: bool
    created_at: Optional[str]


class UserProfileUpdate(BaseModel):
    username: Optional[str] = None
    full_name: Optional[str] = None


class Settings(BaseModel):
    theme: str = "dark"
    language: str = "en"
    notifications_email: bool = True
    notifications_scan: bool = True


class SettingsUpdate(BaseModel):
    theme: Optional[str] = None
    language: Optional[str] = None
    notifications_email: Optional[bool] = None
    notifications_scan: Optional[bool] = None

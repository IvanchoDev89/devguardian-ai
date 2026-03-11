from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime
from app.core.encryption import encrypt_value, decrypt_value
import secrets
import string


class APIKey:
    def __init__(
        self,
        key_id: str,
        key_prefix: str,
        hashed_key: str,
        user_id: str,
        name: str,
        plan: str,
        monthly_quota: int,
        scans_used: int,
        created_at: str,
        expires_at: Optional[str],
        last_used: Optional[str],
        is_active: bool
    ):
        self.key_id = key_id
        self.key_prefix = key_prefix
        self.hashed_key = hashed_key
        self.user_id = user_id
        self.name = name
        self.plan = plan
        self.monthly_quota = monthly_quota
        self.scans_used = scans_used
        self.created_at = created_at
        self.expires_at = expires_at
        self.last_used = last_used
        self.is_active = is_active

    def to_dict(self) -> dict:
        return {
            "key_id": self.key_id,
            "key_prefix": self.key_prefix,
            "name": self.name,
            "plan": self.plan,
            "monthly_quota": self.monthly_quota,
            "scans_used": self.scans_used,
            "remaining": self.monthly_quota - self.scans_used,
            "created_at": self.created_at,
            "expires_at": self.expires_at,
            "last_used": self.last_used,
            "is_active": self.is_active
        }


def generate_api_key() -> tuple[str, str, str]:
    """Generate a new API key and return (full_key, hashed_key, prefix)"""
    key = f"dg_{secrets.token_urlsafe(32)}"
    hashed = encrypt_value(key)
    prefix = key[:12] + "..."
    return key, hashed, prefix


def hash_api_key(api_key: str) -> str:
    """Hash an API key for storage"""
    return encrypt_value(api_key)


def verify_api_key(api_key: str, hashed_key: str) -> bool:
    """Verify an API key against its hash"""
    try:
        stored = decrypt_value(hashed_key)
        return secrets.compare_digest(api_key, stored)
    except Exception:
        return False


PLAN_QUOTAS = {
    "free": 50,
    "pro": 500,
    "enterprise": -1  # Unlimited
}


class APIKeyManager:
    def __init__(self):
        self.keys: Dict[str, APIKey] = {}
        self.keys_by_hash: Dict[str, str] = {}  # hashed_key -> key_id
    
    def create_key(
        self,
        user_id: str,
        name: str,
        plan: str = "free",
        expires_days: Optional[int] = None
    ) -> tuple[APIKey, str]:
        """Create a new API key. Returns (APIKey object, full_api_key)"""
        
        key_id = f"key_{len(self.keys) + 1}"
        full_key, hashed_key, prefix = generate_api_key()
        
        from datetime import timedelta
        expires_at = None
        if expires_days:
            expires_at = (datetime.now() + timedelta(days=expires_days)).isoformat()
        
        api_key = APIKey(
            key_id=key_id,
            key_prefix=prefix,
            hashed_key=hashed_key,
            user_id=user_id,
            name=name,
            plan=plan,
            monthly_quota=PLAN_QUOTAS.get(plan, 50),
            scans_used=0,
            created_at=datetime.now().isoformat(),
            expires_at=expires_at,
            last_used=None,
            is_active=True
        )
        
        self.keys[key_id] = api_key
        self.keys_by_hash[hashed_key] = key_id
        
        return api_key, full_key
        """Verify an API key and return the APIKey object if valid"""
        hashed = encrypt_value(api_key)
        
        # Check if key exists
        key_id = self.keys_by_hash.get(hashed)
        if not key_id:
            return None
        
        api_key_obj = self.keys.get(key_id)
        if not api_key_obj:
            return None
        
        # Check if active
        if not api_key_obj.is_active:
            return None
        
        # Check expiration
        if api_key_obj.expires_at:
            expires = datetime.fromisoformat(api_key_obj.expires_at)
            if expires < datetime.now():
                return None
        
        return api_key_obj
    
    def increment_usage(self, key_id: str) -> bool:
        """Increment scan count for an API key. Returns False if quota exceeded"""
        api_key = self.keys.get(key_id)
        if not api_key:
            return False
        
        if api_key.plan == "enterprise":
            return True
        
        if api_key.scans_used >= api_key.monthly_quota:
            return False
        
        api_key.scans_used += 1
        api_key.last_used = datetime.now().isoformat()
        return True
    
    def get_user_keys(self, user_id: str) -> List[APIKey]:
        """Get all API keys for a user"""
        return [k for k in self.keys.values() if k.user_id == user_id]
    
    def revoke_key(self, key_id: str) -> bool:
        """Revoke an API key"""
        api_key = self.keys.get(key_id)
        if api_key:
            api_key.is_active = False
            return True
        return False
    
    def delete_key(self, key_id: str) -> bool:
        """Delete an API key"""
        api_key = self.keys.pop(key_id, None)
        if api_key:
            self.keys_by_hash.pop(api_key.hashed_key, None)
            return True
        return False
    
    def reset_monthly_usage(self):
        """Reset monthly usage for all keys (call monthly)"""
        for key in self.keys.values():
            key.scans_used = 0


_api_key_manager: Optional[APIKeyManager] = None


def get_api_key_manager() -> APIKeyManager:
    global _api_key_manager
    if _api_key_manager is None:
        _api_key_manager = APIKeyManager()
    return _api_key_manager

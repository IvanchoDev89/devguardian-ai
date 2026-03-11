from fastapi import Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Callable
import time

from app.database import get_db, RateLimit


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware using database for tracking
    """
    
    # Default limits
    DEFAULT_LIMIT = 100  # requests
    DEFAULT_WINDOW = 60  # seconds
    
    # Endpoints with different limits
    ENDPOINT_LIMITS = {
        "/api/v1/analyze-code": 20,  # expensive operation
        "/api/auth/login": 10,
        "/api/auth/register": 5,
    }
    
    # Endpoints that don't count towards rate limit
    EXCLUDED_PATHS = [
        "/health",
        "/docs",
        "/openapi.json",
        "/redoc",
    ]
    
    def __init__(self, app, db_generator):
        super().__init__(app)
        self.db_generator = db_generator
    
    async def dispatch(self, request: Request, call_next: Callable):
        # Skip rate limiting for excluded paths
        if any(request.url.path.startswith(path) for path in self.EXCLUDED_PATHS):
            return await call_next(request)
        
        # Get client IP
        client_ip = self._get_client_ip(request)
        
        # Get endpoint-specific limit
        endpoint = request.url.path
        limit = self.ENDPOINT_LIMITS.get(endpoint, self.DEFAULT_LIMIT)
        
        # Check rate limit
        if not await self._check_rate_limit(client_ip, endpoint, limit):
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Too many requests. Please try again later.",
                    "retry_after": 60
                }
            )
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers
        remaining, reset_time = await self._get_rate_limit_info(client_ip, endpoint)
        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int(reset_time))
        
        return response
    
    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP from request"""
        # Check X-Forwarded-For header (for reverse proxy)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        # Check X-Real-IP header
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fall back to client host
        if request.client:
            return request.client.host
        
        return "unknown"
    
    async def _check_rate_limit(self, ip: str, endpoint: str, limit: int) -> bool:
        """Check if request is within rate limit"""
        try:
            db = next(self.db_generator())
            
            now = datetime.utcnow()
            window_start = now - timedelta(seconds=60)
            
            # Get or create rate limit record
            rate_record = db.query(RateLimit).filter(
                RateLimit.ip_address == ip,
                RateLimit.endpoint == endpoint,
                RateLimit.window_start >= window_start
            ).first()
            
            if rate_record is None:
                # Create new record
                rate_record = RateLimit(
                    ip_address=ip,
                    endpoint=endpoint,
                    requests_count=1,
                    window_start=now,
                    blocked_until=None
                )
                db.add(rate_record)
                db.commit()
                return True
            
            # Check if blocked
            if rate_record.blocked_until and rate_record.blocked_until > now:
                return False
            
            # Increment counter
            rate_record.requests_count += 1
            db.commit()
            
            # Check if over limit
            if rate_record.requests_count > limit:
                # Block for 5 minutes
                rate_record.blocked_until = now + timedelta(minutes=5)
                db.commit()
                return False
            
            return True
            
        except Exception as e:
            # On error, allow request (fail open)
            return True
        finally:
            db.close()
    
    async def _get_rate_limit_info(self, ip: str, endpoint: str) -> tuple:
        """Get remaining requests and reset time"""
        try:
            db = next(self.db_generator())
            
            now = datetime.utcnow()
            window_start = now - timedelta(seconds=60)
            
            rate_record = db.query(RateLimit).filter(
                RateLimit.ip_address == ip,
                RateLimit.endpoint == endpoint,
                RateLimit.window_start >= window_start
            ).first()
            
            if rate_record:
                limit = self.ENDPOINT_LIMITS.get(endpoint, self.DEFAULT_LIMIT)
                remaining = max(0, limit - rate_record.requests_count)
                reset_time = int(rate_record.window_start.timestamp()) + 60
                return remaining, reset_time
            
            return self.DEFAULT_LIMIT, int(now.timestamp()) + 60
            
        except:
            return self.DEFAULT_LIMIT, int(datetime.utcnow().timestamp()) + 60
        finally:
            db.close()


def create_rate_limiter(db_generator):
    """Factory function to create rate limiter with db generator"""
    return RateLimitMiddleware

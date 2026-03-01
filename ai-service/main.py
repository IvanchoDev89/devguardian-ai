from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import uvicorn
import os
from datetime import datetime
from typing import Callable

# Import API endpoints
from app.api.endpoints.security import router as security_router
from app.api.endpoints.ai_fix_service import router as ai_fix_router
from app.api.endpoints.ai_fixes import router as ai_fixes_router
from app.api.endpoints.pytorch_scanner import router as pytorch_router
from app.api.endpoints.advanced_ml import router as advanced_ml_router
from app.api.endpoints.pentesting import router as pentest_router
from app.api.endpoints.zero_day_api import router as zero_day_router
from app.api.endpoints.github_scanner import router as github_router
from app.api.endpoints.comprehensive_scanner import router as scanner_router
from app.api.endpoints.semgrep_endpoint import router as semgrep_router
from app.api.endpoints.vulnerability_analyzer import router as vulnerability_router
from app.api.endpoints.llm_analyzer import router as llm_router


# Security middleware for additional protections
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        response = await call_next(request)
        
        # Prevent clickjacking
        response.headers["X-Frame-Options"] = "DENY"
        
        # Prevent XSS attacks
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # XSS Protection
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        # Referrer Policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Content Security Policy
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
        
        # Permissions Policy
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        
        # Remove sensitive headers (use .del instead of .pop)
        if "server" in response.headers:
            response.headers["server"] = ""
        if "x-powered-by" in response.headers:
            response.headers["x-powered-by"] = ""
        
        return response


class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_size: int = 1024 * 1024):  # 1MB default
        super().__init__(app)
        self.max_size = max_size
    
    async def dispatch(self, request: Request, call_next: Callable):
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.max_size:
            return JSONResponse(
                status_code=413,
                content={"error": "Payload Too Large", "message": "Request body too large"}
            )
        return await call_next(request)


class InputSanitizationMiddleware(BaseHTTPMiddleware):
    """Sanitize input to prevent XSS and injection attacks"""
    
    async def dispatch(self, request: Request, call_next: Callable):
        # Skip for GET requests
        if request.method == "GET":
            return await call_next(request)
        
        # Process request body if present
        try:
            body = await request.body()
            if body:
                # Basic sanitization - decode, sanitize, encode
                body_str = body.decode('utf-8', errors='ignore')
                
                # Remove null bytes
                body_str = body_str.replace('\x00', '')
                
                # Create new request with sanitized body
                async def receive():
                    return {"type": "http.request", "body": body_str.encode('utf-8')}
                
                request._receive = receive
        except Exception:
            pass
        
        return await call_next(request)


# Create FastAPI app
app = FastAPI(
    title="DevGuardian AI Service",
    description="AI-powered security vulnerability detection and code analysis service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Get allowed hosts from environment
allowed_hosts = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# Add security middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

# Add security headers
app.add_middleware(SecurityHeadersMiddleware)


# Include routers
app.include_router(security_router)
app.include_router(ai_fix_router)
app.include_router(ai_fixes_router, prefix="/api")
app.include_router(pytorch_router, prefix="/api")
app.include_router(advanced_ml_router, prefix="/api")
app.include_router(pentest_router, prefix="/api")
app.include_router(zero_day_router)
app.include_router(github_router)
app.include_router(scanner_router)
app.include_router(semgrep_router)
app.include_router(vulnerability_router)
app.include_router(llm_router)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    torch_status = {"available": False}
    
    try:
        import torch
        torch_status = {
            "available": True,
            "version": torch.__version__,
            "cuda_available": torch.cuda.is_available(),
            "device_count": torch.cuda.device_count() if torch.cuda.is_available() else 0
        }
    except (ImportError, AttributeError):
        pass
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "DevGuardian AI Service",
        "version": "1.0.0",
        "dependencies": {
            "pytorch": torch_status,
            "fastapi": "available"
        }
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "DevGuardian AI Service",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "security": "/api/security",
            "ai_fix": "/api/ai-fix",
            "ai_fixes": "/api/ai-fixes",
            "pytorch_scanner": "/api/pytorch-scanner",
            "advanced_ml": "/api/advanced-ml",
            "pentest": "/api/pentest",
            "zero_day": "/api/zero-day",
            "docs": "/docs",
            "health": "/health"
        }
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler - doesn't expose error details"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please contact support if this persists.",
            "timestamp": datetime.now().isoformat()
        }
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "127.0.0.1")
    reload = os.getenv("RELOAD", "false").lower() == "true"
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from datetime import datetime

# Import API endpoints
from app.api.endpoints.security import router as security_router
from app.api.endpoints.ai_fix_service import router as ai_fix_router

# Create FastAPI app
app = FastAPI(
    title="DevGuardian AI Service",
    description="AI-powered security vulnerability detection and code analysis service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8001"],  # Frontend and backend URLs
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include routers
app.include_router(security_router)
app.include_router(ai_fix_router)

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
            "docs": "/docs",
            "health": "/api/security/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check if PyTorch is available
        import torch
        torch_status = {
            "available": True,
            "version": torch.__version__,
            "cuda_available": torch.cuda.is_available(),
            "device_count": torch.cuda.device_count() if torch.cuda.is_available() else 0
        }
    except ImportError:
        torch_status = {"available": False}
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "DevGuardian AI Service",
        "version": "1.0.0",
        "dependencies": {
            "pytorch": torch_status,
            "transformers": "available",  # We'll check this in production
            "fastapi": "available"
        }
    }

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )

if __name__ == "__main__":
    # Get port from environment variable or default to 8000
    port = int(os.getenv("PORT", 8000))
    
    # Run application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,  # Set to False in production
        log_level="info"
    )

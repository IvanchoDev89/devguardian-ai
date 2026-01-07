from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time
import os

from app.core.schemas import (
    CodeFixRequest,
    GeneratedFix,
    ValidationResult,
    AnalyzeVulnerabilityRequest,
    VulnerabilityAnalysis,
    ErrorResponse,
    HealthResponse
)
from app.core.services.ai_fix_service import AIFixServiceInterface, MockAIFixService
from app.core.utils import (
    setup_logging,
    CorrelationId,
    log_request,
    log_response,
    log_error,
    AIServiceError,
    metrics
)


# Initialize logging
setup_logging()

# Global AI service instance
ai_service: AIFixServiceInterface = MockAIFixService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    # Startup
    print("🚀 DevGuardian AI Service starting up...")
    print(f"📊 Metrics collection enabled")
    print(f"🤖 AI Service: {type(ai_service).__name__}")
    
    yield
    
    # Shutdown
    print("🛑 DevGuardian AI Service shutting down...")


# Create FastAPI application
app = FastAPI(
    title="DevGuardian AI Service",
    description="AI-powered vulnerability analysis and fix generation service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware for correlation ID and metrics
@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    """Add correlation ID and collect metrics."""
    
    # Get or generate correlation ID
    correlation_id = CorrelationId.get_from_headers(dict(request.headers))
    if not correlation_id:
        correlation_id = CorrelationId.generate()
    
    # Add correlation ID to request state
    request.state.correlation_id = correlation_id
    
    # Log request
    log_request(
        correlation_id=correlation_id,
        method=request.method,
        path=request.url.path,
        query_params=str(request.query_params)
    )
    
    # Track metrics
    start_time = time.time()
    metrics.increment_requests()
    
    try:
        response = await call_next(request)
        
        # Calculate duration
        duration_ms = int((time.time() - start_time) * 1000)
        
        # Log response
        log_response(
            correlation_id=correlation_id,
            status_code=response.status_code,
            duration_ms=duration_ms
        )
        
        # Add correlation ID to response headers
        response.headers["X-Correlation-ID"] = correlation_id
        
        return response
        
    except Exception as e:
        metrics.increment_errors()
        log_error(
            correlation_id=correlation_id,
            error=e,
            path=request.url.path
        )
        raise


# Exception handlers
@app.exception_handler(AIServiceError)
async def ai_service_exception_handler(request: Request, exc: AIServiceError):
    """Handle AI service specific errors."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error=str(exc),
            error_code="AI_SERVICE_ERROR",
            details={"correlation_id": request.state.correlation_id}
        ).dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    log_error(
        correlation_id=getattr(request.state, 'correlation_id', 'unknown'),
        error=exc,
        path=request.url.path
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="Internal server error",
            error_code="INTERNAL_ERROR",
            details={"correlation_id": getattr(request.state, 'correlation_id', 'unknown')}
        ).dict()
    )


# API Endpoints
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        uptime_seconds=metrics.get_uptime_seconds(),
        model_loaded=True,
        memory_usage_mb=metrics.get_memory_usage_mb(),
        cpu_usage_percent=metrics.get_cpu_usage_percent()
    )


@app.post("/api/v1/generate-fix", response_model=GeneratedFix)
async def generate_fix(
    request: CodeFixRequest,
    http_request: Request
):
    """Generate a fix for a vulnerability."""
    correlation_id = http_request.state.correlation_id
    
    try:
        fix = await ai_service.generate_fix(request, correlation_id)
        return fix
        
    except AIServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.post("/api/v1/validate-fix", response_model=ValidationResult)
async def validate_fix(
    fix_id: str,
    http_request: Request
):
    """Validate a generated fix."""
    correlation_id = http_request.state.correlation_id
    
    try:
        result = await ai_service.validate_fix(fix_id, correlation_id)
        return result
        
    except AIServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.post("/api/v1/analyze-vulnerability", response_model=VulnerabilityAnalysis)
async def analyze_vulnerability(
    request: AnalyzeVulnerabilityRequest,
    http_request: Request
):
    """Analyze a vulnerability."""
    correlation_id = http_request.state.correlation_id
    
    try:
        analysis = await ai_service.analyze_vulnerability(request, correlation_id)
        return analysis
        
    except AIServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.get("/api/v1/metrics")
async def get_metrics():
    """Get service metrics."""
    return {
        "uptime_seconds": metrics.get_uptime_seconds(),
        "request_count": metrics.request_count,
        "error_count": metrics.error_count,
        "error_rate_percent": metrics.get_error_rate(),
        "average_generation_time_ms": metrics.get_average_generation_time_ms(),
        "memory_usage_mb": metrics.get_memory_usage_mb(),
        "cpu_usage_percent": metrics.get_cpu_usage_percent()
    }


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )

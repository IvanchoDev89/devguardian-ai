import structlog
from typing import Optional, Dict, Any
import uuid
import time
import psutil
import os

logger = structlog.get_logger(__name__)


class AIServiceError(Exception):
    """Base exception for AI service errors."""
    pass


class ModelNotLoadedError(AIServiceError):
    """Raised when AI model is not loaded."""
    pass


class ValidationError(AIServiceError):
    """Raised when validation fails."""
    pass


class GenerationError(AIServiceError):
    """Raised when fix generation fails."""
    pass


class CorrelationId:
    """Manages correlation IDs for request tracking."""
    
    @staticmethod
    def generate() -> str:
        return str(uuid.uuid4())
    
    @staticmethod
    def get_from_headers(headers: Dict[str, str]) -> Optional[str]:
        return headers.get("X-Correlation-ID")
    
    @staticmethod
    def set_in_headers(headers: Dict[str, str], correlation_id: str) -> Dict[str, str]:
        headers["X-Correlation-ID"] = correlation_id
        return headers


class MetricsCollector:
    """Collects and manages service metrics."""
    
    def __init__(self):
        self.start_time = time.time()
        self.request_count = 0
        self.error_count = 0
        self.generation_times = []
        
    def increment_requests(self):
        self.request_count += 1
        
    def increment_errors(self):
        self.error_count += 1
        
    def record_generation_time(self, duration_ms: int):
        self.generation_times.append(duration_ms)
        
    def get_uptime_seconds(self) -> int:
        return int(time.time() - self.start_time)
        
    def get_memory_usage_mb(self) -> float:
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024
        
    def get_cpu_usage_percent(self) -> float:
        return psutil.cpu_percent(interval=1)
        
    def get_average_generation_time_ms(self) -> float:
        if not self.generation_times:
            return 0.0
        return sum(self.generation_times) / len(self.generation_times)
        
    def get_error_rate(self) -> float:
        if self.request_count == 0:
            return 0.0
        return (self.error_count / self.request_count) * 100


# Global metrics instance
metrics = MetricsCollector()


def setup_logging():
    """Configure structured logging."""
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def log_request(correlation_id: str, method: str, path: str, **kwargs):
    """Log incoming request."""
    logger.info(
        "request_received",
        correlation_id=correlation_id,
        method=method,
        path=path,
        **kwargs
    )


def log_response(correlation_id: str, status_code: int, duration_ms: int, **kwargs):
    """Log outgoing response."""
    logger.info(
        "response_sent",
        correlation_id=correlation_id,
        status_code=status_code,
        duration_ms=duration_ms,
        **kwargs
    )


def log_error(correlation_id: str, error: Exception, **kwargs):
    """Log error."""
    logger.error(
        "error_occurred",
        correlation_id=correlation_id,
        error_type=type(error).__name__,
        error_message=str(error),
        **kwargs
    )


def log_generation(correlation_id: str, vulnerability_id: str, duration_ms: int, confidence: float, **kwargs):
    """Log fix generation."""
    logger.info(
        "fix_generated",
        correlation_id=correlation_id,
        vulnerability_id=vulnerability_id,
        duration_ms=duration_ms,
        confidence_score=confidence,
        **kwargs
    )


def log_validation(correlation_id: str, fix_id: str, is_valid: bool, duration_ms: int, **kwargs):
    """Log fix validation."""
    logger.info(
        "fix_validated",
        correlation_id=correlation_id,
        fix_id=fix_id,
        is_valid=is_valid,
        duration_ms=duration_ms,
        **kwargs
    )

"""
LLM Analysis API Endpoints
POST /api/llm/analyze - Analyze a vulnerability with LLM
POST /api/llm/fix - Generate fix for vulnerability
POST /api/llm/batch - Batch analyze multiple vulnerabilities
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import os

from app.services.llm_analyzer import LLMAnalyzer, create_analyzer, AnalysisResult

router = APIRouter(prefix="/api/llm", tags=["llm-analyzer"])

# Initialize analyzer (lazy loading)
_analyzer = None


def get_analyzer() -> LLMAnalyzer:
    """Get or create LLM analyzer"""
    global _analyzer
    if _analyzer is None:
        api_key = os.getenv("CLAUDE_API_KEY") or os.getenv("OPENAI_API_KEY")
        provider = "claude" if os.getenv("CLAUDE_API_KEY") else "openai"
        _analyzer = create_analyzer(provider=provider, api_key=api_key)
    return _analyzer


class VulnerabilityInput(BaseModel):
    """Single vulnerability input"""
    type: str = Field(..., description="Vulnerability type (e.g., sql-injection)")
    severity: str = Field(default="medium", description="Severity level")
    message: str = Field(..., description="Vulnerability message")
    line_content: Optional[str] = Field(None, description="Code snippet")
    cwe_id: Optional[str] = Field(None, description="CWE ID if known")


class AnalyzeRequest(BaseModel):
    """Request to analyze a vulnerability"""
    vulnerability: VulnerabilityInput
    code_snippet: str = Field(..., description="Code containing the vulnerability")
    language: str = Field(default="python", description="Programming language")
    generate_fix: bool = Field(default=True, description="Whether to generate fix suggestion")


class FixRequest(BaseModel):
    """Request to generate fix"""
    vulnerability: VulnerabilityInput
    code_snippet: str
    language: str = "python"


class BatchAnalyzeRequest(BaseModel):
    """Request to batch analyze vulnerabilities"""
    vulnerabilities: List[VulnerabilityInput]
    code_context: str
    language: str = "python"


class AnalysisResponse(BaseModel):
    """Response from LLM analysis"""
    explanation: str
    suggested_fix: Optional[str] = None
    confidence: float
    is_false_positive: bool = False
    false_positive_reason: Optional[str] = None
    remediation_steps: Optional[List[str]] = None


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_vulnerability(request: AnalyzeRequest) -> AnalysisResponse:
    """
    Analyze a single vulnerability with LLM
    
    Provides:
    - Detailed explanation of the vulnerability
    - Suggested fix code
    - Confidence score
    - Remediation steps
    """
    analyzer = get_analyzer()
    
    # Check if API key is configured
    if not analyzer.api_key:
        # Return fallback analysis
        result = analyzer.analyze_vulnerability(
            vulnerability=request.vulnerability.model_dump(),
            code_snippet=request.code_snippet,
            language=request.language
        )
    else:
        result = analyzer.analyze_vulnerability(
            vulnerability=request.vulnerability.model_dump(),
            code_snippet=request.code_snippet,
            language=request.language
        )
    
    return AnalysisResponse(
        explanation=result.explanation,
        suggested_fix=result.suggested_fix if request.generate_fix else None,
        confidence=result.confidence,
        is_false_positive=result.is_false_positive,
        false_positive_reason=result.false_positive_reason,
        remediation_steps=result.remediation_steps
    )


@router.post("/fix", response_model=AnalysisResponse)
async def generate_fix(request: FixRequest) -> AnalysisResponse:
    """
    Generate a secure fix for vulnerable code
    
    Returns code suggestion to fix the vulnerability
    """
    analyzer = get_analyzer()
    
    result = analyzer.analyze_vulnerability(
        vulnerability=request.vulnerability.model_dump(),
        code_snippet=request.code_snippet,
        language=request.language
    )
    
    return AnalysisResponse(
        explanation=result.explanation,
        suggested_fix=result.suggested_fix,
        confidence=result.confidence,
        remediation_steps=result.remediation_steps
    )


@router.post("/batch", response_model=List[AnalysisResponse])
async def batch_analyze(request: BatchAnalyzeRequest) -> List[AnalysisResponse]:
    """
    Batch analyze multiple vulnerabilities
    
    More efficient for analyzing many findings at once
    """
    analyzer = get_analyzer()
    
    results = analyzer.batch_analyze(
        vulnerabilities=[v.model_dump() for v in request.vulnerabilities],
        code_context=request.code_context
    )
    
    return [
        AnalysisResponse(
            explanation=r.explanation,
            suggested_fix=r.suggested_fix,
            confidence=r.confidence,
            is_false_positive=r.is_false_positive,
            false_positive_reason=r.false_positive_reason,
            remediation_steps=r.remediation_steps
        )
        for r in results
    ]


@router.get("/health")
async def llm_health():
    """Check LLM service health"""
    analyzer = get_analyzer()
    
    has_api_key = bool(analyzer.api_key)
    provider = analyzer.provider
    
    return {
        "status": "ok" if has_api_key else "no_api_key",
        "provider": provider,
        "api_configured": has_api_key,
        "cache_size": len(analyzer._cache)
    }


@router.post("/cache/clear")
async def clear_cache():
    """Clear the analysis cache"""
    analyzer = get_analyzer()
    analyzer.clear_cache()
    return {"message": "Cache cleared", "cache_size": 0}

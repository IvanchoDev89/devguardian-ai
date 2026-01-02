from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from enum import Enum
from datetime import datetime


class SeverityLevel(str, Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class VulnerabilityStatus(str, Enum):
    DETECTED = "detected"
    ANALYZING = "analyzing"
    FIXING = "fixing"
    FIXED = "fixed"
    IGNORED = "ignored"
    FALSE_POSITIVE = "false_positive"


class FileLocation(BaseModel):
    file_path: str = Field(..., description="Path to the vulnerable file")
    line_number: int = Field(..., gt=0, description="Line number where vulnerability is located")
    column_number: Optional[int] = Field(None, gt=0, description="Column number")
    function_name: Optional[str] = Field(None, description="Function name containing vulnerability")
    class_name: Optional[str] = Field(None, description="Class name containing vulnerability")


class CVSSScore(BaseModel):
    score: float = Field(..., ge=0.0, le=10.0, description="CVSS score from 0.0 to 10.0")
    vector: Optional[str] = Field(None, description="CVSS vector string")
    version: Optional[str] = Field(None, description="CVSS version")

    @property
    def severity(self) -> SeverityLevel:
        if self.score >= 9.0:
            return SeverityLevel.CRITICAL
        elif self.score >= 7.0:
            return SeverityLevel.HIGH
        elif self.score >= 4.0:
            return SeverityLevel.MEDIUM
        elif self.score > 0.0:
            return SeverityLevel.LOW
        else:
            return SeverityLevel.NONE


class VulnerabilityContext(BaseModel):
    repository_id: str = Field(..., description="Repository UUID")
    vulnerability_id: str = Field(..., description="Vulnerability UUID")
    cve_id: Optional[str] = Field(None, description="CVE identifier")
    identifier: str = Field(..., description="Vulnerability identifier")
    title: str = Field(..., description="Vulnerability title")
    description: str = Field(..., description="Vulnerability description")
    severity: SeverityLevel = Field(..., description="Severity level")
    cvss_score: Optional[CVSSScore] = Field(None, description="CVSS score information")
    location: FileLocation = Field(..., description="File location of vulnerability")
    source_code: str = Field(..., description="Source code containing vulnerability")
    language: str = Field(..., description="Programming language")
    framework: Optional[str] = Field(None, description="Framework being used")
    dependencies: List[str] = Field(default_factory=list, description="Relevant dependencies")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")


class CodeFixRequest(BaseModel):
    vulnerability_context: VulnerabilityContext
    additional_context: Optional[str] = Field(None, description="Additional context for fix generation")
    fix_style: str = Field("minimal", description="Style of fix: minimal, comprehensive, defensive")
    include_tests: bool = Field(True, description="Whether to generate test cases")
    max_attempts: int = Field(3, ge=1, le=5, description="Maximum generation attempts")


class GeneratedFix(BaseModel):
    fix_id: str = Field(..., description="Unique identifier for the generated fix")
    vulnerability_id: str = Field(..., description="Associated vulnerability ID")
    diff_content: str = Field(..., description="Git-compatible diff format")
    fixed_code: str = Field(..., description="Complete fixed file content")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="AI confidence in fix quality")
    explanation: str = Field(..., description="Explanation of the fix")
    potential_side_effects: List[str] = Field(default_factory=list, description="Potential side effects")
    test_cases: Optional[List[str]] = Field(None, description="Generated test cases")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")
    generation_time_ms: int = Field(..., description="Time taken to generate fix in milliseconds")


class ValidationResult(BaseModel):
    fix_id: str = Field(..., description="Fix identifier")
    is_valid: bool = Field(..., description="Whether the fix passed validation")
    syntax_valid: bool = Field(..., description="Whether the syntax is valid")
    security_valid: bool = Field(..., description="Whether security is maintained")
    tests_passed: bool = Field(..., description="Whether tests pass")
    performance_impact: str = Field(..., description="Performance impact assessment")
    compatibility_score: float = Field(..., ge=0.0, le=1.0, description="Compatibility score")
    error_message: Optional[str] = Field(None, description="Error message if validation failed")
    validation_details: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Detailed validation results")
    validation_time_ms: int = Field(..., description="Time taken for validation in milliseconds")


class AnalyzeVulnerabilityRequest(BaseModel):
    vulnerability_context: VulnerabilityContext
    analysis_depth: str = Field("standard", description="Analysis depth: quick, standard, deep")
    include_fix_suggestions: bool = Field(True, description="Whether to include fix suggestions")


class VulnerabilityAnalysis(BaseModel):
    vulnerability_id: str = Field(..., description="Vulnerability identifier")
    analysis_id: str = Field(..., description="Analysis identifier")
    root_cause: str = Field(..., description="Identified root cause")
    attack_vector: str = Field(..., description="Attack vector description")
    impact_assessment: str = Field(..., description="Impact assessment")
    exploitability: str = Field(..., description="Exploitability assessment")
    fix_complexity: str = Field(..., description="Complexity of fixing")
    suggested_approaches: List[str] = Field(default_factory=list, description="Suggested fix approaches")
    related_patterns: List[str] = Field(default_factory=list, description="Related vulnerability patterns")
    analysis_time_ms: int = Field(..., description="Time taken for analysis in milliseconds")


class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    error_code: str = Field(..., description="Error code")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")


class HealthResponse(BaseModel):
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="Service version")
    uptime_seconds: int = Field(..., description="Service uptime in seconds")
    model_loaded: bool = Field(..., description="Whether AI model is loaded")
    memory_usage_mb: float = Field(..., description="Memory usage in MB")
    cpu_usage_percent: float = Field(..., description="CPU usage percentage")

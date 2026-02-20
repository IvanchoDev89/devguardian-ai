"""
PyTorch Scanner Data Models
Pydantic models for vulnerability scanning requests and responses
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class VulnerabilityTypeEnum(str, Enum):
    """Enumeration of vulnerability types"""
    SQL_INJECTION = "sql_injection"
    XSS = "xss"
    COMMAND_INJECTION = "command_injection"
    PATH_TRAVERSAL = "path_traversal"
    INSECURE_DESERIALIZATION = "insecure_deserialization"
    HARDCODED_CREDENTIALS = "hardcoded_credentials"
    WEAK_CRYPTOGRAPHY = "weak_cryptography"
    INSECURE_RANDOM = "insecure_random"
    BUFFER_OVERFLOW = "buffer_overflow"
    RACE_CONDITION = "race_condition"

class SeverityEnum(str, Enum):
    """Enumeration of severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class ScanRequest(BaseModel):
    """Request model for code scanning"""
    code: str = Field(..., description="Code content to scan")
    file_name: Optional[str] = Field(None, description="Name of the file being scanned")
    file_path: Optional[str] = Field(None, description="Full path of the file")
    language: Optional[str] = Field(None, description="Programming language")
    scan_depth: str = Field("standard", description="Scan depth: basic, standard, comprehensive")

class ScanResponse(BaseModel):
    """Response model for scan initiation"""
    scan_id: str = Field(..., description="Unique identifier for the scan")
    status: str = Field(..., description="Current status of the scan")
    message: str = Field(..., description="Status message")
    estimated_time: str = Field(..., description="Estimated time to complete")

class VulnerabilityDetail(BaseModel):
    """Detailed vulnerability information"""
    file_path: str = Field(..., description="Path to the vulnerable file")
    vulnerability_type: VulnerabilityTypeEnum = Field(..., description="Type of vulnerability")
    severity: SeverityEnum = Field(..., description="Severity level")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    line_number: int = Field(..., ge=1, description="Line number of vulnerability")
    code_snippet: str = Field(..., description="Code snippet containing vulnerability")
    description: str = Field(..., description="Description of the vulnerability")
    recommendation: str = Field(..., description="Remediation recommendation")
    cwe_id: Optional[str] = Field(None, description="CWE identifier")
    cvss_score: Optional[float] = Field(None, ge=0.0, le=10.0, description="CVSS score")

class ScanStatus(BaseModel):
    """Status of an ongoing scan"""
    scan_id: str = Field(..., description="Unique identifier for the scan")
    status: str = Field(..., description="Current status: scanning, analyzing, generating_report, completed, failed")
    progress: int = Field(..., ge=0, le=100, description="Progress percentage")
    started_at: datetime = Field(..., description="Scan start time")
    completed_at: Optional[datetime] = Field(None, description="Scan completion time")
    file_name: str = Field(..., description="Name of the file/directory being scanned")
    error: Optional[str] = Field(None, description="Error message if scan failed")
    files_processed: Optional[int] = Field(None, description="Number of files processed")
    total_files: Optional[int] = Field(None, description="Total number of files to scan")

class VulnerabilityReport(BaseModel):
    """Comprehensive vulnerability report"""
    scan_id: str = Field(..., description="Unique identifier for the scan")
    scan_date: str = Field(..., description="Date and time of the scan")
    total_vulnerabilities: int = Field(..., ge=0, description="Total number of vulnerabilities found")
    severity_breakdown: Dict[str, int] = Field(..., description="Breakdown by severity level")
    type_breakdown: Dict[str, int] = Field(..., description="Breakdown by vulnerability type")
    risk_score: float = Field(..., ge=0.0, description="Overall risk score")
    vulnerabilities: List[VulnerabilityDetail] = Field(..., description="List of all vulnerabilities")
    recommendations: List[str] = Field(..., description="General recommendations")

class TrainingDataSample(BaseModel):
    """Sample of training data for model training"""
    code: str = Field(..., description="Code content")
    file_path: str = Field(..., description="File path")
    label: int = Field(..., ge=0, description="Vulnerability label (0=clean, 1-9=vulnerability types)")
    vulnerability_type: Optional[VulnerabilityTypeEnum] = Field(None, description="Type of vulnerability")
    severity: Optional[SeverityEnum] = Field(None, description="Severity level")
    line_number: Optional[int] = Field(None, ge=1, description="Line number of vulnerability")

class ModelTrainingRequest(BaseModel):
    """Request for model training"""
    training_data: List[TrainingDataSample] = Field(..., description="Training data samples")
    epochs: int = Field(10, ge=1, le=100, description="Number of training epochs")
    batch_size: int = Field(32, ge=1, le=128, description="Batch size for training")
    learning_rate: float = Field(0.001, ge=0.0001, le=0.1, description="Learning rate")
    validation_split: float = Field(0.2, ge=0.1, le=0.5, description="Validation data split ratio")

class ModelTrainingResponse(BaseModel):
    """Response for model training"""
    training_id: str = Field(..., description="Unique identifier for training session")
    status: str = Field(..., description="Training status")
    message: str = Field(..., description="Training status message")
    estimated_time: str = Field(..., description="Estimated training time")
    final_accuracy: Optional[float] = Field(None, ge=0.0, le=1.0, description="Final model accuracy")
    loss_history: Optional[List[float]] = Field(None, description="Training loss history")

class ModelMetrics(BaseModel):
    """Model performance metrics"""
    accuracy: float = Field(..., ge=0.0, le=1.0, description="Model accuracy")
    precision: float = Field(..., ge=0.0, le=1.0, description="Model precision")
    recall: float = Field(..., ge=0.0, le=1.0, description="Model recall")
    f1_score: float = Field(..., ge=0.0, le=1.0, description="F1 score")
    confusion_matrix: Optional[List[List[int]]] = Field(None, description="Confusion matrix")
    class_report: Optional[Dict[str, Any]] = Field(None, description="Detailed classification report")

class ScanStatistics(BaseModel):
    """Statistics about scanning operations"""
    total_scans: int = Field(..., ge=0, description="Total number of scans performed")
    successful_scans: int = Field(..., ge=0, description="Number of successful scans")
    failed_scans: int = Field(..., ge=0, description="Number of failed scans")
    total_vulnerabilities_found: int = Field(..., ge=0, description="Total vulnerabilities found")
    average_scan_time: float = Field(..., ge=0.0, description="Average scan time in seconds")
    most_common_vulnerability: Optional[VulnerabilityTypeEnum] = Field(None, description="Most commonly found vulnerability type")
    scan_trend: List[Dict[str, Any]] = Field(..., description="Scan trend over time")

class VulnerabilityPattern(BaseModel):
    """Vulnerability detection pattern"""
    pattern: str = Field(..., description="Regex pattern for detection")
    severity: SeverityEnum = Field(..., description="Severity level")
    description: str = Field(..., description="Pattern description")
    cwe_id: Optional[str] = Field(None, description="CWE identifier")
    language: Optional[str] = Field(None, description="Programming language")
    category: Optional[str] = Field(None, description="Vulnerability category")

class ScanConfiguration(BaseModel):
    """Configuration for vulnerability scanning"""
    enable_ml_detection: bool = Field(True, description="Enable ML-based detection")
    enable_pattern_detection: bool = Field(True, description="Enable pattern-based detection")
    confidence_threshold: float = Field(0.5, ge=0.0, le=1.0, description="Minimum confidence threshold")
    max_vulnerabilities_per_file: int = Field(100, ge=1, le=1000, description="Maximum vulnerabilities to report per file")
    file_extensions: List[str] = Field(default_factory=lambda: ['.php', '.js', '.py', '.rb', '.pl', '.sh', '.bat', '.java', '.cpp', '.c'], description="File extensions to scan")
    exclude_patterns: List[str] = Field(default_factory=list, description="Patterns to exclude from scanning")
    include_patterns: List[str] = Field(default_factory=list, description="Patterns to include in scanning")
    custom_patterns: List[VulnerabilityPattern] = Field(default_factory=list, description="Custom vulnerability patterns")

class BatchScanRequest(BaseModel):
    """Request for batch scanning multiple files"""
    files: List[Dict[str, str]] = Field(..., description="List of files with path and content")
    configuration: ScanConfiguration = Field(default_factory=ScanConfiguration, description="Scan configuration")
    parallel_processing: bool = Field(True, description="Enable parallel processing")
    max_workers: int = Field(4, ge=1, le=16, description="Maximum number of parallel workers")

class BatchScanResponse(BaseModel):
    """Response for batch scanning"""
    batch_id: str = Field(..., description="Unique identifier for batch scan")
    status: str = Field(..., description="Batch scan status")
    total_files: int = Field(..., ge=0, description="Total number of files in batch")
    processed_files: int = Field(..., ge=0, description="Number of processed files")
    failed_files: int = Field(..., ge=0, description="Number of failed files")
    total_vulnerabilities: int = Field(..., ge=0, description="Total vulnerabilities found")
    estimated_completion_time: str = Field(..., description="Estimated completion time")

class VulnerabilityFix(BaseModel):
    """AI-generated vulnerability fix"""
    vulnerability_id: str = Field(..., description="ID of the vulnerability")
    original_code: str = Field(..., description="Original vulnerable code")
    fixed_code: str = Field(..., description="Fixed code")
    fix_description: str = Field(..., description="Description of the fix")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in the fix")
    breaking_changes: bool = Field(False, description="Whether the fix introduces breaking changes")
    test_cases: Optional[List[str]] = Field(None, description="Test cases for the fix")

class FixGenerationRequest(BaseModel):
    """Request for generating AI fixes"""
    vulnerabilities: List[VulnerabilityDetail] = Field(..., description="List of vulnerabilities to generate fixes for")
    repository_id: Optional[str] = Field(None, description="Repository ID")
    scan_id: Optional[str] = Field(None, description="Scan ID")
    auto_approve: bool = Field(False, description="Automatically approve generated fixes")

class FixGenerationResponse(BaseModel):
    """Response for AI fix generation"""
    success: bool = Field(..., description="Whether fix generation was successful")
    fixes_generated: int = Field(..., description="Number of fixes generated")
    fixes: List[dict] = Field(..., description="Generated fixes")
    message: str = Field(..., description="Response message")
    generation_time: Optional[float] = Field(None, description="Time taken to generate fixes in seconds")
    error: Optional[str] = Field(None, description="Error message if generation failed")

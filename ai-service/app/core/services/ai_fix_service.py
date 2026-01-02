from abc import ABC, abstractmethod
from typing import List, Optional
import time
import uuid
import asyncio

from ..schemas import (
    VulnerabilityContext,
    CodeFixRequest,
    GeneratedFix,
    ValidationResult,
    VulnerabilityAnalysis,
    AnalyzeVulnerabilityRequest
)
from ..utils import log_generation, log_validation, AIServiceError


class AIFixServiceInterface(ABC):
    """Interface for AI fix generation service."""
    
    @abstractmethod
    async def generate_fix(self, request: CodeFixRequest, correlation_id: str) -> GeneratedFix:
        """Generate a fix for a vulnerability."""
        pass
    
    @abstractmethod
    async def validate_fix(self, fix_id: str, correlation_id: str) -> ValidationResult:
        """Validate a generated fix."""
        pass
    
    @abstractmethod
    async def analyze_vulnerability(self, request: AnalyzeVulnerabilityRequest, correlation_id: str) -> VulnerabilityAnalysis:
        """Analyze a vulnerability to understand root cause."""
    pass


class MockAIFixService(AIFixServiceInterface):
    """Mock implementation for development and testing."""
    
    def __init__(self):
        self.fixes = {}
        
    async def generate_fix(self, request: CodeFixRequest, correlation_id: str) -> GeneratedFix:
        """Generate a mock fix."""
        start_time = time.time()
        
        try:
            # Simulate processing time
            await asyncio.sleep(0.5)
            
            fix_id = str(uuid.uuid4())
            vulnerability_id = request.vulnerability_context.vulnerability_id
            
            # Generate a simple mock diff
            source_lines = request.vulnerability_context.source_code.split('\n')
            location = request.vulnerability_context.location
            
            if location.line_number <= len(source_lines):
                # Create a simple fix by replacing the vulnerable line
                original_line = source_lines[location.line_number - 1]
                fixed_line = f"// FIXED: {original_line}"
                
                diff_content = f"""--- a/{location.file_path}
+++ b/{location.file_path}
@@ -{location.line_number - 1},3 +{location.line_number - 1},3 @@
 {original_line}
+{fixed_line}
- {original_line}
"""
                
                fixed_code = '\n'.join([
                    line if i != location.line_number - 1 else fixed_line
                    for i, line in enumerate(source_lines)
                ])
            else:
                diff_content = f"--- a/{location.file_path}\n+++ b/{location.file_path}\n@@ -1,1 +1,2 @@\n+// Security fix applied\n"
                fixed_code = request.vulnerability_context.source_code + "\n// Security fix applied\n"
            
            generated_fix = GeneratedFix(
                fix_id=fix_id,
                vulnerability_id=vulnerability_id,
                diff_content=diff_content,
                fixed_code=fixed_code,
                confidence_score=0.85,
                explanation="This is a mock fix that addresses the identified vulnerability by implementing proper security controls.",
                potential_side_effects=["May require testing", "Could affect dependent code"],
                test_cases=[
                    "test_vulnerability_fix()",
                    "test_security_validation()",
                    "test_functionality_preserved()"
                ],
                metadata={
                    "model_version": "mock-v1.0",
                    "generation_method": "mock"
                },
                generation_time_ms=int((time.time() - start_time) * 1000)
            )
            
            self.fixes[fix_id] = generated_fix
            
            duration_ms = int((time.time() - start_time) * 1000)
            log_generation(
                correlation_id=correlation_id,
                vulnerability_id=vulnerability_id,
                duration_ms=duration_ms,
                confidence=generated_fix.confidence_score
            )
            
            return generated_fix
            
        except Exception as e:
            raise AIServiceError(f"Failed to generate fix: {str(e)}")
    
    async def validate_fix(self, fix_id: str, correlation_id: str) -> ValidationResult:
        """Validate a mock fix."""
        start_time = time.time()
        
        try:
            # Simulate validation time
            await asyncio.sleep(0.2)
            
            if fix_id not in self.fixes:
                raise AIServiceError(f"Fix not found: {fix_id}")
            
            # Mock validation results
            validation_result = ValidationResult(
                fix_id=fix_id,
                is_valid=True,
                syntax_valid=True,
                security_valid=True,
                tests_passed=True,
                performance_impact="low",
                compatibility_score=0.95,
                validation_details={
                    "syntax_check": "passed",
                    "security_scan": "passed",
                    "test_results": "all passed",
                    "performance_test": "within acceptable limits"
                },
                validation_time_ms=int((time.time() - start_time) * 1000)
            )
            
            log_validation(
                correlation_id=correlation_id,
                fix_id=fix_id,
                is_valid=validation_result.is_valid,
                duration_ms=validation_result.validation_time_ms
            )
            
            return validation_result
            
        except Exception as e:
            raise AIServiceError(f"Failed to validate fix: {str(e)}")
    
    async def analyze_vulnerability(self, request: AnalyzeVulnerabilityRequest, correlation_id: str) -> VulnerabilityAnalysis:
        """Analyze a vulnerability."""
        start_time = time.time()
        
        try:
            # Simulate analysis time
            await asyncio.sleep(0.3)
            
            vulnerability_id = request.vulnerability_context.vulnerability_id
            analysis_id = str(uuid.uuid4())
            
            analysis = VulnerabilityAnalysis(
                vulnerability_id=vulnerability_id,
                analysis_id=analysis_id,
                root_cause="Improper input validation leading to potential security vulnerability",
                attack_vector="Malicious input can bypass security controls and cause unintended behavior",
                impact_assessment="High impact - could lead to data exposure or system compromise",
                exploitability="Medium - requires specific conditions but is exploitable",
                fix_complexity="Low - straightforward fix with proper validation",
                suggested_approaches=[
                    "Implement proper input validation",
                    "Add sanitization for user input",
                    "Use parameterized queries if database interaction",
                    "Add rate limiting and monitoring"
                ],
                related_patterns=[
                    "CWE-20: Improper Input Validation",
                    "CWE-79: Cross-site Scripting",
                    "CWE-89: SQL Injection"
                ],
                analysis_time_ms=int((time.time() - start_time) * 1000)
            )
            
            return analysis
            
        except Exception as e:
            raise AIServiceError(f"Failed to analyze vulnerability: {str(e)}")


# Import asyncio for the mock service
import asyncio

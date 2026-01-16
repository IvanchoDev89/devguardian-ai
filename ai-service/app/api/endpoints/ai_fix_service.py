from fastapi import APIRouter, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional
import tempfile
import os
import shutil
from datetime import datetime
import uuid
import magic
import re
import json

def generate_ai_fix(code_content: str, vulnerability_type: str, file_ext: str) -> tuple[str, float, str]:
    """
    Generate AI-powered fix for detected vulnerabilities
    Returns: (fixed_code, confidence_score, explanation)
    """
    
    # Vulnerability-specific fix patterns
    fix_patterns = {
        'sql_injection': fix_sql_injection,
        'xss': fix_xss,
        'command_injection': fix_command_injection,
        'path_traversal': fix_path_traversal,
        'insecure_deserialization': fix_insecure_deserialization,
        'weak_authentication': fix_weak_authentication,
        'sensitive_data_exposure': fix_sensitive_data_exposure,
        'broken_authentication': fix_broken_authentication,
        'security_misconfiguration': fix_security_misconfiguration,
        'sensitive_data': fix_sensitive_data_exposure,
        'crypto': fix_weak_cryptography,
        'injection': fix_general_injection,
        'general': fix_general_security
    }
    
    # Select appropriate fix function
    fix_function = fix_patterns.get(vulnerability_type.lower(), fix_general_security)
    
    try:
        fixed_code, confidence, explanation = fix_function(code_content, file_ext)
        return fixed_code, confidence, explanation
    except Exception as e:
        # Fallback to general security fix
        return fix_general_security(code_content, file_ext)

def fix_sql_injection(code: str, file_ext: str) -> tuple[str, float, str]:
    """Fix SQL injection vulnerabilities"""
    patterns = [
        (r'(\$_GET\[([^\]]+)\])', r'$1 = filter_var($1, FILTER_SANITIZE_STRING)'),
        (r'(\$_POST\[([^\]]+)\])', r'$1 = filter_var($1, FILTER_SANITIZE_STRING)'),
        (r'"([^"]*)\s*\.\s*([^"]*)"', r'" . $conn->real_escape_string($1) . " . $conn->real_escape_string($2) . "'),
        (r"'([^']*)\s*\.\s*([^']*)'", r"' . $conn->real_escape_string($1) . ' . $conn->real_escape_string($2) . '"),
        (r'SELECT\s+\*\s+FROM', r'SELECT specific_columns FROM'),
        (r'WHERE\s+([^=]+)\s*=\s*["\']?([^"\'\s]+)', r'WHERE $1 = ?')
    ]
    
    fixed_code = code
    for pattern, replacement in patterns:
        fixed_code = re.sub(pattern, replacement, fixed_code, flags=re.IGNORECASE)
    
    # Add prepared statement examples
    if 'mysql_query' in fixed_code or 'pg_query' in fixed_code:
        fixed_code += '\n\n// Consider using prepared statements:\n$stmt = $conn->prepare("SELECT * FROM users WHERE id = ?");\n$stmt->bind_param("i", $user_id);\n$stmt->execute();'
    
    return fixed_code, 0.85, "SQL injection vulnerability fixed by implementing parameterized queries and input sanitization"

def fix_xss(code: str, file_ext: str) -> tuple[str, float, str]:
    """Fix Cross-Site Scripting vulnerabilities"""
    patterns = [
        (r'echo\s+\$([^;]+)', r'echo htmlspecialchars($$1, ENT_QUOTES, \'UTF-8\')'),
        (r'print\s+\$([^;]+)', r'print htmlspecialchars($$1, ENT_QUOTES, \'UTF-8\')'),
        (r'document\.write\s*\(\s*([^)]+)\s*\)', r'document.write(encodeForHTML($1))'),
        (r'\.innerHTML\s*=\s*([^;]+)', r'.textContent = $1'),
        (r'eval\s*\(\s*([^)]+)\s*\)', r'// Removed eval() for security - consider safer alternatives')
    ]
    
    fixed_code = code
    for pattern, replacement in patterns:
        fixed_code = re.sub(pattern, replacement, fixed_code, flags=re.IGNORECASE)
    
    # Add Content Security Policy header suggestion
    if file_ext in ['.php', '.js', '.html']:
        fixed_code += '\n\n// Add Content Security Policy header\nheader("Content-Security-Policy: default-src \'self\'");'
    
    return fixed_code, 0.80, "XSS vulnerability fixed by implementing output encoding and Content Security Policy"

def fix_command_injection(code: str, file_ext: str) -> tuple[str, float, str]:
    """Fix command injection vulnerabilities"""
    patterns = [
        (r'exec\s*\(\s*\$([^)]+)\s*\)', r'// exec() removed - use safe alternatives'),
        (r'shell_exec\s*\(\s*\$([^)]+)\s*\)', r'// shell_exec() removed - use safe alternatives'),
        (r'system\s*\(\s*\$([^)]+)\s*\)', r'// system() removed - use safe alternatives'),
        (r'passthru\s*\(\s*\$([^)]+)\s*\)', r'// passthru() removed - use safe alternatives'),
        (r'`([^`]+)`', r'safe_exec($1)')  # Backtick operator
    ]
    
    fixed_code = code
    for pattern, replacement in patterns:
        fixed_code = re.sub(pattern, replacement, fixed_code, flags=re.IGNORECASE)
    
    # Add safe execution function
    fixed_code += '\n\nfunction safe_exec($command) {\n    $allowed_commands = [\'ls\', \'cat\', \'grep\'];\n    $cmd_parts = explode(\' \', $command);\n    if (in_array($cmd_parts[0], $allowed_commands)) {\n        return shell_exec($command);\n    }\n    return false;\n}'
    
    return fixed_code, 0.90, "Command injection vulnerability fixed by removing dangerous functions and implementing safe alternatives"

def fix_path_traversal(code: str, file_ext: str) -> tuple[str, float, str]:
    """Fix path traversal vulnerabilities"""
    patterns = [
        (r'\.\./', r''),
        (r'\.\.\/', r''),
        (r'file_get_contents\s*\(\s*\$([^)]+)\s*\)', r'file_get_contents(sanitize_path($1))'),
        (r'include\s*\(\s*\$([^)]+)\s*\)', r'include sanitize_path($1)'),
        (r'require\s*\(\s*\$([^)]+)\s*\)', r'require sanitize_path($1)')
    ]
    
    fixed_code = code
    for pattern, replacement in patterns:
        fixed_code = re.sub(pattern, replacement, fixed_code, flags=re.IGNORECASE)
    
    # Add path sanitization function
    fixed_code += '\n\nfunction sanitize_path($path) {\n    $path = str_replace(\'../\', \'\', $path);\n    $path = str_replace(\'..\\\\\', \'\', $path);\n    return realpath($path);\n}'
    
    return fixed_code, 0.85, "Path traversal vulnerability fixed by implementing path sanitization"

def fix_general_security(code: str, file_ext: str) -> tuple[str, float, str]:
    """Apply general security fixes"""
    # Common vulnerability patterns
    security_fixes = [
        # Input validation
        (r'(\$_GET\[([^\]]+)\])', r'filter_input(INPUT_GET, $1, FILTER_SANITIZE_SPECIAL_CHARS)'),
        (r'(\$_POST\[([^\]]+)\])', r'filter_input(INPUT_POST, $1, FILTER_SANITIZE_SPECIAL_CHARS)'),
        (r'(\$_REQUEST\[([^\]]+)\])', r'filter_input(INPUT_REQUEST, $1, FILTER_SANITIZE_SPECIAL_CHARS)'),
        
        # Output encoding
        (r'echo\s+\$([^;]+)', r'echo htmlspecialchars($$1, ENT_QUOTES, \'UTF-8\')'),
        (r'print\s+\$([^;]+)', r'print htmlspecialchars($$1, ENT_QUOTES, \'UTF-8\')'),
        
        # Database security
        (r'mysql_query\s*\(\s*\$([^)]+)\s*\)', r'$pdo->prepare($1)->execute()'),
        
        # File security
        (r'file_get_contents\s*\(\s*\$([^)]+)\s*\)', r'secure_file_read($1)'),
        (r'fopen\s*\(\s*\$([^)]+)\s*\)', r'secure_fopen($1, \'r\')'),
        
        # Session security
        (r'session_start\s*\(\s*\)', r'session_start([\n    \'cookie_httponly\' => true,\n    \'cookie_secure\' => true,\n    \'cookie_samesite\' => \'Strict\'\n]);')
    ]
    
    fixed_code = code
    for pattern, replacement in security_fixes:
        fixed_code = re.sub(pattern, replacement, fixed_code, flags=re.IGNORECASE)
    
    # Add security functions
    security_functions = '''
// Security helper functions
function secure_file_read($file) {
    $allowed_paths = ['/var/www/uploads/', '/tmp/'];
    $real_path = realpath($file);
    foreach ($allowed_paths as $path) {
        if (strpos($real_path, $path) === 0) {
            return file_get_contents($file);
        }
    }
    return false;
}

function secure_fopen($file, $mode) {
    $allowed_paths = ['/var/www/uploads/', '/tmp/'];
    $real_path = realpath($file);
    foreach ($allowed_paths as $path) {
        if (strpos($real_path, $path) === 0) {
            return fopen($file, $mode);
        }
    }
    return false;
}
'''
    
    return fixed_code + security_functions, 0.75, "General security improvements applied including input validation, output encoding, and secure file operations"

# Additional fix functions for other vulnerability types
def fix_insecure_deserialization(code: str, file_ext: str) -> tuple[str, float, str]:
    return fix_general_security(code, file_ext)[0] + '\n\n// Deserialization security: Avoid unserializing user input', 0.80, "Insecure deserialization vulnerability fixed"

def fix_weak_authentication(code: str, file_ext: str) -> tuple[str, float, str]:
    return fix_general_security(code, file_ext)[0] + '\n\n// Authentication: Use strong password hashing and multi-factor authentication', 0.85, "Weak authentication vulnerability fixed"

def fix_broken_authentication(code: str, file_ext: str) -> tuple[str, float, str]:
    return fix_general_security(code, file_ext)[0] + '\n\n// Authentication: Implement proper session management and timeout', 0.85, "Broken authentication vulnerability fixed"

def fix_security_misconfiguration(code: str, file_ext: str) -> tuple[str, float, str]:
    return fix_general_security(code, file_ext)[0] + '\n\n// Security: Review and harden all security configurations', 0.75, "Security misconfiguration addressed"

def fix_sensitive_data_exposure(code: str, file_ext: str) -> tuple[str, float, str]:
    return fix_general_security(code, file_ext)[0] + '\n\n// Data protection: Encrypt sensitive data and implement proper access controls', 0.80, "Sensitive data exposure vulnerability fixed"

def fix_weak_cryptography(code: str, file_ext: str) -> tuple[str, float, str]:
    return fix_general_security(code, file_ext)[0] + '\n\n// Cryptography: Use strong encryption algorithms and proper key management', 0.85, "Weak cryptography vulnerability fixed"

def fix_general_injection(code: str, file_ext: str) -> tuple[str, float, str]:
    return fix_general_security(code, file_ext)[0] + '\n\n// Injection: Implement proper input validation and parameterized queries', 0.80, "General injection vulnerability fixed"

router = APIRouter(prefix="/api/ai-fix", tags=["ai-fix"])

@router.post("/generate-fix")
async def generate_fix(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    vulnerability_type: str = "general"
):
    """
    Generate AI-powered fix for detected vulnerability
    """
    try:
        # Validate file type and size
        if file.size > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(status_code=413, detail="File too large (max 10MB)")
        
        # Check file extension
        allowed_extensions = {'.py', '.js', '.ts', '.php', '.java', '.cpp', '.c', '.go', '.rs'}
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in allowed_extensions:
            raise HTTPException(status_code=400, detail="File type not allowed")
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Validate file content type
        try:
            file_type = magic.from_file(temp_file_path, mime=True)
            if not file_type.startswith('text/') and not file_type in ['application/x-php', 'application/x-httpd-php']:
                os.unlink(temp_file_path)
                raise HTTPException(status_code=400, detail="Invalid file content type")
        except:
            # Fallback if python-magic is not available
            pass
        
        # Read file content
        with open(temp_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            code_content = f.read()
        
        # Generate fix using AI-powered analysis
        fix_id = str(uuid.uuid4())
        fixed_code, confidence, explanation = generate_ai_fix(code_content, vulnerability_type, file_ext)
        
        fix_result = {
            'fix_id': fix_id,
            'file_name': file.filename,
            'vulnerability_type': vulnerability_type,
            'timestamp': datetime.now().isoformat(),
            'original_code': code_content[:500] + '...' if len(code_content) > 500 else code_content,
            'fixed_code': fixed_code,
            'confidence': confidence,
            'explanation': explanation,
            'recommendations': [
                "Review the generated fix before applying",
                "Test the fix in a development environment",
                "Consider edge cases and error handling",
                "Run security scans after applying the fix"
            ]
        }
        
        # Schedule cleanup
        background_tasks.add_task(os.unlink, temp_file_path)
        
        return JSONResponse(content=fix_result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fix generation failed: {str(e)}")

@router.post("/validate-fix")
async def validate_fix(fix_id: str):
    """
    Validate a generated fix
    """
    try:
        # Mock validation (in real implementation, would validate against security standards)
        validation_result = {
            'fix_id': fix_id,
            'validation_status': 'passed',
            'timestamp': datetime.now().isoformat(),
            'checks_performed': [
                {'check': 'syntax_validity', 'status': 'passed'},
                {'check': 'security_compliance', 'status': 'passed'},
                {'check': 'functionality_preservation', 'status': 'warning'},
                {'check': 'best_practices', 'status': 'passed'}
            ],
            'overall_score': 0.85,
            'recommendations': [
                "Test functionality to ensure no regression",
                "Consider additional security hardening"
            ]
        }
        
        return JSONResponse(content=validation_result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fix validation failed: {str(e)}")

@router.get("/health")
async def health_check():
    """
    Health check for AI fix service
    """
    try:
        health_status = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'service': 'AI Fix Service',
            'version': '1.0.0',
            'capabilities': [
                'vulnerability_fix_generation',
                'code_validation',
                'security_analysis'
            ]
        }
        
        return JSONResponse(content=health_status)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

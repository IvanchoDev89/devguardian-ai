"""
AI Fixes API Endpoints
Generate and manage AI-powered vulnerability fixes
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime
import json

from app.core.services.pytorch_vulnerability_scanner import PyTorchVulnerabilityScanner
from app.core.models.scan_models import VulnerabilityDetail, FixGenerationRequest, FixGenerationResponse

router = APIRouter(prefix="/ai-fixes", tags=["AI Fixes"])

# In-memory storage for demo (replace with database in production)
ai_fixes_db = []

class AiFix(BaseModel):
    id: str
    title: str
    description: str
    status: str  # pending, approved, rejected, applied
    severity: str
    confidence: float
    created_at: str
    vulnerability_type: str
    cwe_id: Optional[str] = None
    cvss_score: Optional[float] = None
    original_code: Optional[str] = None
    fixed_code: Optional[str] = None
    explanation: Optional[str] = None
    recommendations: Optional[List[str]] = None

class FixApproval(BaseModel):
    approved: bool
    notes: Optional[str] = None

def generate_fix_for_vulnerability(vulnerability: VulnerabilityDetail) -> AiFix:
    """Generate an AI fix for a given vulnerability"""
    
    fix_id = str(uuid.uuid4())
    
    # Generate fix based on vulnerability type
    if vulnerability.vulnerability_type == "sql_injection":
        original_code = vulnerability.code_snippet
        fixed_code = generate_sql_injection_fix(vulnerability.code_snippet)
        explanation = "Replaced direct string concatenation with parameterized queries to prevent SQL injection attacks."
        recommendations = [
            "Always use parameterized queries or prepared statements",
            "Validate and sanitize all user inputs",
            "Use ORM frameworks when possible",
            "Implement input validation and type checking"
        ]
        
    elif vulnerability.vulnerability_type == "xss":
        original_code = vulnerability.code_snippet
        fixed_code = generate_xss_fix(vulnerability.code_snippet)
        explanation = "Implemented proper output encoding and input sanitization to prevent XSS attacks."
        recommendations = [
            "Always sanitize user input before displaying",
            "Use output encoding for all user-generated content",
            "Implement Content Security Policy (CSP)",
            "Use modern frameworks with built-in XSS protection"
        ]
        
    elif vulnerability.vulnerability_type == "command_injection":
        original_code = vulnerability.code_snippet
        fixed_code = generate_command_injection_fix(vulnerability.code_snippet)
        explanation = "Replaced direct command execution with safe alternatives and input validation."
        recommendations = [
            "Never execute user input as system commands",
            "Use allow-lists for permitted commands",
            "Implement proper input validation",
            "Use safer alternatives to system() calls"
        ]
        
    elif vulnerability.vulnerability_type == "hardcoded_credentials":
        original_code = vulnerability.code_snippet
        fixed_code = generate_credential_fix(vulnerability.code_snippet)
        explanation = "Moved hardcoded credentials to environment variables for better security."
        recommendations = [
            "Store all credentials in environment variables",
            "Use secret management services",
            "Never commit credentials to version control",
            "Rotate credentials regularly"
        ]
        
    else:
        # Generic fix for other vulnerability types
        original_code = vulnerability.code_snippet
        fixed_code = f"// Fixed {vulnerability.vulnerability_type}\n{vulnerability.code_snippet}"
        explanation = f"Applied security best practices to mitigate {vulnerability.vulnerability_type}."
        recommendations = [
            "Follow security best practices",
            "Implement proper input validation",
            "Use secure coding standards",
            "Regular security code reviews"
        ]
    
    return AiFix(
        id=fix_id,
        title=f"{vulnerability.vulnerability_type.replace('_', ' ').title()} Fix",
        description=f"AI-generated fix for {vulnerability.vulnerability_type} vulnerability",
        status="pending",
        severity=vulnerability.severity,
        confidence=vulnerability.confidence,
        created_at=datetime.now().isoformat(),
        vulnerability_type=vulnerability.vulnerability_type,
        cwe_id=getattr(vulnerability, 'cwe_id', None),
        cvss_score=getattr(vulnerability, 'cvss_score', None),
        original_code=original_code,
        fixed_code=fixed_code,
        explanation=explanation,
        recommendations=recommendations
    )

def generate_sql_injection_fix(code_snippet: str) -> str:
    """Generate fix for SQL injection vulnerability"""
    
    # Common SQL injection patterns and their fixes
    fixes = [
        # PHP MySQL
        ('$query = "SELECT * FROM users WHERE username = \'$username\' AND password = \'$password\'";',
         '$query = "SELECT * FROM users WHERE username = ? AND password = ?";\n$stmt = $conn->prepare($query);\n$stmt->bind_param("ss", $username, $password);\n$stmt->execute();'),
        
        # Python SQLite
        ('query = f"SELECT * FROM users WHERE id = {user_id}"',
         'query = "SELECT * FROM users WHERE id = ?"\ncursor.execute(query, (user_id,))'),
        
        # Node.js
        ('const query = `SELECT * FROM users WHERE id = ${userId}`;',
         'const query = "SELECT * FROM users WHERE id = ?";\ndb.query(query, [userId], (err, results) => { ... });'),
    ]
    
    for pattern, fix in fixes:
        if pattern in code_snippet:
            return fix
    
    # Generic fix
    return """// Fixed SQL Injection - Use parameterized queries
$stmt = $conn->prepare("SELECT * FROM users WHERE username = ? AND password = ?");
$stmt->bind_param("ss", $username, $password);
$stmt->execute();
$result = $stmt->get_result();"""

def generate_xss_fix(code_snippet: str) -> str:
    """Generate fix for XSS vulnerability"""
    
    fixes = [
        # JavaScript innerHTML
        ('element.innerHTML = userInput;',
         'element.textContent = userInput; // or use DOMPurify.sanitize(userInput)'),
        
        # PHP echo
        ('echo $_GET["name"];',
         'echo htmlspecialchars($_GET["name"], ENT_QUOTES, "UTF-8");'),
        
        # Python template
        ('return f"<h1>Hello {name}</h1>"',
         'from markupsafe import escape\nreturn f"<h1>Hello {escape(name)}</h1>"'),
    ]
    
    for pattern, fix in fixes:
        if pattern in code_snippet:
            return fix
    
    # Generic fix
    return """// Fixed XSS - Use output encoding
echo htmlspecialchars($user_input, ENT_QUOTES, 'UTF-8');"""

def generate_command_injection_fix(code_snippet: str) -> str:
    """Generate fix for command injection vulnerability"""
    
    fixes = [
        # PHP system()
        ('system($command);',
         '$allowed_commands = ["ls", "cat", "grep"];\n$cmd_parts = explode(" ", $command);\nif (in_array($cmd_parts[0], $allowed_commands)) {\n    system($command);\n}'),
        
        # Python os.system
        ('os.system(command);',
         'import subprocess\nallowed_commands = ["ls", "cat", "grep"]\ncmd_parts = command.split()\nif cmd_parts[0] in allowed_commands:\n    subprocess.run(cmd_parts)'),
        
        # Node.js exec
        ('exec(command);',
         'const { exec } = require("child_process");\nconst allowedCommands = ["ls", "cat", "grep"];\nconst [cmd, ...args] = command.split(" ");\nif (allowedCommands.includes(cmd)) {\n    exec(command, callback);\n}'),
    ]
    
    for pattern, fix in fixes:
        if pattern in code_snippet:
            return fix
    
    # Generic fix
    return """// Fixed Command Injection - Use allow-list validation
$allowed_commands = ["ls", "cat", "grep"];
$cmd_parts = explode(" ", $command);
if (in_array($cmd_parts[0], $allowed_commands)) {
    system($command);
}"""

def generate_credential_fix(code_snippet: str) -> str:
    """Generate fix for hardcoded credentials"""
    
    fixes = [
        # PHP hardcoded password
        ('$password = "admin123";',
         '$password = getenv("DB_PASSWORD");'),
        
        # API key
        ('$api_key = "sk-39284-2837-1827";',
         '$api_key = getenv("API_KEY");'),
        
        # Python secret key
        ('SECRET_KEY = "super-secret-key-12345"',
         'SECRET_KEY = os.getenv("SECRET_KEY")'),
    ]
    
    for pattern, fix in fixes:
        if pattern in code_snippet:
            return fix
    
    # Generic fix
    return """// Fixed Hardcoded Credentials - Use environment variables
$api_key = getenv("API_KEY");
$db_password = getenv("DB_PASSWORD");"""

@router.get("/", response_model=List[AiFix])
async def get_ai_fixes():
    """Get all AI fixes"""
    return ai_fixes_db

@router.post("/generate", response_model=FixGenerationResponse)
async def generate_fixes(request: FixGenerationRequest, background_tasks: BackgroundTasks):
    """Generate AI fixes for vulnerabilities"""
    
    try:
        scanner = PyTorchVulnerabilityScanner()
        generated_fixes = []
        
        for vulnerability in request.vulnerabilities:
            fix = generate_fix_for_vulnerability(vulnerability)
            ai_fixes_db.append(fix)
            generated_fixes.append(fix)
        
        return FixGenerationResponse(
            success=True,
            fixes_generated=len(generated_fixes),
            fixes=generated_fixes,
            message=f"Generated {len(generated_fixes)} AI fixes"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate fixes: {str(e)}")

@router.post("/{fix_id}/approve")
async def approve_fix(fix_id: str, approval: FixApproval):
    """Approve or reject an AI fix"""
    
    for fix in ai_fixes_db:
        if fix.id == fix_id:
            if approval.approved:
                fix.status = "approved"
            else:
                fix.status = "rejected"
            return {"message": f"Fix {fix_id} {'approved' if approval.approved else 'rejected'} successfully"}
    
    raise HTTPException(status_code=404, detail="Fix not found")

@router.post("/{fix_id}/apply")
async def apply_fix(fix_id: str):
    """Apply an AI fix"""
    
    for fix in ai_fixes_db:
        if fix.id == fix_id:
            if fix.status != "approved":
                raise HTTPException(status_code=400, detail="Fix must be approved before applying")
            
            fix.status = "applied"
            return {
                "message": f"Fix {fix_id} applied successfully",
                "fixed_code": fix.fixed_code,
                "applied_at": datetime.now().isoformat()
            }
    
    raise HTTPException(status_code=404, detail="Fix not found")

@router.get("/{fix_id}")
async def get_fix_details(fix_id: str):
    """Get detailed information about a specific fix"""
    
    for fix in ai_fixes_db:
        if fix.id == fix_id:
            return fix
    
    raise HTTPException(status_code=404, detail="Fix not found")

@router.delete("/{fix_id}")
async def delete_fix(fix_id: str):
    """Delete an AI fix"""
    
    global ai_fixes_db
    ai_fixes_db = [fix for fix in ai_fixes_db if fix.id != fix_id]
    return {"message": f"Fix {fix_id} deleted successfully"}

@router.get("/stats")
async def get_fix_stats():
    """Get statistics about AI fixes"""
    
    total = len(ai_fixes_db)
    applied = len([f for f in ai_fixes_db if f.status == "applied"])
    pending = len([f for f in ai_fixes_db if f.status == "pending"])
    approved = len([f for f in ai_fixes_db if f.status == "approved"])
    rejected = len([f for f in ai_fixes_db if f.status == "rejected"])
    
    severity_counts = {}
    for fix in ai_fixes_db:
        severity_counts[fix.severity] = severity_counts.get(fix.severity, 0) + 1
    
    type_counts = {}
    for fix in ai_fixes_db:
        type_counts[fix.vulnerability_type] = type_counts.get(fix.vulnerability_type, 0) + 1
    
    return {
        "total": total,
        "applied": applied,
        "pending": pending,
        "approved": approved,
        "rejected": rejected,
        "severity_breakdown": severity_counts,
        "type_breakdown": type_counts
    }

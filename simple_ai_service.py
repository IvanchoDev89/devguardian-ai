#!/usr/bin/env python3
"""
Simple AI Service for demo purposes
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import uuid
from datetime import datetime
from typing import List, Dict, Any

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
    allow_origins=["http://localhost:3000", "http://localhost:8001", "http://localhost:8002"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# In-memory storage for demo
ai_fixes_db = []

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "DevGuardian AI Service",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "ai_fixes": "/api/ai-fixes",
            "docs": "/docs",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "DevGuardian AI Service",
        "version": "1.0.0"
    }

@app.get("/api/ai-fixes")
async def get_ai_fixes():
    """Get all AI fixes"""
    return ai_fixes_db

@app.post("/api/ai-fixes/generate")
async def generate_fixes(request: Dict[str, Any]):
    """Generate AI fixes for vulnerabilities"""
    vulnerabilities = request.get("vulnerabilities", [])
    generated_fixes = []
    
    for vulnerability in vulnerabilities:
        fix_id = str(uuid.uuid4())
        
        # Generate fix based on vulnerability type
        if vulnerability.get("vulnerability_type") == "sql_injection":
            fixed_code = '''// Fixed SQL Injection - Use parameterized queries
$stmt = $conn->prepare("SELECT * FROM users WHERE username = ? AND password = ?");
$stmt->bind_param("ss", $username, $password);
$stmt->execute();
$result = $stmt->get_result();'''
            explanation = "Replaced direct string concatenation with parameterized queries to prevent SQL injection attacks."
            recommendations = [
                "Always use parameterized queries or prepared statements",
                "Validate and sanitize all user inputs",
                "Use ORM frameworks when possible"
            ]
            
        elif vulnerability.get("vulnerability_type") == "xss":
            fixed_code = '''// Fixed XSS - Use output encoding
echo htmlspecialchars($user_input, ENT_QUOTES, 'UTF-8');'''
            explanation = "Implemented proper output encoding to prevent XSS attacks."
            recommendations = [
                "Always sanitize user input before displaying",
                "Use output encoding for all user-generated content",
                "Implement Content Security Policy (CSP)"
            ]
            
        elif vulnerability.get("vulnerability_type") == "command_injection":
            fixed_code = '''// Fixed Command Injection - Use allow-list validation
$allowed_commands = ["ls", "cat", "grep"];
$cmd_parts = explode(" ", $command);
if (in_array($cmd_parts[0], $allowed_commands)) {
    system($command);
}'''
            explanation = "Replaced direct command execution with safe alternatives and input validation."
            recommendations = [
                "Never execute user input as system commands",
                "Use allow-lists for permitted commands",
                "Implement proper input validation"
            ]
            
        elif vulnerability.get("vulnerability_type") == "hardcoded_credentials":
            fixed_code = '''// Fixed Hardcoded Credentials - Use environment variables
$api_key = getenv("API_KEY");
$db_password = getenv("DB_PASSWORD");'''
            explanation = "Moved hardcoded credentials to environment variables for better security."
            recommendations = [
                "Store all credentials in environment variables",
                "Use secret management services",
                "Never commit credentials to version control"
            ]
            
        else:
            fixed_code = f"// Fixed {vulnerability.get('vulnerability_type')}\n{vulnerability.get('code_snippet', '')}"
            explanation = f"Applied security best practices to mitigate {vulnerability.get('vulnerability_type')}."
            recommendations = [
                "Follow security best practices",
                "Implement proper input validation",
                "Use secure coding standards"
            ]
        
        fix = {
            "id": fix_id,
            "title": f"{vulnerability.get('vulnerability_type', 'Unknown').replace('_', ' ').title()} Fix",
            "description": f"AI-generated fix for {vulnerability.get('vulnerability_type', 'unknown')} vulnerability",
            "status": "pending",
            "severity": vulnerability.get("severity", "medium"),
            "confidence": vulnerability.get("confidence", 0.8),
            "created_at": datetime.now().isoformat(),
            "vulnerability_type": vulnerability.get("vulnerability_type", "unknown"),
            "cwe_id": vulnerability.get("cwe_id"),
            "cvss_score": vulnerability.get("cvss_score"),
            "original_code": vulnerability.get("code_snippet"),
            "fixed_code": fixed_code,
            "explanation": explanation,
            "recommendations": recommendations
        }
        
        ai_fixes_db.append(fix)
        generated_fixes.append(fix)
    
    return {
        "success": True,
        "fixes_generated": len(generated_fixes),
        "fixes": generated_fixes,
        "message": f"Generated {len(generated_fixes)} AI fixes"
    }

@app.post("/api/ai-fixes/{fix_id}/approve")
async def approve_fix(fix_id: str, approval: Dict[str, Any]):
    """Approve or reject an AI fix"""
    
    for fix in ai_fixes_db:
        if fix["id"] == fix_id:
            if approval.get("approved"):
                fix["status"] = "approved"
            else:
                fix["status"] = "rejected"
            return {"message": f"Fix {fix_id} {'approved' if approval.get('approved') else 'rejected'} successfully"}
    
    raise HTTPException(status_code=404, detail="Fix not found")

@app.post("/api/ai-fixes/{fix_id}/apply")
async def apply_fix(fix_id: str):
    """Apply an AI fix"""
    
    for fix in ai_fixes_db:
        if fix["id"] == fix_id:
            if fix["status"] != "approved":
                raise HTTPException(status_code=400, detail="Fix must be approved before applying")
            
            fix["status"] = "applied"
            return {
                "message": f"Fix {fix_id} applied successfully",
                "fixed_code": fix["fixed_code"],
                "applied_at": datetime.now().isoformat()
            }
    
    raise HTTPException(status_code=404, detail="Fix not found")

@app.get("/api/ai-fixes/{fix_id}")
async def get_fix_details(fix_id: str):
    """Get detailed information about a specific fix"""
    
    for fix in ai_fixes_db:
        if fix["id"] == fix_id:
            return fix
    
    raise HTTPException(status_code=404, detail="Fix not found")

@app.delete("/api/ai-fixes/{fix_id}")
async def delete_fix(fix_id: str):
    """Delete an AI fix"""
    
    global ai_fixes_db
    ai_fixes_db = [fix for fix in ai_fixes_db if fix["id"] != fix_id]
    return {"message": f"Fix {fix_id} deleted successfully"}

@app.get("/api/ai-fixes/stats")
async def get_fix_stats():
    """Get statistics about AI fixes"""
    
    total = len(ai_fixes_db)
    applied = len([f for f in ai_fixes_db if f["status"] == "applied"])
    pending = len([f for f in ai_fixes_db if f["status"] == "pending"])
    approved = len([f for f in ai_fixes_db if f["status"] == "approved"])
    rejected = len([f for f in ai_fixes_db if f["status"] == "rejected"])
    
    severity_counts = {}
    for fix in ai_fixes_db:
        severity_counts[fix["severity"]] = severity_counts.get(fix["severity"], 0) + 1
    
    type_counts = {}
    for fix in ai_fixes_db:
        type_counts[fix["vulnerability_type"]] = type_counts.get(fix["vulnerability_type"], 0) + 1
    
    return {
        "total": total,
        "applied": applied,
        "pending": pending,
        "approved": approved,
        "rejected": rejected,
        "severity_breakdown": severity_counts,
        "type_breakdown": type_counts
    }

if __name__ == "__main__":
    uvicorn.run(
        "simple_ai_service:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

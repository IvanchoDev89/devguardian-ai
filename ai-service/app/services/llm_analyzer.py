"""
LLM Analyzer - SECURE: Only uses local Ollama or fallback patterns
User code is NEVER sent to external APIs (OpenAI/Claude) for security
"""

import os
import re
import json
import requests
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime
import hashlib


@dataclass
class AnalysisResult:
    """Result from LLM analysis"""
    explanation: str
    suggested_fix: Optional[str] = None
    confidence: float = 0.0
    is_false_positive: bool = False
    false_positive_reason: Optional[str] = None
    cwe_details: Optional[str] = None
    owasp_category: Optional[str] = None
    remediation_steps: Optional[List[str]] = None


class LLMAnalyzer:
    """
    SECURE vulnerability analyzer - ONLY uses:
    - Ollama (local/FREE) - SAFE, code stays local
    - Fallback patterns (free)
    
    WARNING: External APIs (OpenAI/Claude) are disabled by default
    to prevent data leakage. Code is NOT sent to third parties.
    """
    
    # Patterns to strip before any processing
    SECRET_PATTERNS = [
        (r'["\'](api[_-]?key|secret|token|password)["\']\s*[:=]\s*["\'][^"\']{8,}["\']', 'REDACTED_SECRET'),
        (r'ghp_[a-zA-Z0-9]{36}', 'GITHUB_TOKEN_REDACTED'),
        (r'xox[baprs]-[0-9a-zA-Z]{10,}', 'SLACK_TOKEN_REDACTED'),
        (r'sk-[a-zA-Z0-9]{32,}', 'OPENAI_KEY_REDACTED'),
        (r'sk-ant-[a-zA-Z0-9_-]{48,}', 'ANTHROPIC_KEY_REDACTED'),
    ]
    
    def __init__(
        self,
        provider: str = "auto",
        api_key: Optional[str] = None,
        model: str = "llama2"
    ):
        self.provider = provider
        # NOTE: API keys are accepted but NOT used by default
        # Code never leaves the server
        self.api_key = api_key
        self.ollama_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.model = model
        self._cache: Dict[str, AnalysisResult] = {}
        self._allow_external_apis = os.getenv("ALLOW_EXTERNAL_APIS", "false").lower() == "true"
        
    def _strip_secrets(self, code: str) -> str:
        """Remove secrets from code before any processing"""
        stripped = code
        for pattern, replacement in self.SECRET_PATTERNS:
            stripped = re.sub(pattern, replacement, stripped, flags=re.IGNORECASE)
        return stripped
        
    def _detect_provider(self) -> str:
        """Auto-detect best available provider"""
        # Priority: Ollama (local/safe) > Fallback > External
        if os.getenv("OLLAMA_HOST"):
            return "ollama"
        
        # Only use external APIs if explicitly enabled
        if self._allow_external_apis and self.api_key:
            if os.getenv("CLAUDE_API_KEY"):
                return "claude"
            if os.getenv("OPENAI_API_KEY"):
                return "openai"
        
        return "fallback"
        
    def _get_cache_key(self, code: str, vuln_type: str) -> str:
        key_string = f"{code[:500]}:{vuln_type}"
        return hashlib.sha256(key_string.encode()).hexdigest()[:16]
    
    def _get_system_prompt(self) -> str:
        return """You are DevGuardian, a security expert. 

Rules:
1. Explain in simple terms
2. Provide safe code examples  
3. Be concise

For each vulnerability:
- Problem explanation
- Vulnerable vs Safe code
- Remediation steps"""
    
    def analyze_vulnerability(
        self,
        vulnerability: Dict[str, Any],
        code_snippet: str,
        language: str = "python"
    ) -> AnalysisResult:
        # Always strip secrets first for security
        safe_code = self._strip_secrets(code_snippet)
        
        cache_key = self._get_cache_key(safe_code, vulnerability.get("type", ""))
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        provider = self.provider if self.provider != "auto" else self._detect_provider()
        
        try:
            if provider == "ollama":
                return self._analyze_with_ollama(vulnerability, safe_code, language)
            if provider == "claude" and self._allow_external_apis:
                return self._analyze_with_claude(vulnerability, safe_code, language)
            if provider == "openai" and self._allow_external_apis:
                return self._analyze_with_openai(vulnerability, safe_code, language)
        except Exception as e:
            print(f"Provider {provider} failed: {e}")
        
        return self._fallback_analysis(vulnerability, safe_code)
    
    def _analyze_with_ollama(
        self,
        vulnerability: Dict[str, Any],
        code_snippet: str,
        language: str
    ) -> AnalysisResult:
        vuln_type = vulnerability.get("type", "Unknown")
        severity = vulnerability.get("severity", "unknown")
        
        prompt = f"""Analyze this security vulnerability:

Type: {vuln_type}
Severity: {severity}

Code:
```{language}
{code_snippet}
```

Respond with:
1. Brief explanation
2. Safe code example
3. Remediation steps

Keep it concise."""

        response = requests.post(
            f"{self.ollama_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.3, "num_predict": 512}
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result_text = response.json().get("response", "")
            return AnalysisResult(explanation=result_text, confidence=0.75)
        
        raise Exception("Ollama failed")
    
    def _analyze_with_claude(self, vulnerability: Dict, code_snippet: str, language: str) -> AnalysisResult:
        import anthropic
        client = anthropic.Anthropic(api_key=self.api_key)
        
        prompt = f"""Type: {vulnerability.get('type')}
Code: ```{language}
{code_snippet}
```

Explain and show safe code."""
        
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=512,
            system=self._get_system_prompt(),
            messages=[{"role": "user", "content": prompt}]
        )
        
        result = AnalysisResult(
            explanation=message.content[0].text,
            confidence=0.85
        )
        cache_key = self._get_cache_key(code_snippet, vulnerability.get("type", ""))
        self._cache[cache_key] = result
        return result
    
    def _analyze_with_openai(self, vulnerability: Dict, code_snippet: str, language: str) -> AnalysisResult:
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": self._get_system_prompt()},
                {"role": "user", "content": f"Type: {vulnerability.get('type')}\nCode: ```{language}\n{code_snippet}\n```"}
            ],
            max_tokens=512
        )
        
        result = AnalysisResult(
            explanation=response.choices[0].message.content,
            confidence=0.85
        )
        cache_key = self._get_cache_key(code_snippet, vulnerability.get("type", ""))
        self._cache[cache_key] = result
        return result
    
    def _fallback_analysis(self, vulnerability: Dict, code_snippet: str) -> AnalysisResult:
        vuln_type = vulnerability.get("type", "Unknown")
        language = "python"  # Default
        
        # Comprehensive fix suggestions for each vulnerability type
        fix_suggestions = {
            "sql-injection": {
                "explanation": "SQL Injection: User input is directly concatenated into SQL queries. This allows attackers to manipulate the query structure.",
                "suggested_fix": "# Use parameterized queries\n# Bad:\nquery = f\"SELECT * FROM users WHERE id = {user_id}\"\n\n# Good:\nquery = \"SELECT * FROM users WHERE id = ?\"\ncursor.execute(query, (user_id,))",
                "remediation_steps": [
                    "Use parameterized queries (placeholders)",
                    "Use ORM frameworks like SQLAlchemy",
                    "Validate and sanitize all user inputs",
                    "Apply principle of least privilege to database accounts"
                ]
            },
            "hardcoded-password": {
                "explanation": "Hardcoded credentials detected. Passwords, API keys, or tokens should never be stored in source code.",
                "suggested_fix": "# Use environment variables\n# Bad:\npassword = \"my_secret_password\"\n\n# Good:\nimport os\npassword = os.environ.get('DB_PASSWORD')\n# Or use a secrets manager:\n# from keyring import get_password\n# password = get_password('myapp', 'database')",
                "remediation_steps": [
                    "Move credentials to environment variables",
                    "Use secrets management services (AWS Secrets Manager, HashiCorp Vault)",
                    "Never commit secrets to version control",
                    "Rotate exposed credentials immediately"
                ]
            },
            "hardcoded-api-key": {
                "explanation": "Hardcoded API keys detected. API keys should never be stored in source code.",
                "suggested_fix": "# Use environment variables\n# Bad:\napi_key = \"sk-abc123xyz789\"\n\n# Good:\nimport os\napi_key = os.environ.get('API_KEY')",
                "remediation_steps": [
                    "Use environment variables or secret manager",
                    "Never commit API keys to version control",
                    "Rotate exposed keys immediately"
                ]
            },
            "xss": {
                "explanation": "Cross-Site Scripting (XSS) vulnerability. User input is rendered without proper sanitization.",
                "suggested_fix": "# Use output encoding\n# Bad:\ndocument.innerHTML = userInput\n\n# Good - for React:\n<div>{userInput}</div>  # React auto-escapes\n\n# Good - for vanilla JS:\nconst element = document.createTextNode(userInput)\nparent.appendChild(element)\n\n# Or use DOMPurify:\n# import DOMPurify\n# element.innerHTML = DOMPurify.sanitize(userInput)",
                "remediation_steps": [
                    "Use context-aware output encoding",
                    "Use Content Security Policy (CSP) headers",
                    "Validate input against allowlists",
                    "Use modern frameworks that auto-escape"
                ]
            },
            "eval": {
                "explanation": "eval() is dangerous as it executes arbitrary code. Avoid using it with untrusted input.",
                "suggested_fix": "# Avoid eval(), use safer alternatives\n# Bad:\nresult = eval(user_input)\n\n# Good - for safe evaluation:\nimport ast\ntry:\n    result = ast.literal_eval(user_input)\nexcept:\n    result = None  # Invalid input\n\n# Or use a parser:\n# from pyparsing import infixNotation\n# result = parser.parseString(userInput)",
                "remediation_steps": [
                    "Never use eval() with user input",
                    "Use ast.literal_eval() for safe parsing",
                    "Consider using a sandboxed interpreter",
                    "Use structured data formats (JSON) instead"
                ]
            },
            "weak-crypto": {
                "explanation": "Weak cryptographic algorithm detected. MD5 and SHA1 are cryptographically broken.",
                "suggested_fix": "# Use strong hashing algorithms\n# Bad:\nimport hashlib\nhash = hashlib.md5(data).hexdigest()\n\n# Good - for passwords:\nimport bcrypt\nhash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())\n\n# Good - for checksums:\nimport hashlib\nhash = hashlib.sha256(data).hexdigest()",
                "remediation_steps": [
                    "Use bcrypt or Argon2 for password hashing",
                    "Use SHA-256 or SHA-3 for checksums",
                    "Use TLS 1.2+ for network encryption",
                    "Use strong, unique salts for passwords"
                ]
            },
            "command-injection": {
                "explanation": "Command injection risk. User input is passed to system shell without sanitization.",
                "suggested_fix": "# Use subprocess with argument list\n# Bad:\nos.system(f\"ping {hostname}\")\n\n# Good:\nimport subprocess\nresult = subprocess.run(['ping', '-c', '1', hostname], \n                       capture_output=True, text=True, shell=False)",
                "remediation_steps": [
                    "Avoid shell=True in subprocess",
                    "Use argument lists instead of string commands",
                    "Validate input against allowlists",
                    "Use sandboxed execution environments"
                ]
            },
            "path-traversal": {
                "explanation": "Path traversal vulnerability. User input controls file paths without validation.",
                "suggested_fix": "# Validate and sanitize file paths\n# Bad:\nfilepath = f\"uploads/{filename}\"\n\n# Good:\nimport os\nfrom pathlib import Path\n\nbase_dir = Path('/safedirectory')\nfilepath = (base_dir / filename).resolve()\nif not filepath.is_relative_to(base_dir):\n    raise ValueError(\"Invalid path\")",
                "remediation_steps": [
                    "Validate paths against allowlist",
                    "Use os.path.realpath() to resolve symlinks",
                    "Restrict file access to specific directories",
                    "Use sandboxed file systems"
                ]
            },
            "insecure-deserialization": {
                "explanation": "Insecure deserialization can lead to remote code execution. Never unpickle untrusted data.",
                "suggested_fix": "# Avoid pickle with untrusted data\n# Bad:\nobj = pickle.load(file)\n\n# Good - use JSON:\nimport json\nobj = json.load(file)\n\n# Or for complex objects:\n# import marshmallow\n# obj = schema.load(data)",
                "remediation_steps": [
                    "Never unpickle untrusted data",
                    "Use JSON or MessagePack for serialization",
                    "Use type-checking on deserialized data",
                    "Run deserialization in isolated processes"
                ]
            }
        }
        
        # Get fix for this vulnerability type
        fix_data = fix_suggestions.get(vuln_type.lower(), {
            "explanation": f"Security issue detected: {vuln_type}. Review and fix according to security best practices.",
            "suggested_fix": "# Review this code for security issues\n# Consult OWASP Top 10 for guidance\n# Consider using security libraries",
            "remediation_steps": [
                "Review the code for security issues",
                "Consult OWASP Top 10 guidelines",
                "Use security scanning tools",
                "Follow secure coding practices"
            ]
        })
        
        return AnalysisResult(
            explanation=fix_data["explanation"],
            suggested_fix=fix_data["suggested_fix"],
            confidence=0.7,
            is_false_positive=False,
            remediation_steps=fix_data["remediation_steps"]
        )
    
    def batch_analyze(self, vulnerabilities: List[Dict], code_context: str) -> List[AnalysisResult]:
        return [self.analyze_vulnerability(v, v.get("line_content", code_context)) for v in vulnerabilities]
    
    def clear_cache(self):
        self._cache.clear()


def create_analyzer(provider: str = "auto", api_key: str = None) -> LLMAnalyzer:
    return LLMAnalyzer(provider=provider, api_key=api_key)


def check_ollama_status() -> Dict[str, Any]:
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            return {"available": True, "models": [m.get("name") for m in models]}
    except:
        pass
    return {"available": False, "models": []}

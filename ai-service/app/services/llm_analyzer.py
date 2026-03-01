"""
LLM Analyzer - FREE options: Ollama (local), fallback patterns
"""

import os
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
    FREE vulnerability analyzer - supports:
    - Ollama (local/FREE) - RECOMMENDED
    - Claude API (paid)
    - OpenAI (paid)
    - Fallback patterns (free)
    """
    
    def __init__(
        self,
        provider: str = "auto",
        api_key: Optional[str] = None,
        model: str = "llama2"
    ):
        self.provider = provider
        self.api_key = api_key or os.getenv("CLAUDE_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.ollama_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.model = model
        self._cache: Dict[str, AnalysisResult] = {}
        
    def _detect_provider(self) -> str:
        """Auto-detect best available provider"""
        if os.getenv("OLLAMA_HOST"):
            return "ollama"
        if self.api_key:
            if os.getenv("CLAUDE_API_KEY"):
                return "claude"
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
        cache_key = self._get_cache_key(code_snippet, vulnerability.get("type", ""))
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        provider = self.provider if self.provider != "auto" else self._detect_provider()
        
        try:
            if provider == "ollama":
                return self._analyze_with_ollama(vulnerability, code_snippet, language)
            if provider == "claude" and self.api_key:
                return self._analyze_with_claude(vulnerability, code_snippet, language)
            if provider == "openai" and self.api_key:
                return self._analyze_with_openai(vulnerability, code_snippet, language)
        except Exception as e:
            print(f"Provider {provider} failed: {e}")
        
        return self._fallback_analysis(vulnerability, code_snippet)
    
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
        
        explanations = {
            "sql-injection": "SQL Injection: User input directly in SQL. Use parameterized queries: cursor.execute('SELECT * FROM users WHERE id = ?', [user_id])",
            "hardcoded-password": "Hardcoded credentials detected. Use: os.environ.get('PASSWORD') or secrets manager.",
            "xss": "XSS vulnerability. Use: textContent instead of innerHTML, or sanitize with DOMPurify.",
            "eval": "eval() is dangerous. Use ast.literal_eval() or sandboxed execution.",
            "weak-crypto": "Weak crypto. Use: hashlib.sha256() or bcrypt.hashpw()",
            "command-injection": "Command injection risk. Use subprocess.run(['ping', hostname]) with shell=False.",
        }
        
        explanation = explanations.get(vuln_type.lower(), 
            f"Security issue: {vuln_type}. Review and fix according to security best practices.")
        
        return AnalysisResult(explanation=explanation, confidence=0.5, is_false_positive=False)
    
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

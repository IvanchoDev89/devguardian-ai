"""
LLM Analyzer - Uses Claude/GPT for vulnerability analysis and fix generation
"""

import os
import json
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
    LLM-powered vulnerability analyzer
    
    Supports:
    - Claude API (Anthropic)
    - OpenAI GPT-4
    - Local fallback to pattern matching
    """
    
    def __init__(
        self,
        provider: str = "claude",
        api_key: Optional[str] = None,
        model: str = "claude-3-sonnet-20240229"
    ):
        self.provider = provider
        self.api_key = api_key or os.getenv("CLAUDE_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.model = model
        self._cache: Dict[str, AnalysisResult] = {}
        
    def _get_cache_key(self, code: str, vuln_type: str) -> str:
        """Generate deterministic cache key"""
        key_string = f"{code[:500]}:{vuln_type}"
        return hashlib.sha256(key_string.encode()).hexdigest()[:16]
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for security analysis"""
        return """Eres DevGuardian, un experto en seguridad de aplicaciones. 

Tu trabajo es analizar código en busca de vulnerabilidades, explicar它们的危险性, y sugerir correcciones seguras.

Guidelines:
1. Solo responde en español o inglés
2. Sé conciso y práctico
3. Incluye ejemplos de código seguro
4. Si no estás seguro, dilo honestamente
5. Considera el contexto completo del código

Para cada vulnerabilidad:
- Explica el problema en términos simples
- Proporciona código vulnerable vs código seguro
- Sugiere pasos de remediación específicos"""

    def analyze_vulnerability(
        self,
        vulnerability: Dict[str, Any],
        code_snippet: str,
        language: str = "python"
    ) -> AnalysisResult:
        """
        Analyze a single vulnerability with LLM
        
        Args:
            vulnerability: Vulnerability details from scanner
            code_snippet: The actual code containing vulnerability
            language: Programming language
            
        Returns:
            AnalysisResult with explanation and fix suggestion
        """
        # Check cache first
        cache_key = self._get_cache_key(code_snippet, vulnerability.get("type", ""))
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        if not self.api_key:
            return self._fallback_analysis(vulnerability, code_snippet)
        
        try:
            if self.provider == "claude":
                return self._analyze_with_claude(vulnerability, code_snippet, language)
            else:
                return self._analyze_with_openai(vulnerability, code_snippet, language)
        except Exception as e:
            print(f"LLM analysis failed: {e}")
            return self._fallback_analysis(vulnerability, code_snippet)
    
    def _analyze_with_claude(
        self,
        vulnerability: Dict[str, Any],
        code_snippet: str,
        language: str
    ) -> AnalysisResult:
        """Analyze using Claude API"""
        import anthropic
        
        client = anthropic.Anthropic(api_key=self.api_key)
        
        vuln_type = vulnerability.get("type", "Unknown")
        severity = vulnerability.get("severity", "unknown")
        message = vulnerability.get("message", "")
        
        prompt = f"""Analiza esta vulnerabilidad de seguridad:

Tipo: {vuln_type}
Severidad: {severity}
Mensaje: {message}

Código vulnerable:
```{language}
{code_snippet}
```

Proporciona:
1. Explicación clara del problema
2. Código seguro sugerido
3. Pasos para remediar
4. CWE relacionado si aplica"""

        message = client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=self._get_system_prompt(),
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text
        
        # Parse response
        result = AnalysisResult(
            explanation=response_text,
            confidence=0.85
        )
        
        # Try to extract fix suggestion
        if "```" in response_text:
            parts = response_text.split("```")
            for i, part in enumerate(parts):
                if language in part or "seguro" in part.lower():
                    result.suggested_fix = part.strip()
                    break
        
        cache_key = self._get_cache_key(code_snippet, vulnerability.get("type", ""))
        self._cache[cache_key] = result
        return result
    
    def _analyze_with_openai(
        self,
        vulnerability: Dict[str, Any],
        code_snippet: str,
        language: str
    ) -> AnalysisResult:
        """Analyze using OpenAI API"""
        from openai import OpenAI
        
        client = OpenAI(api_key=self.api_key)
        
        vuln_type = vulnerability.get("type", "Unknown")
        severity = vulnerability.get("severity", "unknown")
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": self._get_system_prompt()},
                {"role": "user", "content": f"""
Analiza esta vulnerabilidad:

Tipo: {vuln_type}
Severity: {severity}
Código:
```{language}
{code_snippet}
```

Responde con:
1. Explicación del problema
2. Código seguro sugerido
3. Pasos de remediación
"""}
            ],
            max_tokens=1024
        )
        
        response_text = response.choices[0].message.content
        
        result = AnalysisResult(
            explanation=response_text,
            confidence=0.85
        )
        
        if "```" in response_text:
            parts = response_text.split("```")
            for part in parts:
                if language in part:
                    result.suggested_fix = part.strip()
                    break
        
        cache_key = self._get_cache_key(code_snippet, vulnerability.get("type", ""))
        self._cache[cache_key] = result
        return result
    
    def _fallback_analysis(
        self,
        vulnerability: Dict[str, Any],
        code_snippet: str
    ) -> AnalysisResult:
        """Fallback to pattern-based analysis"""
        
        vuln_type = vulnerability.get("type", "Unknown")
        severity = vulnerability.get("severity", "medium")
        
        # Pattern-based explanations
        explanations = {
            "sql-injection": "SQL Injection vulnerability. User input is directly concatenated into SQL query. Use parameterized queries instead.",
            "hardcoded-password": "Hardcoded credentials detected. Store secrets in environment variables or a secure vault.",
            "xss": "Cross-Site Scripting (XSS) vulnerability. User input is directly inserted into HTML. Sanitize or escape output.",
            "eval": "Use of eval() is dangerous as it executes arbitrary code. Avoid eval() or sanitize input thoroughly.",
            "weak-crypto": "Weak cryptographic algorithm detected. Use modern algorithms like AES-256 or bcrypt.",
            "command-injection": "Command injection risk. User input should never be passed to shell commands.",
        }
        
        explanation = explanations.get(vuln_type.lower(), 
            f"Security issue detected: {vuln_type}. Review and fix according to security best practices.")
        
        return AnalysisResult(
            explanation=explanation,
            confidence=0.5,
            is_false_positive=False
        )
    
    def batch_analyze(
        self,
        vulnerabilities: List[Dict[str, Any]],
        code_context: str
    ) -> List[AnalysisResult]:
        """Analyze multiple vulnerabilities"""
        results = []
        
        for vuln in vulnerabilities:
            code_snippet = vuln.get("line_content", code_context)
            result = self.analyze_vulnerability(vuln, code_snippet)
            results.append(result)
        
        return results
    
    def clear_cache(self):
        """Clear analysis cache"""
        self._cache.clear()


def create_analyzer(
    provider: str = "claude",
    api_key: Optional[str] = None
) -> LLMAnalyzer:
    """Factory function to create LLM analyzer"""
    return LLMAnalyzer(provider=provider, api_key=api_key)

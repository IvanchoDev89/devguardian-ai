import hmac
import hashlib
import os
from typing import Optional


def get_github_webhook_secret() -> Optional[str]:
    """Get the GitHub webhook secret from environment"""
    return os.getenv("GITHUB_WEBHOOK_SECRET")


def verify_github_signature(payload: bytes, signature: str) -> bool:
    """Verify GitHub webhook signature"""
    secret = get_github_webhook_secret()
    if not secret:
        # If no secret is configured, skip verification (not recommended for production)
        return True
    
    if not signature:
        return False
    
    # Compute expected signature
    expected_signature = "sha256=" + hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected_signature, signature)


def get_github_token() -> Optional[str]:
    """Get GitHub token from environment"""
    return os.getenv("GITHUB_TOKEN")


def create_github_check_run(
    repo_owner: str,
    repo_name: str,
    name: str,
    head_sha: str,
    status: str = "in_progress",
    conclusion: Optional[str] = None
) -> dict:
    """Create a GitHub Check Run"""
    import httpx
    import os
    
    token = get_github_token()
    if not token:
        return {"error": "GitHub token not configured"}
    
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/check-runs"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {token}"
    }
    
    data = {
        "name": name,
        "head_sha": head_sha,
        "status": status,
    }
    
    if conclusion:
        data["conclusion"] = conclusion
    
    try:
        response = httpx.post(url, headers=headers, json=data, timeout=10)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

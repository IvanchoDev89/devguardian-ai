"""
Ticketing Integration - GitHub Issues, JIRA
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import httpx
from datetime import datetime


@dataclass
class Ticket:
    id: str
    title: str
    description: str
    status: str
    severity: str
    url: str
    created_at: str


class TicketingService:
    """Integrate with ticketing systems"""
    
    def __init__(self):
        self.github_token = None
        self.jira_token = None
        self.jira_url = None
        
    def configure_github(self, token: str):
        """Configure GitHub integration"""
        self.github_token = token
        
    def configure_jira(self, url: str, email: str, token: str):
        """Configure JIRA integration"""
        self.jira_url = url
        self.jira_email = email
        self.jira_token = token
        
    async def create_github_issue(
        self,
        owner: str,
        repo: str,
        title: str,
        body: str,
        labels: List[str] = None,
        severity: str = "medium"
    ) -> Ticket:
        """Create GitHub issue"""
        if not self.github_token:
            raise ValueError("GitHub token not configured")
            
        # Map severity to labels
        severity_labels = {
            "critical": ["security", "critical", "bug"],
            "high": ["security", "high", "bug"],
            "medium": ["security", "medium"],
            "low": ["security", "low"]
        }
        
        if labels is None:
            labels = severity_labels.get(severity, ["security"])
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://api.github.com/repos/{owner}/{repo}/issues",
                json={
                    "title": title,
                    "body": body,
                    "labels": labels
                },
                headers={
                    "Authorization": f"token {self.github_token}",
                    "Accept": "application/vnd.github.v3+json"
                }
            )
            
            if response.status_code != 201:
                raise Exception(f"Failed to create issue: {response.text}")
            
            data = response.json()
            
            return Ticket(
                id=str(data["number"]),
                title=data["title"],
                description=data["body"],
                status=data["state"],
                severity=severity,
                url=data["html_url"],
                created_at=data["created_at"]
            )
            
    async def create_jira_ticket(
        self,
        project_key: str,
        issue_type: str,
        summary: str,
        description: str,
        priority: str = "Medium",
        labels: List[str] = None
    ) -> Ticket:
        """Create JIRA ticket"""
        if not self.jira_token:
            raise ValueError("JIRA token not configured")
            
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.jira_url}/rest/api/3/issue",
                json={
                    "fields": {
                        "project": {"key": project_key},
                        "issuetype": {"name": issue_type},
                        "summary": summary,
                        "description": {
                            "type": "doc",
                            "version": 1,
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [{"type": "text", "text": description}]
                                }
                            ]
                        },
                        "priority": {"name": priority},
                        "labels": labels or ["security", "vulnerability"]
                    }
                },
                headers={
                    "Authorization": f"Basic {self.jira_token}",
                    "Content-Type": "application/json"
                }
            )
            
            if response.status_code != 201:
                raise Exception(f"Failed to create ticket: {response.text}")
            
            data = response.json()
            
            return Ticket(
                id=data["key"],
                title=summary,
                description=description,
                status="Open",
                severity=priority.lower(),
                url=f"{self.jira_url}/browse/{data['key']}",
                created_at=datetime.utcnow().isoformat()
            )
    
    def create_ticket_from_vulnerability(
        self,
        vuln: Dict,
        integration: str = "github",
        **config
    ) -> Dict:
        """Create ticket from vulnerability finding"""
        
        severity_emoji = {
            "critical": "🔴",
            "high": "🟠", 
            "medium": "🟡",
            "low": "🔵"
        }
        
        emoji = severity_emoji.get(vuln.get("severity", "medium"), "🟡")
        
        title = f"{emoji} Security: {vuln.get('type', 'Vulnerability')} ({vuln.get('severity', 'medium').upper()})"
        
        body = f"""## Security Vulnerability Found

### Details
- **Type**: {vuln.get('type', 'Unknown')}
- **Severity**: {vuln.get('severity', 'medium').upper()}
- **File**: {vuln.get('file', 'Unknown')}
- **Line**: {vuln.get('line', 'N/A')}

### Description
{vuln.get('description', 'No description available')}

### Recommended Fix
{vuln.get('fix', 'Review and fix manually')}

---
*Generated by DevGuardian AI Security Scanner*"""
        
        return {
            "title": title,
            "body": body,
            "labels": ["security", vuln.get("severity", "medium"), "vulnerability"]
        }


def create_ticketing_service() -> TicketingService:
    return TicketingService()

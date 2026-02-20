"""
n8n Integration Service for DevGuardian AI
Automated workflows and process automation for enhanced user value
"""

import asyncio
import aiohttp
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import hashlib
import secrets
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class WorkflowType(Enum):
    """Types of automated workflows"""
    SECURITY_SCAN = "security_scan"
    FIX_GENERATION = "fix_generation"
    CI_CD_INTEGRATION = "ci_cd_integration"
    REPORTING = "reporting"
    NOTIFICATION = "notification"
    COMPLIANCE_CHECK = "compliance_check"

@dataclass
class N8NWorkflow:
    """n8n workflow configuration"""
    id: str
    name: str
    description: str
    workflow_type: WorkflowType
    trigger_type: str  # webhook, schedule, manual
    config: Dict[str, Any]
    is_active: bool = True
    created_at: datetime = None
    updated_at: datetime = None

class N8NIntegrationService:
    """Service for integrating with n8n automation platform"""
    
    def __init__(self, n8n_url: str = "http://localhost:5678", 
                 api_key: str = None):
        self.n8n_url = n8n_url
        self.api_key = api_key or self._generate_api_key()
        self.headers = {
            "Content-Type": "application/json",
            "X-N8N-API-KEY": self.api_key
        }
        self.workflows = {}
        self.webhook_endpoints = {}
    
    def _generate_api_key(self) -> str:
        """Generate secure API key for n8n"""
        return secrets.token_urlsafe(32)
    
    async def initialize_n8n_connection(self) -> bool:
        """Initialize connection to n8n instance"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.n8n_url}/rest/active-workflows",
                    headers=self.headers
                ) as response:
                    if response.status == 200:
                        workflows = await response.json()
                        logger.info(f"Connected to n8n. Found {len(workflows)} active workflows")
                        return True
                    else:
                        logger.error(f"Failed to connect to n8n: {response.status}")
                        return False
        except Exception as e:
            logger.error(f"Error connecting to n8n: {e}")
            return False
    
    async def create_security_scan_workflow(self, repository_config: Dict) -> str:
        """Create automated security scanning workflow"""
        
        workflow_config = {
            "name": f"Security Scan - {repository_config.get('name', 'Repository')}",
            "nodes": [
                {
                    "parameters": {},
                    "name": "Start",
                    "type": "n8n-nodes-base.start",
                    "typeVersion": 1,
                    "position": [240, 300]
                },
                {
                    "parameters": {
                        "url": repository_config.get('webhook_url'),
                        "options": {}
                    },
                    "name": "Webhook",
                    "type": "n8n-nodes-base.webhook",
                    "typeVersion": 1,
                    "position": [460, 300]
                },
                {
                    "parameters": {
                        "method": "POST",
                        "url": "http://localhost:8000/api/pytorch-scanner/scan",
                        "authentication": "genericCredentialType",
                        "genericAuthType": "httpHeaderAuth"
                    },
                    "name": "Security Scan",
                    "type": "n8n-nodes-base.httpRequest",
                    "typeVersion": 3,
                    "position": [680, 300]
                },
                {
                    "parameters": {
                        "conditions": {
                            "options": {
                                "caseSensitive": True,
                                "leftValue": "={{ $json.vulnerabilities.length }}",
                                "typeValidation": "strict"
                            },
                            "conditions": [
                                {
                                    "id": "1",
                                    "leftValue": "={{ $json.vulnerabilities.length }}",
                                    "rightValue": 0,
                                    "operator": {
                                        "type": "number",
                                        "operation": "gt"
                                    }
                                }
                            ],
                            "combinator": "and"
                        },
                        "name": "Vulnerabilities Found?",
                    "type": "n8n-nodes-base.if",
                    "typeVersion": 1,
                    "position": [900, 300]
                },
                {
                    "parameters": {
                        "method": "POST",
                        "url": "http://localhost:8000/api/ai-fixes/generate",
                        "body": {
                            "vulnerabilities": "={{ $json.vulnerabilities }}",
                            "auto_approve": False
                        }
                    },
                    "name": "Generate Fixes",
                    "type": "n8n-nodes-base.httpRequest",
                    "typeVersion": 3,
                    "position": [1120, 200]
                },
                {
                    "parameters": {
                        "method": "POST",
                        "url": repository_config.get('slack_webhook'),
                        "body": {
                            "text": "🚨 Security vulnerabilities detected in {{ $json.repository_name }}",
                            "attachments": [
                                {
                                    "color": "danger",
                                    "fields": [
                                        {
                                            "title": "Vulnerabilities Found",
                                            "value": "={{ $json.vulnerabilities.length }}",
                                            "short": True
                                        },
                                        {
                                            "title": "Critical Issues",
                                            "value": "={{ $json.critical_count }}",
                                            "short": True
                                        }
                                    ]
                                }
                            ]
                        }
                    },
                    "name": "Send Alert",
                    "type": "n8n-nodes-base.httpRequest",
                    "typeVersion": 3,
                    "position": [1120, 400]
                }
            ],
            "connections": {
                "Start": {
                    "main": [[{"node": "Webhook", "type": "main", "index": 0}]]
                },
                "Webhook": {
                    "main": [[{"node": "Security Scan", "type": "main", "index": 0}]]
                },
                "Security Scan": {
                    "main": [[{"node": "Vulnerabilities Found?", "type": "main", "index": 0}]]
                },
                "Vulnerabilities Found?": {
                    "main": [
                        [{"node": "Generate Fixes", "type": "main", "index": 0}],
                        [{"node": "Send Alert", "type": "main", "index": 0}]
                    ]
                }
            }
        }
        
        # Create workflow in n8n
        workflow_id = await self._create_workflow_in_n8n(workflow_config)
        
        # Store workflow configuration
        workflow = N8NWorkflow(
            id=workflow_id,
            name=workflow_config["name"],
            description="Automated security scanning with fix generation",
            workflow_type=WorkflowType.SECURITY_SCAN,
            trigger_type="webhook",
            config=workflow_config
        )
        
        self.workflows[workflow_id] = workflow
        
        return workflow_id
    
    async def create_ci_cd_integration_workflow(self, ci_config: Dict) -> str:
        """Create CI/CD integration workflow"""
        
        workflow_config = {
            "name": f"CI/CD Security Integration - {ci_config.get('platform', 'GitHub')}",
            "nodes": [
                {
                    "parameters": {},
                    "name": "Start",
                    "type": "n8n-nodes-base.start",
                    "typeVersion": 1,
                    "position": [240, 300]
                },
                {
                    "parameters": {
                        "url": ci_config.get('webhook_url'),
                        "options": {}
                    },
                    "name": "CI/CD Webhook",
                    "type": "n8n-nodes-base.webhook",
                    "typeVersion": 1,
                    "position": [460, 300]
                },
                {
                    "parameters": {
                        "conditions": {
                            "options": {
                                "caseSensitive": True,
                                "leftValue": "={{ $json.event }}",
                                "typeValidation": "strict"
                            },
                            "conditions": [
                                {
                                    "id": "1",
                                    "leftValue": "={{ $json.event }}",
                                    "rightValue": "push",
                                    "operator": {
                                        "type": "string",
                                        "operation": "equals"
                                    }
                                }
                            ],
                            "combinator": "and"
                        },
                        "name": "Is Push Event?",
                    "type": "n8n-nodes-base.if",
                    "typeVersion": 1,
                    "position": [680, 300]
                },
                {
                    "parameters": {
                        "method": "POST",
                        "url": "http://localhost:8000/api/pytorch-scanner/scan-directory",
                        "body": {
                            "directory_path": "={{ $json.repository.clone_url }}",
                            "recursive": True
                        }
                    },
                    "name": "Scan Repository",
                    "type": "n8n-nodes-base.httpRequest",
                    "typeVersion": 3,
                    "position": [900, 200]
                },
                {
                    "parameters": {
                        "method": "POST",
                        "url": ci_config.get('status_check_url'),
                        "body": {
                            "state": "pending",
                            "description": "Security scan in progress...",
                            "context": "devguardian/security"
                        }
                    },
                    "name": "Update Status - Pending",
                    "type": "n8n-nodes-base.httpRequest",
                    "typeVersion": 3,
                    "position": [1120, 200]
                },
                {
                    "parameters": {
                        "conditions": {
                            "options": {
                                "caseSensitive": True,
                                "leftValue": "={{ $json.vulnerabilities.length }}",
                                "typeValidation": "strict"
                            },
                            "conditions": [
                                {
                                    "id": "1",
                                    "leftValue": "={{ $json.vulnerabilities.length }}",
                                    "rightValue": 0,
                                    "operator": {
                                        "type": "number",
                                        "operation": "gt"
                                    }
                                }
                            ],
                            "combinator": "and"
                        },
                        "name": "Vulnerabilities Found?",
                    "type": "n8n-nodes-base.if",
                    "typeVersion": 1,
                    "position": [1340, 200]
                },
                {
                    "parameters": {
                        "method": "POST",
                        "url": ci_config.get('status_check_url'),
                        "body": {
                            "state": "failure",
                            "description": "Security vulnerabilities detected! {{ $json.vulnerabilities.length }} issues found.",
                            "context": "devguardian/security"
                        }
                    },
                    "name": "Update Status - Failed",
                    "type": "n8n-nodes-base.httpRequest",
                    "typeVersion": 3,
                    "position": [1560, 100]
                },
                {
                    "parameters": {
                        "method": "POST",
                        "url": ci_config.get('status_check_url'),
                        "body": {
                            "state": "success",
                            "description": "Security scan passed - no vulnerabilities detected",
                            "context": "devguardian/security"
                        }
                    },
                    "name": "Update Status - Success",
                    "type": "n8n-nodes-base.httpRequest",
                    "typeVersion": 3,
                    "position": [1560, 300]
                }
            ],
            "connections": {
                "Start": {
                    "main": [[{"node": "CI/CD Webhook", "type": "main", "index": 0}]]
                },
                "CI/CD Webhook": {
                    "main": [[{"node": "Is Push Event?", "type": "main", "index": 0}]]
                },
                "Is Push Event?": {
                    "main": [[{"node": "Scan Repository", "type": "main", "index": 0}]]
                },
                "Scan Repository": {
                    "main": [[{"node": "Update Status - Pending", "type": "main", "index": 0}]]
                },
                "Update Status - Pending": {
                    "main": [[{"node": "Vulnerabilities Found?", "type": "main", "index": 0}]]
                },
                "Vulnerabilities Found?": {
                    "main": [
                        [{"node": "Update Status - Failed", "type": "main", "index": 0}],
                        [{"node": "Update Status - Success", "type": "main", "index": 0}]
                    ]
                }
            }
        }
        
        workflow_id = await self._create_workflow_in_n8n(workflow_config)
        
        workflow = N8NWorkflow(
            id=workflow_id,
            name=workflow_config["name"],
            description="CI/CD integration with automated security checks",
            workflow_type=WorkflowType.CI_CD_INTEGRATION,
            trigger_type="webhook",
            config=workflow_config
        )
        
        self.workflows[workflow_id] = workflow
        
        return workflow_id
    
    async def create_reporting_workflow(self, report_config: Dict) -> str:
        """Create automated reporting workflow"""
        
        workflow_config = {
            "name": f"Security Reporting - {report_config.get('frequency', 'Daily')}",
            "nodes": [
                {
                    "parameters": {
                        "rule": {
                            "interval": [
                                {
                                    "field": "hours",
                                    "hoursInterval": 24
                                }
                            ]
                        }
                    },
                    "name": "Schedule Trigger",
                    "type": "n8n-nodes-base.cron",
                    "typeVersion": 1,
                    "position": [240, 300]
                },
                {
                    "parameters": {
                        "method": "GET",
                        "url": "http://localhost:8000/api/ai-fixes/stats"
                    },
                    "name": "Get Security Stats",
                    "type": "n8n-nodes-base.httpRequest",
                    "typeVersion": 3,
                    "position": [460, 300]
                },
                {
                    "parameters": {
                        "method": "GET",
                        "url": "http://localhost:8000/api/repositories/stats"
                    },
                    "name": "Get Repository Stats",
                    "type": "n8n-nodes-base.httpRequest",
                    "typeVersion": 3,
                    "position": [460, 420]
                },
                {
                    "parameters": {
                        "jsCode": `
                            const securityStats = items[0].json;
                            const repoStats = items[1].json;
                            
                            const report = {
                                date: new Date().toISOString().split('T')[0],
                                summary: {
                                    total_vulnerabilities: securityStats.total_vulnerabilities || 0,
                                    critical_issues: securityStats.critical_count || 0,
                                    high_issues: securityStats.high_count || 0,
                                    fixes_generated: securityStats.fixes_generated || 0,
                                    repositories_scanned: repoStats.total_repositories || 0
                                },
                                trends: {
                                    new_vulnerabilities: securityStats.new_vulnerabilities || 0,
                                    resolved_issues: securityStats.resolved_issues || 0
                                },
                                recommendations: []
                            };
                            
                            // Generate recommendations based on stats
                            if (securityStats.critical_count > 0) {
                                report.recommendations.push('Address critical vulnerabilities immediately');
                            }
                            if (securityStats.fixes_generated > 0) {
                                report.recommendations.push('Review and apply generated security fixes');
                            }
                            
                            return [{
                                json: report
                            }];
                        `
                    },
                    "name": "Generate Report",
                    "type": "n8n-nodes-base.code",
                    "typeVersion": 2,
                    "position": [680, 300]
                },
                {
                    "parameters": {
                        "method": "POST",
                        "url": report_config.get('email_webhook'),
                        "body": {
                            "to": report_config.get('recipients', []),
                            "subject": "DevGuardian AI Security Report - {{ $json.date }}",
                            "html": `
                                <h2>Security Report - {{ $json.date }}</h2>
                                <h3>Summary</h3>
                                <ul>
                                    <li>Total Vulnerabilities: {{ $json.summary.total_vulnerabilities }}</li>
                                    <li>Critical Issues: {{ $json.summary.critical_issues }}</li>
                                    <li>High Issues: {{ $json.summary.high_issues }}</li>
                                    <li>Fixes Generated: {{ $json.summary.fixes_generated }}</li>
                                    <li>Repositories Scanned: {{ $json.summary.repositories_scanned }}</li>
                                </ul>
                                <h3>Recommendations</h3>
                                <ul>
                                    {{ $json.recommendations.map(rec => '<li>' + rec + '</li>').join('') }}
                                </ul>
                            `
                        }
                    },
                    "name": "Send Email Report",
                    "type": "n8n-nodes-base.httpRequest",
                    "typeVersion": 3,
                    "position": [900, 300]
                }
            ],
            "connections": {
                "Schedule Trigger": {
                    "main": [
                        [{"node": "Get Security Stats", "type": "main", "index": 0}],
                        [{"node": "Get Repository Stats", "type": "main", "index": 0}]
                    ]
                },
                "Get Security Stats": {
                    "main": [[{"node": "Generate Report", "type": "main", "index": 0}]]
                },
                "Get Repository Stats": {
                    "main": [[{"node": "Generate Report", "type": "main", "index": 0}]]
                },
                "Generate Report": {
                    "main": [[{"node": "Send Email Report", "type": "main", "index": 0}]]
                }
            }
        }
        
        workflow_id = await self._create_workflow_in_n8n(workflow_config)
        
        workflow = N8NWorkflow(
            id=workflow_id,
            name=workflow_config["name"],
            description="Automated security reporting and analytics",
            workflow_type=WorkflowType.REPORTING,
            trigger_type="schedule",
            config=workflow_config
        )
        
        self.workflows[workflow_id] = workflow
        
        return workflow_id
    
    async def _create_workflow_in_n8n(self, workflow_config: Dict) -> str:
        """Create workflow in n8n instance"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.n8n_url}/rest/workflows",
                    headers=self.headers,
                    json=workflow_config
                ) as response:
                    if response.status == 201:
                        result = await response.json()
                        workflow_id = result.get("id")
                        
                        # Activate the workflow
                        await self._activate_workflow(workflow_id)
                        
                        logger.info(f"Created n8n workflow: {workflow_id}")
                        return workflow_id
                    else:
                        logger.error(f"Failed to create workflow: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Error creating n8n workflow: {e}")
            return None
    
    async def _activate_workflow(self, workflow_id: str) -> bool:
        """Activate a workflow in n8n"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.n8n_url}/rest/workflows/{workflow_id}/activate",
                    headers=self.headers
                ) as response:
                    return response.status == 200
        except Exception as e:
            logger.error(f"Error activating workflow {workflow_id}: {e}")
            return False
    
    async def trigger_workflow(self, workflow_id: str, data: Dict = None) -> bool:
        """Manually trigger a workflow"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.n8n_url}/rest/workflows/{workflow_id}/execute",
                    headers=self.headers,
                    json={"data": data or {}}
                ) as response:
                    return response.status == 200
        except Exception as e:
            logger.error(f"Error triggering workflow {workflow_id}: {e}")
            return False
    
    async def get_workflow_status(self, workflow_id: str) -> Dict:
        """Get status of a specific workflow"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.n8n_url}/rest/workflows/{workflow_id}",
                    headers=self.headers
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        return {}
        except Exception as e:
            logger.error(f"Error getting workflow status {workflow_id}: {e}")
            return {}
    
    async def list_active_workflows(self) -> List[Dict]:
        """List all active workflows"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.n8n_url}/rest/active-workflows",
                    headers=self.headers
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        return []
        except Exception as e:
            logger.error(f"Error listing workflows: {e}")
            return []
    
    def generate_webhook_url(self, workflow_id: str) -> str:
        """Generate webhook URL for workflow"""
        webhook_path = hashlib.md5(f"{workflow_id}_{secrets.token_hex(8)}".encode()).hexdigest()
        self.webhook_endpoints[webhook_path] = workflow_id
        return f"{self.n8n_url}/webhook/{webhook_path}"
    
    async def create_compliance_workflow(self, compliance_config: Dict) -> str:
        """Create compliance checking workflow"""
        
        workflow_config = {
            "name": f"Compliance Check - {compliance_config.get('standard', 'OWASP')}",
            "nodes": [
                {
                    "parameters": {
                        "rule": {
                            "interval": [
                                {
                                    "field": "hours",
                                    "hoursInterval": 168  # Weekly
                                }
                            ]
                        }
                    },
                    "name": "Weekly Schedule",
                    "type": "n8n-nodes-base.cron",
                    "typeVersion": 1,
                    "position": [240, 300]
                },
                {
                    "parameters": {
                        "method": "GET",
                        "url": "http://localhost:8000/api/repositories"
                    },
                    "name": "Get All Repositories",
                    "type": "n8n-nodes-base.httpRequest",
                    "typeVersion": 3,
                    "position": [460, 300]
                },
                {
                    "parameters": {
                        "method": "POST",
                        "url": "http://localhost:8000/api/compliance/check",
                        "body": {
                            "repository_id": "={{ $json.id }}",
                            "standard": compliance_config.get('standard', 'OWASP'),
                            "framework": compliance_config.get('framework', 'NIST')
                        }
                    },
                    "name": "Check Compliance",
                    "type": "n8n-nodes-base.httpRequest",
                    "typeVersion": 3,
                    "position": [680, 300]
                },
                {
                    "parameters": {
                        "conditions": {
                            "options": {
                                "caseSensitive": True,
                                "leftValue": "={{ $json.compliance_score }}",
                                "typeValidation": "strict"
                            },
                            "conditions": [
                                {
                                    "id": "1",
                                    "leftValue": "={{ $json.compliance_score }}",
                                    "rightValue": 80,
                                    "operator": {
                                        "type": "number",
                                        "operation": "lt"
                                    }
                                }
                            ],
                            "combinator": "and"
                        },
                        "name": "Compliance Issues?",
                    "type": "n8n-nodes-base.if",
                    "typeVersion": 1,
                    "position": [900, 300]
                },
                {
                    "parameters": {
                        "method": "POST",
                        "url": compliance_config.get('notification_webhook'),
                        "body": {
                            "message": "🚨 Compliance issues detected in {{ $json.repository_name }}",
                            "compliance_score": "={{ $json.compliance_score }}",
                            "issues": "={{ $json.issues }}",
                            "required_actions": "={{ $json.required_actions }}"
                        }
                    },
                    "name": "Notify Compliance Team",
                    "type": "n8n-nodes-base.httpRequest",
                    "typeVersion": 3,
                    "position": [1120, 300]
                }
            ],
            "connections": {
                "Weekly Schedule": {
                    "main": [[{"node": "Get All Repositories", "type": "main", "index": 0}]]
                },
                "Get All Repositories": {
                    "main": [[{"node": "Check Compliance", "type": "main", "index": 0}]]
                },
                "Check Compliance": {
                    "main": [[{"node": "Compliance Issues?", "type": "main", "index": 0}]]
                },
                "Compliance Issues?": {
                    "main": [[{"node": "Notify Compliance Team", "type": "main", "index": 0}]]
                }
            }
        }
        
        workflow_id = await self._create_workflow_in_n8n(workflow_config)
        
        workflow = N8NWorkflow(
            id=workflow_id,
            name=workflow_config["name"],
            description="Automated compliance checking and reporting",
            workflow_type=WorkflowType.COMPLIANCE_CHECK,
            trigger_type="schedule",
            config=workflow_config
        )
        
        self.workflows[workflow_id] = workflow
        
        return workflow_id

class WorkflowManager:
    """Manager for n8n workflows and automation"""
    
    def __init__(self):
        self.n8n_service = N8NIntegrationService()
        self.templates = self._load_workflow_templates()
    
    def _load_workflow_templates(self) -> Dict:
        """Load predefined workflow templates"""
        return {
            "github_security": {
                "name": "GitHub Security Integration",
                "description": "Automated security scanning for GitHub repositories",
                "config": {
                    "webhook_url": "https://api.github.com/webhooks",
                    "platform": "GitHub"
                }
            },
            "slack_notifications": {
                "name": "Slack Security Notifications",
                "description": "Send security alerts to Slack channels",
                "config": {
                    "slack_webhook": "https://hooks.slack.com/services/...",
                    "channels": ["#security", "#devops"]
                }
            },
            "daily_reports": {
                "name": "Daily Security Reports",
                "description": "Automated daily security reporting",
                "config": {
                    "frequency": "daily",
                    "recipients": ["security@company.com"]
                }
            }
        }
    
    async def setup_default_workflows(self, user_config: Dict) -> Dict[str, str]:
        """Setup default workflows for new user"""
        workflow_ids = {}
        
        # Security scan workflow
        security_workflow_id = await self.n8n_service.create_security_scan_workflow(
            user_config.get('repository', {})
        )
        if security_workflow_id:
            workflow_ids['security_scan'] = security_workflow_id
        
        # CI/CD integration
        if user_config.get('ci_cd'):
            cicd_workflow_id = await self.n8n_service.create_ci_cd_integration_workflow(
                user_config['ci_cd']
            )
            if cicd_workflow_id:
                workflow_ids['ci_cd'] = cicd_workflow_id
        
        # Reporting workflow
        reporting_workflow_id = await self.n8n_service.create_reporting_workflow(
            user_config.get('reporting', {})
        )
        if reporting_workflow_id:
            workflow_ids['reporting'] = reporting_workflow_id
        
        return workflow_ids
    
    async def get_workflow_analytics(self) -> Dict:
        """Get analytics for all workflows"""
        workflows = await self.n8n_service.list_active_workflows()
        
        analytics = {
            "total_workflows": len(workflows),
            "active_workflows": len([w for w in workflows if w.get('active')]),
            "workflow_types": {},
            "execution_stats": {}
        }
        
        for workflow in workflows:
            workflow_type = workflow.get('type', 'unknown')
            analytics["workflow_types"][workflow_type] = analytics["workflow_types"].get(workflow_type, 0) + 1
        
        return analytics

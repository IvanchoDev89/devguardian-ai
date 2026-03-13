"""
Cloud Security Scanner
Scan AWS, Azure, GCP configurations for security issues
"""

import json
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class CloudFinding:
    resource: str
    issue: str
    severity: str
    description: str
    remediation: str
    provider: str


class CloudSecurityScanner:
    """Scan cloud configurations for security issues"""
    
    # AWS Patterns
    AWS_RULES = [
        {
            "resource": "S3 Bucket",
            "pattern": r"aws_s3_bucket[^}]*?acl\s*=\s*\"public\"",
            "severity": "critical",
            "issue": "S3 bucket is publicly accessible",
            "remediation": "Set ACL to private or use bucket policy"
        },
        {
            "resource": "IAM User",
            "pattern": r"aws_iam_user[^}]*?policy\s*=\s*.*\*",
            "severity": "high",
            "issue": "IAM user has full admin access",
            "remediation": "Follow principle of least privilege"
        },
        {
            "resource": "Security Group",
            "pattern": r"cidr_blocks\s*=\s*\[\s*\"0\.0\.0\.0/0\"",
            "severity": "high",
            "issue": "Security group allows open access",
            "remediation": "Restrict to specific IP ranges"
        },
        {
            "resource": "RDS",
            "pattern": r"publicly_accessible\s*=\s*true",
            "severity": "critical",
            "issue": "Database is publicly accessible",
            "remediation": "Disable public access, use VPC"
        },
    ]
    
    # Azure Patterns
    AZURE_RULES = [
        {
            "resource": "Storage Account",
            "pattern": r"allow\s*=\s*true.*https_traffic_only\s*=\s*false",
            "severity": "high",
            "issue": "Storage account allows HTTP traffic",
            "remediation": "Enable HTTPS only and disable HTTP"
        },
        {
            "resource": "SQL Database",
            "pattern": r"public_network_access_enabled\s*=\s*true",
            "severity": "high",
            "issue": "SQL database allows public access",
            "remediation": "Disable public network access"
        },
        {
            "resource": "Network Security Group",
            "pattern": r"source_address_prefix\s*=\s*\"\*\"",
            "severity": "medium",
            "issue": "NSG allows traffic from anywhere",
            "remediation": "Restrict to specific IP ranges"
        },
    ]
    
    # GCP Patterns
    GCP_RULES = [
        {
            "resource": "Storage Bucket",
            "pattern": r"storage_bucket[^}]*?uniform_bucket_level_access\s*=\s*false",
            "severity": "high",
            "issue": "Bucket uses fine-grained access",
            "remediation": "Enable uniform bucket-level access"
        },
        {
            "resource": "Firewall",
            "pattern": r"source_ranges\s*=\s*\[\s*\"0\.0\.0\.0/0\"",
            "severity": "high",
            "issue": "Firewall allows open access",
            "remediation": "Restrict to specific IP ranges"
        },
        {
            "resource": "SQL Instance",
            "pattern": r"public_ip\s*=\s*true",
            "severity": "critical",
            "issue": "SQL instance has public IP",
            "remediation": "Use private IP only"
        },
    ]
    
    # Kubernetes Patterns
    K8S_RULES = [
        {
            "resource": "Pod Security",
            "pattern": r"runAsUser:\s*0",
            "severity": "high",
            "issue": "Pod runs as root user",
            "remediation": "Set runAsNonRoot: true and runAsUser: non-zero"
        },
        {
            "resource": "Container Security",
            "pattern": r"privileged:\s*true",
            "severity": "critical",
            "issue": "Container runs in privileged mode",
            "remediation": "Set privileged: false"
        },
        {
            "resource": "Network Policy",
            "pattern": r"podSelector:\s*\{\}",
            "severity": "medium",
            "issue": "Network policy allows all traffic",
            "remediation": "Define specific ingress/egress rules"
        },
    ]
    
    def __init__(self):
        self.findings: List[CloudFinding] = []
        
    def scan_terraform(self, content: str) -> List[Dict]:
        """Scan Terraform configuration"""
        findings = []
        
        # Check AWS rules
        for rule in self.AWS_RULES:
            if re.search(rule["pattern"], content, re.IGNORECASE):
                findings.append({
                    "provider": "aws",
                    "resource": rule["resource"],
                    "severity": rule["severity"],
                    "issue": rule["issue"],
                    "remediation": rule["remediation"]
                })
        
        # Check Azure rules
        for rule in self.AZURE_RULES:
            if re.search(rule["pattern"], content, re.IGNORECASE):
                findings.append({
                    "provider": "azure",
                    "resource": rule["resource"],
                    "severity": rule["severity"],
                    "issue": rule["issue"],
                    "remediation": rule["remediation"]
                })
        
        # Check GCP rules
        for rule in self.GCP_RULES:
            if re.search(rule["pattern"], content, re.IGNORECASE):
                findings.append({
                    "provider": "gcp",
                    "resource": rule["resource"],
                    "severity": rule["severity"],
                    "issue": rule["issue"],
                    "remediation": rule["remediation"]
                })
        
        return findings
    
    def scan_kubernetes(self, content: str) -> List[Dict]:
        """Scan Kubernetes YAML"""
        findings = []
        
        for rule in self.K8S_RULES:
            if re.search(rule["pattern"], content, re.IGNORECASE):
                findings.append({
                    "provider": "kubernetes",
                    "resource": rule["resource"],
                    "severity": rule["severity"],
                    "issue": rule["issue"],
                    "remediation": rule["remediation"]
                })
        
        return findings
    
    def scan_docker_compose(self, content: str) -> List[Dict]:
        """Scan Docker Compose files"""
        findings = []
        
        # Check for security issues in docker-compose
        if re.search(r"privileged:\s*true", content, re.IGNORECASE):
            findings.append({
                "provider": "docker",
                "resource": "Container",
                "severity": "critical",
                "issue": "Container runs in privileged mode",
                "remediation": "Set privileged: false"
            })
        
        if re.search(r"network_mode:\s*\"host\"", content, re.IGNORECASE):
            findings.append({
                "provider": "docker",
                "resource": "Network",
                "severity": "high",
                "issue": "Container uses host networking",
                "remediation": "Use bridge network instead"
            })
        
        if re.search(r"user:\s*\"root\"", content, re.IGNORECASE):
            findings.append({
                "provider": "docker",
                "resource": "Container",
                "severity": "high", 
                "issue": "Container runs as root",
                "remediation": "Specify non-root user"
            })
        
        if not re.search(r"read_only:\s*true", content, re.IGNORECASE):
            findings.append({
                "provider": "docker",
                "resource": "Container",
                "severity": "medium",
                "issue": "Filesystem is not read-only",
                "remediation": "Set read_only: true"
            })
        
        return findings
    
    def scan_github_actions(self, content: str) -> List[Dict]:
        """Scan GitHub Actions workflows"""
        findings = []
        
        if re.search(r"GITHUB_TOKEN.*permissions:\s*\{\}", content):
            findings.append({
                "provider": "github",
                "resource": "Workflow",
                "severity": "medium",
                "issue": "GitHub Token has no permissions set",
                "remediation": "Set specific permissions for GITHUB_TOKEN"
            })
        
        if re.search(r"pull_request.*from-contributors", content):
            findings.append({
                "provider": "github", 
                "resource": "Workflow",
                "severity": "medium",
                "issue": "Workflow runs on all contributor PRs",
                "remediation": "Use stricter trigger conditions"
            })
        
        return findings
    
    def scan_cloudformation(self, content: str) -> List[Dict]:
        """Scan CloudFormation templates"""
        findings = []
        
        # Check for publicly accessible S3
        if re.search(r"Type:\s*AWS::S3::Bucket.*PublicAccessBlockConfiguration", content):
            if not re.search(r"BlockPublicAcls\s*:\s*true", content):
                findings.append({
                    "provider": "aws",
                    "resource": "S3 Bucket",
                    "severity": "high",
                    "issue": "S3 doesn't block public access",
                    "remediation": "Enable BlockPublicAcls"
                })
        
        return findings


def create_cloud_scanner() -> CloudSecurityScanner:
    return CloudSecurityScanner()

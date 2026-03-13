"""
Compliance Reporting - SOC2, ISO 27001, HIPAA, PCI-DSS
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Control:
    id: str
    name: str
    description: str
    status: str  # passed, failed, not_applicable, needs_review
    evidence: List[str] = None
    findings: List[str] = None


class ComplianceReporter:
    """Generate compliance reports for various frameworks"""
    
    FRAMEWORKS = {
        "soc2": {
            "name": "SOC 2 Type II",
            "version": "2017",
            "controls": [
                {"id": "CC1.1", "name": "Control Environment", "description": "Entity demonstrates commitment to integrity and ethical values"},
                {"id": "CC2.1", "name": "Information & Communication", "description": "Entity obtains relevant quality information"},
                {"id": "CC3.1", "name": "Risk Assessment", "description": "Entity specifies objectives with sufficient clarity"},
                {"id": "CC4.1", "name": "Monitoring Activities", "description": "Entity selects and develops ongoing evaluations"},
                {"id": "CC5.1", "name": "Control Activities", "description": "Entity selects and develops control activities"},
                {"id": "CC6.1", "name": "Logical Access", "description": "Restricts logical access to systems"},
                {"id": "CC7.1", "name": "System Operations", "description": "Detects and responds to anomalies"},
                {"id": "CC8.1", "name": "Change Management", "description": "Manages changes to system components"},
            ]
        },
        "iso27001": {
            "name": "ISO/IEC 27001:2022",
            "version": "2022",
            "controls": [
                {"id": "A.5.1", "name": "Information Security Policies", "description": "Policies for information security"},
                {"id": "A.6.1", "name": "Organization of Information Security", "description": "Internal organization and responsibilities"},
                {"id": "A.7.1", "name": "Human Resource Security", "description": "Security responsibilities prior to employment"},
                {"id": "A.8.1", "name": "Asset Management", "description": "Responsibility for assets"},
                {"id": "A.8.2", "name": "Information Classification", "description": "Classification of information"},
                {"id": "A.8.5", "name": "Secure Authentication", "description": "Secure authentication technologies"},
                {"id": "A.8.12", "name": "Data Leakage Prevention", "description": "Data leakage prevention measures"},
                {"id": "A.8.20", "name": "Networks Security", "description": "Security of networks and supporting infrastructure"},
                {"id": "A.8.24", "name": "Vulnerability Management", "description": "Management of technical vulnerabilities"},
            ]
        },
        "hipaa": {
            "name": "HIPAA Security Rule",
            "version": "2020",
            "controls": [
                {"id": "164.308(a)(1)", "name": "Security Management Process", "description": "Risk analysis and management"},
                {"id": "164.308(a)(5)", "name": "Security Awareness Training", "description": "Security awareness and training program"},
                {"id": "164.308(a)(7)", "name": "Contingency Plan", "description": "Data backup and disaster recovery"},
                {"id": "164.310(a)(1)", "name": "Facility Access Controls", "description": "Limit physical access to PHI"},
                {"id": "164.310(d)(1)", "name": "Workstation Security", "description": "Physical safeguards for workstations"},
                {"id": "164.312(a)(1)", "name": "Access Control", "description": "Technical safeguards for access to PHI"},
                {"id": "164.312(b)", "name": "Audit Controls", "description": "Audit trails and monitoring"},
                {"id": "164.312(e)(1)", "name": "Transmission Security", "description": "Encryption of PHI in transit"},
            ]
        },
        "pci_dss": {
            "name": "PCI DSS v4.0",
            "version": "4.0",
            "controls": [
                {"id": "Req-1", "name": "Firewalls", "description": "Install and maintain firewall configurations"},
                {"id": "Req-2", "name": "Vendor Defaults", "description": "Change vendor defaults"},
                {"id": "Req-3", "name": "Stored Cardholder Data", "description": "Protect stored cardholder data"},
                {"id": "Req-4", "name": "Transmission Data", "description": "Encrypt transmission of cardholder data"},
                {"id": "Req-5", "name": "Malware", "description": "Maintain anti-virus software"},
                {"id": "Req-6", "name": "Secure Systems", "description": "Develop secure systems"},
                {"id": "Req-7", "name": "Restrict Access", "description": "Restrict access to cardholder data"},
                {"id": "Req-8", "name": "User IDs", "description": "Identify and authenticate access"},
            ]
        }
    }
    
    def __init__(self):
        self.scan_results = {}
        
    def assess_controls(self, framework: str, vulnerabilities: List[Dict]) -> Dict:
        """Assess security controls based on scan results"""
        if framework not in self.FRAMEWORKS:
            raise ValueError(f"Unknown framework: {framework}")
            
        framework_info = self.FRAMEWORKS[framework]
        controls = []
        
        for control in framework_info["controls"]:
            assessment = self._assess_control(control, vulnerabilities)
            controls.append(assessment)
            
        return {
            "framework": framework_info["name"],
            "version": framework_info["version"],
            "total_controls": len(controls),
            "passed": sum(1 for c in controls if c["status"] == "passed"),
            "failed": sum(1 for c in controls if c["status"] == "failed"),
            "not_applicable": sum(1 for c in controls if c["status"] == "not_applicable"),
            "needs_review": sum(1 for c in controls if c["status"] == "needs_review"),
            "controls": controls,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _assess_control(self, control: Dict, vulnerabilities: List[Dict]) -> Dict:
        """Assess a single control"""
        control_id = control["id"]
        
        # Simple mapping - in production this would be more sophisticated
        passed_checks = []
        failed_checks = []
        
        # Map vulnerabilities to controls
        for vuln in vulnerabilities:
            severity = vuln.get("severity", "low")
            vuln_type = vuln.get("type", "")
            
            if "access" in control_id.lower() or "authentication" in control["name"].lower():
                if "hardcoded" in vuln_type or "weak" in vuln_type:
                    failed_checks.append(f"Found {vuln_type} vulnerability")
                    
            if "vulnerability" in control_id.lower() or "malware" in control["name"].lower():
                if severity in ["critical", "high"]:
                    failed_checks.append(f"Critical/High vulnerability found: {vuln_type}")
                    
            if "encryption" in control["name"].lower() or "transmission" in control["name"].lower():
                if "hardcoded" in vuln_type or "weak" in vuln_type:
                    failed_checks.append(f"Encryption issue: {vuln_type}")
        
        if failed_checks:
            status = "failed"
        elif passed_checks:
            status = "passed"
        else:
            status = "needs_review"
            
        return {
            "id": control_id,
            "name": control["name"],
            "description": control["description"],
            "status": status,
            "findings": failed_checks,
            "evidence": passed_checks if passed_checks else []
        }
    
    def generate_report(self, framework: str, vulnerabilities: List[Dict], project_name: str = "Project") -> Dict:
        """Generate full compliance report"""
        assessment = self.assess_controls(framework, vulnerabilities)
        
        score = (assessment["passed"] / assessment["total_controls"]) * 100 if assessment["total_controls"] > 0 else 0
        
        return {
            "report_id": f"COMP-{datetime.utcnow().strftime('%Y%m%d')}-{project_name[:8]}",
            "project_name": project_name,
            "framework": assessment["framework"],
            "version": assessment["version"],
            "score": round(score, 2),
            "compliance_level": self._get_compliance_level(score),
            "summary": {
                "total_controls": assessment["total_controls"],
                "passed": assessment["passed"],
                "failed": assessment["failed"],
                "needs_review": assessment["needs_review"]
            },
            "controls": assessment["controls"],
            "recommendations": self._generate_recommendations(assessment),
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def _get_compliance_level(self, score: float) -> str:
        if score >= 95:
            return "FULLY_COMPLIANT"
        elif score >= 80:
            return "MOSTLY_COMPLIANT"
        elif score >= 60:
            return "PARTIALLY_COMPLIANT"
        elif score >= 40:
            return "NON_COMPLIANT"
        else:
            return "CRITICAL_NON_COMPLIANT"
    
    def _generate_recommendations(self, assessment: Dict) -> List[str]:
        """Generate recommendations based on assessment"""
        recommendations = []
        
        failed = [c for c in assessment["controls"] if c["status"] == "failed"]
        
        if failed:
            recommendations.append(f"Address {len(failed)} failed controls immediately")
            
            # Group by category
            for control in failed[:5]:  # Top 5
                recommendations.append(
                    f"Control {control['id']}: Review and remediate findings"
                )
        
        recommendations.append("Implement continuous security monitoring")
        recommendations.append("Conduct regular penetration testing")
        recommendations.append("Maintain updated incident response plan")
        
        return recommendations


def create_compliance_reporter() -> ComplianceReporter:
    return ComplianceReporter()

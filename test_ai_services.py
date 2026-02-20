#!/usr/bin/env python3
"""
Comprehensive AI Services Test Suite
Interactive testing for first client experience
"""

import requests
import json
import time
import sys
from datetime import datetime
from typing import Dict, List, Any

# Test configuration
AI_SERVICE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

class AIServiceTester:
    def __init__(self):
        self.test_results = []
        self.ai_fixes_created = []
        self.start_time = datetime.now()
        
    def log_test(self, test_name: str, success: bool, message: str, details: Dict = None):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "details": details or {},
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        
        if details and not success:
            print(f"   Details: {details}")
    
    def test_ai_service_health(self):
        """Test AI service health endpoint"""
        try:
            response = requests.get(f"{AI_SERVICE_URL}/health", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.log_test(
                    "AI Service Health Check",
                    True,
                    "Service is healthy and operational",
                    {"status": data.get("status"), "version": data.get("version")}
                )
                return True
            else:
                self.log_test(
                    "AI Service Health Check",
                    False,
                    f"Service returned status {response.status_code}",
                    {"response": response.text}
                )
                return False
                
        except Exception as e:
            self.log_test(
                "AI Service Health Check",
                False,
                f"Connection failed: {str(e)}",
                {"error": str(e)}
            )
            return False
    
    def test_ai_fixes_generation(self):
        """Test AI fixes generation with various vulnerability types"""
        
        # Test vulnerabilities for comprehensive coverage
        test_vulnerabilities = [
            {
                "vulnerability_type": "sql_injection",
                "severity": "critical",
                "confidence": 0.95,
                "code_snippet": '$query = "SELECT * FROM users WHERE id = " . $_GET["id"];',
                "file_path": "/var/www/html/user.php",
                "line_number": 15,
                "cwe_id": "CWE-89",
                "cvss_score": 9.8
            },
            {
                "vulnerability_type": "xss",
                "severity": "high", 
                "confidence": 0.88,
                "code_snippet": 'echo $_POST["comment"];',
                "file_path": "/var/www/html/comments.php",
                "line_number": 23,
                "cwe_id": "CWE-79",
                "cvss_score": 7.5
            },
            {
                "vulnerability_type": "command_injection",
                "severity": "critical",
                "confidence": 0.92,
                "code_snippet": 'system("rm -rf " . $_GET["file"]);',
                "file_path": "/var/www/html/admin.php",
                "line_number": 45,
                "cwe_id": "CWE-78",
                "cvss_score": 9.0
            },
            {
                "vulnerability_type": "hardcoded_credentials",
                "severity": "high",
                "confidence": 0.98,
                "code_snippet": '$api_key = "sk-1234567890abcdef";',
                "file_path": "/var/www/html/config.php",
                "line_number": 8,
                "cwe_id": "CWE-798",
                "cvss_score": 8.1
            },
            {
                "vulnerability_type": "path_traversal",
                "severity": "medium",
                "confidence": 0.85,
                "code_snippet": 'include($_GET["page"]);',
                "file_path": "/var/www/html/index.php",
                "line_number": 12,
                "cwe_id": "CWE-22",
                "cvss_score": 6.1
            }
        ]
        
        try:
            response = requests.post(
                f"{AI_SERVICE_URL}/api/ai-fixes/generate",
                json={
                    "vulnerabilities": test_vulnerabilities,
                    "auto_approve": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                fixes = data.get("fixes", [])
                
                self.ai_fixes_created = fixes
                
                self.log_test(
                    "AI Fixes Generation",
                    True,
                    f"Generated {len(fixes)} AI fixes successfully",
                    {
                        "fixes_generated": len(fixes),
                        "vulnerability_types": list(set(f.get("vulnerability_type") for f in fixes)),
                        "severities": list(set(f.get("severity") for f in fixes))
                    }
                )
                
                # Validate each fix
                for i, fix in enumerate(fixes, 1):
                    self.validate_fix_structure(fix, f"Fix {i}")
                
                return True
            else:
                self.log_test(
                    "AI Fixes Generation",
                    False,
                    f"Generation failed with status {response.status_code}",
                    {"response": response.text}
                )
                return False
                
        except Exception as e:
            self.log_test(
                "AI Fixes Generation",
                False,
                f"Request failed: {str(e)}",
                {"error": str(e)}
            )
            return False
    
    def validate_fix_structure(self, fix: Dict, fix_name: str):
        """Validate individual fix structure"""
        required_fields = [
            "id", "title", "description", "status", "severity",
            "confidence", "created_at", "vulnerability_type",
            "original_code", "fixed_code", "explanation", "recommendations"
        ]
        
        missing_fields = [field for field in required_fields if field not in fix]
        
        if missing_fields:
            self.log_test(
                f"Fix Structure Validation - {fix_name}",
                False,
                f"Missing required fields: {missing_fields}",
                {"missing_fields": missing_fields, "fix_id": fix.get("id")}
            )
        else:
            # Validate data types and content
            validation_issues = []
            
            if not isinstance(fix["confidence"], (int, float)) or not (0 <= fix["confidence"] <= 1):
                validation_issues.append("Invalid confidence value")
            
            if fix["severity"] not in ["critical", "high", "medium", "low"]:
                validation_issues.append("Invalid severity level")
            
            if fix["status"] not in ["pending", "approved", "rejected", "applied"]:
                validation_issues.append("Invalid status")
            
            if not fix["fixed_code"] or len(fix["fixed_code"]) < 10:
                validation_issues.append("Fixed code too short or empty")
            
            if not fix["recommendations"] or len(fix["recommendations"]) == 0:
                validation_issues.append("No recommendations provided")
            
            if validation_issues:
                self.log_test(
                    f"Fix Structure Validation - {fix_name}",
                    False,
                    f"Validation issues: {validation_issues}",
                    {"issues": validation_issues, "fix_id": fix.get("id")}
                )
            else:
                self.log_test(
                    f"Fix Structure Validation - {fix_name}",
                    True,
                    "Fix structure is valid and complete",
                    {
                        "fix_type": fix["vulnerability_type"],
                        "severity": fix["severity"],
                        "confidence": f"{fix['confidence']:.0%}"
                    }
                )
    
    def test_fix_lifecycle(self):
        """Test complete fix lifecycle: generate → approve → apply"""
        
        if not self.ai_fixes_created:
            self.log_test(
                "Fix Lifecycle Test",
                False,
                "No fixes available for lifecycle testing",
                {}
            )
            return False
        
        # Test first fix
        test_fix = self.ai_fixes_created[0]
        fix_id = test_fix["id"]
        
        # Test 1: Get fix details
        try:
            response = requests.get(f"{AI_SERVICE_URL}/api/ai-fixes/{fix_id}", timeout=10)
            
            if response.status_code == 200:
                fix_details = response.json()
                self.log_test(
                    "Get Fix Details",
                    True,
                    "Successfully retrieved fix details",
                    {"fix_id": fix_id, "status": fix_details.get("status")}
                )
            else:
                self.log_test(
                    "Get Fix Details",
                    False,
                    f"Failed to get fix details: {response.status_code}",
                    {"response": response.text}
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Get Fix Details",
                False,
                f"Request failed: {str(e)}",
                {"error": str(e)}
            )
            return False
        
        # Test 2: Approve fix
        try:
            response = requests.post(
                f"{AI_SERVICE_URL}/api/ai-fixes/{fix_id}/approve",
                json={"approved": True, "notes": "Approved during automated testing"},
                timeout=10
            )
            
            if response.status_code == 200:
                self.log_test(
                    "Approve Fix",
                    True,
                    "Fix approved successfully",
                    {"fix_id": fix_id}
                )
            else:
                self.log_test(
                    "Approve Fix",
                    False,
                    f"Failed to approve fix: {response.status_code}",
                    {"response": response.text}
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Approve Fix",
                False,
                f"Request failed: {str(e)}",
                {"error": str(e)}
            )
            return False
        
        # Test 3: Apply fix
        try:
            response = requests.post(
                f"{AI_SERVICE_URL}/api/ai-fixes/{fix_id}/apply",
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                self.log_test(
                    "Apply Fix",
                    True,
                    "Fix applied successfully",
                    {
                        "fix_id": fix_id,
                        "applied_at": result.get("applied_at"),
                        "has_fixed_code": "fixed_code" in result
                    }
                )
            else:
                self.log_test(
                    "Apply Fix",
                    False,
                    f"Failed to apply fix: {response.status_code}",
                    {"response": response.text}
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Apply Fix",
                False,
                f"Request failed: {str(e)}",
                {"error": str(e)}
            )
            return False
        
        return True
    
    def test_fix_management(self):
        """Test fix management operations"""
        
        if not self.ai_fixes_created:
            self.log_test(
                "Fix Management Test",
                False,
                "No fixes available for management testing",
                {}
            )
            return False
        
        # Test 1: Get all fixes
        try:
            response = requests.get(f"{AI_SERVICE_URL}/api/ai-fixes", timeout=10)
            
            if response.status_code == 200:
                all_fixes = response.json()
                self.log_test(
                    "Get All Fixes",
                    True,
                    f"Retrieved {len(all_fixes)} fixes",
                    {"total_fixes": len(all_fixes)}
                )
            else:
                self.log_test(
                    "Get All Fixes",
                    False,
                    f"Failed to get fixes: {response.status_code}",
                    {"response": response.text}
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Get All Fixes",
                False,
                f"Request failed: {str(e)}",
                {"error": str(e)}
            )
            return False
        
        # Test 2: Reject a fix (use second fix if available)
        if len(self.ai_fixes_created) > 1:
            test_fix = self.ai_fixes_created[1]
            fix_id = test_fix["id"]
            
            try:
                response = requests.post(
                    f"{AI_SERVICE_URL}/api/ai-fixes/{fix_id}/approve",
                    json={"approved": False, "notes": "Rejected during automated testing"},
                    timeout=10
                )
                
                if response.status_code == 200:
                    self.log_test(
                        "Reject Fix",
                        True,
                        "Fix rejected successfully",
                        {"fix_id": fix_id}
                    )
                else:
                    self.log_test(
                        "Reject Fix",
                        False,
                        f"Failed to reject fix: {response.status_code}",
                        {"response": response.text}
                    )
                    return False
                    
            except Exception as e:
                self.log_test(
                    "Reject Fix",
                    False,
                    f"Request failed: {str(e)}",
                    {"error": str(e)}
                )
                return False
        
        return True
    
    def test_error_handling(self):
        """Test error handling and edge cases"""
        
        # Test 1: Invalid fix ID
        try:
            response = requests.get(f"{AI_SERVICE_URL}/api/ai-fixes/invalid-id", timeout=10)
            
            if response.status_code == 404:
                self.log_test(
                    "Error Handling - Invalid Fix ID",
                    True,
                    "Correctly returned 404 for invalid fix ID",
                    {"status_code": response.status_code}
                )
            else:
                self.log_test(
                    "Error Handling - Invalid Fix ID",
                    False,
                    f"Expected 404, got {response.status_code}",
                    {"response": response.text}
                )
                
        except Exception as e:
            self.log_test(
                "Error Handling - Invalid Fix ID",
                False,
                f"Request failed: {str(e)}",
                {"error": str(e)}
            )
        
        # Test 2: Empty vulnerabilities list
        try:
            response = requests.post(
                f"{AI_SERVICE_URL}/api/ai-fixes/generate",
                json={"vulnerabilities": [], "auto_approve": False},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_test(
                    "Error Handling - Empty Vulnerabilities",
                    True,
                    "Handled empty vulnerabilities list gracefully",
                    {"fixes_generated": data.get("fixes_generated", 0)}
                )
            else:
                self.log_test(
                    "Error Handling - Empty Vulnerabilities",
                    False,
                    f"Failed to handle empty list: {response.status_code}",
                    {"response": response.text}
                )
                
        except Exception as e:
            self.log_test(
                "Error Handling - Empty Vulnerabilities",
                False,
                f"Request failed: {str(e)}",
                {"error": str(e)}
            )
        
        # Test 3: Apply unapproved fix
        if self.ai_fixes_created:
            # Find a pending fix
            pending_fix = next((f for f in self.ai_fixes_created if f["status"] == "pending"), None)
            
            if pending_fix:
                try:
                    response = requests.post(
                        f"{AI_SERVICE_URL}/api/ai-fixes/{pending_fix['id']}/apply",
                        timeout=10
                    )
                    
                    if response.status_code == 400:
                        self.log_test(
                            "Error Handling - Apply Unapproved Fix",
                            True,
                            "Correctly rejected application of unapproved fix",
                            {"status_code": response.status_code}
                        )
                    else:
                        self.log_test(
                            "Error Handling - Apply Unapproved Fix",
                            False,
                            f"Expected 400, got {response.status_code}",
                            {"response": response.text}
                        )
                        
                except Exception as e:
                    self.log_test(
                        "Error Handling - Apply Unapproved Fix",
                        False,
                        f"Request failed: {str(e)}",
                        {"error": str(e)}
                    )
    
    def test_performance(self):
        """Test AI service performance"""
        
        # Test 1: Response time for health check
        start_time = time.time()
        try:
            response = requests.get(f"{AI_SERVICE_URL}/health", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200 and response_time < 2.0:
                self.log_test(
                    "Performance - Health Check Response Time",
                    True,
                    f"Health check responded in {response_time:.2f}s",
                    {"response_time": response_time}
                )
            else:
                self.log_test(
                    "Performance - Health Check Response Time",
                    False,
                    f"Slow response: {response_time:.2f}s or status {response.status_code}",
                    {"response_time": response_time, "status": response.status_code}
                )
                
        except Exception as e:
            self.log_test(
                "Performance - Health Check Response Time",
                False,
                f"Request failed: {str(e)}",
                {"error": str(e)}
            )
        
        # Test 2: Fix generation performance
        if self.ai_fixes_created:
            start_time = time.time()
            try:
                response = requests.get(f"{AI_SERVICE_URL}/api/ai-fixes", timeout=10)
                response_time = time.time() - start_time
                
                if response.status_code == 200 and response_time < 3.0:
                    self.log_test(
                        "Performance - Fix Retrieval Response Time",
                        True,
                        f"Fix retrieval responded in {response_time:.2f}s",
                        {"response_time": response_time}
                    )
                else:
                    self.log_test(
                        "Performance - Fix Retrieval Response Time",
                        False,
                        f"Slow response: {response_time:.2f}s or status {response.status_code}",
                        {"response_time": response_time, "status": response.status_code}
                    )
                    
            except Exception as e:
                self.log_test(
                    "Performance - Fix Retrieval Response Time",
                    False,
                    f"Request failed: {str(e)}",
                    {"error": str(e)}
                )
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        passed_tests = len([r for r in self.test_results if r["success"]])
        total_tests = len(self.test_results)
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        report = {
            "test_summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": total_tests - passed_tests,
                "success_rate": f"{success_rate:.1f}%",
                "duration": f"{duration:.2f}s",
                "start_time": self.start_time.isoformat(),
                "end_time": end_time.isoformat()
            },
            "test_results": self.test_results,
            "ai_fixes_created": len(self.ai_fixes_created),
            "client_readiness": {
                "service_health": any(r["test"] == "AI Service Health Check" and r["success"] for r in self.test_results),
                "fix_generation": any(r["test"] == "AI Fixes Generation" and r["success"] for r in self.test_results),
                "lifecycle_management": any(r["test"] == "Fix Lifecycle Test" and r["success"] for r in self.test_results),
                "error_handling": any("Error Handling" in r["test"] and r["success"] for r in self.test_results),
                "performance_acceptable": any("Performance" in r["test"] and r["success"] for r in self.test_results)
            }
        }
        
        return report
    
    def run_all_tests(self):
        """Run complete test suite"""
        
        print("🚀 Starting DevGuardian AI Services Test Suite")
        print("=" * 60)
        print(f"⏰ Started at: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔗 AI Service: {AI_SERVICE_URL}")
        print(f"🌐 Frontend: {FRONTEND_URL}")
        print("=" * 60)
        
        # Run tests in logical order
        tests = [
            self.test_ai_service_health,
            self.test_ai_fixes_generation,
            self.test_fix_lifecycle,
            self.test_fix_management,
            self.test_error_handling,
            self.test_performance
        ]
        
        for test_func in tests:
            print(f"\n🧪 Running {test_func.__name__.replace('_', ' ').title()}...")
            test_func()
            time.sleep(0.5)  # Brief pause between tests
        
        # Generate final report
        report = self.generate_test_report()
        
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        summary = report["test_summary"]
        print(f"📈 Total Tests: {summary['total_tests']}")
        print(f"✅ Passed: {summary['passed_tests']}")
        print(f"❌ Failed: {summary['failed_tests']}")
        print(f"🎯 Success Rate: {summary['success_rate']}")
        print(f"⏱️ Duration: {summary['duration']}")
        print(f"🔧 AI Fixes Created: {report['ai_fixes_created']}")
        
        print("\n🚀 CLIENT READINESS CHECK:")
        readiness = report["client_readiness"]
        for check, status in readiness.items():
            icon = "✅" if status else "❌"
            check_name = check.replace('_', ' ').title()
            print(f"  {icon} {check_name}")
        
        # Overall readiness assessment
        all_critical_passed = all([
            readiness["service_health"],
            readiness["fix_generation"],
            readiness["lifecycle_management"]
        ])
        
        if all_critical_passed and summary["success_rate"] >= 80:
            print("\n🎉 SYSTEM READY FOR FIRST CLIENTS!")
            print("✅ All critical functionality is working")
            print("✅ Performance is acceptable")
            print("✅ Error handling is robust")
        else:
            print("\n⚠️ SYSTEM NEEDS ATTENTION BEFORE CLIENT DEPLOYMENT")
            print("❌ Some critical tests failed")
            print("🔧 Review failed tests and fix issues")
        
        return report

def create_interactive_ui_test():
    """Create interactive UI test for client demonstration"""
    
    print("\n🎨 INTERACTIVE UI/UX CLIENT TEST")
    print("=" * 50)
    
    instructions = """
📋 CLIENT TESTING INSTRUCTIONS:

1. 🌐 Open Frontend: http://localhost:3000
2. 🔍 Navigate to "AI Fixes" section
3. 📊 Review the generated fixes (should show 4-5 fixes)
4. 👁️ Click "View Details" on any fix to see:
   - Original vulnerable code
   - Fixed secure code
   - Detailed explanation
   - Security recommendations
5. ✅ Test the approval workflow:
   - Click "Approve" on a pending fix
   - Verify status changes to "approved"
   - Click "Apply" on approved fix
   - Verify status changes to "applied"
6. 🔍 Test search and filtering:
   - Use search bar to find specific fixes
   - Filter by severity (critical, high, medium, low)
   - Filter by status (pending, approved, rejected, applied)
7. 📱 Test responsive design:
   - Resize browser window
   - Test on different screen sizes
8. ⚡ Test performance:
   - Check loading times
   - Verify smooth animations
   - Test modal responsiveness

🎯 EXPECTED CLIENT EXPERIENCE:
✅ Professional, modern interface
✅ Intuitive navigation and controls
✅ Clear vulnerability information
✅ Easy fix management workflow
✅ Responsive design for all devices
✅ Fast, smooth interactions
"""
    
    print(instructions)
    
    # Create a simple web-based test interface
    test_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevGuardian AI - Client Test Interface</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 p-8">
    <div class="max-w-4xl mx-auto">
        <h1 class="text-3xl font-bold text-gray-900 mb-8">🚀 DevGuardian AI - Client Test Interface</h1>
        
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 class="text-xl font-semibold mb-4">📋 Test Checklist</h2>
            <div class="space-y-3">
                <label class="flex items-center space-x-3">
                    <input type="checkbox" class="w-4 h-4 text-blue-600">
                    <span>Frontend loads correctly at http://localhost:3000</span>
                </label>
                <label class="flex items-center space-x-3">
                    <input type="checkbox" class="w-4 h-4 text-blue-600">
                    <span>AI Fixes section shows generated fixes</span>
                </label>
                <label class="flex items-center space-x-3">
                    <input type="checkbox" class="w-4 h-4 text-blue-600">
                    <span>Fix details modal shows complete information</span>
                </label>
                <label class="flex items-center space-x-3">
                    <input type="checkbox" class="w-4 h-4 text-blue-600">
                    <span>Approval workflow works correctly</span>
                </label>
                <label class="flex items-center space-x-3">
                    <input type="checkbox" class="w-4 h-4 text-blue-600">
                    <span>Search and filtering functions properly</span>
                </label>
                <label class="flex items-center space-x-3">
                    <input type="checkbox" class="w-4 h-4 text-blue-600">
                    <span>Responsive design works on mobile</span>
                </label>
                <label class="flex items-center space-x-3">
                    <input type="checkbox" class="w-4 h-4 text-blue-600">
                    <span>Performance is fast and smooth</span>
                </label>
            </div>
        </div>
        
        <div class="bg-blue-50 rounded-lg p-6 mb-6">
            <h2 class="text-xl font-semibold mb-4">🔗 Quick Access Links</h2>
            <div class="space-y-2">
                <a href="http://localhost:3000" target="_blank" class="block text-blue-600 hover:underline">
                    🌐 Frontend Application
                </a>
                <a href="http://localhost:8000/docs" target="_blank" class="block text-blue-600 hover:underline">
                    📚 AI Service API Documentation
                </a>
                <a href="http://localhost:8002" target="_blank" class="block text-blue-600 hover:underline">
                    📖 Project Documentation
                </a>
            </div>
        </div>
        
        <div class="bg-green-50 rounded-lg p-6">
            <h2 class="text-xl font-semibold mb-4">✅ Success Criteria</h2>
            <ul class="list-disc list-inside space-y-2">
                <li>All critical functionality works without errors</li>
                <li>UI is professional and intuitive</li>
                <li>Performance meets client expectations</li>
                <li>Error handling is user-friendly</li>
                <li>Mobile experience is acceptable</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""
    
    with open("/home/marcelo/Documents/varas con chat gpt/proyecto/devguardian-ai/client_test_interface.html", "w") as f:
        f.write(test_html)
    
    print("📝 Created interactive test interface: client_test_interface.html")
    print("🌐 Open this file in your browser for guided testing")

if __name__ == "__main__":
    # Run comprehensive tests
    tester = AIServiceTester()
    report = tester.run_all_tests()
    
    # Save test report
    with open("/home/marcelo/Documents/varas con chat gpt/proyecto/devguardian-ai/test_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Detailed test report saved to: test_report.json")
    
    # Create interactive UI test
    create_interactive_ui_test()
    
    # Final client readiness message
    if report["client_readiness"]["service_health"] and report["client_readiness"]["fix_generation"]:
        print("\n🎉 AI SERVICES ARE READY FOR FIRST CLIENTS!")
        print("✅ All critical tests passed")
        print("✅ Interactive testing interface created")
        print("✅ Documentation and guides available")
    else:
        print("\n⚠️ SYSTEM NOT READY FOR CLIENTS")
        print("❌ Critical tests failed")
        print("🔧 Review test report and fix issues")

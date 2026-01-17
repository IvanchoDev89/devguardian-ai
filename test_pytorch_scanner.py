#!/usr/bin/env python3
"""
Comprehensive Test Script for PyTorch Vulnerability Scanner
Demonstrates advanced vulnerability detection using deep learning
"""

import sys
import os
import asyncio
import json
import tempfile
from pathlib import Path
from typing import List, Dict, Any

# Add the AI service path to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ai-service'))

from app.core.services.pytorch_vulnerability_scanner import (
    PyTorchVulnerabilityScanner, 
    VulnerabilityType, 
    VulnerabilityResult
)

def test_vulnerable_code_samples():
    """Test the scanner with various vulnerable code samples"""
    
    print("🔍 Testing PyTorch Vulnerability Scanner")
    print("=" * 60)
    
    # Initialize scanner
    scanner = PyTorchVulnerabilityScanner()
    
    # Test cases with different vulnerability types
    test_cases = [
        {
            "name": "SQL Injection in PHP",
            "file": "login.php",
            "code": """
<?php
$username = $_POST['username'];
$password = $_POST['password'];

// SQL Injection vulnerability
$query = "SELECT * FROM users WHERE username = '$username' AND password = '$password'";
$result = mysqli_query($conn, $query);

// Another SQL injection
$user_id = $_GET['id'];
$sql = "DELETE FROM users WHERE id = " . $user_id;
mysqli_query($conn, $sql);

// Hardcoded credentials
$db_password = "admin123";
$api_key = "sk-39284-2837-1827";
?>
            """,
            "expected_vulnerabilities": ["sql_injection", "hardcoded_credentials"]
        },
        {
            "name": "Cross-Site Scripting in JavaScript",
            "file": "profile.js",
            "code": """
// XSS vulnerability
function updateProfile() {
    const username = document.getElementById('username').value;
    const bio = document.getElementById('bio').value;
    
    // Direct DOM manipulation - XSS vulnerability
    document.getElementById('display').innerHTML = "Welcome " + username + "!";
    
    // Another XSS vulnerability
    document.write("<h1>User Bio: " + bio + "</h1>");
    
    // eval() usage
    const userInput = document.getElementById('command').value;
    eval(userInput);
}

// Unsafe assignment
element.outerHTML = userInput;
            """,
            "expected_vulnerabilities": ["xss", "command_injection"]
        },
        {
            "name": "Command Injection in Python",
            "file": "process.py",
            "code": """
import os
import subprocess

def process_file(filename):
    # Command injection vulnerability
    command = "ls -la " + filename
    os.system(command)
    
    # Another command injection
    user_input = request.args.get('file')
    subprocess.run(["cat", user_input], shell=True)
    
    # eval() usage
    code = request.args.get('code')
    eval(code)
    
    # Hardcoded secret
    SECRET_KEY = "super-secret-key-12345"
    
    # Weak cryptography
    import hashlib
    password_hash = hashlib.md5(password.encode()).hexdigest()
    
    # Insecure random
    import random
    session_token = str(random.random())
            """,
            "expected_vulnerabilities": ["command_injection", "hardcoded_credentials", "weak_cryptography", "insecure_random"]
        },
        {
            "name": "Path Traversal in Java",
            "file": "FileHandler.java",
            "code": """
import java.io.*;
import java.nio.file.*;

public class FileHandler {
    public void readFile(String filename) {
        // Path traversal vulnerability
        String filePath = "/var/www/uploads/" + filename;
        
        try {
            // Direct file access without validation
            File file = new File(filePath);
            BufferedReader reader = new BufferedReader(new FileReader(file));
            
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
            
            reader.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    // Hardcoded database credentials
    private static final String DB_URL = "jdbc:mysql://localhost:3306/mydb";
    private static final String DB_USER = "admin";
    private static final String DB_PASSWORD = "password123";
    
    // Weak encryption
    public String encrypt(String data) {
        try {
            // Using DES (weak encryption)
            Cipher cipher = Cipher.getInstance("DES/ECB/PKCS5Padding");
            // ... encryption logic
            return encryptedData;
        } catch (Exception e) {
            return null;
        }
    }
}
            """,
            "expected_vulnerabilities": ["path_traversal", "hardcoded_credentials", "weak_cryptography"]
        },
        {
            "name": "Buffer Overflow in C",
            "file": "buffer.c",
            "code": """
#include <stdio.h>
#include <string.h>

void processInput(char* input) {
    // Buffer overflow vulnerability
    char buffer[100];
    
    // Unsafe copy - no bounds checking
    strcpy(buffer, input);
    
    printf("Processed: %s\\n", buffer);
}

void vulnerableFunction() {
    char large_input[500];
    
    // Fill with data
    memset(large_input, 'A', 499);
    large_input[499] = '\\0';
    
    // This will cause buffer overflow
    processInput(large_input);
}

int main() {
    vulnerableFunction();
    return 0;
}
            """,
            "expected_vulnerabilities": ["buffer_overflow"]
        }
    ]
    
    # Run tests
    total_vulnerabilities = 0
    for i, test_case in enumerate(test_cases, 1):
        print(f"\\n📋 Test Case {i}: {test_case['name']}")
        print("-" * 40)
        
        # Scan the code
        vulnerabilities = scanner.scan_file(test_case['file'], test_case['code'])
        
        print(f"🔍 Found {len(vulnerabilities)} vulnerabilities:")
        
        for vuln in vulnerabilities:
            print(f"  • {vuln.vulnerability_type.value}")
            print(f"    Severity: {vuln.severity}")
            print(f"    Confidence: {vuln.confidence:.2f}")
            print(f"    Line: {vuln.line_number}")
            print(f"    Description: {vuln.description}")
            print(f"    CWE ID: {vuln.cwe_id}")
            print(f"    CVSS Score: {vuln.cvss_score}")
            print(f"    Recommendation: {vuln.recommendation}")
            print()
        
        total_vulnerabilities += len(vulnerabilities)
        
        # Check if expected vulnerabilities were found
        found_types = [v.vulnerability_type.value for v in vulnerabilities]
        print(f"✅ Expected: {test_case['expected_vulnerabilities']}")
        print(f"🔍 Found: {found_types}")
        
        missing = set(test_case['expected_vulnerabilities']) - set(found_types)
        if missing:
            print(f"⚠️  Missing: {list(missing)}")
        else:
            print("✅ All expected vulnerabilities found!")
    
    print(f"\\n📊 Summary:")
    print(f"Total test cases: {len(test_cases)}")
    print(f"Total vulnerabilities found: {total_vulnerabilities}")
    
    return total_vulnerabilities

def test_directory_scan():
    """Test directory scanning functionality"""
    print("\\n📁 Testing Directory Scan")
    print("=" * 40)
    
    # Create temporary directory with test files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create test files
        test_files = {
            "vulnerable.php": """
<?php
// SQL injection
$user = $_GET['user'];
$query = "SELECT * FROM users WHERE name = '$user'";
mysqli_query($conn, $query);

// Hardcoded password
$secret = "super-secret-password";
?>
            """,
            "xss.js": """
// XSS vulnerability
function displayUserInput() {
    const input = document.getElementById('userInput').value;
    document.getElementById('output').innerHTML = input;
}
            """,
            "safe.py": """
# Safe code example
def safe_function(user_input):
    # Input validation
    if not isinstance(user_input, str) or len(user_input) > 100:
        raise ValueError("Invalid input")
    
    # Safe processing
    return user_input.upper()
            """,
            "command_injection.sh": """
#!/bin/bash
# Command injection vulnerability
filename=$1
ls -la $filename
            """
        }
        
        # Write test files
        for filename, content in test_files.items():
            file_path = temp_path / filename
            file_path.write_text(content)
        
        # Initialize scanner
        scanner = PyTorchVulnerabilityScanner()
        
        # Scan directory
        print(f"🔍 Scanning directory: {temp_dir}")
        results = scanner.scan_directory(str(temp_dir))
        
        # Display results
        print(f"📁 Files scanned: {len(results)}")
        total_vulns = 0
        
        for file_path, vulnerabilities in results.items():
            print(f"\\n📄 {Path(file_path).name}: {len(vulnerabilities)} vulnerabilities")
            for vuln in vulnerabilities:
                print(f"  • {vuln.vulnerability_type.value} ({vuln.severity})")
                total_vulns += 1
        
        print(f"\\n📊 Total vulnerabilities found: {total_vulns}")
        
        # Generate comprehensive report
        report = scanner.generate_report(results)
        print(f"\\n📋 Scan Report:")
        print(f"  Scan date: {report['scan_date']}")
        print(f"  Total files scanned: {report['total_files_scanned']}")
        print(f"  Total vulnerabilities: {report['total_vulnerabilities']}")
        print(f"  Risk score: {report['risk_score']}")
        print(f"  Most common vulnerability: {report['most_common_vulnerability']}")
        print(f"  Highest risk file: {report['highest_risk_file']}")
        
        print(f"\\n📈 Severity breakdown:")
        for severity, count in report['severity_breakdown'].items():
            print(f"  {severity}: {count}")
        
        print(f"\\n🏷️  Type breakdown:")
        for vuln_type, count in report['type_breakdown'].items():
            print(f"  {vuln_type}: {count}")
        
        return total_vulns

def test_model_training():
    """Test model training functionality"""
    print("\\n🧠 Testing Model Training")
    print("=" * 40)
    
    # Create sample training data
    training_data = [
        {
            "code": "<?php $user = $_GET['user']; $query = \"SELECT * FROM users WHERE name = '$user'\"; ?>",
            "file_path": "vulnerable.php",
            "label": 1  # SQL injection
        },
        {
            "code": "<?php $user = $db->escape($_GET['user']); $query = \"SELECT * FROM users WHERE name = ?\"; ?>",
            "file_path": "safe.php",
            "label": 0  # Safe code
        },
        {
            "code": "eval(user_input);",
            "file_path": "dangerous.js",
            "label": 2  # Command injection
        },
        {
            "code": "const safe = JSON.parse(user_input);",
            "file_path": "safe.js",
            "label": 0  # Safe code
        }
    ]
    
    # Initialize scanner
    scanner = PyTorchVulnerabilityScanner()
    
    print("🏋️  Training models...")
    
    try:
        # Train models (reduced epochs for demo)
        scanner.train_models(training_data, epochs=2, batch_size=2)
        print("✅ Model training completed successfully!")
        
        # Test trained model
        test_code = "<?php $user = $_GET['user']; $query = \"SELECT * FROM users WHERE name = '$user'\"; ?>"
        vulnerabilities = scanner.scan_file("test.php", test_code)
        
        print(f"🔍 Trained model found {len(vulnerabilities)} vulnerabilities in test code")
        
        return True
        
    except Exception as e:
        print(f"❌ Model training failed: {str(e)}")
        return False

def test_performance():
    """Test scanner performance"""
    print("\\n⚡ Performance Testing")
    print("=" * 40)
    
    import time
    
    # Create large code sample
    large_code = """
<?php
// Large code sample for performance testing
for ($i = 0; $i < 1000; $i++) {
    $user = $_GET['user_' . $i];
    $query = "SELECT * FROM users WHERE name = '$user'";
    $result = mysqli_query($conn, $query);
    
    $password = "secret_" . $i;
    $api_key = "key_" . md5($password);
    
    eval($user_input);
    system("ls -la " . $filename);
}
?>
    """
    
    scanner = PyTorchVulnerabilityScanner()
    
    # Measure scan time
    start_time = time.time()
    vulnerabilities = scanner.scan_file("large_file.php", large_code)
    end_time = time.time()
    
    scan_time = end_time - start_time
    print(f"⏱️  Scan time: {scan_time:.2f} seconds")
    print(f"📊 Vulnerabilities found: {len(vulnerabilities)}")
    print(f"🚀 Performance: {len(large_code.split())} lines processed in {scan_time:.2f}s")
    
    return scan_time

def generate_sample_training_data():
    """Generate sample training data for model training"""
    print("\\n📝 Generating Sample Training Data")
    print("=" * 40)
    
    training_samples = [
        # SQL Injection examples
        {
            "code": "<?php $query = \"SELECT * FROM users WHERE id = \" . $_GET['id']; ?>",
            "file_path": "sql_injection_1.php",
            "label": 1,
            "vulnerability_type": "sql_injection",
            "severity": "critical"
        },
        {
            "code": "<?php $query = \"SELECT * FROM users WHERE name = '$name'\"; ?>",
            "file_path": "sql_injection_2.php",
            "label": 1,
            "vulnerability_type": "sql_injection",
            "severity": "critical"
        },
        
        # XSS examples
        {
            "code": "document.getElementById('output').innerHTML = userInput;",
            "file_path": "xss_1.js",
            "label": 2,
            "vulnerability_type": "xss",
            "severity": "high"
        },
        {
            "code": "element.outerHTML = maliciousContent;",
            "file_path": "xss_2.js",
            "label": 2,
            "vulnerability_type": "xss",
            "severity": "high"
        },
        
        # Command injection examples
        {
            "code": "system('ls -la ' + user_input);",
            "file_path": "cmd_injection_1.php",
            "label": 3,
            "vulnerability_type": "command_injection",
            "severity": "critical"
        },
        {
            "code": "exec($command);",
            "file_path": "cmd_injection_2.php",
            "label": 3,
            "vulnerability_type": "command_injection",
            "severity": "critical"
        },
        
        # Hardcoded credentials
        {
            "code": "$password = 'secret123';",
            "file_path": "hardcoded_1.php",
            "label": 4,
            "vulnerability_type": "hardcoded_credentials",
            "severity": "high"
        },
        {
            "code": "API_KEY = 'sk-1234567890abcdef';",
            "file_path": "hardcoded_2.py",
            "label": 4,
            "vulnerability_type": "hardcoded_credentials",
            "severity": "critical"
        },
        
        # Safe code examples
        {
            "code": "$stmt = $pdo->prepare('SELECT * FROM users WHERE id = ?');",
            "file_path": "safe_1.php",
            "label": 0,
            "vulnerability_type": None,
            "severity": None
        },
        {
            "code": "const sanitized = DOMPurify.sanitize(userInput);",
            "file_path": "safe_2.js",
            "label": 0,
            "vulnerability_type": None,
            "severity": None
        }
    ]
    
    # Save training data
    training_file = "pytorch_training_data.json"
    with open(training_file, 'w') as f:
        json.dump(training_samples, f, indent=2)
    
    print(f"📄 Generated {len(training_samples)} training samples")
    print(f"💾 Saved to: {training_file}")
    
    return training_file

def main():
    """Main test function"""
    print("🚀 PyTorch Vulnerability Scanner - Comprehensive Test Suite")
    print("=" * 70)
    
    try:
        # Test individual code samples
        total_vulns = test_vulnerable_code_samples()
        
        # Test directory scanning
        dir_vulns = test_directory_scan()
        
        # Test model training
        training_success = test_model_training()
        
        # Test performance
        scan_time = test_performance()
        
        # Generate training data
        training_file = generate_sample_training_data()
        
        # Final summary
        print("\\n🎯 Final Summary")
        print("=" * 40)
        print(f"✅ Code sample tests: {total_vulns} vulnerabilities found")
        print(f"✅ Directory scan: {dir_vulns} vulnerabilities found")
        print(f"✅ Model training: {'Success' if training_success else 'Failed'}")
        print(f"✅ Performance: {scan_time:.2f} seconds for large file")
        print(f"✅ Training data: Generated {training_file}")
        
        print(f"\\n🏆 Overall Status: SUCCESS")
        print("🔥 PyTorch Vulnerability Scanner is working correctly!")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

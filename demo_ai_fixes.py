#!/usr/bin/env python3
"""
Demo script to generate AI fixes for vulnerabilities
"""

import requests
import json
import time

# Sample vulnerabilities for demo
sample_vulnerabilities = [
    {
        "vulnerability_type": "sql_injection",
        "severity": "critical",
        "confidence": 0.95,
        "code_snippet": '$query = "SELECT * FROM users WHERE username = \'$username\' AND password = \'$password\'";',
        "file_path": "/var/www/html/login.php",
        "line_number": 15,
        "cwe_id": "CWE-89",
        "cvss_score": 9.8
    },
    {
        "vulnerability_type": "xss",
        "severity": "high",
        "confidence": 0.88,
        "code_snippet": "echo $_GET['name'];",
        "file_path": "/var/www/html/profile.php",
        "line_number": 42,
        "cwe_id": "CWE-79",
        "cvss_score": 7.5
    },
    {
        "vulnerability_type": "command_injection",
        "severity": "critical",
        "confidence": 0.92,
        "code_snippet": "system($user_command);",
        "file_path": "/var/www/html/admin.php",
        "line_number": 78,
        "cwe_id": "CWE-78",
        "cvss_score": 9.0
    },
    {
        "vulnerability_type": "hardcoded_credentials",
        "severity": "high",
        "confidence": 0.98,
        "code_snippet": '$api_key = "sk-39284-2837-1827";',
        "file_path": "/var/www/html/config.php",
        "line_number": 12,
        "cwe_id": "CWE-798",
        "cvss_score": 8.1
    }
]

def generate_ai_fixes():
    """Generate AI fixes for sample vulnerabilities"""
    
    print("🚀 Generating AI fixes for vulnerabilities...")
    
    try:
        response = requests.post(
            "http://localhost:8000/api/ai-fixes/generate",
            json={
                "vulnerabilities": sample_vulnerabilities,
                "auto_approve": False
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Successfully generated {result['fixes_generated']} AI fixes!")
            print(f"📊 Message: {result['message']}")
            
            # Display generated fixes
            for i, fix in enumerate(result['fixes'], 1):
                print(f"\n🔧 Fix {i}:")
                print(f"   Title: {fix['title']}")
                print(f"   Type: {fix['vulnerability_type']}")
                print(f"   Severity: {fix['severity']}")
                print(f"   Status: {fix['status']}")
                print(f"   Confidence: {fix['confidence']:.0%}")
                print(f"   Created: {fix['created_at']}")
            
            return result['fixes']
        else:
            print(f"❌ Failed to generate fixes: {response.status_code}")
            print(f"Response: {response.text}")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to AI service: {e}")
        return []

def get_ai_fixes():
    """Get all AI fixes"""
    
    print("\n📋 Retrieving all AI fixes...")
    
    try:
        response = requests.get("http://localhost:8000/api/ai-fixes", timeout=10)
        
        if response.status_code == 200:
            fixes = response.json()
            print(f"✅ Found {len(fixes)} AI fixes")
            
            for i, fix in enumerate(fixes, 1):
                print(f"\n🔧 Fix {i}:")
                print(f"   ID: {fix['id']}")
                print(f"   Title: {fix['title']}")
                print(f"   Type: {fix['vulnerability_type']}")
                print(f"   Severity: {fix['severity']}")
                print(f"   Status: {fix['status']}")
                print(f"   Confidence: {fix['confidence']:.0%}")
            
            return fixes
        else:
            print(f"❌ Failed to get fixes: {response.status_code}")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to AI service: {e}")
        return []

def approve_fix(fix_id):
    """Approve a specific fix"""
    
    print(f"\n✅ Approving fix {fix_id}...")
    
    try:
        response = requests.post(
            f"http://localhost:8000/api/ai-fixes/{fix_id}/approve",
            json={"approved": True, "notes": "Approved via demo script"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {result['message']}")
            return True
        else:
            print(f"❌ Failed to approve fix: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to AI service: {e}")
        return False

def apply_fix(fix_id):
    """Apply a specific fix"""
    
    print(f"\n🔧 Applying fix {fix_id}...")
    
    try:
        response = requests.post(
            f"http://localhost:8000/api/ai-fixes/{fix_id}/apply",
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {result['message']}")
            if 'fixed_code' in result:
                print(f"📝 Fixed code preview:")
                print(result['fixed_code'][:200] + "..." if len(result['fixed_code']) > 200 else result['fixed_code'])
            return True
        else:
            print(f"❌ Failed to apply fix: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to AI service: {e}")
        return False

def get_fix_stats():
    """Get fix statistics"""
    
    print("\n📊 Getting AI fix statistics...")
    
    try:
        response = requests.get("http://localhost:8000/api/ai-fixes/stats", timeout=10)
        
        if response.status_code == 200:
            stats = response.json()
            print(f"📈 AI Fix Statistics:")
            print(f"   Total fixes: {stats['total']}")
            print(f"   Applied: {stats['applied']}")
            print(f"   Pending: {stats['pending']}")
            print(f"   Approved: {stats['approved']}")
            print(f"   Rejected: {stats['rejected']}")
            
            print(f"\n🎯 Severity Breakdown:")
            for severity, count in stats['severity_breakdown'].items():
                print(f"   {severity}: {count}")
            
            print(f"\n🔍 Type Breakdown:")
            for vtype, count in stats['type_breakdown'].items():
                print(f"   {vtype}: {count}")
            
            return stats
        else:
            print(f"❌ Failed to get stats: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to AI service: {e}")
        return None

def main():
    """Main demo function"""
    
    print("🚀 DevGuardian AI - AI Fixes Demo")
    print("=" * 50)
    
    # Check if AI service is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            print("❌ AI service is not running or not healthy")
            print("Please start the AI service first:")
            print("cd ai-service && python main.py")
            return
    except requests.exceptions.RequestException:
        print("❌ Cannot connect to AI service")
        print("Please start the AI service first:")
        print("cd ai-service && python main.py")
        return
    
    print("✅ AI service is running!")
    
    # Generate AI fixes
    fixes = generate_ai_fixes()
    
    if fixes:
        # Wait a moment for processing
        time.sleep(1)
        
        # Get all fixes
        all_fixes = get_ai_fixes()
        
        if all_fixes:
            # Demo: Approve first fix
            if len(all_fixes) > 0:
                first_fix = all_fixes[0]
                if approve_fix(first_fix['id']):
                    # Apply the approved fix
                    apply_fix(first_fix['id'])
            
            # Get final statistics
            get_fix_stats()
    
    print("\n🎉 Demo completed!")
    print("You can now view the AI fixes in the frontend at http://localhost:3000")

if __name__ == "__main__":
    main()

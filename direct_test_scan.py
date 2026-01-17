#!/usr/bin/env python3
"""
Direct test scan of local repository
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from automated_repository_analyzer import AutomatedRepositoryAnalyzer

def main():
    """Direct scan of local test repository"""
    
    print("🔍 Direct Repository Security Scan")
    print("=" * 50)
    
    # Create analyzer
    analyzer = AutomatedRepositoryAnalyzer()
    
    # Get test repository path
    test_repo_path = Path("test_repository")
    
    if not test_repo_path.exists():
        print("❌ Test repository not found!")
        print("📁 Run 'python3 create_test_repo.py' first")
        return
    
    print(f"📁 Scanning local repository: {test_repo_path.absolute()}")
    
    # Scan the repository directly
    try:
        vulnerabilities = analyzer._scan_repository(test_repo_path, "standard")
        
        print(f"\n📊 Scan Results")
        print("=" * 30)
        print(f"🚨 Total vulnerabilities found: {len(vulnerabilities)}")
        
        if vulnerabilities:
            # Group by file
            files_vulns = {}
            for vuln in vulnerabilities:
                file_path = vuln['file_path']
                if file_path not in files_vulns:
                    files_vulns[file_path] = []
                files_vulns[file_path].append(vuln)
            
            print(f"\n📁 Vulnerabilities by file:")
            for file_path, vulns in files_vulns.items():
                print(f"\n📄 {file_path}:")
                for vuln in vulns:
                    print(f"  • {vuln['vulnerability_type']} ({vuln['severity']})")
                    print(f"    Line {vuln['line_number']}: {vuln['description']}")
                    print(f"    Code: {vuln['code_snippet'][:80]}...")
                    print(f"    Recommendation: {vuln['recommendation']}")
                    print()
            
            # Severity breakdown
            severity_counts = {}
            type_counts = {}
            
            for vuln in vulnerabilities:
                severity = vuln['severity']
                vuln_type = vuln['vulnerability_type']
                
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
                type_counts[vuln_type] = type_counts.get(vuln_type, 0) + 1
            
            print(f"📈 Severity Breakdown:")
            for severity, count in severity_counts.items():
                icon = {'critical': '🚨', 'high': '⚠️', 'medium': '🔸', 'low': '🔹'}.get(severity, '📊')
                print(f"  {icon} {severity}: {count}")
            
            print(f"\n🏷️  Type Breakdown:")
            for vuln_type, count in type_counts.items():
                print(f"  🎯 {vuln_type}: {count}")
            
            # Calculate risk score
            risk_score = (
                severity_counts.get('critical', 0) * 10 +
                severity_counts.get('high', 0) * 7 +
                severity_counts.get('medium', 0) * 4 +
                severity_counts.get('low', 0) * 1
            )
            
            print(f"\n⚠️  Overall Risk Score: {risk_score}")
            
            # Recommendations
            recommendations = analyzer._generate_suite_recommendations(severity_counts, type_counts)
            print(f"\n💡 Key Recommendations:")
            for i, rec in enumerate(recommendations[:5], 1):
                print(f"  {i}. {rec}")
        
        else:
            print("✅ No vulnerabilities found!")
            print("🎉 The repository appears to be secure.")
        
        print(f"\n🚀 Direct scan completed successfully!")
        
    except Exception as e:
        print(f"❌ Scan failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

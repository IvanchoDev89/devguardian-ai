#!/usr/bin/env python3
"""
Security Test Runner
Comprehensive test runner for automated repository security analysis
"""

import sys
import os
import argparse
import time
from pathlib import Path
from typing import Optional, List

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from automated_repository_analyzer import AutomatedRepositoryAnalyzer
from test_configurations import create_test_suites, get_suite_info, create_custom_suite

def print_banner():
    """Print application banner"""
    print("🔍 Automated Repository Security Analyzer")
    print("=" * 60)
    print("🛡️  Comprehensive security vulnerability scanning using PyTorch")
    print("📊 Automated analysis of multiple repositories with detailed reporting")
    print("🚀 Production-ready security testing for development teams")
    print()

def list_suites():
    """List all available test suites"""
    print("📋 Available Test Suites")
    print("=" * 40)
    
    suites_info = get_suite_info()
    
    for i, (name, info) in enumerate(suites_info.items(), 1):
        print(f"\n{i}. {name}")
        print(f"   📝 {info['description']}")
        print(f"   📁 Repositories: {info['repository_count']}")
        print(f"   ⏱️  Estimated time: {info['estimated_time']}")
        print(f"   🔧 Scan depth: {info['scan_depth']}")
        print(f"   ⚡ Workers: {info['max_workers']}")

def run_suite(suite_name: str, output_dir: Optional[str] = None):
    """Run a specific test suite"""
    
    print(f"🚀 Running test suite: {suite_name}")
    print("=" * 50)
    
    # Get test suites
    suites = create_test_suites()
    
    if suite_name not in suites:
        print(f"❌ Test suite '{suite_name}' not found!")
        print("📋 Available suites:")
        for name in suites.keys():
            print(f"  - {name}")
        return False
    
    suite = suites[suite_name]
    
    # Create analyzer
    workspace_dir = Path("analysis_workspace")
    if output_dir:
        workspace_dir = Path(output_dir)
    
    analyzer = AutomatedRepositoryAnalyzer(str(workspace_dir))
    
    print(f"📋 Suite: {suite.name}")
    print(f"📝 Description: {suite.description}")
    print(f"📁 Repositories: {len(suite.repositories)}")
    print(f"🔧 Scan depth: {suite.scan_depth}")
    print(f"⚡ Parallel processing: {suite.parallel_processing}")
    print(f"👥 Max workers: {suite.max_workers}")
    print()
    
    # Run the test suite
    start_time = time.time()
    
    try:
        report = analyzer.run_test_suite(suite)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Display results
        print("\n📊 Test Suite Results")
        print("=" * 40)
        print(f"✅ Successful analyses: {report['summary']['successful_analyses']}")
        print(f"❌ Failed analyses: {report['summary']['failed_analyses']}")
        print(f"📁 Total files analyzed: {report['summary']['total_files_analyzed']}")
        print(f"🚨 Total vulnerabilities: {report['summary']['total_vulnerabilities']}")
        print(f"⚠️  Overall risk score: {report['summary']['overall_risk_score']}")
        print(f"⏱️  Total scan time: {report['summary']['total_scan_time']:.2f}s")
        print(f"📈 Average scan time: {report['summary']['average_scan_time']:.2f}s")
        print(f"⏰ Total duration: {duration:.2f}s")
        
        # Severity breakdown
        if report['severity_breakdown']:
            print("\n📈 Severity Breakdown:")
            for severity, count in sorted(report['severity_breakdown'].items(), 
                                        key=lambda x: {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}.get(x[0], 0), 
                                        reverse=True):
                icon = {'critical': '🚨', 'high': '⚠️', 'medium': '🔸', 'low': '🔹'}.get(severity, '📊')
                print(f"  {icon} {severity}: {count}")
        
        # Type breakdown
        if report['type_breakdown']:
            print("\n🏷️  Vulnerability Types:")
            for vuln_type, count in sorted(report['type_breakdown'].items(), 
                                         key=lambda x: x[1], reverse=True)[:10]:
                print(f"  🎯 {vuln_type}: {count}")
        
        # Top repositories by risk
        if report['repository_results']:
            print("\n🔥 Highest Risk Repositories:")
            sorted_repos = sorted(report['repository_results'], 
                                key=lambda x: x['risk_score'], reverse=True)[:5]
            for repo in sorted_repos:
                if repo['status'] == 'success':
                    print(f"  📁 {repo['repository_name']}: Risk Score {repo['risk_score']} "
                          f"({repo['total_vulnerabilities']} vulnerabilities)")
        
        # Key recommendations
        if report['recommendations']:
            print("\n💡 Key Recommendations:")
            for i, rec in enumerate(report['recommendations'][:5], 1):
                print(f"  {i}. {rec}")
        
        # Output location
        print(f"\n📁 Results saved to: test_results/")
        print(f"🎉 Test suite '{suite_name}' completed successfully!")
        
        return True
        
    except KeyboardInterrupt:
        print("\n⚠️  Test suite interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Test suite failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def run_custom_test(repositories: List[str], suite_name: str = "custom", 
                    scan_depth: str = "standard", max_workers: int = 4):
    """Run a custom test with specified repositories"""
    
    print(f"🚀 Running custom test suite: {suite_name}")
    print("=" * 50)
    
    # Create custom suite
    suite = create_custom_suite(
        name=suite_name,
        description=f"Custom test suite with {len(repositories)} repositories",
        repositories=repositories,
        scan_depth=scan_depth,
        max_workers=max_workers
    )
    
    # Create analyzer and run
    analyzer = AutomatedRepositoryAnalyzer()
    
    try:
        report = analyzer.run_test_suite(suite)
        
        print(f"\n📊 Custom Test Results")
        print("=" * 30)
        print(f"📁 Repositories analyzed: {len(repositories)}")
        print(f"🚨 Total vulnerabilities: {report['summary']['total_vulnerabilities']}")
        print(f"⚠️  Overall risk score: {report['summary']['overall_risk_score']}")
        print(f"⏱️  Total scan time: {report['summary']['total_scan_time']:.2f}s")
        
        return True
        
    except Exception as e:
        print(f"❌ Custom test failed: {str(e)}")
        return False

def quick_demo():
    """Run a quick demonstration"""
    
    print("🚀 Quick Demo Mode")
    print("=" * 30)
    print("Running analysis on a small repository for demonstration...")
    
    # Use a small, safe repository for demo
    demo_repos = [
        "https://github.com/octocat/Hello-World"
    ]
    
    return run_custom_test(demo_repos, "quick_demo", "basic", 1)

def main():
    """Main function"""
    
    parser = argparse.ArgumentParser(
        description="Automated Repository Security Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_security_tests.py --list                          # List available test suites
  python run_security_tests.py --suite quick_demo              # Run quick demo
  python run_security_tests.py --suite popular_open_source     # Run popular open source suite
  python run_security_tests.py --custom https://github.com/user/repo  # Run custom test
  python run_security_tests.py --demo                          # Quick demonstration
        """
    )
    
    parser.add_argument("--list", action="store_true", 
                       help="List all available test suites")
    parser.add_argument("--suite", type=str, 
                       help="Run a specific test suite")
    parser.add_argument("--custom", type=str, nargs="+", 
                       help="Run custom test with specified repository URLs")
    parser.add_argument("--demo", action="store_true", 
                       help="Run quick demonstration")
    parser.add_argument("--name", type=str, default="custom_test",
                       help="Name for custom test suite")
    parser.add_argument("--depth", type=str, default="standard",
                       choices=["basic", "standard", "comprehensive"],
                       help="Scan depth for custom test")
    parser.add_argument("--workers", type=int, default=4,
                       help="Number of parallel workers")
    parser.add_argument("--output", type=str,
                       help="Output directory for results")
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Handle commands
    if args.list:
        list_suites()
    elif args.demo:
        quick_demo()
    elif args.suite:
        success = run_suite(args.suite, args.output)
        sys.exit(0 if success else 1)
    elif args.custom:
        success = run_custom_test(args.custom, args.name, args.depth, args.workers)
        sys.exit(0 if success else 1)
    else:
        parser.print_help()
        print("\n🚀 Quick start:")
        print("  python run_security_tests.py --demo")
        print("  python run_security_tests.py --list")
        print("  python run_security_tests.py --suite quick_demo")

if __name__ == "__main__":
    main()

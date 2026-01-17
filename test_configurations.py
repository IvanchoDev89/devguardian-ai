#!/usr/bin/env python3
"""
Test Configurations for Automated Repository Analyzer
Predefined test suites for different security analysis scenarios
"""

from dataclasses import dataclass
from typing import List, Dict, Any
from automated_repository_analyzer import TestSuite

@dataclass
class RepositoryConfig:
    """Configuration for a single repository"""
    url: str
    branch: str = "main"
    priority: str = "medium"  # high, medium, low
    description: str = ""

# Predefined repository configurations
POPULAR_OPEN_SOURCE = [
    RepositoryConfig(
        url="https://github.com/WordPress/WordPress",
        branch="master",
        priority="high",
        description="Most popular CMS - large codebase with historical vulnerabilities"
    ),
    RepositoryConfig(
        url="https://github.com/laravel/laravel",
        branch="master",
        priority="high",
        description="Popular PHP framework with comprehensive security features"
    ),
    RepositoryConfig(
        url="https://github.com/django/django",
        branch="main",
        priority="high",
        description="Python web framework with strong security focus"
    ),
    RepositoryConfig(
        url="https://github.com/nodejs/node",
        branch="main",
        priority="medium",
        description="Node.js JavaScript runtime"
    ),
    RepositoryConfig(
        url="https://github.com/python/cpython",
        branch="main",
        priority="medium",
        description="Python programming language implementation"
    )
]

SECURITY_FOCUSED = [
    RepositoryConfig(
        url="https://github.com/OWASP/OWASP-CheatSheetSeries",
        branch="master",
        priority="high",
        description="OWASP security cheat sheets - should be secure"
    ),
    RepositoryConfig(
        url="https://github.com/PortSwigger/http-requests-smuggler",
        branch="master",
        priority="high",
        description="HTTP request smuggling tool - security focused"
    ),
    RepositoryConfig(
        url="https://github.com/rapid7/metasploit-framework",
        branch="master",
        priority="medium",
        description="Metasploit penetration testing framework"
    ),
    RepositoryConfig(
        url="https://github.com/Azure/azure-sdk-for-python",
        branch="main",
        priority="medium",
        description="Azure SDK with security considerations"
    )
]

WEB_APPLICATIONS = [
    RepositoryConfig(
        url="https://github.com/facebook/react",
        branch="main",
        priority="high",
        description="React JavaScript library"
    ),
    RepositoryConfig(
        url="https://github.com/vuejs/vue",
        branch="main",
        priority="high",
        description="Vue.js JavaScript framework"
    ),
    RepositoryConfig(
        url="https://github.com/angular/angular",
        branch="main",
        priority="medium",
        description="Angular TypeScript framework"
    ),
    RepositoryConfig(
        url="https://github.com/expressjs/express",
        branch="master",
        priority="high",
        description="Express.js web framework"
    ),
    RepositoryConfig(
        url="https://github.com/rails/rails",
        branch="main",
        priority="medium",
        description="Ruby on Rails web framework"
    )
]

MOBILE_APPLICATIONS = [
    RepositoryConfig(
        url="https://github.com/facebook/react-native",
        branch="main",
        priority="medium",
        description="React Native mobile framework"
    ),
    RepositoryConfig(
        url="https://github.com/flutter/flutter",
        branch="main",
        priority="medium",
        description="Flutter mobile development framework"
    ),
    RepositoryConfig(
        url="https://github.com/kivy/kivy",
        branch="master",
        priority="low",
        description="Python mobile app framework"
    )
]

SYSTEM_TOOLS = [
    RepositoryConfig(
        url="https://github.com/systemd/systemd",
        branch="main",
        priority="high",
        description="System and service manager - critical system component"
    ),
    RepositoryConfig(
        url="https://github.com/torvalds/linux",
        branch="master",
        priority="high",
        description="Linux kernel - critical system software"
    ),
    RepositoryConfig(
        url="https://github.com/nginx/nginx",
        branch="main",
        priority="medium",
        description="Nginx web server"
    ),
    RepositoryConfig(
        url="https://github.com/openssl/openssl",
        branch="master",
        priority="high",
        description="OpenSSL cryptography library"
    )
]

DEVOPS_TOOLS = [
    RepositoryConfig(
        url="https://github.com/kubernetes/kubernetes",
        branch="main",
        priority="high",
        description="Kubernetes container orchestration"
    ),
    RepositoryConfig(
        url="https://github.com/docker/docker",
        branch="master",
        priority="medium",
        description="Docker container platform"
    ),
    RepositoryConfig(
        url="https://github.com/hashicorp/terraform",
        branch="main",
        priority="medium",
        description="Terraform infrastructure as code"
    ),
    RepositoryConfig(
        url="https://github.com/ansible/ansible",
        branch="main",
        priority="medium",
        description="Ansible automation tool"
    )
]

DATABASE_SYSTEMS = [
    RepositoryConfig(
        url="https://github.com/postgres/postgres",
        branch="master",
        priority="high",
        description="PostgreSQL database system"
    ),
    RepositoryConfig(
        url="https://github.com/mysql/mysql-server",
        branch="master",
        priority="high",
        description="MySQL database server"
    ),
    RepositoryConfig(
        url="https://github.com/redis/redis",
        branch="main",
        priority="medium",
        description="Redis in-memory data store"
    ),
    RepositoryConfig(
        url="https://github.com/mongodb/mongo",
        branch="main",
        priority="medium",
        description="MongoDB NoSQL database"
    )
]

def create_test_suites() -> Dict[str, TestSuite]:
    """Create predefined test suites"""
    
    suites = {}
    
    # Quick Demo Suite
    suites["quick_demo"] = TestSuite(
        name="Quick_Demo",
        description="Quick demonstration with 2-3 small repositories",
        repositories=[
            "https://github.com/octocat/Hello-World",
            "https://github.com/octocat/Spoon-Knife"
        ],
        scan_depth="basic",
        enable_ml_detection=True,
        enable_pattern_detection=True,
        parallel_processing=True,
        max_workers=2,
        output_format="json"
    )
    
    # Popular Open Source Suite
    suites["popular_open_source"] = TestSuite(
        name="Popular_Open_Source",
        description="Analysis of popular open source projects",
        repositories=[config.url for config in POPULAR_OPEN_SOURCE],
        scan_depth="standard",
        enable_ml_detection=True,
        enable_pattern_detection=True,
        parallel_processing=True,
        max_workers=4,
        output_format="json"
    )
    
    # Security Focused Suite
    suites["security_focused"] = TestSuite(
        name="Security_Focused_Projects",
        description="Analysis of security-focused repositories",
        repositories=[config.url for config in SECURITY_FOCUSED],
        scan_depth="comprehensive",
        enable_ml_detection=True,
        enable_pattern_detection=True,
        parallel_processing=True,
        max_workers=3,
        output_format="json"
    )
    
    # Web Applications Suite
    suites["web_applications"] = TestSuite(
        name="Web_Applications",
        description="Analysis of popular web application frameworks",
        repositories=[config.url for config in WEB_APPLICATIONS],
        scan_depth="standard",
        enable_ml_detection=True,
        enable_pattern_detection=True,
        parallel_processing=True,
        max_workers=4,
        output_format="json"
    )
    
    # Mobile Applications Suite
    suites["mobile_applications"] = TestSuite(
        name="Mobile_Applications",
        description="Analysis of mobile application frameworks",
        repositories=[config.url for config in MOBILE_APPLICATIONS],
        scan_depth="standard",
        enable_ml_detection=True,
        enable_pattern_detection=True,
        parallel_processing=True,
        max_workers=2,
        output_format="json"
    )
    
    # System Tools Suite
    suites["system_tools"] = TestSuite(
        name="System_Tools",
        description="Analysis of critical system tools and software",
        repositories=[config.url for config in SYSTEM_TOOLS],
        scan_depth="comprehensive",
        enable_ml_detection=True,
        enable_pattern_detection=True,
        parallel_processing=True,
        max_workers=2,
        output_format="json"
    )
    
    # DevOps Tools Suite
    suites["devops_tools"] = TestSuite(
        name="DevOps_Tools",
        description="Analysis of DevOps and infrastructure tools",
        repositories=[config.url for config in DEVOPS_TOOLS],
        scan_depth="standard",
        enable_ml_detection=True,
        enable_pattern_detection=True,
        parallel_processing=True,
        max_workers=3,
        output_format="json"
    )
    
    # Database Systems Suite
    suites["database_systems"] = TestSuite(
        name="Database_Systems",
        description="Analysis of database management systems",
        repositories=[config.url for config in DATABASE_SYSTEMS],
        scan_depth="comprehensive",
        enable_ml_detection=True,
        enable_pattern_detection=True,
        parallel_processing=True,
        max_workers=2,
        output_format="json"
    )
    
    # Comprehensive Suite (All categories)
    all_repos = []
    for category in [POPULAR_OPEN_SOURCE, SECURITY_FOCUSED, WEB_APPLICATIONS, 
                    MOBILE_APPLICATIONS, SYSTEM_TOOLS, DEVOPS_TOOLS, DATABASE_SYSTEMS]:
        all_repos.extend([config.url for config in category])
    
    suites["comprehensive"] = TestSuite(
        name="Comprehensive_Analysis",
        description="Comprehensive analysis of all repository categories",
        repositories=all_repos,
        scan_depth="comprehensive",
        enable_ml_detection=True,
        enable_pattern_detection=True,
        parallel_processing=True,
        max_workers=6,
        output_format="json"
    )
    
    # Performance Testing Suite
    suites["performance_test"] = TestSuite(
        name="Performance_Testing",
        description="Performance testing with large repositories",
        repositories=[
            "https://github.com/torvalds/linux",
            "https://github.com/chromium/chromium",
            "https://github.com/microsoft/vscode"
        ],
        scan_depth="basic",  # Basic scan for performance
        enable_ml_detection=False,  # Disable ML for speed
        enable_pattern_detection=True,
        parallel_processing=True,
        max_workers=8,
        output_format="json"
    )
    
    return suites

def get_suite_info() -> Dict[str, Dict[str, Any]]:
    """Get information about all available test suites"""
    
    suites = create_test_suites()
    info = {}
    
    for name, suite in suites.items():
        info[name] = {
            "name": suite.name,
            "description": suite.description,
            "repository_count": len(suite.repositories),
            "scan_depth": suite.scan_depth,
            "parallel_processing": suite.parallel_processing,
            "max_workers": suite.max_workers,
            "estimated_time": f"{len(suite.repositories) * 2}-{len(suite.repositories) * 5} minutes"
        }
    
    return info

def create_custom_suite(name: str, description: str, repositories: List[str], 
                        scan_depth: str = "standard", max_workers: int = 4) -> TestSuite:
    """Create a custom test suite"""
    
    return TestSuite(
        name=name,
        description=description,
        repositories=repositories,
        scan_depth=scan_depth,
        enable_ml_detection=True,
        enable_pattern_detection=True,
        parallel_processing=True,
        max_workers=max_workers,
        output_format="json"
    )

def main():
    """Display available test suites"""
    
    print("🔧 Available Test Suites")
    print("=" * 60)
    
    suites_info = get_suite_info()
    
    for name, info in suites_info.items():
        print(f"\n📋 {name}")
        print(f"   Description: {info['description']}")
        print(f"   Repositories: {info['repository_count']}")
        print(f"   Scan depth: {info['scan_depth']}")
        print(f"   Estimated time: {info['estimated_time']}")
        print(f"   Parallel workers: {info['max_workers']}")
    
    print(f"\n📊 Total available suites: {len(suites_info)}")
    print("🚀 Use these suite names with the automated repository analyzer")

if __name__ == "__main__":
    main()

"""
Pytest configuration and fixtures
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def sample_clean_code():
    """Fixture for clean code sample"""
    return """
def hello_world():
    print("Hello, World!")
    return True

class Calculator:
    def add(self, a, b):
        return a + b
"""


@pytest.fixture
def sample_vulnerable_code():
    """Fixture for vulnerable code sample"""
    return """
password = "hardcoded123"
query = f"SELECT * FROM users WHERE id = {user_id}"
eval("dangerous_code")
"""


@pytest.fixture
def scanner():
    """Fixture for vulnerability scanner"""
    from app.scanners.vulnerability_scanner import create_scanner
    return create_scanner()

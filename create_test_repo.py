#!/usr/bin/env python3
"""
Create test repositories for demonstration
"""

import os
import subprocess
from pathlib import Path

def create_test_repository():
    """Create a test repository with vulnerabilities"""
    
    # Create test directory
    test_dir = Path("test_repository")
    if test_dir.exists():
        import shutil
        shutil.rmtree(test_dir)
    
    test_dir.mkdir()
    
    # Initialize git repo
    subprocess.run(["git", "init"], cwd=test_dir, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=test_dir, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=test_dir, check=True)
    
    # Create vulnerable files
    
    # Vulnerable PHP file
    php_file = test_dir / "login.php"
    php_file.write_text("""<?php
// SQL Injection vulnerability
$username = $_POST['username'];
$password = $_POST['password'];

// Direct SQL concatenation - VULNERABLE
$query = "SELECT * FROM users WHERE username = '$username' AND password = '$password'";
$result = mysqli_query($conn, $query);

// Hardcoded credentials - VULNERABLE
$db_password = "admin123";
$api_key = "sk-39284-2837-1827";

// Another SQL injection
$user_id = $_GET['id'];
$sql = "DELETE FROM users WHERE id = " . $user_id;
mysqli_query($conn, $sql);

// Command injection - VULNERABLE
$cmd = "ls -la " . $_GET['dir'];
system($cmd);

// XSS vulnerability - VULNERABLE
echo "<h1>Welcome " . $_GET['name'] . "</h1>";

// eval() usage - VULNERABLE
eval($_GET['code']);
?>
""")
    
    # Vulnerable JavaScript file
    js_file = test_dir / "profile.js"
    js_file.write_text("""// XSS vulnerability
function updateProfile() {
    const username = document.getElementById('username').value;
    const bio = document.getElementById('bio').value;
    
    // Direct DOM manipulation - VULNERABLE
    document.getElementById('display').innerHTML = "Welcome " + username + "!";
    
    // Another XSS vulnerability
    document.write("<h1>User Bio: " + bio + "</h1>");
    
    // eval() usage - VULNERABLE
    const userInput = document.getElementById('command').value;
    eval(userInput);
    
    // Unsafe assignment
    element.outerHTML = userInput;
}

// Command injection simulation
function runCommand(cmd) {
    // This would be vulnerable if it actually executed commands
    console.log("Would execute: " + cmd);
}
""")
    
    # Vulnerable Python file
    py_file = test_dir / "process.py"
    py_file.write_text("""import os
import subprocess

def process_file(filename):
    # Command injection vulnerability - VULNERABLE
    command = "ls -la " + filename
    os.system(command)
    
    # Another command injection - VULNERABLE
    user_input = request.args.get('file')
    subprocess.run(["cat", user_input], shell=True)
    
    # eval() usage - VULNERABLE
    code = request.args.get('code')
    eval(code)
    
    # Hardcoded secret - VULNERABLE
    SECRET_KEY = "super-secret-key-12345"
    
    # Weak cryptography - VULNERABLE
    import hashlib
    password_hash = hashlib.md5(password.encode()).hexdigest()
    
    # Insecure random - VULNERABLE
    import random
    session_token = str(random.random())
    
    # Path traversal vulnerability - VULNERABLE
    file_path = "/var/www/uploads/" + request.args.get('filename')
    with open(file_path, 'r') as f:
        return f.read()

# Safe function for comparison
def safe_function(user_input):
    # Input validation - SAFE
    if not isinstance(user_input, str) or len(user_input) > 100:
        raise ValueError("Invalid input")
    
    # Safe processing
    return user_input.upper()
""")
    
    # Safe file for comparison
    safe_file = test_dir / "safe.py"
    safe_file.write_text("""# Safe code example
import hashlib
import secrets

def safe_user_auth(username, password):
    # Input validation
    if not username or not password:
        raise ValueError("Username and password required")
    
    if len(username) > 50 or len(password) > 100:
        raise ValueError("Invalid input length")
    
    # Safe password hashing
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    # Secure random token generation
    session_token = secrets.token_hex(32)
    
    return {
        'username': username,
        'session_token': session_token,
        'password_hash': password_hash
    }

def safe_database_query(user_id):
    # Parameterized query - SAFE
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    
    return cursor.fetchall()

# Safe file handling
def safe_file_read(filename):
    # Input validation
    if not filename or '..' in filename or '/' in filename:
        raise ValueError("Invalid filename")
    
    # Restrict to safe directory
    safe_dir = "/var/www/uploads/"
    file_path = safe_dir + filename
    
    if not os.path.exists(file_path):
        raise FileNotFoundError("File not found")
    
    with open(file_path, 'r') as f:
        return f.read()
""")
    
    # Add and commit files
    subprocess.run(["git", "add", "."], cwd=test_dir, check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit with test files"], cwd=test_dir, check=True)
    
    print(f"✅ Test repository created at: {test_dir.absolute()}")
    print("📁 Files created:")
    print("  - login.php (SQL injection, command injection, XSS, hardcoded credentials)")
    print("  - profile.js (XSS, code execution)")
    print("  - process.py (Command injection, hardcoded secrets, weak crypto)")
    print("  - safe.py (Safe code for comparison)")
    
    return str(test_dir.absolute())

if __name__ == "__main__":
    create_test_repository()

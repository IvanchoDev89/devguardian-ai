"""
SBOM Generator - Software Bill of Materials
Generates CycloneDX and SPDX SBOMs for dependencies
"""

import json
import os
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from packaging import version


@dataclass
class Dependency:
    name: str
    version: str
    ecosystem: str  # npm, pip, maven, go, etc.
    license: Optional[str] = None
    description: Optional[str] = None
    repository_url: Optional[str] = None
    homepage_url: Optional[str] = None
    vulnerabilities: List[Dict] = None
    
    def __post_init__(self):
        if self.vulnerabilities is None:
            self.vulnerabilities = []


class SBOMGenerator:
    """Generate Software Bill of Materials"""
    
    # Common package files
    PACKAGE_FILES = {
        "npm": ["package.json", "package-lock.json"],
        "pip": ["requirements.txt", "Pipfile", "Pipfile.lock", "pyproject.toml", "poetry.lock"],
        "maven": ["pom.xml", "build.gradle"],
        "go": ["go.mod", "go.sum"],
        "ruby": ["Gemfile", "Gemfile.lock"],
        "rust": ["Cargo.toml", "Cargo.lock"],
        "dotnet": ["*.csproj", "packages.config"]
    }
    
    def __init__(self):
        self.dependencies: List[Dependency] = []
        
    def detect_ecosystem(self, filepath: str) -> Optional[str]:
        """Detect ecosystem from file path"""
        filename = os.path.basename(filepath).lower()
        
        for ecosystem, files in self.PACKAGE_FILES.items():
            if filename in files:
                return ecosystem
        return None
    
    def parse_requirements_txt(self, content: str) -> List[Dependency]:
        """Parse Python requirements.txt"""
        deps = []
        for line in content.split('\n'):
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('-'):
                continue
            
            # Handle various formats: package, package==version, package>=version
            match = re.match(r'^([a-zA-Z0-9_-]+)([=<>!~]+)?(.+)?$', line)
            if match:
                name = match.group(1)
                version = match.group(3) if match.group(3) else "latest"
                deps.append(Dependency(name=name, version=version, ecosystem="pip"))
                
        return deps
    
    def parse_package_json(self, content: str) -> List[Dependency]:
        """Parse npm package.json"""
        deps = []
        try:
            data = json.loads(content)
            
            # Get all dependency sections
            for key in ['dependencies', 'devDependencies', 'peerDependencies', 'optionalDependencies']:
                if key in data:
                    for name, ver in data[key].items():
                        ver_str = str(ver).lstrip('^~')
                        deps.append(Dependency(
                            name=name,
                            version=ver_str,
                            ecosystem="npm",
                            description=data.get('description'),
                            repository_url=data.get('repository', {}).get('url'),
                            homepage_url=data.get('homepage')
                        ))
        except json.JSONDecodeError:
            pass
        return deps
    
    def parse_go_mod(self, content: str) -> List[Dependency]:
        """Parse Go go.mod"""
        deps = []
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('require ('):
                continue
            if line.startswith(')'):
                break
            if line and not line.startswith('module') and not line.startswith('go '):
                parts = line.split()
                if len(parts) >= 2:
                    name = parts[0]
                    ver = parts[1] if len(parts) > 1 else "latest"
                    deps.append(Dependency(name=name, version=ver, ecosystem="go"))
        return deps
    
    def parse_pom_xml(self, content: str) -> List[Dependency]:
        """Parse Maven pom.xml (simplified)"""
        deps = []
        # Simplified - would need XML parsing for full support
        return deps
    
    def parse_gemfile(self, content: str) -> List[Dependency]:
        """Parse Ruby Gemfile"""
        deps = []
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('gem '):
                match = re.search(r"gem\s+['\"]([^'\"]+)['\"]", line)
                if match:
                    name = match.group(1)
                    ver_match = re.search(r",\s*['\"]([^'\"]+)['\"]", line)
                    ver = ver_match.group(1) if ver_match else "latest"
                    deps.append(Dependency(name=name, version=ver, ecosystem="ruby"))
        return deps
    
    def parse_cargo_toml(self, content: str) -> List[Dependency]:
        """Parse Rust Cargo.toml"""
        deps = []
        in_deps = False
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('[dependencies]') or line.startswith('[dev-dependencies]'):
                in_deps = True
                continue
            if line.startswith('['):
                in_deps = False
            if in_deps and '=' in line:
                parts = line.split('=')
                if len(parts) == 2:
                    name = parts[0].strip()
                    ver = parts[1].strip().strip('"').strip("'")
                    deps.append(Dependency(name=name, version=ver, ecosystem="rust"))
        return deps
    
    def parse_file(self, filepath: str) -> List[Dependency]:
        """Parse a package file based on its type"""
        ecosystem = self.detect_ecosystem(filepath)
        if not ecosystem:
            return []
            
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except:
            return []
        
        if ecosystem == "pip":
            return self.parse_requirements_txt(content)
        elif ecosystem == "npm":
            return self.parse_package_json(content)
        elif ecosystem == "go":
            return self.parse_go_mod(content)
        elif ecosystem == "ruby":
            return self.parse_gemfile(content)
        elif ecosystem == "rust":
            return self.parse_cargo_toml(content)
        
        return []
    
    def scan_directory(self, directory: str) -> List[Dependency]:
        """Scan directory for all dependency files"""
        all_deps = []
        
        for root, dirs, files in os.walk(directory):
            # Skip common non-dependency dirs
            dirs[:] = [d for d in dirs if d not in [
                'node_modules', 'venv', '.venv', '__pycache__', 
                '.git', 'dist', 'build', 'vendor'
            ]]
            
            for file in files:
                filepath = os.path.join(root, file)
                deps = self.parse_file(filepath)
                all_deps.extend(deps)
        
        # Remove duplicates
        seen = set()
        unique_deps = []
        for dep in all_deps:
            key = (dep.name, dep.version, dep.ecosystem)
            if key not in seen:
                seen.add(key)
                unique_deps.append(dep)
        
        self.dependencies = unique_deps
        return unique_deps
    
    def generate_cyclonedx(self) -> Dict:
        """Generate CycloneDX SBOM format"""
        components = []
        for dep in self.dependencies:
            components.append({
                "type": "library",
                "name": dep.name,
                "version": dep.version,
                "description": dep.description,
                "licenses": [{"license": {"id": dep.license}}] if dep.license else None,
                "externalReferences": [
                    {"url": dep.repository_url, "type": "vcs"} if dep.repository_url else None,
                    {"url": dep.homepage_url, "type": "website"} if dep.homepage_url else None
                ]
            })
        
        return {
            "bomFormat": "CycloneDX",
            "specVersion": "1.4",
            "serialNumber": f"urn:uuid:{datetime.utcnow().isoformat()}",
            "version": 1,
            "metadata": {
                "timestamp": datetime.utcnow().isoformat(),
                "tools": [{"name": "DevGuardian AI", "version": "1.0.0"}]
            },
            "components": [c for c in components if c]
        }
    
    def generate_spdx(self) -> Dict:
        """Generate SPDX SBOM format"""
        packages = []
        for i, dep in enumerate(self.dependencies):
            packages.append({
                "SPDXID": f"SPDXRef-Package-{i+1}",
                "name": dep.name,
                "versionInfo": dep.version,
                "downloadLocation": dep.repository_url or "NOASSERTION",
                "filesAnalyzed": False
            })
        
        return {
            "spdxVersion": "SPDX-2.3",
            "dataLicense": "CC0-1.0",
            "SPDXID": "SPDXRef-DOCUMENT",
            "name": "DevGuardian AI SBOM",
            "documentNamespace": f"https://devguardian.ai/sbom/{datetime.utcnow().isoformat()}",
            "creationInfo": {
                "created": datetime.utcnow().isoformat(),
                "creators": ["Tool: DevGuardian AI 1.0.0"]
            },
            "packages": packages
        }
    
    def generate_summary(self) -> Dict:
        """Generate summary statistics"""
        ecosystems = {}
        for dep in self.dependencies:
            ecosystems[dep.ecosystem] = ecosystems.get(dep.ecosystem, 0) + 1
        
        return {
            "total_dependencies": len(self.dependencies),
            "by_ecosystem": ecosystems,
            "timestamp": datetime.utcnow().isoformat()
        }


def create_sbom_generator() -> SBOMGenerator:
    return SBOMGenerator()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        generator = create_sbom_generator()
        deps = generator.scan_directory(sys.argv[1])
        
        print(f"Found {len(deps)} dependencies:")
        for dep in deps:
            print(f"  [{dep.ecosystem}] {dep.name}@{dep.version}")
        
        print("\nCycloneDX:")
        print(json.dumps(generator.generate_cyclonedx(), indent=2))
    else:
        print("Usage: python sbom_generator.py <directory>")

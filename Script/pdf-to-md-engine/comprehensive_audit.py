#!/usr/bin/env python3
"""
🔍 Comprehensive Project Audit & Update Script
Performs complete analysis, verification, and optimization of the PDF-to-MD Engine
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
import subprocess
import importlib.util

class ProjectAuditor:
    """Comprehensive project auditor and optimizer"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.audit_results = {
            "timestamp": datetime.now().isoformat(),
            "structure_analysis": {},
            "dependency_analysis": {},
            "functionality_analysis": {},
            "obsolete_files": [],
            "missing_files": [],
            "recommendations": []
        }
    
    def run_comprehensive_audit(self):
        """Run complete project audit"""
        print("🔍 COMPREHENSIVE PROJECT AUDIT")
        print("=" * 60)
        
        # 1. Project Structure Analysis
        self._analyze_project_structure()
        
        # 2. File Integrity Check
        self._check_file_integrity()
        
        # 3. Dependency Analysis
        self._analyze_dependencies()
        
        # 4. Functionality Verification
        self._verify_functionality()
        
        # 5. Performance Analysis
        self._analyze_performance()
        
        # 6. Documentation Review
        self._review_documentation()
        
        # 7. Generate Report
        self._generate_audit_report()
        
        # 8. Apply Optimizations
        self._apply_optimizations()
        
        return self.audit_results
    
    def _analyze_project_structure(self):
        """Analyze project structure and identify issues"""
        print("\n📁 Analyzing Project Structure...")
        
        # Expected structure
        expected_structure = {
            "core_files": [
                "main.py",
                "run_enhanced.py", 
                "intelligent_install.py",
                "requirements.txt",
                "README.md",
                "CHANGELOG.md",
                "pyproject.toml"
            ],
            "src_files": [
                "src/config.py",
                "src/enhanced_processor.py",
                "src/enhanced_text_extractor.py",
                "src/enhanced_table_detector.py",
                "src/stream_converter.py",
                "src/unified_converter.py",
                "src/pdf_analyzer.py",
                "src/quality_assessor.py",
                "src/utils.py"
            ],
            "directories": [
                "src/",
                "data/",
                "data/input/",
                "data/output/",
                "data/processing/"
            ]
        }
        
        # Check files
        missing_files = []
        present_files = []
        
        for category, files in expected_structure.items():
            if category != "directories":
                for file_path in files:
                    if Path(file_path).exists():
                        present_files.append(file_path)
                    else:
                        missing_files.append(file_path)
        
        # Check directories
        missing_dirs = []
        for dir_path in expected_structure["directories"]:
            if not Path(dir_path).exists():
                missing_dirs.append(dir_path)
        
        self.audit_results["structure_analysis"] = {
            "present_files": present_files,
            "missing_files": missing_files,
            "missing_directories": missing_dirs,
            "total_files": len(present_files) + len(missing_files)
        }
        
        print(f"  ✅ Present files: {len(present_files)}")
        print(f"  ❌ Missing files: {len(missing_files)}")
        print(f"  📁 Missing directories: {len(missing_dirs)}")
    
    def _check_file_integrity(self):
        """Check integrity of existing files"""
        print("\n🔍 Checking File Integrity...")
        
        integrity_issues = []
        
        # Check main.py
        if Path("main.py").exists():
            try:
                with open("main.py", 'r') as f:
                    content = f.read()
                    if "def main()" not in content:
                        integrity_issues.append("main.py: Missing main() function")
                    if "import" not in content:
                        integrity_issues.append("main.py: No imports found")
            except Exception as e:
                integrity_issues.append(f"main.py: Read error - {e}")
        
        # Check requirements.txt
        if Path("requirements.txt").exists():
            try:
                with open("requirements.txt", 'r') as f:
                    content = f.read()
                    if len(content.strip()) < 50:
                        integrity_issues.append("requirements.txt: Suspiciously short")
            except Exception as e:
                integrity_issues.append(f"requirements.txt: Read error - {e}")
        
        # Check src files
        src_files = list(Path("src").glob("*.py")) if Path("src").exists() else []
        for src_file in src_files:
            try:
                with open(src_file, 'r') as f:
                    content = f.read()
                    if len(content.strip()) < 100:
                        integrity_issues.append(f"{src_file}: Suspiciously short")
            except Exception as e:
                integrity_issues.append(f"{src_file}: Read error - {e}")
        
        self.audit_results["integrity_issues"] = integrity_issues
        print(f"  🔍 Integrity issues found: {len(integrity_issues)}")
    
    def _analyze_dependencies(self):
        """Analyze project dependencies"""
        print("\n📦 Analyzing Dependencies...")
        
        # Read requirements.txt
        requirements = []
        if Path("requirements.txt").exists():
            with open("requirements.txt", 'r') as f:
                requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        # Test imports
        available_deps = []
        missing_deps = []
        
        critical_deps = [
            ("PyMuPDF", "fitz"),
            ("loguru", "loguru"),
            ("Pillow", "PIL"),
            ("numpy", "numpy"),
            ("pydantic", "pydantic"),
            ("jinja2", "jinja2"),
            ("tqdm", "tqdm"),
            ("psutil", "psutil")
        ]
        
        for dep_name, import_name in critical_deps:
            try:
                spec = importlib.util.find_spec(import_name)
                if spec is not None:
                    available_deps.append(dep_name)
                else:
                    missing_deps.append(dep_name)
            except ImportError:
                missing_deps.append(dep_name)
        
        self.audit_results["dependency_analysis"] = {
            "total_requirements": len(requirements),
            "available_dependencies": available_deps,
            "missing_dependencies": missing_deps,
            "dependency_health": len(available_deps) / len(critical_deps) if critical_deps else 0
        }
        
        print(f"  ✅ Available: {len(available_deps)}")
        print(f"  ❌ Missing: {len(missing_deps)}")
    
    def _verify_functionality(self):
        """Verify core functionality"""
        print("\n⚙️ Verifying Functionality...")
        
        functionality_status = {}
        
        # Test core imports
        try:
            if Path("src/config.py").exists():
                spec = importlib.util.spec_from_file_location("config", "src/config.py")
                config_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(config_module)
                functionality_status["config"] = "working"
            else:
                functionality_status["config"] = "missing"
        except Exception as e:
            functionality_status["config"] = f"error: {e}"
        
        # Test enhanced processor
        try:
            if Path("src/enhanced_processor.py").exists():
                with open("src/enhanced_processor.py", 'r') as f:
                    content = f.read()
                    if "def process_pdf" in content:
                        functionality_status["enhanced_processor"] = "working"
                    else:
                        functionality_status["enhanced_processor"] = "incomplete"
            else:
                functionality_status["enhanced_processor"] = "missing"
        except Exception as e:
            functionality_status["enhanced_processor"] = f"error: {e}"
        
        self.audit_results["functionality_analysis"] = functionality_status
        
        working_count = sum(1 for status in functionality_status.values() if status == "working")
        print(f"  ✅ Working components: {working_count}/{len(functionality_status)}")
    
    def _analyze_performance(self):
        """Analyze performance characteristics"""
        print("\n⚡ Analyzing Performance...")
        
        performance_metrics = {
            "file_count": len(list(Path(".").rglob("*.py"))),
            "total_size_mb": sum(f.stat().st_size for f in Path(".").rglob("*") if f.is_file()) / (1024*1024),
            "src_files": len(list(Path("src").glob("*.py"))) if Path("src").exists() else 0
        }
        
        # Check for performance optimizations
        optimizations = []
        if Path("src/enhanced_processor.py").exists():
            with open("src/enhanced_processor.py", 'r') as f:
                content = f.read()
                if "multiprocessing" in content or "threading" in content:
                    optimizations.append("parallel_processing")
                if "cache" in content.lower():
                    optimizations.append("caching")
                if "gpu" in content.lower():
                    optimizations.append("gpu_acceleration")
        
        performance_metrics["optimizations"] = optimizations
        self.audit_results["performance_analysis"] = performance_metrics
        
        print(f"  📊 Total files: {performance_metrics['file_count']}")
        print(f"  💾 Project size: {performance_metrics['total_size_mb']:.1f}MB")
        print(f"  ⚡ Optimizations: {len(optimizations)}")
    
    def _review_documentation(self):
        """Review documentation completeness"""
        print("\n📚 Reviewing Documentation...")
        
        doc_files = ["README.md", "CHANGELOG.md", "TROUBLESHOOTING.md"]
        doc_status = {}
        
        for doc_file in doc_files:
            if Path(doc_file).exists():
                with open(doc_file, 'r') as f:
                    content = f.read()
                    word_count = len(content.split())
                    if word_count > 100:
                        doc_status[doc_file] = "comprehensive"
                    elif word_count > 50:
                        doc_status[doc_file] = "basic"
                    else:
                        doc_status[doc_file] = "minimal"
            else:
                doc_status[doc_file] = "missing"
        
        self.audit_results["documentation_analysis"] = doc_status
        
        comprehensive_count = sum(1 for status in doc_status.values() if status == "comprehensive")
        print(f"  📖 Comprehensive docs: {comprehensive_count}/{len(doc_files)}")
    
    def _generate_audit_report(self):
        """Generate comprehensive audit report"""
        print("\n📋 Generating Audit Report...")
        
        # Calculate overall health score
        structure_score = len(self.audit_results["structure_analysis"]["present_files"]) / self.audit_results["structure_analysis"]["total_files"]
        dependency_score = self.audit_results["dependency_analysis"]["dependency_health"]
        functionality_score = sum(1 for status in self.audit_results["functionality_analysis"].values() if status == "working") / len(self.audit_results["functionality_analysis"])
        
        overall_health = (structure_score + dependency_score + functionality_score) / 3
        
        # Generate recommendations
        recommendations = []
        
        if self.audit_results["structure_analysis"]["missing_files"]:
            recommendations.append("Create missing core files")
        
        if self.audit_results["dependency_analysis"]["missing_dependencies"]:
            recommendations.append("Install missing dependencies")
        
        if overall_health < 0.8:
            recommendations.append("Run intelligent_install.py for automated setup")
        
        if len(self.audit_results["performance_analysis"]["optimizations"]) < 2:
            recommendations.append("Implement performance optimizations")
        
        self.audit_results["overall_health"] = overall_health
        self.audit_results["recommendations"] = recommendations
        
        # Save report
        with open("audit_report.json", "w") as f:
            json.dump(self.audit_results, f, indent=2)
        
        print(f"  📊 Overall Health: {overall_health:.1%}")
        print(f"  💡 Recommendations: {len(recommendations)}")
    
    def _apply_optimizations(self):
        """Apply automatic optimizations"""
        print("\n🔧 Applying Optimizations...")
        
        optimizations_applied = []
        
        # Create missing directories
        for missing_dir in self.audit_results["structure_analysis"]["missing_directories"]:
            Path(missing_dir).mkdir(parents=True, exist_ok=True)
            optimizations_applied.append(f"Created directory: {missing_dir}")
        
        # Create basic .gitignore if missing
        if not Path(".gitignore").exists():
            gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Project specific
data/processing/
*.log
audit_report.json
intelligent_config.json
"""
            with open(".gitignore", "w") as f:
                f.write(gitignore_content)
            optimizations_applied.append("Created .gitignore")
        
        # Update verification script
        self._update_verification_script()
        optimizations_applied.append("Updated verification script")
        
        print(f"  ✅ Applied {len(optimizations_applied)} optimizations")
        return optimizations_applied
    
    def _update_verification_script(self):
        """Update the verification script with enhanced checks"""
        
        enhanced_verify_content = '''#!/usr/bin/env python3
"""
Enhanced Project Verification Script - Updated by Comprehensive Audit
"""
import os
import sys
import json
from pathlib import Path
import importlib.util

def check_project_health():
    """Check overall project health"""
    print("🔍 Enhanced Project Health Check")
    print("=" * 50)
    
    # Load audit report if available
    audit_data = {}
    if Path("audit_report.json").exists():
        with open("audit_report.json", 'r') as f:
            audit_data = json.load(f)
        
        print(f"📊 Last Audit: {audit_data.get('timestamp', 'Unknown')}")
        print(f"🎯 Health Score: {audit_data.get('overall_health', 0):.1%}")
    
    # Quick dependency check
    critical_deps = [
        ("PyMuPDF", "fitz"),
        ("loguru", "loguru"), 
        ("Pillow", "PIL"),
        ("numpy", "numpy")
    ]
    
    available = 0
    for name, module in critical_deps:
        try:
            spec = importlib.util.find_spec(module)
            if spec is not None:
                available += 1
                print(f"  ✅ {name}")
            else:
                print(f"  ❌ {name}")
        except:
            print(f"  ❌ {name}")
    
    print(f"\\n📦 Dependencies: {available}/{len(critical_deps)} available")
    
    # Quick functionality test
    if Path("src/config.py").exists():
        print("  ✅ Core configuration available")
    else:
        print("  ❌ Core configuration missing")
    
    if Path("main.py").exists():
        print("  ✅ Main entry point available")
    else:
        print("  ❌ Main entry point missing")
    
    # Recommendations
    if available < len(critical_deps):
        print("\\n💡 Run: python intelligent_install.py")
    
    if available == len(critical_deps):
        print("\\n🚀 Ready to use: python main.py")
    
    return available == len(critical_deps)

if __name__ == "__main__":
    success = check_project_health()
    sys.exit(0 if success else 1)
'''
        
        with open("verify_project.py", "w") as f:
            f.write(enhanced_verify_content)

def main():
    """Main audit function"""
    auditor = ProjectAuditor()
    results = auditor.run_comprehensive_audit()
    
    print("\n" + "=" * 60)
    print("🎯 AUDIT COMPLETE")
    print("=" * 60)
    
    print(f"📊 Overall Health: {results['overall_health']:.1%}")
    print(f"📁 Structure Issues: {len(results['structure_analysis']['missing_files'])}")
    print(f"📦 Missing Dependencies: {len(results['dependency_analysis']['missing_dependencies'])}")
    print(f"💡 Recommendations: {len(results['recommendations'])}")
    
    if results['recommendations']:
        print("\n🔧 RECOMMENDED ACTIONS:")
        for i, rec in enumerate(results['recommendations'], 1):
            print(f"  {i}. {rec}")
    
    # Show next steps
    print("\n🚀 NEXT STEPS:")
    if results['overall_health'] < 0.5:
        print("  1. Run: python intelligent_install.py")
        print("  2. Install dependencies: pip install -r requirements.txt")
    elif results['overall_health'] < 0.8:
        print("  1. Address missing dependencies")
        print("  2. Run: python verify_project.py")
    else:
        print("  1. Project is ready!")
        print("  2. Run: python main.py")
    
    return 0 if results['overall_health'] > 0.7 else 1

if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""
Enhanced Project Verification Script - Checks venv dependencies
"""
import os
import sys
import json
import subprocess
from pathlib import Path

def check_project_health():
    """Check project health with venv dependency verification"""
    print("🔍 Enhanced Project Health Check (venv-aware)")
    print("=" * 55)
    
    # Load audit report
    if Path("audit_report.json").exists():
        with open("audit_report.json", 'r') as f:
            audit_data = json.load(f)
        print(f"📊 Last Audit: {audit_data.get('timestamp', 'Unknown')[:19]}")
        print(f"🎯 Health Score: {audit_data.get('overall_health', 0):.1%}")
    
    # Check venv dependencies
    critical_deps = [("PyMuPDF", "fitz"), ("loguru", "loguru"), ("Pillow", "PIL"), ("numpy", "numpy")]
    
    if Path("venv").exists():
        python_cmd = "venv\\Scripts\\python" if os.name == 'nt' else "venv/bin/python"
        available = 0
        
        for name, module in critical_deps:
            try:
                result = subprocess.run(f'{python_cmd} -c "import {module}"', 
                                      shell=True, capture_output=True, timeout=5)
                if result.returncode == 0:
                    available += 1
                    print(f"  ✅ {name} (venv)")
                else:
                    print(f"  ❌ {name} (venv)")
            except:
                print(f"  ❌ {name} (venv)")
    else:
        print("  ⚠️  No venv found - checking system")
        available = 0
        import importlib.util
        for name, module in critical_deps:
            try:
                if importlib.util.find_spec(module):
                    available += 1
                    print(f"  ✅ {name} (system)")
                else:
                    print(f"  ❌ {name}")
            except:
                print(f"  ❌ {name}")
    
    print(f"\n📦 Dependencies: {available}/{len(critical_deps)} available")
    
    # Check core files
    if Path("main.py").exists() and Path("src/config.py").exists():
        print("  ✅ Core files present")
    else:
        print("  ❌ Core files missing")
    
    # Recommendations
    if available < len(critical_deps):
        print("\n💡 Run: python intelligent_install.py")
    else:
        print("\n🚀 Ready: python main.py")
    
    return available >= len(critical_deps) * 0.75

if __name__ == "__main__":
    sys.exit(0 if check_project_health() else 1)

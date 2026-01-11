#!/usr/bin/env python3
"""
Project verification script - checks current structure and dependencies
"""
import os
import sys
from pathlib import Path

def check_project_structure():
    """Verify current project structure"""
    print("🔍 PDF to Markdown Engine v2.0 - Project Structure")
    print("=" * 60)
    
    # Core files that should exist
    required_files = [
        "main.py",
        "run_enhanced.py", 
        "test_enhanced_extraction.py",
        "requirements.txt",
        "README.md",
        "TROUBLESHOOTING.md",
        "pyproject.toml",
        "src/config.py",
        "src/enhanced_processor.py",
        "src/enhanced_text_extractor.py",
        "src/utils.py",
        "src/templates/chapter.md.j2"
    ]
    
    # Files that should be removed
    obsolete_files = [
        "src/processor.py",
        "src/text_extractor.py",
        "test_extraction.sh",
        "test_text_layer.py", 
        "run_with_memory_fix.py",
        "requirements_updated.txt",
        "fix_gcc.sh",
        "setup.sh",
        "enhanced_image_extractor.py",
        ".venv_orig/"
    ]
    
    print("✅ Required Files:")
    missing_files = []
    for file in required_files:
        if Path(file).exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} (MISSING)")
            missing_files.append(file)
    
    print("\n🗑️  Obsolete Files (should be removed):")
    remaining_obsolete = []
    for file in obsolete_files:
        if Path(file).exists():
            print(f"  ✗ {file} (STILL EXISTS)")
            remaining_obsolete.append(file)
        else:
            print(f"  ✓ {file} (removed)")
    
    print("\n📊 Summary:")
    if not missing_files and not remaining_obsolete:
        print("  🎉 Project structure is clean and complete!")
    else:
        if missing_files:
            print(f"  ⚠️  Missing {len(missing_files)} required files")
        if remaining_obsolete:
            print(f"  ⚠️  {len(remaining_obsolete)} obsolete files still present")
    
    return len(missing_files) == 0 and len(remaining_obsolete) == 0

def check_dependencies():
    """Check if key dependencies can be imported"""
    print("\n🔧 Dependency Check:")
    print("=" * 30)
    
    dependencies = [
        ("docling", "docling"),
        ("PyMuPDF", "fitz"),
        ("pdfplumber", "pdfplumber"),
        ("loguru", "loguru"),
        ("pydantic", "pydantic"),
        ("jinja2", "jinja2"),
        ("tqdm", "tqdm"),
        ("psutil", "psutil"),
        ("torch", "torch"),
        ("PIL", "PIL"),
        ("numpy", "numpy")
    ]
    
    optional_deps = [
        ("EasyOCR", "easyocr"),
        ("Tesseract", "pytesseract"),
        ("OpenCV", "cv2"),
        ("chardet", "chardet"),
        ("ftfy", "ftfy")
    ]
    
    print("Core Dependencies:")
    missing_core = []
    for name, module in dependencies:
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} (missing)")
            missing_core.append(name)
    
    print("\nOptional Dependencies:")
    for name, module in optional_deps:
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  - {name} (optional)")
    
    if missing_core:
        print(f"\n⚠️  Missing {len(missing_core)} core dependencies")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All core dependencies available!")
        return True

def check_enhanced_features():
    """Test enhanced features"""
    print("\n🚀 Enhanced Features Check:")
    print("=" * 35)
    
    try:
        # Test enhanced text extractor
        from src.enhanced_text_extractor import extract_pdf_text_hybrid, clean_extracted_text
        print("  ✓ Enhanced text extraction")
        
        # Test text cleaning
        test_text = 'This is a ﬁle with "smart quotes"'
        cleaned = clean_extracted_text(test_text)
        if "fi" in cleaned and "smart quotes" in cleaned:
            print("  ✓ Text cleaning and encoding fixes")
        else:
            print("  ⚠️  Text cleaning may have issues")
        
        # Test enhanced processor
        from src.enhanced_processor import detect_chapter_structure, EnhancedOCREngine
        print("  ✓ Enhanced chapter detection")
        print("  ✓ Enhanced OCR engine")
        
        return True
        
    except ImportError as e:
        print(f"  ✗ Enhanced features not available: {e}")
        return False

def main():
    """Main verification function"""
    print("PDF to Markdown Engine v2.0 - Project Verification")
    print("=" * 60)
    
    structure_ok = check_project_structure()
    deps_ok = check_dependencies() 
    features_ok = check_enhanced_features()
    
    print("\n" + "=" * 60)
    print("🎯 Overall Status:")
    
    if structure_ok and deps_ok and features_ok:
        print("  🎉 Project is ready to use!")
        print("  Run: python run_enhanced.py")
        return 0
    else:
        print("  ⚠️  Issues found - check messages above")
        if not structure_ok:
            print("     - Fix project structure issues")
        if not deps_ok:
            print("     - Install missing dependencies")
        if not features_ok:
            print("     - Check enhanced features")
        return 1

if __name__ == "__main__":
    sys.exit(main())
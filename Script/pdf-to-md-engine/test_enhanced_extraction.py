#!/usr/bin/env python3
"""
Test script for enhanced PDF text extraction and chapter detection
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from src.enhanced_text_extractor import (
    extract_pdf_text_hybrid,
    extract_pdf_outline_enhanced,
    should_use_ocr_enhancement,
    detect_pdf_text_quality
)

def test_enhanced_extraction():
    """Test the enhanced text extraction on the Red Hand of Doom PDF"""
    pdf_path = Path("data/input/Adventure-RedHandofDoom06-12-ocr.pdf")
    
    if not pdf_path.exists():
        print(f"❌ PDF not found: {pdf_path}")
        return
    
    print("🔍 Testing Enhanced PDF Text Extraction")
    print("=" * 50)
    
    # Test 1: Text quality analysis
    print("\n1. Analyzing text quality...")
    analysis = detect_pdf_text_quality(pdf_path)
    
    print(f"   📊 Total pages: {analysis.get('total_pages', 0)}")
    print(f"   📝 Total characters: {analysis.get('total_chars', 0):,}")
    print(f"   ✨ Readable characters: {analysis.get('readable_chars', 0):,}")
    print(f"   🎯 Text quality: {analysis.get('text_quality', 0):.2%}")
    print(f"   ⚠️  Encoding issues: {analysis.get('encoding_issues', 0)} pages")
    print(f"   🔧 Needs OCR enhancement: {analysis.get('needs_ocr_enhancement', False)}")
    
    # Test 2: Enhanced text extraction
    print("\n2. Extracting text with hybrid method...")
    text, text_analysis = extract_pdf_text_hybrid(pdf_path)
    
    print(f"   📄 Extracted text length: {len(text):,} characters")
    print(f"   🔧 Extraction method: {text_analysis.get('extraction_method', 'unknown')}")
    
    # Show sample of extracted text
    if text:
        sample = text[:500].replace('\n', ' ')
        print(f"   📖 Sample text: {sample}...")
    
    # Test 3: Outline extraction
    print("\n3. Extracting PDF outline...")
    outline = extract_pdf_outline_enhanced(pdf_path)
    
    if outline:
        print(f"   📑 Found {len(outline)} outline entries:")
        for i, entry in enumerate(outline[:10]):  # Show first 10
            level = "  " * (entry['level'] - 1)
            print(f"      {level}• {entry['title']} (page {entry['page']})")
        if len(outline) > 10:
            print(f"      ... and {len(outline) - 10} more entries")
    else:
        print("   📑 No outline found in PDF")
    
    # Test 4: OCR enhancement check
    print("\n4. Checking OCR enhancement needs...")
    needs_ocr = should_use_ocr_enhancement(pdf_path)
    print(f"   🔧 OCR enhancement recommended: {needs_ocr}")
    
    # Test 5: Chapter detection preview
    print("\n5. Chapter detection preview...")
    if text:
        # Look for chapter patterns
        import re
        
        patterns = [
            r'^(# .+)$',
            r'^([A-Z][A-Z ]{10,})$',
            r'^(CHAPTER \d+.*)$',
            r'^(Chapter \d+.*)$',
        ]
        
        found_chapters = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.MULTILINE)
            if matches:
                found_chapters.extend(matches[:5])  # First 5 matches
                break
        
        if found_chapters:
            print(f"   📚 Found potential chapters:")
            for chapter in found_chapters:
                print(f"      • {chapter}")
        else:
            print("   📚 No clear chapter structure detected")
    
    print("\n✅ Enhanced extraction test completed!")
    print(f"📊 Summary: {analysis.get('total_chars', 0):,} chars, "
          f"{analysis.get('text_quality', 0):.1%} quality, "
          f"{len(outline)} outline entries")

if __name__ == "__main__":
    test_enhanced_extraction()
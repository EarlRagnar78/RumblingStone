#!/usr/bin/env python3
"""
Test layout-preserving PDF extraction
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from src.layout_processor import extract_pdf_with_layout

def test_layout_extraction():
    """Test layout preservation on Red Hand of Doom PDF"""
    pdf_path = Path("data/input/Adventure-RedHandofDoom06-12-ocr.pdf")
    
    if not pdf_path.exists():
        print(f"❌ PDF not found: {pdf_path}")
        return
    
    print("🔍 Testing Layout-Preserving Extraction")
    print("=" * 50)
    
    # Extract with layout preservation
    layout_text = extract_pdf_with_layout(pdf_path)
    
    if layout_text:
        print(f"✅ Extracted {len(layout_text):,} characters with layout preservation")
        
        # Show sample
        sample = layout_text[:1000]
        print(f"\n📖 Sample output:\n{sample}...")
        
        # Count tables
        table_count = layout_text.count('| --- |')
        print(f"\n📊 Found {table_count} tables")
        
        # Count headers
        header_count = layout_text.count('# ')
        print(f"📑 Found {header_count} headers")
        
    else:
        print("❌ Layout extraction failed")

if __name__ == "__main__":
    test_layout_extraction()
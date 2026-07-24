#!/usr/bin/env python3
"""
Test PDF Analyzer - Verify enhanced PDF analysis capabilities
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from src.pdf_analyzer import analyze_pdf_characteristics, get_extraction_strategy

def test_pdf_analyzer():
    """Test the PDF analyzer on available PDFs"""
    input_dir = Path("data/input")
    
    if not input_dir.exists():
        print("❌ Input directory not found: data/input")
        return
    
    pdfs = list(input_dir.glob("*.pdf"))
    if not pdfs:
        print("❌ No PDFs found in data/input")
        return
    
    print("🔍 PDF Analysis Test")
    print("=" * 60)
    
    for pdf_path in pdfs:
        print(f"\n📄 Analyzing: {pdf_path.name}")
        print("-" * 40)
        
        try:
            # Analyze PDF characteristics
            characteristics = analyze_pdf_characteristics(pdf_path)
            strategy = get_extraction_strategy(characteristics)
            
            # Display results
            print(f"📋 PDF Information:")
            print(f"   Version: {characteristics.version}")
            print(f"   Pages: {characteristics.page_count}")
            print(f"   Standard: {characteristics.pdf_standard}")
            print(f"   Creation: {characteristics.creation_method}")
            
            print(f"\n🔍 Content Analysis:")
            print(f"   Text Layer: {'✅' if characteristics.has_text_layer else '❌'}")
            print(f"   Scanned: {'✅' if characteristics.is_scanned else '❌'}")
            print(f"   Tagged: {'✅' if characteristics.is_tagged else '❌'}")
            print(f"   Bookmarks: {'✅' if characteristics.has_bookmarks else '❌'}")
            print(f"   Tables: {characteristics.table_count}")
            print(f"   Fonts: {characteristics.font_count}")
            
            print(f"\n📊 Coverage Analysis:")
            print(f"   Text Coverage: {characteristics.text_coverage:.1f}%")
            print(f"   Image Coverage: {characteristics.image_coverage:.1f}%")
            print(f"   Color Space: {characteristics.color_space}")
            
            print(f"\n🎯 Extraction Strategy:")
            print(f"   Optimal Method: {characteristics.optimal_extraction_method}")
            print(f"   Confidence: {characteristics.extraction_confidence:.2f}")
            print(f"   Expected Quality: {strategy['expected_quality']}")
            print(f"   Processing Time: {strategy['processing_time_estimate']}")
            print(f"   Resource Needs: {strategy['resource_requirements']}")
            
            if strategy['fallback_methods']:
                print(f"   Fallback Methods: {', '.join(strategy['fallback_methods'])}")
            
            if strategy['preprocessing_steps']:
                print(f"   Preprocessing: {', '.join(strategy['preprocessing_steps'])}")
            
            print(f"\n✅ Analysis completed successfully!")
            
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
    
    print(f"\n🎉 PDF Analysis test completed!")

if __name__ == "__main__":
    test_pdf_analyzer()
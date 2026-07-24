#!/bin/bash

# Test the enhanced PDF to Markdown engine with graphical image detection
# Usage: ./test_enhanced_engine.sh

echo "🔍 Testing Enhanced PDF-to-Markdown Engine with Graphical Image Detection"
echo "========================================================================="

# Check if input directory exists
if [ ! -d "./data/input" ]; then
    echo "📁 Creating input directory..."
    mkdir -p ./data/input
fi

# Check if output directory exists
if [ ! -d "./data/output" ]; then
    echo "📁 Creating output directory..."
    mkdir -p ./data/output
fi

# Check for PDF files in input directory
PDF_COUNT=$(find ./data/input -name "*.pdf" | wc -l)

if [ $PDF_COUNT -eq 0 ]; then
    echo "⚠️  No PDF files found in ./data/input/"
    echo "   Please copy your PDF files to ./data/input/ and run again"
    echo ""
    echo "   Example:"
    echo "   cp '../Pdf_To_extract/Adventure - Red Hand of Doom 06-12-ocr.pdf' ./data/input/"
    exit 1
fi

echo "📄 Found $PDF_COUNT PDF file(s) in input directory"
echo ""

# Install dependencies if needed
echo "🔧 Checking dependencies..."
if ! python3 -c "import cv2, easyocr, pytesseract" 2>/dev/null; then
    echo "📦 Installing missing dependencies..."
    pip3 install -r requirements_updated.txt
fi

echo ""
echo "🚀 Starting enhanced processing..."
echo "   - Graphical image detection enabled"
echo "   - OCR text extraction enabled"
echo "   - Adaptive resource management enabled"
echo ""

# Run the main processor
python3 main.py

echo ""
echo "✅ Processing complete!"
echo "📁 Check ./data/output/ for results"
echo ""
echo "Enhanced features used:"
echo "  ✓ Computer vision image filtering (creatures vs text)"
echo "  ✓ OCR text extraction from images"
echo "  ✓ Intelligent resource management"
echo "  ✓ Markdown integration with OCR content"
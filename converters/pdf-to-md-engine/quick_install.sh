#!/bin/bash
# Quick Install Script for PDF-to-MD Engine v2.0

echo "🚀 PDF-to-MD Engine v2.0 - Quick Install"
echo "========================================"

# Install missing dependencies in current venv
echo "📦 Installing missing dependencies..."

pip install --upgrade pip
pip install cryptography>=3.0.0
pip install pdfminer.six>=20220319
pip install -r requirements.txt

echo ""
echo "✅ Dependencies installed!"
echo ""
echo "🧪 Testing installation..."

# Test critical imports
python -c "
try:
    import cryptography
    print('✅ cryptography')
except ImportError as e:
    print('❌ cryptography:', e)

try:
    import pdfplumber
    print('✅ pdfplumber')
except ImportError as e:
    print('❌ pdfplumber:', e)

try:
    import fitz
    print('✅ PyMuPDF')
except ImportError as e:
    print('❌ PyMuPDF:', e)

try:
    from src.enhanced_processor import process_pdf
    print('✅ enhanced_processor')
except ImportError as e:
    print('❌ enhanced_processor:', e)
"

echo ""
echo "🎯 Ready to use!"
echo "Run: python main.py"
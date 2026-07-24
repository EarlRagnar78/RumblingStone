#!/usr/bin/env python3
"""
Enhanced PDF to Markdown conversion with better text extraction
"""
import sys
from pathlib import Path
from loguru import logger

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from src.enhanced_processor import process_pdf
from src.config import settings

def main():
    """Run enhanced PDF processing"""
    logger.add(sys.stderr, format="{time} {level} {message}", level=settings.LOG_LEVEL)
    
    pdfs = list(settings.INPUT_DIR.glob("*.pdf"))
    
    if not pdfs:
        logger.warning(f"No PDFs found in {settings.INPUT_DIR}")
        return

    logger.info(f"🚀 Enhanced PDF processing starting...")
    logger.info(f"📁 Found {len(pdfs)} PDFs to process")
    logger.info(f"🔧 Features: Enhanced text extraction, OCR enhancement, better chapter detection")
    
    for pdf in pdfs:
        try:
            logger.info(f"📄 Processing: {pdf.name}")
            process_pdf(pdf)
            logger.success(f"✅ Completed: {pdf.name}")
        except Exception as e:
            logger.error(f"❌ Failed to process {pdf.name}: {e}")
            # Continue to next file for robustness

    logger.success("🎉 Enhanced processing completed!")

if __name__ == "__main__":
    main()
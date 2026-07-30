#!/usr/bin/env python3
"""
Debug version with detailed logging to file
"""
import sys
from pathlib import Path
from loguru import logger

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from src.enhanced_processor import process_pdf
from src.config import settings

def main():
    """Run with debug logging to file"""
    # Setup file logging with DEBUG level
    log_file = Path("debug.log")
    logger.add(log_file, format="{time} {level} {message}", level="DEBUG", rotation="10 MB")
    logger.add(sys.stderr, format="{time} {level} {message}", level="INFO")
    
    logger.info("🐛 Debug mode enabled - logging to debug.log")
    
    pdfs = list(settings.INPUT_DIR.glob("*.pdf"))
    
    if not pdfs:
        logger.warning(f"No PDFs found in {settings.INPUT_DIR}")
        return

    logger.info(f"🚀 Debug PDF processing starting...")
    logger.debug(f"Settings: {settings}")
    
    for pdf in pdfs:
        try:
            logger.info(f"📄 Processing: {pdf.name}")
            logger.debug(f"PDF path: {pdf}")
            process_pdf(pdf)
            logger.success(f"✅ Completed: {pdf.name}")
        except Exception as e:
            logger.error(f"❌ Failed to process {pdf.name}: {e}")
            logger.debug(f"Full error traceback:", exc_info=True)

    logger.info(f"📋 Debug log saved to: {log_file.absolute()}")

if __name__ == "__main__":
    main()
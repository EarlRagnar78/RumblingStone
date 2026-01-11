import sys
from loguru import logger
from src.config import settings
from src.enhanced_processor import process_pdf

def main():
    logger.add(sys.stderr, format="{time} {level} {message}", level=settings.LOG_LEVEL)
    
    pdfs = list(settings.INPUT_DIR.glob("*.pdf"))
    
    if not pdfs:
        logger.warning(f"No PDFs found in {settings.INPUT_DIR}")
        return

    logger.info(f"Found {len(pdfs)} PDFs to process.")
    
    for pdf in pdfs:
        try:
            process_pdf(pdf)
        except Exception as e:
            logger.error(f"Failed to process {pdf.name}: {e}")
            # We continue to the next file (Robustness)

if __name__ == "__main__":
    main()
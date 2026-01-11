import sys
import time
from loguru import logger
from src.config import settings
from src.enhanced_processor import process_pdf
from src.utils import clean_filename

def main():
    logger.add(sys.stderr, format="{time} {level} {message}", level=settings.LOG_LEVEL)
    
    pdfs = list(settings.INPUT_DIR.glob("*.pdf"))
    
    if not pdfs:
        logger.warning(f"No PDFs found in {settings.INPUT_DIR}")
        return

    logger.info(f"🚀 PDF-to-MD Engine v2.1 with Quality Assessment")
    logger.info(f"Found {len(pdfs)} PDFs to process.")
    
    # Track processing results
    results = []
    
    for pdf in pdfs:
        try:
            logger.info(f"📄 Processing: {pdf.name}")
            start_time = time.time()
            process_pdf(pdf)
            processing_time = time.time() - start_time
            
            # Read results from receipt
            receipt_file = settings.OUTPUT_DIR / clean_filename(pdf.stem) / ".receipt"
            if receipt_file.exists():
                import json
                metadata = json.loads(receipt_file.read_text())
                results.append({
                    'file': pdf.name,
                    'method': metadata.get('extraction_strategy', {}).get('method_used', 'unknown'),
                    'quality': metadata.get('quality_metrics', {}).get('overall_score', 0.0),
                    'time': processing_time,
                    'chapters': metadata.get('chapters_detected', 0)
                })
            else:
                results.append({
                    'file': pdf.name,
                    'method': 'unknown',
                    'quality': 0.0,
                    'time': processing_time,
                    'chapters': 0
                })
            
            logger.success(f"✅ Completed: {pdf.name}")
        except Exception as e:
            logger.error(f"❌ Failed to process {pdf.name}: {e}")
            results.append({
                'file': pdf.name,
                'method': 'failed',
                'quality': 0.0,
                'time': 0.0,
                'chapters': 0
            })
    
    # Print summary
    logger.info("\n" + "="*60)
    logger.info("📊 PROCESSING SUMMARY")
    logger.info("="*60)
    
    for result in results:
        quality_label = "EXCELLENT" if result['quality'] > 0.85 else "GOOD" if result['quality'] > 0.75 else "ACCEPTABLE" if result['quality'] > 0.5 else "POOR"
        logger.info(f"📄 {result['file']}:")
        logger.info(f"   Method: {result['method']}, Quality: {result['quality']:.2f} ({quality_label})")
        logger.info(f"   Chapters: {result['chapters']}, Time: {result['time']:.1f}s")
    
    # Overall stats
    successful = [r for r in results if r['method'] != 'failed']
    if successful:
        avg_quality = sum(r['quality'] for r in successful) / len(successful)
        total_time = sum(r['time'] for r in results)
        total_chapters = sum(r['chapters'] for r in successful)
        
        logger.info(f"\n🎯 Overall: {len(successful)}/{len(results)} successful")
        logger.info(f"📈 Average Quality: {avg_quality:.2f}")
        logger.info(f"⏱️ Total Time: {total_time:.1f}s")
        logger.info(f"📚 Total Chapters: {total_chapters}")

if __name__ == "__main__":
    main()
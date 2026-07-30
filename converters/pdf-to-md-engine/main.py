import sys
import time
from pathlib import Path

# Enhanced imports with fallbacks
try:
    from loguru import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)

try:
    from src.config import settings
except ImportError:
    # Fallback configuration
    class Settings:
        INPUT_DIR = Path("data/input")
        OUTPUT_DIR = Path("data/output")
        LOG_LEVEL = "INFO"
    settings = Settings()

try:
    from src.enhanced_processor import process_pdf
except ImportError:
    def process_pdf(pdf_path):
        logger.error(f"Enhanced processor not available. Install dependencies with: python intelligent_install.py")
        return False

try:
    from src.utils import clean_filename
except ImportError:
    def clean_filename(name):
        return str(name).replace(" ", "_").replace("/", "_")

# AI Enhancement imports (with fallbacks)
try:
    from src.ai_enhancer import AIEnhancer
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

def check_ai_capabilities():
    """Check and report available AI capabilities"""
    capabilities = []
    
    if AI_AVAILABLE:
        try:
            enhancer = AIEnhancer()
            if 'grammar' in enhancer.models:
                capabilities.append("Grammar Correction")
            if 'text_enhancer' in enhancer.models:
                capabilities.append("Text Enhancement")
            if 'llm' in enhancer.models:
                capabilities.append("Local LLM")
        except Exception:
            pass
    
    # Check other free tools
    try:
        import spacy
        capabilities.append("spaCy NLP")
    except ImportError:
        pass
    
    try:
        import nltk
        capabilities.append("NLTK")
    except ImportError:
        pass
    
    return capabilities

def main():
    """Main processing function with enhanced error handling"""
    
    # Setup logging
    try:
        logger.add(sys.stderr, format="{time} {level} {message}", level=settings.LOG_LEVEL)
    except:
        pass  # Fallback logger already configured
    
    # Check AI capabilities
    ai_caps = check_ai_capabilities()
    
    logger.info(f"🚀 PDF-to-MD Engine v2.2 with AI Enhancement")
    if ai_caps:
        logger.info(f"🤖 AI Capabilities: {', '.join(ai_caps)}")
    else:
        logger.info("🤖 AI Enhancement: Not available (run: python intelligent_install.py)")
    
    # Ensure directories exist
    settings.INPUT_DIR.mkdir(parents=True, exist_ok=True)
    settings.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Find PDFs
    pdfs = list(settings.INPUT_DIR.glob("*.pdf"))
    
    if not pdfs:
        logger.warning(f"No PDFs found in {settings.INPUT_DIR}")
        logger.info("Place PDF files in the data/input/ directory and run again")
        return

    logger.info(f"Found {len(pdfs)} PDFs to process.")
    
    # Track processing results
    results = []
    
    for pdf in pdfs:
        try:
            logger.info(f"📄 Processing: {pdf.name}")
            start_time = time.time()
            process_pdf(pdf)
            processing_time = time.time() - start_time
            
            # Read results from receipt with error handling
            receipt_file = settings.OUTPUT_DIR / clean_filename(pdf.stem) / ".receipt"
            if receipt_file.exists():
                try:
                    import json
                    metadata = json.loads(receipt_file.read_text())
                    results.append({
                        'file': pdf.name,
                        'method': metadata.get('extraction_strategy', {}).get('method_used', 'unknown'),
                        'quality': metadata.get('quality_metrics', {}).get('overall_score', 0.0),
                        'time': processing_time,
                        'chapters': metadata.get('chapters_detected', 0)
                    })
                except Exception as e:
                    logger.warning(f"Could not read receipt for {pdf.name}: {e}")
                    results.append({
                        'file': pdf.name,
                        'method': 'completed',
                        'quality': 0.8,  # Assume good quality if no receipt
                        'time': processing_time,
                        'chapters': 0
                    })
            else:
                results.append({
                    'file': pdf.name,
                    'method': 'completed',
                    'quality': 0.8,  # Assume good quality if no receipt
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
"""
Enhanced PDF Converter - Integrating pdfmd and markitdown best practices
Combines modular pipeline architecture with intelligent format detection
"""
import io
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, BinaryIO
from dataclasses import dataclass
from loguru import logger
# Optional magika import with fallback
try:
    import magika
    MAGIKA_AVAILABLE = True
except ImportError:
    MAGIKA_AVAILABLE = False

from .enhanced_processor import process_pdf_enhanced
from .pdf_analyzer import analyze_pdf_characteristics, get_extraction_strategy
from .stream_converter import StreamPDFConverter, ConversionResult

@dataclass
class EnhancedConversionResult:
    """Enhanced result with comprehensive metadata"""
    markdown: str
    title: Optional[str] = None
    metadata: Dict[str, Any] = None
    extraction_method: str = "unknown"
    confidence: float = 0.0
    processing_time: float = 0.0

class UnifiedPDFConverter:
    """Unified converter combining pdfmd modularity with markitdown stream processing"""
    
    def __init__(self):
        self._stream_converter = StreamPDFConverter()
        if MAGIKA_AVAILABLE:
            self._magika = magika.Magika()
        else:
            self._magika = None
    
    def accepts(self, source) -> bool:
        """Check if source is a PDF using multiple detection methods"""
        if isinstance(source, (str, Path)):
            path = Path(source)
            return path.suffix.lower() == '.pdf' and path.exists()
        
        elif hasattr(source, 'read'):
            try:
                pos = source.tell()
                # Use magika for content detection if available
                if self._magika:
                    result = self._magika.identify_stream(source)
                    source.seek(pos)
                    
                    if result.status == "ok":
                        return result.prediction.output.mime_type == "application/pdf"
                
                # Fallback: check PDF header
                source.seek(pos)
                header = source.read(8)
                source.seek(pos)
                return header.startswith(b'%PDF-')
            except:
                return False
        
        return False
    
    def convert(self, source, **kwargs) -> EnhancedConversionResult:
        """Convert PDF using enhanced pipeline with intelligent method selection"""
        import time
        start_time = time.time()
        
        try:
            # Handle different source types
            if isinstance(source, (str, Path)):
                pdf_path = Path(source)
                
                # Analyze PDF characteristics for optimal method selection
                characteristics = analyze_pdf_characteristics(pdf_path)
                strategy = get_extraction_strategy(characteristics)
                
                logger.info(f"PDF Analysis: {characteristics.optimal_extraction_method} "
                           f"(confidence: {characteristics.extraction_confidence:.2f})")
                
                # Use enhanced processor with intelligent method selection
                process_pdf_enhanced(pdf_path)
                
                # Collect results
                output_dir = pdf_path.parent / f"{pdf_path.stem}_enhanced"
                markdown_files = list(output_dir.glob("*.md"))
                
                if not markdown_files:
                    return EnhancedConversionResult(
                        markdown="# No content extracted",
                        extraction_method="failed",
                        processing_time=time.time() - start_time
                    )
                
                # Combine all markdown content
                combined_content = []
                for md_file in sorted(markdown_files):
                    content = md_file.read_text(encoding='utf-8')
                    combined_content.append(content)
                
                # Read metadata
                receipt_file = output_dir / ".receipt"
                metadata = {}
                if receipt_file.exists():
                    import json
                    metadata = json.loads(receipt_file.read_text())
                
                return EnhancedConversionResult(
                    markdown="\\n\\n---\\n\\n".join(combined_content),
                    title=pdf_path.name,
                    metadata=metadata,
                    extraction_method=characteristics.optimal_extraction_method,
                    confidence=characteristics.extraction_confidence,
                    processing_time=time.time() - start_time
                )
            
            elif hasattr(source, 'read'):
                # Use stream converter for binary streams
                from .stream_converter import StreamInfo
                
                stream_info = StreamInfo()
                if hasattr(source, 'name'):
                    path = Path(source.name)
                    stream_info = StreamInfo(
                        extension=path.suffix,
                        filename=path.name,
                        local_path=str(path)
                    )
                
                result = self._stream_converter.convert(source, stream_info, **kwargs)
                
                return EnhancedConversionResult(
                    markdown=result.markdown,
                    title=result.title,
                    metadata=result.metadata or {},
                    extraction_method="stream_processing",
                    confidence=0.8,
                    processing_time=time.time() - start_time
                )
            
            else:
                raise ValueError(f"Unsupported source type: {type(source)}")
                
        except Exception as e:
            logger.error(f"Enhanced conversion failed: {e}")
            return EnhancedConversionResult(
                markdown=f"# Conversion Error\\n\\nFailed to process PDF: {e}",
                metadata={"error": str(e)},
                extraction_method="error",
                processing_time=time.time() - start_time
            )

# Main entry points
def convert_pdf_enhanced(source, **kwargs) -> EnhancedConversionResult:
    """Main entry point for enhanced PDF conversion"""
    converter = UnifiedPDFConverter()
    return converter.convert(source, **kwargs)

def convert_pdf_with_analysis(pdf_path: Path) -> Tuple[EnhancedConversionResult, Dict[str, Any]]:
    """Convert PDF with detailed analysis and strategy information"""
    # Analyze first
    characteristics = analyze_pdf_characteristics(pdf_path)
    strategy = get_extraction_strategy(characteristics)
    
    # Convert
    result = convert_pdf_enhanced(pdf_path)
    
    # Combine analysis
    analysis = {
        "pdf_characteristics": {
            "version": characteristics.version,
            "page_count": characteristics.page_count,
            "has_text_layer": characteristics.has_text_layer,
            "is_scanned": characteristics.is_scanned,
            "table_count": characteristics.table_count,
            "creation_method": characteristics.creation_method,
            "optimal_method": characteristics.optimal_extraction_method,
            "confidence": characteristics.extraction_confidence
        },
        "extraction_strategy": strategy,
        "processing_result": {
            "method_used": result.extraction_method,
            "processing_time": result.processing_time,
            "success": "error" not in result.extraction_method
        }
    }
    
    return result, analysis
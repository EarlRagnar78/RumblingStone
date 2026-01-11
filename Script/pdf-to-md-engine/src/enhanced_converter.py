"""
Enhanced PDF Converter - Integrating best practices from pdfmd and markitdown
Combines modular pipeline architecture with intelligent format detection
"""
import io
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, BinaryIO
from dataclasses import dataclass
from loguru import logger
import fitz
import magika

from .enhanced_processor import process_pdf_enhanced
from .pdf_analyzer import analyze_pdf_characteristics, get_extraction_strategy

@dataclass
class ConversionResult:
    """Result of PDF conversion with metadata"""
    text_content: str
    metadata: Dict[str, Any]
    images: List[Path]
    extraction_method: str
    confidence: float

class EnhancedPDFConverter:
    """Enhanced PDF converter with intelligent format detection and modular pipeline"""
    
    def __init__(self):
        self._magika = magika.Magika()
    
    def accepts(self, file_stream: BinaryIO) -> bool:
        """Check if file is a PDF using content analysis"""
        try:
            # Use magika for content-based detection
            result = self._magika.identify_stream(file_stream)
            if result.status == "ok":
                return result.prediction.output.mime_type == "application/pdf"
            
            # Fallback: check PDF header
            file_stream.seek(0)
            header = file_stream.read(8)
            file_stream.seek(0)
            return header.startswith(b'%PDF-')
        except:
            return False
    
    def convert(self, source, output_path: Optional[Path] = None) -> ConversionResult:
        """Convert PDF using enhanced pipeline with intelligent method selection"""
        
        # Handle different source types
        if isinstance(source, (str, Path)):
            pdf_path = Path(source)
        elif hasattr(source, 'read'):
            # Stream input - save to temp file
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
                tmp.write(source.read())
                pdf_path = Path(tmp.name)
        else:
            raise ValueError(f"Unsupported source type: {type(source)}")
        
        # Analyze PDF characteristics for optimal method selection
        characteristics = analyze_pdf_characteristics(pdf_path)
        strategy = get_extraction_strategy(characteristics)
        
        logger.info(f"PDF Analysis: {characteristics.optimal_extraction_method} "
                   f"(confidence: {characteristics.extraction_confidence:.2f})")
        
        # Set output path if not provided
        if output_path is None:
            output_path = pdf_path.parent / f"{pdf_path.stem}_enhanced"
        
        # Use enhanced processor with intelligent method selection
        try:
            process_pdf_enhanced(pdf_path)
            
            # Collect results
            output_files = list(output_path.glob("*.md"))
            if not output_files:
                raise ValueError("No markdown files generated")
            
            # Combine all markdown content
            combined_content = []
            for md_file in sorted(output_files):
                combined_content.append(md_file.read_text(encoding='utf-8'))
            
            # Collect images
            assets_dir = output_path / "assets"
            images = list(assets_dir.glob("*.png")) if assets_dir.exists() else []
            
            # Read metadata
            receipt_file = output_path / ".receipt"
            metadata = {}
            if receipt_file.exists():
                import json
                metadata = json.loads(receipt_file.read_text())
            
            return ConversionResult(
                text_content="\n\n---\n\n".join(combined_content),
                metadata=metadata,
                images=images,
                extraction_method=characteristics.optimal_extraction_method,
                confidence=characteristics.extraction_confidence
            )
            
        except Exception as e:
            logger.error(f"Enhanced conversion failed: {e}")
            raise

class StreamBasedConverter:
    """Stream-based converter inspired by markitdown architecture"""
    
    def __init__(self):
        self.pdf_converter = EnhancedPDFConverter()
    
    def convert_stream(self, stream: BinaryIO, **kwargs) -> ConversionResult:
        """Convert from binary stream"""
        if not self.pdf_converter.accepts(stream):
            raise ValueError("Stream is not a valid PDF")
        
        return self.pdf_converter.convert(stream, **kwargs)
    
    def convert_local(self, path: Path, **kwargs) -> ConversionResult:
        """Convert from local file"""
        return self.pdf_converter.convert(path, **kwargs)

def convert_pdf_enhanced(source, output_path: Optional[Path] = None, **kwargs) -> ConversionResult:
    """Main entry point for enhanced PDF conversion"""
    converter = StreamBasedConverter()
    
    if isinstance(source, (str, Path)):
        return converter.convert_local(Path(source), **kwargs)
    else:
        return converter.convert_stream(source, **kwargs)
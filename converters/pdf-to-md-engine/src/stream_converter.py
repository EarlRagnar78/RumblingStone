"""
Stream-based PDF Converter - Inspired by Microsoft MarkItDown
Provides unified interface for PDF processing with intelligent content detection
"""
import io
from pathlib import Path
from typing import BinaryIO, Optional, Any, Dict
from dataclasses import dataclass
# Optional magika import with fallback
try:
    import magika
    MAGIKA_AVAILABLE = True
except ImportError:
    MAGIKA_AVAILABLE = False

from .enhanced_processor import process_pdf_enhanced

@dataclass(frozen=True)
class StreamInfo:
    """Stream metadata for intelligent processing"""
    mimetype: Optional[str] = None
    extension: Optional[str] = None
    filename: Optional[str] = None
    local_path: Optional[str] = None

@dataclass
class ConversionResult:
    """Result of PDF conversion"""
    markdown: str
    title: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class StreamPDFConverter:
    """Stream-based PDF converter with intelligent content detection"""
    
    def __init__(self):
        if MAGIKA_AVAILABLE:
            self._magika = magika.Magika()
        else:
            self._magika = None
    
    def accepts(self, file_stream: BinaryIO, stream_info: StreamInfo) -> bool:
        """Check if stream is a PDF using content analysis"""
        try:
            if stream_info.extension and stream_info.extension.lower() == '.pdf':
                return True
            if stream_info.mimetype and 'pdf' in stream_info.mimetype.lower():
                return True
            
            pos = file_stream.tell()
            if self._magika:
                result = self._magika.identify_stream(file_stream)
                file_stream.seek(pos)
                
                if result.status == "ok":
                    return result.prediction.output.mime_type == "application/pdf"
            
            file_stream.seek(pos)
            header = file_stream.read(8)
            file_stream.seek(pos)
            return header.startswith(b'%PDF-')
            
        except Exception:
            return False
    
    def convert(self, file_stream: BinaryIO, stream_info: StreamInfo, **kwargs) -> ConversionResult:
        """Convert PDF stream to markdown"""
        if hasattr(file_stream, 'name') and Path(file_stream.name).exists():
            pdf_path = Path(file_stream.name)
        else:
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
                tmp.write(file_stream.read())
                pdf_path = Path(tmp.name)
        
        try:
            process_pdf_enhanced(pdf_path)
            
            output_dir = pdf_path.parent / f"{pdf_path.stem}_enhanced"
            markdown_files = list(output_dir.glob("*.md"))
            
            if not markdown_files:
                return ConversionResult(markdown="# No content extracted")
            
            combined_content = []
            for md_file in sorted(markdown_files):
                content = md_file.read_text(encoding='utf-8')
                combined_content.append(content)
            
            receipt_file = output_dir / ".receipt"
            metadata = {}
            if receipt_file.exists():
                import json
                metadata = json.loads(receipt_file.read_text())
            
            return ConversionResult(
                markdown="\n\n---\n\n".join(combined_content),
                title=stream_info.filename or "PDF Document",
                metadata=metadata
            )
            
        except Exception as e:
            return ConversionResult(
                markdown=f"# Conversion Error\n\nFailed to process PDF: {e}",
                metadata={"error": str(e)}
            )

def convert_pdf_stream(source, **kwargs) -> ConversionResult:
    """Main entry point for stream-based PDF conversion"""
    converter = StreamPDFConverter()
    
    if isinstance(source, (str, Path)):
        pdf_path = Path(source)
        stream_info = StreamInfo(
            extension=pdf_path.suffix,
            filename=pdf_path.name,
            local_path=str(pdf_path)
        )
        with open(pdf_path, 'rb') as f:
            return converter.convert(f, stream_info, **kwargs)
    
    elif hasattr(source, 'read'):
        stream_info = StreamInfo()
        if hasattr(source, 'name'):
            path = Path(source.name)
            stream_info = StreamInfo(
                extension=path.suffix,
                filename=path.name,
                local_path=str(path)
            )
        
        return converter.convert(source, stream_info, **kwargs)
    
    else:
        raise ValueError(f"Unsupported source type: {type(source)}")
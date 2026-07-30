"""
PDF Utilities inspired by FusePDF
Provides Ghostscript integration and page extraction capabilities
"""

import subprocess
import hashlib
from pathlib import Path
from typing import Optional, List, Tuple
from loguru import logger

class PDFUtilities:
    """PDF utilities using Ghostscript for reliable operations"""
    
    @staticmethod
    def find_ghostscript() -> Optional[str]:
        """Find Ghostscript executable"""
        candidates = ['gs', 'gswin64c', 'gswin32c', 'ghostscript']
        
        for cmd in candidates:
            try:
                result = subprocess.run([cmd, '--version'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    return cmd
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
        return None
    
    @staticmethod
    def get_page_count(pdf_path: Path) -> int:
        """Get PDF page count using Ghostscript"""
        gs_cmd = PDFUtilities.find_ghostscript()
        if not gs_cmd:
            logger.warning("Ghostscript not found, using fallback")
            return PDFUtilities._get_page_count_fallback(pdf_path)
        
        try:
            cmd = [gs_cmd, '-q', '-dNODISPLAY', '-dNOSAFER', '-c', 
                   f'/pdffile ({pdf_path}) (r) file runpdfbegin pdfpagecount = quit']
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                return int(result.stdout.strip())
        except Exception as e:
            logger.warning(f"Ghostscript page count failed: {e}")
        
        return PDFUtilities._get_page_count_fallback(pdf_path)
    
    @staticmethod
    def _get_page_count_fallback(pdf_path: Path) -> int:
        """Fallback page count using PyMuPDF"""
        try:
            import fitz
            doc = fitz.open(str(pdf_path))
            count = len(doc)
            doc.close()
            return count
        except Exception:
            return 0
    
    @staticmethod
    def extract_page_range(pdf_path: Path, output_path: Path, 
                          start_page: int, end_page: int) -> bool:
        """Extract page range using Ghostscript"""
        gs_cmd = PDFUtilities.find_ghostscript()
        if not gs_cmd:
            return False
        
        try:
            cmd = [gs_cmd, '-q', '-dNOPAUSE', '-dBATCH', 
                   f'-sOutputFile={output_path}',
                   f'-dFirstPage={start_page}', f'-dLastPage={end_page}',
                   '-sDEVICE=pdfwrite', str(pdf_path)]
            
            result = subprocess.run(cmd, capture_output=True, timeout=60)
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Page extraction failed: {e}")
            return False
    
    @staticmethod
    def get_pdf_checksum(pdf_path: Path) -> str:
        """Get PDF checksum for caching"""
        sha256_hash = hashlib.sha256()
        try:
            with open(pdf_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(chunk)
            return sha256_hash.hexdigest()[:16]  # Short hash
        except Exception:
            return ""
    
    @staticmethod
    def validate_pdf(pdf_path: Path) -> bool:
        """Validate PDF file integrity"""
        try:
            import fitz
            doc = fitz.open(str(pdf_path))
            is_valid = len(doc) > 0
            doc.close()
            return is_valid
        except Exception:
            return False
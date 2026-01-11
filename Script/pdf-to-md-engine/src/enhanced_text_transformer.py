"""
Enhanced Text Transformation - Inspired by pdfmd
Cleans and normalizes extracted text with intelligent heuristics
"""
import re
from collections import Counter
from typing import List, Optional, Tuple
from loguru import logger

class EnhancedTextTransformer:
    """Text transformation with pdfmd-inspired heuristics"""
    
    def __init__(self):
        self.bullet_pattern = re.compile(r"^[•◦◦·\-—–]\s*$")
        self.footer_dash_pattern = re.compile(r"^-+\s*\d+\s*-+$")
        self.footer_pagenum_pattern = re.compile(r"^\d+$")
        self.footer_page_label_pattern = re.compile(r"^page\s+\d+$", re.IGNORECASE)
    
    def transform_text(self, text: str) -> str:
        """Apply comprehensive text transformations"""
        lines = text.split('\n')
        
        # 1. Remove header/footer patterns
        lines = self._remove_header_footer_patterns(lines)
        
        # 2. Strip drop caps
        lines = self._strip_drop_caps(lines)
        
        # 3. Merge bullet lines
        lines = self._merge_bullet_lines(lines)
        
        # 4. Fix hyphenation
        text = '\n'.join(lines)
        text = self._fix_hyphenation(text)
        
        # 5. Normalize punctuation
        text = self._normalize_punctuation(text)
        
        return text
    
    def _remove_header_footer_patterns(self, lines: List[str]) -> List[str]:
        """Remove repeating header/footer patterns"""
        if len(lines) < 10:  # Too short to have meaningful patterns
            return lines
        
        # Detect repeating patterns at start/end of sections
        header_candidates = []
        footer_candidates = []
        
        # Sample every ~10 lines to find patterns
        for i in range(0, len(lines), 10):
            if i < len(lines) and lines[i].strip():
                header_candidates.append(lines[i].strip())
            if i + 9 < len(lines) and lines[i + 9].strip():
                footer_candidates.append(lines[i + 9].strip())
        
        # Find most common patterns
        header_pattern = self._find_common_pattern(header_candidates)
        footer_pattern = self._find_common_pattern(footer_candidates)
        
        # Remove matching lines
        cleaned_lines = []
        for line in lines:
            line_clean = line.strip()
            
            # Skip header patterns
            if header_pattern and self._similarity(line_clean, header_pattern) > 0.8:
                continue
            
            # Skip footer patterns
            if footer_pattern and self._similarity(line_clean, footer_pattern) > 0.8:
                continue
            
            # Skip obvious footer noise
            if self._is_footer_noise(line_clean):
                continue
            
            cleaned_lines.append(line)
        
        return cleaned_lines
    
    def _find_common_pattern(self, candidates: List[str]) -> Optional[str]:
        """Find most common pattern in candidates"""
        if len(candidates) < 3:
            return None
        
        # Normalize candidates
        normalized = [self._normalize_text(c) for c in candidates if c.strip()]
        if not normalized:
            return None
        
        # Find most frequent
        counts = Counter(normalized)
        most_common, freq = counts.most_common(1)[0]
        
        # Must appear in at least 30% of candidates
        if freq < len(normalized) * 0.3:
            return None
        
        # Return original candidate that matches
        for candidate in candidates:
            if self._normalize_text(candidate) == most_common:
                return candidate
        
        return None
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for comparison"""
        return re.sub(r'\s+', ' ', text.strip().lower())
    
    def _similarity(self, a: str, b: str) -> float:
        """Calculate similarity between two strings"""
        na = self._normalize_text(a)
        nb = self._normalize_text(b)
        
        if not na or not nb:
            return 0.0
        
        # Simple word-based Jaccard similarity
        words_a = set(na.split())
        words_b = set(nb.split())
        
        intersection = len(words_a & words_b)
        union = len(words_a | words_b)
        
        return intersection / union if union > 0 else 0.0
    
    def _is_footer_noise(self, text: str) -> bool:
        """Detect footer noise patterns"""
        if not text:
            return False
        
        if self.footer_dash_pattern.match(text):
            return True
        if self.footer_pagenum_pattern.match(text):
            return True
        if self.footer_page_label_pattern.match(text):
            return True
        
        return False
    
    def _strip_drop_caps(self, lines: List[str]) -> List[str]:
        """Remove decorative drop caps from line starts"""
        cleaned_lines = []
        
        for line in lines:
            # Check if line starts with single large letter
            stripped = line.lstrip()
            if len(stripped) > 2 and stripped[0].isupper() and stripped[1].isspace():
                # Check if it looks like a drop cap (isolated capital letter)
                rest = stripped[2:].strip()
                if rest and rest[0].islower():
                    # Likely drop cap - remove the first character
                    line = line.replace(stripped[0], '', 1)
            
            cleaned_lines.append(line)
        
        return cleaned_lines
    
    def _merge_bullet_lines(self, lines: List[str]) -> List[str]:
        """Merge bullet-only lines with following text"""
        merged_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Check if this is a bullet-only line
            if (self.bullet_pattern.match(line) and 
                i + 1 < len(lines) and 
                lines[i + 1].strip()):
                
                # Merge with next line
                bullet = line
                next_line = lines[i + 1].strip()
                merged = f"{bullet} {next_line}"
                merged_lines.append(merged)
                i += 2  # Skip both lines
            else:
                merged_lines.append(lines[i])
                i += 1
        
        return merged_lines
    
    def _fix_hyphenation(self, text: str) -> str:
        """Fix line-wrap hyphenation"""
        # Fix hyphenated words across line breaks
        text = re.sub(r'-\n\s*', '', text)
        
        # Fix common hyphenation patterns
        text = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', text)
        
        return text
    
    def _normalize_punctuation(self, text: str) -> str:
        """Normalize punctuation and spacing"""
        # Fix smart quotes
        text = text.replace(''', "'")
        text = text.replace(''', "'")
        text = text.replace('"', '"')
        text = text.replace('"', '"')
        
        # Fix dashes
        text = text.replace('–', '-')
        text = text.replace('—', '--')
        
        # Fix ellipsis
        text = text.replace('…', '...')
        
        # Normalize whitespace
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        
        # Fix spacing around punctuation
        text = re.sub(r'\s+([,.;:?!])', r'\1', text)
        
        return text.strip()

def transform_text_enhanced(text: str) -> str:
    """Enhanced text transformation with pdfmd-inspired heuristics"""
    transformer = EnhancedTextTransformer()
    return transformer.transform_text(text)

def detect_repeating_edges(pages_text: List[str]) -> Tuple[Optional[str], Optional[str]]:
    """Detect repeating header and footer across pages"""
    if len(pages_text) < 3:
        return None, None
    
    transformer = EnhancedTextTransformer()
    
    # Extract first and last lines from each page
    headers = []
    footers = []
    
    for page_text in pages_text:
        lines = [line.strip() for line in page_text.split('\n') if line.strip()]
        if lines:
            headers.append(lines[0])
            footers.append(lines[-1])
    
    # Find common patterns
    header_pattern = transformer._find_common_pattern(headers)
    footer_pattern = transformer._find_common_pattern(footers)
    
    return header_pattern, footer_pattern
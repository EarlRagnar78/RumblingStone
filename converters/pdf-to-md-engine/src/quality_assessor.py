"""
Quality Assessment and Iterative Refinement System
Analyzes extraction results and applies secondary methods for quality improvement
"""
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from loguru import logger

@dataclass
class QualityMetrics:
    """Quality assessment metrics for extracted content"""
    text_completeness: float = 0.0  # 0-1 score
    structure_preservation: float = 0.0  # 0-1 score
    table_quality: float = 0.0  # 0-1 score
    image_coverage: float = 0.0  # 0-1 score
    overall_score: float = 0.0  # 0-1 weighted average
    needs_refinement: bool = False
    recommended_method: Optional[str] = None

class QualityAssessor:
    """Assess extraction quality and recommend refinements"""
    
    def __init__(self):
        self.quality_threshold = 0.75  # Minimum acceptable quality
        self.weights = {
            'text_completeness': 0.4,
            'structure_preservation': 0.3,
            'table_quality': 0.2,
            'image_coverage': 0.1
        }
    
    def assess_quality(self, markdown_content: str, metadata: Dict) -> QualityMetrics:
        """Comprehensive quality assessment"""
        
        # Text completeness assessment
        text_score = self._assess_text_completeness(markdown_content, metadata)
        
        # Structure preservation assessment
        structure_score = self._assess_structure_preservation(markdown_content)
        
        # Table quality assessment
        table_score = self._assess_table_quality(markdown_content)
        
        # Image coverage assessment
        image_score = self._assess_image_coverage(metadata)
        
        # Calculate weighted overall score
        overall = (
            text_score * self.weights['text_completeness'] +
            structure_score * self.weights['structure_preservation'] +
            table_score * self.weights['table_quality'] +
            image_score * self.weights['image_coverage']
        )
        
        # Determine if refinement is needed
        needs_refinement = overall < self.quality_threshold
        recommended_method = self._recommend_refinement_method(
            text_score, structure_score, table_score, image_score, metadata
        ) if needs_refinement else None
        
        return QualityMetrics(
            text_completeness=text_score,
            structure_preservation=structure_score,
            table_quality=table_score,
            image_coverage=image_score,
            overall_score=overall,
            needs_refinement=needs_refinement,
            recommended_method=recommended_method
        )
    
    def _assess_text_completeness(self, content: str, metadata: Dict) -> float:
        """Assess text extraction completeness"""
        if not content.strip():
            return 0.0
        
        # Check for common extraction issues
        issues = 0
        total_checks = 5
        
        # 1. Too many garbled characters
        garbled_ratio = len(re.findall(r'[^\w\s\-.,!?;:()\[\]{}"\']', content)) / max(len(content), 1)
        if garbled_ratio > 0.1:
            issues += 1
        
        # 2. Excessive line breaks (poor formatting)
        excessive_breaks = len(re.findall(r'\n\s*\n\s*\n', content))
        if excessive_breaks > len(content.split('\n')) * 0.3:
            issues += 1
        
        # 3. Very short content relative to page count
        page_count = metadata.get('pdf_characteristics', {}).get('page_count', 1)
        chars_per_page = len(content) / page_count
        if chars_per_page < 500:  # Very low content per page
            issues += 1
        
        # 4. Missing common document elements
        has_headers = bool(re.search(r'^#+\s', content, re.MULTILINE))
        has_paragraphs = len(content.split('\n\n')) > 2
        if not (has_headers or has_paragraphs):
            issues += 1
        
        # 5. Text quality from metadata
        text_quality = metadata.get('text_analysis', {}).get('text_quality', 1.0)
        if text_quality < 0.7:
            issues += 1
        
        return max(0.0, 1.0 - (issues / total_checks))
    
    def _assess_structure_preservation(self, content: str) -> float:
        """Assess document structure preservation"""
        score = 0.0
        
        # Check for headers (structure indicators)
        headers = re.findall(r'^#+\s.+', content, re.MULTILINE)
        if headers:
            score += 0.3
        
        # Check for proper paragraph breaks
        paragraphs = content.split('\n\n')
        if len(paragraphs) > 2:
            score += 0.2
        
        # Check for lists
        lists = re.findall(r'^\s*[-*+]\s', content, re.MULTILINE)
        if lists:
            score += 0.2
        
        # Check for proper spacing (not too dense, not too sparse)
        lines = content.split('\n')
        non_empty_lines = [l for l in lines if l.strip()]
        if len(non_empty_lines) > len(lines) * 0.3:  # Good content density
            score += 0.3
        
        return min(1.0, score)
    
    def _assess_table_quality(self, content: str) -> float:
        """Assess table extraction quality"""
        tables = re.findall(r'\|.*\|', content)
        if not tables:
            return 0.8  # No tables expected, good score
        
        score = 0.0
        
        # Check for proper table structure
        table_blocks = re.findall(r'(\|.*\|\n)+', content)
        well_formed_tables = 0
        
        for table_block in table_blocks:
            lines = table_block.strip().split('\n')
            if len(lines) >= 2:  # Header + separator minimum
                # Check if has separator line
                has_separator = any('---' in line for line in lines)
                if has_separator:
                    well_formed_tables += 1
        
        if table_blocks:
            score = well_formed_tables / len(table_blocks)
        
        return score
    
    def _assess_image_coverage(self, metadata: Dict) -> float:
        """Assess image extraction coverage"""
        pdf_chars = metadata.get('pdf_characteristics', {})
        has_images = pdf_chars.get('has_images', False)
        
        if not has_images:
            return 1.0  # Perfect score if no images expected
        
        # Check if images were extracted
        ocr_results = metadata.get('ocr_text_results', 0)
        if ocr_results > 0:
            return 0.8  # Good coverage with OCR text extraction
        
        return 0.3  # Images present but not processed
    
    def _recommend_refinement_method(self, text_score: float, structure_score: float, 
                                   table_score: float, image_score: float, metadata: Dict) -> str:
        """Recommend specific refinement method based on weak areas"""
        
        # Identify the weakest area
        scores = {
            'text': text_score,
            'structure': structure_score,
            'tables': table_score,
            'images': image_score
        }
        
        weakest_area = min(scores, key=scores.get)
        current_method = metadata.get('extraction_strategy', {}).get('method_used', 'unknown')
        
        # Recommend alternative method based on weakness
        if weakest_area == 'text' and text_score < 0.5:
            if current_method != 'docling_conversion':
                return 'docling_conversion'
            else:
                return 'enhanced_text'
        
        elif weakest_area == 'structure' and structure_score < 0.6:
            if current_method != 'layout_preserving':
                return 'layout_preserving'
            else:
                return 'docling_conversion'
        
        elif weakest_area == 'tables' and table_score < 0.5:
            return 'layout_preserving'  # Best for tables
        
        elif weakest_area == 'images' and image_score < 0.4:
            return 'ocr_enhancement'  # Focus on OCR text extraction
        
        # Default fallback
        return 'docling_conversion'

def assess_extraction_quality(markdown_content: str, metadata: Dict) -> QualityMetrics:
    """Main entry point for quality assessment"""
    assessor = QualityAssessor()
    return assessor.assess_quality(markdown_content, metadata)
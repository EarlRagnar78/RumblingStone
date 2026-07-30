"""
AI Enhancement Module for PDF-to-MD Engine
Integrates multiple AI models for quality improvement
"""

import warnings
warnings.filterwarnings("ignore")

from pathlib import Path
from typing import Dict, List, Optional, Tuple
from loguru import logger
import torch

# AI Model Imports (with fallbacks)
try:
    import transformers
    from transformers import pipeline, AutoTokenizer, AutoModel
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

try:
    from PIL import Image
    import cv2
    import numpy as np
    VISION_AVAILABLE = True
except ImportError:
    VISION_AVAILABLE = False

class AIEnhancer:
    """AI-powered enhancement for extracted content"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.models = {}
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize available AI models"""
        
        # 1. Text Enhancement Model
        if TRANSFORMERS_AVAILABLE:
            try:
                self.models['text_enhancer'] = pipeline(
                    "text2text-generation",
                    model="google/flan-t5-base",
                    device=0 if torch.cuda.is_available() else -1
                )
                logger.info("✅ Text enhancement model loaded")
            except Exception as e:
                logger.warning(f"Text enhancer failed: {e}")
        
        # 2. Grammar Correction
        try:
            import language_tool_python
            self.models['grammar'] = language_tool_python.LanguageTool('en-US')
            logger.info("✅ Grammar correction loaded")
        except ImportError:
            logger.warning("LanguageTool not available")
        
        # 3. Ollama Local LLM
        if OLLAMA_AVAILABLE:
            try:
                # Check if Ollama is running
                models = ollama.list()
                if models:
                    self.models['llm'] = 'llama3.2:3b'  # or available model
                    logger.info("✅ Ollama LLM available")
            except Exception:
                logger.warning("Ollama not running")
    
    def enhance_text_quality(self, text: str, context: Dict = None) -> str:
        """Enhance text quality using AI models"""
        
        if not text.strip():
            return text
        
        enhanced_text = text
        
        # 1. Grammar and style correction
        if 'grammar' in self.models:
            enhanced_text = self._fix_grammar(enhanced_text)
        
        # 2. Structure improvement
        if 'text_enhancer' in self.models:
            enhanced_text = self._improve_structure(enhanced_text)
        
        # 3. LLM-based refinement
        if 'llm' in self.models:
            enhanced_text = self._llm_refine(enhanced_text, context)
        
        return enhanced_text
    
    def _fix_grammar(self, text: str) -> str:
        """Fix grammar and spelling errors"""
        try:
            tool = self.models['grammar']
            matches = tool.check(text)
            corrected = language_tool_python.utils.correct(text, matches)
            return corrected
        except Exception as e:
            logger.debug(f"Grammar correction failed: {e}")
            return text
    
    def _improve_structure(self, text: str) -> str:
        """Improve text structure using T5"""
        try:
            enhancer = self.models['text_enhancer']
            
            # Split into chunks for processing
            chunks = self._split_text(text, max_length=512)
            enhanced_chunks = []
            
            for chunk in chunks:
                prompt = f"Improve the structure and clarity of this text: {chunk}"
                result = enhancer(prompt, max_length=len(chunk) + 100)
                enhanced_chunks.append(result[0]['generated_text'])
            
            return '\n\n'.join(enhanced_chunks)
        except Exception as e:
            logger.debug(f"Structure improvement failed: {e}")
            return text
    
    def _llm_refine(self, text: str, context: Dict = None) -> str:
        """Refine text using local LLM"""
        try:
            model_name = self.models['llm']
            
            prompt = f"""
            Please improve this extracted PDF text by:
            1. Fixing OCR errors and typos
            2. Improving markdown formatting
            3. Ensuring proper paragraph structure
            4. Maintaining original meaning
            
            Text to improve:
            {text[:2000]}  # Limit for context
            """
            
            response = ollama.generate(model=model_name, prompt=prompt)
            return response['response']
        except Exception as e:
            logger.debug(f"LLM refinement failed: {e}")
            return text
    
    def enhance_table_structure(self, table_text: str) -> str:
        """Enhance table structure and formatting"""
        
        if not table_text.strip():
            return table_text
        
        # Basic table enhancement
        lines = table_text.split('\n')
        enhanced_lines = []
        
        for line in lines:
            # Detect table rows and improve formatting
            if '|' in line:
                # Clean up table formatting
                cells = [cell.strip() for cell in line.split('|')]
                cells = [cell for cell in cells if cell]  # Remove empty cells
                enhanced_line = '| ' + ' | '.join(cells) + ' |'
                enhanced_lines.append(enhanced_line)
            else:
                enhanced_lines.append(line)
        
        return '\n'.join(enhanced_lines)
    
    def enhance_mathematical_content(self, text: str) -> str:
        """Enhance mathematical expressions and formulas"""
        
        # Convert common mathematical symbols
        math_replacements = {
            '±': '\\pm',
            '≤': '\\leq',
            '≥': '\\geq',
            '∞': '\\infty',
            '∑': '\\sum',
            '∏': '\\prod',
            '∫': '\\int',
            '√': '\\sqrt',
            'α': '\\alpha',
            'β': '\\beta',
            'γ': '\\gamma',
            'δ': '\\delta',
            'π': '\\pi',
            'θ': '\\theta',
            'λ': '\\lambda',
            'μ': '\\mu',
            'σ': '\\sigma',
            'φ': '\\phi',
            'ω': '\\omega'
        }
        
        enhanced_text = text
        for symbol, latex in math_replacements.items():
            enhanced_text = enhanced_text.replace(symbol, f'${latex}$')
        
        return enhanced_text
    
    def _split_text(self, text: str, max_length: int = 512) -> List[str]:
        """Split text into manageable chunks"""
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) > max_length:
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                    current_chunk = [word]
                    current_length = len(word)
            else:
                current_chunk.append(word)
                current_length += len(word) + 1
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks

class VisionAIEnhancer:
    """Vision AI for image and layout enhancement"""
    
    def __init__(self):
        self.models = {}
        self._initialize_vision_models()
    
    def _initialize_vision_models(self):
        """Initialize vision models"""
        
        if not VISION_AVAILABLE:
            logger.warning("Vision libraries not available")
            return
        
        # Layout analysis model (if available)
        try:
            # This would load a layout detection model
            # self.models['layout'] = load_layout_model()
            logger.info("Vision models initialized")
        except Exception as e:
            logger.warning(f"Vision model loading failed: {e}")
    
    def enhance_image_extraction(self, image_path: Path) -> Dict:
        """Enhance image extraction with AI analysis"""
        
        try:
            image = cv2.imread(str(image_path))
            if image is None:
                return {}
            
            # Basic image analysis
            height, width = image.shape[:2]
            
            # Detect if image contains text, diagrams, or photos
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            edge_ratio = np.sum(edges > 0) / (height * width)
            
            image_type = "diagram" if edge_ratio > 0.1 else "photo"
            
            return {
                'type': image_type,
                'dimensions': (width, height),
                'edge_ratio': edge_ratio,
                'quality_score': min(1.0, (width * height) / 100000)
            }
        
        except Exception as e:
            logger.debug(f"Image analysis failed: {e}")
            return {}

# Integration function for enhanced_processor.py
def apply_ai_enhancement(content: str, context: Dict = None) -> str:
    """Apply AI enhancement to extracted content"""
    
    enhancer = AIEnhancer()
    
    # Enhance text quality
    enhanced_content = enhancer.enhance_text_quality(content, context)
    
    # Enhance mathematical content
    enhanced_content = enhancer.enhance_mathematical_content(enhanced_content)
    
    # Enhance table structures
    if '|' in enhanced_content:
        enhanced_content = enhancer.enhance_table_structure(enhanced_content)
    
    return enhanced_content
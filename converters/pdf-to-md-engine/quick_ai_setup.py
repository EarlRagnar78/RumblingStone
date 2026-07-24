#!/usr/bin/env python3
"""
Quick AI Setup - Install only free, no-cost AI tools
"""

import subprocess
import sys
from pathlib import Path

def install_free_ai_tools():
    """Install completely free AI tools"""
    
    print("🆓 Installing FREE AI tools (no API costs)...")
    
    # Activate virtual environment
    if Path("venv/bin/activate").exists():
        pip_cmd = "venv/bin/pip"
    elif Path("venv/Scripts/pip.exe").exists():
        pip_cmd = "venv/Scripts/pip"
    else:
        print("❌ Virtual environment not found. Run setup.py first.")
        return False
    
    # Free AI tools (no API costs)
    free_tools = [
        "transformers>=4.35.0",      # Hugging Face models (local)
        "language-tool-python>=2.7.1",  # Grammar correction (local)
        "spacy>=3.7.0",              # NLP processing (local)
        "nltk>=3.8.1",               # Text processing (local)
        "scikit-learn>=1.3.0",       # ML algorithms (local)
    ]
    
    for tool in free_tools:
        print(f"📦 Installing {tool.split('>=')[0]}...")
        try:
            subprocess.run([pip_cmd, "install", tool], check=True, capture_output=True)
            print(f"   ✅ Success")
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️ Warning: {e}")
    
    # Download spaCy model
    print("📥 Downloading spaCy English model...")
    try:
        if Path("venv/bin/python").exists():
            python_cmd = "venv/bin/python"
        else:
            python_cmd = "venv/Scripts/python"
        
        subprocess.run([python_cmd, "-m", "spacy", "download", "en_core_web_sm"], 
                      check=True, capture_output=True)
        print("   ✅ spaCy model downloaded")
    except subprocess.CalledProcessError:
        print("   ⚠️ spaCy model download failed (optional)")
    
    # Test AI capabilities
    print("\n🧪 Testing AI capabilities...")
    test_script = '''
try:
    from src.ai_enhancer import AIEnhancer
    enhancer = AIEnhancer()
    
    # Test text enhancement
    test_text = "this is a test with poor grammar and formatting"
    enhanced = enhancer.enhance_text_quality(test_text)
    
    print("✅ AI Enhancement working!")
    print(f"Original: {test_text}")
    print(f"Enhanced: {enhanced}")
    
    # Show available models
    available = list(enhancer.models.keys())
    if available:
        print(f"🤖 Available AI models: {', '.join(available)}")
    else:
        print("⚠️ No AI models loaded (check dependencies)")
        
except Exception as e:
    print(f"❌ AI test failed: {e}")
    print("💡 Try running: ./setup_ai.sh for full setup")
'''
    
    try:
        if Path("venv/bin/python").exists():
            python_cmd = "venv/bin/python"
        else:
            python_cmd = "venv/Scripts/python"
        
        subprocess.run([python_cmd, "-c", test_script], check=False)
    except Exception as e:
        print(f"Test execution failed: {e}")
    
    print("\n🎉 Free AI tools installation complete!")
    print("\n💡 For advanced AI features (Ollama LLM), run: ./setup_ai.sh")
    
    return True

if __name__ == "__main__":
    install_free_ai_tools()
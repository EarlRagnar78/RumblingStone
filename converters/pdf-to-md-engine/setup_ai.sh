#!/bin/bash

# AI Enhancement Setup Script
# Installs optional AI models and dependencies

echo "🤖 Setting up AI Enhancement capabilities..."

# Activate virtual environment
source venv/bin/activate

# Install AI dependencies
echo "📦 Installing AI dependencies..."
pip install -r ai_requirements.txt

# Download spaCy model
echo "📥 Downloading spaCy English model..."
python -m spacy download en_core_web_sm

# Setup Ollama (optional)
echo "🦙 Setting up Ollama for local LLM..."
if command -v ollama &> /dev/null; then
    echo "✅ Ollama already installed"
    
    # Pull a lightweight model
    echo "📥 Pulling Llama 3.2 3B model..."
    ollama pull llama3.2:3b
    
    echo "🚀 Starting Ollama service..."
    ollama serve &
    sleep 5
    
    echo "✅ Ollama setup complete"
else
    echo "⚠️  Ollama not found. Install from: https://ollama.ai"
    echo "   Then run: ollama pull llama3.2:3b"
fi

# Test AI capabilities
echo "🧪 Testing AI enhancement..."
python3 -c "
try:
    from src.ai_enhancer import AIEnhancer
    enhancer = AIEnhancer()
    test_text = 'This is a test document with some errors and poor formatting.'
    enhanced = enhancer.enhance_text_quality(test_text)
    print('✅ AI Enhancement working!')
    print(f'Original: {test_text}')
    print(f'Enhanced: {enhanced}')
except Exception as e:
    print(f'❌ AI Enhancement test failed: {e}')
"

echo ""
echo "🎉 AI Enhancement setup complete!"
echo ""
echo "Available AI features:"
echo "  🔤 Text quality enhancement (T5 model)"
echo "  📝 Grammar correction (LanguageTool)"
echo "  🦙 Local LLM refinement (Ollama)"
echo "  🔢 Mathematical content enhancement"
echo "  📊 Table structure improvement"
echo ""
echo "To enable AI enhancement, the system will automatically use available models."
echo "Quality scores below 0.75 will trigger AI enhancement automatically."
#!/bin/bash
# Setup script for HTML to Markdown Converter
# System Engineering Best Practices

set -euo pipefail  # Exit on error, undefined vars, pipe failures

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONVERTER_SCRIPT="$SCRIPT_DIR/html_to_markdown_converter.py"
REQUIREMENTS_FILE="$SCRIPT_DIR/requirements.txt"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_python() {
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is required but not installed"
        exit 1
    fi
    
    local python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    log_info "Found Python $python_version"
    
    if [[ $(echo "$python_version 3.7" | awk '{print ($1 >= $2)}') -eq 0 ]]; then
        log_error "Python 3.7+ is required, found $python_version"
        exit 1
    fi
}

install_dependencies() {
    log_info "Installing Python dependencies..."
    
    if command -v pip3 &> /dev/null; then
        pip3 install -r "$REQUIREMENTS_FILE" --user
    elif command -v pip &> /dev/null; then
        pip install -r "$REQUIREMENTS_FILE" --user
    else
        log_error "pip is not available. Please install pip first."
        exit 1
    fi
}

make_executable() {
    log_info "Making converter script executable..."
    chmod +x "$CONVERTER_SCRIPT"
}

create_symlink() {
    local bin_dir="$HOME/.local/bin"
    local symlink_path="$bin_dir/html2md"
    
    # Create bin directory if it doesn't exist
    mkdir -p "$bin_dir"
    
    # Remove existing symlink if it exists
    if [[ -L "$symlink_path" ]]; then
        rm "$symlink_path"
    fi
    
    # Create new symlink
    ln -s "$CONVERTER_SCRIPT" "$symlink_path"
    log_info "Created symlink: $symlink_path"
    
    # Check if ~/.local/bin is in PATH
    if [[ ":$PATH:" != *":$bin_dir:"* ]]; then
        log_warn "Add $bin_dir to your PATH to use 'html2md' command globally"
        log_warn "Add this line to your ~/.bashrc or ~/.zshrc:"
        log_warn "export PATH=\"\$HOME/.local/bin:\$PATH\""
    fi
}

run_tests() {
    log_info "Running basic tests..."
    
    # Test script syntax
    if python3 -m py_compile "$CONVERTER_SCRIPT"; then
        log_info "Script syntax check passed"
    else
        log_error "Script syntax check failed"
        exit 1
    fi
    
    # Test dependencies
    python3 -c "
import html2text
from PIL import Image
import requests
from bs4 import BeautifulSoup
print('All dependencies imported successfully')
" || {
        log_error "Dependency test failed"
        exit 1
    }
    
    log_info "All tests passed"
}

main() {
    log_info "Setting up HTML to Markdown Converter..."
    
    check_python
    install_dependencies
    make_executable
    create_symlink
    run_tests
    
    log_info "Setup completed successfully!"
    log_info ""
    log_info "Usage examples:"
    log_info "  $CONVERTER_SCRIPT file.html output.md"
    log_info "  $CONVERTER_SCRIPT html_folder/ markdown_folder/"
    log_info "  html2md --help  # If ~/.local/bin is in PATH"
}

main "$@"
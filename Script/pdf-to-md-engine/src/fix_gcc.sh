#!/bin/bash
# Fix GCC version issue for Python package compilation

set -e

echo "Fixing GCC version compatibility issue..."

# Method 1: Create gcc-12 symlink (temporary fix)
if command -v gcc-15 &> /dev/null; then
    echo "Found gcc-15, creating gcc-12 symlink..."
    
    # Create local bin directory
    mkdir -p ~/.local/bin
    
    # Create symlink
    ln -sf $(which gcc-15) ~/.local/bin/gcc-12
    
    # Add to PATH for this session
    export PATH="$HOME/.local/bin:$PATH"
    
    echo "Created gcc-12 -> gcc-15 symlink"
    
elif command -v gcc &> /dev/null; then
    echo "Found gcc, creating gcc-12 symlink..."
    
    mkdir -p ~/.local/bin
    ln -sf $(which gcc) ~/.local/bin/gcc-12
    export PATH="$HOME/.local/bin:$PATH"
    
    echo "Created gcc-12 -> gcc symlink"
else
    echo "No GCC found. Please install GCC first."
    exit 1
fi

# Method 2: Set environment variables to force compiler
export CC=gcc
export CXX=g++

echo "Environment variables set:"
echo "CC=$CC"
echo "CXX=$CXX"
echo "PATH includes: ~/.local/bin"

echo ""
echo "Now run: pip install -e ."
echo "Or add this to your shell profile:"
echo "export PATH=\"\$HOME/.local/bin:\$PATH\""
echo "export CC=gcc"
echo "export CXX=g++"
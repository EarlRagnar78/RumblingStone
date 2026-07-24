#!/usr/bin/env bash

################################################################################
# SETUP SCRIPT FOR WEBP IMAGE CONVERTER
# Prepares environment and validates configuration
################################################################################

set -e

readonly SETUP_VERSION="1.0"
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Color codes
readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m'

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}WebP Converter Environment Setup${NC}"
    echo -e "${BLUE}Version: $SETUP_VERSION${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓${NC} $*"
}

print_error() {
    echo -e "${RED}✗${NC} $*"
}

print_warning() {
    echo -e "${YELLOW}!${NC} $*"
}

print_info() {
    echo -e "${BLUE}→${NC} $*"
}

# Check system dependencies
check_dependencies() {
    echo -e "\n${BLUE}Checking system dependencies...${NC}\n"
    
    local missing=0
    
    # Check for required commands
    for cmd in find mkdir bash magick convert identify; do
        if command -v "$cmd" &> /dev/null; then
            print_success "Found: $cmd"
        else
            print_error "Missing: $cmd"
            ((missing++))
        fi
    done
    
    if [[ $missing -gt 0 ]]; then
        echo -e "\n${RED}Missing dependencies detected!${NC}\n"
        echo "Install on Ubuntu/Debian:"
        echo "  sudo apt-get install imagemagick libmagickcore-6.q16-3-extra\n"
        echo "Install on CentOS/RHEL:"
        echo "  sudo yum install ImageMagick ImageMagick-devel\n"
        echo "Install on macOS:"
        echo "  brew install imagemagick\n"
        return 1
    fi
    
    print_success "All required dependencies found"
    return 0
}

# Check ImageMagick WebP support
check_webp_support() {
    echo -e "\n${BLUE}Checking WebP support...${NC}\n"
    
    if identify -list format 2>/dev/null | grep -qi "webp"; then
        print_success "WebP format support detected"
        
        # Show WebP version info
        local webp_info=$(convert -version 2>/dev/null | grep -i webp || true)
        if [[ -n "$webp_info" ]]; then
            echo "  $webp_info"
        fi
        return 0
    else
        print_error "WebP support not available in ImageMagick"
        echo -e "\n${YELLOW}Install WebP support:${NC}"
        echo "  Ubuntu/Debian: sudo apt-get install libmagickcore-6.q16-3-extra"
        echo "  CentOS/RHEL:   sudo yum install libjpeg-turbo-devel libpng-devel libtiff-devel"
        return 1
    fi
}

# Create directory structure
setup_directories() {
    echo -e "\n${BLUE}Setting up directory structure...${NC}\n"
    
    local dirs=(
        "Script"
        "Script/Original_images"
        "logs"
        ".conversion_temp"
    )
    
    for dir in "${dirs[@]}"; do
        if mkdir -p "$dir" 2>/dev/null; then
            print_success "Created: $dir"
        else
            print_error "Failed to create: $dir"
            return 1
        fi
    done
    
    # Set proper permissions
    chmod 755 Script logs .conversion_temp 2>/dev/null || true
    
    return 0
}

# Validate script file
validate_script() {
    echo -e "\n${BLUE}Validating conversion script...${NC}\n"
    
    if [[ ! -f "convert_webp.sh" ]]; then
        print_error "convert_webp.sh not found in current directory"
        return 1
    fi
    
    # Check syntax
    if bash -n convert_webp.sh 2>/dev/null; then
        print_success "Script syntax validation passed"
    else
        print_error "Script contains syntax errors"
        bash -n convert_webp.sh
        return 1
    fi
    
    # Check if executable
    if [[ ! -x "convert_webp.sh" ]]; then
        print_warning "Making script executable..."
        chmod +x convert_webp.sh
        print_success "Script is now executable"
    else
        print_success "Script is executable"
    fi
    
    return 0
}

# Test basic functionality
test_functionality() {
    echo -e "\n${BLUE}Testing basic functionality...${NC}\n"
    
    # Create test image
    local test_dir="Script/test_images"
    mkdir -p "$test_dir"
    
    # Create a simple test PNG using ImageMagick
    print_info "Creating test image..."
    convert -size 100x100 xc:blue "$test_dir/test_blue.png" 2>/dev/null || true
    
    if [[ ! -f "$test_dir/test_blue.png" ]]; then
        print_warning "Could not create test image (not critical)"
        return 0
    fi
    
    print_success "Test image created"
    
    # Run conversion on test image
    print_info "Testing conversion..."
    if magick "$test_dir/test_blue.png" -quality 90 "$test_dir/test_blue.webp" 2>/dev/null; then
        print_success "Conversion test successful"
        
        if [[ -f "$test_dir/test_blue.webp" ]]; then
            print_success "WebP file generated successfully"
            
            # Show file sizes
            local orig_size=$(stat -f%z "$test_dir/test_blue.png" 2>/dev/null || stat -c%s "$test_dir/test_blue.png" 2>/dev/null || echo "unknown")
            local webp_size=$(stat -f%z "$test_dir/test_blue.webp" 2>/dev/null || stat -c%s "$test_dir/test_blue.webp" 2>/dev/null || echo "unknown")
            
            if [[ "$orig_size" != "unknown" && "$webp_size" != "unknown" ]]; then
                echo "  Original size: $orig_size bytes"
                echo "  WebP size: $webp_size bytes"
            fi
        fi
    else
        print_error "Conversion test failed"
        return 1
    fi
    
    return 0
}

# Show system information
show_system_info() {
    echo -e "\n${BLUE}System Information:${NC}\n"
    
    print_info "OS: $(uname -s)"
    print_info "Bash version: ${BASH_VERSION%.*}"
    print_info "User: $(whoami)"
    print_info "Current directory: $(pwd)"
    
    local imagemagick_version=$(convert --version 2>/dev/null | head -1 || echo "Unknown")
    print_info "ImageMagick: $imagemagick_version"
}

# Generate configuration summary
generate_summary() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}Setup Summary${NC}"
    echo -e "${BLUE}========================================${NC}\n"
    
    echo "Configuration paths:"
    echo "  Source directory:   $(pwd)/Script"
    echo "  Archive directory:  $(pwd)/Script/Original_images"
    echo "  Log directory:      $(pwd)/logs"
    echo "  Temp directory:     $(pwd)/.conversion_temp"
    
    echo -e "\n${GREEN}Setup completed successfully!${NC}\n"
    
    echo "Next steps:"
    echo "  1. Place your images in the 'Script/' directory"
    echo "  2. Run the converter:"
    echo "     ./convert_webp.sh"
    echo ""
    echo "  3. View results:"
    echo "     - Converted files: Script/*.webp"
    echo "     - Original files: Script/Original_images/"
    echo "     - Logs: logs/webp_conversion_*.log"
    echo ""
    echo "For more options, run:"
    echo "  ./convert_webp.sh --help"
    echo ""
}

# Cleanup test files
cleanup_test_files() {
    if [[ -d "Script/test_images" ]]; then
        rm -rf Script/test_images
        print_success "Cleaned up test files"
    fi
}

# Main setup flow
main() {
    print_header
    
    local exit_code=0
    
    # Run all checks
    check_dependencies || exit_code=1
    check_webp_support || exit_code=1
    setup_directories || exit_code=1
    validate_script || exit_code=1
    
    # Optional tests
    if [[ $exit_code -eq 0 ]]; then
        test_functionality || print_warning "Functionality test encountered issues (not critical)"
        cleanup_test_files
    fi
    
    show_system_info
    
    if [[ $exit_code -eq 0 ]]; then
        generate_summary
    else
        echo -e "\n${RED}Setup completed with errors. Please fix the issues above.${NC}\n"
    fi
    
    return $exit_code
}

# Run main function
main "$@"
exit $?

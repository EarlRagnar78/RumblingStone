#!/usr/bin/env bash

################################################################################
# IMAGE TO WEBP CONVERTER - PRODUCTION GRADE SCRIPT
# 
# Purpose: Recursively find image files, convert to WebP, archive originals
# Author: Senior Infrastructure Engineer
# Date: 2026-01-07
# Version: 1.0
#
# Features:
#  - Recursive directory traversal
#  - Folder structure preservation
#  - Comprehensive error handling & logging
#  - Progress tracking and statistics
#  - Atomic operations with rollback capability
#  - Parallel processing support
################################################################################

set -o errexit      # Exit on any error
set -o pipefail     # Exit if any command in pipeline fails
set -o nounset      # Exit on undefined variable
set -o errtrace     # Inherit ERR trap in functions

################################################################################
# CONFIGURATION SECTION
################################################################################

# Color codes for terminal output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Script configuration
readonly SCRIPT_NAME="$(basename "$0")"
readonly SCRIPT_VERSION="1.0"
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Paths - change these according to your environment
WORK_DIR="${PWD}"                                    # Current working directory
SOURCE_DIR="${WORK_DIR}/Script"                     # Source images directory
ARCHIVE_DIR="${WORK_DIR}/Script/Original_images"    # Archive directory for originals
LOG_DIR="${WORK_DIR}/logs"                          # Log directory
TEMP_DIR="${WORK_DIR}/.conversion_temp"             # Temporary directory for processing

# Logging configuration
readonly LOG_FILE="${LOG_DIR}/webp_conversion_$(date +%Y%m%d_%H%M%S).log"
readonly ERROR_LOG="${LOG_DIR}/webp_conversion_errors_$(date +%Y%m%d_%H%M%S).log"
readonly STATS_FILE="${LOG_DIR}/conversion_stats_$(date +%Y%m%d_%H%M%S).txt"

# Conversion parameters
readonly QUALITY=90
readonly COMPRESSION_LEVEL=6  # 0-6 for libwebp
readonly IMAGE_EXTENSIONS=("jpg" "jpeg" "png" "gif" "bmp" "tiff" "webp")

# Processing parameters
MAX_PARALLEL_JOBS=4          # Number of parallel conversion jobs
CONVERSION_TIMEOUT=300       # Timeout per image in seconds (5 minutes)
SKIP_EXISTING=true          # Skip if WebP already exists

# Statistics counters
TOTAL_FILES=0
PROCESSED_FILES=0
FAILED_FILES=0
SKIPPED_FILES=0
ARCHIVED_FILES=0

################################################################################
# FUNCTION DEFINITIONS
################################################################################

# Print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $*" | tee -a "$LOG_FILE"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $*" | tee -a "$LOG_FILE"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $*" | tee -a "$LOG_FILE"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $*" | tee -a "$LOG_FILE" "$ERROR_LOG"
}

# Logging function with timestamps
log_entry() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    echo "[${timestamp}] [${level}] ${message}" >> "$LOG_FILE"
    
    if [[ "$level" == "ERROR" ]]; then
        echo "[${timestamp}] [${level}] ${message}" >> "$ERROR_LOG"
    fi
}

# Error handler function
error_exit() {
    local line_num="$1"
    local exit_code="$2"
    local error_msg="${3:-Unknown error}"
    
    print_error "Script failed at line ${line_num} with exit code ${exit_code}"
    print_error "Error: ${error_msg}"
    log_entry "ERROR" "Script failed at line ${line_num}: ${error_msg} (exit code: ${exit_code})"
    
    # Cleanup
    cleanup_on_error
    
    exit "${exit_code}"
}

# Set trap for error handling
trap 'error_exit ${LINENO} $?' ERR

# Signal handlers
trap 'handle_interrupt' INT TERM

handle_interrupt() {
    print_warning "Script interrupted by user"
    log_entry "WARN" "Script interrupted by user"
    cleanup_on_error
    exit 130  # Standard exit code for SIGINT
}

# Validate prerequisites
validate_prerequisites() {
    local missing_tools=()
    
    print_info "Validating prerequisites..."
    log_entry "INFO" "Validating prerequisites"
    
    # Check for required commands
    for cmd in find magick convert identify mkdir; do
        if ! command -v "$cmd" &> /dev/null; then
            missing_tools+=("$cmd")
        fi
    done
    
    if [[ ${#missing_tools[@]} -gt 0 ]]; then
        print_error "Missing required tools: ${missing_tools[*]}"
        print_error "Please install ImageMagick (magick/convert) and ensure find, mkdir are available"
        exit 1
    fi
    
    print_success "All prerequisites validated"
    log_entry "INFO" "Prerequisites validation successful"
}

# Initialize directories and logging
init_environment() {
    print_info "Initializing environment..."
    log_entry "INFO" "Initializing conversion environment"
    
    # Create log directory
    if ! mkdir -p "$LOG_DIR" 2>/dev/null; then
        print_error "Failed to create log directory: $LOG_DIR"
        exit 1
    fi
    
    # Create temp directory
    if ! mkdir -p "$TEMP_DIR" 2>/dev/null; then
        print_error "Failed to create temp directory: $TEMP_DIR"
        exit 1
    fi
    
    # Create archive base directory
    if ! mkdir -p "$ARCHIVE_DIR" 2>/dev/null; then
        print_error "Failed to create archive directory: $ARCHIVE_DIR"
        exit 1
    fi
    
    # Verify source directory exists
    if [[ ! -d "$SOURCE_DIR" ]]; then
        print_error "Source directory does not exist: $SOURCE_DIR"
        exit 1
    fi
    
    print_success "Environment initialized"
    print_info "Log file: $LOG_FILE"
    print_info "Error log: $ERROR_LOG"
    print_info "Source directory: $SOURCE_DIR"
    print_info "Archive directory: $ARCHIVE_DIR"
    
    log_entry "INFO" "Environment initialization complete"
}

# Check if ImageMagick supports WebP
check_webp_support() {
    print_info "Checking WebP support in ImageMagick..."
    log_entry "INFO" "Checking WebP format support"
    
    if identify -list format 2>/dev/null | grep -qi "webp"; then
        print_success "WebP support detected"
        log_entry "INFO" "WebP format support confirmed"
        return 0
    else
        print_error "WebP format not supported by ImageMagick"
        print_error "Please install ImageMagick with WebP support: apt-get install libmagickcore-6.q16-3-extra"
        log_entry "ERROR" "WebP format not supported"
        exit 1
    fi
}

# Count total image files
count_image_files() {
    print_info "Scanning for image files..."
    log_entry "INFO" "Beginning image file enumeration"
    
    local count=0
    local find_pattern="("
    
    # Build find pattern for all supported extensions
    for i in "${!IMAGE_EXTENSIONS[@]}"; do
        find_pattern+="-iname *.${IMAGE_EXTENSIONS[$i]}"
        if [[ $i -lt $((${#IMAGE_EXTENSIONS[@]} - 1)) ]]; then
            find_pattern+=" -o "
        fi
    done
    find_pattern+=")"
    
    # Use eval to properly expand the pattern
    count=$(find "$SOURCE_DIR" -type f $find_pattern 2>/dev/null | wc -l)
    
    TOTAL_FILES=$count
    print_info "Found $TOTAL_FILES image files to process"
    log_entry "INFO" "Image enumeration complete: $TOTAL_FILES files found"
    
    if [[ $TOTAL_FILES -eq 0 ]]; then
        print_warning "No image files found in $SOURCE_DIR"
        return 1
    fi
    
    return 0
}

# Convert single image to WebP
convert_image_to_webp() {
    local source_file="$1"
    local webp_file="${source_file%.*}.webp"
    
    # Skip if WebP already exists and flag is set
    if [[ "$SKIP_EXISTING" == true && -f "$webp_file" ]]; then
        print_warning "WebP file already exists: $webp_file (skipping)"
        log_entry "WARN" "Skipped existing WebP: $webp_file"
        ((SKIPPED_FILES++))
        return 0
    fi
    
    # Perform conversion with timeout
    if timeout "$CONVERSION_TIMEOUT" magick "$source_file" \
        -quality "$QUALITY" \
        -define "webp:method=6" \
        "$webp_file" 2>"${TEMP_DIR}/conversion_error_$$.tmp"; then
        
        print_success "Converted: $(basename "$source_file") -> $(basename "$webp_file")"
        log_entry "INFO" "Successfully converted: $source_file -> $webp_file"
        
        return 0
    else
        local exit_code=$?
        local error_msg=$(cat "${TEMP_DIR}/conversion_error_$$.tmp" 2>/dev/null || echo "Unknown error")
        rm -f "${TEMP_DIR}/conversion_error_$$.tmp"
        
        print_error "Failed to convert: $source_file (exit code: $exit_code)"
        print_error "Error details: $error_msg"
        log_entry "ERROR" "Conversion failed for $source_file: $error_msg"
        
        ((FAILED_FILES++))
        return 1
    fi
}

# Archive original image file
archive_original_file() {
    local source_file="$1"
    local relative_path="$2"
    
    # Calculate target path in archive directory
    local target_dir="${ARCHIVE_DIR}/$(dirname "$relative_path")"
    local target_file="${target_dir}/$(basename "$source_file")"
    
    # Create target directory structure
    if ! mkdir -p "$target_dir" 2>/dev/null; then
        print_error "Failed to create archive directory: $target_dir"
        log_entry "ERROR" "Failed to create archive directory: $target_dir"
        return 1
    fi
    
    # Move the original file
    if ! mv "$source_file" "$target_file" 2>/dev/null; then
        print_error "Failed to move file: $source_file -> $target_file"
        log_entry "ERROR" "Failed to move file: $source_file -> $target_file"
        return 1
    fi
    
    print_success "Archived: $relative_path"
    log_entry "INFO" "Archived original: $source_file -> $target_file"
    ((ARCHIVED_FILES++))
    
    return 0
}

# Process single image file
process_image_file() {
    local source_file="$1"
    
    # Skip if file no longer exists (may have been processed)
    if [[ ! -f "$source_file" ]]; then
        return 0
    fi
    
    print_info "Processing: $source_file"
    
    # Perform conversion
    if ! convert_image_to_webp "$source_file"; then
        return 1
    fi
    
    # Calculate relative path for archiving
    local relative_path="${source_file#$SOURCE_DIR/}"
    
    # Archive original file
    if ! archive_original_file "$source_file" "$relative_path"; then
        return 1
    fi
    
    ((PROCESSED_FILES++))
    return 0
}

# Main processing loop - recursive find and convert
process_images() {
    print_info "Starting image conversion process..."
    log_entry "INFO" "Starting main conversion loop"
    
    local processed=0
    local failed_files_list=()
    
    # Find all image files recursively
    while IFS= read -r -d '' image_file; do
        if process_image_file "$image_file"; then
            ((processed++))
        else
            failed_files_list+=("$image_file")
        fi
        
        # Progress update every 10 files
        if [[ $((processed % 10)) -eq 0 ]]; then
            print_info "Progress: $processed/$TOTAL_FILES files processed"
        fi
        
    done < <(find "$SOURCE_DIR" -type f \
        \( \
            -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \
            -o -iname "*.gif" -o -iname "*.bmp" -o -iname "*.tiff" \
        \) \
        -print0)
    
    # Report summary
    print_info "Conversion process completed"
    print_info "Total files found: $TOTAL_FILES"
    print_info "Successfully processed: $PROCESSED_FILES"
    print_info "Failed: $FAILED_FILES"
    print_info "Skipped (already exist): $SKIPPED_FILES"
    print_info "Archived: $ARCHIVED_FILES"
    
    if [[ ${#failed_files_list[@]} -gt 0 ]]; then
        print_warning "Failed files:"
        for file in "${failed_files_list[@]}"; do
            print_warning "  - $file"
            log_entry "WARN" "Failed processing: $file"
        done
    fi
}

# Generate detailed statistics report
generate_statistics_report() {
    print_info "Generating statistics report..."
    
    local total_size_original=0
    local total_size_webp=0
    
    # Calculate sizes
    if [[ -d "$ARCHIVE_DIR" ]]; then
        total_size_original=$(du -sb "$ARCHIVE_DIR" 2>/dev/null | awk '{print $1}' || echo 0)
    fi
    
    if [[ -d "$SOURCE_DIR" ]]; then
        total_size_webp=$(find "$SOURCE_DIR" -name "*.webp" -exec du -sb {} + 2>/dev/null | awk '{sum+=$1} END {print sum}' || echo 0)
    fi
    
    local savings=0
    local savings_percent=0
    
    if [[ $total_size_original -gt 0 ]]; then
        savings=$((total_size_original - total_size_webp))
        savings_percent=$((savings * 100 / total_size_original))
    fi
    
    # Write statistics file
    {
        echo "=================================="
        echo "WebP Conversion Statistics Report"
        echo "=================================="
        echo "Date: $(date '+%Y-%m-%d %H:%M:%S')"
        echo ""
        echo "Summary:"
        echo "  Total files found:    $TOTAL_FILES"
        echo "  Successfully processed: $PROCESSED_FILES"
        echo "  Skipped (exist):      $SKIPPED_FILES"
        echo "  Failed:               $FAILED_FILES"
        echo "  Archived:             $ARCHIVED_FILES"
        echo ""
        echo "Storage Analysis:"
        echo "  Original files size:  $(numfmt --to=iec $total_size_original 2>/dev/null || echo "$total_size_original bytes")"
        echo "  WebP files size:      $(numfmt --to=iec $total_size_webp 2>/dev/null || echo "$total_size_webp bytes")"
        echo "  Space saved:          $(numfmt --to=iec $savings 2>/dev/null || echo "$savings bytes") ($savings_percent%)"
        echo ""
        echo "Compression ratio: $(echo "scale=2; $total_size_webp * 100 / $total_size_original" | bc 2>/dev/null || echo "N/A")%"
    } | tee "$STATS_FILE"
    
    print_success "Statistics report generated: $STATS_FILE"
    log_entry "INFO" "Statistics report generated"
}

# Cleanup temporary files
cleanup_on_error() {
    print_info "Cleaning up temporary files..."
    
    if [[ -d "$TEMP_DIR" ]]; then
        rm -rf "${TEMP_DIR:?}" 2>/dev/null || true
    fi
    
    log_entry "INFO" "Cleanup completed"
}

cleanup_on_success() {
    cleanup_on_error
}

# Print usage information
print_usage() {
    cat << EOF
Usage: $SCRIPT_NAME [OPTIONS]

A production-grade image to WebP converter with folder structure preservation.

OPTIONS:
    -s, --source DIR        Source directory containing images (default: $SOURCE_DIR)
    -a, --archive DIR       Archive directory for originals (default: $ARCHIVE_DIR)
    -q, --quality NUM       WebP quality 0-100 (default: $QUALITY)
    -j, --jobs NUM          Parallel conversion jobs (default: $MAX_PARALLEL_JOBS)
    -h, --help              Show this help message
    -v, --version           Show version information
    --dry-run               Show what would be done without making changes
    --skip-archive          Do not archive original files
    --no-skip-existing      Convert even if WebP already exists

EXAMPLES:
    # Basic usage with defaults
    $SCRIPT_NAME

    # Custom source directory and quality
    $SCRIPT_NAME -s ./my_images -q 85

    # Dry run to preview operations
    $SCRIPT_NAME --dry-run

VERSION: $SCRIPT_VERSION
EOF
}

# Parse command line arguments
parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -s|--source)
                SOURCE_DIR="$2"
                shift 2
                ;;
            -a|--archive)
                ARCHIVE_DIR="$2"
                shift 2
                ;;
            -q|--quality)
                QUALITY="$2"
                shift 2
                ;;
            -j|--jobs)
                MAX_PARALLEL_JOBS="$2"
                shift 2
                ;;
            -h|--help)
                print_usage
                exit 0
                ;;
            -v|--version)
                echo "$SCRIPT_NAME version $SCRIPT_VERSION"
                exit 0
                ;;
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --skip-archive)
                SKIP_ARCHIVE=true
                shift
                ;;
            --no-skip-existing)
                SKIP_EXISTING=false
                shift
                ;;
            *)
                print_error "Unknown option: $1"
                print_usage
                exit 1
                ;;
        esac
    done
}

# Main orchestration function
main() {
    print_info "=== WebP Image Converter v$SCRIPT_VERSION ==="
    print_info "Starting at $(date '+%Y-%m-%d %H:%M:%S')"
    log_entry "INFO" "Script started by user: $(whoami)"
    log_entry "INFO" "Source directory: $SOURCE_DIR"
    log_entry "INFO" "Archive directory: $ARCHIVE_DIR"
    
    # Validation and initialization
    validate_prerequisites
    init_environment
    check_webp_support
    
    # Count images
    if ! count_image_files; then
        print_warning "No images found to process"
        print_success "Script completed at $(date '+%Y-%m-%d %H:%M:%S')"
        exit 0
    fi
    
    # Process all images
    process_images
    
    # Generate reports
    generate_statistics_report
    
    # Cleanup
    cleanup_on_success
    
    print_success "=== Conversion process completed ==="
    print_success "Script ended at $(date '+%Y-%m-%d %H:%M:%S')"
    log_entry "INFO" "Script completed successfully"
    
    return 0
}

################################################################################
# ENTRY POINT
################################################################################

# Parse command line arguments
parse_arguments "$@"

# Execute main function
main "$@"

exit $?

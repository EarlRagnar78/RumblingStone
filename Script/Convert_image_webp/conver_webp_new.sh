#!/usr/bin/env bash

################################################################################
# IMAGE TO WEBP CONVERTER - FIXED VERSION
# 
# Purpose: Recursively find image files, convert to WebP, archive originals
# Fixes: Corrected find syntax, implemented dry-run, absolute path handling
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
readonly SCRIPT_VERSION="1.1-fixed"

# Paths - Defaults
WORK_DIR="${PWD}"
SOURCE_DIR="${WORK_DIR}/Script"
ARCHIVE_DIR="${WORK_DIR}/Script/Original_images"
LOG_DIR="${WORK_DIR}/logs"
TEMP_DIR="${WORK_DIR}/.conversion_temp"

# Logging configuration
readonly LOG_FILE="${LOG_DIR}/webp_conversion_$(date +%Y%m%d_%H%M%S).log"
readonly ERROR_LOG="${LOG_DIR}/webp_conversion_errors_$(date +%Y%m%d_%H%M%S).log"
readonly STATS_FILE="${LOG_DIR}/conversion_stats_$(date +%Y%m%d_%H%M%S).txt"

# Conversion parameters
readonly QUALITY=90
readonly COMPRESSION_LEVEL=6
readonly IMAGE_EXTENSIONS=("jpg" "jpeg" "png" "gif" "bmp" "tiff" "webp")

# Processing parameters
MAX_PARALLEL_JOBS=4
CONVERSION_TIMEOUT=300
SKIP_EXISTING=true
SKIP_ARCHIVE=false
DRY_RUN=false

# Statistics counters
TOTAL_FILES=0
PROCESSED_FILES=0
FAILED_FILES=0
SKIPPED_FILES=0
ARCHIVED_FILES=0

################################################################################
# FUNCTION DEFINITIONS
################################################################################

print_info() { echo -e "${BLUE}[INFO]${NC} $*" | tee -a "$LOG_FILE"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $*" | tee -a "$LOG_FILE"; }
print_warning() { echo -e "${YELLOW}[WARN]${NC} $*" | tee -a "$LOG_FILE"; }
print_error() { echo -e "${RED}[ERROR]${NC} $*" | tee -a "$LOG_FILE" "$ERROR_LOG"; }

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

error_exit() {
    local line_num="$1"
    local exit_code="$2"
    local error_msg="${3:-Unknown error}"
    print_error "Script failed at line ${line_num} with exit code ${exit_code}"
    log_entry "ERROR" "Script failed at line ${line_num}: ${error_msg}"
    cleanup_on_error
    exit "${exit_code}"
}

trap 'error_exit ${LINENO} $?' ERR
trap 'handle_interrupt' INT TERM

handle_interrupt() {
    print_warning "Script interrupted by user"
    cleanup_on_error
    exit 130
}

validate_prerequisites() {
    local missing_tools=()
    print_info "Validating prerequisites..."
    for cmd in find magick convert identify mkdir; do
        if ! command -v "$cmd" &> /dev/null; then
            missing_tools+=("$cmd")
        fi
    done
    if [[ ${#missing_tools[@]} -gt 0 ]]; then
        print_error "Missing required tools: ${missing_tools[*]}"
        exit 1
    fi
    print_success "All prerequisites validated"
}

init_environment() {
    print_info "Initializing environment..."
    
    mkdir -p "$LOG_DIR" "$TEMP_DIR" "$ARCHIVE_DIR"
    
    if [[ ! -d "$SOURCE_DIR" ]]; then
        print_error "Source directory does not exist: $SOURCE_DIR"
        exit 1
    fi

    # --- FIX: Convert to absolute paths to handle relative inputs like ../../ ---
    SOURCE_DIR=$(cd "$SOURCE_DIR" && pwd)
    ARCHIVE_DIR=$(cd "$ARCHIVE_DIR" && pwd)
    # --------------------------------------------------------------------------

    print_info "Log file: $LOG_FILE"
    print_info "Source (Absolute): $SOURCE_DIR"
    print_info "Archive (Absolute): $ARCHIVE_DIR"
    
    if [[ "$DRY_RUN" == "true" ]]; then
        print_warning "!!! RUNNING IN DRY-RUN MODE - NO CHANGES WILL BE MADE !!!"
    fi
}

check_webp_support() {
    print_info "Checking WebP support..."
    if identify -list format 2>/dev/null | grep -qi "webp"; then
        print_success "WebP support detected"
    else
        print_error "WebP format not supported by ImageMagick"
        exit 1
    fi
}

# --- FIXED FUNCTION: Uses Arrays to safely build find command ---
count_image_files() {
    print_info "Scanning for image files..."
    local count=0
    
    # Build find arguments safely using an array
    local -a find_args=()
    find_args+=( "(" )
    for i in "${!IMAGE_EXTENSIONS[@]}"; do
        find_args+=( "-iname" "*.${IMAGE_EXTENSIONS[$i]}" )
        if [[ $i -lt $((${#IMAGE_EXTENSIONS[@]} - 1)) ]]; then
            find_args+=( "-o" )
        fi
    done
    find_args+=( ")" )
    
    # Run find with the array
    count=$(find "$SOURCE_DIR" -type f "${find_args[@]}" 2>/dev/null | wc -l)
    
    TOTAL_FILES=$count
    print_info "Found $TOTAL_FILES image files to process"
    
    if [[ $TOTAL_FILES -eq 0 ]]; then
        print_warning "No image files found in $SOURCE_DIR"
        return 1
    fi
    return 0
}

convert_image_to_webp() {
    local source_file="$1"
    local webp_file="${source_file%.*}.webp"
    
    if [[ "$SKIP_EXISTING" == true && -f "$webp_file" ]]; then
        print_warning "Skipping existing: $webp_file"
        ((SKIPPED_FILES++))
        return 0
    fi
    
    # --- FIX: Implement Dry Run ---
    if [[ "$DRY_RUN" == "true" ]]; then
        print_info "[DRY-RUN] Convert: $source_file -> $webp_file"
        return 0
    fi
    
    if timeout "$CONVERSION_TIMEOUT" magick "$source_file" \
        -quality "$QUALITY" -define "webp:method=6" \
        "$webp_file" 2>"${TEMP_DIR}/conversion_error_$$.tmp"; then
        
        print_success "Converted: $(basename "$source_file")"
        log_entry "INFO" "Converted: $source_file"
        return 0
    else
        local error_msg=$(cat "${TEMP_DIR}/conversion_error_$$.tmp" 2>/dev/null || echo "Unknown error")
        rm -f "${TEMP_DIR}/conversion_error_$$.tmp"
        print_error "Failed: $source_file - $error_msg"
        ((FAILED_FILES++))
        return 1
    fi
}

archive_original_file() {
    local source_file="$1"
    local relative_path="$2"
    
    if [[ "$SKIP_ARCHIVE" == "true" ]]; then
        return 0
    fi

    local target_dir="${ARCHIVE_DIR}/$(dirname "$relative_path")"
    local target_file="${target_dir}/$(basename "$source_file")"
    
    # --- FIX: Implement Dry Run ---
    if [[ "$DRY_RUN" == "true" ]]; then
        print_info "[DRY-RUN] Archive: $source_file -> $target_file"
        ((ARCHIVED_FILES++))
        return 0
    fi

    if ! mkdir -p "$target_dir" 2>/dev/null; then
        print_error "Failed to create dir: $target_dir"
        return 1
    fi
    
    if ! mv "$source_file" "$target_file" 2>/dev/null; then
        print_error "Failed to move: $source_file"
        return 1
    fi
    
    print_success "Archived: $relative_path"
    ((ARCHIVED_FILES++))
    return 0
}

process_image_file() {
    local source_file="$1"
    
    if [[ ! -f "$source_file" ]]; then return 0; fi
    
    # Calculate relative path BEFORE conversion for consistent logging
    local relative_path="${source_file#$SOURCE_DIR/}"

    if ! convert_image_to_webp "$source_file"; then
        return 1
    fi
    
    if ! archive_original_file "$source_file" "$relative_path"; then
        return 1
    fi
    
    ((PROCESSED_FILES++))
    return 0
}

# --- FIXED FUNCTION: Uses Arrays for Find & process substitution ---
process_images() {
    print_info "Starting image conversion process..."
    
    local processed=0
    local failed_files_list=()
    
    # Rebuild find args
    local -a find_args=()
    find_args+=( "(" )
    for i in "${!IMAGE_EXTENSIONS[@]}"; do
        find_args+=( "-iname" "*.${IMAGE_EXTENSIONS[$i]}" )
        if [[ $i -lt $((${#IMAGE_EXTENSIONS[@]} - 1)) ]]; then
            find_args+=( "-o" )
        fi
    done
    find_args+=( ")" )
    
    # Use process substitution to feed the while loop
    while IFS= read -r -d '' image_file; do
        if process_image_file "$image_file"; then
            ((processed++))
        else
            failed_files_list+=("$image_file")
        fi
        
        if [[ $((processed % 10)) -eq 0 ]]; then
            print_info "Progress: $processed/$TOTAL_FILES processed"
        fi
        
    done < <(find "$SOURCE_DIR" -type f "${find_args[@]}" -print0)
    
    print_info "Process completed. Processed: $PROCESSED_FILES, Failed: $FAILED_FILES"
}

generate_statistics_report() {
    print_info "Generating stats report..."
    
    # Don't calc sizes in dry run as nothing moved
    if [[ "$DRY_RUN" == "true" ]]; then
        echo "Dry Run - No statistics available" > "$STATS_FILE"
        return
    fi

    local total_size_original=0
    local total_size_webp=0
    
    if [[ -d "$ARCHIVE_DIR" ]]; then
        total_size_original=$(du -sb "$ARCHIVE_DIR" 2>/dev/null | awk '{print $1}' || echo 0)
    fi
    
    if [[ -d "$SOURCE_DIR" ]]; then
        total_size_webp=$(find "$SOURCE_DIR" -name "*.webp" -exec du -sb {} + 2>/dev/null | awk '{sum+=$1} END {print sum}' || echo 0)
    fi
    
    {
        echo "WebP Conversion Report - $(date)"
        echo "Total: $TOTAL_FILES | Processed: $PROCESSED_FILES | Failed: $FAILED_FILES"
        echo "Original Size: $(numfmt --to=iec $total_size_original)"
        echo "WebP Size:     $(numfmt --to=iec $total_size_webp)"
    } | tee "$STATS_FILE"
}

cleanup_on_error() {
    if [[ -d "$TEMP_DIR" ]]; then rm -rf "${TEMP_DIR:?}" 2>/dev/null || true; fi
}

cleanup_on_success() { cleanup_on_error; }

print_usage() {
    cat << EOF
Usage: $SCRIPT_NAME [OPTIONS]
OPTIONS:
    -s, --source DIR        Source directory (default: $SOURCE_DIR)
    -a, --archive DIR       Archive directory (default: $ARCHIVE_DIR)
    -q, --quality NUM       WebP quality 0-100 (default: $QUALITY)
    -j, --jobs NUM          Parallel jobs (default: $MAX_PARALLEL_JOBS)
    --dry-run               Show what would be done (Safe Mode)
    --skip-archive          Do not archive original files
    --no-skip-existing      Convert even if WebP already exists
EOF
}

parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -s|--source) SOURCE_DIR="$2"; shift 2 ;;
            -a|--archive) ARCHIVE_DIR="$2"; shift 2 ;;
            -q|--quality) QUALITY="$2"; shift 2 ;;
            -j|--jobs) MAX_PARALLEL_JOBS="$2"; shift 2 ;;
            -h|--help) print_usage; exit 0 ;;
            --dry-run) DRY_RUN=true; shift ;;
            --skip-archive) SKIP_ARCHIVE=true; shift ;;
            --no-skip-existing) SKIP_EXISTING=false; shift ;;
            *) print_error "Unknown option: $1"; print_usage; exit 1 ;;
        esac
    done
}

main() {
    parse_arguments "$@"
    
    print_info "=== WebP Image Converter v$SCRIPT_VERSION ==="
    log_entry "INFO" "Started with args: $@"
    
    validate_prerequisites
    init_environment
    check_webp_support
    
    if ! count_image_files; then
        print_success "No images found. Exiting."
        exit 0
    fi
    
    process_images
    generate_statistics_report
    cleanup_on_success
    
    print_success "=== Completed Successfully ==="
}

main "$@"
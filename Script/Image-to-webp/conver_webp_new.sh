#!/usr/bin/env bash

################################################################################
# IMAGE TO WEBP CONVERTER - UPDATED (exclude images referenced by HTML pages)
# 
# Purpose: Recursively find image files, convert to WebP, archive originals
# New: Exclude images that are referenced from HTML (.html/.htm) files.
# Fixes: safer path canonicalization, builds exclusion list from HTML files,
#        ensures counts exclude HTML-referenced images, preserves dry-run.
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
readonly SCRIPT_VERSION="1.2-exclude-html"

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
QUALITY=90
readonly COMPRESSION_LEVEL=6
readonly IMAGE_EXTENSIONS=("jpg" "jpeg" "png" "gif" "bmp" "tiff" "webp")

# Processing parameters
MAX_PARALLEL_JOBS=4
CONVERSION_TIMEOUT=300
SKIP_EXISTING=true
SKIP_ARCHIVE=false
DRY_RUN=false
EXCLUDE_HTML=true   # NEW: by default exclude images referenced from HTML pages
EXCLUDE_SUBFOLDERS=()  # Array of subfolder patterns to exclude from processing

# Statistics counters
TOTAL_FILES=0
PROCESSED_FILES=0
FAILED_FILES=0
SKIPPED_FILES=0
ARCHIVED_FILES=0

# Temp file for skip list (populated by build_html_image_exclusion_list)
SKIP_LIST_FILE=""
# Associative array for efficient HTML exclusion lookups
declare -A HTML_EXCLUDED_FILES
# Associative array for excluded subfolders (for efficient lookups)
declare -A EXCLUDED_SUBFOLDERS

################################################################################
# UTILS
################################################################################

print_info() { echo -e "${BLUE}[INFO]${NC} $*" | tee -a "$LOG_FILE"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $*" | tee -a "$LOG_FILE"; }
print_warning() { echo -e "${YELLOW}[WARN]${NC} $*" | tee -a "$LOG_FILE"; }
print_error() { echo -e "${RED}[ERROR]${NC} $*" | tee -a "$LOG_FILE" "$ERROR_LOG"; }

log_entry() {
    local level="$1"
    shift
    local message="$*"
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[${timestamp}] [${level}] ${message}" >> "$LOG_FILE"
    if [[ "$level" == "ERROR" ]]; then
        echo "[${timestamp}] [${level}] ${message}" >> "$ERROR_LOG"
    fi
}

error_exit() {
    local line_num="$1"
    local exit_code="$2"
    local error_msg="${3:-Unknown error}"
    
    # Don't trigger error handling if we're already in cleanup
    if [[ "${IN_ERROR_HANDLER:-}" == "true" ]]; then
        exit "${exit_code}"
    fi
    
    IN_ERROR_HANDLER="true"
    print_error "Script failed at line ${line_num} with exit code ${exit_code}"
    log_entry "ERROR" "Script failed at line ${line_num}: ${error_msg}" 2>/dev/null || true
    cleanup_on_error
    exit "${exit_code}"
}

trap 'error_exit ${LINENO} $?' ERR
trap 'handle_interrupt' INT TERM

handle_interrupt() {
    print_warning "Script interrupted by user"
    print_info "Cleaning up temporary files..."
    
    # Kill any running background processes
    local pids
    if pids=$(jobs -p 2>/dev/null); then
        if [[ -n "$pids" ]]; then
            print_info "Terminating background processes..."
            # shellcheck disable=SC2086
            kill $pids 2>/dev/null || true
            sleep 2
            # shellcheck disable=SC2086
            kill -9 $pids 2>/dev/null || true
        fi
    fi
    
    cleanup_on_error
    exit 130
}

# Resolve canonical/absolute path robustly (fallback to python if readlink isn't available)
canonicalize_path() {
    local path="$1"
    local base="${2:-}"   # optional base (for relative paths)
    
    if command -v readlink &>/dev/null; then
        if [[ -n "$base" ]]; then
            # If path is absolute already, use it; else combine with base
            if [[ "$path" == /* ]]; then
                readlink -f "$path"
            else
                readlink -f "${base%/}/$path"
            fi
        else
            readlink -f "$path"
        fi
    elif command -v python3 &>/dev/null; then
        # Fallback using python3
        if [[ -n "$base" ]]; then
            python3 -c "import os,sys; print(os.path.abspath(os.path.join(sys.argv[2], sys.argv[1])))" "$path" "$base"
        else
            python3 -c "import os,sys; print(os.path.abspath(sys.argv[1]))" "$path"
        fi
    else
        # Last resort: simple concatenation
        if [[ -n "$base" ]]; then
            if [[ "$path" == /* ]]; then
                echo "$path"
            else
                echo "${base%/}/$path"
            fi
        else
            echo "$path"
        fi
    fi
}

################################################################################
# PREREQUISITES & ENV
################################################################################

validate_prerequisites() {
    local missing_tools=()
    print_info "Validating prerequisites..."
    
    # Check required commands
    local required_commands=("find" "magick" "identify" "mkdir" "grep" "awk" "sed" "sort" "uniq" "timeout" "mv" "du" "wc")
    for cmd in "${required_commands[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            missing_tools+=("$cmd")
        fi
    done
    
    # Check optional commands with fallbacks
    if ! command -v "readlink" &> /dev/null && ! command -v "python3" &> /dev/null; then
        missing_tools+=("readlink or python3")
    fi
    
    if ! command -v "numfmt" &> /dev/null; then
        print_warning "numfmt not available - file sizes will be shown in bytes"
    fi
    
    if [[ ${#missing_tools[@]} -gt 0 ]]; then
        print_error "Missing required tools: ${missing_tools[*]}"
        print_error "Please install the missing tools and try again"
        exit 1
    fi
    
    # Validate ImageMagick version and capabilities
    local magick_version
    if magick_version=$(magick -version 2>/dev/null | head -1); then
        print_info "ImageMagick: $magick_version"
    else
        print_error "ImageMagick not properly installed or not working"
        exit 1
    fi
    
    print_success "All prerequisites validated"
}

init_environment() {
    print_info "Initializing environment..."
    
    # Validate and create directories with proper error handling
    local dirs_to_create=("$LOG_DIR" "$TEMP_DIR")
    for dir in "${dirs_to_create[@]}"; do
        if ! mkdir -p "$dir" 2>/dev/null; then
            print_error "Failed to create directory: $dir"
            exit 1
        fi
    done
    
    # Validate source directory exists and is readable
    if [[ ! -d "$SOURCE_DIR" ]]; then
        print_error "Source directory does not exist: $SOURCE_DIR"
        exit 1
    fi
    
    if [[ ! -r "$SOURCE_DIR" ]]; then
        print_error "Source directory is not readable: $SOURCE_DIR"
        exit 1
    fi
    
    # Create archive directory if it doesn't exist
    if ! mkdir -p "$ARCHIVE_DIR" 2>/dev/null; then
        print_error "Failed to create archive directory: $ARCHIVE_DIR"
        exit 1
    fi

    # Convert to absolute paths to handle relative inputs like ../../
    SOURCE_DIR=$(cd "$SOURCE_DIR" && pwd) || {
        print_error "Failed to resolve source directory path"
        exit 1
    }
    
    ARCHIVE_DIR=$(cd "$ARCHIVE_DIR" && pwd) || {
        print_error "Failed to resolve archive directory path"
        exit 1
    }
    
    TEMP_DIR=$(cd "$TEMP_DIR" && pwd) || {
        print_error "Failed to resolve temp directory path"
        exit 1
    }
    
    SKIP_LIST_FILE="${TEMP_DIR}/skip_images.lst"
    
    # Validate disk space (warn if less than 1GB free)
    local available_space
    if available_space=$(df "$SOURCE_DIR" 2>/dev/null | awk 'NR==2 {print $4}'); then
        if [[ $available_space -lt 1048576 ]]; then  # Less than 1GB in KB
            print_warning "Low disk space available: $(numfmt --to=iec $((available_space * 1024)) 2>/dev/null || echo "${available_space}KB")"
        fi
    fi

    print_info "Log file: $LOG_FILE"
    print_info "Source (Absolute): $SOURCE_DIR"
    print_info "Archive (Absolute): $ARCHIVE_DIR"
    print_info "Temp dir: $TEMP_DIR"
    
    if [[ "$DRY_RUN" == "true" ]]; then
        print_warning "!!! RUNNING IN DRY-RUN MODE - NO CHANGES WILL BE MADE !!!"
    fi

    if [[ "$EXCLUDE_HTML" == "true" ]]; then
        print_info "HTML-based exclusion is ENABLED"
    else
        print_info "HTML-based exclusion is DISABLED"
    fi
    
    if [[ ${#EXCLUDE_SUBFOLDERS[@]} -gt 0 ]]; then
        print_info "Subfolder exclusions: ${EXCLUDE_SUBFOLDERS[*]}"
    else
        print_info "No subfolder exclusions configured"
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

################################################################################
# HTML PARSING: build exclusion list of images referenced by HTML pages
################################################################################

# Build a regex pattern from IMAGE_EXTENSIONS array: jpg|jpeg|png|...
build_extension_pattern() {
    local IFS='|'
    echo "${IMAGE_EXTENSIONS[*]}"
}

build_html_image_exclusion_list() {
    if [[ "$EXCLUDE_HTML" != "true" ]]; then
        # Ensure skip list is empty
        : > "$SKIP_LIST_FILE"
        return 0
    fi

    print_info "Building HTML image exclusion list..."
    : > "$SKIP_LIST_FILE" || { print_error "Cannot write to $SKIP_LIST_FILE"; exit 1; }

    local ext_pattern
    ext_pattern=$(build_extension_pattern)

    # Find all html/htm files and extract image references via src and href attributes.
    while IFS= read -r -d '' html_file; do
        # Extract image references using a simpler, more maintainable approach
        # First extract src attributes - use simpler regex to avoid issues
        {
            grep -oiE 'src[[:space:]]*=[[:space:]]*["'"'"]*[^"'"'" >]+\.(jpg|jpeg|png|gif|bmp|tiff|webp)' "$html_file" 2>/dev/null || true
            grep -oiE 'href[[:space:]]*=[[:space:]]*["'"'"]*[^"'"'" >]+\.(jpg|jpeg|png|gif|bmp|tiff|webp)' "$html_file" 2>/dev/null || true
        } | sed -E 's/^(src|href)[[:space:]]*=[[:space:]]*["'"'"]*//i' | \
          sed -E 's/["'"'"]*$//' > "${TEMP_DIR}/_html_refs.tmp" 2>/dev/null || true

        # Process each reference found
        while IFS= read -r relpath; do
            [[ -z "$relpath" ]] && continue
            # Skip remote references
            if [[ "$relpath" =~ ^(https?:)?// ]]; then
                continue
            fi
            # Remove any query string or fragment
            relpath="${relpath%%\?*}"
            relpath="${relpath%%\#*}"
            local resolved=""
            if [[ "$relpath" == /* ]]; then
                # Treat leading slash as relative to SOURCE_DIR root (typical for site roots)
                resolved=$(canonicalize_path "${SOURCE_DIR%/}${relpath}")
            else
                resolved=$(canonicalize_path "$relpath" "$(dirname "$html_file")")
            fi
            # Only add if the referenced file actually exists
            if [[ -f "$resolved" ]]; then
                echo "$resolved" >> "$SKIP_LIST_FILE"
            fi
        done < "${TEMP_DIR}/_html_refs.tmp"

        # NEW: Auto-exclude corresponding _files folder for this HTML file
        local html_basename="$(basename "$html_file" .html)"
        html_basename="$(basename "$html_basename" .htm)"
        local files_folder="$(dirname "$html_file")/${html_basename}_files"
        if [[ -d "$files_folder" ]]; then
            print_info "Auto-excluding HTML assets folder: $files_folder"
            # Add all images in the _files folder to exclusion list
            while IFS= read -r -d '' img_in_folder; do
                echo "$img_in_folder" >> "$SKIP_LIST_FILE"
            done < <(find "$files_folder" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.gif" -o -iname "*.bmp" -o -iname "*.tiff" -o -iname "*.webp" \) -print0 2>/dev/null)
        fi

    done < <(find "$SOURCE_DIR" -type f \( -iname "*.html" -o -iname "*.htm" \) -print0 2>/dev/null)

    # Deduplicate and load into associative array for efficient lookups
    if [[ -f "$SKIP_LIST_FILE" ]]; then
        sort -u "$SKIP_LIST_FILE" -o "$SKIP_LIST_FILE" || true
        local skip_count=0
        while IFS= read -r excluded_file; do
            [[ -n "$excluded_file" ]] && HTML_EXCLUDED_FILES["$excluded_file"]=1 && skip_count=$((skip_count + 1))
        done < "$SKIP_LIST_FILE"
        print_info "Found ${skip_count} unique image(s) referenced from HTML pages to exclude"
    else
        print_info "No HTML-referenced images found"
    fi
}

is_image_excluded_by_html() {
    local img="$1"
    # Use associative array for O(1) lookup instead of O(n) grep
    [[ -n "${HTML_EXCLUDED_FILES[$img]:-}" ]]
}

# Check if a file path is in an excluded subfolder
is_in_excluded_subfolder() {
    local file_path="$1"
    
    # If no exclusions defined, nothing is excluded
    if [[ ${#EXCLUDE_SUBFOLDERS[@]} -eq 0 ]]; then
        return 1
    fi
    
    # Check each exclusion pattern
    for pattern in "${EXCLUDE_SUBFOLDERS[@]}"; do
        # Convert pattern to absolute path for comparison
        local abs_pattern
        if [[ "$pattern" == /* ]]; then
            abs_pattern="$pattern"
        else
            abs_pattern="${SOURCE_DIR%/}/$pattern"
        fi
        
        # Check if file path starts with the exclusion pattern
        if [[ "$file_path" == "$abs_pattern"* ]]; then
            return 0  # File is excluded
        fi
    done
    
    return 1  # File is not excluded
}

# Initialize excluded subfolders lookup
init_excluded_subfolders() {
    if [[ ${#EXCLUDE_SUBFOLDERS[@]} -eq 0 ]]; then
        return 0
    fi
    
    print_info "Initializing subfolder exclusions..."
    for pattern in "${EXCLUDE_SUBFOLDERS[@]}"; do
        local abs_pattern
        if [[ "$pattern" == /* ]]; then
            abs_pattern="$pattern"
        else
            abs_pattern="${SOURCE_DIR%/}/$pattern"
        fi
        EXCLUDED_SUBFOLDERS["$abs_pattern"]=1
        print_info "Excluding subfolder: $abs_pattern"
    done
}

################################################################################
# CORE FUNCTIONS
################################################################################

# Count image files but exclude HTML-referenced images when EXCLUDE_HTML=true
count_image_files() {
    print_info "Scanning for image files..."
    local count=0

    # Build find args safely using an array
    local -a find_args=()
    find_args+=( "(" )
    for i in "${!IMAGE_EXTENSIONS[@]}"; do
        find_args+=( "-iname" "*.${IMAGE_EXTENSIONS[$i]}" )
        if [[ $i -lt $((${#IMAGE_EXTENSIONS[@]} - 1)) ]]; then
            find_args+=( "-o" )
        fi
    done
    find_args+=( ")" )

    # iterate and count, skipping any HTML-referenced images and excluded subfolders
    while IFS= read -r -d '' file; do
        # Skip if in excluded subfolder
        if is_in_excluded_subfolder "$file"; then
            continue
        fi
        
        if [[ "$EXCLUDE_HTML" == "true" ]] && is_image_excluded_by_html "$file"; then
            # Don't increment SKIPPED_FILES here - will be counted in processing
            continue
        fi
        count=$((count + 1))
    done < <(find "$SOURCE_DIR" -type f "${find_args[@]}" -print0 2>/dev/null)

    TOTAL_FILES=$count
    print_info "Found $TOTAL_FILES image files to process (excluded: $SKIPPED_FILES via HTML references)"
    if [[ $TOTAL_FILES -eq 0 ]]; then
        print_warning "No image files to process in $SOURCE_DIR (after exclusions)"
        return 1
    fi
    return 0
}

convert_image_to_webp() {
    local source_file="$1"
    local webp_file="${source_file%.*}.webp"

    # Validate input file
    if [[ ! -f "$source_file" ]] || [[ ! -r "$source_file" ]]; then
        print_error "Source file not found or not readable: $source_file"
        FAILED_FILES=$((FAILED_FILES + 1))
        return 1
    fi

    if [[ "$SKIP_EXISTING" == true && -f "$webp_file" ]]; then
        print_warning "Skipping existing: $webp_file"
        SKIPPED_FILES=$((SKIPPED_FILES + 1))
        return 0
    fi

    # Skip if referenced in HTML (double-check)
    if [[ "$EXCLUDE_HTML" == "true" ]] && is_image_excluded_by_html "$source_file"; then
        print_info "[SKIP-HTML] Skipping referenced file: $source_file"
        SKIPPED_FILES=$((SKIPPED_FILES + 1))
        return 0
    fi

    # Implement Dry Run
    if [[ "$DRY_RUN" == "true" ]]; then
        print_info "[DRY-RUN] Convert: $source_file -> $webp_file"
        return 0
    fi

    # Check if output directory is writable
    local output_dir
    output_dir="$(dirname "$webp_file")"
    if [[ ! -w "$output_dir" ]]; then
        print_error "Output directory not writable: $output_dir"
        ((FAILED_FILES++))
        return 1
    fi

    # Run conversion with timeout; redirect stderr to temp
    local errtmp="${TEMP_DIR}/conversion_error_$$.tmp"
    if timeout "$CONVERSION_TIMEOUT" magick "$source_file" \
        -quality "$QUALITY" -define "webp:method=${COMPRESSION_LEVEL}" \
        "$webp_file" 2>"$errtmp"; then

        # Verify the output file was created and is valid
        if [[ -f "$webp_file" ]] && [[ -s "$webp_file" ]]; then
            print_success "Converted: $(basename "$source_file")"
            log_entry "INFO" "Converted: $source_file"
            rm -f "$errtmp" 2>/dev/null || true
            return 0
        else
            print_error "Conversion failed - output file empty or missing: $webp_file"
            rm -f "$webp_file" "$errtmp" 2>/dev/null || true
            FAILED_FILES=$((FAILED_FILES + 1))
            return 1
        fi
    else
        local exit_code=$?
        local error_msg
        error_msg=$(cat "$errtmp" 2>/dev/null || echo "Unknown error")
        rm -f "$errtmp" 2>/dev/null || true
        
        if [[ $exit_code -eq 124 ]]; then
            print_error "Conversion timeout (${CONVERSION_TIMEOUT}s): $source_file"
        else
            print_error "Failed: $source_file - $error_msg"
        fi
        FAILED_FILES=$((FAILED_FILES + 1))
        return 1
    fi
}

archive_original_file() {
    local source_file="$1"
    local relative_path="$2"

    if [[ "$SKIP_ARCHIVE" == "true" ]]; then
        return 0
    fi

    # Validate source file exists
    if [[ ! -f "$source_file" ]]; then
        print_error "Source file for archiving not found: $source_file"
        return 1
    fi

    local target_dir="${ARCHIVE_DIR}/$(dirname "$relative_path")"
    local target_file="${target_dir}/$(basename "$source_file")"

    # Dry Run
    if [[ "$DRY_RUN" == "true" ]]; then
        print_info "[DRY-RUN] Archive: $source_file -> $target_file"
        ARCHIVED_FILES=$((ARCHIVED_FILES + 1))
        return 0
    fi

    # Create target directory with proper error handling
    if ! mkdir -p "$target_dir" 2>/dev/null; then
        print_error "Failed to create archive directory: $target_dir"
        return 1
    fi

    # Check if target directory is writable
    if [[ ! -w "$target_dir" ]]; then
        print_error "Archive directory not writable: $target_dir"
        return 1
    fi

    # Use mv with better error handling
    if mv "$source_file" "$target_file" 2>/dev/null; then
        print_success "Archived: $relative_path"
        ARCHIVED_FILES=$((ARCHIVED_FILES + 1))
        return 0
    else
        local mv_exit_code=$?
        print_error "Failed to archive: $source_file -> $target_file (exit code: $mv_exit_code)"
        return 1
    fi
}

process_image_file() {
    local source_file="$1"

    if [[ ! -f "$source_file" ]]; then return 0; fi

    # Calculate relative path BEFORE conversion for consistent logging
    # Handle SOURCE_DIR with or without trailing slash
    local relative_path
    relative_path="${source_file#${SOURCE_DIR%/}/}"

    if ! convert_image_to_webp "$source_file"; then
        return 1
    fi

    # Only archive if conversion was successful and not in dry run
    if [[ "$DRY_RUN" != "true" ]]; then
        if ! archive_original_file "$source_file" "$relative_path"; then
            return 1
        fi
    else
        # In dry run, simulate archiving
        if [[ "$SKIP_ARCHIVE" != "true" ]]; then
            print_info "[DRY-RUN] Archive: $source_file -> ${ARCHIVE_DIR}/$relative_path"
            ARCHIVED_FILES=$((ARCHIVED_FILES + 1))
        fi
    fi

    PROCESSED_FILES=$((PROCESSED_FILES + 1))
    return 0
}

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
        # Skip if in excluded subfolder
        if is_in_excluded_subfolder "$image_file"; then
            SKIPPED_FILES=$((SKIPPED_FILES + 1))
            continue
        fi
        
        # Skip HTML-referenced images (single check here)
        if [[ "$EXCLUDE_HTML" == "true" ]] && is_image_excluded_by_html "$image_file"; then
            SKIPPED_FILES=$((SKIPPED_FILES + 1))
            continue
        fi

        if process_image_file "$image_file"; then
            processed=$((processed + 1))
        else
            failed_files_list+=("$image_file")
        fi

        if [[ $((processed % 10)) -eq 0 ]] && [[ $processed -gt 0 ]]; then
            print_info "Progress: $processed/$TOTAL_FILES processed"
        fi

    done < <(find "$SOURCE_DIR" -type f "${find_args[@]}" -print0)

    print_info "Process completed. Processed: $PROCESSED_FILES, Failed: $FAILED_FILES, Archived: $ARCHIVED_FILES, Skipped: $SKIPPED_FILES"
    if [[ ${#failed_files_list[@]} -gt 0 ]]; then
        print_warning "Some files failed during conversion (see error log)."
    fi
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
        echo "Total: $TOTAL_FILES | Processed: $PROCESSED_FILES | Failed: $FAILED_FILES | Archived: $ARCHIVED_FILES | Skipped: $SKIPPED_FILES"
        printf "Original Size: %s\n" "$(numfmt --to=iec $total_size_original 2>/dev/null || echo "${total_size_original} bytes")"
        printf "WebP Size:     %s\n" "$(numfmt --to=iec $total_size_webp 2>/dev/null || echo "${total_size_webp} bytes")"
    } | tee "$STATS_FILE"
}

cleanup_on_error() {
    # Prevent recursive cleanup calls
    if [[ "${IN_CLEANUP:-}" == "true" ]]; then
        return 0
    fi
    IN_CLEANUP="true"
    
    if [[ -d "$TEMP_DIR" ]]; then 
        rm -rf "${TEMP_DIR:?}" 2>/dev/null || true
    fi
    # Clear associative arrays
    unset HTML_EXCLUDED_FILES 2>/dev/null || true
    unset EXCLUDED_SUBFOLDERS 2>/dev/null || true
}

cleanup_on_success() { 
    cleanup_on_error
}

print_usage() {
    cat << EOF
Usage: $SCRIPT_NAME [OPTIONS]
OPTIONS:
    -s, --source DIR        Source directory (default: $SOURCE_DIR)
    -a, --archive DIR       Archive directory (default: $ARCHIVE_DIR)
    -q, --quality NUM       WebP quality 0-100 (default: $QUALITY)
    -j, --jobs NUM          Parallel jobs (default: $MAX_PARALLEL_JOBS)
    --exclude-subfolder DIR Exclude subfolder from processing (can be used multiple times)
    --dry-run               Show what would be done (Safe Mode)
    --skip-archive          Do not archive original files
    --no-skip-existing      Convert even if WebP already exists
    --no-exclude-html       Do NOT exclude images referenced from HTML files
    -h, --help              Show this help

EXAMPLES:
    $SCRIPT_NAME --exclude-subfolder "backup" --exclude-subfolder "temp"
    $SCRIPT_NAME --exclude-subfolder "/absolute/path/to/exclude"
EOF
}

parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -s|--source) 
                if [[ -z "${2:-}" ]]; then
                    print_error "Option $1 requires an argument"
                    exit 1
                fi
                SOURCE_DIR="$2"; shift 2 ;;
            -a|--archive) 
                if [[ -z "${2:-}" ]]; then
                    print_error "Option $1 requires an argument"
                    exit 1
                fi
                ARCHIVE_DIR="$2"; shift 2 ;;
            -q|--quality) 
                if [[ -z "${2:-}" ]] || ! [[ "$2" =~ ^[0-9]+$ ]] || [[ "$2" -lt 0 ]] || [[ "$2" -gt 100 ]]; then
                    print_error "Quality must be a number between 0-100"
                    exit 1
                fi
                QUALITY="$2"; shift 2 ;;
            -j|--jobs) 
                if [[ -z "${2:-}" ]] || ! [[ "$2" =~ ^[0-9]+$ ]] || [[ "$2" -lt 1 ]]; then
                    print_error "Jobs must be a positive integer"
                    exit 1
                fi
                MAX_PARALLEL_JOBS="$2"; shift 2 ;;
            --exclude-subfolder)
                if [[ -z "${2:-}" ]]; then
                    print_error "Option $1 requires an argument"
                    exit 1
                fi
                EXCLUDE_SUBFOLDERS+=("$2"); shift 2 ;;
            -h|--help) print_usage; exit 0 ;;
            --dry-run) DRY_RUN=true; shift ;;
            --skip-archive) SKIP_ARCHIVE=true; shift ;;
            --no-skip-existing) SKIP_EXISTING=false; shift ;;
            --no-exclude-html) EXCLUDE_HTML=false; shift ;;
            *) print_error "Unknown option: $1"; print_usage; exit 1 ;;
        esac
    done
}

main() {
    # Validate arguments first
    parse_arguments "$@"
    
    # Initialize logging before any other operations
    if ! touch "$LOG_FILE" 2>/dev/null; then
        echo "ERROR: Cannot create log file: $LOG_FILE" >&2
        exit 1
    fi

    print_info "=== WebP Image Converter v$SCRIPT_VERSION ==="
    print_info "Started at: $(date)"
    print_info "PID: $$"
    print_info "User: $(whoami)"
    print_info "Working directory: $(pwd)"
    log_entry "INFO" "Started with args: $*"

    # System validation and setup
    validate_prerequisites
    init_environment
    check_webp_support

    # Initialize excluded subfolders
    init_excluded_subfolders
    
    # Build list of HTML-referenced images to exclude (if enabled)
    build_html_image_exclusion_list

    # Count and validate files to process
    if ! count_image_files; then
        print_success "No images found to convert. Exiting."
        cleanup_on_success
        exit 0
    fi

    # Main processing
    local start_time
    start_time=$(date +%s)
    
    process_images
    
    local end_time
    end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    # Generate final report
    generate_statistics_report
    
    print_info "Processing completed in ${duration} seconds"
    print_success "=== Completed Successfully ==="
    log_entry "INFO" "Completed successfully in ${duration} seconds"
    
    cleanup_on_success
}

main "$@"
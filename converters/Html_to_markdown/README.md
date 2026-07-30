# HTML to Markdown Converter with WebP Image Processing

A robust, production-ready script that converts HTML files and directories to Markdown format while automatically converting images to optimized WebP format. Built following system engineering best practices for reliability, maintainability, and scalability.

## Features

- **Batch Processing**: Convert single files or entire directory structures
- **Image Optimization**: Automatic conversion to WebP format with configurable quality
- **Robust Error Handling**: Comprehensive logging and graceful failure recovery
- **Atomic Operations**: Safe conversions with rollback capability
- **Remote Image Support**: Downloads and processes images from URLs
- **Progress Tracking**: Detailed logging and conversion summaries
- **Configurable**: Extensive customization options
- **Cross-Platform**: Works on Linux, macOS, and Windows

## System Requirements

- Python 3.7 or higher
- Internet connection (for remote images)
- Sufficient disk space for image processing

## Quick Start

### 1. Automated Setup (Recommended)

```bash
# Clone or download the script files
# Run the automated setup
./setup.sh
```

### 2. Manual Installation

```bash
# Install dependencies
pip3 install -r requirements.txt

# Make script executable
chmod +x html_to_markdown_converter.py
```

## Usage

### Basic Usage

```bash
# Convert single file
./html_to_markdown_converter.py input.html output.md

# Convert entire directory
./html_to_markdown_converter.py html_folder/ markdown_folder/
```

### Advanced Usage

```bash
# High quality WebP conversion
./html_to_markdown_converter.py --quality 95 input.html output.md

# Lossless WebP compression
./html_to_markdown_converter.py --lossless input/ output/

# Custom image size limits
./html_to_markdown_converter.py --max-size 1920x1080 input/ output/

# Verbose logging
./html_to_markdown_converter.py --verbose input/ output/

# Custom timeout for remote images
./html_to_markdown_converter.py --timeout 60 input/ output/
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--quality` | WebP quality (0-100) | 85 |
| `--lossless` | Use lossless WebP compression | False |
| `--max-size` | Maximum image size (WxH) | 2048x2048 |
| `--timeout` | HTTP timeout for remote images (seconds) | 30 |
| `--verbose` | Enable verbose logging | False |

## Configuration

The script uses a configuration class that can be customized:

```python
class Config:
    webp_quality = 85          # WebP quality (0-100)
    webp_lossless = False      # Use lossless compression
    max_image_size = (2048, 2048)  # Max image dimensions
    supported_image_formats = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
    html_extensions = {'.html', '.htm'}
    timeout = 30               # HTTP timeout in seconds
    max_retries = 3           # Max retry attempts
```

## Output Structure

When converting directories, the script maintains the original structure:

```
input_folder/
├── page1.html
├── page2.html
├── images/
│   ├── photo1.jpg
│   └── photo2.png
└── subfolder/
    └── page3.html

output_folder/
├── page1.md
├── page1_images/
│   ├── photo1.webp
│   └── photo2.webp
├── page2.md
├── page2_images/
│   └── converted_images.webp
└── subfolder/
    ├── page3.md
    └── page3_images/
```

## Error Handling

The script implements comprehensive error handling:

- **Atomic Operations**: Uses temporary directories to ensure safe conversions
- **Rollback Capability**: Failed conversions don't leave partial results
- **Graceful Degradation**: Continues processing even if individual files fail
- **Detailed Logging**: Comprehensive logs for troubleshooting
- **Validation**: Input validation and configuration checks

## Performance Considerations

- **Memory Efficient**: Processes images one at a time
- **Concurrent Safe**: Can be run in parallel on different directories
- **Disk Space**: Temporary files are cleaned up automatically
- **Network Optimized**: Configurable timeouts and retry logic

## Troubleshooting

### Common Issues

1. **Missing Dependencies**
   ```bash
   pip3 install html2text pillow requests beautifulsoup4
   ```

2. **Permission Errors**
   ```bash
   chmod +x html_to_markdown_converter.py
   ```

3. **Python Version Issues**
   - Ensure Python 3.7+ is installed
   - Use `python3` instead of `python` if needed

4. **Image Processing Errors**
   - Check available disk space
   - Verify image file integrity
   - Increase timeout for large remote images

### Logging

Enable verbose logging for detailed troubleshooting:

```bash
./html_to_markdown_converter.py --verbose input/ output/
```

Log format: `YYYY-MM-DD HH:MM:SS - LEVEL - MESSAGE`

## Security Considerations

- **Input Validation**: All inputs are validated before processing
- **Safe File Operations**: Uses secure temporary directories
- **Network Security**: Configurable timeouts prevent hanging requests
- **Path Traversal Protection**: Prevents directory traversal attacks
- **Resource Limits**: Configurable limits prevent resource exhaustion

## Contributing

1. Follow PEP 8 style guidelines
2. Add comprehensive error handling
3. Include unit tests for new features
4. Update documentation
5. Test on multiple platforms

## License

This project is released under the MIT License. See LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs with `--verbose` flag
3. Create an issue with detailed error information

## Changelog

### v1.0.0
- Initial release
- HTML to Markdown conversion
- WebP image processing
- Directory batch processing
- Comprehensive error handling
- Atomic operations with rollback
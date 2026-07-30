# Deployment Instructions

This document provides comprehensive deployment instructions for the HTML to Markdown Converter across different environments and use cases.

## Table of Contents

- [Local Development Setup](#local-development-setup)
- [Production Deployment](#production-deployment)
- [Docker Deployment](#docker-deployment)
- [CI/CD Integration](#cicd-integration)
- [Server Deployment](#server-deployment)
- [Monitoring and Maintenance](#monitoring-and-maintenance)

## Local Development Setup

### Prerequisites

- Python 3.7+
- pip or pip3
- Git (optional)

### Quick Setup

```bash
# 1. Download/clone the project
git clone <repository-url>
cd html-to-markdown-converter

# 2. Run automated setup
./setup.sh

# 3. Test installation
./html_to_markdown_converter.py --help
```

### Manual Setup

```bash
# 1. Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Make executable
chmod +x html_to_markdown_converter.py

# 4. Test installation
python3 html_to_markdown_converter.py --help
```

## Production Deployment

### System Requirements

- **CPU**: 2+ cores recommended for batch processing
- **RAM**: 2GB minimum, 4GB+ recommended
- **Storage**: 10GB+ free space for temporary files
- **Network**: Stable internet connection for remote images

### Production Setup

```bash
# 1. Create dedicated user
sudo useradd -m -s /bin/bash htmlconverter
sudo su - htmlconverter

# 2. Install in user directory
mkdir -p ~/tools/html-converter
cd ~/tools/html-converter

# 3. Copy files
cp html_to_markdown_converter.py .
cp requirements.txt .
cp setup.sh .

# 4. Run setup
./setup.sh

# 5. Create production configuration
cat > config.py << 'EOF'
class ProductionConfig:
    webp_quality = 90
    webp_lossless = False
    max_image_size = (1920, 1080)
    timeout = 60
    max_retries = 5
    log_level = "INFO"
EOF
```

### System Service (Linux)

Create a systemd service for automated processing:

```bash
# Create service file
sudo tee /etc/systemd/system/html-converter.service << 'EOF'
[Unit]
Description=HTML to Markdown Converter Service
After=network.target

[Service]
Type=oneshot
User=htmlconverter
Group=htmlconverter
WorkingDirectory=/home/htmlconverter/tools/html-converter
ExecStart=/home/htmlconverter/tools/html-converter/html_to_markdown_converter.py /var/input /var/output
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable html-converter.service
```

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libjpeg-dev \
    libpng-dev \
    libwebp-dev \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN useradd -m -u 1000 converter
USER converter
WORKDIR /app

# Copy requirements and install dependencies
COPY --chown=converter:converter requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy application files
COPY --chown=converter:converter html_to_markdown_converter.py .
RUN chmod +x html_to_markdown_converter.py

# Create directories
RUN mkdir -p /app/input /app/output /app/temp

# Set environment variables
ENV PATH="/home/converter/.local/bin:${PATH}"
ENV PYTHONPATH="/app"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import html2text, PIL, requests, bs4; print('OK')" || exit 1

ENTRYPOINT ["./html_to_markdown_converter.py"]
CMD ["--help"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  html-converter:
    build: .
    container_name: html-converter
    volumes:
      - ./input:/app/input:ro
      - ./output:/app/output
      - ./temp:/app/temp
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
    command: ["--verbose", "/app/input", "/app/output"]
    
  # Optional: Web interface
  converter-web:
    build: .
    ports:
      - "8080:8080"
    volumes:
      - ./uploads:/app/input
      - ./downloads:/app/output
    command: ["python3", "-m", "http.server", "8080"]
```

### Build and Run

```bash
# Build image
docker build -t html-converter .

# Run single conversion
docker run --rm \
  -v $(pwd)/input:/app/input:ro \
  -v $(pwd)/output:/app/output \
  html-converter /app/input /app/output

# Run with docker-compose
docker-compose up -d
```

## CI/CD Integration

### GitHub Actions

```yaml
name: HTML Converter CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.7, 3.8, 3.9, '3.10']

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        python -m py_compile html_to_markdown_converter.py
        python -c "import html2text, PIL, requests, bs4"
    
    - name: Test conversion
      run: |
        echo '<html><body><h1>Test</h1><img src="test.jpg"></body></html>' > test.html
        python html_to_markdown_converter.py test.html test.md
        test -f test.md

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker image
      run: docker build -t html-converter:latest .
    
    - name: Deploy to production
      run: |
        # Add your deployment commands here
        echo "Deploying to production..."
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.9'
        DOCKER_IMAGE = 'html-converter'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Test') {
            steps {
                sh '''
                    . venv/bin/activate
                    python -m py_compile html_to_markdown_converter.py
                    python -c "import html2text, PIL, requests, bs4"
                '''
            }
        }
        
        stage('Build Docker') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE:$BUILD_NUMBER .'
                sh 'docker tag $DOCKER_IMAGE:$BUILD_NUMBER $DOCKER_IMAGE:latest'
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                    docker stop html-converter || true
                    docker rm html-converter || true
                    docker run -d --name html-converter \
                        -v /data/input:/app/input:ro \
                        -v /data/output:/app/output \
                        $DOCKER_IMAGE:latest
                '''
            }
        }
    }
    
    post {
        always {
            sh 'docker system prune -f'
        }
    }
}
```

## Server Deployment

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name converter.example.com;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /uploads {
        alias /var/www/html-converter/uploads;
        client_max_body_size 100M;
    }
    
    location /downloads {
        alias /var/www/html-converter/downloads;
        autoindex on;
    }
}
```

### Cron Job Setup

```bash
# Add to crontab for automated processing
crontab -e

# Process files every hour
0 * * * * /home/htmlconverter/tools/html-converter/html_to_markdown_converter.py /var/input /var/output >> /var/log/html-converter.log 2>&1

# Clean up old files daily
0 2 * * * find /var/output -name "*.md" -mtime +30 -delete
0 2 * * * find /tmp -name "html_converter_*" -mtime +1 -delete
```

## Monitoring and Maintenance

### Log Rotation

```bash
# Create logrotate configuration
sudo tee /etc/logrotate.d/html-converter << 'EOF'
/var/log/html-converter.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 htmlconverter htmlconverter
    postrotate
        systemctl reload html-converter || true
    endscript
}
EOF
```

### Health Check Script

```bash
#!/bin/bash
# health_check.sh

CONVERTER_PATH="/home/htmlconverter/tools/html-converter/html_to_markdown_converter.py"
TEST_HTML="<html><body><h1>Health Check</h1></body></html>"
TEST_DIR="/tmp/health_check_$$"

mkdir -p "$TEST_DIR"
echo "$TEST_HTML" > "$TEST_DIR/test.html"

if "$CONVERTER_PATH" "$TEST_DIR/test.html" "$TEST_DIR/test.md" &>/dev/null; then
    echo "OK: Converter is working"
    rm -rf "$TEST_DIR"
    exit 0
else
    echo "ERROR: Converter failed"
    rm -rf "$TEST_DIR"
    exit 1
fi
```

### Performance Monitoring

```bash
# Monitor script for resource usage
#!/bin/bash
# monitor.sh

while true; do
    if pgrep -f "html_to_markdown_converter.py" > /dev/null; then
        echo "$(date): Converter running"
        ps aux | grep html_to_markdown_converter.py | grep -v grep
        df -h /tmp
        free -h
    fi
    sleep 60
done
```

## Security Considerations

### File Permissions

```bash
# Set secure permissions
chmod 755 html_to_markdown_converter.py
chmod 644 requirements.txt
chmod 644 README.md

# Secure directories
chmod 750 /var/input
chmod 755 /var/output
chown -R htmlconverter:htmlconverter /var/input /var/output
```

### Firewall Rules

```bash
# Allow only necessary ports
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

### Resource Limits

```bash
# Add to /etc/security/limits.conf
htmlconverter soft nproc 100
htmlconverter hard nproc 200
htmlconverter soft nofile 1024
htmlconverter hard nofile 2048
htmlconverter soft fsize 1048576  # 1GB
```

## Backup and Recovery

### Backup Script

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backup/html-converter"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

# Backup configuration and scripts
tar -czf "$BACKUP_DIR/html-converter-$DATE.tar.gz" \
    /home/htmlconverter/tools/html-converter/ \
    /etc/systemd/system/html-converter.service \
    /etc/logrotate.d/html-converter

# Keep only last 30 days of backups
find "$BACKUP_DIR" -name "html-converter-*.tar.gz" -mtime +30 -delete
```

### Recovery Procedure

```bash
# 1. Stop service
sudo systemctl stop html-converter

# 2. Restore from backup
cd /
sudo tar -xzf /backup/html-converter/html-converter-YYYYMMDD_HHMMSS.tar.gz

# 3. Restore permissions
sudo chown -R htmlconverter:htmlconverter /home/htmlconverter/tools/html-converter/

# 4. Restart service
sudo systemctl start html-converter
sudo systemctl status html-converter
```

## Troubleshooting Deployment Issues

### Common Problems

1. **Permission Denied**
   ```bash
   chmod +x html_to_markdown_converter.py
   chown htmlconverter:htmlconverter html_to_markdown_converter.py
   ```

2. **Module Not Found**
   ```bash
   pip install -r requirements.txt --user
   export PYTHONPATH="/home/htmlconverter/.local/lib/python3.9/site-packages:$PYTHONPATH"
   ```

3. **Docker Build Fails**
   ```bash
   docker system prune -a
   docker build --no-cache -t html-converter .
   ```

4. **Service Won't Start**
   ```bash
   sudo journalctl -u html-converter.service -f
   sudo systemctl status html-converter.service
   ```

For additional support, check the main README.md file and enable verbose logging for detailed error information.
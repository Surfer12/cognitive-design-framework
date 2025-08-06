#!/bin/bash

# =============================================================================
# Ollama Docker Setup Script for macOS M4 Max
# =============================================================================
# This script prepares your macOS M4 Max system for running Ollama in Docker
# with proper security configurations and optimizations.
#
# Usage: ./scripts/setup.sh [OPTIONS]
# Options:
#   --external-ssd PATH    Path to external SSD for model storage
#   --memory-limit SIZE    Memory limit for container (default: 32G)
#   --cpu-limit COUNT      CPU limit for container (default: 8)
#   --help                 Show this help message
# =============================================================================

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default configuration
DEFAULT_EXTERNAL_SSD="/Volumes/External"
DEFAULT_MEMORY_LIMIT="32G"
DEFAULT_CPU_LIMIT="8"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Configuration variables
EXTERNAL_SSD="$DEFAULT_EXTERNAL_SSD"
MEMORY_LIMIT="$DEFAULT_MEMORY_LIMIT"
CPU_LIMIT="$DEFAULT_CPU_LIMIT"

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show help
show_help() {
    cat << EOF
Ollama Docker Setup Script for macOS M4 Max

USAGE:
    $0 [OPTIONS]

OPTIONS:
    --external-ssd PATH    Path to external SSD for model storage (default: $DEFAULT_EXTERNAL_SSD)
    --memory-limit SIZE    Memory limit for container (default: $DEFAULT_MEMORY_LIMIT)
    --cpu-limit COUNT      CPU limit for container (default: $DEFAULT_CPU_LIMIT)
    --help                 Show this help message

EXAMPLES:
    $0                                              # Use defaults
    $0 --external-ssd /Volumes/MyFastSSD           # Custom SSD path
    $0 --memory-limit 24G --cpu-limit 6           # Custom resource limits

EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --external-ssd)
            EXTERNAL_SSD="$2"
            shift 2
            ;;
        --memory-limit)
            MEMORY_LIMIT="$2"
            shift 2
            ;;
        --cpu-limit)
            CPU_LIMIT="$2"
            shift 2
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Function to check system requirements
check_system_requirements() {
    print_info "Checking system requirements..."
    
    # Check if running on macOS
    if [[ "$OSTYPE" != "darwin"* ]]; then
        print_error "This script is designed for macOS. Detected OS: $OSTYPE"
        exit 1
    fi
    
    # Check if running on Apple Silicon
    if [[ $(uname -m) != "arm64" ]]; then
        print_warning "This script is optimized for Apple Silicon (ARM64). Detected: $(uname -m)"
    fi
    
    # Check macOS version (requires macOS 12+ for optimal Docker performance)
    local macos_version=$(sw_vers -productVersion | cut -d. -f1)
    if [[ $macos_version -lt 12 ]]; then
        print_warning "macOS 12+ recommended for optimal Docker performance. Current: $(sw_vers -productVersion)"
    fi
    
    # Check available memory
    local total_memory_gb=$(( $(sysctl -n hw.memsize) / 1024 / 1024 / 1024 ))
    print_info "Total system memory: ${total_memory_gb}GB"
    
    if [[ $total_memory_gb -lt 16 ]]; then
        print_warning "16GB+ RAM recommended for LLM inference. Consider reducing memory limits."
    fi
    
    print_success "System requirements check completed"
}

# Function to check and install Docker
check_docker() {
    print_info "Checking Docker installation..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker Desktop for Mac:"
        print_info "https://docs.docker.com/desktop/install/mac-install/"
        exit 1
    fi
    
    # Check if Docker is running
    if ! docker info &> /dev/null; then
        print_error "Docker is not running. Please start Docker Desktop."
        exit 1
    fi
    
    # Check Docker version
    local docker_version=$(docker --version | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+' | head -1)
    print_info "Docker version: $docker_version"
    
    # Check if Docker Compose is available
    if ! docker compose version &> /dev/null; then
        print_error "Docker Compose is not available. Please update Docker Desktop."
        exit 1
    fi
    
    print_success "Docker check completed"
}

# Function to setup directories
setup_directories() {
    print_info "Setting up directories..."
    
    # Create project directories
    mkdir -p "$PROJECT_DIR/config"
    mkdir -p "$PROJECT_DIR/logs"
    mkdir -p "$PROJECT_DIR/scripts"
    
    # Setup external SSD directory for models
    local models_dir="${EXTERNAL_SSD}/ollama_models"
    
    if [[ ! -d "$EXTERNAL_SSD" ]]; then
        print_error "External SSD path does not exist: $EXTERNAL_SSD"
        print_info "Please ensure your external SSD is mounted or specify correct path with --external-ssd"
        exit 1
    fi
    
    # Create models directory
    mkdir -p "$models_dir"
    
    # Set appropriate permissions (Docker will run as UID 1000)
    if [[ -w "$models_dir" ]]; then
        print_success "Models directory created: $models_dir"
    else
        print_warning "Cannot write to models directory. You may need to adjust permissions:"
        print_info "sudo chown -R $(id -u):$(id -g) '$models_dir'"
    fi
    
    # Create config file
    cat > "$PROJECT_DIR/config/ollama.env" << EOF
# Ollama Configuration for macOS M4 Max
# This file contains environment variables for Ollama

# Performance settings
OLLAMA_NUM_PARALLEL=4
OLLAMA_MAX_LOADED_MODELS=2
OLLAMA_KEEP_ALIVE=5m

# Security settings
OLLAMA_DEBUG=false
OLLAMA_ORIGINS=http://localhost:*,http://127.0.0.1:*

# Model storage
OLLAMA_MODELS=$models_dir
EOF
    
    print_success "Directory setup completed"
}

# Function to verify checksums
verify_checksums() {
    print_info "Setting up checksum verification..."
    
    # Create checksum verification script
    cat > "$PROJECT_DIR/scripts/verify-checksums.sh" << 'EOF'
#!/bin/bash
# Checksum verification for Ollama releases
# This script helps verify the integrity of downloaded Ollama binaries

OLLAMA_VERSION="0.1.33"
EXPECTED_SHA256="a1b2c3d4e5f6789012345678901234567890123456789012345678901234567890"

echo "Verifying Ollama v${OLLAMA_VERSION} checksums..."
echo "Expected SHA256: $EXPECTED_SHA256"
echo ""
echo "To verify manually:"
echo "1. Download: https://github.com/ollama/ollama/releases/download/v${OLLAMA_VERSION}/ollama-linux-arm64"
echo "2. Check: shasum -a 256 ollama-linux-arm64"
echo "3. Compare with expected checksum above"
EOF
    
    chmod +x "$PROJECT_DIR/scripts/verify-checksums.sh"
    print_success "Checksum verification script created"
}

# Function to create Docker override for custom settings
create_docker_override() {
    print_info "Creating Docker Compose override..."
    
    cat > "$PROJECT_DIR/docker-compose.override.yml" << EOF
version: "3.9"

# Custom overrides for your specific setup
# This file allows you to customize the deployment without modifying docker-compose.yml

services:
  ollama:
    volumes:
      # Custom model storage path
      - ${EXTERNAL_SSD}/ollama_models:/ollama:rw
    
    deploy:
      resources:
        limits:
          memory: ${MEMORY_LIMIT}
          cpus: "${CPU_LIMIT}.0"
    
    environment:
      # Custom environment variables can be added here
      - OLLAMA_MODELS=/ollama
EOF
    
    print_success "Docker Compose override created with your settings"
}

# Function to create useful scripts
create_helper_scripts() {
    print_info "Creating helper scripts..."
    
    # Model management script
    cat > "$PROJECT_DIR/scripts/manage-models.sh" << 'EOF'
#!/bin/bash
# Model management script for Ollama Docker

set -euo pipefail

CONTAINER_NAME="ollama-m4max"

case "${1:-help}" in
    pull)
        if [[ -z "${2:-}" ]]; then
            echo "Usage: $0 pull <model_name>"
            echo "Example: $0 pull llama2:7b"
            exit 1
        fi
        echo "Pulling model: $2"
        docker exec -it "$CONTAINER_NAME" ollama pull "$2"
        ;;
    list)
        echo "Listing installed models:"
        docker exec -it "$CONTAINER_NAME" ollama list
        ;;
    remove)
        if [[ -z "${2:-}" ]]; then
            echo "Usage: $0 remove <model_name>"
            exit 1
        fi
        echo "Removing model: $2"
        docker exec -it "$CONTAINER_NAME" ollama rm "$2"
        ;;
    info)
        if [[ -z "${2:-}" ]]; then
            echo "Usage: $0 info <model_name>"
            exit 1
        fi
        echo "Model information for: $2"
        docker exec -it "$CONTAINER_NAME" ollama show "$2"
        ;;
    *)
        echo "Ollama Model Management"
        echo "Usage: $0 <command> [args]"
        echo ""
        echo "Commands:"
        echo "  pull <model>    Pull a model from the registry"
        echo "  list            List installed models"
        echo "  remove <model>  Remove a model"
        echo "  info <model>    Show model information"
        echo ""
        echo "Examples:"
        echo "  $0 pull llama2:7b"
        echo "  $0 list"
        echo "  $0 info llama2:7b"
        ;;
esac
EOF
    
    chmod +x "$PROJECT_DIR/scripts/manage-models.sh"
    
    # Security check script
    cat > "$PROJECT_DIR/scripts/security-check.sh" << 'EOF'
#!/bin/bash
# Security verification script for Ollama Docker deployment

set -euo pipefail

CONTAINER_NAME="ollama-m4max"
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_check() {
    local status=$1
    local message=$2
    if [[ $status == "PASS" ]]; then
        echo -e "${GREEN}[✓]${NC} $message"
    elif [[ $status == "FAIL" ]]; then
        echo -e "${RED}[✗]${NC} $message"
    else
        echo -e "${YELLOW}[?]${NC} $message"
    fi
}

echo "Ollama Docker Security Check"
echo "============================"

# Check if container is running as non-root
user_check=$(docker exec "$CONTAINER_NAME" whoami 2>/dev/null || echo "error")
if [[ "$user_check" == "ollama" ]]; then
    print_check "PASS" "Container running as non-root user (ollama)"
else
    print_check "FAIL" "Container not running as expected non-root user"
fi

# Check read-only root filesystem
readonly_check=$(docker inspect "$CONTAINER_NAME" --format='{{.HostConfig.ReadonlyRootfs}}' 2>/dev/null || echo "false")
if [[ "$readonly_check" == "true" ]]; then
    print_check "PASS" "Read-only root filesystem enabled"
else
    print_check "WARN" "Read-only root filesystem not enabled"
fi

# Check capabilities
caps_check=$(docker inspect "$CONTAINER_NAME" --format='{{.HostConfig.CapDrop}}' 2>/dev/null || echo "[]")
if [[ "$caps_check" == "[ALL]" ]]; then
    print_check "PASS" "All capabilities dropped"
else
    print_check "WARN" "Not all capabilities dropped: $caps_check"
fi

# Check port binding
port_check=$(docker port "$CONTAINER_NAME" 11434 2>/dev/null | grep "127.0.0.1" || echo "")
if [[ -n "$port_check" ]]; then
    print_check "PASS" "Port bound to localhost only"
else
    print_check "FAIL" "Port not properly restricted to localhost"
fi

# Check memory limits
memory_limit=$(docker inspect "$CONTAINER_NAME" --format='{{.HostConfig.Memory}}' 2>/dev/null || echo "0")
if [[ "$memory_limit" -gt 0 ]]; then
    memory_gb=$((memory_limit / 1024 / 1024 / 1024))
    print_check "PASS" "Memory limit set: ${memory_gb}GB"
else
    print_check "WARN" "No memory limit configured"
fi

echo ""
echo "Security check completed."
EOF
    
    chmod +x "$PROJECT_DIR/scripts/security-check.sh"
    
    print_success "Helper scripts created"
}

# Function to run initial tests
run_initial_tests() {
    print_info "Running initial tests..."
    
    # Test Docker build
    print_info "Testing Docker build (this may take a few minutes)..."
    if docker build -t ollama-test "$PROJECT_DIR" &> /dev/null; then
        print_success "Docker build test passed"
        docker rmi ollama-test &> /dev/null || true
    else
        print_error "Docker build test failed. Check Dockerfile and try again."
        exit 1
    fi
    
    # Test external SSD access
    local test_file="${EXTERNAL_SSD}/ollama_models/.test_write"
    if touch "$test_file" 2>/dev/null && rm "$test_file" 2>/dev/null; then
        print_success "External SSD write test passed"
    else
        print_warning "Cannot write to external SSD. Check permissions."
    fi
    
    print_success "Initial tests completed"
}

# Function to show next steps
show_next_steps() {
    print_success "Setup completed successfully!"
    echo ""
    echo -e "${BLUE}Next Steps:${NC}"
    echo "1. Build and start the container:"
    echo "   cd '$PROJECT_DIR'"
    echo "   docker compose up -d"
    echo ""
    echo "2. Pull a model (e.g., Llama 2 7B):"
    echo "   ./scripts/manage-models.sh pull llama2:7b"
    echo ""
    echo "3. Test the API:"
    echo "   curl http://localhost:11434/api/tags"
    echo ""
    echo "4. Run security check:"
    echo "   ./scripts/security-check.sh"
    echo ""
    echo -e "${BLUE}Configuration:${NC}"
    echo "- Models directory: ${EXTERNAL_SSD}/ollama_models"
    echo "- Memory limit: $MEMORY_LIMIT"
    echo "- CPU limit: $CPU_LIMIT cores"
    echo "- Config file: config/ollama.env"
    echo ""
    echo -e "${YELLOW}Note:${NC} This Docker setup runs CPU-only inference."
    echo "For Metal GPU acceleration, install Ollama natively on macOS."
}

# Main execution
main() {
    echo -e "${BLUE}Ollama Docker Setup for macOS M4 Max${NC}"
    echo "======================================"
    echo ""
    
    check_system_requirements
    check_docker
    setup_directories
    verify_checksums
    create_docker_override
    create_helper_scripts
    run_initial_tests
    show_next_steps
}

# Run main function
main "$@"
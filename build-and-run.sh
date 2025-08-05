#!/bin/bash

# =============================================================================
# Ollama Docker Build and Run Script for macOS M4 Max
# =============================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
OLLAMA_VERSION="0.2.8"
IMAGE_NAME="local/ollama:${OLLAMA_VERSION}"
CONTAINER_NAME="ollama"
MODEL_STORAGE="/Volumes/SSD1/ollama_models"

# Function to print colored output
print_status() {
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

# Function to check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker Desktop and try again."
        exit 1
    fi
    print_success "Docker is running"
}

# Function to check if external storage exists
check_storage() {
    if [ ! -d "$MODEL_STORAGE" ]; then
        print_warning "Model storage directory $MODEL_STORAGE does not exist"
        read -p "Create it now? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            sudo mkdir -p "$MODEL_STORAGE"
            sudo chown -R 1000:1000 "$MODEL_STORAGE"
            print_success "Created and configured model storage directory"
        else
            print_error "Cannot proceed without model storage directory"
            exit 1
        fi
    else
        print_success "Model storage directory exists"
    fi
}

# Function to build the Docker image
build_image() {
    print_status "Building Ollama Docker image..."
    
    # Check if Dockerfile exists
    if [ ! -f "Dockerfile" ]; then
        print_error "Dockerfile not found in current directory"
        exit 1
    fi
    
    # Build the image
    docker build \
        --build-arg OLLAMA_VER="${OLLAMA_VERSION}" \
        -t "${IMAGE_NAME}" .
    
    print_success "Docker image built successfully"
}

# Function to stop and remove existing container
cleanup_container() {
    if docker ps -a --format "table {{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
        print_status "Stopping existing container..."
        docker stop "${CONTAINER_NAME}" 2>/dev/null || true
        docker rm "${CONTAINER_NAME}" 2>/dev/null || true
        print_success "Existing container cleaned up"
    fi
}

# Function to run the container
run_container() {
    print_status "Starting Ollama container..."
    
    docker run -d \
        --name "${CONTAINER_NAME}" \
        --restart unless-stopped \
        --read-only \
        --tmpfs /tmp \
        -p 127.0.0.1:11434:11434 \
        --mount type=bind,src="${MODEL_STORAGE}",dst=/ollama \
        --cap-drop ALL \
        --security-opt no-new-privileges:true \
        --memory "32g" \
        --cpus "8" \
        "${IMAGE_NAME}"
    
    print_success "Container started successfully"
}

# Function to wait for container to be ready
wait_for_container() {
    print_status "Waiting for Ollama to be ready..."
    
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if docker exec "${CONTAINER_NAME}" curl -f http://localhost:11434/api/tags >/dev/null 2>&1; then
            print_success "Ollama is ready!"
            return 0
        fi
        
        echo -n "."
        sleep 2
        ((attempt++))
    done
    
    print_error "Container failed to start properly"
    docker logs "${CONTAINER_NAME}"
    exit 1
}

# Function to show container status
show_status() {
    print_status "Container status:"
    docker ps --filter "name=${CONTAINER_NAME}" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    
    print_status "Resource usage:"
    docker stats "${CONTAINER_NAME}" --no-stream --format "table {{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}"
}

# Function to provide usage instructions
show_usage() {
    echo
    print_status "Next steps:"
    echo "1. Pull a model:"
    echo "   docker exec -it ${CONTAINER_NAME} ollama pull llama2:7b-q8_0"
    echo
    echo "2. Test the API:"
    echo "   curl -X POST http://localhost:11434/api/chat -d '{\"model\":\"llama2:7b-q8_0\",\"messages\":[{\"role\":\"user\",\"content\":\"Hello!\"}],\"stream\":false}'"
    echo
    echo "3. View logs:"
    echo "   docker logs ${CONTAINER_NAME}"
    echo
    echo "4. Stop container:"
    echo "   docker stop ${CONTAINER_NAME}"
    echo
    print_warning "Note: This runs CPU-only. For Metal GPU acceleration, run Ollama natively on macOS."
}

# Function to show security verification
verify_security() {
    print_status "Verifying security configuration..."
    
    # Check if running as non-root
    local user=$(docker exec "${CONTAINER_NAME}" whoami 2>/dev/null)
    if [ "$user" = "ollama" ]; then
        print_success "Running as non-root user: $user"
    else
        print_error "Not running as non-root user: $user"
    fi
    
    # Check if read-only filesystem
    local readonly=$(docker inspect "${CONTAINER_NAME}" --format='{{.HostConfig.ReadonlyRootfs}}' 2>/dev/null)
    if [ "$readonly" = "true" ]; then
        print_success "Read-only root filesystem enabled"
    else
        print_error "Read-only root filesystem not enabled"
    fi
    
    # Check capabilities
    local caps=$(docker inspect "${CONTAINER_NAME}" --format='{{json .HostConfig.CapAdd}}' 2>/dev/null)
    if [ "$caps" = "null" ]; then
        print_success "All capabilities dropped"
    else
        print_error "Capabilities not properly dropped: $caps"
    fi
}

# Main execution
main() {
    echo "============================================================================="
    echo "Ollama Docker Setup for macOS M4 Max"
    echo "============================================================================="
    echo
    
    check_docker
    check_storage
    build_image
    cleanup_container
    run_container
    wait_for_container
    show_status
    verify_security
    show_usage
}

# Handle command line arguments
case "${1:-}" in
    "stop")
        print_status "Stopping Ollama container..."
        docker stop "${CONTAINER_NAME}" 2>/dev/null || true
        docker rm "${CONTAINER_NAME}" 2>/dev/null || true
        print_success "Container stopped and removed"
        ;;
    "logs")
        docker logs -f "${CONTAINER_NAME}"
        ;;
    "status")
        show_status
        ;;
    "verify")
        verify_security
        ;;
    "help"|"-h"|"--help")
        echo "Usage: $0 [command]"
        echo
        echo "Commands:"
        echo "  (no args)  Build and run Ollama container"
        echo "  stop       Stop and remove the container"
        echo "  logs       Show container logs"
        echo "  status     Show container status"
        echo "  verify     Verify security configuration"
        echo "  help       Show this help message"
        ;;
    "")
        main
        ;;
    *)
        print_error "Unknown command: $1"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac
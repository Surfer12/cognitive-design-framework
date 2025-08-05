#!/bin/bash

# Secure Ollama Docker Setup Script
# This script sets up a hardened Ollama container with security best practices

set -euo pipefail

# Configuration
OLLAMA_VERSION="0.2.8"
MODELS_DIR="/Volumes/SSD1/ollama_models"
CONTAINER_NAME="ollama"
IMAGE_NAME="local/ollama:${OLLAMA_VERSION}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        log_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    log_info "Docker is running"
}

# Create models directory if it doesn't exist
setup_models_dir() {
    if [[ ! -d "$MODELS_DIR" ]]; then
        log_info "Creating models directory: $MODELS_DIR"
        mkdir -p "$MODELS_DIR"
    else
        log_info "Models directory already exists: $MODELS_DIR"
    fi
}

# Build the Docker image
build_image() {
    log_info "Building Ollama Docker image..."
    docker build -f Dockerfile.ollama -t "$IMAGE_NAME" \
        --build-arg OLLAMA_VERSION="$OLLAMA_VERSION" \
        --build-arg TARGETARCH="amd64" \
        .
    log_info "Docker image built successfully"
}

# Stop and remove existing container
cleanup_existing() {
    if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        log_warn "Stopping and removing existing container: $CONTAINER_NAME"
        docker stop "$CONTAINER_NAME" >/dev/null 2>&1 || true
        docker rm "$CONTAINER_NAME" >/dev/null 2>&1 || true
    fi
}

# Run the secure Ollama container
run_container() {
    log_info "Starting secure Ollama container..."
    
    docker run -d \
        --name "$CONTAINER_NAME" \
        --restart unless-stopped \
        --read-only \
        --tmpfs /tmp:noexec,nosuid,size=1g \
        --tmpfs /var/tmp:noexec,nosuid,size=512m \
        -p 127.0.0.1:11434:11434 \
        --mount type=bind,src="$MODELS_DIR",dst=/ollama \
        -e OLLAMA_NO_NETWORK=0 \
        -e OLLAMA_HOST=0.0.0.0 \
        -e OLLAMA_MODELS=/ollama \
        --cap-drop ALL \
        --security-opt no-new-privileges:true \
        --memory "32g" \
        --cpus "8" \
        "$IMAGE_NAME"
    
    log_info "Container started successfully"
}

# Wait for Ollama to be ready
wait_for_ollama() {
    log_info "Waiting for Ollama to be ready..."
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
            log_info "Ollama is ready!"
            return 0
        fi
        
        echo -n "."
        sleep 2
        ((attempt++))
    done
    
    log_error "Ollama failed to start within expected time"
    docker logs "$CONTAINER_NAME"
    return 1
}

# Pull a default model
pull_model() {
    local model="${1:-llama2:7b-q8_0}"
    log_info "Pulling model: $model"
    
    docker exec -it "$CONTAINER_NAME" ollama pull "$model"
    log_info "Model pulled successfully"
}

# Display status and usage information
show_status() {
    echo
    log_info "=== Ollama Container Status ==="
    docker ps --filter name="$CONTAINER_NAME" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    
    echo
    log_info "=== Usage Instructions ==="
    echo "• Ollama API is available at: http://127.0.0.1:11434"
    echo "• List available models: docker exec $CONTAINER_NAME ollama list"
    echo "• Pull a model: docker exec $CONTAINER_NAME ollama pull <model_name>"
    echo "• Chat with a model: docker exec -it $CONTAINER_NAME ollama run <model_name>"
    echo "• View logs: docker logs $CONTAINER_NAME"
    echo "• Stop container: docker stop $CONTAINER_NAME"
    
    echo
    log_info "=== Security Features Enabled ==="
    echo "• Read-only root filesystem"
    echo "• No new privileges"
    echo "• All capabilities dropped"
    echo "• Resource limits (32GB RAM, 8 CPUs)"
    echo "• Network binding to localhost only"
    echo "• Temporary filesystems with security options"
    echo "• Non-root user execution"
}

# Main execution
main() {
    log_info "Starting secure Ollama setup..."
    
    check_docker
    setup_models_dir
    cleanup_existing
    build_image
    run_container
    wait_for_ollama
    
    # Ask if user wants to pull a model
    echo
    read -p "Would you like to pull the default model (llama2:7b-q8_0)? [y/N]: " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pull_model
    fi
    
    show_status
    log_info "Setup complete! Your secure Ollama container is ready."
}

# Handle script arguments
case "${1:-}" in
    "pull")
        pull_model "${2:-llama2:7b-q8_0}"
        ;;
    "status")
        show_status
        ;;
    "stop")
        docker stop "$CONTAINER_NAME"
        log_info "Container stopped"
        ;;
    "start")
        docker start "$CONTAINER_NAME"
        log_info "Container started"
        ;;
    "logs")
        docker logs -f "$CONTAINER_NAME"
        ;;
    "shell")
        docker exec -it "$CONTAINER_NAME" /bin/sh
        ;;
    *)
        main
        ;;
esac
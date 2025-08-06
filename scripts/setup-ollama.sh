#!/bin/bash

# Secure Ollama Setup Script
# This script provides multiple deployment options for Ollama

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
OLLAMA_VERSION="0.2.8"
MODELS_DIR="/Volumes/SSD1/ollama_models"
CONTAINER_NAME="ollama"

print_header() {
    echo -e "${BLUE}=== Ollama Secure Setup ===${NC}"
    echo
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

check_prerequisites() {
    print_header
    echo "Checking prerequisites..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        print_error "Docker daemon is not running. Please start Docker."
        exit 1
    fi
    
    if [ ! -d "$MODELS_DIR" ]; then
        print_warning "Models directory $MODELS_DIR does not exist. Creating..."
        mkdir -p "$MODELS_DIR"
    fi
    
    print_success "Prerequisites check passed"
    echo
}

deploy_with_docker_run() {
    echo "Deploying with docker run (original one-liner)..."
    
    # Stop and remove existing container if it exists
    docker stop "$CONTAINER_NAME" 2>/dev/null || true
    docker rm "$CONTAINER_NAME" 2>/dev/null || true
    
    docker run -d \
        --name "$CONTAINER_NAME" \
        --restart unless-stopped \
        --read-only \
        --tmpfs /tmp \
        -p 127.0.0.1:11434:11434 \
        --mount type=bind,src="$MODELS_DIR",dst=/ollama \
        -e OLLAMA_NO_NETWORK=0 \
        --cap-drop ALL \
        --security-opt no-new-privileges:true \
        --memory "32g" \
        --cpus "8" \
        local/ollama:$OLLAMA_VERSION
    
    print_success "Container started with docker run"
}

deploy_with_compose() {
    echo "Deploying with Docker Compose..."
    
    if [ ! -f "docker-compose.ollama.yml" ]; then
        print_error "docker-compose.ollama.yml not found"
        exit 1
    fi
    
    docker-compose -f docker-compose.ollama.yml up -d
    
    print_success "Container started with Docker Compose"
}

pull_model() {
    local model_name="${1:-llama2:7b-q8_0}"
    
    echo "Pulling model: $model_name"
    
    if docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
        docker exec -it "$CONTAINER_NAME" ollama pull "$model_name"
        print_success "Model $model_name pulled successfully"
    else
        print_error "Ollama container is not running"
        exit 1
    fi
}

check_status() {
    echo "Checking Ollama status..."
    
    if docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
        print_success "Container is running"
        
        # Test API endpoint
        if curl -s http://127.0.0.1:11434/api/tags &> /dev/null; then
            print_success "API is responding"
        else
            print_warning "API is not responding yet (may still be starting)"
        fi
    else
        print_error "Container is not running"
    fi
}

show_usage() {
    echo "Usage: $0 [OPTION]"
    echo
    echo "Options:"
    echo "  run      Deploy using docker run (original one-liner)"
    echo "  compose  Deploy using Docker Compose"
    echo "  pull     Pull a model (default: llama2:7b-q8_0)"
    echo "  status   Check container status"
    echo "  stop     Stop the container"
    echo "  logs     Show container logs"
    echo "  help     Show this help message"
    echo
    echo "Examples:"
    echo "  $0 run"
    echo "  $0 compose"
    echo "  $0 pull llama2:7b-q8_0"
    echo "  $0 status"
}

main() {
    case "${1:-help}" in
        "run")
            check_prerequisites
            deploy_with_docker_run
            ;;
        "compose")
            check_prerequisites
            deploy_with_compose
            ;;
        "pull")
            if [ -n "${2:-}" ]; then
                pull_model "$2"
            else
                pull_model
            fi
            ;;
        "status")
            check_status
            ;;
        "stop")
            docker stop "$CONTAINER_NAME" 2>/dev/null || true
            print_success "Container stopped"
            ;;
        "logs")
            docker logs -f "$CONTAINER_NAME"
            ;;
        "help"|*)
            show_usage
            ;;
    esac
}

main "$@"
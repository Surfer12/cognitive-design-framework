#!/bin/bash
# Alternative Mojo installation methods (no Homebrew)

set -e

echo "🔧 Alternative Mojo Installation Methods"
echo "======================================="

show_help() {
    echo "Usage: $0 [method]"
    echo ""
    echo "Available methods:"
    echo "  direct    - Direct download from Modular (default)"
    echo "  conda     - Try conda-forge (experimental)"
    echo "  manual    - Manual installation instructions"
    echo "  docker    - Docker-based setup"
    echo "  help      - Show this help"
}

install_direct() {
    echo "📦 Method 1: Direct Installation (Recommended)"
    echo "=============================================="
    
    # Use the main setup script
    bash "$(dirname "$0")/setup_mojo.sh"
}

install_conda_experimental() {
    echo "📦 Method 2: Conda/Mamba (Experimental)"
    echo "======================================="
    
    echo "⚠️  This is experimental and may not work"
    echo "Trying to install via conda-forge..."
    
    # Try with mamba first (faster)
    if command -v mamba &> /dev/null; then
        echo "Using mamba..."
        mamba install -c conda-forge -c modular mojo || echo "❌ Mamba installation failed"
    elif command -v conda &> /dev/null; then
        echo "Using conda..."
        conda install -c conda-forge -c modular mojo || echo "❌ Conda installation failed"
    else
        echo "❌ Neither conda nor mamba found"
        echo "Install miniconda or mambaforge first"
        return 1
    fi
}

show_manual_instructions() {
    echo "📖 Method 3: Manual Installation"
    echo "================================"
    
    echo "1. Visit: https://docs.modular.com/mojo/manual/get-started/"
    echo "2. Sign up for a Modular account"
    echo "3. Download the installer for your platform:"
    echo "   - macOS: https://get.modular.com"
    echo "   - Linux: https://get.modular.com"
    echo "4. Run the installer:"
    echo "   curl -s https://get.modular.com | sh -"
    echo "5. Install Mojo:"
    echo "   modular install mojo"
    echo "6. Add to PATH:"
    echo "   echo 'export PATH=\"\$HOME/.modular/bin:\$PATH\"' >> ~/.zshrc"
    echo "   source ~/.zshrc"
}

setup_docker() {
    echo "🐳 Method 4: Docker Setup"
    echo "========================="
    
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker not found. Please install Docker first:"
        echo "   - macOS: Download Docker Desktop"
        echo "   - Linux: Use your package manager"
        return 1
    fi
    
    echo "Creating Dockerfile with Mojo..."
    
    cat > Dockerfile.mojo << 'EOF'
FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Modular CLI and Mojo
RUN curl -s https://get.modular.com | sh -s -- --no-modify-path
ENV PATH="/root/.modular/bin:$PATH"
RUN modular install mojo

# Set working directory
WORKDIR /workspace

# Copy project files
COPY . .

# Install Python dependencies
RUN pip3 install -r requirements.txt

CMD ["bash"]
EOF

    echo "✅ Created Dockerfile.mojo"
    echo "To build and run:"
    echo "  docker build -f Dockerfile.mojo -t cognitive-framework-mojo ."
    echo "  docker run -it -v \$(pwd):/workspace cognitive-framework-mojo"
}

# Main execution
METHOD=${1:-direct}

case $METHOD in
    direct)
        install_direct
        ;;
    conda)
        install_conda_experimental
        ;;
    manual)
        show_manual_instructions
        ;;
    docker)
        setup_docker
        ;;
    help)
        show_help
        ;;
    *)
        echo "❌ Unknown method: $METHOD"
        show_help
        exit 1
        ;;
esac

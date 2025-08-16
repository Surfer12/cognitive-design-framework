#!/bin/bash
# Setup script for Mojo installation (no Homebrew required)

set -e

echo "🧠 Cognitive Design Framework - Mojo Setup (No Homebrew)"
echo "========================================================"

# Detect OS and architecture
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)

echo "🔍 Detected system: $OS ($ARCH)"

# Function to install Modular CLI directly
install_modular_cli() {
    echo "📦 Installing Modular CLI (direct download)..."
    
    # Create temporary directory
    TEMP_DIR=$(mktemp -d)
    cd "$TEMP_DIR"
    
    # Download Modular CLI installer
    if [[ "$OS" == "darwin" ]]; then
        # macOS
        curl -L -o modular-installer.sh "https://get.modular.com"
    elif [[ "$OS" == "linux" ]]; then
        # Linux
        curl -L -o modular-installer.sh "https://get.modular.com"
    else
        echo "❌ Unsupported operating system: $OS"
        exit 1
    fi
    
    # Make installer executable and run it
    chmod +x modular-installer.sh
    bash modular-installer.sh --no-modify-path
    
    # Clean up
    cd - > /dev/null
    rm -rf "$TEMP_DIR"
    
    echo "✅ Modular CLI installed"
}

# Function to install via curl (alternative method)
install_via_curl() {
    echo "📦 Installing Modular CLI via curl..."
    curl -s https://get.modular.com | sh -s -- --no-modify-path
}

# Function to install via wget (if curl not available)
install_via_wget() {
    echo "📦 Installing Modular CLI via wget..."
    wget -qO- https://get.modular.com | sh -s -- --no-modify-path
}

# Check if Modular CLI is already installed
if command -v modular &> /dev/null; then
    echo "✅ Modular CLI already installed"
else
    echo "🔧 Installing Modular CLI..."
    
    # Try different installation methods
    if command -v curl &> /dev/null; then
        install_via_curl
    elif command -v wget &> /dev/null; then
        install_via_wget
    else
        echo "❌ Neither curl nor wget found. Please install one of them first."
        echo "   On macOS: Install Xcode Command Line Tools"
        echo "   On Linux: sudo apt install curl (or equivalent for your distro)"
        exit 1
    fi
fi

# Add Modular to PATH for current session
export PATH="$HOME/.modular/bin:$PATH"

# Verify Modular CLI installation
if ! command -v modular &> /dev/null; then
    echo "❌ Modular CLI installation failed"
    echo "Please try manual installation:"
    echo "1. Visit: https://docs.modular.com/mojo/manual/get-started/"
    echo "2. Follow the installation instructions for your platform"
    exit 1
fi

echo "✅ Modular CLI ready: $(modular --version 2>/dev/null || echo 'installed')"

# Install Mojo
echo "🔥 Installing Mojo..."
modular install mojo

# Verify Mojo installation
if command -v mojo &> /dev/null; then
    echo "✅ Mojo installed successfully!"
    echo "📍 Mojo version: $(mojo --version)"
else
    echo "❌ Mojo installation failed"
    echo "Troubleshooting:"
    echo "1. Check if PATH includes: $HOME/.modular/bin"
    echo "2. Try: source ~/.bashrc or source ~/.zshrc"
    echo "3. Manual PATH export: export PATH=\"\$HOME/.modular/bin:\$PATH\""
    exit 1
fi

# Setup environment variables
echo "🔧 Setting up environment..."

# Determine shell configuration file
SHELL_PROFILE=""
if [[ -n "$ZSH_VERSION" ]] || [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_PROFILE="$HOME/.zshrc"
elif [[ -n "$BASH_VERSION" ]] || [[ "$SHELL" == *"bash"* ]]; then
    if [[ "$OS" == "darwin" ]]; then
        SHELL_PROFILE="$HOME/.bash_profile"
    else
        SHELL_PROFILE="$HOME/.bashrc"
    fi
fi

# Add to shell profile if detected
if [[ -n "$SHELL_PROFILE" ]]; then
    if ! grep -q "\.modular/bin" "$SHELL_PROFILE" 2>/dev/null; then
        echo "" >> "$SHELL_PROFILE"
        echo "# Added by Cognitive Design Framework Mojo setup" >> "$SHELL_PROFILE"
        echo 'export PATH="$HOME/.modular/bin:$PATH"' >> "$SHELL_PROFILE"
        echo "✅ Added Mojo to PATH in $SHELL_PROFILE"
    else
        echo "✅ Mojo already in PATH configuration"
    fi
else
    echo "⚠️  Could not detect shell profile. Please manually add to your shell config:"
    echo '   export PATH="$HOME/.modular/bin:$PATH"'
fi

# Create activation script for pixi integration
ACTIVATION_SCRIPT="$HOME/.modular/activate_mojo.sh"
cat > "$ACTIVATION_SCRIPT" << 'EOF'
#!/bin/bash
# Mojo activation script for pixi integration
export PATH="$HOME/.modular/bin:$PATH"
export MODULAR_HOME="$HOME/.modular"
EOF

chmod +x "$ACTIVATION_SCRIPT"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Installation summary:"
echo "- Modular CLI: $HOME/.modular/bin/modular"
echo "- Mojo: $HOME/.modular/bin/mojo"
echo "- Activation script: $ACTIVATION_SCRIPT"
echo ""
echo "Next steps:"
echo "1. Restart your terminal or run: source $SHELL_PROFILE"
echo "2. Or manually export PATH: export PATH=\"\$HOME/.modular/bin:\$PATH\""
echo "3. Activate pixi environment: pixi shell"
echo "4. Test Mojo: mojo --version"
echo "5. Start developing with the cognitive framework!"
echo ""
echo "No Homebrew required! 🎉"

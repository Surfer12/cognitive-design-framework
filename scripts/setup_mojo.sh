#!/bin/bash
# Setup script for Mojo installation alongside pixi environment

set -e

echo "🧠 Cognitive Design Framework - Mojo Setup"
echo "=========================================="

# Check if Modular CLI is installed
if ! command -v modular &> /dev/null; then
    echo "📦 Installing Modular CLI..."
    curl -s https://get.modular.com | sh -
    
    # Add to PATH for current session
    export PATH="$HOME/.modular/bin:$PATH"
    
    echo "✅ Modular CLI installed"
else
    echo "✅ Modular CLI already installed"
fi

# Install Mojo
echo "🔥 Installing Mojo..."
modular install mojo

# Verify installation
if command -v mojo &> /dev/null; then
    echo "✅ Mojo installed successfully!"
    echo "📍 Mojo version: $(mojo --version)"
else
    echo "❌ Mojo installation failed"
    exit 1
fi

# Setup environment
echo "🔧 Setting up environment..."

# Add Mojo to PATH in shell profile
SHELL_PROFILE=""
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_PROFILE="$HOME/.zshrc"
elif [[ "$SHELL" == *"bash"* ]]; then
    SHELL_PROFILE="$HOME/.bashrc"
fi

if [[ -n "$SHELL_PROFILE" ]]; then
    if ! grep -q "modular" "$SHELL_PROFILE"; then
        echo 'export PATH="$HOME/.modular/bin:$PATH"' >> "$SHELL_PROFILE"
        echo "✅ Added Mojo to PATH in $SHELL_PROFILE"
    fi
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Restart your terminal or run: source $SHELL_PROFILE"
echo "2. Activate pixi environment: pixi shell"
echo "3. Test Mojo: mojo --version"
echo "4. Start developing with the cognitive framework!"

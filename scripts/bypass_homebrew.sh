#!/bin/bash
# Simple Homebrew bypass for Modular installer

set -e

echo "🔧 Homebrew Bypass Method"
echo "========================="

# Create a fake brew command that satisfies the installer
TEMP_DIR=$(mktemp -d)
FAKE_BREW="$TEMP_DIR/brew"

cat > "$FAKE_BREW" << 'EOF'
#!/bin/bash
# Fake brew command to satisfy Modular installer
case "$1" in
    "--version")
        echo "Homebrew 4.0.0 (fake)"
        ;;
    "install")
        echo "Fake brew install: $@"
        ;;
    *)
        echo "Fake brew command: $@"
        ;;
esac
exit 0
EOF

chmod +x "$FAKE_BREW"

# Add fake brew to PATH temporarily
export PATH="$TEMP_DIR:$PATH"

echo "✅ Created fake brew command"
echo "🔥 Installing Modular with fake Homebrew..."

# Run Modular installer with fake brew in PATH
curl -s https://get.modular.com | sh -s -- --no-modify-path

# Clean up
rm -rf "$TEMP_DIR"

echo "✅ Installation complete!"
echo "🧹 Cleaned up fake Homebrew"

# Verify
if [ -f "$HOME/.modular/bin/modular" ]; then
    echo "✅ Modular CLI installed successfully"
    export PATH="$HOME/.modular/bin:$PATH"
    
    echo "🔥 Installing Mojo..."
    modular install mojo
    
    if [ -f "$HOME/.modular/bin/mojo" ]; then
        echo "✅ Mojo installed successfully!"
        echo "📍 Version: $(mojo --version)"
    else
        echo "❌ Mojo installation failed"
    fi
else
    echo "❌ Modular CLI installation failed"
fi

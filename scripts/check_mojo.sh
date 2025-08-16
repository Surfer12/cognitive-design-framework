#!/bin/bash
# Check if Mojo is available and provide helpful feedback

if command -v mojo &> /dev/null; then
    echo "✅ Mojo is available: $(mojo --version)"
    exit 0
else
    echo "❌ Mojo not found in PATH"
    echo ""
    echo "To install Mojo:"
    echo "  pixi run setup-mojo"
    echo ""
    echo "Or manually:"
    echo "  curl -s https://get.modular.com | sh -"
    echo "  modular install mojo"
    echo "  export PATH=\"\$HOME/.modular/bin:\$PATH\""
    exit 1
fi

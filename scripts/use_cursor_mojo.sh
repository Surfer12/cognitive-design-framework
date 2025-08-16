#!/bin/bash
# Use the existing Mojo installation from Cursor

CURSOR_MOJO_PATH="/Users/ryan_david_oates/Library/Application Support/Cursor/User/globalStorage/modular-mojotools.vscode-mojo/magic-data-home/envs/max/bin"

if [ -f "$CURSOR_MOJO_PATH/mojo" ]; then
    echo "✅ Found Cursor Mojo installation"
    echo "📍 Version: $("$CURSOR_MOJO_PATH/mojo" --version)"
    
    # Add to shell profile
    SHELL_PROFILE="$HOME/.zshrc"
    PATH_EXPORT="export PATH=\"$CURSOR_MOJO_PATH:\$PATH\""
    
    if ! grep -q "modular-mojotools.vscode-mojo" "$SHELL_PROFILE" 2>/dev/null; then
        echo "" >> "$SHELL_PROFILE"
        echo "# Added by Cognitive Design Framework - Use Cursor Mojo" >> "$SHELL_PROFILE"
        echo "$PATH_EXPORT" >> "$SHELL_PROFILE"
        echo "✅ Added Cursor Mojo to PATH in $SHELL_PROFILE"
    else
        echo "✅ Cursor Mojo already in PATH configuration"
    fi
    
    # Add to current session
    export PATH="$CURSOR_MOJO_PATH:$PATH"
    
    echo ""
    echo "🎉 Setup complete!"
    echo "You can now use: mojo --version"
    echo "Restart terminal or run: source ~/.zshrc"
    
else
    echo "❌ Cursor Mojo not found at expected location"
    echo "Try reinstalling the Mojo extension in Cursor"
fi

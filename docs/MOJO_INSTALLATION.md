# 🔥 Mojo Installation Guide (No Homebrew Required!)

This guide provides multiple ways to install Mojo for the Cognitive Design Framework without requiring Homebrew.

## 🚀 Quick Start (Recommended)

```bash
# Install Python dependencies
pixi install

# Install Mojo (pure Python method)
pixi run setup-mojo-python

# Activate environment and test
pixi shell
mojo --version
```

## 📋 Available Installation Methods

### Method 1: Pure Python Installer (Recommended)
```bash
pixi run setup-mojo-python
```
- ✅ No external dependencies beyond Python
- ✅ Cross-platform (macOS, Linux)
- ✅ Automatic PATH configuration
- ✅ Verification included

### Method 2: Direct Bash Installer
```bash
pixi run setup-mojo
```
- ✅ Traditional shell-based approach
- ✅ Robust error handling
- ✅ Multiple fallback methods

### Method 3: Alternative Methods Menu
```bash
pixi run setup-mojo-alt help
```
Available options:
- `direct` - Direct download (same as Method 2)
- `docker` - Docker-based setup
- `manual` - Step-by-step manual instructions

### Method 4: Docker Setup
```bash
pixi run setup-mojo-docker
```
- ✅ Isolated environment
- ✅ No system modifications
- ✅ Reproducible setup

## 🔧 Manual Installation (If Scripts Fail)

### Step 1: Install Modular CLI
```bash
# Download and run installer
curl -s https://get.modular.com | sh -s -- --no-modify-path

# Or download first, then run
curl -L -o modular-installer.sh https://get.modular.com
chmod +x modular-installer.sh
./modular-installer.sh --no-modify-path
```

### Step 2: Install Mojo
```bash
# Add to PATH for current session
export PATH="$HOME/.modular/bin:$PATH"

# Install Mojo
modular install mojo
```

### Step 3: Configure Environment
```bash
# Add to shell profile (choose your shell)
echo 'export PATH="$HOME/.modular/bin:$PATH"' >> ~/.zshrc    # zsh
echo 'export PATH="$HOME/.modular/bin:$PATH"' >> ~/.bashrc   # bash (Linux)
echo 'export PATH="$HOME/.modular/bin:$PATH"' >> ~/.bash_profile  # bash (macOS)

# Reload configuration
source ~/.zshrc  # or ~/.bashrc or ~/.bash_profile
```

## 🐳 Docker Alternative

If you prefer containerized development:

```bash
# Generate Dockerfile
pixi run setup-mojo-docker

# Build and run
docker build -f Dockerfile.mojo -t cognitive-framework-mojo .
docker run -it -v $(pwd):/workspace cognitive-framework-mojo

# Inside container
mojo --version
```

## 🔍 Verification

After installation, verify everything works:

```bash
# Check Mojo
mojo --version

# Check pixi environment
pixi shell
python --version

# Test framework
pixi run test
```

## 🛠️ Troubleshooting

### Mojo Not Found in PATH
```bash
# Manually add to current session
export PATH="$HOME/.modular/bin:$PATH"

# Check if Mojo exists
ls -la ~/.modular/bin/mojo

# Re-run shell configuration
source ~/.zshrc  # or your shell config
```

### Permission Issues
```bash
# Make sure scripts are executable
chmod +x scripts/*.sh
chmod +x scripts/*.py

# Check Modular directory permissions
ls -la ~/.modular/
```

### Network Issues
```bash
# Try alternative download methods
wget -qO- https://get.modular.com | sh -s -- --no-modify-path

# Or use the Python installer (uses urllib)
pixi run setup-mojo-python
```

### macOS Specific Issues
```bash
# Install Xcode Command Line Tools if needed
xcode-select --install

# Check for curl
which curl || echo "Install Xcode Command Line Tools"
```

## 🎯 Integration with Pixi

The framework is designed to work seamlessly with pixi:

```bash
# Available pixi tasks
pixi run check-mojo          # Check if Mojo is installed
pixi run setup-mojo-python   # Install via Python
pixi run setup-mojo          # Install via bash
pixi run setup-mojo-alt      # Show all methods
pixi run dev-setup           # Complete development setup
```

## 📚 Why No Homebrew?

We avoid Homebrew because:
- ❌ Not available on all systems
- ❌ Can conflict with system Python
- ❌ Adds unnecessary complexity
- ❌ Mojo isn't officially distributed via Homebrew

Our approach uses:
- ✅ Official Modular distribution
- ✅ Cross-platform compatibility
- ✅ No external package managers
- ✅ Direct integration with pixi

## 🤝 Getting Help

If you encounter issues:

1. Check the [troubleshooting section](#🛠️-troubleshooting)
2. Run `pixi run setup-mojo-alt manual` for detailed instructions
3. Visit [Modular's documentation](https://docs.modular.com/mojo/manual/get-started/)
4. Open an issue in this repository

## 🎉 Success!

Once installed, you can:
- Use Mojo alongside Python in the same environment
- Leverage pixi for dependency management
- Develop high-performance cognitive systems
- Contribute to the framework

Happy coding with the Cognitive Design Framework! 🧠✨

#!/usr/bin/env python3
"""
Pure Python Mojo installer (no Homebrew required)
"""

import os
import platform
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

def get_system_info():
    """Get system information"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    print(f"🔍 Detected system: {system} ({machine})")
    return system, machine

def check_dependencies():
    """Check for required dependencies"""
    missing = []
    
    # Check for curl or wget
    has_curl = subprocess.run(['which', 'curl'], 
                             capture_output=True).returncode == 0
    has_wget = subprocess.run(['which', 'wget'], 
                             capture_output=True).returncode == 0
    
    if not (has_curl or has_wget):
        missing.append("curl or wget")
    
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print("Please install them first:")
        if platform.system().lower() == 'darwin':
            print("  - Install Xcode Command Line Tools: xcode-select --install")
        else:
            print("  - Ubuntu/Debian: sudo apt install curl")
            print("  - CentOS/RHEL: sudo yum install curl")
        return False
    
    return True

def download_installer():
    """Download Modular installer"""
    print("📦 Downloading Modular installer...")
    
    installer_url = "https://get.modular.com"
    
    try:
        with tempfile.NamedTemporaryFile(mode='w+b', suffix='.sh', delete=False) as f:
            with urllib.request.urlopen(installer_url) as response:
                f.write(response.read())
            return f.name
    except Exception as e:
        print(f"❌ Failed to download installer: {e}")
        return None

def install_modular_cli(installer_path=None):
    """Install Modular CLI"""
    print("🔧 Installing Modular CLI...")
    
    if installer_path:
        # Use downloaded installer
        os.chmod(installer_path, 0o755)
        result = subprocess.run(['bash', installer_path, '--no-modify-path'], 
                               capture_output=True, text=True)
    else:
        # Use curl method
        cmd = "curl -s https://get.modular.com | sh -s -- --no-modify-path"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Modular CLI installation failed: {result.stderr}")
        return False
    
    print("✅ Modular CLI installed")
    return True

def install_mojo():
    """Install Mojo using Modular CLI"""
    print("🔥 Installing Mojo...")
    
    # Add modular to PATH for this session
    modular_bin = Path.home() / ".modular" / "bin"
    current_path = os.environ.get('PATH', '')
    os.environ['PATH'] = f"{modular_bin}:{current_path}"
    
    # Install Mojo
    result = subprocess.run(['modular', 'install', 'mojo'], 
                           capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Mojo installation failed: {result.stderr}")
        return False
    
    print("✅ Mojo installed successfully!")
    return True

def setup_environment():
    """Setup environment variables"""
    print("🔧 Setting up environment...")
    
    # Determine shell config file
    shell = os.environ.get('SHELL', '')
    home = Path.home()
    
    if 'zsh' in shell:
        config_file = home / '.zshrc'
    elif 'bash' in shell:
        if platform.system().lower() == 'darwin':
            config_file = home / '.bash_profile'
        else:
            config_file = home / '.bashrc'
    else:
        config_file = None
    
    # Add to PATH
    path_export = 'export PATH="$HOME/.modular/bin:$PATH"'
    
    if config_file and config_file.exists():
        content = config_file.read_text()
        if '.modular/bin' not in content:
            with config_file.open('a') as f:
                f.write(f'\n# Added by Cognitive Design Framework\n{path_export}\n')
            print(f"✅ Added Mojo to PATH in {config_file}")
        else:
            print("✅ Mojo already in PATH configuration")
    else:
        print("⚠️  Please manually add to your shell config:")
        print(f"   {path_export}")
    
    return config_file

def verify_installation():
    """Verify Mojo installation"""
    print("🔍 Verifying installation...")
    
    # Add modular to PATH
    modular_bin = Path.home() / ".modular" / "bin"
    current_path = os.environ.get('PATH', '')
    os.environ['PATH'] = f"{modular_bin}:{current_path}"
    
    try:
        result = subprocess.run(['mojo', '--version'], 
                               capture_output=True, text=True, check=True)
        print(f"✅ Mojo version: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Mojo verification failed")
        return False

def main():
    """Main installation process"""
    print("🧠 Cognitive Design Framework - Python Mojo Installer")
    print("===================================================")
    print("📝 No Homebrew required!")
    print()
    
    # Check system
    system, machine = get_system_info()
    
    if system not in ['darwin', 'linux']:
        print(f"❌ Unsupported system: {system}")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check if already installed
    modular_bin = Path.home() / ".modular" / "bin" / "modular"
    if modular_bin.exists():
        print("✅ Modular CLI already installed")
    else:
        # Download and install
        installer_path = download_installer()
        if not install_modular_cli(installer_path):
            sys.exit(1)
        
        # Clean up
        if installer_path:
            os.unlink(installer_path)
    
    # Install Mojo
    if not install_mojo():
        sys.exit(1)
    
    # Setup environment
    config_file = setup_environment()
    
    # Verify installation
    if not verify_installation():
        print("⚠️  Installation completed but verification failed")
        print("Try restarting your terminal or running:")
        if config_file:
            print(f"   source {config_file}")
        print('   export PATH="$HOME/.modular/bin:$PATH"')
    
    print()
    print("🎉 Installation complete!")
    print()
    print("Next steps:")
    print("1. Restart your terminal or source your shell config")
    print("2. Run: pixi shell")
    print("3. Test: mojo --version")
    print("4. Start coding with the cognitive framework!")

if __name__ == "__main__":
    main()

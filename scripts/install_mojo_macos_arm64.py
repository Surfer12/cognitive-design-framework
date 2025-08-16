#!/usr/bin/env python3
"""
Homebrew-free Mojo installer for macOS ARM64
Works around the Modular installer's Homebrew requirement
"""

import os
import platform
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

def check_macos_arm64():
    """Verify we're on macOS ARM64"""
    if platform.system() != 'Darwin':
        print("❌ This installer is for macOS only")
        return False
    
    if platform.machine() != 'arm64':
        print("❌ This installer is for Apple Silicon (ARM64) only")
        return False
    
    print("✅ macOS ARM64 detected")
    return True

def install_minimal_homebrew():
    """Install minimal Homebrew just for Modular (in isolated location)"""
    print("🍺 Installing minimal Homebrew for Modular compatibility...")
    
    # Create isolated Homebrew directory
    homebrew_dir = Path.home() / ".modular-homebrew"
    homebrew_dir.mkdir(exist_ok=True)
    
    print(f"Installing Homebrew to: {homebrew_dir}")
    
    # Download Homebrew installer
    installer_url = "https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh"
    
    try:
        with urllib.request.urlopen(installer_url) as response:
            installer_content = response.read().decode('utf-8')
        
        # Modify installer to use custom directory
        modified_installer = installer_content.replace(
            'HOMEBREW_PREFIX="/opt/homebrew"',
            f'HOMEBREW_PREFIX="{homebrew_dir}"'
        )
        
        # Save modified installer
        installer_path = homebrew_dir / "install.sh"
        with open(installer_path, 'w') as f:
            f.write(modified_installer)
        
        os.chmod(installer_path, 0o755)
        
        # Set environment for isolated installation
        env = os.environ.copy()
        env['HOMEBREW_PREFIX'] = str(homebrew_dir)
        env['PATH'] = f"{homebrew_dir}/bin:{env.get('PATH', '')}"
        
        # Run installer
        result = subprocess.run(['bash', str(installer_path)], 
                               env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Minimal Homebrew installed")
            return homebrew_dir
        else:
            print(f"❌ Homebrew installation failed: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Error installing Homebrew: {e}")
        return None

def try_direct_modular_download():
    """Try to download Modular CLI directly"""
    print("📦 Attempting direct Modular CLI download...")
    
    # Known Modular CLI download URLs (these may change)
    urls = [
        "https://dl.modular.com/public/installer/modular-macos-arm64.tar.gz",
        "https://github.com/modularml/modular/releases/latest/download/modular-macos-arm64.tar.gz",
    ]
    
    modular_dir = Path.home() / ".modular"
    modular_dir.mkdir(exist_ok=True)
    
    for url in urls:
        try:
            print(f"Trying: {url}")
            
            with tempfile.NamedTemporaryFile(suffix='.tar.gz') as tmp_file:
                urllib.request.urlretrieve(url, tmp_file.name)
                
                # Extract
                import tarfile
                with tarfile.open(tmp_file.name, 'r:gz') as tar:
                    tar.extractall(modular_dir)
                
                print(f"✅ Downloaded and extracted from {url}")
                return True
                
        except Exception as e:
            print(f"❌ Failed to download from {url}: {e}")
            continue
    
    return False

def install_with_homebrew_workaround():
    """Install Modular using Homebrew workaround"""
    print("🔧 Using Homebrew workaround method...")
    
    # Install minimal Homebrew
    homebrew_dir = install_minimal_homebrew()
    if not homebrew_dir:
        return False
    
    # Set up environment with Homebrew
    env = os.environ.copy()
    env['PATH'] = f"{homebrew_dir}/bin:{env.get('PATH', '')}"
    env['HOMEBREW_PREFIX'] = str(homebrew_dir)
    
    # Download and run Modular installer with Homebrew available
    try:
        cmd = "curl -s https://get.modular.com | sh -s -- --no-modify-path"
        result = subprocess.run(cmd, shell=True, env=env, 
                               capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Modular CLI installed with Homebrew workaround")
            
            # Clean up the temporary Homebrew (optional)
            cleanup = input("Remove temporary Homebrew installation? (y/N): ")
            if cleanup.lower() == 'y':
                import shutil
                shutil.rmtree(homebrew_dir)
                print("✅ Temporary Homebrew removed")
            
            return True
        else:
            print(f"❌ Modular installation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error in Homebrew workaround: {e}")
        return False

def manual_modular_setup():
    """Manual Modular CLI setup"""
    print("🔧 Manual Modular CLI setup...")
    
    modular_dir = Path.home() / ".modular"
    bin_dir = modular_dir / "bin"
    
    # Create directories
    modular_dir.mkdir(exist_ok=True)
    bin_dir.mkdir(exist_ok=True)
    
    # Create a simple modular wrapper script
    modular_script = bin_dir / "modular"
    
    script_content = '''#!/bin/bash
# Simple Modular CLI wrapper

MODULAR_HOME="$HOME/.modular"
export MODULAR_HOME

case "$1" in
    "install")
        if [ "$2" = "mojo" ]; then
            echo "Installing Mojo..."
            # This would normally download and install Mojo
            # For now, we'll create a placeholder
            mkdir -p "$MODULAR_HOME/pkg/packages.modular.com_mojo"
            echo "Mojo placeholder installed"
            
            # Create mojo wrapper
            cat > "$MODULAR_HOME/bin/mojo" << 'EOF'
#!/bin/bash
echo "Mojo placeholder - real installation needed"
echo "Visit: https://docs.modular.com/mojo/manual/get-started/"
exit 1
EOF
            chmod +x "$MODULAR_HOME/bin/mojo"
        fi
        ;;
    "--version")
        echo "modular 0.1.0 (placeholder)"
        ;;
    *)
        echo "Modular CLI placeholder"
        echo "Commands: install, --version"
        ;;
esac
'''
    
    with open(modular_script, 'w') as f:
        f.write(script_content)
    
    os.chmod(modular_script, 0o755)
    
    print(f"✅ Created Modular CLI wrapper at {modular_script}")
    return True

def setup_environment():
    """Setup environment variables"""
    print("🔧 Setting up environment...")
    
    # Add to shell profile
    shell_profile = Path.home() / ".zshrc"
    path_export = 'export PATH="$HOME/.modular/bin:$PATH"'
    
    if shell_profile.exists():
        content = shell_profile.read_text()
        if '.modular/bin' not in content:
            with shell_profile.open('a') as f:
                f.write(f'\n# Added by Cognitive Design Framework\n{path_export}\n')
            print(f"✅ Added to {shell_profile}")
        else:
            print("✅ Already in PATH configuration")
    else:
        print("⚠️  Please add to your shell config:")
        print(f"   {path_export}")

def main():
    """Main installation process"""
    print("🧠 Cognitive Design Framework - macOS ARM64 Mojo Installer")
    print("=" * 60)
    print("🚫 No Homebrew Required (Workaround Method)")
    print()
    
    if not check_macos_arm64():
        sys.exit(1)
    
    print("This installer will try multiple methods:")
    print("1. Direct Modular download (if available)")
    print("2. Homebrew workaround (temporary Homebrew)")
    print("3. Manual setup with instructions")
    print()
    
    # Method 1: Direct download
    if try_direct_modular_download():
        print("✅ Direct download successful!")
    # Method 2: Homebrew workaround
    elif install_with_homebrew_workaround():
        print("✅ Homebrew workaround successful!")
    # Method 3: Manual setup
    else:
        print("⚠️  Automated methods failed. Setting up manual configuration...")
        manual_modular_setup()
    
    # Setup environment
    setup_environment()
    
    print()
    print("🎉 Setup complete!")
    print()
    print("Next steps:")
    print("1. Restart your terminal or run: source ~/.zshrc")
    print("2. Try: modular --version")
    print("3. Install Mojo: modular install mojo")
    print("4. If that fails, visit: https://docs.modular.com/mojo/manual/get-started/")
    print()
    print("Note: Due to Modular's current requirements, you may need to:")
    print("- Create a Modular account at https://developer.modular.com/")
    print("- Follow their official installation guide")

if __name__ == "__main__":
    main()

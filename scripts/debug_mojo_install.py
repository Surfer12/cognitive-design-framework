#!/usr/bin/env python3
"""
Debug script for Mojo installation issues on macOS ARM64
"""

import os
import platform
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

def check_system_requirements():
    """Check system requirements for Mojo on macOS ARM64"""
    print("🔍 System Requirements Check")
    print("=" * 30)
    
    # System info
    system = platform.system()
    machine = platform.machine()
    version = platform.mac_ver()[0] if system == 'Darwin' else 'N/A'
    
    print(f"System: {system}")
    print(f"Architecture: {machine}")
    print(f"macOS Version: {version}")
    print()
    
    # Check macOS version (Mojo requires macOS 11.0+)
    if system == 'Darwin':
        major_version = int(version.split('.')[0]) if version != 'N/A' else 0
        if major_version < 11:
            print("❌ macOS version too old. Mojo requires macOS 11.0 (Big Sur) or later")
            return False
        else:
            print("✅ macOS version compatible")
    
    # Check for Xcode Command Line Tools
    try:
        result = subprocess.run(['xcode-select', '-p'], 
                               capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Xcode Command Line Tools: {result.stdout.strip()}")
        else:
            print("❌ Xcode Command Line Tools not installed")
            print("Run: xcode-select --install")
            return False
    except FileNotFoundError:
        print("❌ xcode-select not found")
        return False
    
    # Check for curl
    try:
        result = subprocess.run(['curl', '--version'], 
                               capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ curl available")
        else:
            print("❌ curl not working properly")
            return False
    except FileNotFoundError:
        print("❌ curl not found")
        return False
    
    # Check internet connectivity
    try:
        urllib.request.urlopen('https://get.modular.com', timeout=10)
        print("✅ Internet connectivity to Modular")
    except Exception as e:
        print(f"❌ Cannot reach Modular servers: {e}")
        return False
    
    return True

def test_modular_installer():
    """Test the Modular installer download and execution"""
    print("\n🧪 Testing Modular Installer")
    print("=" * 30)
    
    try:
        # Download installer
        print("Downloading installer...")
        with urllib.request.urlopen('https://get.modular.com') as response:
            installer_content = response.read().decode('utf-8')
        
        print(f"✅ Downloaded installer ({len(installer_content)} bytes)")
        
        # Check if it looks like a valid shell script
        if installer_content.startswith('#!/'):
            print("✅ Installer appears to be a valid shell script")
        else:
            print("❌ Installer doesn't look like a shell script")
            print("First 200 characters:")
            print(installer_content[:200])
            return False
        
        # Save to temp file and test
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as f:
            f.write(installer_content)
            temp_path = f.name
        
        os.chmod(temp_path, 0o755)
        
        # Test with --help flag (safer than full install)
        print("Testing installer with --help...")
        result = subprocess.run(['bash', temp_path, '--help'], 
                               capture_output=True, text=True, timeout=30)
        
        print(f"Installer help exit code: {result.returncode}")
        if result.stdout:
            print("Installer help output:")
            print(result.stdout[:500])
        if result.stderr:
            print("Installer help errors:")
            print(result.stderr[:500])
        
        # Clean up
        os.unlink(temp_path)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error testing installer: {e}")
        return False

def try_alternative_install():
    """Try alternative installation methods"""
    print("\n🔄 Alternative Installation Methods")
    print("=" * 35)
    
    # Method 1: Direct download with specific flags
    print("Method 1: Direct install with verbose output")
    try:
        cmd = "curl -fsSL https://get.modular.com | bash -s -- --verbose --no-modify-path"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        
        print(f"Exit code: {result.returncode}")
        if result.stdout:
            print("Output:", result.stdout[-500:])  # Last 500 chars
        if result.stderr:
            print("Errors:", result.stderr[-500:])
        
        if result.returncode == 0:
            print("✅ Method 1 succeeded!")
            return True
    except Exception as e:
        print(f"Method 1 failed: {e}")
    
    # Method 2: Manual download and install
    print("\nMethod 2: Manual download and install")
    try:
        # Download to specific location
        installer_path = Path.home() / "modular_installer.sh"
        
        print(f"Downloading to {installer_path}")
        urllib.request.urlretrieve('https://get.modular.com', installer_path)
        
        # Make executable
        os.chmod(installer_path, 0o755)
        
        # Run with specific environment
        env = os.environ.copy()
        env['SHELL'] = '/bin/bash'
        
        result = subprocess.run(['bash', str(installer_path), '--no-modify-path'], 
                               capture_output=True, text=True, env=env, timeout=300)
        
        print(f"Exit code: {result.returncode}")
        if result.stdout:
            print("Output:", result.stdout[-500:])
        if result.stderr:
            print("Errors:", result.stderr[-500:])
        
        # Clean up
        installer_path.unlink()
        
        if result.returncode == 0:
            print("✅ Method 2 succeeded!")
            return True
            
    except Exception as e:
        print(f"Method 2 failed: {e}")
    
    return False

def check_existing_installation():
    """Check if Modular/Mojo is already partially installed"""
    print("\n🔍 Checking Existing Installation")
    print("=" * 35)
    
    modular_dir = Path.home() / ".modular"
    
    if modular_dir.exists():
        print(f"✅ Modular directory exists: {modular_dir}")
        
        # Check contents
        for item in modular_dir.iterdir():
            print(f"  - {item.name}")
        
        # Check for binaries
        bin_dir = modular_dir / "bin"
        if bin_dir.exists():
            print(f"✅ Bin directory exists: {bin_dir}")
            for binary in bin_dir.iterdir():
                if binary.is_file() and os.access(binary, os.X_OK):
                    print(f"  - {binary.name} (executable)")
                else:
                    print(f"  - {binary.name}")
        
        # Try to run modular
        modular_bin = bin_dir / "modular"
        if modular_bin.exists():
            try:
                result = subprocess.run([str(modular_bin), '--version'], 
                                       capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ Modular CLI working: {result.stdout.strip()}")
                    return True
                else:
                    print(f"❌ Modular CLI not working: {result.stderr}")
            except Exception as e:
                print(f"❌ Error running Modular CLI: {e}")
    else:
        print("❌ No existing Modular installation found")
    
    return False

def provide_manual_instructions():
    """Provide manual installation instructions"""
    print("\n📖 Manual Installation Instructions")
    print("=" * 40)
    
    print("If automated installation fails, try these steps:")
    print()
    print("1. Ensure Xcode Command Line Tools are installed:")
    print("   xcode-select --install")
    print()
    print("2. Create a Modular account at: https://developer.modular.com/")
    print()
    print("3. Download the installer manually:")
    print("   curl -L -o ~/modular_installer.sh https://get.modular.com")
    print("   chmod +x ~/modular_installer.sh")
    print()
    print("4. Run the installer with debug output:")
    print("   bash -x ~/modular_installer.sh --no-modify-path")
    print()
    print("5. If successful, add to PATH:")
    print("   echo 'export PATH=\"$HOME/.modular/bin:$PATH\"' >> ~/.zshrc")
    print("   source ~/.zshrc")
    print()
    print("6. Install Mojo:")
    print("   modular install mojo")
    print()
    print("7. Verify installation:")
    print("   mojo --version")

def main():
    """Main debug function"""
    print("🧠 Cognitive Design Framework - Mojo Installation Debug")
    print("=" * 55)
    print("🍎 macOS ARM64 Troubleshooting")
    print()
    
    # Check system requirements
    if not check_system_requirements():
        print("\n❌ System requirements not met. Please fix the issues above.")
        provide_manual_instructions()
        return
    
    # Check existing installation
    if check_existing_installation():
        print("\n✅ Modular CLI already installed and working!")
        print("Try installing Mojo: modular install mojo")
        return
    
    # Test installer
    if not test_modular_installer():
        print("\n❌ Modular installer test failed")
    
    # Try alternative methods
    if try_alternative_install():
        print("\n✅ Alternative installation succeeded!")
        print("Try: modular install mojo")
    else:
        print("\n❌ All automated methods failed")
        provide_manual_instructions()

if __name__ == "__main__":
    main()

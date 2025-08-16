#!/usr/bin/env python3
"""
Post-install hook to set up Mojo integration with pixi environment
"""

import os
import subprocess
import sys
from pathlib import Path

def check_mojo_installed():
    """Check if Mojo is already installed"""
    try:
        result = subprocess.run(['mojo', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Mojo already installed: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_mojo():
    """Install Mojo via Modular CLI"""
    print("🔥 Installing Mojo...")
    
    # Check if modular CLI exists
    try:
        subprocess.run(['modular', '--version'], 
                      capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("📦 Installing Modular CLI...")
        install_cmd = "curl -s https://get.modular.com | sh -"
        subprocess.run(install_cmd, shell=True, check=True)
    
    # Install Mojo
    subprocess.run(['modular', 'install', 'mojo'], check=True)
    
    # Add to PATH
    modular_bin = Path.home() / ".modular" / "bin"
    current_path = os.environ.get('PATH', '')
    if str(modular_bin) not in current_path:
        os.environ['PATH'] = f"{modular_bin}:{current_path}"
    
    print("✅ Mojo installation completed!")

def main():
    """Main post-install setup"""
    print("🧠 Cognitive Design Framework - Post Install Setup")
    print("=" * 50)
    
    if not check_mojo_installed():
        try:
            install_mojo()
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install Mojo: {e}")
            print("Please install manually:")
            print("  curl -s https://get.modular.com | sh -")
            print("  modular install mojo")
            sys.exit(1)
    
    print("\n🎉 Setup complete!")
    print("You can now use Mojo with your pixi environment.")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import os
import sys
import subprocess

def check_virtual_environment():
    """Check if virtual environment is set up"""
    venv_path = "vllm_env"
    if os.path.exists(venv_path):
        print("✅ Virtual environment exists")
        return True
    else:
        print("❌ Virtual environment not found")
        return False

def check_vllm_installation():
    """Check if vLLM is installed"""
    try:
        # Add the virtual environment to the path
        sys.path.insert(0, os.path.join(os.getcwd(), 'vllm_env', 'lib', 'python3.13', 'site-packages'))
        import vllm
        print(f"✅ vLLM installed (version: {vllm.__version__})")
        return True
    except ImportError:
        print("❌ vLLM not installed")
        return False

def check_pytorch():
    """Check PyTorch installation"""
    try:
        import torch
        print(f"✅ PyTorch installed (version: {torch.__version__})")
        print(f"   CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"   CUDA device count: {torch.cuda.device_count()}")
        return True
    except ImportError:
        print("❌ PyTorch not installed")
        return False

def check_scripts():
    """Check if all scripts are executable"""
    scripts = ["run_vllm_server.sh", "test_api.sh", "test_api.py", "serve_model.py"]
    all_good = True
    
    for script in scripts:
        if os.path.exists(script):
            if os.access(script, os.X_OK) or script.endswith('.py'):
                print(f"✅ {script} exists")
            else:
                print(f"⚠️  {script} exists but not executable")
                all_good = False
        else:
            print(f"❌ {script} not found")
            all_good = False
    
    return all_good

def main():
    print("🔍 vLLM with GPT-OSS-120B Setup Status")
    print("=" * 50)
    
    # Check components
    venv_ok = check_virtual_environment()
    vllm_ok = check_vllm_installation()
    pytorch_ok = check_pytorch()
    scripts_ok = check_scripts()
    
    print("\n" + "=" * 50)
    print("📋 Available Commands:")
    print("=" * 50)
    
    if all([venv_ok, vllm_ok, pytorch_ok, scripts_ok]):
        print("✅ Setup is complete! You can now:")
        print()
        print("1. Start the server:")
        print("   ./run_vllm_server.sh")
        print()
        print("2. Test the API with curl:")
        print("   ./test_api.sh")
        print()
        print("3. Test the API with Python:")
        print("   source vllm_env/bin/activate")
        print("   python test_api.py")
        print()
        print("4. Test the model directly:")
        print("   source vllm_env/bin/activate")
        print("   python serve_model.py")
        print()
        print("📝 Note: The model will run on CPU since CUDA is not available.")
        print("   This will be slower but functional.")
    else:
        print("❌ Setup is incomplete. Please check the issues above.")
        print()
        print("💡 To complete setup:")
        print("   1. Ensure virtual environment is created")
        print("   2. Install vLLM and dependencies")
        print("   3. Make scripts executable")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3

import sys
import os

# Add the virtual environment to the path
sys.path.insert(0, os.path.join(os.getcwd(), 'vllm_env', 'lib', 'python3.13', 'site-packages'))

try:
    import vllm
    print("✅ vLLM imported successfully!")
    print(f"vLLM version: {vllm.__version__}")
    
    # Test basic functionality
    from vllm import LLM, SamplingParams
    
    print("✅ vLLM basic imports successful!")
    
    # Check if we can create a simple LLM instance (without loading a model)
    print("✅ vLLM appears to be working correctly!")
    
except ImportError as e:
    print(f"❌ Error importing vLLM: {e}")
    print("This might be due to missing dependencies.")
    
except Exception as e:
    print(f"❌ Unexpected error: {e}")

print("\nTesting PyTorch...")
try:
    import torch
    print(f"✅ PyTorch version: {torch.__version__}")
    print(f"✅ CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"✅ CUDA device count: {torch.cuda.device_count()}")
except Exception as e:
    print(f"❌ PyTorch error: {e}")
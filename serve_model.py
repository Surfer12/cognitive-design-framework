#!/usr/bin/env python3

import os
import sys

# Add the virtual environment to the path
sys.path.insert(0, os.path.join(os.getcwd(), 'vllm_env', 'lib', 'python3.13', 'site-packages'))

from vllm import LLM, SamplingParams
import torch

def main():
    print("🚀 Starting vLLM server with GPT-OSS-120B model...")
    
    # Check CUDA availability
    if torch.cuda.is_available():
        print("✅ CUDA is available - using GPU acceleration")
        device = "cuda"
    else:
        print("⚠️  CUDA not available - using CPU (this will be much slower)")
        device = "cpu"
    
    try:
        # Initialize the model
        print("📥 Loading GPT-OSS-120B model...")
        llm = LLM(
            model="openai/gpt-oss-120b",
            trust_remote_code=True,
            tensor_parallel_size=1,  # Adjust based on available GPUs
            gpu_memory_utilization=0.9,
            max_model_len=4096,
            dtype="auto"
        )
        
        print("✅ Model loaded successfully!")
        print(f"📊 Model info: {llm.llm_engine.model_config}")
        
        # Test the model
        print("\n🧪 Testing the model...")
        sampling_params = SamplingParams(
            temperature=0.7,
            top_p=0.9,
            max_tokens=100
        )
        
        prompt = "What is the capital of France?"
        outputs = llm.generate([prompt], sampling_params)
        
        print(f"📝 Test prompt: {prompt}")
        print(f"🤖 Model response: {outputs[0].outputs[0].text}")
        
        print("\n🎉 vLLM server is ready!")
        print("💡 You can now use the model for inference.")
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        print("💡 This might be due to:")
        print("   - Insufficient memory")
        print("   - Network issues downloading the model")
        print("   - Missing dependencies")
        return False
    
    return True

if __name__ == "__main__":
    main()
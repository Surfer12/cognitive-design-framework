#!/usr/bin/env python3

import os
import sys

# Add the virtual environment to the path
sys.path.insert(0, os.path.join(os.getcwd(), 'vllm_env', 'lib', 'python3.13', 'site-packages'))

from vllm import LLM, SamplingParams
import torch

def demo_vllm():
    """Demo of using vLLM with GPT-OSS-120B model"""
    
    print("🚀 vLLM with GPT-OSS-120B Demo")
    print("=" * 50)
    
    # Check CUDA availability
    if torch.cuda.is_available():
        print("✅ CUDA is available - using GPU acceleration")
    else:
        print("⚠️  CUDA not available - using CPU (this will be slower)")
    
    try:
        print("\n📥 Loading GPT-OSS-120B model...")
        print("💡 This may take a while on first run as the model needs to be downloaded.")
        
        # Initialize the model
        llm = LLM(
            model="openai/gpt-oss-120b",
            trust_remote_code=True,
            tensor_parallel_size=1,
            gpu_memory_utilization=0.9,
            max_model_len=4096,
            dtype="auto"
        )
        
        print("✅ Model loaded successfully!")
        
        # Define sampling parameters
        sampling_params = SamplingParams(
            temperature=0.7,
            top_p=0.9,
            max_tokens=200
        )
        
        # Test prompts
        test_prompts = [
            "What is the capital of France?",
            "Explain quantum computing in simple terms.",
            "Write a short poem about artificial intelligence.",
            "What are the main benefits of renewable energy?"
        ]
        
        print(f"\n🧪 Running {len(test_prompts)} test prompts...")
        
        for i, prompt in enumerate(test_prompts, 1):
            print(f"\n📝 Test {i}: {prompt}")
            print("-" * 40)
            
            # Generate response
            outputs = llm.generate([prompt], sampling_params)
            response = outputs[0].outputs[0].text
            
            print(f"🤖 Response: {response}")
            print(f"📊 Tokens generated: {len(outputs[0].outputs[0].token_ids)}")
        
        print("\n🎉 Demo completed successfully!")
        print("💡 You can now use this model for your own applications.")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        print("💡 This might be due to:")
        print("   - Insufficient memory")
        print("   - Network issues downloading the model")
        print("   - Missing dependencies")

if __name__ == "__main__":
    demo_vllm()
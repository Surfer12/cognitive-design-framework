#!/usr/bin/env python3
"""
vLLM Installation and Usage Demo

This script demonstrates how to install and use vLLM for serving OpenAI GPT-OSS-120B model.
Due to complex dependencies (Rust compiler, CUDA, etc.), this serves as a reference guide.
"""

import subprocess
import sys
import os

def print_section(title):
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def main():
    print_section("vLLM Installation and Usage Guide")
    
    print("\n📦 OPTION 1: PIP INSTALLATION")
    print("-" * 30)
    print("# Create virtual environment")
    print("python3 -m venv vllm_env")
    print("source vllm_env/bin/activate")
    print()
    print("# Install vLLM")
    print("pip install vllm")
    print()
    print("# Start vLLM server")
    print('vllm serve "openai/gpt-oss-120b"')
    print()
    print("# Test the server with curl")
    print("""curl -X POST "http://localhost:8000/v1/chat/completions" \\
    -H "Content-Type: application/json" \\
    --data '{
        "model": "openai/gpt-oss-120b",
        "messages": [
            {
                "role": "user",
                "content": "What is the capital of France?"
            }
        ]
    }'""")

    print("\n🐳 OPTION 2: DOCKER INSTALLATION")
    print("-" * 30)
    print("# Deploy with Docker on Linux (requires NVIDIA Docker)")
    print("""docker run --runtime nvidia --gpus all \\
    --name my_vllm_container \\
    -v ~/.cache/huggingface:/root/.cache/huggingface \\
    --env "HUGGING_FACE_HUB_TOKEN=<your_token_here>" \\
    -p 8000:8000 \\
    --ipc=host \\
    vllm/vllm-openai:latest \\
    --model openai/gpt-oss-120b""")
    
    print("\n# Alternative: Run model inside container")
    print('docker exec -it my_vllm_container bash -c "vllm serve openai/gpt-oss-120b"')
    
    print("\n# Test the Docker deployment")
    print("""curl -X POST "http://localhost:8000/v1/chat/completions" \\
    -H "Content-Type: application/json" \\
    --data '{
        "model": "openai/gpt-oss-120b",
        "messages": [
            {
                "role": "user",
                "content": "What is the capital of France?"
            }
        ]
    }'""")

    print("\n🔧 PYTHON API USAGE")
    print("-" * 30)
    print("""# Python client example
from openai import OpenAI

# Point to the local vLLM server
client = OpenAI(
    api_key="EMPTY",  # vLLM doesn't require API key
    base_url="http://localhost:8000/v1",
)

completion = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {"role": "user", "content": "What is the capital of France?"}
    ]
)

print(completion.choices[0].message.content)""")

    print("\n⚠️  SYSTEM REQUIREMENTS")
    print("-" * 30)
    print("• Python 3.8+")
    print("• CUDA-compatible GPU (for GPU acceleration)")
    print("• Sufficient RAM/VRAM for the model (120B requires significant resources)")
    print("• Docker with NVIDIA Container Toolkit (for Docker option)")
    print("• Rust compiler (for some dependencies)")

    print("\n🚀 INSTALLATION TROUBLESHOOTING")
    print("-" * 30)
    print("If you encounter dependency issues:")
    print("1. Install Rust: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh")
    print("2. Install CUDA toolkit if using GPU")
    print("3. Use precompiled wheels: VLLM_USE_PRECOMPILED=1 pip install vllm")
    print("4. Consider using Docker for easier setup")

    print("\n✅ DEMO COMPLETED")
    print("This script demonstrates the vLLM installation and usage process.")
    print("For actual deployment, follow the commands shown above in your environment.")

if __name__ == "__main__":
    main()
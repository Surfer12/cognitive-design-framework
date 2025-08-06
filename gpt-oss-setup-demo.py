#!/usr/bin/env python3
"""
GPT-OSS Setup and Demo Script
=============================

This script demonstrates how to set up and use OpenAI's GPT-OSS models with various backends.
It covers the key components mentioned in the $500K Red Teaming Challenge announcement.

Features covered:
- Installation options for different backends (PyTorch, Triton, Metal, vLLM)
- Model downloading from Hugging Face
- Terminal chat interface
- Browser and Python tools integration
- Responses API server setup
- Codex integration

For the Red Teaming Challenge: https://github.com/openai/gpt-oss
"""

import os
import sys
import subprocess
import argparse
import platform
from pathlib import Path
from typing import Optional, List

class GPTOSSSetup:
    """Main setup class for GPT-OSS components"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.is_apple_silicon = self.system == "darwin" and platform.machine() == "arm64"
        self.project_dir = Path.cwd()
        
    def run_command(self, cmd: List[str], check: bool = True) -> subprocess.CompletedProcess:
        """Run a shell command with error handling"""
        print(f"Running: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, check=check, capture_output=True, text=True)
            if result.stdout:
                print(result.stdout)
            return result
        except subprocess.CalledProcessError as e:
            print(f"Error running command: {e}")
            if e.stderr:
                print(f"Error output: {e.stderr}")
            if check:
                raise
            return e
    
    def check_prerequisites(self):
        """Check system prerequisites"""
        print("🔍 Checking prerequisites...")
        
        # Check Python version
        if sys.version_info < (3, 12):
            print("❌ Python 3.12+ is required")
            return False
            
        # Check for required tools
        required_tools = ["git", "pip"]
        if self.system == "darwin":
            required_tools.append("xcode-select")
            
        for tool in required_tools:
            try:
                subprocess.run([tool, "--version"], capture_output=True, check=True)
                print(f"✅ {tool} found")
            except (subprocess.CalledProcessError, FileNotFoundError):
                print(f"❌ {tool} not found")
                return False
                
        return True
    
    def clone_repository(self):
        """Clone the GPT-OSS repository if not already present"""
        if not Path("gpt-oss").exists():
            print("📥 Cloning GPT-OSS repository...")
            self.run_command(["git", "clone", "https://github.com/openai/gpt-oss.git"])
        else:
            print("✅ GPT-OSS repository already exists")
    
    def install_base_package(self):
        """Install the base GPT-OSS package"""
        print("📦 Installing base GPT-OSS package...")
        os.chdir("gpt-oss")
        self.run_command(["pip", "install", "-e", "."])
    
    def install_backend(self, backend: str):
        """Install specific backend dependencies"""
        print(f"📦 Installing {backend} backend...")
        
        if backend == "torch":
            self.run_command(["pip", "install", "-e", ".[torch]"])
            
        elif backend == "triton":
            print("Installing Triton from source (required for GPT-OSS)...")
            # Clone and install triton
            if not Path("../triton").exists():
                os.chdir("..")
                self.run_command(["git", "clone", "https://github.com/triton-lang/triton"])
                os.chdir("triton")
                self.run_command(["pip", "install", "-r", "python/requirements.txt"])
                self.run_command(["pip", "install", "-e", ".", "--verbose", "--no-build-isolation"])
                os.chdir("../gpt-oss")
            
            self.run_command(["pip", "install", "-e", ".[triton]"])
            
        elif backend == "metal":
            if not self.is_apple_silicon:
                print("❌ Metal backend only available on Apple Silicon")
                return False
            self.run_command(["pip", "install", "-e", ".[metal]"])
            
        elif backend == "vllm":
            print("Installing vLLM with GPT-OSS support...")
            self.run_command([
                "pip", "install", "--pre", "vllm==0.10.1+gptoss",
                "--extra-index-url", "https://wheels.vllm.ai/gpt-oss/",
                "--extra-index-url", "https://download.pytorch.org/whl/nightly/cu128",
                "--index-strategy", "unsafe-best-match"
            ], check=False)  # May fail on some systems
            
        return True
    
    def download_models(self, model_size: str = "20b"):
        """Download GPT-OSS models from Hugging Face"""
        print(f"📥 Downloading GPT-OSS {model_size} model...")
        
        # Check if huggingface-cli is available
        try:
            self.run_command(["huggingface-cli", "--version"])
        except:
            print("Installing Hugging Face CLI...")
            self.run_command(["pip", "install", "huggingface_hub[cli]"])
        
        model_name = f"openai/gpt-oss-{model_size}"
        model_dir = f"gpt-oss-{model_size}"
        
        if not Path(model_dir).exists():
            # Download original weights
            self.run_command([
                "huggingface-cli", "download", model_name,
                "--include", "original/*",
                "--local-dir", f"{model_dir}/"
            ])
            
            # Download Metal weights if on Apple Silicon
            if self.is_apple_silicon:
                self.run_command([
                    "huggingface-cli", "download", model_name,
                    "--include", "metal/*",
                    "--local-dir", f"{model_dir}/metal/"
                ])
        else:
            print(f"✅ Model {model_size} already downloaded")
    
    def setup_environment_variables(self):
        """Set up required environment variables"""
        print("🔧 Setting up environment variables...")
        
        # For CUDA memory management
        os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
        
        # For EXA API (browser tool) - user needs to set this
        if not os.getenv("EXA_API_KEY"):
            print("⚠️  EXA_API_KEY not set - browser tool will not work")
            print("   Get your API key from: https://exa.ai/")
    
    def create_demo_scripts(self):
        """Create demonstration scripts"""
        print("📝 Creating demo scripts...")
        
        # Chat demo script
        chat_demo = '''#!/usr/bin/env python3
"""
GPT-OSS Chat Demo
Run with: python chat_demo.py
"""
import subprocess
import sys

def run_chat():
    """Run the GPT-OSS chat interface"""
    model_path = "gpt-oss-20b/original/"
    
    cmd = [
        sys.executable, "-m", "gpt_oss.chat",
        "--backend", "triton",  # or "torch", "vllm"
        "--reasoning-effort", "medium",
        "--python",  # Enable Python tool
        "--browser",  # Enable browser tool (needs EXA_API_KEY)
        model_path
    ]
    
    print("Starting GPT-OSS chat interface...")
    print("Available commands:")
    print("  --python: Enable Python execution")
    print("  --browser: Enable web browsing")
    print("  --reasoning-effort: low/medium/high")
    
    subprocess.run(cmd)

if __name__ == "__main__":
    run_chat()
'''
        
        with open("chat_demo.py", "w") as f:
            f.write(chat_demo)
        
        # API server demo
        api_demo = '''#!/usr/bin/env python3
"""
GPT-OSS Responses API Server Demo
Run with: python api_server_demo.py
"""
import subprocess
import sys

def run_api_server():
    """Run the GPT-OSS Responses API server"""
    cmd = [
        sys.executable, "-m", "gpt_oss.responses_api.serve",
        "--checkpoint", "gpt-oss-20b/original/",
        "--port", "8000",
        "--inference-backend", "triton"
    ]
    
    print("Starting GPT-OSS Responses API server on http://localhost:8000")
    subprocess.run(cmd)

if __name__ == "__main__":
    run_api_server()
'''
        
        with open("api_server_demo.py", "w") as f:
            f.write(api_demo)
        
        # Ollama setup script
        ollama_setup = '''#!/bin/bash
"""
GPT-OSS Ollama Setup
This script sets up GPT-OSS with Ollama for easy local inference
"""

echo "Setting up GPT-OSS with Ollama..."

# Install Ollama if not present
if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
fi

# Pull GPT-OSS models
echo "Pulling GPT-OSS 20B model..."
ollama pull gpt-oss:20b

echo "Pulling GPT-OSS 120B model..."
ollama pull gpt-oss:120b

echo "✅ Setup complete! You can now run:"
echo "  ollama run gpt-oss:20b"
echo "  ollama run gpt-oss:120b"
'''
        
        with open("setup_ollama.sh", "w") as f:
            f.write(ollama_setup)
        os.chmod("setup_ollama.sh", 0o755)
        
        # Codex configuration
        codex_config = '''# GPT-OSS Codex Configuration
# Save this to ~/.codex/config.toml

disable_response_storage = true
show_reasoning_content = true

[model_providers.local]
name = "local"
base_url = "http://localhost:11434/v1"  # Ollama default

[profiles.oss]
model = "gpt-oss:20b"
model_provider = "local"

# Usage:
# 1. Start Ollama: ollama run gpt-oss:20b
# 2. Run Codex: codex -p oss
'''
        
        with open("codex_config.toml", "w") as f:
            f.write(codex_config)
        
        print("✅ Demo scripts created:")
        print("  - chat_demo.py: Terminal chat interface")
        print("  - api_server_demo.py: Responses API server")
        print("  - setup_ollama.sh: Ollama setup script")
        print("  - codex_config.toml: Codex configuration")
    
    def create_red_teaming_guide(self):
        """Create a guide for the Red Teaming Challenge"""
        guide = '''# GPT-OSS Red Teaming Challenge Guide

## Overview
OpenAI is launching a $500K Red Teaming Challenge to strengthen open source safety.
Researchers, developers, and enthusiasts worldwide are invited to help uncover novel risks.

## Challenge Details
- **Prize Pool**: $500,000
- **Judges**: Experts from OpenAI and other leading labs  
- **Goal**: Discover novel risks in GPT-OSS models
- **Repository**: https://github.com/openai/gpt-oss

## Getting Started

### 1. Model Access
Two models are available:
- `gpt-oss-120b`: Production-ready, high reasoning (117B params, 5.1B active)
- `gpt-oss-20b`: Lower latency, local use (21B params, 3.6B active)

### 2. Key Areas to Explore

#### Safety & Security
- Prompt injection vulnerabilities
- Jailbreaking attempts
- Information leakage
- Adversarial inputs

#### Tool Usage Risks
- Python code execution safety
- Web browsing security
- File system access controls
- Container escape attempts

#### Model Behavior
- Reasoning chain manipulation
- Output consistency issues
- Hallucination patterns
- Bias and fairness concerns

#### Technical Vulnerabilities
- Memory safety issues
- Quantization artifacts
- Model extraction attempts
- Performance degradation attacks

### 3. Testing Framework

Use the provided tools:
```bash
# Terminal chat with tools
python -m gpt_oss.chat --python --browser gpt-oss-20b/original/

# API server for automated testing
python -m gpt_oss.responses_api.serve --checkpoint gpt-oss-20b/original/
```

### 4. Documentation & Reporting

Document your findings with:
- Clear reproduction steps
- Impact assessment
- Proposed mitigations
- Code examples

### 5. Harmony Format
Models use the Harmony response format - understanding this is crucial:
- Chain-of-thought reasoning
- Tool calling mechanisms
- Message structure
- Error handling

## Resources
- [Model Card](https://openai.com/index/gpt-oss-model-card)
- [OpenAI Blog](https://openai.com/index/introducing-gpt-oss/)
- [Cookbook](https://cookbook.openai.com/topic/gpt-oss)
- [Harmony Documentation](https://github.com/openai/harmony)

## Submission Guidelines
Check the official repository for submission guidelines and deadlines.

Good luck finding those novel risks! 🔍
'''
        
        with open("RED_TEAMING_GUIDE.md", "w") as f:
            f.write(guide)
        
        print("✅ Red Teaming Challenge guide created: RED_TEAMING_GUIDE.md")

def main():
    parser = argparse.ArgumentParser(description="GPT-OSS Setup and Demo")
    parser.add_argument("--backend", choices=["torch", "triton", "metal", "vllm", "all"], 
                       default="triton", help="Backend to install")
    parser.add_argument("--model-size", choices=["20b", "120b"], default="20b",
                       help="Model size to download")
    parser.add_argument("--skip-download", action="store_true",
                       help="Skip model download")
    parser.add_argument("--setup-only", action="store_true",
                       help="Only setup, don't create demos")
    
    args = parser.parse_args()
    
    setup = GPTOSSSetup()
    
    print("🚀 GPT-OSS Setup and Demo")
    print("=" * 50)
    
    # Check prerequisites
    if not setup.check_prerequisites():
        print("❌ Prerequisites not met. Please install required tools.")
        return 1
    
    try:
        # Setup steps
        setup.clone_repository()
        setup.install_base_package()
        
        # Install backends
        if args.backend == "all":
            backends = ["torch", "triton"]
            if setup.is_apple_silicon:
                backends.append("metal")
            backends.append("vllm")
        else:
            backends = [args.backend]
        
        for backend in backends:
            if not setup.install_backend(backend):
                print(f"⚠️  Failed to install {backend} backend")
        
        # Download models
        if not args.skip_download:
            setup.download_models(args.model_size)
        
        # Setup environment
        setup.setup_environment_variables()
        
        # Create demos and guides
        if not args.setup_only:
            setup.create_demo_scripts()
            setup.create_red_teaming_guide()
        
        print("\n🎉 Setup complete!")
        print("\nNext steps:")
        print("1. Set EXA_API_KEY for browser tool: export EXA_API_KEY=your_key")
        print("2. Run chat demo: python chat_demo.py")
        print("3. Start API server: python api_server_demo.py")
        print("4. Check RED_TEAMING_GUIDE.md for challenge details")
        
        return 0
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
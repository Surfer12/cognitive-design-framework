# GPT-OSS Comprehensive Guide

## 🚀 OpenAI's $500K Red Teaming Challenge

OpenAI has launched a **$500,000 Red Teaming Challenge** to strengthen open source safety. Researchers, developers, and enthusiasts worldwide are invited to help uncover novel risks in the GPT-OSS models, judged by experts from OpenAI and other leading labs.

**Repository**: https://github.com/openai/gpt-oss

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Models](#models)
3. [Key Features](#key-features)
4. [Installation & Setup](#installation--setup)
5. [Usage Examples](#usage-examples)
6. [Tools & Capabilities](#tools--capabilities)
7. [Inference Backends](#inference-backends)
8. [Red Teaming Guide](#red-teaming-guide)
9. [Integration Options](#integration-options)
10. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

GPT-OSS is OpenAI's series of open-weight models designed for powerful reasoning, agentic tasks, and versatile developer use cases. These models are released under the permissive **Apache 2.0 license** and feature native capabilities for function calling, web browsing, and Python code execution.

### Models Available

| Model | Parameters | Active Parameters | Use Case | Hardware Requirements |
|-------|------------|-------------------|----------|----------------------|
| **gpt-oss-120b** | 117B | 5.1B | Production, high reasoning | Single H100 GPU |
| **gpt-oss-20b** | 21B | 3.6B | Lower latency, local use | 16GB+ memory |

---

## 🔑 Key Features

### 🎛️ **Configurable Reasoning Effort**
Easily adjust reasoning effort (low, medium, high) based on your specific use case and latency needs.

### 🔍 **Full Chain-of-Thought**
Complete access to the model's reasoning process for easier debugging and increased trust in outputs.

### 🛠️ **Agentic Capabilities**
Native support for:
- Function calling
- Web browsing (via browser tool)
- Python code execution
- Structured outputs

### ⚡ **Native MXFP4 Quantization**
Models trained with native MXFP4 precision for MoE layers, enabling efficient inference on single GPUs.

### 🎨 **Fine-tunable**
Fully customizable through parameter fine-tuning for specific use cases.

---

## 🛠️ Installation & Setup

### Quick Start

```bash
# Clone the repository and run setup
git clone https://github.com/openai/gpt-oss.git
cd gpt-oss

# Install base package
pip install -e .

# Install with specific backend
pip install -e .[triton]  # Recommended for single GPU
pip install -e .[torch]   # Educational/multi-GPU
pip install -e .[metal]   # Apple Silicon only
```

### System Requirements

| Platform | Requirements |
|----------|-------------|
| **macOS** | Xcode CLI tools: `xcode-select --install` |
| **Linux** | CUDA support required |
| **Windows** | Use Ollama or other solutions (reference implementations not tested) |

### Model Download

```bash
# Install Hugging Face CLI
pip install huggingface_hub[cli]

# Download GPT-OSS 20B
huggingface-cli download openai/gpt-oss-20b --include "original/*" --local-dir gpt-oss-20b/

# Download GPT-OSS 120B  
huggingface-cli download openai/gpt-oss-120b --include "original/*" --local-dir gpt-oss-120b/
```

---

## 💻 Usage Examples

### Terminal Chat Interface

```bash
# Basic chat
python -m gpt_oss.chat gpt-oss-20b/original/

# With tools enabled
python -m gpt_oss.chat \
  --backend triton \
  --reasoning-effort medium \
  --python \
  --browser \
  gpt-oss-20b/original/
```

### Python API Usage

```python
from transformers import pipeline
import torch

model_id = "openai/gpt-oss-20b"

pipe = pipeline(
    "text-generation",
    model=model_id,
    torch_dtype="auto",
    device_map="auto",
)

messages = [
    {"role": "user", "content": "Explain quantum mechanics clearly and concisely."},
]

outputs = pipe(messages, max_new_tokens=256)
print(outputs[0]["generated_text"][-1])
```

### vLLM Server

```bash
# Install vLLM with GPT-OSS support
uv pip install --pre vllm==0.10.1+gptoss \
    --extra-index-url https://wheels.vllm.ai/gpt-oss/ \
    --extra-index-url https://download.pytorch.org/whl/nightly/cu128 \
    --index-strategy unsafe-best-match

# Start server
vllm serve openai/gpt-oss-20b
```

### Ollama (Consumer Hardware)

```bash
# Install and run with Ollama
ollama pull gpt-oss:20b
ollama run gpt-oss:20b

# For 120B model
ollama pull gpt-oss:120b
ollama run gpt-oss:120b
```

---

## 🔧 Tools & Capabilities

### Browser Tool

The browser tool enables web search and browsing capabilities:

```python
from gpt_oss.tools.simple_browser import SimpleBrowserTool
from gpt_oss.tools.simple_browser.backend import ExaBackend

# Requires EXA_API_KEY environment variable
backend = ExaBackend(source="web")
browser_tool = SimpleBrowserTool(backend=backend)
```

**Available Methods:**
- `search`: Search for key phrases
- `open`: Open a particular page  
- `find`: Look for contents on a page

### Python Tool

Stateless Python code execution in Docker container:

```python
from gpt_oss.tools.python_docker.docker_tool import PythonTool

python_tool = PythonTool()
```

**⚠️ Warning**: Runs in permissive Docker container - implement your own restrictions for production.

### Apply Patch Tool

Create, update, or delete files locally:

```bash
python -m gpt_oss.chat --apply-patch gpt-oss-20b/original/
```

---

## 🖥️ Inference Backends

### Triton (Recommended)

Optimized for single GPU inference with MXFP4 support:

```bash
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
python -m gpt_oss.generate --backend triton gpt-oss-120b/original/
```

### PyTorch (Educational)

Reference implementation for learning (requires 4x H100s):

```bash
torchrun --nproc-per-node=4 -m gpt_oss.generate gpt-oss-120b/original/
```

### Metal (Apple Silicon)

Optimized for Apple Silicon hardware:

```bash
# Convert weights
python gpt_oss/metal/scripts/create-local-model.py -s <model_dir> -d <output_file>

# Or download pre-converted
huggingface-cli download openai/gpt-oss-20b --include "metal/*" --local-dir gpt-oss-20b/metal/

# Run inference
python gpt_oss/metal/examples/generate.py gpt-oss-20b/metal/model.bin -p "why did the chicken cross the road?"
```

---

## 🔍 Red Teaming Guide

### Challenge Focus Areas

#### 🛡️ **Safety & Security**
- Prompt injection vulnerabilities
- Jailbreaking attempts  
- Information leakage
- Adversarial inputs

#### 🔧 **Tool Usage Risks**
- Python code execution safety
- Web browsing security
- File system access controls
- Container escape attempts

#### 🧠 **Model Behavior**
- Reasoning chain manipulation
- Output consistency issues
- Hallucination patterns
- Bias and fairness concerns

#### 💾 **Technical Vulnerabilities**
- Memory safety issues
- Quantization artifacts
- Model extraction attempts
- Performance degradation attacks

### Testing Framework

```bash
# Interactive testing
python -m gpt_oss.chat --python --browser gpt-oss-20b/original/

# API server for automated testing
python -m gpt_oss.responses_api.serve --checkpoint gpt-oss-20b/original/
```

### Documentation Requirements

For challenge submissions, document:
- Clear reproduction steps
- Impact assessment  
- Proposed mitigations
- Code examples

---

## 🔗 Integration Options

### Responses API Server

```bash
python -m gpt_oss.responses_api.serve \
  --checkpoint gpt-oss-20b/original/ \
  --port 8000 \
  --inference-backend triton
```

### Codex Integration

Create `~/.codex/config.toml`:

```toml
disable_response_storage = true
show_reasoning_content = true

[model_providers.local]
name = "local"
base_url = "http://localhost:11434/v1"

[profiles.oss]
model = "gpt-oss:20b"
model_provider = "local"
```

Usage:
```bash
ollama run gpt-oss:20b
codex -p oss
```

### LM Studio

```bash
# Download models
lms get openai/gpt-oss-20b
lms get openai/gpt-oss-120b
```

---

## 🚨 Troubleshooting

### Common Issues

#### CUDA Out of Memory
```bash
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
```

#### Triton Installation Issues
```bash
# Install from source
git clone https://github.com/triton-lang/triton
cd triton/
pip install -r python/requirements.txt
pip install -e . --verbose --no-build-isolation
```

#### EXA API Key Missing
```bash
export EXA_API_KEY=your_key_here
```

#### Docker Issues (Python Tool)
Ensure Docker is running and accessible:
```bash
docker --version
docker run hello-world
```

### Performance Optimization

#### Recommended Sampling Parameters
- `temperature=1.0`
- `top_p=1.0`

#### Memory Management
- Use expandable CUDA allocator
- Consider model quantization for limited hardware
- Monitor GPU memory usage

---

## 📚 Resources

- **Model Card**: https://openai.com/index/gpt-oss-model-card
- **OpenAI Blog**: https://openai.com/index/introducing-gpt-oss/
- **Cookbook**: https://cookbook.openai.com/topic/gpt-oss
- **Harmony Documentation**: https://github.com/openai/harmony
- **Awesome GPT-OSS**: [./awesome-gpt-oss.md](./awesome-gpt-oss.md)

---

## 🤝 Contributing

The reference implementations are meant as starting points. Outside of bug fixes, feature contributions should be added to the [awesome-gpt-oss.md](./awesome-gpt-oss.md) file.

---

## 📄 License

Apache 2.0 License - Build freely without copyleft restrictions or patent risk.

---

## 🎯 Getting Started Checklist

- [ ] Install prerequisites (Python 3.12+, Git, CUDA/Xcode)
- [ ] Clone repository: `git clone https://github.com/openai/gpt-oss.git`
- [ ] Install backend: `pip install -e .[triton]`
- [ ] Download model: `huggingface-cli download openai/gpt-oss-20b`
- [ ] Set environment variables: `export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`
- [ ] Test installation: `python -m gpt_oss.chat gpt-oss-20b/original/`
- [ ] Enable tools: Set `EXA_API_KEY` for browser tool
- [ ] Explore red teaming opportunities! 🔍

---

**Ready to contribute to the $500K Red Teaming Challenge? Start exploring the models and discover novel risks to strengthen open source AI safety!** 🚀
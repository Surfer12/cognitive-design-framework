# vLLM with GPT-OSS-120B Setup

This repository contains a setup for running the GPT-OSS-120B model using vLLM (Very Large Language Model inference engine).

## 🚀 Quick Start

### 1. Environment Setup

The virtual environment is already set up with all necessary dependencies:

```bash
# Activate the virtual environment
source vllm_env/bin/activate
```

### 2. Start the vLLM Server

Run the server script:

```bash
./run_vllm_server.sh
```

Or manually:

```bash
source vllm_env/bin/activate
vllm serve "openai/gpt-oss-120b" \
    --trust-remote-code \
    --tensor-parallel-size 1 \
    --gpu-memory-utilization 0.9 \
    --max-model-len 4096 \
    --host 0.0.0.0 \
    --port 8000
```

### 3. Test the API

#### Using curl:

```bash
./test_api.sh
```

Or manually:

```bash
curl -X POST "http://localhost:8000/v1/chat/completions" \
    -H "Content-Type: application/json" \
    --data '{
        "model": "openai/gpt-oss-120b",
        "messages": [
            {
                "role": "user",
                "content": "What is the capital of France?"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 100
    }'
```

#### Using Python:

```bash
source vllm_env/bin/activate
python test_api.py
```

## 📋 Requirements

- Python 3.13
- Virtual environment with vLLM and dependencies
- Sufficient RAM (at least 16GB recommended for CPU inference)
- GPU with CUDA support (optional, for faster inference)

## 🔧 Installation Details

The setup includes:

- **vLLM 0.8.3**: High-performance LLM inference engine
- **PyTorch 2.6.0**: Deep learning framework
- **Transformers**: Hugging Face transformers library
- **FastAPI**: Web framework for the API
- **Other dependencies**: All required packages for vLLM operation

## 📊 Model Information

- **Model**: `openai/gpt-oss-120b`
- **Parameters**: 120 billion parameters
- **Context Length**: 4096 tokens (configurable)
- **API Endpoint**: `http://localhost:8000/v1/chat/completions`

## 🐳 Docker Alternative

If you prefer using Docker, you can run:

```bash
# Deploy with docker on Linux:
docker run --runtime nvidia --gpus all \
    --name my_vllm_container \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    --env "HUGGING_FACE_HUB_TOKEN=<secret>" \
    -p 8000:8000 \
    --ipc=host \
    vllm/vllm-openai:latest \
    --model openai/gpt-oss-120b

# Load and run the model:
docker exec -it my_vllm_container bash -c "vllm serve openai/gpt-oss-120b"

# Call the server using curl:
curl -X POST "http://localhost:8000/v1/chat/completions" \
    -H "Content-Type: application/json" \
    --data '{
        "model": "openai/gpt-oss-120b",
        "messages": [
            {
                "role": "user",
                "content": "What is the capital of France?"
            }
        ]
    }'
```

## 🔍 Troubleshooting

### Common Issues:

1. **CUDA not available**: The model will run on CPU, which is slower but functional
2. **Memory issues**: Reduce `--max-model-len` or `--gpu-memory-utilization`
3. **Model download issues**: Check internet connection and Hugging Face access
4. **Port conflicts**: Change the port in the server command

### Performance Tips:

- Use GPU acceleration when available
- Adjust `tensor_parallel_size` based on available GPUs
- Monitor memory usage during inference
- Consider using smaller models for faster inference

## 📝 API Usage Examples

### Basic Chat Completion:

```python
import requests

response = requests.post("http://localhost:8000/v1/chat/completions", 
    json={
        "model": "openai/gpt-oss-120b",
        "messages": [
            {"role": "user", "content": "Hello, how are you?"}
        ],
        "temperature": 0.7,
        "max_tokens": 100
    }
)

print(response.json()["choices"][0]["message"]["content"])
```

### Streaming Response:

```python
import requests

response = requests.post("http://localhost:8000/v1/chat/completions", 
    json={
        "model": "openai/gpt-oss-120b",
        "messages": [
            {"role": "user", "content": "Tell me a story"}
        ],
        "stream": True
    },
    stream=True
)

for line in response.iter_lines():
    if line:
        print(line.decode())
```

## 📚 Additional Resources

- [vLLM Documentation](https://docs.vllm.ai/)
- [GPT-OSS-120B Model Card](https://huggingface.co/openai/gpt-oss-120b)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

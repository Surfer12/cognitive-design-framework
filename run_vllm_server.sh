#!/bin/bash

# Activate the virtual environment
source vllm_env/bin/activate

echo "🚀 Starting vLLM server with GPT-OSS-120B model..."
echo "📝 This will start a server on http://localhost:8000"

# Run vLLM serve command
vllm serve "openai/gpt-oss-120b" \
    --trust-remote-code \
    --tensor-parallel-size 1 \
    --gpu-memory-utilization 0.9 \
    --max-model-len 4096 \
    --host 0.0.0.0 \
    --port 8000
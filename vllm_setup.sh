#!/bin/bash
# vLLM Setup Script - OpenAI GPT-OSS-120B

echo "🚀 vLLM Setup and Usage Commands"
echo "================================="

echo ""
echo "📦 PIP INSTALLATION:"
echo "pip install vllm"

echo ""
echo "🔧 LOAD AND RUN THE MODEL:"
echo 'vllm serve "openai/gpt-oss-120b"'

echo ""
echo "🧪 TEST WITH CURL:"
echo 'curl -X POST "http://localhost:8000/v1/chat/completions" \'
echo '    -H "Content-Type: application/json" \'
echo '    --data '"'"'{'
echo '        "model": "openai/gpt-oss-120b",'
echo '        "messages": ['
echo '            {'
echo '                "role": "user",'
echo '                "content": "What is the capital of France?"'
echo '            }'
echo '        ]'
echo '    }'"'"

echo ""
echo "🐳 DOCKER DEPLOYMENT:"
echo "docker run --runtime nvidia --gpus all \\"
echo "    --name my_vllm_container \\"
echo "    -v ~/.cache/huggingface:/root/.cache/huggingface \\"
echo '    --env "HUGGING_FACE_HUB_TOKEN=<secret>" \'
echo "    -p 8000:8000 \\"
echo "    --ipc=host \\"
echo "    vllm/vllm-openai:latest \\"
echo "    --model openai/gpt-oss-120b"

echo ""
echo "🔧 ALTERNATIVE DOCKER COMMAND:"
echo 'docker exec -it my_vllm_container bash -c "vllm serve openai/gpt-oss-120b"'

echo ""
echo "🧪 TEST DOCKER DEPLOYMENT:"
echo 'curl -X POST "http://localhost:8000/v1/chat/completions" \'
echo '    -H "Content-Type: application/json" \'
echo '    --data '"'"'{'
echo '        "model": "openai/gpt-oss-120b",'
echo '        "messages": ['
echo '            {'
echo '                "role": "user",'
echo '                "content": "What is the capital of France?"'
echo '            }'
echo '        ]'
echo '    }'"'"

echo ""
echo "⚠️  NOTE: This script displays the commands. Due to system dependencies"
echo "   (Rust compiler, CUDA, etc.), manual installation may be required."
echo ""
echo "✅ For a working environment, consider using Docker with NVIDIA runtime."
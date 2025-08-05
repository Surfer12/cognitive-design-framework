#!/bin/bash

echo "🧪 Testing vLLM API with GPT-OSS-120B model..."
echo "📝 Sending request to http://localhost:8000/v1/chat/completions"

# Test the API using curl
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
    }' | jq '.'

echo ""
echo "✅ API test completed!"
#!/usr/bin/env python3

import requests
import json

def test_vllm_api():
    """Test the vLLM API with GPT-OSS-120B model"""
    
    url = "http://localhost:8000/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "openai/gpt-oss-120b",
        "messages": [
            {
                "role": "user",
                "content": "What is the capital of France?"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 100
    }
    
    try:
        print("🧪 Testing vLLM API...")
        print(f"📝 Sending request to: {url}")
        print(f"📤 Request data: {json.dumps(data, indent=2)}")
        
        response = requests.post(url, headers=headers, json=data)
        
        print(f"📥 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API call successful!")
            print(f"🤖 Model response: {result['choices'][0]['message']['content']}")
        else:
            print(f"❌ API call failed with status {response.status_code}")
            print(f"📄 Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Make sure the vLLM server is running on localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_vllm_api()
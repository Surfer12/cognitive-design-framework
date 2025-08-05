# Quick Start Guide - Ollama Docker on macOS M4 Max

Get Ollama running in Docker on your Apple Silicon Mac in under 5 minutes.

## Prerequisites ✅

- macOS 12+ with Apple Silicon (M1/M2/M3/M4)
- Docker Desktop installed and running
- 16GB+ RAM (48GB recommended)
- External SSD for model storage (recommended)

## 1. Setup (2 minutes)

```bash
# Clone or download this configuration
git clone <your-repo> ollama-docker
cd ollama-docker

# Run automated setup
./scripts/setup.sh
```

**Custom setup options:**
```bash
# Custom external SSD path
./scripts/setup.sh --external-ssd /Volumes/MyFastSSD

# Custom resource limits
./scripts/setup.sh --memory-limit 24G --cpu-limit 6
```

## 2. Start Container (30 seconds)

```bash
# Start Ollama in background
docker compose up -d

# Check status
docker compose ps
```

## 3. Download a Model (2-5 minutes)

```bash
# Pull Llama 2 7B (recommended first model)
./scripts/manage-models.sh pull llama2:7b

# Or pull a smaller model for testing
./scripts/manage-models.sh pull llama2:3b

# Check what's installed
./scripts/manage-models.sh list
```

## 4. Test the API (10 seconds)

```bash
# Simple test
curl http://localhost:11434/api/tags

# Chat test
curl -X POST http://localhost:11434/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama2:7b",
    "messages": [{"role":"user","content":"Hello! How are you?"}],
    "stream": false
  }'
```

## 5. Python Example (Optional)

```python
import requests
import json

def chat_with_ollama(message):
    response = requests.post('http://localhost:11434/api/chat', 
        json={
            "model": "llama2:7b",
            "messages": [{"role": "user", "content": message}],
            "stream": False
        })
    return response.json()['message']['content']

# Test it
print(chat_with_ollama("Explain quantum computing in simple terms"))
```

## Common Commands

### Container Management
```bash
# View logs
docker compose logs -f ollama

# Restart container
docker compose restart

# Stop container
docker compose down

# Access container shell
docker compose exec ollama bash
```

### Model Management
```bash
# Pull models
./scripts/manage-models.sh pull codellama:13b
./scripts/manage-models.sh pull mistral:7b

# Remove models
./scripts/manage-models.sh remove llama2:7b

# Get model info
./scripts/manage-models.sh info llama2:7b
```

### Monitoring
```bash
# Check resource usage
docker stats ollama-m4max

# Run security check
./scripts/security-check.sh

# Monitor API health
curl http://localhost:11434/api/tags
```

## Recommended Models for M4 Max

| Model | Size | RAM Usage | Speed | Use Case |
|-------|------|-----------|-------|----------|
| `llama2:7b` | 3.8GB | 8GB | Fast | General chat |
| `codellama:13b` | 7.3GB | 16GB | Medium | Code generation |
| `mistral:7b` | 4.1GB | 9GB | Fast | Instruction following |
| `llama2:13b` | 7.3GB | 16GB | Medium | Better reasoning |

## Troubleshooting

### Container won't start
```bash
# Check Docker is running
docker info

# Check logs
docker compose logs ollama

# Rebuild container
docker compose build --no-cache
```

### Out of memory
```bash
# Check memory usage
docker stats ollama-m4max

# Use smaller model
./scripts/manage-models.sh pull llama2:3b

# Reduce memory limit in docker-compose.yml
```

### Model download fails
```bash
# Check disk space
df -h /Volumes/External/ollama_models

# Check permissions
ls -la /Volumes/External/ollama_models

# Try smaller model first
./scripts/manage-models.sh pull llama2:3b
```

### API not responding
```bash
# Check container status
docker compose ps

# Check port binding
docker port ollama-m4max

# Restart container
docker compose restart
```

## Performance Tips

### For Better Speed
- Use external SSD for model storage
- Allocate more CPU cores (8+ recommended)
- Use quantized models (Q4, Q8)
- Keep models in memory with longer `OLLAMA_KEEP_ALIVE`

### For Better Memory Usage
- Use smaller models (3B, 7B vs 13B+)
- Reduce `OLLAMA_MAX_LOADED_MODELS`
- Set shorter `OLLAMA_KEEP_ALIVE`
- Monitor with `docker stats`

## Security Notes

✅ **What's Secure:**
- Container runs as non-root user
- API bound to localhost only
- Read-only root filesystem
- Resource limits enforced
- No external network access

⚠️ **Important:**
- This runs CPU-only (no Metal GPU)
- For Metal GPU, install Ollama natively
- Models stored on external drive (encrypt recommended)

## Next Steps

1. **Explore models**: Try different models for various tasks
2. **Build applications**: Use the API in your projects  
3. **Monitor performance**: Check resource usage regularly
4. **Security review**: Run `./scripts/security-check.sh`
5. **Read full docs**: See [README.md](README.md) for details

## Need Help?

- **Logs**: `docker compose logs ollama`
- **Status**: `docker compose ps`
- **Security**: `./scripts/security-check.sh`
- **Full docs**: [README.md](README.md)
- **Security guide**: [SECURITY.md](SECURITY.md)

---

**🎯 Success!** You now have Ollama running securely in Docker on your M4 Max. The API is available at `http://localhost:11434` for your applications to use.
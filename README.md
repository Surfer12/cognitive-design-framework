# Ollama Docker Configuration for macOS M4 Max

Secure, reproducible deployment of Ollama (open-source GPT-style engine) using Docker on macOS M4 Max with 48GB unified memory.

## 🎯 Overview

This configuration provides:
- ✅ **Isolation**: Container runs as unprivileged user with read-only filesystem
- ✅ **Reproducibility**: Exact Ollama version baked into image
- ✅ **Security**: Checksum verification, capability dropping, resource limits
- ✅ **Portability**: Works on Linux or Apple Silicon hosts
- ✅ **Offline mode**: Optional network lockdown after model caching

## ⚠️ Important: GPU Limitations on macOS

**Docker Desktop on Apple Silicon runs Linux containers in a VM that cannot access the host's Metal GPU.** This means:

- 🚫 **Container inference is CPU-only** (slower than native Metal)
- ✅ **For Metal acceleration**: Run Ollama natively on macOS (see alternative below)
- ✅ **For security/isolation**: Use this Docker setup with CPU inference

## 🏗️ Quick Start

### 1. Prepare External Storage

```bash
# Create model storage directory on external SSD
mkdir -p /Volumes/SSD1/ollama_models
sudo chown -R 1000:1000 /Volumes/SSD1/ollama_models
```

### 2. Build and Run

```bash
# Build the image
docker build -t local/ollama:0.2.8 .

# Run with Docker Compose (recommended)
docker compose up -d

# Or run manually
docker run -d \
  --name ollama \
  --restart unless-stopped \
  --read-only \
  --tmpfs /tmp \
  -p 127.0.0.1:11434:11434 \
  --mount type=bind,src=/Volumes/SSD1/ollama_models,dst=/ollama \
  --cap-drop ALL \
  --security-opt no-new-privileges:true \
  --memory "32g" \
  --cpus "8" \
  local/ollama:0.2.8
```

### 3. Pull Models

```bash
# Pull a 7B model (fits in 48GB M4 Max)
docker exec -it ollama ollama pull llama2:7b-q8_0

# Verify the model
docker exec -it ollama ollama list
docker exec -it ollama ollama inspect llama2:7b-q8_0
```

### 4. Test the API

```bash
curl -X POST http://localhost:11434/api/chat -d '{
  "model": "llama2:7b-q8_0",
  "messages": [{"role":"user","content":"Explain why the M4 Max is great for LLM inference"}],
  "stream": false
}'
```

## 🔒 Security Features

| Feature | Implementation | Verification |
|---------|---------------|--------------|
| **Non-root user** | `USER ollama` in Dockerfile | `docker exec -it ollama whoami` |
| **Read-only root** | `--read-only` flag | `docker inspect ollama --format='{{.HostConfig.ReadonlyRootfs}}'` |
| **No capabilities** | `--cap-drop ALL` | `docker inspect ollama --format='{{json .HostConfig.CapAdd}}'` |
| **Checksum verification** | SHA256 in Dockerfile | Built-in during image build |
| **Resource limits** | 32GB RAM, 8 CPU cores | `docker stats ollama` |
| **Localhost only** | `127.0.0.1:11434` | `netstat -an \| grep 11434` |

## 🚀 Advanced Usage

### Offline Mode

After caching all needed models, enable offline mode:

```yaml
# In docker-compose.yml
environment:
  - OLLAMA_NO_NETWORK=1
```

### Custom Model Storage

```bash
# Use different external drive
docker run ... --mount type=bind,src=/Volumes/MyDrive/ollama,dst=/ollama ...

# Or use local directory (not recommended for large models)
docker run ... --mount type=bind,src=./models,dst=/ollama ...
```

### Python Client Example

```python
import requests
import json

url = "http://localhost:11434/api/chat"
payload = {
    "model": "llama2:7b-q8_0",
    "messages": [{"role": "user", "content": "What's the difference between CPU and GPU?"}],
    "stream": False
}

response = requests.post(url, json=payload)
print(json.dumps(response.json(), indent=2))
```

## 🔧 Alternative: Native Ollama with Metal GPU

For Metal acceleration, run Ollama natively on macOS:

```bash
# Install native Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Run with Metal GPU
ollama serve

# Your containers can still connect via host network
docker run ... -e OLLAMA_HOST=http://host.docker.internal:11434 ...
```

## 📊 Resource Management

### M4 Max Configuration
- **Total RAM**: 48GB unified memory
- **Container limit**: 32GB (leaves 16GB for system)
- **CPU cores**: 8 cores (adjust based on your workload)
- **Storage**: External SSD recommended for models

### Monitoring

```bash
# Check resource usage
docker stats ollama

# View logs
docker logs ollama

# Check health status
docker exec -it ollama curl -f http://localhost:11434/api/tags
```

## 🔄 Model Management

### Available Models

```bash
# List available models
docker exec -it ollama ollama list

# Pull different models
docker exec -it ollama ollama pull llama2:13b-q4_0  # Larger model
docker exec -it ollama ollama pull codellama:7b      # Code-focused
docker exec -it ollama ollama pull mistral:7b        # Fast inference
```

### Model Verification

```bash
# Verify model integrity
docker exec -it ollama ollama inspect llama2:7b-q8_0

# Compare with official digest from Ollama website
```

## 🛠️ Troubleshooting

### Common Issues

1. **Permission denied on volume mount**
   ```bash
   sudo chown -R 1000:1000 /Volumes/SSD1/ollama_models
   ```

2. **Container won't start**
   ```bash
   docker logs ollama
   docker inspect ollama
   ```

3. **Out of memory**
   ```bash
   # Reduce memory limit in docker-compose.yml
   memory: 24g
   ```

4. **Checksum verification fails**
   ```bash
   # Update OLLAMA_SHA256 in Dockerfile
   # Get from: https://github.com/ollama/ollama/releases
   ```

### Security Checklist

- [ ] Binary checksum verified during build
- [ ] Running as non-root user (`ollama`)
- [ ] Read-only root filesystem
- [ ] All capabilities dropped
- [ ] Resource limits set
- [ ] Only localhost exposed
- [ ] Models stored on encrypted volume

## 📝 Configuration Files

### Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `OLLAMA_HOME` | `/ollama` | Model storage directory |
| `OLLAMA_NO_NETWORK` | `0` | Disable network access |
| `OLLAMA_GPU` | `metal` | GPU backend (not used in Docker) |

### Docker Run Flags Explained

| Flag | Purpose |
|------|---------|
| `--read-only` | Prevents filesystem writes |
| `--tmpfs /tmp` | Provides writable temp directory |
| `--cap-drop ALL` | Removes Linux capabilities |
| `--security-opt no-new-privileges` | Prevents privilege escalation |
| `--memory "32g"` | Limits RAM usage |
| `--cpus "8"` | Limits CPU cores |

## 🎯 Performance Notes

- **CPU-only inference**: ~2-5 tokens/second for 7B models
- **Memory usage**: ~8-12GB for 7B models
- **Model loading**: 30-60 seconds first time
- **Response time**: 1-3 seconds for short prompts

For faster inference, consider:
1. Running natively with Metal GPU
2. Using smaller models (3B instead of 7B)
3. Using quantized models (q4_0, q8_0)

## 📚 References

- [Ollama Documentation](https://ollama.ai/docs)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [Apple Silicon Docker Guide](https://docs.docker.com/desktop/mac/apple-silicon/)

---

**Note**: This configuration prioritizes security and reproducibility over performance. For production workloads requiring Metal acceleration, run Ollama natively on macOS and connect your applications via the HTTP API.

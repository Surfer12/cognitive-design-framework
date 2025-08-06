# Secure Ollama Docker Setup

This repository provides a hardened, production-ready Docker setup for Ollama with comprehensive security features and easy deployment options.

## 🚀 Quick Start

### Option 1: Original One-liner (Recommended)
```bash
docker run -d \
  --name ollama \
  --restart unless-stopped \
  --read-only \
  --tmpfs /tmp \
  -p 127.0.0.1:11434:11434 \
  --mount type=bind,src=/Volumes/SSD1/ollama_models,dst=/ollama \
  -e OLLAMA_NO_NETWORK=0 \
  --cap-drop ALL \
  --security-opt no-new-privileges:true \
  --memory "32g" \
  --cpus "8" \
  local/ollama:0.2.8
```

### Option 2: Using the Setup Script
```bash
# Deploy with docker run
./scripts/setup-ollama.sh run

# Deploy with Docker Compose
./scripts/setup-ollama.sh compose

# Pull a model
./scripts/setup-ollama.sh pull llama2:7b-q8_0

# Check status
./scripts/setup-ollama.sh status
```

### Option 3: Docker Compose
```bash
docker-compose -f docker-compose.ollama.yml up -d
```

## 🔒 Security Features

### Container Hardening
- **Read-only filesystem**: Prevents file system modifications
- **Non-root user**: Runs as `ollama` user instead of root
- **Dropped capabilities**: Removes all Linux capabilities (`--cap-drop ALL`)
- **No new privileges**: Prevents privilege escalation (`--security-opt no-new-privileges:true`)
- **Temporary filesystem**: Uses tmpfs for `/tmp` to prevent persistence
- **Resource limits**: Memory and CPU constraints to prevent resource exhaustion

### Network Security
- **Local binding**: Only accessible from localhost (`127.0.0.1:11434`)
- **Optional offline mode**: Can run without network access (`OLLAMA_NO_NETWORK=1`)

### Data Security
- **Volume mounting**: Models stored outside container for persistence
- **Checksum verification**: Binary integrity verification in Dockerfile
- **Multi-stage build**: Minimal attack surface

## 📊 Resource Configuration

### M4 Max Mac (48GB RAM)
- **Memory**: 32GB limit (leaves 16GB for system)
- **CPU**: 8 cores (adjust based on your system)
- **Storage**: Models stored on external SSD for performance

### Customization
Edit the resource limits in `docker-compose.ollama.yml` or the docker run command:

```yaml
deploy:
  resources:
    limits:
      memory: 32G    # Adjust based on your RAM
      cpus: '8'      # Adjust based on your CPU cores
```

## 🎯 Usage Examples

### Pull and Run Models
```bash
# Pull a model
docker exec -it ollama ollama pull llama2:7b-q8_0

# List available models
docker exec -it ollama ollama list

# Run inference
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama2:7b-q8_0",
    "prompt": "Hello, how are you?",
    "stream": false
  }'
```

### Python Client Example
```python
import requests

response = requests.post('http://localhost:11434/api/generate', json={
    'model': 'llama2:7b-q8_0',
    'prompt': 'Explain quantum computing in simple terms',
    'stream': False
})

print(response.json()['response'])
```

### JavaScript Client Example
```javascript
const response = await fetch('http://localhost:11434/api/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        model: 'llama2:7b-q8_0',
        prompt: 'Write a haiku about AI',
        stream: false
    })
});

const data = await response.json();
console.log(data.response);
```

## 🔧 Troubleshooting

### Common Issues

**Container won't start:**
```bash
# Check logs
docker logs ollama

# Check if port is already in use
lsof -i :11434
```

**Model download fails:**
```bash
# Check network connectivity
docker exec ollama curl -I https://ollama.ai

# Pull with verbose output
docker exec -it ollama ollama pull llama2:7b-q8_0 --verbose
```

**Memory issues:**
```bash
# Check container resource usage
docker stats ollama

# Reduce memory limit if needed
docker update --memory 16g ollama
```

### Performance Optimization

**For M4 Max Mac:**
- Use native Ollama for Metal GPU acceleration
- Point containers to `http://host.docker.internal:11434`
- Store models on fast SSD storage

**For CPU-only workloads:**
- The containerized setup is perfect
- Adjust CPU cores based on your system
- Monitor temperature and throttling

## 📁 File Structure

```
.
├── Dockerfile.ollama          # Secure Ollama Dockerfile
├── docker-compose.ollama.yml  # Docker Compose configuration
├── scripts/
│   └── setup-ollama.sh       # Deployment script
└── README.ollama.md          # This documentation
```

## 🛡️ Security Best Practices

1. **Regular Updates**: Keep Ollama version updated
2. **Network Isolation**: Use `OLLAMA_NO_NETWORK=1` for offline mode
3. **Resource Monitoring**: Monitor container resource usage
4. **Log Analysis**: Review container logs regularly
5. **Model Verification**: Verify model checksums when possible

## 🚀 Production Deployment

For production use, consider:

- **Reverse Proxy**: Use nginx or traefik for SSL termination
- **Authentication**: Implement API key authentication
- **Monitoring**: Add Prometheus metrics and Grafana dashboards
- **Backup**: Regular model and configuration backups
- **Updates**: Automated security updates and model refreshes

## 📝 License

This setup follows Ollama's open-source license. The security hardening is based on Docker security best practices.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

**Happy prompting! 🎉**
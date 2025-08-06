# Secure Ollama Docker Setup

A hardened Docker deployment for Ollama with security best practices, perfect for running local LLMs safely on your system.

## 🔒 Security Features

This setup implements comprehensive security hardening:

- **Read-only root filesystem** - Prevents runtime modifications
- **Non-root user execution** - Runs as dedicated `ollama` user (UID 1000)
- **Capability dropping** - All Linux capabilities removed
- **No new privileges** - Prevents privilege escalation
- **Resource limits** - 32GB RAM and 8 CPU cores maximum
- **Network isolation** - Binds only to localhost (127.0.0.1)
- **Secure tmpfs** - Temporary filesystems with `noexec` and `nosuid`
- **Checksum verification** - Binary integrity validation during build

## 🚀 Quick Start

### Option 1: One-liner (Manual Docker)

```bash
# Build the image
docker build -f Dockerfile.ollama -t local/ollama:0.2.8 .

# Run the secure container
docker run -d \
  --name ollama \
  --restart unless-stopped \
  --read-only \
  --tmpfs /tmp:noexec,nosuid,size=1g \
  -p 127.0.0.1:11434:11434 \
  --mount type=bind,src=/Volumes/SSD1/ollama_models,dst=/ollama \
  -e OLLAMA_NO_NETWORK=0 \
  --cap-drop ALL \
  --security-opt no-new-privileges:true \
  --memory "32g" \
  --cpus "8" \
  local/ollama:0.2.8

# Pull a model
docker exec -it ollama ollama pull llama2:7b-q8_0
```

### Option 2: Automated Setup Script

```bash
# Make the setup script executable
chmod +x setup-ollama.sh

# Run the automated setup
./setup-ollama.sh
```

### Option 3: Docker Compose

```bash
# Start with Docker Compose
docker-compose up -d

# Pull a model
docker-compose exec ollama ollama pull llama2:7b-q8_0
```

## 📁 File Structure

```
.
├── Dockerfile.ollama      # Multi-stage secure Dockerfile
├── docker-compose.yml     # Docker Compose configuration
├── setup-ollama.sh       # Automated setup script
└── README-Ollama.md      # This documentation
```

## 🛠 Management Commands

The setup script provides convenient management commands:

```bash
# Check status
./setup-ollama.sh status

# Pull a specific model
./setup-ollama.sh pull llama2:13b-q4_0

# View logs
./setup-ollama.sh logs

# Stop container
./setup-ollama.sh stop

# Start container
./setup-ollama.sh start

# Access shell (for debugging)
./setup-ollama.sh shell
```

## 🔧 Configuration

### Environment Variables

- `OLLAMA_HOST=0.0.0.0` - Listen on all interfaces within container
- `OLLAMA_MODELS=/ollama` - Model storage path
- `OLLAMA_NO_NETWORK=0` - Allow network access for model downloads

### Resource Limits

- **Memory**: 32GB maximum (4GB reserved minimum)
- **CPU**: 8 cores maximum (2 cores reserved minimum)
- **Disk**: Unlimited (bound to host directory)

### Network Configuration

- **Port**: 11434 (bound to localhost only)
- **Access**: http://127.0.0.1:11434

## 📦 Supported Models

Popular models you can pull:

```bash
# Llama 2 variants
docker exec ollama ollama pull llama2:7b-q8_0    # High quality, ~7GB
docker exec ollama ollama pull llama2:13b-q4_0   # Balanced, ~7GB
docker exec ollama ollama pull llama2:70b-q2_0   # Large, ~38GB

# Code models
docker exec ollama ollama pull codellama:7b-code
docker exec ollama ollama pull codellama:13b-instruct

# Other popular models
docker exec ollama ollama pull mistral:7b-instruct
docker exec ollama ollama pull neural-chat:7b
docker exec ollama ollama pull orca-mini:3b
```

## 🖥 Usage Examples

### API Usage

```bash
# List available models
curl http://127.0.0.1:11434/api/tags

# Generate text
curl -X POST http://127.0.0.1:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama2:7b-q8_0",
    "prompt": "Why is the sky blue?",
    "stream": false
  }'

# Chat completion
curl -X POST http://127.0.0.1:11434/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama2:7b-q8_0",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ]
  }'
```

### Interactive Chat

```bash
# Start interactive chat session
docker exec -it ollama ollama run llama2:7b-q8_0

# With system prompt
docker exec -it ollama ollama run llama2:7b-q8_0 \
  "You are a helpful coding assistant. How do I optimize this Python function?"
```

## 🍎 macOS Metal GPU Acceleration

For GPU acceleration on macOS, run Ollama natively and point containers to it:

```bash
# Install Ollama natively for GPU acceleration
brew install ollama

# Start native Ollama server
ollama serve

# Configure containers to use native server
export OLLAMA_HOST=http://host.docker.internal:11434
```

## 🔍 Monitoring & Troubleshooting

### Health Checks

The container includes built-in health monitoring:

```bash
# Check container health
docker inspect ollama --format='{{.State.Health.Status}}'

# View health check logs
docker inspect ollama --format='{{range .State.Health.Log}}{{.Output}}{{end}}'
```

### Resource Monitoring

```bash
# Monitor resource usage
docker stats ollama

# Check memory usage
docker exec ollama cat /proc/meminfo

# Check disk usage
docker exec ollama df -h /ollama
```

### Common Issues

1. **Container won't start**: Check Docker daemon and available resources
2. **Model download fails**: Verify internet connectivity and disk space
3. **API not responding**: Check port binding and firewall settings
4. **Out of memory**: Reduce model size or increase memory limits

### Logs

```bash
# View real-time logs
docker logs -f ollama

# View last 100 lines
docker logs --tail 100 ollama

# Search for errors
docker logs ollama 2>&1 | grep -i error
```

## 🔐 Security Considerations

### Container Security

- Runs as non-root user (UID 1000)
- Read-only root filesystem prevents tampering
- No privileged access or capabilities
- Isolated network namespace
- Resource limits prevent DoS attacks

### Host Security

- Models stored in dedicated directory
- Port bound to localhost only
- No host filesystem access beyond models directory
- Automatic container restart on failure

### Network Security

- No external network access from container
- API accessible only from localhost
- No SSH or shell access by default
- Health checks use internal endpoints only

## 📊 Performance Tuning

### CPU Optimization

```bash
# Adjust CPU limits
docker update --cpus="16" ollama

# Check CPU usage
docker exec ollama cat /proc/cpuinfo
```

### Memory Optimization

```bash
# Adjust memory limits
docker update --memory="64g" ollama

# Monitor memory usage
docker exec ollama cat /proc/meminfo | grep MemAvailable
```

### Model Selection

Choose models based on your hardware:

- **8GB RAM**: `orca-mini:3b`, `llama2:7b-q2_0`
- **16GB RAM**: `llama2:7b-q4_0`, `mistral:7b-instruct`
- **32GB RAM**: `llama2:13b-q4_0`, `codellama:13b-instruct`
- **64GB+ RAM**: `llama2:70b-q2_0`, `llama2:70b-q4_0`

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Happy prompting!** 🚀 Your secure, local LLM service is ready to use.
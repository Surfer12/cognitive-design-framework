# Ollama Docker Configuration for macOS M4 Max - Complete Deployment Guide

This repository provides a secure, reproducible Docker-based deployment of Ollama for your 48GB M4 Max macOS system.

## 📁 Repository Structure

```
ollama-docker-m4max/
├── Dockerfile                 # Secure container configuration
├── docker-compose.yml         # Orchestration and security settings
├── build-and-run.sh          # Automated build and deployment script
├── README.md                 # Comprehensive usage guide
├── security-checklist.md      # Security verification checklist
├── native-metal-setup.md     # Alternative native Metal GPU setup
└── DEPLOYMENT_SUMMARY.md     # This file - complete overview
```

## 🎯 Quick Start (3 Steps)

### 1. Prepare Storage
```bash
mkdir -p /Volumes/SSD1/ollama_models
sudo chown -R 1000:1000 /Volumes/SSD1/ollama_models
```

### 2. Build and Run
```bash
./build-and-run.sh
```

### 3. Pull a Model
```bash
docker exec -it ollama ollama pull llama2:7b-q8_0
```

## 🔧 What Each File Does

### `Dockerfile`
- **Purpose**: Defines the secure container image
- **Key Features**:
  - Uses Debian Bullseye slim (arm64) for Apple Silicon
  - Downloads and verifies Ollama binary with SHA256 checksum
  - Creates non-root user (`ollama`)
  - Sets up model storage directory
  - Runs as unprivileged user

### `docker-compose.yml`
- **Purpose**: Orchestrates the container with security settings
- **Key Features**:
  - Read-only root filesystem
  - All capabilities dropped
  - Resource limits (32GB RAM, 8 CPU cores)
  - Localhost-only port binding
  - Health checks
  - Volume mounting for external SSD

### `build-and-run.sh`
- **Purpose**: Automated deployment script
- **Key Features**:
  - Checks Docker environment
  - Verifies storage setup
  - Builds image with proper arguments
  - Runs container with security flags
  - Waits for service readiness
  - Provides usage instructions
  - Security verification

### `README.md`
- **Purpose**: Comprehensive user guide
- **Key Features**:
  - Step-by-step instructions
  - Security feature explanations
  - Performance notes
  - Troubleshooting guide
  - API usage examples

### `security-checklist.md`
- **Purpose**: Security verification guide
- **Key Features**:
  - Pre-deployment security checks
  - Runtime verification commands
  - Security monitoring guidelines
  - Incident response procedures

### `native-metal-setup.md`
- **Purpose**: Alternative native setup guide
- **Key Features**:
  - Full Metal GPU acceleration
  - Native macOS integration
  - Performance optimization
  - Docker integration options

## 🛡️ Security Features

| Feature | Implementation | Verification |
|---------|---------------|--------------|
| **Non-root user** | `USER ollama` in Dockerfile | `docker exec -it ollama whoami` |
| **Read-only root** | `--read-only` flag | `docker inspect ollama --format='{{.HostConfig.ReadonlyRootfs}}'` |
| **No capabilities** | `--cap-drop ALL` | `docker inspect ollama --format='{{json .HostConfig.CapAdd}}'` |
| **Checksum verification** | SHA256 in Dockerfile | Built-in during build |
| **Resource limits** | 32GB RAM, 8 CPU cores | `docker stats ollama` |
| **Localhost only** | `127.0.0.1:11434` | `netstat -an \| grep 11434` |

## 🚀 Usage Commands

### Basic Operations
```bash
# Start the service
./build-and-run.sh

# Check status
./build-and-run.sh status

# View logs
./build-and-run.sh logs

# Stop service
./build-and-run.sh stop

# Verify security
./build-and-run.sh verify
```

### Model Management
```bash
# Pull models
docker exec -it ollama ollama pull llama2:7b-q8_0
docker exec -it ollama ollama pull codellama:7b

# List models
docker exec -it ollama ollama list

# Inspect model
docker exec -it ollama ollama inspect llama2:7b-q8_0
```

### API Usage
```bash
# Test API
curl -X POST http://localhost:11434/api/chat -d '{
  "model": "llama2:7b-q8_0",
  "messages": [{"role":"user","content":"Hello!"}],
  "stream": false
}'

# Python client
python3 -c "
import requests
response = requests.post('http://localhost:11434/api/chat', json={
    'model': 'llama2:7b-q8_0',
    'messages': [{'role': 'user', 'content': 'Hello!'}],
    'stream': False
})
print(response.json())
"
```

## 📊 Performance Characteristics

### M4 Max Configuration
- **Total RAM**: 48GB unified memory
- **Container limit**: 32GB (leaves 16GB for system)
- **CPU cores**: 8 cores allocated
- **Storage**: External SSD for models

### Performance Notes
- **CPU-only inference**: ~2-5 tokens/second for 7B models
- **Memory usage**: ~8-12GB for 7B models
- **Model loading**: 30-60 seconds first time
- **Response time**: 1-3 seconds for short prompts

## ⚠️ Important Limitations

### GPU Support
**Docker Desktop on Apple Silicon cannot access Metal GPU.** This means:
- 🚫 **Container inference is CPU-only** (slower than native Metal)
- ✅ **For Metal acceleration**: Use `native-metal-setup.md`
- ✅ **For security/isolation**: Use this Docker setup

### Alternative: Native + Docker
You can run Ollama natively with Metal GPU and connect Docker containers:

```bash
# Run native Ollama with Metal
ollama serve &

# Connect Docker containers via host network
docker run -e OLLAMA_HOST=http://host.docker.internal:11434 your-app
```

## 🔄 Maintenance

### Regular Tasks
```bash
# Update Ollama version
# Edit OLLAMA_VER in Dockerfile and docker-compose.yml
# Update OLLAMA_SHA256 with new checksum

# Rebuild image
docker build -t local/ollama:new-version .

# Update container
docker-compose down
docker-compose up -d

# Clean up old images
docker image prune -f
```

### Monitoring
```bash
# Check resource usage
docker stats ollama

# Monitor logs
docker logs -f ollama

# Verify security
./build-and-run.sh verify
```

## 🛠️ Troubleshooting

### Common Issues

1. **Permission denied on volume**
   ```bash
   sudo chown -R 1000:1000 /Volumes/SSD1/ollama_models
   ```

2. **Container won't start**
   ```bash
   docker logs ollama
   ./build-and-run.sh stop
   ./build-and-run.sh
   ```

3. **Out of memory**
   ```bash
   # Reduce limits in docker-compose.yml
   memory: 24g
   ```

4. **Checksum verification fails**
   ```bash
   # Update OLLAMA_SHA256 in Dockerfile
   # Get from: https://github.com/ollama/ollama/releases
   ```

## 📚 Additional Resources

- [Ollama Documentation](https://ollama.ai/docs)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [Apple Silicon Docker Guide](https://docs.docker.com/desktop/mac/apple-silicon/)
- [Metal Performance Shaders](https://developer.apple.com/metal/performance-shaders/)

## 🎯 Deployment Options

### Option 1: Docker (This Setup)
- ✅ **Maximum security and isolation**
- ✅ **Reproducible deployment**
- ✅ **Resource limits and monitoring**
- ❌ **CPU-only inference (slower)**

### Option 2: Native Metal GPU
- ✅ **Full Metal GPU acceleration**
- ✅ **Best performance**
- ❌ **Less isolation**
- ❌ **Manual security configuration**

### Option 3: Hybrid Approach
- ✅ **Native Ollama with Metal GPU**
- ✅ **Docker containers for applications**
- ✅ **Best of both worlds**
- ⚠️ **More complex setup**

## 📋 Quick Reference

### Essential Commands
```bash
# Start everything
./build-and-run.sh

# Pull a model
docker exec -it ollama ollama pull llama2:7b-q8_0

# Test API
curl -X POST http://localhost:11434/api/chat -d '{"model":"llama2:7b-q8_0","messages":[{"role":"user","content":"Hello!"}],"stream":false}'

# Check status
./build-and-run.sh status

# Stop everything
./build-and-run.sh stop
```

### Configuration Files
- **Dockerfile**: Container definition
- **docker-compose.yml**: Orchestration and security
- **build-and-run.sh**: Automated deployment
- **security-checklist.md**: Security verification

### Key Directories
- **Model storage**: `/Volumes/SSD1/ollama_models`
- **Container logs**: `docker logs ollama`
- **API endpoint**: `http://localhost:11434`

---

**Ready to deploy?** Run `./build-and-run.sh` to get started with a secure, reproducible Ollama setup optimized for your M4 Max!
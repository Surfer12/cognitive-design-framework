# Native Ollama Setup with Metal GPU on macOS M4 Max

This guide provides an alternative to the Docker setup for running Ollama natively on macOS with full Metal GPU acceleration.

## 🎯 Why Native Setup?

**Advantages:**
- ✅ **Full Metal GPU acceleration** (10-50x faster than CPU)
- ✅ **Direct access to 48GB unified memory**
- ✅ **Native macOS integration**
- ✅ **Better performance for large models**

**Trade-offs:**
- ⚠️ **Less isolation** than Docker
- ⚠️ **Manual security configuration**
- ⚠️ **System-level installation**

## 🚀 Quick Installation

### 1. Install Ollama

```bash
# Download and install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Verify installation
ollama --version
```

### 2. Start Ollama Server

```bash
# Start the server with Metal GPU support
ollama serve

# Or run in background
ollama serve &
```

### 3. Pull Your First Model

```bash
# Pull a 7B model optimized for M4 Max
ollama pull llama2:7b-q8_0

# Verify the model
ollama list
ollama inspect llama2:7b-q8_0
```

### 4. Test the API

```bash
# Test with curl
curl -X POST http://localhost:11434/api/chat -d '{
  "model": "llama2:7b-q8_0",
  "messages": [{"role":"user","content":"Explain why the M4 Max is great for LLM inference"}],
  "stream": false
}'
```

## 🔧 Advanced Configuration

### Environment Variables

Create `~/.ollama/config.yaml`:

```yaml
# Ollama configuration for M4 Max
gpu: metal
host: 127.0.0.1:11434
models: /Volumes/SSD1/ollama_models

# Performance tuning
numa: false
num_threads: 8
```

### Model Storage on External SSD

```bash
# Create model directory on external SSD
mkdir -p /Volumes/SSD1/ollama_models

# Set environment variable
export OLLAMA_HOME=/Volumes/SSD1/ollama_models

# Or add to your shell profile
echo 'export OLLAMA_HOME=/Volumes/SSD1/ollama_models' >> ~/.zshrc
```

### System Service Setup

Create `/Library/LaunchDaemons/com.ollama.serve.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ollama.serve</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/ollama</string>
        <string>serve</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardErrorPath</key>
    <string>/var/log/ollama.log</string>
    <key>StandardOutPath</key>
    <string>/var/log/ollama.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>OLLAMA_HOME</key>
        <string>/Volumes/SSD1/ollama_models</string>
    </dict>
</dict>
</plist>
```

Load the service:

```bash
sudo launchctl load /Library/LaunchDaemons/com.ollama.serve.plist
```

## 📊 Performance Optimization

### M4 Max Specific Tuning

```bash
# Check Metal GPU availability
system_profiler SPDisplaysDataType | grep "Metal"

# Monitor GPU usage
sudo powermetrics --samplers gpu_power -n 1

# Check memory usage
vm_stat
```

### Model Recommendations for M4 Max

| Model | Size | Memory Usage | Speed | Use Case |
|-------|------|--------------|-------|----------|
| `llama2:7b-q8_0` | ~4GB | ~8GB | Fast | General purpose |
| `llama2:13b-q4_0` | ~7GB | ~12GB | Medium | Better reasoning |
| `codellama:7b` | ~4GB | ~8GB | Fast | Code generation |
| `mistral:7b` | ~4GB | ~8GB | Very Fast | Fast responses |
| `llama2:70b-q4_0` | ~35GB | ~40GB | Slow | Best quality |

### Memory Management

```bash
# Monitor memory usage
top -l 1 | grep ollama

# Check unified memory
system_profiler SPHardwareDataType | grep "Memory"

# Optimize for large models
sudo sysctl -w vm.swapusage=0
```

## 🔒 Security Configuration

### Firewall Rules

```bash
# Allow only localhost connections
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/local/bin/ollama
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --unblock /usr/local/bin/ollama
```

### File Permissions

```bash
# Secure model directory
chmod 700 /Volumes/SSD1/ollama_models
chown $(whoami):staff /Volumes/SSD1/ollama_models
```

### Network Security

```bash
# Test localhost-only binding
netstat -an | grep 11434
# Should show: tcp4 127.0.0.1.11434

# Block external access (if needed)
sudo pfctl -e
echo "block drop in proto tcp from any to any port 11434" | sudo pfctl -f -
```

## 🐳 Docker Integration

You can still use Docker containers that connect to the native Ollama server:

### Docker Compose for Client Apps

```yaml
version: "3.9"
services:
  myapp:
    image: python:3.11-slim
    environment:
      - OLLAMA_HOST=http://host.docker.internal:11434
    volumes:
      - ./app:/app
    working_dir: /app
    command: python main.py
```

### Python Client Example

```python
import requests
import json

# Connect to native Ollama server
url = "http://host.docker.internal:11434/api/chat"
payload = {
    "model": "llama2:7b-q8_0",
    "messages": [{"role": "user", "content": "Hello!"}],
    "stream": False
}

response = requests.post(url, json=payload)
print(json.dumps(response.json(), indent=2))
```

## 📈 Performance Monitoring

### GPU Usage

```bash
# Monitor Metal GPU usage
sudo powermetrics --samplers gpu_power -n 10 -i 1000

# Check GPU memory
system_profiler SPDisplaysDataType | grep "VRAM"
```

### Memory Usage

```bash
# Monitor unified memory
vm_stat | grep "Pages"

# Check Ollama memory usage
ps aux | grep ollama
```

### Performance Benchmarks

```bash
# Test inference speed
time curl -X POST http://localhost:11434/api/chat -d '{
  "model": "llama2:7b-q8_0",
  "messages": [{"role":"user","content":"Write a short poem about AI"}],
  "stream": false
}'
```

## 🔧 Troubleshooting

### Common Issues

1. **GPU not detected**
   ```bash
   # Check Metal support
   system_profiler SPDisplaysDataType
   
   # Restart Ollama
   pkill ollama
   ollama serve
   ```

2. **Out of memory**
   ```bash
   # Check available memory
   vm_stat
   
   # Use smaller model or reduce batch size
   ollama pull llama2:7b-q4_0
   ```

3. **Slow performance**
   ```bash
   # Check CPU usage
   top -l 1 | grep ollama
   
   # Verify Metal GPU usage
   sudo powermetrics --samplers gpu_power -n 1
   ```

### Logs and Debugging

```bash
# View Ollama logs
tail -f /var/log/ollama.log

# Check system logs
log show --predicate 'process == "ollama"' --last 1h

# Debug GPU issues
system_profiler SPDisplaysDataType
```

## 🎯 Best Practices

### Model Management

```bash
# List all models
ollama list

# Remove unused models
ollama rm llama2:7b

# Export/import models
ollama cp llama2:7b-q8_0 llama2:7b-q8_0-backup
```

### Backup Strategy

```bash
# Backup models to external drive
rsync -av /Volumes/SSD1/ollama_models/ /Volumes/Backup/ollama_models/

# Create compressed backup
tar -czf ollama-models-$(date +%Y%m%d).tar.gz /Volumes/SSD1/ollama_models/
```

### Performance Tuning

```bash
# Optimize for your workload
export OLLAMA_NUM_THREADS=8
export OLLAMA_GPU_LAYERS=35

# Start with optimized settings
ollama serve --numa --num-threads 8
```

## 📚 Additional Resources

- [Ollama Documentation](https://ollama.ai/docs)
- [Metal Performance Shaders](https://developer.apple.com/metal/performance-shaders/)
- [macOS Security Guide](https://support.apple.com/guide/mac-help/security-privacy-overview-mh40589/mac)
- [Apple Silicon Optimization](https://developer.apple.com/documentation/metal/optimizing_metal_apps_for_apple_silicon)

---

**Note**: This native setup provides the best performance for your M4 Max but requires more careful security management than the Docker approach. Consider your specific needs when choosing between Docker isolation and native Metal performance.
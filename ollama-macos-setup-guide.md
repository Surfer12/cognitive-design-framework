# Ollama macOS Setup Guide (M4 Max / macOS 13+)

## Quick-Start Security Checklist

| Step | Action | Security Benefit |
|------|--------|-----------------|
| 1 | Keep macOS updated + Enable FileVault & Gatekeeper + Enable firewall | Latest security patches & encryption for model files |
| 2 | Verify Ollama download with checksum | Guarantees binary integrity |
| 3 | Install via Homebrew or official DMG | Officially-signed, auto-updates |
| 4 | Run as non-admin user | Reduces compromise impact (least-privilege) |
| 5 | Isolate data directory | Keeps heavy model files separate |
| 6 | Configure Metal GPU + Memory limits | Optimizes performance, prevents memory oversubscription |
| 7 | Pull vetted open-source models | Signed & checksummed by Ollama registry |
| 8 | Verify model integrity | Ensures no corruption in transit |
| 9 | Run offline (optional hardening) | Prevents accidental outbound connections |
| 10 | Test the setup | Confirm safe, local LLM operation |

## 1. System Preparation & Hardening

### A. System Security Baseline

```bash
# Update macOS to latest version
softwareupdate --install --all

# Verify Gatekeeper settings
# System Settings > Privacy & Security > "App Store and identified developers"

# Enable FileVault
# System Settings > Security & Privacy > FileVault

# Enable firewall
# System Settings > Network > Firewall > Turn On

# Disable SSH unless needed
# System Settings > Sharing > Remote Login (disable)
```

### B. Create Limited User Account (Optional)

```bash
# Create non-admin user for Ollama
sudo dscl . -create /Users/llm_user
sudo dscl . -create /Users/llm_user UserShell /bin/bash
sudo dscl . -create /Users/llm_user RealName "LLM Service"
sudo dscl . -create /Users/llm_user UniqueID "506"
sudo dscl . -create /Users/llm_user PrimaryGroupID 20

# Make ollama executable for the user
sudo chmod 755 $(which ollama)
```

## 2. Download & Verify Ollama

### A. Download with Verification

```bash
# Download from official source
curl -O https://ollama.com/download/Ollama.dmg

# Verify checksum (compare with website)
shasum -a 256 Ollama.dmg

# Verify Apple notarization
spctl -a -t exec -vv Ollama.dmg
# Should show "accepted"
```

### B. Installation Options

**Homebrew (Recommended)**
```bash
# Install Homebrew if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Add to path
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
source ~/.zshrc

# Install Ollama
brew install --cask ollama
```

**Direct Installation**
```bash
# Open DMG and drag to Applications
open Ollama.dmg
```

### C. Verify Installation

```bash
# Check binary signature
/usr/bin/spctl -a -v /Applications/Ollama.app

# Check version
ollama version
```

## 3. Configuration & Setup

### A. Data Directory Isolation

```bash
# For external SSD (recommended for large models)
export OLLAMA_HOME=/Volumes/SSD1/ollama
mkdir -p $OLLAMA_HOME/models
ln -s $OLLAMA_HOME $HOME/.ollama

# Add to shell profile
echo 'export OLLAMA_HOME="/Volumes/SSD1/ollama"' >> ~/.zshrc
```

### B. GPU Configuration

Create `~/.ollama/config.yaml`:

```yaml
runtime:
  # Force Metal backend (default on Apple silicon)
  gpu: metal
  
  # Cap GPU memory usage (32GB for models, rest for OS)
  gpu_memory: "32GiB"
  
  # Context length
  max_context: 4096
```

### C. Start Service

```bash
# Start automatically at login
launchctl load -w ~/Library/LaunchAgents/ai.ollama.ollama.plist

# Or with Homebrew
brew services start ollama

# Verify it's listening only on localhost
lsof -iTCP:11434 -sTCP:LISTEN
# Should show: 127.0.0.1:11434
```

## 4. Model Management

### A. Pull Verified Models

```bash
# 7B models (comfortable on 48GB memory)
ollama pull llama2:7b
ollama pull mistral:7b

# Quantized versions (less memory usage)
ollama pull llama2:7b-q8_0

# Smaller models for faster startup
ollama pull gemma:2b
```

### B. Verify Model Integrity

```bash
# List all models with sizes and digests
ollama list

# Detailed inspection with checksum
ollama inspect llama2:7b
# Compare checksum with https://ollama.com/library/llama2-7b
```

## 5. Security Hardening (Optional)

### A. Offline Mode

```bash
# Prevent outbound connections
export OLLAMA_NO_NETWORK=1

# Unload network services
launchctl unload -w /Library/LaunchDaemons/ai.ollama.ollama.plist

# Re-enable only when pulling new models
```

### B. Network Monitoring

```bash
# Monitor for hidden outbound traffic
sudo tcpdump -i lo0 -n -c 10
```

## 6. Testing

```bash
# Test your setup
ollama run llama2:7b "Explain the advantage of Apple's M4-Max architecture for LLM inference."
```

## Model Recommendations

| Model | Size | Memory Usage | Use Case |
|-------|------|--------------|----------|
| `llama2:7b` | ~13GB | ~32GB | General purpose |
| `llama2:7b-q8_0` | ~7GB | ~16GB | Memory-constrained |
| `mistral:7b` | ~13GB | ~32GB | High performance |
| `gemma:2b` | ~4GB | ~8GB | Fast startup |

## Troubleshooting

### GPU Detection
```bash
# Check GPU backend usage
tail -f ~/Library/Logs/Ollama.log | grep "gpu"
# Expected: "using Metal via Apple GPU (M4-Max)"
```

### Memory Issues
- Use quantized models (`-q8_0` suffix)
- Reduce `gpu_memory` in config
- Ensure adequate free space on storage

### Service Issues
```bash
# Restart service after config changes
launchctl unload -w ~/Library/LaunchAgents/ai.ollama.ollama.plist
launchctl load -w ~/Library/LaunchAgents/ai.ollama.ollama.plist
```

---

**Note**: This guide prioritizes security and stability. All models are pulled from the official Ollama registry with cryptographic verification, and the setup isolates the LLM environment from the rest of your system.
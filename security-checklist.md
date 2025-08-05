# Security Checklist for Ollama Docker Deployment

This checklist ensures your Ollama Docker deployment follows security best practices for your macOS M4 Max system.

## 🔍 Pre-Deployment Checks

### ✅ Docker Environment
- [ ] Docker Desktop is up to date
- [ ] Docker daemon is running
- [ ] User has appropriate Docker permissions
- [ ] No unnecessary Docker images or containers running

### ✅ Storage Security
- [ ] External SSD is encrypted (FileVault or third-party)
- [ ] Model storage directory has correct permissions (1000:1000)
- [ ] Storage path is on external drive, not system drive
- [ ] Backup strategy for models (if needed)

### ✅ Network Security
- [ ] Firewall is enabled on macOS
- [ ] No unnecessary ports exposed
- [ ] Container only binds to localhost (127.0.0.1)

## 🏗️ Build-Time Security

### ✅ Image Security
- [ ] Base image is from official source (debian:bullseye-slim)
- [ ] Ollama binary checksum is verified during build
- [ ] No unnecessary packages installed
- [ ] Image is built with specific version tags

### ✅ Binary Verification
- [ ] SHA256 checksum matches official Ollama release
- [ ] Binary is downloaded over HTTPS
- [ ] Checksum verification step is in Dockerfile
- [ ] Build fails if checksum doesn't match

## 🚀 Runtime Security

### ✅ Container Configuration
- [ ] Container runs as non-root user (`ollama`)
- [ ] Read-only root filesystem enabled
- [ ] All Linux capabilities dropped (`--cap-drop ALL`)
- [ ] No new privileges allowed (`--security-opt no-new-privileges`)
- [ ] Resource limits set (memory: 32g, cpus: 8)

### ✅ Network Configuration
- [ ] Only port 11434 exposed
- [ ] Port bound to localhost only (127.0.0.1)
- [ ] No external network access unless needed
- [ ] Offline mode enabled after model caching (optional)

### ✅ Volume Security
- [ ] Model storage mounted as read-write bind mount
- [ ] No other volumes mounted unnecessarily
- [ ] Volume permissions match container user (1000:1000)
- [ ] Volume is on encrypted storage

## 🔒 Verification Commands

Run these commands to verify your security configuration:

### User and Privileges
```bash
# Check if running as non-root
docker exec -it ollama whoami
# Expected: ollama

# Check if read-only filesystem
docker inspect ollama --format='{{.HostConfig.ReadonlyRootfs}}'
# Expected: true

# Check capabilities
docker inspect ollama --format='{{json .HostConfig.CapAdd}}'
# Expected: null

# Check security options
docker inspect ollama --format='{{json .HostConfig.SecurityOpt}}'
# Expected: ["no-new-privileges"]
```

### Network Security
```bash
# Check port binding
docker port ollama
# Expected: 127.0.0.1:11434->11434/tcp

# Check network connectivity
netstat -an | grep 11434
# Expected: Only localhost binding

# Test API access from host
curl -f http://localhost:11434/api/tags
# Expected: JSON response or 404 (if no models)
```

### Resource Limits
```bash
# Check resource limits
docker stats ollama --no-stream
# Verify memory and CPU usage are within limits

# Check container configuration
docker inspect ollama --format='{{json .HostConfig.Memory}}'
docker inspect ollama --format='{{json .HostConfig.CpuCount}}'
```

## 🛡️ Ongoing Security

### ✅ Regular Checks
- [ ] Monitor container logs for unusual activity
- [ ] Check resource usage regularly
- [ ] Verify no unauthorized network connections
- [ ] Update base image periodically
- [ ] Review security advisories for Ollama

### ✅ Model Security
- [ ] Verify model checksums after download
- [ ] Use only official Ollama models
- [ ] Monitor model storage for unauthorized changes
- [ ] Backup models securely if needed

### ✅ Access Control
- [ ] Limit who can access the API
- [ ] Use authentication if exposing to network
- [ ] Monitor API usage patterns
- [ ] Log access attempts

## 🚨 Security Alerts

### ⚠️ Warning Signs
- Container running as root
- Unnecessary ports exposed
- High resource usage without explanation
- Unusual network connections
- Model files modified unexpectedly
- API responding to external requests

### 🚨 Immediate Actions
If you detect any security issues:

1. **Stop the container immediately:**
   ```bash
   docker stop ollama
   ```

2. **Investigate the issue:**
   ```bash
   docker logs ollama
   docker inspect ollama
   ```

3. **Rebuild with fresh image:**
   ```bash
   docker rmi local/ollama:0.2.8
   ./build-and-run.sh
   ```

4. **Verify security configuration:**
   ```bash
   ./build-and-run.sh verify
   ```

## 📋 Quick Verification Script

Create a verification script (`verify-security.sh`):

```bash
#!/bin/bash
echo "=== Ollama Docker Security Verification ==="

# Check user
USER=$(docker exec -it ollama whoami 2>/dev/null)
echo "User: $USER (expected: ollama)"

# Check read-only filesystem
READONLY=$(docker inspect ollama --format='{{.HostConfig.ReadonlyRootfs}}' 2>/dev/null)
echo "Read-only: $READONLY (expected: true)"

# Check capabilities
CAPS=$(docker inspect ollama --format='{{json .HostConfig.CapAdd}}' 2>/dev/null)
echo "Capabilities: $CAPS (expected: null)"

# Check port binding
PORTS=$(docker port ollama 2>/dev/null)
echo "Ports: $PORTS (expected: 127.0.0.1:11434->11434/tcp)"

# Check API access
API_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:11434/api/tags 2>/dev/null)
echo "API accessible: $API_RESPONSE (expected: 200 or 404)"

echo "=== Verification Complete ==="
```

## 🔐 Advanced Security (Optional)

### Seccomp Profile
Create a custom seccomp profile to further restrict system calls:

```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "syscalls": [
    {
      "names": ["read", "write", "open", "close", "stat", "fstat"],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

### AppArmor Profile
If available, use AppArmor to restrict file and network access.

### Network Namespace
Run container in its own network namespace for additional isolation.

## 📞 Security Contacts

- **Docker Security**: https://docs.docker.com/engine/security/
- **Ollama Security**: https://github.com/ollama/ollama/security
- **macOS Security**: https://support.apple.com/guide/mac-help/security-privacy-overview-mh40589/mac

---

**Remember**: Security is an ongoing process. Regularly review and update your security configuration as new threats emerge and best practices evolve.
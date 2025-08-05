# Security Guidelines for Ollama Docker Configuration

This document outlines the security measures, best practices, and verification procedures for the Ollama Docker deployment on macOS M4 Max.

## 🔒 Security Architecture

### Defense in Depth

This configuration implements multiple security layers:

```
┌─────────────────────────────────────────────────────────────┐
│                        Host Security                        │
├─────────────────────────────────────────────────────────────┤
│                     Network Security                       │
├─────────────────────────────────────────────────────────────┤
│                    Container Security                      │
├─────────────────────────────────────────────────────────────┤
│                   Application Security                     │
└─────────────────────────────────────────────────────────────┘
```

## ✅ Security Checklist

### Pre-Deployment Security

- [ ] **System Requirements**
  - [ ] macOS 12.0+ with latest security updates
  - [ ] Docker Desktop latest version installed
  - [ ] FileVault disk encryption enabled
  - [ ] Firewall enabled and configured

- [ ] **Binary Verification**
  - [ ] Ollama binary checksum verified
  - [ ] Docker images scanned for vulnerabilities
  - [ ] Base images from official sources only

- [ ] **Configuration Security**
  - [ ] Non-root user configured (UID 1000)
  - [ ] Read-only root filesystem enabled
  - [ ] All capabilities dropped except necessary ones
  - [ ] Network bound to localhost only

### Runtime Security

- [ ] **Container Isolation**
  - [ ] Container running as non-root user
  - [ ] No privileged mode
  - [ ] Resource limits enforced
  - [ ] Security profiles active

- [ ] **Network Security**
  - [ ] API accessible only via localhost
  - [ ] No external network exposure
  - [ ] Custom bridge network configured
  - [ ] Origin restrictions in place

- [ ] **Data Security**
  - [ ] Models stored on encrypted external SSD
  - [ ] Proper file permissions set
  - [ ] Sensitive data not in logs
  - [ ] Temporary files cleaned up

### Ongoing Security

- [ ] **Monitoring**
  - [ ] Container logs monitored
  - [ ] Resource usage tracked
  - [ ] Security events logged
  - [ ] Regular security audits performed

- [ ] **Updates**
  - [ ] Ollama version kept current
  - [ ] Docker images regularly updated
  - [ ] macOS security updates applied
  - [ ] Dependencies updated

## 🛡️ Security Features

### Container Security

#### User Isolation
```dockerfile
# Create non-root user
RUN useradd -m -s /bin/bash -u 1000 ollama
USER ollama
```

**Security Benefits:**
- Prevents privilege escalation
- Limits damage from container breakouts
- Follows principle of least privilege

#### Filesystem Protection
```yaml
read_only: true
tmpfs:
  - /tmp:size=2G,mode=1777
  - /var/tmp:size=1G,mode=1777
```

**Security Benefits:**
- Prevents malicious file modifications
- Limits attack surface
- Contains potential exploits

#### Capability Management
```yaml
cap_drop:
  - ALL
cap_add:
  - SETUID
  - SETGID
```

**Security Benefits:**
- Removes unnecessary system privileges
- Prevents kernel exploits
- Minimizes attack vectors

### Network Security

#### Localhost Binding
```yaml
ports:
  - "127.0.0.1:11434:11434"
```

**Security Benefits:**
- Prevents external access
- Limits network attack surface
- Enables local firewall control

#### Origin Restrictions
```yaml
environment:
  - OLLAMA_ORIGINS=http://localhost:*,http://127.0.0.1:*
```

**Security Benefits:**
- Prevents CSRF attacks
- Controls API access
- Enforces same-origin policy

### Resource Security

#### Memory Limits
```yaml
deploy:
  resources:
    limits:
      memory: 32G
      cpus: "8.0"
```

**Security Benefits:**
- Prevents resource exhaustion attacks
- Limits DoS potential
- Maintains system stability

## 🔍 Security Verification

### Automated Security Check

Run the security verification script:

```bash
./scripts/security-check.sh
```

This script verifies:
- Non-root user execution
- Read-only filesystem status
- Capability configuration
- Port binding restrictions
- Resource limit enforcement

### Manual Verification

#### 1. User Context Check
```bash
# Verify container runs as non-root
docker exec ollama-m4max whoami
# Expected: ollama

# Check user ID
docker exec ollama-m4max id
# Expected: uid=1000(ollama) gid=1000(ollama)
```

#### 2. Filesystem Security
```bash
# Verify read-only root filesystem
docker inspect ollama-m4max --format='{{.HostConfig.ReadonlyRootfs}}'
# Expected: true

# Test write protection
docker exec ollama-m4max touch /test-file 2>&1 | grep "Read-only"
# Expected: Error about read-only filesystem
```

#### 3. Network Security
```bash
# Verify port binding
docker port ollama-m4max
# Expected: 11434/tcp -> 127.0.0.1:11434

# Test external access (should fail)
curl -m 5 http://$(hostname):11434/api/tags
# Expected: Connection refused or timeout
```

#### 4. Capability Verification
```bash
# Check dropped capabilities
docker inspect ollama-m4max --format='{{.HostConfig.CapDrop}}'
# Expected: [ALL]

# Check added capabilities
docker inspect ollama-m4max --format='{{.HostConfig.CapAdd}}'
# Expected: [SETUID SETGID]
```

## 🚨 Security Monitoring

### Log Analysis

Monitor container logs for security events:

```bash
# Check for authentication attempts
docker logs ollama-m4max | grep -i "auth\|login\|access"

# Monitor for errors that might indicate attacks
docker logs ollama-m4max | grep -i "error\|fail\|denied"

# Watch for unusual activity patterns
docker logs ollama-m4max | grep -E "(unusual|suspicious|anomal)"
```

### Resource Monitoring

Track resource usage for anomalies:

```bash
# Monitor memory usage
docker stats ollama-m4max --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"

# Check for memory leaks
docker exec ollama-m4max ps aux | sort -k4 -nr | head -10

# Monitor network connections
docker exec ollama-m4max netstat -an | grep LISTEN
```

### File System Monitoring

Watch for unauthorized file changes:

```bash
# Monitor model directory
ls -la /Volumes/External/ollama_models/

# Check for unexpected files
find /Volumes/External/ollama_models/ -type f -name ".*" -o -name "*~" -o -name "*.tmp"

# Verify file integrity
./scripts/verify-checksums.sh
```

## 🔧 Security Hardening

### Additional Hardening Options

#### Enhanced Container Security
```yaml
# Add to docker-compose.yml
security_opt:
  - no-new-privileges:true
  - seccomp:unconfined  # Required for ML operations
  - apparmor:docker-default  # If AppArmor is available

# Additional user namespace mapping
user_ns_mode: "host"
```

#### Network Hardening
```yaml
# Custom network with restricted access
networks:
  ollama-network:
    driver: bridge
    internal: true  # No external access
    ipam:
      config:
        - subnet: 172.20.0.0/24
```

#### Storage Security
```yaml
# Read-only volume mounts where possible
volumes:
  - /Volumes/External/ollama_models:/ollama:rw,Z  # SELinux label
  - ./config:/config:ro,Z  # Read-only config
```

### macOS-Specific Security

#### System Integrity Protection (SIP)
```bash
# Verify SIP is enabled
csrutil status
# Expected: System Integrity Protection status: enabled
```

#### Gatekeeper Verification
```bash
# Check Gatekeeper status
spctl --status
# Expected: assessments enabled

# Verify Docker Desktop signature
spctl -a -vv /Applications/Docker.app
# Expected: accepted
```

#### FileVault Encryption
```bash
# Verify disk encryption
fdesetup status
# Expected: FileVault is On
```

## 🚫 Security Incidents

### Incident Response Plan

#### 1. Detection
- Monitor logs for suspicious activity
- Set up alerts for resource anomalies
- Watch for unexpected network connections

#### 2. Containment
```bash
# Immediately stop the container
docker stop ollama-m4max

# Isolate the system
sudo pfctl -f /dev/stdin <<< "block all"

# Preserve evidence
docker logs ollama-m4max > incident-logs-$(date +%Y%m%d-%H%M%S).txt
```

#### 3. Investigation
```bash
# Analyze container state
docker inspect ollama-m4max > container-state.json

# Check filesystem changes
docker diff ollama-m4max

# Review network connections
netstat -an | grep 11434 > network-state.txt
```

#### 4. Recovery
```bash
# Remove compromised container
docker rm ollama-m4max

# Rebuild from clean image
docker compose build --no-cache

# Restore from backup if needed
# ... restore procedures ...
```

### Common Security Issues

#### Issue: Container Running as Root
**Detection:**
```bash
docker exec ollama-m4max whoami
# Returns: root (instead of ollama)
```

**Resolution:**
1. Check Dockerfile USER directive
2. Verify docker-compose.yml user specification
3. Rebuild container with correct user

#### Issue: External Network Access
**Detection:**
```bash
curl http://$(hostname):11434/api/tags
# Should fail, but succeeds
```

**Resolution:**
1. Check port binding in docker-compose.yml
2. Verify firewall rules
3. Update network configuration

#### Issue: Privilege Escalation
**Detection:**
```bash
docker exec ollama-m4max sudo whoami
# Should fail, but succeeds
```

**Resolution:**
1. Remove sudo/su from container
2. Check capability configuration
3. Verify security options

## 📋 Security Compliance

### Security Standards Alignment

This configuration aligns with:

- **NIST Cybersecurity Framework**
  - Identify: Asset inventory and risk assessment
  - Protect: Access controls and data security
  - Detect: Monitoring and anomaly detection
  - Respond: Incident response procedures
  - Recover: Backup and restoration plans

- **CIS Docker Benchmark**
  - Non-root user execution
  - Read-only root filesystem
  - Capability restrictions
  - Resource limitations

- **OWASP Container Security**
  - Secure base images
  - Minimal attack surface
  - Runtime protection
  - Monitoring and logging

### Audit Trail

Maintain security documentation:

```bash
# Security configuration audit
./scripts/security-check.sh > security-audit-$(date +%Y%m%d).txt

# Container configuration dump
docker inspect ollama-m4max > container-config-$(date +%Y%m%d).json

# Network configuration
docker network ls > network-config-$(date +%Y%m%d).txt
```

## 🔄 Security Updates

### Update Procedures

#### 1. Ollama Updates
```bash
# Check current version
docker exec ollama-m4max ollama --version

# Update Dockerfile with new version
# Verify new checksums
# Rebuild container
docker compose build --no-cache
```

#### 2. Base Image Updates
```bash
# Pull latest base image
docker pull debian:bullseye-slim

# Rebuild with new base
docker compose build --pull --no-cache
```

#### 3. Security Patches
```bash
# Update macOS
sudo softwareupdate -i -a

# Update Docker Desktop
# (Use Docker Desktop updater)

# Update container dependencies
docker system prune -a
```

### Security Testing

Regular security testing schedule:

- **Weekly**: Automated security scans
- **Monthly**: Manual security review
- **Quarterly**: Penetration testing
- **Annually**: Full security audit

```bash
# Weekly automated scan
./scripts/security-check.sh
docker scan local/ollama:0.1.33

# Monthly manual review
./scripts/manual-security-review.sh

# Quarterly testing
./scripts/penetration-test.sh
```

## 📞 Security Contacts

### Reporting Security Issues

If you discover a security vulnerability:

1. **Do not** create a public issue
2. Email security concerns to: [security@example.com]
3. Include detailed reproduction steps
4. Allow 48 hours for initial response

### Security Resources

- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [macOS Security Guide](https://support.apple.com/guide/security/)
- [Ollama Security Documentation](https://github.com/ollama/ollama/security)
- [Container Security Checklist](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)

---

**Remember**: Security is an ongoing process, not a one-time setup. Regularly review and update your security measures to address new threats and vulnerabilities.
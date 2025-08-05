# =============================================================================
# Ollama Docker Configuration for macOS M4 Max
# Secure, reproducible deployment with CPU-only inference
# =============================================================================

# Base image: Debian Bullseye slim (arm64) optimized for Apple Silicon
FROM debian:bullseye-slim AS base

# Set environment variables for non-interactive package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install essential packages for security and functionality
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        gnupg \
        acl \
        && rm -rf /var/lib/apt/lists/*

# =============================================================================
# Ollama version and verification
# =============================================================================
ARG OLLAMA_VER=0.2.8
ARG OLLAMA_URL=https://github.com/ollama/ollama/releases/download/v${OLLAMA_VER}/ollama-linux-arm64
# IMPORTANT: Update this checksum when updating OLLAMA_VER
# Get the current checksum from: https://github.com/ollama/ollama/releases
ARG OLLAMA_SHA256=2bfa1e3d5a7c6b4e8f9a3e8c1b2d6f58f4e7c9b1124f6d7e5d3c9a2e1f7b4c2a

# =============================================================================
# Security: Create non-root user
# =============================================================================
RUN useradd -m -s /bin/bash -U ollama

# =============================================================================
# Download and verify Ollama binary
# =============================================================================
RUN curl -fsSL -o /usr/local/bin/ollama ${OLLAMA_URL} && \
    echo "${OLLAMA_SHA256}  /usr/local/bin/ollama" | sha256sum -c - && \
    chmod +x /usr/local/bin/ollama

# =============================================================================
# Set up model storage directory
# =============================================================================
ENV OLLAMA_HOME=/ollama
RUN mkdir -p ${OLLAMA_HOME} && \
    chown -R ollama:ollama ${OLLAMA_HOME}

# =============================================================================
# Security: Switch to non-root user
# =============================================================================
USER ollama
WORKDIR ${OLLAMA_HOME}

# =============================================================================
# Expose Ollama API port
# =============================================================================
EXPOSE 11434

# =============================================================================
# Default command: Run Ollama server
# =============================================================================
CMD ["ollama", "serve"]
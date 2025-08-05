# syntax=docker/dockerfile:1.5

# =============================================================================
# Secure Ollama Docker Container for macOS M4 Max (ARM64)
# =============================================================================
# This Dockerfile creates a hardened container for running Ollama locally
# with security best practices for Apple Silicon machines.
# 
# Key Features:
# - Runs as non-root user for security
# - Verifies binary checksums
# - Read-only root filesystem support
# - Optimized for ARM64 architecture
# - Supports CPU-only inference (Metal GPU requires native installation)
# =============================================================================

FROM debian:bullseye-slim

# Metadata
LABEL maintainer="Ollama Docker Configuration" \
      description="Secure Ollama container for macOS M4 Max" \
      version="1.0" \
      architecture="arm64"

# Build arguments for version control and verification
ARG OLLAMA_VERSION=0.1.33
ARG OLLAMA_URL=https://github.com/ollama/ollama/releases/download/v${OLLAMA_VERSION}/ollama-linux-arm64
# SHA256 checksum for ollama-linux-arm64 v0.1.33 
# NOTE: Replace with actual SHA256 from https://github.com/ollama/ollama/releases/tag/v0.1.33
# Download the ollama-linux-arm64 binary and run: shasum -a 256 ollama-linux-arm64
ARG OLLAMA_SHA256=REPLACE_WITH_ACTUAL_SHA256_FROM_OFFICIAL_RELEASE

# Environment variables for non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive \
    OLLAMA_HOME=/ollama \
    OLLAMA_HOST=0.0.0.0:11434 \
    OLLAMA_ORIGINS=http://localhost:*,http://127.0.0.1:*,http://0.0.0.0:*

# Install minimal required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        gnupg \
        dumb-init \
        && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# Create non-root user for security
RUN useradd -m -s /bin/bash -u 1000 ollama && \
    mkdir -p ${OLLAMA_HOME} && \
    chown -R ollama:ollama ${OLLAMA_HOME}

# Download and verify Ollama binary
RUN curl -fsSL -o /tmp/ollama ${OLLAMA_URL} && \
    echo "${OLLAMA_SHA256}  /tmp/ollama" | sha256sum -c - && \
    install -o root -g root -m 0755 /tmp/ollama /usr/local/bin/ollama && \
    rm /tmp/ollama

# Verify the binary works
RUN /usr/local/bin/ollama --version

# Create directory structure and set permissions
RUN mkdir -p ${OLLAMA_HOME}/.ollama/models && \
    mkdir -p /tmp/ollama && \
    chown -R ollama:ollama ${OLLAMA_HOME} && \
    chown -R ollama:ollama /tmp/ollama

# Switch to non-root user
USER ollama
WORKDIR ${OLLAMA_HOME}

# Health check to ensure service is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:11434/api/tags || exit 1

# Expose the API port
EXPOSE 11434

# Use dumb-init to handle signals properly
ENTRYPOINT ["/usr/bin/dumb-init", "--"]

# Default command to start Ollama server
CMD ["ollama", "serve"]
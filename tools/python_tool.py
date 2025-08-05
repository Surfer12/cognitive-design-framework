"""
Python Tool Implementation for GPT-OSS

This implementation provides Python code execution capabilities for the cognitive framework.
Based on the GPT-OSS Python tool specification.
"""

import os
import asyncio
import json
import subprocess
import tempfile
import docker
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
import uuid
import time


@dataclass
class PythonToolConfig:
    """Configuration for the Python tool."""
    timeout: int = 30
    memory_limit: str = "512m"
    cpu_limit: str = "1.0"
    network_disabled: bool = True
    read_only: bool = True
    container_image: str = "python:3.11-slim"
    max_output_size: int = 1000000  # 1MB


class DockerBackend:
    """
    Docker backend for safe Python code execution.
    
    Note: This is a simplified implementation. In production, you should:
    1. Implement proper security measures
    2. Add resource monitoring
    3. Implement proper cleanup
    4. Add logging and monitoring
    """
    
    def __init__(self, config: Optional[PythonToolConfig] = None):
        self.config = config or PythonToolConfig()
        self.client = docker.from_env()
        self.container_name_prefix = "gpt_oss_python_"
    
    def _create_container_name(self) -> str:
        """Create a unique container name."""
        return f"{self.container_name_prefix}{uuid.uuid4().hex[:8]}"
    
    def _create_dockerfile(self, code: str) -> str:
        """Create a Dockerfile for the Python code."""
        return f"""
FROM {self.config.container_image}

# Install basic packages
RUN pip install --no-cache-dir numpy pandas matplotlib requests

# Create a non-root user
RUN useradd -m -u 1000 pythonuser
USER pythonuser
WORKDIR /app

# Copy the code
COPY code.py /app/code.py

# Run the code
CMD ["python", "code.py"]
"""
    
    async def execute(self, code: str) -> Dict[str, Any]:
        """Execute Python code in a Docker container."""
        container_name = self._create_container_name()
        
        try:
            # Create temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                # Write code to file
                code_file = os.path.join(temp_dir, "code.py")
                with open(code_file, 'w') as f:
                    f.write(code)
                
                # Create Dockerfile
                dockerfile_content = self._create_dockerfile(code)
                dockerfile_path = os.path.join(temp_dir, "Dockerfile")
                with open(dockerfile_path, 'w') as f:
                    f.write(dockerfile_content)
                
                # Build image
                image, logs = self.client.images.build(
                    path=temp_dir,
                    tag=f"gpt_oss_python_{uuid.uuid4().hex[:8]}",
                    rm=True
                )
                
                # Run container
                container = self.client.containers.run(
                    image.id,
                    name=container_name,
                    detach=True,
                    mem_limit=self.config.memory_limit,
                    cpu_quota=int(float(self.config.cpu_limit) * 100000),
                    cpu_period=100000,
                    network_disabled=self.config.network_disabled,
                    read_only=self.config.read_only,
                    remove=True
                )
                
                # Wait for completion with timeout
                start_time = time.time()
                while container.status == 'running':
                    if time.time() - start_time > self.config.timeout:
                        container.kill()
                        return {
                            "error": "Execution timeout",
                            "stdout": "",
                            "stderr": "",
                            "exit_code": -1
                        }
                    await asyncio.sleep(0.1)
                    container.reload()
                
                # Get logs
                logs = container.logs().decode('utf-8')
                
                # Check output size
                if len(logs) > self.config.max_output_size:
                    logs = logs[:self.config.max_output_size] + "\n... (output truncated)"
                
                return {
                    "stdout": logs,
                    "stderr": "",
                    "exit_code": container.attrs['State']['ExitCode'],
                    "error": None
                }
                
        except Exception as e:
            return {
                "error": str(e),
                "stdout": "",
                "stderr": "",
                "exit_code": -1
            }
        finally:
            # Cleanup
            try:
                container = self.client.containers.get(container_name)
                container.remove(force=True)
            except:
                pass


class PythonTool:
    """
    Python tool implementation for GPT-OSS.
    
    Provides safe Python code execution in isolated containers.
    """
    
    def __init__(self, backend: Optional[DockerBackend] = None, config: Optional[PythonToolConfig] = None):
        self.backend = backend or DockerBackend(config)
        self.config = config or PythonToolConfig()
        self.state: Dict[str, Any] = {}
    
    @property
    def tool_config(self) -> Dict[str, Any]:
        """Return the tool configuration for harmony formatting."""
        return {
            "type": "python",
            "description": "A Python execution tool that can run Python code in isolated containers",
            "methods": {
                "execute": {
                    "description": "Execute Python code",
                    "parameters": {
                        "code": {"type": "string", "description": "Python code to execute"}
                    }
                },
                "get_state": {
                    "description": "Get the current state",
                    "parameters": {}
                },
                "set_state": {
                    "description": "Set a value in the state",
                    "parameters": {
                        "key": {"type": "string", "description": "State key"},
                        "value": {"type": "string", "description": "State value"}
                    }
                }
            }
        }
    
    async def execute(self, code: str) -> Dict[str, Any]:
        """Execute Python code and return the result."""
        # Add state variables to the code
        if self.state:
            state_code = "\n".join([f"{k} = {repr(v)}" for k, v in self.state.items()])
            code = f"{state_code}\n\n{code}"
        
        result = await self.backend.execute(code)
        
        # Parse output for state updates
        if result.get("stdout"):
            try:
                # Look for state updates in the output
                lines = result["stdout"].split('\n')
                for line in lines:
                    if line.startswith("STATE_UPDATE:"):
                        try:
                            update = json.loads(line[13:])
                            self.state.update(update)
                        except:
                            pass
            except:
                pass
        
        return result
    
    def get_state(self) -> Dict[str, Any]:
        """Get the current state."""
        return self.state.copy()
    
    def set_state(self, key: str, value: Any) -> None:
        """Set a value in the state."""
        self.state[key] = value
    
    def clear_state(self) -> None:
        """Clear the state."""
        self.state.clear()
    
    async def process(self, message) -> List[Dict[str, Any]]:
        """Process a Python tool message and return response messages."""
        # This would be implemented based on the specific message format
        # from the harmony encoding system
        pass


# Example usage
async def main():
    """Example usage of the Python tool."""
    # Initialize the Python tool
    python_tool = PythonTool()
    
    # Execute simple code
    code = """
import math
print("Hello from Python!")
print(f"Pi: {math.pi}")
print(f"Square root of 16: {math.sqrt(16)}")
"""
    
    result = await python_tool.execute(code)
    print("Execution result:", result)
    
    # Execute code with state
    python_tool.set_state("x", 10)
    code_with_state = """
print(f"Current x: {x}")
x = x * 2
print(f"New x: {x}")
"""
    
    result = await python_tool.execute(code_with_state)
    print("Execution with state:", result)
    print("Final state:", python_tool.get_state())


if __name__ == "__main__":
    asyncio.run(main())
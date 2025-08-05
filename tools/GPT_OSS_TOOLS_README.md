# GPT-OSS Tools Implementation

This directory contains implementations of the browser and Python tools for GPT-OSS models, as described in the official documentation. These tools provide web browsing and Python code execution capabilities for cognitive AI systems.

## Overview

The GPT-OSS models were trained with the capability to browse using the browser tool and execute Python code using the Python tool. This implementation provides:

- **Browser Tool**: Web search, page opening, and content finding capabilities
- **Python Tool**: Safe Python code execution in isolated Docker containers
- **Integration Example**: Complete demonstration of tool usage with harmony encoding

## Files

- `browser_tool.py` - Browser tool implementation with Exa backend
- `python_tool.py` - Python tool implementation with Docker backend
- `integration_example.py` - Complete integration demonstration
- `requirements.txt` - Python dependencies
- `GPT_OSS_TOOLS_README.md` - This documentation

## Browser Tool

### Features

The browser tool provides three main methods:

1. **search(query)**: Search for key phrases on the web
2. **open(url)**: Open a particular page and retrieve content
3. **find(url, query)**: Look for specific content on a page

### Implementation Details

- Uses Exa API for web search and content retrieval
- Implements scrollable window for large pages
- Caches requests for performance
- Configurable content limits and timeouts

### Setup

1. Get an Exa API key from [exa.ai](https://exa.ai)
2. Set the environment variable:
   ```bash
   export EXA_API_KEY="your_api_key_here"
   ```

### Usage

```python
from browser_tool import SimpleBrowserTool, ExaBackend

# Initialize the browser tool
backend = ExaBackend(source="web")
browser_tool = SimpleBrowserTool(backend=backend)

# Search for information
results = await browser_tool.search("artificial intelligence")

# Open a specific page
content = await browser_tool.open("https://example.com")

# Find content on a page
matches = await browser_tool.find("https://example.com", "example")
```

## Python Tool

### Features

The Python tool provides safe code execution with:

1. **execute(code)**: Execute Python code in isolated containers
2. **get_state()**: Retrieve the current execution state
3. **set_state(key, value)**: Set values in the execution state

### Implementation Details

- Uses Docker containers for isolation
- Implements resource limits (memory, CPU, timeout)
- Supports stateful execution across multiple calls
- Configurable security settings

### Setup

1. Install Docker on your system
2. Ensure Docker daemon is running
3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

```python
from python_tool import PythonTool

# Initialize the Python tool
python_tool = PythonTool()

# Execute simple code
code = """
import math
print(f"Pi: {math.pi}")
"""
result = await python_tool.execute(code)

# Execute code with state
python_tool.set_state("x", 10)
code_with_state = """
print(f"Current x: {x}")
x = x * 2
print(f"New x: {x}")
"""
result = await python_tool.execute(code_with_state)
```

## Integration with Harmony Encoding

The tools are designed to work with the harmony encoding system. Here's how to integrate them:

### System Message Configuration

```python
import datetime
from openai_harmony import SystemContent, Message, Conversation, Role

# Create system content with tools
system_content = SystemContent.new().with_conversation_start_date(
    datetime.datetime.now().strftime("%Y-%m-%d")
)

# Add browser tool
system_content = system_content.with_tools(browser_tool.tool_config)

# Add python tool
system_content = system_content.with_tools(python_tool.tool_config)

# Create system message
system_message = Message.from_role_and_content(Role.SYSTEM, system_content)
```

### Processing Tool Messages

```python
# Convert conversation to tokens
token_ids = encoding.render_conversation_for_completion(conversation, Role.ASSISTANT)

# Perform inference
output_tokens = await model.infer(token_ids)

# Parse the output
messages = encoding.parse_messages_from_completion_tokens(output_tokens, Role.ASSISTANT)
last_message = messages[-1]

# Check if message is for a tool
if last_message.recipient.startswith("browser"):
    response_messages = await browser_tool.process(last_message)
    # Extend conversation and run inference again
    messages.extend(response_messages)
```

## Configuration

### Browser Tool Configuration

```python
from browser_tool import BrowserConfig

config = BrowserConfig(
    max_content_length=50000,
    max_lines_per_page=200,
    cache_size=100,
    timeout=30
)

browser_tool = SimpleBrowserTool(config=config)
```

### Python Tool Configuration

```python
from python_tool import PythonToolConfig

config = PythonToolConfig(
    timeout=30,
    memory_limit="512m",
    cpu_limit="1.0",
    network_disabled=True,
    read_only=True
)

python_tool = PythonTool(config=config)
```

## Security Considerations

### Browser Tool

- API key management
- Rate limiting
- Content filtering
- URL validation

### Python Tool

- Container isolation
- Resource limits
- Network restrictions
- Read-only filesystem
- Non-root user execution

## Performance Optimization

### Browser Tool

- Request caching
- Content compression
- Parallel requests
- Smart pagination

### Python Tool

- Container reuse
- State management
- Output streaming
- Resource monitoring

## Error Handling

Both tools implement comprehensive error handling:

- Network timeouts
- API rate limits
- Container failures
- Resource exhaustion
- Invalid inputs

## Testing

Run the integration example:

```bash
cd tools
python integration_example.py
```

Run individual tool tests:

```bash
python browser_tool.py
python python_tool.py
```

## Production Deployment

### Requirements

1. **Environment Setup**
   - Docker daemon running
   - Exa API key configured
   - Resource monitoring

2. **Security Measures**
   - Container security policies
   - API key rotation
   - Access logging

3. **Monitoring**
   - Tool usage metrics
   - Error tracking
   - Performance monitoring

### Scaling Considerations

- Container orchestration
- Load balancing
- Caching strategies
- Resource allocation

## Troubleshooting

### Common Issues

1. **Docker not available**
   - Install Docker
   - Ensure Docker daemon is running
   - Check user permissions

2. **Exa API key not set**
   - Set EXA_API_KEY environment variable
   - Verify API key validity
   - Check rate limits

3. **Container execution failures**
   - Check Docker logs
   - Verify resource limits
   - Review security policies

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

1. Follow the existing code style
2. Add comprehensive tests
3. Update documentation
4. Consider security implications

## License

[Specify your licensing terms]

## Acknowledgments

- GPT-OSS development team
- Exa.ai for web search API
- Docker community
- Open-source contributors
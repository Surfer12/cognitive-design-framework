"""
Integration Example for GPT-OSS Tools

This example demonstrates how to integrate the browser and Python tools
with the harmony encoding system as described in the GPT-OSS documentation.
"""

import os
import asyncio
import datetime
from typing import Dict, List, Optional, Any

# Import the tools we created
from browser_tool import SimpleBrowserTool, ExaBackend, BrowserConfig
from python_tool import PythonTool, DockerBackend, PythonToolConfig

# Mock imports for harmony encoding (you would need to install these)
# from openai_harmony import SystemContent, Message, Conversation, Role, load_harmony_encoding, HarmonyEncodingName


class MockHarmonyEncoding:
    """Mock implementation of harmony encoding for demonstration."""
    
    @staticmethod
    def render_conversation_for_completion(conversation, role):
        """Mock rendering of conversation to tokens."""
        return [1, 2, 3, 4, 5]  # Mock token IDs
    
    @staticmethod
    def parse_messages_from_completion_tokens(tokens, role):
        """Mock parsing of tokens back to messages."""
        return [{"role": "assistant", "content": "Mock response"}]


class MockSystemContent:
    """Mock SystemContent for demonstration."""
    
    def __init__(self):
        self.tools = []
        self.browser_enabled = False
    
    def with_conversation_start_date(self, date):
        return self
    
    def with_tools(self, tool_config):
        self.tools.append(tool_config)
        return self
    
    def with_browser(self):
        self.browser_enabled = True
        return self
    
    def with_python(self):
        self.tools.append({"type": "python"})
        return self


class MockMessage:
    """Mock Message for demonstration."""
    
    def __init__(self, role, content):
        self.role = role
        self.content = content
        self.recipient = None
    
    @staticmethod
    def from_role_and_content(role, content):
        return MockMessage(role, content)


class MockConversation:
    """Mock Conversation for demonstration."""
    
    def __init__(self, messages):
        self.messages = messages
    
    @staticmethod
    def from_messages(messages):
        return MockConversation(messages)


class MockRole:
    """Mock Role enum for demonstration."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class GPTOSSToolsIntegration:
    """
    Integration class for GPT-OSS tools with harmony encoding.
    
    This demonstrates how to use the browser and Python tools
    as described in the GPT-OSS documentation.
    """
    
    def __init__(self, use_browser_tool: bool = True, use_python_tool: bool = True):
        self.use_browser_tool = use_browser_tool
        self.use_python_tool = use_python_tool
        
        # Initialize tools
        self.browser_tool = None
        self.python_tool = None
        
        if use_browser_tool:
            # Check for API key
            if not os.getenv("EXA_API_KEY"):
                print("Warning: EXA_API_KEY not set. Browser tool will not work.")
            else:
                backend = ExaBackend(source="web")
                self.browser_tool = SimpleBrowserTool(backend=backend)
        
        if use_python_tool:
            try:
                import docker
                self.python_tool = PythonTool()
            except ImportError:
                print("Warning: Docker not available. Python tool will not work.")
    
    def create_system_message(self) -> MockMessage:
        """Create a system message with tool configurations."""
        # Create basic system prompt
        system_content = MockSystemContent().with_conversation_start_date(
            datetime.datetime.now().strftime("%Y-%m-%d")
        )
        
        # Add browser tool if enabled
        if self.use_browser_tool and self.browser_tool:
            system_content = system_content.with_tools(self.browser_tool.tool_config)
            # Alternatively: system_content = system_content.with_browser()
        
        # Add python tool if enabled
        if self.use_python_tool and self.python_tool:
            system_content = system_content.with_tools(self.python_tool.tool_config)
            # Alternatively: system_content = system_content.with_python()
        
        return MockMessage.from_role_and_content(MockRole.SYSTEM, system_content)
    
    def create_conversation(self, user_message: str) -> MockConversation:
        """Create a conversation with system and user messages."""
        system_message = self.create_system_message()
        user_msg = MockMessage.from_role_and_content(MockRole.USER, user_message)
        
        return MockConversation.from_messages([system_message, user_msg])
    
    async def process_with_tools(self, user_query: str) -> Dict[str, Any]:
        """Process a user query with the available tools."""
        # Create conversation
        conversation = self.create_conversation(user_query)
        
        # Mock token rendering (in real implementation, this would use the actual harmony encoding)
        encoding = MockHarmonyEncoding()
        token_ids = encoding.render_conversation_for_completion(conversation, MockRole.ASSISTANT)
        
        # Mock inference (in real implementation, this would call your model)
        output_tokens = await self.mock_inference(token_ids)
        
        # Parse the output
        messages = encoding.parse_messages_from_completion_tokens(output_tokens, MockRole.ASSISTANT)
        last_message = messages[-1]
        
        # Check if the message is for a tool
        if last_message.get("recipient", "").startswith("browser") and self.browser_tool:
            response_messages = await self.browser_tool.process(last_message)
            # Extend conversation and run inference again
            conversation.messages.extend(response_messages)
            return {"type": "browser_response", "messages": response_messages}
        
        elif last_message.get("recipient", "").startswith("python") and self.python_tool:
            response_messages = await self.python_tool.process(last_message)
            # Extend conversation and run inference again
            conversation.messages.extend(response_messages)
            return {"type": "python_response", "messages": response_messages}
        
        else:
            return {"type": "assistant_response", "message": last_message}
    
    async def mock_inference(self, token_ids: List[int]) -> List[int]:
        """Mock inference function (replace with actual model call)."""
        # In a real implementation, this would call your GPT-OSS model
        await asyncio.sleep(0.1)  # Simulate processing time
        return [6, 7, 8, 9, 10]  # Mock output tokens
    
    async def demonstrate_browser_tool(self):
        """Demonstrate browser tool functionality."""
        if not self.browser_tool:
            print("Browser tool not available")
            return
        
        print("=== Browser Tool Demonstration ===")
        
        # Search for information
        print("Searching for 'artificial intelligence'...")
        results = await self.browser_tool.search("artificial intelligence")
        print(f"Found {len(results)} results")
        for i, result in enumerate(results[:3]):
            print(f"{i+1}. {result.get('title', 'No title')}")
            print(f"   URL: {result.get('url', 'No URL')}")
            print(f"   Snippet: {result.get('snippet', 'No snippet')[:100]}...")
            print()
        
        # Open a specific page
        print("Opening example.com...")
        content = await self.browser_tool.open("https://example.com")
        if content:
            print(f"Page content length: {len(content)} characters")
            print(f"First 200 characters: {content[:200]}...")
        else:
            print("Failed to retrieve page content")
        print()
    
    async def demonstrate_python_tool(self):
        """Demonstrate Python tool functionality."""
        if not self.python_tool:
            print("Python tool not available")
            return
        
        print("=== Python Tool Demonstration ===")
        
        # Execute simple code
        print("Executing simple Python code...")
        code = """
import math
import json

print("Hello from Python!")
print(f"Pi: {math.pi}")
print(f"Square root of 16: {math.sqrt(16)}")

# Demonstrate state updates
result = {"pi": math.pi, "sqrt_16": math.sqrt(16)}
print(f"STATE_UPDATE:{json.dumps(result)}")
"""
        
        result = await self.python_tool.execute(code)
        print("Execution result:")
        print(f"Exit code: {result.get('exit_code', 'Unknown')}")
        print(f"Output: {result.get('stdout', 'No output')}")
        if result.get('error'):
            print(f"Error: {result.get('error')}")
        print()
        
        # Execute code with mathematical calculations
        print("Executing mathematical calculations...")
        math_code = """
import numpy as np

# Create some data
data = np.array([1, 2, 3, 4, 5])
mean = np.mean(data)
std = np.std(data)

print(f"Data: {data}")
print(f"Mean: {mean}")
print(f"Standard deviation: {std}")

# State update
print(f"STATE_UPDATE:{{\"mean\": {mean}, \"std\": {std}}}")
"""
        
        result = await self.python_tool.execute(math_code)
        print("Math execution result:")
        print(f"Output: {result.get('stdout', 'No output')}")
        print()
        
        # Show final state
        print("Final tool state:")
        print(self.python_tool.get_state())
        print()


async def main():
    """Main demonstration function."""
    print("GPT-OSS Tools Integration Demonstration")
    print("=" * 50)
    print()
    
    # Create integration instance
    integration = GPTOSSToolsIntegration(
        use_browser_tool=True,
        use_python_tool=True
    )
    
    # Demonstrate browser tool
    await integration.demonstrate_browser_tool()
    
    # Demonstrate Python tool
    await integration.demonstrate_python_tool()
    
    # Demonstrate integrated processing
    print("=== Integrated Processing Demonstration ===")
    
    # Example queries that might trigger tool usage
    queries = [
        "What's the weather in San Francisco?",
        "Calculate the factorial of 10",
        "Search for information about machine learning",
        "What is 2^10?"
    ]
    
    for query in queries:
        print(f"Processing query: {query}")
        try:
            result = await integration.process_with_tools(query)
            print(f"Result type: {result.get('type', 'Unknown')}")
            print()
        except Exception as e:
            print(f"Error processing query: {e}")
            print()
    
    print("Demonstration complete!")


if __name__ == "__main__":
    asyncio.run(main())
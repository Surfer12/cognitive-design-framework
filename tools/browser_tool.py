"""
Browser Tool Implementation for GPT-OSS

This implementation provides web browsing capabilities for the cognitive framework.
Based on the GPT-OSS browser tool specification.
"""

import os
import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import requests
from urllib.parse import urlparse, urljoin
import re


@dataclass
class BrowserConfig:
    """Configuration for the browser tool."""
    max_content_length: int = 50000
    max_lines_per_page: int = 200
    cache_size: int = 100
    timeout: int = 30
    user_agent: str = "Mozilla/5.0 (compatible; GPT-OSS-Browser/1.0)"


class ExaBackend:
    """
    Exa backend implementation for web browsing.
    
    Note: This is a simplified implementation. In production, you should:
    1. Implement proper error handling
    2. Add rate limiting
    3. Implement proper caching
    4. Add security measures
    """
    
    def __init__(self, source: str = "web", api_key: Optional[str] = None):
        self.source = source
        self.api_key = api_key or os.getenv("EXA_API_KEY")
        if not self.api_key:
            raise ValueError("EXA_API_KEY environment variable must be set")
        
        self.base_url = "https://api.exa.ai"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": "GPT-OSS-Browser/1.0"
        })
    
    async def search(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """Search for content using Exa API."""
        try:
            response = self.session.post(
                f"{self.base_url}/search",
                json={
                    "query": query,
                    "numResults": num_results,
                    "includeDomains": [],
                    "excludeDomains": [],
                    "useAutoprompt": True
                }
            )
            response.raise_for_status()
            return response.json().get("results", [])
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    async def get_content(self, url: str) -> Optional[str]:
        """Get content from a URL using Exa API."""
        try:
            response = self.session.post(
                f"{self.base_url}/contents",
                json={"urls": [url]}
            )
            response.raise_for_status()
            results = response.json().get("contents", [])
            return results[0].get("text") if results else None
        except Exception as e:
            print(f"Content retrieval error: {e}")
            return None


class SimpleBrowserTool:
    """
    Simple browser tool implementation for GPT-OSS.
    
    Provides three main methods:
    - search: Search for key phrases
    - open: Open a particular page
    - find: Look for contents on a page
    """
    
    def __init__(self, backend: Optional[ExaBackend] = None, config: Optional[BrowserConfig] = None):
        self.backend = backend or ExaBackend()
        self.config = config or BrowserConfig()
        self.cache: Dict[str, str] = {}
        self.page_cache: Dict[str, List[str]] = {}
    
    @property
    def tool_config(self) -> Dict[str, Any]:
        """Return the tool configuration for harmony formatting."""
        return {
            "type": "browser",
            "description": "A web browser tool that can search, open pages, and find content",
            "methods": {
                "search": {
                    "description": "Search for key phrases on the web",
                    "parameters": {
                        "query": {"type": "string", "description": "Search query"}
                    }
                },
                "open": {
                    "description": "Open a particular page",
                    "parameters": {
                        "url": {"type": "string", "description": "URL to open"}
                    }
                },
                "find": {
                    "description": "Look for contents on a page",
                    "parameters": {
                        "url": {"type": "string", "description": "URL of the page"},
                        "query": {"type": "string", "description": "Text to search for on the page"}
                    }
                }
            }
        }
    
    async def search(self, query: str) -> List[Dict[str, Any]]:
        """Search for key phrases on the web."""
        results = await self.backend.search(query)
        return [
            {
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "snippet": result.get("text", "")[:200] + "..."
            }
            for result in results
        ]
    
    async def open(self, url: str) -> Optional[str]:
        """Open a particular page and return its content."""
        if url in self.cache:
            return self.cache[url]
        
        content = await self.backend.get_content(url)
        if content:
            # Split content into lines for scrollable window
            lines = content.split('\n')
            self.page_cache[url] = lines
            self.cache[url] = content[:self.config.max_content_length]
            
            # Manage cache size
            if len(self.cache) > self.config.cache_size:
                oldest_key = next(iter(self.cache))
                del self.cache[oldest_key]
                del self.page_cache[oldest_key]
        
        return content
    
    async def find(self, url: str, query: str) -> List[Dict[str, Any]]:
        """Look for contents on a page."""
        content = await self.open(url)
        if not content:
            return []
        
        # Simple text search implementation
        lines = content.split('\n')
        matches = []
        
        for i, line in enumerate(lines):
            if query.lower() in line.lower():
                start_line = max(0, i - 2)
                end_line = min(len(lines), i + 3)
                context = lines[start_line:end_line]
                
                matches.append({
                    "line": i + 1,
                    "context": "\n".join(context),
                    "match": line.strip()
                })
        
        return matches
    
    async def process(self, message) -> List[Dict[str, Any]]:
        """Process a browser tool message and return response messages."""
        # This would be implemented based on the specific message format
        # from the harmony encoding system
        pass


# Example usage
async def main():
    """Example usage of the browser tool."""
    # Initialize the browser tool
    browser = SimpleBrowserTool()
    
    # Search for information
    results = await browser.search("artificial intelligence latest developments")
    print("Search results:", results)
    
    # Open a specific page
    content = await browser.open("https://example.com")
    print("Page content length:", len(content) if content else 0)
    
    # Find specific content on a page
    matches = await browser.find("https://example.com", "example")
    print("Found matches:", len(matches))


if __name__ == "__main__":
    asyncio.run(main())
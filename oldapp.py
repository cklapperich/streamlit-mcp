import chainlit as cl
from typing import List, Dict, Any
from mcpclient import MCPClient
import httpx
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class OpenRouterClient:
    def __init__(self, api_key: str, model: str = "anthropic/claude-3.5-sonnet"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1"
        
    async def chat_completion(self, messages: List[Dict[str, str]], stream=True) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "HTTP-Referer": "http://localhost:8000",
                    "X-Title": "Local Testing"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": stream
                },
                timeout=60.0
            )
            response.raise_for_status()
            
            if stream:
                content = ""
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        try:
                            chunk = json.loads(line[6:])
                            if chunk["choices"][0]["finish_reason"] is not None:
                                continue
                            delta = chunk["choices"][0]["delta"].get("content", "")
                            content += delta
                            yield delta
                        except json.JSONDecodeError:
                            continue
            else:
                content = response.json()["choices"][0]["message"]["content"]
                yield content



@cl.on_chat_start
async def start():
    try:
        # Initialize OpenRouter client with API key from environment variables
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is not set")
            
        llm = OpenRouterClient(
            api_key=api_key,
            model="anthropic/claude-3.5-sonnet"
        )
        
        # Initialize MCP client using context manager
        client = MCPClient('mcp_config_windows.json')
        await client.__aenter__()  # This starts all server connections
        
        # Store in session for later cleanup
        cl.user_session.set("client", client)
        cl.user_session.set("llm", llm)
        cl.user_session.set("conversation_history", [])
        
        # List available tools after servers are started
        tools_info = await client.list_available_tools()
        
        tools_display = []
        for server_id, tools in tools_info.items():
            for tool in tools:
                tools_display.append(f"- {tool['name']}: {tool['description']}")
        
        await cl.Message(
            content=f"Connected to MCP Servers: {list(tools_info.keys())}\n\nAvailable tools:\n" + 
                    "\n".join(tools_display)
        ).send()
    except Exception as e:
        import traceback
        error_details = f"Error during initialization: {str(e)}\n{traceback.format_exc()}"
        print("\nERROR DETAILS:", error_details)
        await cl.Message(content=f"Error during initialization: {str(e)}").send()

@cl.on_chat_end
async def end():
    """Cleanup MCP client when the chat session ends"""
    client = cl.user_session.get("client")
    if client:
        await client.__aexit__(None, None, None)

@cl.on_message
async def main(message: cl.Message):
    response = cl.Message(content="sample response...")
    response.send()

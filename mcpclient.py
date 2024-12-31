import json
import asyncio
from typing import Optional, Dict
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from anthropic import Anthropic
from dotenv import load_dotenv
import os

class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic()
        
    @staticmethod
    def load_config(config_path: str) -> Dict:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config.get('mcpServers', {})

    async def connect_to_server(self, server_config: Dict):
        command = server_config.get('command')
        args = server_config.get('args', [])
        env = server_config.get('env')
        
        server_params = StdioServerParameters(
            command=command,
            args=args,
            env=env
        )
        
        try:
            transport = await stdio_client(server_params)
            self.stdio, self.write = transport
            self.session = ClientSession(self.stdio, self.write)
            await self.session.initialize()
            return await self.session.list_tools()
        finally:
            if hasattr(self, 'session') and hasattr(self.session, 'close'):
                await self.session.close()
            if hasattr(self, 'stdio') and hasattr(self.stdio, 'close'):
                await self.stdio.close()

    async def process_query(self, query: str) -> str:
        messages = [{"role": "user", "content": query}]

        response = await self.session.list_tools()
        available_tools = [{ 
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema
        } for tool in response.tools]

        response = self.anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=messages,
            tools=available_tools
        )

        tool_results = []
        final_text = []

        for content in response.content:
            if content.type == 'text':
                final_text.append(content.text)
            elif content.type == 'tool_use':
                tool_name = content.name
                tool_args = content.input
                
                result = await self.session.call_tool(tool_name, tool_args)
                tool_results.append({"call": tool_name, "result": result})
                final_text.append(f"[Tool {tool_name} called with {tool_args}]")
                final_text.append(f"[Result: {result.content}]")

                if hasattr(content, 'text') and content.text:
                    messages.append({
                      "role": "assistant",
                      "content": content.text
                    })
                messages.append({
                    "role": "user", 
                    "content": result.content
                })

                response = self.anthropic.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1000,
                    messages=messages,
                )

                final_text.append(response.content[0].text)

        return "\n".join(final_text)

    async def cleanup(self):
        await self.exit_stack.aclose()
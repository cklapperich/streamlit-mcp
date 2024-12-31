import json
import asyncio
from typing import Optional, Dict
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from anthropic import Anthropic
from dotenv import load_dotenv
import os

class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
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
        
        print(f"Connecting with command: {command}, args: {args}")
        
        server_params = StdioServerParameters(
            command=command,
            args=args,
            env=env
        )

        try:
            print("Establishing stdio connection...")
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    # Initialize the connection
                    await session.initialize()

                    # List available tools
                    tools = await session.list_tools()
                    return tools
                            
        except Exception as e:
            print(f"Connection error: {e}")
            raise

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
        if self.session:
            await self.session.close()
        if hasattr(self, 'stdio'):
            await self.stdio.close()

if __name__=='__main__':
    async def main():
        client = MCPClient()
        config = client.load_config('mcp_config.json')
        tools = await client.connect_to_server(config['filesystem'])
        # print(tools)

    asyncio.run(main())
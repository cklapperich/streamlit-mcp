from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import json
from typing import Dict

# Create server parameters for stdio connection
def load_config(config_path: str) -> Dict:
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config.get('mcpServers', {})


server_config = load_config('mcp_config.json')['filesystem']
command = server_config.get('command')
args = server_config.get('args', [])
env = server_config.get('env')
server_params = StdioServerParameters(
    command=command,
    args=args,
    env=env
)

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:


            # Initialize the connection
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print(tools)
            
            # # Call a tool
            # result = await session.call_tool("tool-name", arguments={"arg1": "value"})

if __name__ == "__main__":
    import asyncio
    asyncio.run(run())
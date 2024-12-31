from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import json
from typing import Dict


# Create server parameters for stdio connection
def load_config(config_path: str) -> Dict:
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config.get('mcpServers', {})


server_config = load_config('mcp_config_windows.json')['filesystem']
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
# [Tool(name='read_file', description='Read the complete contents of a file from the file system. Handles various text encodings and provides detailed error messages if the file cannot be read. Use this tool when you need to examine the contents of a single file. Only works within allowed directories.', inputSchema={'type': 'object', 'properties': {'path': {'type': 'string'}}, 'required': ['path'], 'additionalProperties': False, '$schema': 'http://json-schema.org/draft-07/schema#'})
            # List available tools
            nextCursor, tools_tuple = await session.list_tools()
            tools = tools_tuple[1]
            for tool in tools:
                print(type(tool))
                print(tool.name, tool.description, tool.inputSchema)
            # # Call a tool
            # result = await session.call_tool("tool-name", arguments={"arg1": "value"})

if __name__ == "__main__":
    import asyncio
    asyncio.run(run())
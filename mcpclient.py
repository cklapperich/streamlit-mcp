import json
import asyncio
from typing import Optional, Dict
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from anthropic import Anthropic
from llama_index.core.agent import ReActAgent
from mcp.types import Tool
from llama_index.core.llms import LLM
from llama_index.core.tools import FunctionTool
from llama_index.core import Settings
from typing import List

# # Call a tool
# result = await session.call_tool("tool-name", arguments={"arg1": "value"})

class MCPClient:
    def __init__(self, config_path='./mcp_config.json'):
        self.server_params_dict = self._load_config(config_path)
        self.sessions: Optional[List[ClientSession]] = None
        self.anthropic = Anthropic()

    @staticmethod
    def _load_config(config_path: str) -> Dict[str, StdioServerParameters]:
        with open(config_path, 'r') as f:
            config = json.load(f)

        print(f"Connecting with command: {command}, args: {args}")
        

        server_params_dict = {}
        server_dict = config.get('mcpServers', {})

        for item, server_config in server_dict.items():
            command = server_config.get('command')
            args = server_config.get('args', [])
            env = server_config.get('env')
            server_params = StdioServerParameters(command, args, env)
            server_params_dict[item] = server_params

        return server_params_dict

    async def connect(self):
        """ Connect to all available MCP servers and maintain a list of active sessions in a dictionary"""
        for servername, server_params in self.server_params_dict.items():
            self.sessions[servername] = self._connect_to_server(server_params)

    async def _connect_to_server(self, server_params:StdioServerParameters):
        try:
            print("Establishing stdio connection...")
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    return session
                            
        except Exception as e:
            print(f"Connection error: {e}")
            raise

    async def _get_tools_for_server(self, servername: str) -> List[FunctionTool]:
        """Get a list of tools for a specific MCP server."""
        
        if servername not in self.sessions:
            raise ValueError(f"No active session for server: {servername}"
                             "Please connect to the server first.")
        
        tool_functions = []

        session = self.sessions[servername]
        nextCursor, tools_tuple = await session.list_tools()
        tools:List[Tool] = tools_tuple[1]

        for tool in tools:
            # Create a synchronous wrapper function that will call the async tool
            def make_sync_tool(tool_name):
                async def _call_tool(**kwargs):
                    return await session.call(tool_name, kwargs)
                
                # Create a sync wrapper that runs the async function
                def sync_tool_wrapper(**kwargs):
                    # Get or create an event loop
                    loop = asyncio.get_event_loop()
                    return loop.run_until_complete(_call_tool(**kwargs))
                
                return sync_tool_wrapper

            # Create the sync function for this specific tool
            sync_fn = make_sync_tool(tool.name)
            
            # Create the llama_index tool
            llama_index_tool = FunctionTool.from_defaults(
                fn=sync_fn,
                name=tool.name,
                description=tool.description
            )
            tool_functions.append(llama_index_tool)
            
        return tool_functions

    def _get_all_tool_functions(self) -> List[FunctionTool]:
        """Get a list of all tool functions from all connected MCP servers."""
        all_tools = []
        
        for servername in self.sessions:
            tools = self._get_tools_for_server(servername)            
            all_tools.extend(tools)
            
        return all_tools

    def get_agent(self, llm=Settings.llm, verbose=False) -> ReActAgent:
        """Get an agent that can use all tools from all connected MCP servers."""
        tools = self._get_all_tool_functions()
        agent = ReActAgent.from_tools(tools, llm=llm, verbose=True)
        return agent
    
if __name__=='__main__':
    async def main():
        client = MCPClient('mcp_config_windows.json')
        tools = await client.connect_to_server()
        agent = client.get_agent()
        # print(tools)

    asyncio.run(main())
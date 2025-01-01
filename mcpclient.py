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
from typing import List, Dict, Any
from llama_index.llms.openrouter import OpenRouter
from llama_index.core.callbacks import CallbackManager
from tool_callback_handler import ToolCallbackHandler
from mcp_connection import MCPConnection
class MCPClient:
    def __init__(self, config_path='./mcp_config.json'):
        self.server_params_dict = self._load_config(config_path)
        self.sessions = {}  # Track connection instances by server name
        
    @staticmethod
    def _load_config(config_path: str) -> Dict[str, StdioServerParameters]:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        server_params_dict = {}
        server_dict = config.get('mcpServers', {})
        
        for item, server_config in server_dict.items():
            command = server_config.get('command')
            args = server_config.get('args', [])
            env = server_config.get('env')
            
            print(command, args, env)
            server_params = StdioServerParameters(command=command,
                                               args=args,
                                               env=env)
            server_params_dict[item] = server_params
        
        return server_params_dict

    async def _execute_with_session(self, servername: str, operation):
        """Execute an operation with a persistent session"""
        server_params = self.server_params_dict[servername]
        session = await MCPConnection.get_session(server_params)
        return await operation(session)
        

    async def _get_tools_for_server(self, servername: str) -> List[FunctionTool]:
        """Get a list of tools for a specific MCP server."""
        async def get_tools(session):
            nextCursor, tools_tuple = await session.list_tools()
            tools: List[Tool] = tools_tuple[1]
            
            tool_functions = []
            for tool in tools:
                def create_tool_call_fn(tool=tool):
                    async def _call_tool(**kwargs):
                        async def tool_operation(session):
                            return await session.call_tool(tool.name, kwargs)
                        return await self._execute_with_session(servername, tool_operation)
                    return _call_tool
                
                llama_index_tool = FunctionTool.from_defaults(
                    async_fn=create_tool_call_fn(),
                    name=tool.name,
                    description=tool.description
                )
                tool_functions.append(llama_index_tool)
            
            return tool_functions
        
        return await self._execute_with_session(servername, get_tools)

    async def _get_all_tool_functions(self) -> List[FunctionTool]:
        """Get a list of all tool functions from all connected MCP servers."""
        all_tools = []
        for servername in self.server_params_dict:
            tools = await self._get_tools_for_server(servername)
            all_tools.extend(tools)
        return all_tools

    async def get_agent(self, llm=None, callback_manager=None, verbose=False) -> ReActAgent:
        """Get an agent that can use all tools from all connected MCP servers."""
        if not llm:
            llm = self.llm
        
        tools = await self._get_all_tool_functions()
        agent = ReActAgent.from_tools(tools, llm=llm, callback_manager=callback_manager, verbose=verbose)
        return agent

    async def cleanup(self):
        """Clean up all connections when done"""
        await MCPConnection.close()
    

if __name__=='__main__':
    client = MCPClient('mcp_config_windows.json')
    import nest_asyncio
    nest_asyncio.apply()
    async def main():
        tool_handler = ToolCallbackHandler()
        callback_manager = CallbackManager([tool_handler])
        gpt_4o_mini = OpenRouter('anthropic/claude-3.5-sonnet')

        agent = await client.get_agent(
            llm=gpt_4o_mini,
            callback_manager=callback_manager
        )
        
        response = await agent.achat("Call list allowed directories tool, then call list_directory, then summarize the results.")
        
        print("Agent Response:", response)
        # print("\nTool Outputs:", tool_handler.tool_outputs)
    
    import asyncio
    asyncio.run(main())

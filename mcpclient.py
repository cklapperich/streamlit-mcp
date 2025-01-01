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
from llama_index.llms.openrouter import OpenRouter

class MCPClient:
    def __init__(self, config_path='./mcp_config.json'):
        self.server_params_dict = self._load_config(config_path)
        
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
        """Execute an operation with a fresh session"""
        server_params = self.server_params_dict[servername]
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
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

    async def get_agent(self, llm=None, verbose=False) -> ReActAgent:
        """Get an agent that can use all tools from all connected MCP servers."""
        if not llm:
            llm = self.llm

        tools = await self._get_all_tool_functions()
        agent = ReActAgent.from_tools(tools, llm=llm, verbose=verbose)
        return agent

    async def get_agent(self, llm=None, verbose=False) -> ReActAgent:
        if not llm:
            llm = self.llm

        tools = await self._get_all_tool_functions()
        agent = ReActAgent.from_tools(tools, llm=llm, verbose=verbose)
        return agent

if __name__=='__main__':
    client = MCPClient('mcp_config_windows.json')
    import nest_asyncio
    nest_asyncio.apply()

    async def main():
        gpt_4o_mini = OpenRouter('anthropic/claude-3.5-sonnet')
        tools:List[FunctionTool] = await client._get_all_tool_functions()

        # # call tools manually:
        # tool = tools[0]
        # response = tool(path='C:\\Users\\cklap\\streamlit-mcp\\snowflake_docs')
        # print(response)

        agent = await client.get_agent(llm=gpt_4o_mini)
        response = await agent.achat("call the list_directory tool to list some files in a directory, as a test. If you get an error or exception, reproduce the EXACT error message as accurately as possible.")
        print(response)

    asyncio.run(main())
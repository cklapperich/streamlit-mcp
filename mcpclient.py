import asyncio
import logging
import json
from typing import Dict, Any, Optional, Tuple
from types import TracebackType
import chainlit as cl
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPClient:
    def __init__(self, config_path: str = 'mcp_config.json'):
        self.servers: Dict[str, Any] = {}
        self.sessions: Dict[str, Any] = {}
        self._lock = asyncio.Lock()
        self.logger = logging.getLogger(__name__)
        self.server_configs = self._load_config(config_path)

    @staticmethod
    def _load_config(config_path: str) -> Dict[str, StdioServerParameters]:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        server_params_dict = {}
        for item, server_config in config.get('mcpServers', {}).items():
            server_params = StdioServerParameters(
                command=server_config.get('command'),
                args=server_config.get('args', []),
                env=server_config.get('env')
            )
            server_params_dict[item] = server_params
        
        return server_params_dict

    async def _start_server(self, server_id: str, server_params: StdioServerParameters) -> bool:
        async with self._lock:
            if server_id in self.servers:
                return False
            
            try:
                stdio = stdio_client(server_params)
                read, write = await stdio.__aenter__()
                session = await ClientSession(read, write).__aenter__()
                
                self.servers[server_id] = stdio
                self.sessions[server_id] = session
                return True
            except Exception as e:
                self.logger.error(f"Failed to start server {server_id}: {str(e)}")
                await self._cleanup_server(server_id)
                raise

    async def _cleanup_server(self, server_id: str) -> None:
        async with self._lock:
            if server_id in self.sessions:
                session = self.sessions[server_id]
                del self.sessions[server_id]
                await session.__aexit__(None, None, None)

            if server_id in self.servers:
                stdio = self.servers[server_id]
                del self.servers[server_id]
                await stdio.__aexit__(None, None, None)

    async def execute_tool(self, name, parameters_dict=None)-> Tuple[str, str]:
        """Execute a tool by name and parameters"""
        if not parameters_dict:
            parameters_dict = {}

        # Find the server that has the tool
        names = name.split('_')
        server_id = names[0]
        tool_name = '_'.join(names[1:])

        # Execute the tool
        session = self.sessions[server_id]
        response = await session.call_tool(tool_name, parameters_dict)
        meta, content_list, isError = response.meta, response.content, response.isError

        if len(content_list) == 1:
            result = content_list[0].text
            type = content_list[0].type
        else:
            raise ValueError("in mcpclient.execute_tool, a multipart content list was returned, which is not allowed currently. Response from call: ", 
                             content_list)
                
        """ FUNCTION RESPONSE STRUCTURE
        meta=None content=[TextContent(type='text', text='Allowed directories:\nc:\\users\\cklap\\streamlit-mcp\\snowflake_docs')] isError=False
        """
        return result, type
    
    async def list_available_tools(self) -> list[Dict[str, Any]]:
        """List all available tools across all servers in OpenAI function format"""
        tools = []
        for server_id, session in self.sessions.items():
            meta, next_cursor, tools_tuple = await session.list_tools()

            server_tools = tools_tuple[1]
            # example tool object in the server tools list:
            """
            [Tool(name='read_file', description='Read the complete contents of a file from the file system. Handles various text encodings and provides detailed error messages if the file cannot be read. Use this tool when you need to examine the contents of a single file. Only works within allowed directories.', inputSchema={'type': 'object', 'properties': {'path': {'type': 'string'}}, 'required': ['path'], 'additionalProperties': False, ...]
            """
            for tool in server_tools:
                # Convert MCP tool schema to OpenAI function format
                function_def = {
                    "type": "function",
                    "function": {
                        "name": f"{server_id}_{tool.name}",  # Prefix with server_id to avoid name conflicts
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    }
                }
                
                tools.append(function_def)
        
        return tools

    async def __aenter__(self) -> 'MCPClient':
        # Start all servers
        for server_id, params in self.server_configs.items():
            success = await self._start_server(server_id, params)
            if not success:
                self.logger.warning(f"Failed to start server {server_id}")
        
        if not self.sessions:
            raise RuntimeError("No servers could be started successfully")
        
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType]
    ) -> None:
        server_ids = list(self.servers.keys())
        for server_id in server_ids:
            await self._cleanup_server(server_id)

import pytest
import json
from unittest.mock import Mock, patch, AsyncMock
from mcpclient import MCPClient

@pytest.fixture
def mcp_config():
    return {
        "mcpServers": {
            "filesystem": {
                "command": "node",
                "args": ["server.js", "path1", "path2"]
            }
        }
    }

@pytest.fixture
def mock_tool():
    return Mock(
        name='read_file',
        description='Read the complete contents of a file from the file system.',
        input_schema=json.dumps({
            'type': 'object',
            'properties': {
                'path': {'type': 'string'}
            },
            'required': ['path'],
            'additionalProperties': False
        })
    )

@pytest.mark.asyncio
async def test_load_config(tmp_path):
    # Create temporary config file
    config_file = tmp_path / "test_config.json"
    config_file.write_text(json.dumps({"mcpServers": {"test": {"command": "test"}}}))
    
    client = MCPClient()
    config = client._load_config(str(config_file))
    
    assert isinstance(config, dict)
    assert "test" in config
    assert config["test"].command == "test"

@pytest.mark.asyncio
async def test_connect_to_server(mock_tool):
    client = MCPClient()
    
    mock_session = AsyncMock()
    mock_session.initialize = AsyncMock()
    # Mock the list_tools response with a tuple containing metadata, cursor, and tools list
    mock_session.list_tools = AsyncMock(return_value=(Mock(), None, [mock_tool]))
    
    with patch('mcpclient.stdio_client', new_callable=AsyncMock) as mock_stdio_client:
        mock_stdio_client.return_value = (Mock(), Mock())
        with patch('mcpclient.ClientSession', return_value=mock_session):
            server_config = {
                "command": "test",
                "args": [],
                "env": {}
            }
            
            await client._start_server("test_server", server_config)
            tools = await client.list_available_tools()
            
            assert mock_session.initialize.called
            assert mock_session.list_tools.called
            assert len(tools) == 1
            assert tools[0]["function"]["name"] == "test_server.read_file"
            assert "description" in tools[0]["function"]
            assert "parameters" in tools[0]["function"]

@pytest.mark.asyncio 
async def test_cleanup():
    client = MCPClient()
    
    # Mock servers and sessions
    client.servers = {"test_server": AsyncMock()}
    client.sessions = {"test_server": AsyncMock()}
    
    # Add __aexit__ mocks
    client.servers["test_server"].__aexit__ = AsyncMock()
    client.sessions["test_server"].__aexit__ = AsyncMock()
    
    await client._cleanup_server("test_server")
    
    assert client.sessions["test_server"].__aexit__.called
    assert client.servers["test_server"].__aexit__.called
    assert "test_server" not in client.sessions
    assert "test_server" not in client.servers

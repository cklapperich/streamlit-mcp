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
def mock_anthropic():
    mock = Mock()
    mock.messages.create.return_value = Mock(
        content=[
            Mock(type='text', text='Test response'),
            Mock(
                type='tool_use',
                name='test_tool',
                input={'param': 'value'},
                text='Tool response'
            )
        ]
    )
    return mock

@pytest.mark.asyncio
async def test_load_config(tmp_path):
    # Create temporary config file
    config_file = tmp_path / "test_config.json"
    config_file.write_text(json.dumps({"mcpServers": {"test": {"command": "test"}}}))
    
    client = MCPClient()
    config = client.load_config(str(config_file))
    
    assert isinstance(config, dict)
    assert "test" in config
    assert config["test"]["command"] == "test"

@pytest.mark.asyncio
async def test_connect_to_server():
    client = MCPClient()
    
    mock_session = AsyncMock()
    mock_session.initialize = AsyncMock()
    mock_session.list_tools = AsyncMock(return_value=Mock(tools=[]))
    
    with patch('mcpclient.stdio_client', new_callable=AsyncMock) as mock_stdio_client:
        mock_stdio_client.return_value = (Mock(), Mock())
        with patch('mcpclient.ClientSession', return_value=mock_session):
            server_config = {
                "command": "test",
                "args": [],
                "env": {}
            }
            
            tools = await client.connect_to_server(server_config)
            
            assert mock_session.initialize.called
            assert mock_session.list_tools.called

@pytest.mark.asyncio
async def test_process_query(mock_anthropic):
    client = MCPClient()
    client.session = AsyncMock()
    client.session.list_tools.return_value = Mock(tools=[])
    client.session.call_tool.return_value = Mock(content="Tool result")
    client.anthropic = mock_anthropic
    
    result = await client.process_query("Test query")
    
    assert isinstance(result, str)
    assert client.session.list_tools.called
    assert mock_anthropic.messages.create.called

@pytest.mark.asyncio 
async def test_cleanup():
    client = MCPClient()
    client.exit_stack = AsyncMock()
    
    await client.cleanup()
    
    assert client.exit_stack.aclose.called
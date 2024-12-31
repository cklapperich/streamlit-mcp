# app.py
import streamlit as st
from mcp_client import MCPClient
import asyncio
from typing import Dict

def init_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'client' not in st.session_state:
        st.session_state.client = None
    if 'server_connected' not in st.session_state:
        st.session_state.server_connected = False
    if 'server_config' not in st.session_state:
        st.session_state.server_config = None

async def connect_to_server(server_config: Dict):
    """Connect to the MCP server and store client in session state"""
    try:
        client = MCPClient()
        tools = await client.connect_to_server(server_config)
        st.session_state.client = client
        st.session_state.server_connected = True
        return [tool.name for tool in tools.tools]
    except Exception as e:
        st.error(f"Failed to connect to server: {str(e)}")
        return None

async def process_message(message: str):
    """Process a message through the MCP client"""
    try:
        response = await st.session_state.client.process_query(message)
        return response
    except Exception as e:
        return f"Error processing message: {str(e)}"

def main():
    st.title("MCP Chat Assistant")
    init_session_state()

    # Server connection section
    with st.sidebar:
        st.header("Server Connection")
        config_path = st.text_input("Config File Path", 
                                  placeholder="Enter path to config.json")
        
        if st.button("Load Configuration"):
            if config_path:
                try:
                    st.session_state.server_config = MCPClient.load_config(config_path)
                    st.success("Configuration loaded!")
                    st.write("Available servers:", list(st.session_state.server_config.keys()))
                except Exception as e:
                    st.error(f"Failed to load configuration: {str(e)}")

        if st.session_state.server_config:
            server_name = st.selectbox(
                "Select Server",
                options=list(st.session_state.server_config.keys())
            )
            
            if st.button("Connect"):
                server_config = st.session_state.server_config[server_name]
                tools = asyncio.run(connect_to_server(server_config))
                if tools:
                    st.success(f"Connected to {server_name}!")
                    st.write("Available tools:", tools)

    # Chat interface
    st.header("Chat")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Enter your message"):
        if not st.session_state.server_connected:
            st.error("Please connect to a server first")
            return

        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get bot response
        with st.chat_message("assistant"):
            response = asyncio.run(process_message(prompt))
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
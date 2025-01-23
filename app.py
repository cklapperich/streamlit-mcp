import chainlit as cl
from typing import List, Dict, Any
from mcpclient import MCPClient
import httpx
import json
from dotenv import load_dotenv
import os
from clients import OpenRouterClient
import ast

# Load environment variables from .env file
load_dotenv()

MCP_CONFIG_FILE = 'mcp_config_windows.json'

@cl.step(type="tool")
async def call_tool(tool_call, message_history):
    function_name = tool_call['function']['name']
    dict_args = tool_call['function']['arguments']
    print("DEBUG DICT ARGS FOR TOOL CALL: ", dict_args)
    if dict_args:
        try:
            arguments = ast.literal_eval(dict_args)
        except:
            arguments = {}
            print(f"DEBUG | FAILED TO PARSE ARGS: '{dict_args}'")
    else:
        arguments = {}
    print("DEBUG | PARSED ARGS: ", arguments)

    current_step = cl.context.current_step
    current_step.name = function_name

    current_step.input = arguments
    client = cl.user_session.get("client")
    function_response, response_type = await client.execute_tool(function_name, arguments)
    current_step.output = function_response
    current_step.language = response_type

    return {
            "role": "tool",
            "name": function_name,
            "content": function_response,
            "tool_call_id": tool_call['id'],
           }

async def process_user_message(llm, message_history, tools):
    print('TOOL CALL MESSAGE HISTORY: ')
    print(message_history)
    print('======================')
    response_data =  await llm.chat_completion(
            messages=message_history,
            tools=tools,
            stream=False
        )
    
    if 'choices' in response_data:
        message = response_data['choices'][0]['message']
    else:
        message = response_data
        print("DEBUG RESPONSE DATA: ", response_data)
        raise ValueError("Unexpected response format")
    
    # First handle the LLM response
    message_history.append(message)
    content = message.get('content')
    if content:
        cl.context.current_step.output = content
        await cl.Message(content=content).send()

    # Then process any tool calls
    finish_reason = response_data['choices'][0]['finish_reason']
    for tool_call in message.get('tool_calls',[]):
        if tool_call['type'] == "function":
            tool_response = await call_tool(tool_call, message_history)
            message_history.append(tool_response)

    return message


def init_llm():
    # Initialize OpenRouter client with API key from environment variables
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable is not set")
        
    llm = OpenRouterClient(
        api_key=api_key,
        model="openai/gpt-4o",
    )
    return llm

async def init_mcp_client():
    mcp_client = MCPClient(MCP_CONFIG_FILE)
    await mcp_client.__aenter__()  # This starts all server connections
    return mcp_client

@cl.on_chat_start
async def start():
    try:
        # Initialize MCP client and get available tools
        mcp_client = await init_mcp_client()
        tools = await mcp_client.list_available_tools()  # Now returns list in OpenAI format
        
        # Initialize LLM
        llm = init_llm()
        
        # Store everything in session
        cl.user_session.set("client", mcp_client)
        cl.user_session.set("llm", llm)
        cl.user_session.set("tools", tools)
        
        # Set initial message history with system prompt about available tools
        tools_desc = "\n".join([f"- {t['function']['name']}: {t['function']['description']}" 
                               for t in tools])
        system_prompt = f"""You are a helpful assistant with access to tools."""
        
        cl.user_session.set(
            "message_history",
            [{"role": "system", "content": system_prompt}]
        )
        
    except Exception as e:
        import traceback
        error_details = f"Error during initialization: {str(e)}\n{traceback.format_exc()}"
        print("\nERROR DETAILS:", error_details)
        await cl.Message(content=f"Error during initialization: {str(e)}").send()

MAX_ITER = 5
@cl.on_message
async def run_conversation(message: cl.Message):
    """
    !!! the 'message' being passed in to this func is a cl.message object
    but the response from process_user_message is a dict with keys 'content' and 'tool_calls'
    """
    llm = cl.user_session.get("llm")
    tools = cl.user_session.get("tools")
    message_history = cl.user_session.get("message_history")
    message_history.append({"name": "user", "role": "user", "content": message.content})

    cur_iter = 0

    while cur_iter < MAX_ITER:
        response_dict:dict = await process_user_message(llm, message_history, tools)
        print("RESPONSE DICT: ")
        print(response_dict.get('content'))
        print(response_dict.get('tool_calls'))
        print("=====================")
        
        # Break if there are no tool calls to process (content is already handled)
        if not response_dict.get('tool_calls'):
            break
        
        cur_iter += 1

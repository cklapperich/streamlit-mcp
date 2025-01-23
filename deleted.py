
# No need for a separate execute_tool step since MCPClient.execute_tool already handles steps
async def process_llm_response(messages: list) -> str:
    """Process LLM response with streaming and tool handling"""
    llm = cl.user_session.get("llm")
    client = cl.user_session.get("client")
    current_step = cl.context.current_step
    
    buffer = ""
    tool_call_detected = False
    
    async for chunk in llm.stream_chat(messages):
        if not tool_call_detected and "{{TOOL" in chunk:
            tool_call_detected = True
            # Extract tool call parameters
            start_idx = chunk.find("{{TOOL")
            end_idx = chunk.find("}}", start_idx)
            if end_idx != -1:
                tool_str = chunk[start_idx:end_idx + 2]
                try:
                    # Parse tool call parameters
                    tool_params = json.loads(tool_str.replace("{{TOOL:", "").replace("}}", ""))
                    tool_name = tool_params["name"]  # Will be in format "server_id_tool_name"
                    tool_input = tool_params["input"]
                    
                    # Stream content before tool call
                    await current_step.stream_token(buffer + chunk[:start_idx])
                    
                    # Execute tool (MCPClient handles the step creation)
                    tool_result = await client.execute_tool(tool_name, tool_input)
                    
                    # Stream a newline for formatting
                    await current_step.stream_token("\n")
                    
                    # Reset buffer for after tool call
                    buffer = ""
                    continue
                except Exception as e:
                    await current_step.stream_token(f"\nError processing tool call: {str(e)}\n")
        
        if tool_call_detected:
            # Buffer content until we're past the tool call
            buffer += chunk
            if "}}" in buffer:
                # We've found the end of the tool call, resume normal streaming
                tool_call_detected = False
                end_idx = buffer.find("}}") + 2
                buffer = buffer[end_idx:]
        else:
            # Normal streaming
            await current_step.stream_token(chunk)
    
    # Stream any remaining buffer
    if buffer:
        await current_step.stream_token(buffer)

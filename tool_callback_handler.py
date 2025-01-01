from llama_index.core.callbacks.base_handler import BaseCallbackHandler
from llama_index.core.callbacks.schema import CBEventType
from typing import Optional, Dict, Any, List
from llama_index.core.callbacks.schema import CBEventType, EventPayload

class ToolCallbackHandler(BaseCallbackHandler):
    def __init__(self):
        super().__init__([], [])
        self.tool_outputs = []
        self.current_tool_name = "unknown"

    def _format_tool_output(self, payload):
        """Generic formatter for any tool output"""
        formatted = f"\n📤 Tool Output: {self.current_tool_name}\n"
        formatted += "=" * (13 + len(self.current_tool_name)) + "\n"
        
        output = payload.get('function_call_response')
        if output:
            # The output is a string containing a TextContent object representation
            # Let's parse out just the actual text content
            if "TextContent" in output:
                # Extract the text between text=' and ']
                start = output.find("text='") + 6
                end = output.find("')] isError")
                if start > 5 and end > 0:  # Make sure we found both markers
                    actual_text = output[start:end]
                    # Properly handle escaped newlines
                    actual_text = actual_text.replace('\\n', '\n')
                    formatted += actual_text
            else:
                formatted += output
        
        return formatted
    
    def on_event_start(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        parent_id: str = "",
        **kwargs: Any,
    ) -> str:
        if event_type == CBEventType.FUNCTION_CALL and payload:
            self.current_tool_name = payload.get('tool').name
            print(f"\n🔧 Calling: {self.current_tool_name}")
        return event_id

    def on_event_end(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        **kwargs: Any,
    ) -> None:
        if event_type == CBEventType.FUNCTION_CALL and payload:
            formatted_output = self._format_tool_output(payload)
            print(formatted_output)
            
            self.tool_outputs.append({
                "tool": self.current_tool_name,
                "output": formatted_output
            })

    def start_trace(self, trace_id: Optional[str] = None) -> None:
        pass

    def end_trace(
        self,
        trace_id: Optional[str] = None,
        trace_map: Optional[Dict[str, List[str]]] = None,
    ) -> None:
        self.current_tool_name = "unknown"
from typing import List, Dict, Any
import json 
import httpx
"""
type Response = {
  id: string;
  // Depending on whether you set "stream" to "true" and
  // whether you passed in "messages" or a "prompt", you
  // will get a different output shape
  choices: (NonStreamingChoice | StreamingChoice | NonChatChoice)[];
  created: number; // Unix timestamp
  model: string;
  object: "chat.completion" | "chat.completion.chunk";

  system_fingerprint?: string; // Only present if the provider supports it

  // Usage data is always returned for non-streaming.
  // When streaming, you will get one usage object at
  // the end accompanied by an empty choices array.
  usage?: ResponseUsage;
};
"""
"""
SAMPLE RESPONSE: 
 {'id': 'gen-1737316577-Fzz7IrH8LF410nPfztv8', 'provider': 'Amazon Bedrock', 'model': 'anthropic/claude-3.5-sonnet', 'object': 'chat.completion', 'created': 1737316577, 'choices': 
 
 [{'logprobs': None, 'finish_reason': 'tool_calls', 'native_finish_reason': 'tool_calls', 'index': 0, 'message': {'role': 'assistant', 'content': "I'll help you test a tool call. Let's use one of the simplest tools available - `filesystem_list_allowed_directories` since it doesn't require any parameters. This will show us which directories we have access to work with.", 'refusal': None,'tool_calls':     
 
         [{'id': 'tooluse_7EA9yBd7TriESo59Vozndg', 'index': 0, 'type': 'function', 'function': {'name': 'filesystem_list_allowed_directories', 'arguments': ''}}]}}], 'usage': {'prompt_tokens': 1498, 'completion_tokens': 91, 'total_tokens': 1589}}
 """
class OpenRouterClient:
    def __init__(self, api_key: str, model: str = "anthropic/claude-3.5-sonnet"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1"
        
    async def chat_completion(self, messages: List[Dict[str, Any]], tools=None, stream=False):
        async with httpx.AsyncClient() as client:
            request_body = {
                "model": self.model,
                "messages": messages,
                "stream": False  # Always set to False to disable streaming
            }
            
            # Add tools to request if provided
            if tools:
                request_body["tools"] = tools
                request_body["tool_choice"] = "auto"  # Let the model decide when to use tools
            
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "HTTP-Referer": "http://localhost:8000",
                    "X-Title": "Local Testing"
                },
                json=request_body,
                timeout=60.0
            )
            response.raise_for_status()

            response_data = response.json()
            return response_data
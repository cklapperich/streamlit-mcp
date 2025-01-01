import time
import logging
import contextlib
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from typing import Optional
from functools import wraps

def async_timer(func):
   @wraps(func)
   async def wrapper(*args, **kwargs):
       start = time.perf_counter()
       try:
           result = await func(*args, **kwargs)
           elapsed = time.perf_counter() - start
           logging.info(f"{func.__name__} took {elapsed:.2f} seconds")
           return result
       except Exception as e:
           elapsed = time.perf_counter() - start
           logging.error(f"{func.__name__} failed after {elapsed:.2f} seconds with error: {str(e)}")
           raise
   return wrapper

class MCPConnection:
   _instance: Optional[ClientSession] = None
   _read = None
   _write = None
   _client = None
   _instrumentation_enabled = False

   @classmethod
   def enable_instrumentation(cls, enabled: bool = True):
       """Toggle instrumentation"""
       cls._instrumentation_enabled = enabled
       if enabled:
           logging.basicConfig(level=logging.INFO)

   @classmethod
   @async_timer
   async def get_session(cls, server_params: StdioServerParameters) -> ClientSession:
       """Get or create session, validating connection"""
       if cls._instance is None:
           logging.info("Creating new session")
           await cls._create_session(server_params)
       else:
           try:
               logging.info("Testing existing session")
               await cls._instance.list_tools()
               logging.info("Using existing session")
           except Exception:
               logging.info("Session dead, recreating")
               await cls.close()
               await cls._create_session(server_params)
               
       return cls._instance

   @classmethod
   @async_timer 
   async def _create_session(cls, server_params: StdioServerParameters):
       """Create a new session"""
       start = time.perf_counter()
       
       logging.info("Opening stdio client")
       cls._client = stdio_client(server_params)
       cls._read, cls._write = await cls._client.__aenter__()
       stdio_time = time.perf_counter() - start
       logging.info(f"stdio client setup took {stdio_time:.2f} seconds")

       try:
           logging.info("Creating client session")
           session_start = time.perf_counter()
           cls._instance = await ClientSession(cls._read, cls._write).__aenter__()
           session_time = time.perf_counter() - session_start
           logging.info(f"Client session creation took {session_time:.2f} seconds")

           logging.info("Initializing session")
           init_start = time.perf_counter()
           await cls._instance.initialize()
           init_time = time.perf_counter() - init_start
           logging.info(f"Session initialization took {init_time:.2f} seconds")

       except Exception:
           if cls._client:
               with contextlib.suppress(Exception):
                   await cls._client.__aexit__(None, None, None)
           raise

   @classmethod
   @async_timer
   async def close(cls):
       """Clean shutdown"""
       if cls._instance:
           with contextlib.suppress(Exception):
               await cls._instance.aclose()
           cls._instance = None
       
       if cls._client:
           with contextlib.suppress(Exception):
               await cls._client.__aexit__(None, None, None)
           cls._client = None
           cls._read = None
           cls._write = None
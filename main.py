import asyncio
from dotenv import load_dotenv
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.tools import load_mcp_tools


load_dotenv()
llm = ChatOpenAI()

stdio_server_params = StdioServerParameters(
    transport="stdio",
    server_name="mcp-crash-course",
    server_description="A simple MCP server for the crash course",
    command="python3",
    args=["/Users/raviiyer/dev/mcp-crash-course/servers/math_server.py"],
)

async def main():
    print("Hello from mcp-crash-course!")


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
from dotenv import load_dotenv
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent


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
    async with stdio_client(stdio_server_params) as (read, write): #create stdio context manager with read+write objects
        async with ClientSession(read_stream=read, write_stream=write) as session:
            await session.initialize()
            print("Session initialized")
            tools = await load_mcp_tools(session) #await session.list_tools()
            print(tools)
            #agent = create_react_agent(llm, tools)
            # tools = load_mcp_tools(session)
            # llm_with_tools = llm.bind_tools(tools)
            # response = llm_with_tools.invoke("What is 2 + 2?")
            # print(response)


if __name__ == "__main__":
    asyncio.run(main())

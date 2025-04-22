import asyncio
import logging
from dotenv import load_dotenv
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI

from langgraph.prebuilt import create_react_agent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Disable LangSmith tracking
# os.environ["LANGCHAIN_TRACING_V2"] = "true"

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
    try:
        logger.debug("Starting stdio client")
        async with stdio_client(stdio_server_params) as (read, write):
            logger.debug("Stdio client started, initializing session")
            async with ClientSession(read_stream=read, write_stream=write) as session:
                await session.initialize()
                logger.info("Session initialized")
                tools = await load_mcp_tools(session)
                # logger.debug(f"Loaded tools: {tools}")
                agent = create_react_agent(llm, tools)
                # logger.debug("Created agent")

                result = await agent.ainvoke({"messages": [HumanMessage(content="What is 100 + 4 / 3?")]})
                logger.info(f"Result: {result['messages'][-1].content}")

    except Exception as e:
        logger.exception("An error occurred:")
        raise

if __name__ == "__main__":
    asyncio.run(main())

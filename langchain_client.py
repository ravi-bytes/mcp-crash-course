import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()
llm = ChatOpenAI()


async def main():
    # print("Hello langchain MCP");
    async with MultiServerMCPClient(
        {
            "math": {
                "command": "python3",
                "args": ["/Users/raviiyer/dev/mcp-crash-course/servers/math_server.py"],
            },
            "weather": {
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            },
        }
    ) as client:
        # print(client.get_tools())
        agent = create_react_agent(llm, client.get_tools())
        # result = await agent.ainvoke({"messages": [HumanMessage(content="What is 2 + 2?")]})
        result = await agent.ainvoke(
            {
                "messages": [
                    HumanMessage(content="What is the weather in San Francisco?")
                ]
            }
        )
        print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())

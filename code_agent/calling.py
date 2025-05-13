import os
from typing import Any

from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import Tool,tool
from langchain_openai import ChatOpenAI
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
    create_tool_calling_agent
)
from langchain_community.tools.tavily_search import TavilySearchResults
load_dotenv()

@tool
def multiply(a: int, b: int) -> int:
    """Multiplies two numbers."""
    return a * b

if __name__ == "__main__":
    print("Hello Tool Calling")
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant."),
            ("user", "{input}"),
            ("placeholder","{agent_scratchpad}"),
        ]
    )
    tools = [
        TavilySearchResults(tavily_api_key=os.getenv("TAVILY_API_KEY")),
        multiply
    ]
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    agent = create_tool_calling_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    res = agent_executor.invoke({"input": "what is the result of 2*3?"})
    print(res)
import os
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from dotenv import load_dotenv
from engine.search import get_profile_url_tavily

load_dotenv()

def lookup(name: str) -> str:
    llm = ChatOpenAI(
        model="gpt-3.5-turbo", temperature=0, api_key=os.getenv("OPENAI_API_KEY")
    )
    template = """
        Give the name {name_of_person} I want you to find a link to their Twitter profile page, and extract from it their username.
        In your final answer, please only include the username without any additional text or explanation which extracted from: https://x.com/USERNAME
        """
    
    tools_for_agent = [
        Tool(
            name="Crawl Google for Twitter profile page",  # name of the tool
            func=get_profile_url_tavily,  # function to call
            description="useful for when you need get the Twitter Page URL",  # description of the tool SUPER IMPORTANT
        )
    ]

    promp_template = PromptTemplate(input_variables=["name_of_person"], template=template)
    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(
        llm=llm,
        tools=tools_for_agent,
        prompt=react_prompt,
    )  # accept the tools and the prompt (like recipe)
    
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools_for_agent,
        verbose=True,
        handle_parsing_errors=True,
    )  # have a responsible to run the agent

    result = agent_executor.invoke(
        input={"input": promp_template.format(name_of_person=name)}
    )
    twitter_username = result["output"]
    return twitter_username
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from engine.search import get_profile_url_tavily


load_dotenv()

# 
def lookup(name: str) -> str:
    llm = ChatOpenAI(
        model="gpt-3.5-turbo", temperature=0, api_key=os.getenv("OPENAI_API_KEY")
    )

    template = """
        Give the full name {name_of_person} I want you to get it me a link to their Linkedin profile page.
        Your name should contain only a URL
    """
    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )
    tool_for_agent =[
        Tool(
            name="Crawl Google 4 linkedin profile page", # name of the tool
            func=get_profile_url_tavily, # function to call
            description="useful for when you need get the Linkedin Page URL", # description of the tool SUPER IMPORTANT
        )
    ]
    react_prompt = hub.pull("hwchase17/react")
    
    agent = create_react_agent(
        llm=llm,
        tools=tool_for_agent,
        prompt=react_prompt,
    ) #accept the tools and the prompt (like recipe)
    
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tool_for_agent,
        verbose=True,
        handle_parsing_errors=True,
    ) # have a responsible to run the agent

    result = agent_executor.invoke(
        input={"input":prompt_template.format(name_of_person=name)}
    )

    linkedin_profile_url = result["output"]
    return linkedin_profile_url


if __name__ == "__main__":
    name = "Eden Marco"
    linkedin_profile_url = lookup(name)
    print(linkedin_profile_url)
import os
from dotenv import load_dotenv
from template.prompt import summary_template
from langchain_openai import ChatOpenAI
from craw.linkedin import scrape_linkedin_profile_with_proxy
from agent.linkedin_lookup_agent import lookup as linkedin_lookup_agent




def ice_break_with(name:str)-> str:
    linkedin_username = linkedin_lookup_agent(name)
    linkedin_data = scrape_linkedin_profile_with_proxy(linkedin_username, mock_proxy=True)
    
    llm = ChatOpenAI(
        model="gpt-3.5-turbo", temperature=0, api_key=os.getenv("OPENAI_API_KEY")
    )
    summary_prompt_temaplate = summary_template()
    chain = summary_prompt_temaplate | llm
    result = chain.invoke(input={"information": linkedin_data})
    return result

if __name__ == "__main__":
    load_dotenv()
    result = ice_break_with("Eden Marco")
    print(result)
   

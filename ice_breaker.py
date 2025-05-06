import os
from dotenv import load_dotenv
from template.prompt import summary_template
from langchain_openai import ChatOpenAI
from craw.linkedin import scrape_linkedin_profile_with_proxy
from agent.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agent.tweets_lookup_agent import lookup as twitter_lookup_agent
from craw.twitter import  scrape_user_tweets_mook



def ice_break_with(name:str)-> str:
    linkedin_username = linkedin_lookup_agent(name)
    linkedin_data = scrape_linkedin_profile_with_proxy(linkedin_username, mock_proxy=True)
    

    twitter_username = twitter_lookup_agent(name=name)
    tweets = scrape_user_tweets_mook(username=twitter_username)
    llm = ChatOpenAI(
        model="gpt-3.5-turbo", temperature=0, api_key=os.getenv("OPENAI_API_KEY")
    )
    summary_prompt_temaplate = summary_template()
    chain = summary_prompt_temaplate | llm
    result = chain.invoke(input={"information": linkedin_data, "twitter_post":tweets})
    return result

if __name__ == "__main__":
    load_dotenv()
    result = ice_break_with("Eden Marco")
    print(result)
   

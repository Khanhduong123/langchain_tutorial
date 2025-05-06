from langchain_core.prompts import PromptTemplate

def summary_template() -> str:
    summary_template = """
        Give the Linkedin informattion {information}, and twitter post {twitter_post} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about them

        Use the both information from the Linkedin and Twitter to create a summary.
    """

    return  PromptTemplate(
        input_variables=["information","twitter_post"], template=summary_template
    )
    
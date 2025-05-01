from langchain_core.prompts import PromptTemplate

def summary_template() -> str:
    summary_template = """
        Give the Linkedin informattion {information} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about them
    """

    return  PromptTemplate(
        input_variables=["information"], template=summary_template
    )
    
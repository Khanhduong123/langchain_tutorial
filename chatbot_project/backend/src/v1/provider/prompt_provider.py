from langchain import hub

def get_retrieval_qa_prompt():
    return hub.pull("langchain-ai/retrieval-qa-chat")

def get_rephraser_prompt():
    return hub.pull("langchain-ai/chat-langchain-rephrase")
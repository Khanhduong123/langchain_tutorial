
from backend.src.v1.config.config import INDEX_NAME
from typing import List, Dict, Any
from langchain_pinecone import PineconeVectorStore
from backend.src.v1.provider.prompt_provider import retrieval_qa_prompt_template, result_parser
from backend.src.v1.provider.embedding_provider import get_embedding_model
from backend.src.v1.provider.openai_chat_provider import get_chat_model
from langchain.schema import HumanMessage, AIMessage, BaseMessage


def convert_dict_to_messages(history: List[Dict[str, str]]) -> List[BaseMessage]:
    messages = []
    for item in history:
        if item["role"] == "user":
            messages.append(HumanMessage(content=item["content"]))
        elif item["role"] == "assistant":
            messages.append(AIMessage(content=item["content"]))
    return messages

def run_llm(query: str, chat_history: List[Dict[str, Any]] = []):
    embeddings = get_embedding_model()
    docsearch = PineconeVectorStore( index_name= INDEX_NAME,embedding=embeddings)
    chat = get_chat_model()
    retriever = docsearch.as_retriever(search_kwargs={"k": 3})
    contexts = retriever.invoke(query)
    retrieval_qa_prompt = retrieval_qa_prompt_template()
    chain = retrieval_qa_prompt | chat | result_parser
    result = chain.invoke({"chat_history":chat_history,"question": query, "context": contexts})

    if result.answer.strip().lower() == "no answer":
        contexts = []

    return result, contexts
    

import os
from dotenv import load_dotenv
from typing import List, Dict, Any
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from backend.prompt import retrieval_qa_prompt_template
from backend.output_parser import result_parser

# from prompt import retrieval_qa_prompt_template
# from output_parser import result_parser
load_dotenv()
def run_llm(query: str, chat_history: List[Dict[str, Any]] = []):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small",openai_api_key=os.getenv("OPENAI_API_KEY"))
    docsearch = PineconeVectorStore( index_name="langchain-doc-index",embedding=embeddings)
    chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
    retriever = docsearch.as_retriever(search_kwargs={"k": 3})
    contexts = retriever.invoke(query)
    retrieval_qa_prompt = retrieval_qa_prompt_template()
    chain = retrieval_qa_prompt | chat | result_parser
    result = chain.invoke({"chat_history":chat_history,"question": query, "context": contexts})

    if result.answer.strip().lower() == "no answer":
        contexts = []
    
    return result, contexts


if __name__ == "__main__":
    query = "What is Pinecone?"
    result = run_llm(query)
    print(result.answer)
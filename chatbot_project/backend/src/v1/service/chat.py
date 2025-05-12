import os
from backend.src.v1.config.config import OPENAI_API_KEY, INDEX_NAME,MODEL_EMBEDDING,MODEL_CHAT
from typing import List, Dict, Any
from langchain.chains.retrieval import create_retrieval_chain
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import create_history_aware_retriever



def run_llm(query: str, chat_history: List[Dict[str, Any]] = []):
    embeddings = OpenAIEmbeddings(model=MODEL_EMBEDDING,openai_api_key=OPENAI_API_KEY)
    docsearch = PineconeVectorStore( index_name= INDEX_NAME,embedding=embeddings)
    chat = ChatOpenAI(model=MODEL_CHAT, temperature=0, openai_api_key=OPENAI_API_KEY)
    retrieval_qa_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    stuff_documents_chain = create_stuff_documents_chain(chat, retrieval_qa_prompt)

    rephraser_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")
    history_aware_retrieval = create_history_aware_retriever(
        llm = chat,
        retriever=docsearch.as_retriever(),
        prompt = rephraser_prompt
    )
    
    qa = create_retrieval_chain(
        retriever=history_aware_retrieval,
        combine_docs_chain=stuff_documents_chain,
    )

    result = qa.invoke({"input": query, "chat_history": chat_history})
    final_result = {
        "query": result['input'],
        "answer": result['answer'],
        "source_documents": result['context']
    }
    return final_result

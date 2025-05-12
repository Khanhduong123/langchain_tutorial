
from backend.src.v1.config.config import INDEX_NAME
from typing import List, Dict, Any
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_pinecone import PineconeVectorStore
from langchain.chains import create_history_aware_retriever
from backend.src.v1.provider.prompt_provider import get_retrieval_qa_prompt, get_rephraser_prompt
from backend.src.v1.provider.embedding_provider import get_embedding_model
from backend.src.v1.provider.openai_chat_provider import get_chat_model


def run_llm(query: str, chat_history: List[Dict[str, Any]] = []):
    embeddings = get_embedding_model()
    docsearch = PineconeVectorStore( index_name= INDEX_NAME,embedding=embeddings)
    chat = get_chat_model()
    
    retrieval_qa_prompt = get_retrieval_qa_prompt()
    stuff_documents_chain = create_stuff_documents_chain(chat, retrieval_qa_prompt)
    rephraser_prompt = get_rephraser_prompt()
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

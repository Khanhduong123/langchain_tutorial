import os
from dotenv import load_dotenv
from langchain.chains.retrieval import create_retrieval_chain
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
load_dotenv()
def run_llm(query: str):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small",openai_api_key=os.getenv("OPENAI_API_KEY"))
    docsearch = PineconeVectorStore( index_name="langchain-doc-index",embedding=embeddings)
    chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
    retrieval_qa_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    stuff_documents_chain = create_stuff_documents_chain(chat, retrieval_qa_prompt)
    qa = create_retrieval_chain(
        retriever=docsearch.as_retriever(),
        combine_docs_chain=stuff_documents_chain,
    )

    result = qa.invoke({"input": query})
    final_result = {
        "query": result['input'],
        "answer": result['answer'],
        "source_documents": result['source_documents']
    }
    return final_result

if __name__ == "__main__":
    query = "What is Pinecone?"
    result = run_llm(query)
    print(result['answer'])
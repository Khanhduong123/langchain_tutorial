import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain import hub
from langchain.schema.runnable import RunnablePassthrough, RunnableMap
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
load_dotenv()


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

if __name__ == "__main__":
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small",openai_api_key=os.getenv("OPENAI_API_KEY"))
    llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=os.getenv("OPENAI_API_KEY"), temperature=0.0)
    query =  "What is Pinecone in machine learning?"

    vectorstore = PineconeVectorStore(embedding=embeddings, index_name=os.getenv("INDEX_NAME"))
    retriver = vectorstore.as_retriever(search_kwargs={"k": 3})
    # retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    # combine_docs_chain = create_stuff_documents_chain(llm=llm, prompt=retrieval_qa_chat_prompt)
    # retrieval_chain = create_retrieval_chain(retriever=vectorstore.as_retriever(), combine_docs_chain=combine_docs_chain)
    

    template = """
    Using the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Use three sentences maximum and keep the answer as concise as possible.
    Always say "thanks for asking!" at the end of the answer.

    {context}

    Question: {question}
    Helpful Answer:
"""
    custom_rag_prompt = PromptTemplate.from_template(template)

    rag_chain = (
       {
            "context": retriver | format_docs,
            "question": RunnablePassthrough()
        }
        | custom_rag_prompt
        | llm
    )
    result = rag_chain.invoke(query)
    print(result.content)


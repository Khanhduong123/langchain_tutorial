import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore

load_dotenv()
def ingest_docs():
    loader= TextLoader("./data/mediumblog1.txt", encoding="utf-8")
    raw_documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.split_documents(raw_documents)
    print(f"Loaded {len(documents)} documents")
    
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small",openai_api_key=os.getenv("OPENAI_API_KEY"))
    PineconeVectorStore.from_documents(documents,embeddings, index_name="langchain-doc-index")

    



if __name__ == "__main__":
    ingest_docs()
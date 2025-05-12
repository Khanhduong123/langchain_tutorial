from backend.src.v1.config.config import OPENAI_API_KEY, INDEX_NAME, MODEL_EMBEDDING
from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader,PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter  



def ingest_text_documents_to_pinecone(file_path):
    loader = TextLoader(file_path, encoding="utf-8")
    raw_documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.split_documents(raw_documents)

    print(f"Loaded {len(documents)} documents")

    embeddings = OpenAIEmbeddings(
        model=MODEL_EMBEDDING,
        openai_api_key=OPENAI_API_KEY
    )

    PineconeVectorStore.from_documents(documents,embeddings, index_name=INDEX_NAME)

def ingest_pdf_documents_to_pinecone(file_path):
    loader = PyPDFLoader(file_path)
    raw_documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.split_documents(raw_documents)

    embeddings = OpenAIEmbeddings(
        model=MODEL_EMBEDDING,
        openai_api_key=OPENAI_API_KEY
    )

    PineconeVectorStore.from_documents(documents,embeddings, index_name=INDEX_NAME)

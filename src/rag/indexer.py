from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS, Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings 
from langchain_openai import OpenAIEmbeddings
from src.utils.config import CONFIG, OPENAI_API_KEY 
from src.rag.document_loader import load_documents
import os

def get_embedding_function():
    """Initializes and returns the embedding function based on config."""
    provider = CONFIG['embedding']['provider']
    model_name = CONFIG['embedding']['model_name']

    if provider == "openai":
        if not OPENAI_API_KEY:
             raise ValueError("OpenAI API Key required for OpenAI embeddings.")
        return OpenAIEmbeddings(model=model_name, api_key=OPENAI_API_KEY)
    elif provider == "huggingface":
        # You might need `pip install sentence_transformers`
        return HuggingFaceEmbeddings(model_name=model_name)
    # Add other providers like OllamaEmbeddings here
    else:
        raise ValueError(f"Unsupported embedding provider: {provider}")

def create_vector_store(documents):
    """Creates and persists the vector store."""
    if not documents:
        print("No documents loaded, skipping vector store creation.")
        return None

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len,
    )
    splits = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(splits)} chunks.")

    embedding_function = get_embedding_function()
    store_type = CONFIG['vector_store']['type']
    persist_directory = CONFIG['vector_store']['persist_directory']
    index_name = CONFIG['vector_store'].get('index_name', 'customer_support_index') # Get index name or default

    print(f"Creating vector store using {store_type}...")
    if store_type == "faiss":
        # Ensure the directory exists
        os.makedirs(persist_directory, exist_ok=True)
        vector_store = FAISS.from_documents(splits, embedding_function)
        vector_store.save_local(folder_path=persist_directory, index_name=index_name)
        print(f"FAISS index saved to {persist_directory}/{index_name}")
        return vector_store # Return the in-memory version for potential immediate use
    elif store_type == "chroma":
        vector_store = Chroma.from_documents(
            documents=splits,
            embedding=embedding_function,
            persist_directory=persist_directory
        )
        vector_store.persist()
        print(f"Chroma database persisted to {persist_directory}")
        return vector_store
    # Add other vector store types here
    else:
        raise ValueError(f"Unsupported vector store type: {store_type}")


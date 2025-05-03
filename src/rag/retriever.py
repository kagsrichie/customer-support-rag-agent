from langchain_community.vectorstores import FAISS, Chroma
from src.rag.indexer import get_embedding_function # Reuse embedding function
from src.utils.config import CONFIG
import os

def load_vector_store():
    """Loads the persisted vector store."""
    store_type = CONFIG['vector_store']['type']
    persist_directory = CONFIG['vector_store']['persist_directory']
    index_name = CONFIG['vector_store'].get('index_name', 'customer_support_index') # Get index name or default
    embedding_function = get_embedding_function()

    if store_type == "faiss":
        index_path = os.path.join(persist_directory, index_name + ".faiss") # Default FAISS index file name
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"FAISS index not found at {index_path}. Run the indexing script first.")
        # `allow_dangerous_deserialization=True` might be needed depending on your FAISS/Langchain version & environment. Be aware of security implications.
        vector_store = FAISS.load_local(persist_directory, embedding_function, index_name=index_name, allow_dangerous_deserialization=True)
        print(f"FAISS index loaded from {persist_directory}/{index_name}")
        return vector_store
    elif store_type == "chroma":
        if not os.path.exists(persist_directory):
             raise FileNotFoundError(f"Chroma persistent directory not found at {persist_directory}. Run the indexing script first.")
        vector_store = Chroma(persist_directory=persist_directory, embedding_function=embedding_function)
        print(f"Chroma database loaded from {persist_directory}")
        return vector_store
    # Add other vector store types here
    else:
        raise ValueError(f"Unsupported vector store type: {store_type}")

def get_retriever(vector_store):
    """Creates a retriever from the vector store."""
    search_k = CONFIG['retriever']['search_k']
    search_type = CONFIG['retriever']['search_type']
    return vector_store.as_retriever(search_type=search_type, search_kwargs={"k": search_k})


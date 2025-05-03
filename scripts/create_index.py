import sys
import os

# Add src directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.rag.document_loader import load_documents
from src.rag.indexer import create_vector_store
from src.utils.config import CONFIG # Ensure config is loaded correctly

def main():
    print("--- Starting Knowledge Base Indexing ---")
    # 1. Load documents
    documents = load_documents(CONFIG['data']['source_directory'])

    if not documents:
        print("No documents found. Exiting.")
        return

    # 2. Create Vector Store
    create_vector_store(documents)

    print("--- Indexing Complete ---")

if __name__ == "__main__":
    main()

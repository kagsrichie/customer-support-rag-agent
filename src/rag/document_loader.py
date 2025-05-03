from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader # Add others as needed
from src.utils.config import CONFIG
import os

def load_documents(directory_path=CONFIG['data']['source_directory']):
    """Loads documents from various formats in the specified directory."""
    # Configure loaders for different file types
    loaders = {
        ".txt": TextLoader,
        ".pdf": PyPDFLoader,
        # Add loaders for .md, .csv, .html, etc.
    }

    all_docs = []
    print(f"Loading documents from: {directory_path}")
    if not os.path.exists(directory_path):
         print(f"Error: Data directory '{directory_path}' not found.")
         return []

    # Use DirectoryLoader with glob patterns if needed, or iterate manually
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            ext = os.path.splitext(file_path)[1].lower()
            if ext in loaders:
                try:
                    print(f"  Loading: {file_path}")
                    loader_class = loaders[ext]
                    loader = loader_class(file_path)
                    docs = loader.load()
                    # Add metadata (like source file path) if not automatically added
                    for doc in docs:
                        doc.metadata["source"] = file_path.replace(directory_path, "").strip("/")
                    all_docs.extend(docs)
                except Exception as e:
                    print(f"  Error loading {file_path}: {e}")
            else:
                print(f"  Skipping unsupported file type: {file_path}")

    print(f"Loaded {len(all_docs)} documents.")
    return all_docs


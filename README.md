# Customer Support Agent with RAG and Tools

This project implements an AI customer support assistant using a Large Language Model (LLM) combined with Retrieval-Augmented Generation (RAG) from a custom knowledge base and agentic tool usage capabilities.

The agent can understand user queries in a conversational context, retrieve relevant information from internal documents (FAQs, policies, guides), and use predefined tools to perform actions like checking order status or creating support tickets.

## Features

*   **Retrieval-Augmented Generation (RAG):** Answers user queries based on information retrieved from a specified knowledge base (documents in `./data`), reducing hallucinations and providing grounded responses.
*   **Agentic Behavior:** Uses LangChain agents framework to understand when to use specific tools (functions) to access external information or perform actions beyond the knowledge base.
*   **Tool Usage:** Includes example tools for common customer support tasks (e.g., `check_order_status`, `create_support_ticket`). Easily extensible.
*   **Conversational Memory:** Remembers previous turns in the conversation to maintain context using `ConversationBufferWindowMemory`.
*   **Configurable:** Key components like LLM provider/model, embedding model, vector store type, and data sources are configured via `config.yaml`.
*   **Modular Structure:** Code is organized into distinct modules for data loading, indexing, retrieval, agent logic, and tools.
*   **Command-Line Interface:** Includes a simple CLI (`main_cli.py`) for interacting with the agent.

## Project Structure
customer-support-agent-rag/
├── .github/ # Optional: GitHub Actions Workflows
│ └── workflows/
│ └── python-app.yml
├── data/ # Raw knowledge base documents (PDFs, TXT, etc.)
│ ├── faq.txt
│ └── ...
├── src/ # Source code
│ ├── agent/ # Agent core logic, prompts, tool definitions
│ │ ├── prompts.py
│ │ ├── support_agent.py # Agent setup and execution
│ │ └── tools.py # Tool definitions
│ ├── rag/ # RAG specific components
│ │ ├── document_loader.py # Loading documents
│ │ ├── indexer.py # Creating the vector store index
│ │ └── retriever.py # Retrieving documents
│ ├── utils/ # Utility functions (config loading)
│ │ └── config.py
│ └── vector_store/ # Persisted vector store index (e.g., FAISS files)
│ └── .gitkeep
├── scripts/ # Standalone scripts
│ └── create_index.py # Script to build the vector store index
├── tests/ # Unit and integration tests (Optional)
├── .env.example # Example environment variables file
├── .gitignore # Git ignore file
├── config.yaml # Configuration settings
├── main_cli.py # Command-Line Interface entry point
├── requirements.txt # Python dependencies
└── README.md # This file

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-github-repository-url>
    cd customer-support-agent-rag
    ```

2.  **Create and activate a virtual environment (Recommended):**
    ```bash
    python -m venv venv
    # On macOS/Linux:
    source venv/bin/activate
    # On Windows:
    .\venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: Depending on your chosen vector store (`faiss`, `chromadb`) or specific document loaders (`unstructured`), you might need to install additional system dependencies like `build-essential`, `poppler-utils` (for PDFs), etc. Check the documentation for those libraries if you encounter issues.)*

4.  **Configure Environment Variables:**
    *   Copy `.env.example` to `.env`:
        ```bash
        cp .env.example .env
        ```
    *   Edit the `.env` file and add your necessary API keys (e.g., `OPENAI_API_KEY` if using OpenAI).

5.  **Add Knowledge Base Documents:**
    *   Place your customer support documents (e.g., `.txt`, `.pdf`, `.md` files) into the `./data` directory. You can create subdirectories as needed.

6.  **Configure Settings:**
    *   Review and modify `config.yaml` to specify your desired LLM (provider, model name), embedding model, vector store type (`faiss`, `chroma`), paths, and retriever settings.

7.  **Create the Knowledge Base Index:**
    *   Run the indexing script. This processes the documents in `./data`, generates embeddings, and saves the vector store index to `./src/vector_store`. **This must be done initially and whenever you add, remove, or modify documents in the `./data` directory.**
    ```bash
    python scripts/create_index.py
    ```

## Running the Agent (CLI)

*   Ensure your virtual environment is activated and you have completed the setup steps (especially creating the index).
*   Start the command-line interface:
    ```bash
    python main_cli.py
    ```
*   The agent will greet you. Type your queries and press Enter.
*   Type `exit`, `quit`, or `bye` to end the conversation.

## Customization

*   **Knowledge Base:**
    *   Add, edit, or remove files in the `./data` directory.
    *   **Important:** Re-run `python scripts/create_index.py` after making changes to the knowledge base documents.
*   **Tools:**
    *   Define new tools in `src/agent/tools.py` using the `@tool` decorator from LangChain. Ensure functions have clear docstrings explaining their purpose and arguments.
    *   Add your new tool function to the `CUSTOMER_SUPPORT_TOOLS` list in `src/agent/tools.py`.
    *   Update the agent prompt in `src/agent/prompts.py` to make the agent aware of the new tool's capabilities if necessary.
    *   **Security:** Replace placeholder logic in tools with actual, secure API calls, including proper authentication, authorization, error handling, and input validation.
*   **Agent Behavior (Prompt Engineering):**
    *   Modify the `SYSTEM_PROMPT_TEMPLATE` in `src/agent/prompts.py` to change the agent's persona, instructions, constraints, or how it uses context and tools.
*   **Models & Configuration:**
    *   Change LLM providers (e.g., `openai`, `huggingface`, `ollama`), model names, embedding models, vector stores, or RAG parameters (like `search_k`) in `config.yaml`.
    *   Ensure you have the corresponding libraries installed (e.g., `langchain-openai`, `langchain-community`, `sentence-transformers`, `ollama`) and API keys set in `.env`.

## Future Enhancements / TODO

*   [ ] Implement a web interface using FastAPI/Streamlit.
*   [ ] Add more robust error handling and logging throughout the application.
*   [ ] Implement stricter security measures for tool execution, especially for tools performing actions.
*   [ ] Develop evaluation scripts to measure retrieval relevance, generation faithfulness, and task success rate.
*   [ ] Support a wider range of document types and vector store options.
*   [ ] Implement user session management for concurrent users (essential for web deployment).
*   [ ] Explore different agent types and prompting strategies (e.g., ReAct, Self-Ask).
*   [ ] Add mechanisms for feedback collection and continuous improvement of the RAG system.
*   [ ] Implement unit and integration tests in the `tests/` directory.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs, feature requests, or improvements. (Add specific contribution guidelines if desired).

## License

(Specify your chosen license here, e.g., MIT, Apache 2.0, or leave as proprietary if applicable).

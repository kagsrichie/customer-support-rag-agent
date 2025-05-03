from langchain_openai import ChatOpenAI        
from langchain.agents import AgentExecutor, create_openai_tools_agent 
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.messages import AIMessage, HumanMessage

from src.rag.retriever import load_vector_store, get_retriever
from src.agent.tools import CUSTOMER_SUPPORT_TOOLS
from src.agent.prompts import agent_prompt
from src.utils.config import CONFIG, OPENAI_API_KEY # Import API keys

# --- Initialize LLM ---
def get_llm():
    provider = CONFIG['llm']['provider']
    model_name = CONFIG['llm']['model_name']
    temperature = CONFIG['llm']['temperature']

    if provider == "openai":
        if not OPENAI_API_KEY:
            raise ValueError("OpenAI API Key required.")
        return ChatOpenAI(model=model_name, temperature=temperature, api_key=OPENAI_API_KEY)
    # Add other LLM providers (ChatOllama, HuggingFaceHub, etc.)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")

# --- Initialize Components ---
llm = get_llm()
vector_store = load_vector_store()
retriever = get_retriever(vector_store)
tools = CUSTOMER_SUPPORT_TOOLS


# Let's make a retrieval tool for the agent:
from langchain.tools.retriever import create_retriever_tool

retriever_tool = create_retriever_tool(
    retriever,
    "knowledge_base_search",
    "Search the customer support knowledge base for relevant information about the user's query. Use this before answering questions about policies, troubleshooting, or general product information.",
)

# Combine custom tools with the retriever tool
all_tools = CUSTOMER_SUPPORT_TOOLS + [retriever_tool]

# --- The Agent ---
# Using OpenAI Tools agent as an example
# Requires an LLM that supports function/tool calling (like OpenAI's models)
agent = create_openai_tools_agent(llm, all_tools, agent_prompt)

# --- Setting up Memory ---
# Use a windowed buffer to keep context manageable
memory = ConversationBufferWindowMemory(
    k=5, # Remember last 5 turns
    memory_key="chat_history",
    input_key="input",
    output_key="output",
    return_messages=True # Return messages objects for the prompt
)

# --- Create the Agent Executor ---
# This runs the agent loop (thought -> action -> observation -> thought...)
agent_executor = AgentExecutor(
    agent=agent,
    tools=all_tools,
    memory=memory,
    verbose=True, # Set to True to see agent's thoughts and actions
    max_iterations=CONFIG['agent']['max_iterations'],
    handle_parsing_errors=True, # Gracefully handle occasional LLM format errors
)

def run_agent_interaction(user_input: str):
    """Runs a single interaction cycle with the agent."""
    # The AgentExecutor handles history automatically via the memory object
    response = agent_executor.invoke({"input": user_input})
    return response['output']

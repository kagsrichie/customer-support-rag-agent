import sys
import os

# Add src directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# It's cleaner to import the run function rather than initializing everything here
from agent.support_agent import run_agent_interaction

def main():
    print("--- Customer Support Agent (CLI) ---")
    print("Type 'exit', 'quit', or 'bye' to end the conversation.")
    print("\nSupportAI: Hello! How can I help you today?")

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("SupportAI: Goodbye! Have a great day.")
                break

            if not user_input.strip():
                continue

            # Run the agent interaction
            ai_response = run_agent_interaction(user_input)

            print(f"SupportAI: {ai_response}")

        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Please try again or type 'exit' to quit.")
            # Optional: Add more robust error handling or restart logic

if __name__ == "__main__":
    # Perform checks before starting (e.g., ensure index exists)
    # Example check (can be more sophisticated):
    vector_store_path = os.path.join("src", "vector_store")
    if not os.path.exists(vector_store_path) or not os.listdir(vector_store_path):
         print("\nERROR: Vector store index not found!")
         print("Please run the indexing script first:")
         print("  python scripts/create_index.py")
         sys.exit(1)
    if not os.path.exists(".env"):
        print("\nERROR: .env file not found!")
        print("Please create a .env file with your API keys (see .env.example).")
        sys.exit(1)

    main()

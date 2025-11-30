import os
import sys

# Add the project root to sys.path
sys.path.append(os.path.abspath("/Users/srinija/rag_search_engine"))

from app.llm import LLMClient

def verify_fix():
    print("Initializing LLMClient...")
    client = LLMClient()
    
    if client.provider != "groq":
        print("WARNING: Not using Groq provider. Please check GROQ_API_KEY env var.")
        # If we can't test the actual API, we can't verify the fix fully, but we can check the code doesn't crash.
        return

    print("Sending test query...")
    try:
        answer = client.generate_answer("What is the capital of France?", ["Paris is the capital of France."])
        print(f"Success! Answer received: {answer}")
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    verify_fix()

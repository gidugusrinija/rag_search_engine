import os
from groq import Groq
from app.core import get_settings

settings = get_settings()

class LLMClient:
    def __init__(self):
        self.provider = "groq" if settings.GROQ_API_KEY else "mock"
        if self.provider == "groq":
            self.client = Groq(api_key=settings.GROQ_API_KEY)
        else:
            print("No API key found. Using Mock LLM.")

    def generate_answer(self, query: str, context: list[str]) -> str:
        context_str = "\n\n".join(context)
        prompt = f"""Answer the question based on the context below.
        
Context:
{context_str}

Question: {query}

Answer:"""

        if self.provider == "groq":
            try:
                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model="llama-3.1-8b-instant",
                )
                return chat_completion.choices[0].message.content
            except Exception as e:
                return f"Error generating answer: {str(e)}"
        else:
            return "This is a mock answer. Please provide a GROQ_API_KEY to get real answers."

_llm_client_instance = None

def get_llm_client():
    global _llm_client_instance
    if _llm_client_instance is None:
        _llm_client_instance = LLMClient()
    return _llm_client_instance

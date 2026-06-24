from src.retrieve import retrieve_context
import google.generativeai as genai
import time
from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL
)

SYSTEM_PROMPT = """
You are a financial compliance assistant.

Rules:
1. Answer only using the provided context.
2. Do not hallucinate.
3. Be concise and accurate.
"""

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(GEMINI_MODEL)


def get_answer(query: str) -> str:
    chunks = retrieve_context(query)

    prompt = f"""
{SYSTEM_PROMPT}

CONTEXT:
{chunks}

QUESTION:
{query}
"""


    response = model.generate_content(prompt)

    return response.text


# Example usage
if __name__ == "__main__":
    while True:
        query = input("Enter the query: ")

        if query == "1":
            break

        answer = get_answer(query)
        print(answer)
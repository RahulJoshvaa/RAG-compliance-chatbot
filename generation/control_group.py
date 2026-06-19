from src.retrieve import retrieve_context

SYSTEM_PROMPT = """
You are a financial compliance assistant.

Rules:
1. Answer only using the provided context.
2. Do not hallucinate.

3. Be concise and accurate.
"""


import google.generativeai as genai

from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL
)

genai.configure(
    api_key=GEMINI_API_KEY
)

model = genai.GenerativeModel(
    GEMINI_MODEL
)

def generate(prompt) -> str:

    response = model.generate_content(
        prompt
    )

    return response.text


def build_prompt(query: str) -> str:
    chunks = retrieve_context(query)

    return f"""
{SYSTEM_PROMPT}

CONTEXT:
{chunks}

QUESTION:
{query}
"""
    


while True:
    query = input("Enter the query: ")
    if query == "1":
        break
    else:
        prompt = build_prompt(query)
        answer = generate(prompt)
        print(answer)

from compress import compress_context
from src.retrieve import retrieve_context

SYSTEM_PROMPT = """
You are a financial compliance assistant.

Rules:
1. Answer only using the provided context.
2. Do not hallucinate.
3. Be concise and accurate.
"""



def build_prompt(query: str) -> str:
    chunks = retrieve_context(query)
    context = compress_context(query, chunks)

    return f"""
{SYSTEM_PROMPT}

CONTEXT:
{context}

QUESTION:
{query}
"""
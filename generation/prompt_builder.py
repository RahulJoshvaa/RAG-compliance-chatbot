from kompress import compress_context
from mock_retriever import retrieve

SYSTEM_PROMPT = """
You are a financial compliance assistant.

Rules:
1. Answer only using the provided context.
2. Do not hallucinate.

3. Be concise and accurate.
"""



def build_prompt(query: str) -> str:
    chunks = retrieve(query)
    context = compress_context(query, chunks)

    return f"""
{SYSTEM_PROMPT}

CONTEXT:
{context}

QUESTION:
{query}
"""
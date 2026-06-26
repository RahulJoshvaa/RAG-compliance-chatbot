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
    compressed = compress_context(query, chunks)

    # compress_context returns {"compressed_text", "c_ratio"} normally, but
    # falls back to a plain string when there are no sentences to compress.
    context = (
        compressed["compressed_text"]
        if isinstance(compressed, dict)
        else compressed
    )

    return f"""
{SYSTEM_PROMPT}

CONTEXT:
{context}

QUESTION:
{query}
"""
from compress import compress_context
from src.retrieve import retrieve_context
import time
SYSTEM_PROMPT = """
You are a financial compliance assistant.

Rules:
1. Answer only using the provided context.
2. Do not hallucinate.
3. Be concise and accurate.
"""


def build_prompt(query):

    t = time.perf_counter()
    chunks = retrieve_context(query)
    print(f"Retrieve: {time.perf_counter() - t:.2f}s")

    t = time.perf_counter()
    compressed = compress_context(query, chunks)
    print(f"Compress: {time.perf_counter() - t:.2f}s")

    context = (
        compressed["compressed_text"]
        if isinstance(compressed, dict)
        else compressed
    )

    prompt = f"""
{SYSTEM_PROMPT}

CONTEXT:
{context}

QUESTION:
{query}
"""

    return prompt, chunks
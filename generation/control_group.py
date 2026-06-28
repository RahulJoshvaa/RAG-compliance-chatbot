from groq import Groq

from src.retrieve import retrieve_context

from config import (
    GROQ_API_KEY,
    GROQ_MODEL
)

SYSTEM_PROMPT = """
You are a financial compliance assistant.

Rules:
1. Answer only using the provided context.
2. Do not hallucinate.
3. Be concise and accurate.
"""

client = Groq(
    api_key=GROQ_API_KEY
)


def dedupe_sources(chunks):

    seen = set()
    sources = []

    for chunk in chunks:

        key = (chunk["source"], chunk["page"])

        if key in seen:
            continue

        seen.add(key)

        sources.append(
            {
                "source": chunk["source"],
                "page": chunk["page"]
            }
        )

    return sources


def get_answer(query):

    chunks = retrieve_context(query)

    context = "\n\n".join(
        chunk["text"]
        for chunk in chunks
    )

    prompt = f"""
{SYSTEM_PROMPT}

CONTEXT:
{context}

QUESTION:
{query}
"""

    completion = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return {
        "answer": completion.choices[0].message.content,
        "sources": dedupe_sources(chunks),
        "input_tokens": completion.usage.prompt_tokens,
        "output_tokens": completion.usage.completion_tokens,
        "total_tokens": completion.usage.total_tokens
    }


if __name__ == "__main__":

    while True:

        query = input("Enter the query: ")

        if query == "1":
            break

        result = get_answer(query)

        print("\nAnswer:\n")
        print(result["answer"])

        print("\nSources:")
        for source in result["sources"]:
            print(
                f"{source['source']} (Page {source['page']})"
            )
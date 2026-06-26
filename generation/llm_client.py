from groq import Groq

from prompt_builder import build_prompt
from config import GROQ_API_KEY, GROQ_MODEL
import time

client = Groq(api_key=GROQ_API_KEY)


def dedupe_sources(chunks):

    seen = set()
    sources = []

    for chunk in chunks:

        key = (chunk["source"], chunk["page"])

        if key not in seen:
            seen.add(key)
            sources.append(
                {
                    "source": chunk["source"],
                    "page": chunk["page"]
                }
            )

    return sources


def generate(query):

    prompt, chunks = build_prompt(query)
    start = time.time()
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

    print(f"Time Taken by LLM {time.time() - start}")

    return {
        "answer": completion.choices[0].message.content,
        "sources": dedupe_sources(chunks)
    }
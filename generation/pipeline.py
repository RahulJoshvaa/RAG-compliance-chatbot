import time

from llm_client import generate
from control_group import get_answer


def run_pipeline(query):

    start = time.perf_counter()

    result = generate(query)

    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "mode": "COMPRESSED_RAG",
        "live": True,
        "metrics": {
            "latency": round(
                time.perf_counter() - start,
                2
            )
        }
    }


def run_traditional_pipeline(query):

    start = time.time()

    result = get_answer(query)

    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "mode": "TRADITIONAL_RAG",
        "live": True,
        "metrics": {
            "latency": round(
                time.time() - start,
                2
            )
        }
    }
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
            ),
            "input_tokens": result["input_tokens"],
            "output_tokens": result["output_tokens"],
            "total_tokens": result["total_tokens"]
        }
    }


def run_traditional_pipeline(query):

    start = time.perf_counter()

    result = get_answer(query)

    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "mode": "TRADITIONAL_RAG",
        "live": True,
        "metrics": {
            "latency": round(
                time.perf_counter() - start,
                2
            ),
            "input_tokens": result["input_tokens"],
            "output_tokens": result["output_tokens"],
            "total_tokens": result["total_tokens"]
        }
    }
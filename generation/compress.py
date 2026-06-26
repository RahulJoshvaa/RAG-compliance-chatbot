import time
import torch

from sentence_transformers import (
    SentenceTransformer,
    util
)

# Same model used during ingestion
model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)


def compress_context(
    query,
    chunks,
    top_n=10,
    window_size=1
):

    original_words = sum(
        len(chunk["text"].split())
        for chunk in chunks
    )

    all_sentences = []
    all_embeddings = []

    for chunk in chunks:

        all_sentences.extend(
            chunk["sentences"]
        )

        all_embeddings.extend(
            chunk["sentence_embeddings"]
        )

    if not all_sentences:
        return ""

    start = time.perf_counter()

    with torch.no_grad():

        query_embedding = model.encode(
            query,
            convert_to_tensor=True
        )

    sentence_embeddings = torch.tensor(
        all_embeddings,
        dtype=torch.float32
    )

    print(
        f"Query Embedding: {time.perf_counter() - start:.2f}s"
    )

    start = time.perf_counter()

    scores = util.cos_sim(
        query_embedding,
        sentence_embeddings
    )[0]

    print(
        f"Similarity Time: {time.perf_counter() - start:.4f}s"
    )

    ranked = sorted(
        enumerate(scores),
        key=lambda x: float(x[1]),
        reverse=True
    )

    top_indices = {
        idx
        for idx, _
        in ranked[:min(top_n, len(all_sentences))]
    }

    selected_indices = set()

    for idx in top_indices:

        left = max(
            0,
            idx - window_size
        )

        right = min(
            len(all_sentences),
            idx + window_size + 1
        )

        selected_indices.update(
            range(left, right)
        )

    compressed_sentences = [
        all_sentences[i]
        for i in sorted(selected_indices)
    ]

    compressed_text = "\n".join(
        compressed_sentences
    )

    compressed_words = len(
        compressed_text.split()
    )

    print("\n===== COMPRESSION STATS =====")

    print(
        "Total Sentences:",
        len(all_sentences)
    )

    print(
        "Selected Sentences:",
        len(selected_indices)
    )

    print(
        "Original Words:",
        original_words
    )

    print(
        "Compressed Words:",
        compressed_words
    )

    print(
        "Words Saved:",
        original_words - compressed_words
    )

    print(
        "Compression Ratio:",
        f"{compressed_words/original_words:.2f}"
    )

    c_ratio = round(
        compressed_words / original_words,
        2
    )

    return {
        "compressed_text": compressed_text,
        "c_ratio": c_ratio
    }
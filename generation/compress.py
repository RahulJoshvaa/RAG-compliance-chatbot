import re
from sentence_transformers import (
    SentenceTransformer,
    util
)
import time
# Keep same embedding as retriever for fair comparison
model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)


def compress_context(
    query,
    chunks,
    top_n=10,
    window_size=1
):
    print("Loading Sentence Compressor...")

    content = "\n\n".join(
        chunk["text"]
        for chunk in chunks
    )


    start = time.time()

    original_words = len(content.split())

    sentences = [
        s.strip()
        for s in re.split(
            r'(?<=[.!?])\s+',
            content
        )
        if s.strip()
    ]

    if not sentences:
        return content

    query_embedding = model.encode(
        query,
        convert_to_tensor=True
    )


    sentence_embeddings = model.encode(
        sentences,
        convert_to_tensor=True
    )

    scores = util.cos_sim(
        query_embedding,
        sentence_embeddings
    )[0]

    # Rank sentences by similarity
    ranked = sorted(
        enumerate(scores),
        key=lambda x: float(x[1]),
        reverse=True
    )

    # Keep top N
    top_indices = {
        idx
        for idx, _
        in ranked[:min(top_n, len(sentences))]
    }

    # Add neighboring sentences for context
    selected_indices = set()

    for idx in top_indices:
        start = max(
            0,
            idx - window_size
        )

        end = min(
            len(sentences),
            idx + window_size + 1
        )

        for i in range(start, end):
            selected_indices.add(i)

    compressed_sentences = [
        sentences[i]
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
        len(sentences)
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
        original_words -
        compressed_words
    )

    print(
        "Compression Ratio:",
        f"{compressed_words/original_words:.2f}"
    )

    c_ratio = round(compressed_words/original_words, 2)

    return {"compressed_text": compressed_text, "c_ratio": c_ratio}
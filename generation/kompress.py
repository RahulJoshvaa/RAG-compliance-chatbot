import time

from headroom.transforms.kompress_compressor import (
    KompressCompressor,
    KompressConfig
)

# Mild compression for compliance documents


def compress_context(query, chunks):
    config = KompressConfig(
    score_threshold=0.2,
    chunk_words=100,
    enable_ccr=False
)
    print("Loading Kompress...")

    kompress = KompressCompressor(config=config)

    print("Kompress Loaded")

    start = time.time()

    content = "\n\n".join(
        chunk["text"]
        for chunk in chunks
    )
    print(f"Time for join{time.time() - start}")


    start = time.time()

    result = kompress.compress(
        content,
        context=query
    )
    print(f"Time for compress{time.time() - start}")


    print("\n===== KOMPRESS STATS =====")

    print(
        "Original Tokens:",
        result.original_tokens
    )

    print(
        "Compressed Tokens:",
        result.compressed_tokens
    )

    print(
        "Tokens Saved:",
        result.original_tokens -
        result.compressed_tokens
    )

    # print(result.compressed)

    return result.compressed
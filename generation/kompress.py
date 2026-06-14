
from headroom.transforms.kompress_compressor import (
    KompressCompressor,
    KompressConfig
)

# Mild compression for compliance documents


def compress_context(query, chunks):
    config = KompressConfig(
    score_threshold=0.3,
    chunk_words=500,
    enable_ccr=True
)
    print("Loading Kompress...")

    kompress = KompressCompressor(config=config)

    print("Kompress Loaded")


    content = "\n\n".join(
        chunk["text"]
        for chunk in chunks
    )

    result = kompress.compress(
        content,
    )

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

    print(result.compressed)

    return result.compressed
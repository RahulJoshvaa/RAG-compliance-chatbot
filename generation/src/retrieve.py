import json
import chromadb
import os

from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)

BASE_DIR = os.path.dirname(__file__)

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-en-v1.5"
)

# ------------------------------------------------------------------
# Load parent document store ONCE at startup
# ------------------------------------------------------------------

PARENT_STORE_PATH = os.path.join(
    BASE_DIR,
    "parent_document_store.json"
)

print("[Startup] Loading parent document store...")

try:

    with open(
        PARENT_STORE_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        PARENT_DOCUMENT_STORE = json.load(file)

    print(
        f"[Startup] Loaded {len(PARENT_DOCUMENT_STORE)} parent chunks."
    )

except FileNotFoundError:

    print(
        "[Error] Parent document store missing."
    )

    PARENT_DOCUMENT_STORE = {}


# ------------------------------------------------------------------
# Initialize Chroma ONCE at startup
# ------------------------------------------------------------------

DB_PATH = os.path.join(
    BASE_DIR,
    "chroma_db"
)

try:

    chroma_client = chromadb.PersistentClient(
        path=DB_PATH
    )

    CHILD_COLLECTION = chroma_client.get_collection(
        name="compliance_child_chunks"
    )

    print("[Startup] Chroma collection loaded.")

except Exception:

    print(
        "[Error] Could not find Chroma collection."
    )

    CHILD_COLLECTION = None


def retrieve_context(
    query,
    top_k=5
):

    if CHILD_COLLECTION is None:
        return []

    print(
        f"\n[Query] Searching database for: '{query}'"
    )

    query_embedding = embeddings.embed_query(
        query
    )

    results = CHILD_COLLECTION.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=top_k
    )

    metadatas = (
        results["metadatas"][0]
        if results["metadatas"]
        else []
    )

    seen_parents = set()

    retrieved_contexts = []

    for meta in metadatas:

        parent_id = meta.get(
            "parent_id"
        )

        if (
            parent_id
            and parent_id not in seen_parents
        ):

            seen_parents.add(
                parent_id
            )

            if parent_id in PARENT_DOCUMENT_STORE:

                parent_data = (
                    PARENT_DOCUMENT_STORE[
                        parent_id
                    ]
                )

                retrieved_contexts.append(
                    {
                        "text":
                        parent_data["text"],

                        "sentences":
                        parent_data["sentences"],

                        "sentence_embeddings":
                        parent_data[
                            "sentence_embeddings"
                        ],

                        "source":
                        parent_data[
                            "metadata"
                        ][
                            "source_file"
                        ],

                        "page":
                        parent_data[
                            "metadata"
                        ][
                            "page_number"
                        ]
                    }
                )

    total_words = sum(
        len(ctx["text"].split())
        for ctx in retrieved_contexts
    )

    total_chars = sum(
        len(ctx["text"])
        for ctx in retrieved_contexts
    )

    print(
        f"[Retrieved {len(retrieved_contexts)} parent chunks]"
    )

    print(
        f"[Retrieved Words: {total_words}]"
    )

    print(
        f"[Retrieved Characters: {total_chars}]"
    )

    return retrieved_contexts


if __name__ == "__main__":

    sample_query = (
        "What are the rules regarding "
        "risk management framework and ICT compliance?"
    )

    contexts = retrieve_context(
        sample_query,
        top_k=3
    )

    for i, ctx in enumerate(
        contexts,
        start=1
    ):

        print(
            f"\n--- Result {i} ---"
        )

        print(
            f"Source: {ctx['source']}"
        )

        print(
            f"Page: {ctx['page']}"
        )

        print(
            ctx["text"][:500]
        )
import json
import chromadb
import os

from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)

BASE_DIR = os.path.dirname(__file__)

# MUST match ingest.py
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-en-v1.5"
)


def retrieve_context(
    query,
    top_k=4
):

    db_path = os.path.join(
        BASE_DIR,
        "chroma_db"
    )

    parent_store_path = os.path.join(
        BASE_DIR,
        "parent_document_store.json"
    )

    try:
        chroma_client = (
            chromadb.PersistentClient(
                path=db_path
            )
        )

        child_collection = (
            chroma_client.get_collection(
                name="compliance_child_chunks"
            )
        )

    except Exception:
        print(
            "[Error] Could not find Chroma collection."
        )
        return []

    try:
        with open(
            parent_store_path,
            "r",
            encoding="utf-8"
        ) as file:

            parent_document_store = (
                json.load(file)
            )

    except FileNotFoundError:
        print(
            "[Error] Parent document store missing."
        )
        return []

    print(
        f"\n[Query] Searching database for: '{query}'"
    )

    # Embed query using BGE
    query_embedding = (
        embeddings.embed_query(query)
    )

    # Search using vector
    results = child_collection.query(
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
            and parent_id
            not in seen_parents
        ):

            seen_parents.add(
                parent_id
            )

            if (
                parent_id
                in parent_document_store
            ):

                parent_data = (
                    parent_document_store[
                        parent_id
                    ]
                )

                retrieved_contexts.append(
                    {
                        "text":
                        parent_data[
                            "text"
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

    print(
        f"[Retrieved {len(retrieved_contexts)} parent chunks]"
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
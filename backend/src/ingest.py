import os
import json
import uuid
import chromadb
import re
from sentence_transformers import SentenceTransformer

from langchain_community.document_loaders import (
    PyPDFLoader
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)

from langchain_experimental.text_splitter import (
    SemanticChunker
)


def run_pipeline():

    data_folder = "./data"
    db_path = "./chroma_db"
    parent_store_path = "parent_document_store.json"

    print(
        "[Ingestion] Initializing embedding model..."
    )

    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-base-en-v1.5"
    )

    sentence_model = SentenceTransformer(
        "BAAI/bge-small-en-v1.5"
    )
    sample_vector = embeddings.embed_query(
        "test"
    )

    print(
        "Embedding Dimension:",
        len(sample_vector)
    )

    chroma_client = chromadb.PersistentClient(
        path=db_path
    )

    try:
        chroma_client.delete_collection(
            "compliance_child_chunks"
        )
        print(
            "[Info] Existing collection deleted."
        )
    except:
        pass

    child_collection = (
        chroma_client.create_collection(
            name="compliance_child_chunks"
        )
    )

    parent_document_store = {}

    if not os.path.exists(data_folder):
        print(
            f"[Error] Folder '{data_folder}' not found."
        )
        return

    pdf_files = [
        f
        for f in os.listdir(data_folder)
        if f.endswith(".pdf")
    ]

    if not pdf_files:
        print(
            "[Warning] No PDF files found."
        )
        return

    print(
        f"[Ingestion] Found {len(pdf_files)} PDFs"
    )

    parent_splitter = (
        RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=200
        )
    )

    child_splitter = SemanticChunker(
        embeddings,
        breakpoint_threshold_type="percentile"
    )

    for pdf_name in pdf_files:

        print(
            f"\n--- Processing {pdf_name} ---"
        )

        file_path = os.path.join(
            data_folder,
            pdf_name
        )

        loader = PyPDFLoader(
            file_path
        )

        pages = loader.load()

        parent_chunks = (
            parent_splitter.split_documents(
                pages
            )
        )

        for parent_chunk in parent_chunks:

            parent_id = (
                f"parent_{uuid.uuid4()}"
            )

            page_num = (
                parent_chunk.metadata.get(
                    "page",
                    0
                ) + 1
            )

            sentences = [
                s.strip()
                for s in re.split(
                    r'(?<=[.!?])\s+',
                    parent_chunk.page_content
                )
                if s.strip()
            ]

            sentence_embeddings = sentence_model.encode(
                sentences,
                convert_to_numpy=True
            ).tolist()

            parent_document_store[parent_id] = {

                "text": parent_chunk.page_content,

                "sentences": sentences,

                "sentence_embeddings": sentence_embeddings,

                "metadata": {

                    "source_file": pdf_name,

                    "page_number": page_num
                }
            }

            semantic_children = (
                child_splitter.create_documents(
                    [
                        parent_chunk.page_content
                    ]
                )
            )

            child_texts = []
            child_ids = []
            child_metadatas = []

            for idx, child_doc in enumerate(
                semantic_children
            ):

                child_texts.append(
                    child_doc.page_content
                )

                child_ids.append(
                    f"child_{parent_id}_{idx}"
                )

                child_metadatas.append(
                    {
                        "parent_id":
                        parent_id,

                        "source_file":
                        pdf_name,

                        "page_number":
                        page_num
                    }
                )

            if not child_texts:
                continue

            child_embeddings = (
                embeddings.embed_documents(
                    child_texts
                )
            )

            child_collection.add(
                ids=child_ids,

                documents=child_texts,

                embeddings=child_embeddings,

                metadatas=child_metadatas
            )

    with open(
        parent_store_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            parent_document_store,
            f,
            indent=4
        )

    print(
        "\n[Success] Ingestion Complete!"
    )


if __name__ == "__main__":
    run_pipeline()
import os
import json
import uuid
import chromadb
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_experimental.text_splitter import SemanticChunker

def run_pipeline():
    data_folder = "./data"
    db_path = "./chroma_db"
    parent_store_path = "parent_document_store.json"

    print("[Ingestion] Initializing local embedding model...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    chroma_client = chromadb.PersistentClient(path=db_path)
    child_collection = chroma_client.get_or_create_collection(name="compliance_child_chunks")
    parent_document_store = {}

    if not os.path.exists(data_folder):
        print(f"[Error] The folder '{data_folder}' does not exist.")
        return

    pdf_files = [f for f in os.listdir(data_folder) if f.endswith(".pdf")]
    if not pdf_files:
        print(f"[Warning] No PDF files found inside '{data_folder}'. Please put your 5 PDFs there.")
        return

    print(f"[Ingestion] Found {len(pdf_files)} PDF files: {pdf_files}")

    parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    child_splitter = SemanticChunker(embeddings, breakpoint_threshold_type="percentile")

    for pdf_name in pdf_files:
        file_path = os.path.join(data_folder, pdf_name)
        print(f"\n--- Processing Document: {pdf_name} ---")
        
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        raw_parent_chunks = parent_splitter.split_documents(pages)

        for parent_chunk in raw_parent_chunks:
            parent_id = f"parent_{uuid.uuid4()}"
            page_num = parent_chunk.metadata.get("page", 0) + 1
            
            parent_document_store[parent_id] = {
                "text": parent_chunk.page_content,
                "metadata": {"source_file": pdf_name, "page_number": page_num}
            }

            semantic_children = child_splitter.create_documents([parent_chunk.page_content])
            
            child_texts = []
            child_metadatas = []
            child_ids = []

            for c_index, child_doc in enumerate(semantic_children):
                child_texts.append(child_doc.page_content)
                child_metadatas.append({
                    "parent_id": parent_id,
                    "source_file": pdf_name,
                    "page_number": page_num
                })
                child_ids.append(f"child_{parent_id}_{c_index}")

            if child_texts:
                child_collection.add(documents=child_texts, metadatas=child_metadatas, ids=child_ids)

    with open(parent_store_path, "w") as file:
        json.dump(parent_document_store, file, indent=4)
        
    print("[Success] Ingestion Complete!")

if __name__ == "__main__":
    run_pipeline()
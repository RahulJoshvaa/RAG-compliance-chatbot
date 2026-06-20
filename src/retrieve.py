import time
import json
import tiktoken
import chromadb
from langchain_community.embeddings import HuggingFaceEmbeddings

def evaluate_retrieval_performance(retrieved_contexts, pricing_per_1k_tokens=0.0015):
    """
    Calculates the 4 performance metrics for the control group pipeline.
    """
    # Initialize the tokenizer layout used by standard LLMs
    tokenizer = tiktoken.get_encoding("cl100k_base")
    
    # Combine all the text from the retrieved parent chunks into one string
    full_context_text = " ".join([chunk["text"] for chunk in retrieved_contexts])
    
    # --- METRIC 1: Tokens per query ---
    tokens = len(tokenizer.encode(full_context_text))
    
    # --- METRIC 2: Cost per 1,000 queries ---
    # Formula: (Tokens / 1000) * Price per 1K * 1000 queries
    cost_per_single_query = (tokens / 1000) * pricing_per_1k_tokens
    cost_per_1k_queries = cost_per_single_query * 1000
    
    return {
        "tokens_per_query": tokens,
        "cost_per_1k_queries": round(cost_per_1k_queries, 4)
    }

def retrieve_context(query, top_k=3):
    # --- START LATENCY STOPWATCH ---
    start_time = time.perf_counter()

    db_path = "./chroma_db"
    parent_store_path = "parent_document_store.json"

    # 1. Initialize the exact same local embedding model
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # 2. Connect to our local ChromaDB collection
    chroma_client = chromadb.PersistentClient(path=db_path)
    try:
        child_collection = chroma_client.get_collection(name="compliance_child_chunks")
    except Exception:
        print("[Error] Could not find the vector database collection. Did you run ingest.py first?")
        return

    # 3. Load our Parent document mapper
    try:
        with open(parent_store_path, "r") as file:
            parent_document_store = json.load(file)
    except FileNotFoundError:
        print("[Error] Parent document store file missing.")
        return

    print(f"\n[Query] Searching baseline database for: '{query}'")

    # 4. Search the database using the child vectors
    results = child_collection.query(
        query_texts=[query],
        n_results=top_k
    )

    # 5. Fetch the structural Parent contexts using the retrieved child IDs
    metadatas = results['metadatas'][0] if results['metadatas'] else []
    
    seen_parents = set()
    retrieved_contexts = []

    for meta in metadatas:
        parent_id = meta.get("parent_id")
        
        # Avoid pulling the duplicate parent block if multiple children match it
        if parent_id and parent_id not in seen_parents:
            seen_parents.add(parent_id)
            
            if parent_id in parent_document_store:
                parent_data = parent_document_store[parent_id]
                retrieved_contexts.append({
                    "text": parent_data["text"],
                    "source": parent_data["metadata"]["source_file"],
                    "page": parent_data["metadata"]["page_number"]
                })

    # --- STOP LATENCY STOPWATCH ---
    end_time = time.perf_counter()
    latency_ms = (end_time - start_time) * 1000

    # 6. Display what our baseline control group found
    print(f"\n=== Baseline Control Group Results (Found {len(retrieved_contexts)} Unique Matching Blocks) ===")
    for idx, ctx in enumerate(retrieved_contexts):
        print(f"\n[Match #{idx+1}] Source: {ctx['source']} (Page {ctx['page']})")
        print("-" * 60)
        print(ctx['text'][:400] + "..." if len(ctx['text']) > 400 else ctx['text'])
        print("-" * 60)

    # 7. Calculate and display the core efficiency metrics
    metrics = evaluate_retrieval_performance(retrieved_contexts)
    
    print("\n=== SYSTEM PERFORMANCE METRICS ===")
    print(f"Latency per query: {latency_ms:.2f} ms")
    print(f"Tokens per query: {metrics['tokens_per_query']} tokens")
    print(f"Cost per 1,000 queries: ${metrics['cost_per_1k_queries']}")
    print("==================================\n")

    return retrieved_contexts

if __name__ == "__main__":
    # Test your baseline pipeline with a common compliance keyword
    sample_query = "What are the rules regarding risk management framework and ICT compliance?"
    retrieve_context(sample_query, top_k=3)
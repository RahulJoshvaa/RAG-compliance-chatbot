import time
import json
import tiktoken
import chromadb
from langchain_community.embeddings import HuggingFaceEmbeddings

def evaluate_retrieval_performance(retrieved_contexts, pricing_per_1k_tokens=0.0015):
    """
    Calculates the automated efficiency and cost metrics.
    """
    tokenizer = tiktoken.get_encoding("cl100k_base")
    full_context_text = " ".join([chunk["text"] for chunk in retrieved_contexts])
    
    tokens = len(tokenizer.encode(full_context_text))
    cost_per_single_query = (tokens / 1000) * pricing_per_1k_tokens
    cost_per_1k_queries = cost_per_single_query * 1000
    
    return {
        "tokens_per_query": tokens,
        "cost_per_1k_queries": round(cost_per_1k_queries, 4)
    }

def calculate_sources_fit_rate(query, retrieved_contexts):
    """
    Calculates the Sources-fit rate by prompting the user to verify relevance in the terminal.
    """
    print(f"\n[MANUAL EVALUATION] Query: '{query}'")
    relevant_count = 0
    total_chunks = len(retrieved_contexts)
    
    for idx, chunk in enumerate(retrieved_contexts):
        print(f"\n--- Retrieved Match #{idx + 1} ---")
        # Print a short 300-character snippet so you can read it quickly
        print(chunk['text'][:300] + "...\n")
        
        # Pause the script and ask you for judgment
        is_relevant = input("Does this chunk contain the correct regulatory answer? (y/n): ").strip().lower()
        if is_relevant == 'y':
            relevant_count += 1
            
    # Calculate the exact percentage
    if total_chunks > 0:
        sources_fit_rate = (relevant_count / total_chunks) * 100
    else:
        sources_fit_rate = 0.0
        
    return {
        "relevant_chunks": relevant_count,
        "total_chunks": total_chunks,
        "sources_fit_rate_percent": round(sources_fit_rate, 2)
    }

def retrieve_context(query, top_k=3):
    # --- START LATENCY STOPWATCH ---
    start_time = time.perf_counter()

    db_path = "./chroma_db"
    parent_store_path = "parent_document_store.json"

    # 1. Initialize the embedding model
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # 2. Connect to ChromaDB
    chroma_client = chromadb.PersistentClient(path=db_path)
    try:
        child_collection = chroma_client.get_collection(name="compliance_child_chunks")
    except Exception:
        print("[Error] Could not find the vector database collection.")
        return

    # 3. Load the Parent document mapper
    try:
        with open(parent_store_path, "r") as file:
            parent_document_store = json.load(file)
    except FileNotFoundError:
        print("[Error] Parent document store file missing.")
        return

    print(f"\n[Query] Searching baseline database for: '{query}'")

    # 4. Search the database
    results = child_collection.query(
        query_texts=[query],
        n_results=top_k
    )

    # 5. Fetch the Parent contexts
    metadatas = results['metadatas'][0] if results['metadatas'] else []
    seen_parents = set()
    retrieved_contexts = []

    for meta in metadatas:
        parent_id = meta.get("parent_id")
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

    # 6. Run the Interactive Sources-Fit Grader
    fit_metrics = calculate_sources_fit_rate(query, retrieved_contexts)

    # 7. Calculate automated metrics
    metrics = evaluate_retrieval_performance(retrieved_contexts)
    
    # 8. Print the Final Dashboard
    print("\n=== SYSTEM PERFORMANCE METRICS ===")
    print(f"Latency per query: {latency_ms:.2f} ms")
    print(f"Tokens per query: {metrics['tokens_per_query']} tokens")
    print(f"Cost per 1,000 queries: ${metrics['cost_per_1k_queries']}")
    print(f"Sources-fit rate: {fit_metrics['sources_fit_rate_percent']}% ({fit_metrics['relevant_chunks']}/{fit_metrics['total_chunks']} chunks relevant)")
    print("==================================\n")

    return retrieved_contexts

if __name__ == "__main__":
    # Test your baseline pipeline with a specific question you know the answer to
    sample_query = "What are the rules regarding risk management framework and ICT compliance?"
    retrieve_context(sample_query, top_k=3)